from rest_framework.exceptions import APIException
from rest_framework import status


class ChannelNotFound(APIException):
    status_code = status.HTTP_412_PRECONDITION_FAILED
    default_detail = "The requested Tiff channel for the given data does not exist."
    default_code = "error"
