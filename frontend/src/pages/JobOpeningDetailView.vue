<template>
  <div class="min-h-screen bg-gray-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header>
        <div class="flex space-x-3">
          <Button variant="solid" theme="gray" @click="edit">
            <template #prefix>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </template>
            {{ __('Edit') }}
          </Button>
        </div>
        <div class="flex space-x-3">
          <Button variant="solid" theme="blue" @click="share">
            <template #prefix>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
                class="feather feather-share-2 shrink-0 h-4 w-4">
                <circle cx="18" cy="5" r="3"></circle>
                <circle cx="6" cy="12" r="3"></circle>
                <circle cx="18" cy="19" r="3"></circle>
                <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
                <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
              </svg>
            </template>
            {{ __('Share') }}
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

          <!-- <div class="info-item">
            <label class="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
              {{ __('Phòng ban') }}
            </label>
            <p class="text-sm font-medium text-gray-900">{{ data.department_name || '-' }}</p>
          </div> -->

          <div class="info-item">
            <label class="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
              {{ __('Closing Date') }}
            </label>
            <p class="text-sm font-medium text-gray-900">{{ formatDate(data.closing_date) || '-' }}</p>
          </div>

          <!-- <div class="info-item">
            <label class="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
              {{ __('Vị trí') }}
            </label>
            <p class="text-sm font-medium text-gray-900">{{ data.location_name || '-' }}</p>
          </div> -->

          <!-- <div class="info-item">
            <label class="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
              {{ __('Chủ sở hữu') }}
            </label>
            <p class="text-sm font-medium text-gray-900">{{ data.owner_id || '-' }}</p>
          </div> -->

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

    <!-- Edit Form Dialog -->
    <Dialog v-model="showEditForm" :options="{
      title: __('Edit Job Opening'),
      size: '3xl',
    }" :disableOutsideClickToClose="true">

      <template #body-title>
        <div>
          <h4 class="text-lg font-medium text-gray-900">{{ __('Basic Information') }}</h4>
          <p class="text-sm text-gray-500">{{ __('Job title, position, and department') }}</p>
        </div>
      </template>

      <template #body-content>
        <div class="overflow-y-auto">
          <!-- Basic Information Section -->
          <div class="mb-8">
            <div class="space-y-4">
              <FormControl v-model="editForm.job_title" type="text" :label="__('Job Title')" :required="true" />

              <div class="grid grid-cols-2 gap-4">
                <FormControl v-model="editForm.department_name" type="text" :label="__('Department')" />
                <FormControl v-model="editForm.location_name" type="text" :label="__('Location')" />
              </div>

              <FormControl v-model="editForm.number_of_openings" type="number" :label="__('Number Of Openings')" />

              <div class="grid grid-cols-2 gap-4">
                <FormControl v-model="editForm.posting_date" type="date" :label="__('Posting Date')" />
                <FormControl v-model="editForm.closing_date" type="date" :label="__('Closing Date')" />
              </div>

              <div class="grid grid-cols-2 gap-4">
                <FormControl v-model="editForm.approval_status" type="select" :label="__('Status')"
                  :options="statusOptions" />
                <FormControl v-model="editForm.owner_id" type="select" :label="__('Owner')" :options="ownerOptions" />
              </div>
            </div>
          </div>

          <!-- Job Description Section -->
          <div>
            <div class="flex items-center justify-between mb-6">
              <div>
                <h4 class="text-lg font-medium text-gray-900">{{ __('Job Description') }}</h4>
                <p class="text-sm text-gray-500">{{ __('Description, requirements, and responsibilities') }}</p>
              </div>
              <Button variant="outline" size="sm" theme="blue" @click="openAIModal">
                <template #prefix>
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </template>
                {{ __('AI Generation') }}
              </Button>
            </div>

            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Job Description') }}</label>
                <TextEditor ref="descriptionEditor" variant="outline"
                  editor-class="!prose-sm !max-w-full overflow-auto !w-full min-h-[120px] max-h-[150px] py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 hover:shadow-sm focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400 text-gray-800 transition-colors"
                  :bubbleMenu="true" :fixedMenu="true" :content="editForm.description"
                  :placeholder="__('Provide a detailed description of the job responsibilities and day-to-day tasks')"
                  @change="editForm.description = $event" />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Job Requirements') }}</label>
                <TextEditor ref="requirementsEditor" variant="outline"
                  editor-class="!prose-sm !max-w-full overflow-auto !w-full min-h-[120px] max-h-[150px] py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 hover:shadow-sm focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400 text-gray-800 transition-colors"
                  :bubbleMenu="true" :fixedMenu="true" :content="editForm.requirements"
                  :placeholder="__('Specify required qualifications, skills, experience, and education')"
                  @change="editForm.requirements = $event" />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Benefits') }}</label>
                <TextEditor ref="benefitsEditor" variant="outline"
                  editor-class="!prose-sm !max-w-full overflow-auto !w-full min-h-[120px] max-h-[150px] py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 hover:shadow-sm focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400 text-gray-800 transition-colors"
                  :bubbleMenu="true" :fixedMenu="true" :content="editForm.benefits"
                  :placeholder="__('Highlight the benefits and what makes this role attractive')"
                  @change="editForm.benefits = $event" />
              </div>
            </div>
          </div>
        </div>
      </template>

      <template #actions>
        <!-- Action Buttons -->
        <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
          <Button variant="outline" theme="gray" @click="closeEditForm" :disabled="saving">
            {{ __('Cancel') }}
          </Button>
          <Button variant="solid" theme="gray" :loading="saving" @click="saveChanges">
            {{ __('Update') }}
          </Button>
        </div>
      </template>
    </Dialog>

    <!-- AI Generation Dialog -->
    <Dialog v-model="showAIModal" :options="{
      title: __('Generate Job Description AI'),
      size: '6xl',
      disableOutsideClickToClose: true
    }">
      <template #body-content>
        <div class="max-h-[80vh] overflow-y-auto">
          <div class="p-6">
            <div class="grid grid-cols-2 gap-6">
              <!-- Left Panel - Input Configuration -->
              <div class="space-y-6">
                <div>
                  <FormControl v-model="aiForm.job_title" type="text" :label="__('Job Title')"
                    :placeholder="__('Enter job title')" @input="updateMainFormJobTitle" />
                </div>

                <div>
                  <FormControl type="select" v-model="aiForm.tone" :options="[
                    { label: __('Professional'), value: 'Professional' },
                    { label: __('Friendly'), value: 'Friendly' },
                    { label: __('Creative'), value: 'Creative' },
                    { label: __('Formal'), value: 'Formal' },
                    { label: __('Casual'), value: 'Casual' }
                  ]" variant="outline" :placeholder="__('Select Tone')" :label="__('Tone')" />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __('Additional Instructions') }}
                  </label>
                  <textarea v-model="aiForm.comments" rows="4"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    :placeholder="__('Write your comments here. Example: I want to create a job description for a software engineer with 3 years of experience in React and Node.js.')"></textarea>
                </div>

                <div class="pt-4">
                  <Button variant="solid" theme="gray" @click="generateAIContent" :loading="aiGenerating"
                    class="w-full">
                    {{ __('Generate') }}
                  </Button>
                </div>

                <div v-if="aiHistory.length > 1" class="flex items-center justify-between text-sm text-gray-500">
                  <Button variant="ghost" :disabled="currentAiVersion === 0" @click="previousAIVersion"
                    class="flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24"
                      stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                    {{ __('Previous') }}
                  </Button>

                  <span class="text-sm">
                    {{ currentAiVersion + 1 }} / {{ aiHistory.length }}
                  </span>

                  <Button variant="ghost" :disabled="currentAiVersion === aiHistory.length - 1" @click="nextAIVersion"
                    class="flex items-center">
                    {{ __('Next') }}
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24"
                      stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </Button>
                </div>
              </div>

              <!-- Right Panel - Rich Text Editors -->
              <div class="space-y-6">
                <!-- Job Description -->
                <div>
                  <div class="flex items-center justify-between mb-2">
                    <label class="block text-sm font-medium text-gray-700">{{ __('Job Description') }}</label>
                    <Button v-if="aiForm.job_description" variant="outline" size="sm" theme="blue"
                      @click="rewriteWithAI('job_description')" :loading="rewritingSection === 'job_description'">
                      <template #prefix>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                          stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                      </template>
                      {{ __('Rewrite') }}
                    </Button>
                  </div>
                  <div class="prose max-w-none border rounded-md p-3 min-h-[150px] max-h-[200px] overflow-y-auto"
                    v-html="aiForm.job_description || '<p class=\'text-gray-400\'>Generated job description will appear here...</p>'">
                  </div>
                </div>

                <!-- Job Requirements -->
                <div>
                  <div class="flex items-center justify-between mb-2">
                    <label class="block text-sm font-medium text-gray-700">{{ __('Job Requirements') }}</label>
                    <Button v-if="aiForm.job_requirement" variant="outline" size="sm" theme="blue"
                      @click="rewriteWithAI('job_requirement')" :loading="rewritingSection === 'job_requirement'">
                      <template #prefix>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                          stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                      </template>
                      {{ __('Rewrite') }}
                    </Button>
                  </div>
                  <div class="prose max-w-none border rounded-md p-3 min-h-[150px] max-h-[200px] overflow-y-auto"
                    v-html="aiForm.job_requirement || '<p class=\'text-gray-400\'>Generated requirements will appear here...</p>'">
                  </div>
                </div>

                <!-- Benefits -->
                <div>
                  <div class="flex items-center justify-between mb-2">
                    <label class="block text-sm font-medium text-gray-700">{{ __('Benefits') }}</label>
                    <Button v-if="aiForm.job_benefits" variant="outline" size="sm" theme="blue"
                      @click="rewriteWithAI('job_benefits')" :loading="rewritingSection === 'job_benefits'">
                      <template #prefix>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                          stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                      </template>
                      {{ __('Rewrite') }}
                    </Button>
                  </div>
                  <div class="prose max-w-none border rounded-md p-3 min-h-[150px] max-h-[200px] overflow-y-auto"
                    v-html="aiForm.job_benefits || '<p class=\'text-gray-400\'>Generated benefits will appear here...</p>'">
                  </div>
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex justify-between items-center pt-6 border-t border-gray-200 mt-6">
              <div v-if="contentApplied" class="text-sm text-green-600 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                {{ __('Content applied successfully!') }}
              </div>
              <div v-else></div>

              <div class="flex space-x-3">
                <Button variant="outline" theme="gray" @click="closeAIModal">
                  {{ __('Cancel') }}
                </Button>
                <Button variant="solid" theme="gray"
                  :disabled="!aiForm.job_description && !aiForm.job_requirement && !aiForm.job_benefits"
                  @click="useGeneratedContent">
                  {{ __('Use This Content') }}
                </Button>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Dialog>

    <!-- Share Dialog -->
    <ShareDialog 
      v-model="showShareDialog" 
      :jobData="data" 
      :jobId="data.name"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import ShareDialog from '@/components/ShareDialog.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Breadcrumbs, Button, FormControl, TextEditor, Dialog, call } from 'frappe-ui'
