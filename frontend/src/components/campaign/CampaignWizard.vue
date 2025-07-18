<template>
  <Dialog v-model="show" :options="dialogOptions">
    <template #body>
      <div class="bg-white">
        <!-- Header -->
        <div class="flex justify-between items-center p-6 border-b border-gray-200">
          <h2 class="text-xl font-bold text-gray-900">{{ __(modalTitle) }}</h2>
          <Button
            theme="gray"
            variant="ghost"
            class="w-7 h-7"
            @click="closeWizard"
          >
            <FeatherIcon name="x" class="h-4 w-4" />
          </Button>
        </div>

        <!-- Stepper -->
        <div class="p-6 pb-4">
          <div class="flex items-center">
            <template v-for="(step, index) in steps" :key="step.number">
              <div
                class="flex flex-col items-center min-w-[80px]"
                :class="getStepClass(step.number)"
              >
                <div class="w-10 h-10 rounded-full border-2 flex items-center justify-center font-semibold transition-all duration-300"
                     :class="getStepIconClass(step.number)">
                  <FeatherIcon v-if="step.number < currentStep" name="check" class="h-4 w-4" />
                  <span v-else-if="step.number === 4">🎉</span>
                  <span v-else>{{ step.number }}</span>
                </div>
                <span class="mt-1 text-xs font-medium text-center transition-all duration-300"
                      :class="getStepLabelClass(step.number)">{{ step.label }}</span>
              </div>
              <div
                v-if="index < steps.length - 1"
                class="flex-grow h-0.5 mx-2 transition-all duration-400"
                :class="step.number < currentStep ? 'bg-blue-500' : 'bg-gray-300'"
              />
            </template>
          </div>
        </div>

        <!-- Step Content -->
        <div class="p-6">
          <!-- Step 1: Campaign Information -->
          <div v-if="currentStep === 1" class="space-y-4 animate-fadeIn">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Campaign Name') }} <span class="text-red-500">*</span>
              </label>
              <input
                v-model="campaignData.campaign_name"
                type="text"
                :placeholder="__('Example: React Candidate Nurturing Q4/2024')"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                :class="{ 'border-red-500': !campaignData.campaign_name && currentStep > 1 }"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Objective') }} <span class="text-red-500">*</span>
              </label>
              <textarea
                v-model="campaignData.description"
                rows="3"
                :placeholder="__('Brief description of campaign purpose...')"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                :class="{ 'border-red-500': !campaignData.description && currentStep > 1 }"
              />
            </div>
          </div>

          <!-- Step 2: Select Source -->
          <div v-if="currentStep === 2" class="animate-fadeIn">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div
                v-for="source in sources"
                :key="source.key"
                class="border rounded-lg p-4 text-center cursor-pointer transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg"
                :class="selectedSource === source.key ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
                @click="selectSource(source.key)"
              >
                <FeatherIcon :name="getSourceIcon(source.key)" class="h-8 w-8 mx-auto mb-2" 
                           :class="selectedSource === source.key ? 'text-blue-600' : 'text-gray-400'" />
                <div class="text-sm font-medium mb-1" 
                     :class="selectedSource === source.key ? 'text-blue-900' : 'text-gray-900'">
                  {{ source.title }}
                </div>
                <div class="text-xs text-gray-500">
                  {{ source.description }}
                </div>
              </div>
            </div>
          </div>

          <!-- Step 3: Configuration and Selection -->
          <div v-if="currentStep === 3" class="animate-fadeIn">
            <!-- Configuration Form -->
            <div v-if="!showCandidates" class="space-y-4">
              <p class="text-sm text-gray-600 mb-4">
                {{ sourceConfigs[selectedSource]?.description }}
              </p>
              
              <!-- Data Source Type Selection (when Data Source is selected) -->
              <div v-if="selectedSource === 'datasource' && !selectedDataSourceType" class="space-y-4">
                <h4 class="text-lg font-medium text-gray-900 mb-4">{{ __('Select Data Source Type') }}</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div
                    v-for="sourceType in dataSourceTypes"
                    :key="sourceType.key"
                    class="border rounded-lg p-4 text-center cursor-pointer transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg border-gray-200 hover:border-gray-300"
                    @click="selectDataSourceType(sourceType.key)"
                  >
                    <FeatherIcon :name="sourceType.icon" class="h-8 w-8 mx-auto mb-2 text-gray-400" />
                    <div class="text-sm font-medium mb-1 text-gray-900">
                      {{ sourceType.title }}
                    </div>
                    <div class="text-xs text-gray-500">
                      {{ sourceType.description }}
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Specific Data Source Selection (when type is selected) -->
              <div v-else-if="selectedSource === 'datasource' && selectedDataSourceType && !selectedDataSourceId" class="space-y-4">
                <div class="flex items-center justify-between mb-4">
                  <h4 class="text-lg font-medium text-gray-900">
                    {{ __('Select {0} Source', [selectedDataSourceType]) }}
                  </h4>
                  <Button variant="ghost" theme="gray" @click="selectedDataSourceType = ''" class="text-sm">
                    <FeatherIcon name="arrow-left" class="h-4 w-4 mr-1" />
                    {{ __('Back') }}
                  </Button>
                </div>
                
                <div v-if="filteredDataSources.length === 0" class="text-center py-8">
                  <div class="text-gray-500 mb-2">{{ __('No {0} sources available', [selectedDataSourceType]) }}</div>
                  <Button variant="outline" theme="gray" @click="selectedDataSourceType = ''" class="text-sm">
                    {{ __('Choose Different Type') }}
                  </Button>
                </div>
                
                <div v-else class="grid grid-cols-1 gap-3">
                  <div
                    v-for="dataSource in filteredDataSources"
                    :key="dataSource.name"
                    class="border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md border-gray-200 hover:border-gray-300"
                    @click="selectSpecificDataSource(dataSource)"
                  >
                    <div class="flex items-center">
                      <FeatherIcon :name="getDataSourceIcon(dataSource.source_type)" class="h-6 w-6 mr-3 text-gray-400" />
                      <div class="flex-1">
                        <div class="text-sm font-medium text-gray-900">
                          {{ dataSource.source_name }}
                        </div>
                        <div class="text-xs text-gray-500">
                          {{ dataSource.description || `${dataSource.source_type} data source` }}
                        </div>
                      </div>
                      <span class="text-xs px-2 py-1 bg-gray-100 text-gray-600 rounded">
                        {{ dataSource.source_type }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Standard Configuration Components -->
              <div v-else>
                <component
                  :is="getConfigComponent(selectedSource)"
                  v-model="configData"
                  :selected-data-source="configData.selectedDataSource"
                />
              </div>
            </div>

            <!-- Loading -->
            <div v-if="loading" class="text-center py-8">
              <div class="flex justify-center mb-4">
                <svg class="animate-spin h-12 w-12 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </div>
              <p class="text-base text-gray-700">{{ __('Processing...') }}</p>
            </div>

            <!-- Candidate Selection -->
            <div v-if="showCandidates && !loading" class="space-y-4">
              <h4 class="text-lg font-semibold mb-4">
                {{ __('Results ({0} candidates)', [mockCandidates.length]) }}
              </h4>
              
              <div class="border border-gray-200 rounded-lg p-2 max-h-80 overflow-y-auto">
                <div
                  v-for="candidate in mockCandidates"
                  :key="candidate.id"
                  class="border rounded-lg mb-2 p-3 cursor-pointer transition-colors duration-200"
                  :class="selectedCandidates.has(candidate.id) ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
                  @click="toggleCandidate(candidate.id)"
                >
                  <div class="flex items-center">
                    <input
                      type="checkbox"
                      :checked="selectedCandidates.has(candidate.id)"
                      @click.stop
                      @change="toggleCandidate(candidate.id)"
                      class="mr-3 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <div class="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center mr-3">
                      <span class="text-white text-sm font-medium">{{ candidate.name.charAt(0) }}</span>
                    </div>
                    <div class="flex-grow">
                      <div class="text-sm font-medium text-gray-900">
                        {{ candidate.name }}
                      </div>
                      <div class="text-xs text-gray-500">
                        {{ candidate.title }}
                      </div>
                    </div>
                    <span class="text-xs border border-gray-300 rounded px-2 py-1 text-gray-600">
                      {{ candidate.source }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Step 4: Activation -->
          <div v-if="currentStep === 4" class="text-center py-6 animate-fadeIn">
            <div class="text-6xl mb-4">🎉</div>
            <h3 class="text-xl font-bold mb-4 text-gray-900">{{ __('Campaign Ready!') }}</h3>
            <p class="text-base mb-2 text-gray-700">
              <template v-if="selectedCandidates.size > 0">
                {{ __('You are about to add {0} candidates to campaign "{1}".', [selectedCandidates.size, campaignData.campaign_name]) }}
              </template>
              <template v-else>
                {{ __('You are about to create campaign "{0}" as draft to add candidates later.', [campaignData.campaign_name]) }}
              </template>
            </p>
            <p class="text-xs text-gray-500">
              <template v-if="selectedCandidates.size > 0">
                {{ __('After creation, the campaign will be in draft status for you to edit and activate later.') }}
              </template>
              <template v-else>
                {{ __('You can add candidates and activate the campaign after creation.') }}
              </template>
            </p>
          </div>
        </div>

        <!-- Footer Actions -->
        <div class="flex justify-between items-center p-4 border-t border-gray-200">
          <Button
            v-if="currentStep > 1"
            variant="outline"
            theme="gray"
            @click="prevStep"
            :disabled="loading"
          >
            {{ __('Back') }}
          </Button>
          
          <div v-else></div>
          
          <div class="flex space-x-3">
            <Button
              v-if="currentStep < 3"
              variant="solid"
              theme="gray"
              @click="nextStep"
              :disabled="!canProceed"
            >
              {{ __('Continue') }}
            </Button>
            
            <Button
              v-if="currentStep === 3 && !showCandidates"
              variant="solid"
              theme="gray"
              @click="handleSearch"
              :loading="loading"
              :disabled="!canProceedToSearch"
            >
              {{ __(getSearchButtonText()) }}
            </Button>
            
            <Button
              v-if="currentStep === 3 && showCandidates"
              variant="solid"
              theme="gray"
              @click="nextStep"
            >
              {{ selectedCandidates.size > 0 ? __(`Add ${selectedCandidates.size} candidates`) : __('Skip this step') }}
            </Button>
            
            <Button
              v-if="currentStep === 4"
              variant="solid"
              theme="gray"
              @click="createCampaign"
              :loading="activating"
            >
              {{ __('Create Campaign') }}
            </Button>
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { Dialog, Button, FeatherIcon } from 'frappe-ui'
import PoolConfig from './PoolConfig.vue'
import AtsConfig from './AtsConfig.vue'
import WebConfig from './WebConfig.vue'
import FileConfig from './FileConfig.vue'
import { submitNewCampaign, searchCandidates } from '@/services/campaignService'
import { 
  campaignService, 
  candidateService, 
  candidateSegmentService, 
  talentSegmentService,
  candidateCampaignService 
} from '@/services/universalService'
import { processSkills } from '@/services/candidateService'
import candidateDataSourceRepository from '@/repositories/candidateDataSourceRepository'
import moment from 'moment'

// Props & Emits
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  preselectedSegment: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'success'])

