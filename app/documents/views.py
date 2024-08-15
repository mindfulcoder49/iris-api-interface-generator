from django.http import StreamingHttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import openai
import dotenv
from .models import Document
from .existing import query_existing_document, get_clean_name
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage, get_response_synthesizer
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from .vectorstore import IRISVectorStore
import os

@method_decorator(csrf_exempt, name='dispatch')
def index(request):
    logger = logging.getLogger(__name__)
    dotenv.load_dotenv()
    try:
        json_data = json.loads(request.body)
    except json.JSONDecodeError:
        logger.error("Invalid JSON received in request.")
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    query = json_data.get("query_text", "Describe the document")
    if query == "":
        query = "Describe the document"
        
    model_name = json_data.get("model_name", "gpt-4o-mini")
    temperature = json_data.get("temperature", 0.5)  # Default temperature is 0.5
    top_k_similarity = json_data.get("top_k_similarity", 10)
    similarity_threshold = json_data.get("similarity_threshold", 0.7)
    embed_type = json_data.get("embed_type", "openai")
    embed_dim = 0

    logger.debug(f"Querying with model: {model_name}") 
    logger.debug(f"temperature: {temperature}")
    logger.debug(f"top_k_similarity: {top_k_similarity}") 
    logger.debug(f"similarity_threshold: {similarity_threshold}")
    logger.debug(f"embed_type: {embed_type}")
    logger.debug(f"embed_dim: {embed_dim}")
    logger.debug(f"query: {query}")

    if model_name == "phi3":
        llm = Ollama(model="phi3:mini", base_url="http://ollama:11434")
    else:
        llm = OpenAI(model=model_name, temperature=temperature)
    LlamaSettings.llm = llm

    def stream_responses():
        selected_documents = json_data.get("selected_documents", [])
        responses = {}

        for doc in selected_documents:
            try:
                response = query_existing_document(doc, query, top_k_similarity, similarity_threshold)
                responses[doc] = {
                    "response": response.response,
                    "citations": response.get_formatted_sources(1000)
                }
                yield f"data: {json.dumps({doc: responses[doc]})}\n\n"
            except Exception as e:
                logger.error(f"Error querying document {doc}: {str(e)}")
                responses[doc] = {"error": "Failed to query document"}
                yield f"data: {json.dumps({doc: responses[doc]})}\n\n"

        if json_data["document_text"] != "" and json_data["document_name"] != "":
            if embed_type == "openai":
                embed_dim = 1536
                LlamaSettings.embed_model = OpenAIEmbedding(model="text-embedding-3-small", embed_batch_size=100)
            elif embed_type == "bga-large":
                embed_dim = 1024
                LlamaSettings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5")
            elif embed_type == "bga-base":
                embed_dim = 768
                LlamaSettings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
            elif embed_type == "bga-small":
                embed_dim = 384
                LlamaSettings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

            document_text = json_data["document_text"]
            document_name = json_data["document_name"]
            original_name = document_name
            document_name = get_clean_name(document_name)
            documents = [LlamaDocument(text=document_text)]
            CONNECTION_STRING = os.getenv("IRIS_CONNECTION_STRING")
            vector_store = IRISVectorStore.from_params(
                connection_string=CONNECTION_STRING,
                table_name=document_name,
                embed_dim=embed_dim,
            )
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            try:
                index = VectorStoreIndex.from_documents(
                    documents,
                    storage_context=storage_context,
                    show_progress=False,
                )
                logger.debug(f"Index created and stored successfully for document: {document_name}")
                newdoc = Document(name=original_name, content=document_text, table_name=f"data_{document_name}", embed_dim=embed_dim, embed_type=embed_type)
                newdoc.save()
                retriever = VectorIndexRetriever(
                    index=index,
                    similarity_top_k=top_k_similarity,
                )
                response_synthesizer = get_response_synthesizer(streaming=True)
                query_engine = RetrieverQueryEngine(
                    retriever=retriever,
                    response_synthesizer=response_synthesizer,
                    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=similarity_threshold)],
                )
                streaming_response = query_engine.query(query)
                for text in streaming_response.response_gen:
                    yield f"data: {json.dumps({document_name: {'response': text}})}\n\n"
            except Exception as e:
                logger.error(f"Error creating or querying index for document {document_name}: {str(e)}")
                responses[document_name] = {"error": "Failed to create or query index"}
                yield f"data: {json.dumps({document_name: responses[document_name]})}\n\n"

    return StreamingHttpResponse(stream_responses(), content_type='text/event-stream')

def ollama_pull(request):
    url = "http://ollama:11434/api/pull"  # Use Docker service name for hostname if applicable
    try:
        api_response = requests.post(url, json=request.body)
        api_response.raise_for_status()
        return JsonResponse(api_response.json())
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def ollama(request):
    prompt = request.GET.get("prompt", "who are you?")
    url = "http://ollama:11434/api/generate"
    payload = {
        "model": "phi3",
        "prompt": prompt,
        "stream": False,
    }
    try:
        api_response = requests.post(url, json=payload)
        api_response.raise_for_status()
        return JsonResponse(api_response.json())
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_documents(request):
    existing_document_names = [doc.name for doc in Document.objects.all()]
    existing_documents = []
    for doc in Document.objects.all():
        existing_documents.append({
            "name": doc.name,
            "content": doc.content,
            "table_name": doc.table_name,
            "embed_dim": doc.embed_dim,
            "embed_type": doc.embed_type
        })
    return JsonResponse({"existing_document_names": existing_document_names, "existing_documents": existing_documents}, status=200)

def delete_documents(request):
    dotenv.load_dotenv()
    try:
        json_data = json.loads(request.body)
        document_names = json_data.get("document_names", [])
        if not document_names:
            return JsonResponse({"error": "No document names provided"}, status=400)
        CONNECTION_STRING = os.getenv("IRIS_CONNECTION_STRING")
        if not CONNECTION_STRING:
            return JsonResponse({"error": "IRIS_CONNECTION_STRING not set"}, status=500)
        for name in document_names:
            clean_name = get_clean_name(name)
            table_name = f"data_{name.lower()}"
            try:
                vector_store = IRISVectorStore.from_params(
                    connection_string=CONNECTION_STRING,
                    table_name=clean_name,
                    embed_dim=1536,
                    perform_setup=False
                )
                vector_store.drop_table()
            except Exception as sql_error:
                return JsonResponse({"error": f"Failed to drop table {table_name}: {str(sql_error)}"}, status=500)
            logging.debug(f"Type of name: {type(clean_name)}, Value of name: {clean_name}")
            if isinstance(name, str):
                try:
                    all_documents = Document.objects.all()
                    for doc in all_documents:
                        if doc.name == name:
                            doc.delete()
                except Exception as orm_error:
                    return JsonResponse({"error": f"Failed to delete document {name}: {str(orm_error)}"}, status=500)
            else:
                logging.error("The name variable is not a string.")
                return JsonResponse({"error": "Invalid document name type"}, status=400)
        return JsonResponse({"status": "success", "message": "Documents and tables deleted successfully"})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
