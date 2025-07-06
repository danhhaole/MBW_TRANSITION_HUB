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
              <div class="text-caption text-medium-emphasis">Emails</div>
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
              <div class="text-caption text-medium-emphasis">Calls</div>
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
      <v-card-text>
        <div class="row">
          <div class="col-md-3">
            <v-text-field
              v-model="search"
              label="Search interactions..."
              prepend-inner-icon="mdi-magnify"
              clearable
              hide-details
              @input="debouncedSearch"
            />
          </div>
          <div class="col-md-2">
            <v-select
              v-model="filters.interaction_type"
              :items="filterOptions.interactionTypes"
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
              v-model="filters.campaign_id"
              :items="filterOptions.campaigns"
              label="Campaign"
              clearable
              hide-details
              @update:model-value="applyFilters"
            />
          </div>
          <div class="col-md-2">
            <v-select
              v-model="filters.direction"
              :items="directionOptions"
              label="Direction"
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

        <template #item.campaign_id="{ item }">
          <v-chip
            color="primary"
            variant="outlined"
            size="small"
            v-if="item.campaign_id"
          >
            {{ item.campaign_id }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <template #item.direction="{ item }">
          <v-chip
            :color="getDirectionColor(item.direction)"
            variant="outlined"
            size="small"
            :prepend-icon="getDirectionIcon(item.direction)"
          >
            {{ item.direction }}
          </v-chip>
        </template>

        <template #item.subject="{ item }">
          <div class="text-truncate" style="max-width: 200px;">
            {{ item.subject || item.content?.substring(0, 50) + '...' }}
          </div>
        </template>

        <template #item.interaction_date="{ item }">
          <div class="text-body-2">
            {{ formatDate(item.interaction_date) }}
          </div>
        </template>

        <template #item.actions="{ item }">
          <div class="d-flex align-center">
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
          <span>{{ formData.name ? 'Edit' : 'Add' }} Interaction</span>
          <v-btn icon="mdi-close" variant="text" @click="closeFormModal" />
        </v-card-title>
        
        <v-card-text>
          <v-form ref="form" v-model="formValid">
            <div class="row">
              <div class="col-md-6">
                <v-select
                  v-model="formData.interaction_type"
                  :items="filterOptions.interactionTypes"
                  label="Interaction Type *"
                  :rules="[v => !!v || 'Type is required']"
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
                  v-model="formData.direction"
                  :items="directionOptions"
                  label="Direction *"
                  :rules="[v => !!v || 'Direction is required']"
                  required
                />
              </div>
              <div class="col-md-6">
                <v-text-field
                  v-model="formData.interaction_date"
                  label="Interaction Date *"
                  type="datetime-local"
                  :rules="[v => !!v || 'Date is required']"
                  required
                />
              </div>
              <div class="col-md-6">
                <v-text-field
                  v-model="formData.duration"
                  label="Duration (minutes)"
                  type="number"
                  min="0"
                  v-if="formData.interaction_type === 'Call'"
                />
              </div>
              <div class="col-12">
                <v-text-field
                  v-model="formData.subject"
                  label="Subject"
                  v-if="formData.interaction_type === 'Email'"
                />
              </div>
              <div class="col-12">
                <v-textarea
                  v-model="formData.content"
                  label="Content *"
                  rows="5"
                  no-resize
                  :rules="[v => !!v || 'Content is required']"
                  required
                />
              </div>
              <div class="col-12">
                <v-textarea
                  v-model="formData.notes"
                  label="Notes"
                  rows="3"
                  no-resize
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
          Are you sure you want to delete this interaction?
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
import { interactionService, candidateService, campaignService } from '../services/universalService'
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

// Direction options
const directionOptions = [
  { title: 'Inbound', value: 'Inbound' },
  { title: 'Outbound', value: 'Outbound' }
]

// Form data
const formData = reactive({
  name: '',
  interaction_type: '',
  candidate_id: '',
  campaign_id: '',
  direction: '',
  interaction_date: '',
  subject: '',
  content: '',
  duration: '',
  notes: ''
})

// Filters
const filters = reactive({
  interaction_type: '',
  candidate_id: '',
  campaign_id: '',
  direction: ''
})

// Filter options
const filterOptions = reactive({
  interactionTypes: [],
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
  emails: 0,
  calls: 0,
  today: 0
})

// Table headers
const headers = [
  { title: 'Type', key: 'interaction_type', sortable: false },
  { title: 'Candidate', key: 'candidate_id', sortable: false },
  { title: 'Campaign', key: 'campaign_id', sortable: false },
  { title: 'Direction', key: 'direction', sortable: false },
  { title: 'Subject/Content', key: 'subject', sortable: false },
  { title: 'Date', key: 'interaction_date', sortable: false },
  { title: 'Actions', key: 'actions', sortable: false, width: '150px' }
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
      searchConditions.push(['subject', 'like', `%${search.value}%`])
      searchConditions.push(['content', 'like', `%${search.value}%`])
      searchConditions.push(['candidate_id', 'like', `%${search.value}%`])
    }
    
    const params = {
      filters: apiFilters,
      page_length: pagination.limit,
      start: (pagination.page - 1) * pagination.limit,
      order_by: 'interaction_date desc',
      fields: ['name', 'interaction_type', 'candidate_id', 'campaign_id', 'direction', 'interaction_date', 'subject', 'content', 'duration', 'notes', 'modified']
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
      stats.emails = result.data?.filter(item => item.interaction_type === 'Email').length || 0
      stats.calls = result.data?.filter(item => item.interaction_type === 'Call').length || 0
      stats.today = result.data?.filter(item => 
        new Date(item.interaction_date).toDateString() === new Date().toDateString()
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
    // Load interaction types
    const interactionTypesResult = await interactionService.getFilterOptions('interaction_type')
    if (interactionTypesResult.success) {
      filterOptions.interactionTypes = interactionTypesResult.options.map(option => ({
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
    if (formData.interaction_date) {
      formData.interaction_date = new Date(formData.interaction_date).toISOString().slice(0, 16)
    }
  } else {
    Object.keys(formData).forEach(key => {
      formData[key] = ''
    })
    formData.interaction_date = new Date().toISOString().slice(0, 16)
    formData.direction = 'Outbound'
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
    const result = await interactionService.save(formData, formData.name)
    
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

const viewDetails = (item) => {
  router.push(`/interactions/${item.name}`)
}

const confirmDelete = (item) => {
  itemToDelete.value = item
  showDeleteDialog.value = true
}

const deleteItem = async () => {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    const result = await interactionService.delete(itemToDelete.value.name)
    
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

const bulkDelete = async () => {
  if (selected.value.length === 0) return

  const confirmed = confirm(`Are you sure you want to delete ${selected.value.length} interactions?`)
  if (!confirmed) return

  try {
    await Promise.all(
      selected.value.map(name => interactionService.delete(name))
    )
    selected.value = []
    loadData()
  } catch (error) {
    console.error('Error bulk deleting:', error)
  }
}

const exportData = () => {
  const data = items.value.map(item => ({
    'Type': item.interaction_type,
    'Candidate': item.candidate_id,
    'Campaign': item.campaign_id,
    'Direction': item.direction,
    'Subject': item.subject,
    'Content': item.content,
    'Date': formatDate(item.interaction_date),
    'Duration': item.duration,
    'Notes': item.notes
  }))

  const csv = [
    Object.keys(data[0]).join(','),
    ...data.map(row => Object.values(row).join(','))
  ].join('\n')

  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'interactions.csv'
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

const getInteractionTypeColor = (type) => {
  const colors = {
    'Email': 'primary',
    'Call': 'warning',
    'Meeting': 'success',
    'SMS': 'info',
    'LinkedIn': 'secondary'
  }
  return colors[type] || 'grey'
}

const getInteractionTypeIcon = (type) => {
  const icons = {
    'Email': 'mdi-email',
    'Call': 'mdi-phone',
    'Meeting': 'mdi-calendar',
    'SMS': 'mdi-message',
    'LinkedIn': 'mdi-linkedin'
  }
  return icons[type] || 'mdi-chat'
}

const getDirectionColor = (direction) => {
  return direction === 'Inbound' ? 'success' : 'primary'
}

const getDirectionIcon = (direction) => {
  return direction === 'Inbound' ? 'mdi-arrow-down' : 'mdi-arrow-up'
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

.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
