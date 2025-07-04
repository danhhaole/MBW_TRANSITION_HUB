<template>
  <v-card class="elevation-2">
    <!-- Header với search và filters -->
    <v-card-title class="pa-4">
      <v-row align="center">
        <v-col cols="12" md="3">
          <v-text-field
            :model-value="searchText"
            label="Tìm kiếm chiến dịch"
            prepend-inner-icon="mdi-magnify"
            variant="outlined"
            density="compact"
            hide-details
            clearable
            @update:model-value="handleSearch"
          />
        </v-col>
        
        <v-col cols="12" md="2">
          <v-select
            :model-value="statusFilter"
            :items="statusFilterOptions"
            label="Trạng thái"
            prepend-inner-icon="mdi-flag"
            variant="outlined"
            density="compact"
            hide-details
            @update:model-value="handleFilterChange"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-select
            :model-value="typeFilter"
            :items="typeFilterOptions"
            label="Loại"
            prepend-inner-icon="mdi-tag"
            variant="outlined"
            density="compact"
            hide-details
            @update:model-value="handleTypeFilterChange"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-select
            :model-value="activeFilter"
            :items="activeFilterOptions"
            label="Hoạt động"
            prepend-inner-icon="mdi-power"
            variant="outlined"
            density="compact"
            hide-details
            @update:model-value="handleActiveFilterChange"
          />
        </v-col>

        <v-spacer />

        <v-col cols="auto">
          <!-- <v-btn
            color="primary"
            variant="flat"
            prepend-icon="mdi-plus"
            @click="handleCreate"
            :disabled="loading"
          >
            Tạo mới
          </v-btn> -->
        </v-col>

        <v-col cols="auto">
          <v-btn
            variant="outlined"
            icon="mdi-refresh"
            @click="handleRefresh"
            :loading="loading"
          />
        </v-col>
      </v-row>
    </v-card-title>

    <v-divider />

    <!-- Data Table -->
    <v-data-table
      :headers="headers"
      :items="props.campaigns"
      :loading="loading"
      item-value="name"
      class="elevation-0"
      loading-text="Đang tải dữ liệu..."
      no-data-text="Không có dữ liệu"
      hide-default-footer
    >
      <!-- Custom slots -->
      
      <!-- Tên yêu cầu với description -->
      <template #item.campaign_name="{ value, item }">
        <div class="d-flex align-center">
          <v-avatar size="32" color="primary" variant="tonal" class="mr-3">
            <v-icon size="18" color="primary">mdi-briefcase</v-icon>
          </v-avatar>
          <div class="d-flex flex-column">
            <span class="text-body-1 font-weight-medium">{{ value }}</span>
            <span class="text-caption text-grey-darken-1">{{ item.description || 'Tuyển dụng cho vị trí quan trọng trong công ty.' }}</span>
          </div>
        </div>
      </template>

      <!-- Trạng thái -->
      <template #item.status="{ value, item }">
        <v-chip
          :color="getStatusColor(item.displayStatus || value)"
          variant="tonal"
          size="small"
        >
          {{ getStatusText(item.displayStatus || value) }}
        </v-chip>
      </template>

      <!-- Tiến độ -->
      <template #item.progress="{ item }">
        <div class="d-flex align-center">
          <v-progress-linear
            :model-value="getCampaignProgress(item)"
            :color="getProgressColor(item)"
            size="28"
            width="3"
          />
          <span class="ml-2 text-body-2 font-weight-medium">{{ getCampaignProgress(item) }}%</span>
        </div>
      </template>

      <!-- Ngày bắt đầu -->
      <template #item.start_date="{ value }">
        <div v-if="value" class="d-flex align-center">
          <v-icon size="16" color="grey-lighten-1" class="mr-1">mdi-calendar</v-icon>
          <span class="text-body-2">{{ value }}</span>
        </div>
        <span v-else class="text-grey-lighten-1">-</span>
      </template>

      <!-- Người phụ trách -->
      <template #item.owner_id="{ value, item }">
        <div v-if="value" class="d-flex align-center">
          <v-avatar size="28" :color="getOwnerColor(value)" class="mr-2">
            <span class="text-caption font-weight-medium text-white">{{ getInitials(value) }}</span>
          </v-avatar>
          <span class="text-body-2">{{ value }}</span>
        </div>
        <span v-else class="text-grey-lighten-1">-</span>
      </template>

      <!-- Hành động -->
      <template #item.actions="{ item }">
        <div class="d-flex align-center ">
          <v-btn
            variant="text"
            :border=false
            color="blue-darken-3"
            class="text-blue-600 mr-2"
            @click="handleView(item)"
          >
            Xem timeline
          </v-btn>
          
          <v-menu>
            <template #activator="{ props }">
              <v-btn
                icon="mdi-dots-vertical"
                variant="text"
                size="small"
                v-bind="props"
              />
            </template>
            <v-list density="compact">
              <v-list-item @click="handleEdit(item)">
                <template #prepend>
                  <v-icon size="16">mdi-pencil</v-icon>
                </template>
                <v-list-item-title>Chỉnh sửa</v-list-item-title>
              </v-list-item>
              <v-list-item @click="handleView(item)">
                <template #prepend>
                  <v-icon size="16">mdi-eye</v-icon>
                </template>
                <v-list-item-title>Xem chi tiết</v-list-item-title>
              </v-list-item>
              <v-divider />
              <v-list-item @click="handleDelete(item)" class="text-error">
                <template #prepend>
                  <v-icon size="16" color="error">mdi-delete</v-icon>
                </template>
                <v-list-item-title>Xóa</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </div>
      </template>

      <!-- Loading slot -->
      <template #loading>
        <v-skeleton-loader type="table-row@5" />
      </template>


    </v-data-table>

    <!-- Custom Pagination -->
    <div class="d-flex justify-space-between align-center pa-4 border-t" v-if="pagination.total > 0">
      <div class="text-body-2 text-medium-emphasis">
        Hiển thị {{ pagination.showing_from }} đến {{ pagination.showing_to }} trong tổng số {{ pagination.total }} chiến dịch
      </div>
      
      <div class="d-flex align-center" v-if="pagination.pages > 1">
        <span class="text-body-2 mr-4">Hàng mỗi trang:</span>
        <v-select
          :model-value="pagination.limit"
          @update:model-value="handleItemsPerPageChange"
          :items="[
            { title: '10', value: 10 },
            { title: '25', value: 25 },
            { title: '50', value: 50 },
            { title: '100', value: 100 }
          ]"
          variant="outlined"
          density="compact"
          hide-details
          style="width: 90px;"
          class="mr-6"
        />
        
        <v-pagination
          :model-value="pagination.page"
          @update:model-value="handlePageChange"
          :length="pagination.pages"
          :total-visible="5"
          size="small"
          variant="outlined"
          show-first-last-page
        />
      </div>
    </div>

    <!-- Confirm Delete Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h6">
          <v-icon color="error" class="mr-2">mdi-alert-circle</v-icon>
          Xác nhận xóa
        </v-card-title>
        
        <v-card-text>
          Bạn có chắc chắn muốn xóa chiến dịch 
          <strong>"{{ itemToDelete?.campaign_name }}"</strong>?
          <br><br>
          <v-alert type="warning" variant="tonal" text="Hành động này không thể hoàn tác!" />
        </v-card-text>
        
        <v-card-actions>
          <v-spacer />
          <v-btn variant="outlined" @click="deleteDialog = false">
            Hủy bỏ
          </v-btn>
          <v-btn 
            color="error" 
            variant="flat"
            :loading="deleting"
            @click="confirmDelete"
          >
            Xóa
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// Props
const props = defineProps({
  campaigns: {
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
      limit: 10,
      total: 0,
      pages: 1,
      has_next: false,
      has_prev: false,
      showing_from: 0,
      showing_to: 0
    })
  },
  searchText: {
    type: String,
    default: ''
  },
  statusFilter: {
    type: String,
    default: 'all'
  },
  typeFilter: {
    type: String,
    default: 'all'
  },
  activeFilter: {
    type: String,
    default: 'all'
  },
  refreshTrigger: {
    type: Number,
    default: 0
  }
})

