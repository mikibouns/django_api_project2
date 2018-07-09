from rest_framework import status
from .models import Log
import json


class LoggingMixin(object):
    # логирует только при выполнении одного из следующих методов
    allowed_logging_methods = ('get','post', 'patch', 'delete')
    def finalize_response(self, request, response, *args, **kwargs):
        # берем ответ из оригинального метода
        response = super().finalize_response(request, response, *args, **kwargs)
        # не логирует если метод не используется
        if request.method.lower() not in self.allowed_logging_methods:
            return response
        status_code = response.status_code
        log_kwargs = {
            'view': self.get_view_name(),
            'action': self.action,
            'method': request.method.lower(),
            'status_code': status_code,
            'request_path': request.path,
        }
        log_kwargs = json.dumps(log_kwargs)

        if status.is_server_error(status_code):
            # logger.error('error', extra=log_kwargs)
            Log.write_log(request=request, log=log_kwargs)
        elif status.is_client_error(status_code):
            # logger.warning('warning', extra=log_kwargs)
            Log.write_log(request=request, log=log_kwargs)
        else:
            # logger.info('info', extra=log_kwargs)
            Log.write_log(request=request, log=log_kwargs)
        return response