<template>
  <div v-if="show" class="fixed inset-0 bg-white z-50 flex flex-col">
    <!-- Header -->
    <CampaignWizardHeader
      :campaign-name="campaignData.campaign_name"
      :current-step="currentStep"
      :total-steps="steps.length"
      :loading="loading"
      :saving="draftCampaignLoading"
      :finalizing="activating"
      :can-save="true"
      :can-proceed="canProceed"
      :can-finalize="currentStep === steps.length"
      @exit="closeWizard"
      @back="prevStep"
      @save="saveDraft"
      @save-and-continue="nextStep"
      @finalize="finalizeCampaign"
      @update:campaign-name="updateCampaignName"
    />

    <!-- Stepper -->
    <CampaignWizardStepper
      :steps="steps"
      :current-step="currentStep"
    />

    <!-- Content -->
    <CampaignWizardContent :current-step="currentStep">
      <template #default="{ currentStep: step }">
        <div class="space-y-6">
          <!-- Step 1: Campaign Information -->
          <div v-if="step === 1" class="space-y-4">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">Campaign Information</h2>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Campaign Name <span class="text-red-500">*</span>
              </label>
              <input
                v-model="campaignData.campaign_name"
                type="text"
                placeholder="Example: React Candidate Nurturing Q4/2024"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                :class="{
                  'border-red-500': !campaignData.campaign_name && currentStep > 1,
                }"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select
                v-model="campaignData.status"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              >
                <option value="DRAFT">DRAFT</option>
                <option value="ACTIVE">ACTIVE</option>
                <option value="PAUSED">PAUSED</option>
                <option value="ARCHIVED">ARCHIVED</option>
              </select>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Start Date/Time
                </label>
                <input
                  v-model="campaignData.start_date"
                  type="datetime-local"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  End Date/Time
                </label>
                <input
                  v-model="campaignData.end_date"
                  type="datetime-local"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Campaign Type <span class="text-red-500">*</span>
              </label>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div
                  v-for="type in campaignTypes"
                  :key="type.value"
                  class="border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md"
                  :class="
                    campaignData.type === type.value
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  "
                  @click="campaignData.type = type.value"
                >
                  <div class="flex items-center">
                    <div
                      class="flex items-center justify-center w-8 h-8 rounded-full mr-3"
                      :class="
                        campaignData.type === type.value
                          ? 'bg-blue-100 text-blue-600'
                          : 'bg-gray-100 text-gray-400'
                      "
                    >
                      <FeatherIcon :name="type.icon" class="h-4 w-4" />
                    </div>
                    <div>
                      <div
                        class="text-sm font-medium"
                        :class="
                          campaignData.type === type.value
                            ? 'text-blue-900'
                            : 'text-gray-900'
                        "
                      >
                        {{ type.label }}
                      </div>
                      <div class="text-xs text-gray-500">
                        {{ type.description }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Objective <span class="text-red-500">*</span>
              </label>
              <textarea
                v-model="campaignData.description"
                rows="3"
                placeholder="Brief description of campaign purpose..."
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                :class="{
                  'border-red-500': !campaignData.description && currentStep > 1,
                }"
              />
            </div>
          </div>

          <!-- Step 2: Select Source -->
          <div v-if="step === 2" class="space-y-4">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">Select Data Source</h2>
            <p class="text-gray-600 mb-6">Choose how you want to import candidates for this campaign.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div
                v-for="source in sources"
                :key="source.key"
                class="border rounded-lg p-6 text-center cursor-pointer transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg"
                :class="
                  selectedSource === source.key
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                "
                @click="selectSource(source.key)"
              >
                <FeatherIcon
                  :name="source.icon"
                  class="h-8 w-8 mx-auto mb-3"
                  :class="
                    selectedSource === source.key
                      ? 'text-blue-600'
                      : 'text-gray-400'
                  "
                />
                <div class="text-sm font-medium mb-1 text-gray-900">
                  {{ source.title }}
                </div>
                <div class="text-xs text-gray-500">
                  {{ source.description }}
                </div>
              </div>
            </div>
          </div>

          <!-- Step 3: Target Segment -->
          <div v-if="step === 3" class="space-y-4">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">Select Target Segment</h2>
            <p class="text-gray-600 mb-6">Choose the talent segment you want to target with this campaign.</p>
            
            <div class="bg-gray-50 rounded-lg p-6">
              <p class="text-center text-gray-500">Target segment selection will be implemented here.</p>
            </div>
          </div>

          <!-- Step 4: Create Triggers -->
          <div v-if="step === 4" class="space-y-6">
            <!-- Debug Info -->
            <div class="bg-yellow-50 border border-yellow-200 rounded p-3 text-sm">
              <strong>Debug:</strong> 
              Step = {{ step }}, 
              selectedWorkflowTemplate = {{ selectedWorkflowTemplate?.name || 'null' }}, 
              showWorkflowBuilder = {{ showWorkflowBuilder }}
            </div>
            
            <WorkflowTemplateSelector
              v-if="!selectedWorkflowTemplate && !showWorkflowBuilder"
              v-model="selectedWorkflowTemplate"
              @continue="onTemplateSelected"
              @back="prevStep"
            />
            
            <WorkflowBuilder
              v-else-if="showWorkflowBuilder || selectedWorkflowTemplate"
              :selected-template="selectedWorkflowTemplate"
              :is-custom="isCustomWorkflow"
              @back="prevStep"
              @back-to-templates="backToTemplates"
              @continue="onWorkflowComplete"
              @save-draft="saveDraft"
            />
            
            <!-- Fallback content -->
            <div v-else class="bg-gray-50 rounded-lg p-8 text-center">
              <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <FeatherIcon name="zap" class="h-8 w-8 text-blue-600" />
              </div>
              <h4 class="text-lg font-medium text-gray-900 mb-2">Workflow Builder Loading...</h4>
              <p class="text-gray-600">Setting up workflow templates...</p>
            </div>
          </div>

          <!-- Step 5: Review & Activate -->
          <div v-if="step === 5" class="space-y-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">Review Campaign</h2>
            <p class="text-gray-600 mb-6">Review your campaign details and workflow before finalizing.</p>
            
            <!-- Campaign Information -->
            <div class="bg-gray-50 rounded-lg p-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Campaign Information</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="text-sm font-medium text-gray-700">Campaign Name</label>
                  <p class="text-sm text-gray-900">
                    {{ campaignData.campaign_name || "Untitled Campaign" }}
                  </p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-700">Type</label>
                  <p class="text-sm text-gray-900">{{ campaignData.type }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-700">Source</label>
                  <p class="text-sm text-gray-900">{{ selectedSource || "Not selected" }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-700">Status</label>
                  <p class="text-sm text-gray-900">{{ campaignData.status }}</p>
                </div>
                <div class="md:col-span-2">
                  <label class="text-sm font-medium text-gray-700">Description</label>
                  <p class="text-sm text-gray-900">
                    {{ campaignData.description || "No description" }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Workflow Steps -->
            <div v-if="workflowSteps.length > 0" class="bg-white border border-gray-200 rounded-lg p-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Workflow Steps</h3>
              <div class="space-y-3">
                <div
                  v-for="(workflowStep, index) in workflowSteps"
                  :key="workflowStep.id"
                  class="flex items-center p-3 bg-gray-50 rounded-lg"
                >
                  <div class="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                    <span class="text-sm font-medium text-blue-600">{{ index + 1 }}</span>
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center mb-1">
                      <FeatherIcon :name="workflowStep.icon" class="h-4 w-4 mr-2 text-gray-600" />
                      <span class="font-medium text-gray-900">{{ workflowStep.name }}</span>
                    </div>
                    <p class="text-xs text-gray-600">{{ workflowStep.description }}</p>
                    <div v-if="workflowStep.delay > 0" class="text-xs text-blue-600 mt-1">
                      Send after {{ workflowStep.delay }} {{ workflowStep.delayUnit }}
                    </div>
                    <div v-else class="text-xs text-green-600 mt-1">
                      Send immediately
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="mt-4 text-center">
                <p class="text-sm text-gray-600">
                  {{ workflowSteps.length }} step{{ workflowSteps.length !== 1 ? 's' : '' }} configured
                </p>
              </div>
            </div>

            <div class="text-center">
              <p class="text-sm text-gray-600 mb-2">
                Campaign will be created in {{ campaignData.status }} status
              </p>
              <p class="text-xs text-gray-500">
                You can add profiles and activate the campaign after creation
              </p>
            </div>
          </div>
        </div>
      </template>
    </CampaignWizardContent>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { FeatherIcon } from 'frappe-ui'
import CampaignWizardHeader from './CampaignWizardHeader.vue'
import CampaignWizardStepper from './CampaignWizardStepper.vue'
import CampaignWizardContent from './CampaignWizardContent.vue'
import WorkflowTemplateSelector from './WorkflowTemplateSelector.vue'
import WorkflowBuilder from './WorkflowBuilder.vue'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'success', 'draft-created'])

// State
const show = ref(false)
const currentStep = ref(1)
const loading = ref(false)
const draftCampaignLoading = ref(false)
const activating = ref(false)
const selectedSource = ref('')

// Workflow state
const selectedWorkflowTemplate = ref(null)
const showWorkflowBuilder = ref(false)
const isCustomWorkflow = ref(false)
const workflowSteps = ref([])

// Campaign data
const campaignData = ref({
  campaign_name: '',
  description: '',
  type: '',
  status: 'DRAFT',
  start_date: '',
  end_date: ''
})

// Steps definition
const steps = [
  { number: 1, label: 'Information' },
  { number: 2, label: 'Select Source' },
  { number: 3, label: 'Target Segment' },
  { number: 4, label: 'Create Triggers' },
  { number: 5, label: 'Review & Activate' }
]

// Campaign types
const campaignTypes = [
  {
    value: 'NURTURING',
    label: 'Nurturing',
    description: 'Long-term candidate engagement',
    icon: 'heart'
  },
  {
    value: 'ATTRACTION',
    label: 'Attraction',
    description: 'Active talent acquisition',
    icon: 'magnet'
  },
  {
    value: 'RECRUITMENT',
    label: 'Recruitment',
    description: 'Direct job recruitment',
    icon: 'briefcase'
  },
  {
    value: 'REFERRAL',
    label: 'Referral',
    description: 'Employee referral program',
    icon: 'users'
  }
]

// Sources
const sources = [
  {
    key: 'search',
    title: 'Search',
    description: 'Search and select from Contacts and Talents',
    icon: 'search'
  },
  {
    key: 'file',
    title: 'File Import',
    description: 'Import from CSV/Excel file',
    icon: 'upload'
  },
  {
    key: 'datasource',
    title: 'Data Source',
    description: 'Import from external data sources',
    icon: 'database'
  }
]

// Computed
const canProceed = computed(() => {
  if (currentStep.value === 1) {
    return !!(campaignData.value.campaign_name && campaignData.value.description && campaignData.value.type)
  }
  if (currentStep.value === 2) {
    return !!selectedSource.value
  }
  if (currentStep.value === 4) {
    return workflowSteps.value.length > 0
  }
  return true
})

// Methods
const updateCampaignName = (newName) => {
  campaignData.value.campaign_name = newName
}

const saveDraft = async () => {
  console.log('Saving draft...', campaignData.value)
}

const nextStep = () => {
  if (currentStep.value < steps.length) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const selectSource = (sourceKey) => {
  selectedSource.value = sourceKey
  console.log('Selected source:', sourceKey)
}

// Workflow methods
const onTemplateSelected = (data) => {
  selectedWorkflowTemplate.value = data.template
  isCustomWorkflow.value = data.isCustom
  showWorkflowBuilder.value = true
  console.log('Template selected:', data)
}

const backToTemplates = () => {
  showWorkflowBuilder.value = false
  selectedWorkflowTemplate.value = null
  isCustomWorkflow.value = false
}

const onWorkflowComplete = (data) => {
  workflowSteps.value = data.steps
  console.log('Workflow completed:', data)
  // Auto advance to next step
  nextStep()
}

const finalizeCampaign = async () => {
  activating.value = true
  try {
    console.log('Finalizing campaign...', campaignData.value)
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    emit('success', { action: 'create', data: campaignData.value })
    closeWizard()
  } catch (error) {
    console.error('Error finalizing campaign:', error)
  } finally {
    activating.value = false
  }
}

const closeWizard = () => {
  show.value = false
  emit('update:modelValue', false)
  // Reset state
  currentStep.value = 1
  campaignData.value = {
    campaign_name: '',
    description: '',
    type: '',
    status: 'DRAFT',
    start_date: '',
    end_date: ''
  }
  selectedSource.value = ''
  
  // Reset workflow state
  selectedWorkflowTemplate.value = null
  showWorkflowBuilder.value = false
  isCustomWorkflow.value = false
  workflowSteps.value = []
}

// Watch modelValue
watch(() => props.modelValue, (newVal) => {
  show.value = newVal
})

watch(show, (newVal) => {
  emit('update:modelValue', newVal)
})
</script>
