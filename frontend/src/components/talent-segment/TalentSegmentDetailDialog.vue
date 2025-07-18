<template>
  <v-dialog 
    :model-value="modelValue" 
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="1200"
    scrollable
  >
    <v-card class="rounded-lg" v-if="segment">
      <!-- Header -->
      <v-card-title class="bg-primary text-white pa-4">
        <div class="d-flex align-center justify-space-between w-100">
          <div class="d-flex align-center">
            <v-avatar 
              size="40" 
              :color="segment.type === 'DYNAMIC' ? 'blue-lighten-1' : 'green-lighten-1'"
              variant="tonal"
              class="mr-3"
            >
              <v-icon size="24" color="white">
                {{ segment.type === 'DYNAMIC' ? 'mdi-robot' : 'mdi-hand' }}
              </v-icon>
            </v-avatar>
            <div>
              <h3 class="text-h6 mb-0">{{ segment.title }}</h3>
              <div class="text-caption opacity-90">
                {{ __('Talent Segment Details') }}
              </div>
            </div>
          </div>
          <div class="d-flex align-center">
            <v-btn
              variant="text"
              icon="mdi-pencil"
              color="white"
              @click="$emit('edit', segment)"
              class="mr-2"
            >
              <v-icon>mdi-pencil</v-icon>
              <v-tooltip activator="parent" location="bottom">{{ __('Edit') }}</v-tooltip>
            </v-btn>
            <v-btn
              variant="text"
              icon="mdi-close"
              color="white"
              @click="$emit('close')"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </div>
        </div>
      </v-card-title>

      <!-- Content -->
      <v-card-text class="pa-0">
        <v-container fluid class="pa-6">
          <v-row>
            <!-- Left Panel - Segment Info -->
            <v-col cols="12" md="4">
              <!-- Basic Info Card -->
              <v-card variant="outlined" class="mb-4">
                <v-card-title class="text-h6 pb-2">Thông tin cơ bản</v-card-title>
                <v-card-text>
                  <div class="mb-3">
                    <div class="text-caption text-medium-emphasis mb-1">Loại phân khúc</div>
                    <v-chip 
                      :color="getTypeColor(segment.type)"
                      variant="tonal"
                      size="small"
                    >
                      {{ getTypeLabel(segment.type) }}
                    </v-chip>
                  </div>

                  <div class="mb-3" v-if="segment.description">
                    <div class="text-caption text-medium-emphasis mb-1">Mô tả</div>
                    <p class="text-body-2">{{ segment.description }}</p>
                  </div>

                  <div class="mb-3" v-if="segment.owner_id">
                    <div class="text-caption text-medium-emphasis mb-1">Người quản lý</div>
                    <div class="d-flex align-center">
                      <v-avatar size="32" :color="getAvatarColor(segment.owner_id)" class="mr-2">
                        <span class="text-caption white--text">
                          {{ getAvatarText(segment.owner_id) }}
                        </span>
                      </v-avatar>
                      <span class="text-body-2">{{ segment.owner_id }}</span>
                    </div>
                  </div>

                  <div class="mb-3">
                    <div class="text-caption text-medium-emphasis mb-1">Ngày tạo</div>
                    <div class="d-flex align-center">
                      <v-icon size="16" color="grey" class="mr-1">mdi-calendar</v-icon>
                      <span class="text-body-2">{{ formatDate(segment.creation) }}</span>
                    </div>
                  </div>

                  <div>
                    <div class="text-caption text-medium-emphasis mb-1">Cập nhật cuối</div>
                    <div class="d-flex align-center">
                      <v-icon size="16" color="grey" class="mr-1">mdi-update</v-icon>
                      <span class="text-body-2">{{ formatDate(segment.modified) }}</span>
                    </div>
                  </div>
                </v-card-text>
              </v-card>

              <!-- Stats Card -->
              <v-card variant="outlined" class="mb-4">
                <v-card-title class="text-h6 pb-2">Thống kê</v-card-title>
                <v-card-text>
                  <div class="mb-4">
                    <div class="text-caption text-medium-emphasis mb-1">Tổng ứng viên</div>
                    <div class="text-h4 font-weight-bold text-primary">
                      {{ segment.candidate_count || 0 }}
                    </div>
                  </div>

                  <div class="mb-4">
                    <div class="text-caption text-medium-emphasis mb-1">Tỷ lệ tương tác</div>
                    <div class="d-flex align-center">
                      <v-progress-linear
                        :model-value="getEngagementRate(segment)"
                        height="12"
                        rounded
                        :color="getEngagementColor(getEngagementRate(segment))"
                        class="flex-grow-1 mr-3"
                      />
                      <span class="text-h6 font-weight-medium">
                        {{ getEngagementRate(segment) }}%
                      </span>
                    </div>
                  </div>

                  <div class="mb-3">
                    <div class="text-caption text-medium-emphasis mb-1">Ứng viên mới (7 ngày)</div>
                    <div class="text-h6 font-weight-medium text-success">+12</div>
                  </div>

                  <div>
                    <div class="text-caption text-medium-emphasis mb-1">Ứng viên hoạt động</div>
                    <div class="text-h6 font-weight-medium text-info">
                      {{ Math.round((segment.candidate_count || 0) * 0.7) }}
                    </div>
                  </div>
                </v-card-text>
              </v-card>

              <!-- AI Config Card (for DYNAMIC segments) -->
              <v-card v-if="segment.type === 'DYNAMIC'" variant="outlined">
                <v-card-title class="text-h6 pb-2">
                  <v-icon class="mr-2" color="blue">mdi-robot</v-icon>
                  Cấu hình AI
                </v-card-title>
                <v-card-text>
                  <div class="mb-3" v-if="segment.ai_criteria">
                    <div class="text-caption text-medium-emphasis mb-1">Tiêu chí AI</div>
                    <p class="text-body-2">{{ segment.ai_criteria }}</p>
                  </div>

                  <div class="mb-3">
                    <div class="text-caption text-medium-emphasis mb-1">Ngưỡng tin cậy</div>
                    <div class="d-flex align-center">
                      <v-progress-linear
                        :model-value="segment.confidence_threshold || 70"
                        height="6"
                        rounded
                        color="blue"
                        class="flex-grow-1 mr-2"
                      />
                      <span class="text-body-2 font-weight-medium">
                        {{ segment.confidence_threshold || 70 }}%
                      </span>
                    </div>
                  </div>

                  <div>
                    <div class="text-caption text-medium-emphasis mb-1">Tự động cập nhật</div>
                    <v-chip 
                      :color="segment.auto_update ? 'success' : 'grey'"
                      variant="tonal"
                      size="small"
                    >
                      {{ segment.auto_update ? 'Bật' : 'Tắt' }}
                    </v-chip>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>

            <!-- Right Panel - Candidates List -->
            <v-col cols="12" md="8">
              <v-card variant="outlined">
                <v-card-title class="d-flex align-center justify-space-between">
                  <span class="text-h6">Danh sách Ứng viên</span>
                  <div class="d-flex align-center">
                    <v-text-field
                      v-model="candidateSearch"
                      placeholder="Tìm kiếm ứng viên..."
                      prepend-inner-icon="mdi-magnify"
                      variant="outlined"
                      density="compact"
                      hide-details
                      style="max-width: 300px;"
                      class="mr-2"
                    />
                    <v-btn
                      color="primary"
                      variant="elevated"
                      size="small"
                      @click="showAddCandidateDialog = true"
                      prepend-icon="mdi-plus"
                    >
                      Thêm ứng viên
                    </v-btn>
                  </div>
                </v-card-title>

                <v-card-text class="pa-0">
                  <!-- Candidates Data Table -->
                  <v-data-table
                    :headers="candidateHeaders"
                    :items="candidates"
                    :loading="loadingCandidates"
                    :search="candidateSearch"
                    item-key="id"
                    class="elevation-0"
                    :items-per-page="10"
                    loading-text="Đang tải danh sách ứng viên..."
                    no-data-text="Chưa có ứng viên nào trong phân khúc này"
                  >
                    <!-- Avatar + Name column -->
                    <template v-slot:item.name="{ item }">
                      <div class="d-flex align-center">
                        <v-avatar size="32" :color="getAvatarColor(item.name)" class="mr-3">
                          <span class="text-caption white--text">
                            {{ getAvatarText(item.name) }}
                          </span>
                        </v-avatar>
                        <div>
                          <div class="font-weight-medium">{{ item.name }}</div>
                          <div class="text-caption text-medium-emphasis">{{ item.email }}</div>
                        </div>
                      </div>
                    </template>

                    <!-- Position column -->
                    <template v-slot:item.position="{ item }">
                      <div>
                        <div class="font-weight-medium">{{ item.position || 'Chưa cập nhật' }}</div>
                        <div class="text-caption text-medium-emphasis">{{ item.experience || '' }}</div>
                      </div>
                    </template>

                    <!-- Status column -->
                    <template v-slot:item.status="{ item }">
                      <v-chip 
                        size="small" 
                        :color="getCandidateStatusColor(item.status)"
                        variant="tonal"
                      >
                        {{ getCandidateStatusLabel(item.status) }}
                      </v-chip>
                    </template>

                    <!-- Score column -->
                    <template v-slot:item.score="{ item }">
                      <div class="d-flex align-center">
                        <v-progress-circular
                          :model-value="item.score || 0"
                          size="24"
                          width="3"
                          :color="getScoreColor(item.score || 0)"
                          class="mr-2"
                        />
                        <span class="text-body-2 font-weight-medium">{{ item.score || 0 }}/100</span>
                      </div>
                    </template>

                    <!-- Actions column -->
                    <template v-slot:item.actions="{ item }">
                      <v-menu>
                        <template v-slot:activator="{ props }">
                          <v-btn
                            v-bind="props"
                            variant="text"
                            icon="mdi-dots-vertical"
                            size="small"
                          />
                        </template>
                        <v-list density="compact">
                          <v-list-item @click="viewCandidateDetails(item)">
                            <template v-slot:prepend>
                              <v-icon size="18">mdi-eye</v-icon>
                            </template>
                            <v-list-item-title>Xem hồ sơ</v-list-item-title>
                          </v-list-item>
                          <v-list-item @click="editCandidate(item)">
                            <template v-slot:prepend>
                              <v-icon size="18">mdi-pencil</v-icon>
                            </template>
                            <v-list-item-title>Chỉnh sửa</v-list-item-title>
                          </v-list-item>
                          <v-divider />
                          <v-list-item @click="removeCandidateFromSegment(item)" class="text-error">
                            <template v-slot:prepend>
                              <v-icon size="18" color="error">mdi-delete</v-icon>
                            </template>
                            <v-list-item-title>Xóa khỏi phân khúc</v-list-item-title>
                          </v-list-item>
                        </v-list>
                      </v-menu>
                    </template>

                    <!-- No data template -->
                    <template v-slot:no-data>
                      <div class="text-center py-8">
                        <v-icon size="48" color="grey-lighten-2">mdi-account-outline</v-icon>
                        <div class="text-h6 mt-2 mb-1">{{ __('No candidates yet') }}</div>
                        <div class="text-body-2 text-medium-emphasis mb-4">
                          {{ __('This segment has no candidates yet') }}
                        </div>
                        <v-btn 
                          color="primary" 
                          variant="outlined"
                          @click="showAddCandidateDialog = true"
                          prepend-icon="mdi-plus"
                        >
                          {{ __('Add first candidate') }}
                        </v-btn>
                      </div>
                    </template>
                  </v-data-table>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

      <!-- Actions -->
      <v-card-actions class="pa-6 pt-0">
        <v-spacer />
        <v-btn
          variant="text"
          @click="$emit('close')"
        >
          {{ __('Close') }}
        </v-btn>
        <v-btn
          color="primary"
          variant="elevated"
          @click="$emit('edit', segment)"
        >
          {{ __('Edit Segment') }}
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Add Candidate Dialog (placeholder) -->
    <v-dialog v-model="showAddCandidateDialog" max-width="600">
      <v-card>
        <v-card-title>{{ __('Add candidate to segment') }}</v-card-title>
        <v-card-text>
          <p>{{ __('The add candidate feature will be developed in the next phase.') }}</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="showAddCandidateDialog = false">{{ __('Close') }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { getSegmentCandidates, calculateEngagementRate, formatDate } from '@/services/talentSegmentService'

// Translation helper function


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
const emit = defineEmits(['update:modelValue', 'edit', 'delete', 'close'])

// Local state
const candidates = ref([])
const loadingCandidates = ref(false)
const candidateSearch = ref('')
const showAddCandidateDialog = ref(false)

// Sample candidate data (sẽ được thay thế bằng API thực)
const sampleCandidates = [
  {
    id: 1,
    name: 'Nguyễn Văn A',
    email: 'nguyenvana@email.com',
    position: 'Frontend Developer',
    experience: '3 năm kinh nghiệm',
    status: 'ACTIVE',
    score: 85
  },
  {
    id: 2,
    name: 'Trần Thị B',
    email: 'tranthib@email.com',
    position: 'Backend Developer',
    experience: '5 năm kinh nghiệm',
    status: 'POTENTIAL',
    score: 92
  },
  {
    id: 3,
    name: 'Lê Văn C',
    email: 'levanc@email.com',
    position: 'Full Stack Developer',
    experience: '2 năm kinh nghiệm',
    status: 'INACTIVE',
    score: 76
  }
]

// Table headers for candidates
const candidateHeaders = [
  {
    title: 'Candidate',
    key: 'name',
    sortable: true,
    width: '30%'
  },
  {
    title: 'Position',
    key: 'position',
    sortable: true,
    width: '25%'
  },
  {
    title: 'Status',
    key: 'status',
    sortable: true,
    width: '15%'
  },
  {
    title: 'Score',
    key: 'score',
    sortable: true,
    width: '15%'
  },
  {
    title: 'Actions',
    key: 'actions',
    sortable: false,
    width: '15%',
    align: 'center'
  }
]

// Helper functions
const getTypeColor = (type) => {
  return type === 'DYNAMIC' ? 'blue' : 'green'
}

const getTypeLabel = (type) => {
  return type === 'DYNAMIC' ? 'Automatic (AI)' : 'Manual'
}

const getEngagementRate = (segment) => {
  return calculateEngagementRate(segment.candidate_count || 0)
}

const getEngagementColor = (rate) => {
  if (rate >= 70) return 'success'
  if (rate >= 40) return 'warning'
  return 'error'
}

const getAvatarColor = (name) => {
  const colors = ['primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success']
  const hash = name?.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0)
    return a & a
  }, 0) || 0
  return colors[Math.abs(hash) % colors.length]
}

