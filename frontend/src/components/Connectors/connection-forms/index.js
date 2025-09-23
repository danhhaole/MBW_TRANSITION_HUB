// connection-forms/index.js
// Central file để import và export tất cả form components

import FacebookConnectionForm from '@/components/Connectors/FacebookConnectionForm.vue'
import ZaloConnectionForm from '@/components/Connectors/ZaloConnectionForm.vue'
import CalcomConnectionForm from '@/components/Connectors/CalcomConnectionForm.vue'
import TopcvConnectionForm from '@/components/Connectors/TopcvConnectionForm.vue'

// Export components
export {
  FacebookConnectionForm,
  ZaloConnectionForm,
  CalcomConnectionForm,
  TopcvConnectionForm
}

// Component mapping for dynamic loading
export const connectionFormComponents = {
  facebook: FacebookConnectionForm,
  zalo: ZaloConnectionForm,
  cal_com: CalcomConnectionForm,
  topcv: TopcvConnectionForm
}

// Helper function to get component by platform ID
export const getConnectionFormComponent = (platformId) => {
  return connectionFormComponents[platformId] || FacebookConnectionForm
}

// Platform-specific form validation rules
export const formValidationRules = {
  facebook: {
    required: ['tenant_name', 'user_email', 'full_name', 'app_id', 'app_secret', 'hook_url', 'redirect_url'],
    email: ['user_email'],
    url: ['hook_url', 'redirect_url']
  },
  zalo: {
    required: ['tenant_name', 'user_email', 'full_name', 'oa_id', 'app_id', 'app_secret', 'hook_url', 'redirect_url'],
    email: ['user_email'],
    url: ['hook_url', 'redirect_url']
  },
  cal_com: {
    required: ['tenant_name', 'user_email', 'full_name', 'calcom_username', 'api_key', 'hook_url', 'redirect_url'],
    email: ['user_email'],
    url: ['hook_url', 'redirect_url', 'instance_url']
  },
  topcv: {
    required: ['tenant_name', 'user_email', 'full_name', 'company_id', 'api_key', 'api_secret', 'hook_url', 'redirect_url'],
    email: ['user_email'],
    url: ['hook_url', 'redirect_url']
  }
}

// Default form values for each platform
export const defaultFormValues = {
  facebook: {
    api_version: 'v18.0',
    sync_frequency: 'hourly',
    max_retries: 3,
    debug_mode: false,
    auto_sync_pages: true,
    default_permissions: 'read',
    permissions: ['pages_show_list', 'pages_read_engagement', 'pages_manage_posts']
  },
  zalo: {
    oa_type: 'business',
    sync_frequency: 'hourly',
    max_retries: 3,
    debug_mode: false,
    auto_sync_templates: true,
    default_language: 'vi',
    enable_broadcasting: true,
    daily_message_limit: 1000,
    message_priority: 'normal',
    auto_create_contacts: true,
    sync_user_profiles: true,
    contact_source: 'zalo',
    permissions: ['oa_info', 'send_message', 'manage_followers']
  },
  cal_com: {
    instance_url: 'https://cal.com',
    account_type: 'personal',
    primary_calendar: 'google',
    two_way_sync: true,
    buffer_time: 15,
    auto_sync_event_types: true,
    default_duration: 30,
    allow_cancellations: true,
    email_notifications: true,
    sms_notifications: false,
    reminder_timing: '24h',
    timezone: 'Asia/Ho_Chi_Minh',
    booking_lead_time: 24,
    max_bookings_per_day: 10,
    auto_create_contacts: true,
    contact_source: 'booking',
    sync_booking_history: false,
    sync_frequency: 'hourly',
    max_retries: 3,
    debug_mode: false,
    permissions: ['bookings', 'event_types', 'availability']
  },
  topcv: {
    account_type: 'basic',
    auto_post_jobs: true,
    default_job_status: 'active',
    job_duration: 30,
    auto_import_applications: true,
    sync_candidate_profiles: true,
    application_status_mapping: 'standard',
    download_cv_files: false,
    enable_resume_search: false,
    daily_search_limit: 100,
    search_criteria: 'relevant',
    primary_industry: 'technology',
    default_location: 'ho_chi_minh',
    allow_remote: true,
    new_application_alerts: true,
    job_expiry_warnings: true,
    notification_frequency: 'immediate',
    sync_frequency: 'hourly',
    max_retries: 3,
    debug_mode: false,
    permissions: ['job_posting', 'application_management', 'candidate_search']
  }
}

// Helper function to validate form data
export const validateFormData = (platformId, formData) => {
  const rules = formValidationRules[platformId]
  if (!rules) return { valid: true, errors: [] }

  const errors = []

  // Check required fields
  rules.required.forEach(field => {
    if (!formData[field] || formData[field].toString().trim() === '') {
      errors.push(`${field} is required`)
    }
  })

  // Check email fields
  if (rules.email) {
    rules.email.forEach(field => {
      if (formData[field] && !isValidEmail(formData[field])) {
        errors.push(`${field} must be a valid email address`)
      }
    })
  }

  // Check URL fields
  if (rules.url) {
    rules.url.forEach(field => {
      if (formData[field] && !isValidUrl(formData[field])) {
        errors.push(`${field} must be a valid URL`)
      }
    })
  }

  return {
    valid: errors.length === 0,
    errors
  }
}

// Utility functions
const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

const isValidUrl = (url) => {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

// Transform form data before API submission
export const transformFormDataForAPI = (platformId, formData) => {
  const transformed = { ...formData }
  
  // Platform-specific transformations
  switch (platformId) {
    case 'facebook':
      // Convert permissions array to comma-separated string if needed
      if (Array.isArray(transformed.permissions)) {
        transformed.permissions = transformed.permissions.join(',')
      }
      break
      
    case 'zalo':
      // Ensure numeric fields are numbers
      if (transformed.daily_message_limit) {
        transformed.daily_message_limit = parseInt(transformed.daily_message_limit)
      }
      break
      
    case 'cal_com':
      // Convert duration and buffer time to numbers
      ;['default_duration', 'buffer_time', 'booking_lead_time', 'max_bookings_per_day'].forEach(field => {
        if (transformed[field]) {
          transformed[field] = parseInt(transformed[field])
        }
      })
      break
      
    case 'topcv':
      // Convert numeric fields
      ;['job_duration', 'daily_search_limit'].forEach(field => {
        if (transformed[field]) {
          transformed[field] = parseInt(transformed[field])
        }
      })
      break
  }
  
  return transformed
}