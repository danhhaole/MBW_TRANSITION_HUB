<template>
  <div class="candidate-table-container">
    <v-data-table
      :headers="headers"
      :items="candidates"
      :loading="loading"
      hide-default-footer
      class="elevation-1"
      item-key="name"
    >
      <!-- Custom header -->
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title class="text-h6">
            Danh sách ứng viên
          </v-toolbar-title>
          <v-spacer />
          <slot name="toolbar-actions" />
        </v-toolbar>
      </template>

      <!-- Candidate column -->
      <template v-slot:item.candidate="{ item }">
        <div class="d-flex align-center py-2">
          <v-avatar
            :color="getAvatarColor(item.full_name)"
            size="40"
            class="mr-3"
          >
            <v-img
              v-if="item.avatar"
              :src="item.avatar"
              :alt="item.full_name"
            />
            <span
              v-else
              class="text-white font-weight-medium"
            >
              {{ getAvatarText(item.full_name) }}
            </span>
          </v-avatar>
          
          <div>
            <div class="font-weight-medium">{{ item.full_name }}</div>
            <div class="text-caption text-medium-emphasis">{{ item.email }}</div>
            <div v-if="item.phone" class="text-caption text-medium-emphasis">
              {{ item.phone }}
            </div>
          </div>
        </div>
      </template>

      <!-- Headline column -->
      <template v-slot:item.headline="{ item }">
        <div class="text-body-2">
          {{ item.headline || '-' }}
        </div>
      </template>

      <!-- Skills column -->
      <template v-slot:item.skills="{ item }">
        <div class="d-flex flex-wrap" style="gap: 4px; max-width: 200px;">
          <v-chip
            v-for="skill in getTopSkills(item.skills)"
            :key="skill"
            size="x-small"
            variant="outlined"
            color="primary"
          >
            {{ skill }}
          </v-chip>
          <v-chip
            v-if="item.skills && item.skills.length > 2"
            size="x-small"
            variant="outlined"
            color="grey"
          >
            +{{ item.skills.length - 2 }}
          </v-chip>
        </div>
      </template>

      <!-- Source column -->
      <template v-slot:item.source="{ item }">
        <v-chip
          v-if="item.source"
          size="small"
          variant="tonal"
          color="info"
        >
          {{ item.source }}
        </v-chip>
        <span v-else class="text-medium-emphasis">-</span>
      </template>

      <!-- Last Interaction column -->
      <template v-slot:item.last_interaction="{ item }">
        <div class="text-body-2">
          {{ formatRelativeTime(item.last_interaction) }}
        </div>
      </template>

      <!-- Engagement column -->
      <template v-slot:item.engagement="{ item }">
        <div class="d-flex align-center" style="min-width: 100px;">
          <v-progress-linear
            :model-value="calculateEngagementScore(item)"
            :color="getEngagementColor(calculateEngagementScore(item))"
            height="6"
            rounded
            class="flex-grow-1 mr-2"
          />
          <span class="text-caption font-weight-medium">
            {{ calculateEngagementScore(item) }}%
          </span>
        </div>
      </template>

      <!-- Status column -->
      <template v-slot:item.status="{ item }">
        <v-chip
          :color="getStatusChipColor(item.status)"
          size="small"
          variant="flat"
        >
          {{ formatCandidateStatus(item.status).text }}
        </v-chip>
      </template>

      <!-- Actions column -->
      <template v-slot:item.actions="{ item }">
        <div class="d-flex align-center">
          <v-btn
            size="small"
            variant="text"
            color="primary"
            @click="$emit('view-candidate', item)"
          >
            Xem
          </v-btn>
          <v-menu>
            <template v-slot:activator="{ props }">
              <v-btn
                v-bind="props"
                size="small"
                variant="text"
                icon="mdi-dots-vertical"
              />
            </template>
            <v-list density="compact">
              <v-list-item @click="$emit('edit-candidate', item)">
                <template v-slot:prepend>
                  <v-icon size="18">mdi-pencil</v-icon>
                </template>
                <v-list-item-title>Chỉnh sửa</v-list-item-title>
              </v-list-item>
              <v-list-item @click="$emit('duplicate-candidate', item)">
                <template v-slot:prepend>
                  <v-icon size="18">mdi-content-copy</v-icon>
                </template>
                <v-list-item-title>Sao chép</v-list-item-title>
              </v-list-item>
              <v-divider />
              <v-list-item 
                @click="$emit('delete-candidate', item)"
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
      </template>

      <!-- Loading state -->
      <template v-slot:loading>
        <v-skeleton-loader
          v-for="n in 5"
          :key="n"
          type="table-row"
          class="mx-auto"
        />
      </template>

      <!-- No data state -->
      <template v-slot:no-data>
        <div class="text-center pa-8">
          <v-icon size="64" color="grey-lighten-1" class="mb-4">
            mdi-account-search
          </v-icon>
          <h3 class="text-h6 text-medium-emphasis mb-2">
            {{ hasFilters ? 'Không tìm thấy ứng viên' : 'Chưa có ứng viên nào' }}
          </h3>
          <p class="text-body-2 text-medium-emphasis mb-4">
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
        </div>
      </template>
    </v-data-table>

    <!-- Custom Pagination -->
    <v-card
      v-if="pagination.total > 0"
      class="d-flex align-center justify-space-between pa-4 mt-4"
      variant="outlined"
    >
      <!-- Items per page selector -->
      <div class="d-flex align-center">
        <span class="text-body-2 mr-2">Số hàng mỗi trang:</span>
        <v-select
          :model-value="pagination.limit"
          :items="itemsPerPageOptions"
          @update:model-value="$emit('items-per-page-change', $event)"
          density="compact"
          variant="outlined"
          hide-details
          style="width: 80px;"
        />
      </div>

      <!-- Page info -->
      <div class="text-body-2 text-medium-emphasis">
        Hiển thị {{ pagination.showing_from }} đến {{ pagination.showing_to }} 
        trong tổng số {{ pagination.total }} ứng viên
      </div>

      <!-- Page navigation -->
      <div class="d-flex align-center">
        <v-btn
          :disabled="!pagination.has_prev"
          variant="text"
          size="small"
          @click="$emit('page-change', 1)"
        >
          <v-icon>mdi-page-first</v-icon>
        </v-btn>
        
        <v-btn
          :disabled="!pagination.has_prev"
          variant="text"
          size="small"
          @click="$emit('page-change', pagination.page - 1)"
        >
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>

        <!-- Page numbers -->
        <div class="d-flex align-center mx-2">
          <template v-for="page in visiblePages" :key="page">
            <v-btn
              v-if="page === '...'"
              variant="text"
              size="small"
              disabled
            >
              ...
            </v-btn>
            <v-btn
              v-else
              :variant="page === pagination.page ? 'flat' : 'text'"
              :color="page === pagination.page ? 'primary' : undefined"
              size="small"
              @click="$emit('page-change', page)"
            >
              {{ page }}
            </v-btn>
          </template>
        </div>

        <v-btn
          :disabled="!pagination.has_next"
          variant="text"
          size="small"
          @click="$emit('page-change', pagination.page + 1)"
        >
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
        
        <v-btn
          :disabled="!pagination.has_next"
          variant="text"
          size="small"
          @click="$emit('page-change', pagination.pages)"
        >
          <v-icon>mdi-page-last</v-icon>
        </v-btn>
      </div>
    </v-card>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  calculateEngagementScore,
  formatCandidateStatus,
  formatRelativeTime,
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
  pagination: {
    type: Object,
    default: () => ({
      page: 1,
      limit: 25,
      total: 0,
      pages: 0,
      has_next: false,
      has_prev: false,
      showing_from: 0,
      showing_to: 0
    })
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
  'clear-filters',
  'page-change',
  'items-per-page-change'
])

