<template>
  <Dialog
    v-model="isOpen"
    :options="{
      size: '5xl',
      title: __('Sync History')
    }"
  >
    <template #body-content>
      <div class="space-y-4">
        <!-- Header with refresh button -->
        <div class="flex items-center justify-between">
          <div>
            <h4 class="font-medium text-gray-900">{{ __('Candidate to Talent Sync History') }}</h4>
            <p class="text-sm text-gray-500 mt-1">
              {{ __('View all sync operations from ATS to Talent Pool') }}
            </p>
          </div>
          <Button
            variant="outline"
            size="sm"
            @click="fetchSyncLogs(currentPage)"
            :loading="loadingSyncLogs"
          >
            <template #prefix>
              <FeatherIcon name="refresh-cw" class="h-4 w-4" />
            </template>
            {{ __('Refresh') }}
          </Button>
        </div>
        
        <!-- Loading State -->
        <div v-if="loadingSyncLogs" class="flex items-center justify-center py-12">
          <LoadingIndicator class="w-8 h-8" />
          <span class="ml-3 text-gray-600">{{ __('Loading sync history...') }}</span>
        </div>
        
        <!-- Sync Logs Table -->
        <div v-else-if="syncLogs.length > 0" class="border rounded-lg overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ __('Connection') }}
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ __('Status') }}
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ __('Records') }}
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ __('Start Time') }}
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ __('End Time') }}
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ __('Details') }}
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ __('Actions') }}
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="log in syncLogs" :key="log.name" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ log.connection }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      :class="[
                        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                        getStatusClass(log.status)
                      ]"
                    >
                      {{ log.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <div class="flex items-center gap-2">
                      <span class="text-green-600 font-medium">{{ log.success_count || 0 }}</span>
                      <span class="text-gray-400">/</span>
                      <span class="text-gray-600">{{ log.total_records || 0 }}</span>
                      <span v-if="log.failed_count > 0" class="text-red-600">({{ log.failed_count }} failed)</span>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatDateTime(log.start_time) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ log.end_time ? formatDateTime(log.end_time) : '-' }}
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-500 max-w-xs">
                    <div class="truncate" :title="log.details">
                      {{ log.details || '-' }}
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <div class="flex items-center gap-2">
                      <!-- Cancel Button -->
                      <Button
                        v-if="log.status === 'Pending' || log.status === 'In Progress'"
                        variant="outline"
                        theme="red"
                        size="sm"
                        @click="cancelSync(log.name)"
                        :loading="actionLoading[log.name]"
                      >
                        <template #prefix>
                          <FeatherIcon name="x" class="h-3 w-3" />
                        </template>
                        {{ __('Cancel') }}
                      </Button>
                      
                      <!-- Retry Button -->
                      <Button
                        v-if="log.status === 'Failed' || log.status === 'Partially Completed' || log.status === 'Cancelled'"
                        variant="outline"
                        theme="gray"
                        size="sm"
                        @click="retrySync(log.name)"
                        :loading="actionLoading[log.name]"
                      >
                        <template #prefix>
                          <FeatherIcon name="refresh-cw" class="h-3 w-3" />
                        </template>
                        {{ __('Retry') }}
                      </Button>
                      
                      <!-- No actions for completed -->
                      <span v-if="log.status === 'Completed'" class="text-gray-400 text-xs">
                        {{ __('No actions') }}
                      </span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <!-- Empty State -->
        <div v-else class="text-center py-12 border rounded-lg bg-gray-50">
          <FeatherIcon name="clock" class="w-12 h-12 mx-auto mb-4 text-gray-300" />
          <p class="text-gray-500 mb-2">{{ __('No sync history found') }}</p>
          <p class="text-sm text-gray-400">
            {{ __('Sync operations will appear here once they are executed.') }}
          </p>
        </div>
        
        <!-- Pagination -->
        <div v-if="syncLogs.length > 0 && totalRecords > pageSize" class="flex items-center justify-between mt-4 pt-4 border-t border-gray-200">
          <div class="text-sm text-gray-500">
            {{ __('Showing {0} to {1} of {2} entries', [
              (currentPage - 1) * pageSize + 1,
              Math.min(currentPage * pageSize, totalRecords),
              totalRecords
            ]) }}
          </div>
          <div class="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              @click="fetchSyncLogs(currentPage - 1)"
              :disabled="currentPage <= 1"
            >
              <template #prefix>
                <FeatherIcon name="chevron-left" class="h-4 w-4" />
              </template>
              {{ __('Previous') }}
            </Button>
            
            <div class="flex items-center gap-1">
              <Button
                v-for="page in getVisiblePages()"
                :key="page"
                :variant="page === currentPage ? 'solid' : 'outline'"
                :theme="page === currentPage ? 'gray' : 'gray'"
                size="sm"
                @click="fetchSyncLogs(page)"
                class="min-w-[32px]"
              >
                {{ page }}
              </Button>
            </div>
            
            <Button
              variant="outline"
              size="sm"
              @click="fetchSyncLogs(currentPage + 1)"
              :disabled="currentPage >= Math.ceil(totalRecords / pageSize)"
            >
              {{ __('Next') }}
              <template #suffix>
                <FeatherIcon name="chevron-right" class="h-4 w-4" />
              </template>
            </Button>
          </div>
        </div>
      </div>
    </template>

    <template #actions>
      <div class="flex justify-end pt-4 border-t border-gray-200">
        <Button
          variant="outline"
          theme="gray"
          @click="closeDialog"
        >
          {{ __('Close') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Dialog, Button, FeatherIcon, LoadingIndicator } from 'frappe-ui'
import { useToast } from '@/composables/useToast'
import { call } from 'frappe-ui'
import { globalStore } from '@/stores/global'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const { showError, showSuccess } = useToast()

// State
const isOpen = ref(props.modelValue)
const loadingSyncLogs = ref(false)
const syncLogs = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const totalRecords = ref(0)
const actionLoading = ref({})

// Watch dialog state
watch(() => props.modelValue, (newValue) => {
  isOpen.value = newValue
  if (newValue) {
    fetchSyncLogs()
  }
})

watch(isOpen, (newValue) => {
  emit('update:modelValue', newValue)
  if (!newValue) {
    // Reset when closed
    currentPage.value = 1
    syncLogs.value = []
    totalRecords.value = 0
  }
})

// Methods
const closeDialog = () => {
  isOpen.value = false
  emit('update:modelValue', false)
}

const fetchSyncLogs = async (page = 1) => {
  currentPage.value = page
  loadingSyncLogs.value = true
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Mira ATS Sync Log',
      filters: {
        sync_type: 'Candidate to Talent'
      },
      fields: [
        'name',
        'connection',
        'status',
        'start_time',
        'end_time',
        'total_records',
        'success_count',
        'failed_count',
        'details'
      ],
      order_by: 'creation desc',
      limit_page_length: pageSize.value,
      limit_start: (page - 1) * pageSize.value
    })
    
    syncLogs.value = response || []
    
    // Get total count for pagination
    const countResponse = await call('frappe.client.get_count', {
      doctype: 'Mira ATS Sync Log',
      filters: {
        sync_type: 'Candidate to Talent'
      }
    })
    
    totalRecords.value = countResponse || 0
  } catch (error) {
    console.error('Error fetching sync logs:', error)
    showError(__('Failed to load sync history'))
  } finally {
    loadingSyncLogs.value = false
  }
}