import { getJobOpeningDetails, updateJobOpeningData } from '@/services/jobOpeningService'
import { useToast } from '@/composables/useToast'

const toast = useToast()

const route = useRoute()
const data = reactive({})

// Form state
const showEditForm = ref(false)
const saving = ref(false)
const editForm = reactive({
  job_title: '',
  job_code: '',
  department_name: '',
  location_name: '',
  number_of_openings: 1,
  posting_date: '',
  closing_date: '',
  approval_status: 'Draft',
  owner_id: '',
  description: '',
  requirements: '',
  benefits: ''
})

// AI Generation state
const showAIModal = ref(false)
const showShareDialog = ref(false)
const aiGenerating = ref(false)
const rewritingSection = ref(null)
const contentApplied = ref(false)
const showPreview = ref(true)
const ownerOptions = ref([])

const aiForm = reactive({
  job_title: '',
  job_description: '',
  job_requirement: '',
  job_benefits: '',
  tone: 'Professional',
  comments: ''
})

const aiHistory = ref([])
let currentAiVersion = 0

const breadcrumbs = computed(() => [
  { label: __('Job Openings'), route: { name: 'JobOpeningManagement' } },
  { label: data.job_title || __('Job Detail'), route: { name: 'JobOpeningDetailView' } }
])

