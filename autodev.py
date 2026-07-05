#!/usr/bin/env python3
"""
autodev.py — 需求進、成品出的一條龍流水線

    ./autodev.py 密碼生成器要支援自訂字元集 還要能批量生成
    ./autodev.py --no-merge "只跑到實作完成,不合併回 main"

    多行需求:引號內直接換行,或用 heredoc 餵 stdin:
    ./autodev.py <<'EOF'
    1. 調整A
    2. 調整B
    3. 調整C
    EOF

流程:
  1. AI 依需求取英文 kebab-case slug(取不到就用時間戳)
  2. ./spec-autorun.sh <slug> "<需求>"   規劃迭代 → specs/NNN-slug/
  3. ./speckit-autorun.sh                實作到 ALL_DONE(含測試關卡)
  4. 合併 feature 分支回 main 並刪除分支(--no-merge 跳過)

需求參數不用加引號:slug 之後的所有參數會自動合併。
中斷後重跑:規劃階段用 ./spec-autorun.sh 續跑;實作階段直接重跑本腳本或
./speckit-autorun.sh(兩者都會從 tasks.md 的勾選狀態接著做)。
"""

import argparse
import datetime
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE_FILE = ROOT / ".autorun-logs" / "spec-autorun.state"
SLUG_MODEL = "vllm-coder/qwen3-coder-next"   # 取 slug 用的模型(小任務)


def die(msg: str, code: int = 1):
    print(f"\n❌ {msg}", file=sys.stderr)
    sys.exit(code)


def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    """執行命令,輸出直通終端(bash 腳本自帶日誌)。"""
    return subprocess.run(cmd, cwd=ROOT, **kw)


def precheck():
    if shutil.which("opencode") is None:
        die("找不到 opencode,請先安裝")
    if sh(["git", "rev-parse", "--git-dir"], capture_output=True).returncode != 0:
        die("不在 git repo 內")
    dirty = subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=ROOT, text=True
    ).strip()
    if dirty:
        die("工作區有未提交變更,請先 commit 或 stash(agent 會 git add -A,"
            "髒工作區的內容會被一起提交):\n" + dirty)


def ai_slug(requirement: str) -> str:
    """讓 AI 取 slug;輸出不合格就退回時間戳。"""
    prompt = (
        "為以下功能需求取一個英文 kebab-case slug(2-4 個單詞,全小寫,"
        "只含 a-z0-9 和連字號)。只輸出 slug 本身,不要任何其他文字:\n"
        f"{requirement[:500]}"
    )
    for attempt in (1, 2):        # 偶發超時見過實例,重試一次再退路
        try:
            out = subprocess.run(
                ["opencode", "run", "-m", SLUG_MODEL, prompt],
                cwd=ROOT, capture_output=True, text=True, timeout=90,
            ).stdout
            # 取輸出中最後一個像 slug 的 token(模型偶爾會囉嗦)
            candidates = re.findall(r"\b[a-z][a-z0-9]*(?:-[a-z0-9]+){1,4}\b", out)
            if candidates:
                return candidates[-1][:40]
        except Exception as e:
            print(f"⚠️  AI 取 slug 第 {attempt} 次失敗({e})")
    print("⚠️  改用時間戳 slug")
    return "feature-" + datetime.datetime.now().strftime("%m%d-%H%M")


def read_spec_dir() -> str:
    """規劃完成後,從 spec-autorun 的 state 檔取得 spec 目錄。"""
    lines = STATE_FILE.read_text().splitlines()
    if len(lines) < 2 or not lines[1].strip():
        die(f"無法從 {STATE_FILE} 取得 spec 目錄")
    return lines[1].strip()


def main():
    ap = argparse.ArgumentParser(description="需求 → 規劃 → 實作 → 合併 一條龍")
    ap.add_argument("requirement", nargs="*",
                    help="功能需求描述(不用加引號;支援多行;留空則讀 stdin)")
    ap.add_argument("--slug", help="手動指定 slug(預設由 AI 決定)")
    ap.add_argument("--no-merge", action="store_true", help="實作完成後不合併回 main")
    ap.add_argument("--dry-run", action="store_true",
                    help="只顯示 AI 取的 slug 與收到的需求,不啟動流水線")
    args = ap.parse_args()
    requirement = " ".join(args.requirement).strip()
    if not requirement and not sys.stdin.isatty():
        requirement = sys.stdin.read().strip()
    if not requirement:
        ap.error("需要需求描述(參數或 stdin)")

    if not args.dry_run:          # dry-run 不動任何東西,免除髒工作區檢查
        precheck()

    # ---- 1. slug ----
    slug = args.slug or ai_slug(requirement)
    print(f"\n📛 slug = {slug}")
    if args.dry_run:
        print(f"\n--- 需求(dry-run,未啟動)---\n{requirement}")
        return

    # ---- 2. 規劃 ----
    print(f"\n🔍 [1/3] 規劃循環:spec-autorun.sh {slug} …")
    if sh(["bash", "spec-autorun.sh", slug, requirement]).returncode != 0:
        die("規劃循環未收斂,人工檢查後可用 ./spec-autorun.sh(無參數)續跑")
    spec_dir = read_spec_dir()
    branch = Path(spec_dir).name
    print(f"\n✅ 規劃完成:{spec_dir}")

    # ---- 3. 實作 ----
    print(f"\n🔨 [2/3] 實作循環:speckit-autorun.sh(分支 {branch})…")
    if sh(["bash", "speckit-autorun.sh"]).returncode != 0:
        die("實作循環未完成,檢查 .autorun-logs/ 後重跑 ./speckit-autorun.sh 可續作")
    print("\n✅ 實作完成(tasks 全勾 + ALL_DONE + 測試通過)")

    # ---- 4. 合併 ----
    if args.no_merge:
        print(f"\n⏭  [3/3] 依 --no-merge 跳過合併,成果在分支 {branch}")
        return
    print(f"\n🔀 [3/3] 合併 {branch} → main …")
    for cmd in (["git", "checkout", "main"],
                ["git", "merge", branch],
                ["git", "branch", "-d", branch]):
        if sh(cmd).returncode != 0:
            die(f"合併步驟失敗:{' '.join(cmd)}(成果安全地留在分支 {branch})")

    print(f"\n🎉 完成:{requirement[:60]}…\n   已合併進 main,spec 見 {spec_dir}/")


if __name__ == "__main__":
    main()
