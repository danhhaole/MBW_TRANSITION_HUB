<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 w-full via-white to-indigo-50 py-8 container mx-auto">
    <div class="mx-auto w-full px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-full mb-4">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ __('Contact Information') }}</h1>
        <p class="text-gray-600">{{ __('Are you interested in our company? Please leave your information and we will contact you shortly!') }}</p>
      </div>

      <!-- Main Form Card -->
      <div class="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
        <form @submit.prevent="submit" class="p-8">
          <!-- Personal Information Section -->
          <div class="mb-8">
            <h2 class="text-xl font-semibold text-gray-800 mb-1 flex items-center">
              <svg class="w-5 h-5 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              {{ __('Personal Information') }}
            </h2>
            <p class="text-sm text-gray-500 mb-6">{{ __('Please provide accurate information about yourself') }}</p>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <FormControl v-for="field in personalFields" :key="field.fieldname" v-model="form[field.fieldname]"
                :type="field.type" :label="field.label" :options="field.options" :required="field.required"
                :placeholder="field.placeholder" class="form-field" />
            </div>
          </div>

          <!-- Professional Information Section -->
          <div class="mb-8 pt-6 border-t border-gray-100">
            <h2 class="text-xl font-semibold text-gray-800 mb-1 flex items-center">
              <svg class="w-5 h-5 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6" />
              </svg>
              {{ __('Professional Information') }}
            </h2>
            <p class="text-sm text-gray-500 mb-6">{{ __('Please provide information about your experience and skills') }}</p>

            <div class="space-y-6">
              <FormControl v-for="field in professionalFields" :key="field.fieldname" v-model="form[field.fieldname]"
                :type="field.type" :label="field.label" :options="field.options" :required="field.required"
                :placeholder="field.placeholder" class="form-field" />
            </div>
          </div>

          <!-- Skills Section -->
          <!-- {{campaignDetails}} -->
          <div
            v-if="(campaignDetails.skills && campaignDetails.skills.length) || (campaignDetails.segment_skills && campaignDetails.segment_skills.length)"
            class="mb-8 pt-6 border-t border-gray-100">
            <h2 class="text-xl font-semibold text-gray-800 mb-1 flex items-center">
              <svg class="w-5 h-5 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              {{ __('Skills') }}
            </h2>
            <p class="text-sm text-gray-500 mb-6">{{ __('Please select the skills that are relevant to the position you are applying for') }}</p>

            <!-- Campaign Skills -->

            <!-- Segment Skills -->
            <div v-if="campaignDetails.segment_skills && campaignDetails.segment_skills.length">
              <label class="block text-sm font-medium text-gray-700 mb-3">{{ __('Skills from segment') }}</label>
              <div class="flex flex-wrap gap-2">
                <Button v-for="skill in campaignDetails.segment_skills" :key="'s-' + skill"
                  :variant="form.skills.includes(skill) ? 'default' : 'outline'" @click.prevent="toggleSkill(skill)"
                  size="sm" class="skill-button transition-all duration-200 hover:scale-105">
                  {{ skill }}
                </Button>
              </div>
            </div>

            <!-- Selected Skills Display -->
            <div v-if="form.skills.length" class="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <p class="text-sm font-medium text-blue-800 mb-2">{{ __('Selected skills') }} ({{ form.skills.length }}):
              </p>
              <div class="flex flex-wrap gap-1">
                <span v-for="skill in form.skills" :key="skill"
                  class="inline-flex items-center px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">
                  {{ skill }}
                  <button @click.prevent="toggleSkill(skill)" class="ml-1 hover:text-blue-600">
                    <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd"
                        d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                        clip-rule="evenodd" />
                    </svg>
                  </button>
                </span>
              </div>
            </div>
          </div>

          <!-- Submit Button -->
          <div class="pt-6 border-t border-gray-100">
            <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
              <p class="text-sm text-gray-500">
                {{ __('By submitting this form, you agree to our terms of use.') }}
              </p>
              <Button type="submit" variant="solid" theme="gray" :loading="resource.loading" class="submit-button">
                <div class="flex items-center">
                  <FeatherIcon name="send" class="w-4 h-4 mr-2" />
                  {{ resource.loading ? __('Sending...') : __('Submit') }}
                </div>
              </Button>
            </div>
          </div>
        </form>
      </div>

      <!-- Footer -->
      <div class="text-center mt-8 text-sm text-gray-500">
        <p>{{ __('Need help? Contact us via email or hotline') }}</p>
      </div>
    </div>
    <ToastContainer />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Card, Button, FormControl, createResource, call } from 'frappe-ui'
import { useToast } from '@/composables/useToast'
import { useRouter } from 'vue-router'
import { ToastContainer } from '@/components/shared'

const router = useRouter()


const form = ref({
  full_name: '',
  email: '',
  phone: '',
  dob: '',
  headline: '',
  position: '',
  skills: [],
  cv_original_url: '',
  ai_summary: '',
  campaign: ''
})

const { showToast, showSuccess, showError } = useToast()

