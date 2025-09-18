<template>
  <div class="min-h-screen bg-gray-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header>
        <div class="flex space-x-3">
          <Button variant="solid" theme="blue" @click="create">
            <template #prefix>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
            </template>
            {{ __('Create New') }}
          </Button>
          <Button variant="outline" theme="gray" @click="edit">
            <template #prefix>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </template>
            {{ __('Edit') }}
          </Button>
        </div>
      </template>
    </LayoutHeader>

    <div class="container mx-auto px-6 py-6">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <h1 class="text-2xl font-bold mb-4">{{ data.job_title || __('Loading...') }}</h1>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-3">
            <div>
              <label class="text-sm text-gray-600">{{ __('Job Code') }}</label>
              <p class="text-sm">{{ data.job_code || '-' }}</p>
            </div>
            <div>
              <label class="text-sm text-gray-600">{{ __('Department') }}</label>
              <p class="text-sm">{{ data.department_name || '-' }}</p>
            </div>
            <div>
              <label class="text-sm text-gray-600">{{ __('Location') }}</label>
              <p class="text-sm">{{ data.location_name || '-' }}</p>
            </div>
            <div>
              <label class="text-sm text-gray-600">{{ __('Status') }}</label>
              <div class="mt-1">
                <span :class="badgeClass(data.approval_status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">{{ data.approval_status }}</span>
              </div>
            </div>
          </div>
          <div class="space-y-3">
            <div>
              <label class="text-sm text-gray-600">{{ __('Posting Date') }}</label>
              <p class="text-sm">{{ formatDate(data.posting_date) || '-' }}</p>
            </div>
            <div>
              <label class="text-sm text-gray-600">{{ __('Closing Date') }}</label>
              <p class="text-sm">{{ formatDate(data.closing_date) || '-' }}</p>
            </div>
            <div>
              <label class="text-sm text-gray-600">{{ __('Owner') }}</label>
              <p class="text-sm">{{ data.owner_id || '-' }}</p>
            </div>
            <div>
              <label class="text-sm text-gray-600">{{ __('Total Applicants') }}</label>
              <p class="text-sm">{{ data.total_applicants || 0 }}</p>
            </div>
          </div>
        </div>
        <div class="mt-6">
          <label class="text-sm text-gray-600">{{ __('Description') }}</label>
          <div class="prose" v-html="data.description"></div>
        </div>
        <div class="mt-6">
          <label class="text-sm text-gray-600">{{ __('Requirements') }}</label>
          <div class="prose" v-html="data.requirements"></div>
        </div>
        <div class="mt-6">
          <label class="text-sm text-gray-600">{{ __('Benefits') }}</label>
          <div class="prose" v-html="data.benefits"></div>
        </div>
      </div>

      <!-- Job Opening Wizard Dialog -->
      <Dialog v-model="showForm" :options="{ size: 'xl' }">
        <template #body>
          <div class="flex h-[600px]">
            <!-- Left Panel - Steps -->
            <div class="w-80 bg-gray-50 p-6 border-r border-gray-200">
              <div class="mb-6">
                <h3 class="text-lg font-semibold text-gray-900">
                  {{ isEditMode ? __('Edit Job Opening') : __('Create Job Opening') }}
                </h3>
                <p class="text-sm text-gray-500 mt-1">
                  {{ __('Complete 2 simple steps to') }} {{ isEditMode ? __('update your job opening') : __('create your job opening') }}
                </p>
              </div>
              
              <!-- Step 1 -->
              <div class="flex items-center mb-4">
                <div :class="[
                  'flex items-center justify-center w-8 h-8 rounded-full text-sm font-medium',
                  currentStep >= 1 ? 'bg-green-500 text-white' : 'bg-gray-300 text-gray-600'
                ]">
                  <svg v-if="currentStep > 1" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  <span v-else>1</span>
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-900">{{ __('Basic Information') }}</p>
                  <p class="text-xs text-gray-500">{{ __('Job title, position, and department') }}</p>
                </div>
              </div>

              <!-- Step 2 -->
              <div class="flex items-center mb-6">
                <div :class="[
                  'flex items-center justify-center w-8 h-8 rounded-full text-sm font-medium',
                  currentStep >= 2 ? 'bg-blue-500 text-white' : 'bg-gray-300 text-gray-600'
                ]">
                  <svg v-if="currentStep > 2" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  <span v-else>2</span>
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-900">{{ __('Job Description') }}</p>
                  <p class="text-xs text-gray-500">{{ __('Description, requirements, and responsibilities') }}</p>
                </div>
              </div>

              <!-- Progress Bar -->
              <div class="mt-6">
                <div class="flex justify-between text-xs text-gray-500 mb-1">
                  <span>{{ __('Progress') }}</span>
                  <span>{{ currentStep }}/2</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-blue-500 h-2 rounded-full transition-all duration-300" :style="{ width: `${(currentStep / 2) * 100}%` }"></div>
                </div>
              </div>
            </div>

            <!-- Right Panel - Content -->
            <div class="flex-1 p-6">
              <!-- Step 1: Basic Information -->
              <div v-if="currentStep === 1">
                <div class="mb-6">
                  <h4 class="text-lg font-medium text-gray-900">{{ __('Basic Information') }}</h4>
                  <p class="text-sm text-gray-500">{{ __('Job title, position, and department') }}</p>
                </div>
                
                <div class="space-y-4">
                  <FormControl v-model="form.job_title" type="text" :label="__('Job Title')" :required="true" />
                  <FormControl v-model="form.job_code" type="text" :label="__('Job Code')" />
                  <div class="grid grid-cols-2 gap-4">
                    <FormControl v-model="form.department_name" type="text" :label="__('Department')" />
                    <FormControl v-model="form.location_name" type="text" :label="__('Location')" />
                  </div>
                  <FormControl v-model="form.number_of_openings" type="number" :label="__('Number Of Openings')" />
                  <div class="grid grid-cols-2 gap-4">
                    <FormControl v-model="form.posting_date" type="date" :label="__('Posting Date')" />
                    <FormControl v-model="form.closing_date" type="date" :label="__('Closing Date')" />
                  </div>
                  <div class="grid grid-cols-2 gap-4">
                    <FormControl v-model="form.approval_status" type="select" :label="__('Status')" :options="statusOptions" />
                    <FormControl v-model="form.owner_id" type="select" :label="__('Owner')" :options="ownerOptions" />
                  </div>
                </div>
              </div>

              <!-- Step 2: Job Description -->
              <div v-if="currentStep === 2">
                <div class="flex items-center justify-between mb-6">
                  <div>
                    <h4 class="text-lg font-medium text-gray-900">{{ __('Job Description') }}</h4>
                    <p class="text-sm text-gray-500">{{ __('Description, requirements, and responsibilities') }}</p>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    theme="blue"
                    @click="showAIModal = true"
                  >
                    <template #prefix>
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                    </template>
                    {{ __('AI Generation') }}
                  </Button>
                </div>
                
                <div class="space-y-4">
                  <div>
                    <FormControl v-model="form.description" type="textarea" :label="__('Job Description')" :rows="4" />
                    <div class="mt-2 text-xs text-gray-500">
                      {{ __('Provide a detailed description of the job responsibilities and day-to-day tasks') }}
                    </div>
                  </div>
                  <div>
                    <FormControl v-model="form.requirements" type="textarea" :label="__('Job Requirements')" :rows="4" />
                    <div class="mt-2 text-xs text-gray-500">
                      {{ __('Specify required qualifications, skills, experience, and education') }}
                    </div>
                  </div>
                  <div>
                    <FormControl v-model="form.benefits" type="textarea" :label="__('Benefits')" :rows="4" />
                    <div class="mt-2 text-xs text-gray-500">
                      {{ __('Highlight the benefits and what makes this role attractive') }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- Navigation Buttons -->
              <div class="flex justify-between pt-6 border-t border-gray-200 mt-6">
                <Button 
                  v-if="currentStep > 1"
                  variant="outline" 
                  theme="gray" 
                  @click="previousStep"
                >
                  <template #prefix>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                    </svg>
                  </template>
                  {{ __('Previous') }}
                </Button>
                <div v-else></div>
                
                <div class="flex space-x-3">
                  <Button variant="outline" theme="gray" @click="closeForm">
                    {{ __('Cancel') }}
                  </Button>
                  <Button 
                    v-if="currentStep < 2"
                    variant="solid" 
                    theme="blue" 
                    @click="nextStep"
                  >
                    {{ __('Next') }}
                    <template #suffix>
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                      </svg>
                    </template>
                  </Button>
                  <Button 
                    v-else
                    variant="solid" 
                    theme="blue" 
                    :loading="saving" 
                    @click="save"
                  >
                    {{ isEditMode ? __('Update') : __('Create') }}
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </template>
      </Dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Dialog, Breadcrumbs, Button, FormControl } from 'frappe-ui'
