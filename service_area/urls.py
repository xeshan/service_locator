from service_area import views
from django.urls import path
from service_area.views import ProviderCRUD, ServiceAreaCRUD, SearchServiceArea

urlpatterns = [
    path('provider/', ProviderCRUD.as_view(), name='provider'),
	path('provider/<provider_id>/', ProviderCRUD.as_view(), name='provider_by_id'),
    path('service-area/', ServiceAreaCRUD.as_view(), name='service_area'),
    path('service-area/<service_area_id>/', ServiceAreaCRUD.as_view(), name='service_area_by_id'),
    path('search/', SearchServiceArea.as_view(), name='service_area_search')
]
