<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="text-center mb-6">
      <h4 class="text-lg font-medium text-gray-900 mb-2">
        {{ title || __("Target Segment") }}
      </h4>
      <p class="text-sm text-gray-600">
        {{ description || __("Choose candidates and configure targeting strategy") }}
      </p>
    </div>

    <!-- Segment Selection -->
    <div class="bg-gray-50 rounded-lg p-6">
      <h5 class="text-md font-medium text-gray-900 mb-4">
        {{ __("Select Candidates") }}
      </h5>
      <p class="text-sm text-gray-600 mb-4">
        {{ __("Which candidates do you want to target in this campaign?") }}
      </p>
      
      <!-- Segment Options -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <!-- Choose Candidates (Segment) -->
        <div 
          class="border rounded-lg p-4 bg-white cursor-pointer transition-colors"
          :class="localMode === 'segment' ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' : 'border-gray-200 hover:border-blue-300'"
          @click="localMode = 'segment'"
        >
          <div class="text-center">
            <div class="flex items-center justify-center w-12 h-12 rounded-full mx-auto mb-3"
                 :class="localMode === 'segment' ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'">
              <FeatherIcon name="users" class="h-6 w-6" />
            </div>
            <h6 class="text-sm font-semibold mb-1"
                :class="localMode === 'segment' ? 'text-blue-900' : 'text-gray-900'">
              {{ __("Choose Candidates (Segment)") }}
            </h6>
            <p class="text-xs text-gray-600">
              {{ __("Use existing candidate segments") }}
            </p>
          </div>
        </div>

        <!-- Custom Conditions -->
        <div 
          class="border rounded-lg p-4 bg-white cursor-pointer transition-colors"
          :class="localMode === 'conditions' ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' : 'border-gray-200 hover:border-blue-300'"
          @click="localMode = 'conditions'"
        >
          <div class="text-center">
            <div class="flex items-center justify-center w-12 h-12 rounded-full mx-auto mb-3"
                 :class="localMode === 'conditions' ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'">
              <FeatherIcon name="filter" class="h-6 w-6" />
            </div>
            <h6 class="text-sm font-semibold mb-1"
                :class="localMode === 'conditions' ? 'text-blue-900' : 'text-gray-900'">
              {{ __("Custom Conditions") }}
            </h6>
            <p class="text-xs text-gray-600">
              {{ __("Create custom filtering conditions") }}
            </p>
          </div>
        </div>
      </div>

      <!-- Segment Selection Content -->
      <div v-if="localMode === 'segment'">
        <!-- Use existing PoolConfig component for segment selection -->
        <component :is="PoolConfig" v-model="localConfigData" />
      </div>

      <!-- Custom Conditions Content -->
      <div v-else-if="localMode === 'conditions'" class="space-y-4">
        <ConditionsBuilder
          v-model="localConditions"
          doctype="Mira Talent"
          :title="__('Campaign Target Conditions')"
          :description="__('Define conditions to filter candidates who will receive your campaign')"
          :show-preview="false"
          :validate-on-change="true"
          @validate="handleConditionsValidate"
          @change="handleConditionsChange"
        />
      </div>
    </div>

    <!-- Candidate Count -->
    <div class="bg-blue-50 rounded-lg p-4">
      <h5 class="text-md font-medium text-gray-900 mb-2">
        {{ __("Candidate Count") }}
      </h5>
      <p class="text-sm text-gray-600 mb-2">
        {{ __("This campaign will be sent to approximately") }}
      </p>
      <div class="text-2xl font-bold text-blue-600">
        {{ candidateCount }} {{ __("candidates") }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { FeatherIcon } from 'frappe-ui'
import PoolConfig from '@/components/campaign/PoolConfig.vue'
import ConditionsBuilder from '@/components/ConditionsFilter/ConditionsBuilder.vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  selectionMode: {
    type: String,
    default: 'segment' // 'segment' or 'conditions'
  },
  configData: {
    type: Object,
    default: () => ({})
  },
  conditions: {
    type: Array,
    default: () => []
  },
  candidateCount: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits([
  'update:selectionMode',
  'update:configData',
  'update:conditions',
  'validate',
  'change'
])

// Local state
const localMode = computed({
  get: () => props.selectionMode,
  set: (value) => emit('update:selectionMode', value)
})

const localConfigData = computed({
  get: () => props.configData,
  set: (value) => emit('update:configData', value)
})

const localConditions = computed({
  get: () => props.conditions,
  set: (value) => emit('update:conditions', value)
})

// Handlers
const handleConditionsValidate = (isValid) => {
  emit('validate', isValid)
}

const handleConditionsChange = (conditions) => {
  emit('change', conditions)
}

// Translation helper
const __ = (text) => text
</script>

<style scoped>
/* Add any custom styles here */
</style>