// Table headers
const headers = [
  {
    title: 'Ứng viên',
    key: 'candidate',
    align: 'start',
    sortable: false,
    width: '300px'
  },
  {
    title: 'Chức danh',
    key: 'headline',
    align: 'start',
    sortable: false,
    width: '200px'
  },
  {
    title: 'Kỹ năng',
    key: 'skills',
    align: 'start',
    sortable: false,
    width: '200px'
  },
  {
    title: 'Nguồn',
    key: 'source',
    align: 'start',
    sortable: false,
    width: '120px'
  },
  {
    title: 'Tương tác cuối',
    key: 'last_interaction',
    align: 'start',
    sortable: false,
    width: '140px'
  },
  {
    title: 'Điểm tương tác',
    key: 'engagement',
    align: 'start',
    sortable: false,
    width: '140px'
  },
  {
    title: 'Trạng thái',
    key: 'status',
    align: 'start',
    sortable: false,
    width: '120px'
  },
  {
    title: 'Thao tác',
    key: 'actions',
    align: 'end',
    sortable: false,
    width: '120px'
  }
]

// Items per page options
const itemsPerPageOptions = [
  { title: '10', value: 10 },
  { title: '25', value: 25 },
  { title: '50', value: 50 },
  { title: '100', value: 100 }
]

// Computed
const visiblePages = computed(() => {
  const current = props.pagination.page
  const total = props.pagination.pages
  const delta = 2 // Number of pages to show on each side of current page
  
  if (total <= 7) {
    // Show all pages if total is small
    return Array.from({ length: total }, (_, i) => i + 1)
  }
  
  const pages = []
  
  // Always show first page
  pages.push(1)
  
  if (current - delta > 2) {
    pages.push('...')
  }
  
  // Show pages around current
  const start = Math.max(2, current - delta)
  const end = Math.min(total - 1, current + delta)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  if (current + delta < total - 1) {
    pages.push('...')
  }
  
  // Always show last page
  if (total > 1) {
    pages.push(total)
  }
  
  return pages
})

// Helper functions
const getTopSkills = (skills) => {
  if (!skills || !Array.isArray(skills)) return []
  return skills.slice(0, 2) // Show only 2 skills in table
}
</script>

<style scoped>
.candidate-table-container {
  width: 100%;
}

/* Custom table styling */
:deep(.v-data-table) {
  border-radius: 12px;
}

:deep(.v-data-table__wrapper) {
  border-radius: 12px;
}

:deep(.v-data-table-header) {
  background-color: rgb(var(--v-theme-surface-variant));
}

:deep(.v-data-table-header th) {
  font-weight: 600;
  color: rgb(var(--v-theme-on-surface-variant));
}

/* Pagination styling */
:deep(.v-pagination) {
  justify-content: center;
}

:deep(.v-pagination__item) {
  margin: 0 2px;
}

/* Loading skeleton styling */
:deep(.v-skeleton-loader) {
  background: transparent;
}
</style> 