console.log('CampaignTable props.campaigns:', props.campaigns.length, props.campaigns)

// Emits
const emit = defineEmits([
  'create', 'edit', 'view', 'delete', 'refresh', 
  'update:search-text', 'update:status-filter', 'update:type-filter', 'update:active-filter',
  'page-change', 'items-per-page-change'
])

// Refs
const deleteDialog = ref(false)
const itemToDelete = ref(null)
const deleting = ref(false)

// Watch props changes
watch(() => props.campaigns, (newCampaigns) => {
  console.log('CampaignTable - campaigns props changed:', newCampaigns.length)
}, { deep: true })

// Table headers
const headers = [
  {
    title: 'Tên yêu cầu',
    key: 'campaign_name',
    align: 'start',
    sortable: true,
    width: '30%'
  },
  {
    title: 'Trạng thái',
    key: 'status',
    align: 'start',
    sortable: true,
    width: '15%'
  },
  {
    title: 'Tiến độ',
    key: 'progress',
    align: 'center',
    sortable: false,
    width: '15%'
  },
  {
    title: 'Ngày bắt đầu',
    key: 'start_date',
    align: 'start',
    sortable: true,
    width: '15%'
  },
  {
    title: 'Người phụ trách',
    key: 'owner_id',
    align: 'start',
    sortable: true,
    width: '15%'
  },
  {
    title: 'Hành động',
    key: 'actions',
    align: 'center',
    sortable: false,
    width: '10%'
  }
]

