import time
import uuid

from django.utils.translation import gettext as _
from rest_framework import HTTP_HEADER_ENCODING, authentication, exceptions, permissions
from six import string_types

from authentication.models import AccessKey
from common.utils import get_object_or_none, http_to_unixtime, make_signature


def get_request_date_header(request):
    date = request.META.get("HTTP_DATE", b"")
    if isinstance(date, string_types):
        # Work around django test client oddness
        date = date.encode(HTTP_HEADER_ENCODING)
    return date


class MyToken(authentication.TokenAuthentication):
    token = "HJHzo3YzElgZG2YtoBs62YMpYwguW0C8b8LJYJzcs"

    def authenticate_credentials(self, key):
        if self.token == key:
            return ("my_api", key)
        else:
            raise exceptions.AuthenticationFailed(_("Invalid token."))


class WithBootstrapToken(permissions.BasePermission):
    token = "HJHzo3YzElgZG2YtoBs62YMpYwguW0C8b8LJYJzc"

    def has_permission(self, request, view):
        authorization = request.META.get("HTTP_AUTHORIZATION", "")
        # print(authentication)
        if not authorization:
            return False
        request_bootstrap_token = authorization.split()[-1]
        return self.token == request_bootstrap_token


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    基於用戶角色 (UserProfile.role) 的精確權限控制：
    - admin / superuser / staff: 擁有所有權限（GET, POST, PUT, PATCH, DELETE）。
    - operator: 擁有查看、創建、修改權限，但不可刪除（不可執行 DELETE）。
    - auditor / visitor: 僅有唯讀權限（SAFE_METHODS）。
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        # 如果是超級用戶或員工，直接放行所有操作
        if request.user.is_superuser or request.user.is_staff:
            return True

        # 取得用戶角色，預設為 visitor
        role = getattr(request.user, "role", "visitor")

        # admin 有所有權限
        if role == "admin":
            return True

        # operator 允許唯讀以及創建、修改（不可刪除）
        if role == "operator":
            return request.method in permissions.SAFE_METHODS or request.method in ["POST", "PUT", "PATCH"]

        # 其餘角色（auditor, visitor）僅允許唯讀
        return request.method in permissions.SAFE_METHODS


class TokenAuthentication(authentication.BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = "Token"
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        # from rest_framework.authtoken.models import Token
        from authentication.models import ExpiringToken

        return ExpiringToken

    """
    A custom token model may be used, but must have the following properties.

    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _("Invalid token header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _("Invalid token header. Token string should not contain spaces.")
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _("Invalid token header. Token string should not contain invalid characters.")
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related("user").get(key=key)
            if token.expired():
                # print(token)
                raise exceptions.AuthenticationFailed(_("token超時"))

        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("Invalid token."))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_("User inactive or deleted."))

        return (token.user, token)

    def authenticate_header(self, request):
        return self.keyword


class AccessKeyAuthentication(authentication.BaseAuthentication):
    """App使用Access key進行籤名認證, 目前籤名算法比較簡單,
    app註冊或者手動建立後,會生成 access_key_id 和 access_key_secret,
    然後使用 如下算法生成籤名:
    Signature = md5(access_key_secret + '\n' + Date)
    example: Signature = md5('d32d2b8b-9a10-4b8d-85bb-1a66976f6fdc' + '\n' +
                    'Thu, 12 Jan 2017 08:19:41 GMT')
    請求時設置請求header
    header['Authorization'] = 'Sign access_key_id:Signature' 如:
    header['Authorization'] =
        'Sign d32d2b8b-9a10-4b8d-85bb-1a66976f6fdc:OKOlmdxgYPZ9+SddnUUDbQ=='

    驗證時根據相同算法進行驗證, 取到access_key_id對應的access_key_id, 從request
    headers取到Date, 然後進行md5, 判斷得到的結果是否相同, 如果是認證通過, 否則 認證
    失敗
    """

    keyword = "Sign"

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _("Invalid signature header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _("Invalid signature header. Signature string should not contain spaces.")
            raise exceptions.AuthenticationFailed(msg)

        try:
            sign = auth[1].decode().split(":")
            if len(sign) != 2:
                msg = _("Invalid signature header. Format like AccessKeyId:Signature")
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = _("Invalid signature header. Signature string should not contain invalid characters.")
            raise exceptions.AuthenticationFailed(msg)

        access_key_id = sign[0]
        try:
            uuid.UUID(access_key_id)
        except ValueError:
            raise exceptions.AuthenticationFailed("Access key id invalid")
        request_signature = sign[1]

        return self.authenticate_credentials(request, access_key_id, request_signature)

    @staticmethod
    def authenticate_credentials(request, access_key_id, request_signature):
        access_key = get_object_or_none(AccessKey, id=access_key_id)
        request_date = get_request_date_header(request)
        if access_key is None or not access_key.user:
            raise exceptions.AuthenticationFailed(_("L173 Invalid signature."))
        access_key_secret = access_key.secret

        try:
            request_unix_time = http_to_unixtime(request_date)
        except ValueError:
            raise exceptions.AuthenticationFailed(_("HTTP header: Date not provide or not %a, %d %b %Y %H:%M:%S GMT"))

        if int(time.time()) - request_unix_time > 15 * 60:
            raise exceptions.AuthenticationFailed(_("Expired, more than 15 minutes"))

        signature = make_signature(access_key_secret, request_date)
        if not signature == request_signature:
            raise exceptions.AuthenticationFailed(_("L189 Invalid signature."))

        if not access_key.user.is_active:
            raise exceptions.AuthenticationFailed(_("User disabled."))
        return access_key.user, None


class JWTAuthentication(authentication.BaseAuthentication):
    """
    JSON Web Token based authentication using Django Core Signing.
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Bearer ". For example:
        Authorization: Bearer <access_token>
    """

    keyword = "Bearer"

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed(_("無效的 Token 標頭，未提供憑證。"))
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed(_("無效的 Token 標頭，Token 字串不應包含空格。"))

        try:
            token = auth[1].decode()
        except UnicodeError:
            raise exceptions.AuthenticationFailed(_("無效的 Token 標頭，Token 包含無效字元。"))

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        from django.contrib.auth import get_user_model
        from django.core import signing

        User = get_user_model()

        try:
            # 校驗 access token，設置 1 分鐘過期（60 秒），方便 Demo 展示無感刷新
            data = signing.loads(key, salt="jwt_access", max_age=60)
        except signing.SignatureExpired:
            raise exceptions.AuthenticationFailed(_("token已過期"))
        except signing.BadSignature:
            raise exceptions.AuthenticationFailed(_("無效的token"))

        user_id = data.get("user_id")
        if not user_id:
            raise exceptions.AuthenticationFailed(_("無效的token內容"))

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("用戶不存在"))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_("用戶已被停用。"))

        return (user, key)

    def authenticate_header(self, request):
        return self.keyword
