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
  let title = 'TalentSegment'
  const breadcrumbs = [{ label: title, route: { name: 'TalentSegment' } }]
  </script>
  