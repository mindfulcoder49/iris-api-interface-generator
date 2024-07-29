<template>
  <div class="max-w-4xl mx-auto px-4 py-6">
    <!-- Header -->
    <h1 class="text-3xl font-extrabold mb-6 text-gray-900">Query and Manage Documents</h1>

    <!-- Model Name Dropdown -->
    <div class="mb-6">
      <label for="model_name" class="block text-gray-700 text-sm font-bold mb-2">Model Name</label>
      <select
        id="model_name"
        v-model="model_name"
        class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
      >
        <option value="gpt-4">GPT-4</option>
        <option value="gpt-3.5-turbo">GPT-3.5-turbo</option>
        <option value="gpt-4o">GPT-4o</option>
        <option value="gpt-4o-mini">GPT-4o-mini</option>
        <option value="phi3">Phi3</option>
      </select>
    </div>

    <!-- Add section explaining a button that triggers an endpoint to download the phi3 model or check if it is downloaded.
     the section needs a spot for the status of the mode
    <div class="mb-6">
      <h2 class="text-2xl font-semibold mb-2 text-gray-900">Phi3 Model</h2>
      <p class="text-sm text-gray-600">The Phi3 model is a large model that requires additional setup. Click the button below to download the model.</p>
      <button
        @click="downloadPhi3Model"
        class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        Download Phi3 Model
      </button>
      <p class="text-sm text-gray-600 mt-2" v-if="phi3Status">Status: {{ phi3Status }}</p>
    </div>
  -->

    <!-- embed_type either openai or bga-large-->
    <div class="mb-6">
      <label for="embed_type" class="block text-gray-700 text-sm font-bold mb-2">Embed Type</label>
      <select
        id="embed_type"
        v-model="embed_type"
        class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
      >
        <option value="openai">OpenAI</option>
        <option value="bga-small">BGA-Small (Fastest)</option>
        <option value="bga-base">BGA-Base (Medium)</option>
        <option value="bga-large">BGA-Large (Slow)</option>

      </select>
    </div>

    <!-- Temperature Input -->
    <div class="mb-6">
      <label for="temperature" class="block text-gray-700 text-sm font-bold mb-2">Temperature (0-2)</label>
      <p class="text-sm text-gray-600">Controls the randomness of the generated text. Lower values are more deterministic, higher values are more random.</p>
      <input
        id="temperature"
        type="number"
        v-model.number="temperature"
        min="0"
        max="2"
        step="0.1"
        class="block w-full bg-white border border-gray-400 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
        placeholder="Enter temperature"
      />
    </div>

    <!-- Top_k_similarity Input -->
    <div class="mb-6">
      <label for="top_k_similarity" class="block text-gray-700 text-sm font-bold mb-2">Top_k_similarity (0-20)</label>
      <p class="text-sm text-gray-600">Number of similar documents to retrieve</p>
      <input
        id="top_k_similarity"
        type="number"
        v-model.number="top_k_similarity"
        min="0"
        max="20"
        step="1"
        class="block w-full bg-white border border-gray-400 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
        placeholder="Enter top_k_similarity"
      />
    </div>

    <!-- Similarity Threshold Input -->
    <div class="mb-6">
      <label for="similarity_threshold" class="block text-gray-700 text-sm font-bold mb-2">Similarity Threshold (0-1)</label>
      <p class="text-sm text-gray-600">Minimum similarity score for a document to be considered relevant</p>
      <input
        id="similarity_threshold"
        type="number"
        v-model.number="similarity_threshold"
        min="0"
        max="1"
        step="0.1"
        class="block w-full bg-white border border-gray-400 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
        placeholder="Enter similarity threshold"
      />
    </div>

    <!-- Query Input -->
    <div class="mb-6 relative">
      <label for="query" class="block text-gray-700 text-sm font-bold mb-2">Query</label>
      <textarea
        id="query"
        v-model="query"
        placeholder="Enter your query"
        class="block w-full bg-white border border-gray-400 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
        rows="6"
      ></textarea>
      <button @click="clearQuery" class="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-600 hover:text-gray-900">
        &#x2715;
      </button>
    </div>

    <!-- Document Name Input -->
    <div class="mb-6 relative">
      <label for="document_name" class="block text-gray-700 text-sm font-bold mb-2">Document Name</label>
      <p class="text-sm text-gray-600">If blank then this and the document will be ignored</p>
      <input
        id="document_name"
        v-model="document_name"
        placeholder="Enter document name"
        class="block w-full bg-white border border-gray-400 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
      />
      <button @click="clearDocumentName" class="absolute right-2 bottom-2 text-gray-600 hover:text-gray-900">
        &#x2715;
      </button>
    </div>

    <!-- Document Textarea -->
    <div class="mb-6 relative">
      <label for="document" class="block text-gray-700 text-sm font-bold mb-2">Document</label>
      <p class="text-sm text-gray-600">If blank then this and the document name will be ignored</p>
      <textarea
        id="document"
        v-model="document"
        placeholder="Enter your document text"
        class="block w-full bg-white border border-gray-400 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
        rows="6"
      ></textarea>
      <button @click="clearDocument" class="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-600 hover:text-gray-900">
        &#x2715;
      </button>
    </div>

    <!-- Existing Documents Multiselect -->
    <div class="mb-6">
      <label for="existing_documents" class="block text-gray-700 text-sm font-bold mb-2">Existing Documents</label>
      <p class="text-sm text-gray-600">Select one or more documents to query against</p>
      <p class="text-sm text-gray-600">Hold down the Ctrl (windows) / Command (Mac) button to select or unselect multiple options.</p>
      <select
        id="existing_documents"
        v-model="selectedDocuments"
        multiple
        class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
      >
        <option v-for="(doc, index) in existing_documents" :key="index" :value="doc.name">
          {{ doc.name }} - {{ doc.embed_type }} - {{ doc.embed_dim }}
        </option>
      </select>
    </div>

    <div class="mb-6 flex space-x-4">
    <!-- Submit Button -->
    <button
      @click="submitQuery"
      id="submitQuery"
      class="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
    >
      Query/Add Document
    </button>

    <!-- Clear All Button -->
    <button
      @click="clearAll"
      class="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
    >
      Clear All
    </button>

    <!-- Delete Button -->
    <button
      @click="deleteDocuments"
      class="flex-1 bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
    >
      Delete Selected Documents
    </button>
  </div>

    <!-- Response Section -->
    <div v-if="responses" class="mb-6">
      <h2 class="text-2xl font-semibold mb-2 text-gray-900">Responses:</h2>
      <div v-for="(response, document_name) in responses" :key="document_name" class="mb-4">
        <h3 class="text-lg font-semibold text-gray-800">{{ document_name }}</h3>
        <p class="text-gray-700 mb-2">{{ parseResponse(response.response) }}</p>
        <div v-if="response.citations" class="text-gray-600">
          <h4 class="text-md font-semibold mb-1">Citations:</h4>
          <div v-for="(citation, index) in parseCitations(response.citations)" :key="index" class="mb-2 p-2 border border-gray-200 rounded-lg">
            <p>{{ citation }}</p>
          </div>
        </div>
        <!-- might have error in response.error-->
        <p v-if="response.error" class="text-red-600">{{ response.error }}</p>
        <hr class="my-4 border-gray-300" />
      </div>
    </div>

  </div>
