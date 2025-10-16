<template>
  <div class="min-h-screen bg-gray-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header>
        <!-- Create dropdown button -->
        <Dropdown :options="dropdownActions" @click.stop>
          <template v-slot="{ open }">
            <Button variant="solid" theme="gray" size="sm" :disabled="loading">
              <template #prefix>
                <FeatherIcon name="plus" class="h-4 w-4" />
              </template>
              <span>{{ __("New") }}</span>
              <template #suffix>
                <FeatherIcon
                  :name="open ? 'chevron-up' : 'chevron-down'"
                  class="h-4 w-4"
                />
              </template>
            </Button>
          </template>
        </Dropdown>
      </template>
    </LayoutHeader>

    <div class="container mx-auto px-6 py-6">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <!-- Search box -->
        <div class="relative">
          <input
            v-model="searchText"
            type="text"
            :placeholder="__('Search flows...')"
            class="block w-60 pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            @input="handleSearch"
          />
          <div
            class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
          >
            <FeatherIcon name="search" class="h-5 w-5 text-gray-400" />
          </div>
          <button
            v-if="searchText"
            @click="handleClearSearch"
            class="absolute inset-y-0 right-0 pr-3 flex items-center"
          >
            <FeatherIcon name="x" class="h-5 w-5 text-gray-400 hover:text-gray-600" />
          </button>
        </div>

        <div class="flex items-center space-x-4">
          <!-- Status Filter -->
          <Select
            v-model="statusFilter"
            :options="statusOptions"
            class="min-w-40 text-sm"
            size="md"
            variant="outlined"
          />

          <!-- Refresh Button -->
          <Button
            variant="outline"
            theme="gray"
            @click="handleRefresh"
            :loading="loading"
            class="flex items-center py-4"
          >
            <template #prefix>
              <FeatherIcon name="refresh-cw" class="h-4 w-4" />
            </template>
            {{ __("Refresh") }}
          </Button>
        </div>
      </div>

      <!-- Flow List -->
      <div class="bg-white shadow rounded-lg">
        <!-- Table Header -->
        <div class="px-6 py-3 border-b border-gray-200 bg-gray-50">
          <div class="flex items-center">
            <div class="flex-1 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              {{ __("Flow Name") }}
            </div>
            <div class="w-32 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              {{ __("Status") }}
            </div>
            <div class="w-32 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              {{ __("Actions") }}
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading && flows.length === 0" class="px-6 py-12 text-center">
          <div class="inline-flex items-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span class="text-gray-500">{{ __("Loading flows...") }}</span>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="!loading && flows.length === 0" class="px-6 py-12 text-center">
          <FeatherIcon name="workflow" class="mx-auto h-12 w-12 text-gray-400" />
          <h3 class="mt-2 text-sm font-medium text-gray-900">{{ __("No flows") }}</h3>
          <p class="mt-1 text-sm text-gray-500">{{ __("Get started by creating a new flow.") }}</p>
        </div>

        <!-- Flow Items -->
        <div v-else>
          <div
            v-for="flow in flows"
            :key="flow.name"
            class="px-6 py-4 border-b border-gray-200 hover:bg-gray-50 transition-colors duration-150"
          >
            <div class="flex items-center">
              <!-- Flow Info -->
              <div class="flex-1">
                <div class="flex items-center">
                  <h3 class="text-sm font-medium text-gray-900">
                    {{ flow.title }}
                  </h3>
                </div>
                <p v-if="flow.description" class="mt-1 text-sm text-gray-500">
                  {{ flow.description }}
                </p>
                <div class="mt-1 flex items-center text-xs text-gray-400">
                  <span>{{ __("Created") }}: {{ flow.formatted_created_at }}</span>
                  <span class="mx-2">•</span>
                  <span>{{ __("Modified") }}: {{ flow.formatted_modified }}</span>
                </div>
              </div>

              <!-- Status -->
              <div class="w-32">
                <Badge
                  :variant="getStatusVariant(flow.status)"
                  :label="flow.display_status"
                  size="md"
                />
              </div>

              <!-- Actions -->
              <div class="w-32 flex justify-end">
                <Dropdown :options="getFlowActions(flow)" placement="bottom-end">
                  <template v-slot="{ open }">
                    <Button variant="ghost" size="sm">
                      <FeatherIcon name="more-horizontal" class="h-4 w-4" />
                    </Button>
                  </template>
                </Dropdown>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="flows.length > 0" class="px-6 py-3 border-t border-gray-200 bg-gray-50">
          <div class="flex items-center justify-between">
            <div class="text-sm text-gray-700">
              {{ __("Showing") }} {{ pagination.showing_from }} {{ __("to") }} {{ pagination.showing_to }}
              {{ __("of") }} {{ pagination.total }} {{ __("results") }}
            </div>
            <div class="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                @click="previousPage"
                :disabled="!pagination.has_prev"
              >
                <FeatherIcon name="chevron-left" class="h-4 w-4" />
              </Button>
              <span class="text-sm text-gray-700">
                {{ __("Page") }} {{ pagination.page }}
              </span>
              <Button
                variant="outline"
                size="sm"
                @click="nextPage"
                :disabled="!pagination.has_next"
              >
                <FeatherIcon name="chevron-right" class="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Flow Form Modal -->
    <FlowFormModal
      v-model="showFlowModal"
      :flow="selectedFlow"
      @success="handleFlowSuccess"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useMiraFlowStore } from '@/stores/miraFlow'