// Reactive state
const show = ref(false)
const currentStep = ref(1)
const loading = ref(false)
const activating = ref(false)
const showCandidates = ref(false)
const loadingDataSources = ref(false)

// Form data
const campaignData = ref({
  campaign_name: '',
  description: '',
  type: 'NURTURING',
  status: 'DRAFT',
  target_segment: props.preselectedSegment || '',
  source_type: '', // New field: 'DataSource', 'File', 'Search'
  source_file: '', // For File type
  data_source_id: '' // For DataSource type
})

const selectedSource = ref(props.preselectedSegment ? 'search' : '')
const selectedDataSourceType = ref('') // ATS, JobBoard, SocialNetwork, TalentPool
const selectedDataSourceId = ref('') // Specific data source ID
const configData = ref({
  selectedSegment: props.preselectedSegment || '',
  selectedDataSource: '',
  selectedFile: null
})
const selectedCandidates = ref(new Set())
const realCandidates = ref([]) // Replace mockCandidates
const dataSources = ref([]) // All data sources from API
const filteredDataSources = ref([]) // Filtered by type

// Translation helper function


// Steps definition
const steps = [
  { number: 1, label: 'Information' },
  { number: 2, label: 'Source' },
  { number: 3, label: 'Selection' },
  { number: 4, label: 'Activate' }
]

