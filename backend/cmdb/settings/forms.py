# -*- coding: utf-8 -*-
#
import json
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from .models import Setting, settings
from common.fields import (
    FormDictField, FormEncryptCharField, FormEncryptMixin
)


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            value = getattr(settings, name, None)
            if value is None:  # and django_value is None:
                continue

            if value is not None:
                if isinstance(value, dict):
                    value = json.dumps(value)
                initial_value = value
            else:
                initial_value = ''
            field.initial = initial_value

    def save(self, category="default"):
        if not self.is_bound:
            raise ValueError("Form is not bound")

        # db_settings = Setting.objects.all()
        if not self.is_valid():
            raise ValueError(self.errors)

        with transaction.atomic():
            print(self.cleaned_data.items())

            for name, value in self.cleaned_data.items():
                field = self.fields[name]
                print(field)
                if isinstance(field.widget, forms.PasswordInput) and not value:
                    continue
                # if value == getattr(settings, name):
                #     continue

                encrypted = True if isinstance(field, FormEncryptMixin) else False
                try:
                    setting = Setting.objects.get(name=name)
                except Setting.DoesNotExist:
                    setting = Setting()
                setting.name = name
                setting.category = category
                setting.encrypted = encrypted
                setting.cleaned_value = value
                setting.save()


class BasicSettingForm(BaseForm):
    SITE_URL = forms.URLField(
        label=_("Current SITE URL"),
        help_text="eg: http://jumpserver.abc.com:8080"
    )
    USER_GUIDE_URL = forms.URLField(
        label=_("User Guide URL"), required=False,
        help_text=_("User first login update profile done redirect to it")
    )
    EMAIL_SUBJECT_PREFIX = forms.CharField(
        max_length=1024, label=_("Email Subject Prefix"),
        help_text=_("Tips: Some word will be intercept by mail provider")
    )


class EmailSettingForm(BaseForm):
    EMAIL_HOST = forms.CharField(
        max_length=1024, label=_("SMTP host"), initial='smtp.jumpserver.org'
    )
    EMAIL_PORT = forms.CharField(max_length=5, label=_("SMTP port"), initial=25)
    EMAIL_HOST_USER = forms.CharField(
        max_length=128, label=_("SMTP user"), initial='noreply@jumpserver.org'
    )
    EMAIL_HOST_PASSWORD = FormEncryptCharField(
        max_length=1024, label=_("SMTP password"), widget=forms.PasswordInput,
        required=False,
        help_text=_("Tips: Some provider use token except password")
    )
    EMAIL_FROM = forms.CharField(
        max_length=128, label=_("Send user"), initial='', required=False,
        help_text=_(
            "Tips: Send mail account, default SMTP account as the send account"
        )
    )
    EMAIL_USE_SSL = forms.BooleanField(
        label=_("Use SSL"), initial=False, required=False,
        help_text=_("If SMTP port is 465, may be select")
    )
    EMAIL_USE_TLS = forms.BooleanField(
        label=_("Use TLS"), initial=False, required=False,
        help_text=_("If SMTP port is 587, may be select")
    )


class LDAPSettingForm(BaseForm):
    AUTH_LDAP_SERVER_URI = forms.CharField(
        label=_("LDAP server"),
    )
    AUTH_LDAP_BIND_DN = forms.CharField(
        required=False, label=_("Bind DN"),
    )
    AUTH_LDAP_BIND_PASSWORD = FormEncryptCharField(
        label=_("Password"),
        widget=forms.PasswordInput, required=False
    )
    AUTH_LDAP_SEARCH_OU = forms.CharField(
        label=_("User OU"),
        help_text=_("Use | split User OUs"),
        required=False,
    )
    AUTH_LDAP_SEARCH_FILTER = forms.CharField(
        label=_("User search filter"),
        help_text=_("Choice may be (cn|uid|sAMAccountName)=%(user)s)")
    )
    AUTH_LDAP_USER_ATTR_MAP = FormDictField(
        label=_("User attr map"),
        help_text=_(
            "User attr map present how to map LDAP user attr to jumpserver, "
            "username,name,email is jumpserver attr"
        ),
    )
    # AUTH_LDAP_GROUP_SEARCH_OU = CONFIG.AUTH_LDAP_GROUP_SEARCH_OU
    # AUTH_LDAP_GROUP_SEARCH_FILTER = CONFIG.AUTH_LDAP_GROUP_SEARCH_FILTER
    # AUTH_LDAP_START_TLS = forms.BooleanField(
    #     label=_("Use SSL"), required=False
    # )
    AUTH_LDAP = forms.BooleanField(label=_("Enable LDAP auth"), required=False)




class EmailContentSettingForm(BaseForm):
    EMAIL_CUSTOM_USER_CREATED_SUBJECT = forms.CharField(
        max_length=1024,  required=False, label=_("Create user email subject"),
        help_text=_("Tips: When creating a user, send the subject of the email"
                    " (eg:Create account successfully)")
    )
    EMAIL_CUSTOM_USER_CREATED_HONORIFIC = forms.CharField(
        max_length=1024, required=False, label=_("Create user honorific"),
        help_text=_("Tips: When creating a user, send the honorific of the "
                    "email (eg:Hello)")
    )
    EMAIL_CUSTOM_USER_CREATED_BODY = forms.CharField(
        max_length=4096, required=False, widget=forms.Textarea(),
        label=_('Create user email content'),
        help_text=_('Tips:When creating a user, send the content of the email')
    )
    EMAIL_CUSTOM_USER_CREATED_SIGNATURE = forms.CharField(
        max_length=512, required=False, label=_("Signature"),
        help_text=_("Tips: Email signature (eg:jumpserver)")
    )