const getAvatarText = (name) => {
  if (!name) return ''
  return name.split(' ').map(word => word[0]).join('').toUpperCase().substring(0, 2)
}

const getCandidateStatusColor = (status) => {
  const statusColors = {
    'ACTIVE': 'success',
    'POTENTIAL': 'warning',
    'INACTIVE': 'grey'
  }
  return statusColors[status] || 'grey'
}

const getCandidateStatusLabel = (status) => {
  const statusLabels = {
    'ACTIVE': 'Active',
    'POTENTIAL': 'Potential',
    'INACTIVE': 'Inactive'
  }
  return statusLabels[status] || 'Unknown'
}

const getScoreColor = (score) => {
  if (score >= 80) return 'success'
  if (score >= 60) return 'warning'
  return 'error'
}

// Event handlers
const loadCandidates = async () => {
  if (!props.segment) return
  
  loadingCandidates.value = true
  try {
    // TODO: Replace with actual API call
    // const result = await getSegmentCandidates(props.segment.name)
    // candidates.value = result || []
    
    // Use sample data for now
    candidates.value = sampleCandidates
  } catch (error) {
    console.error('Error loading candidates:', error)
    candidates.value = []
  } finally {
    loadingCandidates.value = false
  }
}

const viewCandidateDetails = (candidate) => {
  console.log('View candidate details:', candidate)
  // TODO: Implement candidate detail view
}

