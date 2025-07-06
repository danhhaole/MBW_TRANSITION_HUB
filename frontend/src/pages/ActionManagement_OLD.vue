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
              <div class="text-h6">{{ stats.completed }}</div>
              <div class="text-caption text-medium-emphasis">Completed</div>
            </div>
          </div>
        </v-card>
      </div>
      <div class="col-md-3 col-6">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="warning" size="40" class="mr-3">mdi-clock-outline</v-icon>
            <div>
              <div class="text-h6">{{ stats.pending }}</div>
              <div class="text-caption text-medium-emphasis">Pending</div>
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

    <!-- Filters & Search -->
    <v-card class="mb-4">
      <v-card-text>
        <div class="row">
          <div class="col-md-3">
            <v-text-field
              v-model="search"
              label="Search actions..."
              prepend-inner-icon="mdi-magnify"
              clearable
              hide-details
              @input="debouncedSearch"
            />
          </div>
          <div class="col-md-2">
            <v-select
              v-model="filters.action_type"
              :items="filterOptions.actionTypes"
              label="Action Type"
              clearable
              hide-details
              @update:model-value="applyFilters"
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
              v-model="filters.candidate_id"
              :items="filterOptions.candidates"
              label="Candidate"
              clearable
              hide-details
              @update:model-value="applyFilters"
            />
          </div>
          <div class="col-md-2">
            <v-select
              v-model="filters.campaign_id"
              :items="filterOptions.campaigns"
              label="Campaign"
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
            prepend-icon="mdi-download"
            @click="exportData"
          >
            Export
          </v-btn>
        </div>
      </v-card-title>
      
      <v-data-table
        v-model="selected"
        :headers="headers"
        :items="items"
        :loading="loading"
        item-value="name"
        show-select
        :items-per-page="pagination.limit"
        :page="pagination.page"
        hide-default-footer
        class="elevation-1"
      >
        <template #item.action_type="{ item }">
          <v-chip
            :color="getActionTypeColor(item.action_type)"
            variant="tonal"
            size="small"
            :prepend-icon="getActionTypeIcon(item.action_type)"
          >
            {{ item.action_type }}
          </v-chip>
        </template>

        <template #item.candidate_id="{ item }">
          <div class="d-flex align-center">
            <v-avatar size="24" color="primary" class="mr-2">
              <span class="text-caption">{{ item.candidate_id?.charAt(0) }}</span>
            </v-avatar>
            <span class="text-body-2">{{ item.candidate_id }}</span>
          </div>
        </template>

        <template #item.campaign_id="{ item }">
          <v-chip
            color="primary"
            variant="outlined"
            size="small"
          >
            {{ item.campaign_id }}
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

        <template #item.actions="{ item }">
          <div class="d-flex align-center">
            <v-btn
              icon="mdi-play"
              size="small"
              variant="text"
              color="success"
              @click="executeAction(item)"
              v-if="item.status === 'Pending' || item.status === 'Failed'"
            />
            <v-btn
              icon="mdi-eye"
              size="small"
              variant="text"
              @click="viewDetails(item)"
            />
            <v-btn
              icon="mdi-pencil"
              size="small"
              variant="text"
              @click="openFormModal(item)"
            />
            <v-btn
              icon="mdi-delete"
              size="small"
              variant="text"
              color="error"
              @click="confirmDelete(item)"
            />
          </div>
        </template>
      </v-data-table>

      <!-- Pagination -->
      <v-card-actions class="justify-space-between">
        <div class="text-caption text-medium-emphasis">
          Showing {{ pagination.showing_from }} to {{ pagination.showing_to }} of {{ pagination.total }} entries
        </div>
        <v-pagination
          v-model="pagination.page"
          :length="pagination.pages"
          :total-visible="7"
          @update:model-value="loadData"
        />
      </v-card-actions>
    </v-card>

    <!-- Form Modal -->
    <v-dialog v-model="showFormModal" max-width="800px" persistent>
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center">
          <span>{{ formData.name ? 'Edit' : 'Add' }} Action</span>
          <v-btn icon="mdi-close" variant="text" @click="closeFormModal" />
        </v-card-title>
        
        <v-card-text>
          <v-form ref="form" v-model="formValid">
            <div class="row">
              <div class="col-md-6">
                <v-select
                  v-model="formData.action_type"
                  :items="filterOptions.actionTypes"
                  label="Action Type *"
                  :rules="[v => !!v || 'Action type is required']"
                  required
                />
              </div>
              <div class="col-md-6">
                <v-select
                  v-model="formData.candidate_id"
                  :items="filterOptions.candidates"
                  label="Candidate *"
                  :rules="[v => !!v || 'Candidate is required']"
                  required
                />
              </div>
              <div class="col-md-6">
                <v-select
                  v-model="formData.campaign_id"
                  :items="filterOptions.campaigns"
                  label="Campaign"
                />
              </div>
              <div class="col-md-6">
                <v-select
                  v-model="formData.status"
                  :items="statusOptions"
                  label="Status *"
                  :rules="[v => !!v || 'Status is required']"
                  required
                />
              </div>
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
                  v-if="formData.status === 'Completed'"
                />
              </div>
              <div class="col-12">
                <v-textarea
                  v-model="formData.action_config"
                  label="Action Configuration (JSON)"
                  rows="4"
                  no-resize
                  placeholder='{"template": "email_template", "subject": "Hello"}'
                />
              </div>
              <div class="col-12">
                <v-textarea
                  v-model="formData.result"
                  label="Result"
                  rows="3"
                  no-resize
                  v-if="formData.status === 'Completed' || formData.status === 'Failed'"
                />
              </div>
            </div>
          </v-form>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer />
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
            :disabled="!formValid"
            @click="saveForm"
          >
            {{ formData.name ? 'Update' : 'Save' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation -->
    <v-dialog v-model="showDeleteDialog" max-width="400px">
      <v-card>
        <v-card-title>Confirm Delete</v-card-title>
        <v-card-text>
          Are you sure you want to delete this action?
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="grey" variant="text" @click="showDeleteDialog = false">
            Cancel
          </v-btn>
          <v-btn color="error" :loading="deleting" @click="deleteItem">
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
import { actionService, candidateService, campaignService } from '../services/universalService'
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

// Status options
const statusOptions = [
  { title: 'Pending', value: 'Pending' },
  { title: 'Completed', value: 'Completed' },
  { title: 'Failed', value: 'Failed' },
  { title: 'Cancelled', value: 'Cancelled' }
]

// Form data
const formData = reactive({
  name: '',
  action_type: '',
  candidate_id: '',
  campaign_id: '',
  status: 'Pending',
  scheduled_at: '',
  executed_at: '',
  action_config: '',
  result: ''
})

// Filters
const filters = reactive({
  action_type: '',
  candidate_id: '',
  campaign_id: '',
  status: ''
})

// Filter options
const filterOptions = reactive({
  actionTypes: [],
  candidates: [],
  campaigns: []
})

// Pagination
const pagination = reactive({
  page: 1,
  limit: 20,
  total: 0,
  pages: 0,
  showing_from: 0,
  showing_to: 0
})

// Stats
const stats = reactive({
  total: 0,
  completed: 0,
  pending: 0,
  failed: 0
})

// Table headers
const headers = [
  { title: 'Action Type', key: 'action_type', sortable: false },
  { title: 'Candidate', key: 'candidate_id', sortable: false },
  { title: 'Campaign', key: 'campaign_id', sortable: false },
  { title: 'Status', key: 'status', sortable: false },
  { title: 'Scheduled At', key: 'scheduled_at', sortable: false },
  { title: 'Executed At', key: 'executed_at', sortable: false },
  { title: 'Actions', key: 'actions', sortable: false, width: '180px' }
]

// Computed
const debouncedSearch = debounce(() => {
  loadData()
}, 300)

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
      searchConditions.push(['action_type', 'like', `%${search.value}%`])
      searchConditions.push(['candidate_id', 'like', `%${search.value}%`])
      searchConditions.push(['campaign_id', 'like', `%${search.value}%`])
    }
    
    const params = {
      filters: apiFilters,
      page_length: pagination.limit,
      start: (pagination.page - 1) * pagination.limit,
      order_by: 'scheduled_at desc',
      fields: ['name', 'action_type', 'candidate_id', 'campaign_id', 'status', 'scheduled_at', 'executed_at', 'action_config', 'result', 'modified']
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
      stats.completed = result.data?.filter(item => item.status === 'Completed').length || 0
      stats.pending = result.data?.filter(item => item.status === 'Pending').length || 0
      stats.failed = result.data?.filter(item => item.status === 'Failed').length || 0
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
    // Load action types
    const actionTypesResult = await actionService.getFilterOptions('action_type')
    if (actionTypesResult.success) {
      filterOptions.actionTypes = actionTypesResult.options.map(option => ({
        title: option.label || option.value,
        value: option.value
      }))
    }

    // Load candidates
    const candidatesResult = await candidateService.getList({ 
      fields: ['name', 'candidate_name'],
      page_length: 1000,
      filters: {}
    })
    if (candidatesResult.success) {
      filterOptions.candidates = candidatesResult.data.map(item => ({
        title: item.candidate_name || item.name,
        value: item.name
      }))
    }

    // Load campaigns
    const campaignsResult = await campaignService.getList({ 
      fields: ['name', 'campaign_name'],
      page_length: 1000,
      filters: {}
    })
    if (campaignsResult.success) {
      filterOptions.campaigns = campaignsResult.data.map(item => ({
        title: item.campaign_name || item.name,
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

const clearFilters = () => {
  Object.keys(filters).forEach(key => {
    filters[key] = ''
  })
  search.value = ''
  pagination.page = 1
  loadData()
}

const openFormModal = (item = null) => {
  if (item) {
    Object.assign(formData, item)
  } else {
    Object.keys(formData).forEach(key => {
      formData[key] = ''
    })
    formData.status = 'Pending'
  }
  showFormModal.value = true
}

const closeFormModal = () => {
  showFormModal.value = false
  Object.keys(formData).forEach(key => {
    formData[key] = ''
  })
}

const saveForm = async () => {
  if (!formValid.value) return

  saving.value = true
  try {
    const result = await actionService.save(formData, formData.name)
    
    if (result.success) {
      closeFormModal()
      loadData()
    }
  } catch (error) {
    console.error('Error saving:', error)
  } finally {
    saving.value = false
  }
}

const executeAction = async (item) => {
  try {
    const result = await actionService.save(
      { 
        ...item, 
        status: 'Completed', 
        executed_at: new Date().toISOString(),
        result: 'Action executed successfully'
      },
      item.name
    )
    
    if (result.success) {
      loadData()
    }
  } catch (error) {
    console.error('Error executing action:', error)
  }
}

const viewDetails = (item) => {
  router.push(`/actions/${item.name}`)
}

const confirmDelete = (item) => {
  itemToDelete.value = item
  showDeleteDialog.value = true
}

const deleteItem = async () => {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    const result = await actionService.delete(itemToDelete.value.name)
    
    if (result.success) {
      showDeleteDialog.value = false
      itemToDelete.value = null
      loadData()
    }
  } catch (error) {
    console.error('Error deleting:', error)
  } finally {
    deleting.value = false
  }
}

const bulkExecute = async () => {
  if (selected.value.length === 0) return

  const confirmed = confirm(`Are you sure you want to execute ${selected.value.length} actions?`)
  if (!confirmed) return

  try {
    const executePromises = selected.value.map(name => {
      const item = items.value.find(i => i.name === name)
      return actionService.save({ 
        ...item, 
        status: 'Completed', 
        executed_at: new Date().toISOString(),
        result: 'Bulk action executed'
      }, name)
    })
    
    await Promise.all(executePromises)
    selected.value = []
    loadData()
  } catch (error) {
    console.error('Error bulk executing:', error)
  }
}

const bulkDelete = async () => {
  if (selected.value.length === 0) return

  const confirmed = confirm(`Are you sure you want to delete ${selected.value.length} actions?`)
  if (!confirmed) return

  try {
    await Promise.all(
      selected.value.map(name => actionService.delete(name))
    )
    selected.value = []
    loadData()
  } catch (error) {
    console.error('Error bulk deleting:', error)
  }
}

const exportData = () => {
  const data = items.value.map(item => ({
    'Action Type': item.action_type,
    Candidate: item.candidate_id,
    Campaign: item.campaign_id,
    Status: item.status,
    'Scheduled At': formatDate(item.scheduled_at),
    'Executed At': formatDate(item.executed_at),
    Result: item.result
  }))

  const csv = [
    Object.keys(data[0]).join(','),
    ...data.map(row => Object.values(row).join(','))
  ].join('\n')

  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'actions.csv'
  a.click()
  URL.revokeObjectURL(url)
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getActionTypeColor = (type) => {
  const colors = {
    'Email': 'primary',
    'SMS': 'success',
    'Call': 'warning',
    'LinkedIn': 'info',
    'Follow Up': 'secondary'
  }
  return colors[type] || 'grey'
}

const getActionTypeIcon = (type) => {
  const icons = {
    'Email': 'mdi-email',
    'SMS': 'mdi-message',
    'Call': 'mdi-phone',
    'LinkedIn': 'mdi-linkedin',
    'Follow Up': 'mdi-repeat'
  }
  return icons[type] || 'mdi-lightning-bolt'
}

const getStatusColor = (status) => {
  const colors = {
    'Pending': 'warning',
    'Completed': 'success',
    'Failed': 'error',
    'Cancelled': 'grey'
  }
  return colors[status] || 'grey'
}

const getStatusIcon = (status) => {
  const icons = {
    'Pending': 'mdi-clock-outline',
    'Completed': 'mdi-check-circle',
    'Failed': 'mdi-alert-circle',
    'Cancelled': 'mdi-close-circle'
  }
  return icons[status] || 'mdi-help-circle'
}

// Lifecycle
onMounted(async () => {
  await loadFilterOptions()
  await loadData()
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
</style>