// Source options - 3 fixed choices only
const sources = computed(() => [
  {
    key: 'search',
    title: 'Search',
    description: 'Search and select candidates',
    icon: 'search',
    type: 'fixed',
    source_type: 'Search'
  },
  {
    key: 'file',
    title: 'File Import',
    description: 'Import from CSV/Excel file',
    icon: 'upload',
    type: 'fixed',
    source_type: 'File'
  },
  {
    key: 'datasource',
    title: 'Data Source',
    description: 'Import from external data sources',
    icon: 'database',
    type: 'fixed',
    source_type: 'DataSource'
  }
])

// Data source type options
const dataSourceTypes = computed(() => [
  { key: 'ATS', title: 'ATS', description: 'Applicant Tracking System', icon: 'briefcase' },
  { key: 'JobBoard', title: 'Job Board', description: 'Job posting platforms', icon: 'clipboard' },
  { key: 'SocialNetwork', title: 'Social Network', description: 'LinkedIn, Facebook, etc.', icon: 'users' },
  { key: 'TalentPool', title: 'Talent Pool', description: 'External talent pools', icon: 'user-check' }
])

// Helper function for data source icons
const getDataSourceIcon = (sourceType) => {
  const iconMap = {
    'ATS': 'database',
    'JobBoard': 'briefcase',
    'SocialNetwork': 'users',
    'TalentPool': 'user-check'
  }
  return iconMap[sourceType] || 'server'
}

