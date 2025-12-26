<template>
  <Dialog
    v-model="isOpen"
    :options="{
      title: __('Enter Company Information'),
      size: '4xl'
    }"
  >
    <template #body-title>
      <div>
        <h3 class="text-lg font-semibold text-gray-900">
          {{ isEditMode ? __('Edit Page Information') : __('Enter Company & Job Information') }}
        </h3>
        <p class="text-sm text-gray-500 mt-1">
          {{ isEditMode ? __('Update the information for your landing page') : __('Fill in the information to customize your landing page') }}
        </p>
      </div>
    </template>

    <template #body-content>
      <div class="overflow-y-auto max-h-[70vh] p-1">
        <!-- Page Title -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __('Page Title') }}
            <span class="text-red-500">*</span>
          </label>
          <FormControl
            v-model="formData.page_title"
            type="text"
            :placeholder="__('Enter page title (e.g., Tuyển dụng Developer)')"
          />
        </div>

        <!-- Tabs for different sections -->
        <Tabs
          as="div"
          class="border rounded-lg"
          v-model="activeTabIndex"
          :tabs="tabsConfig"
        >
          <template #tab-panel="{ tab }">
            <div class="p-6">
              <!-- Company Information Tab -->
              <div v-if="tab.key === 'company'" class="space-y-4">
            <!-- Company Profile Selection -->
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div class="flex items-start">
                <FeatherIcon name="info" class="h-4 w-4 text-blue-600 mr-2 mt-0.5" />
                <div class="flex-1">
                  <p class="text-sm font-medium text-blue-900 mb-2">{{ __('Quick Fill from Company Profile') }}</p>
                  <p class="text-xs text-blue-700 mb-3">{{ __('Select a saved company profile to auto-fill information (you can still edit after selecting)') }}</p>
                  
                  <FormControl
                    v-model="selectedCompanyProfile"
                    type="select"
                    :options="companyProfileOptions"
                    :placeholder="__('Select company profile...')"
                    :loading="loadingProfiles"
                  />
                </div>
              </div>
            </div>

            <!-- Company Information Fields -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Company Name') }}
                </label>
                <FormControl
                  v-model="formData.company_name"
                  type="text"
                  :placeholder="__('Enter company name')"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Company Logo') }}
              </label>
              <FileUploader
                :file-types="['image/*']"
                :upload-args="{
                  doctype: 'Mira Campaign',
                  docname: 'temp',
                  private: false
                }"
                @success="(file) => formData.company_logo = file.file_url"
              >
                <template #default="{ file, uploading, progress, error: uploadError, openFileSelector }">
                  <div 
                    class="border-2 border-dashed border-gray-300 rounded-lg p-4 hover:border-blue-400 transition-colors cursor-pointer"
                    @click="!formData.company_logo && openFileSelector()"
                  >
                    <div v-if="uploading" class="text-center">
                      <FeatherIcon name="loader" class="h-8 w-8 text-blue-600 animate-spin mx-auto mb-2" />
                      <p class="text-sm text-gray-600">{{ __('Uploading...') }} {{ progress }}%</p>
                    </div>
                    <div v-else-if="formData.company_logo" class="text-center">
                      <img :src="formData.company_logo" class="h-20 mx-auto mb-2 object-contain" />
                      <p class="text-xs text-gray-500 mb-2 truncate">{{ formData.company_logo }}</p>
                      <Button
                        @click.stop="formData.company_logo = ''"
                        variant="ghost"
                        size="sm"
                      >
                        {{ __('Remove') }}
                      </Button>
                    </div>
                    <div v-else class="text-center">
                      <FeatherIcon name="upload-cloud" class="h-8 w-8 text-gray-400 mx-auto mb-2" />
                      <p class="text-sm text-gray-600">{{ __('Click to upload logo') }}</p>
                      <p class="text-xs text-gray-500 mt-1">{{ __('PNG, JPG, SVG up to 5MB') }}</p>
                    </div>
                    <p v-if="uploadError" class="text-xs text-red-600 mt-2">{{ uploadError }}</p>
                  </div>
                </template>
              </FileUploader>
            </div>

            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Company Slogan') }}
              </label>
              <FormControl
                v-model="formData.company_slogan"
                type="text"
                :placeholder="__('Enter company slogan')"
              />
            </div>

            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Company Short Description') }}
              </label>
              <FormControl
                v-model="formData.company_short_description"
                type="textarea"
                :placeholder="__('Enter short description')"
                :rows="3"
              />
            </div>

            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Company Vision') }}
              </label>
              <FormControl
                v-model="formData.company_vision"
                type="textarea"
                :placeholder="__('Enter company vision')"
                :rows="3"
              />
            </div>

            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Company Mission') }}
              </label>
              <FormControl
                v-model="formData.company_mission"
                type="textarea"
                :placeholder="__('Enter company mission')"
                :rows="3"
              />
            </div>
              </div>

              <!-- Job Information Tab -->
              <div v-if="tab.key === 'job'" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Job Title') }}
              </label>
              <FormControl
                v-model="formData.job_title"
                type="text"
                :placeholder="__('Enter job title')"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Work Address') }}
              </label>
              <FormControl
                v-model="formData.work_address"
                type="text"
                :placeholder="__('Enter work address')"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Employment Type') }}
              </label>
              <FormControl
                v-model="formData.employment_type"
                type="select"
                :options="employmentTypeOptions"
                :placeholder="__('Select employment type')"
              />
            </div>

            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Salary Range') }}
              </label>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <FormControl
                    v-model="formData.salary_min"
                    type="text"
                    :placeholder="__('Min (e.g., 10M)')"
                  />
                </div>
                <div>
                  <FormControl
                    v-model="formData.salary_max"
                    type="text"
                    :placeholder="__('Max (e.g., 20M)')"
                  />
                </div>
              </div>
              <p v-if="salaryDisplay" class="text-xs text-gray-500 mt-1.5">
                {{ __('Preview:') }} <span class="font-medium text-gray-700">{{ salaryDisplay }}</span>
              </p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Hiring Quantity') }}
              </label>
              <FormControl
                v-model="formData.hiring_quantity"
                type="text"
                :placeholder="__('Enter number of positions')"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Application Deadline') }}
              </label>
              <FormControl
                v-model="formData.application_deadline"
                type="date"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Published Date') }}
              </label>
              <FormControl
                v-model="formData.published_date"
                type="date"
              />
            </div>

            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Job Description') }}
              </label>
              <TextEditor
                variant="outline"
                :content="formData.job_description"
                @change="(content) => formData.job_description = content"
                :placeholder="__('Enter job description')"
                :bubbleMenu="true"
                :fixedMenu="true"
                :editorClass="'prose-sm !w-full !max-w-full overflow-auto min-h-[150px] max-h-80 py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 focus:border-gray-500 focus:ring-0 transition-colors'"
              />
            </div>

            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Job Requirements') }}
              </label>
              <TextEditor
                variant="outline"
                :content="formData.job_requirements"
                @change="(content) => formData.job_requirements = content"
                :placeholder="__('Enter job requirements')"
                :bubbleMenu="true"
                :fixedMenu="true"
                :editorClass="'prose-sm !w-full !max-w-full overflow-auto min-h-[150px] max-h-80 py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 focus:border-gray-500 focus:ring-0 transition-colors'"
              />
            </div>

            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Job Benefits') }}
              </label>
              <TextEditor
                variant="outline"
                :content="formData.job_benefits"
                @change="(content) => formData.job_benefits = content"
                :placeholder="__('Enter job benefits')"
                :bubbleMenu="true"
                :fixedMenu="true"
                :editorClass="'prose-sm !w-full !max-w-full overflow-auto min-h-[150px] max-h-80 py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 focus:border-gray-500 focus:ring-0 transition-colors'"
              />
            </div>
              </div>

              <!-- Contact Information Tab -->
              <div v-if="tab.key === 'contact'" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Phone Number 1') }}
              </label>
              <FormControl
                v-model="formData.company_number_one"
                type="text"
                :placeholder="__('Enter phone number')"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Phone Number 2') }}
              </label>
              <FormControl
                v-model="formData.company_number_two"
                type="text"
                :placeholder="__('Enter phone number')"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Email 1') }}
              </label>
              <FormControl
                v-model="formData.company_email_one"
                type="email"
                :placeholder="__('Enter email address')"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Email 2') }}
              </label>
              <FormControl
                v-model="formData.company_email_two"
                type="email"
                :placeholder="__('Enter email address')"
              />
            </div>

            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Head Office Address') }}
              </label>
              <FormControl
                v-model="formData.head_office"
                type="text"
                :placeholder="__('Enter head office address')"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Company Website') }}
              </label>
              <FormControl
                v-model="formData.company_website"
                type="text"
                :placeholder="__('Enter website URL')"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Web Favicon') }}
              </label>
              <FileUploader
                :file-types="['image/*']"
                :upload-args="{
                  doctype: 'Mira Campaign',
                  docname: 'temp',
                  private: false
                }"
                @success="(file) => formData.web_favicon = file.file_url"
              >
                <template #default="{ file, uploading, progress, error: uploadError, openFileSelector }">
                  <div 
                    class="border-2 border-dashed border-gray-300 rounded-lg p-3 hover:border-blue-400 transition-colors cursor-pointer"
                    @click="!formData.web_favicon && openFileSelector()"
                  >
                    <div v-if="uploading" class="text-center">
                      <FeatherIcon name="loader" class="h-6 w-6 text-blue-600 animate-spin mx-auto mb-1" />
                      <p class="text-xs text-gray-600">{{ __('Uploading...') }} {{ progress }}%</p>
                    </div>
                    <div v-else-if="formData.web_favicon" class="text-center">
                      <img :src="formData.web_favicon" class="h-12 mx-auto mb-1 object-contain" />
                      <p class="text-xs text-gray-500 mb-1 truncate">{{ formData.web_favicon }}</p>
                      <Button
                        @click.stop="formData.web_favicon = ''"
                        variant="ghost"
                        size="sm"
                      >
                        {{ __('Remove') }}
                      </Button>
                    </div>
                    <div v-else class="text-center">
                      <FeatherIcon name="upload-cloud" class="h-6 w-6 text-gray-400 mx-auto mb-1" />
                      <p class="text-xs text-gray-600">{{ __('Click to upload favicon') }}</p>
                      <p class="text-xs text-gray-500 mt-0.5">{{ __('ICO, PNG 16x16 or 32x32') }}</p>
                    </div>
                    <p v-if="uploadError" class="text-xs text-red-600 mt-1">{{ uploadError }}</p>
                  </div>
                </template>
              </FileUploader>
            </div>
              </div>

              <!-- Social Media Tab -->
              <div v-if="tab.key === 'social'" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Facebook') }}
              </label>
              <FormControl
                v-model="formData.company_fb"
                type="text"
                :placeholder="__('Enter Facebook link')"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('LinkedIn') }}
              </label>
              <FormControl
                v-model="formData.company_linkedin"
                type="text"
                :placeholder="__('Enter LinkedIn link')"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('YouTube') }}
              </label>
              <FormControl
                v-model="formData.company_youtube"
                type="text"
                :placeholder="__('Enter YouTube link')"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Zalo OA') }}
              </label>
              <FormControl
                v-model="formData.company_zalo_oa"
                type="text"
                :placeholder="__('Enter Zalo OA link')"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('TikTok') }}
              </label>
              <FormControl
                v-model="formData.company_tiktok"
                type="text"
                :placeholder="__('Enter TikTok link')"
              />
            </div>
              </div>

              <!-- Data Collection Tab -->
              <div v-if="tab.key === 'data'">
                <ReceiveDataConfigsManager
                  ref="receiveDataConfigsRef"
                  v-model="formData.receive_data_configs"
                  :template-id="selectedTemplate?.template_id || formData.template_id"
                  :form-config-id="formData.form_config_id"
                />
              </div>
            </div>
          </template>
        </Tabs>
      </div>
    </template>

    <template #actions>
      <div class="flex flex-col w-full">
        <!-- Error Message -->
        <div v-if="error" class="mb-3 p-3 bg-red-50 border border-red-200 rounded-lg">
          <div class="flex items-start">
            <FeatherIcon name="alert-circle" class="h-5 w-5 text-red-600 mr-2 mt-0.5" />
            <div>
              <p class="text-sm font-medium text-red-900">{{ __('Failed to create page') }}</p>
              <p class="text-xs text-red-700 mt-1">{{ error }}</p>
            </div>
          </div>
        </div>
        
        <div class="flex items-center justify-between w-full">
          <div class="text-sm text-gray-600">
            <span class="text-red-500">*</span>
            {{ __('Required fields') }}
          </div>
          <div class="flex gap-3">
            <Button
              @click="closeDialog"
              :disabled="loading"
              variant="ghost"
            >
              {{ __('Cancel') }}
            </Button>
            <Button
              @click="confirmSubmit"
              :disabled="!formData.page_title || loading"
              :loading="loading"
              variant="solid"
            >
              {{ loading ? (isEditMode ? __('Updating...') : __('Creating...')) : (isEditMode ? __('Update Page') : __('Create Page')) }}
            </Button>
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch, computed, onMounted, h } from 'vue'
import { Dialog, Button, FeatherIcon, FormControl, FileUploader, TextEditor, Tabs, call } from 'frappe-ui'
import { useToast } from '@/composables/useToast'
import ReceiveDataConfigsManager from './ReceiveDataConfigsManager.vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  selectedTemplate: {
    type: Object,
    default: null
  },
  campaignName: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  },
  isEditMode: {
    type: Boolean,
    default: false
  },
  initialData: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'submit'])

