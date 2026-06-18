#

from django.conf import settings

from .models import Client

__all__ = ["new_client"]


def new_client():
    """
    :return: authentication.models.Client
    """
    server_url = getattr(settings, "AUTH_OPENID_SERVER_URL", "http://localhost/auth")
    realm_name = getattr(settings, "AUTH_OPENID_REALM_NAME", "master")
    client_id = getattr(settings, "AUTH_OPENID_CLIENT_ID", "cmdb")
    client_secret = getattr(settings, "AUTH_OPENID_CLIENT_SECRET", "")
    return Client(server_url=server_url, realm_name=realm_name, client_id=client_id, client_secret=client_secret)
