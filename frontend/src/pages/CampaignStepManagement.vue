<template>
  <div class="campaign-step-management-page">
    <!-- Header Section -->
    <div class="page-header bg-white pa-6 mb-6 elevation-1">
      <div class="d-flex align-center justify-space-between">
        <div>
          <h1 class="text-h4 font-weight-bold text-primary mb-2">
            <v-icon class="mr-3" size="36">mdi-chart-timeline-variant</v-icon>
            Quản lý bước chiến dịch
          </h1>
          <p class="text-body-1 text-medium-emphasis mb-0">
            Quản lý và cấu hình các bước trong chiến dịch marketing
          </p>
        </div>
        
        <div class="d-flex align-center">
          <v-btn
            color="primary"
            variant="flat"
            prepend-icon="mdi-plus"
            size="large"
            @click="openCreateModal"
          >
            Thêm bước chiến dịch
          </v-btn>
        </div>
      </div>
    </div>

    <!-- Filters and Controls -->
    <v-card class="mb-6" variant="default">
      <v-card-text class="pa-4">
        <v-row align="center">
          <!-- Search -->
          <v-col cols="12" md="4">
            <v-text-field
              v-model="filters.search"
              label="Tìm kiếm bước chiến dịch"
              variant="outlined"
              density="compact"
              prepend-inner-icon="mdi-magnify"
              clearable
              hide-details
              @input="debouncedSearch"
            />
          </v-col>
          
          <!-- Campaign Filter -->
          <v-col cols="12" md="3" sm="6">
            <v-select
              v-model="filters.campaign"
              label="Chiến dịch"
              variant="outlined"
              density="compact"
              :items="campaignOptions"
              item-title="label"
              item-value="value"
              clearable
              hide-details
              @update:model-value="updateCampaign"
            />
          </v-col>
          
          <!-- Action Type Filter -->
          <v-col cols="12" md="3" sm="6">
            <v-select
              v-model="filters.action_type"
              label="Loại hành động"
              variant="outlined"
              density="compact"
              :items="actionTypeOptions"
              item-title="label"
              item-value="value"
              clearable
              hide-details
              @update:model-value="updateActionType"
            />
          </v-col>
          
          <!-- Clear Filters -->
          <v-col cols="12" md="2" sm="6" class="d-flex justify-end">
            <v-btn
              variant="outlined"
              color="grey"
              @click="clearFilters"
            >
              <v-icon>mdi-filter-remove</v-icon>
              Xóa bộ lọc
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Statistics Cards -->
    <v-row class="mb-6">
      <v-col cols="12" md="3" sm="6">
        <v-card class="text-center pa-4" color="primary" variant="flat">
          <v-card-text class="text-white">
            <div class="text-h3 font-weight-bold mb-2">{{ stats.total_steps || 0 }}</div>
            <div class="text-body-1">Tổng số bước</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="3" sm="6">
        <v-card class="text-center pa-4" color="success" variant="flat">
          <v-card-text class="text-white">
            <div class="text-h3 font-weight-bold mb-2">{{ emailStepsCount }}</div>
            <div class="text-body-1">Bước gửi Email</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="3" sm="6">
        <v-card class="text-center pa-4" color="warning" variant="flat">
          <v-card-text class="text-white">
            <div class="text-h3 font-weight-bold mb-2">{{ manualStepsCount }}</div>
            <div class="text-body-1">Bước thủ công</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="3" sm="6">
        <v-card class="text-center pa-4" color="info" variant="flat">
          <v-card-text class="text-white">
            <div class="text-h3 font-weight-bold mb-2">{{ activeCampaignsCount }}</div>
            <div class="text-body-1">Chiến dịch có bước</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Data Table -->
    <v-card>
      <v-card-title class="d-flex align-center justify-space-between">
        <span>Danh sách bước chiến dịch</span>
        <div class="d-flex align-center">
          <v-chip
            v-if="selectedSteps.length > 0"
            color="primary"
            variant="flat"
            class="mr-3"
          >
            {{ selectedSteps.length }} đã chọn
          </v-chip>
          <v-menu v-if="selectedSteps.length > 0">
            <template v-slot:activator="{ props }">
              <v-btn
                v-bind="props"
                variant="outlined"
                color="primary"
                prepend-icon="mdi-dots-vertical"
              >
                Hành động
              </v-btn>
            </template>
            <v-list>
              <v-list-item @click="bulkDelete">
                <v-list-item-title>
                  <v-icon class="mr-2">mdi-delete</v-icon>
                  Xóa đã chọn
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </div>
      </v-card-title>
      
      <v-data-table
        v-model="selectedSteps"
        :headers="headers"
        :items="campaignSteps"
        :loading="loading"
        item-value="name"
        show-select
        :items-per-page="pagination.limit"
        :page="pagination.page"
        hide-default-footer
        class="elevation-0"
      >
        <!-- Step Order Column -->
        <template v-slot:item.step_order="{ item }">
          <v-chip
            color="primary"
            variant="flat"
            size="small"
          >
            {{ item.step_order }}
          </v-chip>
        </template>

        <!-- Campaign Column -->
        <template v-slot:item.campaign="{ item }">
          <div class="d-flex align-center">
            <v-icon class="mr-2" size="20">mdi-bullhorn</v-icon>
            <span>{{ item.campaign }}</span>
          </div>
        </template>

        <!-- Action Type Column -->
        <template v-slot:item.action_type="{ item }">
          <v-chip
            :color="getActionTypeColor(item.action_type)"
            variant="flat"
            size="small"
          >
            <v-icon class="mr-1" size="16">{{ getActionTypeIcon(item.action_type) }}</v-icon>
            {{ getActionTypeLabel(item.action_type) }}
          </v-chip>
        </template>

        <!-- Delay Column -->
        <template v-slot:item.delay_in_days="{ item }">
          <span class="text-body-2">
            {{ formatDelayText(item.delay_in_days) }}
          </span>
        </template>

        <!-- Template Column -->
        <template v-slot:item.template="{ item }">
          <div class="template-preview">
            <span v-if="item.template" class="text-body-2">
              {{ item.template.length > 50 ? item.template.substring(0, 50) + '...' : item.template }}
            </span>
            <span v-else class="text-medium-emphasis">Không có template</span>
          </div>
        </template>

        <!-- Actions Column -->
        <template v-slot:item.actions="{ item }">
          <div class="d-flex align-center">
            <v-tooltip text="Xem chi tiết">
              <template v-slot:activator="{ props }">
                <v-btn
                  v-bind="props"
                  icon
                  size="small"
                  variant="text"
                  @click="viewStep(item)"
                >
                  <v-icon>mdi-eye</v-icon>
                </v-btn>
              </template>
            </v-tooltip>
            
            <v-tooltip text="Chỉnh sửa">
              <template v-slot:activator="{ props }">
                <v-btn
                  v-bind="props"
                  icon
                  size="small"
                  variant="text"
                  @click="editStep(item)"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
              </template>
            </v-tooltip>
            
            <v-tooltip text="Xóa">
              <template v-slot:activator="{ props }">
                <v-btn
                  v-bind="props"
                  icon
                  size="small"
                  variant="text"
                  color="error"
                  @click="deleteStep(item)"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-tooltip>
          </div>
        </template>
      </v-data-table>

      <!-- Pagination -->
      <div class="d-flex justify-between align-center pa-4">
        <div class="text-body-2 text-medium-emphasis">
          Hiển thị {{ pagination.showing_from }} - {{ pagination.showing_to }} 
          trong tổng số {{ pagination.total }} bước chiến dịch
        </div>
        
        <v-pagination
          v-model="pagination.page"
          :length="pagination.pages"
          :total-visible="5"
          @update:model-value="changePage"
        />
      </div>
    </v-card>

    <!-- Create/Edit Modal -->
    <v-dialog v-model="showModal" max-width="800px" persistent>
      <v-card>
        <v-card-title class="d-flex align-center justify-space-between">
          <span>{{ isEditing ? 'Chỉnh sửa bước chiến dịch' : 'Thêm bước chiến dịch mới' }}</span>
          <v-btn
            icon
            variant="text"
            @click="closeModal"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        
        <v-card-text>
          <v-form ref="form" v-model="formValid">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.campaign_step_name"
                  label="Tên bước chiến dịch"
                  variant="outlined"
                  :rules="[v => !!v || 'Tên bước chiến dịch là bắt buộc']"
                  required
                />
              </v-col>
              
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.campaign"
                  label="Chiến dịch"
                  variant="outlined"
                  :items="campaignOptions"
                  item-title="label"
                  item-value="value"
                  :rules="[v => !!v || 'Chiến dịch là bắt buộc']"
                  required
                />
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="formData.step_order"
                  label="Thứ tự bước"
                  variant="outlined"
                  type="number"
                  :rules="[
                    v => !!v || 'Thứ tự bước là bắt buộc',
                    v => v > 0 || 'Thứ tự bước phải lớn hơn 0'
                  ]"
                  required
                />
              </v-col>
              
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.action_type"
                  label="Loại hành động"
                  variant="outlined"
                  :items="actionTypeOptions"
                  item-title="label"
                  item-value="value"
                  :rules="[v => !!v || 'Loại hành động là bắt buộc']"
                  required
                />
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="formData.delay_in_days"
                  label="Số ngày chờ"
                  variant="outlined"
                  type="number"
                  :rules="[
                    v => v >= 0 || 'Số ngày chờ không được âm'
                  ]"
                />
              </v-col>
              
              <v-col cols="12">
                <v-textarea
                  v-model="formData.template"
                  label="Template"
                  variant="outlined"
                  rows="4"
                  placeholder="Nhập template cho bước này..."
                />
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        
        <v-card-actions class="pa-4">
          <v-spacer />
          <v-btn
            variant="outlined"
            @click="closeModal"
          >
            Hủy
          </v-btn>
          <v-btn
            color="primary"
            variant="flat"
            :loading="saving"
            :disabled="!formValid"
            @click="saveStep"
          >
            {{ isEditing ? 'Cập nhật' : 'Tạo mới' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- View Modal -->
    <v-dialog v-model="showViewModal" max-width="600px">
      <v-card v-if="selectedStep">
        <v-card-title class="d-flex align-center justify-space-between">
          <span>Chi tiết bước chiến dịch</span>
          <v-btn
            icon
            variant="text"
            @click="showViewModal = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <v-list-item>
                <v-list-item-title>Tên bước</v-list-item-title>
                <v-list-item-subtitle>{{ selectedStep.campaign_step_name }}</v-list-item-subtitle>
              </v-list-item>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-list-item>
                <v-list-item-title>Chiến dịch</v-list-item-title>
                <v-list-item-subtitle>{{ selectedStep.campaign }}</v-list-item-subtitle>
              </v-list-item>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-list-item>
                <v-list-item-title>Thứ tự bước</v-list-item-title>
                <v-list-item-subtitle>{{ selectedStep.step_order }}</v-list-item-subtitle>
              </v-list-item>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-list-item>
                <v-list-item-title>Loại hành động</v-list-item-title>
                <v-list-item-subtitle>{{ getActionTypeLabel(selectedStep.action_type) }}</v-list-item-subtitle>
              </v-list-item>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-list-item>
                <v-list-item-title>Số ngày chờ</v-list-item-title>
                <v-list-item-subtitle>{{ formatDelayText(selectedStep.delay_in_days) }}</v-list-item-subtitle>
              </v-list-item>
            </v-col>
            
            <v-col cols="12">
              <v-list-item>
                <v-list-item-title>Template</v-list-item-title>
                <v-list-item-subtitle>
                  <pre class="text-wrap">{{ selectedStep.template || 'Không có template' }}</pre>
                </v-list-item-subtitle>
              </v-list-item>
            </v-col>
          </v-row>
        </v-card-text>
        
        <v-card-actions class="pa-4">
          <v-spacer />
          <v-btn
            variant="outlined"
            @click="showViewModal = false"
          >
            Đóng
          </v-btn>
          <v-btn
            color="primary"
            variant="flat"
            @click="editStep(selectedStep)"
          >
            Chỉnh sửa
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
    >
      {{ snackbar.message }}
      <template v-slot:actions>
        <v-btn
          variant="text"
          @click="snackbar.show = false"
        >
          Đóng
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { debounce } from 'lodash'
import * as campaignStepService from '@/services/campaignStepService'

export default {
  name: 'CampaignStepManagement',
  setup() {
    const router = useRouter()

    // Reactive data
    const loading = ref(false)
    const saving = ref(false)
    const formValid = ref(false)
    const showModal = ref(false)
    const showViewModal = ref(false)
    const isEditing = ref(false)
    const selectedStep = ref(null)
    const selectedSteps = ref([])
    
    const filters = reactive({
      search: '',
      campaign: '',
      action_type: ''
    })
    
    const pagination = reactive({
      page: 1,
      limit: 10,
      total: 0,
      pages: 0,
      has_next: false,
      has_prev: false,
      showing_from: 0,
      showing_to: 0
    })
    
    const campaignSteps = ref([])
    const stats = ref({})
    const campaignOptions = ref([])
    const actionTypeOptions = ref([])
    
    const formData = reactive({
      campaign_step_name: '',
      campaign: '',
      step_order: 1,
      action_type: '',
      delay_in_days: 0,
      template: ''
    })
    
    const snackbar = reactive({
      show: false,
      message: '',
      color: 'success',
      timeout: 3000
    })

    // Computed
    const headers = computed(() => [
      { title: 'Thứ tự', key: 'step_order', width: '80px' },
      { title: 'Tên bước', key: 'campaign_step_name', width: '200px' },
      { title: 'Chiến dịch', key: 'campaign', width: '150px' },
      { title: 'Loại hành động', key: 'action_type', width: '150px' },
      { title: 'Số ngày chờ', key: 'delay_in_days', width: '120px' },
      { title: 'Template', key: 'template', width: '200px' },
      { title: 'Hành động', key: 'actions', width: '150px', sortable: false }
    ])

    const emailStepsCount = computed(() => {
      return stats.value.action_type_stats?.find(s => s.action_type === 'SEND_EMAIL')?.count || 0
    })

    const manualStepsCount = computed(() => {
      const manualTypes = ['MANUAL_CALL', 'MANUAL_TASK']
      return stats.value.action_type_stats?.filter(s => manualTypes.includes(s.action_type))
        .reduce((sum, s) => sum + s.count, 0) || 0
    })

    const activeCampaignsCount = computed(() => {
      return stats.value.campaign_stats?.length || 0
    })

    // Methods
    const loadData = async () => {
      loading.value = true
      try {
        const response = await campaignStepService.getFilteredCampaignSteps({
          page: pagination.page,
          limit: pagination.limit,
          search: filters.search,
          campaign: filters.campaign,
          action_type: filters.action_type
        })
        
        campaignSteps.value = response.data
        Object.assign(pagination, response.pagination)
      } catch (error) {
        showSnackbar(error.message, 'error')
      } finally {
        loading.value = false
      }
    }

    const loadStats = async () => {
      try {
        const response = await campaignStepService.getCampaignStepStats()
        stats.value = response
      } catch (error) {
        console.error('Error loading stats:', error)
      }
    }

    const loadOptions = async () => {
      try {
        const [campaigns, actionTypes] = await Promise.all([
          campaignStepService.getCampaignOptions(),
          campaignStepService.getActionTypes()
        ])
        
        campaignOptions.value = campaigns
        actionTypeOptions.value = actionTypes
      } catch (error) {
        console.error('Error loading options:', error)
      }
    }

    const debouncedSearch = debounce(() => {
      pagination.page = 1
      loadData()
    }, 300)

    const updateCampaign = () => {
      pagination.page = 1
      loadData()
    }

    const updateActionType = () => {
      pagination.page = 1
      loadData()
    }

    const clearFilters = () => {
      filters.search = ''
      filters.campaign = ''
      filters.action_type = ''
      pagination.page = 1
      loadData()
    }

    const changePage = (page) => {
      pagination.page = page
      loadData()
    }

    const openCreateModal = () => {
      isEditing.value = false
      resetForm()
      showModal.value = true
    }

    const editStep = (step) => {
      isEditing.value = true
      selectedStep.value = step
      Object.assign(formData, step)
      showViewModal.value = false
      showModal.value = true
    }

    const viewStep = (step) => {
      selectedStep.value = step
      showViewModal.value = true
    }

    const closeModal = () => {
      showModal.value = false
      resetForm()
    }

    const resetForm = () => {
      Object.assign(formData, {
        campaign_step_name: '',
        campaign: '',
        step_order: 1,
        action_type: '',
        delay_in_days: 0,
        template: ''
      })
      selectedStep.value = null
    }

    const saveStep = async () => {
      if (!formValid.value) return
      
      saving.value = true
      try {
        if (isEditing.value) {
          await campaignStepService.updateCampaignStep(selectedStep.value.name, formData)
          showSnackbar('Cập nhật bước chiến dịch thành công', 'success')
        } else {
          await campaignStepService.createNewCampaignStep(formData)
          showSnackbar('Tạo bước chiến dịch thành công', 'success')
        }
        
        closeModal()
        await loadData()
        await loadStats()
      } catch (error) {
        showSnackbar(error.message, 'error')
      } finally {
        saving.value = false
      }
    }

    const deleteStep = async (step) => {
      if (!confirm('Bạn có chắc chắn muốn xóa bước chiến dịch này?')) return
      
      try {
        await campaignStepService.deleteCampaignStep(step.name)
        showSnackbar('Xóa bước chiến dịch thành công', 'success')
        await loadData()
        await loadStats()
      } catch (error) {
        showSnackbar(error.message, 'error')
      }
    }

    const bulkDelete = async () => {
      if (!confirm(`Bạn có chắc chắn muốn xóa ${selectedSteps.value.length} bước chiến dịch đã chọn?`)) return
      
      try {
        const deletePromises = selectedSteps.value.map(stepName => 
          campaignStepService.deleteCampaignStep(stepName)
        )
        await Promise.all(deletePromises)
        
        showSnackbar(`Xóa ${selectedSteps.value.length} bước chiến dịch thành công`, 'success')
        selectedSteps.value = []
        await loadData()
        await loadStats()
      } catch (error) {
        showSnackbar(error.message, 'error')
      }
    }

    const showSnackbar = (message, color = 'success') => {
      snackbar.message = message
      snackbar.color = color
      snackbar.show = true
    }

    const getActionTypeLabel = (actionType) => {
      return campaignStepService.getActionTypeLabel(actionType)
    }

    const formatDelayText = (delayInDays) => {
      return campaignStepService.formatDelayText(delayInDays)
    }

    const getActionTypeColor = (actionType) => {
      const colorMap = {
        'SEND_EMAIL': 'success',
        'SEND_SMS': 'info',
        'MANUAL_CALL': 'warning',
        'MANUAL_TASK': 'orange'
      }
      return colorMap[actionType] || 'grey'
    }

    const getActionTypeIcon = (actionType) => {
      const iconMap = {
        'SEND_EMAIL': 'mdi-email',
        'SEND_SMS': 'mdi-message-text',
        'MANUAL_CALL': 'mdi-phone',
        'MANUAL_TASK': 'mdi-clipboard-check'
      }
      return iconMap[actionType] || 'mdi-help'
    }

    // Lifecycle
    onMounted(async () => {
      await loadOptions()
      await loadData()
      await loadStats()
    })

    return {
      // Reactive data
      loading,
      saving,
      formValid,
      showModal,
      showViewModal,
      isEditing,
      selectedStep,
      selectedSteps,
      filters,
      pagination,
      campaignSteps,
      stats,
      campaignOptions,
      actionTypeOptions,
      formData,
      snackbar,
      
      // Computed
      headers,
      emailStepsCount,
      manualStepsCount,
      activeCampaignsCount,
      
      // Methods
      loadData,
      debouncedSearch,
      updateCampaign,
      updateActionType,
      clearFilters,
      changePage,
      openCreateModal,
      editStep,
      viewStep,
      closeModal,
      saveStep,
      deleteStep,
      bulkDelete,
      getActionTypeLabel,
      formatDelayText,
      getActionTypeColor,
      getActionTypeIcon
    }
  }
}
</script>

<style scoped>
.campaign-step-management-page {
  padding: 0;
}

.page-header {
  border-radius: 8px;
}

.template-preview {
  max-width: 200px;
  word-wrap: break-word;
}

.text-wrap {
  white-space: pre-wrap;
}
</style>
