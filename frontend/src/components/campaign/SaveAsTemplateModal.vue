<template>
  <Dialog
    v-model="isOpen"
    :options="{
      title: __('Save as Template'),
      size: 'md'
    }"
  >
    <template #body-content>
      <div class="space-y-4">
        <!-- Icon & Description -->
        <div class="flex items-start space-x-4">
          <div class="flex-shrink-0 w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
            <FeatherIcon name="bookmark" class="w-6 h-6 text-purple-600" />
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-900">
              {{ __('Create a reusable template') }}
            </h3>
            <p class="mt-1 text-sm text-gray-500">
              {{ __('Save this campaign as a template to quickly create similar campaigns in the future.') }}
            </p>
          </div>
        </div>



        <!-- Form -->
        <div class="space-y-4">
          <FormControl
            type="text"
            :label="__('Template Name')"
            v-model="templateName"
            :placeholder="__('Enter a name for your template...')"
            required
          />

          <FormControl
            type="textarea"
            :label="__('Description')"
            v-model="description"
            :placeholder="__('Describe what this template is for...')"
            :rows="3"
          />
        </div>

        <!-- What will be saved -->
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div class="flex items-start space-x-3">
            <FeatherIcon name="info" class="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
            <div class="text-sm text-blue-800">
              <p class="font-medium">{{ __('What will be saved:') }}</p>
              <ul class="mt-2 space-y-1 list-disc list-inside text-blue-700">
                <li>{{ __('Campaign settings and configuration') }}</li>
                <li>{{ __('Social media contents') }}</li>
                <li>{{ __('Automation triggers and flows') }}</li>
                <li>{{ __('Landing page settings') }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </template>

    <template #actions>
      <div class="flex justify-end space-x-3">
        <Button
          variant="outline"
          @click="handleClose"
          :disabled="saving"
        >
          {{ __('Cancel') }}
        </Button>
        <Button
          variant="solid"
          theme="blue"
          @click="handleSave"
          :loading="saving"
          :disabled="!templateName.trim()"
        >
          <template #prefix>
            <FeatherIcon name="bookmark" class="w-4 h-4" />
          </template>
          {{ __('Save Template') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Dialog, Button, FormControl, FeatherIcon, call } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  campaign: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'saved'])

// Translation helper
const __ = (text) => text

// State
const isOpen = ref(false)
const templateName = ref('')
const description = ref('')
const saving = ref(false)

// Computed
const getCampaignIcon = computed(() => {
  const icons = {
    'ATTRACTION': 'target',
    'NURTURING': 'heart',
    'RECRUITMENT': 'users'
  }
  return icons[props.campaign?.type] || 'file-text'
})

const getCampaignTypeLabel = computed(() => {
  const labels = {
    'ATTRACTION': 'Attraction Campaign',
    'NURTURING': 'Nurturing Campaign',
    'RECRUITMENT': 'Recruitment Campaign'
  }
  return labels[props.campaign?.type] || 'Campaign'
})

// Watch modelValue
watch(() => props.modelValue, (val) => {
  isOpen.value = val
  if (val && props.campaign) {
    // Pre-fill template name
    templateName.value = `${props.campaign.campaign_name} Template`
    description.value = `Template created from campaign: ${props.campaign.campaign_name}`
  }
})

watch(isOpen, (val) => {
  emit('update:modelValue', val)
})

// Methods
const handleClose = () => {
  isOpen.value = false
  templateName.value = ''
  description.value = ''
}

const handleSave = async () => {
  if (!templateName.value.trim()) return

  saving.value = true
  try {
    const result = await call('mbw_mira.api.campaign_to_template.save_campaign_as_template', {
      campaign_id: props.campaign.name,
      template_name: templateName.value.trim(),
      description: description.value.trim()
    })

    if (result?.success) {
      emit('saved', result.data)
      handleClose()
    } else {
      console.error('Failed to save template:', result?.error)
    }
  } catch (error) {
    console.error('Error saving template:', error)
  } finally {
    saving.value = false
  }
}
</script>
