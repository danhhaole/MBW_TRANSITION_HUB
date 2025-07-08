<template>
  <v-dialog 
    :model-value="modelValue" 
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="600"
    persistent
    scrollable
  >
    <v-card class="rounded-lg">
      <!-- Header -->
      <v-card-title class="bg-primary text-white pa-4">
        <div class="d-flex align-center">
          <v-icon class="mr-3">mdi-account-group</v-icon>
          <div>
            <h3 class="text-h6 mb-0">
              {{ isEditing ? 'Chỉnh sửa Phân khúc' : 'Tạo Phân khúc Mới' }}
            </h3>
            <div class="text-caption opacity-90">
              {{ isEditing ? 'Cập nhật thông tin phân khúc' : 'Định nghĩa phân khúc nhân tài' }}
            </div>
          </div>
        </div>
      </v-card-title>

      <!-- Form Content -->
      <v-card-text class="pa-6">
        <v-form v-model="formValid" @submit.prevent="handleSubmit">
          <v-row>
            <!-- Title -->
            <v-col cols="12">
              <v-text-field
                v-model="formData.title"
                label="Tên phân khúc *"
                placeholder="Nhập tên phân khúc..."
                variant="outlined"
                :rules="titleRules"
                required
                clearable
                counter="100"
                hint="Tên này sẽ được hiển thị trong danh sách phân khúc"
              />
            </v-col>

            <!-- Description -->
            <v-col cols="12">
              <v-textarea
                v-model="formData.description"
                label="Mô tả"
                placeholder="Mô tả chi tiết về phân khúc này..."
                variant="outlined"
                rows="3"
                auto-grow
                counter="500"
                :rules="descriptionRules"
                hint="Mô tả sẽ giúp người khác hiểu rõ mục đích của phân khúc"
              />
            </v-col>

            <!-- Type -->
            <v-col cols="12" md="6">
              <v-select
                v-model="formData.type"
                :items="typeOptions"
                label="Loại phân khúc *"
                variant="outlined"
                :rules="typeRules"
                required
              >
                <template v-slot:item="{ props, item }">
                  <v-list-item v-bind="props" :title="item.title">
                    <template v-slot:prepend>
                      <v-icon :color="item.raw.color">{{ item.raw.icon }}</v-icon>
                    </template>
                    <template v-slot:subtitle>
                      {{ item.raw.description }}
                    </template>
                  </v-list-item>
                </template>
                <template v-slot:selection="{ item }">
                  <div class="d-flex align-center">
                    <v-icon :color="item.raw.color" class="mr-2">{{ item.raw.icon }}</v-icon>
                    {{ item.title }}
                  </div>
                </template>
              </v-select>
            </v-col>

            <!-- Owner ID -->
            <v-col cols="12" md="6">
              <v-autocomplete
                v-model="formData.owner_id"
                :items="userOptions"
                label="Người quản lý"
                placeholder="Chọn người quản lý..."
                variant="outlined"
                clearable
                :loading="loadingUsers"
                item-title="full_name"
                item-value="name"
                :rules="ownerRules"
              >
                <template v-slot:item="{ props, item }">
                  <v-list-item v-bind="props" :title="item.raw.full_name">
                    <template v-slot:prepend>
                      <v-avatar size="32" :color="getAvatarColor(item.raw.name)">
                        <span class="text-caption white--text">
                          {{ getAvatarText(item.raw.full_name) }}
                        </span>
                      </v-avatar>
                    </template>
                    <template v-slot:subtitle>
                      {{ item.raw.email }}
                    </template>
                  </v-list-item>
                </template>
                <template v-slot:selection="{ item }">
                  <div class="d-flex align-center">
                    <v-avatar size="24" :color="getAvatarColor(item.raw.name)" class="mr-2">
                      <span class="text-caption white--text">
                        {{ getAvatarText(item.raw.full_name) }}
                      </span>
                    </v-avatar>
                    {{ item.raw.full_name }}
                  </div>
                </template>
              </v-autocomplete>
            </v-col>

            <!-- Candidate Count (if editing) -->
            <v-col v-if="isEditing" cols="12" md="6">
              <v-text-field
                v-model.number="formData.candidate_count"
                label="Số lượng ứng viên"
                type="number"
                variant="outlined"
                min="0"
                :rules="candidateCountRules"
                hint="Số lượng ứng viên hiện tại trong phân khúc"
              />
            </v-col>

            <!-- AI Configuration (only for DYNAMIC type) -->
            <v-col v-if="formData.type === 'DYNAMIC'" cols="12">
              <v-expansion-panels variant="accordion">
                <v-expansion-panel>
                  <v-expansion-panel-title>
                    <div class="d-flex align-center">
                      <v-icon class="mr-2" color="blue">mdi-robot</v-icon>
                      Cấu hình AI (Tùy chọn)
                    </div>
                  </v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <v-row>
                      <v-col cols="12">
                        <div class="mb-4">
                          <h4 class="text-h6 mb-2">Tiêu chí AI</h4>
                          <p class="text-caption text-medium-emphasis">
                            Cấu hình các tiêu chí để AI tự động phân loại ứng viên
                          </p>
                        </div>
                        
                        <!-- Skills Selection -->
                        <div class="mb-4">
                          <label class="text-subtitle-2 font-weight-medium mb-2 d-block">
                            Kỹ năng cần thiết
                          </label>
                          <v-combobox
                            v-model="criteriaForm.skills"
                            :items="skillOptions"
                            label="Chọn hoặc nhập kỹ năng"
                            placeholder="Ví dụ: Java, Spring, React..."
                            variant="outlined"
                            multiple
                            chips
                            closable-chips
                            clearable
                            hint="Nhấn Enter để thêm kỹ năng mới"
                            persistent-hint
                          />
                        </div>

                        <!-- Experience Years -->
                        <div class="mb-4">
                          <label class="text-subtitle-2 font-weight-medium mb-2 d-block">
                            Kinh nghiệm làm việc
                          </label>
                          <v-row>
                            <v-col cols="4">
                              <v-select
                                v-model="criteriaForm.experienceOperator"
                                :items="experienceOperators"
                                label="Điều kiện"
                                variant="outlined"
                                density="compact"
                              />
                            </v-col>
                            <v-col cols="8">
                              <v-text-field
                                v-model.number="criteriaForm.experienceYears"
                                label="Số năm kinh nghiệm"
                                type="number"
                                variant="outlined"
                                density="compact"
                                min="0"
                                max="50"
                                suffix="năm"
                              />
                            </v-col>
                          </v-row>
                        </div>

                        <!-- Location -->
                        <div class="mb-4">
                          <label class="text-subtitle-2 font-weight-medium mb-2 d-block">
                            Địa điểm làm việc
                          </label>
                          <v-combobox
                            v-model="criteriaForm.locations"
                            :items="locationOptions"
                            label="Chọn hoặc nhập địa điểm"
                            placeholder="Ví dụ: Hà Nội, TP.HCM..."
                            variant="outlined"
                            multiple
                            chips
                            closable-chips
                            clearable
                          />
                        </div>

                        <!-- Education Level -->
                        <div class="mb-4">
                          <label class="text-subtitle-2 font-weight-medium mb-2 d-block">
                            Trình độ học vấn
                          </label>
                          <v-select
                            v-model="criteriaForm.educationLevel"
                            :items="educationLevels"
                            label="Chọn trình độ học vấn"
                            variant="outlined"
                            clearable
                          />
                        </div>

                        <!-- Salary Range -->
                        <div class="mb-4">
                          <label class="text-subtitle-2 font-weight-medium mb-2 d-block">
                            Mức lương mong muốn (triệu VND)
                          </label>
                          <v-row>
                            <v-col cols="6">
                              <v-text-field
                                v-model.number="criteriaForm.salaryMin"
                                label="Từ"
                                type="number"
                                variant="outlined"
                                density="compact"
                                min="0"
                                suffix="triệu"
                              />
                            </v-col>
                            <v-col cols="6">
                              <v-text-field
                                v-model.number="criteriaForm.salaryMax"
                                label="Đến"
                                type="number"
                                variant="outlined"
                                density="compact"
                                min="0"
                                suffix="triệu"
                              />
                            </v-col>
                          </v-row>
                        </div>
                      </v-col>
                    </v-row>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>

      <!-- Actions -->
      <v-card-actions class="pa-6 pt-0">
        <v-spacer />
        <v-btn
          variant="text"
          @click="handleCancel"
          :disabled="loading"
        >
          Hủy
        </v-btn>
        <v-btn
          color="primary"
          variant="elevated"
          @click="handleSubmit"
          :loading="loading"
          :disabled="!formValid"
        >
          {{ isEditing ? 'Cập nhật' : 'Tạo mới' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { talentSegmentService, userService } from '@/services/universalService'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  segment: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'success', 'close'])

