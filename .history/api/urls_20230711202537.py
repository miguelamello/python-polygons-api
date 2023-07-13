from django.urls import path, include
import views

urlpatterns = [
    path('api/providers/', views.ProviderListCreateView.as_view(), name='provider-list'),
    path('api/providers/<int:pk>/', views.ProviderRetrieveUpdateDestroyView.as_view(), name='provider-detail'),
    path('api/service-areas/', views.ServiceAreaListCreateView.as_view(), name='service-area-list'),
    path('api/service-areas/<int:pk>/', views.ServiceAreaRetrieveUpdateDestroyView.as_view(), name='service-area-detail'),
    path('api/find-polygons/', views.FindPolygonsByLatLngView.as_view(), name='find-polygons'),
]
