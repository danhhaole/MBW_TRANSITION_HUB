<template>
    <div class="bg-gray-50 min-h-screen p-4 lg:p-8">
      <LayoutHeader>
        <template #left-header>
          <Breadcrumbs :items="breadcrumbs" />
        </template>
      </LayoutHeader>
      <div class="flex flex-col lg:flex-row gap-6 w-full">
        <!-- LEFT: Candidate Info -->
        <div class="bg-white rounded-2xl shadow p-6 w-full lg:w-1/3 h-fit relative">
          <!-- Source Badge -->
          <div v-if="data.source" class="absolute top-4 left-6">
            <span class="px-3 py-1 bg-blue-100 text-blue-700 text-xs font-medium rounded">
              {{ data.source }}
            </span>
          </div>
          
          <!-- Edit Button -->
          <button 
            @click="openEditDialog"
            class="absolute top-4 right-4 p-2 rounded-full hover:bg-gray-100 text-gray-500 hover:text-gray-700 transition-colors"
            :title="__('Edit')"
          >
            <i class="ti ti-pencil"></i>
          </button>
          
          <!-- Avatar -->
          <div class="flex flex-col items-center text-center">
            <Avatar
              :label="data.full_name"
              :title="data.full_name"
              size="3xl"
              class="w-20 h-20 text-3xl font-semibold"
            />
            <h2 class="mt-4 text-lg font-semibold text-gray-800">
              {{ data.full_name || 'N/A' }}
            </h2>
            <p class="text-sm text-gray-500" v-if="data.title">
              {{ data.title }}
            </p>
          </div>
  
          <!-- Contact -->
          <div class="mt-6 border-t">
            <h3 class="text-sm font-semibold text-gray-700 my-3">
              THÔNG TIN LIÊN HỆ
            </h3>
            <ul class="text-sm text-gray-600 space-y-2">
              <li class="flex items-center gap-2" v-if="data.email">
                <i class="ti ti-mail text-gray-500"></i>
                <a :href="'mailto:' + data.email" class="hover:text-blue-600">
                  {{ data.email }}
                </a>
              </li>
              <li class="flex items-center gap-2" v-if="data.phone">
                <i class="ti ti-phone text-gray-500"></i>
                <a :href="'tel:' + data.phone" class="hover:text-blue-600">
                  {{ data.phone }}
                </a>
              </li>
              <li class="flex items-center gap-2" v-if="data.linkedin_profile">
                <i class="ti ti-brand-linkedin text-gray-500"></i>
                <a :href="data.linkedin_profile" target="_blank" class="hover:text-blue-600">
                  LinkedIn
                </a>
              </li>
              <li class="flex items-center gap-2" v-if="data.facebook_profile">
                <i class="ti ti-brand-facebook text-gray-500"></i>
                <a :href="data.facebook_profile" target="_blank" class="hover:text-blue-600">
                  Facebook
                </a>
              </li>
              <!-- <li class="flex items-center gap-2" v-if="data.zalo_profile">
                <i class="ti ti-brand-zalo text-gray-500"></i>
                <a :href="data.zalo_profile" target="_blank" class="hover:text-blue-600">
                  Zalo
                </a>
              </li> -->
            </ul>
          </div>
  
          <!-- Skills -->
          <div class="mt-6 border-t" v-if="data.skills">
            <h3 class="text-sm font-semibold text-gray-700 my-3">KỸ NĂNG</h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="(skill, index) in data.skills.split(',').map(s => s.trim())"
                :key="index"
                class="px-3 py-1 bg-purple-100 text-purple-700 text-xs font-medium rounded"
              >
                {{ skill }}
              </span>
            </div>
          </div>
  
          <!-- Summary -->
          <div class="mt-6 border-t" v-if="true">
            <h3 class="text-sm font-semibold text-gray-700 my-3">AI TÓM TẮT</h3>
            <p class="text-sm text-gray-600 leading-relaxed">
              <!-- AI Summary content will go here -->
                Ứng viên có hồ sơ nổi bật với nền tảng chuyên môn vững chắc và kinh nghiệm làm việc phù hợp với yêu cầu vị trí. Thông tin cá nhân, học vấn và kỹ năng được trình bày rõ ràng, thể hiện sự nghiêm túc và đầu tư trong quá trình ứng tuyển. Ứng viên có khả năng giao tiếp tốt, tư duy logic, và thái độ tích cực trong công việc. Hồ sơ thể hiện tiềm năng phát triển lâu dài và khả năng thích nghi nhanh với môi trường mới. Đây là một hồ sơ tiềm năng, nên được ưu tiên xem xét ở các vòng tuyển chọn tiếp theo.
            </p>
          </div>
        </div>
  
        <!-- RIGHT: Interaction Journey -->
        <div class="bg-white rounded-2xl shadow p-6 flex-1 h-fit">
          <h3 class="text-base font-semibold text-gray-800 mb-2">
            Hành trình Tương tác
          </h3>
          <!-- <p class="text-sm text-gray-500 mb-6">
            Chiến dịch:
            <span class="font-medium">Nuôi dưỡng ứng viên React Quý 4/2025</span>
          </p> -->
  
          <div v-if="!data.interactions.length" class="text-center py-8 text-gray-500">
            <p>Chưa có tương tác nào được ghi nhận.</p>
          </div>
          
          <div v-else class="space-y-8 relative">
            <!-- Timeline Line -->
            <div class="absolute left-4 top-0 bottom-0 w-px bg-gray-200"></div>
            
            <!-- Interaction Items -->
            <div v-for="(interaction, index) in data.interactions" :key="interaction.name" class="relative pl-10">
              <!-- Interaction Icon -->
              <div 
                class="absolute left-0 top-1 w-8 h-8 text-white rounded-full flex items-center justify-center"
                :class="getInteractionIcon(interaction).bgColor"
              >
                <i :class="getInteractionIcon(interaction).icon"></i>
              </div>
              
              <!-- Interaction Header -->
              <div class="flex justify-between items-start">
                <h4 class="font-semibold text-gray-800">
                  {{ getInteractionTitle(interaction) }}
                </h4>
                <span 
                  class="text-xs px-2 py-0.5 rounded-full"
                  :class="getStatusBadgeClass(interaction.action_status)"
                >
                  {{ getStatusText(interaction.action_status) }}
                </span>
              </div>
              
              <p class="text-xs text-gray-500 mb-1">
                {{ interaction.creation }}
                <span v-if="interaction.scheduled_at" class="ml-2">
                  • Dự kiến: {{ interaction.scheduled_at }}
                </span>
              </p>
              
              <p v-if="interaction.description" class="text-sm text-gray-600 mt-1">
                {{ interaction.description }}
              </p>
              
              <!-- Action Details -->
              <div v-if="interaction.action_status" class="mt-2">
                <p class="text-xs text-gray-500">
                  <span v-if="interaction.campaign_step">Bước chiến dịch: {{ interaction.campaign_step }}</span>
                </p>
                <p v-if="interaction.executed_at" class="text-xs text-gray-500">
                  Thực hiện lúc: {{ interaction.executed_at }}
                </p>
              </div>
              
              <!-- Action Buttons for Pending Actions -->
              <div v-if="interaction.action_status === 'PENDING_MANUAL'" class="mt-3">
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="action in getAvailableActions(interaction)"
                    :key="action.value"
                    class="px-3 py-1 text-xs rounded-full"
                    :class="action.class"
                    @click="handleAction(interaction, action.value)"
                  >
                    {{ action.label }}
                  </button>
                </div>
              </div>
            </div>
            <!-- <div class="relative pl-10">
              <div
                class="absolute left-0 top-1 w-8 h-8 bg-gray-600 text-white rounded-full flex items-center justify-center"
              >
                <i class="ti ti-send"></i>
              </div>
              <h4 class="font-semibold text-gray-800">Gửi Email Follow-up</h4>
              <p class="text-xs text-gray-500 mb-1">27/06/2025</p>
              <p class="text-sm text-gray-600">
                Hệ thống được lên lịch gửi email thứ hai nếu không có phản hồi sau
                cuộc gọi.
              </p>
            </div> -->
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Dialog -->
    <Dialog v-model="showEditDialog" :options="{
      title: __('Edit Talent'),
      size: '2xl'
    }">

      <template #body-content>
        <div class="space-y-4">
          <FormControl
            :label="__('Full Name')"
            v-model="editData.full_name"
            :required="true"
          />

          <FormControl
            :label="__('Email')"
            v-model="editData.email"
            type="email"
            :required="true"
          />
          
          <FormControl
            :label="__('Phone')"
            v-model="editData.phone"
            type="tel"
          />
          
          <FormControl
            :label="__('Linkin')"
            v-model="editData.linkedin_profile"
            type="url"
            :placeholder="__('https://linkedin.com/in/...')"
          >
            <template #prefix>
              <i class="ti ti-brand-linkedin text-gray-400"></i>
            </template>
          </FormControl>
          
          <FormControl
            :label="__('Facebook')"
            v-model="editData.facebook_profile"
            type="url"
            :placeholder="__('https://facebook.com/...')"
          >
            <template #prefix>
              <i class="ti ti-brand-facebook text-gray-400"></i>
            </template>
          </FormControl>
          
          <FormControl
            :label="__('Skills (separated by commas)')"
            v-model="editData.skills"
            as="textarea"
            rows="2"
            :placeholder="__('Example: React, Node.js, JavaScript')"
          />
        </div>
      </template>
      
      <template #actions>
        <div class="flex justify-end space-x-3">
          <Button variant="ghost" @click="showEditDialog = false">
            Hủy
          </Button>
          <Button variant="solid" @click="saveChanges">
            Lưu thay đổi
          </Button>
        </div>
      </template>
    </Dialog>
  </template>
  
