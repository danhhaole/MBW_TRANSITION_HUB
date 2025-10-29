<template>
  <div class="flex flex-col h-full">
    <!-- Header Section -->
    <div class="flex items-center justify-between px-6 py-5 border-b border-gray-200">
      <div>
        <h2 class="text-lg font-semibold text-gray-900">{{ __('Campaign Templates') }}</h2>
        <p class="mt-1 text-sm text-gray-500">
          {{ __('Create and manage reusable campaign templates for your automation workflows') }}
        </p>
      </div>
      <Button variant="solid" @click="handleCreateTemplate">
        <template #prefix>
          <FeatherIcon name="plus" class="h-4 w-4" />
        </template>
        {{ __('New') }}
      </Button>
    </div>

    <!-- Content Section -->
    <div class="flex-1 overflow-y-auto p-6">
      <CampaignTemplateManagement :isInModal="true" ref="templateManagementRef" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Button, FeatherIcon } from 'frappe-ui'
import CampaignTemplateManagement from '@/pages/CampaignTemplateManagement.vue'

const templateManagementRef = ref(null)

const handleCreateTemplate = () => {
  // Trigger create action in CampaignTemplateManagement component
  if (templateManagementRef.value && templateManagementRef.value.handleCreate) {
    templateManagementRef.value.handleCreate()
  }
}
</script>
