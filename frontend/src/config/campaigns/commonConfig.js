/**
 * Common Campaign Configuration
 * Shared triggers and actions for all campaign types
 * TODO: Filter per campaign type when requirements are documented
 */

/**
 * All trigger types (12 types - based on documentation)
 * Currently shared across all campaigns
 */
export const allTriggerTypes = [
  // Talent Interactions (5)
  { label: __('Form Submission'), value: 'ON_FORM_SUBMISSION' },
  { label: __('Link Click'), value: 'ON_LINK_CLICK' },
  { label: __('Email Open'), value: 'ON_EMAIL_OPEN' },
  { label: __('Job Application'), value: 'ON_JOB_APPLICATION' },
  { label: __('Unsubscribe'), value: 'ON_UNSUBSCRIBE' },
  // Data Management (2)
  { label: __('Tag Added'), value: 'ON_TAG_ADDED' },
  { label: __('Tag Removed'), value: 'ON_TAG_REMOVED' },
  // System Interactions (5)
  { label: __('Status Change'), value: 'ON_STATUS_CHANGED' },
  { label: __('Score Threshold Reached'), value: 'ON_SCORE_REACHED' },
  { label: __('Hard Bounce'), value: 'ON_EMAIL_BOUNCE' },
  { label: __('Inactivity Timeout'), value: 'ON_INACTIVITY_TIMEOUT' },
  { label: __('Flow Step Completed'), value: 'ON_SEQUENCE_COMPLETED' },
  // Birthday & Email Engagement (2)
  { label: __('Birthday'), value: 'ON_BIRTHDAY' },
//   { label: __('No Email Click After N Days'), value: 'ON_NO_EMAIL_CLICK' }
]

/**
 * All action types (8 types - based on documentation)
 * Currently shared across all campaigns
 * NOTE: CREATE_TASK has been removed from documentation
 */
export const allActionTypes = [
  // Communication Actions
  { label: __('Send Email'), value: 'EMAIL' },
  { label: __('Send Zalo/SMS Message'), value: 'MESSAGE' },
  // Field Management
  { label: __('Update Field Value'), value: 'UPDATE_FIELD_VALUE' },
  // Tag Management
  { label: __('Add Tag'), value: 'ADD_TAG' },
  { label: __('Remove Tag'), value: 'REMOVE_TAG' },
  // Status & Tracking
  { label: __('Change Status'), value: 'CHANGE_STATUS' },
  { label: __('Stop Tracking'), value: 'STOP_TRACKING' },
  // Notifications & ATS
  { label: __('Send Internal Notification'), value: 'INTERNAL_NOTIFICATION' },
  { label: __('Handoff to ATS'), value: 'HANDOFF_TO_ATS' }
]

/**
 * Trigger icon mapping (12 triggers only)
 */
export const triggerIcons = {
  // Talent Interactions
  'ON_FORM_SUBMISSION': 'file-text',
  'ON_LINK_CLICK': 'mouse-pointer',
  'ON_EMAIL_OPEN': 'mail-open',
  'ON_JOB_APPLICATION': 'briefcase',
  'ON_UNSUBSCRIBE': 'user-minus',
  // Data Management
  'ON_TAG_ADDED': 'tag',
  'ON_TAG_REMOVED': 'minus-circle',
  // System Interactions
  'ON_STATUS_CHANGED': 'activity',
  'ON_SCORE_REACHED': 'trending-up',
  'ON_EMAIL_BOUNCE': 'alert-circle',
  'ON_INACTIVITY_TIMEOUT': 'clock',
  'ON_SEQUENCE_COMPLETED': 'check-circle',
  // Birthday & Email Engagement
  'ON_BIRTHDAY': 'gift',
  'ON_NO_EMAIL_CLICK': 'mouse-pointer'
}

/**
 * Trigger descriptions (12 triggers only)
 */
export const triggerDescriptions = {
  // Talent Interactions
  'ON_FORM_SUBMISSION': __('Talent fills out form or submits application'),
  'ON_LINK_CLICK': __('Talent clicks on a link in email or message'),
  'ON_EMAIL_OPEN': __('Talent opens an email from the campaign'),
  'ON_JOB_APPLICATION': __('Talent applies to a job posting'),
  'ON_UNSUBSCRIBE': __('Talent unsubscribes from campaign'),
  // Data Management
  'ON_TAG_ADDED': __('A specific tag is added to talent'),
  'ON_TAG_REMOVED': __('A specific tag is removed from talent'),
  // System Interactions
  'ON_STATUS_CHANGED': __('Talent status changes (e.g., Active, Paused, Completed)'),
  'ON_SCORE_REACHED': __('Talent engagement score reaches threshold'),
  'ON_EMAIL_BOUNCE': __('Email bounces (invalid email address)'),
  'ON_INACTIVITY_TIMEOUT': __('Talent shows no activity for set period'),
  'ON_SEQUENCE_COMPLETED': __('Previous flow step is completed'),
  // Birthday & Email Engagement
  'ON_BIRTHDAY': __('Send birthday greeting email'),
//   'ON_NO_EMAIL_CLICK': __('After N days without email click - Stop nurturing or Send another email')
}

/**
 * Action icon mapping (8 actions only)
 */
export const actionIcons = {
  // Communication Actions
  'EMAIL': 'mail',
  'MESSAGE': 'message-circle',
  // Field Management
  'UPDATE_FIELD_VALUE': 'edit',
  // Tag Management
  'ADD_TAG': 'tag',
  'REMOVE_TAG': 'x-square',
  // Status & Tracking
  'CHANGE_STATUS': 'toggle-right',
  'STOP_TRACKING': 'user-minus',
  // Notifications & ATS
  'INTERNAL_NOTIFICATION': 'bell-ring',
  'HANDOFF_TO_ATS': 'send'
}

/**
 * Action descriptions (8 actions only)
 */
export const actionDescriptions = {
  // Communication Actions
  'EMAIL': __('Send email to talent'),
  'MESSAGE': __('Send Zalo/SMS message to talent'),
  // Field Management
  'UPDATE_FIELD_VALUE': __('Update field value in talent profile'),
  // Tag Management
  'ADD_TAG': __('Add tag to talent profile'),
  'REMOVE_TAG': __('Remove tag from talent profile'),
  // Status & Tracking
  'CHANGE_STATUS': __('Change talent status'),
  'STOP_TRACKING': __('Stop tracking this talent'),
  // Notifications & ATS
  'INTERNAL_NOTIFICATION': __('Send notification to team members'),
  'HANDOFF_TO_ATS': __('Transfer talent to ATS system')
}
