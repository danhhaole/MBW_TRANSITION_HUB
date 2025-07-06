<template>
  <div class="pa-4">
    <!-- Header -->
    <div class="d-flex justify-space-between align-center mb-4">
      <div>
        <h1 class="text-h4 font-weight-bold">Interactions</h1>
        <p class="text-subtitle-1 text-medium-emphasis">Track and manage candidate interactions</p>
      </div>
      <v-btn
        color="primary"
        size="large"
        prepend-icon="mdi-plus"
        @click="openFormModal()"
        class="text-none"
      >
        Add New Interaction
      </v-btn>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-md-3 col-6">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="primary" size="40" class="mr-3">mdi-chat</v-icon>
            <div>
              <div class="text-h6">{{ stats.total }}</div>
              <div class="text-caption text-medium-emphasis">Total Interactions</div>
            </div>
          </div>
        </v-card>
      </div>
      <div class="col-md-3 col-6">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="success" size="40" class="mr-3">mdi-email-check</v-icon>
            <div>
              <div class="text-h6">{{ stats.emails }}</div>
              <div class="text-caption text-medium-emphasis">Email Interactions</div>
            </div>
          </div>
        </v-card>
      </div>
      <div class="col-md-3 col-6">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="warning" size="40" class="mr-3">mdi-phone</v-icon>
            <div>
              <div class="text-h6">{{ stats.calls }}</div>
              <div class="text-caption text-medium-emphasis">Call Interactions</div>
            </div>
          </div>
        </v-card>
      </div>
      <div class="col-md-3 col-6">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="info" size="40" class="mr-3">mdi-calendar-today</v-icon>
            <div>
              <div class="text-h6">{{ stats.today }}</div>
              <div class="text-caption text-medium-emphasis">Today</div>
            </div>
          </div>
        </v-card>
      </div>
    </div>

    <!-- Filters & Search -->
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
              label="Search interactions..."
              prepend-inner-icon="mdi-magnify"
              clearable
              hide-details
              @update:model-value="debouncedSearch"
            />
          </div>
          <div class="col-md-2">
            <v-select
              v-model="filters.interaction_type"
              :items="interactionTypeOptions"
              label="Type"
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
              v-model="filters.action"
              :items="filterOptions.actions"
              label="Source Action"
              clearable
              hide-details
              @update:model-value="applyFilters"
            />
          </div>
          <div class="col-md-2">
            <v-text-field
              v-model="filters.url"
              label="URL"
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
        <span>Interactions ({{ pagination.total }})</span>
        <div>
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

        <template #item.interaction_type="{ item }">
          <v-chip
            :color="getInteractionTypeColor(item.interaction_type)"
            variant="tonal"
            size="small"
            :prepend-icon="getInteractionTypeIcon(item.interaction_type)"
          >
            {{ item.interaction_type }}
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

        <template #item.action="{ item }">
          <v-chip
            color="secondary"
            variant="outlined"
            size="small"
            v-if="item.action"
          >
            {{ item.action }}
          </v-chip>
          <span v-else class="text-grey">-</span>
        </template>

        <template #item.url="{ item }">
          <v-btn
            v-if="item.url"
            :href="item.url"
            target="_blank"
            variant="text"
            size="small"
            prepend-icon="mdi-open-in-new"
          >
            Link
          </v-btn>
          <span v-else class="text-grey">-</span>
        </template>

        <template #item.description="{ item }">
          <v-tooltip location="top">
            <template #activator="{ props }">
              <span v-bind="props" class="text-truncate" style="max-width: 200px; display: block;">
                {{ item.description || '-' }}
              </span>
            </template>
            <span>{{ item.description || 'No description' }}</span>
          </v-tooltip>
        </template>

        <template #item.modified="{ item }">
          <div class="text-body-2">
            {{ formatDate(item.modified) }}
          </div>
        </template>

        <template #item.actions="{ item }">
          <div class="d-flex align-center">
            <v-btn
              icon="mdi-eye"
              size="small"
              variant="text"
              @click="openFormModal(item)"
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
          <v-icon class="mr-2">mdi-chat</v-icon>
          {{ formData.name ? 'Edit Interaction' : 'Add New Interaction' }}
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-4">
          <v-form v-model="formValid" lazy-validation>
            <div class="row">
              <div class="col-md-6">
                <v-select
                  v-model="formData.candidate_id"
                  :items="filterOptions.candidates"
                  label="Candidate *"
                  required
                  :rules="[v => !!v || 'Candidate is required']"
                />
              </div>
              <div class="col-md-6">
                <v-select
                  v-model="formData.interaction_type"
                  :items="interactionTypeOptions"
                  label="Interaction Type *"
                  required
                  :rules="[v => !!v || 'Interaction type is required']"
                />
              </div>
            </div>

            <div class="row">
              <div class="col-md-6">
                <v-select
                  v-model="formData.action"
                  :items="filterOptions.actions"
                  label="Source Action"
                  clearable
                />
              </div>
              <div class="col-md-6">
                <v-text-field
                  v-model="formData.url"
                  label="URL"
                  placeholder="https://example.com/page"
                />
              </div>
            </div>

            <div class="row">
              <div class="col-12">
                <v-textarea
                  v-model="formData.description"
                  label="Description"
                  placeholder="Enter detailed description of the interaction..."
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
          Are you sure you want to delete this interaction? This action cannot be undone.
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
import { interactionService, candidateService, actionService } from '../services/universalService'
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

