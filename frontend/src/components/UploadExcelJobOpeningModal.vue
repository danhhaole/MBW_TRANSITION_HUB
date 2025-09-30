<template>
  <Dialog v-model="show" :options="{ 
    title: __('Upload Job Openings'), 
    size: '6xl',
    showCloseButton: true
  }">
    <template #body>
      <div class="p-6">
        <!-- Progress Steps -->
        <div class="mb-8">
          <div class="flex items-center justify-between">
            <div 
              v-for="(step, index) in steps" 
              :key="index"
              class="flex items-center"
            >
              <div class="flex items-center">
                <div 
                  class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium"
                  :class="getStepClass(index)"
                >
                  <span v-if="currentStep > index" class="text-white">✓</span>
                  <span v-else>{{ index + 1 }}</span>
                </div>
                <span 
                  class="ml-2 text-sm font-medium"
                  :class="currentStep >= index ? 'text-gray-900' : 'text-gray-500'"
                >
                  {{ step.title }}
                </span>
              </div>
              <div 
                v-if="index < steps.length - 1" 
                class="w-16 h-0.5 mx-4"
                :class="currentStep > index ? 'bg-blue-600' : 'bg-gray-300'"
              ></div>
            </div>
          </div>
        </div>

        <!-- Step 1: Prepare & Upload -->
        <div v-if="currentStep === 0" class="space-y-6">
          <div class="text-center mb-6">
            <h3 class="text-lg font-medium text-gray-900 mb-2">{{ __('Step 1: Prepare Your Data') }}</h3>
            <p class="text-sm text-gray-500">{{ __('Download the template and prepare your job opening data.') }}</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Download Template -->
            <div class="border border-gray-200 rounded-lg p-6 text-center">
              <div class="mx-auto w-12 h-12 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h4 class="font-medium text-gray-900 mb-2">{{ __('Download Template') }}</h4>
              <p class="text-sm text-gray-500 mb-4">{{ __('Get the correct format for your data') }}</p>
              <Button 
                variant="outline" 
                size="sm" 
                @click="downloadTemplate"
                class="w-full"
              >
                <template #prefix>
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </template>
                {{ __('Download') }}
              </Button>
            </div>

            <!-- Select Job Opening -->
            <div class="border border-gray-200 rounded-lg p-6 text-center">
              <div class="mx-auto w-12 h-12 rounded-full bg-green-50 text-green-600 flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V8a2 2 0 012-2V6" />
                </svg>
              </div>
              <h4 class="font-medium text-gray-900 mb-2">{{ __('Select Job Opening') }}</h4>
              <p class="text-sm text-gray-500 mb-4">{{ __('Link job openings to a specific position (optional)') }}</p>
              <Select 
                v-model="selectedJobOpening" 
                :options="jobOpeningOptions" 
                placeholder="Select job opening"
                class="w-full"
                size="sm"
              />
            </div>

            <!-- Upload File -->
            <div class="border border-gray-200 rounded-lg p-6 text-center">
              <div class="mx-auto w-12 h-12 rounded-full bg-purple-50 text-purple-600 flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              <h4 class="font-medium text-gray-900 mb-2">{{ __('Upload Your File') }}</h4>
              <p class="text-sm text-gray-500 mb-4">{{ __('Drop your Excel or CSV file here') }}</p>
              
              <!-- File Upload Area -->
              <div 
                class="border-2 border-dashed border-gray-300 rounded-lg p-4 cursor-pointer hover:border-gray-400 transition-colors"
                :class="{ 'border-blue-500 bg-blue-50': isDragOver }"
                @click="triggerFileInput"
                @dragover.prevent="isDragOver = true"
                @dragleave.prevent="isDragOver = false"
                @drop.prevent="handleFileDrop"
              >
                <div class="text-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                  <p class="mt-2 text-sm text-gray-600">
                    {{ selectedFile ? selectedFile.name : __('Drop files here or click to upload') }}
                  </p>
                  <p class="text-xs text-gray-500">{{ __('Support Excel (.xlsx, .xls) and CSV files') }}</p>
                </div>
              </div>
              
              <input 
                ref="fileInput"
                type="file" 
                accept=".xlsx,.xls,.csv"
                @change="handleFileSelect"
                class="hidden"
              />
              
              <Button 
                v-if="selectedFile"
                variant="outline" 
                size="sm" 
                @click="triggerFileInput"
                class="w-full mt-4"
              >
                <template #prefix>
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </template>
                {{ __('Select File') }}
              </Button>
            </div>
          </div>
        </div>

        <!-- Step 2: Processing -->
        <div v-if="currentStep === 1" class="space-y-6">
          <div class="text-center mb-6">
            <h3 class="text-lg font-medium text-gray-900 mb-2">{{ __('Step 2: Processing') }}</h3>
            <p class="text-sm text-gray-500">{{ __('Processing your file and extracting data...') }}</p>
          </div>

          <div class="flex items-center justify-center py-12">
            <div class="text-center">
              <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p class="text-gray-600">{{ processingMessage }}</p>
              <div v-if="processingProgress > 0" class="mt-4 w-64 mx-auto">
                <div class="bg-gray-200 rounded-full h-2">
                  <div 
                    class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    :style="{ width: processingProgress + '%' }"
                  ></div>
                </div>
                <p class="text-sm text-gray-500 mt-2">{{ processingProgress }}% {{ __('complete') }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 3: Preview & Mapping -->
<div v-if="currentStep === 2" class="step-content">
  <div class="step-header">
    <h4 class="step-title">{{ __("Step 3: Review and Map Fields") }}</h4>
    <p class="step-description">{{ __("Review your data and map columns to job opening fields") }}</p>
    <button class="btn btn-outline mt-4" @click="() => { currentStep = 0; selectedFile = null; previewBundle = { filename: '', total_rows: 0, columns: [], sample: [] }; fieldMapping = {}; availableFields = []; }">
      <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
      {{ __("Back to Upload") }}
    </button>
  </div>

  <div class="card mb-6">
    <div class="card-header">
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <div class="icon-circle bg-green-100 text-green-600 mr-3">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div>
            <h5 class="card-title">{{ previewBundle.filename }}</h5>
            <p class="card-subtitle">{{ previewBundle.total_rows }} {{ __("records found") }}</p>
          </div>
        </div>
        <button class="btn btn-outline btn-sm" @click="() => { currentStep = 0; selectedFile = null; previewBundle = { filename: '', total_rows: 0, columns: [], sample: [] }; fieldMapping = {}; availableFields = []; }">
          {{ __("Upload Different File") }}
        </button>
      </div>
    </div>
  </div>

  <div class="card mb-6">
    <div class="card-header">
      <h5 class="card-title">{{ __("Sample Data Preview") }}</h5>
      <p class="card-subtitle">{{ __("First few rows from your file") }}</p>
    </div>
    <div class="card-body">
      <div class="overflow-x-auto max-h-64 border rounded-lg">
        <table class="min-w-full border-collapse">
          <thead class="bg-gray-50 sticky top-0">
            <tr>
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">#</th>
              <th v-for="column in previewBundle.columns" :key="column" class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase border-l">
                {{ column }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in previewBundle.sample" :key="index" class="hover:bg-gray-50">
              <td class="px-4 py-2 text-sm font-medium text-gray-900 border-b">{{ index + 1 }}</td>
              <td v-for="column in previewBundle.columns" :key="column" class="px-4 py-2 text-sm text-gray-900 border-b border-l max-w-xs truncate" :title="row[column]">
                {{ row[column] || '-' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <div class="card mb-6">
    <div class="card-header">
      <div class="flex items-center justify-between">
        <div>
          <h5 class="card-title">{{ __("Field Mapping") }}</h5>
          <p class="card-subtitle">{{ __("Map your file columns to job opening fields") }}</p>
        </div>
        <div class="flex space-x-2">
          <button class="btn btn-outline btn-sm" @click="autoMapFields">
            <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            {{ __("Auto Map") }}
          </button>
          <button class="btn btn-outline btn-sm" @click="clearMapping">
            <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            {{ __("Clear All") }}
          </button>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="mapping-grid">
        <div v-for="field in availableFields" :key="field.fieldname" class="mapping-field">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ field.label }}
            <span v-if="field.reqd" class="text-red-500 ml-1">*</span>
          </label>
          <select v-model="fieldMapping[field.fieldname]"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                  :class="{ 'border-red-500 ring-red-500': field.reqd && !fieldMapping[field.fieldname] }">
            <option value="">{{ __("-- Select Column --") }}</option>
            <option v-for="column in previewBundle.columns" :key="column" :value="column">
              {{ column }}
            </option>
          </select>
        </div>
      </div>
    </div>
  </div>

  <div class="card mb-6">
    <div class="card-header">
      <h5 class="card-title">{{ __("Import Options") }}</h5>
      <p class="card-subtitle">{{ __("Configure how data should be imported") }}</p>
    </div>
    <div class="card-body">
      <div class="space-y-3">
        <label class="flex items-center">
          <input type="checkbox" v-model="validateOnly" class="form-checkbox h-4 w-4 text-blue-600 rounded">
          <span class="ml-3 text-sm text-gray-700">{{ __("Validate only (don't import data)") }}</span>
        </label>
        <label class="flex items-center">
          <input type="checkbox" v-model="skipDuplicates" class="form-checkbox h-4 w-4 text-blue-600 rounded">
          <span class="ml-3 text-sm text-gray-700">{{ __("Skip duplicates") }}</span>
        </label>
      </div>
    </div>
  </div>

  <div v-if="availableFields.length && availableFields.some(f => f.reqd && !fieldMapping[f.fieldname])" class="alert alert-warning mb-6">
    <div class="flex items-start">
      <svg class="h-5 w-5 text-yellow-400 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
      </svg>
      <div class="ml-3">
        <h6 class="text-sm font-medium text-yellow-800">{{ __('Mapping Issues') }}</h6>
        <div class="mt-2 text-sm text-yellow-700">
          <ul class="list-disc list-inside space-y-1">
            <li v-for="field in availableFields.filter(f => f.reqd && !fieldMapping[f.fieldname])" :key="field.fieldname">
              {{ __('Required field "{0}" is not mapped').replace('{0}', field.label) }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <div class="flex justify-end">
    <div class="flex space-x-3">
      <button class="btn btn-outline" @click="validateData" :disabled="isValidating || !availableFields.length">
        <span v-if="isValidating" class="inline-block animate-spin mr-2">⌛</span>
        <svg v-else class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ isValidating ? __("Validating...") : __("Validate Data") }}
      </button>
      <button class="btn btn-primary" @click="processImport" :disabled="isImporting || !availableFields.length">
        <span v-if="isImporting" class="inline-block animate-spin mr-2">⌛</span>
        <svg v-else class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
        </svg>
        {{ isImporting ? __("Importing...") : (validateOnly ? __("Validate") : __("Import Data")) }}
      </button>
    </div>
  </div>
</div>

        <!-- Step 4: Importing -->
        <div v-if="currentStep === 3" class="space-y-6">
          <div class="text-center mb-6">
            <h3 class="text-lg font-medium text-gray-900 mb-2">{{ __('Step 4: Importing') }}</h3>
            <p class="text-sm text-gray-500">{{ __('Creating job openings from your data...') }}</p>
          </div>

          <div class="flex items-center justify-center py-12">
            <div class="text-center">
              <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-green-600 mx-auto mb-4"></div>
              <p class="text-gray-600">{{ importingMessage }}</p>
              <div class="mt-4 w-64 mx-auto">
                <div class="bg-gray-200 rounded-full h-2">
                  <div 
                    class="bg-green-600 h-2 rounded-full transition-all duration-300"
                    :style="{ width: importingProgress + '%' }"
                  ></div>
                </div>
                <p class="text-sm text-gray-500 mt-2">{{ importingProgress }}% {{ __('complete') }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 5: Results -->
        <div v-if="currentStep === 4" class="space-y-6">
          <div class="text-center mb-6">
            <h3 class="text-lg font-medium text-gray-900 mb-2">{{ __('Step 5: Results') }}</h3>
            <p class="text-sm text-gray-500">{{ __('Import completed. Review the results below.') }}</p>
          </div>

          <!-- Results Summary -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div class="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
              <div class="text-2xl font-bold text-green-600 mb-2">{{ results.success }}</div>
              <div class="text-sm text-green-700">{{ __('Successfully Created') }}</div>
            </div>
            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
              <div class="text-2xl font-bold text-yellow-600 mb-2">{{ results.warnings }}</div>
              <div class="text-sm text-yellow-700">{{ __('Warnings') }}</div>
            </div>
            <div class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
              <div class="text-2xl font-bold text-red-600 mb-2">{{ results.errors }}</div>
              <div class="text-sm text-red-700">{{ __('Errors') }}</div>
            </div>
          </div>

          <!-- Error Details -->
          <div v-if="results.errors > 0" class="bg-red-50 border border-red-200 rounded-lg p-6">
            <h4 class="font-medium text-red-900 mb-4">{{ __('Error Details') }}</h4>
            <div class="space-y-2 max-h-40 overflow-y-auto">
              <div v-for="(error, index) in errorDetails" :key="index" class="text-sm text-red-700">
                <strong>{{ __('Row') }} {{ error.row }}:</strong> {{ error.message }}
              </div>
            </div>
          </div>

          <!-- Warning Details -->
          <div v-if="results.warnings > 0" class="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <h4 class="font-medium text-yellow-900 mb-4">{{ __('Warning Details') }}</h4>
            <div class="space-y-2 max-h-40 overflow-y-auto">
              <div v-for="(warning, index) in warningDetails" :key="index" class="text-sm text-yellow-700">
                <strong>{{ __('Row') }} {{ warning.row }}:</strong> {{ warning.message }}
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-between items-center pt-6 border-t border-gray-200 mt-8">
          <Button 
            v-if="currentStep > 0 && currentStep < 4"
            variant="outline" 
            @click="previousStep"
            :disabled="processing"
          >
            {{ __('Previous') }}
          </Button>
          <div v-else></div>

          <div class="flex space-x-3">
            <Button 
              v-if="currentStep === 0"
              variant="outline" 
              @click="closeModal"
            >
              {{ __('Cancel') }}
            </Button>
            <Button 
              v-if="currentStep === 0"
              variant="solid" 
              @click="startProcessing"
              :disabled="!selectedFile"
            >
              {{ __('Next') }}
            </Button>
            <Button 
              v-if="currentStep === 2"
              variant="solid" 
              @click="startImporting"
            >
              {{ __('Import') }}
            </Button>
            <Button 
              v-if="currentStep === 4"
              variant="solid" 
              @click="closeModal"
            >
              {{ __('Done') }}
            </Button>
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { Dialog, Button, Select } from 'frappe-ui'
import { useToast } from '@/composables/useToast'
import { call } from 'frappe-ui'

const toast = useToast()

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'created', 'close'])

