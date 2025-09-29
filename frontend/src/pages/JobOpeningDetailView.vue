<template>
  <div class="min-h-screen bg-gray-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header>
        <div class="flex space-x-3">
          <Button variant="solid" theme="blue" @click="edit">
            <template #prefix>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </template>
            {{ __('Chỉnh sửa') }}
          </Button>
        </div>
      </template>
    </LayoutHeader>

    <div class="container mx-auto px-6 py-6">
      <!-- Basic Information Card -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">{{ __('Thông tin cơ bản') }}</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="info-item">
            <label class="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
              {{ __('Job Code') }}
            </label>
            <p class="text-sm font-medium text-gray-900">{{ data.job_code || '-' }}</p>
          </div>
          
          <div class="info-item">
            <label class="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
              {{ __('Posting Date') }}
            </label>
            <p class="text-sm font-medium text-gray-900">{{ formatDate(data.posting_date) || '-' }}</p>
          </div>
          
          <div class="info-item">
            <label class="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
              {{ __('Phòng ban') }}
            </label>
            <p class="text-sm font-medium text-gray-900">{{ data.department_name || '-' }}</p>
          </div>
          
          <div class="info-item">
            <label class="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
              {{ __('Closing Date') }}
            </label>
            <p class="text-sm font-medium text-gray-900">{{ formatDate(data.closing_date) || '-' }}</p>
          </div>
          
          <div class="info-item">
            <label class="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
              {{ __('Vị trí') }}
            </label>
            <p class="text-sm font-medium text-gray-900">{{ data.location_name || '-' }}</p>
          </div>
          
          <div class="info-item">
            <label class="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
              {{ __('Chủ sở hữu') }}
            </label>
            <p class="text-sm font-medium text-gray-900">{{ data.owner_id || '-' }}</p>
          </div>
          
          <div class="info-item">
            <label class="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
              {{ __('Trạng thái') }}
            </label>
            <div class="mt-1">
              <span :class="badgeClass(data.approval_status || 'Draft')" 
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                {{ data.approval_status || 'Draft' }}
              </span>
            </div>
          </div>
          
          <div class="info-item">
            <label class="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
              {{ __('Total Applicants') }}
            </label>
            <p class="text-sm font-medium text-gray-900">{{ data.total_applicants || 0 }}</p>
          </div>
        </div>
      </div>

      <!-- Job Description Card -->
      <div v-if="data.description" class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">{{ __('Mô tả công việc') }}</h2>
        <div class="prose max-w-none text-gray-700">
          <div v-html="formatDescription(data.description)"></div>
        </div>
      </div>

      <!-- Requirements Card -->
      <div v-if="data.requirements" class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">{{ __('Yêu cầu') }}</h2>
        <div v-html="formatRequirements(data.requirements)" class="prose max-w-none text-gray-700"></div>
      </div>

      <!-- Benefits Card -->
      <div v-if="data.benefits" class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">{{ __('Quyền lợi') }}</h2>
        <div v-html="formatBenefits(data.benefits)" class="prose max-w-none text-gray-700"></div>
      </div>
    </div>

    <!-- Edit Form Modal -->
    <div v-if="showEditForm" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen p-4 text-center">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>

        <div class="relative w-full max-w-4xl mx-auto bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all">
          <div class="bg-white px-6 py-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-medium text-gray-900">
                {{ __('Chỉnh sửa Job Opening') }}
              </h3>
              <button
                @click="closeEditForm"
                class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition-colors"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          <div class="px-6 py-4 max-h-[70vh] overflow-y-auto">
            <div class="space-y-4">
              <FormControl 
                v-model="editForm.job_title" 
                type="text" 
                :label="__('Job Title')" 
                :required="true" 
              />
              
              <div class="grid grid-cols-2 gap-4">
                <FormControl 
                  v-model="editForm.job_code" 
                  type="text" 
                  :label="__('Job Code')" 
                />
                <FormControl 
                  v-model="editForm.department_name" 
                  type="text" 
                  :label="__('Department')" 
                />
              </div>

              <div class="grid grid-cols-2 gap-4">
                <FormControl 
                  v-model="editForm.posting_date" 
                  type="date" 
                  :label="__('Posting Date')" 
                />
                <FormControl 
                  v-model="editForm.closing_date" 
                  type="date" 
                  :label="__('Closing Date')" 
                />
              </div>

              <FormControl 
                v-model="editForm.approval_status" 
                type="select" 
                :label="__('Status')" 
                :options="statusOptions" 
              />

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Job Description') }}
                </label>
                <TextEditor
                  ref="descriptionEditor"
                  variant="outline"
                  editor-class="min-h-[120px] max-h-[200px] overflow-auto"
                  :bubbleMenu="true"
                  :fixedMenu="true"
                  :content="editForm.description"
                  :placeholder="__('Provide detailed job description...')"
                  @change="editForm.description = $event"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Requirements') }}
                </label>
                <TextEditor
                  ref="requirementsEditor"
                  variant="outline"
                  editor-class="min-h-[120px] max-h-[200px] overflow-auto"
                  :bubbleMenu="true"
                  :fixedMenu="true"
                  :content="editForm.requirements"
                  :placeholder="__('Specify job requirements...')"
                  @change="editForm.requirements = $event"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Benefits') }}
                </label>
                <TextEditor
                  ref="benefitsEditor"
                  variant="outline"
                  editor-class="min-h-[120px] max-h-[200px] overflow-auto"
                  :bubbleMenu="true"
                  :fixedMenu="true"
                  :content="editForm.benefits"
                  :placeholder="__('Highlight job benefits...')"
                  @change="editForm.benefits = $event"
                />
              </div>
            </div>
          </div>

          <div class="bg-gray-50 px-6 py-4 flex justify-end space-x-3">
            <Button variant="outline" theme="gray" @click="closeEditForm">
              {{ __('Cancel') }}
            </Button>
            <Button 
              variant="solid" 
              theme="blue" 
              :loading="saving" 
              @click="saveChanges"
            >
              {{ __('Save Changes') }}
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Breadcrumbs, Button, FormControl, TextEditor } from 'frappe-ui'
import { getJobOpeningDetails, updateJobOpeningData } from '@/services/jobOpeningService'

