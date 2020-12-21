from django.dispatch import receiver
from django.utils import timezone
from .tasks import write_login_log_async
from .signals import post_auth_success, post_auth_failed
from .utils import get_request_ip

import logging


def generate_data(username, request):
    logging.debug("generate_data {}".format(request))

    login_ip = get_request_ip(request)
    logging.debug("generate_data {}".format(login_ip))
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    login_type = 'W'

    data = {
        'username': username,
        'ip': login_ip,
        'type': login_type,
        'user_agent': user_agent,
        'datetime': timezone.now()
    }
    # print(data)
    return data

@receiver(post_auth_success)
def on_user_auth_success(sender, user, request, **kwargs):

    logging.debug('on_user_auth_success')
    
    data = generate_data(user.username, request)
    data.update({'status': True})

    # 沒開celery會卡在這裡
    # write_login_log_async.delay(**data)
    write_login_log_async(**data)


@receiver(post_auth_failed)
def on_user_auth_failed(sender, username, request, reason, **kwargs):
    logging.debug('on_user_auth_failed')
    
    data = generate_data(username, request)
    data.update({'reason': reason, 'status': False})
    write_login_log_async(**data)
