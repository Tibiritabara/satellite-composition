"""
Module with all required serializers for the API
"""
from rest_framework import serializers


class RequestSerializer(serializers.Serializer):
    """
    Serializer handling the GeoTiff request
    """
    CHANNEL_MAP_CHOICES = (
        ('visible', 'visible'),
        ('vegetation', 'vegetation'),
        ('waterVapor', 'waterVapor'),
    )

    utm_zone = serializers.CharField(required=True)
    latitude_band = serializers.CharField(required=True)
    grid_square = serializers.CharField(required=True)
    date = serializers.DateField(required=True)
    channel_map = serializers.ChoiceField(choices=CHANNEL_MAP_CHOICES)

    def __str__(self):
        return "T%s%s%s_%sT" % (
            self.validated_data.get("utm_zone"),
            self.validated_data.get("latitude_band"),
            self.validated_data.get("grid_square"),
            self.validated_data.get("date").strftime("%Y%m%d")
        )
