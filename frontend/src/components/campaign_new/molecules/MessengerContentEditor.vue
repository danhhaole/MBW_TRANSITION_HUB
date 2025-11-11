<template>
  <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
    <!-- Left: Editor -->
    <div class="space-y-4">
      <!-- Header with Character Count -->
      <div class="flex items-center justify-between">
        <h4 class="text-sm font-semibold text-gray-900">
          {{ __('Message Blocks') }}
        </h4>
        <span class="text-xs text-gray-500">
          {{ totalCharacters }}/2000 {{ __('characters') }}
        </span>
      </div>

      <!-- Message Blocks -->
      <div class="space-y-4">
        <div
          v-for="(block, blockIndex) in localBlocks"
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
                  {{ __('Text Block') }} {{ getTextBlockNumber(blockIndex) }}
                </span>
                <span class="text-xs text-gray-500">
                  {{ getBlockCharacterCount(block) }}/640
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

            <!-- Text Content -->
            <div class="mb-3">
              <textarea
                v-model="block.text_content"
                :placeholder="__('Enter your message text...')"
                rows="3"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm resize-none"
                :class="{ 'border-red-500': !block.text_content?.trim() }"
                @input="updateContent"
              />
              <div class="flex justify-between items-center mt-1">
                <p class="text-xs text-gray-500">
                  {{ __('Use variables like [Name], [Job Title]') }}
                </p>
                <span class="text-xs text-gray-500">
                  {{ (block.text_content?.length || 0) }}
                </span>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="space-y-3">
              <!-- Website URL -->
              <div v-if="block.website_url !== undefined" class="space-y-2">
                <label class="block text-xs font-medium text-gray-700">
                  {{ __('Website Button') }}
                </label>
                <div class="space-y-2">
                  <div class="flex space-x-2">
                    <input
                      v-model="block.website_label"
                      :placeholder="__('Button text (e.g., Apply Now, Learn More)')"
                      type="text"
                      class="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-blue-500 focus:border-blue-500"
                      @input="updateContent"
                    />
                  </div>
                  <div class="flex space-x-2">
                    <input
                      v-model="block.website_url"
                      :placeholder="__('https://example.com')"
                      type="url"
                      class="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-blue-500 focus:border-blue-500"
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
              </div>

              <!-- Add Action Buttons -->
              <div class="flex flex-wrap gap-2">
                <button
                  v-if="block.website_url === undefined"
                  @click="addAction(block, 'website_url')"
                  class="inline-flex items-center px-3 py-1 border border-gray-300 rounded-md text-xs font-medium text-gray-700 bg-white hover:bg-gray-50"
                >
                  <FeatherIcon name="globe" class="w-3 h-3 mr-1" />
                  {{ __('Add Website Button') }}
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
                  {{ __('Image Block') }} {{ getImageBlockNumber(blockIndex) }}
                </span>
              </div>
              <button
                @click="removeBlock(blockIndex)"
                class="text-red-500 hover:text-red-700 p-1"
              >
                <FeatherIcon name="trash-2" class="w-4 h-4" />
              </button>
            </div>

            <!-- Image Upload -->
            <div v-if="block.image" class="relative">
              <img
                :src="block.image.file_url || block.image"
                alt="Block image"
                class="w-full h-48 object-cover rounded-lg border border-gray-200"
              />
              <button
                @click="removeImageFromBlock(block)"
                class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-2 hover:bg-red-600 shadow-lg"
              >
                <FeatherIcon name="x" class="w-4 h-4" />
              </button>
            </div>

            <FileUploader
              v-else
              :file-types="['image/*']"
              @success="(file) => handleImageUploadToBlock(block, file)"
            >
              <template #default="{ openFileSelector, uploading }">
                <div
                  @click="openFileSelector"
                  class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-blue-400"
                >
                  <FeatherIcon name="image" class="w-8 h-8 text-gray-400 mx-auto mb-2" />
                  <p class="text-sm text-gray-600">
                    {{ uploading ? __('Uploading...') : __('Click to upload image') }}
                  </p>
                </div>
              </template>
            </FileUploader>
          </div>
        </div>
      </div>

      <!-- Add Block Buttons -->
      <div class="flex justify-center space-x-4 pt-4 border-t border-gray-200">
        <button
          @click="addTextBlock"
          class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
        >
          <FeatherIcon name="plus" class="w-4 h-4 mr-2" />
          {{ __('Add Text Block') }}
        </button>
        <button
          @click="addImageBlock"
          class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
        >
          <FeatherIcon name="image" class="w-4 h-4 mr-2" />
          {{ __('Add Image Block') }}
        </button>
      </div>
    </div>

    <!-- Right: Preview -->
    <div class="space-y-4">
      <div class="sticky top-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Preview') }}
        </label>
        
        <!-- Messenger Chat Preview Card -->
        <div class="border border-gray-300 rounded-lg bg-white shadow-sm overflow-hidden">
          <!-- Chat Header -->
          <div class="bg-gradient-to-r from-blue-500 to-blue-600 p-4 text-white">
            <div class="flex items-center">
              <div class="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center mr-3">
                <FeatherIcon name="facebook" class="h-5 w-5" />
              </div>
              <div class="flex-1">
                <div class="text-sm font-semibold">
                  {{ __('Your Facebook Page') }}
                </div>
                <div class="text-xs opacity-90">
                  {{ __('Active now') }}
                </div>
              </div>
            </div>
          </div>

          <!-- Chat Content -->
          <div class="p-4 bg-gray-50 min-h-[300px] space-y-3">
            <!-- Message Bubbles for each block -->
            <div
              v-for="(block, index) in localBlocks"
              :key="block.id"
              class="flex justify-start"
            >
              <div class="max-w-[80%]">
                <!-- Text Block -->
                <div v-if="block.type === 'text' && block.text_content">
                  <div class="bg-white rounded-2xl rounded-tl-sm p-3 shadow-sm border border-gray-200">
                    <div class="text-sm text-gray-900 whitespace-pre-wrap break-words">
                      {{ block.text_content }}
                    </div>
                    
                    <!-- Action Buttons in Preview -->
                    <div v-if="block.website_url" class="mt-2 pt-2 border-t border-gray-200">
                      <a
                        :href="block.website_url"
                        target="_blank"
                        class="flex items-center justify-center px-3 py-2 bg-blue-500 text-white text-xs font-medium rounded hover:bg-blue-600"
                      >
                        <FeatherIcon name="external-link" class="w-3 h-3 mr-1" />
                        {{ block.website_label || __('Visit Website') }}
                      </a>
                    </div>
                  </div>
                </div>

                <!-- Image Block -->
                <div v-if="block.type === 'image' && block.image">
                  <img 
                    :src="block.image.file_url || block.image" 
                    alt="Message image" 
                    class="rounded-lg max-w-full max-h-64 object-cover shadow-sm"
                  />
                </div>

                <!-- Timestamp -->
                <div class="text-xs text-gray-500 mt-1 ml-2">
                  {{ __('Just now') }}
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="!localBlocks.length || !hasContent" class="text-center py-8">
              <div class="text-sm text-gray-400 italic">
                {{ __('Your messages will appear here...') }}
              </div>
            </div>
          </div>

          <!-- Chat Actions -->
          <div class="border-t border-gray-200 p-3 bg-white">
            <div class="flex items-center space-x-2">
              <button class="p-2 rounded-full hover:bg-gray-100">
                <FeatherIcon name="smile" class="h-5 w-5 text-gray-600" />
              </button>
              <div class="flex-1 bg-gray-100 rounded-full px-4 py-2 text-sm text-gray-500">
                {{ __('Type a message...') }}
              </div>
              <button class="p-2 rounded-full hover:bg-gray-100">
                <FeatherIcon name="send" class="h-5 w-5 text-blue-600" />
              </button>
            </div>
          </div>
        </div>

        <!-- Preview Note -->
        <p class="text-xs text-gray-500 mt-2 text-center">
          {{ __('This is a preview. Actual message may vary.') }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { FeatherIcon, FileUploader } from 'frappe-ui'

const props = defineProps({
  content: {
    type: Object,
    default: () => ({ blocks: [] })
  }
})

const emit = defineEmits(['update:content'])

// Local blocks state
const localBlocks = ref([
  {
    id: Date.now(),
    type: 'text',
    text_content: ''
  }
])

// Initialize from props
if (props.content?.blocks && props.content.blocks.length > 0) {
  localBlocks.value = props.content.blocks
}

// Computed
const totalCharacters = computed(() => {
  return localBlocks.value.reduce((total, block) => {
    if (block.type === 'text') {
      return total + (block.text_content?.length || 0)
    }
    return total
  }, 0)
})

const hasContent = computed(() => {
  return localBlocks.value.some(block => {
    if (block.type === 'text') return block.text_content?.trim()
    if (block.type === 'image') return block.image
    return false
  })
})

// Methods
const getBlockCharacterCount = (block) => {
  return block.text_content?.length || 0
}

const getTextBlockNumber = (blockIndex) => {
  let count = 0
  for (let i = 0; i <= blockIndex; i++) {
    if (localBlocks.value[i]?.type === 'text') count++
  }
  return count
}

const getImageBlockNumber = (blockIndex) => {
  let count = 0
  for (let i = 0; i <= blockIndex; i++) {
    if (localBlocks.value[i]?.type === 'image') count++
  }
  return count
}

const canRemoveBlock = () => {
  const textBlocks = localBlocks.value.filter(b => b.type === 'text')
  return textBlocks.length > 1 || localBlocks.value.length > 1
}

const addTextBlock = () => {
  localBlocks.value.push({
    id: Date.now() + Math.random(),
    type: 'text',
    text_content: ''
  })
  updateContent()
}

const addImageBlock = () => {
  localBlocks.value.push({
    id: Date.now() + Math.random(),
    type: 'image',
    image: null
  })
  updateContent()
}

const removeBlock = (index) => {
  if (canRemoveBlock()) {
    localBlocks.value.splice(index, 1)
    updateContent()
  }
}

const addAction = (block, actionType) => {
  block[actionType] = ''
  if (actionType === 'website_url') {
    block.website_label = ''
  }
  updateContent()
}

const removeAction = (block, actionType) => {
  delete block[actionType]
  if (actionType === 'website_url') {
    delete block.website_label
  }
  updateContent()
}

const handleImageUploadToBlock = (block, file) => {
  block.image = {
    file_name: file.file_name,
    file_url: file.file_url
  }
  updateContent()
}

const removeImageFromBlock = (block) => {
  block.image = null
  updateContent()
}

const updateContent = () => {
  emit('update:content', { blocks: localBlocks.value })
}

// Watch for prop changes
watch(() => props.content, (newContent) => {
  if (newContent?.blocks && newContent.blocks.length > 0) {
    localBlocks.value = newContent.blocks
  }
}, { deep: true })
</script>

<style scoped>
.resize-none {
  resize: none;
}
</style>
