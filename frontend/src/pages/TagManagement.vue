<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <Breadcrumbs
              :items="[
               
                { label: __('Tags Management'), route: { name: 'TagManagement' } }
              ]"
            />

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
              {{ __('Refresh') }}
            </div>
            </Button>
            <Button
              variant="solid"
              theme="blue"
              @click="showCreateModal = true"
            >
            <div class="flex items-center">
              <FeatherIcon name="plus" class="w-4 h-4 mr-2" />
              {{ __('Create New Tag') }}
            </div>
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <FeatherIcon name="tag" class="w-4 h-4 text-blue-600" />
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">{{ __('Total Tags') }}</p>
              <p class="text-2xl font-semibold text-gray-900">{{ statistics.total }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                <FeatherIcon name="clock" class="w-4 h-4 text-green-600" />
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">{{ __('Recent Tags') }}</p>
              <p class="text-2xl font-semibold text-gray-900">{{ recentTagsCount }}</p>
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
                  :placeholder="__('Search by tag name...')"
                  class="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>
            
            <div class="flex items-center space-x-3">
              <Button
                v-if="hasActiveFilters"
                variant="outline"
                theme="gray"
                @click="clearAllFilters"
              >
                <FeatherIcon name="x" class="w-4 h-4 mr-2" />
                {{ __('Clear Filters') }}
              </Button>
            </div>
          </div>
        </div>

        <!-- Tags List -->
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ __('Tag') }}
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ __('Color') }}
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ __('Order') }}
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ __('Created At') }}
                </th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ __('Actions') }}
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="loading" class="animate-pulse">
                <td colspan="5" class="px-6 py-4 text-center text-gray-500">
                  <FeatherIcon name="loader" class="w-5 h-5 animate-spin mx-auto" />
                  <span class="ml-2">{{ __('Loading...') }}</span>
                </td>
              </tr>
              
              <tr v-else-if="!loading && filteredTags.length === 0">
                <td colspan="5" class="px-6 py-4 text-center text-gray-500">
                  <FeatherIcon name="inbox" class="w-8 h-8 mx-auto mb-2 text-gray-400" />
                  <p>{{ __('No tags found') }}</p>
                </td>
              </tr>
              
              <tr v-else v-for="tag in filteredTags" :key="tag.name" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center"
                         :style="{ backgroundColor: tag.color + '20', color: tag.color }">
                      <FeatherIcon name="tag" class="w-4 h-4" />
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">{{ tag.title }}</div>
                      <div class="text-sm text-gray-500">{{ tag.name }}</div>
                    </div>
                  </div>
                </td>
                
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="w-6 h-6 rounded-full border border-gray-200"
                         :style="{ backgroundColor: tag.color }"></div>
                    <span class="ml-2 text-sm text-gray-600">{{ tag.color }}</span>
                  </div>
                </td>
                
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  <div class="flex items-center space-x-2">
                    <span class="font-mono">{{ tag.order || 0 }}</span>
                    <div class="flex flex-col space-y-3">
                      <Button
                        variant="ghost"
                        theme="gray"
                        size="sm"
                        @click="moveTagUp(tag)"
                        :disabled="isFirstTag(tag)"
                        class="p-1 h-6 w-8"
                      >
                        <FeatherIcon name="chevron-up" class="w-5 h-5" />
                      </Button>
                      <Button
                        variant="ghost"
                        theme="gray"
                        size="sm"
                        @click="moveTagDown(tag)"
                        :disabled="isLastTag(tag)"
                        class="p-1 h-6 w-8"
                      >
                        <FeatherIcon name="chevron-down" class="w-5 h-5" />
                      </Button>
                    </div>
                  </div>
                </td>
                
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ tag.formatted_created_at }}
                </td>
                
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <Dropdown :options="getActionOptions(tag)">
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
              {{ __('Showing') }} {{ pagination.showing_from }} {{ __('to') }} {{ pagination.showing_to }} 
              {{ __('of') }} {{ pagination.total }} {{ __('results') }}
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
                {{ __('Page') }} {{ pagination.page }}
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
    </div>

    <!-- Create/Edit Modal -->
    <TagFormModal
      v-if="showCreateModal || showEditModal"
      :show="showCreateModal || showEditModal"
      :tag="editingTag"
      @close="closeModals"
      @success="handleFormSuccess"
    />

    <!-- View Modal -->
    <TagViewModal
      v-if="showViewModal"
      :show="showViewModal"
      :tag="viewingTag"
      @close="showViewModal = false"
    />

    <!-- Delete Confirmation Modal -->
    <DeleteConfirmModal
      v-if="showDeleteModal"
      :show="showDeleteModal"
      :title="'Xóa Tag'"
      :message="`Bạn có chắc chắn muốn xóa tag '${deletingTag?.title}'? Hành động này không thể hoàn tác.`"
      @close="showDeleteModal = false"
      @confirm="confirmDelete"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { Button, Select, Badge, Dropdown, FeatherIcon, Breadcrumbs } from 'frappe-ui'
