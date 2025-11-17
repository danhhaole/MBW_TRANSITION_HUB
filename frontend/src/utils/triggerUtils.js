

/**
 * Get icon name for trigger type
 * @param {string} triggerType - Trigger type
 * @returns {string} Icon name
 */
export const getTriggerIcon = (triggerType) => {
  const iconMap = {
    // Talent Creation & Updates
    'ON_CREATE': 'user-plus',
    'ON_UPDATE': 'edit',
    'ON_FORM_SUBMISSION': 'file-text',
    // Email Interactions
    'ON_LINK_CLICK': 'mouse-pointer',
    'ON_EMAIL_OPEN': 'mail-open',
    'ON_EMAIL_REPLY': 'corner-up-left',
    'ON_EMAIL_BOUNCE': 'alert-circle',
    // Talent Actions
    'ON_JOB_APPLICATION': 'briefcase',
    'ON_UNSUBSCRIBE': 'user-minus',
    // Tag & Status Changes
    'ON_TAG_ADDED': 'tag',
    'ON_TAG_REMOVED': 'minus-circle',
    'ON_STATUS_CHANGED': 'activity',
    // Score & Activity
    'ON_SCORE_REACHED': 'trending-up',
    'ON_INACTIVITY_TIMEOUT': 'clock',
    // Flow & Schedule
    'ON_SEQUENCE_COMPLETED': 'check-circle',
    'ON_SCHEDULED_TIME': 'calendar',
    // System Events
    'ON_SEND_SUCCESS': 'check',
    'ON_SEND_FAILED': 'x-circle',
    'ON_USER_RESPONSE': 'message-square',
    'CUSTOM_EVENT': 'zap'
  }
  return iconMap[triggerType] || 'zap'
}

/**
 * Get label for trigger type
 * @param {string} triggerType - Trigger type
 * @returns {string} Trigger label
 */
export const getTriggerLabel = (triggerType) => {
  const labels = {
    // Talent Creation & Updates
    'ON_CREATE': __('On Create'),
    'ON_UPDATE': __('On Update'),
    'ON_FORM_SUBMISSION': __('On Form Submission'),
    // Email Interactions
    'ON_LINK_CLICK': __('On Link Click'),
    'ON_EMAIL_OPEN': __('On Email Open'),
    'ON_EMAIL_REPLY': __('On Email Reply'),
    'ON_EMAIL_BOUNCE': __('On Email Bounce'),
    // Talent Actions
    'ON_JOB_APPLICATION': __('On Job Application'),
    'ON_UNSUBSCRIBE': __('On Unsubscribe'),
    // Tag & Status Changes
    'ON_TAG_ADDED': __('On Tag Added'),
    'ON_TAG_REMOVED': __('On Tag Removed'),
    'ON_STATUS_CHANGED': __('On Status Changed'),
    // Score & Activity
    'ON_SCORE_REACHED': __('On Score Reached'),
    'ON_INACTIVITY_TIMEOUT': __('On Inactivity Timeout'),
    // Flow & Schedule
    'ON_SEQUENCE_COMPLETED': __('On Sequence Completed'),
    'ON_SCHEDULED_TIME': __('On Scheduled Time'),
    // System Events
    'ON_SEND_SUCCESS': __('On Send Success'),
    'ON_SEND_FAILED': __('On Send Failed'),
    'ON_USER_RESPONSE': __('On User Response'),
    'CUSTOM_EVENT': __('Custom Event')
  }
  return labels[triggerType] || triggerType
}

/**
 * Get description for trigger type
 * @param {string} triggerType - Trigger type
 * @returns {string} Trigger description
 */
export const getTriggerDescription = (triggerType) => {
  const descriptions = {
    // Talent Creation & Updates
    'ON_CREATE': __('Talent is created in the system'),
    'ON_UPDATE': __('Talent profile is updated'),
    'ON_FORM_SUBMISSION': __('Talent fills out form or submits application'),
    // Email Interactions
    'ON_LINK_CLICK': __('Talent clicks on a link in email or message'),
    'ON_EMAIL_OPEN': __('Talent opens an email from the campaign'),
    'ON_EMAIL_REPLY': __('Talent replies to an email'),
    'ON_EMAIL_BOUNCE': __('Email bounces (invalid email address)'),
    // Talent Actions
    'ON_JOB_APPLICATION': __('Talent applies to a job posting'),
    'ON_UNSUBSCRIBE': __('Talent unsubscribes from campaign'),
    // Tag & Status Changes
    'ON_TAG_ADDED': __('A specific tag is added to talent'),
    'ON_TAG_REMOVED': __('A specific tag is removed from talent'),
    'ON_STATUS_CHANGED': __('Talent status changes (e.g., recruited, rejected)'),
    // Score & Activity
    'ON_SCORE_REACHED': __('Talent engagement score reaches threshold'),
    'ON_INACTIVITY_TIMEOUT': __('Talent shows no activity for set period'),
    // Flow & Schedule
    'ON_SEQUENCE_COMPLETED': __('Previous flow step is completed'),
    'ON_SCHEDULED_TIME': __('Scheduled time is reached'),
    // System Events
    'ON_SEND_SUCCESS': __('Message/email sent successfully'),
    'ON_SEND_FAILED': __('Message/email failed to send'),
    'ON_USER_RESPONSE': __('Talent responds or interacts with campaign'),
    'CUSTOM_EVENT': __('Custom event triggered by external system')
  }
  return descriptions[triggerType] || ''
}

/**
 * Trigger type options for dropdown/select
 */
export const triggerTypeOptions = [
  // Talent Creation & Updates
  { label: __('On Create'), value: 'ON_CREATE' },
  { label: __('On Update'), value: 'ON_UPDATE' },
  { label: __('On Form Submission'), value: 'ON_FORM_SUBMISSION' },
  // Email Interactions
  { label: __('On Link Click'), value: 'ON_LINK_CLICK' },
  { label: __('On Email Open'), value: 'ON_EMAIL_OPEN' },
  { label: __('On Email Reply'), value: 'ON_EMAIL_REPLY' },
  { label: __('On Email Bounce'), value: 'ON_EMAIL_BOUNCE' },
  // Talent Actions
  { label: __('On Job Application'), value: 'ON_JOB_APPLICATION' },
  { label: __('On Unsubscribe'), value: 'ON_UNSUBSCRIBE' },
  // Tag & Status Changes
  { label: __('On Tag Added'), value: 'ON_TAG_ADDED' },
  { label: __('On Tag Removed'), value: 'ON_TAG_REMOVED' },
  { label: __('On Status Changed'), value: 'ON_STATUS_CHANGED' },
  // Score & Activity
  { label: __('On Score Reached'), value: 'ON_SCORE_REACHED' },
  { label: __('On Inactivity Timeout'), value: 'ON_INACTIVITY_TIMEOUT' },
  // Flow & Schedule
  { label: __('On Sequence Completed'), value: 'ON_SEQUENCE_COMPLETED' },
  { label: __('On Scheduled Time'), value: 'ON_SCHEDULED_TIME' },
  // System Events
  { label: __('On Send Success'), value: 'ON_SEND_SUCCESS' },
  { label: __('On Send Failed'), value: 'ON_SEND_FAILED' },
  { label: __('User Response'), value: 'ON_USER_RESPONSE' },
  { label: __('Custom Event'), value: 'CUSTOM_EVENT' }
]
