<template>
  <div class="pa-4">
    <h2>Test EasyLinkField</h2>
    
    <div class="mb-4">
      <EasyLinkField 
        v-model="userValue" 
        doctype="User" 
        label="Chọn User"
        placeholder="Tìm user..."
      />
      <p>Selected: {{ userValue }}</p>
    </div>

    <div class="mb-4">
      <EasyLinkField 
        v-model="customerValue" 
        doctype="Customer" 
        label="Chọn Customer"
        placeholder="Tìm customer..."
      />
      <p>Selected: {{ customerValue }}</p>
    </div>

    <div class="mb-4">
      <EasyLinkField 
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
import EasyLinkField from './EasyLinkField.vue'

const userValue = ref('')
const customerValue = ref('')
const companyValue = ref('')
</script> 