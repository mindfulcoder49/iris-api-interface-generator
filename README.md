# Project Documentation

## Overview

This project is a Django-based web application with vector search capabilities. It integrates LlamaIndex and IRIS database technologies for document management and querying. The application features both backend and frontend components, orchestrated using Docker.

## Attribution

The vectorstore.py file in this project that implements the IrisVectorStore object with sqlalchemy was written mostly by "Dmitry Maslennikov <dmitry@caretdev.com>" in the llama-iris package here: https://github.com/caretdev/llama-iris/ which is why llama-iris is included in the requirements.txt but not used in the package. It's dependencies are required and better defined in the llama-iris package which I hope to integrate into this project in the future after small updates are applied. For the sake of speed in creating this project for the InterSystems 2024 Python Contest, I brought the code in directly to have full control over the vector storage functionality.

# Table of Contents

- [Project Documentation](#project-documentation)
  - [Overview](#overview)
  - [Attribution](#attribution)
  - [Quickstart](#quickstart)
    - [Setup and Configuration](#setup-and-configuration)
    - [Usage](#usage)
  - [Backend](#backend)
    - [URLs Configuration](#urls-configuration)
    - [Vector Store](#vector-store)
    - [Models](#models)
    - [Views](#views)
    - [Features](#features)
    - [Endpoints](#endpoints)
      - [`index(request)`](#indexrequest)
      - [`get_documents(request)`](#get_documentsrequest)
      - [`delete_documents(request)`](#delete_documentsrequest)
    - [Dependencies](#dependencies)
    - [Existing Document Handling](#existing-document-handling)
      - [`get_clean_name(name)`](#get_clean_namename)
      - [`query_existing_document(name, query)`](#query_existing_documentname-query)
  - [Frontend](#frontend)
    - [Components](#components)
    - [Template](#template)
      - [Main Sections](#main-sections)
    - [Script](#script)
      - [Data](#data)
      - [Methods](#methods)
      - [Lifecycle Hooks](#lifecycle-hooks)
    - [Styles](#styles)
  - [License](#license)


## Quickstart

### Setup and Configuration

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/mindfulcoder49/iris-django-template.git
   cd iris-django-template
   ```

2. **Create .env file:**

    - Put it in the root directory with your Docker file
    - Add your OPENAI_API_KEY and IRIS_CONNECTION_STRING
    ```bash
    OPENAI_API_KEY=sk-dkjhf...
    IRIS_CONNECTION_STRING=iris://SuperUser:SYS@localhost:1972/IRISAPP
    ```
3. **Run `docker-compose build`**

    - The Docker file and entrypoint.sh script will handle the rest of the installation and migration

4. **Change the permissions on the repository folder and its contents**

    - In order for the docker container internal users to be able to write to the repository directory the permissions need to allow for that.
    - The easiest way to do that is just set full permissions. 
    - On Linux you can run 
    ```bash
    chmod -R 777 .
    ```
    or
    ```bash
    chmod -R 777 ../iris_django_template
    ```

5. **Run `docker-compose up`**


### Usage

1. **Access the Application:**

   - Frontend: `http://localhost:53795/django/documents/`
   - Backend: `http://localhost:53795/csp/irisapp/EnsPortal.ProductionConfig.zen` login: SuperUser/SYS


## Backend

### URLs Configuration

`app/app/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
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

`app/documents/vectorstore.py`

- **Attribution**: This implementation is a slightly updated version of llama-iris found at https://github.com/caretdev/llama-iris.
- **Purpose**: Implements an IRIS-based vector store for storing and querying vector embeddings.

### Models

`app/documents/models.py`

- **Purpose**: Defines the model for documents stored in the database.

### Views

`app/documents/views.py`

- **Purpose**: Provides view functions for rendering templates and handling API requests related to documents.

This Django module provides several functionalities for managing and querying documents using a vector store and an AI model. It offers endpoints for indexing new documents, querying existing documents, retrieving a list of document names, and deleting documents from the database and vector store. The code integrates with OpenAI and utilizes LlamaIndex for handling vector storage and querying.

### Features

1. **Index Document**: Accepts a request with document text and metadata, creates a vector index for the document, and stores it in the database and vector store.
2. **Query Document**: Queries the indexed documents using a specified query and model, returning responses and citations.
3. **Get Document Names**: Returns a list of existing document names stored in the database.
4. **Delete Documents**: Deletes specified documents from both the database and the vector store.

### Endpoints

#### `index(request)`

**Description**: Handles document indexing and querying. It:
- Parses JSON data from the request.
- Indexes new documents if provided.
- Queries existing documents and returns responses and citations.
- Returns the list of existing document names.

**Request Payload**:
- `query_text`: The query to be executed on existing documents.
- `model_name`: The model to be used for querying (default: `gpt-4o-mini`).
- `temperature`: The temperature setting for the model (default: `0.5`).
- `selected_documents`: List of document names to query.
- `document_text`: The text content of the new document.
- `document_name`: The name of the new document.

**Response**:
- `responses`: A dictionary with document names as keys and their responses and citations as values.
- `existing_document_names`: List of names of all documents stored in the database.

#### `get_documents(request)`

**Description**: Retrieves and returns the names of all documents currently stored in the database.

**Response**:
- `existing_document_names`: List of names of all documents stored in the database.

#### `delete_documents(request)`

**Description**: Deletes specified documents from both the database and the vector store.

**Request Payload**:
- `document_names`: List of document names to be deleted.

**Response**:
- `status`: Success message if documents are deleted successfully.
- `error`: Error message if the operation fails.

### Dependencies

- `Django`: Web framework.
- `logging`: For logging errors and debugging information.
- `dotenv`: For loading environment variables.
- `json`: For parsing JSON data.
- `openai`: For integrating with OpenAI's language models.
- `llama_index`: For vector storage and querying.
- `os`: For accessing environment variables and file operations.


### Existing Document Handling

`app/documents/existing_document_handling.py`

- **Purpose**: Provides functionality for querying existing documents from the vector store using LlamaIndex. Includes functions for loading and querying vector indices and handling query responses.

#### Features

- **`get_clean_name(name)`**: Sanitizes and formats a document name for use in the vector store.
- **`query_existing_document(name, query)`**: Queries a document in the vector store and returns the response.

#### Functions

##### `get_clean_name(name)`

**Description**: Cleans and formats a document name by converting it to lowercase and replacing whitespace with underscores.

**Parameters**:
- `name` (str): The original document name.

**Returns**:
- (str): The sanitized document name.

**Example**:
```python
clean_name = get_clean_name("My Document Name")
# Output: "my_document_name"
```

##### `query_existing_document(name, query)`

**Description**: Queries a document in the vector store and returns the response. Connects to the vector store, loads the document's index, and processes the query.

**Parameters**:
- `name` (str): The name of the document to query.
- `query` (str): The query text to be executed against the document.

**Returns**:
- `response` (ResponseType): The response object containing the result of the query.

**Raises**:
- `ValueError`: If the connection string is not set or if loading the index fails.

**Example**:
```python
response = query_existing_document("my_document_name", "What is the content?")
print(response.response)
# Output: (response from the vector store)
```

## Frontend

### Components

- The frontend utilizes a modern JavaScript framework (e.g., React or Vue.js). Ensure your build process is configured according to the framework's documentation.

#### Features

- **Model Selection**: Choose from different AI models.
- **Temperature Setting**: Adjust the temperature parameter for the model.
- **Query Input**: Enter a query to retrieve information from documents.
- **Document Management**: Add, view, and delete documents.
- **Response Display**: View responses and citations from the queries.
- **Existing Documents**: Display and select from a list of existing documents.

### Template

#### Main Sections

1. **Header**: Displays the main title: "Query and Manage Documents".
2. **Model Name Dropdown**: Allows selection of the AI model for querying.
3. **Temperature Input**: Numeric input to set the temperature parameter (range 0-2).
4. **Query Input**: Text input field for entering the query.
5. **Document Name Input**: Text input field for entering the document name.
6. **Document Textarea**: Textarea for entering the document content.
7. **Existing Documents Multiselect**: Multi-select dropdown for existing documents.
8. **Submit Button**: Submits the query and document information.
9. **Clear All Button**: Clears all input fields and selections.
10. **Delete Button**: Deletes selected documents from the backend.
11. **Response Section**: Displays responses and citations.
12. **Existing Document Names Section**: Lists all existing document names.

### Script

#### Data

- **query**: Stores the query text.
- **document**: Stores the document content.
- **document_name**: Stores the document name.
- **model_name**: Stores the selected model name (default: `gpt-4o-mini`).
- **temperature**: Stores the temperature parameter (default: `0.5`).
- **responses**: Stores responses from the backend.
- **existing_document_names**: Stores names of existing documents.
- **selectedDocuments**: Stores names of selected documents for deletion.

#### Methods

- **submitQuery()**: Sends a POST request to submit the query and document data. Updates `responses` and `existing_document_names`.
- **fetchExistingDocumentNames()**: Sends a GET request to fetch existing document names.
- **deleteDocuments()**: Sends a DELETE request to remove selected documents.
- **parseCitations(citations)**: Parses and formats citations from the response.
- **clearQuery()**: Clears the query input field.
- **clearDocumentName()**: Clears the document name input field.
- **clearDocument()**: Clears the document content textarea.
- **clearAll()**: Clears all input fields and selections.

#### Lifecycle Hooks

- **created()**: Fetches existing document names when the component is created.

### Styles

- **Disabled Button Style**: Custom style for disabled buttons.

```css
button:disabled {
  background-color: #999;
  cursor: not-allowed;
}
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

