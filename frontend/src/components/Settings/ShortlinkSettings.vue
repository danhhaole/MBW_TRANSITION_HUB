<template>
  <div class="flex h-full flex-col overflow-hidden">
    <!-- Header -->
    <div class="px-6 py-4 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold text-gray-900">{{ __('Shortlinks') }}</h2>
          <p class="mt-1 text-sm text-gray-500">{{ __('Manage shortlinks for campaigns and communications.') }}</p>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="flex-1 overflow-auto px-6 py-4">
      <!-- Search and Actions -->
      <div class="flex items-center justify-between mb-4">
        <!-- Search box -->
        <div class="relative">
          <input
            v-model="searchText"
            type="text"
            :placeholder="__('Search shortlinks...')"
            class="block w-80 pl-10 pr-10 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            @input="handleSearchInput($event.target.value)"
          />
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <FeatherIcon name="search" class="h-5 w-5 text-gray-400" />
          </div>
          <button
            v-if="searchText"
            @click="handleClearSearch"
            class="absolute inset-y-0 right-0 pr-3 flex items-center"
          >
            <svg
              class="h-5 w-5 text-gray-400 hover:text-gray-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              ></path>
            </svg>
          </button>
        </div>

        <!-- Actions -->
        <div class="flex items-center gap-2">
          <Button
            variant="outline"
            @click="handleRefresh"
            :loading="loading"
          >
            <template #prefix>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4"
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
        </div>
      </div>

      <!-- Table -->
      <div class="bg-white rounded-lg border border-gray-200">
        <div v-if="filteredItems.length > 0" class="overflow-x-auto">
          <table class="min-w-full bg-white rounded-lg overflow-hidden">
            <thead class="bg-gray-100">
              <tr>
                <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">{{ __('Short Code') }}</th>
                <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">{{ __('Long URL') }}</th>
                <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">{{ __('Created By') }}</th>
                <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">{{ __('Created At') }}</th>
                <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">{{ __('Actions') }}</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr
                v-for="item in paginatedItems"
                :key="item.name"
                class="hover:bg-gray-50"
              >
                <!-- Short Code -->
                <td class="py-4 px-4">
                  <div
                    class="font-medium text-sm text-blue-600 hover:text-blue-800 cursor-pointer underline"
                    @click="handleShortLinkClick(item)"
                  >
                    {{ getShortUrlDisplay(getShortUrlFromCode(item.short_code)) }}
                  </div>
                </td>

                <!-- Long URL -->
                <td class="py-4 px-4">
                  <div class="text-sm text-gray-700 max-w-xs truncate">
                    {{ item.long_url }}
                  </div>
                </td>

                <!-- Created By -->
                <td class="py-4 px-4">
                  <div class="text-sm text-gray-700">
                    {{ item.modified_by || 'Admin' }}
                  </div>
                </td>

                <!-- Created At -->
                <td class="py-4 px-4">
                  <div class="text-sm text-gray-700">
                    {{ formatDate(item.creation) }}
                  </div>
                </td>

                <!-- Actions -->
                <td class="py-4 px-4">
                  <div class="flex items-center space-x-2">
                    <Button
                      @click="openView(item)"
                      variant="ghost"
                      size="sm"
                      class="text-gray-500 hover:text-gray-700"
                      :title="__('View Details')"
                    >
                      <FeatherIcon name="eye" class="h-4 w-4" />
                    </Button>
                    <Button
                      @click="openDelete(item)"
                      variant="ghost"
                      size="sm"
                      class="text-gray-500 hover:text-red-600 hover:bg-red-50"
                      :title="__('Delete')"
                    >
                      <FeatherIcon name="trash-2" class="h-4 w-4" />
                    </Button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="text-center py-12">
          <div class="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-4">
            <FeatherIcon name="link-2" class="h-8 w-8 text-gray-400" />
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">{{ __('No shortlinks found') }}</h3>
          <p class="text-gray-500 mb-4">{{ __('Create your first shortlink to get started') }}</p>
        </div>

        <!-- Pagination -->
        <div v-if="filteredItems.length > 0" class="flex items-center justify-between p-6 border-t border-gray-200">
          <div class="text-sm text-gray-600">
            {{ __('Showing') }} {{ (currentPage - 1) * pageSize + 1 }}-{{ Math.min(currentPage * pageSize, filteredItems.length) }} {{ __('of') }}
            <span class="font-medium">{{ filteredItems.length }}</span> {{ __('shortlinks') }}
          </div>
          <div class="flex space-x-1">
            <Button
              @click="currentPage--"
              :disabled="currentPage === 1"
              variant="outline"
              size="sm"
              class="px-3 py-1.5"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </Button>

            <template v-for="page in visiblePages" :key="page">
              <Button
                v-if="page === '...'"
                variant="ghost"
                size="sm"
                class="px-3 py-1.5"
                disabled
              >
                ...
              </Button>
              <Button
                v-else
                @click="currentPage = page"
                :variant="currentPage === page ? 'solid' : 'ghost'"
                :theme="currentPage === page ? 'gray' : 'gray'"
                size="sm"
                class="px-3 py-1.5"
              >
                {{ page }}
              </Button>
            </template>

            <Button
              @click="currentPage++"
              :disabled="currentPage >= totalPages"
              variant="outline"
              size="sm"
              class="px-3 py-1.5"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- View Modal -->
    <Dialog v-model="showView" :options="{ title: __('Shortlink Details'), size: '3xl' }">
      <template #body-content>
        <div v-if="viewData" class="divide-y divide-gray-200">
          <!-- Short Code -->
          <div class="py-4 px-6">
            <div class="flex items-center gap-2">
              <div class="flex-1">
                <dt class="text-sm font-medium text-gray-500 mb-1">{{ __('Short URL') }}</dt>
                <a
                  :href="getShortUrlFromCode(viewData.short_code)"
                  target="_blank"
                  class="text-sm font-mono text-blue-600 hover:underline"
                >
                  {{ getShortUrlFromCode(viewData.short_code) }}
                </a>
              </div>
            </div>
          </div>

          <!-- Long URL -->
          <div class="py-4 px-6">
            <dt class="text-sm font-medium text-gray-500 mb-1">{{ __('Long URL') }}</dt>
            <dd class="text-sm text-gray-900">
              <div class="flex items-center gap-2">
                <div class="flex-1">
                  <a
                    :href="viewData.long_url"
                    target="_blank"
                    class="text-blue-600 hover:underline block"
                  >
                    {{ truncateUrl(viewData.long_url, 120) }}
                  </a>
                </div>
              </div>
            </dd>
          </div>

          <!-- Created By -->
          <div class="py-4 px-6">
            <dt class="text-sm font-medium text-gray-500 mb-1">{{ __('Created By') }}</dt>
            <dd class="text-sm text-gray-900">{{ viewData.modified_by || viewData.owner || 'System' }}</dd>
          </div>

          <!-- Created At -->
          <div class="py-4 px-6">
            <dt class="text-sm font-medium text-gray-500 mb-1">{{ __('Created At') }}</dt>
            <dd class="text-sm text-gray-900">{{ formatDate(viewData.creation) }}</dd>
          </div>
        </div>
      </template>
    </Dialog>

    <!-- Delete Confirmation Dialog -->
    <Dialog v-model="showDelete" :options="{ title: __('Delete Shortlink'), size: 'sm' }">
      <template #body-content>
        <div class="p-4">
          <div class="flex flex-col items-center text-center">
            <div class="bg-red-50 rounded-full p-3 mb-4">
              <FeatherIcon name="alert-triangle" class="h-6 w-6 text-red-500" />
            </div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">{{ __('Delete Shortlink') }}</h3>
            <p class="text-gray-600 mb-6">
              {{ 'Any external links using this short URL will stop working.' }}
            </p>
          </div>
        </div>
      </template>
      <template #actions>
        <div class="w-full flex justify-end space-x-3">
          <Button variant="outline" @click="showDelete = false" class="px-4">
            {{ __('Cancel') }}
          </Button>
          <Button
            variant="solid"
            theme="red"
            @click="confirmDelete"
            :loading="deleting"
            class="px-4"
          >
            <template #prefix>
              <FeatherIcon name="trash-2" class="h-4 w-4" />
            </template>
            {{ deleting ? __('Deleting...') : __('Delete') }}
          </Button>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Button, Dialog, FeatherIcon } from 'frappe-ui'
