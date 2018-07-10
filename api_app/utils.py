from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    print(response)
    if 'detail' not in response.data:
        response.data = {'detail': response.data}
    if response is not None:
        response.data['message'] = response.status_code
        response.data['success'] = 0
        response.data['exception'] = response.data.pop('detail')
    return response
