#!/usr/bin/env bash
# =============================================================
# session-autorun.sh
# 同一個 opencode session 內，雙 agent 乒乓循環直到完成：
#
#   [task]  按照計畫構建當前階段（首輪：先制定分階段計畫再執行第一階段）
#   [測試]  跑 TEST_CMD（可選），結果餵給審查者
#   [plan]  審查代碼：緊急問題 → 立即調整計畫；
#           非緊急 → 記錄後續優化；然後安排下一階段計畫
#   → 回到 [task]，直到審查者單獨輸出一行 ALL_DONE（且測試通過）
#
# 計畫存活在 session 對話上下文中，兩個 agent 都看得到全部歷史。
#
# 用法：
#   ./session-autorun.sh "任務描述"           # 開新 session
#   ./session-autorun.sh ses_xxx              # 接續指定 session
#   ./session-autorun.sh                      # 接續上次記住的 session
#
# 環境變數：
#   BUILD_AGENT=do      構建 agent（需能寫檔/commit）
#   REVIEW_AGENT=review 審查 agent（用內建 plan 也行——完成判定
#                       靠輸出 ALL_DONE 而非寫檔，但它就沒法寫 backlog.md）
#   TEST_CMD=...        客觀驗證命令（強烈建議設置）
#   MAX_ROUNDS / RUN_TIMEOUT / RUN_ATTEMPTS / LOG_DIR
#
# 注意：bash 3.2 下變數一律 ${var}，嚴禁 $var 緊接全形標點
# =============================================================
set -uo pipefail

BUILD_AGENT="${BUILD_AGENT:-do}"
REVIEW_AGENT="${REVIEW_AGENT:-review}"
MAX_ROUNDS="${MAX_ROUNDS:-30}"
RUN_TIMEOUT="${RUN_TIMEOUT:-3600}"
RUN_ATTEMPTS="${RUN_ATTEMPTS:-2}"
TEST_CMD="${TEST_CMD:-}"
LOG_DIR="${LOG_DIR:-.autorun-logs}"
SID_FILE="${SID_FILE:-${LOG_DIR}/session-autorun.sid}"
mkdir -p "$LOG_DIR"

log() { echo "[$(date '+%F %T')] $*" | tee -a "${LOG_DIR}/session-autorun.log"; }

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

# ---- 解析參數 ----
SID="" TASK=""
case "${1:-}" in
  ses_*) SID="$1";;
  "")    [ -f "$SID_FILE" ] && SID="$(cat "$SID_FILE")"
         [ -n "$SID" ] || { echo "沒有記住的 session，請提供任務描述開新 session"; exit 2; };;
  *)     TASK="$1";;
esac

# ---- 首輪（無 session）：task agent 制定計畫並執行第一階段 ----
round=1
if [ -z "$SID" ]; then
  first_log="${LOG_DIR}/session-pp-$(date +%s).r1-build.json"
  log "開新 session：${TASK}"
  oc_run "$first_log" --format json --agent "$BUILD_AGENT" "$(cat <<EOF
任務：${TASK}

先制定一份分階段的實施計畫（直接寫在回覆中），然後執行第一階段的構建。
每個階段做完就停，不要越界。有代碼變更就 git add -A && git commit。
EOF
)" || { log "首輪構建失敗，見 ${first_log}"; exit 1; }
  SID=$(grep -o '"sessionID":"[^"]*"' "$first_log" | head -1 | cut -d'"' -f4)
  [ -n "$SID" ] || { log "!! 無法擷取 session id"; exit 1; }
  echo "$SID" > "$SID_FILE"
  log "session id = ${SID}（已存入 ${SID_FILE}）"
  skip_build=1   # 首輪已經構建過，直接進審查
else
  log "接續 session ${SID}"
  echo "$SID" > "$SID_FILE"
  skip_build=0
fi

# ---- 乒乓循環 ----
last_head=""
while [ "$round" -le "$MAX_ROUNDS" ]; do
  ts=$(date +%s)

  # ---- [task] 構建當前階段（首輪已做過則跳過）----
  if [ "${skip_build}" != "1" ]; then
    build_log="${LOG_DIR}/session-pp-${ts}.r${round}-build.log"
    log "第 ${round} 輪 [${BUILD_AGENT}] 構建"
    oc_run "$build_log" -s "$SID" --agent "$BUILD_AGENT" \
"按照剛才審查者安排的下一階段計畫執行構建。只做這一個階段，不要越界。
有代碼變更就 git add -A && git commit。" \
      || { log "構建失敗，見 ${build_log}"; exit 1; }
  fi
  skip_build=0

  # ---- [測試] 客觀驗證 ----
  tests_ok=1
  test_note="（未配置 TEST_CMD，無自動化驗證）"
  if [ -n "$TEST_CMD" ]; then
    test_log="${LOG_DIR}/session-pp-${ts}.r${round}.tests"
    if eval "$TEST_CMD" >"$test_log" 2>&1; then
      test_note="測試通過：$(tail -1 "$test_log")"
      log "第 ${round} 輪 測試通過"
    else
      tests_ok=0
      test_note="測試失敗！輸出末尾：
$(tail -30 "$test_log")"
      log "!! 第 ${round} 輪 測試失敗（詳見 ${test_log}）"
    fi
  fi

  # ---- [plan] 審查 + 安排下一階段 ----
  review_log="${LOG_DIR}/session-pp-${ts}.r${round}-review.log"
  log "第 ${round} 輪 [${REVIEW_AGENT}] 審查"
  oc_run "$review_log" -s "$SID" --agent "$REVIEW_AGENT" "$(cat <<EOF
審查剛才構建的代碼有沒有問題。

自動化測試結果：
${test_note}

- 有緊急/嚴重問題（測試失敗、阻塞後續、破壞既有功能、安全隱患）：
  立即調整計畫，把修復安排為下一階段的首要工作。
- 沒有緊急問題：把可後續優化的點記錄下來（能寫檔就記入 backlog.md，
  否則直接寫在回覆裡），然後安排下一階段的計畫工作，寫清楚做什麼、驗收標準。
- 只有當整個任務全部完成且測試通過時，才在回覆最後單獨輸出一行
  （行首開始，禁止加 #、*、✅ 等任何裝飾）：
ALL_DONE
EOF
)" || { log "審查失敗，見 ${review_log}"; exit 1; }

  # ---- 完成判定：審查者輸出 ALL_DONE 且（若有測試）本輪測試通過 ----
  if grep -qE '^[[:space:]#*>✅-]*ALL_DONE' "$review_log"; then
    if [ "$tests_ok" = "1" ]; then
      log "=== 全部完成（第 ${round} 輪，session ${SID}）==="
      exit 0
    fi
    log "!! 審查者輸出 ALL_DONE 但本輪測試失敗，不採信，繼續循環"
  fi

  # ---- 停滯偵測：連續兩輪無新 commit → 空轉 ----
  head_now=$(git rev-parse HEAD 2>/dev/null || echo none)
  if [ "$head_now" = "$last_head" ]; then
    log "!! 連續兩輪無新 commit，疑似空轉，停止（人工檢查 session ${SID}）"
    exit 1
  fi
  last_head="$head_now"
  round=$((round+1))
done

log "!! 達到最大輪數 ${MAX_ROUNDS}，停止（session ${SID} 可手動接續）"
exit 1
