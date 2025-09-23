<template>
  <div class="calcom-connection-form space-y-4">
    <!-- Basic Information -->
    <div class="space-y-4">
      <h4 class="font-medium text-gray-900 border-b pb-2">{{__('Basic Information')}}</h4>
      
      <!-- <FormControl 
        :label="__('Tenant Name')"
        v-model="formData.tenant_name"
        :required="true"
        :readonly="isEdit"
        :placeholder="__('Enter tenant name')"
      /> -->
      
      <FormControl 
        :label="__('User Email')"
        type="email"
        v-model="formData.user_email"
        :required="true"
        :readonly="isEdit"
        :placeholder="__('user@company.com')"
      />
      
      <FormControl 
        :label="__('Full Name')"
        v-model="formData.full_name"
        :required="true"
        :placeholder="__('Enter full name')"
      />
    </div>

    <!-- Cal.com Configuration -->
    <div class="space-y-4">
      <h4 class="font-medium text-gray-900 border-b pb-2">{{__('Cal.com Configuration')}}</h4>
      
      <FormControl 
        :label="__('Cal.com Username')"
        v-model="formData.calcom_username"
        :required="true"
        :placeholder="__('your-username')"
        :description="__('Your Cal.com username (e.g., john-doe)')"
      />
      
      <FormControl 
        :label="__('API Key')"
        type="password"
        v-model="formData.api_key"
        :required="true"
        :placeholder="__('Your Cal.com API Key')"
        :description="__('Get this from Cal.com API settings')"
      />
      
      <FormControl 
        :label="__('Cal.com Instance URL')"
        v-model="formData.instance_url"
        :placeholder="__('https://cal.com')"
        :description="__('Leave empty for default Cal.com, or enter your self-hosted URL')"
      />
      
      <FormControl 
        type="select"
        :label="__('Account Type')"
        v-model="formData.account_type"
        :options="accountTypeOptions"
        :required="true"
        :description="__('Type of your Cal.com account')"
      />
    </div>

    <!-- Webhook Configuration -->
    <div class="space-y-4">
      <h4 class="font-medium text-gray-900 border-b pb-2">{{__('Webhook Configuration')}}</h4>
      
      <FormControl 
        :label="__('Hook URL')"
        v-model="formData.hook_url"
        :required="true"
        :placeholder="__('https://your-domain.com/api/webhook/calcom')"
        :description="__('URL to receive Cal.com webhooks')"
      />
      
      <FormControl 
        :label="__('Redirect URL')"
        v-model="formData.redirect_url"
        :required="true"
        :placeholder="__('https://your-domain.com/auth/calcom/callback')"
        :description="__('OAuth redirect URL after authentication')"
      />
      
      <FormControl 
        :label="__('Webhook Secret')"
        v-model="formData.webhook_secret"
        :placeholder="__('Auto-generated if empty')"
        :description="__('Secret for webhook signature verification')"
      />
    </div>

    <!-- Calendar Integration -->
    <div class="space-y-4">
      <h4 class="font-medium text-gray-900 border-b pb-2">{{__('Calendar Integration')}}</h4>
      
      <div class="bg-orange-50 rounded-lg p-3">
        <div class="flex items-center gap-2 mb-2">
          <FeatherIcon name="calendar" class="w-4 h-4 text-orange-600" />
          <span class="text-sm font-medium text-orange-900">{{__('Calendar Sync')}}</span>
        </div>
        <div class="text-xs text-orange-700">
          {{__('Configure how bookings sync with your calendar system')}}
        </div>
      </div>

      <FormControl 
        type="select"
        :label="__('Primary Calendar')"
        v-model="formData.primary_calendar"
        :options="calendarOptions"
        :description="__('Which calendar to use for bookings')"
      />
      
      <FormControl 
        type="checkbox"
        :label="__('Two-way sync')"
        v-model="formData.two_way_sync"
        :description="__('Sync events both from and to Cal.com')"
      />
      
      <FormControl 
        type="number"
        :label="__('Buffer Time (minutes)')"
        v-model="formData.buffer_time"
        :placeholder="__('15')"
        :description="__('Buffer time between bookings')"
      />
    </div>

    <!-- Event Types Management -->
    <div class="space-y-4" v-if="isEdit && existingConnection">
      <h4 class="font-medium text-gray-900 border-b pb-2">{{__('Event Types')}}</h4>
      
      <FormControl 
        type="checkbox"
        :label="__('Auto-sync event types')"
        v-model="formData.auto_sync_event_types"
        :description="__('Automatically sync new event types from Cal.com')"
      />
      
      <FormControl 
        type="select"
        :label="__('Default Event Duration')"
        v-model="formData.default_duration"
        :options="durationOptions"
        :description="__('Default duration for new event types')"
      />
      
      <FormControl 
        type="checkbox"
        :label="__('Allow cancellations')"
        v-model="formData.allow_cancellations"
        :description="__('Allow attendees to cancel bookings')"
      />
    </div>

    <!-- Notification Settings -->
    <div class="space-y-4">
      <h4 class="font-medium text-gray-900 border-b pb-2">{{__('Notification Settings')}}</h4>
      
      <FormControl 
        type="checkbox"
        :label="__('Email notifications')"
        v-model="formData.email_notifications"
        :description="__('Send email notifications for bookings')"
      />
      
      <FormControl 
        type="checkbox"
        :label="__('SMS notifications')"
        v-model="formData.sms_notifications"
        :description="__('Send SMS notifications for bookings')"
      />
      
      <FormControl 
        type="select"
        :label="__('Reminder timing')"
        v-model="formData.reminder_timing"
        :options="reminderOptions"
        :description="__('When to send booking reminders')"
      />
      
      <FormControl 
        :label="__('Custom reminder message')"
        type="textarea"
        v-model="formData.custom_reminder"
        :placeholder="__('Don\'t forget about your upcoming appointment...')"
        :description="__('Custom message for booking reminders')"
      />
    </div>

    <!-- Availability Settings -->
    <div class="space-y-4">
      <h4 class="font-medium text-gray-900 border-b pb-2">{{__('Availability Settings')}}</h4>
      
      <FormControl 
        type="select"
        :label="__('Timezone')"
        v-model="formData.timezone"
        :options="timezoneOptions"
        :description="__('Default timezone for bookings')"
      />
      
      <FormControl 
        type="number"
        :label="__('Booking lead time (hours)')"
        v-model="formData.booking_lead_time"
        :placeholder="__('24')"
        :description="__('Minimum hours in advance for bookings')"
      />
      
      <FormControl 
        type="number"
        :label="__('Max bookings per day')"
        v-model="formData.max_bookings_per_day"
        :placeholder="__('10')"
        :description="__('Maximum number of bookings per day')"
      />
    </div>

    <!-- Integration Settings -->
    <div class="space-y-4">
      <h4 class="font-medium text-gray-900 border-b pb-2">{{__('Integration Settings')}}</h4>
      
      <FormControl 
        type="checkbox"
        :label="__('Create contacts automatically')"
        v-model="formData.auto_create_contacts"
        :description="__('Automatically create contacts for new bookings')"
      />
      
      <FormControl 
        type="select"
        :label="__('Contact source')"
        v-model="formData.contact_source"
        :options="contactSourceOptions"
        :description="__('How to categorize contacts from bookings')"
      />
      
      <FormControl 
        type="checkbox"
        :label="__('Sync booking history')"
        v-model="formData.sync_booking_history"
        :description="__('Import existing booking history')"
      />
    </div>

    <!-- Advanced Settings -->
    <div class="space-y-4">
      <h4 class="font-medium text-gray-900 border-b pb-2">{{__('Advanced Settings')}}</h4>
      
      <FormControl 
        type="select"
        :label="__('Sync Frequency')"
        v-model="formData.sync_frequency"
        :options="syncFrequencyOptions"
        :description="__('How often to sync data from Cal.com')"
      />
      
      <FormControl 
        type="number"
        :label="__('Max Retries')"
        v-model="formData.max_retries"
        :placeholder="__('3')"
        :description="__('Maximum number of retry attempts for failed requests')"
      />
      
      <FormControl 
        type="checkbox"
        :label="__('Enable Debug Mode')"
        v-model="formData.debug_mode"
        :description="__('Enable detailed logging for troubleshooting')"
      />
    </div>

    <!-- Required Permissions -->
    <div class="space-y-4">
      <h4 class="font-medium text-gray-900 border-b pb-2">{{__('Required Permissions')}}</h4>
      
      <div class="grid grid-cols-1 gap-3">
        <div 
          v-for="permission in calcomPermissions" 
          :key="permission.value"
          class="flex items-start gap-2"
        >
          <input 
            type="checkbox" 
            :id="permission.value"
            v-model="formData.permissions"
            :value="permission.value"
            class="mt-1"
          />
          <label :for="permission.value" class="text-sm">
            <div class="font-medium text-gray-900">{{ __(permission.label) }}</div>
            <div class="text-xs text-gray-500">{{ __(permission.description) }}</div>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, computed, onMounted } from 'vue'
