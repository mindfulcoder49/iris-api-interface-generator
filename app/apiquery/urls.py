from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'queries', views.APIQueryViewSet, basename='query')

urlpatterns = [
    path('', include(router.urls)),
    path('save/', views.save_query, name='save_query'),
]
