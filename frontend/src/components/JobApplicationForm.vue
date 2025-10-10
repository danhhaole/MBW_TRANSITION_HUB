<template>
  <div class="job-application-form">
    <p class="text-gray-600 mb-6">{{ ('Please fill in the information below') }}</p>
    
    <form @submit.prevent="submitForm" class="space-y-4">
      <!-- Full Name -->
      <div class="form-group">
        <label for="full_name" class="block text-sm font-medium text-gray-700 mb-1">{{ ('Full Name') }} <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="full_name"
          v-model="formData.full_name"
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        >
      </div>

      <!-- Email -->
      <div class="form-group">
        <label for="email" class="block text-sm font-medium text-gray-700 mb-1">{{ ('Email') }}</label>
        <input
          type="email"
          id="email"
          v-model="formData.email"
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          
        >
      </div>

      <!-- Phone -->
      <div class="form-group">
        <label for="phone" class="block text-sm font-medium text-gray-700 mb-1">{{ ('Phone Number') }} <span class="text-red-500">*</span></label>
        <input
          type="tel"
          id="phone"
          v-model="formData.phone"
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        >
      </div>

      <!-- Current Position -->
      <!-- <div class="form-group">
        <label for="current_designation" class="block text-sm font-medium text-gray-700 mb-1">Vị trí hiện tại</label>
        <input
          type="text"
          id="current_designation"
          v-model="formData.current_designation"
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
      </div> -->

      <!-- Current Company -->
      <!-- <div class="form-group">
        <label for="current_company" class="block text-sm font-medium text-gray-700 mb-1">Công ty hiện tại</label>
        <input
          type="text"
          id="current_company"
          v-model="formData.current_company"
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
      </div> -->

      <!-- Years of Experience -->
      <!-- <div class="form-group">
        <label for="experience_years" class="block text-sm font-medium text-gray-700 mb-1">Số năm kinh nghiệm</label>
        <input
          type="number"
          id="experience_years"
          v-model.number="formData.experience_years"
          min="0"
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
      </div> -->

      <!-- Resume Upload -->
      <!-- <div class="form-group">
        <label class="block text-sm font-medium text-gray-700 mb-1">Tải lên CV của bạn</label>
        <div class="mt-1 flex items-center">
          <input
            type="file"
            id="resume"
            ref="resumeInput"
            class="hidden"
            @change="handleFileUpload"
            accept=".pdf,.doc,.docx"
          >
          <button
            type="button"
            @click="$refs.resumeInput.click()"
            class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Chọn tệp
          </button>
          <span class="ml-3 text-sm text-gray-500" v-if="!formData.resume">Chưa có tệp nào được chọn</span>
          <span class="ml-3 text-sm text-gray-700" v-else>{{ formData.resume.name }}</span>
        </div>
        <p class="mt-1 text-xs text-gray-500">Hỗ trợ: PDF, DOC, DOCX (tối đa 5MB)</p>
      </div> -->

      <!-- LinkedIn Profile -->
      <div class="form-group">
        <label for="linkedin_profile" class="block text-sm font-medium text-gray-700 mb-1">{{ ('LinkedIn Profile') }}</label>
        <input
          type="url"
          id="linkedin_profile"
          v-model="formData.linkedin_profile"
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="https://linkedin.com/in/username"
        >
      </div>

      <!-- Notes -->
      <div class="form-group">
        <label for="notes" class="block text-sm font-medium text-gray-700 mb-1">{{ ('Notes') }}</label>
        <textarea
          id="notes"
          v-model="formData.notes"
          rows="3"
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Bạn có thể chia sẻ thêm thông tin về bản thân hoặc câu hỏi cho chúng tôi"
        ></textarea>
      </div>

      <!-- Submit Button -->
      <div class="pt-2">
        <button
          type="submit"
          class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          :disabled="isSubmitting"
        >
          <span v-if="!isSubmitting">{{__('Submit')}}</span>
          <span v-else>{{__('Submitting')}}</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useToast } from '@/composables/useToast'
const toast = useToast()
const emit = defineEmits(['success', 'cancel']);

const isSubmitting = ref(false);
const resumeInput = ref(null);

