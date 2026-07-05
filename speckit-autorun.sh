#!/usr/bin/env bash
# =============================================================
# speckit-autorun.sh (v2)
# 無人值守跑完 specs/ 下所有 feature（001, 002, 003...）
#
# 流程（每個 spec）：
#   loop:
#     [新 session] build agent 執行 tasks.md 當前階段
#     [測試關卡]   跑 TEST_CMD，結果餵給 plan（客觀驗證）
#     [同 session] plan agent 審查；緊急問題改計畫，
#                  非緊急記入 backlog.md，安排下一階段
#   直到 tasks.md 沒有未勾選項「且」出現 ALL_DONE
#
# v2 修復：
#   - 完成判定雙重確認：ALL_DONE 且未勾選數為 0
#   - build 後強制跑測試，結果（含失敗輸出）餵給 plan 審查
#   - 分支不存在時自動建立，避免直接寫 main
#   - plan 用 --session <id> 顯式接 build 的 session（取不到才退回 -c）
#   - opencode run 帶重試與單輪超時（macOS 無 timeout，用 perl alarm）
#   - 停滯偵測改用 git HEAD + tasks.md 指紋，且不跨 spec 殘留
#   - unchecked_count 修正 grep -c 無匹配時的雙行輸出
#
# 前提：
#   - opencode 權限已設 allow（在可拋棄 branch/worktree 跑）
#   - agent plan/build 已綁定各自模型（全域或專案 opencode 設定）
#   - spec-kit 已生成 specs/NNN-xxx/{spec,plan,tasks}.md
# =============================================================
set -uo pipefail

SPECS_DIR="${SPECS_DIR:-specs}"
MAX_PHASES_PER_SPEC="${MAX_PHASES_PER_SPEC:-30}"   # 單個 spec 最大迭代數（保險絲）
LOG_DIR="${LOG_DIR:-.autorun-logs}"
CHECKOUT_BRANCH="${CHECKOUT_BRANCH:-1}"            # spec-kit 每個 feature 一個同名分支；設 0 停用
# 客觀驗證關卡；設空字串停用。
# macOS 上 pip 裝的 pyzbar 運行時按庫名 dlopen zbar，但 dyld 預設不搜
# Homebrew 目錄，需借 DYLD_LIBRARY_PATH 指路；只在對應目錄真的存在
# libzbar 時才加前綴（Apple Silicon 與 Intel 路徑不同），Linux 不需要。
ZBAR_PREFIX=""
if [ "$(uname -s)" = "Darwin" ]; then
  for _d in /opt/homebrew/lib /usr/local/lib; do
    [ -e "${_d}/libzbar.dylib" ] && { ZBAR_PREFIX="DYLD_LIBRARY_PATH=${_d} "; break; }
  done
fi
TEST_CMD="${TEST_CMD:-${ZBAR_PREFIX}uv run pytest -q}"
RUN_TIMEOUT="${RUN_TIMEOUT:-3600}"                 # 單次 opencode run 超時（秒）
RUN_ATTEMPTS="${RUN_ATTEMPTS:-2}"                  # 單次 opencode run 最多嘗試次數
REVIEW_AGENT="${REVIEW_AGENT:-review}"             # 審查 agent（需有檔案寫入權限，見 opencode.json）
mkdir -p "$LOG_DIR"

log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG_DIR/autorun.log"; }

unchecked_count() {  # 統計 tasks.md 未完成項
  local n
  n=$(grep -cE '^\s*[-*] \[ \]' "$1" 2>/dev/null) || true
  echo "${n:-0}"
}

spec_done() {        # 完成 = ALL_DONE 且未勾選數為 0（不信任單方宣告）
  local tasks="$1"
  grep -qE '^[[:space:]#*>✅-]*ALL_DONE' "$tasks" || return 1
  if [ "$(unchecked_count "$tasks")" != "0" ]; then
    log "!! $tasks 有 ALL_DONE 但仍有未勾選項，視為未完成"
    return 1
  fi
  return 0
}

tasks_fingerprint() { # 停滯偵測用：HEAD + tasks.md 內容指紋
  local tasks="$1" h m
  h=$(git rev-parse HEAD 2>/dev/null) || h=none
  m=$(md5 -q "$tasks" 2>/dev/null) || m=$(md5sum "$tasks" 2>/dev/null | cut -d' ' -f1)
  echo "$h:$m"
}

oc_run() {           # $1=日誌檔，其餘為 opencode run 參數；帶超時與重試
  local logf="$1"; shift
  local attempt rc
  for attempt in $(seq 1 "$RUN_ATTEMPTS"); do
    perl -e 'alarm shift; exec @ARGV' "$RUN_TIMEOUT" opencode run "$@" >>"$logf" 2>&1
    rc=$?
    [ "$rc" -eq 0 ] && return 0
    log "opencode run 失敗（rc=${rc}，第 ${attempt}/${RUN_ATTEMPTS} 次嘗試）"
  done
  return 1
}

