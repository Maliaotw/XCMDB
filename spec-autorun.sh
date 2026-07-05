#!/usr/bin/env bash
# =============================================================
# spec-autorun.sh
# 迭代式「規劃」循環（不寫代碼）：同一個 opencode session 內
#
#   [research] 理解需求 → 探索代碼庫 → 搜尋外部資料 →
#              架構設計 / 方案比較 → 撰寫或修訂 spec 文件
#   [review]   質疑式審查：需求覆蓋？假設成立？風險？更優方案？
#              → 列出必須修訂的點，安排下一輪分析重點
#   → 回到 [research]，反覆「分析→審查→再分析→再審查」
#   直到審查者輸出 SPEC_READY 且 spec 三件套齊備
#
# 產出：specs/NNN-slug/{spec.md, plan.md, tasks.md, research-notes.md}
# 之後用 speckit-autorun.sh 執行實作。
#
# 用法：
#   ./spec-autorun.sh <slug> "需求描述"   # 開新規劃，自動編號 specs/NNN-slug
#   ./spec-autorun.sh                     # 接續上次的規劃 session
#
# 環境變數：
#   RESEARCH_AGENT=research  研究 agent（需可寫檔 + webfetch）
#   REVIEW_AGENT=review      審查 agent
#   MIN_ROUNDS=2             至少迭代輪數（強制真的來回打磨，不許一輪過）
#   MAX_ROUNDS / RUN_TIMEOUT / RUN_ATTEMPTS / LOG_DIR
#
# 注意：bash 3.2 下變數一律 ${var}，嚴禁 $var 緊接全形標點
# =============================================================
set -uo pipefail

RESEARCH_AGENT="${RESEARCH_AGENT:-research}"
REVIEW_AGENT="${REVIEW_AGENT:-review}"
MIN_ROUNDS="${MIN_ROUNDS:-2}"
MAX_ROUNDS="${MAX_ROUNDS:-15}"
RUN_TIMEOUT="${RUN_TIMEOUT:-3600}"
RUN_ATTEMPTS="${RUN_ATTEMPTS:-2}"
SPECS_ROOT="${SPECS_ROOT:-specs}"
LOG_DIR="${LOG_DIR:-.autorun-logs}"
STATE_FILE="${STATE_FILE:-${LOG_DIR}/spec-autorun.state}"
mkdir -p "$LOG_DIR"

# 範圍紀律：兩個 agent 每輪 prompt 都會帶上，防止規劃發散/鍍金
SCOPE_RULES="$(cat <<'EOF'
範圍紀律（必須遵守）：
- 規模與需求相稱：這是既有專案的一個 feature 規劃，不要發明需求之外的
  企業級要求（rate limiting、CDN 後備、多環境部署、SLA 等）。
- 文件精簡可執行：spec.md 與 plan.md 各控制在 300 行內，tasks.md 控制在
  50 項任務內；超出就先裁剪，砍掉的內容在 backlog 用一句話帶過即可。
- 「必須修訂」的唯一標準：會導致實作失敗，或明顯的需求缺口。
  風格問題、完備性潔癖、錦上添花一律不擋路，記入 backlog。
EOF
)"

log() { echo "[$(date '+%F %T')] $*" | tee -a "${LOG_DIR}/spec-autorun.log"; }

oc_run() {  # $1=日誌檔，其餘為 opencode run 參數；帶超時與重試
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

spec_fingerprint() {  # spec 目錄所有 md 檔的內容指紋
  cat "$1"/*.md 2>/dev/null | { md5 -q /dev/stdin 2>/dev/null || md5sum | cut -d' ' -f1; }
}

spec_complete() {     # 三件套齊備且 tasks.md 至少有一個未勾選任務
  [ -s "$1/spec.md" ] && [ -s "$1/plan.md" ] && [ -s "$1/tasks.md" ] || return 1
  grep -qE '^\s*[-*] \[ \]' "$1/tasks.md"
}

# ---- 解析參數 ----
SID="" SPEC_DIR="" REQ=""
if [ -n "${1:-}" ]; then
  slug="$1"; shift; REQ="$*"   # slug 後所有參數合併為需求，容忍未加引號
  [ -n "$REQ" ] || { echo "開新規劃需要需求描述"; exit 2; }
  # 自動編號：現有最大 NNN + 1
  last=$(ls -d "${SPECS_ROOT}"/[0-9][0-9][0-9]-*/ 2>/dev/null | sed 's|.*/\([0-9]\{3\}\)-.*|\1|' | sort -n | tail -1)
  next=$(printf '%03d' $(( ${last:-0} + 1 )) )
  SPEC_DIR="${SPECS_ROOT}/${next}-${slug}"
  mkdir -p "$SPEC_DIR"
else
  [ -f "$STATE_FILE" ] || { echo "沒有進行中的規劃，用法：$0 <slug> \"需求描述\""; exit 2; }
  SID=$(sed -n 1p "$STATE_FILE"); SPEC_DIR=$(sed -n 2p "$STATE_FILE")
  log "接續規劃 session ${SID}（${SPEC_DIR}）"
fi

# ---- 首輪：research 開新 session ----
round=1
skip_research=0
if [ -z "$SID" ]; then
  first_log="${LOG_DIR}/spec-$(date +%s).r1-research.json"
  log "開新規劃：${SPEC_DIR}"
  oc_run "$first_log" --format json --agent "$RESEARCH_AGENT" "$(cat <<EOF
需求：${REQ}

這是一個迭代式規劃任務，本輪先做：
1. 理解需求：邊界、使用者、成功標準；不清楚的地方列出你的假設。
2. 探索本代碼庫，弄清楚現況與可複用的部分。
3. 需要外部知識時，搜尋官方文件/最佳實踐（webfetch），把來源記下來。
4. 給出 2-3 個備選架構方案，比較取捨，選定一個並說明理由。
5. 把以上產出寫入 ${SPEC_DIR}/research-notes.md 與 ${SPEC_DIR}/spec.md 初稿。
先不用寫 plan.md 和 tasks.md，等審查意見後再逐步完善。不要寫任何實作代碼。

${SCOPE_RULES}
EOF
)" || { log "首輪研究失敗，見 ${first_log}"; exit 1; }
  SID=$(grep -o '"sessionID":"[^"]*"' "$first_log" | head -1 | cut -d'"' -f4)
  [ -n "$SID" ] || { log "!! 無法擷取 session id"; exit 1; }
  printf '%s\n%s\n' "$SID" "$SPEC_DIR" > "$STATE_FILE"
  log "session id = ${SID}（已存入 ${STATE_FILE}）"
  skip_research=1   # 首輪研究已做，直接進審查
