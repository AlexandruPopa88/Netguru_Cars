from rest_framework import serializers
from Cars.models import Cars, CarRatings

class CarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = "__all__"

class CarRatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarRatings
        fields = "__all__"