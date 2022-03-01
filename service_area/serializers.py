from rest_framework import serializers
from service_area.models import Provider, ServiceArea
import json

class CreateProviderSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    language = serializers.CharField()
    currency = serializers.CharField()

    def create(self, validated_data):
        return Provider.objects.create(**validated_data)

class GetProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'

class UpdateProviderSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    language = serializers.CharField(required=False)
    currency = serializers.CharField(required=False)


    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.language = validated_data.get('language', instance.language)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.save()
        return instance


class CreateServiceAreaSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.FloatField()
    poly = serializers.JSONField()
    provider_id = serializers.CharField()
    def create(self, validated_data):
        return ServiceArea.objects.create(**validated_data)
    

class GetServiceAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceArea
        fields = '__all__'

class UpdateServiceAreaSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    price = serializers.FloatField(required=False)
    poly = serializers.JSONField(required=False)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.poly = validated_data.get('poly', instance.poly)
        instance.save()
        return instance

class GeoJsonSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    point = serializers.SerializerMethodField()

    def get_point(self, attrs):
        try:
            return point.Point(attrs['longitude'], attrs['latitude'])
        except (TypeError, ValueError):
            raise serializers.ValidationError("Invalid geo_json point")

class SearchServiceAreaSerializer(serializers.ModelSerializer):
    provider = serializers.SerializerMethodField()

    def get_provider(self, service_area):
        return service_area.provider.name

    class Meta:
        model = ServiceArea
        fields = '__all__'