<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Breadcrumbs, Avatar, Dialog, Input, FormControl, call } from 'frappe-ui'
import { useRouter } from 'vue-router'
import { useTalentPoolStore } from '@/stores/talentPool'
import { ref, reactive, onMounted, nextTick } from 'vue'
import { useToast } from '@/composables/useToast'


const talentPoolStore = useTalentPoolStore()
const route = useRouter()
const toast = useToast()
const data = reactive({
  // Talent Pool info
  talent_pool_id: null,
  talent_id: null,
  contact_id: null,
  
  // Talent details
  full_name: '',
  email: '',
  phone: '',
  skills: '',
  source: '',
  linkedin_profile: '',
  facebook_profile: '',
  zalo_profile: '',
  
  // Interactions
  interactions: [],
  
  // Other fields that might be used in the template
  title: '',
  contact_email: '',
  contact_phone: ''
})
const showEditDialog = ref(false)
const editData = reactive({})
const editForm = ref(null)
let title = __('Talent Pools Details')
const breadcrumbs = [{ label: title, route: { name: 'TalentPoolDetail' } }]

// Helper methods for interactions
const getInteractionIcon = (interaction) => {
  const types = {
    // Email interactions
    'EMAIL_DRAFT': { icon: 'ti ti-mail', bgColor: 'bg-gray-400' },
    'EMAIL_SENT': { icon: 'ti ti-send', bgColor: 'bg-blue-500' },
    'EMAIL_DELIVERED': { icon: 'ti ti-mail-check', bgColor: 'bg-blue-400' },
    'EMAIL_OPENED': { icon: 'ti ti-eye', bgColor: 'bg-green-500' },
    'EMAIL_CLICKED': { icon: 'ti ti-cursor-click', bgColor: 'bg-purple-500' },
    'EMAIL_BOUNCED': { icon: 'ti ti-mail-x', bgColor: 'bg-red-500' },
    'EMAIL_UNSUBSCRIBED': { icon: 'ti ti-bell-off', bgColor: 'bg-gray-500' },
    'EMAIL_REPLIED': { icon: 'ti ti-arrow-back-up', bgColor: 'bg-teal-500' },
    'EMAIL_FORWARDED': { icon: 'ti ti-arrow-forward-up', bgColor: 'bg-indigo-500' },
    'EMAIL_SCHEDULED': { icon: 'ti ti-clock', bgColor: 'bg-yellow-500' },
    'EMAIL_FAILED': { icon: 'ti ti-alert-circle', bgColor: 'bg-red-600' },
    
    // Website interactions
    'PAGE_VISITED': { icon: 'ti ti-device-desktop', bgColor: 'bg-indigo-500' },
    'FORM_SUBMITTED': { icon: 'ti ti-forms', bgColor: 'bg-purple-500' },
    'DOWNLOAD_TRIGGERED': { icon: 'ti ti-download', bgColor: 'bg-blue-500' },
    'LINK_CLICKED': { icon: 'ti ti-link', bgColor: 'bg-blue-400' },
    'BUTTON_CLICKED': { icon: 'ti ti-hand-click', bgColor: 'bg-blue-300' },
    'SCROLL_DEPTH': { icon: 'ti ti-arrow-down', bgColor: 'bg-indigo-400' },
    'TIME_ON_PAGE': { icon: 'ti ti-clock-hour-4', bgColor: 'bg-indigo-300' },
    'EXIT_INTENT': { icon: 'ti ti-arrow-bar-to-right', bgColor: 'bg-red-400' },
    'PAGE_NAVIGATION': { icon: 'ti ti-route', bgColor: 'bg-blue-200' },
    
    // Chat interactions
    'CHAT_STARTED': { icon: 'ti ti-messages', bgColor: 'bg-green-500' },
    'CHAT_MESSAGE_SENT': { icon: 'ti ti-message', bgColor: 'bg-green-400' },
    'CHAT_MESSAGE_RECEIVED': { icon: 'ti ti-message-2', bgColor: 'bg-blue-400' },
    'CHAT_COMPLETED': { icon: 'ti ti-message-off', bgColor: 'bg-gray-500' },
    'CHAT_TRANSFERRED': { icon: 'ti ti-arrow-forward-up', bgColor: 'bg-orange-400' },
    'CHAT_RATING': { icon: 'ti ti-star', bgColor: 'bg-yellow-500' },
    'CHAT_FILE_UPLOAD': { icon: 'ti ti-upload', bgColor: 'bg-blue-300' },
    'CHAT_ATTACHMENT_VIEWED': { icon: 'ti ti-file-text', bgColor: 'bg-blue-200' },
    'CHAT_QUEUE_ENTERED': { icon: 'ti ti-hourglass', bgColor: 'bg-yellow-400' },
    'CHAT_QUEUE_EXITED': { icon: 'ti ti-hourglass-high', bgColor: 'bg-green-400' },
    
    // Call interactions
    'CALL_INITIATED': { icon: 'ti ti-phone-outgoing', bgColor: 'bg-green-400' },
    'CALL_RECEIVED': { icon: 'ti ti-phone-incoming', bgColor: 'bg-blue-400' },
    'CALL_MISSED': { icon: 'ti ti-phone-missed', bgColor: 'bg-red-500' },
    'CALL_COMPLETED': { icon: 'ti ti-phone-call', bgColor: 'bg-green-500' },
    'CALL_RECORDING_AVAILABLE': { icon: 'ti ti-microphone', bgColor: 'bg-purple-400' },
    'CALL_TRANSCRIPT_AVAILABLE': { icon: 'ti ti-notes', bgColor: 'bg-indigo-400' },
    'CALL_QUEUED': { icon: 'ti ti-phone-plus', bgColor: 'bg-yellow-500' },
    'CALL_TRANSFERRED': { icon: 'ti ti-arrow-forward-up', bgColor: 'bg-orange-400' },
    'CALL_HOLD': { icon: 'ti ti-player-pause', bgColor: 'bg-gray-400' },
    'CALL_RESUMED': { icon: 'ti ti-player-play', bgColor: 'bg-green-400' },
    
    // SMS interactions
    'SMS_DRAFT': { icon: 'ti ti-message-2', bgColor: 'bg-gray-400' },
    'SMS_SENT': { icon: 'ti ti-send', bgColor: 'bg-blue-500' },
    'SMS_DELIVERED': { icon: 'ti ti-message-check', bgColor: 'bg-green-500' },
    'SMS_READ': { icon: 'ti ti-eye', bgColor: 'bg-green-600' },
    'SMS_REPLIED': { icon: 'ti ti-message-reply', bgColor: 'bg-teal-500' },
    'SMS_FAILED': { icon: 'ti ti-alert-circle', bgColor: 'bg-red-600' },
    'SMS_SCHEDULED': { icon: 'ti ti-clock', bgColor: 'bg-yellow-500' },
    'SMS_OPT_IN': { icon: 'ti ti-check', bgColor: 'bg-green-500' },
    'SMS_OPT_OUT': { icon: 'ti ti-x', bgColor: 'bg-red-500' },
    'SMS_KEYWORD': { icon: 'ti ti-hash', bgColor: 'bg-purple-500' },
    
    // Application interactions
    'APPLICATION_STARTED': { icon: 'ti ti-file-text', bgColor: 'bg-amber-400' },
    'APPLICATION_SUBMITTED': { icon: 'ti ti-file-check', bgColor: 'bg-amber-500' },
    'APPLICATION_REVIEWED': { icon: 'ti ti-file-search', bgColor: 'bg-blue-500' },
    'APPLICATION_APPROVED': { icon: 'ti ti-check', bgColor: 'bg-green-500' },
    'APPLICATION_REJECTED': { icon: 'ti ti-x', bgColor: 'bg-red-500' },
    'APPLICATION_ON_HOLD': { icon: 'ti ti-hourglass', bgColor: 'bg-yellow-500' },
    'APPLICATION_WITHDRAWN': { icon: 'ti ti-arrow-back', bgColor: 'bg-gray-500' },
    'APPLICATION_UPDATED': { icon: 'ti ti-refresh', bgColor: 'bg-blue-400' },
    'APPLICATION_EXPIRED': { icon: 'ti ti-clock-off', bgColor: 'bg-gray-500' },
    'APPLICATION_ARCHIVED': { icon: 'ti ti-archive', bgColor: 'bg-gray-600' },
    
    // Document interactions
    'DOCUMENT_UPLOADED': { icon: 'ti ti-upload', bgColor: 'bg-amber-400' },
    'DOCUMENT_VIEWED': { icon: 'ti ti-file-text', bgColor: 'bg-blue-400' },
    'DOCUMENT_DOWNLOADED': { icon: 'ti ti-download', bgColor: 'bg-blue-500' },
    'DOCUMENT_SIGNED': { icon: 'ti ti-signature', bgColor: 'bg-green-500' },
    'DOCUMENT_EXPIRED': { icon: 'ti ti-clock-off', bgColor: 'bg-red-500' },
    'DOCUMENT_REJECTED': { icon: 'ti ti-x', bgColor: 'bg-red-600' },
    'DOCUMENT_APPROVED': { icon: 'ti ti-check', bgColor: 'bg-green-600' },
    'DOCUMENT_COMMENT_ADDED': { icon: 'ti ti-message-circle', bgColor: 'bg-blue-300' },
    'DOCUMENT_VERSION_UPDATED': { icon: 'ti ti-versions', bgColor: 'bg-purple-400' },
    'DOCUMENT_DELETED': { icon: 'ti ti-trash', bgColor: 'bg-red-400' },
    
    // Test interactions
    'TEST_INVITED': { icon: 'ti ti-clipboard-list', bgColor: 'bg-purple-400' },
    'TEST_STARTED': { icon: 'ti ti-clipboard-text', bgColor: 'bg-purple-500' },
    'TEST_COMPLETED': { icon: 'ti ti-clipboard-check', bgColor: 'bg-green-500' },
    'TEST_PASSED': { icon: 'ti ti-check', bgColor: 'bg-green-600' },
    'TEST_FAILED': { icon: 'ti ti-x', bgColor: 'bg-red-500' },
    'TEST_REVIEWED': { icon: 'ti ti-clipboard-plus', bgColor: 'bg-blue-500' },
    'TEST_RETAKEN': { icon: 'ti ti-reload', bgColor: 'bg-orange-500' },
    'TEST_EXPIRED': { icon: 'ti ti-clock-off', bgColor: 'bg-gray-500' },
    'TEST_QUESTION_ANSWERED': { icon: 'ti ti-message-circle', bgColor: 'bg-blue-400' },
    'TEST_TIME_UPDATED': { icon: 'ti ti-clock-plus', bgColor: 'bg-yellow-500' },
    
    // Interview interactions
    'INTERVIEW_SCHEDULED': { icon: 'ti ti-calendar', bgColor: 'bg-blue-500' },
    'INTERVIEW_CONFIRMED': { icon: 'ti ti-calendar-check', bgColor: 'bg-green-500' },
    'INTERVIEW_RESCHEDULED': { icon: 'ti ti-calendar-time', bgColor: 'bg-yellow-500' },
    'INTERVIEW_CANCELLED': { icon: 'ti ti-calendar-off', bgColor: 'bg-red-500' },
    'INTERVIEW_COMPLETED': { icon: 'ti ti-check', bgColor: 'bg-green-600' },
    'INTERVIEW_NO_SHOW': { icon: 'ti ti-user-off', bgColor: 'bg-red-600' },
    'INTERVIEW_FEEDBACK_SUBMITTED': { icon: 'ti ti-message-circle', bgColor: 'bg-blue-400' },
    'INTERVIEW_RECORDING_AVAILABLE': { icon: 'ti ti-video', bgColor: 'bg-purple-500' },
    'INTERVIEW_REMINDER_SENT': { icon: 'ti ti-bell', bgColor: 'bg-yellow-400' },
    'INTERVIEW_INVITATION_SENT': { icon: 'ti ti-send', bgColor: 'bg-blue-400' },
    
    // Meeting interactions
    'MEETING_SCHEDULED': { icon: 'ti ti-calendar', bgColor: 'bg-blue-500' },
    'MEETING_STARTED': { icon: 'ti ti-video', bgColor: 'bg-green-500' },
    'MEETING_ENDED': { icon: 'ti ti-phone-off', bgColor: 'bg-gray-500' },
    'MEETING_JOINED': { icon: 'ti ti-user-plus', bgColor: 'bg-green-400' },
    'MEETING_LEFT': { icon: 'ti ti-user-minus', bgColor: 'bg-red-400' },
    'MEETING_RECORDING_AVAILABLE': { icon: 'ti ti-video', bgColor: 'bg-purple-500' },
    'MEETING_CHAT_MESSAGE': { icon: 'ti ti-message', bgColor: 'bg-blue-300' },
    'MEETING_POLL_CREATED': { icon: 'ti ti-chart-bar', bgColor: 'bg-indigo-400' },
    'MEETING_POLL_VOTED': { icon: 'ti ti-checkbox', bgColor: 'bg-green-400' },
    'MEETING_WHITEBOARD_STARTED': { icon: 'ti ti-palette', bgColor: 'bg-yellow-400' },
    
    // Default fallback
    'DEFAULT': { icon: 'ti ti-circle', bgColor: 'bg-gray-400' }
  };
  
  return types[interaction.interaction_type] || types['DEFAULT'];
};

