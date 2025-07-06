<template>
  <div class="pa-4">
    <!-- Header -->
    <div class="d-flex justify-space-between align-center mb-4">
      <div>
        <h1 class="text-h4 font-weight-bold">Actions</h1>
        <p class="text-subtitle-1 text-medium-emphasis">Manage campaign actions and activities</p>
      </div>
      <v-btn
        color="primary"
        size="large"
        prepend-icon="mdi-plus"
        @click="openFormModal()"
        class="text-none"
      >
        Add New Action
      </v-btn>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-md-3 col-6">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="primary" size="40" class="mr-3">mdi-lightning-bolt</v-icon>
            <div>
              <div class="text-h6">{{ stats.total }}</div>
              <div class="text-caption text-medium-emphasis">Total Actions</div>
            </div>
          </div>
        </v-card>
      </div>
      <div class="col-md-3 col-6">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="success" size="40" class="mr-3">mdi-check-circle</v-icon>
            <div>
              <div class="text-h6">{{ stats.executed }}</div>
              <div class="text-caption text-medium-emphasis">Executed</div>
            </div>
          </div>
        </v-card>
      </div>
      <div class="col-md-3 col-6">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="warning" size="40" class="mr-3">mdi-clock-outline</v-icon>
            <div>
              <div class="text-h6">{{ stats.scheduled }}</div>
              <div class="text-caption text-medium-emphasis">Scheduled</div>
            </div>
          </div>
        </v-card>
      </div>
      <div class="col-md-3 col-6">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="error" size="40" class="mr-3">mdi-alert-circle</v-icon>
            <div>
              <div class="text-h6">{{ stats.failed }}</div>
              <div class="text-caption text-medium-emphasis">Failed</div>
            </div>
          </div>
        </v-card>
      </div>
    </div>

    <!-- Filters -->
    <v-card class="mb-4">
      <v-card-title>
        <v-icon class="mr-2">mdi-filter</v-icon>
        Filters
      </v-card-title>
      <v-card-text>
        <div class="row">
          <div class="col-md-3">
            <v-text-field
              v-model="search"
              label="Search..."
              prepend-inner-icon="mdi-magnify"
              clearable
              hide-details
              @update:model-value="debouncedSearch"
            />
          </div>
          <div class="col-md-2">
            <v-select
              v-model="filters.status"
              :items="statusOptions"
              label="Status"
              clearable
              hide-details
              @update:model-value="applyFilters"
            />
          </div>
          <div class="col-md-2">
            <v-select
              v-model="filters.campaign_step"
              :items="filterOptions.campaignSteps"
              label="Campaign Step"
              clearable
              hide-details
              @update:model-value="applyFilters"
            />
          </div>
          <div class="col-md-2">
            <v-select
              v-model="filters.candidate_campaign_id"
              :items="filterOptions.candidateCampaigns"
              label="Candidate Campaign"
              clearable
              hide-details
              @update:model-value="applyFilters"
            />
          </div>
          <div class="col-md-2">
            <v-select
              v-model="filters.assignee_id"
              :items="filterOptions.assignees"
              label="Assignee"
              clearable
              hide-details
              @update:model-value="applyFilters"
            />
          </div>
          <div class="col-md-1">
            <v-btn
              color="primary"
              variant="outlined"
              @click="clearFilters"
              class="mt-1"
            >
              Clear
            </v-btn>
          </div>
        </div>
      </v-card-text>
    </v-card>

    <!-- Data Table -->
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span>Actions ({{ pagination.total }})</span>
        <div>
          <v-btn
            v-if="selected.length > 0"
            color="success"
            variant="outlined"
            prepend-icon="mdi-play"
            @click="bulkExecute"
            class="mr-2"
          >
            Execute Selected ({{ selected.length }})
          </v-btn>
          <v-btn
            v-if="selected.length > 0"
            color="error"
            variant="outlined"
            prepend-icon="mdi-delete"
            @click="bulkDelete"
            class="mr-2"
          >
            Delete Selected ({{ selected.length }})
          </v-btn>
          <v-btn
            color="primary"
            variant="outlined"
            prepend-icon="mdi-export"
            @click="exportData"
          >
            Export
          </v-btn>
        </div>
      </v-card-title>
      <v-divider></v-divider>
      <v-data-table
        v-model="selected"
        :headers="headers"
        :items="items"
        :loading="loading"
        :server-items-length="pagination.total"
        :items-per-page="pagination.limit"
        :page="pagination.page"
        show-select
        class="elevation-0"
        @update:options="handleTableOptions"
      >
        <template #loading>
          <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
        </template>

        <template #item.candidate_campaign_id="{ item }">
          <v-chip
            color="primary"
            variant="outlined"
            size="small"
          >
            {{ item.candidate_campaign_id }}
          </v-chip>
        </template>

        <template #item.campaign_step="{ item }">
          <v-chip
            color="secondary"
            variant="outlined"
            size="small"
          >
            {{ item.campaign_step }}
          </v-chip>
        </template>

        <template #item.status="{ item }">
          <v-chip
            :color="getStatusColor(item.status)"
            variant="tonal"
            size="small"
            :prepend-icon="getStatusIcon(item.status)"
          >
            {{ item.status }}
          </v-chip>
        </template>

        <template #item.scheduled_at="{ item }">
          <div class="text-body-2">
            {{ formatDate(item.scheduled_at) }}
          </div>
        </template>

        <template #item.executed_at="{ item }">
          <div class="text-body-2">
            {{ formatDate(item.executed_at) }}
          </div>
        </template>

        <template #item.assignee_id="{ item }">
          <v-chip
            color="info"
            variant="outlined"
            size="small"
          >
            {{ item.assignee_id }}
          </v-chip>
        </template>

        <template #item.actions="{ item }">
          <div class="d-flex align-center">
            <v-btn
              icon="mdi-play"
              size="small"
              variant="text"
              color="success"
              @click="executeAction(item)"
              v-if="item.status === 'SCHEDULED' || item.status === 'FAILED'"
            />
            <v-btn
              icon="mdi-eye"
              size="small"
              variant="text"
              @click="openFormModal(item)"
              class="ml-1"
            />
            <v-btn
              icon="mdi-pencil"
              size="small"
              variant="text"
              @click="openFormModal(item)"
              class="ml-1"
            />
            <v-btn
              icon="mdi-delete"
              size="small"
              variant="text"
              color="error"
              @click="confirmDelete(item)"
              class="ml-1"
            />
          </div>
        </template>
      </v-data-table>

      <!-- Pagination -->
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-pagination
          v-model="pagination.page"
          :length="Math.ceil(pagination.total / pagination.limit)"
          @update:model-value="loadData"
        ></v-pagination>
      </v-card-actions>
    </v-card>

    <!-- Form Modal -->
    <v-dialog v-model="showFormModal" max-width="800">
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon class="mr-2">mdi-lightning-bolt</v-icon>
          {{ formData.name ? 'Edit Action' : 'Add New Action' }}
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-4">
          <v-form v-model="formValid" lazy-validation>
            <div class="row">
              <div class="col-md-6">
                <v-select
                  v-model="formData.candidate_campaign_id"
                  :items="filterOptions.candidateCampaigns"
                  label="Candidate Campaign *"
                  required
                  :rules="[v => !!v || 'Candidate Campaign is required']"
                />
              </div>
              <div class="col-md-6">
                <v-select
                  v-model="formData.campaign_step"
                  :items="filterOptions.campaignSteps"
                  label="Campaign Step *"
                  required
                  :rules="[v => !!v || 'Campaign Step is required']"
                />
              </div>
            </div>

            <div class="row">
              <div class="col-md-6">
                <v-select
                  v-model="formData.status"
                  :items="statusOptions"
                  label="Status *"
                  required
                  :rules="[v => !!v || 'Status is required']"
                />
              </div>
              <div class="col-md-6">
                <v-select
                  v-model="formData.assignee_id"
                  :items="filterOptions.assignees"
                  label="Assignee"
                  clearable
                />
              </div>
            </div>

            <div class="row">
              <div class="col-md-6">
                <v-text-field
                  v-model="formData.scheduled_at"
                  label="Scheduled At"
                  type="datetime-local"
                />
              </div>
              <div class="col-md-6">
                <v-text-field
                  v-model="formData.executed_at"
                  label="Executed At"
                  type="datetime-local"
                />
              </div>
            </div>

            <div class="row">
              <div class="col-12">
                <v-textarea
                  v-model="formData.result"
                  label="Result (JSON)"
                  placeholder="Enter result data as JSON..."
                  rows="4"
                />
              </div>
            </div>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="grey"
            variant="text"
            @click="closeFormModal"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            :loading="saving"
            @click="saveData"
          >
            {{ formData.name ? 'Update' : 'Create' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation -->
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">
          Confirm Delete
        </v-card-title>
        <v-card-text>
          Are you sure you want to delete this action? This action cannot be undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="grey"
            variant="text"
            @click="showDeleteDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="error"
            :loading="deleting"
            @click="deleteData"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { actionService, candidateCampaignService, campaignStepService, userService } from '../services/universalService'
import { debounce } from 'lodash'

const router = useRouter()

// State
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const items = ref([])
const selected = ref([])
const search = ref('')
const showFormModal = ref(false)
const showDeleteDialog = ref(false)
const formValid = ref(false)
const itemToDelete = ref(null)

// Status options matching doctype
const statusOptions = [
  { title: 'Scheduled', value: 'SCHEDULED' },
  { title: 'Executed', value: 'EXECUTED' },
  { title: 'Skipped', value: 'SKIPPED' },
  { title: 'Failed', value: 'FAILED' },
  { title: 'Pending Manual', value: 'PENDING_MANUAL' }
]

// Form data matching doctype fields
const formData = reactive({
  name: '',
  candidate_campaign_id: '',
  campaign_step: '',
  status: 'SCHEDULED',
  scheduled_at: '',
  executed_at: '',
  result: '',
  assignee_id: ''
})

// Filters
const filters = reactive({
  status: '',
  campaign_step: '',
  candidate_campaign_id: '',
  assignee_id: ''
})

// Filter options
const filterOptions = reactive({
  candidateCampaigns: [],
  campaignSteps: [],
  assignees: []
})

// Pagination
const pagination = reactive({
  page: 1,
  limit: 20,
  total: 0
})

// Stats
const stats = reactive({
  total: 0,
  executed: 0,
  scheduled: 0,
  failed: 0
})

// Table headers matching doctype fields
const headers = [
  { title: 'Candidate Campaign', key: 'candidate_campaign_id', sortable: true },
  { title: 'Campaign Step', key: 'campaign_step', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Scheduled At', key: 'scheduled_at', sortable: true },
  { title: 'Executed At', key: 'executed_at', sortable: true },
  { title: 'Assignee', key: 'assignee_id', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false }
]

// Methods
const loadData = async () => {
  loading.value = true
  try {
    // Prepare filters
    const apiFilters = {}
    
    // Add non-empty filters
    Object.keys(filters).forEach(key => {
      if (filters[key] && filters[key] !== '') {
        apiFilters[key] = filters[key]
      }
    })
    
    // Prepare search conditions
    const searchConditions = []
    if (search.value && search.value.trim() !== '') {
      searchConditions.push(['candidate_campaign_id', 'like', `%${search.value}%`])
      searchConditions.push(['campaign_step', 'like', `%${search.value}%`])
      searchConditions.push(['assignee_id', 'like', `%${search.value}%`])
    }
    
    const params = {
      filters: apiFilters,
      page_length: pagination.limit,
      start: (pagination.page - 1) * pagination.limit,
      order_by: 'scheduled_at desc',
      fields: ['name', 'candidate_campaign_id', 'campaign_step', 'status', 'scheduled_at', 'executed_at', 'result', 'assignee_id', 'modified']
    }
    
    // Add search conditions if any
    if (searchConditions.length > 0) {
      params.filters.search_text = searchConditions
    }

    const result = await actionService.getList(params)
    
    if (result.success) {
      items.value = result.data || []
      Object.assign(pagination, result.pagination)
      
      // Update stats
      stats.total = result.pagination.total || 0
      stats.executed = result.data?.filter(item => item.status === 'EXECUTED').length || 0
      stats.scheduled = result.data?.filter(item => item.status === 'SCHEDULED').length || 0
      stats.failed = result.data?.filter(item => item.status === 'FAILED').length || 0
    } else {
      console.error('Error loading data:', result.error)
      items.value = []
    }
  } catch (error) {
    console.error('Error loading data:', error)
    items.value = []
  } finally {
    loading.value = false
  }
}

const loadFilterOptions = async () => {
  try {
    // Load candidate campaigns
    const candidateCampaignResult = await candidateCampaignService.getList({
      fields: ['name', 'candidate_id', 'campaign_id'],
      page_length: 1000
    })
    if (candidateCampaignResult.success) {
      filterOptions.candidateCampaigns = candidateCampaignResult.data.map(item => ({
        title: `${item.name} (${item.candidate_id} - ${item.campaign_id})`,
        value: item.name
      }))
    }
    
    // Load campaign steps
    const campaignStepResult = await campaignStepService.getList({
      fields: ['name', 'step_name', 'campaign_id'],
      page_length: 1000
    })
    if (campaignStepResult.success) {
      filterOptions.campaignSteps = campaignStepResult.data.map(item => ({
        title: `${item.step_name} (${item.campaign_id})`,
        value: item.name
      }))
    }
    
    // Load assignees (users)
    const userResult = await userService.getList({
      fields: ['name', 'first_name', 'last_name', 'email'],
      page_length: 1000
    })
    if (userResult.success) {
      filterOptions.assignees = userResult.data.map(item => ({
        title: `${item.first_name} ${item.last_name} (${item.email})`,
        value: item.name
      }))
    }
  } catch (error) {
    console.error('Error loading filter options:', error)
  }
}

const applyFilters = debounce(() => {
  pagination.page = 1
  loadData()
}, 300)

const debouncedSearch = debounce(() => {
  pagination.page = 1
  loadData()
}, 300)

const clearFilters = () => {
  Object.keys(filters).forEach(key => {
    filters[key] = ''
  })
  search.value = ''
  pagination.page = 1
  loadData()
}

const handleTableOptions = (options) => {
  pagination.page = options.page
  pagination.limit = options.itemsPerPage
  loadData()
}

const openFormModal = (item = null) => {
  if (item) {
    Object.assign(formData, item)
  } else {
    resetForm()
  }
  showFormModal.value = true
}

const closeFormModal = () => {
  showFormModal.value = false
  resetForm()
}

const resetForm = () => {
  Object.assign(formData, {
    name: '',
    candidate_campaign_id: '',
    campaign_step: '',
    status: 'SCHEDULED',
    scheduled_at: '',
    executed_at: '',
    result: '',
    assignee_id: ''
  })
}

const saveData = async () => {
  if (!formValid.value) return

  saving.value = true
  try {
    const result = await actionService.save(formData)
    if (result.success) {
      closeFormModal()
      loadData()
    } else {
      console.error('Error saving data:', result.error)
    }
  } catch (error) {
    console.error('Error saving data:', error)
  } finally {
    saving.value = false
  }
}

const confirmDelete = (item) => {
  itemToDelete.value = item
  showDeleteDialog.value = true
}

const deleteData = async () => {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    const result = await actionService.delete(itemToDelete.value.name)
    if (result.success) {
      showDeleteDialog.value = false
      loadData()
    } else {
      console.error('Error deleting data:', result.error)
    }
  } catch (error) {
    console.error('Error deleting data:', error)
  } finally {
    deleting.value = false
  }
}

const executeAction = async (item) => {
  try {
    // Update status to EXECUTED
    const result = await actionService.save({
      name: item.name,
      status: 'EXECUTED',
      executed_at: new Date().toISOString()
    })
    if (result.success) {
      loadData()
    }
  } catch (error) {
    console.error('Error executing action:', error)
  }
}

const bulkExecute = async () => {
  try {
    for (const item of selected.value) {
      await executeAction(item)
    }
    selected.value = []
    loadData()
  } catch (error) {
    console.error('Error executing bulk actions:', error)
  }
}

const bulkDelete = async () => {
  try {
    for (const item of selected.value) {
      await actionService.delete(item.name)
    }
    selected.value = []
    loadData()
  } catch (error) {
    console.error('Error deleting bulk actions:', error)
  }
}

const exportData = async () => {
  try {
    const result = await actionService.export({
      filters: filters,
      fields: ['name', 'candidate_campaign_id', 'campaign_step', 'status', 'scheduled_at', 'executed_at', 'result', 'assignee_id']
    })
    if (result.success) {
      // Handle export (download file)
      console.log('Export successful')
    }
  } catch (error) {
    console.error('Error exporting data:', error)
  }
}

const getStatusColor = (status) => {
  switch (status) {
    case 'SCHEDULED': return 'info'
    case 'EXECUTED': return 'success'
    case 'SKIPPED': return 'warning'
    case 'FAILED': return 'error'
    case 'PENDING_MANUAL': return 'purple'
    default: return 'grey'
  }
}

const getStatusIcon = (status) => {
  switch (status) {
    case 'SCHEDULED': return 'mdi-clock-outline'
    case 'EXECUTED': return 'mdi-check-circle'
    case 'SKIPPED': return 'mdi-skip-forward'
    case 'FAILED': return 'mdi-alert-circle'
    case 'PENDING_MANUAL': return 'mdi-account-clock'
    default: return 'mdi-help-circle'
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  try {
    return new Date(dateString).toLocaleString()
  } catch {
    return dateString
  }
}

// Lifecycle
onMounted(() => {
  loadData()
  loadFilterOptions()
})
</script>

<style scoped>
.v-card {
  border-radius: 8px;
}

.v-data-table {
  border-radius: 8px;
}

.v-chip {
  font-weight: 500;
}

.text-h4 {
  color: #1976d2;
}

.text-subtitle-1 {
  margin-top: 4px;
}

.v-skeleton-loader {
  margin: 16px;
}

.v-btn {
  text-transform: none;
}

.v-dialog .v-card {
  border-radius: 12px;
}

.v-select, .v-text-field, .v-textarea {
  margin-bottom: 16px;
}

.row {
  margin: 0 -8px;
}

.row > [class*="col-"] {
  padding: 0 8px;
}
</style>