const toast = useToast()
const isOpen = ref(props.show)
const receiveDataConfigsRef = ref(null)

// Company profile selection
const selectedCompanyProfile = ref('')
const companyProfileOptions = ref([])
const companyProfilesData = ref([])
const loadingProfiles = ref(false)

// Employment type options
const employmentTypeOptions = [
  { label: 'Full-time', value: 'Full-time' },
  { label: 'Part-time', value: 'Part-time' },
  { label: 'Contract', value: 'Contract' },
  { label: 'Internship', value: 'Internship' },
  { label: 'Freelance', value: 'Freelance' },
  { label: 'Remote', value: 'Remote' }
]

// Tabs configuration
const activeTabIndex = ref(0)

const tabsConfig = [
  {
    key: 'company',
    label: __('Company Info'),
    icon: h(FeatherIcon, { name: 'briefcase', class: 'w-4 h-4' })
  },
  {
    key: 'job',
    label: __('Job Details'),
    icon: h(FeatherIcon, { name: 'file-text', class: 'w-4 h-4' })
  },
  {
    key: 'contact',
    label: __('Contact Info'),
    icon: h(FeatherIcon, { name: 'phone', class: 'w-4 h-4' })
  },
  {
    key: 'social',
    label: __('Social Media'),
    icon: h(FeatherIcon, { name: 'share-2', class: 'w-4 h-4' })
  },
  {
    key: 'data',
    label: __('Data Collection'),
    icon: h(FeatherIcon, { name: 'database', class: 'w-4 h-4' })
  }
]

