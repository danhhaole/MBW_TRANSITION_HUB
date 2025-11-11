<template>
  <Dialog
    :options="{
      title: __('Choose Template'),
      size: '5xl',
    }"
    v-model="show"
  >
    <template #body-content>
      <div class="">
        <!-- Search and Filters -->
        <div class="border-b border-gray-200 p-4 bg-gray-50">
          <div class="flex items-center gap-4">
            <!-- Search Box -->
            <div class="flex-1">
              <FormControl
                v-model="searchText"
                type="text"
                placeholder="Search templates..."
              >
                <template #prefix>
                  <FeatherIcon name="search" class="h-4 w-4 text-gray-400" />
                </template>
              </FormControl>
            </div>

            <!-- Channel Filter -->
            <div class="">
              <Select
                v-model="selectedChannel"
                :options="channelOptions"
                
              />
            </div>

            <!-- Show Recommended Only -->
            <div class="whitespace-nowrap">
              <Checkbox
                v-model="showRecommendedOnly"
                :label="__('Recommended only')"
              />
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-12">
          <FeatherIcon name="loader" class="h-8 w-8 animate-spin text-gray-400" />
          <span class="ml-3 text-gray-500">{{ __('Loading templates...') }}</span>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="text-center py-12">
          <FeatherIcon name="alert-circle" class="h-12 w-12 mx-auto mb-4 text-red-500" />
          <p class="text-red-600">{{ error }}</p>
        </div>

        <!-- Templates Grid -->
        <div v-else-if="filteredTemplates.length > 0" class="p-4 max-h-[calc(85vh-200px)] overflow-y-auto">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
            <div
              v-for="template in paginatedTemplates"
              :key="template.name"
              @click="selectTemplate(template)"
              class="group relative cursor-pointer rounded-lg border border-gray-200 overflow-hidden transition-all hover:shadow-lg hover:border-blue-500"
            >
            <!-- Template Preview Image -->
            <div class="relative h-36 bg-gray-100 overflow-hidden">
              <img
                v-if="template.thumbnail"
                :src="template.thumbnail"
                :alt="template.name_template"
                class="w-full h-full object-cover"
              />
              <div v-else class="flex items-center justify-center h-full">
                <FeatherIcon name="layout" class="h-16 w-16 text-gray-300" />
              </div>
              
              <!-- Recommended Badge -->
              <div
                v-if="template.is_suggestion"
                class="absolute top-3 right-3 bg-green-500 text-white text-xs font-medium px-2 py-1 rounded"
              >
                {{ __("Recommended") }}
              </div>

              <!-- Premium Badge -->
              <div
                v-if="template.is_premium"
                class="absolute top-3 left-3 bg-yellow-500 text-white text-xs font-medium px-2 py-1 rounded"
              >
                {{ __("Premium") }}
              </div>
            </div>

            <!-- Template Info -->
            <div class="p-4">
              <h3 class="font-semibold text-gray-900 mb-1 line-clamp-1">
                {{ template.name_template }}
              </h3>
              <p class="text-sm text-gray-600 mb-3 line-clamp-2">
                {{ template.description || __("No description") }}
              </p>

              <!-- Template Type Badges -->
              <div class="flex items-center gap-2 flex-wrap">
                <!-- Channel Badge -->
                <span
                  v-if="template.channel"
                  class="inline-flex items-center px-2 py-1 rounded text-xs font-medium"
                  :class="getChannelBadgeClass(template.channel)"
                >
                  <FeatherIcon :name="getChannelIcon(template.channel)" class="h-3 w-3 mr-1" />
                  {{ template.channel }}
                </span>
              </div>
            </div>

            <!-- Hover Overlay -->
            <div class="absolute inset-0 bg-blue-500 bg-opacity-0 group-hover:bg-opacity-10 transition-all pointer-events-none" />
            </div>
          </div>

          <!-- Pagination -->
        </div>
        <div v-if="totalPages > 1" class="flex items-center justify-between border-t border-gray-200 pt-4">
          <div class="text-sm text-gray-600">
            {{ __('Showing') }} {{ startIndex + 1 }} - {{ Math.min(endIndex, filteredTemplates.length) }} {{ __('of') }} {{ filteredTemplates.length }} {{ __('templates') }}
          </div>
          <div class="flex items-center gap-2">
            <button
              @click="currentPage--"
              :disabled="currentPage === 1"
              class="px-3 py-1 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <FeatherIcon name="chevron-left" class="h-4 w-4" />
            </button>
            <span class="text-sm text-gray-700">
              {{ __('Page') }} {{ currentPage }} {{ __('of') }} {{ totalPages }}
            </span>
            <button
              @click="currentPage++"
              :disabled="currentPage === totalPages"
              class="px-3 py-1 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <FeatherIcon name="chevron-right" class="h-4 w-4" />
            </button>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-12">
          <FeatherIcon name="inbox" class="h-12 w-12 mx-auto mb-4 text-gray-300" />
          <p class="text-gray-500">{{ __('No templates available') }}</p>
        </div>
      </div>
    </template>

    <template #actions>
      <div class="flex justify-end">
        <Button variant="outline" @click="handleClose">
          {{ __('Cancel') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { Dialog, Button, FeatherIcon, FormControl, Select, Checkbox } from 'frappe-ui'
import { createResource } from 'frappe-ui'
import { useToast } from '@/composables/useToast'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'select'])

