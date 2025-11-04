<template>
  <div class="space-y-6 p-6">
    <!-- Action Type Selection -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">
        {{ __("Select Event") }}
      </label>  
      <FormControl
        type="select"
        v-model="localAction.type"
        :options="actionTypeOptions"
        :placeholder="__('Select Event')"
      />
    </div>

    <!-- Action Configuration -->
    <div v-if="localAction.type" class="border-t pt-4">
      <!-- Add Tag Configuration -->
      <div v-if="localAction.type === 'add_tag'" class="space-y-4">
        <h4 class="text-sm font-medium text-gray-900">{{ __("Add Tag") }}</h4>
        
        <!-- Select existing tags -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Select existing tag") }}
          </label>
          
          <!-- Selected tags display -->
          <div v-if="selectedTagsDisplay?.length > 0" class="mb-3">
            <div class="flex flex-wrap gap-2">
              <div
                v-for="tag in selectedTagsDisplay"
                :key="tag.value"
                class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800 border border-blue-200"
              >
                <span>{{ tag.label }}</span>
                <button
                  @click="removeSelectedTag(tag.value)"
                  class="ml-2 text-blue-600 hover:text-blue-800 focus:outline-none"
                >
                  <FeatherIcon name="x" class="h-3 w-3" />
                </button>
              </div>
            </div>
          </div>
          
          <!-- Tag selector -->
          <FormControl
            type="select"
            v-model="selectedTagToAdd"
            :options="availableTagOptions"
            :placeholder="__('Select existing tag')"
            :loading="tagsLoading"
            @change="addSelectedTag"
          />
        </div>
        
        <!-- Or create new tag -->
        <div class="text-center text-sm text-gray-500">
          {{ __("or") }}
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Create new tag") }}
          </label>
          <div class="flex space-x-2">
            <FormControl
              v-model="newTagName"
              type="text"
              :placeholder="__('New tag name (e.g: Webinar MBWN DMS 2110)')"
              class="flex-1"
            />
            <Button 
              variant="outline" 
              size="sm"
              :loading="creatingTag"
              @click="createNewTag"
            >
              <template #prefix>
                <FeatherIcon name="plus" class="h-4 w-4" />
              </template>
              {{ __("Add") }}
            </Button>
          </div>
        </div>
        
        <p class="text-xs text-gray-500">
          {{ __("Tag will be added to the directory and assigned to the candidate") }}
        </p>
        <p v-if="localAction.type === 'add_tag' && selectedTagsDisplay.length === 0 && !newTagName.trim()" class="text-red-500 text-xs">
          {{ __("Please select existing tags or create a new tag") }}
        </p>
      </div>

      <!-- Remove Tag Configuration -->
      <div v-else-if="localAction.type === 'remove_tag'" class="space-y-4">
        <h4 class="text-sm font-medium text-gray-900">{{ __("Remove Tag") }}</h4>
        
        <!-- Select tags to remove -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Select tag to remove") }}
          </label>
          
          <!-- Selected tags display -->
          <div v-if="selectedTagsDisplay.length > 0" class="mb-3">
            <div class="flex flex-wrap gap-2">
              <div
                v-for="tag in selectedTagsDisplay"
                :key="tag.value"
                class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-red-100 text-red-800 border border-red-200"
              >
                <span>{{ tag.label }}</span>
                <button
                  @click="removeSelectedTag(tag.value)"
                  class="ml-2 text-red-600 hover:text-red-800 focus:outline-none"
                >
                  <FeatherIcon name="x" class="h-3 w-3" />
                </button>
              </div>
            </div>
          </div>
          
          <!-- Tag selector -->
          <FormControl
            type="select"
            v-model="selectedTagToAdd"
            :options="availableTagOptions"
            :placeholder="__('Select tag to remove')"
            :loading="tagsLoading"
            @change="addSelectedTag"
          />
        </div>
        
        <p class="text-xs text-gray-500">
          {{ __("Tag will be removed from the candidate") }}
        </p>
        <p v-if="localAction.type === 'remove_tag' && selectedTagsDisplay.length === 0" class="text-red-500 text-xs">
          {{ __("Please select at least one tag to remove") }}
        </p>
      </div>

      <!-- Send Email Configuration -->
      <div v-else-if="localAction.type === 'send_email'" class="space-y-4">
        <h4 class="text-sm font-medium text-gray-900">{{ __("Send Email Notification") }}</h4>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Email Content") }} <span class="text-red-500">*</span>
          </label>
          <TextEditor
            editor-class="prose-sm min-h-[20rem] border rounded-lg border-gray-300 p-3"
            :content="localAction.data.content"
            :placeholder="__('Compose your email content here...')"
            @change="(val) => localAction.data.content = val"
            :bubbleMenu="true"
            :fixedMenu="true"
          />
          <p class="text-xs text-gray-500 mt-2">
            {{ __("Use rich text formatting to create professional emails") }}
          </p>
          <p v-if="localAction.type === 'send_email' && !localAction.data.content" class="text-red-500 text-xs mt-1">
            {{ __("Email content is required") }}
          </p>
        </div>
      </div>

      <!-- Unsubscribe Configuration -->
      <div v-else-if="localAction.type === 'unsubscribe'" class="space-y-4">
        <h4 class="text-sm font-medium text-gray-900">{{ __("Unsubscribe") }}</h4>
        <div class="flex items-center space-x-2">
          <FormControl
            v-model="localAction.data.send_confirmation"
            type="checkbox"
            :label="__('Send confirmation email')"
          />
        </div>
      </div>

      <!-- Next Flow Configuration -->
      <div v-else-if="localAction.type === 'next_flow'" class="space-y-4">
        <h4 class="text-sm font-medium text-gray-900">{{ __("Execute Next Flow") }}</h4>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Select Flow") }} <span class="text-red-500">*</span>
          </label>
          <FormControl
            type="select"
            v-model="localAction.data.flow_id"
            :options="flowOptions"
            :placeholder="__('Select flow...')"
            :loading="flowsLoading"
            :class="{ 'border-red-300': localAction.type === 'next_flow' && !localAction.data.flow_id }"
          />
          <p class="text-xs text-gray-500 mt-1">
            {{ __("Only active flows are shown. Delay will be configured in the selected flow.") }}
          </p>
          <p v-if="localAction.type === 'next_flow' && !localAction.data.flow_id" class="text-red-500 text-xs mt-1">
            {{ __("Please select a flow to execute") }}
          </p>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex justify-end space-x-3 pt-4 border-t">
      <Button variant="ghost" @click="$emit('cancel')">
        {{ __("Close") }}
      </Button>
      <Button variant="solid" @click="handleSave" :disabled="!isValid">
        {{ __("Save") }}
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { Button, FeatherIcon, FormControl, Autocomplete, TextEditor } from 'frappe-ui'
import { useTagStore } from '@/stores/tag'
import { useMiraFlowStore } from '@/stores/miraFlow'
import { useToast } from '@/composables/useToast'
import { storeToRefs } from 'pinia'