import { useToast } from '@/composables/useToast'
import { debounce } from 'lodash-es'

// Components
import LayoutHeader from "@/components/LayoutHeader.vue";
import FlowFormModal from "@/components/Modals/FlowFormModal.vue";

import { Button, Select, Badge, Dropdown, FeatherIcon, Breadcrumbs } from 'frappe-ui'


// Router
const router = useRouter()

// Store
const flowStore = useMiraFlowStore()

// Toast
const toast = useToast()

// Reactive data
const searchText = ref('')
const statusFilter = ref('')
const showFlowModal = ref(false)
const selectedFlow = ref(null)

// Computed
const flows = computed(() => flowStore.filteredFlows)
const loading = computed(() => flowStore.loading)
const pagination = computed(() => flowStore.pagination)

const breadcrumbs = computed(() => [
  { label: __('Flow Management'), route: { name: 'FlowManagement' } }
])

const statusOptions = computed(() => [
  { label: __('All Statuses'), value: '' },
  { label: __('Active'), value: 'Active' },
  { label: __('Draft'), value: 'Draft' },
  { label: __('Paused'), value: 'Paused' },
  { label: __('Archived'), value: 'Archived' }
])

const dropdownActions = computed(() => [
  {
    label: __('Use Template Flow'),
    description: __('Use pre-built scenarios to optimize your campaigns effectively'),
    icon: 'template',
    onClick: () => handleUseTemplate()
  },
  {
    label: __('Create Flow'),
    description: __('Design your own Flow according to your ideas'),
    icon: 'plus-circle',
    onClick: () => handleCreateFlow()
  },
  {
    label: __('Upload Flow from Computer'),
    description: __('Use .ladiflow design file from your computer'),
    icon: 'upload',
    onClick: () => handleUploadFlow()
  }
])

// Methods
const handleSearch = debounce((event) => {
  const value = event?.target?.value || searchText.value
  flowStore.setSearch(value)
  loadFlows()
}, 300)

const handleClearSearch = () => {
  searchText.value = ''
  flowStore.setSearch('')
  loadFlows()
}

const handleStatusFilter = (value) => {
  console.log('Status filter changed:', value)
  flowStore.setStatusFilter(value)
  loadFlows()
}

const handleRefresh = () => {
  loadFlows()
}