// Form data với tất cả fields từ API
const formData = ref({
  // Required
  page_title: '',
  
  // Company info
  company_name: '',
  company_logo: '',
  company_slogan: '',
  company_short_description: '',
  company_vision: '',
  company_mission: '',
  web_favicon: '',
  
  // Job info
  job_title: '',
  work_address: '',
  employment_type: '',
  salary_min: '',
  salary_max: '',
  hiring_quantity: '',
  application_deadline: '',
  published_date: '',
  job_description: '',
  job_requirements: '',
  job_benefits: '',
  
  // Contact info
  company_number_one: '',
  company_number_two: '',
  company_email_one: '',
  company_email_two: '',
  head_office: '',
  company_website: '',
  
  // Social media
  company_fb: '',
  company_linkedin: '',
  company_youtube: '',
  company_zalo_oa: '',
  company_tiktok: '',
  
  // Receive data configurations
  receive_data_configs: [],
  form_config_id: null,
  template_id: null
})

// Computed salary display with smart formatting
const salaryDisplay = computed(() => {
  const min = formData.value.salary_min?.trim()
  const max = formData.value.salary_max?.trim()
  
  if (!min && !max) return ''
  if (min && max) return `${min} - ${max}`
  if (min && !max) return `Từ ${min}`
  if (!min && max) return `Lên đến ${max}`
  return ''
})

