<template>
  <Dialog
    :model-value="show"
    @update:model-value="$emit('close')"
    :options="{
      title: isEditing ? __('Edit Blacklist') : __('Add to Blacklist'),
      size: 'md'
    }"
  >
    <template #body-content>
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Email -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ __('Email') }} *
          </label>
          <input
            v-model="formData.email"
            type="email"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            :placeholder="__('Enter email address')"
          />
        </div>

        <!-- Tag -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ __('Tag') }}
          </label>
          <input
            v-model="formData.tag"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            :placeholder="__('Enter tag (optional)')"
          />
          <p class="mt-1 text-xs text-gray-500">
            {{ __('Add a tag to categorize this blacklist entry') }}
          </p>
        </div>

        <!-- Preview -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ __('Preview') }}
          </label>
          <div class="flex items-center p-3 border border-gray-200 rounded-md bg-gray-50">
            <div class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center mr-3 bg-red-100 text-red-600">
              <FeatherIcon name="slash" class="w-4 h-4" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate">
                {{ formData.email || __('email@example.com') }}
              </p>
              <p v-if="formData.tag" class="text-xs text-gray-500 truncate">
                {{ formData.tag }}
              </p>
            </div>
          </div>
        </div>
      </form>
    </template>

    <template #actions>
      <div class="flex items-center space-x-3 justify-end">
        <Button
          variant="outline"
          theme="gray"
          @click="$emit('close')"
        >
          {{ __('Cancel') }}
        </Button>
        <Button
          variant="solid"
          theme="gray"
          :loading="loading"
          @click="handleSubmit"
        >
          {{ isEditing ? __('Update') : __('Add') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Button, Dialog, FeatherIcon } from 'frappe-ui'
import { useBlacklistStore } from '@/stores/blacklist'

// Props
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  blacklist: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['close', 'success'])

// Composables
const blacklistStore = useBlacklistStore()

// Reactive state
const formData = ref({
  email: '',
  tag: ''
})

// Computed
const loading = computed(() => blacklistStore.loading)
const isEditing = computed(() => !!props.blacklist)

// Methods
const resetForm = () => {
  formData.value = {
    email: '',
    tag: ''
  }
}

const loadBlacklistData = () => {
  if (props.blacklist) {
    formData.value = {
      email: props.blacklist.email || '',
      tag: props.blacklist.tag || ''
    }
  } else {
    formData.value = {
      email: '',
      tag: ''
    }
  }
}

const handleSubmit = async () => {
  try {
    let result
    
    if (isEditing.value) {
      result = await blacklistStore.updateBlacklist(props.blacklist.name, formData.value)
      if (result.success) {
        emit('success', __('Blacklist updated successfully'))
      }
    } else {
      result = await blacklistStore.createBlacklist(formData.value)
      if (result.success) {
        emit('success', __('Email added to blacklist successfully'))
      }
    }
    
    if (!result.success) {
      throw new Error(result.error || __('An error occurred'))
    }
  } catch (error) {
    console.error('Error saving blacklist:', error)
    // Error will be handled by the store and displayed via toast
  }
}

// Watchers
watch(() => props.show, (newValue) => {
  if (newValue) {
    loadBlacklistData()
  }
})

watch(() => props.blacklist, (newValue) => {
  if (props.show) {
    loadBlacklistData()
  }
}, { immediate: true })

watch([() => props.show, () => props.blacklist], ([show, blacklist]) => {
  if (show) {
    loadBlacklistData()
  }
})
</script>