// Model
const show = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// State
const currentStep = ref(0)
const selectedFile = ref(null)
const selectedDepartment = ref('')
const selectedJobOpening = ref('')
const isDragOver = ref(false)
const isDownloading = ref(false)
const processing = ref(false)
const processingProgress = ref(0)
const processingMessage = ref('')
const importingProgress = ref(0)
const importingMessage = ref('')
const sessionId = ref(null)

// Add these
const isValidating = ref(false)
const isImporting = ref(false)
const validateOnly = ref(false)
const skipDuplicates = ref(true)
const importResults = ref(null)
const logFilter = ref('all')
const availableFields = ref([])        // [{ fieldname, label, fieldtype, reqd }]
const fieldMapping = ref({})           // { fieldname: 'Excel Header' }
const previewBundle = ref({            // unify preview for Step 3
  filename: '',
  total_rows: 0,
  columns: [],
  sample: []
})

// Steps configuration
const steps = [
  { title: 'Prepare & Upload' },
  { title: 'Processing' },
  { title: 'Review & Map' },
  { title: 'Importing' },
  { title: 'Results' }
]

// Job opening options - load from API
const jobOpeningOptions = ref([
  { label: '', value: '' }
])

// Department options
const departmentOptions = ref([
  { label: 'All Departments', value: '' },
  { label: 'Engineering', value: 'Engineering' },
  { label: 'Marketing', value: 'Marketing' },
  { label: 'Sales', value: 'Sales' },
  { label: 'HR', value: 'HR' },
  { label: 'Finance', value: 'Finance' }
])