import { useTagStore } from '@/stores/tag'
import { useToast } from '@/composables/useToast'
import TagFormModal from '@/components/tag/TagFormModal.vue'
import TagViewModal from '@/components/tag/TagViewModal.vue'
import DeleteConfirmModal from '@/components/common/DeleteConfirmModal.vue'

// Composables
const router = useRouter()
const tagStore = useTagStore()
const toast = useToast()

// Reactive state
const searchText = ref('')
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showViewModal = ref(false)
const showDeleteModal = ref(false)
const editingTag = ref(null)
const viewingTag = ref(null)
const deletingTag = ref(null)

// Computed
const loading = computed(() => tagStore.loading)
const filteredTags = computed(() => tagStore.filteredTags)
const pagination = computed(() => tagStore.pagination)
const statistics = computed(() => tagStore.statistics)
const recentTagsCount = computed(() => tagStore.recentTags.length)

const hasActiveFilters = computed(() => {
  return searchText.value
})

// Methods
const loadTags = async (options = {}) => {
  try {
    await tagStore.fetchTags(options)
  } catch (error) {
    console.error('Error loading tags:', error)
    toast.error('Không thể tải danh sách tags')
  }
}

const loadStatistics = async () => {
  try {
    await tagStore.fetchStatistics()
  } catch (error) {
    console.error('Error loading statistics:', error)
  }
}

const refreshData = async () => {
  try {
    await Promise.all([
      loadTags({ page: 1 }),
      loadStatistics()
    ])
    toast.success(__('Refreshed successfully'))
  } catch (error) {
    console.error('Error refreshing data:', error)
    toast.error(__('Failed to refresh data'))
  }
}

const goToPage = (page) => {
  loadTags({ page })
}

const clearAllFilters = () => {
  searchText.value = ''
  tagStore.clearFilters()
  loadTags({ page: 1 })
}

const getActionOptions = (tag) => {
  return [
    {
      label: __('View'),
      icon: 'eye',
      onClick: () => viewTag(tag)
    },
    {
      label: __('Edit'),
      icon: 'edit',
      onClick: () => editTag(tag)
    },
    {
      label: __('Duplicate'),
      icon: 'copy',
      onClick: () => duplicateTag(tag)
    },
    {
      label: __('Delete'),
      icon: 'trash-2',
      onClick: () => deleteTag(tag),
      class: 'text-red-600'
    }
  ]
}

const viewTag = async (tag) => {
  try {
    const result = await tagStore.getTag(tag.name)
    if (result.success) {
      viewingTag.value = result.data
      showViewModal.value = true
    } else {
      toast.error(result.error || 'Không thể tải chi tiết tag')
    }
  } catch (error) {
    console.error('Error loading tag details:', error)
    toast.error('Có lỗi xảy ra khi tải chi tiết tag')
  }
}

