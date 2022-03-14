from service_area.models import Provider, ServiceArea
from service_area.serializers import CreateProviderSerializer, \
  GetProviderSerializer, UpdateProviderSerializer, CreateServiceAreaSerializer,\
  GetServiceAreaSerializer, UpdateServiceAreaSerializer, GeoJsonSerializer, SearchServiceAreaSerializer
from rest_framework import status
import json
from service_area.cache import CacheError, CacheService
from shapely.geometry import mapping, shape, polygon, point

def get_providers(query_data=None):
  response = {}
  providers = Provider.objects.all()
  response["success"] = True
  status_code = status.HTTP_204_NO_CONTENT
  if providers:
      serializer_obj = provider_serializer = GetProviderSerializer(providers, many=True)
      response["data"] = serializer_obj.data
      response["message"] = "Providers fetched successfully"
      status_code = status.HTTP_200_OK
  else:
      response["data"] = None
      response["message"] = "No provider found"
  return response, status_code

def create_provider(data):
  response = {}
  status_code = status.HTTP_400_BAD_REQUEST
  serializer_obj = CreateProviderSerializer(data=data)
  if serializer_obj.is_valid():
      serializer_obj.save()
      response["data"] = None
      response["message"] = "Provider created successfully"
      response["success"] = True
      status_code = status.HTTP_201_CREATED
  else:
      response["data"] = serializer_obj.errors
      response["message"] = "Provider creation failed"
      response["success"] = False
  return response, status_code

def update_provider(provider_id, data):
  provider = Provider.objects.get(pk=provider_id)
  response = {}
  status_code = status.HTTP_400_BAD_REQUEST
  serializer_obj = UpdateProviderSerializer(provider, data=data)
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
  return response, status_code

def delete_provider(provider_id):
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
  return response, status_code

def create_service_area(data):
  _mutable = data._mutable
  data._mutable = True
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
      response["message"] = "Service Area created successfully"
      response["success"] = True
      status_code = status.HTTP_201_CREATED
  else:
      response["data"] = serializer_obj.errors
      response["message"] = "Service Area creation failed"
      response["success"] = False  
  return response, status_code

def get_service_area():
  services = ServiceArea.objects.all()
  response={}
  response["success"] = True
  status_code = status.HTTP_204_NO_CONTENT
  if services:
      services_serializer = GetServiceAreaSerializer(services, many=True)
      response["data"] = services_serializer.data
      response["message"] = "Service area fetched successfully"
      status_code = status.HTTP_200_OK
  else:
      response["data"] = None
      response["message"] = "No service area found"
      response["success"] = False  

  return response, status_code

def update_service_area(data, service_area_id):
  _mutable = data._mutable
  data._mutable = True
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

  return response, status_code

def delete_service_area(service_area_id):
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

  return response, status_code

def search_service_area(data):
  response = {}
  status_code = status.HTTP_200_OK
  service_areas = ServiceArea.objects.filter()
  matching_service_area = []
  serializer_obj = GeoJsonSerializer(data=data)
  response_data = {}
  if serializer_obj.is_valid():
    point = serializer_obj.data["point"]
    try:
        response_data = CacheService.get(json.dumps(mapping(point)))
    except CacheError:
        pass
    if not response_data:
        for service_area in service_areas:
            polygon = shape(service_area.poly)
            if polygon.contains(polygon):
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
    status_code = status.HTTP_400_BAD_REQUEST
    response["data"] = serializer_obj.errors
    response["message"] = "Search for service area failed"
    response["success"] = False  
  return response, status_code


