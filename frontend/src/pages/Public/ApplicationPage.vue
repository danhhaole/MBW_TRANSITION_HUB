<template>
    <div class="flex justify-center items-center min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 py-8 container mx-auto">
      <div class="w-full max-w-xl bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-gray-600 rounded-full mb-4">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">{{ __('Apply for campaign') }}</h1>
          <p class="text-gray-600">{{ __('Please fill in the information and upload your CV') }}</p>
        </div>
        <form @submit.prevent="submit">
          <div class="space-y-5">
            <!-- Debug: Show fields array -->
            <!-- {{ fields }} -->
            
            <!-- Basic fields without complex filtering -->
            <FormControl
              v-model="form.email"
              type="email"
              label="Email"
              required
              placeholder="example@email.com"
              class="mb-2"
            />
            
            <FormControl
              v-model="form.full_name"
              type="text"
              label="Full Name"
              required
              class="mb-2"
            />
            
            <FormControl
              v-model="form.position"
              type="text"
              label="Position"
              placeholder="Position you want to apply for"
              class="mb-2"
            />
            
            <FormControl
              v-model="form.campaign_id"
              type="select"
              label="Campaign"
              :options="campaignOptions"
              required
              class="mb-2"
            />
            <FormControl
              v-model="form.segment_id"
              type="select"
              label="Segment (if any)"
              :options="segmentOptions"
              class="mb-2"
            />
            <div>
              <label class="block font-semibold mb-1 text-gray-700">{{ __('Upload CV (PDF, DOCX)') }}</label>
              <FileUploader
              :fileTypes="['.pdf', '.doc', '.docx']"
              :max-size="5 * 1024 * 1024"
              @success="onFileSuccess"
              @error="onFileError"
            >
              <template #default="{ file, uploading, progress, uploaded, message, error, total, success, openFileSelector }">
                <div class="flex items-center gap-3">
                  <Button 
                    type="button" 
                    theme="gray" 
                    @click.prevent="openFileSelector" 
                    :loading="uploading"
                  >
                    <span v-if="!file">{{ __('Select file') }}</span>
                    <span v-else>{{ uploading ? `${__('Uploading...')} ${progress}%` : getFileName(file) }}</span>
                  </Button>
                  <span v-if="file && !uploading && !error" class="text-green-600 text-xs">{{ __('Selected') }}: {{ getFileName(file) }}</span>
                  <span v-if="error" class="text-red-600 text-xs">{{ error }}</span>
                </div>
              </template>
            </FileUploader>
            </div>
          </div>
          <div class="mt-8 flex justify-end">
            <Button type="submit" theme="gray" :loading="loading" class="w-full py-3 text-lg font-semibold rounded-xl">
              {{ __('Apply') }}
            </Button>
          </div>
        </form>
      </div>
    </div>
    <ToastContainer />
  </template>
  <script setup>
  import { ref, onMounted } from 'vue'
  import { FormControl, Button, FileUploader, call } from 'frappe-ui'
  import { ToastContainer } from '@/components/shared'
  import { useToast } from '@/composables/useToast'

  const { showToast, showSuccess, showError } = useToast()

  const form = ref({
    email: '',
    full_name: '',
    campaign_id: '',
    position: '',
    segment_id: '',
    resume: ''
  })
  
  // Fix: Initialize fields as empty array to prevent undefined error
  const fields = ref([
    { fieldname: 'email', label: 'Email', type: 'email', required: true, placeholder: 'example@email.com' },
    { fieldname: 'full_name', label: 'Họ tên', type: 'text', required: true },
    { fieldname: 'position', label: 'Vị trí ứng tuyển', type: 'text', placeholder: 'Vị trí bạn muốn ứng tuyển' },
  ])
  
  const campaignOptions = ref([])
  const segmentOptions = ref([])
  const loading = ref(false)
  
  onMounted(async () => {
    try {
      // Lấy danh sách campaign
      const campaigns = await call('frappe.client.get_list', {
        doctype: 'Campaign',
        fields: ['name', 'campaign_name'],
        filters: {
          status: 'ACTIVE',
          is_active: 1
        },
        order_by: 'campaign_name asc',
        limit_page_length: 1000
      })
      campaignOptions.value = (campaigns || []).map(c => ({ 
        label: c.campaign_name || c.name, 
        value: c.name 
      }))
  
      // Lấy danh sách segment
      const segments = await call('frappe.client.get_list', {
        doctype: 'Mira Segment',
        fields: ['name', 'title'],
        order_by: 'title asc',
        limit_page_length: 1000
      })
      segmentOptions.value = (segments || []).map(s => ({ 
        label: s.title || s.name, 
        value: s.name 
      }))
    } catch (error) {
      console.error('Error loading data:', error)
      // Add empty option để không bị lỗi
      campaignOptions.value = []
      segmentOptions.value = []
    }
  })
  
  function getFileName(file) {
    if (!file) return ''
    if (typeof file === 'string') return file.split('/').pop()
    if (file && file.name) return file.name
    return 'Unknown file'
  }
  
  function onFileSuccess(file) {
    form.value.resume = file.url || file.file_url || file.name || file
    console.log('File uploaded successfully:', file)
  }
  
  function onFileError(error) {
    form.value.resume = ''
    console.error('File upload error:', error)
  }
  
  async function submit() {
    // Validation
    if (!form.value.email || !form.value.full_name || !form.value.campaign_id) {
      showError('Please fill in all required fields!')
      return
    }
  
    loading.value = true
    try {
      const payload = { ...form.value }
      console.log('Submitting payload:', payload)
      
      const res = await call('mbw_mira.api.submit_application', payload)
      console.log('API Response:', res)
      
      if (res && res.success) {
        showSuccess(res.message || 'Application submitted successfully!')
        // Reset form sau khi thành công
        form.value = {
          email: '',
          full_name: '',
          campaign_id: '',
          position: '',
          segment_id: '',
          resume: ''
        }
      } else {
        showError(res?.message || 'An error occurred!')
      }
    } catch (e) {
      console.error('Submit error:', e)
      showError(e.message || 'An error occurred while submitting the information!')
    } finally {
      loading.value = false
    }
  }
  </script>
  
  <style scoped>
  .file-uploader {
    @apply flex items-center gap-3 mt-2;
  }
  .file-uploader .file-info {
    @apply text-green-600 text-xs;
  }
  .file-uploader .file-error {
    @apply text-red-600 text-xs;
  }
  .file-uploader .file-btn {
    @apply rounded-lg px-4 py-2 font-medium shadow-sm transition-all duration-200;
  }
  </style>