import { FormControl, FeatherIcon } from 'frappe-ui'

// Props
const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  },
  platform: {
    type: Object,
    required: true
  },
  isEdit: {
    type: Boolean,
    default: false
  },
  existingConnection: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:modelValue'])

// Form data
const formData = reactive({
  // Basic fields
  tenant_name: '',
  user_email: '',
  full_name: '',
  
  // Cal.com specific
  calcom_username: '',
  api_key: '',
  instance_url: 'https://cal.com',
  account_type: 'personal',
  
  // Webhook
  hook_url: '',
  redirect_url: '',
  webhook_secret: '',
  
  // Calendar
  primary_calendar: 'google',
  two_way_sync: true,
  buffer_time: 15,
  
  // Event types
  auto_sync_event_types: true,
  default_duration: 30,
  allow_cancellations: true,
  
  // Notifications
  email_notifications: true,
  sms_notifications: false,
  reminder_timing: '24h',
  custom_reminder: '',
  
  // Availability
  timezone: 'Asia/Ho_Chi_Minh',
  booking_lead_time: 24,
  max_bookings_per_day: 10,
  
  // Integration
  auto_create_contacts: true,
  contact_source: 'booking',
  sync_booking_history: false,
  
  // Settings
  sync_frequency: 'hourly',
  max_retries: 3,
  debug_mode: false,
  permissions: ['bookings', 'event_types', 'availability']
})

