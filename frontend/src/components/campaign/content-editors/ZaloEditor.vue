<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h3 class="text-lg font-medium text-gray-900">{{ __("Zalo ZNS Message") }}</h3>
      <div class="flex items-center space-x-2">
        <span class="text-sm text-gray-500">
          {{ totalCharacters }}/{{ maxCharacters }} {{ __("characters") }}
        </span>
      </div>
    </div>

    <!-- Message Blocks -->
    <div class="space-y-4">
      <div
        v-for="(block, blockIndex) in localContent.blocks"
        :key="block.id"
        class="border border-gray-200 rounded-lg p-4 bg-gray-50"
      >
        <!-- Text Block -->
        <div v-if="block.type === 'text'">
          <!-- Block Header -->
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center space-x-2">
              <FeatherIcon name="edit-3" class="w-4 h-4 text-gray-500" />
              <span class="text-sm font-medium text-gray-700">
                {{ __("Text Block") }} {{ getTextBlockNumber(blockIndex) }}
              </span>
              <span class="text-xs text-gray-500">
                {{ getBlockCharacterCount(block) }}/640 {{ __("characters") }}
              </span>
            </div>
            <button
              v-if="canRemoveBlock()"
              @click="removeBlock(blockIndex)"
              class="text-red-500 hover:text-red-700 p-1"
            >
              <FeatherIcon name="trash-2" class="w-4 h-4" />
            </button>
          </div>

        <!-- Text Content (Required) -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Message Text") }} <span class="text-red-500">*</span>
          </label>
          <textarea
            v-model="block.text_content"
            :placeholder="__('Enter your message text...')"
            :disabled="readonly"
            rows="3"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm resize-none"
            :class="{
              'bg-gray-100 cursor-not-allowed': readonly,
              'border-red-500': !block.text_content?.trim()
            }"
            @input="updateContent"
          />
          <div class="flex justify-between items-center mt-1">
            <p class="text-xs text-gray-500">
              {{ __("Use variables like [Candidate Name], [Job Title], [Company]") }}
            </p>
            <span class="text-xs text-gray-500">
              {{ (block.text_content?.length || 0) }} {{ __("characters") }}
            </span>
          </div>
        </div>

          <!-- Action Buttons in Block -->
          <div class="space-y-3">
            <!-- Website URL -->
            <div v-if="block.website_url !== undefined" class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">
                {{ __("Website URL") }}
              </label>
              <div class="flex space-x-2">
                <input
                  v-model="block.website_url"
                  :placeholder="__('https://example.com')"
                  :disabled="readonly"
                  type="url"
                  class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  :class="{ 'bg-gray-100 cursor-not-allowed': readonly }"
                  @input="updateContent"
                />
                <button
                  @click="removeAction(block, 'website_url')"
                  class="text-red-500 hover:text-red-700 p-2"
                >
                  <FeatherIcon name="x" class="w-4 h-4" />
                </button>
              </div>
            </div>

            <!-- Phone Number -->
            <div v-if="block.phone_number !== undefined" class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">
                {{ __("Phone Number") }}
              </label>
              <div class="flex space-x-2">
                <input
                  v-model="block.phone_number"
                  :placeholder="__('0123456789')"
                  :disabled="readonly"
                  type="tel"
                  class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  :class="{ 'bg-gray-100 cursor-not-allowed': readonly }"
                  @input="updateContent"
                />
                <button
                  @click="removeAction(block, 'phone_number')"
                  class="text-red-500 hover:text-red-700 p-2"
                >
                  <FeatherIcon name="x" class="w-4 h-4" />
                </button>
              </div>
            </div>

            <!-- Flow Trigger -->
            <div v-if="block.flow_trigger !== undefined" class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">
                {{ __("Start Flow") }}
              </label>
              <div class="flex space-x-2">
                <input
                  v-model="block.flow_trigger"
                  :placeholder="__('Flow ID or trigger name')"
                  :disabled="readonly"
                  class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  :class="{ 'bg-gray-100 cursor-not-allowed': readonly }"
                  @input="updateContent"
                />
                <button
                  @click="removeAction(block, 'flow_trigger')"
                  class="text-red-500 hover:text-red-700 p-2"
                >
                  <FeatherIcon name="x" class="w-4 h-4" />
                </button>
              </div>
            </div>

            <!-- Add Action Buttons -->
            <div v-if="!readonly" class="flex flex-wrap gap-2">
              <button
                v-if="block.website_url === undefined"
                @click="addAction(block, 'website_url')"
                class="inline-flex items-center px-3 py-1 border border-gray-300 rounded-md text-xs font-medium text-gray-700 bg-white hover:bg-gray-50"
              >
                <FeatherIcon name="globe" class="w-3 h-3 mr-1" />
                {{ __("Add Website") }}
              </button>
              <button
                v-if="block.phone_number === undefined"
                @click="addAction(block, 'phone_number')"
                class="inline-flex items-center px-3 py-1 border border-gray-300 rounded-md text-xs font-medium text-gray-700 bg-white hover:bg-gray-50"
              >
                <FeatherIcon name="phone" class="w-3 h-3 mr-1" />
                {{ __("Add Phone") }}
              </button>
              <button
                v-if="block.flow_trigger === undefined"
                @click="addAction(block, 'flow_trigger')"
                class="inline-flex items-center px-3 py-1 border border-gray-300 rounded-md text-xs font-medium text-gray-700 bg-white hover:bg-gray-50"
              >
                <FeatherIcon name="play-circle" class="w-3 h-3 mr-1" />
                {{ __("Start Flow") }}
              </button>
            </div>
          </div>
        </div>

        <!-- Image Block -->
        <div v-else-if="block.type === 'image'">
          <!-- Block Header -->
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center space-x-2">
              <FeatherIcon name="image" class="w-4 h-4 text-gray-500" />
              <span class="text-sm font-medium text-gray-700">
                {{ __("Image Block") }} {{ getImageBlockNumber(blockIndex) }}
              </span>
            </div>
            <button
              @click="removeBlock(blockIndex)"
              class="text-red-500 hover:text-red-700 p-1"
            >
              <FeatherIcon name="trash-2" class="w-4 h-4" />
            </button>
          </div>

          <!-- Image Upload Area -->
          <div class="space-y-3">
            <div v-if="block.image" class="relative">
              <img
                :src="block.image.file_url || block.image.preview"
                :alt="block.image.file_name"
                class="w-full h-64 object-cover rounded-lg border border-gray-200"
              />
              <button
                v-if="!readonly"
                @click="removeImageFromBlock(block)"
                class="absolute top-4 right-4 bg-red-500 text-white rounded-full p-2 hover:bg-red-600 shadow-lg"
              >
                <FeatherIcon name="x" class="w-5 h-5" />
              </button>
              <div class="mt-3 text-center">
                <p class="text-sm text-gray-700 font-medium">{{ block.image.file_name }}</p>
              </div>
            </div>

            <div v-else class="border-2 border-dashed border-gray-300 rounded-lg p-6">
              <div class="text-center">
                <FeatherIcon name="image" class="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p class="text-sm text-gray-600 mb-4">
                  {{ __("Upload an image for this block") }}
                </p>
                <FileUploader
                  v-if="!readonly"
                  :fileTypes="['.jpg', '.jpeg', '.png', '.gif']"
                  :upload-args="{
                    doctype: 'Mira Campaign',
                    docname: 'temp',
                    private: false,
                  }"
                  @success="(file) => handleImageUploadToBlock(block, file)"
                  @error="handleImageUploadError"
                >
                  <template v-slot="{ openFileSelector }">
                    <button
                      @click="openFileSelector()"
                      class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      type="button"
                    >
                      <FeatherIcon name="upload" class="h-4 w-4 mr-2" />
                      {{ __("Choose Image") }}
                    </button>
                  </template>
                </FileUploader>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Block Buttons -->
    <div v-if="!readonly" class="flex justify-center space-x-4 pt-4 border-t border-gray-200">
      <button
        @click="addTextBlock"
        class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
      >
        <FeatherIcon name="plus" class="w-4 h-4 mr-2" />
        {{ __("Add Text Block") }}
      </button>
      <button
        @click="addImageBlock"
        class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
      >
        <FeatherIcon name="image" class="w-4 h-4 mr-2" />
        {{ __("Add Image Block") }}
      </button>
    </div>

    <!-- Action Buttons -->
    <!-- <div v-if="!readonly" class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
      <Button variant="ghost" @click="$emit('preview')">
        {{ __("Preview") }}
      </Button>
      <Button variant="solid" theme="blue" @click="$emit('save')">
        {{ __("Save") }}
      </Button>
    </div> -->
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { FeatherIcon, Dialog, Button, FileUploader } from 'frappe-ui'
import { useToast } from '../../../composables/useToast'