const loadFlows = async () => {
  try {
    await flowStore.fetchFlows()
  } catch (error) {
    console.error('Error loading flows:', error)
    toast.showLoadError('flows', error)
  }
}

const previousPage = () => {
  if (pagination.value.has_prev) {
    loadFlows({ page: pagination.value.page - 1 })
  }
}

const nextPage = () => {
  if (pagination.value.has_next) {
    loadFlows({ page: pagination.value.page + 1 })
  }
}

const getStatusVariant = (status) => {
  const variantMap = {
    'Active': 'success',
    'Draft': 'gray',
    'Paused': 'warning',
    'Archived': 'error'
  }
  return variantMap[status] || 'gray'
}

const getFlowActions = (flow) => [
  {
    label: 'Xuất bản',
    icon: 'upload',
    onClick: () => handlePublishFlow(flow),
    condition: () => flow.status === 'Draft'
  },
  {
    label: 'Chỉnh sửa',
    icon: 'edit',
    onClick: () => handleEditFlow(flow)
  },
  {
    label: 'Nhân bản',
    icon: 'copy',
    onClick: () => handleDuplicateFlow(flow)
  },
  {
    label: 'Xóa',
    icon: 'trash-2',
    onClick: () => handleDeleteFlow(flow),
    condition: () => flow.status !== 'Active'
  }
].filter(action => !action.condition || action.condition())

// Action handlers
const handleUseTemplate = () => {
  // TODO: Navigate to template selection
  toast.info('Template flow selection coming soon')
}

const handleCreateFlow = () => {
  selectedFlow.value = null
  showFlowModal.value = true
}

const handleUploadFlow = () => {
  // TODO: Open file upload dialog
  toast.info('Flow upload coming soon')
}

const handlePublishFlow = async (flow) => {
  try {
    const result = await flowStore.updateFlow(flow.name, { status: 'Active' })
    if (result.success) {
      toast.success('Flow đã được xuất bản thành công')
      await loadFlows() // Reload to show updated status
    } else {
      toast.error(result.error || 'Có lỗi xảy ra khi xuất bản flow')
    }
  } catch (error) {
    console.error('Error publishing flow:', error)
    toast.error('Có lỗi xảy ra khi xuất bản flow')
  }
}

const handleEditFlow = (flow) => {
  router.push({ name: 'FlowEditor', params: { id: flow.name } })
}

const handleDuplicateFlow = async (flow) => {
  try {
    const result = await flowStore.duplicateFlow(flow.name)
    if (result.success) {
      toast.success('Flow đã được nhân bản thành công')
      await loadFlows() // Reload to show the new flow
    } else {
      toast.error(result.error || 'Có lỗi xảy ra khi nhân bản flow')
    }
  } catch (error) {
    console.error('Error duplicating flow:', error)
    toast.error('Có lỗi xảy ra khi nhân bản flow')
  }
}

const handleDeleteFlow = async (flow) => {
  if (confirm('Bạn có chắc chắn muốn xóa flow này không?')) {
    try {
      const result = await flowStore.deleteFlow(flow.name)
      console.log(result)
      if (result.success) {
        toast.success('Flow đã được xóa thành công')
      } else {
        toast.error(result.error || 'Có lỗi xảy ra khi xóa flow')
      }
    } catch (error) {
      console.error('Error deleting flow:', error)
      toast.error('Có lỗi xảy ra khi xóa flow')
    }
  }
}

const handleFlowSuccess = (flow) => {
  toast.success(selectedFlow.value ? 'Flow đã được cập nhật thành công' : 'Flow đã được tạo thành công')
  loadFlows() // Reload the list
}

// Watchers
watch(searchText, (newValue) => {
  flowStore.setSearch(newValue)
})

watch(statusFilter, (newValue) => {
  console.log('Status filter watcher:', newValue)
  flowStore.setStatusFilter(newValue)
  loadFlows()
})

// Lifecycle
onMounted(() => {
  loadFlows()
})
</script>
