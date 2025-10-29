<template>
  <div class="flex flex-col h-full">
    <!-- Header Section -->
    <div class="flex items-center justify-between px-6 py-5 border-b border-gray-200">
      <div>
        <h2 class="text-lg font-semibold text-gray-900">{{ __('Tags') }}</h2>
        <p class="mt-1 text-sm text-gray-500">
          {{ __('Manage tags to organize and categorize your contacts') }}
        </p>
      </div>
      <Button variant="solid" @click="showCreateModal = true">
        <template #prefix>
          <FeatherIcon name="plus" class="h-4 w-4" />
        </template>
        {{ __('New') }}
      </Button>
    </div>

    <!-- Content Section -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Search Bar -->
      <div class="px-6 py-4 border-b border-gray-200">
        <FormControl
          v-model="searchText"
          type="text"
          :placeholder="__('Search tags...')"
        >
          <template #prefix>
            <FeatherIcon name="search" class="w-4" />
          </template>
        </FormControl>
      </div>

      <!-- Tags List -->
      <div class="px-6 py-4 overflow-y-auto">
        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-12">
          <FeatherIcon name="loader" class="w-6 h-6 animate-spin text-gray-400" />
          <span class="ml-2 text-sm text-gray-500">{{ __('Loading...') }}</span>
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredTags.length === 0" class="text-center py-12">
          <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 mb-4">
            <FeatherIcon name="tag" class="h-8 w-8 text-gray-400" />
          </div>
          <h3 class="text-sm font-medium text-gray-900 mb-1">{{ __('No tags found') }}</h3>
          <p class="text-sm text-gray-500 mb-4">{{ __('Create your first tag to get started') }}</p>
          <Button variant="solid" size="sm" @click="showCreateModal = true">
            <template #prefix>
              <FeatherIcon name="plus" class="h-4 w-4" />
            </template>
            {{ __('Create Tag') }}
          </Button>
        </div>

        <!-- Tags Grid -->
        <div v-else class="grid grid-cols-1 gap-3 overflow-y-auto">
          <div
            v-for="tag in filteredTags"
            :key="tag.name"
            class="flex items-center justify-between p-4 bg-white border border-gray-200 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all"
          >
            <div class="flex items-center flex-1 min-w-0">
              <!-- Tag Icon with Color -->
              <div
                class="flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center"
                :style="{ backgroundColor: tag.color + '20', color: tag.color }"
              >
                <FeatherIcon name="tag" class="w-5 h-5" />
              </div>

              <!-- Tag Info -->
              <div class="ml-4 flex-1 min-w-0">
                <div class="flex items-center space-x-2">
                  <h3 class="text-sm font-medium text-gray-900 truncate">{{ tag.title }}</h3>
                  <div
                    class="w-4 h-4 rounded-full border border-gray-200 flex-shrink-0"
                    :style="{ backgroundColor: tag.color }"
                  ></div>
                </div>
                <p class="text-xs text-gray-500 mt-0.5">{{ tag.name }}</p>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center space-x-2 ml-4">
              <Button
                variant="ghost"
                size="sm"
                @click="editTag(tag)"
                class="text-gray-600 hover:text-gray-900"
              >
                <FeatherIcon name="edit-2" class="w-4 h-4" />
              </Button>
              <Button
                variant="ghost"
                size="sm"
                @click="deleteTag(tag)"
                class="text-red-600 hover:text-red-700"
              >
                <FeatherIcon name="trash-2" class="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="pagination.total > pagination.limit" class="flex items-center justify-between mt-6 pt-4 border-t border-gray-200">
          <div class="text-xs text-gray-500">
            {{ __('Showing') }} {{ pagination.showing_from }} - {{ pagination.showing_to }} {{ __('of') }} {{ pagination.total }}
          </div>
          <div class="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              :disabled="!pagination.has_prev"
              @click="goToPage(pagination.page - 1)"
            >
              <FeatherIcon name="chevron-left" class="w-4 h-4" />
            </Button>
            <span class="text-xs text-gray-600">{{ pagination.page }}</span>
            <Button
              variant="outline"
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

    <!-- Modals -->
    <TagFormModal
      v-if="showCreateModal || showEditModal"
      :show="showCreateModal || showEditModal"
      :tag="editingTag"
      @close="closeModals"
      @success="handleFormSuccess"
    />

    <DeleteConfirmModal
      v-if="showDeleteModal"
      :show="showDeleteModal"
      :title="__('Delete Tag')"
      :message="`${__('Are you sure you want to delete tag')} '${deletingTag?.title}'? ${__('This action cannot be undone.')}`"
      @close="showDeleteModal = false"
      @confirm="confirmDelete"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { Button, FeatherIcon, FormControl } from 'frappe-ui'
import { useTagStore } from '@/stores/tag'
import { useToast } from '@/composables/useToast'
import { disableSettingModalOutsideClick } from '@/composables/settings'
import TagFormModal from '@/components/tag/TagFormModal.vue'
import DeleteConfirmModal from '@/components/common/DeleteConfirmModal.vue'
import { debounce } from 'lodash'

const tagStore = useTagStore()
const toast = useToast()

// State
const searchText = ref('')
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const editingTag = ref(null)
const deletingTag = ref(null)

// Computed
const loading = computed(() => tagStore.loading)
const filteredTags = computed(() => tagStore.filteredTags)
const pagination = computed(() => tagStore.pagination)

// Methods
const loadTags = async (options = {}) => {
  try {
    await tagStore.fetchTags(options)
  } catch (error) {
    console.error('Error loading tags:', error)
    toast.error(__('Failed to load tags'))
  }
}

const goToPage = (page) => {
  loadTags({ page })
}

const editTag = async (tag) => {
  try {
    const result = await tagStore.getTag(tag.name)
    if (result.success) {
      editingTag.value = result.data
      await nextTick()
      showEditModal.value = true
    } else {
      toast.error(result.error || __('Failed to load tag details'))
    }
  } catch (error) {
    console.error('Error loading tag details:', error)
    toast.error(__('Failed to load tag details'))
  }
}

const deleteTag = (tag) => {
  deletingTag.value = tag
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  try {
    const result = await tagStore.deleteTag(deletingTag.value.name)
    if (result.success) {
      toast.success(__('Tag deleted successfully'))
      await loadTags()
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

const closeModals = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingTag.value = null
  // Enable outside click when no child modal is open
  disableSettingModalOutsideClick.value = false
}

const handleFormSuccess = async (message) => {
  toast.success(message)
  closeModals()
  await loadTags()
}

// Debounced search
const debouncedSearch = debounce((searchValue) => {
  tagStore.setSearch(searchValue)
  loadTags({ page: 1 })
}, 300)

watch(searchText, (newValue) => {
  debouncedSearch(newValue)
})

// Watch modals to disable outside click when any modal is open
watch([showCreateModal, showEditModal, showDeleteModal], ([create, edit, del]) => {
  disableSettingModalOutsideClick.value = create || edit || del
})

// Lifecycle
onMounted(async () => {
  await loadTags()
})
</script>