const props = defineProps({
  content: { type: Object, default: () => ({}) },
  readonly: { type: Boolean, default: false }
})

const emit = defineEmits(['update:content', 'save', 'preview'])

const toast = useToast()
const maxCharacters = 2000

// Initialize local content with default structure
const localContent = ref({
  blocks: [
    {
      id: Date.now(),
      type: 'text',
      text_content: '',
    }
  ],
  ...props.content
})

// Ensure blocks exists and has at least one text block
if (!localContent.value.blocks || localContent.value.blocks.length === 0) {
  localContent.value.blocks = [
    {
      id: Date.now(),
      type: 'text',
      text_content: '',
    }
  ]
}

// Computed properties
const totalCharacters = computed(() => {
  return localContent.value.blocks.reduce((total, block) => {
    if (block.type === 'text') {
      return total + (block.text_content?.length || 0)
    }
    return total
  }, 0)
})

// Methods
const getBlockCharacterCount = (block) => {
  return block.text_content?.length || 0
}

const getTextBlockNumber = (blockIndex) => {
  let textBlockCount = 0
  for (let i = 0; i <= blockIndex; i++) {
    if (localContent.value.blocks[i]?.type === 'text') {
      textBlockCount++
    }
  }
  return textBlockCount
}

const getImageBlockNumber = (blockIndex) => {
  let imageBlockCount = 0
  for (let i = 0; i <= blockIndex; i++) {
    if (localContent.value.blocks[i]?.type === 'image') {
      imageBlockCount++
    }
  }
  return imageBlockCount
}

