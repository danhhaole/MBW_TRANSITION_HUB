<template>
  <div class="space-y-3">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <h4 class="text-sm font-medium text-gray-900">
          {{ __('Campaign Tags') }}
        </h4>
        <Button
          variant="ghost"
          size="sm"
          @click="openDialog"
          class="p-1 h-6 w-6"
        >
          <template #prefix>
            <FeatherIcon name="plus" class="h-3 w-3" />
          </template>
        </Button>
      </div>
      <div class="text-xs text-gray-500">
        {{ tags.length }} {{ __('tags selected') }}
      </div>
    </div>

    <!-- Selected Tags Display -->
    <div v-if="tags.length > 0" class="flex flex-wrap gap-2">
      <div
        v-for="tag in tags"
        :key="tag.value"
        class="inline-flex items-center px-2 py-1 rounded-md text-white text-xs font-medium"
        :style="{ backgroundColor: tag.color || '#6B7280' }"
      >
        {{ tag.label }}
        <button
          @click="removeTag(tag)"
          class="ml-1 hover:bg-black hover:bg-opacity-20 rounded-full p-0.5 transition-colors"
        >
          <FeatherIcon name="x" class="h-3 w-3" />
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-4 border-2 border-dashed border-gray-200 rounded-lg">
      <FeatherIcon name="tag" class="h-8 w-8 text-gray-400 mx-auto mb-2" />
      <p class="text-sm text-gray-500 mb-2">
        {{ __('No tags assigned') }}
      </p>
      <Button
        variant="ghost"
        size="sm"
        @click="openDialog"
      >
        <template #prefix>
          <FeatherIcon name="plus" class="h-3 w-3" />
        </template>
        {{ __('Add Tags') }}
      </Button>
    </div>

    <!-- Tag Selection Dialog -->
    <Dialog v-model="showDialog" :options="{ size: 'lg' }">
      <template #body-title>
        <h3 class="text-lg font-semibold text-gray-900">
          {{ __('Select Campaign Tags') }}
        </h3>
      </template>

      <template #body-content>
        <div class="space-y-4">
          <!-- Search/Select Existing Tags -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Select from existing tags') }}
            </label>
            <Autocomplete
              v-model="selectedTags"
              :options="suggestions"
              :placeholder="__('Search and select tags...')"
              :multiple="true"
              :loading="loadingSuggestions"
            >
              <template #item-prefix="{ option }">
                <div
                  class="w-3 h-3 rounded-full mr-2"
                  :style="{ backgroundColor: option.color || '#6B7280' }"
                />
              </template>
              
              <template #item-suffix="{ option }">
                <FeatherIcon
                  v-if="selectedTags.find(t => t.value === option.value)"
                  name="check"
                  class="h-4 w-4 text-green-600"
                />
              </template>
            </Autocomplete>
          </div>

          <!-- Create New Tag -->
          <div class="border-t pt-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Create new tag') }}
            </label>
            <div class="flex gap-2">
              <FormControl
                v-model="newTagTitle"
                :placeholder="__('Enter tag name...')"
                class="flex-1"
              />
              <FormControl
                v-model="newTagColor"
                type="color"
                class="w-16"
              />
              <Button
                variant="ghost"
                size="sm"
                @click="createNewTag"
                :loading="creatingTag"
                :disabled="!newTagTitle.trim()"
              >
                <template #prefix>
                  <FeatherIcon name="plus" class="h-3 w-3" />
                </template>
                {{ __('Create') }}
              </Button>
            </div>
          </div>

          <!-- Preview Selected Tags -->
          <div v-if="selectedTags.length > 0" class="border-t pt-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Selected tags') }}
            </label>
            <div class="flex flex-wrap gap-2">
              <div
                v-for="tag in selectedTags"
                :key="tag.value"
                class="inline-flex items-center px-2 py-1 rounded-md text-white text-xs"
                :style="{ backgroundColor: tag.color || '#6B7280' }"
              >
                {{ tag.label }}
                <button
                  @click="removeFromSelected(tag)"
                  class="ml-1 hover:bg-black hover:bg-opacity-20 rounded-full p-0.5"
                >
                  <FeatherIcon name="x" class="h-3 w-3" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </template>

      <template #actions>
        <div class="flex justify-end gap-2">
          <Button
            variant="ghost"
            @click="closeDialog"
          >
            {{ __('Cancel') }}
          </Button>
          <Button
            variant="solid"
            @click="applyTags"
            :loading="applyingTags"
            :disabled="selectedTags.length === 0"
          >
            {{ __('Apply Tags') }}
          </Button>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { FeatherIcon, Button, Dialog, Autocomplete, FormControl, call, toast } from 'frappe-ui'

const props = defineProps({
  campaignId: {
    type: String,
    default: '' // Not required - can be empty for new campaigns
  },
  modelValue: {
    type: Array,
    default: () => []
  },
  doctype: {
    type: String,
    default: 'Mira Campaign' // Can be 'Mira Campaign' or 'Mira Campaign Template'
  }
})

const emit = defineEmits(['update:modelValue'])

// State
const tags = ref([...props.modelValue])
const showDialog = ref(false)
const selectedTags = ref([])
const suggestions = ref([])
const loadingSuggestions = ref(false)
const applyingTags = ref(false)