// Filter options
const statusFilterOptions = [
  { title: 'Tất cả', value: 'all' },
  { title: 'Nháp', value: 'DRAFT' },
  { title: 'Hoạt động', value: 'ACTIVE' },
  { title: 'Tạm dừng', value: 'PAUSED' },
  { title: 'Lưu trữ', value: 'ARCHIVED' }
]

const typeFilterOptions = [
  { title: 'Tất cả', value: 'all' },
  { title: 'Nuôi dưỡng', value: 'NURTURING' },
  { title: 'Thu hút', value: 'ATTRACTION' }
]

const activeFilterOptions = [
  { title: 'Tất cả', value: 'all' },
  { title: 'Kích hoạt', value: 'active' },
  { title: 'Vô hiệu hóa', value: 'inactive' }
]

// Methods
const getStatusColor = (status) => {
  const colors = {
    'DRAFT': 'grey',
    'ACTIVE': 'success',
    'PAUSED': 'warning',
    'ARCHIVED': 'info'
  }
  return colors[status] || 'grey'
}

const getStatusText = (status) => {
  const texts = {
    'DRAFT': 'Nháp',
    'ACTIVE': 'Hoạt động', 
    'PAUSED': 'Tạm dừng',
    'ARCHIVED': 'Lưu trữ'
  }
  return texts[status] || status
}



const getInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
}

const getOwnerColor = (name) => {
  if (!name) return 'grey'
  const colors = ['primary', 'secondary', 'accent', 'success', 'warning', 'info', 'purple', 'pink', 'indigo', 'teal']
  const index = name.length % colors.length
  return colors[index]
}

const getCampaignProgress = (campaign) => {
  if (!campaign.start_date || !campaign.end_date) return 0
  
  const now = new Date()
  const start = new Date(campaign.start_date)
  const end = new Date(campaign.end_date)
  
  if (now < start) return 0
  if (now > end) return 100
  
  const total = end - start
  const current = now - start
  return Math.round((current / total) * 100)
}

const getProgressColor = (campaign) => {
  const progress = getCampaignProgress(campaign)
  if (progress === 0) return 'grey'
  if (progress < 30) return 'error'
  if (progress < 70) return 'warning'
  return 'success'
}

// Event handlers
const handleSearch = (value) => {
  emit('update:searchText', value)
}

const handleFilterChange = (value) => {
  emit('update:statusFilter', value)
}

const handleTypeFilterChange = (value) => {
  emit('update:typeFilter', value)
}

const handleActiveFilterChange = (value) => {
  emit('update:activeFilter', value)
}

const handleRefresh = () => {
  emit('refresh')
}

const handleCreate = () => {
  emit('create')
}

const handleEdit = (item) => {
  emit('edit', item)
}

const handleView = (item) => {
  emit('view', item)
}

const handleDelete = (item) => {
  itemToDelete.value = item
  deleteDialog.value = true
}

const confirmDelete = async () => {
  if (!itemToDelete.value) return
  
  deleting.value = true
  try {
    emit('delete', itemToDelete.value)
  } finally {
    deleting.value = false
    deleteDialog.value = false
    itemToDelete.value = null
  }
}

// Pagination handlers
const handlePageChange = (page) => {
  emit('page-change', page)
}

const handleItemsPerPageChange = (limit) => {
  emit('items-per-page-change', limit)
}
</script>

<style scoped>
.v-data-table {
  background: transparent;
}

.v-data-table__wrapper {
  overflow-x: auto;
}

/* Custom scrollbar for table */
.v-data-table__wrapper::-webkit-scrollbar {
  height: 8px;
}

.v-data-table__wrapper::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.v-data-table__wrapper::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.v-data-table__wrapper::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Pagination styling */
:deep(.v-pagination) {
  justify-content: center;
}

:deep(.v-pagination .v-btn) {
  margin: 0 2px;
}

/* Table header styling */
:deep(.v-data-table-header) {
  background-color: rgb(var(--v-theme-surface-variant));
  font-weight: 600;
}

/* Progress bar styling */
:deep(.v-progress-linear) {
  border-radius: 4px;
}

/* Chip styling */
.v-chip {
  font-weight: 500;
}

/* Border styling */
.border-t {
  border-top: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}
</style> 