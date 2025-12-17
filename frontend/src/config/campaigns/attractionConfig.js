/**
 * Attraction Campaign Configuration
 * Triggers and Actions specific to Attraction campaigns
 */



/**
 * Trigger types available for Attraction campaigns
 */
export const attractionTriggerTypes = [
  // Talent Creation & Updates
  { label: __('Talent Created'), value: 'ON_CREATE' },
  { label: __('Talent Updated'), value: 'ON_UPDATE' },
  { label: __('Form Submission'), value: 'ON_FORM_SUBMISSION' },
  // Email Interactions
  { label: __('Link Click'), value: 'ON_LINK_CLICK' },
  { label: __('Email Open'), value: 'ON_EMAIL_OPEN' },
  { label: __('Email Reply'), value: 'ON_EMAIL_REPLY' },
  { label: __('Email Bounce'), value: 'ON_EMAIL_BOUNCE' },
  // Talent Actions
  { label: __('Job Application'), value: 'ON_JOB_APPLICATION' },
  // Tag & Status Changes
  { label: __('Tag Added'), value: 'ON_TAG_ADDED' },
  { label: __('Tag Removed'), value: 'ON_TAG_REMOVED' },
  { label: __('Status Changed'), value: 'ON_STATUS_CHANGED' },
  // Score & Activity
  { label: __('Score Reached'), value: 'ON_SCORE_REACHED' },
  { label: __('Inactivity Timeout'), value: 'ON_INACTIVITY_TIMEOUT' },
  // System Events
  { label: __('Send Success'), value: 'ON_SEND_SUCCESS' },
  { label: __('Send Failed'), value: 'ON_SEND_FAILED' },
  { label: __('User Response'), value: 'ON_USER_RESPONSE' },
  { label: __('Custom Event'), value: 'CUSTOM_EVENT' }
]

/**
 * Action types available for Attraction campaigns
 */
export const attractionActionTypes = [
  // Communication Actions - Focus on initial outreach
  { label: __('Send Email'), value: 'EMAIL' },
  { label: __('Send Zalo/SMS Message'), value: 'MESSAGE' },
  { label: __('Send Facebook Message'), value: 'FACEBOOK' },
  { label: __('Send SMS'), value: 'SMS' },
  { label: __('Send Zalo Message'), value: 'ZALO' },
  // Tag Management
  { label: __('Add Tag'), value: 'ADD_TAG' },
  { label: __('Remove Tag'), value: 'REMOVE_TAG' },
  // Field Management
  { label: __('Add Custom Field'), value: 'ADD_CUSTOM_FIELD' },
  { label: __('Update Field Value'), value: 'UPDATE_FIELD_VALUE' },
  // Status & Tracking
  { label: __('Change Status'), value: 'CHANGE_STATUS' },
  { label: __('Stop Tracking'), value: 'STOP_TRACKING' },
  { label: __('Unsubscribe'), value: 'UNSUBSCRIBE' },
  // Notifications
  { label: __('Send Notification'), value: 'SENT_NOTIFICATION' },
  { label: __('Internal Notification'), value: 'INTERNAL_NOTIFICATION' },
  { label: __('Handoff to ATS'), value: 'HANDOFF_TO_ATS' }
]

/**
 * Trigger icon mapping for Attraction campaigns
 */
export const attractionTriggerIcons = {
  'ON_CREATE': 'user-plus',
  'ON_UPDATE': 'edit',
  'ON_FORM_SUBMISSION': 'file-text',
  'ON_LINK_CLICK': 'mouse-pointer',
  'ON_EMAIL_OPEN': 'mail-open',
  'ON_EMAIL_REPLY': 'corner-up-left',
  'ON_EMAIL_BOUNCE': 'alert-circle',
  'ON_JOB_APPLICATION': 'briefcase',
  'ON_TAG_ADDED': 'tag',
  'ON_TAG_REMOVED': 'minus-circle',
  'ON_STATUS_CHANGED': 'activity',
  'ON_SCORE_REACHED': 'trending-up',
  'ON_INACTIVITY_TIMEOUT': 'clock',
  'ON_SEND_SUCCESS': 'check',
  'ON_SEND_FAILED': 'x-circle',
  'ON_USER_RESPONSE': 'message-square',
  'CUSTOM_EVENT': 'zap'
}

/**
 * Trigger descriptions for Attraction campaigns
 */
export const attractionTriggerDescriptions = {
  'ON_CREATE': __('New talent enters the system'),
  'ON_UPDATE': __('Talent profile is updated'),
  'ON_FORM_SUBMISSION': __('Talent fills out interest form'),
  'ON_LINK_CLICK': __('Talent clicks on marketing link'),
  'ON_EMAIL_OPEN': __('Talent opens outreach email'),
  'ON_EMAIL_REPLY': __('Talent replies to email'),
  'ON_EMAIL_BOUNCE': __('Email delivery failed'),
  'ON_JOB_APPLICATION': __('Talent applies to job posting'),
  'ON_TAG_ADDED': __('Marketing tag is added'),
  'ON_TAG_REMOVED': __('Marketing tag is removed'),
  'ON_STATUS_CHANGED': __('Talent status changes'),
  'ON_SCORE_REACHED': __('Engagement score threshold reached'),
  'ON_INACTIVITY_TIMEOUT': __('No engagement for set period'),
  'ON_SEND_SUCCESS': __('Message delivered successfully'),
  'ON_SEND_FAILED': __('Message delivery failed'),
  'ON_USER_RESPONSE': __('Talent responds to outreach'),
  'CUSTOM_EVENT': __('Custom marketing event')
}

/**
 * Action icon mapping for Attraction campaigns
 */
export const attractionActionIcons = {
  'EMAIL': 'mail',
  'MESSAGE': 'message-circle',
  'FACEBOOK': 'facebook',
  'SMS': 'smartphone',
  'ZALO': 'message-square',
  'ADD_TAG': 'tag',
  'REMOVE_TAG': 'x-square',
  'ADD_CUSTOM_FIELD': 'edit-3',
  'UPDATE_FIELD_VALUE': 'edit',
  'CHANGE_STATUS': 'toggle-right',
  'STOP_TRACKING': 'user-minus',
  'UNSUBSCRIBE': 'user-x',
  'SENT_NOTIFICATION': 'bell',
  'INTERNAL_NOTIFICATION': 'bell-ring',
  'HANDOFF_TO_ATS': 'send'
}

/**
 * Action descriptions for Attraction campaigns
 */
export const attractionActionDescriptions = {
  'EMAIL': __('Send marketing email to talent'),
  'MESSAGE': __('Send Zalo/SMS message to talent'),
  'FACEBOOK': __('Send Facebook Messenger outreach'),
  'SMS': __('Send SMS marketing message'),
  'ZALO': __('Send Zalo marketing message'),
  'ADD_TAG': __('Add marketing tag to talent'),
  'REMOVE_TAG': __('Remove marketing tag from talent'),
  'ADD_CUSTOM_FIELD': __('Add custom tracking field'),
  'UPDATE_FIELD_VALUE': __('Update tracking field value'),
  'CHANGE_STATUS': __('Change talent status'),
  'STOP_TRACKING': __('Stop tracking this talent'),
  'UNSUBSCRIBE': __('Unsubscribe from marketing'),
  'SENT_NOTIFICATION': __('Send notification to talent'),
  'INTERNAL_NOTIFICATION': __('Notify marketing team'),
  'HANDOFF_TO_ATS': __('Transfer talent to ATS system')
}
