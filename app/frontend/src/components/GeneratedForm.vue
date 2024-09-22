<template>
    <div v-if="formFields.length > 0" class="mb-6">
      <h2 class="text-2xl font-semibold mb-4 text-gray-900">Generated Query Form</h2>
      <form @submit.prevent="submitQueryFromGeneratedForm">
        <div v-for="(field, index) in formFields" :key="index" class="mb-6">
          <!-- Field Rendering Logic -->
          <label :for="field.name" class="block text-gray-700 text-sm font-bold mb-2">
            {{ field.label }}
          </label>
  
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
  
        <!-- Submit Button -->
        <div class="mb-6">
          <button
            type="submit"
            class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Submit Query
          </button>
        </div>
      </form>
  
      <!-- Save Template Button -->
      <div class="mb-6">
        <button
          @click="saveTemplate"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        >
          Save Template
        </button>
      </div>
    </div>
  </template>

<script>
import VueCookies from 'vue-cookies';

export default {
  props: {
    formFields: {
      type: Array,
      required: true,
    },
    baseUrl: {
      type: String,
      required: true,
    },
  },
  methods: {
    async submitQueryFromGeneratedForm() {
      // Collect the form data
      const formData = this.formFields.reduce((acc, field) => {
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

        // Emit the response to the parent component
        this.$emit('responseReceived', data);
      } catch (error) {
        console.error('Error querying API:', error);
        alert('An unexpected error occurred while querying the API.');
      }
    },
    async saveTemplate() {
      try {
        const response = await fetch('/django/api/save_template/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': VueCookies.get('csrftoken'),
          },
          body: JSON.stringify({
            base_url: this.baseUrl,
            form_fields: this.formFields,
          }),
        });
        if (response.ok) {
          alert('Template saved successfully.');
        } else {
          alert('Failed to save template.');
        }
      } catch (error) {
        console.error('Error saving template:', error);
        alert('An unexpected error occurred while saving the template.');
      }
    },
  },
};
</script>

  