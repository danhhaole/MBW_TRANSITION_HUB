<template>
  <Dialog v-model="show" :options="dialogOptions">
    <template #body>
      <div class="bg-white">
        <!-- Header -->
        <div class="flex justify-between items-center p-6 border-b border-gray-200">
          <h2 class="text-xl font-bold text-gray-900">{{ modalTitle }}</h2>
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
          <!-- Step 1: Thông tin chiến dịch -->
          <div v-if="currentStep === 1" class="space-y-4 animate-fadeIn">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Tên chiến dịch <span class="text-red-500">*</span>
              </label>
              <input
                v-model="campaignData.campaign_name"
                type="text"
                placeholder="Ví dụ: Nuôi dưỡng ứng viên React Quý 4/2024"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                :class="{ 'border-red-500': !campaignData.campaign_name && currentStep > 1 }"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Mục tiêu <span class="text-red-500">*</span>
              </label>
              <textarea
                v-model="campaignData.description"
                rows="3"
                placeholder="Mô tả ngắn gọn mục đích của chiến dịch..."
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                :class="{ 'border-red-500': !campaignData.description && currentStep > 1 }"
              />
            </div>
          </div>

          <!-- Step 2: Chọn nguồn -->
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

          <!-- Step 3: Cấu hình và lựa chọn -->
          <div v-if="currentStep === 3" class="animate-fadeIn">
            <!-- Configuration Form -->
            <div v-if="!showCandidates" class="space-y-4">
              <p class="text-sm text-gray-600 mb-4">
                {{ sourceConfigs[selectedSource]?.description }}
              </p>
              
              <component
                :is="getConfigComponent(selectedSource)"
                v-model="configData"
              />
            </div>

            <!-- Loading -->
            <div v-if="loading" class="text-center py-8">
              <div class="flex justify-center mb-4">
                <svg class="animate-spin h-12 w-12 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </div>
              <p class="text-base text-gray-700">Đang xử lý...</p>
            </div>

            <!-- Candidate Selection -->
            <div v-if="showCandidates && !loading" class="space-y-4">
              <h4 class="text-lg font-semibold mb-4">
                Kết quả ({{ mockCandidates.length }} ứng viên)
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

          <!-- Step 4: Kích hoạt -->
          <div v-if="currentStep === 4" class="text-center py-6 animate-fadeIn">
            <div class="text-6xl mb-4">🎉</div>
            <h3 class="text-xl font-bold mb-4 text-gray-900">Chiến dịch đã sẵn sàng!</h3>
            <p class="text-base mb-2 text-gray-700">
              <template v-if="selectedCandidates.size > 0">
                Bạn sắp thêm <strong>{{ selectedCandidates.size }} ứng viên</strong> 
                vào chiến dịch <strong>"{{ campaignData.campaign_name }}"</strong>.
              </template>
              <template v-else>
                Bạn sắp tạo chiến dịch <strong>"{{ campaignData.campaign_name }}"</strong> 
                với trạng thái nháp để bổ sung ứng viên sau.
              </template>
            </p>
            <p class="text-xs text-gray-500">
              <template v-if="selectedCandidates.size > 0">
                Sau khi tạo, chiến dịch sẽ ở trạng thái nháp để bạn có thể chỉnh sửa và kích hoạt sau.
              </template>
              <template v-else>
                Bạn có thể thêm ứng viên và kích hoạt chiến dịch sau khi tạo.
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
            Quay lại
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
              Tiếp tục
            </Button>
            
            <Button
              v-if="currentStep === 3 && !showCandidates"
              variant="solid"
              theme="gray"
              @click="handleSearch"
              :loading="loading"
              :disabled="!selectedSource"
            >
              {{ getSearchButtonText() }}
            </Button>
            
            <Button
              v-if="currentStep === 3 && showCandidates"
              variant="solid"
              theme="gray"
              @click="nextStep"
            >
              {{ selectedCandidates.size > 0 ? `Thêm ${selectedCandidates.size} ứng viên` : 'Bỏ qua bước này' }}
            </Button>
            
            <Button
              v-if="currentStep === 4"
              variant="solid"
              theme="gray"
              @click="createCampaign"
              :loading="activating"
            >
              Tạo Chiến dịch
            </Button>
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Dialog, Button, FeatherIcon } from 'frappe-ui'
import PoolConfig from './PoolConfig.vue'
import AtsConfig from './AtsConfig.vue'
import WebConfig from './WebConfig.vue'
import { submitNewCampaign, searchCandidates } from '@/services/campaignService'
import { 
  campaignService, 
  candidateService, 
  candidateSegmentService, 
  talentSegmentService,
  candidateCampaignService 
} from '@/services/universalService'
import { processSkills } from '@/services/candidateService'
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