// Source configurations
const sourceConfigs = computed(() => ({
  search: {
    description: __('Search and select candidates from existing talent pools.')
  },
  file: {
    description: __('Import candidates from CSV or Excel files.')
  },
  datasource: {
    description: __('Import candidates from external data sources (ATS, Job Board, Social Network, etc.).')
  }
}))

// Mock candidates (will be updated by search)
const mockCandidates = ref([])

// Load candidates from segment
const loadCandidatesFromSegment = async (segmentId) => {
  try {
    // Get candidates from target segment through CandidateSegment
    const candidateSegmentResult = await candidateSegmentService.getList({
      filters: { segment_id: segmentId },
      fields: ['candidate_id']
    })
    
    if (candidateSegmentResult.success && candidateSegmentResult.data.length > 0) {
      const candidateIds = candidateSegmentResult.data.map(cs => cs.candidate_id)
      
      // Get the actual candidate data
      const candidateResult = await candidateService.getList({
        filters: { name: ['in', candidateIds] },
        fields: ['name', 'candidate_name', 'email', 'skills', 'status']
      })
      
      if (candidateResult.success) {
        return candidateResult.data.map(candidate => ({
          id: candidate.name,
          name: candidate.candidate_name || candidate.name,
          title: candidate.email || 'Candidate',
          source: 'Talent Segment',
          email: candidate.email,
          skills: processSkills(candidate.skills)
        }))
      }
    }
    return []
  } catch (error) {
    console.error('Error loading candidates from segment:', error)
    return []
  }
}

