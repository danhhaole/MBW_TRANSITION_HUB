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
          {{ __('Add New Mira Interaction') }}
        </Button>
      </template>
    </LayoutHeader>

    <div class="min-h-screen container mx-auto bg-slate-50 p-4 md:p-6">
      <!-- Header -->


      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <div>
              <div class="text-2xl font-bold text-slate-800">{{ stats.total }}</div>
              <div class="text-sm text-slate-500">{{ __('Total Interactions') }}</div>
            </div>
          </div>
        </div>
        <div class="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center mr-3">
              <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <div class="text-2xl font-bold text-slate-800">{{ stats.emails }}</div>
              <div class="text-sm text-slate-500">{{ __('Email Interactions') }}</div>
            </div>
          </div>
        </div>
        <div class="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-yellow-100 rounded-full flex items-center justify-center mr-3">
              <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
            </div>
            <div>
              <div class="text-2xl font-bold text-slate-800">{{ stats.calls }}</div>
              <div class="text-sm text-slate-500">{{ __('Call Interactions') }}</div>
            </div>
          </div>
        </div>
        <div class="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <div class="text-2xl font-bold text-slate-800">{{ stats.today }}</div>
              <div class="text-sm text-slate-500">{{ __('Today') }}</div>
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
              placeholder="Search interactions..."
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
              Advanced Filters
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
              Clear
            </Button>
          </div>
          
          <!-- Advanced Filters (Collapsible) -->
          <div v-if="showAdvancedFilters" class="mt-4 pt-4 border-t border-slate-200">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
              <FormControl
                type="select"
                v-model="filters.interaction_type"
                :options="interactionTypeOptions"
                placeholder="Type"
                @change="applyFilters"
              />
              <FormControl
                type="select"
                v-model="filters.talent_id"
                :options="filterOptions.candidates"
                placeholder="Candidate"
                @change="applyFilters"
              />
              <FormControl
                type="select"
                v-model="filters.action"
                :options="filterOptions.actions"
                placeholder="Source Action"
                @change="applyFilters"
              />
              <FormControl
                type="text"
                v-model="filters.url"
                placeholder="URL"
                @update:model-value="applyFilters"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Data Table -->
      <div class="bg-white border border-slate-200 rounded-lg">
        <div class="flex justify-between items-center p-4 border-b border-slate-200">
          <span class="text-lg font-semibold text-slate-800">Interactions ({{ pagination.total }})</span>
          <div class="flex gap-2">
            <Button
              v-if="selected.length > 0"
              variant="outline"
              theme="red"
              @click="bulkDelete"
            >
              <template #prefix>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </template>
              Delete Selected ({{ selected.length }})
            </Button>
            <Button
              variant="outline"
              @click="exportData"
            >
              <template #prefix>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </template>
              Export
            </Button>
          </div>
        </div>

        <!-- Table Content -->
        <Loading v-if="loading" text="Loading interactions..." />
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
                <th class="text-left p-3 text-sm font-medium text-slate-600">Candidate</th>
                <th class="text-left p-3 text-sm font-medium text-slate-600">Type</th>
                <th class="text-left p-3 text-sm font-medium text-slate-600">Source Action</th>
                <th class="text-left p-3 text-sm font-medium text-slate-600">URL</th>
                <th class="text-left p-3 text-sm font-medium text-slate-600">Description</th>
                <th class="text-left p-3 text-sm font-medium text-slate-600">Modified</th>
                <th class="text-left p-3 text-sm font-medium text-slate-600">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-200">
              <tr v-if="loading" v-for="i in 5" :key="i" class="animate-pulse">
                <td class="p-3"><div class="w-4 h-4 bg-slate-200 rounded"></div></td>
                <td class="p-3"><div class="h-4 bg-slate-200 rounded w-32"></div></td>
                <td class="p-3"><div class="h-4 bg-slate-200 rounded w-20"></div></td>
                <td class="p-3"><div class="h-4 bg-slate-200 rounded w-24"></div></td>
                <td class="p-3"><div class="h-4 bg-slate-200 rounded w-16"></div></td>
                <td class="p-3"><div class="h-4 bg-slate-200 rounded w-40"></div></td>
                <td class="p-3"><div class="h-4 bg-slate-200 rounded w-24"></div></td>
                <td class="p-3"><div class="h-4 bg-slate-200 rounded w-20"></div></td>
              </tr>
              <tr v-else-if="items.length === 0" class="text-center">
                <td colspan="8" class="p-8 text-slate-500">
                  <div class="flex flex-col items-center">
                    <svg class="w-12 h-12 text-slate-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                    </svg>
                    <span>No interactions found</span>
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
                  <div class="flex items-center">
                    <Avatar
                      :label="item.talent_id?.charAt(0)"
                      size="sm"
                      class="mr-2"
                    />
                    <span class="text-sm text-slate-800">{{ item.talent_id }}</span>
                  </div>
                </td>
                <td class="p-3">
                  <Badge
                    :variant="'subtle'"
                    :theme="getInteractionTypeColor(item.interaction_type)"
                    size="md"
                  >
                    {{ item.interaction_type }}
                  </Badge>
                </td>
                <td class="p-3">
                  <Badge
                    v-if="item.action"
                    variant="outline"
                    theme="gray"
                    size="sm"
                  >
                    {{ item.action }}
                  </Badge>
                  <span v-else class="text-slate-400 text-sm">-</span>
                </td>
                <td class="p-3">
                  <Button
                    v-if="item.url"
                    variant="ghost"
                    size="sm"
                    :link="item.url"
                    target="_blank"
                  >
                    <template #prefix>
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                    </template>
                    Link
                  </Button>
                  <span v-else class="text-slate-400 text-sm">-</span>
                </td>
                <td class="p-3">
                  <div
                    class="text-sm text-slate-600 max-w-xs truncate"
                    :title="item.description || 'No description'"
                  >
                    {{ item.description || '-' }}
                  </div>
                </td>
                <td class="p-3">
                  <div class="text-sm text-slate-600">
                    {{ formatDate(item.modified) }}
                  </div>
                </td>
                <td class="p-3">
                  <div class="flex items-center gap-1">
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
            Showing {{ ((pagination.page - 1) * pagination.limit) + 1 }} to {{ Math.min(pagination.page * pagination.limit, pagination.total) }} of {{ pagination.total }} results
          </div>
          <div class="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              :disabled="pagination.page <= 1"
              @click="pagination.page--; loadData()"
            >
              Previous
            </Button>
            <span class="text-sm text-slate-600">
              Page {{ pagination.page }} of {{ Math.ceil(pagination.total / pagination.limit) }}
            </span>
            <Button
              variant="outline"
              size="sm"
              :disabled="pagination.page >= Math.ceil(pagination.total / pagination.limit)"
              @click="pagination.page++; loadData()"
            >
              Next
            </Button>
          </div>
        </div>
      </div>

      <!-- Form Modal -->
      <Dialog v-model="showFormModal" :options="{ title: formData.name ? 'Edit Mira Interaction' : 'Add New Mira Interaction', size: 'xl' }">
        <template #body-content>
          <div class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormControl
                type="select"
                label="Candidate"
                v-model="formData.talent_id"
                :options="filterOptions.candidates"
                :required="true"
              />
              <FormControl
                type="select"
                label="Mira Interaction Type"
                v-model="formData.interaction_type"
                :options="interactionTypeOptions"
                :required="true"
              />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormControl
                type="select"
                label="Source Action"
                v-model="formData.action"
                :options="filterOptions.actions"
              />
              <FormControl
                type="text"
                label="URL"
                v-model="formData.url"
                placeholder="https://example.com/page"
              />
            </div>

            <FormControl
              type="textarea"
              label="Description"
              v-model="formData.description"
              placeholder="Enter detailed description of the interaction..."
              :rows="4"
            />
          </div>
        </template>
        <template #actions>
          <Button variant="ghost" @click="closeFormModal">
            Cancel
          </Button>
          <Button variant="solid" :loading="saving" @click="saveData">
            {{ formData.name ? 'Update' : 'Create' }}
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
              Are you sure you want to delete this interaction? This action cannot be undone.
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
import { Button, Dialog, FormControl, Avatar, Badge, Breadcrumbs } from 'frappe-ui'
import { interactionService, candidateService, actionService } from 'frappe-ui'
import { debounce } from 'lodash'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Loading from '@/components/Loading.vue'



