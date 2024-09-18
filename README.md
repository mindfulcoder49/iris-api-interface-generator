# IRIS RAG

 Introduction
- [What is Retrieval-Augmented Generation (RAG)?](#what-is-retrieval-augmented-generation-rag)
- [Basic Summation of RAG](#basic-summation-of-rag)
- [Key Features](#key-features)

 InterSystems IRIS Integration
- [Overview](#intersystems-iris-integration)
- [Key Architecture Features](#key-architecture-features)

 IRIS RAG Interface Overview
- [Document Querying](#document-querying)
- [Document Management](#document-management)
- [Configuration Options](#configuration-options)
- [Using the Interface](#using-the-interface)
  - [Model Selection Dropdown](#model-selection-dropdown)
  - [Embed Type Dropdown](#embed-type-dropdown)
  - [Temperature Input](#temperature-input)
  - [Top_k_similarity Input](#top_k_similarity-input)
  - [Similarity Threshold Input](#similarity-threshold-input)
  - [Query Input](#query-input)
  - [Document Name Input](#document-name-input)
  - [Document Textarea](#document-textarea)
  - [Existing Documents Multiselect](#existing-documents-multiselect)
  - [Submit Button](#submit-button)
  - [Clear All Button](#clear-all-button)
  - [Delete Button](#delete-button)
  - [Response Section](#response-section)
  - [Existing Documents Section](#existing-documents-section)
- [Developer Tips](#developer-tips)

 Embedding Options
- [API-Based Embeddings: OpenAI](#api-based-embeddings-openai)

 Attribution
- [Attribution Details](#attribution)

 Quickstart
- [Setup and Configuration](#setup-and-configuration)
- [Usage](#usage)

 Backend
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
  - [Features](#features-1)
  - [Functions](#functions)
    - [`get_clean_name(name)`](#get_clean_namename)
    - [`query_existing_document(name, query)`](#query_existing_documentname-query)

 Frontend
- [Components](#components)
  - [Features](#features-2)
- [Interface](#interface)
  - [Main Sections](#main-sections)
- [Script](#script)
  - [Data](#data)
  - [Methods](#methods)
  - [Lifecycle Hooks](#lifecycle-hooks)
- [Styles](#styles)

 License
- [License](#license)
 

### What is Retrieval-Augmented Generation (RAG)?

Retrieval-Augmented Generation (RAG) is a powerful AI model that combines the strengths of retrieval-based and generative models. It leverages a pre-trained language model to generate responses based on retrieved documents, enabling more accurate and context-aware answers.

### Basic Summation of RAG

RAG enhances the quality of AI-generated responses by incorporating relevant information from existing documents. This approach improves the accuracy and relevance of the generated content, making it ideal for a wide range of applications, from chatbots to content creation.

### Key Features

- Efficiently query documents with an intuitive interface.
- Add new documents and create vector embeddings saved to the database for repeated retrieval-augmented generation.
- Delete existing documents with a few clicks.
- Query multiple documents at once.
- Customize RAG parameters for tailored results.
- View responses and citations for your queries.
- Use local free embeddings or generate OpenAI embeddings via API.

## InterSystems IRIS Integration

This application leverages [InterSystems IRIS](https://www.intersystems.com/products/iris/) as its backend database to efficiently store and manage documents. IRIS is a powerful, high-performance data platform known for its robust data management capabilities.

The application utilizes the [IRIS Django template](https://github.com/grongierisc/iris-django-template/tree/main) for seamless integration with Django, allowing for effective interaction with the IRIS database. Additionally, it incorporates the [Llama-IRIS template](https://github.com/caretdev/llama-iris), which is built on SQLAlchemy, to handle advanced document management and querying.

The application employs **llama_index** to manage the Retrieval-Augmented Generation (RAG) workflow, including handling queries, retrieving relevant documents, and generating responses based on the stored data.

Documents are stored in the IRIS database using the native **iris $VECTOR** data type. This specialized data type supports efficient vector storage and retrieval, which is crucial for handling high-dimensional data used in machine learning and document processing.

The frontend of the application is built with **Vue.js** and styled using **Tailwind CSS**, providing a modern and responsive user interface for interacting with the application.

### Key Architecture Features

- Efficient document storage and retrieval using IRIS’s native $VECTOR data type.
- Integration with Django through the IRIS Django template for seamless backend operations.
- Advanced document management and querying capabilities with the Llama-IRIS template and SQLAlchemy.
- The Django framework handles data operations and document interactions with IRIS.
- Modern and responsive frontend built with Vue.js and styled with Tailwind CSS.
- Robust RAG workflow managed by llama_index for effective document handling and response generation.
- Hugging Face models for document embeddings or OpenAI API for embeddings, supporting variable dimension embeddings on a per-document basis.

## IRIS RAG Interface Overview

The application interface provides several key functionalities:

- **Document Querying**: Perform complex queries on indexed documents using various parameters.
- **Document Management**: Add new documents, view existing ones, and delete documents as needed.
- **Configuration Options**: Adjust parameters such as model type, temperature, and similarity settings for customized query results.

### Using the Interface

Here’s how you can navigate and utilize the key components of the interface:

#### Model Selection Dropdown   
Choose the AI model for processing your queries. This dropdown allows you to select from available models to tailor the query results to your needs.
#### Embed Type Dropdown   
Select the embedding type (e.g., OpenAI or BGA-Large) to influence how documents are represented in vector space.
#### Temperature Input   
Set the temperature parameter (range 0-2) to control the randomness of the AI's responses. Lower values make the output more deterministic.
#### Top_k_similarity Input   
Define the number of top similar documents to consider in the query results. Adjust this value to determine how many results are sent to the LLM to answer the query.
#### Similarity Threshold Input   
Set the threshold for document similarity to filter out less relevant results. This helps in retrieving documents closely matching the query.
#### Query Input   
Enter the text of your query to search through documents. If left blank, a default query will be used: "Describe this document".
#### Document Name Input   
Provide a name for the new document you wish to add. If omitted, the document text will be ignored.
#### Document Textarea   
Input the content of the new document here. This field is crucial for adding new documents to the system.
#### Existing Documents Multiselect   
Select from a list of existing documents for querying or managing. This multi-select input lets you query multiple documents at once.
#### Submit Button   
Use this button to execute queries or add new documents. The results or updates will be displayed accordingly.
#### Clear All Button   
Reset all input fields and selections to their default states, clearing the form for a new entry.
#### Delete Button   
Remove selected documents from the backend, including their vector embeddings. This action is irreversible, so proceed with caution.
#### Response Section   
View the results of your queries, including document content and citations, displayed here.
#### Existing Documents Section   
Displays a list of all currently available documents for quick reference and selection.

### Developer Tips

- Using GPT-4o-mini and local embeddings is the most cost-effective configuration.
- Experiment with different model parameters and embedding types to find the optimal settings for your specific use case.
- Very large documents can take longer to process than the server timeout limit. Split large documents into smaller sections for better performance.
- To select multiple documents, hold the **Ctrl** key while clicking on the document names.

## Embedding Options

When configuring the document management and querying features, you have the option to choose between local embeddings and API-based embeddings. Here’s a detailed comparison of the available embedding options:

### API-Based Embeddings: OpenAI

OpenAI provides embeddings via its API, offering a powerful and scalable solution for generating high-quality document embeddings.

- **Dimension**: 1536
- **Cost**: Usage-based pricing applies; refer to [OpenAI’s pricing page](https://openai.com/api/pricing) for details
- **Accessibility**: Requires an API key and incurs costs based on usage
- **Integration**: Suitable for applications needing high-quality embeddings with scalable cloud-based processing

API-based embeddings provide advanced capabilities and scalability for cloud-based applications.

## Attribution

The vectorstore.py file in this project that implements the IrisVectorStore object with sqlalchemy was written mostly by "Dmitry Maslennikov <dmitry@caretdev.com>" in the llama-iris package here: https://github.com/caretdev/llama-iris/ which is why llama-iris is included in the requirements.txt but not used in the package. It's dependencies are required and better defined in the llama-iris package which I hope to integrate into this project in the future after small updates are applied. For the sake of speed in creating this project for the InterSystems 2024 Python Contest, I brought the code in directly to have full control over the vector storage functionality.

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

This Django module provides several functionalities for managing and querying documents using a vector store and an AI model. It offers endpoints for indexing new documents, querying existing documents, retrieving a list of documents, and deleting documents from the database and vector store. The code integrates with OpenAI and utilizes LlamaIndex for handling vector storage and querying.

### Features

1. **Index Document**: Accepts a request with document text and metadata, creates a vector index for the document, and stores it in the database and vector store.
2. **Query Document**: Queries the indexed documents using a specified query and model, returning responses and citations.
3. **Get Documents**: Returns a list of existing documents stored in the database.
4. **Delete Documents**: Deletes specified documents from both the database and the vector store.

### Endpoints

#### `index(request)`

**Description**: Handles document indexing and querying. It:
- Parses JSON data from the request.
- Indexes new documents if provided.
- Queries existing documents and returns responses and citations.
- Returns the list of existing documents.

**Request Payload**:
- `query_text`: The query to be executed on existing documents.
- `document_text`: The text content of the new document.
- `document_name`: The name of the new document.
- `model_name`: The model to be used for querying (default: `gpt-4o-mini`).
- `embed_type`: The type of embedding to use.
- `temperature`: The temperature setting for the model (default: `0.5`).
- `top_k_similarity`: The number of top similar documents to consider.
- `similarity_threshold`: The threshold for document similarity.
- `selected_documents`: List of document names to query.

**Response**:
- `responses`: A dictionary with document names as keys and their responses and citations as values.
- `existing_documents`: List of all documents stored in the database.

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

- The frontend utilizes a modern JavaScript framework, Vue.js, with Tailwind CSS for styling.

#### Features

- **Model Selection**: Choose from different AI models.
- **Temperature Setting**: Adjust the temperature parameter for the model.
- **Query Input**: Enter a query to retrieve information from documents.
- **Document Management**: Add, view, and delete documents.
- **Response Display**: View responses and citations from the queries.
- **Existing Documents**: Display and select from a list of existing documents.
- **Embed Type Selection**: Choose between OpenAI and BGA-Large embeddings.
- **Top_k_similarity Setting**: Adjust the top_k_similarity parameter for the model.
- **Similarity Threshold Setting**: Adjust the similarity threshold parameter for the model.

### Interface

#### Main Sections

1. **Header**: Displays the main title: "Query and Manage Documents".
2. **Model Name Dropdown**: Allows selection of the AI model for querying.
3. **Embed Type Dropdown**: Allows selection of the embed type (OpenAI or BGA-Large).
4. **Temperature Input**: Numeric input to set the temperature parameter (range 0-2).
5. **Top_k_similarity Input**: Numeric input to set the top_k_similarity parameter (range 0-20).
6. **Similarity Threshold Input**: Numeric input to set the similarity threshold parameter (range 0-1).
7. **Query Input**: Text input field for entering the query. If left blank it will default to "Describe the document".
8. **Document Name Input**: Text input field for entering the document name. If left blank the Document name and Document will be ignored.
9. **Document Textarea**: Textarea for entering the document content. If left blank the Document name will be ignored.
10. **Existing Documents Multiselect**: Multi-select dropdown for existing documents. 
11. **Submit Button**: Submits the query and document information.
12. **Clear All Button**: Clears all input fields and selections.
13. **Delete Button**: Deletes selected documents from the backend. The text and vector embeddings are both deleted.
14. **Response Section**: Displays responses and citations.
15. **Existing Document Section**: Lists all existing documents.

### Script

#### Data

- **query_text**: Stores the query text.
- **document_text**: Stores the document content.
- **document_name**: Stores the document name.
- **model_name**: Stores the selected model name (default: `gpt-4o-mini`).
- **embed_type**: Stores the type of embedding to use.
- **temperature**: Stores the temperature parameter (default: `0.5`).
- **top_k_similarity**: Stores the number of top similar documents to consider.
- **similarity_threshold**: Stores the threshold for document similarity.
- **responses**: Stores responses from the backend.
- **existing_documents**: Stores existing documents.
- **selectedDocuments**: Stores names of selected documents for deletion.

#### Methods

- **submitQuery()**: Sends a POST request to submit the query and document data. Updates `responses` and `existing_document_names`.
- **fetchExistingDocumentNames()**: Sends a POST request to fetch existing documents.
- **deleteDocuments()**: Sends a POST request to remove selected documents. This deleted their vectore stores as well.
- **parseCitations(citations)**: Parses and formats citations from the response.
- **clearQuery()**: Clears the query input field.
- **clearDocumentName()**: Clears the document name input field.
- **clearDocument()**: Clears the document content textarea.
- **clearAll()**: Clears all input fields and selections.

#### Lifecycle Hooks

- **created()**: Fetches existing document names when the component is created.

### Styles

- **Tailwind CSS** is used for styling the vue components

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