const editCandidate = (candidate) => {
  console.log('Edit candidate:', candidate)
  // TODO: Implement candidate edit
}

const removeCandidateFromSegment = (candidate) => {
  console.log('Remove candidate from segment:', candidate)
  // TODO: Implement remove candidate
}

// Watch for dialog open/close
watch(() => props.modelValue, (isOpen) => {
  if (isOpen && props.segment) {
    loadCandidates()
  }
})

// Initialize
onMounted(() => {
  if (props.modelValue && props.segment) {
    loadCandidates()
  }
})
</script>

<style scoped>
/* Dialog styling */
:deep(.v-dialog > .v-overlay__content) {
  border-radius: 12px;
  overflow: hidden;
}

/* Avatar text color fix */
.v-avatar .white--text {
  color: white !important;
}

/* Progress styling */
:deep(.v-progress-linear) {
  border-radius: 4px;
}

:deep(.v-progress-circular) {
  font-weight: 600;
}

/* Card styling */
.v-card {
  border-radius: 8px;
}

/* Data table styling */
:deep(.v-data-table) {
  border-radius: 0;
}

:deep(.v-data-table-header) {
  background-color: rgb(var(--v-theme-surface-variant));
}

/* Menu styling */
:deep(.v-menu > .v-overlay__content) {
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Tooltip styling */
:deep(.v-tooltip > .v-overlay__content) {
  background: rgba(0, 0, 0, 0.8) !important;
  color: white !important;
  border-radius: 6px;
  font-size: 12px;
  padding: 6px 12px;
}

/* Button styling */
.v-btn {
  text-transform: none;
  font-weight: 500;
}

/* Stats card styling */
.text-h4 {
  line-height: 1.2;
}

/* Search field styling */
:deep(.v-text-field .v-field) {
  border-radius: 8px;
}
</style> 