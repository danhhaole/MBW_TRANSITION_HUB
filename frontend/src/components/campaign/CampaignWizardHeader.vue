<template>
  <div class="bg-white border-b border-gray-200 px-6 py-4">
    <div class="flex items-center justify-between">
      <!-- Left: Exit button and Back button -->
      <div class="flex items-center space-x-3">
        <Button
          variant=""
          theme="gray"
          size="sm"
          @click="$emit('exit')"
          class="flex items-center space-x-2"
        >
        <div class="flex items-center space-x-2">
          <FeatherIcon name="x" class="h-4 w-4" />
        </div>
        </Button>
        
        <Button
          v-if="currentStep > 1"
          variant="outline"
          theme="gray"
          size="sm"
          @click="$emit('back')"
          :disabled="loading"
          class="flex items-center space-x-2"
        >
        <div class="flex items-center space-x-2">
          <FeatherIcon name="arrow-left" class="h-4 w-4" />
          <span>{{ __("Back") }}</span>

        </div>
        </Button>

              <!-- Center: Campaign name (editable) -->
      <div class="flex-1 max-w-md mx-6">
        <div v-if="!isEditingName" class="flex items-center justify-center space-x-2">
          <h1 class="text-lg font-semibold text-gray-900 truncate">
            {{ campaignName || __("New Campaign") }}
          </h1>
          <Button
            variant="ghost"
            theme="gray"
            size="sm"
            @click="startEditingName"
            class="p-1"
          >
            <FeatherIcon name="edit-2" class="h-4 w-4" />
          </Button>
        </div>
        
        <div v-else class="flex items-center space-x-2">
          <input
            ref="nameInput"
            v-model="editingNameValue"
            type="text"
            class="flex-1 px-3 py-1 text-lg font-semibold text-center border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            @keyup.enter="saveName"
            @keyup.escape="cancelEditingName"
            @blur="saveName"
          />
          <Button
            variant="ghost"
            theme="green"
            size="sm"
            @click="saveName"
            class="p-1"
          >
            <FeatherIcon name="check" class="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            theme="gray"
            size="sm"
            @click="cancelEditingName"
            class="p-1"
          >
            <FeatherIcon name="x" class="h-4 w-4" />
          </Button>
        </div>
      </div>
      </div>



      <!-- Right: Action buttons -->
      <div class="flex items-center space-x-3">
        <!-- Auto-save indicator -->
        <div v-if="autoSaving" class="flex items-center text-xs text-gray-500">
          <svg class="animate-spin h-3 w-3 mr-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ __("Saving...") }}
        </div>
        
        <!-- Save success indicator -->
        <div v-else-if="saveSuccess" class="flex items-center text-xs text-green-600">
          <svg class="h-4 w-4 mr-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          {{ __("Saved") }}
        </div>
        
        <!-- Continue button - show if not at last step, or if in edit mode and at last step -->
        <Button
          v-if="currentStep < totalSteps && !(isEditMode && canFinalize)"
          variant="solid"
          theme="blue"
          size="sm"
          @click="$emit('save-and-continue')"
          :loading="saving"
          :disabled="!canProceed"
        >
          {{ __("Continue") }}
        </Button>
        
        <!-- Finalize button - show only in create mode at last step -->
        <Button
          v-else-if="!isEditMode && canFinalize"
          variant="solid"
          theme="green"
          size="sm"
          @click="$emit('finalize')"
          :loading="finalizing"
          :disabled="!canFinalize"
        >
          {{ __("Finalize Campaign") }}
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { Button, FeatherIcon } from 'frappe-ui'

// Props
const props = defineProps({
  campaignName: {
    type: String,
    default: ''
  },
  currentStep: {
    type: Number,
    required: true
  },
  totalSteps: {
    type: Number,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  saving: {
    type: Boolean,
    default: false
  },
  finalizing: {
    type: Boolean,
    default: false
  },
  canSave: {
    type: Boolean,
    default: true
  },
  canProceed: {
    type: Boolean,
    default: true
  },
  canFinalize: {
    type: Boolean,
    default: true
  },
  autoSaving: {
    type: Boolean,
    default: false
  },
  saveSuccess: {
    type: Boolean,
    default: false
  },
  isEditMode: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits([
  'exit',
  'back', 
  'save',
  'save-and-continue',
  'finalize',
  'update:campaign-name'
])

// Name editing state
const isEditingName = ref(false)
const editingNameValue = ref('')
const nameInput = ref(null)

// Translation helper
const __ = (text) => text

// Name editing functions
const startEditingName = async () => {
  isEditingName.value = true
  editingNameValue.value = props.campaignName || ''
  await nextTick()
  nameInput.value?.focus()
  nameInput.value?.select()
}

const saveName = () => {
  if (editingNameValue.value.trim()) {
    emit('update:campaign-name', editingNameValue.value.trim())
  }
  isEditingName.value = false
}

const cancelEditingName = () => {
  isEditingName.value = false
  editingNameValue.value = ''
}
</script>
