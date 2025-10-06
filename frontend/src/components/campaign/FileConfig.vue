<template>
  <div class="file-config">
    <div class="space-y-6">
      <!-- 1. Upload -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Select File') }} <span class="text-red-500">*</span>
        </label>

        <FileUploader :fileTypes="['.csv', '.xlsx', '.xls']" :upload-args="{
          doctype: 'Campaign',
          docname: 'temp',
          private: false,
        }" v-model="uploadedFileUrl" @success="handleFileUploadSuccess">
          <template v-slot="{
            file,
            uploading,
            progress,
            uploaded,
            message,
            error,
            openFileSelector,
          }">
            <!-- Uploaded file -->
            <div v-if="uploadedFileUrl" class="space-y-4">
              <div class="flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-lg">
                <div class="flex items-center space-x-3">
                  <svg class="h-10 w-10 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <div class="min-w-0">
                    <a :href="uploadedFileUrl" target="_blank"
                      class="text-sm font-medium text-green-900 hover:text-green-700 underline block truncate">
                      {{ uploadedFileUrl.split('/').pop() }}
                    </a>
                    <div v-if="selectedFile" class="text-xs text-green-700 mt-1">
                      {{ formatFileSize(selectedFile.size) }} • {{ __('Click to download') }}
                    </div>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <Button variant="outline" theme="gray" @click="openFileSelector()" class="text-xs px-2 py-1">
                    {{ __('Change') }}
                  </Button>
                  <button type="button" @click="removeFile" class="text-red-500 hover:text-red-700 p-1">
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Uploading -->
            <div v-else-if="uploading" class="space-y-4">
              <div class="border-2 border-dashed border-blue-300 rounded-lg p-8 text-center bg-blue-50">
                <svg class="mx-auto h-12 w-12 text-blue-500 animate-pulse" stroke="currentColor" fill="none"
                  viewBox="0 0 48 48">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" />
                </svg>
                <div class="mt-4">
                  <p class="text-sm font-medium text-blue-900">{{ __('Uploading...') }}</p>
                  <div class="mt-2 w-full bg-blue-200 rounded-full h-2">
                    <div class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      :style="`width: ${progress}%`" />
                  </div>
                  <p class="text-xs text-blue-700 mt-1">{{ progress }}%</p>
                </div>
              </div>
            </div>

            <!-- Dropzone -->
            <div v-else
              class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-400 transition-colors cursor-pointer group"
              @click="openFileSelector()">
              <svg class="mx-auto h-12 w-12 text-gray-400 group-hover:text-gray-500" stroke="currentColor" fill="none"
                viewBox="0 0 48 48">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" />
              </svg>
              <div class="mt-4">
                <p class="text-sm font-medium text-gray-900 group-hover:text-gray-700">
                  {{ __('Click to upload or drag and drop') }}
                </p>
                <p class="text-xs text-gray-500 mt-1">
                  {{ __('CSV, XLSX files up to 10MB') }}
                </p>
              </div>
              <div class="mt-4">
                <Button variant="solid" theme="gray" class="inline-flex items-center">
                  <div class="flex items-center">
                    <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                    </svg>
                    {{ __('Select File') }}
                  </div>

                </Button>
              </div>
            </div>

            <!-- Error -->
            <div v-if="error" class="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
              <div class="flex items-center">
                <svg class="h-5 w-5 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="text-red-700 text-sm">{{ error }}</span>
              </div>
            </div>
          </template>
        </FileUploader>
      </div>

      <!-- 2. Source Target Selection -->
      <div v-if="uploadedFileUrl">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Import Target') }} <span class="text-red-500">*</span>
        </label>
        <div class="flex space-x-6 mb-4">
          <label class="flex items-center space-x-2">
            <input type="radio" value="contact" v-model="sourceTarget" class="rounded" />
            <span class="text-sm">{{ __('Contact') }}</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="radio" value="talent" v-model="sourceTarget" class="rounded" />
            <span class="text-sm">{{ __('Talent') }}</span>
          </label>
        </div>
      </div>

      <!-- 3. Hướng dẫn -->
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 class="text-sm font-medium text-blue-900 mb-2">{{ __('File Format Requirements') }}</h4>
        <ul class="text-xs text-blue-800 space-y-1">
          <li>• {{ __('First row should contain column headers') }}</li>
          <li>• {{ __('Required columns: full_name, email') }}</li>
          <li>• {{ __('Optional columns: phone, current_position, location, skills') }}</li>
          <li>• {{ __('Skills should be comma-separated') }}</li>
        </ul>
      </div>

      <!-- 3. Preview file -->
      <div v-if="selectedFile && filePreview.length > 0">
        <h4 class="text-sm font-medium text-gray-900 mb-2">{{ __('File Preview') }}</h4>
        <div class="border border-gray-200 rounded-lg overflow-hidden">
          <div class="bg-gray-50 px-4 py-2 border-b">
            <p class="text-xs text-gray-600">{{ __('First 3 rows') }}</p>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full text-xs">
              <thead class="bg-gray-50">
                <tr>
                  <th v-for="header in fileHeaders" :key="header"
                    class="px-3 py-2 text-left font-medium text-gray-900 border-r">
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

      <!-- 4. Mapping Columns -> DocType Fields -->
      <div v-if="parsedFileMeta">
        <h4 class="text-sm font-medium text-gray-900 mb-2">{{ __('Map Columns to Fields') }}</h4>

        <div class="border border-gray-200 rounded-lg overflow-hidden">
          <table class="min-w-full text-xs">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-3 py-2 text-left font-medium text-gray-900 border-r">{{ __('File Column') }}</th>
                <th class="px-3 py-2 text-left font-medium text-gray-900 border-r">{{ __('Sample Values') }}</th>
                <th class="px-3 py-2 text-left font-medium text-gray-900">{{ __('Target Field') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="col in parsedFileMeta.headers" :key="col" class="border-t">
                <td class="px-3 py-2 text-gray-700 border-r">{{ col }}</td>
                <td class="px-3 py-2 text-gray-500 border-r">
                  {{(parsedFileMeta.meta_columns.find(m => m.column === col)?.sample_values || []).join(', ')}}
                </td>
                <td class="px-3 py-2">
                  <FormControl type="select" v-model="columnMapping[col]" :options="targetFieldOptions"
                    :placeholder="__('Select field')" class="w-full" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Required fields warning -->
        <p v-if="missingRequired.length" class="text-xs text-red-600 mt-2">
          {{ __('Missing required fields:') }} {{ missingRequired.join(', ') }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { FileUploader, Button, FormControl, call } from 'frappe-ui'

// Props & Emits
const props = defineProps({
  modelValue: { type: Object, default: () => ({}) },
  metaDoctype: { type: String, default: 'Mira Talent' } // Doctype đích
})
const emit = defineEmits(['update:modelValue'])

// State
const selectedFile = ref(null)
const uploadedFileUrl = ref('')
const filePreview = ref([])
const fileHeaders = ref([])
const parsedFileMeta = ref(null)
const columnMapping = ref({})
const sourceTarget = ref('contact') // Default to contact

// i18n helper
const __ = (text, params = []) =>
  params.length === 0 ? text : text.replace(/\{(\d+)\}/g, (_, i) => params[i] ?? _)

// =========================
// Utils
// =========================
const formatFileSize = (bytes) => {
  if (!bytes) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const updateModelValue = () => {
  emit('update:modelValue', {
    ...props.modelValue,
    selectedFile: selectedFile.value,
    uploadedFileUrl: uploadedFileUrl.value,
    filePreview: filePreview.value,
    fileHeaders: fileHeaders.value,
    mapping: columnMapping.value,
    parsedFileMeta: parsedFileMeta.value,
    sourceTarget: sourceTarget.value
  })
}

// =========================
// File Handling
// =========================
const handleFileUploadSuccess = async (file) => {
  selectedFile.value = {
    name: file.file_name,
    size: file.file_size || 0,
    type: file.content_type || '',
    url: file.file_url
  }
  uploadedFileUrl.value = file.file_url

  // Preview CSV simple (optional)
  const ext = '.' + file.file_name.split('.').pop().toLowerCase()
  if (ext === '.csv') await previewCSVFromUrl(file.file_url)

  // Gọi API parse file (BE đã viết)
  try {
    const res = await call('mbw_mira.api.file_parser.parse_uploaded_file', {
      file_name: file.file_name,
      meta_doctype: props.metaDoctype,
    })
    parsedFileMeta.value = res
    autoGuessMapping()
  } catch (err) {
    console.error('parse_uploaded_file error:', err)
    parsedFileMeta.value = null
  }

  updateModelValue()
}

const previewCSVFromUrl = async (url) => {
  try {
    const text = await (await fetch(url)).text()
    const lines = text.split('\n').filter(l => l.trim())
    if (!lines.length) return
    fileHeaders.value = lines[0].split(',').map(h => h.trim().replace(/"/g, ''))
    filePreview.value = lines.slice(1).map(line =>
      line.split(',').map(c => c.trim().replace(/"/g, ''))
    )
  } catch (e) {
    console.error('previewCSVFromUrl error:', e)
  }
}

const removeFile = () => {
  selectedFile.value = null
  uploadedFileUrl.value = ''
  filePreview.value = []
  fileHeaders.value = []
  parsedFileMeta.value = null
  columnMapping.value = {}
  sourceTarget.value = 'contact' // Reset to default
  updateModelValue()
}

// =========================
// Mapping
// =========================
const targetFieldOptions = computed(() =>
  (parsedFileMeta.value?.target_fields || []).map(f => ({
    label: `${f.label || f.fieldname}${f.reqd ? ' *' : ''} (${f.fieldtype})`,
    value: f.fieldname
  }))
)

const missingRequired = computed(() => {
  if (!parsedFileMeta.value) return []
  return parsedFileMeta.value.target_fields
    .filter(f => f.reqd)
    .filter(f => !Object.values(columnMapping.value).includes(f.fieldname))
    .map(f => f.label || f.fieldname)
})

const autoGuessMapping = () => {
  if (!parsedFileMeta.value) return
  const fields = parsedFileMeta.value.target_fields || []
  const findMatch = (col) => {
    const norm = col.toLowerCase().replace(/\s+/g, '')
    const f = fields.find(field => {
      const lab = (field.label || '').toLowerCase().replace(/\s+/g, '')
      const fn = (field.fieldname || '').toLowerCase()
      return lab === norm || fn === norm
    })
    return f?.fieldname || ''
  }
  const newMap = {}
  parsedFileMeta.value.headers.forEach(h => {
    newMap[h] = findMatch(h)
  })
  columnMapping.value = newMap
}

// =========================
// Watchers
// =========================
watch(() => props.modelValue, (nv) => {
  // sync down if parent changed (optional)
  if (!nv?.selectedFile && selectedFile.value) removeFile()
}, { deep: true })

watch(columnMapping, updateModelValue, { deep: true })
watch(parsedFileMeta, updateModelValue, { deep: true })
watch(sourceTarget, updateModelValue)
</script>

<style scoped>
.file-config {
  max-width: 100%;
}

.border-dashed {
  border-style: dashed;
}

table {
  border-collapse: collapse;
}

th,
td {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px;
}
</style>
