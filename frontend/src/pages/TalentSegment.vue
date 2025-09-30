<template>
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
    </LayoutHeader>
  </template>
  
  <script setup>
  import LayoutHeader from '@/components/LayoutHeader.vue'
  import { Breadcrumbs } from 'frappe-ui'
  
  // Translation helper function
  
  
  let title = __('Talent Segments')
  const breadcrumbs = [{ label: title, route: { name: 'Mira Segment' } }]
  </script>
  