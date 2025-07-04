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
              Bạn sắp thêm <strong>{{ selectedCandidates.size }} ứng viên</strong> 
              vào chiến dịch <strong>"{{ campaignData.campaign_name }}"</strong>.
            </p>
            <p class="text-caption text-grey-darken-1">
              Sau khi kích hoạt, hệ thống sẽ bắt đầu thực hiện các bước tương tác đầu tiên.
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
          :disabled="selectedCandidates.size === 0"
        >
          Thêm {{ selectedCandidates.size }} ứng viên
        </v-btn>
        
        <v-btn
          v-if="currentStep === 4"
          color="success"
          @click="activateCampaign"
          :loading="activating"
        >
          Kích hoạt Chiến dịch
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

// Props & Emits
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
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
  status: 'DRAFT'
})

const selectedSource = ref('')
const configData = ref({})
const selectedCandidates = ref(new Set())

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
    description: 'Sử dụng bộ lọc để tìm ứng viên phù hợp từ nguồn nhân tài có sẵn.'
  },
  ats: {
    description: 'Chọn hệ thống ATS và thiết lập quy tắc để đồng bộ.'
  },
  web: {
    description: 'Nhập từ khóa và chọn nguồn để bắt đầu thu thập dữ liệu.'
  }
}

// Mock candidates (will be updated by search)
const mockCandidates = ref([
  { id: 'c1', name: 'Nguyễn Văn An', title: 'Senior React Developer', source: 'Nguồn nhân tài' },
  { id: 'c2', name: 'Trần Thị Bình', title: 'Fullstack Engineer', source: 'ATS' },
  { id: 'c3', name: 'Lê Hoàng Cường', title: 'Data Scientist', source: 'Web' },
  { id: 'c4', name: 'Phạm Thị Dung', title: 'React Native Developer', source: 'Nguồn nhân tài' }
])

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
    // Call search candidates API (currently returns mock data)
    const candidates = await searchCandidates(selectedSource.value, configData.value)
    
    // Update mock candidates with filtered results
    mockCandidates.value.splice(0, mockCandidates.value.length, ...candidates)
    
    setTimeout(() => {
      loading.value = false
      showCandidates.value = true
    }, 1000) // Shorter delay since we have actual logic
  } catch (error) {
    console.error('Error searching candidates:', error)
    loading.value = false
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

const activateCampaign = async () => {
  activating.value = true
  
  try {
    // Prepare campaign data
    const campaignPayload = {
      ...campaignData.value,
      start_date: new Date().toISOString().split('T')[0], // Today
      end_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0], // 30 days from now
      target_segment: "",
      is_active: true,
      // Add config data based on source
      config_data: {
        source: selectedSource.value,
        ...configData.value,
        selectedCandidates: Array.from(selectedCandidates.value)
      }
    }
    
    console.log('Creating campaign with payload:', campaignPayload)
    
    // Call actual API
    const response = await submitNewCampaign(campaignPayload)
    
    if (response && response.success) {
      emit('success', {
        action: 'create',
        data: response.data || campaignPayload
      })
      
      closeWizard()
    } else {
      throw new Error(response?.message || 'Failed to create campaign')
    }
      } catch (error) {
      console.error('Error creating campaign:', error)
      
      // Better error handling with user-friendly messages
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
  campaignData.value = { campaign_name: '', description: '', type: 'NURTURING', status: 'DRAFT' }
  selectedSource.value = ''
  configData.value = {}
  selectedCandidates.value.clear()
  showCandidates.value = false
  loading.value = false
  activating.value = false
  
  // Reset candidates to default
  mockCandidates.value = [
    { id: 'c1', name: 'Nguyễn Văn An', title: 'Senior React Developer', source: 'Nguồn nhân tài' },
    { id: 'c2', name: 'Trần Thị Bình', title: 'Fullstack Engineer', source: 'ATS' },
    { id: 'c3', name: 'Lê Hoàng Cường', title: 'Data Scientist', source: 'Web' },
    { id: 'c4', name: 'Phạm Thị Dung', title: 'React Native Developer', source: 'Nguồn nhân tài' }
  ]
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