const route = useRoute()
const data = reactive({})

const showEditForm = ref(false)
const saving = ref(false)
const editForm = reactive({})

const breadcrumbs = computed(() => [
  { label: __('Job Openings'), route: { name: 'JobOpeningManagement' } },
  { label: data.job_title || __('Job Detail'), route: { name: 'JobOpeningDetailView' } }
])

const statusOptions = [
  { label: 'Draft', value: 'Draft' },
  { label: 'Pending Approval', value: 'Pending Approval' },
  { label: 'Approved', value: 'Approved' },
  { label: 'Rejected', value: 'Rejected' }
]

// Hàm stripHtml từ file CampaignWizard.vue
const stripHtml = (html) => {
  if (!html || typeof html !== 'string') return ''
  return html.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim()
}

// Format Job Description - tách paragraph và bullet points với dấu -
const formatDescription = (text) => {
  if (!text) return ''
  
  const cleanText = stripHtml(text)
  
  // Tìm phần đầu tiên (paragraph đầu) và phần bullet points
  const lines = cleanText.split('\n').filter(line => line.trim())
  
  if (lines.length === 0) return `<p>${cleanText}</p>`
  
  const result = []
  let inBulletSection = false
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim()
    
    // Kiểm tra nếu bắt đầu bullet points (có dấu -, •, *, hoặc số)
    if (line.match(/^[-•*\d+\.]/) || line.match(/^-/) || i > 2) {
      if (!inBulletSection) {
        inBulletSection = true
      }
      // Loại bỏ ký tự bullet cũ và thêm lại với format chuẩn
      const cleanLine = line.replace(/^[-•*\s*\d+\.\s*]+/, '').trim()
      if (cleanLine) {
        result.push(`<p>- ${cleanLine}</p>`)
      }
    } else {
      // Paragraph thường
      if (line) {
        result.push(`<p class="leading-relaxed">${line}</p>`)
      }
    }
  }
  
  // Nếu không có bullet points, trả về paragraph đơn
  if (!inBulletSection) {
    return `<p class="leading-relaxed">${cleanText}</p>`
  }
  
  // Chia thành paragraph đầu và bullet section
  const paragraphs = result.filter(item => !item.includes('- '))
  const bullets = result.filter(item => item.includes('- '))
  
  return paragraphs.join('') + 
         (bullets.length > 0 ? `<div class="space-y-2 mt-4">${bullets.join('')}</div>` : '')
}