const getStatusClass = (status) => {
  const statusMap = {
    'Pending': 'bg-gray-100 text-gray-800',
    'In Progress': 'bg-blue-100 text-blue-800',
    'Completed': 'bg-green-100 text-green-800',
    'Partially Completed': 'bg-yellow-100 text-yellow-800',
    'Failed': 'bg-red-100 text-red-800',
    'Cancelled': 'bg-orange-100 text-orange-800'
  }
  return statusMap[status] || 'bg-gray-100 text-gray-800'
}

const formatDateTime = (dateTime) => {
  if (!dateTime) return '-'
  const date = new Date(dateTime)
  return date.toLocaleString('vi-VN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const getVisiblePages = () => {
  const totalPages = Math.ceil(totalRecords.value / pageSize.value)
  const current = currentPage.value
  const pages = []
  
  // Show max 5 pages at a time
  const maxVisible = 5
  let start = Math.max(1, current - Math.floor(maxVisible / 2))
  let end = Math.min(totalPages, start + maxVisible - 1)
  
  // Adjust start if we're near the end
  if (end - start + 1 < maxVisible) {
    start = Math.max(1, end - maxVisible + 1)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
}

const cancelSync = async (syncLogName) => {
  actionLoading.value[syncLogName] = true
  try {
    const response = await call('mbw_mira.api.sync_segment.cancel_sync', {
      sync_log_name: syncLogName
    })
    
    if (response.status === 'success') {
      showSuccess(response.message)
      // Refresh the list to show updated status
      await fetchSyncLogs(currentPage.value)
    } else {
      showError(response.message)
    }
  } catch (error) {
    console.error('Error cancelling sync:', error)
    showError(error.message || __('Failed to cancel sync'))
  } finally {
    actionLoading.value[syncLogName] = false
  }
}

const retrySync = async (syncLogName) => {
  actionLoading.value[syncLogName] = true
  try {
    const response = await call('mbw_mira.api.sync_segment.retry_sync', {
      sync_log_name: syncLogName
    })
    
    if (response.status === 'success') {
      showSuccess(response.message)
      // Refresh the list to show updated status
      await fetchSyncLogs(currentPage.value)
    } else {
      showError(response.message)
    }
  } catch (error) {
    console.error('Error retrying sync:', error)
    showError(error.message || __('Failed to retry sync'))
  } finally {
    actionLoading.value[syncLogName] = false
  }
}

// Setup socket listener for sync completion and progress
const { $socket } = globalStore()
if ($socket) {
  // Listen for completion events
  $socket.on('candidate_sync_complete', (data) => {
    if (isOpen.value && data.sync_type === 'Candidate to Talent') {
      // Refresh sync history when modal is open
      fetchSyncLogs(currentPage.value)
    }
  })
  
  $socket.on('position_sync_complete', (data) => {
    if (isOpen.value && data.sync_type === 'Position to Segment') {
      // Refresh sync history when modal is open
      fetchSyncLogs(currentPage.value)
    }
  })
  
  // Listen for progress events
  $socket.on('candidate_sync_progress', (data) => {
    if (isOpen.value) {
      // Update the specific sync log in the list
      const logIndex = syncLogs.value.findIndex(log => log.name === data.sync_log_name)
      if (logIndex !== -1) {
        syncLogs.value[logIndex].success_count = data.success_count
        syncLogs.value[logIndex].failed_count = data.failed_count
        syncLogs.value[logIndex].skipped_count = data.skipped_count || 0
        syncLogs.value[logIndex].total_records = data.total_records
        syncLogs.value[logIndex].details = data.details
      }
    }
  })
  
  $socket.on('position_sync_progress', (data) => {
    if (isOpen.value) {
      // Update the specific sync log in the list
      const logIndex = syncLogs.value.findIndex(log => log.name === data.sync_log_name)
      if (logIndex !== -1) {
        syncLogs.value[logIndex].success_count = data.success_count
        syncLogs.value[logIndex].failed_count = data.failed_count
        syncLogs.value[logIndex].skipped_count = data.skipped_count || 0
        syncLogs.value[logIndex].total_records = data.total_records
        syncLogs.value[logIndex].details = data.details
      }
    }
  })
}
</script>