// Watch show prop to sync with isOpen
watch(() => props.show, (newVal) => {
  isOpen.value = newVal
  if (newVal) {
    if (props.isEditMode && props.initialData) {
      // Load initial data for editing
      loadInitialData()
    } else {
      // Initialize with campaign name as default page title
      formData.value.page_title = props.campaignName || ''
      
      // Initialize default receive_data_configs so customer sees it pre-configured
      initializeDefaultReceiveDataConfig()
    }
    // Load company profiles when modal opens
    loadCompanyProfiles()
  } else {
    // Reset form when closing
    resetForm()
  }
})

// Watch company profile selection
watch(selectedCompanyProfile, (newValue, oldValue) => {
  // Prevent infinite loop by checking if value actually changed
  if (newValue !== oldValue && newValue !== null && newValue !== undefined && newValue !== '') {
    onCompanyProfileSelect(newValue)
  }
}, { flush: 'post' })

// Load initial data for edit mode
const loadInitialData = () => {
  if (!props.initialData) return
  
  console.log('📝 Loading initial data:', props.initialData)
  
  // Parse salary if exists
  let salaryMin = ''
  let salaryMax = ''
  if (props.initialData.salary) {
    const salary = props.initialData.salary
    // Check format: "10M - 20M" or "Từ 10M" or "Lên đến 20M"
    if (salary.includes(' - ')) {
      const parts = salary.split(' - ')
      salaryMin = parts[0]?.trim() || ''
      salaryMax = parts[1]?.trim() || ''
    } else if (salary.startsWith('Từ ')) {
      salaryMin = salary.replace('Từ ', '').trim()
    } else if (salary.startsWith('Lên đến ')) {
      salaryMax = salary.replace('Lên đến ', '').trim()
    } else {
      // Fallback: try to parse as range
      salaryMin = salary
    }
  }
  
  formData.value = {
    page_title: props.initialData.page_title || '',
    company_name: props.initialData.company_name || '',
    company_logo: props.initialData.company_logo || '',
    company_slogan: props.initialData.company_slogan || '',
    company_short_description: props.initialData.company_short_description || '',
    company_vision: props.initialData.company_vision || '',
    company_mission: props.initialData.company_mission || '',
    web_favicon: props.initialData.web_favicon || '',
    job_title: props.initialData.job_title || '',
    work_address: props.initialData.work_address || '',
    employment_type: props.initialData.employment_type || '',
    salary_min: salaryMin,
    salary_max: salaryMax,
    hiring_quantity: props.initialData.hiring_quantity || '',
    application_deadline: props.initialData.application_deadline || '',
    published_date: props.initialData.published_date || '',
    job_description: props.initialData.job_description || '',
    job_requirements: props.initialData.job_requirements || '',
    job_benefits: props.initialData.job_benefits || '',
    company_number_one: props.initialData.company_number_one || '',
    company_number_two: props.initialData.company_number_two || '',
    company_email_one: props.initialData.company_email_one || '',
    company_email_two: props.initialData.company_email_two || '',
    head_office: props.initialData.head_office || '',
    company_website: props.initialData.company_website || '',
    company_fb: props.initialData.company_fb || '',
    company_linkedin: props.initialData.company_linkedin || '',
    company_youtube: props.initialData.company_youtube || '',
    company_zalo_oa: props.initialData.company_zalo_oa || '',
    company_tiktok: props.initialData.company_tiktok || '',
    receive_data_configs: props.initialData.receive_data_configs || [],
    form_config_id: props.initialData.form_config_id || null,
    template_id: props.initialData.template_id || ''
  }
  
  console.log('✅ Form data loaded:', formData.value)
}

