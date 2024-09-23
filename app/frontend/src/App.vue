<template>
  <div id="app">
    <hello-world ></hello-world>
    <app-manager></app-manager>
  </div>
</template>

<script>
import HelloWorld from '@/components/HelloWorld.vue';
import AppManager from '@/components/AppManager.vue';

export default {
  name: 'App',
  components: {
    HelloWorld,
    AppManager,
  },
  data() {
    return {
      currentView: 'hello' // Default view
    };
  },
  methods: {
    switchView(view) {
      this.currentView = view;
    }
  }
};
</script>

<style>
/* Add your styles here */
</style>
