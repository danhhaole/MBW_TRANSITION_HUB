<template>
  <Dialog
    v-model="show"
    :options="{ size: '3xl', title: __('Email Preview') }"
  >
    <template #body-content>
      <div class="flex flex-col gap-4">
        <!-- Sample Data Input -->
        <div class="border-b pb-4">
          <div class="grid grid-cols-2 gap-3">
            <FormControl
              size="sm"
              v-model="sampleData.full_name"
              :label="__('Full Name')"
              placeholder="John Doe"
            />
            <FormControl
              size="sm"
              v-model="sampleData.email"
              :label="__('Email')"
              placeholder="john@example.com"
            />
            <FormControl
              size="sm"
              v-model="sampleData.phone"
              :label="__('Phone')"
              placeholder="+84 123 456 789"
            />
            <FormControl
              size="sm"
              v-model="sampleData.latest_title"
              :label="__('Latest Title')"
              placeholder="Senior Developer"
            />
            <FormControl
              size="sm"
              v-model="sampleData.latest_company"
              :label="__('Latest Company')"
              placeholder="ABC Corporation"
            />
            <FormControl
              size="sm"
              v-model="sampleData.total_years_of_experience"
              :label="__('Years of Experience')"
              placeholder="5"
            />
          </div>
        </div>

        <!-- Email Preview -->
        <div class="flex flex-col gap-3">
          <h3 class="text-base font-medium text-ink-gray-8">
            {{ __('Preview') }}
          </h3>
          
          <!-- Email Container -->
          <div class="border rounded-lg bg-white shadow-sm">
            <!-- Email Header -->
            <div class="border-b bg-surface-gray-2 px-4 py-3">
              <div class="flex items-center gap-2 text-sm text-ink-gray-6 mb-2">
                <FeatherIcon name="mail" class="h-4 w-4" />
                <span class="font-medium">{{ __('From:') }}</span>
                <span>recruitment@company.com</span>
              </div>
              <div class="flex items-center gap-2 text-sm text-ink-gray-6 mb-2">
                <FeatherIcon name="user" class="h-4 w-4" />
                <span class="font-medium">{{ __('To:') }}</span>
                <span>{{ sampleData.email || 'candidate@example.com' }}</span>
              </div>
              <div class="flex items-center gap-2 text-sm text-ink-gray-8 font-medium">
                <FeatherIcon name="file-text" class="h-4 w-4" />
                <span class="font-medium">{{ __('Subject:') }}</span>
                <span>{{ renderedSubject }}</span>
              </div>
            </div>

            <!-- Email Body -->
            <div class="p-6">
              <!-- Render HTML content with CSS injected -->
              <div
                class="email-preview-content max-w-none max-h-[calc(55vh-200px)] overflow-auto"
                v-html="renderedEmailWithCss"
              />
            </div>

            <!-- Email Footer -->
            <div class="border-t bg-surface-gray-2 px-4 py-3 text-xs text-ink-gray-5">
              <div class="flex items-center gap-2">
                <FeatherIcon name="clock" class="h-3 w-3" />
                <span>{{ __('Sent:') }} {{ currentDateTime }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { Dialog, FormControl, Button, FeatherIcon } from 'frappe-ui'
import { ref, computed, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  templateData: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue'])

const show = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})

const sampleData = ref({
  // Campaign fields
  campaign_name: 'Tech Talent Recruitment 2025',
  campaign_type: 'RECRUITMENT',
  campaign_description: 'Recruiting senior developers for new projects',
  jo_position: 'Senior Software Engineer', // Job position
  // Talent fields
  full_name: 'John Doe',
  email: 'john.doe@example.com',
  phone: '+84 123 456 789',
  gender: 'Male',
  date_of_birth: '1990-01-15',
  current_city: 'Ho Chi Minh City',
  linkedin_profile: 'linkedin.com/in/johndoe',
  facebook_profile: 'facebook.com/johndoe',
  zalo_profile: '0123456789',
  skills: 'Python, JavaScript, React, Node.js',
  total_years_of_experience: '5',
  latest_title: 'Senior Software Engineer',
  latest_company: 'Tech Innovations Inc.',
  highest_education: 'Bachelor of Computer Science',
  desired_role: 'Tech Lead',
  domain_expertise: 'Web Development, Cloud Architecture',
  current_salary: '30,000,000 VND',
  expected_salary: '40,000,000 VND',
  preferred_work_model: 'Hybrid',
  availability_date: '2025-12-01',
  current_status: 'Active',
  cultural_fit: 'High',
  internal_rating: 'A',
  priority_level: 'High',
})