const statusOptions = [
  { label: 'Draft', value: 'Draft' },
  { label: 'Pending Approval', value: 'Pending Approval' },
  { label: 'Approved', value: 'Approved' },
  { label: 'Rejected', value: 'Rejected' },
  { label: 'Closed', value: 'Closed' },
  { label: 'Cancelled', value: 'Cancelled' }
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

const edit = async () => {
  try {
    // Reset form first
    Object.assign(editForm, data)

    // Set AI form title and content
    aiForm.job_title = data.job_title || ''
    aiForm.job_description = data.description || ''
    aiForm.job_requirement = data.requirements || ''
    aiForm.job_benefits = data.benefits || ''

    // Load owners if needed
    if (ownerOptions.value.length === 0) {
      await loadOwners()
    }

    // Set default owner to current user if not set
    if (!editForm.owner_id) {
      try {
        const currentUser = await call('frappe.session.get_user')
        if (currentUser && currentUser.name) {
          editForm.owner_id = currentUser.name
        } else {
          console.warn('Could not get current user, owner will not be set automatically')
        }
      } catch (error) {
        console.warn('Error getting current user:', error.message)
        // Continue without setting owner if we can't get the current user
      }
    }

    showEditForm.value = true

    // Set focus to first field when dialog opens
    await nextTick()
    document.querySelector('input')?.focus()
  } catch (error) {
    console.error('Error preparing edit form:', error)
    toast.error('Failed to prepare edit form')
  }
}

const closeEditForm = () => {
  showEditForm.value = false
  // Don't reset the form completely, just close it
  // The form will be reloaded when opened again
}

const saveChanges = async () => {
  saving.value = true
  try {
    if (!route.params.id) {
      throw new Error('No job opening ID found')
    }

    // Validate required fields
    const requiredFields = ['job_title', 'posting_date', 'closing_date']
    const missingFields = requiredFields.filter(field => !editForm[field]?.trim())

    if (missingFields.length > 0) {
      throw new Error(`Please fill in all required fields: ${missingFields.join(', ')}`)
    }

    // Prepare the data to send
    const dataToSave = {
      ...editForm,
      // Ensure these fields are included even if empty
      description: editForm.description || '',
      requirements: editForm.requirements || '',
      benefits: editForm.benefits || ''
    }

    // Remove any empty fields except the ones we want to keep
    Object.keys(dataToSave).forEach(key => {
      if (dataToSave[key] === '' || dataToSave[key] == null) {
        delete dataToSave[key]
      }
    })

    // Save the data
    const result = await updateJobOpeningData(route.params.id, dataToSave)

    if (result) {
      // Update local data
      Object.assign(data, { ...data, ...dataToSave })
      showEditForm.value = false

      // Reload the data to ensure consistency
      await load()

      // Show success message
      toast.success(__('Job opening updated successfully'))
    }
  } catch (error) {
    console.error('Error saving job opening:', error)
    toast.error(__('Failed to update job opening: ') + (error.message || 'Unknown error'))
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

// Load owners for dropdown
const loadOwners = async () => {
  try {
    const result = await call('frappe.client.get_list', {
      doctype: 'User',
      fields: ['name', 'full_name'],
      filters: {
        enabled: 1,
        user_type: 'System User'
      },
      limit: 100
    })

    // Sort by full name
    result.sort((a, b) => {
      const nameA = (a.full_name || a.name).toLowerCase()
      const nameB = (b.full_name || b.name).toLowerCase()
      return nameA.localeCompare(nameB)
    })

    ownerOptions.value = result.map(user => ({
      label: user.full_name ? `${user.full_name} (${user.name})` : user.name,
      value: user.name
    }))

    return ownerOptions.value
  } catch (error) {
    console.error('Error loading owners:', error)
    toast.error('Failed to load user list')
    return []
  }
}

// AI Generation Functions
const updateMainFormJobTitle = () => {
  if (aiForm.job_title && aiForm.job_title !== editForm.job_title) {
    editForm.job_title = aiForm.job_title
  }
}

const openAIModal = () => {
  // Save current content to history
  aiForm.job_title = editForm.job_title || ''
  aiForm.job_description = editForm.description || ''
  aiForm.job_requirement = editForm.requirements || ''
  aiForm.job_benefits = editForm.benefits || ''

  // Reset AI history
  aiHistory.value = [{
    description: aiForm.job_description,
    requirement: aiForm.job_requirement,
    benefits: aiForm.job_benefits
  }]
  currentAiVersion = 0
  contentApplied.value = false

  showAIModal.value = true
}

const closeAIModal = () => {
  showAIModal.value = false
}

const generateAIContent = async () => {
  if (!aiForm.job_title) {
    toast.error('Please enter a job title')
    return
  }

  aiGenerating.value = true

  try {
    // Call your AI generation API here
    // This is a placeholder - replace with your actual API call
    const prompt = `Generate a professional job description for ${aiForm.job_title}. \n\n` +
      `Tone: ${aiForm.tone}\n` +
      `Additional comments: ${aiForm.comments || 'None'}`

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))

    // This is just sample data - replace with actual API response
    aiForm.job_description = `## Job Description\n\n` +
      `We are looking for a skilled ${aiForm.job_title} to join our team. The ideal candidate will have a strong background in the field and a passion for excellence.\n\n` +
      `### Responsibilities\n` +
      `- Sample responsibility 1\n` +
      `- Sample responsibility 2\n` +
      `- Sample responsibility 3`

    aiForm.job_requirement = `### Requirements\n` +
      `- Sample requirement 1\n` +
      `- Sample requirement 2\n` +
      `- Sample requirement 3`

    aiForm.job_benefits = `### Benefits\n` +
      `- Competitive salary\n` +
      `- Flexible working hours\n` +
      `- Health insurance`

    // Add to history
    aiHistory.value.push({
      description: aiForm.job_description,
      requirement: aiForm.job_requirement,
      benefits: aiForm.job_benefits
    })
    currentAiVersion = aiHistory.value.length - 1

    toast.success('AI content generated successfully')
  } catch (error) {
    console.error('Error generating AI content:', error)
    toast.error('Failed to generate content. Please try again.')
  } finally {
    aiGenerating.value = false
  }
}

const rewriteWithAI = async (section) => {
  if (!aiForm.job_title) {
    toast.error('Please enter a job title first')
    return
  }

  rewritingSection.value = section

  try {
    // Call your AI API to rewrite the specific section
    // This is a placeholder - replace with actual API call
    await new Promise(resolve => setTimeout(resolve, 1000))

    // Sample rewritten content
    const sampleContent = {
      job_description: '## Job Description\n\nRewritten job description with AI...',
      job_requirement: '### Requirements\n\nRewritten requirements with AI...',
      job_benefits: '### Benefits\n\nRewritten benefits with AI...'
    }

    aiForm[section] = sampleContent[section] || aiForm[section]

    // Update history
    const currentState = {
      description: aiForm.job_description,
      requirement: aiForm.job_requirement,
      benefits: aiForm.job_benefits
    }

    // Only add to history if different from last state
    const lastState = aiHistory.value[aiHistory.value.length - 1]
    if (JSON.stringify(currentState) !== JSON.stringify(lastState)) {
      aiHistory.value.push(currentState)
      currentAiVersion = aiHistory.value.length - 1
    }

    toast.success('Section rewritten successfully')
  } catch (error) {
    console.error('Error rewriting section:', error)
    toast.error('Failed to rewrite section. Please try again.')
  } finally {
    rewritingSection.value = null
  }
}

const share = () => {
  showShareDialog.value = true
}

const useGeneratedContent = () => {
  // Update the form with AI generated content
  editForm.description = aiForm.job_description
  editForm.requirements = aiForm.job_requirement
  editForm.benefits = aiForm.job_benefits

  // Update the editors
  nextTick(() => {
    if (editForm.description && $refs.descriptionEditor) {
      $refs.descriptionEditor.setContent(editForm.description)
    }
    if (editForm.requirements && $refs.requirementsEditor) {
      $refs.requirementsEditor.setContent(editForm.requirements)
    }
    if (editForm.benefits && $refs.benefitsEditor) {
      $refs.benefitsEditor.setContent(editForm.benefits)
    }
  })

  contentApplied.value = true
  setTimeout(() => {
    contentApplied.value = false
  }, 3000)

  // Close the AI modal
  showAIModal.value = false
}

const previousAIVersion = () => {
  if (currentAiVersion > 0) {
    currentAiVersion--
    const version = aiHistory.value[currentAiVersion]
    aiForm.job_description = version.description
    aiForm.job_requirement = version.requirement
    aiForm.job_benefits = version.benefits
  }
}

const nextAIVersion = () => {
  if (currentAiVersion < aiHistory.value.length - 1) {
    currentAiVersion++
    const version = aiHistory.value[currentAiVersion]
    aiForm.job_description = version.description
    aiForm.job_requirement = version.requirement
    aiForm.job_benefits = version.benefits
  }
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