import { getJobOpeningDetails, updateJobOpeningData } from '@/services/jobOpeningService'

const route = useRoute()
const data = reactive({})
const showForm = ref(false)
const saving = ref(false)
const form = reactive({})
const isEditMode = ref(true)
const currentStep = ref(1)
const showAIModal = ref(false)
const ownerOptions = ref([])

const breadcrumbs = computed(() => [
  { label: __('Job Openings'), route: { name: 'JobOpeningManagement' } },
  { label: data.job_title || __('Loading...'), route: { name: 'JobOpeningDetailView' } }
])

const statusOptions = [
  { label: 'Draft', value: 'Draft' },
  { label: 'Pending Approval', value: 'Pending Approval' },
  { label: 'Approved', value: 'Approved' },
  { label: 'Rejected', value: 'Rejected' }
]

// Load owners for dropdown
const loadOwners = async () => {
  try {
    // Replace with your actual API call to get users
    const response = await fetch('/api/method/frappe.desk.reportview.get', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        doctype: 'User',
        fields: ['name', 'full_name'],
        filters: [['enabled', '=', 1]],
        limit_page_length: 100
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      
      // Xử lý dữ liệu từ cấu trúc {keys: [...], values: [...]}
      if (data.message && data.message.values) {
        ownerOptions.value = data.message.values.map(user => ({
          label: user[1] || user[0], // full_name hoặc name
          value: user[0] // name
        }))
      } else if (Array.isArray(data.message)) {
        // Fallback cho cấu trúc array thông thường
        ownerOptions.value = data.message.map(user => ({
          label: user.full_name || user.name,
          value: user.name
        }))
      }
    }
  } catch (error) {
    console.error('Error loading owners:', error)
    // Fallback options
    ownerOptions.value = [
      { label: __('Select Owner'), value: '' },
      { label: 'Administrator', value: 'Administrator' }
    ]
  }
}

