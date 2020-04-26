from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TempConfig(AppConfig):
    name = 'memmem_app'


class ProfilesConfig(AppConfig):
    name = 'memmem_app'
    verbose_name = _('profiles')

    def ready(self):
        import memmem_app.signals