// Watch isOpen to emit close event
watch(isOpen, (newVal) => {
  if (!newVal) {
    emit('close')
  }
})

const resetForm = () => {
  formData.value = {
    page_title: '',
    company_name: '',
    company_logo: '',
    company_slogan: '',
    company_short_description: '',
    company_vision: '',
    company_mission: '',
    web_favicon: '',
    job_title: '',
    work_address: '',
    employment_type: '',
    salary_min: '',
    salary_max: '',
    hiring_quantity: '',
    application_deadline: '',
    published_date: '',
    job_description: '',
    job_requirements: '',
    job_benefits: '',
    company_number_one: '',
    company_number_two: '',
    company_email_one: '',
    company_email_two: '',
    head_office: '',
    company_website: '',
    company_fb: '',
    company_linkedin: '',
    company_youtube: '',
    company_zalo_oa: '',
    company_tiktok: '',
    receive_data_configs: [],
    form_config_id: null,
    template_id: ''
  }
  selectedCompanyProfile.value = ''
}

// Initialize default receive_data_configs with API webhook
const initializeDefaultReceiveDataConfig = async () => {
  console.log('🤖 Initializing default receive_data_configs...')
  
  const siteUrl = window.location.origin
  const apiPath = '/api/method/mbw_mira.api.v1.talent.create'
  const defaultEndpoint = `${siteUrl}${apiPath}`
  
  // Default field mappings - common fields that should be auto-mapped (displayed in UI)
  // Using Mira Talent field names
  const visibleMappings = [
    { form_field: 'full_name', api_field: 'full_name' },
    { form_field: 'primary_email', api_field: 'email' },
    { form_field: 'phone_number', api_field: 'phone' },
    { form_field: 'cv_upload', api_field: 'resume' },
    { form_field: 'linkedin_url', api_field: 'linkedin_profile' }
  ]
  
  // Hidden metadata fields from CMS - auto-added but NOT displayed in UI
  const hiddenMetadataMappings = [
    { form_field: 'form_id', api_field: 'form_id' },
    { form_field: 'page_id', api_field: 'page_id' },
    { form_field: 'form_url', api_field: 'form_url' },
    { form_field: 'utm_source', api_field: 'utm_source' },
    { form_field: 'utm_medium', api_field: 'utm_medium' },
    { form_field: 'utm_content', api_field: 'utm_content' },
    { form_field: 'utm_campaign', api_field: 'utm_campaign' },
    { form_field: 'utm_term', api_field: 'utm_term' },
    { form_field: 'custom_field', api_field: 'custom_field' }
  ]
  
  // Combine for the full mapping
  const defaultMappings = [...visibleMappings, ...hiddenMetadataMappings]
  
  // Fetch API credentials for current user
  let apiHeaders = {}
  try {
    console.log('🔑 Fetching API credentials...')
    const credResponse = await call('mbw_mira.utils.auth.get_user_api_credentials')
    
    if (credResponse?.status === 'success' && credResponse?.data) {
      const { api_key, api_secret } = credResponse.data
      apiHeaders = {
        'Authorization': `token ${api_key}:${api_secret}`
      }
      console.log('✅ API credentials fetched successfully')
    }
  } catch (error) {
    console.error('⚠️ Could not fetch API credentials:', error)
    // Continue without auth headers - user can add manually
  }
  
  const defaultConfig = {
    type: 'API',
    end_point: defaultEndpoint,
    content_type: 'application/json',
    api_headers: apiHeaders,
    field_mappings: defaultMappings
  }
  
  formData.value.receive_data_configs = [defaultConfig]
  console.log('✅ Default receive_data_configs initialized:', defaultConfig)
}

