# serializers.py

from rest_framework import serializers
from .models import APIQuery, APIQueryTemplate

class APIQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIQuery
        fields = ['id', 'query', 'response', 'response_blob', 'created_at']

class APIQueryTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIQueryTemplate
        fields = ['id', 'form_fields', 'base_url', 'created_at']
