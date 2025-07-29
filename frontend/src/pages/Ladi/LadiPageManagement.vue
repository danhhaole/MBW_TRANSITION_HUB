<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Page Header -->
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header>
        <!-- Create button -->
        <Button variant="solid" theme="gray" @click="handleCreate" :loading="store.loading">
          <template #prefix>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
          </template>
          {{ __('Create Ladi Page') }}
        </Button>
      </template>
    </LayoutHeader>

    <!-- Filters & Controls -->
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <div class="bg-white rounded-lg shadow-sm p-4 mb-4">
        <div class="flex flex-wrap gap-4 items-center justify-between">
          <!-- Search -->
          <div class="flex-1 min-w-[200px]">
            <FormControl
              type="text"
              :placeholder="__('Search Ladi pages...')"
              v-model="store.filters.search"
              @input="handleSearch"
            />
          </div>

          <!-- Filters -->
          <div class="flex flex-wrap gap-4">
            <Select
              v-model="store.filters.status"
              :options="store.statusOptions"
              @change="store.setStatusFilter"
              class="w-40"
            />
            <Select
              v-model="store.filters.campaign"
              :options="campaignOptions"
              @change="store.setCampaignFilter"
              class="w-48"
            />
          </div>

          <!-- Refresh Button -->
          <Button variant="outline" theme="gray" @click="handleRefresh" :loading="refreshing">
            <template #prefix>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </template>
            {{ __('Refresh') }}
          </Button>
        </div>
      </div>

      <!-- Main content -->
      <div class="bg-white rounded-lg shadow-sm">
        <Loading v-if="store.loading" text="Loading Ladi pages..." />

        <!-- Data Table -->
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ __('Title') }}
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ __('Route') }}
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ __('Campaign') }}
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ __('Status') }}
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ __('Created') }}
                </th>
                <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ __('Actions') }}
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="!store.ladiPages.length" class="text-center">
                <td colspan="6" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ __('No Ladi pages found') }}
                </td>
              </tr>
              <tr v-for="page in store.ladiPages" :key="page.name" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">{{ page.title }}</div>
                  <div class="text-sm text-gray-500">{{ page.description }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ page.route }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ page.campaign || __('None') }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                    :class="{
                      'bg-green-100 text-green-800': page.status === 'Published',
                      'bg-yellow-100 text-yellow-800': page.status === 'Draft',
                      'bg-gray-100 text-gray-800': page.status === 'Archived'
                    }"
                  >
                    {{ page.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDate(page.creation) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div class="flex justify-end space-x-2">
                    <Button
                      variant="outline"
                      theme="gray"
                      size="sm"
                      @click="handleEdit(page)"
                      :title="__('Edit')"
                    >
                      <template #prefix>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </template>
                    </Button>
                    <Button
                      variant="outline"
                      theme="red"
                      size="sm"
                      @click="handleDelete(page)"
                      :title="__('Delete')"
                    >
                      <template #prefix>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </template>
                    </Button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="store.pagination.total > store.pagination.limit" class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
          <div class="flex items-center justify-between">
            <div class="flex-1 flex justify-between sm:hidden">
              <Button
                variant="outline"
                theme="gray"
                @click="store.setPage(store.pagination.page - 1)"
                :disabled="store.pagination.page === 1"
              >
                {{ __('Previous') }}
              </Button>
              <Button
                variant="outline"
                theme="gray"
                @click="store.setPage(store.pagination.page + 1)"
                :disabled="store.pagination.page === store.pagination.pages"
              >
                {{ __('Next') }}
              </Button>
            </div>
            <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p class="text-sm text-gray-700">
                  {{ __('Showing') }}
                  <span class="font-medium">{{ ((store.pagination.page - 1) * store.pagination.limit) + 1 }}</span>
                  {{ __('to') }}
                  <span class="font-medium">{{ Math.min(store.pagination.page * store.pagination.limit, store.pagination.total) }}</span>
                  {{ __('of') }}
                  <span class="font-medium">{{ store.pagination.total }}</span>
                  {{ __('results') }}
                </p>
              </div>
              <div>
                <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                  <Button
                    variant="outline"
                    theme="gray"
                    @click="store.setPage(store.pagination.page - 1)"
                    :disabled="store.pagination.page === 1"
                    class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  >
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </Button>
                  <Button
                    variant="outline"
                    theme="gray"
                    @click="store.setPage(store.pagination.page + 1)"
                    :disabled="store.pagination.page === store.pagination.pages"
                    class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  >
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                    </svg>
                  </Button>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <LadiPageFormModal
      v-if="showFormModal"
      v-model="showFormModal"
      :page="selectedPage"
      @saved="handleSaved"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Button, FormControl, Select, Breadcrumbs } from 'frappe-ui'
import { useToast } from '@/composables/useToast'
import { useLadiPageStore } from '@/stores/ladiPage'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Loading from '@/components/Loading.vue'
import LadiPageFormModal from './LadiPageFormModal.vue'

// Initialize store
const store = useLadiPageStore()

// Toast notifications
const { showSuccess, showError } = useToast()

// Page setup
const title = 'Ladi Pages'
const breadcrumbs = [{ label: __('Ladi Pages'), route: { name: 'ladi-pages' } }]

// Reactive state
const refreshing = ref(false)
const showFormModal = ref(false)
const selectedPage = ref(null)
const campaignOptions = ref([
  { label: __('All Campaigns'), value: 'all' }
])

// Load campaign options
const loadCampaignOptions = async () => {
  try {
    const options = await store.fetchCampaignOptions()
    campaignOptions.value = [
      { label: __('All Campaigns'), value: 'all' },
      ...options
    ]
  } catch (error) {
    console.error('Error loading campaign options:', error)
  }
}

// Format date helper
const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

// Handlers
const handleSearch = (value) => {
  store.setSearchFilter(value)
}

const handleCreate = () => {
  selectedPage.value = null
  showFormModal.value = true
}

const handleEdit = (page) => {
  selectedPage.value = page
  showFormModal.value = true
}

const handleDelete = async (page) => {
  if (!confirm(__(`Are you sure you want to delete "${page.title}"?`))) return

  try {
    await store.deleteLadiPage(page.name)
    showSuccess(__('Ladi page deleted successfully'))
  } catch (error) {
    showError(__('Failed to delete Ladi page'))
  }
}

const handleSaved = () => {
  showFormModal.value = false
  store.fetchLadiPages()
  showSuccess(__('Ladi page saved successfully'))
}

const handleRefresh = async () => {
  refreshing.value = true
  await store.fetchLadiPages()
  refreshing.value = false
  showSuccess(__('Data refreshed'))
}

// Initialize
onMounted(async () => {
  await loadCampaignOptions()
  await store.fetchLadiPages()
})
</script>