const editTag = async (tag) => {
  try {
    console.log('editTag called with:', tag)
    const result = await tagStore.getTag(tag.name)
    console.log('getTag result:', result)
    if (result.success) {
      editingTag.value = result.data
      console.log('editingTag set to:', editingTag.value)
      // Đợi một tick để đảm bảo editingTag được set trước khi mở modal
      await nextTick()
      showEditModal.value = true
      console.log('Modal opened')
    } else {
      toast.error(result.error || 'Không thể tải chi tiết tag')
    }
  } catch (error) {
    console.error('Error loading tag details:', error)
    toast.error('Có lỗi xảy ra khi tải chi tiết tag')
  }
}

const deleteTag = (tag) => {
  deletingTag.value = tag
  showDeleteModal.value = true
}

const duplicateTag = async (tag) => {
  try {
    const result = await tagStore.duplicateTag(tag.name)
    if (result.success) {
      toast.success(__('Duplicated tag successfully'))
      await loadTags()
    } else {
      toast.error(result.error || __('Failed to duplicate tag'))
    }
  } catch (error) {
    console.error('Error duplicating tag:', error)
    toast.error(__('Failed to duplicate tag'))
  }
}

const confirmDelete = async () => {
  try {
    const result = await tagStore.deleteTag(deletingTag.value.name)
    if (result.success) {
      toast.success(`Đã xóa tag "${deletingTag.value.title}" thành công`)
      await loadTags()
      await loadStatistics()
    } else {
      toast.error(result.error || __('Failed to delete tag'))
    }
  } catch (error) {
    console.error('Error deleting tag:', error)
    toast.error(__('Failed to delete tag'))
  } finally {
    showDeleteModal.value = false
    deletingTag.value = null
  }
}

// Move tag order functions
const isFirstTag = (tag) => {
  const sortedTags = [...filteredTags.value].sort((a, b) => (a.order || 0) - (b.order || 0))
  return sortedTags[0]?.name === tag.name
}

const isLastTag = (tag) => {
  const sortedTags = [...filteredTags.value].sort((a, b) => (a.order || 0) - (b.order || 0))
  return sortedTags[sortedTags.length - 1]?.name === tag.name
}

const moveTagUp = async (tag) => {
  try {
    const sortedTags = [...filteredTags.value].sort((a, b) => (a.order || 0) - (b.order || 0))
    const currentIndex = sortedTags.findIndex(t => t.name === tag.name)
    
    if (currentIndex > 0) {
      const prevTag = sortedTags[currentIndex - 1]
      const tempOrder = tag.order
      
      // Swap orders
      await tagStore.updateTag(tag.name, { ...tag, order: prevTag.order })
      await tagStore.updateTag(prevTag.name, { ...prevTag, order: tempOrder })
      
      await loadTags()
      toast.success(__('Moved tag up'))
    }
  } catch (error) {
    console.error('Error moving tag up:', error)
    toast.error(__('Failed to move tag up'))
  }
}

const moveTagDown = async (tag) => {
  try {
    const sortedTags = [...filteredTags.value].sort((a, b) => (a.order || 0) - (b.order || 0))
    const currentIndex = sortedTags.findIndex(t => t.name === tag.name)
    
    if (currentIndex < sortedTags.length - 1) {
      const nextTag = sortedTags[currentIndex + 1]
      const tempOrder = tag.order
      
      // Swap orders
      await tagStore.updateTag(tag.name, { ...tag, order: nextTag.order })
      await tagStore.updateTag(nextTag.name, { ...nextTag, order: tempOrder })
      
      await loadTags()
      toast.success(__('Moved tag down'))
    }
  } catch (error) {
    console.error('Error moving tag down:', error)
    toast.error(__('Failed to move tag down'))
  }
}

const closeModals = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingTag.value = null
}

const handleFormSuccess = async (message) => {
  toast.success(message)
  closeModals()
  await loadTags()
  await loadStatistics()
}

// Watchers
watch(searchText, (newValue) => {
  tagStore.setSearch(newValue)
  loadTags({ page: 1 })
}, { debounce: 300 })


// Lifecycle
onMounted(async () => {
  await Promise.all([
    loadTags(),
    loadStatistics()
  ])
})
</script>
