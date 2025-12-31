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
          <!-- Debug info (remove in production) -->
          <div class="text-xs text-gray-500 mt-1" v-if="false">
            Debug: props={{ props.candidateCount }}, local={{ localCandidateCount }}, loading={{ loadingCount }}
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
import { ref, computed, watch, onMounted } from 'vue'
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
  isUserChange.value = true // Mark as user-initiated change
  emit('update:configData', {})
  debouncedRefreshCount()
}

// Fetch candidate count (combining segment + conditions)
const fetchCandidateCount = async () => {
  const segmentId = localConfigData.value?.selectedSegment || localConfigData.value?.selectedSegment?.value || 'N/A'
  console.log('🔄 [TargetSegmentSelector] fetchCandidateCount called with:', {
    config_data: localConfigData.value,
    selectedSegment: segmentId,
    segmentType: typeof segmentId,
    conditions: localConditions.value?.value || localConditions.value,
    conditionsLength: Array.isArray(localConditions.value) ? localConditions.value.length : (localConditions.value?.value?.length || 0),
    hasSegment: hasSegment.value
  })
  
  loadingCount.value = true
  try {
    // Normalize config_data - API expects selectedSegment as string, not object
    let normalizedConfigData = {}
    if (localConfigData.value && Object.keys(localConfigData.value).length > 0) {
      const selectedSegment = localConfigData.value.selectedSegment
      if (selectedSegment) {
        // Extract value if it's an object, otherwise use as-is
        const segmentValue = typeof selectedSegment === 'object' 
          ? selectedSegment.value 
          : selectedSegment
        normalizedConfigData = {
          selectedSegment: segmentValue
        }
        console.log(`📊 [TargetSegmentSelector] Normalized segment: ${segmentValue} (from ${typeof selectedSegment})`)
      }
    }
    
    // Get count with both segment and conditions combined
    const requestData = {
      config_data: normalizedConfigData,
      conditions: localConditions.value?.value || localConditions.value
    }
    console.log('📤 [TargetSegmentSelector] API request data:', JSON.stringify(requestData, null, 2))
    
    const result = await call('mbw_mira.api.campaign.get_combined_candidate_count', requestData)
    
    console.log('📊 [TargetSegmentSelector] API response:', result)
    console.log(`📊 [TargetSegmentSelector] Segment ID: ${segmentId}, Count from API: ${result?.count || 0}`)
    
    const count = result?.count || 0
    console.log(`🔍 [TargetSegmentSelector] Setting localCandidateCount to: ${count}`)
    localCandidateCount.value = count
    // Emit to parent to persist the count
    emit('update:candidateCount', count)
    console.log(`✅ Candidate count: ${count} talents (segment: ${segmentId}, hasSegment: ${hasSegment.value}, conditions: ${Array.isArray(localConditions.value) ? localConditions.value.length : (localConditions.value?.value?.length || 0)})`)
  } catch (error) {
    console.error('❌ Error fetching candidate count:', error)
    console.error('❌ Error details:', {
      message: error.message,
      segmentId: segmentId,
      configData: localConfigData.value
    })
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
  isUserChange.value = true // Mark as user-initiated change
  emit('update:configData', value)
  // Use debounced refresh
  debouncedRefreshCount()
}

// Handlers
const handleConditionsValidate = (isValid) => {
  emit('validate', isValid)
}

const handleConditionsChange = (conditions) => {
  isUserChange.value = true // Mark as user-initiated change
  emit('change', conditions)
  // Use debounced refresh
  debouncedRefreshCount()
}

// Watch for prop changes
watch(() => props.candidateCount, (newVal, oldVal) => {
  console.log(`🔍 [TargetSegmentSelector] candidateCount prop changed: ${oldVal} -> ${newVal}`)
  localCandidateCount.value = newVal
  console.log(`🔍 [TargetSegmentSelector] localCandidateCount updated to: ${localCandidateCount.value}`)
  
  // Log when candidateCount is loaded from parent (e.g., when editing campaign)
  if (newVal > 0 && (oldVal === 0 || oldVal === null || oldVal === undefined)) {
    console.log(`✅ Candidate count loaded from database: ${newVal} (segment: ${hasSegment.value}, conditions: ${localConditions.value?.length || 0})`)
  }
}, { immediate: true })

// Log on mount if candidateCount already has value (when editing existing campaign)
onMounted(() => {
  console.log('🔍 [TargetSegmentSelector] Component mounted with props:', {
    candidateCount: props.candidateCount,
    configData: props.configData,
    conditions: props.conditions,
    hasSegment: hasSegment.value,
    localCandidateCount: localCandidateCount.value,
    selectedSegment: props.configData?.selectedSegment,
    selectedSegmentValue: typeof props.configData?.selectedSegment === 'object' 
      ? props.configData?.selectedSegment?.value 
      : props.configData?.selectedSegment
  })
  
  if (props.candidateCount > 0) {
    console.log(`✅ Candidate count loaded from database (on mount): ${props.candidateCount} (segment: ${hasSegment.value}, conditions: ${localConditions.value?.length || 0})`)
  } else {
    console.log(`⚠️ [TargetSegmentSelector] candidateCount is 0 on mount, hasSegment: ${hasSegment.value}`)
    
    // If there's a segment selected but no count, fetch it automatically
    // Check both object format {value: '...', label: '...'} and string format
    const segmentValue = typeof props.configData?.selectedSegment === 'object' 
      ? props.configData?.selectedSegment?.value 
      : props.configData?.selectedSegment
    
    if (hasSegment.value && segmentValue) {
      console.log(`🔄 [TargetSegmentSelector] Segment found but no count, auto-fetching...`)
      console.log(`📊 [TargetSegmentSelector] Selected segment: ${segmentValue}`)
      console.log(`📊 [TargetSegmentSelector] Segment format: ${typeof props.configData?.selectedSegment}`)
      // Use a small delay to ensure props are fully set
      setTimeout(() => {
        console.log(`🔄 [TargetSegmentSelector] Executing auto-fetch after delay...`)
        fetchCandidateCount()
      }, 500)
    } else {
      console.log(`⏭️ [TargetSegmentSelector] No segment or segment value, skipping auto-fetch`)
      console.log(`   hasSegment: ${hasSegment.value}, segmentValue: ${segmentValue}`)
    }
  }
})

// Track if this is a user-initiated change vs prop update
const isUserChange = ref(false)

// Watch for config/conditions changes and auto-refresh
// Only fetch if change was initiated by user (not from props update)
watch([localConfigData, localConditions], ([newConfig, newConditions], [oldConfig, oldConditions]) => {
  const oldHasSegment = oldConfig && Object.keys(oldConfig).length > 0 && oldConfig.selectedSegment
  const newHasSegment = newConfig && Object.keys(newConfig).length > 0 && newConfig.selectedSegment
  const segmentJustLoaded = newHasSegment && !oldHasSegment
  
  console.log('🔍 [TargetSegmentSelector] configData or conditions changed:', {
    configData: newConfig,
    selectedSegment: newConfig?.selectedSegment,
    oldConfig: oldConfig,
    oldHasSegment,
    newHasSegment,
    segmentJustLoaded,
    conditions: newConditions,
    isUserChange: isUserChange.value,
    hasSegment: hasSegment.value,
    localCandidateCount: localCandidateCount.value
  })
  
  // Only auto-refresh if this is a user-initiated change
  if (isUserChange.value) {
    console.log('🔄 [TargetSegmentSelector] User change detected, fetching count...')
  debouncedRefreshCount()
    isUserChange.value = false // Reset flag
  } else {
    // Props update - check if we need to auto-fetch
    // Get segment value (handle both object and string format)
    const newSegmentValue = typeof newConfig?.selectedSegment === 'object' 
      ? newConfig?.selectedSegment?.value 
      : newConfig?.selectedSegment
    const oldSegmentValue = typeof oldConfig?.selectedSegment === 'object' 
      ? oldConfig?.selectedSegment?.value 
      : oldConfig?.selectedSegment
    
    // Case 1: Segment was just loaded (from empty to having segment)
    if (segmentJustLoaded && localCandidateCount.value === 0) {
      console.log('🔄 [TargetSegmentSelector] Segment loaded from props but count is 0, auto-fetching...')
      console.log(`📊 [TargetSegmentSelector] Selected segment: ${newSegmentValue}`)
      console.log(`📊 [TargetSegmentSelector] Segment type: ${typeof newConfig?.selectedSegment}`)
      setTimeout(() => {
        fetchCandidateCount()
      }, 300)
    } 
    // Case 2: Segment exists but count is still 0 (might have been missed on mount or previous update)
    // Check if hasSegment changed from false to true (even if oldConfig was empty object)
    else if (hasSegment.value && newSegmentValue && localCandidateCount.value === 0 && props.candidateCount === 0) {
      // Only fetch if segment value changed or segment was just set
      const segmentChanged = !oldSegmentValue || oldSegmentValue !== newSegmentValue
      if (segmentChanged) {
        console.log('🔄 [TargetSegmentSelector] Segment exists but count is 0, auto-fetching (fallback)...')
        console.log(`📊 [TargetSegmentSelector] Selected segment: ${newSegmentValue}`)
        console.log(`📊 [TargetSegmentSelector] Old segment: ${oldSegmentValue}, New segment: ${newSegmentValue}`)
        console.log(`📊 [TargetSegmentSelector] props.candidateCount: ${props.candidateCount}, localCandidateCount: ${localCandidateCount.value}`)
        setTimeout(() => {
          fetchCandidateCount()
        }, 500)
      } else {
        console.log('⏭️ [TargetSegmentSelector] Segment unchanged, skipping fetch')
      }
    } 
    else {
      console.log('⏭️ [TargetSegmentSelector] Props update (not user change), skipping fetch')
      console.log('   Reason:', {
        segmentJustLoaded,
        hasSegment: newHasSegment,
        hasSegmentValue: hasSegment.value,
        newSegmentValue,
        oldSegmentValue,
        localCandidateCount: localCandidateCount.value,
        propsCandidateCount: props.candidateCount
      })
    }
  }
}, { deep: true })

// Translation helper
const __ = (text) => text
</script>

<style scoped>
/* Add any custom styles here */
</style>
