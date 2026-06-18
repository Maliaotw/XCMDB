"""Celery 基礎 Task - 統一錯誤處理、重試、日誌"""

import logging
import traceback

from celery import Task


class BaseTask(Task):
    """所有 Celery 任務的基底類別"""

    autoretry_for = (Exception,)
    retry_backoff = True
    retry_backoff_max = 600
    retry_kwargs = {"max_retries": 3}
    ack_late = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 允許透過 init 覆蓋預設值
        for key, value in self.retry_kwargs.items():
            if key not in ["max_retries"]:
                setattr(self, key, value)

    def on_success(self, retval, task_id, args, kwargs):
        logger = logging.getLogger(f"tasks.{self.name}")
        logger.info(f"[Task Done] {self.name} ({task_id}): success")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger = logging.getLogger(f"tasks.{self.name}")
        error_detail = self._format_error(exc)
        logger.error(f"[Task Failed] {self.name} ({task_id}): {error_detail}")

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger = logging.getLogger(f"tasks.{self.name}")
        logger.warning(f"[Task Retry] {self.name} ({task_id}): {type(exc).__name__} - {exc}")

    @staticmethod
    def _format_error(exc):
        tb = traceback.format_exception(type(exc), exc, exc.__traceback__)
        return "".join(tb[-3:])


def get_task_logger(name):
    """取得帶有任務資訊的 logger"""
    return logging.getLogger(f"tasks.{name}")
