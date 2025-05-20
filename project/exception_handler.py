from collections.abc import Mapping
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ErrorDetail
from rest_framework.views import exception_handler
from rest_framework import status


def get_field_from_error_message(message):
    if "phone" in message.lower():
        return "phone"
    elif "password" in message.lower():
        return "password"
    elif "is_active" in message.lower():
        return "is_active"
    elif "otp" in message.lower():
        return "otp"
    elif "old_password" in message.lower():
        return "old_password"
    elif "again" in message.lower():
        return "message"
    elif "action" in message.lower():
        return "action"
    return "non_field_errors"


def flatten_errors(errors):
    flattened = {}

    for key, value in errors.items():
        if key == "non_field_errors" and isinstance(value, list) and len(value) > 0:
            for error in value:
                field_name = get_field_from_error_message(error)

                if field_name:
                    flattened[field_name] = _(error)
                    break
        elif isinstance(value, list) and len(value) > 0:
            # If the value is a list, pick the first item or handle accordingly
            item = value[0]

            if isinstance(item, ErrorDetail):
                flattened[key] = (
                    item == "True" if str(item) in ["True", "False"] else str(item)
                )
            else:
                flattened[key] = item
        elif isinstance(value, Mapping):
            flattened[key] = flatten_errors(value)
        else:
            # Handle individual values including ErrorDetail and booleans
            if isinstance(value, ErrorDetail):
                # Convert ErrorDetail to boolean if it represents True/False
                flattened[key] = (
                    value == "True" if value in ["True", "False"] else str(value)
                )
            elif isinstance(value, str) and value in ["True", "False"]:
                # Convert string "True"/"False" to boolean
                flattened[key] = value == "True"
            else:
                flattened[key] = value
    return flattened


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response and response.status_code == status.HTTP_400_BAD_REQUEST:
        response.data = flatten_errors(response.data)

    return response