// Format Requirements - bullet points với dấu •
const formatRequirements = (text) => {
  if (!text) return ''
  
  const cleanText = stripHtml(text)
  
  // Tách thành các mục dựa trên xuống dòng và các dấu phân cách
  const lines = cleanText.split(/[\n\r]+/).filter(line => line.trim())
  
  if (lines.length === 0) return `<p>${cleanText}</p>`
  
  const result = []
  
  for (const line of lines) {
    const trimmedLine = line.trim()
    if (trimmedLine) {
      // Loại bỏ các ký tự bullet cũ và thêm lại với format chuẩn •
      const cleanLine = trimmedLine.replace(/^[-•*\s*\d+\.\s*]+/, '').trim()
      if (cleanLine) {
        result.push(`<li>• ${cleanLine}</li>`)
      }
    }
  }
  
  return result.length > 0 ? `<ul class="list-none space-y-3 text-gray-700">${result.join('')}</ul>` : `<p>${cleanText}</p>`
}

// Format Benefits - đơn giản hóa
const formatBenefits = (text) => {
  if (!text) return ''
  
  const cleanText = stripHtml(text)
  
  // Nếu có nhiều dòng, format như requirements
  if (cleanText.includes('\n')) {
    return formatRequirements(text)
  }
  
  // Hiển thị đơn giản
  return `<p class="leading-relaxed">${cleanText}</p>`
}

const load = async () => {
  try {
    if (route.params.id) {
      const res = await getJobOpeningDetails(route.params.id)
      Object.assign(data, res)
      console.log('Loaded job data:', data) // Debug log
    }
  } catch (error) {
    console.error('Error loading job details:', error)
  }
}

const edit = () => {
  Object.assign(editForm, data)
  showEditForm.value = true
}

const closeEditForm = () => {
  showEditForm.value = false
}

const saveChanges = async () => {
  saving.value = true
  try {
    if (route.params.id) {
      await updateJobOpeningData(route.params.id, editForm)
      Object.assign(data, editForm)
      showEditForm.value = false
    }
  } catch (error) {
    console.error('Error saving changes:', error)
  } finally {
    saving.value = false
  }
}

const badgeClass = (status) => ({
  'Draft': 'bg-yellow-100 text-yellow-800 border border-yellow-200',
  'Pending Approval': 'bg-orange-100 text-orange-800 border border-orange-200',
  'Approved': 'bg-green-100 text-green-800 border border-green-200',
  'Rejected': 'bg-red-100 text-red-800 border border-red-200'
}[status] || 'bg-gray-100 text-gray-800 border border-gray-200')

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('vi-VN', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit' 
  })
}

onMounted(async () => {
  await load()
})
</script>

<style scoped>
.info-item {
  min-height: 60px;
}

.prose {
  line-height: 1.7;
}

.prose p {
  margin-bottom: 1rem;
}

.prose h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 1.25rem 0 0.75rem 0;
}

.prose ul {
  list-style: none;
  padding: 0;
}

.prose li {
  margin-bottom: 0.75rem;
  padding-left: 0;
}
</style>