<template>
  <div class="min-h-screen bg-gray-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header>
        <Button variant="solid" theme="gray" @click="openCreateDialog" :loading="loading">
          <template #prefix>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
          </template>
          {{ __('Create Candidate') }}
        </Button>
      </template>
    </LayoutHeader>

    <div class="container mx-auto px-6 py-6">
      <div class="flex items-center justify-between mb-6">
        <div class="relative">
          <input v-model="searchText" type="text" :placeholder="__('Search by name...')"
            class="block w-60 pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            @input="handleSearchInput" />
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <Select v-model="statusFilter" :options="statusOptions" @change="reload" class="min-w-40 text-sm" size="md" variant="outlined" placeholder="All Statuses" />
          <Select v-model="sourceFilter" :options="sourceOptions" @change="reload" class="min-w-40 text-sm" size="md" variant="outlined" placeholder="All Sources" />
          <Button variant="outline" theme="gray" @click="reload" :loading="loading" class="flex items-center py-4">
            <template #prefix>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" :class="{ 'animate-spin': loading }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </template>
            {{ __('Refresh') }}
          </Button>
        </div>
      </div>

      <div class="bg-white rounded-lg border border-gray-200">
        <Loading v-if="loading" text="Loading candidates..." />
        <div v-if="!loading" class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Full Name') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Email') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Phone') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Source') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Status') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Email Opt Out') }}</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Actions') }}</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="item in items" :key="item.name" class="hover:bg-gray-50">
                <td class="px-6 py-4">
                  <button class="text-left text-gray-900 hover:underline" @click="view(item)">{{ item.full_name }}</button>
                </td>
                <td class="px-6 py-4">{{ item.email || __('None') }}</td>
                <td class="px-6 py-4">{{ item.phone || __('None') }}</td>
                <td class="px-6 py-4">{{ item.source || __('None') }}</td>
                <td class="px-6 py-4">
                  <span :class="badgeClass(item.status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                    {{ item.status || __('None') }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span :class="emailOptOutClass(item.email_opt_out)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                    {{ item.email_opt_out ? __('Opted Out') : __('Active') }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <div class="flex items-center justify-end gap-3">
                    <button class="text-gray-500 hover:text-gray-700" @click="view(item)" title="{{ __('View') }}">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    </button>
                    <button class="text-blue-600 hover:text-blue-700" @click="openEditDialog(item)" title="{{ __('Edit') }}">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5h2m-7.586 9.586a2 2 0 010-2.828l7.586-7.586a2 2 0 012.828 0l2.172 2.172a2 2 0 010 2.828l-7.586 7.586a2 2 0 01-1.414.586H6v-2.172a2 2 0 01.586-1.414z" />
                      </svg>
                    </button>
                    <button class="text-red-600 hover:text-red-700" @click="remove(item)" title="{{ __('Delete') }}">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="items.length === 0">
                <td colspan="7" class="px-6 py-8 text-center text-gray-500">{{ __('No records') }}</td>
              </tr>
            </tbody>
          </table>

          <div v-if="pagination.pages > 1" class="flex items-center justify-between px-6 py-4 border-t border-gray-200">
            <div class="text-sm text-gray-500">
              {{ __('Display') }} {{ Math.min(((pagination.page - 1) * pagination.limit) + 1, pagination.total) }}-{{ Math.min(pagination.page * pagination.limit, pagination.total) }} {{ __('of') }} {{ pagination.total }} {{ __('records') }}
            </div>
            <div class="flex items-center space-x-2">
              <button class="px-3 py-1 rounded border text-sm" :class="pagination.page === 1 ? 'text-gray-400 border-gray-200 cursor-not-allowed' : 'text-gray-700 border-gray-300 hover:bg-gray-50'" :disabled="pagination.page === 1" @click="goToPage(pagination.page - 1)">
                {{ __('Prev') }}
              </button>
              <button v-for="p in pagination.pages" :key="p" class="px-3 py-1 rounded border text-sm" :class="p === pagination.page ? 'bg-black text-white border-black' : 'text-gray-700 border-gray-300 hover:bg-gray-50'" @click="goToPage(p)">{{ p }}</button>
              <button class="px-3 py-1 rounded border text-sm" :class="pagination.page === pagination.pages ? 'text-gray-400 border-gray-200 cursor-not-allowed' : 'text-gray-700 border-gray-300 hover:bg-gray-50'" :disabled="pagination.page === pagination.pages" @click="goToPage(pagination.page + 1)">
                {{ __('Next') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <Dialog v-model="showCreate" :options="{ title: isEditing ? __('Edit Candidate') : __('Create Candidate'), size: 'xl' }">
      <template #body-content>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ __('Full Name') }}</label>
            <input v-model="form.full_name" type="text" class="block w-full border border-gray-300 rounded-md px-3 py-2 text-sm" placeholder="Nguyễn Văn A" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ __('Email') }}</label>
            <input v-model="form.email" type="email" class="block w-full border border-gray-300 rounded-md px-3 py-2 text-sm" placeholder="email@example.com" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ __('Phone') }}</label>
            <input v-model="form.phone" type="text" class="block w-full border border-gray-300 rounded-md px-3 py-2 text-sm" placeholder="0912..." />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ __('Source') }}</label>
            <Select v-model="form.source" :options="sourceOptions.filter(o => o.value !== 'all')" placeholder="Select source" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ __('Status') }}</label>
            <Select v-model="form.status" :options="statusOptions.filter(o => o.value !== 'all')" placeholder="Select status" />
          </div>
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-2">{{ __('CV (PDF)') }}</label>
            <div class="mb-3">
              <Select v-model="cvMode" :options="cvModeOptions" class="min-w-48" size="md" variant="outlined" />
            </div>
            <div v-if="cvMode === 'upload'" class="space-y-2">
              <input ref="fileInput" type="file" accept="application/pdf" @change="handleFileChange" class="block w-full text-sm" />
              <div v-if="uploading" class="text-xs text-gray-500">{{ __('Uploading...') }}</div>
              <div v-if="form.cv_original_url" class="text-xs text-green-700 break-words">{{ __('Uploaded to:') }} {{ form.cv_original_url }}</div>
              <div v-if="uploadError" class="text-xs text-red-600">{{ uploadError }}</div>
            </div>
            <div v-else>
              <input v-model="form.cv_original_url" type="url" placeholder="https://example.com/cv.pdf" class="block w-full border border-gray-300 rounded-md px-3 py-2 text-sm" />
            </div>
          </div>
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Skills') }}</label>
            <div class="space-y-2">
              <div class="flex flex-wrap gap-2">
                <span v-for="(skill, index) in form.skills" :key="index" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {{ skill }}
                  <button type="button" @click="removeSkill(index)" class="ml-1.5 h-4 w-4 rounded-full inline-flex items-center justify-center text-blue-400 hover:bg-blue-200 hover:text-blue-500 focus:outline-none">
                    <svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
                      <path stroke-linecap="round" stroke-width="1.5" d="m1 1 6 6m0-6-6 6" />
                    </svg>
                  </button>
                </span>
              </div>
              <input v-model="newSkill" @input="handleSkillInput" @blur="finalizeSkillInput" type="text" :placeholder="__('Enter skills separated by commas (e.g. React, Vue, Pinia...)')" class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              <p class="text-xs text-gray-500">{{ __('Tip: You can enter multiple skills at once by separating them with commas') }}</p>
            </div>
          </div>
        </div>
      </template>
      <template #actions>
        <div class="flex items-center gap-2">
          <Button variant="subtle" @click="closeCreateDialog">{{ __('Cancel') }}</Button>
          <Button variant="solid" :loading="creating" @click="submitCreate">{{ isEditing ? __('Save') : __('Create') }}</Button>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Loading from '@/components/Loading.vue'
