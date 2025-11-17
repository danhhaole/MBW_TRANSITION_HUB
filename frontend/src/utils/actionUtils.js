/**
 * Action Utilities
 * Helper functions for Campaign Actions
 */

import { __ } from '../../../frappe/frappe/public/js/frappe/translate'

/**
 * Get icon name for action type
 * @param {string} actionType - Action type
 * @returns {string} Icon name
 */
export const getActionIcon = (actionType) => {
  const iconMap = {
    // Communication Actions
    'MESSAGE': 'message-circle',
    'FACEBOOK': 'facebook',
    'SMS': 'smartphone',
    'EMAIL': 'mail',
    'ZALO': 'message-square',
    // Flow Control
    'SMART_DELAY': 'clock',
    // AI & Advanced
    'AI_CALL': 'phone',
    // Tag Management
    'ADD_TAG': 'tag',
    'REMOVE_TAG': 'x-square',
    // Field Management
    'ADD_CUSTOM_FIELD': 'edit-3',
    'REMOVE_CUSTOM_FIELD': 'minus-square',
    // External & Notifications
    'EXTERNAL_REQUEST': 'external-link',
    'SENT_NOTIFICATION': 'bell',
    // Talent Management
    'UNSUBSCRIBE': 'user-x',
    'UPDATE_FIELD_VALUE': 'edit',
    'CHANGE_STATUS': 'toggle-right',
    'STOP_TRACKING': 'user-minus',
    // Internal & ATS
    'INTERNAL_NOTIFICATION': 'bell-ring',
    'HANDOFF_TO_ATS': 'send'
  }
  return iconMap[actionType] || 'zap'
}

/**
 * Get label for action type
 * @param {string} actionType - Action type
 * @returns {string} Action label
 */
export const getActionLabel = (actionType) => {
  const labels = {
    // Communication Actions
    'MESSAGE': __('Send Message'),
    'FACEBOOK': __('Send Facebook Message'),
    'SMS': __('Send SMS'),
    'EMAIL': __('Send Email'),
    'ZALO': __('Send Zalo Message'),
    // Flow Control
    'SMART_DELAY': __('Smart Delay'),
    // AI & Advanced
    'AI_CALL': __('AI Call'),
    // Tag Management
    'ADD_TAG': __('Add Tag'),
    'REMOVE_TAG': __('Remove Tag'),
    // Field Management
    'ADD_CUSTOM_FIELD': __('Add Custom Field'),
    'REMOVE_CUSTOM_FIELD': __('Remove Custom Field'),
    // External & Notifications
    'EXTERNAL_REQUEST': __('External Request'),
    'SENT_NOTIFICATION': __('Send Notification'),
    // Talent Management
    'UNSUBSCRIBE': __('Unsubscribe'),
    'UPDATE_FIELD_VALUE': __('Update Field Value'),
    'CHANGE_STATUS': __('Change Status'),
    'STOP_TRACKING': __('Stop Tracking'),
    // Internal & ATS
    'INTERNAL_NOTIFICATION': __('Internal Notification'),
    'HANDOFF_TO_ATS': __('Handoff to ATS')
  }
  return labels[actionType] || actionType
}

/**
 * Get description for action type
 * @param {string} actionType - Action type
 * @returns {string} Action description
 */
export const getActionDescription = (actionType) => {
  const descriptions = {
    // Communication Actions
    'MESSAGE': __('Send message to talent via multiple channels'),
    'FACEBOOK': __('Send message via Facebook Messenger'),
    'SMS': __('Send SMS message to talent'),
    'EMAIL': __('Send email to talent'),
    'ZALO': __('Send message via Zalo'),
    // Flow Control
    'SMART_DELAY': __('Intelligently delay next action based on behavior'),
    // AI & Advanced
    'AI_CALL': __('AI-powered call or voice action'),
    // Tag Management
    'ADD_TAG': __('Add tag to talent profile'),
    'REMOVE_TAG': __('Remove tag from talent profile'),
    // Field Management
    'ADD_CUSTOM_FIELD': __('Add custom field to talent profile'),
    'REMOVE_CUSTOM_FIELD': __('Remove custom field from talent profile'),
    // External & Notifications
    'EXTERNAL_REQUEST': __('Send external request or webhook'),
    'SENT_NOTIFICATION': __('Send notification to users'),
    // Talent Management
    'UNSUBSCRIBE': __('Unsubscribe talent from campaign'),
    'UPDATE_FIELD_VALUE': __('Update field value in talent profile'),
    'CHANGE_STATUS': __('Change talent status'),
    'STOP_TRACKING': __('Stop tracking this talent permanently'),
    // Internal & ATS
    'INTERNAL_NOTIFICATION': __('Send notification to team members'),
    'HANDOFF_TO_ATS': __('Transfer talent to ATS system')
  }
  return descriptions[actionType] || ''
}

/**
 * Action type options for dropdown/select
 */
export const actionTypeOptions = [
  // Communication Actions
  { label: __('Send Message'), value: 'MESSAGE' },
  { label: __('Send Facebook Message'), value: 'FACEBOOK' },
  { label: __('Send SMS'), value: 'SMS' },
  { label: __('Send Email'), value: 'EMAIL' },
  { label: __('Send Zalo Message'), value: 'ZALO' },
  // Flow Control
  { label: __('Smart Delay'), value: 'SMART_DELAY' },
  // AI & Advanced
  { label: __('AI Call'), value: 'AI_CALL' },
  // Tag Management
  { label: __('Add Tag'), value: 'ADD_TAG' },
  { label: __('Remove Tag'), value: 'REMOVE_TAG' },
  // Field Management
  { label: __('Add Custom Field'), value: 'ADD_CUSTOM_FIELD' },
  { label: __('Remove Custom Field'), value: 'REMOVE_CUSTOM_FIELD' },
  // External & Notifications
  { label: __('External Request'), value: 'EXTERNAL_REQUEST' },
  { label: __('Send Notification'), value: 'SENT_NOTIFICATION' },
  // Talent Management
  { label: __('Unsubscribe'), value: 'UNSUBSCRIBE' },
  { label: __('Update Field Value'), value: 'UPDATE_FIELD_VALUE' },
  { label: __('Change Status'), value: 'CHANGE_STATUS' },
  { label: __('Stop Tracking'), value: 'STOP_TRACKING' },
  // Internal & ATS
  { label: __('Internal Notification'), value: 'INTERNAL_NOTIFICATION' },
  { label: __('Handoff to ATS'), value: 'HANDOFF_TO_ATS' }
]
