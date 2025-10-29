<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Automation Sidebar -->
    <AutomationSidebar
      @create="handleCreateFromSidebar"
    />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Header -->

      <!-- Main Content -->
      <div class="flex-1 overflow-auto">
        <div class="max-w-full mx-4 px-4 py-8">
      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <FeatherIcon name="list" class="w-4 h-4 text-blue-600" />
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Total Sequences</p>
              <p class="text-2xl font-semibold text-gray-900">{{ statistics.total }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                <FeatherIcon name="play" class="w-4 h-4 text-green-600" />
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Active</p>
              <p class="text-2xl font-semibold text-gray-900">{{ statistics.active }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center">
                <FeatherIcon name="pause" class="w-4 h-4 text-yellow-600" />
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Paused</p>
              <p class="text-2xl font-semibold text-gray-900">{{ statistics.paused }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                <FeatherIcon name="check-circle" class="w-4 h-4 text-purple-600" />
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Completed</p>
              <p class="text-2xl font-semibold text-gray-900">{{ statistics.completed }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters and Search -->
      <div class="bg-white rounded-lg shadow mb-6">
        <div class="p-6 border-b border-gray-200">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
            <div class="flex-1 max-w-lg">
              <div class="relative">
                <FeatherIcon name="search" class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  v-model="searchText"
                  type="text"
                  placeholder="Search by sequence name or purpose..."
                  class="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>
            
            <div class="flex items-center space-x-3">
              <Button
              variant="outline"
              theme="gray"
              @click="refreshData"
              :loading="loading"
            >
              <div class="flex items-center">
                <FeatherIcon name="refresh-cw" class="w-4 h-4 mr-2" />
                Refresh
              </div>
            </Button>
              <Select
                v-model="statusFilter"
                :options="statusOptions"
                placeholder="All Status"
                class="w-40"
              />
              
              <Button
                v-if="hasActiveFilters"
                variant="outline"
                theme="gray"
                @click="clearAllFilters"
              >
              <div class="flex items-center">
                <FeatherIcon name="x" class="w-4 h-4 mr-2" />
                {{ __('Clear Filters') }}
              </div>
              </Button>
            </div>
          </div>
        </div>

        <!-- Sequences List -->
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Sequence
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Steps
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Enrollments
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Created At
                </th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="loading" class="animate-pulse">
                <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                  <FeatherIcon name="loader" class="w-5 h-5 animate-spin mx-auto" />
                  <span class="ml-2">Loading...</span>
                </td>
              </tr>
              
              <tr v-else-if="!loading && filteredSequences.length === 0">
                <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                  <FeatherIcon name="inbox" class="w-8 h-8 mx-auto mb-2 text-gray-400" />
                  <p>No sequences found</p>
                </td>
              </tr>
              
              <tr v-else v-for="sequence in filteredSequences" :key="sequence.name" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center"
                         :class="getStatusIconClass(sequence.status)">
                      <FeatherIcon name="list" class="w-4 h-4" />
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">{{ sequence.title }}</div>
                      <div class="text-sm text-gray-500">{{ sequence.purpose || 'No purpose specified' }}</div>
                    </div>
                  </div>
                </td>
                
                <td class="px-6 py-4 whitespace-nowrap">
                  <Badge
                    :variant="getStatusVariant(sequence.status)"
                    :label="sequence.display_status"
                  />
                </td>
                
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  <div class="flex items-center">
                    <FeatherIcon name="layers" class="w-4 h-4 mr-2 text-gray-400" />
                    {{ sequence.steps_count }} steps
                  </div>
                </td>
                
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  <div class="flex items-center">
                    <FeatherIcon name="users" class="w-4 h-4 mr-2 text-gray-400" />
                    {{ sequence.enrollment_count || 0 }} enrolled
                  </div>
                </td>
                
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ sequence.formatted_created_at }}
                </td>
                
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <Dropdown :options="getActionOptions(sequence)">
                    <Button variant="ghost" theme="gray" size="sm">
                      <FeatherIcon name="more-horizontal" class="w-4 h-4" />
                    </Button>
                  </Dropdown>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="pagination.total > 0" class="px-6 py-4 border-t border-gray-200">
          <div class="flex items-center justify-between">
            <div class="text-sm text-gray-700">
              Showing {{ pagination.showing_from }} to {{ pagination.showing_to }} 
              of {{ pagination.total }} results
            </div>
            
            <div class="flex items-center space-x-2">
              <Button
                variant="outline"
                theme="gray"
                size="sm"
                :disabled="!pagination.has_prev"
                @click="goToPage(pagination.page - 1)"
              >
                <FeatherIcon name="chevron-left" class="w-4 h-4" />
              </Button>
              
              <span class="text-sm text-gray-700">
                Page {{ pagination.page }}
              </span>
              
              <Button
                variant="outline"
                theme="gray"
                size="sm"
                :disabled="!pagination.has_next"
                @click="goToPage(pagination.page + 1)"
              >
                <FeatherIcon name="chevron-right" class="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      <!-- Create Modal -->
      <SequenceCreateModal
        v-if="showCreateModal"
        :show="showCreateModal"
        @close="showCreateModal = false"
        @success="handleCreateSuccess"
      />

      <!-- View Modal -->
      <SequenceViewModal
        v-if="showViewModal"
        :show="showViewModal"
        :sequence="viewingSequence"
        @close="showViewModal = false"
      />

      <!-- Delete Confirmation Modal -->
      <DeleteConfirmModal
        v-if="showDeleteModal"
        :show="showDeleteModal"
        :title="'Delete Sequence'"
        :message="`Are you sure you want to delete sequence '${deletingSequence?.title}'? This action cannot be undone.`"
        @close="showDeleteModal = false"
        @confirm="confirmDelete"
      />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { Button, Select, Badge, Dropdown, FeatherIcon, Breadcrumbs } from 'frappe-ui'
import { useSequenceStore } from '@/stores/sequence'
import { useToast } from '@/composables/useToast'
import SequenceViewModal from '@/components/sequence/SequenceViewModal.vue'
import SequenceCreateModal from '@/components/sequence/SequenceCreateModal.vue'
import DeleteConfirmModal from '@/components/common/DeleteConfirmModal.vue'
import LayoutHeader from "@/components/LayoutHeader.vue"
import AutomationSidebar from "@/components/AutomationSidebar.vue"
import { useAutomationStatsStore } from "@/stores/automationStats"
import { debounce } from 'lodash'

// Composables
const router = useRouter()
const sequenceStore = useSequenceStore()
const statsStore = useAutomationStatsStore()
const toast = useToast()

// Reactive state
const searchText = ref('')
const statusFilter = ref('')
const showCreateModal = ref(false)
const showViewModal = ref(false)
const showDeleteModal = ref(false)
const viewingSequence = ref(null)
const deletingSequence = ref(null)

// Status options for filter
const statusOptions = [
  { label: 'All Status', value: '' },
  { label: 'Active', value: 'Active' },
  { label: 'Draft', value: 'Draft' },
  { label: 'Paused', value: 'Paused' },
  { label: 'Completed', value: 'Completed' }
]

// Computed
const loading = computed(() => sequenceStore.loading)
const filteredSequences = computed(() => sequenceStore.filteredSequences)
const pagination = computed(() => sequenceStore.pagination)
const statistics = computed(() => sequenceStore.statistics)

const hasActiveFilters = computed(() => {
  return searchText.value || statusFilter.value
})

// Methods
const handleCreateFromSidebar = (section) => {
  console.log('Create new from sidebar:', section)
  if (section === 'sequences') {
    showCreateModal.value = true
  }
  // Campaign và Flow sẽ được xử lý bởi router
}

const loadSequences = async (options = {}) => {
  try {
    const result = await sequenceStore.fetchSequences(options)
    
    // Always update statistics from the result data
    if (result && result.count !== undefined) {
      // Check if this is a full data load (no filters, page 1)
      const isFullLoad = (!options.page || options.page === 1) && 
                        !sequenceStore.filters.search && 
                        !sequenceStore.filters.status && 
                        !sequenceStore.filters.owner
      
      if (isFullLoad && result.data) {
        // For full load, calculate accurate statistics from all loaded data
        const statusCounts = { active: 0, draft: 0, paused: 0, completed: 0 }
        result.data.forEach(sequence => {
          const status = sequence.status?.toLowerCase()
          if (statusCounts.hasOwnProperty(status)) {
            statusCounts[status]++
          }
        })
        
        // Update complete statistics
        sequenceStore.statistics = {
          total: result.count,
          ...statusCounts
        }
      } else {
        // For filtered/paginated load, only update total count
        // Keep existing status breakdown (may not be 100% accurate but avoids extra API call)
        sequenceStore.statistics.total = result.count
      }
    }
    
    return result
  } catch (error) {
    console.error('Error loading sequences:', error)
    toast.error('Unable to load sequences list')
  }
}

const loadStatistics = async () => {
  try {
    await sequenceStore.fetchStatistics()
  } catch (error) {
    console.error('Error loading statistics:', error)
  }
}

const refreshData = async () => {
  try {
    // Only load sequences, which will also calculate and update statistics
    await loadSequences({ page: 1 })
    toast.success('Refreshed successfully')
  } catch (error) {
    console.error('Error refreshing data:', error)
    toast.error('Failed to refresh data')
  }
}

const goToPage = (page) => {
  loadSequences({ page })
}

const clearAllFilters = () => {
  searchText.value = ''
  statusFilter.value = ''
  sequenceStore.clearFilters()
  loadSequences({ page: 1 })
}

const getStatusIconClass = (status) => {
  const classMap = {
    'Active': 'bg-green-100 text-green-600',
    'Draft': 'bg-gray-100 text-gray-600',
    'Paused': 'bg-yellow-100 text-yellow-600',
    'Completed': 'bg-blue-100 text-blue-600'
  }
  return classMap[status] || 'bg-gray-100 text-gray-600'
}

const getStatusVariant = (status) => {
  const variantMap = {
    'Active': 'success',
    'Draft': 'gray',
    'Paused': 'warning',
    'Completed': 'blue'
  }
  return variantMap[status] || 'gray'
}

const getActionOptions = (sequence) => {
  const baseOptions = [
    {
      label: 'View',
      icon: 'eye',
      onClick: () => viewSequence(sequence)
    },
    {
      label: 'Edit',
      icon: 'edit',
      onClick: () => editSequence(sequence)
    },
    {
      label: 'Duplicate',
      icon: 'copy',
      onClick: () => duplicateSequence(sequence)
    }
  ]

  // Only allow delete if not Active
  if (sequence.status !== 'Active') {
    baseOptions.push({
      label: 'Delete',
      icon: 'trash-2',
      onClick: () => deleteSequence(sequence),
      class: 'text-red-600'
    })
  }

  return baseOptions
}

const viewSequence = async (sequence) => {
  try {
    const result = await sequenceStore.getSequence(sequence.name)
    if (result.success) {
      viewingSequence.value = result.data
      showViewModal.value = true
    } else {
      toast.error(result.error || 'Unable to load sequence details')
    }
  } catch (error) {
    console.error('Error loading sequence details:', error)
    toast.error('An error occurred while loading sequence details')
  }
}

const editSequence = (sequence) => {
  router.push({ name: 'SequenceEditor', params: { id: sequence.name } })
}

const deleteSequence = (sequence) => {
  if (sequence.status === 'Active') {
    toast.error('Cannot delete active sequence. Please pause the sequence first.')
    return
  }
  
  deletingSequence.value = sequence
  showDeleteModal.value = true
}

const duplicateSequence = async (sequence) => {
  try {
    const result = await sequenceStore.duplicateSequence(sequence.name)
    if (result.success) {
      toast.success('Duplicated sequence successfully')
      await loadSequences() // This will also update statistics
    } else {
      toast.error(result.error || 'Failed to duplicate sequence')
    }
  } catch (error) {
    console.error('Error duplicating sequence:', error)
    toast.error('Failed to duplicate sequence')
  }
}

const confirmDelete = async () => {
  if (!deletingSequence.value) return
  
  try {
    const result = await sequenceStore.deleteSequence(deletingSequence.value.name)
    
    if (result.success) {
      toast.success(`Sequence "${deletingSequence.value.title}" đã được xóa`)
      showDeleteModal.value = false
      deletingSequence.value = null
      await loadSequences({ page: 1 })
      
      // Refresh sidebar stats
      statsStore.refreshStats()
    } else {
      toast.error(result.error || 'Có lỗi xảy ra khi xóa sequence')
    }
  } catch (error) {
    toast.error('Có lỗi xảy ra khi xóa sequence')
  }
}

const handleCreateSuccess = async (newSequence) => {
  showCreateModal.value = false
  toast.success(`Sequence "${newSequence.title}" đã được tạo thành công`)
  await loadSequences({ page: 1 })
  
  // Refresh sidebar stats
  statsStore.refreshStats()
}

// Debounced search function
const debouncedSearch = debounce((searchValue) => {
  sequenceStore.setSearch(searchValue)
  loadSequences({ page: 1 })
}, 500)

// Watchers
watch(searchText, (newValue) => {
  debouncedSearch(newValue)
})

watch(statusFilter, (newValue) => {
  sequenceStore.setStatusFilter(newValue)
  loadSequences({ page: 1 })
})

// Lifecycle
onMounted(async () => {
  // Only load sequences, which will also calculate and update statistics
  await loadSequences()
})
</script>