// Local state
const loading = ref(false)
const loadingUsers = ref(false)
const formValid = ref(false)
const userOptions = ref([])

const formData = ref({
  title: '',
  description: '',
  type: 'MANUAL',
  owner_id: '',
  candidate_count: 0,
  criteria: '{}'
})

// Criteria form for better UX
const criteriaForm = ref({
  skills: [],
  experienceOperator: '>=',
  experienceYears: null,
  locations: [],
  educationLevel: '',
  salaryMin: null,
  salaryMax: null
})

// Options for form fields
const skillOptions = ref([
  'Java', 'JavaScript', 'Python', 'C#', 'PHP', 'C++', 'React', 'Angular', 'Vue.js',
  'Node.js', 'Spring', 'Django', 'Laravel', 'ASP.NET', 'MySQL', 'PostgreSQL',
  'MongoDB', 'Redis', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'Git', 'Linux',
  'HTML', 'CSS', 'TypeScript', 'GraphQL', 'REST API', 'Microservices'
])

const locationOptions = ref([
  'Hà Nội', 'TP.HCM', 'Đà Nẵng', 'Cần Thơ', 'Hải Phòng', 'Bình Dương',
  'Đồng Nai', 'Quảng Ninh', 'Thừa Thiên Huế', 'Khánh Hòa', 'Remote'
])