const closeDialog = () => {
  isOpen.value = false
}

const confirmSubmit = async () => {
  if (!formData.value.page_title || props.loading) {
    return
  }
  
  // Auto-save any pending config before submit
  if (receiveDataConfigsRef.value && receiveDataConfigsRef.value.autoSaveConfigIfNeeded) {
    try {
      const wasSaved = await receiveDataConfigsRef.value.autoSaveConfigIfNeeded()
      if (wasSaved) {
        console.log('✅ Auto-saved pending configuration before submit')
        toast.success(__('Auto-saved pending data collection configuration'))
      }
    } catch (error) {
      console.error('❌ Failed to auto-save config:', error)
      toast.error(__('Failed to save data collection configuration'))
      return // Don't proceed if auto-save failed
    }
  }
  
  // Clean up empty values to reduce payload size
  const cleanedData = {}
  for (const [key, value] of Object.entries(formData.value)) {
    // Skip salary_min and salary_max - we'll combine them
    if (key === 'salary_min' || key === 'salary_max') continue
    
    if (value && value.trim && value.trim() !== '') {
      cleanedData[key] = value.trim()
    } else if (value && !value.trim) {
      cleanedData[key] = value
    }
  }
  
  // Combine salary_min and salary_max into salary field
  if (salaryDisplay.value) {
    cleanedData.salary = salaryDisplay.value
  }
  
  // Add receive_data_configs to cleaned data
  console.log('🔍 Checking receive_data_configs in formData:', formData.value.receive_data_configs)
  if (formData.value.receive_data_configs && formData.value.receive_data_configs.length > 0) {
    cleanedData.receive_data_configs = formData.value.receive_data_configs
    console.log('📧 Receive data configs added to submit:', cleanedData.receive_data_configs)
  } else {
    console.log('⚠️ No receive_data_configs found or empty array')
  }
  
  console.log('📤 Final form data to submit:', cleanedData)
  
  // Don't close modal - let parent handle closing on success
  emit('submit', cleanedData)
}

