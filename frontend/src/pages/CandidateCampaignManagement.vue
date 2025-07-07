<template>
  <div class="pa-4">
    <!-- Header -->
    <div class="d-flex justify-space-between align-center mb-4">
      <div>
        <h1 class="text-h4 font-weight-bold">Candidate Campaigns</h1>
        <p class="text-subtitle-1 text-medium-emphasis">Manage candidate campaign assignments</p>
      </div>
      <v-btn
        color="primary"
        size="large"
        prepend-icon="mdi-plus"
        @click="openFormModal()"
        class="text-none"
      >
        Add New
      </v-btn>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-md-3 col-6 mb-2">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="primary" size="40" class="mr-3">mdi-account-arrow-right</v-icon>
            <div>
              <div class="text-h6">{{ stats.total }}</div>
              <div class="text-caption text-medium-emphasis">Total Campaigns</div>
            </div>
          </div>
        </v-card>
      </div>
      <div class="col-md-3 col-6 mb-2">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="success" size="40" class="mr-3">mdi-play-circle</v-icon>
            <div>
              <div class="text-h6">{{ stats.active }}</div>
              <div class="text-caption text-medium-emphasis">Active</div>
            </div>
          </div>
        </v-card>
      </div>
      <div class="col-md-3 col-6 mb-2">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="warning" size="40" class="mr-3">mdi-pause-circle</v-icon>
            <div>
              <div class="text-h6">{{ stats.paused }}</div>
              <div class="text-caption text-medium-emphasis">Paused</div>
            </div>
          </div>
        </v-card>
      </div>
      <div class="col-md-3 col-6 mb-2">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="error" size="40" class="mr-3">mdi-stop-circle</v-icon>
            <div>
              <div class="text-h6">{{ stats.completed }}</div>
              <div class="text-caption text-medium-emphasis">Completed</div>
            </div>
          </div>
        </v-card>
      </div>
    </div>

    <!-- Filters & Search -->
    <v-card class="mb-4">
      <v-card-text>
        <div class="row">
          <div class="col-md-3 mb-2">
            <v-text-field
              v-model="search"
              label="Search campaigns..."
              prepend-inner-icon="mdi-magnify"
              clearable
              hide-details
              @input="debouncedSearch"
            />
          </div>
          <div class="col-md-2 mb-2">
            <v-select
              v-model="filters.candidate_id"
              :items="filterOptions.candidates"
              label="Candidate"
              clearable
              hide-details
              @update:model-value="applyFilters"
            />
          </div>
          <div class="col-md-2 mb-2">
            <v-select
              v-model="filters.campaign_id"
              :items="filterOptions.campaigns"
              label="Campaign"
              clearable
              hide-details
              @update:model-value="applyFilters"
            />
          </div>
          <div class="col-md-2 mb-2">
            <v-select
              v-model="filters.status"
              :items="statusOptions"
              label="Status"
              clearable
              hide-details
              @update:model-value="applyFilters"
            />
          </div>
          <div class="col-md-2 mb-2">
            <v-select
              v-model="filters.current_step"
              :items="filterOptions.steps"
              label="Current Step"
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
        <span>Candidate Campaigns ({{ pagination.total }})</span>
        <div>
          <v-btn
            v-if="selected.length > 0"
            color="warning"
            variant="outlined"
            prepend-icon="mdi-pause"
            @click="bulkPause"
            class="mr-2"
          >
            Pause Selected ({{ selected.length }})
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
        <template #item.candidate_id="{ item }">
          <div class="d-flex align-center">
            <v-avatar size="32" color="primary" class="mr-2">
              <span class="text-caption">{{ item.candidate_id?.charAt(0) }}</span>
            </v-avatar>
            <span>{{ item.candidate_id }}</span>
          </div>
        </template>

        <template #item.campaign_id="{ item }">
          <v-chip
            color="primary"
            variant="tonal"
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
          >
            {{ item.status }}
          </v-chip>
        </template>

        <template #item.current_step_order="{ item }">
          <v-chip
            color="info"
            variant="outlined"
            size="small"
          >
            Step {{ item.current_step_order }}
          </v-chip>
        </template>

        <template #item.enrolled_at="{ item }">
          <div class="text-body-2">
            {{ formatDate(item.enrolled_at) }}
          </div>
        </template>

        <template #item.next_action_at="{ item }">
          <div class="text-body-2">
            {{ formatDate(item.next_action_at) }}
          </div>
        </template>

        <template #item.actions="{ item }">
          <div class="d-flex align-center">
            <v-btn
              icon="mdi-play"
              size="small"
              variant="text"
              color="success"
              @click="startCampaign(item)"
              v-if="item.status === 'Draft' || item.status === 'Paused'"
            />
            <v-btn
              icon="mdi-pause"
              size="small"
              variant="text"
              color="warning"
              @click="pauseCampaign(item)"
              v-if="item.status === 'Active'"
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
    <v-dialog v-model="showFormModal" max-width="700px" persistent>
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center">
          <span>{{ formData.name ? 'Edit' : 'Add' }} Candidate Campaign</span>
          <v-btn icon="mdi-close" variant="text" @click="closeFormModal" />
        </v-card-title>
        
        <v-card-text>
          <v-form ref="form" v-model="formValid">
            <div class="row">
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
                  label="Campaign *"
                  :rules="[v => !!v || 'Campaign is required']"
                  required
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
                  v-model="formData.current_step_order"
                  label="Current Step Order"
                  type="number"
                  min="1"
                />
              </div>
              <div class="col-md-6">
                <v-text-field
                  v-model="formData.enrolled_at"
                  label="Enrolled At"
                  type="datetime-local"
                />
              </div>
              <div class="col-md-6">
                <v-text-field
                  v-model="formData.next_action_at"
                  label="Next Action At"
                  type="datetime-local"
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
          Are you sure you want to delete this candidate campaign?
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
import { candidateCampaignService, candidateService, campaignService } from '../services/universalService'
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
  { title: 'Active', value: 'ACTIVE' },
  { title: 'Paused', value: 'PAUSED' },
  { title: 'Completed', value: 'COMPLETED' },
  { title: 'Cancelled', value: 'CANCELLED' }
]

