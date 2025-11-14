<template>
  <Dialog
    v-model="isOpen"
    :options="{
      title: __('Choose Landing Page Template'),
      size: '5xl'
    }"
  >
    <template #body-title>
      <div>
        <h3 class="text-lg font-semibold text-gray-900">
          {{ __('Choose Landing Page Template') }}
        </h3>
        <p class="text-sm text-gray-500 mt-1">
          {{ __('Select a template for your recruitment campaign') }}
        </p>
      </div>
    </template>

    <template #body-content>

      <div class="overflow-y-auto max-h-[70vh] p-1">
        <!-- Loading State -->
        <div v-if="loading" class="flex flex-col items-center justify-center py-12">
          <FeatherIcon name="loader" class="h-12 w-12 text-blue-600 animate-spin mb-4" />
          <p class="text-gray-600">{{ __('Loading templates...') }}</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="flex flex-col items-center justify-center py-12">
          <FeatherIcon name="alert-circle" class="h-12 w-12 text-red-600 mb-4" />
          <p class="text-red-600 mb-4">{{ error }}</p>
          <Button
            @click="$emit('retry')"
            variant="solid"
          >
            {{ __('Retry') }}
          </Button>
        </div>

        <!-- Templates Grid -->
        <div v-else-if="templates.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="template in templates"
              :key="template.name"
              class="group border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-all cursor-pointer"
              :class="{ 'ring-2 ring-blue-500': selectedTemplate === template.name }"
              @click="selectTemplate(template)"
            >
              <!-- Preview Image -->
              <div class="relative aspect-video bg-gray-100 overflow-hidden">
                <img
                  v-if="template.preview"
                  :src="template.preview"
                  :alt="template.page_title"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  @error="handleImageError"
                />
                <div v-else class="w-full h-full flex items-center justify-center">
                  <FeatherIcon name="image" class="h-12 w-12 text-gray-400" />
                </div>
                
                <!-- Preview Button Overlay -->
                <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all flex items-center justify-center">
                  <Button
                    @click.stop="openPreview(template)"
                    variant="solid"
                    class="opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    <template #prefix>
                      <FeatherIcon name="external-link" class="h-4 w-4" />
                    </template>
                    {{ __('Preview') }}
                  </Button>
                </div>
                
                <!-- Selected Badge -->
                <div
                  v-if="selectedTemplate === template.name"
                  class="absolute top-2 right-2 bg-blue-600 text-white px-3 py-1 rounded-full text-xs font-medium flex items-center z-10"
                >
                  <FeatherIcon name="check" class="h-3 w-3 mr-1" />
                  {{ __('Selected') }}
                </div>
              </div>

              <!-- Template Info -->
              <div class="p-4">
                <div class="flex items-start justify-between mb-2">
                  <h4 class="font-semibold text-gray-900 line-clamp-2 flex-1">
                    {{ template.page_title || template.name }}
                  </h4>
                </div>
                <p class="text-xs text-gray-500 line-clamp-1 mb-3">
                  {{ template.route }}
                </p> 
              </div>
            </div>
          </div>

        <!-- Empty State -->
        <div v-else class="flex flex-col items-center justify-center py-12">
          <FeatherIcon name="inbox" class="h-12 w-12 text-gray-400 mb-4" />
          <p class="text-gray-600">{{ __('No templates available') }}</p>
        </div>
      </div>
    </template>

    <template #actions>
      <div class="flex items-center justify-between w-full">
        <div class="text-sm text-gray-600">
          <span v-if="selectedTemplate">
            {{ __('1 template selected') }}
          </span>
          <span v-else>
            {{ __('Please select a template') }}
          </span>
        </div>
        <div class="flex gap-3">
          <Button
            @click="closeDialog"
            variant="ghost"
          >
            {{ __('Cancel') }}
          </Button>
          <Button
            @click="confirmSelection"
            :disabled="!selectedTemplate"
            variant="solid"
          >
            {{ __('Confirm Selection') }}
          </Button>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Dialog, Button, FeatherIcon } from 'frappe-ui'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  templates: {
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
  },
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['close', 'select', 'retry', 'update:modelValue'])

const isOpen = ref(props.show)
const selectedTemplate = ref(props.modelValue)
const dataSelectedTemplate = ref(null)

// Watch show prop to sync with isOpen
watch(() => props.show, (newVal) => {
  isOpen.value = newVal
})

// Watch isOpen to emit close event
watch(isOpen, (newVal) => {
  if (!newVal) {
    emit('close')
  }
})

const selectTemplate = (template) => {
  selectedTemplate.value = template.name
  dataSelectedTemplate.value = template
}

const closeDialog = () => {
  isOpen.value = false
}

const confirmSelection = () => {
  if (selectedTemplate.value) {
    emit('update:modelValue', selectedTemplate.value)
    emit('select', selectedTemplate.value, dataSelectedTemplate.value)
    closeDialog()
  }
}

const openPreview = (template) => {
  if (template.route) {
    window.open(template.route, '_blank', 'noopener,noreferrer')
  }
}

const handleImageError = (event) => {
  event.target.style.display = 'none'
}
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