const experienceOperators = ref([
  { title: 'Ít nhất', value: '>=' },
  { title: 'Chính xác', value: '==' },
  { title: 'Nhiều hơn', value: '>' },
  { title: 'Ít hơn', value: '<' },
  { title: 'Tối đa', value: '<=' }
])

const educationLevels = ref([
  { title: 'Trung học phổ thông', value: 'high_school' },
  { title: 'Trung cấp', value: 'vocational' },
  { title: 'Cao đẳng', value: 'college' },
  { title: 'Đại học', value: 'university' },
  { title: 'Thạc sĩ', value: 'master' },
  { title: 'Tiến sĩ', value: 'phd' }
])

// Computed
const isEditing = computed(() => !!props.segment)

// Convert form to JSON criteria
const convertFormToCriteria = () => {
  const criteria = {}
  
  // Add skills if any
  if (criteriaForm.value.skills?.length > 0) {
    criteria.skills = criteriaForm.value.skills
  }
  
  // Add experience years if specified
  if (criteriaForm.value.experienceYears !== null && criteriaForm.value.experienceYears !== '') {
    criteria.experienceYears = `${criteriaForm.value.experienceOperator}${criteriaForm.value.experienceYears}`
  }
  
  // Add locations if any
  if (criteriaForm.value.locations?.length > 0) {
    criteria.locations = criteriaForm.value.locations
  }
  
  // Add education level if specified
  if (criteriaForm.value.educationLevel) {
    criteria.educationLevel = criteriaForm.value.educationLevel
  }
  
  // Add salary range if specified
  if (criteriaForm.value.salaryMin !== null || criteriaForm.value.salaryMax !== null) {
    const salaryRange = {}
    if (criteriaForm.value.salaryMin !== null && criteriaForm.value.salaryMin !== '') {
      salaryRange.min = criteriaForm.value.salaryMin
    }
    if (criteriaForm.value.salaryMax !== null && criteriaForm.value.salaryMax !== '') {
      salaryRange.max = criteriaForm.value.salaryMax
    }
    if (Object.keys(salaryRange).length > 0) {
      criteria.salaryRange = salaryRange
    }
  }
  
  return JSON.stringify(criteria)
}