import { Breadcrumbs, Button, Select, Dialog, toast } from 'frappe-ui'
import { call } from 'frappe-ui'

const router = useRouter()
const breadcrumbs = [{ label: __('Candidates'), route: { name: 'CandidateManagementSimple' } }]

const loading = ref(false)
const items = ref([])
const pagination = ref({ page: 1, limit: 10, total: 0, pages: 0, has_next: false, has_prev: false })
const searchText = ref('')
const statusFilter = ref('all')
const sourceFilter = ref('all')

const statusOptions = [
  { label: __('All Statuses'), value: 'all' },
  { label: 'NEW', value: 'NEW' },
  { label: 'SOURCED', value: 'SOURCED' },
  { label: 'NURTURING', value: 'NURTURING' },
  { label: 'ENGAGED', value: 'ENGAGED' },
  { label: 'ARCHIVED', value: 'ARCHIVED' }
]

const sourceOptions = [
  { label: __('All Sources'), value: 'all' },
  { label: __('Manual'), value: 'Manual' },
  { label: __('LinkedIn'), value: 'LinkedIn' },
  { label: __('Email'), value: 'Email' },
  { label: __('Referral'), value: 'Referral' },
  { label: __('ATS Import'), value: 'ATS Import' },
  { label: __('Website'), value: 'Website' }
]