fi

# ---- 分析↔審查 循環 ----
last_fp=""
while [ "$round" -le "$MAX_ROUNDS" ]; do
  ts=$(date +%s)

  # ---- [research] 按審查意見修訂與深入 ----
  if [ "${skip_research}" != "1" ]; then
    r_log="${LOG_DIR}/spec-${ts}.r${round}-research.log"
    log "第 ${round} 輪 [${RESEARCH_AGENT}] 分析/修訂"
    oc_run "$r_log" -s "$SID" --agent "$RESEARCH_AGENT" "$(cat <<EOF
按照剛才審查者列出的修訂點與分析重點，逐條處理：
- 需要補研究的就去探索代碼庫或搜尋資料，把證據寫進 ${SPEC_DIR}/research-notes.md。
- 修訂 ${SPEC_DIR}/spec.md；方案穩定後撰寫/完善 ${SPEC_DIR}/plan.md（分階段）
  與 ${SPEC_DIR}/tasks.md（- [ ] 任務清單，含編號與驗收標準，格式與其他 spec 一致）。
不要寫任何實作代碼。大段修改時優先重寫整個檔案（write），少用局部編輯（edit）。

${SCOPE_RULES}
EOF
)" || { log "分析失敗，見 ${r_log}"; exit 1; }
  fi
  skip_research=0

  # ---- [review] 質疑式審查 ----
  v_log="${LOG_DIR}/spec-${ts}.r${round}-review.log"
  log "第 ${round} 輪 [${REVIEW_AGENT}] 審查"
  oc_run "$v_log" -s "$SID" --agent "$REVIEW_AGENT" "$(cat <<EOF
以懷疑的眼光審查 ${SPEC_DIR}/ 下的規劃文件（這是第 ${round} 輪審查）：
1. 需求覆蓋完整嗎？有沒有沒問過的關鍵問題、沒考慮的邊界情況？
2. 技術假設站得住腳嗎？research-notes.md 裡的證據支撐結論嗎？
3. 風險：哪裡最可能失敗？有沒有更簡單的方案被忽略了？
4. plan.md 的階段劃分合理嗎？tasks.md 每項任務清晰、可執行、有驗收標準嗎？
把「必須修訂的點」和「下一輪分析重點」具體列出來，把審查結論追加到
${SPEC_DIR}/review-log.md。

${SCOPE_RULES}

只有當存在「會導致實作失敗或明顯需求缺口」的問題時才擋路；否則就是成熟，
在回覆最後單獨輸出一行（行首開始，禁止加 #、*、✅ 等任何裝飾）：
SPEC_READY
EOF
)" || { log "審查失敗，見 ${v_log}"; exit 1; }

  # ---- 完成判定：SPEC_READY + 三件套齊備 + 最少輪數 ----
  if grep -qE '^[[:space:]#*>✅-]*SPEC_READY' "$v_log"; then
    if [ "$round" -lt "$MIN_ROUNDS" ]; then
      log "審查者輸出 SPEC_READY，但未達最少 ${MIN_ROUNDS} 輪打磨，繼續"
    elif ! spec_complete "$SPEC_DIR"; then
      log "!! 審查者輸出 SPEC_READY 但三件套不齊/tasks.md 無任務，不採信"
    else
      log "=== 規劃完成：${SPEC_DIR}（第 ${round} 輪，session ${SID}）==="
      log "下一步：git add 後用 speckit-autorun.sh 執行實作"
      exit 0
    fi
  fi

  # ---- 停滯偵測：spec 文件連續兩輪毫無變化 → 空轉 ----
  fp=$(spec_fingerprint "$SPEC_DIR")
  if [ "$fp" = "$last_fp" ]; then
    log "!! 連續兩輪 spec 文件無任何變化，停止（人工檢查 session ${SID}）"
    exit 1
  fi
  last_fp="$fp"
  round=$((round+1))
done

log "!! 達到最大輪數 ${MAX_ROUNDS}，停止（session ${SID} 可手動接續）"
exit 1
