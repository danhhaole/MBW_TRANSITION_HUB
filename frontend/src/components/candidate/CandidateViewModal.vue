<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="800px"
    persistent
    scrollable
  >
    <v-card class="candidate-view-modal">
      <!-- Header -->
      <v-card-title class="d-flex align-center justify-space-between pa-6 bg-primary">
        <div class="d-flex align-center">
          <v-avatar
            :color="getAvatarColor(candidate?.full_name)"
            size="48"
            class="mr-4"
          >
            <v-img
              v-if="candidate?.avatar"
              :src="candidate.avatar"
              :alt="candidate.full_name"
            />
            <span
              v-else
              class="text-white font-weight-medium text-h6"
            >
              {{ getAvatarText(candidate?.full_name) }}
            </span>
          </v-avatar>
          
          <div>
            <h2 class="text-h5 text-white font-weight-medium mb-1">
              {{ candidate?.full_name || 'Chi tiết ứng viên' }}
            </h2>
            <div class="text-body-2 text-blue-lighten-3">
              {{ candidate?.headline || 'Chưa có thông tin chức danh' }}
            </div>
          </div>
        </div>
        
        <v-btn
          icon="mdi-close"
          variant="text"
          color="white"
          @click="$emit('update:modelValue', false)"
        />
      </v-card-title>

      <!-- Loading State -->
      <div v-if="loading" class="pa-6">
        <v-skeleton-loader
          type="avatar, text, chip, text, divider, text, text, divider, chip"
        />
      </div>

      <!-- Content -->
      <v-card-text v-else-if="candidate" class="pa-0">
        <!-- Status and Actions -->
        <div class="d-flex align-center justify-space-between pa-6 bg-grey-lighten-5">
          <div class="d-flex align-center">
            <v-chip
              :color="getStatusChipColor(candidate.status)"
              size="default"
              variant="flat"
              class="mr-3"
            >
              <v-icon start size="18">mdi-account-check</v-icon>
              {{ formatCandidateStatus(candidate.status).text }}
            </v-chip>
            
            <!-- Engagement Score -->
            <div class="d-flex align-center">
              <span class="text-caption mr-2">Điểm tương tác:</span>
              <v-progress-linear
                :model-value="calculateEngagementScore(candidate)"
                :color="getEngagementColor(calculateEngagementScore(candidate))"
                height="8"
                rounded
                style="width: 100px;"
                class="mr-2"
              />
              <span class="text-caption font-weight-medium">
                {{ calculateEngagementScore(candidate) }}%
              </span>
            </div>
          </div>
          
          <div class="d-flex align-center">
            <v-btn
              color="primary"
              variant="outlined"
              prepend-icon="mdi-pencil"
              @click="$emit('edit-candidate', candidate)"
            >
              Chỉnh sửa
            </v-btn>
            <v-menu>
              <template v-slot:activator="{ props }">
                <v-btn
                  v-bind="props"
                  icon="mdi-dots-vertical"
                  variant="text"
                  class="ml-2"
                />
              </template>
              <v-list>
                <v-list-item @click="$emit('duplicate-candidate', candidate)">
                  <template v-slot:prepend>
                    <v-icon>mdi-content-copy</v-icon>
                  </template>
                  <v-list-item-title>Sao chép</v-list-item-title>
                </v-list-item>
                <v-list-item @click="downloadCV">
                  <template v-slot:prepend>
                    <v-icon>mdi-download</v-icon>
                  </template>
                  <v-list-item-title>Tải CV</v-list-item-title>
                </v-list-item>
                <v-divider />
                <v-list-item 
                  @click="$emit('delete-candidate', candidate)"
                  class="text-error"
                >
                  <template v-slot:prepend>
                    <v-icon color="error">mdi-delete</v-icon>
                  </template>
                  <v-list-item-title>Xóa</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </div>
        </div>

        <!-- Main Content in 2 Columns -->
        <div class="d-flex">
          <!-- Left Column -->
          <div class="flex-grow-1 pa-6">
            <!-- Contact Information -->
            <div class="mb-6">
              <h3 class="text-h6 font-weight-medium mb-4 d-flex align-center">
                <v-icon class="mr-2" color="primary">mdi-account-details</v-icon>
                Thông tin liên hệ
              </h3>
              
              <div class="contact-info">
                <div class="d-flex align-center mb-3">
                  <v-icon class="mr-3" color="medium-emphasis">mdi-email</v-icon>
                  <div>
                    <div class="text-body-1">{{ candidate.email }}</div>
                    <div class="text-caption text-medium-emphasis">Email</div>
                  </div>
                  <v-spacer />
                  <v-btn
                    size="small"
                    variant="text"
                    color="primary"
                    :href="`mailto:${candidate.email}`"
                    target="_blank"
                  >
                    <v-icon>mdi-email-send</v-icon>
                  </v-btn>
                </div>
                
                <div v-if="candidate.phone" class="d-flex align-center mb-3">
                  <v-icon class="mr-3" color="medium-emphasis">mdi-phone</v-icon>
                  <div>
                    <div class="text-body-1">{{ candidate.phone }}</div>
                    <div class="text-caption text-medium-emphasis">Điện thoại</div>
                  </div>
                  <v-spacer />
                  <v-btn
                    size="small"
                    variant="text"
                    color="primary"
                    :href="`tel:${candidate.phone}`"
                  >
                    <v-icon>mdi-phone-dial</v-icon>
                  </v-btn>
                </div>
                
                <div v-if="candidate.source" class="d-flex align-center mb-3">
                  <v-icon class="mr-3" color="medium-emphasis">mdi-source-branch</v-icon>
                  <div>
                    <div class="text-body-1">{{ candidate.source }}</div>
                    <div class="text-caption text-medium-emphasis">Nguồn</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Skills -->
            <div class="mb-6">
              <h3 class="text-h6 font-weight-medium mb-4 d-flex align-center">
                <v-icon class="mr-2" color="primary">mdi-tools</v-icon>
                Kỹ năng
              </h3>
              
              <div v-if="candidate.skills && candidate.skills.length > 0" class="d-flex flex-wrap" style="gap: 8px;">
                <v-chip
                  v-for="skill in candidate.skills"
                  :key="skill"
                  variant="outlined"
                  color="primary"
                  size="default"
                >
                  {{ skill }}
                </v-chip>
              </div>
              <div v-else class="text-medium-emphasis">
                Chưa có thông tin kỹ năng
              </div>
            </div>

            <!-- AI Summary -->
            <div v-if="candidate.ai_summary" class="mb-6">
              <h3 class="text-h6 font-weight-medium mb-4 d-flex align-center">
                <v-icon class="mr-2" color="primary">mdi-brain</v-icon>
                Tóm tắt AI
              </h3>
              
              <div class="bg-grey-lighten-4 pa-4 rounded">
                <p class="text-body-1 mb-0">{{ candidate.ai_summary }}</p>
              </div>
            </div>

            <!-- CV Download -->
            <div v-if="candidate.cv_original_url" class="mb-6">
              <h3 class="text-h6 font-weight-medium mb-4 d-flex align-center">
                <v-icon class="mr-2" color="primary">mdi-file-document</v-icon>
                Hồ sơ
              </h3>
              
              <v-card variant="outlined" class="pa-4">
                <div class="d-flex align-center">
                  <v-icon class="mr-3" color="error">mdi-file-pdf-box</v-icon>
                  <div class="flex-grow-1">
                    <div class="font-weight-medium">CV - {{ candidate.full_name }}</div>
                    <div class="text-caption text-medium-emphasis">PDF Document</div>
                  </div>
                  <v-btn
                    color="primary"
                    variant="outlined"
                    size="small"
                    :href="candidate.cv_original_url"
                    target="_blank"
                    prepend-icon="mdi-download"
                  >
                    Tải xuống
                  </v-btn>
                </div>
              </v-card>
            </div>
          </div>

          <!-- Right Column -->
          <v-divider vertical />
          <div style="width: 320px;" class="pa-6">
            <!-- Activity Timeline -->
            <div class="mb-6">
              <h3 class="text-h6 font-weight-medium mb-4 d-flex align-center">
                <v-icon class="mr-2" color="primary">mdi-timeline-clock</v-icon>
                Hoạt động
              </h3>
              
              <div class="activity-timeline">
                <div class="d-flex align-start mb-4">
                  <v-icon class="mr-3 mt-1" color="success" size="20">mdi-account-plus</v-icon>
                  <div>
                    <div class="text-body-2 font-weight-medium">Được tạo</div>
                    <div class="text-caption text-medium-emphasis">
                      {{ formatDate(candidate.creation) }}
                    </div>
                  </div>
                </div>
                
                <div v-if="candidate.last_interaction" class="d-flex align-start mb-4">
                  <v-icon class="mr-3 mt-1" color="info" size="20">mdi-message</v-icon>
                  <div>
                    <div class="text-body-2 font-weight-medium">Tương tác cuối</div>
                    <div class="text-caption text-medium-emphasis">
                      {{ formatRelativeTime(candidate.last_interaction) }}
                    </div>
                  </div>
                </div>
                
                <div class="d-flex align-start">
                  <v-icon class="mr-3 mt-1" color="warning" size="20">mdi-update</v-icon>
                  <div>
                    <div class="text-body-2 font-weight-medium">Cập nhật cuối</div>
                    <div class="text-caption text-medium-emphasis">
                      {{ formatRelativeTime(candidate.modified) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Email Settings -->
            <div class="mb-6">
              <h3 class="text-h6 font-weight-medium mb-4 d-flex align-center">
                <v-icon class="mr-2" color="primary">mdi-email-settings</v-icon>
                Cài đặt Email
              </h3>
              
              <v-card variant="outlined" class="pa-4">
                <div class="d-flex align-center justify-space-between">
                  <div>
                    <div class="font-weight-medium">Email Marketing</div>
                    <div class="text-caption text-medium-emphasis">
                      {{ candidate.email_opt_out ? 'Đã từ chối' : 'Đã đồng ý' }}
                    </div>
                  </div>
                  <v-chip
                    :color="candidate.email_opt_out ? 'error' : 'success'"
                    size="small"
                    variant="flat"
                  >
                    {{ candidate.email_opt_out ? 'Opt-out' : 'Opt-in' }}
                  </v-chip>
                </div>
              </v-card>
            </div>

            <!-- Profile Data -->
            <div v-if="candidate.profile_data && Object.keys(candidate.profile_data).length > 0">
              <h3 class="text-h6 font-weight-medium mb-4 d-flex align-center">
                <v-icon class="mr-2" color="primary">mdi-account-cog</v-icon>
                Dữ liệu hồ sơ
              </h3>
              
              <v-expansion-panels variant="accordion">
                <v-expansion-panel>
                  <v-expansion-panel-title>
                    Xem dữ liệu JSON
                  </v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <pre class="text-caption bg-grey-lighten-5 pa-2 rounded">{{ JSON.stringify(candidate.profile_data, null, 2) }}</pre>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </div>
          </div>
        </div>
      </v-card-text>

      <!-- Error State -->
      <v-card-text v-else-if="error" class="text-center pa-8">
        <v-icon size="64" color="error" class="mb-4">mdi-alert-circle</v-icon>
        <h3 class="text-h6 mb-2">Có lỗi xảy ra</h3>
        <p class="text-body-2 text-medium-emphasis mb-4">{{ error }}</p>
        <v-btn color="primary" @click="$emit('update:modelValue', false)">
          Đóng
        </v-btn>
      </v-card-text>

      <!-- Actions -->
      <v-card-actions class="px-6 py-4 bg-grey-lighten-5">
        <v-spacer />
        <v-btn
          variant="outlined"
          @click="$emit('update:modelValue', false)"
        >
          Đóng
        </v-btn>
        <v-btn
          color="primary"
          variant="flat"
          prepend-icon="mdi-pencil"
          @click="$emit('edit-candidate', candidate)"
        >
          Chỉnh sửa
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed } from 'vue'
import {
  calculateEngagementScore,
  formatCandidateStatus,
  formatDate,
  getAvatarColor,
  getAvatarText,
  getEngagementColor,
  processSkills
} from '@/utils/candidateHelpers'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  candidate: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  }
})

// Emits
const emit = defineEmits([
  'update:modelValue',
  'edit-candidate',
  'delete-candidate',
  'duplicate-candidate'
])

// Methods
const downloadCV = () => {
  if (props.candidate?.cv_original_url) {
    window.open(props.candidate.cv_original_url, '_blank')
  }
}
</script>

<style scoped>
.candidate-view-modal {
  max-height: 90vh;
}

.contact-info {
  background: rgb(var(--v-theme-surface-variant));
  border-radius: 12px;
  padding: 16px;
}

.activity-timeline {
  position: relative;
}

.activity-timeline::before {
  content: '';
  position: absolute;
  left: 12px;
  top: 24px;
  bottom: 0;
  width: 2px;
  background: rgb(var(--v-theme-outline-variant));
}

/* Custom scrollbar */
:deep(.v-card-text) {
  scrollbar-width: thin;
}

:deep(.v-card-text::-webkit-scrollbar) {
  width: 6px;
}

:deep(.v-card-text::-webkit-scrollbar-track) {
  background: rgb(var(--v-theme-surface-variant));
}

:deep(.v-card-text::-webkit-scrollbar-thumb) {
  background: rgb(var(--v-theme-outline-variant));
  border-radius: 3px;
}
</style> 