// Load candidates from data source
const loadCandidatesFromDataSource = async (dataSourceId) => {
  try {
    // TODO: Implement this function to find TalentPool records with matching data_source_id
    // and convert them to candidates format
    console.log('Loading candidates from data source:', dataSourceId)
    
    // For now, return empty array - this will be implemented later
    return []
  } catch (error) {
    console.error('Error loading candidates from data source:', error)
    return []
  }
}

// Validation rules
const rules = {
  required: value => !!value || __('This field is required')
}

// Dialog options
const dialogOptions = computed(() => ({
  title: modalTitle.value,
  size: '2xl'
}))

// Computed
const modalTitle = computed(() => {
  const titles = {
    1: 'Create New Campaign',
    2: 'Select Data Source',
    3: 'Configure and Select',
    4: 'Activate Campaign'
  }
  return titles[currentStep.value] || 'Create New Campaign'
})

const step1Valid = computed(() => {
  return !!(campaignData.value.campaign_name && campaignData.value.description)
})

const canProceed = computed(() => {
  if (currentStep.value === 1) return step1Valid.value
  if (currentStep.value === 2) return !!selectedSource.value
  return true
})

const canProceedToSearch = computed(() => {
  if (!selectedSource.value) return false
  
  if (selectedSource.value === 'datasource') {
    return !!(selectedDataSourceType.value && selectedDataSourceId.value)
  }
  
  return true
})

// Methods
const getStepClass = (stepNumber) => {
  if (stepNumber < currentStep.value) return 'completed'
  if (stepNumber === currentStep.value) return 'active'
  return ''
}

// Load data sources from API
const loadDataSources = async () => {
  loadingDataSources.value = true
  try {
    const response = await candidateDataSourceRepository.getDataSources()
    if (response.success) {
      dataSources.value = response.data_sources || []
    }
  } catch (error) {
    console.error('Error loading data sources:', error)
  } finally {
    loadingDataSources.value = false
  }
}

const getConfigComponent = (source) => {
  if (source === 'search') return PoolConfig // Use pool config for search
  if (source === 'file') return FileConfig
  if (source === 'datasource' && selectedDataSourceId.value) {
    // Show appropriate config based on data source type
    const dataSource = configData.value.selectedDataSource
    if (dataSource && dataSource.source_type === 'ATS') {
      return AtsConfig
    }
    // Add other config components for different data source types as needed
    return AtsConfig // Default to ATS config for now
  }
  return null
}

// Styling methods for Tailwind CSS
const getStepIconClass = (stepNumber) => {
  if (stepNumber < currentStep.value) return 'border-blue-500 bg-blue-500 text-white'
  if (stepNumber === currentStep.value) return 'border-blue-500 bg-blue-500 text-white'
  return 'border-gray-300 text-gray-400'
}

const getStepLabelClass = (stepNumber) => {
  if (stepNumber < currentStep.value) return 'text-gray-600'
  if (stepNumber === currentStep.value) return 'text-gray-900 font-semibold'
  return 'text-gray-400'
}

const getSourceIcon = (sourceKey) => {
  const icons = {
    pool: 'users',
    ats: 'refresh-cw',
    web: 'globe'
  }
  return icons[sourceKey] || 'circle'
}

const selectSource = (sourceKey) => {
  selectedSource.value = sourceKey
  
  // Reset data source selections
  selectedDataSourceType.value = ''
  selectedDataSourceId.value = ''
  filteredDataSources.value = []
  
  // Find selected source info
  const source = sources.value.find(s => s.key === sourceKey)
  if (source) {
    campaignData.value.source_type = source.source_type
    
    if (source.source_type !== 'DataSource') {
      campaignData.value.data_source_id = ''
      configData.value.selectedDataSource = ''
    }
    
    if (source.source_type === 'File') {
      // Reset file selection
      campaignData.value.source_file = ''
      configData.value.selectedFile = null
    }
  }
}

