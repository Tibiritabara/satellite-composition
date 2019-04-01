"""
This module contains the main views or endpoint definitions available
for the project
"""
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from challenge.builders import Builder
from challenge.serializers import RequestSerializer


@api_view(['GET'])
@permission_classes((AllowAny, ))
def api_root(request):
    """
    User home, Hello world!
    :param request:
    :return:
    """
    return JsonResponse({"Hello": "World"}, status=status.HTTP_200_OK)


class RequestView(GenericAPIView):
    """
    This class will handle the requests and responses
    """
    serializer_class = RequestSerializer
    permission_classes = (
        AllowAny,
    )

    def post(self, request):
        """
        This method will process the user input via a POST request
        ---
        :param request:
        :return HttpResponse:
        """
        req = self.serializer_class(data=request.data)
        req.is_valid(raise_exception=True)
        builder = Builder(req.validated_data.get('channel_map'))
        path = builder.build(req.__str__())
        image = open(path, "rb").read()
        return HttpResponse(image, content_type="image/jpg")
