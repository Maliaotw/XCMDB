from django.apps import AppConfig


class HostsConfig(AppConfig):
    name = 'hosts'
    def ready(self):
        import hosts.signal