// Breadcrumbs
const breadcrumbs = [
  { label: __('Interactions'), route: { name: 'InteractionManagement' } }
]

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
const itemToDelete = ref(null)
const showAdvancedFilters = ref(false)

// Mira Interaction type options matching doctype
const interactionTypeOptions = [
  { label: 'Email Sent', value: 'EMAIL_SENT' },
  { label: 'Email Delivered', value: 'EMAIL_DELIVERED' },
  { label: 'Email Bounced', value: 'EMAIL_BOUNCED' },
  { label: 'Email Opened', value: 'EMAIL_OPENED' },
  { label: 'Email Clicked', value: 'EMAIL_CLICKED' },
  { label: 'Email Unsubscribed', value: 'EMAIL_UNSUBSCRIBED' },
  { label: 'Email Replied', value: 'EMAIL_REPLIED' },
  { label: 'Page Visited', value: 'PAGE_VISITED' },
  { label: 'Form Submitted', value: 'FORM_SUBMITTED' },
  { label: 'Download Triggered', value: 'DOWNLOAD_TRIGGERED' },
  { label: 'Chat Started', value: 'CHAT_STARTED' },
  { label: 'Chat Message Sent', value: 'CHAT_MESSAGE_SENT' },
  { label: 'Chat Completed', value: 'CHAT_COMPLETED' },
  { label: 'Call Missed', value: 'CALL_MISSED' },
  { label: 'Call Completed', value: 'CALL_COMPLETED' },
  { label: 'SMS Sent', value: 'SMS_SENT' },
  { label: 'SMS Delivered', value: 'SMS_DELIVERED' },
  { label: 'SMS Replied', value: 'SMS_REPLIED' },
  { label: 'Application Submitted', value: 'APPLICATION_SUBMITTED' },
  { label: 'Document Uploaded', value: 'DOCUMENT_UPLOADED' },
  { label: 'Test Started', value: 'TEST_STARTED' },
  { label: 'Test Completed', value: 'TEST_COMPLETED' },
  { label: 'Interview Confirmed', value: 'INTERVIEW_CONFIRMED' },
  { label: 'Interview Rescheduled', value: 'INTERVIEW_RESCHEDULED' }
]

