# models.py

from django.db import models

class APIQuery(models.Model):
    query = models.TextField(blank=True, null=True)  # Made optional
    response = models.TextField()
    response_blob = models.BinaryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query made on {self.created_at}"

class APIQueryTemplate(models.Model):
    form_fields = models.TextField()  
    base_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Template created on {self.created_at}"