const load = async () => {
  const res = await getJobOpeningDetails(route.params.id)
  Object.assign(data, res)
}

const edit = () => { 
  isEditMode.value = true
  currentStep.value = 1
  Object.assign(form, data); 
  showForm.value = true 
}

const create = () => {
  isEditMode.value = false
  currentStep.value = 1
  Object.assign(form, {
    job_title: '',
    job_code: '',
    department_name: '',
    location_name: '',
    number_of_openings: '',
    posting_date: '',
    closing_date: '',
    approval_status: 'Draft',
    owner_id: '',
    description: '',
    requirements: '',
    benefits: ''
  })
  showForm.value = true
}

const nextStep = () => {
  if (currentStep.value < 2) {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const closeForm = () => {
  showForm.value = false
  currentStep.value = 1
}

const save = async () => {
  saving.value = true
  try {
    if (isEditMode.value) {
      await updateJobOpeningData(form.name, form)
    } else {
      // Logic để tạo mới job opening
      // await createJobOpening(form)
      console.log('Creating new job opening:', form)
    }
    closeForm()
    await load()
  } finally {
    saving.value = false
  }
}

const badgeClass = (status) => ({
  'Draft': 'bg-gray-100 text-gray-800',
  'Pending Approval': 'bg-yellow-100 text-yellow-800',
  'Approved': 'bg-green-100 text-green-800',
  'Rejected': 'bg-red-100 text-red-800'
}[status] || 'bg-gray-100 text-gray-800')

const formatDate = (date) => date ? new Date(date).toLocaleDateString('vi-VN', { year: 'numeric', month: '2-digit', day: '2-digit' }) : ''

onMounted(async () => {
  await loadOwners()
  await load()
})
</script>