// Job opening fields for mapping
const jobOpeningFields = ref([
  { label: 'Job Title', value: 'job_title' },
  { label: 'Department', value: 'department_name' },
  { label: 'Location', value: 'location_name' },
  { label: 'Number of Openings', value: 'number_of_openings' },
  { label: 'Posting Date', value: 'posting_date' },
  { label: 'Closing Date', value: 'closing_date' },
  { label: 'Status', value: 'approval_status' },
  { label: 'Owner', value: 'owner_id' },
  { label: 'Description', value: 'description' },
  { label: 'Requirements', value: 'requirements' },
  { label: 'Benefits', value: 'benefits' }
])

// Column mappings
const columnMappings = ref([])
const previewData = ref([])
const previewHeaders = ref([])

// Results
const results = reactive({
  success: 0,
  warnings: 0,
  errors: 0
})

const errorDetails = ref([])
const warningDetails = ref([])

// Refs
const fileInput = ref(null)

// Methods
const getStepClass = (index) => {
  if (currentStep > index) {
    return 'bg-blue-600 text-white'
  } else if (currentStep === index) {
    return 'bg-blue-600 text-white'
  } else {
    return 'bg-gray-300 text-gray-600'
  }
}

// const downloadTemplate = () => {
//   // Create a sample Excel template
//   const templateData = [
//     ['Job Title', 'Department', 'Location', 'Number of Openings', 'Posting Date', 'Closing Date', 'Status', 'Description', 'Requirements', 'Benefits'],
//     ['Software Engineer', 'Engineering', 'Ho Chi Minh City', '2', '2024-01-01', '2024-02-01', 'Draft', 'Develop software applications', 'Bachelor degree in Computer Science', 'Competitive salary and benefits'],
//     ['Marketing Manager', 'Marketing', 'Hanoi', '1', '2024-01-01', '2024-02-01', 'Draft', 'Lead marketing campaigns', '3+ years experience', 'Health insurance and flexible hours']
//   ]
  
