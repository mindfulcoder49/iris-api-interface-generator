<template>
    <div class="json-tree">
      <ul>
        <li v-for="(value, key) in json" :key="key">
          <span @click="toggleCollapse(key)">
            <strong>{{ key }}: </strong>
            <template v-if="isObjectOrArray(value)">
              <span class="toggle">
                [{{ collapsed[key] ? '...' : (Array.isArray(value) ? 'Array' : 'Object') }}]
              </span>
            </template>
            <template v-else>
              <span>{{ formatValue(value) }}</span>
            </template>
          </span>
          <div v-if="!collapsed[key] && isObjectOrArray(value)" class="nested">
            <JsonTree :json="value" v-if="isObjectOrArray(value)" />
          </div>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'JsonTree',
    props: {
      json: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        collapsed: {} // Track which fields are collapsed
      };
    },
    methods: {
      isObjectOrArray(value) {
        return typeof value === 'object' && value !== null;
      },
      formatValue(value) {
        if (typeof value === 'string') {
          return `"${value}"`; // Add quotes around strings
        }
        return value;
      },
      toggleCollapse(key) {
        // Toggle collapsed state in Vue 3
        this.collapsed[key] = !this.collapsed[key];
      }
    }
  };
  </script>
  
  <style scoped>
  .json-tree ul {
    list-style-type: none;
    padding-left: 20px;
  }
  
  .nested {
    margin-left: 20px;
  }
  
  span {
    cursor: pointer;
  }
  
  .toggle {
    color: blue;
    cursor: pointer;
  }
  </style>
  