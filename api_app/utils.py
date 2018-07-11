from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        if 'detail' not in response.data:
            response.data = {'detail': response.data}
        response.data['message'] = response.status_code
        response.data['success'] = 0
        response.data['exception'] = response.data.pop('detail')
    return response
