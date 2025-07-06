<template>
  <div class="pa-4">
    <h2>Test EasyLinkField</h2>
    
    <div class="mb-4">
      <LinkField 
        v-model="userValue" 
        doctype="User" 
        label="Chọn User"
        placeholder="Tìm user..."
      />
      <p>Selected: {{ userValue }}</p>
    </div>

    <div class="mb-4">
      <LinkField 
        v-model="customerValue" 
        doctype="Campaign" 
        label="Chọn Campaign"
        placeholder="Tìm campaign..."
      />
      <p>Selected: {{ customerValue }}</p>
    </div>

    <div class="mb-4">
      <LinkField 
        v-model="companyValue" 
        doctype="Company" 
        label="Chọn Company"
        placeholder="Tìm company..."
      />
      <p>Selected: {{ companyValue }}</p>
    </div>

    <div class="mb-4">
      <h3>Debug Info</h3>
      <pre>{{ { userValue, customerValue, companyValue } }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LinkField from './LinkField.vue'

const userValue = ref('')
const customerValue = ref('')
const companyValue = ref('')
</script> 