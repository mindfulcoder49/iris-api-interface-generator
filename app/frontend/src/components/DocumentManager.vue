<template>
  <div class="max-w-4xl mx-auto px-4 py-6">
    <h1 class="text-3xl font-extrabold mb-6 text-gray-900">API Documentation Query</h1>

    <!-- API Documentation Input -->
    <ApiDocumentationInput
      v-model:apiDocumentation="apiDocumentation"
      @formGenerated="handleFormGenerated"
    />

    <!-- Template Selector -->
    <TemplateSelector @templateLoaded="handleTemplateLoaded" />

    <!-- Dynamic Form Generated from API -->
    <GeneratedForm
      v-if="generatedFormFields.length > 0"
      :formFields="generatedFormFields"
      :baseUrl="baseUrl"
      @responseReceived="handleResponseReceived"
    />

    <!-- Display Responses -->
    <ResponseDisplay :responses="responses" />
  </div>
</template>
<script>
import ApiDocumentationInput from './ApiDocumentationInput.vue';
import GeneratedForm from './GeneratedForm.vue';
import ResponseDisplay from './ResponseDisplay.vue';
import TemplateSelector from './TemplateSelector.vue';

export default {
  components: {
    ApiDocumentationInput,
    GeneratedForm,
    ResponseDisplay,
    TemplateSelector,
  },
  data() {
    return {
      apiDocumentation: '',
      generatedFormFields: [],
      baseUrl: '',
      responses: [],
    };
  },
  methods: {
    handleFormGenerated({ formFields, baseUrl }) {
      // Initialize field values
      this.generatedFormFields = formFields.map((field) => ({
        ...field,
        value: field.value || (field.type === 'checkbox' ? false : ''),
      }));
      this.baseUrl = baseUrl;
    },
    handleTemplateLoaded({ formFields, baseUrl }) {
      // Load the template's form fields and base URL
      this.generatedFormFields = formFields.map((field) => ({
        ...field,
        value: field.value || (field.type === 'checkbox' ? false : ''),
      }));
      this.baseUrl = baseUrl;
    },
    handleResponseReceived(data) {
      this.responses.push(JSON.stringify(data, null, 2));
    },
  },
};
</script>
