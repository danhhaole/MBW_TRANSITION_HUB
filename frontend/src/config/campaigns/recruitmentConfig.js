/**
 * Recruitment Campaign Configuration
 * Triggers and Actions specific to Recruitment campaigns
 */


/**
 * Trigger types available for Recruitment campaigns
 */
export const recruitmentTriggerTypes = [
  // Talent Creation & Updates
  { label: __('Talent Created'), value: 'ON_CREATE' },
  { label: __('Talent Updated'), value: 'ON_UPDATE' },
  { label: __('Form Submission'), value: 'ON_FORM_SUBMISSION' },
  // Email Interactions
  { label: __('Link Click'), value: 'ON_LINK_CLICK' },
  { label: __('Email Open'), value: 'ON_EMAIL_OPEN' },
  { label: __('Email Reply'), value: 'ON_EMAIL_REPLY' },
  { label: __('Email Bounce'), value: 'ON_EMAIL_BOUNCE' },
  // Talent Actions - Critical for recruitment
  { label: __('Job Application'), value: 'ON_JOB_APPLICATION' },
  { label: __('Unsubscribe'), value: 'ON_UNSUBSCRIBE' },
  // Tag & Status Changes - Very important in recruitment
  { label: __('Tag Added'), value: 'ON_TAG_ADDED' },
  { label: __('Tag Removed'), value: 'ON_TAG_REMOVED' },
  { label: __('Status Changed'), value: 'ON_STATUS_CHANGED' },
  // Score & Activity
  { label: __('Score Reached'), value: 'ON_SCORE_REACHED' },
  { label: __('Inactivity Timeout'), value: 'ON_INACTIVITY_TIMEOUT' },
  // Flow & Schedule - Important for interview scheduling
  { label: __('Sequence Completed'), value: 'ON_SEQUENCE_COMPLETED' },
  { label: __('Scheduled Time'), value: 'ON_SCHEDULED_TIME' },
  // Birthday & Email Engagement
  { label: __('Birthday'), value: 'ON_BIRTHDAY' },
  { label: __('No Email Click After N Days'), value: 'ON_NO_EMAIL_CLICK' },
  // System Events
  { label: __('Send Success'), value: 'ON_SEND_SUCCESS' },
  { label: __('Send Failed'), value: 'ON_SEND_FAILED' },
  { label: __('User Response'), value: 'ON_USER_RESPONSE' },
  { label: __('Custom Event'), value: 'CUSTOM_EVENT' }
]

/**
 * Action types available for Recruitment campaigns
 */
export const recruitmentActionTypes = [
  // Communication Actions - Full suite
  { label: __('Send Email'), value: 'EMAIL' },
  { label: __('Send Message'), value: 'MESSAGE' },
  { label: __('Send Facebook Message'), value: 'FACEBOOK' },
  { label: __('Send SMS'), value: 'SMS' },
  { label: __('Send Zalo Message'), value: 'ZALO' },
  // Flow Control
  { label: __('Smart Delay'), value: 'SMART_DELAY' },
  // AI & Advanced - Important for screening
  { label: __('AI Call'), value: 'AI_CALL' },
  // Tag Management - Critical for candidate tracking
  { label: __('Add Tag'), value: 'ADD_TAG' },
  { label: __('Remove Tag'), value: 'REMOVE_TAG' },
  // Field Management
  { label: __('Add Custom Field'), value: 'ADD_CUSTOM_FIELD' },
  { label: __('Remove Custom Field'), value: 'REMOVE_CUSTOM_FIELD' },
  { label: __('Update Field Value'), value: 'UPDATE_FIELD_VALUE' },
  // External & Notifications
  { label: __('External Request'), value: 'EXTERNAL_REQUEST' },
  { label: __('Send Notification'), value: 'SENT_NOTIFICATION' },
  // Talent Management - Very important for recruitment
  { label: __('Unsubscribe'), value: 'UNSUBSCRIBE' },
  { label: __('Change Status'), value: 'CHANGE_STATUS' },
  { label: __('Stop Tracking'), value: 'STOP_TRACKING' },
  // Internal & ATS - Critical for recruitment
  { label: __('Internal Notification'), value: 'INTERNAL_NOTIFICATION' },
  { label: __('Handoff to ATS'), value: 'HANDOFF_TO_ATS' }
]

/**
 * Trigger icon mapping for Recruitment campaigns
 */
