<template>
  <Dialog v-model="dialogVisible" :options="{ size: '4xl' }">
    <template #body-title>
      <h3 class="text-lg font-semibold text-gray-900">
        {{ __('Select Published Landing Page') }}
      </h3>
    </template>

    <template #body-content>
      <div class="space-y-4">
        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-12">
          <div class="text-center">
            <FeatherIcon name="loader" class="h-8 w-8 text-gray-400 animate-spin mx-auto mb-3" />
            <p class="text-sm text-gray-500">{{ __('Loading published pages...') }}</p>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="text-center py-12">
          <FeatherIcon name="alert-circle" class="h-12 w-12 text-red-400 mx-auto mb-4" />
          <h3 class="text-lg font-medium text-gray-900 mb-2">
            {{ __('Failed to Load Pages') }}
          </h3>
          <p class="text-sm text-gray-500 mb-4">
            {{ error }}
          </p>
          <Button @click="$emit('retry')" variant="solid">
            {{ __('Try Again') }}
          </Button>
        </div>

        <!-- Empty State -->
        <div v-else-if="!pages || pages.length === 0" class="text-center py-12">
          <FeatherIcon name="file-text" class="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 class="text-lg font-medium text-gray-900 mb-2">
            {{ __('No Published Pages') }}
          </h3>
          <p class="text-sm text-gray-500">
            {{ __('There are no published landing pages available to select from.') }}
          </p>
        </div>

        <!-- Pages Grid -->
        <div v-else>
          <div class="mb-4">
            <p class="text-sm text-gray-600">
              {{ __('Choose from {0} published landing pages', [pages.length]) }}
            </p>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-h-96 overflow-y-auto">
            <div
              v-for="page in pages"
              :key="page.name"
              @click="selectPage(page)"
              class="border border-gray-200 rounded-lg p-3 hover:border-purple-400 hover:shadow-md cursor-pointer transition-all group"
            >
              <!-- Preview Image -->
              <div class="aspect-video bg-gray-100 rounded-md mb-3 overflow-hidden">
                <img
                  v-if="page.url_preview && page.url_preview !== 'https://builder.mbwcloud.com/assets/builder/images/fallback.png'"
                  :src="page.url_preview"
                  :alt="page.title"
                  class="w-full h-full object-cover"
                  @error="handleImageError"
                />
                <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-purple-100 to-blue-100">
                  <FeatherIcon name="layout" class="h-8 w-8 text-purple-400" />
                </div>
              </div>
              
              <!-- Page Info -->
              <div class="space-y-2">
                <h4 class="text-sm font-medium text-gray-900 truncate group-hover:text-purple-600 transition-colors">
                  {{ page.title }}
                </h4>
                <p class="text-xs text-gray-500 truncate">
                  {{ page.router }}
                </p>
                <div class="flex items-center justify-between">
                  <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    <FeatherIcon name="globe" class="h-3 w-3 mr-1" />
                    {{ __('Published') }}
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    class="opacity-0 group-hover:opacity-100 transition-opacity"
                    @click.stop="previewPage(page)"
                  >
                    <template #prefix>
                      <FeatherIcon name="external-link" class="h-3 w-3" />
                    </template>
                    {{ __('Preview') }}
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <template #actions>
      <div class="flex justify-end gap-2">
        <Button variant="ghost" @click="$emit('close')">
          {{ __('Cancel') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { computed } from 'vue'
import { FeatherIcon, Button, Dialog } from 'frappe-ui'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  pages: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['close', 'select', 'retry'])

// Computed for v-model dialog visibility
const dialogVisible = computed({
  get: () => props.show,
  set: (value) => {
    if (!value) {
      emit('close')
    }
  }
})

const selectPage = (page) => {
  emit('select', page)
  emit('close')
}

const previewPage = (page) => {
  if (page.router) {
    window.open(page.router, '_blank', 'noopener,noreferrer')
  }
}

const handleImageError = (event) => {
  event.target.style.display = 'none'
}
</script>

<style scoped>
/* Custom scrollbar for the grid */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