// Options
const accountTypeOptions = [
  { label: __('Personal Account'), value: 'personal' },
  { label: __('Team Account'), value: 'team' },
  { label: __('Organization'), value: 'organization' }
]

const calendarOptions = [
  { label: __('Google Calendar'), value: 'google' },
  { label: __('Outlook Calendar'), value: 'outlook' },
  { label: __('Apple Calendar'), value: 'apple' },
  { label: __('CalDAV'), value: 'caldav' }
]

const durationOptions = [
  { label: __('15 minutes'), value: 15 },
  { label: __('30 minutes'), value: 30 },
  { label: __('45 minutes'), value: 45 },
  { label: __('1 hour'), value: 60 },
  { label: __('1.5 hours'), value: 90 },
  { label: __('2 hours'), value: 120 }
]

const reminderOptions = [
  { label: __('1 hour before'), value: '1h' },
  { label: __('24 hours before'), value: '24h' },
  { label: __('48 hours before'), value: '48h' },
  { label: __('1 week before'), value: '1w' }
]

const timezoneOptions = [
  { label: __('Ho Chi Minh City (GMT+7)'), value: 'Asia/Ho_Chi_Minh' },
  { label: __('Bangkok (GMT+7)'), value: 'Asia/Bangkok' },
  { label: __('Singapore (GMT+8)'), value: 'Asia/Singapore' },
  { label: __('Tokyo (GMT+9)'), value: 'Asia/Tokyo' },
  { label: __('UTC'), value: 'UTC' }
]

const contactSourceOptions = [
  { label: __('Calendar Booking'), value: 'booking' },
  { label: __('Calendar Integration'), value: 'calendar' },
  { label: __('Scheduling'), value: 'scheduling' }
]

const syncFrequencyOptions = [
  { label: __('Every 5 minutes'), value: '5min' },
  { label: __('Every 15 minutes'), value: '15min' },
  { label: __('Every 30 minutes'), value: '30min' },
  { label: __('Every hour'), value: 'hourly' },
  { label: __('Every 6 hours'), value: '6hourly' },
  { label: __('Daily'), value: 'daily' }
]

const calcomPermissions = [
  {
    label: __('Bookings'),
    value: 'bookings',
    description: __('Access and manage bookings')
  },
  {
    label: __('Event Types'),
    value: 'event_types',
    description: __('Access and manage event types')
  },
  {
    label: __('Availability'),
    value: 'availability',
    description: __('Access availability information')
  },
  {
    label: __('Calendar Integration'),
    value: 'calendar',
    description: __('Connect and sync with calendars')
  },
  {
    label: __('Webhooks'),
    value: 'webhooks',
    description: __('Receive webhook notifications')
  },
  {
    label: __('User Profile'),
    value: 'profile',
    description: __('Access user profile information')
  }
]

// Watchers
watch(formData, (newValue) => {
  emit('update:modelValue', { ...newValue })
}, { deep: true })

watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    Object.assign(formData, newValue)
  }
}, { deep: true, immediate: true })

// Initialize form data for edit mode
onMounted(() => {
  if (props.isEdit && props.existingConnection) {
    // Populate form with existing connection data
    Object.assign(formData, {
      tenant_name: props.existingConnection.tenant_name || '',
      user_email: props.existingConnection.user_email || '',
      full_name: props.existingConnection.full_name || '',
      hook_url: props.existingConnection.hook_url || '',
      redirect_url: props.existingConnection.redirect_url || '',
      sync_frequency: props.existingConnection.sync_frequency || 'hourly',
      max_retries: props.existingConnection.max_retries || 3,
      // Parse settings if stored as JSON
      ...parseSettings(props.existingConnection.settings)
    })
  }
})

// Helper function to parse settings
function parseSettings(settings) {
  try {
    return typeof settings === 'string' ? JSON.parse(settings) : settings || {}
  } catch (e) {
    return {}
  }
}
</script>

<style scoped>
.calcom-connection-form {
  max-height: 60vh;
  overflow-y: auto;
  padding-right: 8px;
}

/* Custom scrollbar */
.calcom-connection-form::-webkit-scrollbar {
  width: 6px;
}

.calcom-connection-form::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.calcom-connection-form::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.calcom-connection-form::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>