//   // Convert to CSV and download
//   const csvContent = templateData.map(row => row.join(',')).join('\n')
//   const blob = new Blob([csvContent], { type: 'text/csv' })
//   const url = window.URL.createObjectURL(blob)
//   const a = document.createElement('a')
//   a.href = url
//   a.download = 'job_openings_template.csv'
//   a.click()
//   window.URL.revokeObjectURL(url)
  
//   toast.success(__('Template downloaded successfully'))
// }

// Template download
const downloadTemplate = async () => {
    isDownloading.value = true
    try {
        const response = await call('mbw_mira.mbw_mira.doctype.mira_importsession.mira_importsession.download_import_template')
        
        if (response.file_url) {
            const link = document.createElement('a')
            link.href = response.file_url
            link.download = response.file_name || 'job_import_template.xlsx'
            link.target = '_blank'
            link.style.display = 'none'
            
            document.body.appendChild(link)
            link.click()
            
            setTimeout(() => {
                document.body.removeChild(link)
            }, 100)
        } else {
            throw new Error('No file URL returned from server')
        }
        
        toast.success(__('Template downloaded successfully'))
    } catch (error) {
        console.error('Template download error:', error)
        toast.error(__('Failed to download template: ') + (error.message || 'Unknown error'))
    } finally {
        isDownloading.value = false
    }
}


const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
    processFilePreview(file)
  }
}

const handleFileDrop = (event) => {
  isDragOver.value = false
  const files = event.dataTransfer.files
  if (files.length > 0) {
    const file = files[0]
    selectedFile.value = file
    processFilePreview(file)
  }
}

const processFilePreview = async (file) => {
  currentStep.value = 1
  processing.value = true
  processingProgress.value = 0
  processingMessage.value = __('Reading file...')

  try {
    const formData = new FormData()
    formData.append('file', file)

    const resp = await fetch('/api/method/mbw_mira.mbw_mira.doctype.mira_importsession.mira_importsession.upload_and_preview', {
      method: 'POST',
      headers: { 'X-Frappe-CSRF-Token': window.csrf_token },
      body: formData
    })

    const json = await resp.json()
    if (!resp.ok || !json.message) {
      throw new Error(json?.exc || 'Failed to preview file')
    }

    const data = json.message

    // Normalize columns and sample to arrays
    const sampleIsArray = Array.isArray(data.sample)
    const firstRowObj = sampleIsArray ? (data.sample[0] || {}) : (data.sample || {})
    const normalizedColumns = Array.isArray(data.columns) && data.columns.length
      ? data.columns
      : Object.keys(firstRowObj || {})

    const normalizedSample = sampleIsArray
      ? data.sample
      : (data.sample ? [data.sample] : [])

    availableFields.value = Array.isArray(data.available_fields) ? data.available_fields : []

    previewBundle.value = {
      filename: data.filename || file.name,
      total_rows: Number.isFinite(data.total_rows) ? data.total_rows : normalizedSample.length,
      columns: normalizedColumns,
      sample: normalizedSample.map((row) => {
        const out = {}
        normalizedColumns.forEach((h) => {
          out[h] = row && typeof row === 'object' ? (row[h] ?? '') : ''
        })
        return out
      })
    }

    autoMapFields()
    currentStep.value = 2
    toast.success(__('File processed, please map columns'))
  } catch (e) {
    console.error('Preview error:', e)
    toast.error(__(e.message || 'Failed to process file'))
    currentStep.value = 0
  } finally {
    processing.value = false
  }
}

const previewFile = async (file) => {
  try {
    const response = await call('frappe.client.get_preview', {
      doctype: 'Mira Importsession',
      docname: sessionId.value,
      file_name: file.name,
      file_type: file.type
    })

    if (response.headers && response.data) {
      previewHeaders.value = response.headers
      previewData.value = response.data
    } else {
      throw new Error('Failed to get file preview')
    }
  } catch (error) {
    console.error('Error getting file preview:', error)
    toast.error(__('Error getting file preview: ') + (error.message || 'Unknown error'))
    currentStep.value = 0
  }
}

const startProcessing = async () => {
  if (!selectedFile.value) return
  
  currentStep.value = 1
  processing.value = true
  processingProgress.value = 0
  processingMessage.value = __('Reading file...')
  
  try {
    // Simulate file processing
    await simulateProcessing()
    
    // Parse the file and extract data
    await parseFile()
    
    currentStep.value = 2
  } catch (error) {
    console.error('Error processing file:', error)
    toast.error(__('Error processing file'))
    currentStep.value = 0
  } finally {
    processing.value = false
  }
}

const simulateProcessing = () => {
  return new Promise((resolve) => {
    const interval = setInterval(() => {
      processingProgress.value += 10
      if (processingProgress.value === 30) {
        processingMessage.value = __('Extracting data...')
      } else if (processingProgress.value === 60) {
        processingMessage.value = __('Validating data...')
      } else if (processingProgress.value === 90) {
        processingMessage.value = __('Finalizing...')
      } else if (processingProgress.value >= 100) {
        clearInterval(interval)
        resolve()
      }
    }, 200)
  })
}

const parseFile = async () => {
  // Simulate parsing file and creating column mappings
  const mockHeaders = ['Job Title', 'Department', 'Location', 'Number of Openings', 'Posting Date', 'Closing Date']
  const mockData = [
    ['Software Engineer', 'Engineering', 'Ho Chi Minh City', '2', '2024-01-01', '2024-02-01'],
    ['Marketing Manager', 'Marketing', 'Hanoi', '1', '2024-01-01', '2024-02-01'],
    ['Sales Representative', 'Sales', 'Da Nang', '3', '2024-01-01', '2024-02-01']
  ]
  
  previewHeaders.value = mockHeaders
  previewData.value = mockData.map((row, index) => {
    const obj = {}
    mockHeaders.forEach((header, i) => {
      obj[header] = row[i]
    })
    return obj
  })
  
  // Create column mappings
  columnMappings.value = mockHeaders.map(header => ({
    excelColumn: header,
    jobOpeningField: jobOpeningFields.value.find(field => 
      field.label.toLowerCase().includes(header.toLowerCase()) ||
      header.toLowerCase().includes(field.label.toLowerCase())
    )?.value || '',
    sampleData: mockData[0][mockHeaders.indexOf(header)]
  }))
}

