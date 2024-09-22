<template>
  <div class="max-w-4xl mx-auto px-4 py-6">
    <h1 class="text-3xl font-extrabold mb-6 text-gray-900">API Documentation Query</h1>

    <!-- API Documentation Input -->
    <div class="mb-6 relative">
      <label for="api_documentation" class="block text-gray-700 text-sm font-bold mb-2">Paste API Documentation</label>
      <textarea
        id="api_documentation"
        v-model="apiDocumentation"
        placeholder="Enter your API documentation"
        class="block w-full bg-white border border-gray-400 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
        rows="6"
      ></textarea>
      <button @click="clearDocumentation" class="absolute right-2 top-8 text-gray-600 hover:text-gray-900">
        &#x2715;
      </button>
    </div>

    <!-- Submit API Documentation -->
    <div class="mb-6">
      <button
        @click="submitApiDocumentation"
        :disabled="isGeneratingForm"
        class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        {{ isGeneratingForm ? 'Generating Form...' : 'Generate Form' }}
      </button>
    </div>

    <!-- Dynamic Form Generated from API -->
    <div v-if="generatedFormFields.length > 0" class="mb-6">
      <h2 class="text-2xl font-semibold mb-4 text-gray-900">Generated Query Form</h2>

      <!-- Dynamically Generated Inputs -->
      <form @submit.prevent="submitQueryFromGeneratedForm">
        <div v-for="(field, index) in generatedFormFields" :key="index" class="mb-6">
          <label :for="field.name" class="block text-gray-700 text-sm font-bold mb-2">{{ field.label }}</label>

          <!-- Text Input -->
          <input
            v-if="field.type === 'text'"
            :id="field.name"
            v-model="field.value"
            type="text"
            :placeholder="field.placeholder || ''"
            class="block w-full bg-white border border-gray-400 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
          />

          <!-- Number Input -->
          <input
            v-else-if="field.type === 'number'"
            :id="field.name"
            v-model.number="field.value"
            type="number"
            :placeholder="field.placeholder || ''"
            class="block w-full bg-white border border-gray-400 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
          />

          <!-- Select Input -->
          <select
            v-else-if="field.type === 'select'"
            :id="field.name"
            v-model="field.value"
            class="block w-full bg-white border border-gray-400 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
          >
            <option v-for="option in field.options" :key="option" :value="option">{{ option }}</option>
          </select>

          <!-- Checkbox Input -->
          <div v-else-if="field.type === 'checkbox'" class="flex items-center">
            <input
              :id="field.name"
              v-model="field.value"
              type="checkbox"
              class="mr-2 leading-tight"
            />
            <span class="text-sm">{{ field.description }}</span>
          </div>

          <!-- Textarea Input -->
          <textarea
            v-else-if="field.type === 'textarea'"
            :id="field.name"
            v-model="field.value"
            :placeholder="field.placeholder || ''"
            class="block w-full bg-white border border-gray-400 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
            rows="4"
          ></textarea>

          <!-- Date Input -->
          <input
            v-else-if="field.type === 'date'"
            :id="field.name"
            v-model="field.value"
            type="date"
            class="block w-full bg-white border border-gray-400 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
          />

          <!-- Fallback for Unsupported Types -->
          <input
            v-else
            :id="field.name"
            v-model="field.value"
            :type="field.type"
            :placeholder="field.placeholder || ''"
            class="block w-full bg-white border border-gray-400 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
          />
        </div>

        <!-- Submit Query Directly to the Third-Party API -->
        <div class="mb-6">
          <button
            type="submit"
            class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Submit Query
          </button>
        </div>
      </form>
    </div>

    <!-- Display Responses and Option to Save -->
    <div v-if="responses.length > 0" class="mb-6">
      <h2 class="text-2xl font-semibold mb-4 text-gray-900">Responses</h2>
      <div v-for="(response, index) in responses" :key="index" class="mb-4 p-4 border border-gray-200 rounded-lg">
        <JsonTree :json="JSON.parse(response)" />
        <!--
        <button
          @click="saveResponse(index)"
          class="mt-2 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        >
          Save Response
        </button>
      -->
      </div>
    </div>
  </div>
</template>

<script>
import VueCookies from 'vue-cookies';
import JsonTree from './JsonTree.vue';

export default {
  components: {
    JsonTree,
  },
  data() {
    return {
      apiDocumentation: '', // Holds the inputted API documentation
      generatedFormFields: [], // Holds the generated form fields from the API
      baseUrl: '', // Holds the base URL for the third-party API
      responses: [], // Holds the responses after the query
      isGeneratingForm: false, // Flag to indicate form generation in progress
    };
  },
  methods: {
    async submitApiDocumentation() {
      // Send the API documentation to the backend to generate a form
      try {
        this.isGeneratingForm = true;
        const response = await fetch('/django/api/query_openai/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': VueCookies.get('csrftoken'),
          },
          body: JSON.stringify({
            prompt: this.apiDocumentation,
          }),
        });
        const data = await response.json();
        if (data.form_fields) {
          // Initialize the value of each field if not provided
          this.generatedFormFields = data.form_fields.map((field) => ({
            ...field,
            value: field.value || (field.type === 'checkbox' ? false : ''),
          }));
          // Set the base URL for the third-party API
          this.baseUrl = data.base_url || '';
        } else if (data.error) {
          alert(`Error: ${data.error}`);
        }
      } catch (error) {
        console.error('Error generating form:', error);
        alert('An unexpected error occurred while generating the form.');
      } finally {
        this.isGeneratingForm = false;
      }
    },

    async submitQueryFromGeneratedForm() {
      // Send the filled form data to your backend
      const formData = this.generatedFormFields.reduce((acc, field) => {
        acc[field.name] = field.value;
        return acc;
      }, {});

      try {
        if (!this.baseUrl) {
          alert('Base URL for the third-party API is not available.');
          return;
        }

        const response = await fetch('/django/api/submit_query/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': VueCookies.get('csrftoken'),
          },
          body: JSON.stringify({
            base_url: this.baseUrl,
            form_data: formData,
          }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        // Handle the data as needed
        this.responses.push(JSON.stringify(data, null, 2));
      } catch (error) {
        console.error('Error querying API:', error);
        alert('An unexpected error occurred while querying the API.');
      }
    },



    async saveResponse(index) {
      try {
        const response = await fetch('/django/save/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': VueCookies.get('csrftoken'),
          },
          body: JSON.stringify({
            response: this.responses[index],
          }),
        });
        if (response.ok) {
          alert('Response saved successfully.');
        } else {
          alert('Failed to save response.');
        }
      } catch (error) {
        console.error('Error saving response:', error);
        alert('An unexpected error occurred while saving the response.');
      }
    },

    clearDocumentation() {
      this.apiDocumentation = '';
    },
  },
};
</script>

<style scoped>
button:disabled {
  background-color: #999;
  cursor: not-allowed;
}
</style>
