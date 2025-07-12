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
  const __ = (text) => text
  
  let title = __('Talent Segments')
  const breadcrumbs = [{ label: title, route: { name: 'TalentSegment' } }]
  </script>
  