// Props
const props = defineProps({
  action: {
    type: Object,
    required: true
  },
  interactionType: {
    type: String,
    required: true
  }
})

// Emits
const emit = defineEmits(['save', 'cancel'])

// Stores
const tagStore = useTagStore()
const { tags, loading: tagsLoading } = storeToRefs(tagStore)
const flowStore = useMiraFlowStore()
const { flows, loading: flowsLoading } = storeToRefs(flowStore)
const toast = useToast()

// Translation helper
const __ = (text) => text

// Helper to get default data structure for each action type
const getDefaultDataForType = (type, existingData = {}) => {
  switch (type) {
    case 'add_tag':
    case 'remove_tag':
      return {
        selected_tags: existingData.selected_tags || [],
        ...existingData
      }
    case 'send_email':
      return {
        content: existingData.content || '',
        ...existingData
      }
    case 'next_flow':
      return {
        flow_id: existingData.flow_id || '',
        ...existingData
      }
    case 'unsubscribe':
      return {
        send_confirmation: existingData.send_confirmation || false,
        ...existingData
      }
    default:
      return { ...existingData }
  }
}

// Local state
const localAction = ref({
  trigger: props.action.trigger,
  type: props.action.type || '',
  data: getDefaultDataForType(props.action.type, props.action.data)
})

const newTagName = ref('')
const creatingTag = ref(false)
const selectedTagToAdd = ref('')

// Watch for action type changes and reset data structure
watch(() => localAction.value.type, (newType, oldType) => {
  if (newType !== oldType && oldType) {
    // Reset data when type changes (but keep existing data if same type)
    console.log('🔄 Action type changed from', oldType, 'to', newType)
    localAction.value.data = getDefaultDataForType(newType, {})
  }
})

// Action type options
const actionTypeOptions = [
  { label: __("Add Tag"), value: "add_tag" },
  { label: __("Remove Tag"), value: "remove_tag" },
  { label: __("Send Email"), value: "send_email" },
  { label: __("Unsubscribe"), value: "unsubscribe" },
  { label: __("Next Flow"), value: "next_flow" }
]

// Tag options for select (exclude already selected)
const availableTagOptions = computed(() => {
  const selectedValues = localAction.value.data.selected_tags || []
  const options = tags.value
    .filter(tag => !selectedValues.includes(tag.name))
    .map(tag => ({
      label: tag.title || tag.name,
      value: tag.name
    }))
  
  console.log('🏷️ Available tag options:', options)
  return options
})

// Display selected tags with proper labels
const selectedTagsDisplay = computed(() => {
  const selectedValues = localAction.value.data.selected_tags || []
  return selectedValues.map(value => {
    const tag = tags.value.find(t => t.name === value)
    return {
      label: tag ? (tag.title || tag.name) : value,
      value: value
    }
  })
})

