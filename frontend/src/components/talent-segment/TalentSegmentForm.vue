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
                        <v-textarea
                          v-model="formData.ai_criteria"
                          label="Tiêu chí AI"
                          placeholder="Mô tả các tiêu chí để AI tự động phân loại ứng viên..."
                          variant="outlined"
                          rows="3"
                          auto-grow
                          hint="AI sẽ sử dụng các tiêu chí này để tự động thêm ứng viên vào phân khúc"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-slider
                          v-model="formData.confidence_threshold"
                          label="Ngưỡng tin cậy"
                          min="0"
                          max="100"
                          step="5"
                          thumb-label
                          :thumb-size="24"
                          track-color="grey-lighten-3"
                          hint="AI chỉ thêm ứng viên khi độ tin cậy >= ngưỡng này"
                        >
                          <template v-slot:thumb-label="{ modelValue }">
                            {{ modelValue }}%
                          </template>
                        </v-slider>
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-switch
                          v-model="formData.auto_update"
                          label="Tự động cập nhật"
                          color="primary"
                          inset
                          hint="Cho phép AI tự động thêm/xóa ứng viên"
                        />
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
import { 
  createNewTalentSegment, 
  updateTalentSegmentDetails, 
  getUserOptions,
  validateTalentSegmentForm 
} from '@/services/talentSegmentService'

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
  ai_criteria: '',
  confidence_threshold: 70,
  auto_update: false
})

// Computed
const isEditing = computed(() => !!props.segment)

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

const resetForm = () => {
  formData.value = {
    title: '',
    description: '',
    type: 'MANUAL',
    owner_id: '',
    candidate_count: 0,
    ai_criteria: '',
    confidence_threshold: 70,
    auto_update: false
  }
}

const loadUserOptions = async () => {
  loadingUsers.value = true
  try {
    const users = await getUserOptions()
    userOptions.value = users
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
    // Validate form data
    const validation = validateTalentSegmentForm(formData.value)
    if (!validation.isValid) {
      // Handle validation errors
      return
    }

    let result
    if (isEditing.value) {
      result = await updateTalentSegmentDetails(props.segment.name, formData.value)
    } else {
      result = await createNewTalentSegment(formData.value)
    }

    if (result) {
      emit('success')
      handleCancel()
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
  if (newSegment && props.modelValue) {
    formData.value = {
      title: newSegment.title || '',
      description: newSegment.description || '',
      type: newSegment.type || 'MANUAL',
      owner_id: newSegment.owner_id || '',
      candidate_count: newSegment.candidate_count || 0,
      ai_criteria: newSegment.ai_criteria || '',
      confidence_threshold: newSegment.confidence_threshold || 70,
      auto_update: newSegment.auto_update || false
    }
  }
}, { immediate: true })

// Watch for dialog open/close
watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    loadUserOptions()
    if (!props.segment) {
      resetForm()
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