const autoGuessFieldForHeader = (header) => {
  const h = String(header).toLowerCase()
  const candidates = jobOpeningFields.value || []
  // match theo label gần giống
  const found = candidates.find(f => {
    const lab = String(f.label).toLowerCase()
    return lab.includes(h) || h.includes(lab)
  })
  return found ? found.value : ''
}

const buildFieldMappingForImport = () => {
  // Convert columnMappings -> { fieldname: "Excel Header" }
  const mapping = {}
  for (const m of (columnMappings.value || [])) {
    if (m.jobOpeningField && m.excelColumn) {
      mapping[m.jobOpeningField] = m.excelColumn
    }
  }
  return mapping
}

const startImporting = async () => {
  if (!selectedFile.value) return

  currentStep.value = 3
  importingProgress.value = 0
  importingMessage.value = __('Creating job openings...')

  try {
    const mapping = buildFieldMappingForImport()
    if (!Object.keys(mapping).length) {
      throw new Error('Field mapping is required')
    }

    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('mapping', JSON.stringify(mapping))
    formData.append('selected_job_opening', selectedJobOpening.value || '') // optional
    formData.append('batch_size', '100')
    formData.append('validate_only', '0')
    formData.append('skip_duplicates', '1')

    const resp = await fetch('/api/method/mbw_mira.mbw_mira.doctype.mira_importsession.mira_importsession.import_with_mapping', {
      method: 'POST',
      headers: { 'X-Frappe-CSRF-Token': window.csrf_token },
      body: formData
    })
    const json = await resp.json()
    if (!resp.ok || !json.message) {
      throw new Error(json?.exc || 'Import failed')
    }

    const result = json.message
    sessionId.value = result.session_id || null

    // Kết quả
    results.success = result.success || 0
    results.errors = result.failed || 0
    results.warnings = 0

    errorDetails.value = (result.logs || [])
      .filter(l => l.status === 'error')
      .map(l => ({ row: l.row_number, message: l.message }))
    warningDetails.value = []

    importingProgress.value = 100
    importingMessage.value = __('Completed')
    currentStep.value = 4
    toast.success(__('Job openings imported successfully'))
    emit('created', { success: results.success, total: result.total || 0 })
  } catch (e) {
    console.error('Import error:', e)
    toast.error(__(e.message || 'Error importing job openings'))
    currentStep.value = 2
  }
}

const simulateImporting = () => {
  return new Promise((resolve) => {
    const interval = setInterval(() => {
      importingProgress.value += 20
      if (importingProgress.value === 40) {
        importingMessage.value = __('Validating data...')
      } else if (importingProgress.value === 80) {
        importingMessage.value = __('Saving to database...')
      } else if (importingProgress.value >= 100) {
        clearInterval(interval)
        resolve()
      }
    }, 300)
  })
}

const previousStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const closeModal = () => {
  // Reset state
  currentStep.value = 0
  selectedFile.value = null
  selectedDepartment.value = ''
  selectedJobOpening.value = ''
  processing.value = false
  processingProgress.value = 0
  importingProgress.value = 0
  columnMappings.value = []
  previewData.value = []
  previewHeaders.value = []
  results.success = 0
  results.warnings = 0
  results.errors = 0
  errorDetails.value = []
  warningDetails.value = []
  sessionId.value = null // Clear session ID
  
  show.value = false
  emit('close')
}

// Load job openings when component mounts
const loadJobOpenings = async () => {
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'JobOpening',
      fields: ['name', 'job_title', 'department_name', 'approval_status'],
      filters: {
        approval_status: ['in', ['Draft', 'Approved']]  // Only show active job openings
      },
      order_by: 'job_title asc'
    })
    
    jobOpeningOptions.value = [
      { label: '', value: '' },
      ...response.map(job => ({
        label: `${job.job_title} (${job.department_name || 'No Department'})`,
        value: job.name
      }))
    ]
  } catch (error) {
    console.error('Error loading job openings:', error)
    toast.error(__('Failed to load job openings'))
  }
}

// Call loadJobOpenings when component is created
onMounted(() => {
  loadJobOpenings()
})

let importProgressTimer = null

const startImportProgressPolling = () => {
  if (importProgressTimer) return
  importProgressTimer = setInterval(async () => {
    if (!sessionId.value) return
    try {
      const p = await call('mbw_mira.mbw_mira.doctype.mira_importsession.mira_importsession.get_import_progress', {
        session_id: sessionId.value
      })
      if (p && typeof p.progress_percentage === 'number') {
        importingProgress.value = Math.max(importingProgress.value, Math.floor(p.progress_percentage))
        importingMessage.value = __('Processing...')
        if (p.status === 'Completed') {
          clearInterval(importProgressTimer)
          importProgressTimer = null
        }
      }
    } catch {}
  }, 1000)
}

const stopImportProgressPolling = () => {
  if (importProgressTimer) {
    clearInterval(importProgressTimer)
    importProgressTimer = null
  }
}

const autoMapFields = () => {
  if (!previewBundle.value.columns.length || !availableFields.value.length) return
  const mapping = { ...fieldMapping.value }
  availableFields.value.forEach(field => {
    if (mapping[field.fieldname]) return
    const target = String(field.label).toLowerCase().trim().replace(/[\s_-]+/g, '')
    for (const header of previewBundle.value.columns) {
      const normalizedHeader = String(header).toLowerCase().trim().replace(/[\s_-]+/g, '')
      if (normalizedHeader.includes(target) || target.includes(normalizedHeader)) {
        mapping[field.fieldname] = header
        break
      }
    }
  })
  fieldMapping.value = mapping
}

const clearMapping = () => {
  fieldMapping.value = {}
}

