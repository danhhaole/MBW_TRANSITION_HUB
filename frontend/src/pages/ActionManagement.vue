<template>
  <div class="min-h-screen bg-gray-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header>
        <Button
          variant="solid"
          @click="openFormModal()"
        >
          <template #prefix>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
          </template>
          {{ __('Add New Action') }}
        </Button>
      </template>
    </LayoutHeader>

    <div class="min-h-screen container mx-auto bg-slate-50 p-4 md:p-6">


      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <div class="text-2xl font-bold text-slate-800">{{ stats.total }}</div>
              <div class="text-sm text-slate-500">{{ __('Total Actions') }}</div>
            </div>
          </div>
        </div>
        <div class="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center mr-3">
              <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <div class="text-2xl font-bold text-slate-800">{{ stats.executed }}</div>
              <div class="text-sm text-slate-500">{{ __('Executed') }}</div>
            </div>
          </div>
        </div>
        <div class="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-yellow-100 rounded-full flex items-center justify-center mr-3">
              <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <div class="text-2xl font-bold text-slate-800">{{ stats.scheduled }}</div>
              <div class="text-sm text-slate-500">{{ __('Scheduled') }}</div>
            </div>
          </div>
        </div>
        <div class="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center mr-3">
              <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <div class="text-2xl font-bold text-slate-800">{{ stats.failed }}</div>
              <div class="text-sm text-slate-500">{{ __('Failed') }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Compact Filters -->
      <div class="bg-white border border-slate-200 rounded-lg mb-6">
        <div class="p-4">
          <div class="flex gap-3 items-center">
            <FormControl
              type="text"
              v-model="search"
              :placeholder="__('Search actions...')"
              class="flex-1"
              @update:model-value="debouncedSearch"
            >
              <template #prefix>
                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </template>
            </FormControl>
            <Button
              variant="outline"
              @click="showAdvancedFilters = !showAdvancedFilters"
            >
              <template #prefix>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                </svg>
              </template>
              {{ __('Advanced Filters') }}
              <template #suffix>
                <svg v-if="showAdvancedFilters" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                </svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </template>
            </Button>
            <Button
              variant="outline"
              @click="handleRefresh"
              :loading="loading"
            >
              <template #prefix>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-4 h-4"
                  :class="{ 'animate-spin': loading }"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
              </template>
              {{ __('Refresh') }}
            </Button>
            <Button
              v-if="hasActiveFilters"
              variant="ghost"
              @click="clearFilters"
            >
              <template #prefix>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </template>
              {{ __('Clear') }}
            </Button>
          </div>
          
          <!-- Advanced Filters (Collapsible) -->
          <div v-if="showAdvancedFilters" class="mt-4 pt-4 border-t border-slate-200">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
              <FormControl
                type="select"
                v-model="filters.status"
                :options="statusOptions"
                :placeholder="__('Status')"
                @change="applyFilters"
              />
              <FormControl
                type="select"
                v-model="filters.campaign_step"
                :options="filterOptions.campaignSteps"
                :placeholder="__('Campaign Step')"
                @change="applyFilters"
              />
              <FormControl
                type="select"
                v-model="filters.talent_campaign_id"
                :options="filterOptions.candidateCampaigns"
                :placeholder="__('Candidate Campaign')"
                @change="applyFilters"
              />
              <FormControl
                type="select"
                v-model="filters.assignee_id"
                :options="filterOptions.assignees"
                :placeholder="__('Assignee')"
                @change="applyFilters"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Data Table -->
      <div class="bg-white border border-slate-200 rounded-lg">
        <Loading v-if="loading" text="Loading actions..." />
        <div class="overflow-x-auto" v-else>
          <table class="w-full">
            <thead class="bg-slate-50 border-b border-slate-200">
              <tr>
                <th class="w-12 p-3">
                  <input
                    type="checkbox"
                    class="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                    :checked="selected.length === items.length && items.length > 0"
                    :indeterminate="selected.length > 0 && selected.length < items.length"
                    @change="toggleSelectAll"
                  />
                </th>
                <th class="text-left p-3 text-sm font-medium text-slate-600">{{ __('Candidate Campaign') }}</th>
                <th class="text-left p-3 text-sm font-medium text-slate-600">{{ __('Campaign Step') }}</th>
                <th class="text-left p-3 text-sm font-medium text-slate-600">{{ __('Status') }}</th>
                <th class="text-left p-3 text-sm font-medium text-slate-600">{{ __('Scheduled At') }}</th>
                <th class="text-left p-3 text-sm font-medium text-slate-600">{{ __('Executed At') }}</th>
                <th class="text-left p-3 text-sm font-medium text-slate-600">{{ __('Assignee') }}</th>
                <th class="text-left p-3 text-sm font-medium text-slate-600">{{ __('Actions') }}</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-200">
              <tr v-if="loading" v-for="i in 5" :key="i" class="animate-pulse">
                <td class="p-3"><div class="w-4 h-4 bg-slate-200 rounded"></div></td>
                <td class="p-3"><div class="h-4 bg-slate-200 rounded w-32"></div></td>
                <td class="p-3"><div class="h-4 bg-slate-200 rounded w-24"></div></td>
                <td class="p-3"><div class="h-4 bg-slate-200 rounded w-20"></div></td>
                <td class="p-3"><div class="h-4 bg-slate-200 rounded w-28"></div></td>
                <td class="p-3"><div class="h-4 bg-slate-200 rounded w-28"></div></td>
                <td class="p-3"><div class="h-4 bg-slate-200 rounded w-24"></div></td>
                <td class="p-3"><div class="h-4 bg-slate-200 rounded w-20"></div></td>
              </tr>
              <tr v-else-if="items.length === 0" class="text-center">
                <td colspan="8" class="p-8 text-slate-500">
                  <div class="flex flex-col items-center">
                    <svg class="w-12 h-12 text-slate-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    <span>{{ __('No actions found') }}</span>
                  </div>
                </td>
              </tr>
              <tr
                v-else
                v-for="item in items"
                :key="item.name"
                class="hover:bg-slate-50 transition-colors"
                :class="{ 'bg-blue-50': selected.includes(item) }"
              >
                <td class="p-3 text-center">
                  <input
                    type="checkbox"
                    class="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                    :checked="selected.includes(item)"
                    @change="toggleSelect(item)"
                  />
                </td>
                <td class="p-3">
                  <Badge
                    variant="outline"
                    theme="blue"
                    size="sm"
                  >
                    {{ item.talent_campaign_id }}
                  </Badge>
                </td>
                <td class="p-3">
                  <Badge
                    variant="outline"
                    theme="purple"
                    size="sm"
                  >
                    {{ item.campaign_step }}
                  </Badge>
                </td>
                <td class="p-3">
                  <Badge
                    :variant="'subtle'"
                    :theme="getStatusColor(item.status)"
                    size="md"
                  >
                    {{ item.status }}
                  </Badge>
                </td>
                <td class="p-3">
                  <div class="text-sm text-slate-600">
                    {{ formatDate(item.scheduled_at) }}
                  </div>
                </td>
                <td class="p-3">
                  <div class="text-sm text-slate-600">
                    {{ formatDate(item.executed_at) }}
                  </div>
                </td>
                <td class="p-3">
                  <Badge
                    v-if="item.assignee_id"
                    variant="outline"
                    theme="gray"
                    size="sm"
                  >
                    {{ item.assignee_id }}
                  </Badge>
                  <span v-else class="text-slate-400 text-sm">-</span>
                </td>
                <td class="p-3">
                  <div class="flex items-center gap-1">
                    <Button
                      v-if="item.status === 'SCHEDULED' || item.status === 'FAILED'"
                      variant="ghost"
                      theme="green"
                      size="sm"
                      @click="executeAction(item)"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h.01M19 10a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      @click="openFormModal(item)"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                      </svg>
                    </Button>
                    <Button
                      variant="ghost"
                      theme="red"
                      size="sm"
                      @click="confirmDelete(item)"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </Button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="!loading && items.length > 0" class="flex justify-between items-center p-4 border-t border-slate-200">
          <div class="text-sm text-slate-600">
            {{ __('Showing') }} {{ ((pagination.page - 1) * pagination.limit) + 1 }} {{ __('to') }} {{ Math.min(pagination.page * pagination.limit, pagination.total) }} {{ __('of') }} {{ pagination.total }} {{ __('results') }}
          </div>
          <div class="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              :disabled="pagination.page <= 1"
              @click="pagination.page--; loadData()"
            >
              {{ __('Previous') }}
            </Button>
            <span class="text-sm text-slate-600">
              {{ __('Page') }} {{ pagination.page }} {{ __('of') }} {{ Math.ceil(pagination.total / pagination.limit) }}
            </span>
            <Button
              variant="outline"
              size="sm"
              :disabled="pagination.page >= Math.ceil(pagination.total / pagination.limit)"
              @click="pagination.page++; loadData()"
            >
              {{ __('Next') }}
            </Button>
          </div>
        </div>
      </div>

      <!-- Form Modal -->
      <Dialog v-model="showFormModal" :options="{ title: formData.name ? __('Edit Action') : __('Add New Action'), size: 'xl' }">
        <template #body-content>
          <div class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormControl
                type="select"
                :label="__('Candidate Campaign')"
                v-model="formData.talent_campaign_id"
                :options="filterOptions.candidateCampaigns"
                :required="true"
              />
              <FormControl
                type="select"
                :label="__('Campaign Step')"
                v-model="formData.campaign_step"
                :options="filterOptions.campaignSteps"
                :required="true"
              />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormControl
                type="select"
                :label="__('Status')"
                v-model="formData.status"
                :options="statusOptions"
                :required="true"
              />
              <FormControl
                type="select"
                :label="__('Assignee')"
                v-model="formData.assignee_id"
                :options="filterOptions.assignees"
              />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormControl
                type="datetime-local"
                :label="__('Scheduled At')"
                v-model="formData.scheduled_at"
              />
              <FormControl
                type="datetime-local"
                :label="__('Executed At')"
                v-model="formData.executed_at"
              />
            </div>

            <FormControl
              type="textarea"
              :label="__('Result (JSON)')"
              v-model="formData.result"
              :placeholder="__('Enter result data as JSON or leave empty...')"
              :rows="4"
              help="{{ __('Leave empty or enter valid JSON. Example: {key: value}') }}"
            />
          </div>
        </template>
        <template #actions>
          <Button variant="ghost" @click="closeFormModal">
            {{ __('Cancel') }}
          </Button>
          <Button variant="solid" :loading="saving" @click="saveData">
            {{ formData.name ? __('Update') : __('Create') }}
          </Button>
        </template>
      </Dialog>

      <!-- Delete Confirmation -->
      <Dialog v-model="showDeleteDialog" :options="{ title: 'Confirm Delete', size: 'sm' }">
        <template #body-content>
          <div class="text-center">
            <div class="w-12 h-12 mx-auto mb-4 bg-red-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.996-.833-2.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <p class="text-slate-600">
              Are you sure you want to delete this action? This action cannot be undone.
            </p>
          </div>
        </template>
        <template #actions>
          <Button variant="ghost" @click="showDeleteDialog = false">
            Cancel
          </Button>
          <Button variant="solid" theme="red" :loading="deleting" @click="deleteData">
            Delete
          </Button>
        </template>
      </Dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Button, Dialog, FormControl, Badge } from 'frappe-ui'
