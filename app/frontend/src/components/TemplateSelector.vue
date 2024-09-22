<template>
    <div class="mb-6">
      <label for="template-selector" class="block text-gray-700 text-sm font-bold mb-2">
        Load Saved Template
      </label>
      <select
        id="template-selector"
        v-model="selectedTemplateId"
        @change="loadTemplate"
        class="block w-full bg-white border border-gray-400 px-4 py-2 rounded shadow-sm focus:outline-none focus:shadow-outline"
      >
        <option value="" disabled>
          {{ templates.length > 0 ? 'Select a template' : 'No templates available' }}
        </option>
        <option v-for="template in templates" :key="template.id" :value="template.id">
            {{ template.base_url }} | {{ formatDate(template.created_at) }}
        </option>
      </select>
    </div>
  </template>
  
  <script>
  import VueCookies from 'vue-cookies';
  
  export default {
    data() {
      return {
        templates: [],
        selectedTemplateId: '',
      };
    },
    methods: {
      async fetchTemplates() {
        try {
          const response = await fetch('/django/api/get_templates/', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': VueCookies.get('csrftoken'),
            },
          });
          if (response.ok) {
            this.templates = await response.json();
          } else {
            console.error('Failed to fetch templates');
          }
        } catch (error) {
          console.error('Error fetching templates:', error);
        }
      },
      loadTemplate() {
        const selectedTemplate = this.templates.find(
          (template) => template.id === this.selectedTemplateId
        );
        if (selectedTemplate) {
          // Emit the selected template data to the parent component
          this.$emit('templateLoaded', {
            formFields: selectedTemplate.form_fields,
            baseUrl: selectedTemplate.base_url,
          });
        }
      },
      formatDate(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
      },
    },
    mounted() {
      this.fetchTemplates();
    },
  };
  </script>
  