// Form data
const formData = reactive({
  name: '',
  candidate_id: '',
  campaign_id: '',
  status: 'ACTIVE',
  enrolled_at: '',
  current_step_order: 1,
  next_action_at: ''
})

// Filters
const filters = reactive({
  candidate_id: '',
  campaign_id: '',
  status: '',
  current_step: ''
})

// Filter options
const filterOptions = reactive({
  candidates: [],
  campaigns: [],
  steps: []
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
  active: 0,
  paused: 0,
  completed: 0
})

// Table headers
const headers = [
  { title: 'Candidate', key: 'candidate_id', sortable: false },
  { title: 'Campaign', key: 'campaign_id', sortable: false },
  { title: 'Status', key: 'status', sortable: false },
  { title: 'Current Step Order', key: 'current_step_order', sortable: false },
  { title: 'Enrolled At', key: 'enrolled_at', sortable: false },
  { title: 'Next Action At', key: 'next_action_at', sortable: false },
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
      searchConditions.push(['candidate_id', 'like', `%${search.value}%`])
      searchConditions.push(['campaign_id', 'like', `%${search.value}%`])
    }
    
    const params = {
      filters: apiFilters,
      page_length: pagination.limit,
      start: (pagination.page - 1) * pagination.limit,
      order_by: 'modified desc',
      fields: ['name', 'candidate_id', 'campaign_id', 'status', 'enrolled_at', 'current_step_order', 'next_action_at', 'modified']
    }
    
    // Add search conditions if any
    if (searchConditions.length > 0) {
      params.filters.search_text = searchConditions
    }

    const result = await candidateCampaignService.getList(params)
    
    if (result.success) {
      items.value = result.data || []
      Object.assign(pagination, result.pagination)
      
      // Update stats
      stats.total = result.pagination.total || 0
      stats.active = result.data?.filter(item => item.status === 'ACTIVE').length || 0
      stats.paused = result.data?.filter(item => item.status === 'PAUSED').length || 0
      stats.completed = result.data?.filter(item => item.status === 'COMPLETED').length || 0
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

    // Load steps
    for (let i = 1; i <= 10; i++) {
      filterOptions.steps.push({
        title: `Step ${i}`,
        value: i
      })
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
    formData.status = 'ACTIVE'
    formData.current_step_order = 1
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
    const result = await candidateCampaignService.save(formData, formData.name)
    
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

const startCampaign = async (item) => {
  try {
    const result = await candidateCampaignService.save(
      { ...item, status: 'Active', started_at: new Date().toISOString() },
      item.name
    )
    
    if (result.success) {
      loadData()
    }
  } catch (error) {
    console.error('Error starting campaign:', error)
  }
}

const pauseCampaign = async (item) => {
  try {
    const result = await candidateCampaignService.save(
      { ...item, status: 'Paused' },
      item.name
    )
    
    if (result.success) {
      loadData()
    }
  } catch (error) {
    console.error('Error pausing campaign:', error)
  }
}

const viewDetails = (item) => {
  router.push(`/candidate-campaigns/${item.name}`)
}

const confirmDelete = (item) => {
  itemToDelete.value = item
  showDeleteDialog.value = true
}

const deleteItem = async () => {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    const result = await candidateCampaignService.delete(itemToDelete.value.name)
    
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

const bulkPause = async () => {
  if (selected.value.length === 0) return

  const confirmed = confirm(`Are you sure you want to pause ${selected.value.length} campaigns?`)
  if (!confirmed) return

  try {
    const pausePromises = selected.value.map(name => {
      const item = items.value.find(i => i.name === name)
      return candidateCampaignService.save({ ...item, status: 'Paused' }, name)
    })
    
    await Promise.all(pausePromises)
    selected.value = []
    loadData()
  } catch (error) {
    console.error('Error bulk pausing:', error)
  }
}

const bulkDelete = async () => {
  if (selected.value.length === 0) return

  const confirmed = confirm(`Are you sure you want to delete ${selected.value.length} campaigns?`)
  if (!confirmed) return

  try {
    await Promise.all(
      selected.value.map(name => candidateCampaignService.delete(name))
    )
    selected.value = []
    loadData()
  } catch (error) {
    console.error('Error bulk deleting:', error)
  }
}

const exportData = () => {
  const data = items.value.map(item => ({
    Candidate: item.candidate_id,
    Campaign: item.campaign_id,
    Status: item.status,
    'Current Step Order': item.current_step_order,
    'Enrolled At': formatDate(item.enrolled_at),
    'Next Action At': formatDate(item.next_action_at)
  }))

  const csv = [
    Object.keys(data[0]).join(','),
    ...data.map(row => Object.values(row).join(','))
  ].join('\n')

  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'candidate-campaigns.csv'
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

const getStatusColor = (status) => {
  const colors = {
    'Draft': 'grey',
    'Active': 'success',
    'Paused': 'warning',
    'Completed': 'primary',
    'Stopped': 'error'
  }
  return colors[status] || 'grey'
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

.v-progress-linear {
  margin-bottom: 4px;
}
</style>
