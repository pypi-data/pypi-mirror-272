from django.apps import AppConfig


class EasyAuditConfig(AppConfig):
    name = 'elegant.contrib.audit'
    verbose_name = '事件审计'
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        try:
            from audit.signals import auth_signals
            from audit.signals import model_signals
            from audit.signals import request_signals
        except ImportError:
            pass
