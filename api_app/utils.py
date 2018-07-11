from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        if 'detail' not in response.data:
            response.data = {'detail': response.data}
        response.data['message'] = response.status_code
        response.data['success'] = 0
        response.data['exception'] = response.data.pop('detail')
    return response


def validate_json(self, serializer_fields, request_data):
    if not request_data:
        raise ValidationError({'detail': 'data is none'})
    data = list(filter(lambda x: x not in serializer_fields, request_data))
    if data:
        raise ValidationError({'detail': {'the specified fields are not valid for this request': data}})