<template>
    <div class="mb-6 relative">
      <label for="api_documentation" class="block text-gray-700 text-sm font-bold mb-2">
        Paste API Documentation
      </label>
      <textarea
        id="api_documentation"
        v-model="localApiDocumentation"
        placeholder="Enter your API documentation"
        class="block w-full bg-white border border-gray-400 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
        rows="6"
      ></textarea>
      <button @click="clearDocumentation" class="absolute right-2 top-8 text-gray-600 hover:text-gray-900">
        &#x2715;
      </button>
      <div class="mt-4">
        <button
          @click="submitApiDocumentation"
          :disabled="isGeneratingForm"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        >
          {{ isGeneratingForm ? 'Generating Form...' : 'Generate Form' }}
        </button>
      </div>
    </div>
  </template>
  <script>
  import VueCookies from 'vue-cookies';
  
  export default {
    props: {
      apiDocumentation: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        localApiDocumentation: this.apiDocumentation,
        isGeneratingForm: false,
      };
    },
    watch: {
      localApiDocumentation(newValue) {
        this.$emit('update:apiDocumentation', newValue);
      },
      apiDocumentation(newValue) {
        this.localApiDocumentation = newValue;
      },
    },
    methods: {
      clearDocumentation() {
        this.localApiDocumentation = '';
      },
      async submitApiDocumentation() {
        this.isGeneratingForm = true;
        try {
          const response = await fetch('/django/api/query_openai/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': VueCookies.get('csrftoken'),
            },
            body: JSON.stringify({
              prompt: this.localApiDocumentation,
            }),
          });
          const data = await response.json();
          if (data.form_fields) {
            this.$emit('formGenerated', {
              formFields: data.form_fields,
              baseUrl: data.base_url || '',
            });
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
    },
  };
  </script>
  