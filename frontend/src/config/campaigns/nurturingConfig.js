/**
 * Nurturing Campaign Configuration
 * Triggers and Actions specific to Nurturing campaigns
 */



/**
 * Trigger types available for Nurturing campaigns
 */
export const nurturingTriggerTypes = [
  // Talent Creation & Updates
  { label: __('Talent Created'), value: 'ON_CREATE' },
  { label: __('Talent Updated'), value: 'ON_UPDATE' },
  { label: __('Form Submission'), value: 'ON_FORM_SUBMISSION' },
  // Email Interactions - More important in nurturing
  { label: __('Link Click'), value: 'ON_LINK_CLICK' },
  { label: __('Email Open'), value: 'ON_EMAIL_OPEN' },
  { label: __('Email Reply'), value: 'ON_EMAIL_REPLY' },
  { label: __('Email Bounce'), value: 'ON_EMAIL_BOUNCE' },
  // Talent Actions
  { label: __('Job Application'), value: 'ON_JOB_APPLICATION' },
  { label: __('Unsubscribe'), value: 'ON_UNSUBSCRIBE' },
  // Tag & Status Changes
  { label: __('Tag Added'), value: 'ON_TAG_ADDED' },
  { label: __('Tag Removed'), value: 'ON_TAG_REMOVED' },
  { label: __('Status Changed'), value: 'ON_STATUS_CHANGED' },
  // Score & Activity - Critical for nurturing
  { label: __('Score Reached'), value: 'ON_SCORE_REACHED' },
  { label: __('Inactivity Timeout'), value: 'ON_INACTIVITY_TIMEOUT' },
  // Flow & Schedule - Important for nurturing sequences
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
 * Action types available for Nurturing campaigns
 */
export const nurturingActionTypes = [
  // Communication Actions - Full suite for nurturing
  { label: __('Send Email'), value: 'EMAIL' },
  { label: __('Send Message'), value: 'MESSAGE' },
  { label: __('Send Facebook Message'), value: 'FACEBOOK' },
  { label: __('Send SMS'), value: 'SMS' },
  { label: __('Send Zalo Message'), value: 'ZALO' },
  // Flow Control - Important for nurturing sequences
  { label: __('Smart Delay'), value: 'SMART_DELAY' },
  // AI & Advanced
  { label: __('AI Call'), value: 'AI_CALL' },
  // Tag Management
  { label: __('Add Tag'), value: 'ADD_TAG' },
  { label: __('Remove Tag'), value: 'REMOVE_TAG' },
  // Field Management
  { label: __('Add Custom Field'), value: 'ADD_CUSTOM_FIELD' },
  { label: __('Remove Custom Field'), value: 'REMOVE_CUSTOM_FIELD' },
  { label: __('Update Field Value'), value: 'UPDATE_FIELD_VALUE' },
  // External & Notifications
  { label: __('External Request'), value: 'EXTERNAL_REQUEST' },
  { label: __('Send Notification'), value: 'SENT_NOTIFICATION' },
  // Talent Management
  { label: __('Unsubscribe'), value: 'UNSUBSCRIBE' },
  { label: __('Change Status'), value: 'CHANGE_STATUS' },
  { label: __('Stop Tracking'), value: 'STOP_TRACKING' },
  // Internal & ATS
  { label: __('Internal Notification'), value: 'INTERNAL_NOTIFICATION' },
  { label: __('Handoff to ATS'), value: 'HANDOFF_TO_ATS' }
]

/**
 * Trigger icon mapping for Nurturing campaigns
 */
export const nurturingTriggerIcons = {
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
 * Trigger descriptions for Nurturing campaigns
 */
export const nurturingTriggerDescriptions = {
  'ON_CREATE': __('Talent enters nurturing pipeline'),
  'ON_UPDATE': __('Talent profile updated'),
  'ON_FORM_SUBMISSION': __('Talent submits engagement form'),
  'ON_LINK_CLICK': __('Talent clicks nurturing content link'),
  'ON_EMAIL_OPEN': __('Talent opens nurturing email'),
  'ON_EMAIL_REPLY': __('Talent replies to nurturing email'),
  'ON_EMAIL_BOUNCE': __('Nurturing email bounced'),
  'ON_JOB_APPLICATION': __('Talent applies during nurturing'),
  'ON_UNSUBSCRIBE': __('Talent unsubscribes from nurturing'),
  'ON_TAG_ADDED': __('Engagement tag added'),
  'ON_TAG_REMOVED': __('Engagement tag removed'),
  'ON_STATUS_CHANGED': __('Nurturing status changed'),
  'ON_SCORE_REACHED': __('Engagement score milestone reached'),
  'ON_INACTIVITY_TIMEOUT': __('Talent becomes inactive'),
  'ON_SEQUENCE_COMPLETED': __('Nurturing sequence step completed'),
  'ON_SCHEDULED_TIME': __('Scheduled nurturing time reached'),
  'ON_BIRTHDAY': __('Send birthday greeting email'),
  'ON_NO_EMAIL_CLICK': __('After N days without email click - Stop nurturing or Send another email'),
  'ON_SEND_SUCCESS': __('Nurturing message delivered'),
  'ON_SEND_FAILED': __('Nurturing message failed'),
  'ON_USER_RESPONSE': __('Talent responds to nurturing'),
  'CUSTOM_EVENT': __('Custom nurturing event')
}

/**
 * Action icon mapping for Nurturing campaigns
 */
export const nurturingActionIcons = {
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
 * Action descriptions for Nurturing campaigns
 */
export const nurturingActionDescriptions = {
  'EMAIL': __('Send nurturing email'),
  'MESSAGE': __('Send nurturing message'),
  'FACEBOOK': __('Send Facebook nurturing message'),
  'SMS': __('Send SMS nurturing message'),
  'ZALO': __('Send Zalo nurturing message'),
  'SMART_DELAY': __('Intelligently delay based on engagement'),
  'AI_CALL': __('AI-powered engagement call'),
  'ADD_TAG': __('Add engagement tag'),
  'REMOVE_TAG': __('Remove engagement tag'),
  'ADD_CUSTOM_FIELD': __('Add tracking field'),
  'REMOVE_CUSTOM_FIELD': __('Remove tracking field'),
  'UPDATE_FIELD_VALUE': __('Update engagement field'),
  'EXTERNAL_REQUEST': __('Send external webhook'),
  'SENT_NOTIFICATION': __('Send engagement notification'),
  'UNSUBSCRIBE': __('Unsubscribe from nurturing'),
  'CHANGE_STATUS': __('Change nurturing status'),
  'STOP_TRACKING': __('Stop nurturing tracking'),
  'INTERNAL_NOTIFICATION': __('Notify nurturing team'),
  'HANDOFF_TO_ATS': __('Transfer to recruitment')
}