const canRemoveBlock = () => {
  const textBlocks = localContent.value.blocks.filter(block => block.type === 'text')
  return textBlocks.length > 1 || localContent.value.blocks.length > 1
}

const addTextBlock = () => {
  localContent.value.blocks.push({
    id: Date.now() + Math.random(),
    type: 'text',
    text_content: '',
  })
  updateContent()
}

const addImageBlock = () => {
  localContent.value.blocks.push({
    id: Date.now() + Math.random(),
    type: 'image',
    image: null,
  })
  updateContent()
}

const removeBlock = (index) => {
  if (canRemoveBlock()) {
    localContent.value.blocks.splice(index, 1)
    updateContent()
  }
}

const addAction = (block, actionType) => {
  switch (actionType) {
    case 'website_url':
      block.website_url = ''
      break
    case 'phone_number':
      block.phone_number = ''
      break
    case 'flow_trigger':
      block.flow_trigger = ''
      break
  }
  updateContent()
}

const removeAction = (block, actionType) => {
  delete block[actionType]
  updateContent()
}

const handleImageUploadToBlock = (block, file) => {
  block.image = {
    file_name: file.file_name,
    file_url: file.file_url,
    file_size: file.file_size
  }
  updateContent()
  toast.success(__('Image uploaded successfully'))
}

const handleImageUploadError = (error) => {
  toast.error(__('Failed to upload image: ') + error.message)
}

const removeImageFromBlock = (block) => {
  block.image = null
  updateContent()
}

const updateContent = () => {
  emit('update:content', { ...localContent.value })
}

// Watch for prop changes
watch(() => props.content, (newContent) => {
  if (newContent && Object.keys(newContent).length > 0) {
    localContent.value = {
      blocks: [
        {
          id: Date.now(),
          type: 'text',
          text_content: '',
        }
      ],
      ...newContent
    }
  }
}, { deep: true })

// Translation helper
const __ = (text) => text
</script>

<style scoped>
.resize-none {
  resize: none;
}
</style>
