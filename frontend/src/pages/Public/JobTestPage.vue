<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold mb-8">Test Job Opening Public View</h1>
      
      <!-- Test Form -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">Test API</h2>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Job Opening ID</label>
            <input
              v-model="testJobId"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
              placeholder="Nhập Job Opening ID để test"
            />
          </div>
          
          <div class="flex gap-4">
            <Button @click="testGetPublicDetail" variant="solid" :loading="loading">
              Test Get Public Detail
            </Button>
            <Button @click="openJobPage" variant="outline" :disabled="!testJobId">
              Open Job Page
            </Button>
          </div>
        </div>
      </div>

      <!-- API Response -->
      <div v-if="apiResponse" class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">API Response</h2>
        <pre class="bg-gray-100 p-4 rounded text-sm overflow-auto">{{ JSON.stringify(apiResponse, null, 2) }}</pre>
      </div>

      <!-- Error Display -->
      <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <h3 class="text-red-800 font-semibold mb-2">Error</h3>
        <p class="text-red-700">{{ error }}</p>
      </div>

      <!-- Test Application Form -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4">Test Application Form</h2>
        
        <form @submit.prevent="testSubmitApplication" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
              <input
                v-model="testForm.full_name"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="Nguyen Van A"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                v-model="testForm.email"
                type="email"
                class="w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="test@example.com"
              />
            </div>
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Phone</label>
              <input
                v-model="testForm.phone"
                type="tel"
                class="w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="0123456789"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Experience Level</label>
              <select
                v-model="testForm.experience_level"
                class="w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="">Select experience</option>
                <option value="Mới tốt nghiệp">Mới tốt nghiệp</option>
                <option value="1-2 năm">1-2 năm</option>
                <option value="3-5 năm">3-5 năm</option>
                <option value="5+ năm">5+ năm</option>
              </select>
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Cover Letter</label>
            <textarea
              v-model="testForm.cover_letter"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
              placeholder="Write your cover letter..."
            ></textarea>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">CV File</label>
            <input
              ref="fileInput"
              type="file"
              accept=".pdf,.doc,.docx"
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          
          <Button type="submit" variant="solid" :loading="submitting" :disabled="!testJobId">
            Test Submit Application
          </Button>
        </form>
      </div>

      <!-- Submit Response -->
      <div v-if="submitResponse" class="bg-white rounded-lg shadow-md p-6 mt-6">
        <h2 class="text-xl font-semibold mb-4">Submit Response</h2>
        <pre class="bg-gray-100 p-4 rounded text-sm overflow-auto">{{ JSON.stringify(submitResponse, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { call, Button } from 'frappe-ui'

// State
const testJobId = ref('')
const loading = ref(false)
const submitting = ref(false)
const apiResponse = ref(null)
const submitResponse = ref(null)
const error = ref('')
const fileInput = ref(null)

// Test form data
const testForm = ref({
  full_name: 'Nguyen Van Test',
  email: 'test@example.com',
  phone: '0123456789',
  experience_level: '1-2 năm',
  cover_letter: 'This is a test application.'
})

// Methods
const testGetPublicDetail = async () => {
  if (!testJobId.value) {
    error.value = 'Please enter a Job Opening ID'
    return
  }
  
  loading.value = true
  error.value = ''
  apiResponse.value = null
  
  try {
    const response = await call('mbw_mira.mbw_mira.doctype.jobopening.api.get_public_detail', {
      name: testJobId.value
    })
    
    apiResponse.value = response
  } catch (err) {
    console.error('Error:', err)
    error.value = err.message || 'An error occurred'
  } finally {
    loading.value = false
  }
}

const openJobPage = () => {
  if (testJobId.value) {
    window.open(`/job/${testJobId.value}`, '_blank')
  }
}

const testSubmitApplication = async () => {
  if (!testJobId.value) {
    error.value = 'Please enter a Job Opening ID'
    return
  }
  
  submitting.value = true
  error.value = ''
  submitResponse.value = null
  
  try {
    // Prepare form data
    const formData = new FormData()
    formData.append('job_opening_id', testJobId.value)
    formData.append('full_name', testForm.value.full_name)
    formData.append('email', testForm.value.email)
    formData.append('phone', testForm.value.phone)
    formData.append('experience_level', testForm.value.experience_level)
    formData.append('cover_letter', testForm.value.cover_letter)
    
    // Add file if selected
    if (fileInput.value?.files[0]) {
      formData.append('cv_file', fileInput.value.files[0])
    }
    
    // Submit using fetch
    const response = await fetch('/api/method/mbw_mira.mbw_mira.doctype.jobopening.api.submit_public_application', {
      method: 'POST',
      body: formData
    })
    
    const result = await response.json()
    submitResponse.value = result
    
  } catch (err) {
    console.error('Submit error:', err)
    error.value = err.message || 'An error occurred during submission'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
pre {
  max-height: 400px;
  overflow-y: auto;
}
</style>
