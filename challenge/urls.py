"""
This module contains the project urls
"""
from django.urls import path
from challenge.views import RequestView, api_root


urlpatterns = [
    path(
        "generate-image",
        RequestView.as_view(),
        name="request-view",
    ),
    path('', api_root, name="home"),
]
