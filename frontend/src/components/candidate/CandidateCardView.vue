<template>
  <div>
    <!-- Candidate Grid -->
    <v-row>
      <!-- Loading State -->
      <template v-if="loading">
        <v-col
          v-for="n in 6"
          :key="n"
          cols="12"
          md="4"
          sm="6"
        >
          <v-card
            class="candidate-card"
            min-height="280"
            variant="outlined"
          >
            <v-card-text>
              <v-skeleton-loader
                type="avatar, text, chip, text, divider, actions"
              />
            </v-card-text>
          </v-card>
        </v-col>
      </template>

      <!-- Candidate Cards -->
      <v-col
        v-for="candidate in candidates"
        :key="candidate.name"
        cols="12"
        md="4"
        sm="6"
      >
        <v-card
          class="candidate-card"
          min-height="280"
          variant="default"
          hover
          @click="$emit('view-candidate', candidate)"
        >
          <v-card-text class="pa-3 d-flex flex-column" style="height: 100%;">
            <!-- Header with Avatar and Basic Info -->
            <div class="d-flex align-center mb-3">
              <v-avatar
                :color="getAvatarColor(candidate.full_name)"
                size="44"
                class="mr-3"
              >
                <v-img
                  v-if="candidate.avatar"
                  :src="candidate.avatar"
                  :alt="candidate.full_name"
                />
                <span
                  v-else
                  class="text-white font-weight-medium"
                  style="font-size: 16px;"
                >
                  {{ getAvatarText(candidate.full_name) }}
                </span>
              </v-avatar>
              
              <div class="flex-grow-1">
                <h3 class="text-subtitle-1 font-weight-medium text-truncate">
                  {{ candidate.full_name }}
                </h3>
                <p class="text-body-2 text-medium-emphasis mb-0 text-truncate">
                  {{ candidate.headline || 'Chưa có thông tin' }}
                </p>
              </div>
            </div>

            <!-- Contact Information -->
            <div class="mb-3">
              <div class="d-flex align-center text-body-2 text-medium-emphasis mb-1">
                <v-icon size="14" class="mr-1">mdi-email</v-icon>
                <span class="text-truncate">{{ candidate.email }}</span>
              </div>
              <div class="d-flex align-center text-body-2 text-medium-emphasis">
                <v-icon size="14" class="mr-1">mdi-map-marker</v-icon>
                <span>{{ getLocation(candidate) }}</span>
              </div>
            </div>

            <!-- Skills -->
            <div class="mb-3">
              <div class="text-caption text-medium-emphasis mb-1">Kỹ năng</div>
              <div class="d-flex flex-wrap" style="gap: 4px;">
                <v-chip
                  v-for="skill in getTopSkills(candidate.skills, 2)"
                  :key="skill"
                  size="x-small"
                  variant="outlined"
                  color="primary"
                >
                  {{ skill }}
                </v-chip>
                <v-chip
                  v-if="candidate.skills && candidate.skills.length > 2"
                  size="x-small"
                  variant="outlined"
                  color="grey"
                >
                  +{{ candidate.skills.length - 2 }}
                </v-chip>
              </div>
            </div>

            <!-- Talent Pools -->
            <div class="mb-3">
              <div class="text-caption text-medium-emphasis mb-1">Talent Pools</div>
              <div class="d-flex flex-wrap" style="gap: 4px;">
                <v-chip
                  v-for="pool in getTalentPools(candidate).slice(0, 1)"
                  :key="pool"
                  size="x-small"
                  variant="tonal"
                  color="info"
                >
                  {{ pool }}
                </v-chip>
              </div>
            </div>

            <!-- Engagement Score -->
            <div class="mb-3">
              <div class="text-caption text-medium-emphasis mb-1">Điểm tương tác</div>
              <div class="d-flex align-center">
                <v-progress-linear
                  :model-value="calculateEngagementScore(candidate)"
                  :color="getEngagementColor(calculateEngagementScore(candidate))"
                  height="6"
                  rounded
                  class="flex-grow-1 mr-2"
                />
                <span class="text-caption font-weight-medium">
                  {{ calculateEngagementScore(candidate) }}%
                </span>
              </div>
            </div>

            <!-- Footer with Status and Actions -->
            <div class="d-flex justify-space-between align-center mt-auto">
              <v-chip
                :color="getStatusChipColor(candidate.status)"
                size="x-small"
                variant="flat"
              >
                {{ formatCandidateStatus(candidate.status).text }}
              </v-chip>
              
              <div class="d-flex align-center">
                <v-btn
                  size="x-small"
                  variant="text"
                  color="primary"
                  @click.stop="$emit('view-candidate', candidate)"
                >
                  Xem chi tiết
                </v-btn>
                <v-menu>
                  <template v-slot:activator="{ props }">
                    <v-btn
                      v-bind="props"
                      size="x-small"
                      variant="text"
                      icon="mdi-dots-vertical"
                      @click.stop
                    />
                  </template>
                  <v-list density="compact">
                    <v-list-item @click.stop="$emit('edit-candidate', candidate)">
                      <template v-slot:prepend>
                        <v-icon size="18">mdi-pencil</v-icon>
                      </template>
                      <v-list-item-title>Chỉnh sửa</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click.stop="$emit('duplicate-candidate', candidate)">
                      <template v-slot:prepend>
                        <v-icon size="18">mdi-content-copy</v-icon>
                      </template>
                      <v-list-item-title>Sao chép</v-list-item-title>
                    </v-list-item>
                    <v-divider />
                    <v-list-item 
                      @click.stop="$emit('delete-candidate', candidate)"
                      class="text-error"
                    >
                      <template v-slot:prepend>
                        <v-icon size="18" color="error">mdi-delete</v-icon>
                      </template>
                      <v-list-item-title>Xóa</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Empty State -->
      <v-col
        v-if="!loading && candidates.length === 0"
        cols="12"
        class="d-flex flex-column align-center justify-center pa-8"
        style="min-height: 300px;"
      >
        <v-icon size="64" color="grey-lighten-1" class="mb-4">
          mdi-account-search
        </v-icon>
        <h3 class="text-h6 text-medium-emphasis mb-2">
          {{ hasFilters ? 'Không tìm thấy ứng viên' : 'Chưa có ứng viên nào' }}
        </h3>
        <p class="text-body-2 text-medium-emphasis text-center mb-4">
          {{ hasFilters 
            ? 'Thử thay đổi bộ lọc để tìm thấy ứng viên phù hợp.' 
            : 'Bắt đầu bằng cách thêm ứng viên đầu tiên.' 
          }}
        </p>
        <v-btn
          v-if="!hasFilters"
          color="primary"
          variant="flat"
          prepend-icon="mdi-plus"
          @click="$emit('create-candidate')"
        >
          Thêm ứng viên
        </v-btn>
        <v-btn
          v-else
          color="primary"
          variant="outlined"
          @click="$emit('clear-filters')"
        >
          Xóa bộ lọc
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  calculateEngagementScore,
  formatCandidateStatus,
  getAvatarColor,
  getAvatarText,
  getStatusChipColor,
  getEngagementColor
} from '@/utils/candidateHelpers'