const getInteractionTitle = (interaction) => {
  const titles = {
    // Email interactions
    'EMAIL_SENT': 'Đã gửi email',
    'EMAIL_DELIVERED': 'Email đã được gửi thành công',
    'EMAIL_OPENED': 'Đã mở email',
    'EMAIL_CLICKED': 'Đã nhấp vào liên kết trong email',
    'EMAIL_BOUNCED': 'Email bị trả lại',
    'EMAIL_UNSUBSCRIBED': 'Đã hủy đăng ký nhận email',
    'EMAIL_REPLIED': 'Đã trả lời email',
    
    // Website interactions
    'PAGE_VISITED': 'Đã truy cập trang',
    'FORM_SUBMITTED': 'Đã gửi biểu mẫu',
    'DOWNLOAD_TRIGGERED': 'Đã tải xuống tài liệu',
    
    // Chat interactions
    'CHAT_STARTED': 'Đã bắt đầu trò chuyện',
    'CHAT_MESSAGE_SENT': 'Đã gửi tin nhắn',
    'CHAT_COMPLETED': 'Đã kết thúc trò chuyện',
    
    // Call interactions
    'CALL_MISSED': 'Nhỡ cuộc gọi',
    'CALL_COMPLETED': 'Đã hoàn thành cuộc gọi',
    
    // SMS interactions
    'SMS_SENT': 'Đã gửi SMS',
    'SMS_DELIVERED': 'Đã gửi SMS thành công',
    'SMS_REPLIED': 'Đã phản hồi SMS',
    
    // Application interactions
    'APPLICATION_SUBMITTED': 'Đã nộp hồ sơ',
    'DOCUMENT_UPLOADED': 'Đã tải lên tài liệu',
    
    // Test interactions
    'TEST_STARTED': 'Đã bắt đầu bài kiểm tra',
    'TEST_COMPLETED': 'Đã hoàn thành bài kiểm tra',
    
    // Interview interactions
    'INTERVIEW_CONFIRMED': 'Đã xác nhận lịch phỏng vấn',
    'INTERVIEW_RESCHEDULED': 'Đã dời lịch phỏng vấn',
  };
  
  return titles[interaction.interaction_type] || interaction.interaction_type;
};