const fetchList = async () => {
  const filterArray = []
  if (statusFilter.value !== 'all') filterArray.push(['status', '=', statusFilter.value])
  if (sourceFilter.value !== 'all') filterArray.push(['source', '=', sourceFilter.value])
  if (searchText.value && searchText.value.trim()) filterArray.push(['full_name', 'like', `%${searchText.value.trim()}%`])

  const res = await call('frappe.client.get_list', {
    doctype: 'Mira Candidate',
    filters: filterArray.length ? filterArray : {},
    fields: ['name','full_name','email','phone','source','status','email_opt_out','creation'],
    order_by: 'modified desc',
    limit_start: (pagination.value.page - 1) * pagination.value.limit,
    limit_page_length: pagination.value.limit
  })
  const total = await call('frappe.client.get_count', {
    doctype: 'Mira Candidate',
    filters: filterArray.length ? filterArray : {}
  })
  items.value = res || []
  pagination.value.total = total || 0
  pagination.value.pages = Math.ceil((total || 0) / pagination.value.limit)
}

const reload = async () => {
  loading.value = true
  try { await fetchList() } finally { loading.value = false }
}

let searchTimer = null
const handleSearchInput = () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    pagination.value.page = 1
    reload()
  }, 300)
}

watch(searchText, () => handleSearchInput())

const view = (item) => router.push(`/candidates-simple/${item.name}`)

const badgeClass = (status) => ({
  'NEW': 'bg-gray-100 text-gray-800',
  'SOURCED': 'bg-blue-100 text-blue-800',
  'NURTURING': 'bg-yellow-100 text-yellow-800',
  'ENGAGED': 'bg-green-100 text-green-800',
  'ARCHIVED': 'bg-red-100 text-red-800'
}[status] || 'bg-gray-100 text-gray-800')

const emailOptOutClass = (emailOptOut) => {
  return emailOptOut 
    ? 'bg-red-100 text-red-800' 
    : 'bg-green-100 text-green-800'
}

const formatDate = (date) => date ? new Date(date).toLocaleDateString('vi-VN', { year: 'numeric', month: '2-digit', day: '2-digit' }) : ''

const goToPage = async (page) => {
  if (!pagination.value.pages) return
  if (page < 1 || page > pagination.value.pages) return
  if (page === pagination.value.page) return
  pagination.value.page = page
  await reload()
}

onMounted(async () => {
  await reload()
})

// Create/Edit dialog state
const showCreate = ref(false)
const creating = ref(false)
const isEditing = ref(false)
const editingName = ref('')
const cvMode = ref('upload')
const cvModeOptions = [
  { label: __('Upload PDF'), value: 'upload' },
  { label: __('Paste PDF URL'), value: 'link' }
]
const fileInput = ref(null)
const uploading = ref(false)
const uploadError = ref('')
const newSkill = ref('')

const form = reactive({
  full_name: '',
  email: '',
  phone: '',
  source: 'Manual',
  status: 'NEW',
  cv_original_url: '',
  skills: []
})

function openCreateDialog() {
  resetForm()
  isEditing.value = false
  showCreate.value = true
}

function openEditDialog(item) {
  resetForm()
  isEditing.value = true
  editingName.value = item.name
  // load full doc to populate
  call('frappe.client.get', {
    doctype: 'Mira Candidate',
    name: item.name
  }).then((doc) => {
    form.full_name = doc.full_name || ''
    form.email = doc.email || ''
    form.phone = doc.phone || ''
    form.source = doc.source || 'Manual'
    form.status = doc.status || 'NEW'
    form.cv_original_url = doc.cv_original_url || ''
    try {
      form.skills = doc.skills ? JSON.parse(doc.skills) : []
      if (!Array.isArray(form.skills)) form.skills = []
    } catch (e) {
      form.skills = []
    }
    cvMode.value = form.cv_original_url ? 'link' : 'upload'
    showCreate.value = true
  })
}

function closeCreateDialog() {
  showCreate.value = false
}

function resetForm() {
  form.full_name = ''
  form.email = ''
  form.phone = ''
  form.source = 'Manual'
  form.status = 'NEW'
  form.cv_original_url = ''
  form.skills = []
  cvMode.value = 'upload'
  uploadError.value = ''
  uploading.value = false
  newSkill.value = ''
  if (fileInput.value) fileInput.value.value = ''
}