import { call } from 'frappe-ui'
import { useToast } from '@/composables/useToast'
const toast = useToast()

const loading = ref(true)
const shortlinks = ref([])
const viewData = ref(null)
const showView = ref(false)
const showDelete = ref(false)
const deleting = ref(false)
const itemToDelete = ref(null)
const searchText = ref('')
const isSearching = ref(false)
let searchTimeout = null

// Debounced search function
const debouncedSearch = async (searchValue) => {
  clearTimeout(searchTimeout)

  if (!searchValue.trim()) {
    isSearching.value = false
    currentPage.value = 1
    return
  }

  isSearching.value = true

  searchTimeout = setTimeout(async () => {
    try {
      currentPage.value = 1
    } finally {
      isSearching.value = false
    }
  }, 300)
}

// Handle search input
const handleSearchInput = (value) => {
  searchText.value = value
  debouncedSearch(value)
}

// Clear search
const handleClearSearch = () => {
  searchText.value = ''
  currentPage.value = 1
}

const currentPage = ref(1)
const pageSize = ref(10)

// Computed properties
const filteredItems = computed(() => {
  if (!searchText.value.trim()) return shortlinks.value

  const query = searchText.value.toLowerCase().trim()
  return shortlinks.value.filter(
    item =>
      item.short_code?.toLowerCase().includes(query) ||
      item.long_url?.toLowerCase().includes(query) ||
      (item.modified_by || '').toLowerCase().includes(query) ||
      formatDate(item.creation).toLowerCase().includes(query)
  )
})