run_phase() {        # $1 = spec 目錄
  local dir="$1" name; name="$(basename "$dir")"
  local tasks="$dir/tasks.md"
  local phase_log="$LOG_DIR/${name}-$(date +%s).log"
  local build_log="$phase_log.build.json"

  # ---- 階段內：build 開新 session（json 輸出以便取得 session id）----
  oc_run "$build_log" --format json --agent build "$(cat <<EOF
讀取 $dir/spec.md、$dir/plan.md、$tasks 與 $dir/backlog.md（若存在）。
執行 tasks.md 中「最早的未完成階段」的所有任務。
完成的任務把 - [ ] 改成 - [x]。
只做這一個階段，不要越界。
全部完成後執行 git add -A && git commit -m "feat($name): <階段摘要>"。
EOF
)" || { log "build 失敗，見 $build_log"; return 1; }

  # ---- 取 session id，plan 顯式接同一 session ----
  local sid session_args
  sid=$(grep -o '"sessionID":"[^"]*"' "$build_log" | head -1 | cut -d'"' -f4)
  if [ -n "$sid" ]; then
    session_args=(-s "$sid")
  else
    log "!! 無法從 build 輸出取得 session id，退回 -c（有接錯 session 的風險）"
    session_args=(-c)
  fi

  # ---- 測試關卡：客觀驗證，結果餵給 plan ----
  local test_note="（未配置 TEST_CMD，跳過測試關卡）"
  if [ -n "$TEST_CMD" ]; then
    local test_log="$phase_log.tests"
    if eval "$TEST_CMD" >"$test_log" 2>&1; then
      test_note="測試通過（${TEST_CMD}）：$(tail -1 "$test_log")"
      log "$name 測試通過"
    else
      test_note="測試失敗（${TEST_CMD}）！輸出末尾：
$(tail -30 "$test_log")"
      log "!! ${name} 測試失敗（詳見 ${test_log}），交給 plan 安排修復"
    fi
  fi

  # ---- 階段內：review agent 接同一 session 審查 ----
  # 注意：不能用內建 plan agent，它是唯讀的（Plan Mode），無法寫 tasks/backlog/ALL_DONE
  oc_run "$phase_log" "${session_args[@]}" --agent "$REVIEW_AGENT" "$(cat <<EOF
審查剛才 build 完成的代碼與 $tasks 的勾選狀態。

自動化測試結果：
$test_note

1. 測試失敗，或有緊急/嚴重問題（會阻塞後續階段、破壞已有功能、安全隱患）：
   直接修改 $dir/plan.md 與 $tasks 調整計畫，並在受影響階段加入修復任務。
2. 無緊急問題：把可後續優化的點記入 $dir/backlog.md（沒有就建立）。
3. 確認下一階段任務清晰可執行；必要時細化 tasks.md。
4. 把本次審查結論（3-5 行）追加到 $dir/review-log.md。
只有當 tasks.md 所有項目都已勾選「且」測試通過時，才在 $tasks 末尾追加獨立的一行（行首開始，禁止加 #、*、✅ 等任何裝飾）：ALL_DONE
EOF
)" || { log "plan 審查失敗，見 $phase_log"; return 1; }

  return 0
}

run_spec() {         # $1 = spec 目錄
  local dir="$1" name; name="$(basename "$dir")"
  local tasks="$dir/tasks.md"

  [ -f "$tasks" ] || { log "跳過 ${name}（無 tasks.md）"; return 0; }
  if spec_done "$tasks"; then log "跳過 ${name}（已完成）"; return 0; fi

  # spec-kit 慣例：feature 在同名分支上；不存在就建立，避免直接寫 main
  if [ "$CHECKOUT_BRANCH" = "1" ]; then
    if git rev-parse --verify "$name" >/dev/null 2>&1; then
      git checkout "$name" || { log "切換分支 ${name} 失敗"; return 1; }
    else
      git checkout -b "$name" || { log "建立分支 ${name} 失敗"; return 1; }
      log "已建立並切換到新分支 ${name}"
    fi
  fi

  log "=== 開始 ${name}（未完成任務：$(unchecked_count "$tasks")）==="
  local i=0 last_fp="" fp
  while ! spec_done "$tasks"; do
    i=$((i+1))
    if [ "$i" -gt "$MAX_PHASES_PER_SPEC" ]; then
      log "!! ${name} 達到最大迭代數 ${MAX_PHASES_PER_SPEC}，停止（人工檢查）"
      return 1
    fi
    log "${name} 第 $i 輪（剩 $(unchecked_count "$tasks") 項）"
    run_phase "$dir" || return 1

    # 停滯偵測：一整輪後既無新 commit、tasks.md 也沒變 → 無進展
    fp=$(tasks_fingerprint "$tasks")
    if [ "$fp" = "$last_fp" ]; then
      log "!! ${name} 本輪無任何進展（無新 commit、tasks.md 未變），停止（人工檢查）"
      return 1
    fi
    last_fp="$fp"
  done
  log "=== ${name} 完成 ==="
}

# ---- 主循環：依序跑 001, 002, 003... ----
overall=0
for dir in "$SPECS_DIR"/*/; do
  dir="${dir%/}"
  run_spec "$dir" || { overall=1; log "$dir 未完成，繼續下一個 spec"; }
done

log "全部結束（exit=${overall}）"
exit $overall