const allFields = computed(() => [
  { fieldname: 'full_name', label: 'Full Name', type: 'text', required: true, placeholder: 'Enter your full name' },
  { fieldname: 'email', label: 'Email', type: 'email', required: true, placeholder: 'example@email.com' },
  { fieldname: 'phone', label: 'Phone', type: 'tel', placeholder: '0123 456 789' },
  { fieldname: 'dob', label: 'Date of Birth', type: 'date' },
  { fieldname: 'position', label: 'Position', type: 'select', required: true, placeholder: 'Select your position', options: positionOptions.value },
  { fieldname: 'headline', label: 'Headline', type: 'text', placeholder: 'Example: Frontend Developer with 3 years of experience' },
  { fieldname: 'cv_original_url', label: 'CV Link', type: 'url', placeholder: 'https://drive.google.com/...' },
  { fieldname: 'ai_summary', label: 'Self Introduction', type: 'textarea', placeholder: 'Brief introduction about yourself, experience and career goals...' },
])

const personalFields = computed(() => allFields.value.filter(f => ['full_name', 'email', 'phone', 'dob'].includes(f.fieldname)))
const professionalFields = computed(() => allFields.value.filter(f => ['position', 'headline', 'cv_original_url', 'ai_summary'].includes(f.fieldname)))

const campaignDetails = ref({ skills: [], segment_skills: [] })
const positionOptions = ref([])

onMounted(async () => {
  const params = new URLSearchParams(window.location.search)
  form.value.campaign = params.get('campaign') || ''

  // Position options will be loaded from campaign details

  if (form.value.campaign) {
    try {
      const res = await call('mbw_mira.api.get_campaign_details_for_submit', { campaign_id: form.value.campaign })
      const data = res || {}
      console.log(res)
      
      // Load skills from segments
      campaignDetails.value.skills = data.segments.flatMap(seg => seg.criteria?.skills || [])
      if (Array.isArray(data.segments)) {
        const segmentSkills = data.segments.flatMap(seg => seg.criteria?.skills || [])
        campaignDetails.value.segment_skills = [...new Set(segmentSkills)]
      }
      
      // Load position options from segments
      if (Array.isArray(data.segments)) {
        positionOptions.value = data.segments.map(seg => ({
          label: seg.title,
          value: seg.title
        }))
        console.log('Position options loaded from campaign details:', positionOptions.value)
      }
    } catch (error) {
      console.error('Error loading campaign details:', error)
    }
  }
})

const resource = createResource({
  url: 'mbw_mira.api.submit_talent_profile',
  method: 'POST',
  auto: false,
  onSuccess(data) {
    console.log('API Response:', data)
    if (data.success) {
    showSuccess(data.message || __('Information has been sent!'))
    
    // Show confirmation dialog
    setTimeout(() => {
      if (confirm(__('Registration successful! Continue to homepage?'))) {
        router.push({ name: 'Mira Ladi Page', params: { slug: 'info' } })
      }
    }, 1000)
  } else {
      showError(data.message || __('Failed to send information'))
    }
  },
  onError(error) {
    console.error('API Error:', error)
    showError(error.message || 'An error occurred while sending information')
  }
})

function toggleSkill(skill) {
  const index = form.value.skills.indexOf(skill)
  if (index >= 0) {
    form.value.skills.splice(index, 1)
  } else {
    form.value.skills.push(skill)
  }
}

function submit() {
  // Validate required fields
  if (!form.value.campaign) {
    // showToast({ title: 'Lỗi', text: 'Thiếu thông tin campaign', type: 'error' })
    console.error('Missing campaign parameter')
    return
  }
  
  if (!form.value.full_name || !form.value.email || !form.value.position) {
    // showToast({ title: 'Lỗi', text: 'Vui lòng điền đầy đủ họ tên, email và position', type: 'error' })
    console.error('Missing required fields: full_name, email, or position')
    return
  }

  // Prepare payload - only send fields that have values
  const payload = {
    campaign: form.value.campaign,
    full_name: form.value.full_name.trim(),
    email: form.value.email.trim(),
  }

  // Add optional fields only if they have values
  if (form.value.phone?.trim()) payload.phone = form.value.phone.trim()
  if (form.value.dob) payload.dob = form.value.dob
  if (form.value.position?.trim()) payload.position = form.value.position.trim()
  if (form.value.headline?.trim()) payload.headline = form.value.headline.trim()
  if (form.value.cv_original_url?.trim()) payload.cv_original_url = form.value.cv_original_url.trim()
  if (form.value.ai_summary?.trim()) payload.ai_summary = form.value.ai_summary.trim()
  
  // Skills array - convert to JSON string format
  if (form.value.skills && form.value.skills.length > 0) {
    payload.skills = JSON.stringify(form.value.skills)  // ["React", "Vue", "JavaScript"]
  }

  console.log('Submitting payload:', payload)
  resource.submit(payload)
}
</script>

<style scoped>
.form-field {
  @apply transition-all duration-200;
}

.form-field:focus-within {
  @apply transform scale-[1.02];
}

.skill-button {
  @apply font-medium;
}

.submit-button:disabled {
  @apply opacity-50 cursor-not-allowed;
}

/* Custom scrollbar for better UX */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Responsive improvements */
@media (max-width: 640px) {
  .submit-button {
    @apply w-full justify-center;
  }
}
</style>