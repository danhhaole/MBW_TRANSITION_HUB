<template>
  <div class="space-y-2">
    <!-- Display selected tags as chips -->
    <div v-if="selectedTags.length > 0" class="flex flex-wrap gap-2">
      <span 
        v-for="(tag, index) in selectedTags" 
        :key="index"
        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800"
      >
        {{ tag }}
        <button 
          type="button" 
          @click="removeTag(index)"
          class="ml-1.5 h-4 w-4 rounded-full inline-flex items-center justify-center text-purple-400 hover:bg-purple-200 hover:text-purple-500 focus:outline-none"
        >
          <svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
            <path stroke-linecap="round" stroke-width="1.5" d="m1 1 6 6m0-6-6 6" />
          </svg>
        </button>
      </span>
    </div>

    <!-- Tag selection dropdown + Create button -->
    <div class="flex gap-2">
      <div class="flex-1">
        <Autocomplete
          :options="availableTags"
          v-model="selectedTagToAdd"
          :placeholder="__('Select a tag...')"
          @update:modelValue="addSelectedTag"
        />
      </div>
      
      <Button
        @click="showCreateModal = true"
        icon="plus"
        variant="solid"
      >
        {{ __('New') }}
      </Button>
    </div>

    <!-- <p class="text-xs text-gray-500">
      {{ __('Select existing tags or create new ones') }}
    </p> -->

    <!-- Create Tag Modal -->
    <Dialog v-model="showCreateModal" :options="{ title: __('Create New Tag'), size: 'sm' }">
      <template #body-content>
        <div class="">
          <label class="block text-sm font-medium text-gray-700">
            {{ __('Tag Name') }}
          </label>
          <input
            v-model="newTagName"
            type="text"
            :placeholder="__('Enter tag name...')"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
            @keydown.enter="createTag"
          />
        </div>
      </template>
      <template #actions>
        <div class="flex justify-end gap-2">
          <Button variant="outline" @click="showCreateModal = false">
            {{ __('Cancel') }}
          </Button>
          <Button 
            variant="solid" 
            theme="gray"
            @click="createTag"
            :loading="creatingTag"
            :disabled="!newTagName.trim()"
          >
            {{ __('Create') }}
          </Button>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { Dialog, Button, Autocomplete } from 'frappe-ui'
import { call } from 'frappe-ui'
import { useToast } from '@/composables/useToast'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const { showSuccess, showError } = useToast()

// Local state
const selectedTags = ref([])
const allTags = ref([])
const selectedTagToAdd = ref(null)
const showCreateModal = ref(false)
const newTagName = ref('')
const creatingTag = ref(false)

// Computed
const availableTags = computed(() => {
  return allTags.value
    .filter(tag => !selectedTags.value.includes(tag.title))
    .map(tag => ({
      label: tag.title,
      value: tag.title
    }))
})

// Methods
const loadTags = async () => {
  try {
    const result = await call('frappe.client.get_list', {
      doctype: 'Mira Tag',
      fields: ['name', 'title'],
      limit_page_length: 1000,
      order_by: 'title asc'
    })
    
    if (result && result.length) {
      allTags.value = result.map(tag => ({
        name: tag.name,
        title: tag.title || tag.name
      }))
    }
  } catch (error) {
    console.error('Error loading tags:', error)
  }
}

const addSelectedTag = (tag) => {
  // tag có thể là object {label, value} hoặc string
  const tagValue = typeof tag === 'object' ? tag?.value : tag
  
  if (tagValue && !selectedTags.value.includes(tagValue)) {
    selectedTags.value.push(tagValue)
    selectedTagToAdd.value = null
    emitValue()
  }
}

const removeTag = (index) => {
  selectedTags.value.splice(index, 1)
  emitValue()
}

const createTag = async () => {
  if (!newTagName.value.trim()) return
  
  creatingTag.value = true
  try {
    const result = await call('frappe.client.insert', {
      doc: {
        doctype: 'Mira Tag',
        title: newTagName.value.trim()
      }
    })
    
    if (result && result.name) {
      const newTag = {
        name: result.name,
        title: result.title || newTagName.value.trim()
      }
      
      // Add to tags list
      allTags.value.push(newTag)
      
      // Add to selected tags
      selectedTags.value.push(newTag.title)
      
      showSuccess(__('Tag created successfully'))
      showCreateModal.value = false
      newTagName.value = ''
      emitValue()
    }
  } catch (error) {
    console.error('Error creating tag:', error)
    showError(error.message || __('Failed to create tag'))
  } finally {
    creatingTag.value = false
  }
}

const emitValue = () => {
  const value = selectedTags.value.join(', ')
  emit('update:modelValue', value)
  emit('change', value)
}

const parseValue = (value) => {
  if (!value) {
    selectedTags.value = []
    return
  }
  
  selectedTags.value = value
    .split(',')
    .map(tag => tag.trim())
    .filter(tag => tag.length > 0)
}

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  const currentValue = selectedTags.value.join(', ')
  if (newValue !== currentValue) {
    parseValue(newValue)
  }
}, { immediate: true })

// Load tags on mount
onMounted(() => {
  loadTags()
})
</script>

<style scoped>
/* Add any custom styles if needed */
</style>
