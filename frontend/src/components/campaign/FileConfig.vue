<template>
  <div class="file-config">
    <div class="space-y-4">
      <!-- File Upload Section -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Select File') }} <span class="text-red-500">*</span>
        </label>
        
        <!-- Use Frappe UI FileUploader -->
        <div class="border border-gray-300 rounded-lg p-4">
          <FileUploader
            :fileTypes="['.csv', '.xlsx', '.xls']"
            :upload-args="{
              doctype: 'Campaign',
              docname: 'temp',
              private: false,
            }"
            v-model="uploadedFileUrl"
            @success="handleFileUploadSuccess"
          >
            <template
              v-slot="{
                file,
                uploading,
                progress,
                uploaded,
                message,
                error,
                total,
                success,
                openFileSelector,
              }"
            >
              <div class="space-y-3">
                <!-- Current file display -->
                <div v-if="uploadedFileUrl" class="flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded-lg">
                  <div class="flex items-center space-x-3">
                    <svg class="h-8 w-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <div>
                      <a
                        :href="uploadedFileUrl"
                        target="_blank"
                        class="text-sm font-medium text-green-900 hover:text-green-700 underline"
                      >
                        {{ uploadedFileUrl.split("/").pop() }}
                      </a>
                      <div v-if="selectedFile" class="text-xs text-green-700">
                        {{ formatFileSize(selectedFile.size) }}
                      </div>
                    </div>
                  </div>
                  <button
                    type="button"
                    @click="removeFile"
                    class="text-red-500 hover:text-red-700"
                  >
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
                
                <!-- Upload button -->
                <div class="text-center">
                  <Button 
                    variant="outline" 
                    @click="openFileSelector()" 
                    :loading="uploading"
                    class="w-full"
                  >
                    <div class="flex items-center justify-center gap-2">
                      <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                      </svg>
                      {{ uploading ? `${__('Uploading')} ${progress}%` : (uploadedFileUrl ? __('Change File') : __('Upload File')) }}
                    </div>
                  </Button>
                </div>
                
                <!-- Error message -->
                <div v-if="error" class="text-red-600 text-sm text-center">
                  {{ error }}
                </div>
              </div>
            </template>
          </FileUploader>
        </div>
      </div>
      
      <!-- File Instructions -->
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 class="text-sm font-medium text-blue-900 mb-2">{{ __('File Format Requirements') }}</h4>
        <ul class="text-xs text-blue-800 space-y-1">
          <li>• {{ __('First row should contain column headers') }}</li>
          <li>• {{ __('Required columns: full_name, email') }}</li>
          <li>• {{ __('Optional columns: phone, current_position, location, skills') }}</li>
          <li>• {{ __('Skills should be comma-separated') }}</li>
        </ul>
      </div>
      
      <!-- File Preview (if applicable) -->
      <div v-if="selectedFile && filePreview.length > 0" class="mt-4">
        <h4 class="text-sm font-medium text-gray-900 mb-2">{{ __('File Preview') }}</h4>
        <div class="border border-gray-200 rounded-lg overflow-hidden">
          <div class="bg-gray-50 px-4 py-2 border-b">
            <p class="text-xs text-gray-600">{{ __('First 3 rows') }}</p>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full text-xs">
              <thead class="bg-gray-50">
                <tr>
                  <th v-for="header in fileHeaders" :key="header" class="px-3 py-2 text-left font-medium text-gray-900 border-r">
                    {{ header }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in filePreview.slice(0, 3)" :key="index" class="border-t">
                  <td v-for="(cell, cellIndex) in row" :key="cellIndex" class="px-3 py-2 text-gray-700 border-r">
                    {{ cell }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { FileUploader, Button } from 'frappe-ui'

// Props
const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

// Emits
const emit = defineEmits(['update:modelValue'])

// State
const selectedFile = ref(null)
const uploadedFileUrl = ref('')
const filePreview = ref([])
const fileHeaders = ref([])

// Translation helper


// Handle file upload success
const handleFileUploadSuccess = async (file) => {
  console.log('File upload success:', file)
  
  // Store file metadata
  selectedFile.value = {
    name: file.file_name,
    size: file.file_size || 0,
    type: file.content_type || '',
    url: file.file_url
  }
  
  // Store the uploaded file URL
  uploadedFileUrl.value = file.file_url
  
  // Preview file if it's CSV
  const fileExtension = '.' + file.file_name.split('.').pop().toLowerCase()
  if (fileExtension === '.csv') {
    await previewCSVFromUrl(file.file_url)
  }
  
  // Update parent component
  updateModelValue()
}

// Preview CSV file from URL
const previewCSVFromUrl = async (fileUrl) => {
  try {
    const response = await fetch(fileUrl)
    const text = await response.text()
    const lines = text.split('\n').filter(line => line.trim())
    
    if (lines.length > 0) {
      fileHeaders.value = lines[0].split(',').map(h => h.trim().replace(/"/g, ''))
      filePreview.value = lines.slice(1).map(line => 
        line.split(',').map(cell => cell.trim().replace(/"/g, ''))
      )
    }
  } catch (error) {
    console.error('Error previewing CSV from URL:', error)
  }
}

// Remove file
const removeFile = () => {
  selectedFile.value = null
  uploadedFileUrl.value = ''
  filePreview.value = []
  fileHeaders.value = []
  updateModelValue()
}

// Format file size
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Update model value
const updateModelValue = () => {
  const newValue = {
    ...props.modelValue,
    selectedFile: selectedFile.value,
    uploadedFileUrl: uploadedFileUrl.value,
    filePreview: filePreview.value,
    fileHeaders: fileHeaders.value
  }
  emit('update:modelValue', newValue)
}

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  if (!newValue?.selectedFile && selectedFile.value) {
    removeFile()
  } else if (newValue?.uploadedFileUrl && newValue.uploadedFileUrl !== uploadedFileUrl.value) {
    uploadedFileUrl.value = newValue.uploadedFileUrl
  } else if (newValue?.selectedFile && newValue.selectedFile !== selectedFile.value) {
    selectedFile.value = newValue.selectedFile
  }
}, { deep: true })
</script>

<style scoped>
.file-config {
  max-width: 100%;
}

/* Drag and drop styling */
.border-dashed {
  border-style: dashed;
}

/* Table styling */
table {
  border-collapse: collapse;
}

th, td {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px;
}
</style> 