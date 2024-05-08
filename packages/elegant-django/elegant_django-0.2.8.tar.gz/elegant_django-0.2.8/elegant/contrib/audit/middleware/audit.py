import logging
from threading import local

logger = logging.getLogger(__name__)


class MockRequest:
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


_thread_locals = local()


def get_current_request():
    return getattr(_thread_locals, 'request', None)


def get_current_user():
    if request := get_current_request():
        return getattr(request, 'user', None)


def set_current_user(user):
    try:
        _thread_locals.request.user = user
    except AttributeError:
        request = MockRequest(user=user)
        _thread_locals.request = request


def clear_request():
    try:
        del _thread_locals.request
    except AttributeError as ex:
        logger.exception(ex)


class EasyAuditMiddleware:
    """Makes request available to this app signals."""

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        _thread_locals.request = request

        if hasattr(self, 'process_request'):
            self.process_request(request)

        response = response or self.get_response(request)

        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)

        return response

    def process_request(self, request):
        _thread_locals.request = request
        return None

    def process_response(self, request, response):
        try:
            del _thread_locals.request
        except AttributeError as ex:
            logger.exception(ex)

        return response

    def process_exception(self, *args):
        try:
            del _thread_locals.request
        except AttributeError as ex:
            logger.exception(ex)

        return None