function removeSkill(index) {
  form.skills.splice(index, 1)
  const remaining = form.skills.slice()
  const hadTrailingComma = /,\s*$/.test(newSkill.value || '')
  newSkill.value = remaining.join(', ') + (hadTrailingComma && remaining.length ? ', ' : '')
}

function addSkill() {
  if (!newSkill.value) return
  const parts = newSkill.value.split(',').map(s => s.trim()).filter(Boolean)
  if (!parts.length) return
  const unique = Array.from(new Set(parts))
  form.skills = unique
}

function handleSkillInput(e) {
  const value = e.target.value || ''
  const tokens = value.split(',').map(s => s.trim()).filter(Boolean)
  const unique = Array.from(new Set(tokens))
  form.skills = unique
}

function finalizeSkillInput() {
  const value = newSkill.value || ''
  const tokens = value.split(',').map(s => s.trim()).filter(Boolean)
  const unique = Array.from(new Set(tokens))
  form.skills = unique
  // keep the normalized text in the input
  newSkill.value = unique.join(', ')
}

function handleFileChange(e) {
  uploadError.value = ''
  const file = e.target.files && e.target.files[0]
  if (!file) return
  if (file.type !== 'application/pdf') {
    uploadError.value = __('Please select a PDF file')
    return
  }
  uploadPDF(file)
}

async function uploadPDF(file) {
  try {
    uploading.value = true
    const xhr = new XMLHttpRequest()
    const promise = new Promise((resolve, reject) => {
      xhr.onreadystatechange = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
            let r = null
            try { r = JSON.parse(xhr.responseText) } catch (e) { r = xhr.responseText }
            const msg = r.message || r
            form.cv_original_url = msg.file_url || ''
            resolve(msg)
          } else {
            let err = null
            try { err = JSON.parse(xhr.responseText) } catch (e) { err = xhr.responseText }
            reject(err)
          }
        }
      }
      xhr.onerror = () => reject(__('Network error'))
    })
    xhr.open('POST', '/api/method/upload_file', true)
    xhr.setRequestHeader('Accept', 'application/json')
    if (window.csrf_token && window.csrf_token !== '{{ csrf_token }}') {
      xhr.setRequestHeader('X-Frappe-CSRF-Token', window.csrf_token)
    }
    const formData = new FormData()
    formData.append('file', file, file.name)
    formData.append('is_private', '1')
    formData.append('folder', 'Home/Attachments')
    xhr.send(formData)
    await promise
  } catch (err) {
    console.error('upload_file error:', err)
    uploadError.value = __('Upload failed')
  } finally {
    uploading.value = false
  }
}

async function submitCreate() {
  if (!form.full_name || !form.full_name.trim()) {
    toast.error(__('Full Name is required'))
    return
  }
  if (cvMode.value === 'upload' && uploading.value) {
    toast.error(__('Please wait until upload finishes'))
    return
  }
  creating.value = true
  try {
    const skillsValue = form.skills && form.skills.length ? JSON.stringify(form.skills) : null
    if (isEditing.value) {
      const doc = {
        doctype: 'Mira Candidate',
        name: editingName.value,
        full_name: form.full_name?.trim(),
        email: form.email?.trim() || null,
        phone: form.phone?.trim() || null,
        source: form.source || null,
        status: form.status || 'NEW',
        cv_original_url: form.cv_original_url?.trim() || null,
        skills: skillsValue
      }
      await call('frappe.client.save', { doc, ignore_version: 1 })
      toast.success(__('Saved'))
    } else {
      const doc = {
        doctype: 'Mira Candidate',
        full_name: form.full_name?.trim(),
        email: form.email?.trim() || null,
        phone: form.phone?.trim() || null,
        source: form.source || null,
        status: form.status || 'NEW',
        cv_original_url: form.cv_original_url?.trim() || null,
        skills: skillsValue
      }
      await call('frappe.client.insert', { doc })
      toast.success(__('Created'))
    }
    showCreate.value = false
    await reload()
  } catch (e) {
    console.error(e)
    toast.error(__('Failed to save'))
  } finally {
    creating.value = false
  }
}

async function remove(item) {
  if (!confirm(__('Delete this candidate?'))) return
  try {
    await call('frappe.client.delete', { doctype: 'Mira Candidate', name: item.name })
    toast.success(__('Deleted'))
    await reload()
  } catch (e) {
    console.error(e)
    toast.error(__('Failed to delete'))
  }
}
</script> 