</template>

<script>
import VueCookies from 'vue-cookies';

export default {
  data() {
    return {
      query: '',
      document: '',
      document_name: '',
      model_name: 'gpt-4o-mini', // Default model name
      embed_type: 'openai', // Default embed_type
      temperature: .5, // Default temperature
      top_k_similarity: 3, // Default top_k_similarity
      similarity_threshold: .4, // Default similarity_threshold
      responses: {},  // Should be an object to store document names as keys
      existing_document_names: [], 
      existing_documents: [],
      selectedDocuments: [],
      phi3Status: null,
    };
  },
  methods: {
    async submitQuery() {
      // Check for duplicate document names or content
      if (this.checkDocumentDuplicates()) {
        //ask for confirmation
        if (!confirm('A document with the same name or content already exists. Are you sure you want to proceed?')) {
          return;
        }
      }
      // Change the button text for element with id submitQuery to "Loading..."
      document.getElementById('submitQuery').innerText = 'Loading...';
      //disable it
      document.getElementById('submitQuery').disabled = true;
      try {
        const response = await fetch('/django/api/documents/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': VueCookies.get('csrftoken'),
          },
          body: JSON.stringify({
            query_text: this.query,
            document_text: this.document,
            document_name: this.document_name,
            model_name: this.model_name,
            embed_type: this.embed_type,
            temperature: this.temperature,
            top_k_similarity: this.top_k_similarity,
            similarity_threshold: this.similarity_threshold,
            selected_documents: this.selectedDocuments || [],
          }),
        });
        const data = await response.json();
            // Change the button text for element with id submitQuery back to "Submit to GPT-4o-mini"
        document.getElementById('submitQuery').innerText = 'Query';
        //enable it
        document.getElementById('submitQuery').disabled = false;
        this.responses = data.responses;
        this.existing_document_names = data.existing_document_names;
        this.existing_documents = data.existing_documents;
      } catch (error) {
        // Change the button text for element with id submitQuery back to "Submit to GPT-4o-mini"
        document.getElementById('submitQuery').innerText = 'Query';
        //enable it
        document.getElementById('submitQuery').disabled = false;
        console.error('Error submitting query:', error);
        alert('An unexpected error occurred.');
      }
    },
    
    async fetchExistingDocumentNames() {
      try {
        const response = await fetch('/django/api/document_names/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': VueCookies.get('csrftoken'),
          },
        });
        const data = await response.json();
        this.existing_document_names = data.existing_document_names;
        this.existing_documents = data.existing_documents;
      } catch (error) {
        console.error('Error fetching existing document names:', error);
      }
    },
    
    async deleteDocuments() {
      if (this.selectedDocuments.length === 0) {
        alert('Please select documents to delete.');
        return;
      }
      
      if (!confirm('Are you sure you want to delete the selected documents?')) {
        return;
      }
      
      try {
        const response = await fetch('/django/api/documentsdelete/', {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': VueCookies.get('csrftoken'),
          },
          body: JSON.stringify({ document_names: this.selectedDocuments }),
        });
        const data = await response.json();
        if (response.ok) {
          alert('Documents deleted successfully.');
          this.selectedDocuments = [];
          this.fetchExistingDocumentNames();  // Refresh the list of documents
        } else {
          alert('Error deleting documents: ' + data.error);
        }
      } catch (error) {
        console.error('Error deleting documents:', error);
        alert('An unexpected error occurred.');
      }
    },
    //download the phi3 model the endpoint is api/ollama_pull
    async downloadPhi3Model() {
      try {
        const response = await fetch('/django/api/ollama_pull/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': VueCookies.get('csrftoken'),
          },
        });
        const data = await response.json();
        this.phi3Status = data.status;
      } catch (error) {
        console.error('Error downloading Phi3 model:', error);
        alert('An unexpected error occurred.');
      }
    },

    parseCitations(citations) {
      let splitCitations = citations.split('\n> Source ');
      let filteredCitations = splitCitations.filter(citation => citation.trim());
      let mappedCitations = filteredCitations.map((citation, index) => {
        if (index === 0) {
          return citation.trim();
        } else {
          return '> Source ' + citation.trim();
        }
      });
      return mappedCitations;
    },

    parseResponse(response) {
      //if response == "Empty Response" append "No matching documents above the similarity threshold found. Lower the similarity threshold or try a different query."
      if (response == "Empty Response") {
        return "No matching documents above the similarity threshold found. Lower the similarity threshold or try a different query.";
      } else {
        return response;
      }
    },

    //check the existing_documents for an element with a name or content that matches the document_name or document
    checkDocumentDuplicates() {
      return this.existing_documents.some(doc => doc.name === this.document_name || doc.content === this.document);
    },

    clearQuery() {
      this.query = '';
    },

    clearDocumentName() {
      this.document_name = '';
    },

    clearDocument() {
      this.document = '';
    },

    clearAll() {
      this.query = '';
      this.document = '';
      this.document_name = '';
      this.selectedDocuments = [];
      this.responses = {};
    }
  },
  created() {
    this.fetchExistingDocumentNames();
  }
};
</script>

<style scoped>
/* Disabled button style */
button:disabled {
  background-color: #999;
  cursor: not-allowed;
}
</style>
