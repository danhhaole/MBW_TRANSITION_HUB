<template>
    <div class="sidebar-brand">
      <router-link to="/dashboard" class="brand-link">
        <div class="mb-2 d-flex justify-center align-center" style="width: 434px;">
          <img src="https://mbw.vn/wp-content/uploads/2023/09/logo-1.png" alt="MBW Mira" />
        </div>
        <span v-if="!mini" class="app-title">{{ title }}</span>
      </router-link>
    </div>
  </template>
  
  <script setup>
  defineProps({
    title: { type: String, default: 'MyApp' },
    mini: { type: Boolean, default: false }
  })
  </script>
  
  <style scoped>
  .sidebar-brand {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px 0 12px;
    border-bottom: 1px solid #ddd;
    background-color: #fff;
  }
  .brand-link {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-decoration: none;
  }
  .app-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #222;
  }
  </style>
  