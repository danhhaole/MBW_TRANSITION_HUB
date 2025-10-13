<template>
  <v-card variant="outlined" class="rounded-lg">
    <v-data-table
      :headers="headers"
      :items="segments"
      :loading="loading"
      class="elevation-0"
      item-key="name"
      :items-per-page="15"
      :search="search"
      :loading-text="__('Loading data...')"
      :no-data-text="__('No data available')"
    >
      <!-- Title column -->
      <template v-slot:item.title="{ item }">
        <div class="d-flex align-center">
          <v-avatar 
            size="32" 
            :color="getTypeColor(item.type)"
            variant="tonal"
            class="mr-3"
          >
            <v-icon size="16">
              {{ item.type === 'DYNAMIC' ? 'mdi-robot' : 'mdi-hand' }}
            </v-icon>
          </v-avatar>
          <div>
            <div class="font-weight-medium">{{ item.title }}</div>
            <div class="text-caption text-medium-emphasis" v-if="item.description">
              {{ truncateText(item.description, 50) }}
            </div>
          </div>
        </div>
      </template>

      <!-- Type column -->
      <template v-slot:item.type="{ item }">
        <v-chip 
          size="small" 
          :color="getTypeColor(item.type)"
          variant="tonal"
        >
          {{ getTypeLabel(item.type) }}
        </v-chip>
      </template>

      <!-- Candidate Count column -->
      <template v-slot:item.candidate_count="{ item }">
        <div class="d-flex align-center">
          <v-progress-linear
            :model-value="getEngagementRate(item)"
            height="6"
            rounded
            :color="getEngagementColor(getEngagementRate(item))"
            class="flex-grow-1 mr-2"
            style="max-width: 80px;"
          />
          <div class="text-center" style="min-width: 60px;">
            <div class="font-weight-medium">{{ item.candidate_count || 0 }}</div>
            <div class="text-caption text-success">{{ getEngagementRate(item) }}%</div>
          </div>
        </div>
      </template>

      <!-- Modified date column -->
      <template v-slot:item.modified="{ item }">
        <div class="d-flex align-center">
          <v-icon size="16" color="grey" class="mr-1">mdi-calendar</v-icon>
          <span class="text-body-2">{{ formatDate(item.modified) }}</span>
        </div>
      </template>

      <!-- Owner column -->
      <template v-slot:item.owner_id="{ item }">
        <div v-if="item.owner_id" class="d-flex align-center">
          <v-avatar size="28" :color="getAvatarColor(item.owner_id)" class="mr-2">
            <span class="text-caption white--text">
              {{ getAvatarText(item.owner_id) }}
            </span>
          </v-avatar>
          <span class="text-body-2">{{ item.owner_id }}</span>
        </div>
        <span v-else class="text-medium-emphasis">—</span>
      </template>

      <!-- Actions column -->
      <template v-slot:item.actions="{ item }">
        <div class="d-flex align-center">
          <v-btn
            variant="text"
            icon="mdi-timeline"
            size="small"
            color="primary"
            @click="$emit('view-details', item)"
            class="mr-1"
          >
            <v-icon size="18">mdi-timeline</v-icon>
            <v-tooltip activator="parent" location="top">Chi tiết</v-tooltip>
          </v-btn>
          
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
              <v-list-item @click="$emit('view-details', item)">
                <template v-slot:prepend>
                  <v-icon size="18">mdi-eye</v-icon>
                </template>
                <v-list-item-title>Xem chi tiết</v-list-item-title>
              </v-list-item>
              <v-list-item @click="$emit('edit', item)">
                <template v-slot:prepend>
                  <v-icon size="18">mdi-pencil</v-icon>
                </template>
                <v-list-item-title>Chỉnh sửa</v-list-item-title>
              </v-list-item>
              <v-divider />
              <v-list-item @click="$emit('delete', item)" class="text-error">
                <template v-slot:prepend>
                  <v-icon size="18" color="error">mdi-delete</v-icon>
                </template>
                <v-list-item-title>Xóa</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </div>
      </template>

      <!-- Loading template -->
      <template v-slot:loading>
        <v-skeleton-loader type="table-row-divider@6" />
      </template>

      <!-- No data template -->
      <template v-slot:no-data>
        <div class="text-center py-8">
          <v-icon size="48" color="grey-lighten-2">mdi-account-group-outline</v-icon>
          <div class="text-h6 mt-2 mb-1">{{ __('No segments available') }}</div>
          <div class="text-body-2 text-medium-emphasis">
            {{ __('Create your first segment to get started') }}
          </div>
        </div>
      </template>

      <!-- Bottom slot for pagination -->
      <template v-slot:bottom="{ page, pageCount, itemsPerPage, itemsLength, updateOptions }">
        <div class="d-flex justify-center pa-4">
          <v-pagination
            :model-value="page"
            @update:model-value="(newPage) => updateOptions({ page: newPage })"
            :length="pageCount"
            :total-visible="7"
            size="small"
            variant="outlined"
          />
        </div>
      </template>
    </v-data-table>
  </v-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useTalentSegmentStore } from '@/stores/talentSegment'

// Translation helper function


// Props
const props = defineProps({
  segments: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['view-details', 'edit', 'delete'])

// Local state
const search = ref('')

// Table headers
const headers = [
  {
    title: 'Segment Name',
    key: 'title',
    sortable: true,
    width: '30%'
  },
  {
    title: 'Type',
    key: 'type',
    sortable: true,
    width: '12%'
  },
  {
    title: 'Progress',
    key: 'candidate_count',
    sortable: true,
    width: '15%'
  },
  {
    title: 'Updated Date',
    key: 'modified',
    sortable: true,
    width: '15%'
  },
  {
    title: 'Owner',
    key: 'owner_id',
    sortable: true,
    width: '18%'
  },
  {
    title: 'Actions',
    key: 'actions',
    sortable: false,
    width: '10%',
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
  return  0
}

const getEngagementColor = (rate) => {
  if (rate >= 70) return 'success'
  if (rate >= 40) return 'warning'
  return 'error'
}

const getAvatarColor = (ownerId) => {
  const colors = ['primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success']
  const hash = ownerId?.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0)
    return a & a
  }, 0) || 0
  return colors[Math.abs(hash) % colors.length]
}

const getAvatarText = (ownerId) => {
  if (!ownerId) return ''
  return ownerId.split(' ').map(name => name[0]).join('').toUpperCase().substring(0, 2)
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}
</script>

<style scoped>
/* Data table customization */
:deep(.v-data-table) {
  border-radius: 12px;
}

:deep(.v-data-table__wrapper) {
  border-radius: 12px;
}

:deep(.v-data-table-header) {
  background-color: rgb(var(--v-theme-surface-variant));
}

:deep(.v-data-table-header__content) {
  font-weight: 600;
  color: rgb(var(--v-theme-on-surface-variant));
}

/* Row hover effect */
:deep(.v-data-table__tr:hover) {
  background-color: rgba(var(--v-theme-primary), 0.04);
}

/* Avatar text color fix */
.v-avatar .white--text {
  color: white !important;
}

/* Progress bar in table */
:deep(.v-progress-linear) {
  border-radius: 3px;
}

/* Tooltip styling */
:deep(.v-tooltip > .v-overlay__content) {
  background: rgba(0, 0, 0, 0.8) !important;
  color: white !important;
  border-radius: 6px;
  font-size: 12px;
  padding: 6px 12px;
}

/* Menu styling */
:deep(.v-menu > .v-overlay__content) {
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
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

/* No data styling */
.no-data-container {
  padding: 3rem 0;
}
</style>