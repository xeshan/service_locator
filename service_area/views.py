from django.shortcuts import render
from service_area.serializers import CreateProviderSerializer, \
  GetProviderSerializer, UpdateProviderSerializer, CreateServiceAreaSerializer,\
  GetServiceAreaSerializer, UpdateServiceAreaSerializer, GeoJsonSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from service_area.models import Provider, ServiceArea
from rest_framework import status
from service_area.cache import CacheService, CacheError
import json


# Create your views here.
class ProviderCRUD(APIView):
    def post(self, request):
      response = {}
      serializer_obj = CreateProviderSerializer(data=request.data)
      if serializer_obj.is_valid():
          serializer_obj.save()
          response["data"] = None
          response["message"] = "Provider created successfully"
          response["success"] = True
          status_code = status.HTTP_200_OK        
      else:
          response["data"] = serializer_obj.errors
          response["message"] = "Provider creation failed"
          response["success"] = False
          status_code = status.HTTP_400_BAD_REQUEST
      return Response(response, status=status_code)


    def get(self, request):
      providers = Provider.objects.all()
      provider_serializer = GetProviderSerializer(providers, many=True)
      return Response(provider_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, provider_id):
      provider = Provider.objects.get(pk=provider_id)
      response = {}
      status_code = status.HTTP_400_BAD_REQUEST
      serializer_obj = UpdateProviderSerializer(provider, data=request.data)
      if serializer_obj.is_valid():
          serializer_obj.save()
          response["data"] = None
          response["message"] = "Provider updated successfully"
          response["success"] = True
          status_code = status.HTTP_200_OK
      else:
          response["data"] = serializer_obj.errors
          response["message"] = "Provider updation failed"
          response["success"] = False
      return Response(response, status=status_code)

    def delete(self, request, provider_id):
      response = {}
      provider = Provider.objects.filter(id=provider_id)
      if provider:
        provider.delete()
        status_code = status.HTTP_200_OK
        response["data"] = None
        response["message"] = "Provider deleted successfully"
        response["success"] = True
      else:
        status_code = status.HTTP_200_OK
        response["data"] = None
        response["message"] = "Provider not found"
        response["success"] = True
      
      return Response(response, status=status_code)


class ServiceAreaCRUD(APIView):
  def post(self, request):
    data = request.data
    _mutable = data._mutable
    data._mutable = True
    # print(json.dumps(data["poly"]))
    data["poly"] = json.dumps(data["poly"])
    data._mutable = _mutable

    response = {}
    status_code = status.HTTP_400_BAD_REQUEST
    # if data.get('poly', None):
    #     data["poly"] = json.dumps(data["poly"])
    serializer_obj = CreateServiceAreaSerializer(data=data, context={
        "provider": data.getlist('provider_id')
    })
    if serializer_obj.is_valid():
        serializer_obj.save()
        response["data"] = None
        response["message"] = "Service Area creation successful"
        response["success"] = True
        status_code = status.HTTP_201_CREATED
    else:
        response["data"] = serializer_obj.errors
        response["message"] = "Service Area creation failed"
        response["success"] = False

    return Response(response, status=status_code)


  def get(self, request):
    services = ServiceArea.objects.all()
    services_serializer = GetServiceAreaSerializer(services, many=True)
    return Response(services_serializer.data, status=status.HTTP_200_OK)

  def put(self, request, service_area_id):
    data = request.data
    _mutable = data._mutable
    data._mutable = True
    # print(json.dumps(data["poly"]))
    data["poly"] = json.dumps(data["poly"])
    data._mutable = _mutable    
    response = {}
    status_code = status.HTTP_400_BAD_REQUEST
    try:
        service_area = ServiceArea.objects.get(id=service_area_id)
        serializer_obj = UpdateServiceAreaSerializer(service_area, data=data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            response["data"] = None
            response["message"] = "Service area updated successfully"
            response["success"] = True
            status_code = status.HTTP_200_OK
        else:
            response["data"] = serializer_obj.errors
            response["message"] = "Service Area updation failed"
            response["success"] = False
    except ServiceArea.DoesNotExist:
        response["data"] = None
        response["message"] = "No such service area"
        response["success"] = False
    except Exception as e:
        print(e)

    return Response(response, status=status_code)

  def delete(self, request, service_area_id):
    response = {}
    status_code = status.HTTP_200_OK
    try:
        ServiceArea.objects.get(id=service_area_id).delete()
        response["data"] = None
        response["message"] = "Service Area deleted successfully"
        response["success"] = True
    except ServiceArea.DoesNotExist:
        response["data"] = None
        response["message"] = "Service Area not found"
        response["success"] = False

    return Response(response, status=status_code)


class SearchServiceArea(APIView):
    def put(self, request):
      data = request.data
      response = {}
      status_code = status.HTTP_200_OK
      service_areas = ServiceArea.objects.filter()
      matching_service_area = []
      serializer_obj = GeoJsonSerializer(data=data)
      response_data = {}
      if serializer_obj.is_valid():
        print("here reached")
        point = serializer_obj.data["point"]
        try:
            response_data = CacheService.get(json.dumps(mapping(point)))
        except CacheError:
            pass
        if not response_data:
            for service_area in service_areas:
                polygon = shape(service_area.geo_json)
                if polygon.contains(point):
                    matching_service_area.append(service_area)
            response_data = SearchServiceAreaSerializer(
                        matching_service_area, many=True).data
            try:
                CacheService.set(json.dumps(
                    mapping(point)),
                    response_data)
            except CacheError:
                pass
        response["data"] = response_data
        response["message"] = "Search for service area successfully completed"
        response["success"] = True        
      else:
        print("here reached")
        status_code = status.HTTP_400_BAD_REQUEST
        response["data"] = serializer_obj.errors
        response["message"] = "Search for service area failed"
        response["success"] = False
      return Response(response, status=status_code)