// Form data
const campaignData = ref({
  campaign_name: '',
  description: '',
  type: 'NURTURING',
  status: 'DRAFT',
  target_segment: props.preselectedSegment || ''
})

const selectedSource = ref(props.preselectedSegment ? 'pool' : '')
const configData = ref({
  selectedSegment: props.preselectedSegment || ''
})
const selectedCandidates = ref(new Set())
const realCandidates = ref([]) // Thay thế mockCandidates

// Steps definition
const steps = [
  { number: 1, label: 'Thông tin' },
  { number: 2, label: 'Nguồn' },
  { number: 3, label: 'Lựa chọn' },
  { number: 4, label: 'Kích hoạt' }
]

// Source options
const sources = [
  {
    key: 'pool',
    title: 'Nguồn nhân tài',
    description: 'Sử dụng dữ liệu có sẵn',
    icon: 'mdi-account-group'
  },
  {
    key: 'ats',
    title: 'Đồng bộ từ ATS',
    description: 'Kết nối với hệ thống khác',
    icon: 'mdi-sync'
  },
  {
    key: 'web',
    title: 'Thu thập từ Web',
    description: 'Tìm kiếm trên Internet',
    icon: 'mdi-web'
  }
]

// Source configurations
const sourceConfigs = {
  pool: {
    description: 'Chọn phân khúc nhân tài có sẵn để tạo chiến dịch.'
  },
  ats: {
    description: 'Chọn hệ thống ATS và thiết lập quy tắc để đồng bộ.'
  },
  web: {
    description: 'Nhập từ khóa và chọn nguồn để bắt đầu thu thập dữ liệu.'
  }
}

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

// Validation rules
const rules = {
  required: value => !!value || 'Trường này là bắt buộc'
}

// Dialog options
const dialogOptions = computed(() => ({
  title: modalTitle.value,
  size: '2xl'
}))

// Computed
const modalTitle = computed(() => {
  const titles = {
    1: 'Tạo Chiến dịch mới',
    2: 'Chọn nguồn dữ liệu',
    3: 'Cấu hình và lựa chọn',
    4: 'Kích hoạt chiến dịch'
  }
  return titles[currentStep.value] || 'Tạo Chiến dịch mới'
})

const step1Valid = computed(() => {
  return !!(campaignData.value.campaign_name && campaignData.value.description)
})

const canProceed = computed(() => {
  if (currentStep.value === 1) return step1Valid.value
  if (currentStep.value === 2) return !!selectedSource.value
  return true
})

// Methods
const getStepClass = (stepNumber) => {
  if (stepNumber < currentStep.value) return 'completed'
  if (stepNumber === currentStep.value) return 'active'
  return ''
}

const getConfigComponent = (source) => {
  const components = {
    pool: PoolConfig,
    ats: AtsConfig,
    web: WebConfig
  }
  return components[source] || null
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
  loading.value = true
  
  try {
    let candidates = []
    
    if (selectedSource.value === 'pool') {
      // Load candidates from selected segment
      const segmentId = configData.value.selectedSegment || props.preselectedSegment
      if (segmentId) {
        candidates = await loadCandidatesFromSegment(segmentId)
        
        // Set target_segment in campaign data
        campaignData.value.target_segment = segmentId
      }
    } else {
      // For ATS and Web, use the existing search API
      candidates = await searchCandidates(selectedSource.value, configData.value)
    }
    
    // Update candidates list
    mockCandidates.value = candidates
    
    loading.value = false
    showCandidates.value = true
  } catch (error) {
    console.error('Error searching candidates:', error)
    loading.value = false
    alert('Có lỗi khi tìm kiếm ứng viên. Vui lòng thử lại.')
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
  const texts = {
    pool: 'Tìm kiếm',
    ats: 'Bắt đầu Đồng bộ',
    web: 'Bắt đầu Thu thập'
  }
  return texts[selectedSource.value] || 'Tìm kiếm'
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
      is_active: false
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
    
    let errorMessage = 'Có lỗi xảy ra khi tạo chiến dịch'
    
    if (error.message.includes('campaign_name')) {
      errorMessage = 'Tên chiến dịch không hợp lệ hoặc đã tồn tại'
    } else if (error.message.includes('validation')) {
      errorMessage = 'Dữ liệu nhập vào không đúng định dạng'
    } else if (error.message.includes('network') || error.message.includes('fetch')) {
      errorMessage = 'Lỗi kết nối mạng, vui lòng thử lại'
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
    target_segment: props.preselectedSegment || ''
  }
  selectedSource.value = props.preselectedSegment ? 'pool' : ''
  configData.value = {
    selectedSegment: props.preselectedSegment || ''
  }
  selectedCandidates.value.clear()
  showCandidates.value = false
  loading.value = false
  activating.value = false
  
  // Reset candidates
  mockCandidates.value = []
}

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