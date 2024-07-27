import logging
import dotenv
import os
from llama_index.core import StorageContext, load_index_from_storage, VectorStoreIndex
from .vectorstore import IRISVectorStore
from .models import Document
import re

from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding

from llama_index.core import Settings as LlamaSettings




def get_clean_name(name):
    name = name.lower()
    #strip non-alphanumeric characters
    name = re.sub(r"[^a-z0-9\s]", " ", name)
    document_name = re.sub(r"\s+", "_", name)
    return document_name

def query_existing_document(name, query, top_k_similarity, similarity_threshold):
    dotenv.load_dotenv()
    logger = logging.getLogger(__name__)
    CONNECTION_STRING = os.getenv("IRIS_CONNECTION_STRING")
    if not CONNECTION_STRING:
        logger.error("Connection string is not set. Please check your environment variables.")
        raise ValueError("Connection string is not set.")

    #get embed_dim from the document
    embed_dim = 0
    embed_type = ""
    try:
        all_documents = Document.objects.all()
        for doc in all_documents:
            if doc.name == name:
                embed_dim = doc.embed_dim
                embed_type = doc.embed_type
                if embed_type == "openai":
                    LlamaSettings.embed_model = OpenAIEmbedding(model="text-embedding-3-small", embed_batch_size=100)
                elif embed_type == "bga-large":
                    LlamaSettings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5")
                elif embed_type == "bga-base":
                    LlamaSettings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
                elif embed_type == "bga-small":
                    LlamaSettings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    except Exception as e:
        logger.error(f"Failed to get document: {e}")
        raise ValueError("Failed to get document.") from e

    logger.debug(f"Connecting to vector store with name: {name}")
    
    vector_store = IRISVectorStore.from_params(
        connection_string=CONNECTION_STRING,
        table_name=get_clean_name(name),
        embed_dim=embed_dim,
    )
    
    
    try:
        logger.debug(f"Loading index from storage for document: {name}")
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    except Exception as e:
        logger.error(f"Failed to load index from storage: {e}")
        raise ValueError("Failed to load index from storage.") from e
    
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=top_k_similarity,
    )

    # configure response synthesizer
    response_synthesizer = get_response_synthesizer()

    # assemble query engine
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=similarity_threshold)],
    )
    
    response = query_engine.query(query)
    return response

