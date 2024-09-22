from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.views.generic import TemplateView

# Importing the interop_index view from the interop app
from interop.views import index as interop_index

# Importing views from the APIQuery app
from apiquery import views

# Define the router and register the viewset for queries
router = routers.DefaultRouter()
router.register(r'queries', views.APIQueryViewSet, basename='query')

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL
    path('interop/', interop_index),  # Interop page, as you mentioned
    path('save/', views.save_query, name='save_query'),  # Save query API endpoint
    path('', TemplateView.as_view(template_name='index.html')),  # Root URL serving index.html
    path('api/', include(router.urls)),  # Include the router for API query endpoints
    path('api/', include(router.urls)),
    path('api/query_openai/', views.query_openai, name='query_openai'),  # New endpoint for OpenAI
    path('api/submit_query/', views.submit_query, name='submit_query'), # New endpoint for submitting queries
]
