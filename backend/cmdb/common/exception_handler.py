"""
統一 API 錯誤處理模組

將所有 DRF 與 Django 異常統一格式化為：
{
    "success": false,
    "code": <http_status_code>,
    "message": "<human readable error message>",
    "data": null
}
"""

import logging

from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
    ValidationError,
)
from rest_framework.exceptions import (
    PermissionDenied as DRFPermissionDenied,
)
from rest_framework.views import exception_handler

logger = logging.getLogger("common.exception_handler")


def _flatten_validation_errors(detail):
    """
    將 ValidationError 的 detail (dict / list / str) 扁平化為
    一段可讀的錯誤訊息字串。

    Examples
    --------
    {"username": ["此欄位為必填。"], "email": ["格式錯誤。"]}
    -> "username: 此欄位為必填。; email: 格式錯誤。"

    ["此欄位為必填。"]
    -> "此欄位為必填。"
    """
    if isinstance(detail, dict):
        parts = []
        for field, messages in detail.items():
            if isinstance(messages, list):
                msg_text = ", ".join([str(m) for m in messages])
            else:
                msg_text = str(messages)
            # non_field_errors 不帶欄位前綴
            if field == "non_field_errors":
                parts.append(msg_text)
            else:
                parts.append(f"{field}: {msg_text}")
        return "; ".join(parts)

    if isinstance(detail, list):
        return ", ".join([str(m) for m in detail])

    return str(detail)


def _build_error_response(response, message):
    """
    統一替換 response.data 為標準格式。
    """
    response.data = {
        "success": False,
        "code": response.status_code,
        "message": message,
        "data": None,
    }
    return response


def custom_exception_handler(exc, context):
    """
    自訂 DRF Exception Handler。

    處理流程：
    1. 先交給 DRF 預設 handler 處理 (涵蓋所有 APIException 子類)。
    2. 若 DRF 未處理 (返回 None)，額外捕捉 Django Http404 / PermissionDenied。
    3. 對 ValidationError 做特殊的欄位錯誤拼接。
    4. 5xx 錯誤寫 ERROR log。
    """
    # Step 1: DRF 預設處理
    response = exception_handler(exc, context)

    # Step 2: DRF 未處理的 Django 原生異常
    if response is None:
        if isinstance(exc, Http404):
            response = _create_api_response(status.HTTP_404_NOT_FOUND, "找不到請求的資源。")
        elif isinstance(exc, DjangoPermissionDenied):
            response = _create_api_response(status.HTTP_403_FORBIDDEN, "您沒有執行此操作的權限。")
        else:
            # 未預期的例外 – 記錄完整 traceback 並回傳 500
            logger.exception(
                "[API 500] 未處理的伺服器錯誤: %s",
                exc,
            )
            response = _create_api_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "伺服器內部錯誤，請稍後再試。")
        return response

    # Step 3: 決定 message
    if isinstance(exc, ValidationError):
        message = _flatten_validation_errors(response.data)
    elif isinstance(exc, NotAuthenticated):
        message = "身份驗證憑證未提供或已失效。"
    elif isinstance(exc, AuthenticationFailed):
        message = "身份驗證失敗。"
    elif isinstance(exc, (DRFPermissionDenied, DjangoPermissionDenied)):
        message = "您沒有執行此操作的權限。"
    elif isinstance(exc, APIException):
        # 其餘 DRF 異常，直接使用 detail
        detail = exc.detail
        if isinstance(detail, (list, dict)):
            message = _flatten_validation_errors(detail)
        else:
            message = str(detail)
    else:
        message = "發生未知錯誤。"

    # Step 4: 5xx 錯誤寫 log
    if response.status_code >= 500:
        view = context.get("view", None)
        logger.error(
            "[API %d] %s | view=%s | exc=%s",
            response.status_code,
            context.get("request", {}).method if hasattr(context.get("request", {}), "method") else "N/A",
            getattr(view, "__class__", "").__name__ if view else "N/A",
            exc,
        )

    return _build_error_response(response, message)


def _create_api_response(status_code, message):
    """
    從零建立一個 DRF Response（用於 DRF 預設 handler 不處理的情境）。
    """
    from rest_framework.response import Response

    return Response(
        {
            "success": False,
            "code": status_code,
            "message": message,
            "data": None,
        },
        status=status_code,
    )