import { actionService, candidateCampaignService, userService } from '../services/universalService'
import { useCampaignStepStore } from '@/stores/campaignStep'
import { debounce } from 'lodash'
import { createResource, Breadcrumbs } from 'frappe-ui'
import { ToastContainer } from '@/components/shared'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Loading from '@/components/Loading.vue'

const router = useRouter()

// Campaign step store
const campaignStepStore = useCampaignStepStore()

// Translation helper


// Breadcrumbs
const breadcrumbs = [
  { label: __('Actions'), route: { name: 'ActionManagement' } }
]

// State
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const items = ref([])
const selected = ref([])
const search = ref('')
const showFormModal = ref(false)
const showDeleteDialog = ref(false)
const itemToDelete = ref(null)
const showAdvancedFilters = ref(false)

// Status options matching doctype
const statusOptions = [
  { label: 'Scheduled', value: 'SCHEDULED' },
  { label: 'Executed', value: 'EXECUTED' },
  { label: 'Skipped', value: 'SKIPPED' },
  { label: 'Failed', value: 'FAILED' },
  { label: 'Pending Manual', value: 'PENDING_MANUAL' }
]

// Form data matching doctype fields
const formData = reactive({
  name: '',
  talent_campaign_id: '',
  campaign_step: '',
  status: 'SCHEDULED',
  scheduled_at: null,
  executed_at: null,
  result: null,
  assignee_id: ''
})

