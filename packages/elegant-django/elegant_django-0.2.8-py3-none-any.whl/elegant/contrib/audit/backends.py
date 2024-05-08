import logging

from .models import CRUDEvent
from .models import LoginEvent
from .models import RequestEvent

logger = logging.getLogger(__name__)


class ModelBackend:

    @staticmethod
    def request(request_info):
        return RequestEvent.objects.create(**request_info)

    @staticmethod
    def crud(crud_info):
        return CRUDEvent.objects.create(**crud_info)

    @staticmethod
    def login(login_info):
        return LoginEvent.objects.create(**login_info)
