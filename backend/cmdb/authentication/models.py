# Create your models here.
from django.utils import timezone
from rest_framework.authtoken.models import Token
import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.conf import settings
from .settings import token_settings
from django.db.models import Q

# Create your models here.
class UserLoginLog(models.Model):
    LOGIN_TYPE_CHOICE = (
        ('W', 'Web'),
        ('T', 'Terminal'),
    )

    REASON_NOTHING = 0
    REASON_PASSWORD = 1
    REASON_MFA = 2
    REASON_NOT_EXIST = 3
    REASON_PASSWORD_EXPIRED = 4

    REASON_CHOICE = (
        (REASON_NOTHING, _('-')),
        (REASON_PASSWORD, _('用户名/密码 校验失败')),
        (REASON_MFA, _('MFA authentication failed')),
        (REASON_NOT_EXIST, _("用户名不存在")),
        (REASON_PASSWORD_EXPIRED, _("密碼已過期")),
    )

    STATUS_CHOICE = (
        (True, _('成功')),
        (False, _('失敗'))
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    username = models.CharField(max_length=128, verbose_name=_('Username'))
    type = models.CharField(choices=LOGIN_TYPE_CHOICE, max_length=2, verbose_name=_('Login type'),default='W')
    ip = models.GenericIPAddressField(verbose_name=_('Login ip'))
    city = models.CharField(max_length=254, blank=True, null=True, verbose_name=_('Login city'))
    user_agent = models.CharField(max_length=254, blank=True, null=True, verbose_name=_('User agent'))
    reason = models.SmallIntegerField(default=0, choices=REASON_CHOICE, verbose_name=_('Reason'))
    status = models.BooleanField(max_length=2, default=True, choices=STATUS_CHOICE, verbose_name=_('Status'))
    datetime = models.DateTimeField(default=timezone.now, verbose_name=_('Date login'))

    @classmethod
    def get_login_logs(cls, date_form=None, date_to=None, user=None, keyword=None):
        login_logs = cls.objects.all()
        if date_form and date_to:
            login_logs = login_logs.filter(
                datetime__gt=date_form, datetime__lt=date_to
            )
        if user:
            login_logs = login_logs.filter(username=user)
        if keyword:
            login_logs = login_logs.filter(
                Q(ip__contains=keyword) |
                Q(city__contains=keyword) |
                Q(username__contains=keyword)
            )
        return login_logs

    class Meta:
        ordering = ['-datetime', 'username']


class ExpiringToken(Token):

    """Extend Token to add an expired method."""

    class Meta(object):
        proxy = True

    def expired(self):
        """Return boolean indicating token expiration."""
        now = timezone.now()
        if self.created < now - token_settings.EXPIRING_TOKEN_LIFESPAN:
            return True
        return False



class AccessKey(models.Model):
    id = models.UUIDField(verbose_name='AccessKeyID', primary_key=True,default=uuid.uuid4, editable=False)
    secret = models.UUIDField(verbose_name='AccessKeySecret',default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User',on_delete=models.CASCADE, related_name='access_keys')
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    date_created = models.DateTimeField(auto_now_add=True)

    def get_id(self):
        return str(self.id)

    def get_secret(self):
        return str(self.secret)

    def get_full_value(self):
        return '{}:{}'.format(self.id, self.secret)

    def __str__(self):
        return str(self.id)