const selectDataSourceType = (sourceType) => {
  selectedDataSourceType.value = sourceType
  selectedDataSourceId.value = ''
  
  // Filter data sources by type
  filteredDataSources.value = dataSources.value.filter(ds => ds.source_type === sourceType)
}

const selectSpecificDataSource = (dataSource) => {
  selectedDataSourceId.value = dataSource.name
  campaignData.value.data_source_id = dataSource.name
  configData.value.selectedDataSource = dataSource
}

const nextStep = () => {
  if (currentStep.value < 4) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 1) {
    if (currentStep.value === 3) {
      showCandidates.value = false
      selectedCandidates.value.clear()
    }
    currentStep.value--
  }
}

const handleSearch = async () => {
  // For data source selection, handle step by step
  if (selectedSource.value === 'datasource') {
    if (!selectedDataSourceType.value) {
      // This shouldn't happen due to disabled state, but just in case
      return
    }
    if (!selectedDataSourceId.value) {
      // This shouldn't happen due to disabled state, but just in case
      return
    }
  }
  
  loading.value = true
  
  try {
    let candidates = []
    
    switch (selectedSource.value) {
      case 'search':
        // Load candidates from selected segment (old pool logic)
        const segmentId = configData.value.selectedSegment || props.preselectedSegment
        if (segmentId) {
          candidates = await loadCandidatesFromSegment(segmentId)
          campaignData.value.target_segment = segmentId
        }
        break
        
      case 'file':
        // Handle file import
        if (configData.value.uploadedFileUrl) {
          // File has been uploaded successfully
          console.log('Processing uploaded file:', configData.value.uploadedFileUrl)
          
          // TODO: Parse CSV/Excel file from URL and extract candidates
          // For now, show empty candidates list until file parsing is implemented
          candidates = []
          
          console.log('File uploaded successfully, URL:', configData.value.uploadedFileUrl)
        } else {
          console.log('No file uploaded yet')
          candidates = []
        }
        break
        
      case 'datasource':
        // Handle data source sync
        if (selectedDataSourceId.value) {
          console.log('Syncing from data source:', selectedDataSourceId.value)
          // TODO: Find TalentPools with matching data source and load candidates
          candidates = await loadCandidatesFromDataSource(selectedDataSourceId.value)
        }
        break
        
      default:
        // Fallback to existing search API for compatibility
        candidates = await searchCandidates(selectedSource.value, configData.value)
    }
    
    // Update candidates list
    mockCandidates.value = candidates
    
    loading.value = false
    showCandidates.value = true
  } catch (error) {
    console.error('Error searching candidates:', error)
    loading.value = false
    alert(__('Error searching candidates. Please try again.'))
  }
}

const toggleCandidate = (candidateId) => {
  if (selectedCandidates.value.has(candidateId)) {
    selectedCandidates.value.delete(candidateId)
  } else {
    selectedCandidates.value.add(candidateId)
  }
}

const getSearchButtonText = () => {
  if (selectedSource.value === 'search') return __('Search')
  if (selectedSource.value === 'file') return __('Process File')
  if (selectedSource.value === 'datasource') {
    if (!selectedDataSourceType.value) return __('Select Source Type')
    if (!selectedDataSourceId.value) return __('Select Specific Source')
    return __('Sync Data')
  }
  return __('Continue')
}

