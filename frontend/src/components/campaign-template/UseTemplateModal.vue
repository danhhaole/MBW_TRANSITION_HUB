<template>
  <Dialog
    v-model="isOpen"
    :options="{
      title: __('Use Template'),
      size: 'lg'
    }"
  >
    <template #body-content>
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600">{{ __('Loading template...') }}</span>
      </div>
      
      <div v-else-if="previewData" class="space-y-6">
        <!-- Template Header -->
        <div class="flex items-start space-x-4">
          <div 
            v-if="previewData.thumbnail"
            class="w-20 h-20 rounded-lg overflow-hidden flex-shrink-0"
          >
            <img 
              :src="previewData.thumbnail" 
              :alt="previewData.template_name"
              class="w-full h-full object-cover"
            />
          </div>
          <div 
            v-else 
            class="w-20 h-20 rounded-lg flex-shrink-0 flex items-center justify-center"
            :class="getTypeColor(previewData.campaign_type)"
          >
            <FeatherIcon :name="getTypeIcon(previewData.campaign_type)" class="w-8 h-8 text-white" />
          </div>
          
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-gray-900">{{ previewData.template_name }}</h3>
            <div class="flex items-center space-x-2 mt-1">
              <span 
                class="px-2 py-0.5 text-xs font-medium rounded-full"
                :class="getTypeBadgeClass(previewData.campaign_type)"
              >
                {{ previewData.campaign_type }}
              </span>
              <span v-if="previewData.is_premium" class="px-2 py-0.5 text-xs font-medium rounded-full bg-yellow-100 text-yellow-800">
                Premium
              </span>
            </div>
            <p v-if="previewData.description" class="text-sm text-gray-600 mt-2">
              {{ previewData.description }}
            </p>
          </div>
        </div>

        <!-- Template Stats -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-gray-50 rounded-lg p-3 text-center">
            <div class="text-2xl font-bold text-blue-600">{{ previewData.social_contents_count || 0 }}</div>
            <div class="text-xs text-gray-500">{{ __('Social Contents') }}</div>
          </div>
          <div class="bg-gray-50 rounded-lg p-3 text-center">
            <div class="text-2xl font-bold text-green-600">{{ previewData.triggers_count || 0 }}</div>
            <div class="text-xs text-gray-500">{{ __('Triggers') }}</div>
          </div>
          <div class="bg-gray-50 rounded-lg p-3 text-center">
            <div class="text-2xl font-bold" :class="previewData.has_landing_page ? 'text-green-600' : 'text-gray-400'">
              <FeatherIcon :name="previewData.has_landing_page ? 'check-circle' : 'x-circle'" class="w-6 h-6 mx-auto" />
            </div>
            <div class="text-xs text-gray-500">{{ __('Landing Page') }}</div>
          </div>
          <div class="bg-gray-50 rounded-lg p-3 text-center">
            <div class="text-2xl font-bold text-purple-600">{{ previewData.usage_count || 0 }}</div>
            <div class="text-xs text-gray-500">{{ __('Times Used') }}</div>
          </div>
        </div>

        <!-- Campaign Name Input -->
        <div class="space-y-2">
          <FormControl
            type="text"
            :label="__('Campaign Name')"
            v-model="campaignName"
            :placeholder="__('Enter campaign name...')"
            required
          />
        </div>

        <!-- Info Box -->
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div class="flex items-start space-x-3">
            <FeatherIcon name="info" class="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
            <div class="text-sm text-blue-800">
              <p class="font-medium">{{ __('What will be created:') }}</p>
              <ul class="mt-1 list-disc list-inside space-y-1">
                <li>{{ __('A new {0} campaign', [previewData.campaign_type]) }}</li>
                <li v-if="previewData.social_contents_count > 0">
                  {{ __('Copy {0} social content(s)', [previewData.social_contents_count]) }}
                </li>
                <li v-if="previewData.has_landing_page">{{ __('Link to landing page') }}</li>
                <li v-if="previewData.has_triggers">{{ __('Flow configuration (triggers & actions)') }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="text-center py-12 text-gray-500">
        {{ __('Failed to load template preview') }}
      </div>
    </template>
    
    <template #actions>
      <div class="flex justify-end space-x-3">
        <Button variant="outline" @click="close">
          {{ __('Cancel') }}
        </Button>
        <Button 
          theme="blue" 
          @click="createCampaign"
          :loading="creating"
          :disabled="!campaignName.trim() || !previewData"
        >
          <template #prefix>
            <FeatherIcon name="play" class="w-4 h-4" />
          </template>
          {{ __('Create Campaign') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Dialog, Button, FeatherIcon, FormControl, call } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  template: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'created'])

// State
const isOpen = ref(false)
const loading = ref(false)
const creating = ref(false)
const previewData = ref(null)
const campaignName = ref('')

// Translation helper
const __ = (text, args) => {
  if (args) {
    return text.replace(/{(\d+)}/g, (match, index) => args[index] || match)
  }
  return text
}

// Watch modelValue
watch(() => props.modelValue, (val) => {
  isOpen.value = val
  if (val && props.template) {
    loadPreview()
  }
})

// Watch template changes - in case template is set after modal opens
watch(() => props.template, (val) => {
  if (val && isOpen.value && !previewData.value) {
    loadPreview()
  }
})

watch(isOpen, (val) => {
  emit('update:modelValue', val)
  if (!val) {
    // Reset state when closing
    previewData.value = null
    campaignName.value = ''
  }
})

// Load template preview
const loadPreview = async () => {
  if (!props.template?.name) return
  
  loading.value = true
  try {
    const result = await call('mbw_mira.api.campaign_from_template.get_template_preview', {
      template_id: props.template.name
    })
    
    if (result?.success) {
      previewData.value = result.data
      // Set default campaign name
      campaignName.value = `${result.data.template_name} - ${new Date().toLocaleDateString()}`
    }
  } catch (error) {
    console.error('Error loading template preview:', error)
  } finally {
    loading.value = false
  }
}

// Create campaign
const createCampaign = async () => {
  if (!campaignName.value.trim() || !previewData.value) return
  
  creating.value = true
  try {
    const result = await call('mbw_mira.api.campaign_from_template.create_campaign_from_template', {
      template_id: previewData.value.template_id,
      campaign_name: campaignName.value.trim()
    })
    
    if (result?.success) {
      emit('created', {
        campaign_id: result.data.campaign_id,
        campaign_type: result.data.campaign_type,
        campaign_name: result.data.campaign_name
      })
      close()
    } else {
      console.error('Failed to create campaign:', result?.error)
    }
  } catch (error) {
    console.error('Error creating campaign:', error)
  } finally {
    creating.value = false
  }
}

// Close modal
const close = () => {
  isOpen.value = false
}

// Helper functions
const getTypeIcon = (type) => {
  const icons = {
    'ATTRACTION': 'users',
    'NURTURING': 'mail',
    'RECRUITMENT': 'target'
  }
  return icons[type] || 'file'
}

const getTypeColor = (type) => {
  const colors = {
    'ATTRACTION': 'bg-blue-500',
    'NURTURING': 'bg-green-500',
    'RECRUITMENT': 'bg-purple-500'
  }
  return colors[type] || 'bg-gray-500'
}

const getTypeBadgeClass = (type) => {
  const classes = {
    'ATTRACTION': 'bg-blue-100 text-blue-800',
    'NURTURING': 'bg-green-100 text-green-800',
    'RECRUITMENT': 'bg-purple-100 text-purple-800'
  }
  return classes[type] || 'bg-gray-100 text-gray-800'
}
</script>
