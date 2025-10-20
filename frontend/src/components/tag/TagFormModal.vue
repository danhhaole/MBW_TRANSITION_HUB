<template>
  <Dialog
    :model-value="show"
    @update:model-value="$emit('close')"
    :options="{
      title: isEditing ? __('Edit Tag') : __('Create New Tag'),
      size: 'md'
    }"
  >
    <template #body-content>
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Title -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ __('Tag Name') }} *
          </label>
          <input
            v-model="formData.title"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="{{ __('Enter tag name') }}..."
          />
        </div>

        <!-- Color -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ __('Color') }}
          </label>
          <div class="flex items-center space-x-3">
            <input
              v-model="formData.color"
              type="color"
              class="w-12 h-10 border border-gray-300 rounded cursor-pointer"
            />
            <input
              v-model="formData.color"
              type="text"
              class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="#3B82F6"
            />
          </div>
        </div>

        <!-- Order - Hidden, auto-managed -->
        <input
          v-model.number="formData.order"
          type="hidden"
        />

        <!-- Preview -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ __('Preview') }}
          </label>
          <div class="flex items-center p-3 border border-gray-200 rounded-md bg-gray-50">
            <div class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center mr-3"
                 :style="{ backgroundColor: formData.color + '20', color: formData.color }">
              <FeatherIcon name="tag" class="w-3 h-3" />
            </div>
            <span class="text-sm font-medium text-gray-900">
              {{ formData.title || __('Tag Name') }}
            </span>
          </div>
        </div>
      </form>
    </template>

    <template #actions>
      <Button
        variant="solid"
        theme="blue"
        :loading="loading"
        @click="handleSubmit"
      >
        {{ isEditing ?  __('Update') : __('Create') }}
      </Button>
      <Button
        variant="outline"
        theme="gray"
        @click="$emit('close')"
      >
        {{ __('Cancel') }}
      </Button>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Button, Dialog, FeatherIcon } from 'frappe-ui'
import { useTagStore } from '@/stores/tag'

// Props
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  tag: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['close', 'success'])

// Composables
const tagStore = useTagStore()

// Reactive state
const formData = ref({
  title: '',
  color: '#3B82F6',
  order: 0
})

// Computed
const loading = computed(() => tagStore.loading)
const isEditing = computed(() => !!props.tag)

// Methods
const resetForm = () => {
  formData.value = {
    title: '',
    color: '#3B82F6',
    order: tagStore.getNextOrder()
  }
}

const loadTagData = () => {
  console.log('loadTagData called with tag:', props.tag)
  if (props.tag) {
    console.log('Loading tag data:', props.tag)
    formData.value = {
      title: props.tag.title || '',
      color: props.tag.color || '#3B82F6',
      order: props.tag.order || 0
    }
    console.log('Form data set to:', formData.value)
  } else {
    console.log('Creating new tag form')
    // Khi tạo mới, sử dụng order tự động từ store
    formData.value = {
      title: '',
      color: '#3B82F6',
      order: tagStore.getNextOrder()
    }
  }
}

const handleSubmit = async () => {
  try {
    let result
    
    if (isEditing.value) {
      result = await tagStore.updateTag(props.tag.name, formData.value)
      if (result.success) {
        emit('success', __('Tag updated successfully'))
      }
    } else {
      result = await tagStore.createTag(formData.value)
      if (result.success) {
        emit('success', __('Tag created successfully'))
      }
    }
    
    if (!result.success) {
      throw new Error(result.error || __('An error occurred'))
    }
  } catch (error) {
    console.error('Error saving tag:', error)
    // Error will be handled by the store and displayed via toast
  }
}


// Watchers
watch(() => props.show, (newValue) => {
  if (newValue) {
    loadTagData()
  }
})

watch(() => props.tag, (newValue) => {
  console.log('Tag prop changed:', newValue)
  if (props.show) {
    loadTagData()
  }
}, { immediate: true })

// Also watch both show and tag together
watch([() => props.show, () => props.tag], ([show, tag]) => {
  console.log('Show/Tag changed:', { show, tag })
  if (show) {
    loadTagData()
  }
})
</script>