// Company profile methods
const loadCompanyProfiles = async () => {
  if (companyProfileOptions.value.length > 0) return // Already loaded
  
  loadingProfiles.value = true
  try {
    console.log('🏢 Loading company profiles...')
    
    const response = await call('mbw_mira.integrations.cms_page.get_company_profile_list')
    
    if (response?.message?.status === 'success' && response?.message?.data) {
      // Store full profile data
      companyProfilesData.value = response.message.data
      
      // Create options for dropdown
      companyProfileOptions.value = response.message.data.map((profile, index) => ({
        label: profile.company_name,
        value: index // Use index to reference the full data
      }))
      
      console.log('✅ Company profiles loaded:', companyProfileOptions.value)
    } else {
      console.log('⚠️ No company profiles found')
    }
  } catch (error) {
    console.error('❌ Error loading company profiles:', error)
    toast.error(__('Failed to load company profiles'))
  } finally {
    loadingProfiles.value = false
  }
}

const onCompanyProfileSelect = (selectedIndex) => {
  console.log(selectedIndex)
  if (selectedIndex === null || selectedIndex === undefined || selectedIndex === '') {
    return
  }
  
  const profile = companyProfilesData.value[selectedIndex]
  if (!profile) {
    console.error('❌ Profile not found at index:', selectedIndex)
    return
  }
  
  console.log('📋 Auto-filling company profile:', profile)
  
  // Map API fields to form fields
  formData.value = {
    ...formData.value,
    company_name: profile.company_name || '',
    company_logo: profile.logo || '',
    company_slogan: profile.slogan || '',
    company_short_description: profile.short_description || '',
    company_vision: profile.vision || '',
    company_mission: profile.mission || '',
    web_favicon: profile.favicon || '',
    company_number_one: profile.phone_1 || '',
    company_number_two: profile.phone_2 || '',
    company_email_one: profile.email_1 || '',
    company_email_two: profile.email_2 || '',
    head_office: profile.headquarters_address || '',
    company_website: profile.website || '',
    company_fb: profile.facebook || '',
    company_linkedin: profile.linkedin || '',
    company_youtube: profile.youtube || '',
    company_zalo_oa: profile.zalo_oa || '',
    company_tiktok: profile.tiktok || ''
  }
  
  console.log('✅ Company profile auto-filled into form')
  toast.success(__('Company information loaded successfully'))
}

// Watch formData.receive_data_configs for changes
watch(() => formData.value.receive_data_configs, (newConfigs) => {
  console.log('📥 CompanyInfoModal formData.receive_data_configs changed:', newConfigs)
}, { deep: true })

// Initialize on mount
onMounted(() => {
  if (props.show) {
    loadCompanyProfiles()
  }
})
</script>