const getStatusBadgeClass = (status) => {
  const classes = {
    'PENDING_MANUAL': 'bg-yellow-100 text-yellow-800',
    'SCHEDULED': 'bg-blue-100 text-blue-800',
    'EXECUTED': 'bg-green-100 text-green-800',
    'COMPLETED': 'bg-green-100 text-green-800',
    'FAILED': 'bg-red-100 text-red-800',
    'CANCELLED': 'bg-gray-100 text-gray-800',
  };
  return classes[status] || 'bg-gray-100 text-gray-800';
};

const getStatusText = (status) => {
  const texts = {
    'PENDING_MANUAL': 'Chờ xử lý',
    'SCHEDULED': 'Đã lên lịch',
    'EXECUTED': 'Đã thực hiện',
    'COMPLETED': 'Hoàn thành',
    'FAILED': 'Thất bại',
    'CANCELLED': 'Đã hủy',
  };
  return texts[status] || status;
};

const getAvailableActions = (interaction) => {
  // Define available actions based on interaction type and status
  const actions = [
    { value: 'complete', label: 'Hoàn thành', class: 'bg-green-100 text-green-800 hover:bg-green-200' },
    { value: 'reschedule', label: 'Lên lịch lại', class: 'bg-blue-100 text-blue-800 hover:bg-blue-200' },
    { value: 'cancel', label: 'Hủy', class: 'bg-red-100 text-red-800 hover:bg-red-200' },
  ];
  return actions;
};