// New tag creation
const newTagTitle = ref('')
const newTagColor = ref('#6B7280')
const creatingTag = ref(false)

// Sync tags colors with existing Mira Tags
const syncTagColors = async () => {
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Mira Tag',
      fields: ['name', 'title', 'color'],
      limit_page_length: 0
    })

    const colorMap = {}
    for (const item of response || []) {
      colorMap[item.title] = item.color
    }

    // Update existing tags with colors
    tags.value = tags.value.map(tag => ({
      ...tag,
      color: colorMap[tag.value] || tag.color || '#6B7280'
    }))
  } catch (error) {
    console.error('❌ Error syncing tag colors:', error)
  }
}

// Fetch available tags for suggestions
const fetchSuggestions = async () => {
  loadingSuggestions.value = true
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Mira Tag',
      fields: ['name', 'title', 'color'],
      order_by: 'title asc',
      limit_page_length: 100
    })

    // Filter out tags that are already added
    const existingTagValues = tags.value.map(t => t.value)
    suggestions.value = (response || [])
      .filter(tag => !existingTagValues.includes(tag.title))
      .map(tag => ({
        label: tag.title,
        value: tag.title,
        color: tag.color || '#6B7280'
      }))
    
    console.log('📋 Available tags (excluding added):', suggestions.value.length, 'tags')
  } catch (error) {
    console.error('❌ Error fetching tag suggestions:', error)
    toast.error(__('Failed to load tags'))
  } finally {
    loadingSuggestions.value = false
  }
}

// Create new tag
const createNewTag = async () => {
  if (!newTagTitle.value.trim()) return

  creatingTag.value = true
  try {
    const response = await call('frappe.client.insert', {
      doc: {
        doctype: 'Mira Tag',
        title: newTagTitle.value.trim(),
        color: newTagColor.value,
        order: 0
      }
    })

    // Add to suggestions and select it
    const newTag = {
      label: response.title,
      value: response.title,
      color: response.color
    }
    
    suggestions.value.unshift(newTag)
    selectedTags.value.push(newTag)

    // Reset form
    newTagTitle.value = ''
    newTagColor.value = '#6B7280'

    toast.success(__('Tag created successfully'))
  } catch (error) {
    console.error('❌ Error creating tag:', error)
    toast.error(__('Failed to create tag'))
  } finally {
    creatingTag.value = false
  }
}

// Open dialog
const openDialog = () => {
  selectedTags.value = []
  showDialog.value = true
  fetchSuggestions()
}

// Close dialog
const closeDialog = () => {
  showDialog.value = false
  selectedTags.value = []
  newTagTitle.value = ''
  newTagColor.value = '#6B7280'
}

// Remove from selected in dialog
const removeFromSelected = (tag) => {
  selectedTags.value = selectedTags.value.filter(t => t.value !== tag.value)
}

// Apply selected tags
const applyTags = async () => {
  if (selectedTags.value.length === 0) return

  applyingTags.value = true
  try {
    // Filter out tags that already exist
    const newTags = selectedTags.value.filter(
      tag => !tags.value.find(t => t.value === tag.value)
    )

    if (newTags.length === 0) {
      toast.info(__('All selected tags already exist'))
      closeDialog()
      return
    }

    // If campaign/template exists, add tags to Frappe's tag system
    // Otherwise, just update local state - wizard will add tags after document is created
    if (props.campaignId) {
      for (const tag of newTags) {
        await call('frappe.desk.doctype.tag.tag.add_tag', {
          tag: tag.value,
          dt: props.doctype,
          dn: props.campaignId
        })
      }
      console.log(`✅ Tags added to existing ${props.doctype}`)
    } else {
      console.log(`ℹ️ ${props.doctype} not yet created - tags will be added after document creation`)
    }

    // Update local tags
    tags.value = [...tags.value, ...newTags]
    emit('update:modelValue', [...tags.value])

    toast.success(__('Tags added successfully'))
    closeDialog()
  } catch (error) {
    console.error('❌ Error applying tags:', error)
    toast.error(__('Failed to add tags'))
  } finally {
    applyingTags.value = false
  }
}

// Remove tag
const removeTag = async (tag) => {
  try {
    // If campaign/template exists, remove from Frappe's tag system
    if (props.campaignId) {
      await call('frappe.desk.doctype.tag.tag.remove_tag', {
        tag: tag.value,
        dt: props.doctype,
        dn: props.campaignId
      })
      console.log(`✅ Tag removed from ${props.doctype}`)
    } else {
      console.log(`ℹ️ ${props.doctype} not yet created - removing from local state only`)
    }

    tags.value = tags.value.filter(t => t.value !== tag.value)
    emit('update:modelValue', [...tags.value])

    toast.success(__('Tag removed successfully'))
  } catch (error) {
    console.error('❌ Error removing tag:', error)
    toast.error(__('Failed to remove tag'))
  }
}

// Watch modelValue changes
watch(() => props.modelValue, (newValue) => {
  tags.value = [...newValue]
}, { deep: true })

// Initialize
onMounted(() => {
  syncTagColors()
})
</script>

<style scoped>
/* Custom styles if needed */
</style>
