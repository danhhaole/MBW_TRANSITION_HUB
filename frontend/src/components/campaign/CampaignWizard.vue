<template>
  <v-dialog
    v-model="show"
    max-width="800px"
    persistent
    scrollable
  >
    <v-card class="campaign-wizard">
      <!-- Header -->
      <v-card-title class="d-flex justify-space-between align-center pa-4 border-b">
        <h2 class="text-h5 font-weight-bold">{{ modalTitle }}</h2>
        <v-btn
          icon="mdi-close"
          variant="text"
          size="small"
          @click="closeWizard"
        />
      </v-card-title>

      <!-- Stepper -->
      <div class="stepper-container pa-6 pb-4">
        <div class="stepper d-flex align-center">
          <template v-for="(step, index) in steps" :key="step.number">
            <div
              class="step-indicator d-flex flex-column align-center"
              :class="getStepClass(step.number)"
            >
              <div class="step-icon">
                <v-icon v-if="step.number < currentStep" size="16">mdi-check</v-icon>
                <span v-else-if="step.number === 4">🎉</span>
                <span v-else>{{ step.number }}</span>
              </div>
              <span class="step-label mt-1">{{ step.label }}</span>
            </div>
            <div
              v-if="index < steps.length - 1"
              class="step-connector"
              :class="{ active: step.number < currentStep }"
            />
          </template>
        </div>
      </div>

      <!-- Step Content -->
      <v-card-text class="pa-6">
        <!-- Step 1: Thông tin chiến dịch -->
        <div v-if="currentStep === 1" class="step-content">
          <v-form ref="step1Form" v-model="step1Valid">
            <v-text-field
              v-model="campaignData.campaign_name"
              label="Tên chiến dịch"
              placeholder="Ví dụ: Nuôi dưỡng ứng viên React Quý 4/2024"
              variant="outlined"
              :rules="[rules.required]"
              class="mb-4"
            />
            
            <v-textarea
              v-model="campaignData.description"
              label="Mục tiêu"
              placeholder="Mô tả ngắn gọn mục đích của chiến dịch..."
              rows="3"
              variant="outlined"
              :rules="[rules.required]"
            />
          </v-form>
        </div>

        <!-- Step 2: Chọn nguồn -->
        <div v-if="currentStep === 2" class="step-content">
          <v-row>
            <v-col
              v-for="source in sources"
              :key="source.key"
              cols="12"
              md="4"
            >
              <v-card
                :variant="selectedSource === source.key ? 'tonal' : 'outlined'"
                :color="selectedSource === source.key ? 'primary' : undefined"
                class="source-card pa-4 text-center cursor-pointer"
                height="150"
                @click="selectSource(source.key)"
              >
                <v-icon :icon="source.icon" size="32" class="mb-2" />
                <div class="text-subtitle-1 font-weight-medium mb-1">
                  {{ source.title }}
                </div>
                <div class="text-caption text-grey-darken-1">
                  {{ source.description }}
                </div>
              </v-card>
            </v-col>
          </v-row>
        </div>

        <!-- Step 3: Cấu hình và lựa chọn -->
        <div v-if="currentStep === 3" class="step-content">
          <!-- Configuration Form -->
          <div v-if="!showCandidates" class="config-form">
            <p class="text-body-2 text-grey-darken-1 mb-4">
              {{ sourceConfigs[selectedSource]?.description }}
            </p>
            
                         <component
               :is="getConfigComponent(selectedSource)"
               v-model="configData"
             />
          </div>

          <!-- Loading -->
          <div v-if="loading" class="text-center py-8">
            <v-progress-circular indeterminate color="primary" size="48" />
            <p class="mt-4 text-body-1">Đang xử lý...</p>
          </div>

          <!-- Candidate Selection -->
          <div v-if="showCandidates && !loading" class="candidate-selection">
            <h4 class="text-h6 mb-4">
              Kết quả ({{ mockCandidates.length }} ứng viên)
            </h4>
            
            <div class="candidate-list" style="max-height: 300px; overflow-y: auto;">
              <v-card
                v-for="candidate in mockCandidates"
                :key="candidate.id"
                :variant="selectedCandidates.has(candidate.id) ? 'tonal' : 'outlined'"
                :color="selectedCandidates.has(candidate.id) ? 'primary' : undefined"
                class="mb-2 cursor-pointer"
                @click="toggleCandidate(candidate.id)"
              >
                <div class="d-flex align-center pa-3">
                  <v-checkbox
                    :model-value="selectedCandidates.has(candidate.id)"
                    @click.stop
                    @update:model-value="toggleCandidate(candidate.id)"
                  />
                  <v-avatar size="40" color="primary" class="mr-3">
                    <span class="text-white">{{ candidate.name.charAt(0) }}</span>
                  </v-avatar>
                  <div class="flex-grow-1">
                    <div class="text-subtitle-1 font-weight-medium">
                      {{ candidate.name }}
                    </div>
                    <div class="text-caption text-grey-darken-1">
                      {{ candidate.title }}
                    </div>
                  </div>
                  <v-chip size="small" variant="outlined">
                    {{ candidate.source }}
                  </v-chip>
                </div>
              </v-card>
            </div>
          </div>
        </div>

        <!-- Step 4: Kích hoạt -->
        <div v-if="currentStep === 4" class="step-content text-center">
          <div class="pa-6">
            <div class="text-h1 mb-4">🎉</div>
            <h3 class="text-h5 font-weight-bold mb-4">Chiến dịch đã sẵn sàng!</h3>
            <p class="text-body-1 mb-2">
              <template v-if="selectedCandidates.size > 0">
                Bạn sắp thêm <strong>{{ selectedCandidates.size }} ứng viên</strong> 
                vào chiến dịch <strong>"{{ campaignData.campaign_name }}"</strong>.
              </template>
              <template v-else>
                Bạn sắp tạo chiến dịch <strong>"{{ campaignData.campaign_name }}"</strong> 
                với trạng thái nháp để bổ sung ứng viên sau.
              </template>
            </p>
            <p class="text-caption text-grey-darken-1">
              <template v-if="selectedCandidates.size > 0">
                Sau khi tạo, chiến dịch sẽ ở trạng thái nháp để bạn có thể chỉnh sửa và kích hoạt sau.
              </template>
              <template v-else>
                Bạn có thể thêm ứng viên và kích hoạt chiến dịch sau khi tạo.
              </template>
            </p>
          </div>
        </div>
      </v-card-text>

      <!-- Footer Actions -->
      <v-card-actions class="pa-4 border-t">
        <v-btn
          v-if="currentStep > 1"
          variant="outlined"
          @click="prevStep"
          :disabled="loading"
        >
          Quay lại
        </v-btn>
        
        <v-spacer />
        
        <v-btn
          v-if="currentStep < 3"
          color="primary"
          @click="nextStep"
          :disabled="!canProceed"
        >
          Tiếp tục
        </v-btn>
        
        <v-btn
          v-if="currentStep === 3 && !showCandidates"
          color="primary"
          @click="handleSearch"
          :loading="loading"
          :disabled="!selectedSource"
        >
          {{ getSearchButtonText() }}
        </v-btn>
        
        <v-btn
          v-if="currentStep === 3 && showCandidates"
          color="primary"
          @click="nextStep"
        >
          {{ selectedCandidates.size > 0 ? `Thêm ${selectedCandidates.size} ứng viên` : 'Bỏ qua bước này' }}
        </v-btn>
        
        <v-btn
          v-if="currentStep === 4"
          color="success"
          @click="createCampaign"
          :loading="activating"
        >
          Tạo Chiến dịch
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
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
const step1Valid = ref(false)
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
      target_segment: campaignData.value.target_segment,
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
.campaign-wizard {
  min-height: 600px;
}

.stepper {
  position: relative;
}

.step-indicator {
  position: relative;
  color: #94a3b8;
  transition: all 0.3s ease;
  min-width: 80px;
}

.step-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  background-color: white;
  transition: all 0.3s ease;
}

.step-label {
  font-size: 12px;
  font-weight: 500;
  text-align: center;
}

.step-connector {
  flex-grow: 1;
  height: 2px;
  background-color: #64748b;
  margin: 0 8px;
  transition: all 0.4s ease;
}

.step-indicator.active .step-icon,
.step-indicator.completed .step-icon {
  background-color: rgb(var(--v-theme-primary));
  border-color: rgb(var(--v-theme-primary));
  color: white;
}

.step-indicator.active .step-label {
  color: rgb(var(--v-theme-on-surface));
  font-weight: 600;
}

.step-indicator.completed .step-label {
  color: #64748b;
}

.step-connector.active {
  background-color: rgb(var(--v-theme-primary));
}

.source-card {
  transition: all 0.2s ease;
}

.source-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.candidate-list {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 8px;
}

.step-content {
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
</style> 