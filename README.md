# Project Documentation

## Overview

This project is a Django-based web application with integrated vector search capabilities. It utilizes the Llama Index and IRIS database technologies for document management and querying. The application includes both backend and frontend components, which are orchestrated using Docker.

## Table of Contents

1. [Backend](#backend)
   - [Vector Store](#vector-store)
   - [Models](#models)
   - [Views](#views)
   - [Existing Document Handling](#existing-document-handling)
2. [Frontend](#frontend)
   - [Setup](#setup)
   - [Components](#components)
3. [Docker](#docker)
4. [Setup and Configuration](#setup-and-configuration)
5. [Usage](#usage)
6. [License](#license)

## Backend
### URLs Configuration

`app/app/urls.py`

```python
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from interop.views import index as interop_index
from documents.views import index as documents_index, get_documents, delete_documents
from django.views.generic import TemplateView

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('interop/', interop_index),
    path('api/documents/', documents_index),
    path('api/document_names/', get_documents),
    path('api/documentsdelete/', delete_documents),
    path('documents/', TemplateView.as_view(template_name='index.html')),
]
```

- **Purpose**: Defines URL routing for the Django application, including API endpoints and views.


### Vector Store

`app/documents/vectorstore.py````

- **attribution**: This implementation is a slightly updated version of llama-iris here: https://github.com/caretdev/llama-iris

- **Purpose**: Implements an IRIS-based vector store for storing and querying vector embeddings.

### Models

`app/documents/models.py`

```python
from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```

- **Purpose**: Defines the model for documents stored in the database.

### Views

`app/documents/views.py`

```python
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer

def index(request):
    return render(request, 'documents/index.html')

@api_view(['GET'])
def get_documents(request):
    documents = Document.objects.all()
    serializer = DocumentSerializer(documents, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_documents(request):
    ids = request.data.get('ids', [])
    Document.objects.filter(id__in=ids).delete()
    return Response({"status": "success"})
```

- **Purpose**: Provides view functions for rendering templates and handling API requests related to documents.

### Existing Document Handling

- The existing documents handling is implemented via Django's ORM and REST API views, allowing for CRUD operations on the `Document` model.

## Frontend

### Setup

Ensure you have Node.js and npm installed. Then, install the necessary dependencies:

```bash
cd frontend
npm install
```

### Components

- The frontend utilizes a modern JavaScript framework (such as React or Vue.js). Ensure your build process is set up according to the framework's documentation.

## Docker

### Dockerfile

`Dockerfile`

```dockerfile
# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]
```

## Setup and Configuration

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/mindfulcoder49/iris-django-template.git
   cd your-repo
   ```

2. **Set Up the Backend:**

   ```bash
   cd app
   pip install -r requirements.txt
   ```

3. **Set Up the Frontend:**

   ```bash
   cd frontend
   npm install
   ```

4. **Run Docker Compose:**

   ```bash
   docker-compose up --build
   ```

5. **Migrate the Database:**

   ```bash
   docker-compose exec web python manage.py migrate
   ```

## Usage

1. **Access the Application:**

   - Backend: `http://localhost:53795/csp/irisapp/EnsPortal.ProductionConfig.zen`
   - Frontend: `http://localhost:53795/django/documents/`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to adjust any details or add more specific instructions based on the exact requirements and setup of your project!