// Props
const props = defineProps({
  candidates: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  hasFilters: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits([
  'view-candidate',
  'edit-candidate',
  'delete-candidate',
  'duplicate-candidate',
  'create-candidate',
  'clear-filters'
])

// Helper functions
const getTopSkills = (skills, limit) => {
  if (!skills || !Array.isArray(skills)) return []
  return skills.slice(0, limit || 3)
}

const getTalentPools = (candidate) => {
  // Mock talent pools based on skills or source
  const pools = []
  
  if (candidate.skills) {
    const skills = Array.isArray(candidate.skills) ? candidate.skills : []
    if (skills.some(skill => ['React', 'Vue.js', 'Angular', 'JavaScript'].includes(skill))) {
      pools.push('Frontend Experts')
    }
    if (skills.some(skill => ['Node.js', 'Python', 'Java', 'AWS'].includes(skill))) {
      pools.push('Software Developers')
    }
    if (skills.some(skill => ['React Native', 'Flutter', 'iOS', 'Android'].includes(skill))) {
      pools.push('Mobile Developers')
    }
    if (skills.some(skill => ['AWS', 'DevOps', 'Docker', 'Kubernetes'].includes(skill))) {
      pools.push('Cloud Engineers')
    }
  }
  
  // Default pool if no specific match
  if (pools.length === 0) {
    pools.push('Software Developers')
  }
  
  return pools
}

const getLocation = (candidate) => {
  // Mock location data - in real app this would come from candidate profile
  const locations = ['Ho Chi Minh City', 'Ha Noi', 'Da Nang', 'Can Tho']
  return candidate.location || locations[Math.floor(Math.random() * locations.length)]
}
</script>

<style scoped>
.candidate-card {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  cursor: pointer;
}

.candidate-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}

.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style> 