// Flow options from Mira Flow doctype
const flowOptions = computed(() => {
  console.log('🔍 Computing flow options:', {
    totalFlows: flows.value.length,
    flows: flows.value,
    activeFlows: flows.value.filter(flow => flow.status === 'Active')
  })
  
  // First try without filter to see all flows
  const allFlowOptions = flows.value.map(flow => ({
    label: `${flow.title || flow.name} (${flow.status || 'Unknown'})`,
    value: flow.name
  }))
  
  const activeFlowOptions = flows.value
    .filter(flow => flow.status === 'Active') // Only active flows
    .map(flow => ({
      label: flow.title || flow.name,
      value: flow.name
    }))
    
  // Use all flows for now to debug, switch to activeFlowOptions later
  const options = allFlowOptions.length > 0 ? allFlowOptions : activeFlowOptions
    
  console.log('🏷️ Flow options result:', options)
  return options
})

// Tag management methods
const addSelectedTag = () => {
  if (!selectedTagToAdd.value) return
  
  if (!localAction.value.data.selected_tags) {
    localAction.value.data.selected_tags = []
  }
  
  if (!localAction.value.data.selected_tags.includes(selectedTagToAdd.value)) {
    localAction.value.data.selected_tags.push(selectedTagToAdd.value)
  }
  
  selectedTagToAdd.value = ''
}

const removeSelectedTag = (tagValue) => {
  if (!localAction.value.data.selected_tags) return
  
  const index = localAction.value.data.selected_tags.indexOf(tagValue)
  if (index > -1) {
    localAction.value.data.selected_tags.splice(index, 1)
  }
}

// Create new tag
const createNewTag = async () => {
  if (!newTagName.value.trim()) {
    toast.error('Please enter tag name')
    return
  }

  try {
    creatingTag.value = true
    const result = await tagStore.createTag({
      title: newTagName.value.trim()
    })

    if (result.success) {
      toast.success('Tag created successfully')
      // Add to selected tags
      if (!localAction.value.data.selected_tags) {
        localAction.value.data.selected_tags = []
      }
      localAction.value.data.selected_tags.push(result.data.name)
      newTagName.value = ''
    } else {
      toast.error(result.error || 'Failed to create tag')
    }
  } catch (error) {
    console.error('Error creating tag:', error)
    toast.error('Failed to create tag')
  } finally {
    creatingTag.value = false
  }
}

// Validation
const isValid = computed(() => {
  if (!localAction.value.type) return false
  
  switch (localAction.value.type) {
    case 'add_tag':
      return !!(
        (localAction.value.data.selected_tags && localAction.value.data.selected_tags.length > 0) ||
        newTagName.value.trim()
      )
    case 'remove_tag':
      return !!(localAction.value.data.selected_tags && localAction.value.data.selected_tags.length > 0)
    case 'send_email':
      return !!(localAction.value.data.content && localAction.value.data.content.trim())
    case 'next_flow':
      return !!localAction.value.data.flow_id
    case 'unsubscribe':
      return true
    default:
      return false
  }
})

// Methods
const handleSave = async () => {
  if (!isValid.value) return

  // If creating new tag, create it first
  if (localAction.value.type === 'add_tag' && newTagName.value.trim()) {
    await createNewTag()
  }

  emit('save', localAction.value)
}

// Load data on mount
onMounted(async () => {
  try {
    console.log('🔍 Loading tags and flows...')
    
    // Load tags
    console.log('📋 Fetching tags...')
    await tagStore.fetchTags()
    console.log('✅ Tags loaded:', tags.value.length, tags.value)
    
    // Load flows
    console.log('🌊 Fetching flows...')
    const flowResult = await flowStore.fetchFlows()
    console.log('🌊 Flow fetch result:', flowResult)
    console.log('✅ Flows loaded:', flows.value.length, flows.value)
    console.log('🔍 Flow store state:', {
      loading: flowsLoading.value,
      error: flowStore.error,
      flows: flows.value
    })
    
    // If no data loaded
    if (tags.value.length === 0) {
      console.log('⚠️ No tags found')
    }
    
    if (flows.value.length === 0) {
      console.log('⚠️ No flows found - check if Mira Flow doctype exists and has data')
      
      // Temporary fallback for testing
      console.log('🧪 Adding test flow data for debugging')
      // Uncomment this to test UI with mock data:
      // flows.value = [
      //   { name: 'test-flow-1', title: 'Test Flow 1', status: 'Active' },
      //   { name: 'test-flow-2', title: 'Test Flow 2', status: 'Active' },
      //   { name: 'test-flow-3', title: 'Test Flow 3', status: 'Draft' }
      // ]
    }
  } catch (error) {
    console.error('❌ Error loading data:', error)
    console.error('❌ Error details:', {
      message: error.message,
      stack: error.stack
    })
  }
})
</script>
