from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserProfile(AbstractUser):
    """
    繼承AbstractUser進行擴展

    for i in range(1,101):
        user = models.UserProfile(username='user%s' % i, email='user%s@gmail.com' % i)
        user.set_password('123456')
        user.save()
    """

    class Meta:
        verbose_name = '用戶'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username