const validateData = async () => {
  if (!availableFields.value.length || !previewBundle.value.columns.length) return
  const requiredMapped = availableFields.value.filter(f => f.reqd).every(f => fieldMapping.value[f.fieldname])
  if (!requiredMapped || !selectedFile.value) return

  isValidating.value = true
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('mapping', JSON.stringify(fieldMapping.value))
    formData.append('selected_job_opening', selectedJobOpening.value || '')
    formData.append('batch_size', '100')
    formData.append('validate_only', '1')
    formData.append('skip_duplicates', skipDuplicates.value ? '1' : '0')

    const resp = await fetch('/api/method/mbw_mira.mbw_mira.doctype.mira_importsession.mira_importsession.import_with_mapping', {
      method: 'POST',
      headers: { 'X-Frappe-CSRF-Token': window.csrf_token },
      body: formData
    })
    const json = await resp.json()
    if (!resp.ok || !json.message) {
      throw new Error(json?.exc || 'Validation failed')
    }
    importResults.value = json.message
    validateOnly.value = true
    currentStep.value = 4
    toast.success(__('Validation complete'))
  } catch (e) {
    console.error('Validation error:', e)
    toast.error(__(e.message || 'Validation failed'))
  } finally {
    isValidating.value = false
  }
}

const processImport = async () => {
  const requiredMapped = availableFields.value.filter(f => f.reqd).every(f => fieldMapping.value[f.fieldname])
  if (!requiredMapped || !selectedFile.value) return

  isImporting.value = true
  validateOnly.value = false
  currentStep.value = 3
  importingProgress.value = 0
  importingMessage.value = __('Creating job openings...')

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('mapping', JSON.stringify(fieldMapping.value))
    formData.append('selected_job_opening', selectedJobOpening.value || '')
    formData.append('batch_size', '100')
    formData.append('validate_only', '0')
    formData.append('skip_duplicates', skipDuplicates.value ? '1' : '0')

    const resp = await fetch('/api/method/mbw_mira.mbw_mira.doctype.mira_importsession.mira_importsession.import_with_mapping', {
      method: 'POST',
      headers: { 'X-Frappe-CSRF-Token': window.csrf_token },
      body: formData
    })
    const json = await resp.json()
    if (!resp.ok || !json.message) {
      throw new Error(json?.exc || 'Import failed')
    }

    const result = json.message
    sessionId.value = result.session_id || null
    importResults.value = result

    results.success = result.success || 0
    results.errors = result.failed || 0
    results.warnings = 0

    errorDetails.value = (result.logs || [])
      .filter(l => l.status === 'error')
      .map(l => ({ row: l.row_number, message: l.message }))
    warningDetails.value = []

    importingProgress.value = 100
    importingMessage.value = __('Completed')
    currentStep.value = 4
    toast.success(__('Job openings imported successfully'))
    emit('created', { success: results.success, total: result.total || 0 })
  } catch (e) {
    console.error('Import error:', e)
    toast.error(__(e.message || 'Error importing job openings'))
    currentStep.value = 2
  } finally {
    isImporting.value = false
  }
}
</script> 

<style scoped>
/* Main Layout */
.candidate-uploader {
    max-width: 1200px;
    margin: 0 auto;
    padding: 24px;
}

/* Step Content */
.step-content {
    animation: slideIn 0.3s ease-in-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.step-header {
    text-align: center;
    margin-bottom: 32px;
    padding-bottom: 16px;
    border-bottom: 1px solid #e5e7eb;
}

.step-title {
    font-size: 24px;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 8px;
}

.step-description {
    font-size: 16px;
    color: #6b7280;
}

/* Card Components */
.card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition: all 0.2s ease;
}

.card:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.card-header {
    padding: 20px 24px 16px;
    border-bottom: 1px solid #f3f4f6;
    background: #fafafa;
}

.card-title {
    font-size: 16px;
    font-weight: 600;
    color: #1f2937;
    margin: 0;
}

.card-subtitle {
    font-size: 14px;
    color: #6b7280;
    margin: 4px 0 0 0;
}

.card-body {
    padding: 24px;
}

/* Icon Circles */
.icon-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

/* Drop Zone */
.drop-zone {
    border: 2px dashed #d1d5db;
    border-radius: 12px;
    transition: all 0.3s ease;
    background-color: #fafafa;
    cursor: pointer;
}

.drop-zone:hover,
.drop-zone.drag-over {
    border-color: #3b82f6;
    background-color: #eff6ff;
    transform: scale(1.01);
}

/* Buttons */
.btn {
    display: inline-flex;
    align-items: center;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid transparent;
    font-size: 14px;
    text-decoration: none;
    line-height: 1.4;
}

.btn-sm {
    padding: 6px 12px;
    font-size: 12px;
}

.btn-lg {
    padding: 14px 28px;
    font-size: 16px;
}

.btn-primary {
    background-color: gray;
    color: white;
    border-color: gray;
}

.btn-primary:hover:not(:disabled) {
    background-color: gray;
    border-color: gray;
    transform: translateY(-1px);
}

.btn-success {
    background-color: #10b981;
    color: white;
    border-color: #10b981;
}

.btn-success:hover:not(:disabled) {
    background-color: #059669;
    border-color: #059669;
}

.btn-outline {
    border-color: #d1d5db;
    color: #374151;
    background-color: white;
}

.btn-outline:hover:not(:disabled) {
    background-color: #f9fafb;
    border-color: #9ca3af;
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}

/* Field Mapping Grid */
.mapping-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
}

@media (min-width: 768px) {
    .mapping-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Field Mapping */
.mapping-field {
    padding: 16px;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    background: #fafafa;
    transition: all 0.2s ease;
}

.mapping-field:hover {
    background: #f3f4f6;
    border-color: #d1d5db;
}

.mapping-field select {
    appearance: none;
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
    background-position: right 8px center;
    background-repeat: no-repeat;
    background-size: 16px 12px;
    padding-right: 40px;
    transition: all 0.2s ease;
}

.mapping-field select:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Progress & Loading */
.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f4f6;
    border-top: 4px solid #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto;
}

.progress-spinner {
    width: 60px;
    height: 60px;
    border: 6px solid #f3f4f6;
    border-top: 6px solid #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Statistics Cards */
.stat-card {
    padding: 24px;
    border-radius: 12px;
    text-align: center;
    border: 2px solid;
    transition: all 0.2s ease;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.1);
}

