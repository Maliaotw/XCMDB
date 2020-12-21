from django.apps import AppConfig


class VmConfig(AppConfig):
    name = 'vm'

    def ready(self):
        import vm.signal