const show = ref(props.modelValue)
const templates = ref([])
const loading = ref(false)
const error = ref(null)

// Filter states
const searchText = ref('')
const selectedChannel = ref('')
const showRecommendedOnly = ref(false)

// Channel options for Select component
const channelOptions = [
  { label: __('All Channels'), value: '' },
  { label: __('Email'), value: 'Email' },
  { label: __('Zalo ZNS'), value: 'Zalo_ZNS' },
  { label: __('Zalo OA'), value: 'Zalo_OA' },
  { label: __('SMS'), value: 'SMS' },
]

// Pagination states
const currentPage = ref(1)
const itemsPerPage = 6 // 3x3 grid

// Toast
const { info } = useToast()

// Filtered templates based on search and filters
const filteredTemplates = computed(() => {
  let filtered = templates.value

  // Filter by search text
  if (searchText.value) {
    const search = searchText.value.toLowerCase()
    filtered = filtered.filter(t => 
      t.name_template?.toLowerCase().includes(search) ||
      t.description?.toLowerCase().includes(search)
    )
  }

  // Filter by channel
  if (selectedChannel.value) {
    filtered = filtered.filter(t => t.channel === selectedChannel.value)
  }

  // Filter by recommended
  if (showRecommendedOnly.value) {
    filtered = filtered.filter(t => t.is_suggestion)
  }

  return filtered
})

// Pagination computed properties
const totalPages = computed(() => Math.ceil(filteredTemplates.value.length / itemsPerPage))
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage)
const endIndex = computed(() => startIndex.value + itemsPerPage)
const paginatedTemplates = computed(() => 
  filteredTemplates.value.slice(startIndex.value, endIndex.value)
)

// Reset pagination when filters change
watch([searchText, selectedChannel, showRecommendedOnly], () => {
  currentPage.value = 1
})

// Frappe resource to fetch templates
const templatesResource = createResource({
  url: 'frappe.client.get_list',
  params: {
    doctype: 'Mira Flow Template',
    fields: [
      'name',
      'name_template',
      'description',
      'channel',
      'is_suggestion',
      'is_premium',
      'thumbnail'
    ],
    filters: {},
    order_by: 'is_suggestion desc, modified desc',
    limit_page_length: 50
  },
  auto: false,
  onSuccess(data) {
    templates.value = data || []
    loading.value = false
  },
  onError(err) {
    console.error('Error loading templates:', err)
    error.value = 'Failed to load templates'
    loading.value = false
  }
})

watch(() => props.modelValue, (newVal) => {
  show.value = newVal
  if (newVal) {
    loadTemplates()
  }
})

watch(show, (newVal) => {
  emit('update:modelValue', newVal)
})

const loadTemplates = async () => {
  loading.value = true
  error.value = null
  templatesResource.fetch()
}

const selectTemplate = (template) => {
  // Show "Feature in development" message
  info(
    __('This feature will be available soon'),
    { duration: 5000 }
  )
  
  // Uncomment when ready to implement
  // emit('select', template)
  // show.value = false
}

const handleClose = () => {
  show.value = false
}

const getChannelIcon = (channel) => {
  const iconMap = {
    'Email': 'mail',
    'Zalo_ZNS': 'message-square',
    'Zalo_OA': 'message-circle',
    'SMS': 'message-square',
  }
  return iconMap[channel] || 'send'
}

const getChannelBadgeClass = (channel) => {
  const classMap = {
    'Email': 'bg-blue-100 text-blue-700',
    'Zalo_ZNS': 'bg-green-100 text-green-700',
    'Zalo_OA': 'bg-purple-100 text-purple-700',
    'SMS': 'bg-orange-100 text-orange-700',
  }
  return classMap[channel] || 'bg-gray-100 text-gray-700'
}
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>