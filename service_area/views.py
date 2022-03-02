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
from service_area import utils

class ProviderCRUD(APIView):

  def post(self, request):
    (response, status_code) = utils.create_provider(request.data)
    return Response(response, status=status_code)

  def get(self, request):
    (response, status_code) = utils.get_providers()
    return Response(response, status=status_code)

  def put(self, request, provider_id):
    (response, status_code) = utils.update_provider(provider_id, request.data)
    return Response(response, status=status_code)

  def delete(self, request, provider_id):
    (response, status_code) = utils.delete_provider(provider_id)
    return Response(response, status=status_code)

class ServiceAreaCRUD(APIView):

  def post(self, request):
    (response, status_code) = utils.create_service_area(request.data)
    return Response(response, status=status_code)


  def get(self, request):
    (response, status_code) = utils.get_service_area()
    return Response(response, status=status_code)

  def put(self, request, service_area_id):
    (response, status_code) = utils.update_service_area(request.data, service_area_id)
    return Response(response, status=status_code)

  def delete(self, request, service_area_id):
    (response, status_code) = utils.delete_service_area(service_area_id)
    return Response(response, status=status_code)


class SearchServiceArea(APIView):

  def put(self, request):
    (response, status_code) = utils.search_service_area(request.data)
    return Response(response, status=status_code)

