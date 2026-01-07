<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h2 class="text-xl font-semibold text-gray-900">{{ __('Interaction Notes & Reviews') }}</h2>
    </div>

    <!-- Interaction Notes (Latest) -->
    <div class="bg-white rounded-lg border border-gray-200">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">{{ __('Interaction Notes (Latest)') }}</h3>
      </div>
      <div class="p-6">
        <div v-if="talent.interaction_notes" class="prose prose-sm max-w-none">
          <div class="text-gray-700 whitespace-pre-wrap bg-gray-50 p-4 rounded-lg border border-gray-200">
            {{ talent.interaction_notes }}
          </div>
        </div>
        <div v-else class="text-gray-500 italic text-sm">
          {{ __('Interaction Notes') }}
        </div>
      </div>
    </div>

    <!-- General Notes -->
    <div class="bg-white rounded-lg border border-gray-200">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">{{ __('General Notes') }}</h3>
      </div>
      <div class="p-6">
        <div v-if="talent.notes" class="prose prose-sm max-w-none">
          <div class="text-gray-700 whitespace-pre-wrap bg-gray-50 p-4 rounded-lg border border-gray-200">
            {{ talent.notes }}
          </div>
        </div>
        <div v-else class="text-gray-500 italic text-sm">
          {{ __('None') }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  talent: {
    type: Object,
    required: true
  }
})
</script>