// Filters
const filters = reactive({
  status: '',
  campaign_step: '',
  talent_campaign_id: '',
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
  { title: 'Candidate Campaign', key: 'talent_campaign_id', sortable: true },
  { title: 'Campaign Step', key: 'campaign_step', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Scheduled At', key: 'scheduled_at', sortable: true },
  { title: 'Executed At', key: 'executed_at', sortable: true },
  { title: 'Assignee', key: 'assignee_id', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false }
]

// Computed properties
const hasActiveFilters = computed(() => {
  return Object.values(filters).some(value => value && value !== '')
})

const formValid = computed(() => {
  return formData.talent_campaign_id && formData.campaign_step && formData.status
})

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
    let or_filters = undefined
    if (search.value && search.value.trim() !== '') {
      or_filters = [
        ['talent_campaign_id', 'like', `%${search.value}%`],
        ['campaign_step', 'like', `%${search.value}%`],
        ['assignee_id', 'like', `%${search.value}%`]
      ]
    }
    const params = {
      filters: apiFilters,
      or_filters,
      page_length: pagination.limit,
      start: (pagination.page - 1) * pagination.limit,
      order_by: 'scheduled_at desc',
      fields: ['name', 'talent_campaign_id', 'campaign_step', 'status', 'scheduled_at', 'executed_at', 'result', 'assignee_id', 'modified']
    }

    const result = await actionService.getList(params)
    if (result && Array.isArray(result.data)) {
      items.value = result.data
      Object.assign(pagination, result.pagination)
      // Update stats
      stats.total = result.pagination.total || 0
      stats.executed = result.data?.filter(item => item.status === 'EXECUTED').length || 0
      stats.scheduled = result.data?.filter(item => item.status === 'SCHEDULED').length || 0
      stats.failed = result.data?.filter(item => item.status === 'FAILED').length || 0
    } else {
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
      fields: ['name', 'talent_id', 'campaign_id'],
      page_length: 1000
    })
    if (candidateCampaignResult.success) {
      filterOptions.candidateCampaigns = candidateCampaignResult.data.map(item => ({
        label: `${item.name} (${item.talent_id} - ${item.campaign_id})`,
        value: item.name
      }))
    }
    
    // Load campaign steps
    const campaignStepResult = await campaignStepStore.getFilteredCampaignSteps({
      limit: 1000
    })
    if (campaignStepResult && campaignStepResult.data) {
      filterOptions.campaignSteps = campaignStepResult.data.map(item => ({
        label: `${item.campaign_step_name} (${item.campaign})`,
        value: item.name
      }))
    }
    
    // Load assignees (users)
    const userResult = await userService.getList({
      fields: ['name', 'full_name', 'email'],
      page_length: 1000
    })
    if (userResult.success) {
      filterOptions.assignees = userResult.data.map(item => ({
        label: `${item.full_name} (${item.email})`,
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

const handleRefresh = async () => {
  try {
    await loadData()
    // Show success message
    console.log('Data refreshed successfully')
  } catch (error) {
    console.error('Error refreshing data:', error)
  }
}

const toggleSelectAll = (event) => {
  if (event.target.checked) {
    selected.value = [...items.value]
  } else {
    selected.value = []
  }
}

const toggleSelect = (item) => {
  const index = selected.value.findIndex(s => s.name === item.name)
  if (index > -1) {
    selected.value.splice(index, 1)
  } else {
    selected.value.push(item)
  }
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
    talent_campaign_id: '',
    campaign_step: '',
    status: 'SCHEDULED',
    scheduled_at: null,
    executed_at: null,
    result: null,
    assignee_id: ''
  })
}

const saveData = async () => {
  // Validate required fields
  if (!formData.talent_campaign_id) {
    alert('Please select a candidate campaign')
    return
  }
  if (!formData.campaign_step) {
    alert('Please select a campaign step')
    return
  }
  if (!formData.status) {
    alert('Please select a status')
    return
  }

  saving.value = true
  try {
    // Prepare data for saving
    const dataToSave = { ...formData }
    
    // Handle JSON field - convert empty string to null or valid JSON
    if (dataToSave.result === '' || dataToSave.result === null) {
      dataToSave.result = null
    } else if (typeof dataToSave.result === 'string') {
      try {
        // Try to parse as JSON to validate
        JSON.parse(dataToSave.result)
      } catch (e) {
        alert('Result field must be valid JSON or left empty')
        return
      }
    }

    const result = await actionService.save(dataToSave)
    if (result.success) {
      closeFormModal()
      loadData()
    } else {
      console.error('Error saving data:', result.error)
      alert('Error saving action: ' + (result.error || 'Unknown error'))
    }
  } catch (error) {
    console.error('Error saving data:', error)
    alert('Error saving action: ' + (error.message || 'Unknown error'))
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
      itemToDelete.value = null
      loadData()
    } else {
      console.error('Error deleting data:', result.error)
      alert('Error deleting action: ' + (result.error || 'Unknown error'))
    }
  } catch (error) {
    console.error('Error deleting data:', error)
    alert('Error deleting action: ' + (error.message || 'Unknown error'))
  } finally {
    deleting.value = false
  }
}

const executeAction = async (item) => {
  try {
    // Create resource for updating Action
    const updateResource = createResource({
      url: 'frappe.client.set_value',
      method: 'POST'
    })
    
    // Update status to EXECUTED
    await updateResource.submit({
      doctype: 'Action',
      name: item.name,
      fieldname: 'status',
      value: 'EXECUTED'
    })
    
    // Set executed_at timestamp
    await updateResource.submit({
      doctype: 'Action',
      name: item.name,
      fieldname: 'executed_at',
      value: new Date().toISOString()
    })
    
    // Reload data to reflect changes
    loadData()
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
      fields: ['name', 'talent_campaign_id', 'campaign_step', 'status', 'scheduled_at', 'executed_at', 'result', 'assignee_id']
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
    case 'SCHEDULED': return 'blue'
    case 'EXECUTED': return 'green'
    case 'SKIPPED': return 'orange'
    case 'FAILED': return 'red'
    case 'PENDING_MANUAL': return 'purple'
    default: return 'gray'
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
/* Custom scrollbar for table */
.overflow-x-auto::-webkit-scrollbar {
  height: 8px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Animation for loading skeleton */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Transition for hover effects */
.transition-colors {
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

.transition-shadow {
  transition-property: box-shadow;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Custom checkbox styling */
input[type="checkbox"]:indeterminate {
  background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='M4 8h8'/%3e%3c/svg%3e");
}
</style>