export const recruitmentTriggerIcons = {
  'ON_CREATE': 'user-plus',
  'ON_UPDATE': 'edit',
  'ON_FORM_SUBMISSION': 'file-text',
  'ON_LINK_CLICK': 'mouse-pointer',
  'ON_EMAIL_OPEN': 'mail-open',
  'ON_EMAIL_REPLY': 'corner-up-left',
  'ON_EMAIL_BOUNCE': 'alert-circle',
  'ON_JOB_APPLICATION': 'briefcase',
  'ON_UNSUBSCRIBE': 'user-minus',
  'ON_TAG_ADDED': 'tag',
  'ON_TAG_REMOVED': 'minus-circle',
  'ON_STATUS_CHANGED': 'activity',
  'ON_SCORE_REACHED': 'trending-up',
  'ON_INACTIVITY_TIMEOUT': 'clock',
  'ON_SEQUENCE_COMPLETED': 'check-circle',
  'ON_SCHEDULED_TIME': 'calendar',
  'ON_BIRTHDAY': 'gift',
  'ON_NO_EMAIL_CLICK': 'mouse-pointer',
  'ON_SEND_SUCCESS': 'check',
  'ON_SEND_FAILED': 'x-circle',
  'ON_USER_RESPONSE': 'message-square',
  'CUSTOM_EVENT': 'zap'
}

/**
 * Trigger descriptions for Recruitment campaigns
 */
export const recruitmentTriggerDescriptions = {
  'ON_CREATE': __('Candidate enters recruitment process'),
  'ON_UPDATE': __('Candidate profile updated'),
  'ON_FORM_SUBMISSION': __('Candidate submits application form'),
  'ON_LINK_CLICK': __('Candidate clicks job posting link'),
  'ON_EMAIL_OPEN': __('Candidate opens recruitment email'),
  'ON_EMAIL_REPLY': __('Candidate replies to recruiter'),
  'ON_EMAIL_BOUNCE': __('Recruitment email bounced'),
  'ON_JOB_APPLICATION': __('Candidate applies for position'),
  'ON_UNSUBSCRIBE': __('Candidate withdraws application'),
  'ON_TAG_ADDED': __('Recruitment tag added'),
  'ON_TAG_REMOVED': __('Recruitment tag removed'),
  'ON_STATUS_CHANGED': __('Candidate status changed (screening, interview, offer)'),
  'ON_SCORE_REACHED': __('Candidate score threshold reached'),
  'ON_INACTIVITY_TIMEOUT': __('No response from candidate'),
  'ON_SEQUENCE_COMPLETED': __('Interview stage completed'),
  'ON_SCHEDULED_TIME': __('Interview time scheduled'),
  'ON_BIRTHDAY': __('Send birthday greeting email'),
  'ON_NO_EMAIL_CLICK': __('After N days without email click - Stop nurturing or Send another email'),
  'ON_SEND_SUCCESS': __('Message sent to candidate'),
  'ON_SEND_FAILED': __('Failed to reach candidate'),
  'ON_USER_RESPONSE': __('Candidate responds'),
  'CUSTOM_EVENT': __('Custom recruitment event')
}

/**
 * Action icon mapping for Recruitment campaigns
 */
export const recruitmentActionIcons = {
  'EMAIL': 'mail',
  'MESSAGE': 'message-circle',
  'FACEBOOK': 'facebook',
  'SMS': 'smartphone',
  'ZALO': 'message-square',
  'SMART_DELAY': 'clock',
  'AI_CALL': 'phone',
  'ADD_TAG': 'tag',
  'REMOVE_TAG': 'x-square',
  'ADD_CUSTOM_FIELD': 'edit-3',
  'REMOVE_CUSTOM_FIELD': 'minus-square',
  'UPDATE_FIELD_VALUE': 'edit',
  'EXTERNAL_REQUEST': 'external-link',
  'SENT_NOTIFICATION': 'bell',
  'UNSUBSCRIBE': 'user-x',
  'CHANGE_STATUS': 'toggle-right',
  'STOP_TRACKING': 'user-minus',
  'INTERNAL_NOTIFICATION': 'bell-ring',
  'HANDOFF_TO_ATS': 'send'
}

/**
 * Action descriptions for Recruitment campaigns
 */
export const recruitmentActionDescriptions = {
  'EMAIL': __('Send recruitment email to candidate'),
  'MESSAGE': __('Send message to candidate'),
  'FACEBOOK': __('Send Facebook message to candidate'),
  'SMS': __('Send SMS to candidate'),
  'ZALO': __('Send Zalo message to candidate'),
  'SMART_DELAY': __('Wait for candidate response'),
  'AI_CALL': __('AI screening call'),
  'ADD_TAG': __('Add recruitment tag'),
  'REMOVE_TAG': __('Remove recruitment tag'),
  'ADD_CUSTOM_FIELD': __('Add candidate field'),
  'REMOVE_CUSTOM_FIELD': __('Remove candidate field'),
  'UPDATE_FIELD_VALUE': __('Update candidate information'),
  'EXTERNAL_REQUEST': __('Sync with external system'),
  'SENT_NOTIFICATION': __('Send candidate notification'),
  'UNSUBSCRIBE': __('Withdraw candidate'),
  'CHANGE_STATUS': __('Change recruitment status'),
  'STOP_TRACKING': __('Stop candidate tracking'),
  'INTERNAL_NOTIFICATION': __('Notify recruitment team'),
  'HANDOFF_TO_ATS': __('Transfer to ATS system')
}