const createCampaign = async () => {
  activating.value = true
  
  try {
    // First, create the campaign
    const campaignPayload = {
      campaign_name: campaignData.value.campaign_name,
      description: campaignData.value.description,
      type: campaignData.value.type,
      status: 'DRAFT',
      start_date: new Date().toISOString().split('T')[0],
      end_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      target_segment: campaignData.value.target_segment?.value,
      is_active: false,
      source_type: campaignData.value.source_type,
      source_file: campaignData.value.source_file,
      data_source_id: campaignData.value.data_source_id
    }

    // Set source field based on source_type
    if (campaignData.value.source_type === 'DataSource' && configData.value.selectedDataSource) {
      // Save only the data source record name (ID) in source field
      campaignPayload.source = configData.value.selectedDataSource.name
    } else if (campaignData.value.source_type === 'File' && configData.value.uploadedFileUrl) {
      // For File: only save source_file, leave source empty
      campaignPayload.source_file = configData.value.uploadedFileUrl
      // source field is not used for File type
    } else if (campaignData.value.source_type === 'Search' && campaignData.value.target_segment) {
      // For search, source is the segment info
      campaignPayload.source = campaignData.value.target_segment
    }
    
    console.log('Creating campaign with payload:', campaignPayload)
    
    // Create campaign using universal service
    const campaignResult = await campaignService.save(campaignPayload)
    
    if (campaignResult.success) {
      const campaignId = campaignResult.data.name
      
      // Create CandidateCampaign records for selected candidates (only if any candidates are selected)
      if (selectedCandidates.value.size > 0) {
        const candidateCampaignPromises = Array.from(selectedCandidates.value).map(candidateId => 
          candidateCampaignService.save({
            candidate_id: candidateId,
            campaign_id: campaignId,
            status: 'DRAFT',
            current_step_order: 1,
            enrolled_at: moment().format("YYYY-MM-DD HH:mm:ss")
          })
        )
        
        // Wait for all candidate assignments to complete
        await Promise.all(candidateCampaignPromises)
      }
      
      emit('success', {
        action: 'create',
        data: campaignResult.data
      })
      
      closeWizard()
    } else {
      throw new Error(campaignResult.message || 'Failed to create campaign')
    }
  } catch (error) {
    console.error('Error creating campaign:', error)
    
    let errorMessage = __('An error occurred while creating the campaign')
    
    if (error.message.includes('campaign_name')) {
      errorMessage = __('Campaign name is invalid or already exists')
    } else if (error.message.includes('validation')) {
      errorMessage = __('Input data is not in the correct format')
    } else if (error.message.includes('network') || error.message.includes('fetch')) {
      errorMessage = __('Network connection error, please try again')
    } else if (error.message) {
      errorMessage = error.message
    }
    
    alert(errorMessage)
  } finally {
    activating.value = false
  }
}

const closeWizard = () => {
  show.value = false
  // Reset state
  currentStep.value = 1
  campaignData.value = {
    campaign_name: '',
    description: '',
    type: 'NURTURING',
    status: 'DRAFT',
    target_segment: props.preselectedSegment || '',
    source_type: '',
    source_file: '',
    data_source_id: ''
  }
  selectedSource.value = props.preselectedSegment ? 'search' : ''
  selectedDataSourceType.value = ''
  selectedDataSourceId.value = ''
  configData.value = {
    selectedSegment: props.preselectedSegment || '',
    selectedDataSource: '',
    selectedFile: null,
    uploadedFileUrl: '',
    filePreview: [],
    fileHeaders: []
  }
  filteredDataSources.value = []
  selectedCandidates.value.clear()
  showCandidates.value = false
  loading.value = false
  activating.value = false
  
  // Reset candidates
  mockCandidates.value = []
}

// Load data sources on component mount
onMounted(() => {
  loadDataSources()
})

// Watchers
watch(() => props.modelValue, (newVal) => {
  show.value = newVal
})

watch(show, (newVal) => {
  emit('update:modelValue', newVal)
})
</script>

<style scoped>
/* Custom animations for Tailwind */
.animate-fadeIn {
  animation: fadeIn 0.5s forwards;
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

/* Custom hover effects */
.hover\:-translate-y-0\.5:hover {
  transform: translateY(-2px);
}

.hover\:shadow-lg:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
</style>