// Type options
const typeOptions = [
  {
    title: 'Thủ công',
    value: 'MANUAL',
    icon: 'mdi-hand',
    color: 'green',
    description: 'Thêm ứng viên thủ công'
  },
  {
    title: 'Tự động (AI)',
    value: 'DYNAMIC',
    icon: 'mdi-robot',
    color: 'blue',
    description: 'AI tự động phân loại ứng viên'
  }
]

// Validation rules
const titleRules = [
  v => !!v || 'Tên phân khúc là bắt buộc',
  v => (v && v.length >= 3) || 'Tên phân khúc phải có ít nhất 3 ký tự',
  v => (v && v.length <= 100) || 'Tên phân khúc không được quá 100 ký tự'
]

const descriptionRules = [
  v => !v || v.length <= 500 || 'Mô tả không được quá 500 ký tự'
]

const typeRules = [
  v => !!v || 'Loại phân khúc là bắt buộc'
]

const ownerRules = [
  // Owner is optional, no validation needed
]

const candidateCountRules = [
  v => v === '' || v === null || v >= 0 || 'Số lượng ứng viên phải >= 0'
]

// Helper functions
const getAvatarColor = (userId) => {
  const colors = ['primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success']
  const hash = userId?.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0)
    return a & a
  }, 0) || 0
  return colors[Math.abs(hash) % colors.length]
}

const getAvatarText = (fullName) => {
  if (!fullName) return ''
  return fullName.split(' ').map(name => name[0]).join('').toUpperCase().substring(0, 2)
}

// Convert JSON criteria to form
const parseCriteriaToForm = (criteriaJson) => {
  try {
    const criteria = JSON.parse(criteriaJson || '{}')
    
    criteriaForm.value = {
      skills: criteria.skills || [],
      experienceOperator: '>=',
      experienceYears: null,
      locations: criteria.locations || [],
      educationLevel: criteria.educationLevel || '',
      salaryMin: criteria.salaryRange?.min || null,
      salaryMax: criteria.salaryRange?.max || null
    }
    
    // Parse experience years
    if (criteria.experienceYears) {
      const expStr = criteria.experienceYears.toString()
      const match = expStr.match(/^([><=]+)(.+)$/)
      if (match) {
        criteriaForm.value.experienceOperator = match[1]
        criteriaForm.value.experienceYears = parseInt(match[2])
      }
    }
  } catch (error) {
    console.error('Error parsing criteria JSON:', error)
    // Reset to default values if JSON is invalid
    criteriaForm.value = {
      skills: [],
      experienceOperator: '>=',
      experienceYears: null,
      locations: [],
      educationLevel: '',
      salaryMin: null,
      salaryMax: null
    }
  }
}

const resetForm = () => {
  formData.value = {
    title: '',
    description: '',
    type: 'MANUAL',
    owner_id: '',
    candidate_count: 0,
    criteria: '{}'
  }
  
  criteriaForm.value = {
    skills: [],
    experienceOperator: '>=',
    experienceYears: null,
    locations: [],
    educationLevel: '',
    salaryMin: null,
    salaryMax: null
  }
}

const loadUserOptions = async () => {
  loadingUsers.value = true
  try {
    const result = await userService.getList({ fields: ['name', 'full_name', 'email'] })
    if (result.success) {
      userOptions.value = result.data
    }
  } catch (error) {
    console.error('Error loading users:', error)
  } finally {
    loadingUsers.value = false
  }
}

