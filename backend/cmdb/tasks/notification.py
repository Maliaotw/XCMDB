"""通知相關任務 - 電子郵件與 Webhook"""

import time

import requests
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .base import BaseTask, get_task_logger

logger = get_task_logger("notification")


@shared_task(name="tasks.notification.send_email", bind=True, max_retries=3, base=BaseTask)
def send_email(self, to, subject, message, html_message=None, from_email=None):
    """同步發送電子郵件
    
    Args:
        to: 收件人列表
        subject: 郵件主旨
        message: 純文字內容
        html_message: HTML 內容 (選填)
        from_email: 寄件者 (選填，預設使用 settings.DEFAULT_FROM_EMAIL)
    
    Returns:
        dict: 發送結果
    """
    try:
        recipient_list = to if isinstance(to, list) else [to]
        from_email = from_email or settings.DEFAULT_FROM_EMAIL

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )

        logger.info(f"郵件發送成功: {subject} -> {recipient_list}")
        return {"status": 200, "data": f"郵件發送成功: {subject}"}

    except Exception as exc:
        try:
            raise self.retry(exc=exc, countdown=2 ** self.request.retries)
        except Exception:
            logger.error(f"郵件發送失敗 (已達到最大重試次數): {subject} -> {exc}")
            return {"status": 500, "data": f"郵件發送失敗: {str(exc)}"}


@shared_task(name="tasks.notification.render_email_template", bind=True, max_retries=2, base=BaseTask)
def render_email_template(self, template_name, context, to, subject, from_email=None):
    """使用 Django 模板渲染後發送電子郵件
    
    Args:
        template_name: 模板名稱 (例如 "emails/welcome.html")
        context: 模板上下文字典
        to: 收件人列表
        subject: 郵件主旨
        from_email: 寄件者 (選填)
    
    Returns:
        dict: 發送結果
    """
    try:
        html_content = render_to_string(template_name, context)
        text_content = html_content.replace("<br>", "\n").replace("<p>", "").replace("</p>", "")
        from_email = from_email or settings.DEFAULT_FROM_EMAIL

        send_mail(
            subject=subject,
            message=text_content,
            from_email=from_email,
            recipient_list=to if isinstance(to, list) else [to],
            html_message=html_content,
            fail_silently=False,
        )

        logger.info(f"模板郵件發送成功: {template_name} -> {subject}")
        return {"status": 200, "data": f"模板郵件發送成功: {template_name}"}

    except Exception as exc:
        try:
            raise self.retry(exc=exc, countdown=2 ** self.request.retries)
        except Exception:
            logger.error(f"模板郵件發送失敗: {template_name} -> {exc}")
            return {"status": 500, "data": f"模板郵件發送失敗: {str(exc)}"}


@shared_task(name="tasks.notification.send_webhook", bind=True, max_retries=3, base=BaseTask)
def send_webhook(self, url, payload=None, method="POST", headers=None):
    """發送 Webhook 通知
    
    Args:
        url: Webhook URL
        payload: 請求主體 (預設為 JSON)
        method: HTTP 方法 (GET/POST/PATCH)
        headers: 自訂請求標頭
    
    Returns:
        dict: 發送結果
    """
    try:
        payload = payload or {}
        headers = headers or {}

        timeout = 10

        if method.upper() == "GET":
            response = requests.get(url, params=payload, headers=headers, timeout=timeout)
        elif method.upper() == "PATCH":
            response = requests.patch(url, json=payload, headers=headers, timeout=timeout)
        else:
            response = requests.post(url, json=payload, headers=headers, timeout=timeout)

        response.raise_for_status()
        logger.info(f"Webhook 發送成功: {url} (狀態碼: {response.status_code})")
        return {
            "status": 200,
            "data": f"Webhook 發送成功: {url}",
            "response_code": response.status_code,
        }

    except requests.exceptions.ConnectionError as exc:
        try:
            raise self.retry(exc=exc, countdown=5)
        except Exception:
            logger.error(f"Webhook 發送失敗 (連接錯誤): {url}")
            return {"status": 500, "data": f"Webhook 發送失敗 (連接錯誤): {url}"}

    except requests.exceptions.Timeout as exc:
        try:
            raise self.retry(exc=exc, countdown=10)
        except Exception:
            logger.error(f"Webhook 發送失敗 (逾時): {url}")
            return {"status": 504, "data": f"Webhook 發送失敗 (逾時): {url}"}

    except requests.exceptions.HTTPError as exc:
        logger.error(f"Webhook HTTP 錯誤: {url} - {exc.response.status_code} {exc.response.text}")
        return {
            "status": exc.response.status_code,
            "data": f"Webhook HTTP 錯誤: {exc.response.status_code}",
            "response": exc.response.text,
        }

    except Exception as exc:
        try:
            raise self.retry(exc=exc, countdown=2 ** self.request.retries)
        except Exception:
            logger.error(f"Webhook 發送失敗: {url} - {exc}")
            return {"status": 500, "data": f"Webhook 發送失敗: {str(exc)}"}


@shared_task(name="tasks.notification.send_email_batch", base=BaseTask)
def send_email_batch(emails, subject, message, html_message=None, from_email=None, chunk_size=50):
    """批次發送電子郵件
    
    Args:
        emails: 收件人地址列表
        subject: 郵件主旨
        message: 純文字內容
        html_message: HTML 內容 (選填)
        from_email: 寄件者 (選填)
        chunk_size: 每批次發送數量 (預設 50)
    
    Returns:
        dict: 發送結果摘要
    """
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    total = len(emails)
    success = 0
    failed = 0
    errors = []

    for i in range(0, total, chunk_size):
        chunk = emails[i:i + chunk_size]
        for recipient in chunk:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=[recipient],
                    html_message=html_message,
                    fail_silently=False,
                )
                success += 1
            except Exception as e:
                failed += 1
                errors.append(f"{recipient}: {str(e)}")
                logger.warning(f"批次郵件發送失敗: {recipient} - {e}")

        time.sleep(0.5)  # 避免觸發速率限制

    result = {
        "status": 200,
        "data": {
            "total": total,
            "success": success,
            "failed": failed,
            "errors": errors[:10],  # 最多回傳 10 筆錯誤
        },
    }

    logger.info(f"批次郵件完成: 總計 {total}, 成功 {success}, 失敗 {failed}")
    return result