// Interaction type options matching doctype
const interactionTypeOptions = [
  { title: 'Email Sent', value: 'EMAIL_SENT' },
  { title: 'Email Delivered', value: 'EMAIL_DELIVERED' },
  { title: 'Email Bounced', value: 'EMAIL_BOUNCED' },
  { title: 'Email Opened', value: 'EMAIL_OPENED' },
  { title: 'Email Clicked', value: 'EMAIL_CLICKED' },
  { title: 'Email Unsubscribed', value: 'EMAIL_UNSUBSCRIBED' },
  { title: 'Email Replied', value: 'EMAIL_REPLIED' },
  { title: 'Page Visited', value: 'PAGE_VISITED' },
  { title: 'Form Submitted', value: 'FORM_SUBMITTED' },
  { title: 'Download Triggered', value: 'DOWNLOAD_TRIGGERED' },
  { title: 'Chat Started', value: 'CHAT_STARTED' },
  { title: 'Chat Message Sent', value: 'CHAT_MESSAGE_SENT' },
  { title: 'Chat Completed', value: 'CHAT_COMPLETED' },
  { title: 'Call Missed', value: 'CALL_MISSED' },
  { title: 'Call Completed', value: 'CALL_COMPLETED' },
  { title: 'SMS Sent', value: 'SMS_SENT' },
  { title: 'SMS Delivered', value: 'SMS_DELIVERED' },
  { title: 'SMS Replied', value: 'SMS_REPLIED' },
  { title: 'Application Submitted', value: 'APPLICATION_SUBMITTED' },
  { title: 'Document Uploaded', value: 'DOCUMENT_UPLOADED' },
  { title: 'Test Started', value: 'TEST_STARTED' },
  { title: 'Test Completed', value: 'TEST_COMPLETED' },
  { title: 'Interview Confirmed', value: 'INTERVIEW_CONFIRMED' },
  { title: 'Interview Rescheduled', value: 'INTERVIEW_RESCHEDULED' }
]

// Form data matching doctype fields
const formData = reactive({
  name: '',
  candidate_id: '',
  interaction_type: '',
  action: '',
  url: '',
  description: ''
})

// Filters
const filters = reactive({
  interaction_type: '',
  candidate_id: '',
  action: '',
  url: ''
})

// Filter options
const filterOptions = reactive({
  candidates: [],
  actions: []
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
  emails: 0,
  calls: 0,
  today: 0
})