const handleAction = async (interaction, action) => {
  try {
    // Here you would typically make an API call to update the action status
    console.log(`Action '${action}' triggered for interaction:`, interaction);
    
    // Example API call (uncomment and implement as needed):
    // await call('your_module.your_doctype.doctype.your_doctype.update_action_status', {
    //   action_id: interaction.action,
    //   status: action.toUpperCase()
    // });
    
    toast.success(`Đã cập nhật trạng thái thành: ${action}`);
    
    // Refresh the interactions data
    const res = await talentPoolStore.getTalentInteractions(data.talent_pool_id);
    if (res && res.interactions) {
      data.interactions = res.interactions;
    }
  } catch (error) {
    console.error('Error updating action status:', error);
    toast.error('Có lỗi xảy ra khi cập nhật trạng thái');
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const options = { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  };
  return new Date(dateString).toLocaleString('vi-VN', options);
};

const openEditDialog = () => {
  Object.assign(editData, JSON.parse(JSON.stringify(data)))
  showEditDialog.value = true
  // Focus the first input field when dialog opens
  nextTick(() => {
    if (editForm.value) {
      console.log("editForm.value", editForm.value);
      const firstInput = editForm.value.querySelector('input')
      if (firstInput) firstInput.focus()
    }
  })
}

const saveChanges = async () => {
  try {
    // Update the Talent record instead of Talent Pool
    await call('frappe.client.set_value', {
      doctype: 'Mira Talent',
      name: data.talent_id, // Assuming talent_id is available in the data
      fieldname: {
        full_name: editData.full_name,
        email: editData.email,
        phone: editData.phone,
        linkedin_profile: editData.linkedin_profile,
        facebook_profile: editData.facebook_profile,
        zalo_profile: editData.zalo_profile,
        // Add other talent fields as needed
      }
    });
    
    // Also update the local data
    Object.assign(data, editData);
    showEditDialog.value = false;
    toast.success('Đã cập nhật thông tin ứng viên');
  } catch (error) {
    console.error('Error updating talent:', error);
    toast.error('Có lỗi xảy ra khi cập nhật thông tin');
  }
}

onMounted(async () => {
  try {
    const id = route.currentRoute.value.params.id
    if (id) {
      const res = await talentPoolStore.getTalentInteractions(id)
      
      // Map the API response to the component's data structure
      if (res) {
        // Update talent pool data
        data.talent_pool_id = res.talent_pool;
        data.talent_id = res.talent.id;
        data.contact_id = res.contact_id;
        
        // Update talent details
        Object.assign(data, res.talent);
        
        // Format interactions data if needed
        if (res.interactions && Array.isArray(res.interactions)) {
          data.interactions = res.interactions.map(interaction => ({
            ...interaction,
            creation: formatDate(interaction.creation),
            scheduled_at: interaction.scheduled_at ? formatDate(interaction.scheduled_at) : null,
            executed_at: interaction.executed_at ? formatDate(interaction.executed_at) : null
          }));
        }
        
        console.log('Talent data loaded:', data);
      }
    }
  } catch (error) {
    console.error('Error fetching talent pool details:', error);
    toast.error('Không thể tải thông tin ứng viên');
  }
})

</script>
  
<style scoped>
@import "https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css";
</style>
  