// Form data matching doctype fields
const formData = reactive({
  name: '',
  talent_id: '',
  interaction_type: '',
  action: '',
  url: '',
  description: ''
})

// Filters
const filters = reactive({
  interaction_type: '',
  talent_id: '',
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
  { title: 'Candidate', key: 'talent_id', sortable: true },
  { title: 'Type', key: 'interaction_type', sortable: true },
  { title: 'Source Action', key: 'action', sortable: true },
  { title: 'URL', key: 'url', sortable: false },
  { title: 'Description', key: 'description', sortable: false },
  { title: 'Modified', key: 'modified', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false }
]

// Computed properties
const hasActiveFilters = computed(() => {
  return Object.values(filters).some(value => value && value !== '')
})

const formValid = computed(() => {
  return formData.talent_id && formData.interaction_type
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
    const searchConditions = []
    if (search.value && search.value.trim() !== '') {
      searchConditions.push(['talent_id', 'like', `%${search.value}%`])
      searchConditions.push(['interaction_type', 'like', `%${search.value}%`])
      searchConditions.push(['description', 'like', `%${search.value}%`])
    }
    
    const params = {
      filters: apiFilters,
      page_length: pagination.limit,
      start: (pagination.page - 1) * pagination.limit,
      order_by: 'modified desc',
      fields: ['name', 'talent_id', 'interaction_type', 'action', 'url', 'description', 'modified']
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
        label: `${item.full_name} (${item.email})`,
        value: item.name
      }))
    }
    
    // Load actions
    const actionResult = await actionService.getList({
      fields: ['name', 'talent_campaign_id', 'campaign_step'],
      page_length: 1000
    })
    if (actionResult.success) {
      filterOptions.actions = actionResult.data.map(item => ({
        label: `${item.talent_campaign_id} - ${item.campaign_step}`,
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

const exportData = async () => {
  try {
    const result = await interactionService.export({
      filters: filters,
      fields: ['name', 'talent_id', 'interaction_type', 'action', 'url', 'description', 'modified']
    })
    if (result.success) {
      // Handle export (download file)
      console.log('Export successful')
    }
  } catch (error) {
    console.error('Error exporting data:', error)
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
    talent_id: '',
    interaction_type: '',
    action: '',
    url: '',
    description: ''
  })
}

const saveData = async () => {
  // Validate required fields
  if (!formData.talent_id) {
    alert('Please select a candidate')
    return
  }
  if (!formData.interaction_type) {
    alert('Please select an interaction type')
    return
  }

  saving.value = true
  try {
    const result = await interactionService.save(formData)
    if (result.success) {
      closeFormModal()
      loadData()
    } else {
      console.error('Error saving data:', result.error)
      alert('Error saving interaction: ' + (result.error || 'Unknown error'))
    }
  } catch (error) {
    console.error('Error saving data:', error)
    alert('Error saving interaction: ' + (error.message || 'Unknown error'))
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
      itemToDelete.value = null
      loadData()
    } else {
      console.error('Error deleting data:', result.error)
      alert('Error deleting interaction: ' + (result.error || 'Unknown error'))
    }
  } catch (error) {
    console.error('Error deleting data:', error)
    alert('Error deleting interaction: ' + (error.message || 'Unknown error'))
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

const getInteractionTypeColor = (type) => {
  if (type.includes('EMAIL')) return 'blue'
  if (type.includes('CALL')) return 'orange'
  if (type.includes('SMS')) return 'purple'
  if (type.includes('CHAT')) return 'blue'
  if (type.includes('PAGE')) return 'green'
  if (type.includes('FORM')) return 'purple'
  if (type.includes('DOWNLOAD')) return 'orange'
  if (type.includes('TEST')) return 'indigo'
  if (type.includes('INTERVIEW')) return 'teal'
  return 'gray'
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