.stat-card.success {
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
    border-color: #10b981;
}

.stat-card.error {
    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
    border-color: #ef4444;
}

.stat-card.total {
    background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
    border-color: #3b82f6;
}

.stat-value {
    font-size: 32px;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 8px;
}

.stat-card.success .stat-value {
    color: #047857;
}

.stat-card.error .stat-value {
    color: #dc2626;
}

.stat-card.total .stat-value {
    color: #1d4ed8;
}

.stat-label {
    font-size: 14px;
    font-weight: 500;
    opacity: 0.8;
}

/* Log Entries */
.log-entry {
    padding: 16px;
    border-radius: 8px;
    border-left: 4px solid;
    margin-bottom: 8px;
    transition: all 0.2s ease;
}

.log-entry:hover {
    transform: translateX(4px);
}

.log-entry.success {
    background: #f0fdf4;
    border-left-color: #22c55e;
}

.log-entry.error {
    background: #fef2f2;
    border-left-color: #ef4444;
}

.log-entry.warning {
    background: #fffbeb;
    border-left-color: #f59e0b;
}

/* Status Badges */
.status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.025em;
}

.bg-green-100 {
    background-color: #dcfce7;
    color: #166534;
}

.bg-red-100 {
    background-color: #fee2e2;
    color: #991b1b;
}

.bg-yellow-100 {
    background-color: #fef3c7;
    color: #92400e;
}

.bg-gray-100 {
    background-color: #f3f4f6;
    color: #374151;
}

.bg-blue-100 {
    background-color: #dbeafe;
    color: #1e40af;
}

/* Alerts */
.alert {
    padding: 16px;
    border-radius: 8px;
    border: 1px solid;
}

.alert-warning {
    background-color: #fffbeb;
    border-color: #fbbf24;
    color: #92400e;
}

/* Form Elements */
.form-checkbox {
    border-radius: 4px;
    border: 2px solid #d1d5db;
    transition: all 0.2s ease;
}

.form-checkbox:checked {
    background-color: #3b82f6;
    border-color: #3b82f6;
}

.form-checkbox:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Transitions and Animations */
.animate-spin {
    animation: spin 1s linear infinite;
}

.transition-all {
    transition: all 0.3s ease;
}

/* Table Styling */
.overflow-x-auto table {
    border-collapse: separate;
    border-spacing: 0;
}

.overflow-x-auto th,
.overflow-x-auto td {
    white-space: nowrap;
}

.max-w-xs {
    max-width: 200px;
}

.truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* Progress Bar */
.bg-blue-600 {
    background-color: #2563eb;
}

.h-3 {
    height: 12px;
}

.rounded-full {
    border-radius: 9999px;
}

/* Responsive Design */
@media (max-width: 768px) {
    .candidate-uploader {
        padding: 16px;
    }
    
    .step-header {
        margin-bottom: 24px;
    }
    
    .step-title {
        font-size: 20px;
    }
    
    .card-header,
    .card-body {
        padding: 16px;
    }
    
    .grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-3 {
        grid-template-columns: 1fr;
        gap: 16px;
    }
    
    .grid.grid-cols-1.md\\:grid-cols-3 {
        grid-template-columns: 1fr;
        gap: 12px;
    }
    
    .flex.space-x-3 {
        flex-direction: column;
        gap: 8px;
    }
    
    .flex.space-x-3 > * + * {
        margin-left: 0;
    }
    
    .btn {
        justify-content: center;
        width: 100%;
    }
    
    .drop-zone {
        padding: 16px;
    }
    
    .stat-card {
        padding: 16px;
    }
    
    .stat-value {
        font-size: 24px;
    }
}

@media (max-width: 480px) {
    .step-title {
        font-size: 18px;
    }
    
    .step-description {
        font-size: 14px;
    }
    
    .card-title {
        font-size: 14px;
    }
    
    .card-subtitle {
        font-size: 12px;
    }
}

/* Dark mode support (if needed) */
@media (prefers-color-scheme: dark) {
    .card {
        background: #1f2937;
        border-color: #374151;
    }
    
    .card-header {
        background: #111827;
        border-color: #374151;
    }
    
    .card-title {
        color: #f9fafb;
    }
    
    .card-subtitle {
        color: #9ca3af;
    }
    
    .step-title {
        color: #f9fafb;
    }
    
    .step-description {
        color: #9ca3af;
    }
}

/* Print styles */
@media print {
    .candidate-uploader {
        padding: 0;
    }
    
    .step-content {
        animation: none;
    }
    
    .card {
        box-shadow: none;
        border: 1px solid #000;
    }
    
    .btn {
        display: none;
    }
}

/* Accessibility improvements */
.btn:focus {
    outline: 2px solid #3b82f6;
    outline-offset: 2px;
}

.mapping-field select:focus {
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* High contrast mode support */
@media (prefers-contrast: high) {
    .card {
        border-width: 2px;
    }
    
    .btn {
        border-width: 2px;
    }
    
    .drop-zone {
        border-width: 3px;
    }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
    .step-content {
        animation: none;
    }
    
    .spinner,
    .progress-spinner {
        animation: none;
    }
    
    .btn,
    .card,
    .log-entry {
        transition: none;
    }
    
    .drop-zone {
        transform: none;
    }
    
    .card:hover,
    .btn:hover,
    .log-entry:hover {
        transform: none;
    }
}

/* Additional utility classes */
.text-green-600 {
    color: #059669;
}

.text-red-600 {
    color: #dc2626;
}

.text-blue-600 {
    color: #2563eb;
}

.text-yellow-600 {
    color: #d97706;
}

.text-gray-600 {
    color: #4b5563;
}

.text-gray-500 {
    color: #6b7280;
}

.text-gray-400 {
    color: #9ca3af;
}

.bg-gray-50 {
    background-color: #f9fafb;
}

.bg-gray-200 {
    background-color: #e5e7eb;
}

.border-gray-300 {
    border-color: #d1d5db;
}

.border-red-500 {
    border-color: #ef4444;
}

.ring-red-500 {
    --tw-ring-color: #ef4444;
}

.ring-blue-500 {
    --tw-ring-color: #3b82f6;
}

/* Focus ring utilities */
.focus\:ring-2:focus {
    --tw-ring-offset-shadow: var(--tw-ring-inset) 0 0 0 var(--tw-ring-offset-width) var(--tw-ring-offset-color);
    --tw-ring-shadow: var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color);
    box-shadow: var(--tw-ring-offset-shadow), var(--tw-ring-shadow), var(--tw-shadow, 0 0 #0000);
}

.focus\:border-blue-500:focus {
    border-color: #3b82f6;
}

/* Grid utilities */
.grid {
    display: grid;
}

.grid-cols-1 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
}

