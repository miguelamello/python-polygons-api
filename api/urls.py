from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'providers', views.ProviderViewSet)
router.register(r'service-areas', views.ServiceAreaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