const totalPages = computed(() => {
  return Math.ceil(filteredItems.value.length / pageSize.value)
})

const paginatedItems = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredItems.value.slice(start, end)
})

const visiblePages = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  const range = []

  if (total <= 5) {
    for (let i = 1; i <= total; i++) {
      range.push(i)
    }
  } else {
    if (current <= 3) {
      range.push(1, 2, 3, 4, '...', total)
    } else if (current >= total - 2) {
      range.push(1, '...', total - 3, total - 2, total - 1, total)
    } else {
      range.push(1, '...', current - 1, current, current + 1, '...', total)
    }
  }

  return range
})

// Load shortlinks
async function handleRefresh() {
  await loadShortlinks()
  toast.success(__('Dữ liệu đã được cập nhật'), {
    position: 'top-center',
    timeout: 2000,
    closeOnClick: true,
    pauseOnHover: true
  })
}

async function loadShortlinks() {
  loading.value = true
  try {
    console.log('🔍 Loading shortlinks...')
    const data = await call('frappe.client.get_list', {
      doctype: 'Mira Short URL',
      fields: [
        'name',
        'short_code',
        'long_url',
        'creation',
        'modified_by'
      ],
      order_by: 'creation desc',
      limit: 1000
    })
    console.log('✅ Shortlinks loaded:', data)
    shortlinks.value = data || []
  } catch (error) {
    console.error('❌ Error loading shortlinks:', error)
    toast.error(__('Failed to load shortlinks: ') + (error.message || 'Unknown error'))
  } finally {
    loading.value = false
  }
}

// Utility functions
function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const year = date.getFullYear()
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${day}/${month}/${year} ${hours}:${minutes}`
}

function getShortUrlDisplay(shortUrl) {
  if (!shortUrl) return ''
  const maxLength = 40
  return shortUrl.length > maxLength
    ? `${shortUrl.substring(0, maxLength)}...`
    : shortUrl
}

function getShortUrlFromCode(shortCode) {
  if (!shortCode) return ''
  return `${shortCode}`
}

function handleShortLinkClick(item) {
    const shortUrl = getShortUrlFromCode(item.short_code)
    window.open(shortUrl, '_blank')
}

function truncateUrl(url, maxLength = 70) {
  if (!url) return ''
  if (url.length <= maxLength) return url

  const lastSlash = url.lastIndexOf('/', maxLength - 10)
  if (lastSlash > 0) {
    return url.substring(0, lastSlash) + '...'
  }

  return url.substring(0, maxLength - 3) + '...'
}

// Modal actions
function openView(item) {
  viewData.value = { ...item }
  showView.value = true
}

function openDelete(item) {
  itemToDelete.value = item
  showDelete.value = true
}

async function confirmDelete() {
  if (!itemToDelete.value) return

  try {
    deleting.value = true
    await call('frappe.client.delete', {
      doctype: 'Mira Short URL',
      name: itemToDelete.value.name
    })

    const index = shortlinks.value.findIndex(item => item.name === itemToDelete.value.name)
    if (index > -1) {
      shortlinks.value.splice(index, 1)
    }

    toast.success(__('Shortlink deleted successfully'))
    showDelete.value = false
    itemToDelete.value = null
  } catch (error) {
    console.error('Error deleting shortlink:', error)
    toast.error(error.message || __('Failed to delete shortlink'))
    showDelete.value = false
  } finally {
    deleting.value = false
  }
}

// Clean up on component unmount
onUnmounted(() => {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
})

onMounted(() => {
  loadShortlinks()
})
</script>