// Event handlers
const handleSubmit = async () => {
  if (!formValid.value) return

  loading.value = true
  try {
    // Convert form criteria to JSON
    const criteriaJson = convertFormToCriteria()
    
    // Prepare data to submit
    const dataToSubmit = { 
      ...formData.value,
      criteria: criteriaJson || '{}'
    }
    
    // Ensure criteria is valid JSON
    try {
      JSON.parse(dataToSubmit.criteria)
    } catch (e) {
      console.error('Invalid JSON in criteria:', e)
      dataToSubmit.criteria = '{}'
    }

    let result
    if (isEditing.value) {
      result = await talentSegmentService.save(dataToSubmit, props.segment.name)
    } else {
      result = await talentSegmentService.save(dataToSubmit)
    }

    if (result.success) {
      emit('success')
      handleCancel()
    } else {
      console.error('Error saving talent segment:', result.message)
    }
  } catch (error) {
    console.error('Error submitting form:', error)
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  emit('update:modelValue', false)
  emit('close')
  resetForm()
}

// Watch for segment changes (editing mode)
watch(() => props.segment, (newSegment) => {
  if (newSegment && Object.keys(newSegment).length > 0) {
    formData.value = {
      title: newSegment.title || '',
      description: newSegment.description || '',
      type: newSegment.type || 'MANUAL',
      owner_id: newSegment.owner_id || '',
      candidate_count: newSegment.candidate_count || 0,
      criteria: newSegment.criteria || '{}'
    }
    // Parse criteria to form
    parseCriteriaToForm(newSegment.criteria)
  }
}, { immediate: true, deep: true })

// Watch for dialog open/close
watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    loadUserOptions()
    if (!props.segment) {
      resetForm()
    } else if (props.segment && Object.keys(props.segment).length > 0) {
      // Populate form data when modal opens with existing segment
      formData.value = {
        title: props.segment.title || '',
        description: props.segment.description || '',
        type: props.segment.type || 'MANUAL',
        owner_id: props.segment.owner_id || '',
        candidate_count: props.segment.candidate_count || 0,
        criteria: props.segment.criteria || '{}'
      }
      // Parse criteria to form
      parseCriteriaToForm(props.segment.criteria)
    }
  }
})

// Watch for type changes
watch(() => formData.value.type, (newType) => {
  if (newType === 'MANUAL') {
    formData.value.criteria = '{}'
    // Reset criteria form
    criteriaForm.value = {
      skills: [],
      experienceOperator: '>=',
      experienceYears: null,
      locations: [],
      educationLevel: '',
      salaryMin: null,
      salaryMax: null
    }
  }
})

// Initialize
onMounted(() => {
  loadUserOptions()
})
</script>

<style scoped>
/* Dialog styling */
:deep(.v-dialog > .v-overlay__content) {
  border-radius: 12px;
  overflow: hidden;
}

/* Form styling */
:deep(.v-text-field .v-field) {
  border-radius: 8px;
}

:deep(.v-textarea .v-field) {
  border-radius: 8px;
}

:deep(.v-select .v-field) {
  border-radius: 8px;
}

:deep(.v-autocomplete .v-field) {
  border-radius: 8px;
}

/* Avatar text color fix */
.v-avatar .white--text {
  color: white !important;
}

/* Slider styling */
:deep(.v-slider-thumb) {
  border: 2px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* Switch styling */
:deep(.v-switch .v-selection-control__input) {
  border-radius: 16px;
}

/* Expansion panel styling */
:deep(.v-expansion-panel) {
  border-radius: 8px !important;
  margin-bottom: 8px;
}

:deep(.v-expansion-panel-title) {
  padding: 16px;
}

:deep(.v-expansion-panel-text__wrapper) {
  padding: 0 16px 16px 16px;
}

/* Card actions spacing */
.v-card-actions {
  border-top: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

/* Button styling */
.v-btn {
  text-transform: none;
  font-weight: 500;
}
</style>