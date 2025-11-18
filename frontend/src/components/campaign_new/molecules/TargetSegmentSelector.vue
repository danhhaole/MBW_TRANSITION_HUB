<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="text-center mb-6">
      <h4 class="text-lg font-medium text-gray-900 mb-2">
        {{ title || __("Target Pool") }}
      </h4>
      <p class="text-sm text-gray-600">
        {{ description || __("Choose candidates and configure targeting strategy") }}
      </p>
    </div>

    <!-- Talent Segment Selection (Optional) -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h5 class="text-md font-medium text-gray-900">
            {{ __("Talent Pool") }}
            <span class="text-xs text-gray-500 font-normal ml-2">{{ __("(Optional)") }}</span>
          </h5>
          <p class="text-sm text-gray-600 mt-1">
            {{ __("Start with an existing talent Pool as base") }}
          </p>
        </div>
        <Button
          v-if="hasSegment"
          @click="clearSegment"
          variant="solid"
          :theme="'red'"
          
        >
          {{ __('Clear Pool') }}
        </Button>
      </div>
      
      <!-- Segment Selection -->
      <component 
        :is="PoolConfig" 
        v-model="localConfigData"
        @update:model-value="handleSegmentChange"
      />
    </div>

    <!-- Filter Conditions (Always Show) -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">

      
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

    <!-- Candidate Count -->
    <div class="bg-blue-50 rounded-lg p-4">
      <div class="flex items-center justify-between">
        <div>
          <h5 class="text-md font-medium text-gray-900 mb-2">
            {{ __("Talent Count") }}
          </h5>
          <p class="text-sm text-gray-600 mb-2">
            {{ __("This campaign will be sent to approximately") }}
          </p>
          <div class="text-2xl font-bold text-blue-600">
            {{ loadingCount ? '...' : localCandidateCount }} {{ __("talents") }}
          </div>
        </div>
        <button
          v-if="!loadingCount"
          @click="refreshCount"
          class="text-blue-600 hover:text-blue-700 p-2 rounded-md hover:bg-blue-100 transition-colors"
          :title="__('Refresh count')"
        >
          <FeatherIcon name="refresh-cw" class="h-5 w-5" />
        </button>
        <div v-else class="p-2">
          <FeatherIcon name="loader" class="h-5 w-5 text-blue-600 animate-spin" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { FeatherIcon, call, Button } from 'frappe-ui'
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
  'update:configData',
  'update:conditions',
  'update:candidateCount',
  'validate',
  'change'
])

// Local state
const loadingCount = ref(false)
const localCandidateCount = ref(props.candidateCount)
let debounceTimer = null

const localConfigData = computed({
  get: () => props.configData,
  set: (value) => emit('update:configData', value)
})

const localConditions = computed({
  get: () => props.conditions,
  set: (value) => emit('update:conditions', value)
})

// Check if segment is selected
const hasSegment = computed(() => {
  return localConfigData.value && Object.keys(localConfigData.value).length > 0
})

// Clear segment
const clearSegment = () => {
  emit('update:configData', {})
  debouncedRefreshCount()
}

// Fetch candidate count (combining segment + conditions)
const fetchCandidateCount = async () => {
  loadingCount.value = true
  try {
    // Get count with both segment and conditions combined
    const result = await call('mbw_mira.api.campaign.get_combined_candidate_count', {
      config_data: localConfigData.value,
      conditions: localConditions.value?.value || localConditions.value
    })
    
    const count = result?.count || 0
    localCandidateCount.value = count
    // Emit to parent to persist the count
    emit('update:candidateCount', count)
    console.log(`✅ Candidate count: ${count} (segment: ${hasSegment.value}, conditions: ${localConditions.value?.length || 0})`)
  } catch (error) {
    console.error('❌ Error fetching candidate count:', error)
    localCandidateCount.value = 0
  } finally {
    loadingCount.value = false
  }
}

// Debounced refresh to avoid multiple calls
const debouncedRefreshCount = () => {
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  debounceTimer = setTimeout(() => {
    fetchCandidateCount()
  }, 500)
}

// Refresh count manually (immediate, no debounce)
const refreshCount = () => {
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  fetchCandidateCount()
}

// Handle segment change
const handleSegmentChange = (value) => {
  emit('update:configData', value)
  // Use debounced refresh
  debouncedRefreshCount()
}

// Handlers
const handleConditionsValidate = (isValid) => {
  emit('validate', isValid)
}

const handleConditionsChange = (conditions) => {
  emit('change', conditions)
  // Use debounced refresh
  debouncedRefreshCount()
}

// Watch for prop changes
watch(() => props.candidateCount, (newVal) => {
  localCandidateCount.value = newVal
})

// Watch for config/conditions changes and auto-refresh
watch([localConfigData, localConditions], () => {
  debouncedRefreshCount()
}, { deep: true })

// Translation helper
const __ = (text) => text
</script>

<style scoped>
/* Add any custom styles here */
</style>
