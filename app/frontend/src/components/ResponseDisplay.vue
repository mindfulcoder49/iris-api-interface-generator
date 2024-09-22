<template>
    <div v-if="responses.length > 0" class="mb-6">
      <h2 class="text-2xl font-semibold mb-4 text-gray-900">Responses</h2>
      <div
        v-for="(response, index) in responses"
        :key="index"
        class="mb-4 p-4 border border-gray-200 rounded-lg"
      >
        <JsonTree :json="JSON.parse(response)" />
        <!-- Uncomment if save functionality is needed -->
        <button
          @click="saveResponse(index)"
          class="mt-2 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        >
          Save Response
        </button>
        
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
  props: {
    responses: {
      type: Array,
      required: true,
    },
  },
  methods: {
    async saveResponse(index) {
      try {
        const response = await fetch('/django/api/save_query/', {
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
  },
};
</script>

  