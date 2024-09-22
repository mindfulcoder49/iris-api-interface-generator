from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.views.generic import TemplateView

# Importing the interop_index view from the interop app
from interop.views import index as interop_index

# Importing specific views from the APIQuery app
from apiquery.views import (
    APIQueryViewSet,
    APIQueryTemplateViewSet,
    save_query,
    save_template,
    query_openai,
    submit_query,
    get_templates,
)

# Define the router and register the viewsets
router = routers.DefaultRouter()
router.register(r'api_queries', APIQueryViewSet)
router.register(r'api_templates', APIQueryTemplateViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL
    path('interop/', interop_index),  # Interop page
    path('', TemplateView.as_view(template_name='index.html')),  # Root URL serving index.html
    path('api/', include(router.urls)),  # Include the router for API endpoints
    path('api/save_query/', save_query, name='save_query'),
    path('api/save_template/', save_template, name='save_template'),
    path('api/query_openai/', query_openai, name='query_openai'),
    path('api/submit_query/', submit_query, name='submit_query'),
    path('api/get_templates/', get_templates, name='get_templates'),
]
