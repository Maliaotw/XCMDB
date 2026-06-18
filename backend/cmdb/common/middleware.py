"""
API 請求日誌中間件

記錄每個 API 請求的 method、path、user、status_code 與回應耗時。
- 跳過靜態檔案與健康檢查路徑
- 2xx/3xx → INFO, 4xx → WARNING, 5xx → ERROR

日誌格式範例：
    [API] POST /api/v1/api-token-auth/ | user: admin | 200 | 45ms
"""

import logging
import time

logger = logging.getLogger("common.middleware")

# 不記錄日誌的路徑前綴
SKIP_PATH_PREFIXES = (
    "/static/",
    "/media/",
    "/favicon.ico",
    "/health",
    "/readiness",
)


class RequestLoggingMiddleware:
    """
    Django Middleware – 記錄每一次 HTTP 請求的摘要資訊。

    相容 Django 2.1+ 的 middleware 介面 (callable style)。
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 判斷是否跳過
        if self._should_skip(request.path):
            return self.get_response(request)

        start_time = time.time()

        response = self.get_response(request)

        duration_ms = int((time.time() - start_time) * 1000)

        # 取得使用者名稱
        user = self._get_username(request)
        status_code = response.status_code
        method = request.method
        path = request.get_full_path()

        log_message = f"[API] {method} {path} | user: {user} | {status_code} | {duration_ms}ms"

        # 依據 status_code 分級記錄
        if status_code >= 500:
            logger.error(log_message)
        elif status_code >= 400:
            logger.warning(log_message)
        else:
            logger.info(log_message)

        return response

    @staticmethod
    def _should_skip(path):
        """判斷是否為靜態檔案或健康檢查路徑。"""
        return path.startswith(SKIP_PATH_PREFIXES)

    @staticmethod
    def _get_username(request):
        """
        安全地取得使用者名稱。

        某些認證後端 (例如 Token) 在 middleware 階段
        尚未完成驗證，因此需要檢查 hasattr。
        """
        try:
            if hasattr(request, "user") and request.user and hasattr(request.user, "is_authenticated"):
                if request.user.is_authenticated:
                    return str(request.user)
        except Exception:
            pass
        return "anonymous"
