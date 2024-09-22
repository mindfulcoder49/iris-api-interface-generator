from rest_framework import serializers
from .models import APIQuery

class APIQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIQuery
        fields = ['id', 'query', 'response', 'response_blob', 'created_at']
