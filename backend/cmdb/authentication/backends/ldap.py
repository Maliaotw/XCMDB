#

import ldap
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django_auth_ldap.backend import LDAPBackend, _LDAPUser
from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion, _LDAPConfig

# from users.utils import construct_user_email

logger = _LDAPConfig.get_logger()


def construct_user_email(email, username):
    if "@" not in email:
        if "@" in username:
            email = username
        else:
            email = f"{username}@{settings.EMAIL_SUFFIX}"
    return email


class LDAPAuthorizationBackend(LDAPBackend):
    """
    Override this class to override _LDAPUser to LDAPUser
    """

    def authenticate(self, request=None, username=None, password=None, **kwargs):
        logger.info("Authentication LDAP backend")
        if not username:
            logger.info("Authenticate failed: username is None")
            return None

        ldap_user = LDAPUser(self, username=username.strip(), request=request)
        user = self.authenticate_ldap_user(ldap_user, password)
        logger.info(f"Authenticate user: {user}")
        if user:
            user.is_staff = True
            user.save()

        return user

    def get_user(self, user_id):
        user = None

        try:
            user = self.get_user_model().objects.get(pk=user_id)
            logger.debug(f"get_user {user}")

            LDAPUser(self, user=user)  # This sets user.ldap_user
            logger.debug(f"get_user {LDAPUser}")

        except ObjectDoesNotExist:
            pass

        return user


class LDAPUser(_LDAPUser):
    def _search_for_user_dn(self):
        """
        This method was overridden because the AUTH_LDAP_USER_SEARCH
        configuration in the settings.py file
        is configured with a `lambda` problem value
        """

        user_search_union = [
            LDAPSearch(USER_SEARCH, ldap.SCOPE_SUBTREE, settings.AUTH_LDAP_SEARCH_FILTER)
            for USER_SEARCH in str(settings.AUTH_LDAP_SEARCH_OU).split("|")
        ]

        search = LDAPSearchUnion(*user_search_union)
        if search is None:
            raise ImproperlyConfigured("AUTH_LDAP_USER_SEARCH must be an LDAPSearch instance.")

        results = search.execute(self.connection, {"user": self._username})
        if results is not None and len(results) == 1:
            (user_dn, self._user_attrs) = next(iter(results))
        else:
            user_dn = None

        return user_dn

    def _populate_user_from_attributes(self):
        for field, attr in self.settings.USER_ATTR_MAP.items():
            try:
                value = self.attrs[attr][0]
            except LookupError:
                logger.warning(f"{self.dn} does not have a value for the attribute {attr}")
            else:
                if not hasattr(self._user, field):
                    continue
                if isinstance(getattr(self._user, field), bool):
                    value = value.lower() in ["true", "1"]
                setattr(self._user, field, value)

        email = getattr(self._user, "email", "")
        email = construct_user_email(email, self._user.username)
        self._user.email = email
