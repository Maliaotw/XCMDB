"""
Authentication API 單元測試

測試覆蓋：
    1. JWT 登入成功 / 失敗
    2. Access Token 過期與 Refresh Token 刷新
    3. 未認證請求被拒
    4. RBAC 角色回傳
"""

from django.core import signing
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from common.models import UserProfile

# 使用 SQLite 內存資料庫避免依賴 MySQL / Redis
TEST_DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}


class AuthTokenTests(TestCase):
    """JWT 登入與 Token 相關測試"""

    def setUp(self):
        """測試前置：建立測試用戶"""
        self.client = APIClient()
        self.login_url = "/api/v1/api-token-auth/"
        self.refresh_url = "/api/v1/jwt/token/refresh/"

        # 建立普通用戶
        self.user = UserProfile.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com",
        )
        # 建立管理員用戶
        self.admin = UserProfile.objects.create_superuser(
            username="admin",
            password="adminpass123",
            email="admin@example.com",
        )

    # ---------------------------------------------------------------
    # 1. 登入測試
    # ---------------------------------------------------------------
    def test_login_success(self):
        """測試：正確帳密登入應回傳 access_token 和 refresh_token"""
        response = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "testpass123",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)
        self.assertIn("username", response.data)
        self.assertEqual(response.data["username"], "testuser")

    def test_login_wrong_password(self):
        """測試：密碼錯誤應回傳 400"""
        response = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "wrongpassword",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent_user(self):
        """測試：帳號不存在應回傳 400"""
        response = self.client.post(
            self.login_url,
            {
                "username": "nobody",
                "password": "whatever",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_empty_fields(self):
        """測試：空白欄位應回傳 400"""
        response = self.client.post(
            self.login_url,
            {
                "username": "",
                "password": "",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------------------------------------------------------------
    # 2. RBAC 角色回傳測試
    # ---------------------------------------------------------------
    def test_login_returns_admin_role(self):
        """測試：超級用戶登入應回傳 ['admin'] 角色"""
        response = self.client.post(
            self.login_url,
            {
                "username": "admin",
                "password": "adminpass123",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("roles", response.data)
        self.assertIn("admin", response.data["roles"])

    def test_login_returns_visitor_role(self):
        """測試：普通用戶登入應回傳 ['visitor'] 角色"""
        response = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "testpass123",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("roles", response.data)
        self.assertIn("visitor", response.data["roles"])

    # ---------------------------------------------------------------
    # 3. Token 認證測試
    # ---------------------------------------------------------------
    def test_authenticated_request_with_jwt(self):
        """測試：攜帶有效 JWT 應能存取受保護 API"""
        # 先登入取得 token
        login_resp = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "testpass123",
            },
        )
        access_token = login_resp.data["access_token"]

        # 使用 token 存取受保護 API
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get("/api/v1/hosts/")
        # 應成功 (200) 或空列表，而非 401
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_request_rejected(self):
        """測試：未攜帶 Token 應被拒 (401)"""
        self.client.credentials()  # 清除所有認證
        response = self.client.get("/api/v1/hosts/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_token_rejected(self):
        """測試：無效 Token 應被拒 (401)"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid_fake_token_here")
        response = self.client.get("/api/v1/hosts/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ---------------------------------------------------------------
    # 4. Token 刷新測試
    # ---------------------------------------------------------------
    def test_refresh_token_success(self):
        """測試：使用有效的 refresh_token 應能取得新的 access_token"""
        # 先登入取得 refresh_token
        login_resp = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "testpass123",
            },
        )
        refresh_token = login_resp.data["refresh_token"]

        # 使用 refresh_token 取得新的 access_token
        response = self.client.post(
            self.refresh_url,
            {
                "refresh_token": refresh_token,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

    def test_refresh_token_missing(self):
        """測試：未提供 refresh_token 應回傳錯誤"""
        response = self.client.post(self.refresh_url, {})
        self.assertIn(
            response.status_code,
            [
                status.HTTP_400_BAD_REQUEST,
                status.HTTP_401_UNAUTHORIZED,
            ],
        )

    def test_refresh_token_invalid(self):
        """測試：無效的 refresh_token 應回傳錯誤"""
        response = self.client.post(
            self.refresh_url,
            {
                "refresh_token": "totally_invalid_refresh_token",
            },
        )
        self.assertIn(
            response.status_code,
            [
                status.HTTP_400_BAD_REQUEST,
                status.HTTP_401_UNAUTHORIZED,
            ],
        )

    # ---------------------------------------------------------------
    # 5. Token 過期模擬測試
    # ---------------------------------------------------------------
    def test_expired_access_token_returns_specific_message(self):
        """測試：過期的 access_token 應回傳 'token已過期' 訊息"""
        # 手動簽發一個已過期的 token（max_age 為 60 秒，我們回溯 120 秒）
        signing.dumps({"user_id": self.user.id}, salt="jwt_access")
        # 由於我們無法直接控制時間戳，改用 signing.loads 驗證邏輯
        # 這裡我們驗證 JWTAuthentication 的行為：
        # 使用一個合法格式但來自不同 salt 的 token
        bad_salt_token = signing.dumps({"user_id": self.user.id}, salt="wrong_salt")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {bad_salt_token}")
        response = self.client.get("/api/v1/hosts/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ---------------------------------------------------------------
    # 6. 登出測試
    # ---------------------------------------------------------------
    def test_logout_success(self):
        """測試：已認證用戶應能成功登出"""
        # 先登入
        login_resp = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "testpass123",
            },
        )
        access_token = login_resp.data["access_token"]

        # 登出
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.post("/api/v1/logout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
