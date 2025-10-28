<template>
  <div class="space-y-6">
    <!-- Resume Upload -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">
        {{ __('Upload Resume') }} <span class="text-red-500">*</span>
      </label>
      <FileUploader
        :fileTypes="['.pdf', '.doc', '.docx']"
        :upload-args="{
          private: true,
        }"
        v-model="cvFile"
        @success="handleFileUpload"
      >
        <template v-slot="{ file, uploading, progress, uploaded, message, error, total, success, openFileSelector }">
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-400 transition-colors cursor-pointer" @click="openFileSelector()">
            <div v-if="uploading" class="space-y-2">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
              <p class="text-sm text-gray-600">{{ __('Uploading...') }} {{ progress }}%</p>
              <div class="relative w-full bg-gray-200 rounded-full h-2.5 mt-2">
                <div class="absolute top-0 left-0 h-2.5 bg-blue-600 rounded-full" :style="{ width: progress + '%' }"></div>
              </div>
            </div>
            <div v-else-if="uploadedFile" class="space-y-2">
              <FeatherIcon name="file-text" class="h-12 w-12 text-green-500 mx-auto" />
              <p class="text-sm font-medium text-gray-900">{{ __('Resume Uploaded Successfully') }}</p>
              <p class="text-xs text-gray-500">
                {{ uploadedFile.name }}
              </p>
              <Button variant="outline" @click="openFileSelector" class="mt-2">
                {{ __('Change Resume') }}
              </Button>
            </div>
            <div v-else class="space-y-2">
              <FeatherIcon name="upload" class="h-12 w-12 text-gray-400 mx-auto" />
              <p class="text-sm font-medium text-gray-900">{{ __('Click to upload Resume') }}</p>
              <p class="text-xs text-gray-500">{{ __('PDF, DOC, DOCX up to 10MB') }}</p>
            </div>
          </div>
        </template>
      </FileUploader>
    </div>

    <!-- Processing State -->
    <div v-if="isProcessing" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
      <div class="flex items-center space-x-3">
        <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500"></div>
        <div>
          <p class="text-sm font-medium text-blue-900">{{ __('Processing Resume with AI') }}</p>
          <p class="text-xs text-blue-700">{{ __('Extracting information from your resume...') }}</p>
        </div>
      </div>
    </div>

    <!-- Processing Results -->
    <div v-if="processingResults" class="bg-green-50 border border-green-200 rounded-lg p-4">
      <div class="flex items-start space-x-3">
        <FeatherIcon name="check-circle" class="h-5 w-5 text-green-500 mt-0.5" />
        <div>
          <p class="text-sm font-medium text-green-900">{{ __('Resume Processed Successfully') }}</p>
          <p class="text-xs text-green-700">{{ __('Extracted information:') }}</p>
          <pre class="mt-2 p-2 bg-white rounded text-xs overflow-auto max-h-60">{{ JSON.stringify(processingResults, null, 2) }}</pre>
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <div class="flex items-start space-x-3">
        <FeatherIcon name="alert-circle" class="h-5 w-5 text-red-500 mt-0.5" />
        <div>
          <p class="text-sm font-medium text-red-900">{{ __('Processing Error') }}</p>
          <p class="text-xs text-red-700">{{ errorMessage }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FileUploader, Button, createResource, FeatherIcon } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue', 'processed'])

const cvFile = ref('')
const uploadedFile = ref(null)
const isProcessing = ref(false)
const processingResults = ref(null)
const errorMessage = ref('')

// File upload handler
const handleFileUpload = async (file) => {
  console.log('File uploaded successfully:', file)
  uploadedFile.value = file
  
  // Start processing Resume immediately after upload
  if (file.name) {
    console.log('Starting Resume extraction for file:', file.name)
    // Clear previous results
    processingResults.value = null
    errorMessage.value = ''
    extractCV(file.name)
  } else {
    console.error('No file name available for Resume extraction')
    errorMessage.value = 'File name not available for processing'
  }
}

// Extract Resume information using the AI API
const extractCV = (fileName) => {
  console.log('Starting Resume extraction for:', fileName)
  
  isProcessing.value = true
  errorMessage.value = ''
  processingResults.value = null

  // Call AI API to extract Resume
  const extractCVResource = createResource({
    url: 'mbw_mira.api.ai.extract_cv_url',
    params: {
      file_name: fileName
    },
    onSuccess(data) {
      console.log('Resume extraction successful:', data)
      if (data) {
        processingResults.value = data
        emit('processed', data)
      } else {
        errorMessage.value = 'No data returned from Resume extraction'
      }
      isProcessing.value = false
    },
    onError(error) {
      console.error('Error extracting Resume:', error)
      errorMessage.value = error.messages?.[0] || error.message || 'Failed to extract Resume information'
      isProcessing.value = false
    },
    auto: true
  })
}
</script>