// Table headers matching doctype fields
const headers = [
  { title: 'Candidate', key: 'candidate_id', sortable: true },
  { title: 'Type', key: 'interaction_type', sortable: true },
  { title: 'Source Action', key: 'action', sortable: true },
  { title: 'URL', key: 'url', sortable: false },
  { title: 'Description', key: 'description', sortable: false },
  { title: 'Modified', key: 'modified', sortable: true },
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
      searchConditions.push(['candidate_id', 'like', `%${search.value}%`])
      searchConditions.push(['interaction_type', 'like', `%${search.value}%`])
      searchConditions.push(['description', 'like', `%${search.value}%`])
    }
    
    const params = {
      filters: apiFilters,
      page_length: pagination.limit,
      start: (pagination.page - 1) * pagination.limit,
      order_by: 'modified desc',
      fields: ['name', 'candidate_id', 'interaction_type', 'action', 'url', 'description', 'modified']
    }
    
    // Add search conditions if any
    if (searchConditions.length > 0) {
      params.filters.search_text = searchConditions
    }

    const result = await interactionService.getList(params)
    
    if (result.success) {
      items.value = result.data || []
      Object.assign(pagination, result.pagination)
      
      // Update stats
      stats.total = result.pagination.total || 0
      stats.emails = result.data?.filter(item => item.interaction_type.includes('EMAIL')).length || 0
      stats.calls = result.data?.filter(item => item.interaction_type.includes('CALL')).length || 0
      
      // Count today's interactions
      const today = new Date().toISOString().split('T')[0]
      stats.today = result.data?.filter(item => 
        item.modified && item.modified.startsWith(today)
      ).length || 0
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
    const candidateResult = await candidateService.getList({
      fields: ['name', 'full_name', 'email'],
      page_length: 1000
    })
    if (candidateResult.success) {
      filterOptions.candidates = candidateResult.data.map(item => ({
        title: `${item.full_name} (${item.email})`,
        value: item.name
      }))
    }
    
    // Load actions
    const actionResult = await actionService.getList({
      fields: ['name', 'candidate_campaign_id', 'campaign_step'],
      page_length: 1000
    })
    if (actionResult.success) {
      filterOptions.actions = actionResult.data.map(item => ({
        title: `${item.candidate_campaign_id} - ${item.campaign_step}`,
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
    candidate_id: '',
    interaction_type: '',
    action: '',
    url: '',
    description: ''
  })
}

const saveData = async () => {
  if (!formValid.value) return

  saving.value = true
  try {
    const result = await interactionService.save(formData)
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
    const result = await interactionService.delete(itemToDelete.value.name)
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

const bulkDelete = async () => {
  try {
    for (const item of selected.value) {
      await interactionService.delete(item.name)
    }
    selected.value = []
    loadData()
  } catch (error) {
    console.error('Error deleting bulk interactions:', error)
  }
}

const exportData = async () => {
  try {
    const result = await interactionService.export({
      filters: filters,
      fields: ['name', 'candidate_id', 'interaction_type', 'action', 'url', 'description', 'modified']
    })
    if (result.success) {
      // Handle export (download file)
      console.log('Export successful')
    }
  } catch (error) {
    console.error('Error exporting data:', error)
  }
}

const getInteractionTypeColor = (type) => {
  if (type.includes('EMAIL')) return 'primary'
  if (type.includes('CALL')) return 'warning'
  if (type.includes('SMS')) return 'secondary'
  if (type.includes('CHAT')) return 'info'
  if (type.includes('PAGE')) return 'success'
  if (type.includes('FORM')) return 'purple'
  if (type.includes('DOWNLOAD')) return 'orange'
  if (type.includes('TEST')) return 'indigo'
  if (type.includes('INTERVIEW')) return 'teal'
  return 'grey'
}

const getInteractionTypeIcon = (type) => {
  if (type.includes('EMAIL')) return 'mdi-email'
  if (type.includes('CALL')) return 'mdi-phone'
  if (type.includes('SMS')) return 'mdi-message-text'
  if (type.includes('CHAT')) return 'mdi-chat'
  if (type.includes('PAGE')) return 'mdi-web'
  if (type.includes('FORM')) return 'mdi-form-select'
  if (type.includes('DOWNLOAD')) return 'mdi-download'
  if (type.includes('TEST')) return 'mdi-clipboard-check'
  if (type.includes('INTERVIEW')) return 'mdi-account-voice'
  return 'mdi-information'
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

.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
