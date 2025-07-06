<template>
  <div class="pa-4">
    <!-- Header -->
    <div class="d-flex justify-space-between align-center mb-4">
      <div>
        <h1 class="text-h4 font-weight-bold">Email Logs</h1>
        <p class="text-subtitle-1 text-medium-emphasis">Monitor email delivery and status</p>
      </div>
      <v-btn
        color="primary"
        size="large"
        prepend-icon="mdi-plus"
        @click="openFormModal()"
        class="text-none"
      >
        Add New Log
      </v-btn>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-md-4 col-6">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="primary" size="40" class="mr-3">mdi-email</v-icon>
            <div>
              <div class="text-h6">{{ stats.total }}</div>
              <div class="text-caption text-medium-emphasis">Total Emails</div>
            </div>
          </div>
        </v-card>
      </div>
      <div class="col-md-4 col-6">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="success" size="40" class="mr-3">mdi-check-circle</v-icon>
            <div>
              <div class="text-h6">{{ stats.success }}</div>
              <div class="text-caption text-medium-emphasis">Success</div>
            </div>
          </div>
        </v-card>
      </div>
      <div class="col-md-4 col-6">
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
          <div class="col-md-4">
            <v-text-field
              v-model="search"
              label="Search emails..."
              prepend-inner-icon="mdi-magnify"
              clearable
              hide-details
              @input="debouncedSearch"
            />
          </div>
          <div class="col-md-3">
            <v-select
              v-model="filters.status"
              :items="statusOptions"
              label="Status"
              clearable
              hide-details
              @update:model-value="applyFilters"
            />
          </div>
          <div class="col-md-3">
            <v-text-field
              v-model="filters.sender"
              label="Sender"
              clearable
              hide-details
              @input="applyFilters"
            />
          </div>
          <div class="col-md-2">
            <v-btn
              color="primary"
              variant="outlined"
              @click="clearFilters"
              class="mt-1"
            >
              Clear Filters
            </v-btn>
          </div>
        </div>
      </v-card-text>
    </v-card>

    <!-- Data Table -->
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span>Email Logs ({{ pagination.total }})</span>
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
        <template #item.subject="{ item }">
          <div class="text-truncate" style="max-width: 300px;">
            {{ item.subject }}
          </div>
        </template>

        <template #item.recipients="{ item }">
          <div class="text-truncate" style="max-width: 200px;">
            {{ item.recipients }}
          </div>
        </template>

        <template #item.sender="{ item }">
          <div class="text-body-2">{{ item.sender }}</div>
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
          <span>{{ formData.name ? 'Edit' : 'Add' }} Email Log</span>
          <v-btn icon="mdi-close" variant="text" @click="closeFormModal" />
        </v-card-title>
        
        <v-card-text>
          <v-form ref="form" v-model="formValid">
            <div class="row">
              <div class="col-12">
                <v-text-field
                  v-model="formData.subject"
                  label="Subject *"
                  :rules="[v => !!v || 'Subject is required']"
                  required
                />
              </div>
              <div class="col-md-6">
                <v-textarea
                  v-model="formData.recipients"
                  label="Recipients *"
                  :rules="[v => !!v || 'Recipients is required']"
                  rows="2"
                  required
                  hint="Separate multiple emails with commas"
                />
              </div>
              <div class="col-md-6">
                <v-text-field
                  v-model="formData.sender"
                  label="Sender *"
                  type="email"
                  :rules="[v => !!v || 'Sender is required']"
                  required
                />
              </div>
              <div class="col-md-6">
                <v-textarea
                  v-model="formData.cc"
                  label="CC"
                  rows="2"
                  hint="Separate multiple emails with commas"
                />
              </div>
              <div class="col-md-6">
                <v-textarea
                  v-model="formData.bcc"
                  label="BCC"
                  rows="2"
                  hint="Separate multiple emails with commas"
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
                <v-textarea
                  v-model="formData.attachments"
                  label="Attachments"
                  rows="2"
                  hint="List of attachment file paths"
                />
              </div>
              <div class="col-12">
                <v-textarea
                  v-model="formData.content"
                  label="Content *"
                  rows="8"
                  no-resize
                  :rules="[v => !!v || 'Content is required']"
                  required
                />
              </div>
              <div class="col-12" v-if="formData.status === 'Failed'">
                <v-textarea
                  v-model="formData.error"
                  label="Error Details"
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
          Are you sure you want to delete this email log?
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

    <!-- Detail Modal -->
    <v-dialog v-model="showDetailModal" max-width="900px">
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center">
          <span>Email Log Details</span>
          <v-btn icon="mdi-close" variant="text" @click="showDetailModal = false" />
        </v-card-title>
        
        <v-card-text v-if="selectedItem">
          <div class="row">
            <div class="col-md-6">
              <v-list>
                <v-list-item>
                  <v-list-item-title>Subject</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedItem.subject }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>Recipients</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedItem.recipients }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>Sender</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedItem.sender }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>Status</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip :color="getStatusColor(selectedItem.status)" size="small">
                      {{ selectedItem.status }}
                    </v-chip>
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </div>
            <div class="col-md-6">
              <v-list>
                <v-list-item v-if="selectedItem.cc">
                  <v-list-item-title>CC</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedItem.cc }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item v-if="selectedItem.bcc">
                  <v-list-item-title>BCC</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedItem.bcc }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item v-if="selectedItem.attachments">
                  <v-list-item-title>Attachments</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedItem.attachments }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>Modified</v-list-item-title>
                  <v-list-item-subtitle>{{ formatDate(selectedItem.modified) }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </div>
            <div class="col-12">
              <v-divider class="my-4" />
              <h3 class="mb-3">Content</h3>
              <div class="bg-grey-lighten-4 pa-3 rounded" style="white-space: pre-wrap;">{{ selectedItem.content }}</div>
            </div>
            <div class="col-12" v-if="selectedItem.error && selectedItem.status === 'Failed'">
              <v-divider class="my-4" />
              <h3 class="mb-3 text-error">Error Details</h3>
              <div class="bg-red-lighten-5 pa-3 rounded" style="white-space: pre-wrap;">{{ selectedItem.error }}</div>
            </div>
          </div>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" @click="showDetailModal = false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { emailLogService } from '../services/universalService'
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
const showDetailModal = ref(false)
const formValid = ref(false)
const itemToDelete = ref(null)
const selectedItem = ref(null)

// Status options - matching EmailLog doctype
const statusOptions = [
  { title: 'Success', value: 'Success' },
  { title: 'Failed', value: 'Failed' },
  { title: 'Fallback', value: 'Fallback' }
]

// Form data - matching EmailLog doctype fields
const formData = reactive({
  name: '',
  subject: '',
  recipients: '',
  cc: '',
  bcc: '',
  sender: '',
  content: '',
  attachments: '',
  status: 'Success',
  error: ''
})

// Filters
const filters = reactive({
  status: '',
  sender: ''
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
  success: 0,
  failed: 0
})

// Table headers - matching EmailLog doctype fields
const headers = [
  { title: 'Subject', key: 'subject', sortable: false },
  { title: 'Recipients', key: 'recipients', sortable: false },
  { title: 'Sender', key: 'sender', sortable: false },
  { title: 'Status', key: 'status', sortable: false },
  { title: 'Modified', key: 'modified', sortable: false },
  { title: 'Actions', key: 'actions', sortable: false, width: '120px' }
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
      searchConditions.push(['recipients', 'like', `%${search.value}%`])
      searchConditions.push(['sender', 'like', `%${search.value}%`])
    }
    
    const params = {
      filters: apiFilters,
      page_length: pagination.limit,
      start: (pagination.page - 1) * pagination.limit,
      order_by: 'modified desc',
      fields: ['name', 'subject', 'recipients', 'cc', 'bcc', 'sender', 'content', 'attachments', 'status', 'error', 'modified']
    }
    
    // Add search conditions if any
    if (searchConditions.length > 0) {
      params.filters.search_text = searchConditions
    }

    const result = await emailLogService.getList(params)
    
    if (result.success) {
      items.value = result.data || []
      Object.assign(pagination, result.pagination)
      
      // Update stats
      stats.total = result.pagination.total || 0
      stats.success = result.data?.filter(item => item.status === 'Success').length || 0
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
    formData.status = 'Success'
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
    const result = await emailLogService.save(formData, formData.name)
    
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
  selectedItem.value = item
  showDetailModal.value = true
}

const confirmDelete = (item) => {
  itemToDelete.value = item
  showDeleteDialog.value = true
}

const deleteItem = async () => {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    const result = await emailLogService.delete(itemToDelete.value.name)
    
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

  const confirmed = confirm(`Are you sure you want to delete ${selected.value.length} email logs?`)
  if (!confirmed) return

  try {
    await Promise.all(
      selected.value.map(name => emailLogService.delete(name))
    )
    selected.value = []
    loadData()
  } catch (error) {
    console.error('Error bulk deleting:', error)
  }
}

const exportData = () => {
  const data = items.value.map(item => ({
    Subject: item.subject,
    Recipients: item.recipients,
    Sender: item.sender,
    Status: item.status,
    Modified: formatDate(item.modified)
  }))

  const csv = [
    Object.keys(data[0]).join(','),
    ...data.map(row => Object.values(row).join(','))
  ].join('\n')

  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'email-logs.csv'
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
    'Success': 'success',
    'Failed': 'error',
    'Fallback': 'warning'
  }
  return colors[status] || 'grey'
}

const getStatusIcon = (status) => {
  const icons = {
    'Success': 'mdi-check-circle',
    'Failed': 'mdi-alert-circle',
    'Fallback': 'mdi-backup-restore'
  }
  return icons[status] || 'mdi-help-circle'
}

// Lifecycle
onMounted(async () => {
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