.gap-4 {
    gap: 1rem;
}

.gap-8 {
    gap: 2rem;
}

.gap-12 {
    gap: 3rem;
}

.gap-16 {
    gap: 4rem;
}

/* Flex utilities */
.flex {
    display: flex;
}

.flex-1 {
    flex: 1 1 0%;
}

.flex-shrink-0 {
    flex-shrink: 0;
}

.items-center {
    align-items: center;
}

.items-start {
    align-items: flex-start;
}

.justify-center {
    justify-content: center;
}

.justify-between {
    justify-content: space-between;
}

.space-x-2 > * + * {
    margin-left: 0.5rem;
}

.space-x-3 > * + * {
    margin-left: 0.75rem;
}

.space-x-4 > * + * {
    margin-left: 1rem;
}

.space-y-2 > * + * {
    margin-top: 0.5rem;
}

.space-y-3 > * + * {
    margin-top: 0.75rem;
}

.space-y-4 > * + * {
    margin-top: 1rem;
}

/* Spacing utilities */
.p-4 {
    padding: 1rem;
}

.p-5 {
    padding: 1.25rem;
}

.p-6 {
    padding: 1.5rem;
}

.p-8 {
    padding: 2rem;
}

.px-3 {
    padding-left: 0.75rem;
    padding-right: 0.75rem;
}

.px-4 {
    padding-left: 1rem;
    padding-right: 1rem;
}

.py-1 {
    padding-top: 0.25rem;
    padding-bottom: 0.25rem;
}

.py-2 {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
}

.py-4 {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

.py-8 {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.py-12 {
    padding-top: 3rem;
    padding-bottom: 3rem;
}

.mb-1 {
    margin-bottom: 0.25rem;
}

.mb-2 {
    margin-bottom: 0.5rem;
}

.mb-3 {
    margin-bottom: 0.75rem;
}

.mb-4 {
    margin-bottom: 1rem;
}

.mb-6 {
    margin-bottom: 1.5rem;
}

.mb-8 {
    margin-bottom: 2rem;
}

.mr-1 {
    margin-right: 0.25rem;
}

.mr-2 {
    margin-right: 0.5rem;
}

.mr-3 {
    margin-right: 0.75rem;
}

.ml-2 {
    margin-left: 0.5rem;
}

.ml-3 {
    margin-left: 0.75rem;
}

.mt-1 {
    margin-top: 0.25rem;
}

.mt-2 {
    margin-top: 0.5rem;
}

.mt-6 {
    margin-top: 1.5rem;
}

/* Width and height utilities */
.w-4 {
    width: 1rem;
}

.w-5 {
    width: 1.25rem;
}

.w-8 {
    width: 2rem;
}

.w-12 {
    width: 3rem;
}

.w-16 {
    width: 4rem;
}

.w-full {
    width: 100%;
}

.h-0\.5 {
    height: 0.125rem;
}

.h-4 {
    height: 1rem;
}

.h-5 {
    height: 1.25rem;
}

.h-8 {
    height: 2rem;
}

.h-12 {
    height: 3rem;
}

.h-16 {
    height: 4rem;
}

.max-h-64 {
    max-height: 16rem;
}

.max-h-96 {
    max-height: 24rem;
}

.max-w-md {
    max-width: 28rem;
}

/* Position utilities */
.sticky {
    position: sticky;
}

.top-0 {
    top: 0;
}

/* Text utilities */
.text-xs {
    font-size: 0.75rem;
    line-height: 1rem;
}

.text-sm {
    font-size: 0.875rem;
    line-height: 1.25rem;
}

.text-lg {
    font-size: 1.125rem;
    line-height: 1.75rem;
}

.text-xl {
    font-size: 1.25rem;
    line-height: 1.75rem;
}

.text-2xl {
    font-size: 1.5rem;
    line-height: 2rem;
}

.font-medium {
    font-weight: 500;
}

.font-semibold {
    font-weight: 600;
}

.font-bold {
    font-weight: 700;
}

.uppercase {
    text-transform: uppercase;
}

.text-center {
    text-align: center;
}

.text-left {
    text-align: left;
}

/* Border utilities */
.border {
    border-width: 1px;
}

.border-b {
    border-bottom-width: 1px;
}

.border-l {
    border-left-width: 1px;
}

.border-2 {
    border-width: 2px;
}

.rounded {
    border-radius: 0.25rem;
}

.rounded-md {
    border-radius: 0.375rem;
}

.rounded-lg {
    border-radius: 0.5rem;
}

.rounded-full {
    border-radius: 9999px;
}

/* Display utilities */
.block {
    display: block;
}

.inline-block {
    display: inline-block;
}

.hidden {
    display: none;
}

/* Overflow utilities */
.overflow-hidden {
    overflow: hidden;
}

.overflow-x-auto {
    overflow-x: auto;
}

.overflow-y-auto {
    overflow-y: auto;
}

/* Cursor utilities */
.cursor-pointer {
    cursor: pointer;
}

.cursor-not-allowed {
    cursor: not-allowed;
}

/* Opacity utilities */
.opacity-50 {
    opacity: 0.5;
}

.opacity-80 {
    opacity: 0.8;
}

/* Transform utilities */
.transform {
    transform: var(--tw-transform);
}

.scale-101 {
    --tw-scale-x: 1.01;
    --tw-scale-y: 1.01;
    transform: scale(var(--tw-scale-x), var(--tw-scale-y));
}

/* Transition utilities */
.duration-300 {
    transition-duration: 300ms;
}

.duration-500 {
    transition-duration: 500ms;
}

.ease-in-out {
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
</style>