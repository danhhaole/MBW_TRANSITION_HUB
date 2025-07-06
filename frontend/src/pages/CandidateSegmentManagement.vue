<template>
  <div class="pa-4">
    <!-- Header -->
    <div class="d-flex justify-space-between align-center mb-4">
      <div>
        <h1 class="text-h4 font-weight-bold">Candidate Segments</h1>
        <p class="text-subtitle-1 text-medium-emphasis">Manage candidate segment assignments</p>
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
      <div class="col-md-3 col-6">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="primary" size="40" class="mr-3">mdi-account-group</v-icon>
            <div>
              <div class="text-h6">{{ stats.total }}</div>
              <div class="text-caption text-medium-emphasis">Total Segments</div>
            </div>
          </div>
        </v-card>
      </div>
      <div class="col-md-3 col-6">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="success" size="40" class="mr-3">mdi-account-check</v-icon>
            <div>
              <div class="text-h6">{{ stats.active }}</div>
              <div class="text-caption text-medium-emphasis">Active</div>
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
              <div class="text-caption text-medium-emphasis">Added Today</div>
            </div>
          </div>
        </v-card>
      </div>
      <div class="col-md-3 col-6">
        <v-card class="pa-3">
          <div class="d-flex align-center">
            <v-icon color="warning" size="40" class="mr-3">mdi-calendar-week</v-icon>
            <div>
              <div class="text-h6">{{ stats.week }}</div>
              <div class="text-caption text-medium-emphasis">This Week</div>
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
              label="Search segments..."
              prepend-inner-icon="mdi-magnify"
              clearable
              hide-details
              @input="debouncedSearch"
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
              v-model="filters.segment_id"
              :items="filterOptions.segments"
              label="Segment"
              clearable
              hide-details
              @update:model-value="applyFilters"
            />
          </div>
          <div class="col-md-2">
            <v-select
              v-model="filters.added_by"
              :items="filterOptions.users"
              label="Added By"
              clearable
              hide-details
              @update:model-value="applyFilters"
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
        <span>Candidate Segments ({{ pagination.total }})</span>
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
        <template #item.candidate_id="{ item }">
          <div class="d-flex align-center">
            <v-avatar size="32" color="primary" class="mr-2">
              <span class="text-caption">{{ item.candidate_id?.charAt(0) }}</span>
            </v-avatar>
            <span>{{ item.candidate_id }}</span>
          </div>
        </template>

        <template #item.segment_id="{ item }">
          <v-chip
            :color="getSegmentColor(item.segment_id)"
            variant="tonal"
            size="small"
          >
            {{ item.segment_id }}
          </v-chip>
        </template>

        <template #item.added_at="{ item }">
          {{ formatDate(item.added_at) }}
        </template>

        <template #item.actions="{ item }">
          <div class="d-flex align-center">
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
    <v-dialog v-model="showFormModal" max-width="600px" persistent>
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center">
          <span>{{ formData.name ? 'Edit' : 'Add' }} Candidate Segment</span>
          <v-btn icon="mdi-close" variant="text" @click="closeFormModal" />
        </v-card-title>
        
        <v-card-text>
          <v-form ref="form" v-model="formValid">
            <div class="row">
              <div class="col-12">
                <v-select
                  v-model="formData.candidate_id"
                  :items="filterOptions.candidates"
                  label="Candidate *"
                  :rules="[v => !!v || 'Candidate is required']"
                  required
                />
              </div>
              <div class="col-12">
                <v-select
                  v-model="formData.segment_id"
                  :items="filterOptions.segments"
                  label="Segment *"
                  :rules="[v => !!v || 'Segment is required']"
                  required
                />
              </div>
              <div class="col-12">
                <v-text-field
                  v-model="formData.added_by"
                  label="Added By"
                  readonly
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
          Are you sure you want to delete this candidate segment?
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { candidateSegmentService, candidateService, talentSegmentService } from '../services/universalService'
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

// Form data
const formData = reactive({
  name: '',
  candidate_id: '',
  segment_id: '',
  added_by: '',
  added_at: ''
})

// Filters
const filters = reactive({
  candidate_id: '',
  segment_id: '',
  added_by: ''
})

// Filter options
const filterOptions = reactive({
  candidates: [],
  segments: [],
  users: []
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
  today: 0,
  week: 0
})

// Table headers
const headers = [
  { title: 'Candidate', key: 'candidate_id', sortable: false },
  { title: 'Segment', key: 'segment_id', sortable: false },
  { title: 'Added At', key: 'added_at', sortable: false },
  { title: 'Added By', key: 'added_by', sortable: false },
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
      searchConditions.push(['candidate_id', 'like', `%${search.value}%`])
      searchConditions.push(['segment_id', 'like', `%${search.value}%`])
    }
    
    const params = {
      filters: apiFilters,
      page_length: pagination.limit,
      start: (pagination.page - 1) * pagination.limit,
      order_by: 'modified desc',
      fields: ['name', 'candidate_id', 'segment_id', 'added_at', 'added_by', 'modified']
    }
    
    // Add search conditions if any
    if (searchConditions.length > 0) {
      params.filters.search_text = searchConditions
    }

    const result = await candidateSegmentService.getList(params)
    
    if (result.success) {
      items.value = result.data || []
      Object.assign(pagination, result.pagination)
      
      // Update stats
      stats.total = result.pagination.total || 0
      stats.active = result.data?.length || 0
      stats.today = result.data?.filter(item => 
        new Date(item.added_at).toDateString() === new Date().toDateString()
      ).length || 0
      stats.week = result.data?.filter(item => {
        const itemDate = new Date(item.added_at)
        const weekAgo = new Date()
        weekAgo.setDate(weekAgo.getDate() - 7)
        return itemDate >= weekAgo
      }).length || 0
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

    // Load segments
    const segmentsResult = await talentSegmentService.getList({ 
      fields: ['name', 'segment_name'],
      page_length: 1000,
      filters: {}
    })
    if (segmentsResult.success) {
      filterOptions.segments = segmentsResult.data.map(item => ({
        title: item.segment_name || item.name,
        value: item.name
      }))
    }

    // Load users from filter options
    const usersResult = await candidateSegmentService.getFilterOptions('added_by')
    if (usersResult.success) {
      filterOptions.users = usersResult.options.map(option => ({
        title: option.label || option.value,
        value: option.value
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
    formData.added_by = 'Administrator' // Default user
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
    const result = await candidateSegmentService.save(formData, formData.name)
    
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

const confirmDelete = (item) => {
  itemToDelete.value = item
  showDeleteDialog.value = true
}

const deleteItem = async () => {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    const result = await candidateSegmentService.delete(itemToDelete.value.name)
    
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

  const confirmed = confirm(`Are you sure you want to delete ${selected.value.length} items?`)
  if (!confirmed) return

  try {
    await Promise.all(
      selected.value.map(name => candidateSegmentService.delete(name))
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
    Segment: item.segment_id,
    'Added At': formatDate(item.added_at),
    'Added By': item.added_by
  }))

  const csv = [
    Object.keys(data[0]).join(','),
    ...data.map(row => Object.values(row).join(','))
  ].join('\n')

  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'candidate-segments.csv'
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

const getSegmentColor = (segment) => {
  const colors = ['primary', 'secondary', 'success', 'info', 'warning', 'error']
  const index = segment?.length % colors.length || 0
  return colors[index]
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

.stats-card {
  transition: transform 0.2s;
}

.stats-card:hover {
  transform: translateY(-2px);
}
</style>
