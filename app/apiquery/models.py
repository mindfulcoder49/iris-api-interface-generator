from django.db import models

class APIQuery(models.Model):
    query = models.TextField()  # Store the query string
    response = models.TextField()  # Store response as text
    response_blob = models.BinaryField(null=True, blank=True)  # For large responses like images or files
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query made on {self.created_at}"
