<template>
  <div v-if="showInstructions">
    <button @click="hideInstructions" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4">Hide Instructions</button>
  </div>
  <div v-else>
    <button @click="showInstructionsFunc" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4">Show Instructions</button>
  </div>
  <div v-if="showInstructions">
  <div class="p-6 max-w-4xl mx-auto bg-white shadow-lg rounded-lg">
    <!-- Header -->
    <h1 class="text-4xl font-extrabold text-gray-900 mb-4">IRIS RAG</h1>
    <!-- explanation of RAG-->
    <p class="text-lg text-gray-700 mb-6">
      <span class="font-semibold">What is Retrieval-Augmented Generation (RAG)?</span> 
      Retrieval-Augmented Generation (RAG) is a powerful AI model that combines the strengths of retrieval-based and generative models. It leverages a pre-trained language model to generate responses based on retrieved documents, enabling more accurate and context-aware answers.
    </p>
    <!-- basic summation of rag-->
    <p class="text-lg text-gray-700 mb-6">
      RAG enhances the quality of AI-generated responses by incorporating relevant information from existing documents. This approach improves the accuracy and relevance of the generated content, making it ideal for a wide range of applications, from chatbots to content creation.
    </p>
    <p class="text-lg text-gray-700 mb-6">
      <span class="font-semibold">Key Features:</span>
      <ul class="list-disc pl-5 mt-2">
        <li class="mb-2">Efficiently query documents with an intuitive interface.</li>
        <li class="mb-2">Add new documents and create vector embeddings saved to the database for repeated retrieval augmented generation</li>
        <li class="mb-2">Delete existing documents with a few clicks.</li>
        <li class="mb-2">Query multiple documents at once</li>
        <li class="mb-2">Customize RAG parameters for tailored results.</li>
        <li class="mb-2">View responses and citations for your queries.</li>
        <li class="mb-2">Use local free embeddings or generate OpenAI embeddings via API</li>
      </ul>
    </p>
  </div>
  <div class="p-6 max-w-4xl mx-auto bg-white shadow-lg rounded-lg">
    <h2 class="text-3xl font-extrabold text-gray-900 mb-4">InterSystems IRIS Integration</h2>
    
    <p class="text-lg text-gray-700 mb-6">
      This application leverages <span class="font-semibold text-blue-600">InterSystems IRIS</span> as its backend database to efficiently store and manage documents. IRIS is a powerful, high-performance data platform known for its robust data management capabilities.
    </p>
    
    <p class="text-lg text-gray-700 mb-6">
      The application utilizes the <a href="https://github.com/grongierisc/iris-django-template/tree/main" class="text-blue-600 underline">IRIS Django template</a> for seamless integration with Django, allowing for effective interaction with the IRIS database. Additionally, it incorporates the <a href="https://github.com/caretdev/llama-iris" class="text-blue-600 underline">Llama-IRIS template</a>, which is built on SQLAlchemy, to handle advanced document management and querying.
    </p>
    
    <p class="text-lg text-gray-700 mb-6">
      The application employs <span class="font-semibold text-blue-600">llama_index</span> to manage the Retrieval-Augmented Generation (RAG) workflow. This includes handling queries, retrieving relevant documents, and generating responses based on the stored data.
    </p>
    
    <p class="text-lg text-gray-700 mb-6">
      Documents are stored in the IRIS database using the native <span class="font-semibold text-blue-600">iris $VECTOR</span> data type. This specialized data type supports efficient vector storage and retrieval, which is crucial for handling high-dimensional data used in machine learning and document processing.
    </p>
    
    <p class="text-lg text-gray-700 mb-6">
      The frontend of the application is built with <span class="font-semibold text-blue-600">Vue.js</span> and styled using <span class="font-semibold text-blue-600">Tailwind CSS</span>, providing a modern and responsive user interface for interacting with the application.
    </p>
    
    <p class="text-lg text-gray-700">
      <span class="font-semibold">Key Architecture Features:</span>
      <ul class="list-disc pl-5 mt-2">
        <li class="mb-2">Efficient document storage and retrieval using IRIS’s native $VECTOR data type.</li>
        <li class="mb-2">Integration with Django through the IRIS Django template for seamless backend operations.</li>
        <li class="mb-2">Advanced document management and querying capabilities with the Llama-IRIS template and SQLAlchemy.</li>
        <li class="mb-2">The Django framework handles data operations and document interactions with IRIS.</li>
        <li class="mb-2">Modern and responsive frontend built with Vue.js and styled with Tailwind CSS.</li>
        <li class="mb-2">Robust RAG workflow managed by llama_index for effective document handling and response generation.</li>
        <li class="mb-2">Hugging Face models for document embeddings or OpenAI API for embeddings, supporting variable dimension embeddings on a per document basis.</li>
      </ul>
    </p>
  </div>
  <div class="p-6 max-w-4xl mx-auto bg-white shadow-lg rounded-lg">
    <!-- Header -->
    <h2 class="text-3xl font-extrabold text-gray-900 mb-4">IRIS RAG Interface Overview</h2>
    
    <p class="text-lg text-gray-700 mb-6">
      The application interface provides several key functionalities:
    </p>

    <ul class="list-disc pl-5 mb-6">
      <li class="mb-2">
        <span class="font-semibold text-blue-600">Document Querying</span>: Perform complex queries on indexed documents using various parameters.
      </li>
      <li class="mb-2">
        <span class="font-semibold text-blue-600">Document Management</span>: Add new documents, view existing ones, and delete documents as needed.
      </li>
      <li class="mb-2">
        <span class="font-semibold text-blue-600">Configuration Options</span>: Adjust parameters such as model type, temperature, and similarity settings for customized query results.
      </li>
    </ul>

    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Using the Interface</h2>
    
    <p class="text-lg text-gray-700 mb-6">
      Here’s how you can navigate and utilize the key components of the interface:
    </p>

    <ul class="list-disc pl-5 mb-6">
      <li class="mb-2">
        <span class="font-semibold text-blue-600">Model Selection Dropdown</span>: Choose the AI model for processing your queries. This dropdown allows you to select from available models to tailor the query results to your needs.
      </li>
      <li class="mb-2">
        <span class="font-semibold text-blue-600">Embed Type Dropdown</span>: Select the embedding type (e.g., OpenAI or BGA-Large) to influence how documents are represented in vector space.
      </li>
      <li class="mb-2">
        <span class="font-semibold text-blue-600">Temperature Input</span>: Set the temperature parameter (range 0-2) to control the randomness of the AI's responses. Lower values make the output more deterministic.
      </li>
      <li class="mb-2">
        <span class="font-semibold text-blue-600">Top_k_similarity Input</span>: Define the number of top similar documents to consider in the query results. Adjust this value to determine how many results are sent to the LLM to answer the query.
      </li>
      <li class="mb-2">
        <span class="font-semibold text-blue-600">Similarity Threshold Input</span>: Set the threshold for document similarity to filter out less relevant results. This helps in retrieving documents closely matching the query.
      </li>
      <li class="mb-2">
        <span class="font-semibold text-blue-600">Query Input</span>: Enter the text of your query to search through documents. If left blank, a default query will be used: "Describe this document".
      </li>
      <li class="mb-2">
        <span class="font-semibold text-blue-600">Document Name Input</span>: Provide a name for the new document you wish to add. If omitted, the document text will be ignored.
      </li>
      <li class="mb-2">
        <span class="font-semibold text-blue-600">Document Textarea</span>: Input the content of the new document here. This field is crucial for adding new documents to the system.
      </li>
      <li class="mb-2">
        <span class="font-semibold text-blue-600">Existing Documents Multiselect</span>: Select from a list of existing documents for querying or managing. This multi-select input lets you query multiple documents at once.
      </li>
      <li class="mb-2">
        <span class="font-semibold text-blue-600">Submit Button</span>: Use this button to execute queries or add new documents. The results or updates will be displayed accordingly.
      </li>
      <li class="mb-2">
        <span class="font-semibold text-blue-600">Clear All Button</span>: Reset all input fields and selections to their default states, clearing the form for a new entry.
      </li>
      <li class="mb-2">
        <span class="font-semibold text-blue-600">Delete Button</span>: Remove selected documents from the backend, including their vector embeddings. This action is irreversible, so proceed with caution.
      </li>
      <li class="mb-2">
        <span class="font-semibold text-blue-600">Response Section</span>: View the results of your queries, including document content and citations, displayed here.
      </li>
      <li class="mb-2">
        <span class="font-semibold text-blue-600">Existing Document Names Section</span>: Displays a list of all currently available document names for quick reference and selection.
      </li>
    </ul>

    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Developer Tips</h2>
    
    <p class="text-lg text-gray-700 mb-6">
      - Using GPT-4o-mini and local embeddings is the most cost effective configuration.
    </p>
    <p class="text-lg text-gray-700 mb-6">
      - Experiment with different model parameters and embedding types to find the optimal settings for your specific use case.
    </p>
    <p class="text-lg text-gray-700">
      - Very large documents can take longer to process than the server timeout limit. Split large documents into smaller sections for better performance.
    </p>
    <!-- tip about how to multiselect by holding ctrl key -->
     <p class="text-lg text-gray-700">
      - To select multiple documents, hold the <span class="font-semibold text-blue-600">Ctrl</span> key while clicking on the document names.
    </p>
  </div>
  <div class="p-6 max-w-4xl mx-auto bg-white shadow-lg rounded-lg">
    <!-- Embedding Comparison Section -->
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Embedding Options</h2>
    
    <p class="text-lg text-gray-700 mb-6">
      When configuring the document management and querying features, you have the option to choose between local embeddings and API-based embeddings. Here’s a detailed comparison of the available embedding options:
    </p>

    <div class="bg-gray-100 p-4 rounded-lg mb-6">
      <h3 class="text-xl font-semibold text-gray-800 mb-2">Local Embeddings: AGA-Large</h3>
      <p class="text-lg text-gray-700 mb-4">
        <span class="font-semibold text-blue-600">bge-large</span> is an embedding model provided by <a href="https://huggingface.co/BAAI/bge-large-en-v1.5" class="text-blue-600 underline">BAAI</a> on Hugging Face. It offers a free and open-source solution for generating document embeddings locally.
      </p>
      <ul class="list-disc pl-5 mb-4">
        <li class="mb-2">
          <span class="font-semibold text-blue-600">Dimension</span>: 1024
        </li>
        <li class="mb-2">
          <span class="font-semibold text-blue-600">Cost</span>: Free to use
        </li>
        <li class="mb-2">
          <span class="font-semibold text-blue-600">Accessibility</span>: Available for download and local deployment through Hugging Face
        </li>
        <li class="mb-2">
          <span class="font-semibold text-blue-600">Integration</span>: Ideal for scenarios where local processing is preferred or when avoiding API costs
        </li>
      </ul>
    </div>

    <div class="bg-gray-100 p-4 rounded-lg mb-6">
      <h3 class="text-xl font-semibold text-gray-800 mb-2">API-Based Embeddings: OpenAI</h3>
      <p class="text-lg text-gray-700 mb-4">
        OpenAI provides embeddings via its API, offering a powerful and scalable solution for generating high-quality document embeddings.
      </p>
      <ul class="list-disc pl-5 mb-4">
        <li class="mb-2">
          <span class="font-semibold text-blue-600">Dimension</span>: 1536
        </li>
        <li class="mb-2">
          <span class="font-semibold text-blue-600">Cost</span>: Usage-based pricing applies; refer to <a href="https://openai.com/api/pricing" class="text-blue-600 underline">OpenAI’s pricing page</a> for details
        </li>
        <li class="mb-2">
          <span class="font-semibold text-blue-600">Accessibility</span>: Requires an API key and incurs costs based on usage
        </li>
        <li class="mb-2">
          <span class="font-semibold text-blue-600">Integration</span>: Suitable for applications needing high-quality embeddings with scalable cloud-based processing
        </li>
      </ul>
    </div>
    
    <p class="text-lg text-gray-700">
      Local embeddings offer a cost-effective and flexible solution for offline processing, while API-based embeddings provide advanced capabilities and scalability for cloud-based applications.
    </p>
  </div>
</div>
  <div v-if="showInstructions">
    <button @click="hideInstructions" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4">Hide Instructions</button>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      showInstructions: true
    };
  },
  methods: {
    hideInstructions() {
      this.showInstructions = false;
    },
    showInstructionsFunc() {
      this.showInstructions = true;
    },
  },
};
</script>

<style scoped>
/* Custom styles are now replaced by Tailwind CSS classes */
</style>
