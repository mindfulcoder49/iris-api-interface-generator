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
      <h1 class="text-4xl font-extrabold text-gray-900 mb-4">How to Use the API Query Tool</h1>
      <!-- Explanation -->
      <p class="text-gray-700 mb-4">
        Welcome to the API Query Tool! This application allows you to interact with third-party APIs by generating dynamic forms based on their documentation. Follow the steps below to get started:
      </p>
      <ol class="list-decimal list-inside text-gray-700 mb-4">
        <li class="mb-2">
          <strong>Paste API Documentation:</strong> Copy the API documentation (e.g., from Swagger, API docs, or OpenAPI specifications) and paste it into the "Paste API Documentation" textarea provided.
        </li>
        <li class="mb-2">
          <strong>Generate Form:</strong> Click on the "Generate Form" button. The application will process the API documentation and generate a dynamic form with fields corresponding to the API's parameters.
        </li>
        <li class="mb-2">
          <strong>Fill Out the Form:</strong> Enter the required information into the generated form fields. These fields represent the parameters needed to make a request to the API.
        </li>
        <li class="mb-2">
          <strong>Submit Query:</strong> Click the "Submit Query" button to send your request directly to the third-party API. The response from the API will be displayed below the form.
        </li>
        <li class="mb-2">
          <strong>Save Response:</strong> If you wish to save the API's response for future reference, click the "Save Response" button. This will store the response in your application.
        </li>
      </ol>
      <p class="text-gray-700">
        You can toggle these instructions at any time by clicking the "Hide Instructions" or "Show Instructions" button above.
      </p>
    </div>
  </div>
  <div v-if="showInstructions">
    <button @click="hideInstructions" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4">Hide Instructions</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showInstructions: true,
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
