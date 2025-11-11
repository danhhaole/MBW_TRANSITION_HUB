<template>
  <div v-if="show" class="fixed inset-0 bg-white z-[9] flex flex-col">
    <!-- Header -->
    <div class="border-b border-gray-200 bg-white px-6 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <button
            @click="closeWizard"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <FeatherIcon name="x" class="h-5 w-5" />
          </button>
          <div>
            <h2 class="text-lg font-semibold text-gray-900">
              {{ campaignData.campaign_name || __('New Nurturing Campaign') }}
            </h2>
            <p class="text-sm text-gray-500">
              {{ __('Step') }} {{ currentStep }} {{ __('of') }} {{ totalSteps }}
            </p>
          </div>
        </div>

        <div class="flex items-center space-x-3">
          <Button
            v-if="currentStep > 1"
            @click="prevStep"
            variant="outline"
          >
            <FeatherIcon name="arrow-left" class="h-4 w-4 mr-2" />
            {{ __('Back') }}
          </Button>

          <Button
            @click="saveDraft"
            variant="outline"
            :loading="saving"
          >
            <FeatherIcon name="save" class="h-4 w-4 mr-2" />
            {{ __('Save Draft') }}
          </Button>

          <Button
            v-if="currentStep < totalSteps"
            @click="nextStep"
            :disabled="!canProceed"
          >
            {{ __('Continue') }}
            <FeatherIcon name="arrow-right" class="h-4 w-4 ml-2" />
          </Button>

          <Button
            v-else
            @click="finalizeCampaign"
            :loading="finalizing"
            variant="solid"
          >
            <FeatherIcon name="check" class="h-4 w-4 mr-2" />
            {{ __('Activate Campaign') }}
          </Button>
        </div>
      </div>
    </div>

    <!-- Progress Stepper -->
    <div class="border-b border-gray-200 bg-gray-50 px-6 py-4">
      <div class="flex items-center justify-between max-w-4xl mx-auto">
        <div
          v-for="(step, index) in steps"
          :key="index"
          class="flex items-center"
          :class="{ 'flex-1': index < steps.length - 1 }"
        >
          <div class="flex items-center">
            <div
              class="flex items-center justify-center w-8 h-8 rounded-full border-2 transition-all"
              :class="[
                currentStep > index + 1
                  ? 'bg-green-600 border-green-600 text-white'
                  : currentStep === index + 1
                  ? 'bg-white border-green-600 text-green-600'
                  : 'bg-white border-gray-300 text-gray-400'
              ]"
            >
              <FeatherIcon
                v-if="currentStep > index + 1"
                name="check"
                class="h-4 w-4"
              />
              <span v-else class="text-sm font-medium">{{ index + 1 }}</span>
            </div>
            <span
              class="ml-2 text-sm font-medium"
              :class="
                currentStep >= index + 1 ? 'text-gray-900' : 'text-gray-400'
              "
            >
              {{ step.title }}
            </span>
          </div>
          <div
            v-if="index < steps.length - 1"
            class="flex-1 h-0.5 mx-4"
            :class="
              currentStep > index + 1 ? 'bg-green-600' : 'bg-gray-300'
            "
          />
        </div>
      </div>
    </div>

    <!-- Content Area -->
    <div class="flex-1 overflow-y-auto bg-gray-50">
      <div class="max-w-4xl mx-auto px-6 py-8">
        <!-- Step 1: Campaign Information & Target Segment -->
        <CampaignStep1
          v-if="currentStep === 1"
          :campaign-name="campaignData.campaign_name"
          :objective="campaignData.objective"
          :selection-mode="campaignData.selection_mode"
          :config-data="campaignData.config_data"
          :conditions="campaignData.conditions"
          :candidate-count="campaignData.candidate_count"
          :show-error="showValidationError"
          @update:campaign-name="campaignData.campaign_name = $event"
          @update:objective="campaignData.objective = $event"
          @update:selection-mode="campaignData.selection_mode = $event"
          @update:config-data="campaignData.config_data = $event"
          @update:conditions="campaignData.conditions = $event"
          @validate="handleValidate"
          @change="handleConditionsChange"
        />

        <!-- Placeholder steps -->
        <div v-else class="bg-white rounded-lg border border-gray-200 p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            {{ steps[currentStep - 1].title }}
          </h3>
          <p class="text-gray-600">
            {{ __('This step will be implemented soon') }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Button, FeatherIcon } from 'frappe-ui'
import CampaignStep1 from '@/components/campaign_new/nurturing/Step1_CampaignInfo.vue'
import { useCampaignStore } from '@/stores/campaign'
import { useToast } from '@/composables/useToast'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  campaignType: {
    type: String,
    default: 'NURTURING'
  }
})

const emit = defineEmits(['close', 'success'])

const campaignStore = useCampaignStore()
const toast = useToast()

const currentStep = ref(1)
const saving = ref(false)
const finalizing = ref(false)
const showValidationError = ref(false)

const campaignData = ref({
  campaign_name: '',
  objective: '',
  selection_mode: 'segment',
  config_data: {},
  conditions: [],
  candidate_count: 0,
  channel: '',
  type: props.campaignType, // 'NURTURING'
  status: 'Draft'
})

const steps = ref([
  { title: __('Campaign Info'), key: 'info' },
  { title: __('Audience'), key: 'audience' },
  { title: __('Content'), key: 'content' },
  { title: __('Review'), key: 'review' }
])

const totalSteps = computed(() => steps.value.length)

const canProceed = computed(() => {
  if (currentStep.value === 1) {
    return (
      campaignData.value.campaign_name?.trim() &&
      campaignData.value.objective?.trim()
      // selection_mode and config_data/conditions are optional
    )
  }
  return true
})

const handleValidate = (isValid) => {
  console.log('Conditions validation:', isValid)
}

const handleConditionsChange = (conditions) => {
  console.log('Conditions changed:', conditions)
}

const closeWizard = () => {
  if (confirm(__('Are you sure you want to close? Unsaved changes will be lost.'))) {
    emit('close')
  }
}

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
    showValidationError.value = false
  }
}

const nextStep = async () => {
  if (!canProceed.value) {
    showValidationError.value = true
    toast.error(__('Please fill in all required fields'))
    return
  }

  showValidationError.value = false
  await saveDraft()
  
  if (currentStep.value < totalSteps.value) {
    currentStep.value++
  }
}

const saveDraft = async () => {
  saving.value = true
  try {
    const result = await campaignStore.submitNewCampaign({
      ...campaignData.value,
      status: 'DRAFT'
    })

    if (result.success) {
      toast.success(__('Draft saved successfully'))
      // Update campaign ID if it's a new campaign
      if (result.data?.name) {
        campaignData.value.name = result.data.name
      }
    } else {
      toast.error(result.error || __('Failed to save draft'))
    }
  } catch (error) {
    console.error('Error saving draft:', error)
    toast.error(__('An error occurred while saving'))
  } finally {
    saving.value = false
  }
}

const finalizeCampaign = async () => {
  if (!canProceed.value) {
    showValidationError.value = true
    toast.error(__('Please complete all required fields'))
    return
  }

  finalizing.value = true
  try {
    const result = await campaignStore.updateCampaign(campaignData.value.name, {
      ...campaignData.value,
      status: 'Active'
    })

    if (result.success) {
      toast.success(__('Campaign activated successfully!'))
      emit('success', result.data)
      emit('close')
    } else {
      toast.error(result.error || __('Failed to activate campaign'))
    }
  } catch (error) {
    console.error('Error activating campaign:', error)
    toast.error(__('An error occurred while activating campaign'))
  } finally {
    finalizing.value = false
  }
}
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
