from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class UserProfile(AbstractUser):
    """
    繼承AbstractUser進行擴展

    for i in range(1,101):
        user = models.UserProfile(username='user%s' % i, email='user%s@gmail.com' % i)
        user.set_password('123456')
        user.save()
    """

    role = models.CharField(
        "角色",
        max_length=20,
        default="visitor",
        choices=(("admin", "管理員"), ("operator", "運維工程師"), ("auditor", "安全審計員"), ("visitor", "訪客")),
    )

    class Meta:
        verbose_name = "用戶"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class RolePermission(models.Model):
    role = models.CharField("角色名稱", max_length=50, unique=True)
    menus = models.TextField("菜單權限", default="[]")
    actions = models.TextField("動作權限", default="[]")

    class Meta:
        verbose_name = "角色權限分配表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.role


class OperationLog(models.Model):
    """操作審計日誌"""

    actor_id = models.IntegerField(default=0, verbose_name="操作人ID")
    action = models.CharField(max_length=50, verbose_name="操作類型")
    resource_type = models.CharField(max_length=100, verbose_name="資源類型")
    resource_id = models.CharField(max_length=255, verbose_name="資源ID")
    resource_name = models.CharField(max_length=255, default="", verbose_name="資源名稱")
    old_values = models.TextField(default="{}", verbose_name="舊值")
    new_values = models.TextField(default="{}", verbose_name="新值")
    reason = models.CharField(max_length=255, default="", verbose_name="原因")
    ip = models.GenericIPAddressField(default="", verbose_name="IP")
    user_agent = models.CharField(max_length=255, default="", verbose_name="User Agent")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間")

    class Meta:
        verbose_name = "操作審計日誌"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} {self.resource_type}#{self.resource_id}"