const formData = reactive({
  full_name: '',
  email: '',
  phone: '',
  current_designation: '',
  current_company: '',
  experience_years: null,
  resume: null,
  linkedin_profile: '',
  notes: ''
});

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    // Check file size (5MB max)
    if (file.size > 5 * 1024 * 1024) {
      alert('Kích thước tệp quá lớn. Vui lòng chọn tệp nhỏ hơn 5MB.');
      return;
    }
    
    // Check file type
    const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!validTypes.includes(file.type)) {
      alert('Vui lòng tải lên tệp PDF hoặc Word (DOC/DOCX)');
      return;
    }
    
    formData.resume = file;
  }
};

const resetForm = () => {
  Object.assign(formData, {
    full_name: '',
    email: '',
    phone: '',
    current_designation: '',
    current_company: '',
    experience_years: null,
    resume: null,
    linkedin_profile: '',
    notes: ''
  });
  
  if (resumeInput.value) {
    resumeInput.value.value = '';
  }
};

const submitForm = async () => {
  try {
    isSubmitting.value = true;
    
    // Basic validation
    if (!formData.full_name || !formData.email || !formData.phone) {
      toast.error('Vui lòng điền đầy đủ các trường bắt buộc');
      return;
    }
    
    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      toast.error('Vui lòng nhập địa chỉ email hợp lệ');
      return;
    }
    
    // Phone number validation (basic)
    const phoneRegex = /^[0-9\-\+]{9,15}$/;
    if (!phoneRegex.test(formData.phone)) {
      toast.error('Vui lòng nhập số điện thoại hợp lệ');
      return;
    }

    // Prepare form data for submission
    const formDataToSubmit = new FormData();
    
    // Add all form fields to FormData
    Object.entries(formData).forEach(([key, value]) => {
      if (value !== null && value !== '') {
        // Handle file upload
        if (key === 'resume' && value instanceof File) {
          formDataToSubmit.append('resume', value, value.name);
        } else {
          formDataToSubmit.append(key, value);
        }
      }
    });

    // Call the API to submit the job application
    const response = await fetch('/api/method/mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.submit_job_application', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
      },
      body: formDataToSubmit
    });

    console.log("response",response);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || 'Failed to submit application');
    }

    const result = await response.json();

    console.log("result",result);
    
    
    if (result.message && result.message.success) {
      toast.success('Đơn ứng tuyển của bạn đã được gửi thành công!');
      resetForm();
      emit('success');
    } else {
      // Try to parse server messages for more detailed error
      let errorMessage = 'Có lỗi xảy ra khi gửi đơn ứng tuyển';
      let serverMessage = null;
      
      if (result._server_messages) {
        try {
          const messages = JSON.parse(result._server_messages);
          if (Array.isArray(messages) && messages.length > 0) {
            const firstMessage = JSON.parse(messages[0]);
            serverMessage = firstMessage.message || errorMessage;
            // Remove HTML tags from the message for cleaner display
            serverMessage = serverMessage.replace(/<[^>]*>?/gm, '');
            console.log("serverMessage",serverMessage);
            
          }
        } catch (e) {
          console.error('Error parsing server messages:', e);
        }
      }
      
      // Use server message if available, otherwise fall back to other error messages
      const displayMessage = serverMessage || result.message?.error || errorMessage;
      
      // Show the error message in toast
      toast.error(displayMessage);
      
      // Also log the full error for debugging
      console.error('Form submission error:', {
        serverMessage,
        message: result.message,
        fullResult: result
      });
    }
    
  } catch (error) {
    console.error('Error submitting form:', error);
    toast.error('Có lỗi xảy ra: ' + (error.message || 'Vui lòng thử lại sau'));
  } finally {
    isSubmitting.value = false;
  }
};

const handleCancel = () => {
  resetForm();
  emit('cancel');
};
</script>

<style scoped>
.job-application-form {
  max-width: 600px;
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

input[type="text"],
input[type="email"],
input[type="tel"],
input[type="number"],
input[type="url"],
textarea,
select {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  line-height: 1.5;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

input:focus,
textarea:focus,
select:focus {
  border-color: #3b82f6;
  outline: none;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

button[type="submit"] {
  display: flex;
  justify-content: center;
  width: 100%;
  padding: 0.75rem 1rem;
  font-weight: 500;
  color: white;
  background-color: #3b82f6;
  border: 1px solid transparent;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.15s ease-in-out;
}

button[type="submit"]:hover {
  background-color: #2563eb;
}

button[type="submit"]:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.text-red-500 {
  color: #ef4444;
}
</style>