const currentDateTime = computed(() => {
  return new Date().toLocaleString('vi-VN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
})

function loadSampleData() {
  // Reset to default sample data
  sampleData.value = {
    // Campaign fields
    campaign_name: 'Tech Talent Recruitment 2025',
    campaign_type: 'RECRUITMENT',
    campaign_description: 'Recruiting senior developers for new projects',
    jo_position: 'Senior Software Engineer', // Job position
    // Talent fields
    full_name: 'John Doe',
    email: 'john.doe@example.com',
    phone: '+84 123 456 789',
    gender: 'Male',
    date_of_birth: '1990-01-15',
    current_city: 'Ho Chi Minh City',
    linkedin_profile: 'linkedin.com/in/johndoe',
    facebook_profile: 'facebook.com/johndoe',
    zalo_profile: '0123456789',
    skills: 'Python, JavaScript, React, Node.js',
    total_years_of_experience: '5',
    latest_title: 'Senior Software Engineer',
    latest_company: 'Tech Innovations Inc.',
    highest_education: 'Bachelor of Computer Science',
    desired_role: 'Tech Lead',
    domain_expertise: 'Web Development, Cloud Architecture',
    current_salary: '30,000,000 VND',
    expected_salary: '40,000,000 VND',
    preferred_work_model: 'Hybrid',
    availability_date: '2025-12-01',
    current_status: 'Active',
    cultural_fit: 'High',
    internal_rating: 'A',
    priority_level: 'High',
  }
}

function renderTemplate(template) {
  if (!template) return ''
  
  let rendered = template
  
  // Replace all {{ fieldname }} with actual values
  Object.keys(sampleData.value).forEach((key) => {
    const regex = new RegExp(`{{\\s*${key}\\s*}}`, 'g')
    rendered = rendered.replace(regex, sampleData.value[key] || `[${key}]`)
  })
  
  return rendered
}

const renderedSubject = computed(() => {
  return renderTemplate(props.templateData.subject)
})

// Get CSS content from template
const templateCss = computed(() => {
  const css = props.templateData.css_content || ''
  console.log('🎨 [EmailPreview] CSS content:', css?.substring(0, 200) + '...')
  console.log('🎨 [EmailPreview] CSS length:', css?.length || 0)
  return css
})

// Get HTML content - prefer html_content over message
const templateHtml = computed(() => {
  // Priority: html_content > message
  const html = props.templateData.html_content || props.templateData.message || ''
  console.log('📄 [EmailPreview] HTML content source:', props.templateData.html_content ? 'html_content' : 'message')
  console.log('📄 [EmailPreview] HTML length:', html?.length || 0)
  return html
})

// Render email content with merge tags replaced
const renderedEmailContent = computed(() => {
  let content = templateHtml.value
  
  if (!content) {
    return '<p class="text-gray-500 italic">No content available</p>'
  }
  
  // Replace all {{ fieldname }} with actual values
  content = renderTemplate(content)
  
  console.log('✅ [EmailPreview] Rendered content length:', content.length)
  console.log('✅ [EmailPreview] Has CSS:', !!templateCss.value)
  
  return content
})

// Render email with CSS injected
const renderedEmailWithCss = computed(() => {
  let html = renderedEmailContent.value
  
  // Inject CSS if available
  if (templateCss.value && templateCss.value.trim() !== '') {
    // Wrap CSS in style tag and prepend to HTML
    const styleTag = `<style type="text/css">${templateCss.value}</style>`
    html = styleTag + html
    console.log('✅ [EmailPreview] CSS injected, total length:', html.length)
  } else {
    console.log('⚠️ [EmailPreview] No CSS to inject')
  }
  
  return html
})
</script>
