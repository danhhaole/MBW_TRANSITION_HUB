/**
 * Campaign Configuration Index
 * Central export for campaign configurations
 * 
 * NOTE: Currently all campaigns share the same triggers/actions (20 triggers, 19 actions)
 * TODO: Filter per campaign type when requirements are documented
 */

import {
  allTriggerTypes,
  allActionTypes,
  triggerIcons,
  triggerDescriptions,
  actionIcons,
  actionDescriptions
} from './commonConfig'

// Keep imports for future campaign-specific filtering
import {
  attractionTriggerTypes,
  attractionActionTypes,
  attractionTriggerIcons,
  attractionTriggerDescriptions,
  attractionActionIcons,
  attractionActionDescriptions
} from './attractionConfig'

import {
  nurturingTriggerTypes,
  nurturingActionTypes,
  nurturingTriggerIcons,
  nurturingTriggerDescriptions,
  nurturingActionIcons,
  nurturingActionDescriptions
} from './nurturingConfig'

import {
  recruitmentTriggerTypes,
  recruitmentActionTypes,
  recruitmentTriggerIcons,
  recruitmentTriggerDescriptions,
  recruitmentActionIcons,
  recruitmentActionDescriptions
} from './recruitmentConfig'

/**
 * Campaign types enum
 */
export const CAMPAIGN_TYPES = {
  ATTRACTION: 'attraction',
  NURTURING: 'nurturing',
  RECRUITMENT: 'recruitment'
}

/**
 * Get trigger types for a specific campaign
 * @param {string} campaignType - Campaign type (attraction, nurturing, recruitment)
 * @returns {Array} Array of trigger type options (20 types)
 * 
 * NOTE: Currently returns all triggers for all campaign types
 * TODO: Filter per campaign when requirements are documented
 */
export function getTriggerTypes(campaignType) {
  // TODO: Uncomment when ready to filter per campaign
  // const config = {
  //   [CAMPAIGN_TYPES.ATTRACTION]: attractionTriggerTypes,
  //   [CAMPAIGN_TYPES.NURTURING]: nurturingTriggerTypes,
  //   [CAMPAIGN_TYPES.RECRUITMENT]: recruitmentTriggerTypes
  // }
  // return config[campaignType] || allTriggerTypes
  
  // Return all triggers for now
  return allTriggerTypes
}

/**
 * Get action types for a specific campaign
 * @param {string} campaignType - Campaign type (attraction, nurturing, recruitment)
 * @returns {Array} Array of action type options (19 types)
 * 
 * NOTE: Currently returns all actions for all campaign types
 * TODO: Filter per campaign when requirements are documented
 */
export function getActionTypes(campaignType) {
  const config = {
    [CAMPAIGN_TYPES.ATTRACTION]: attractionActionTypes,
    [CAMPAIGN_TYPES.NURTURING]: nurturingActionTypes,
    [CAMPAIGN_TYPES.RECRUITMENT]: recruitmentActionTypes
  }
  return config[campaignType] || allActionTypes
}

/**
 * Get icon for a trigger type
 * @param {string} triggerType - Trigger type value
 * @param {string} campaignType - Campaign type (currently not used)
 * @returns {string} Icon name
 * 
 * NOTE: Currently uses common icons for all campaigns
 */
export function getTriggerIcon(triggerType, campaignType) {
  // TODO: Uncomment for campaign-specific icons
  // const config = {
  //   [CAMPAIGN_TYPES.ATTRACTION]: attractionTriggerIcons,
  //   [CAMPAIGN_TYPES.NURTURING]: nurturingTriggerIcons,
  //   [CAMPAIGN_TYPES.RECRUITMENT]: recruitmentTriggerIcons
  // }
  // const icons = config[campaignType] || triggerIcons
  // return icons[triggerType] || 'zap'
  
  return triggerIcons[triggerType] || 'zap'
}

/**
 * Get description for a trigger type
 * @param {string} triggerType - Trigger type value
 * @param {string} campaignType - Campaign type (currently not used)
 * @returns {string} Trigger description
 * 
 * NOTE: Currently uses common descriptions for all campaigns
 */
export function getTriggerDescription(triggerType, campaignType) {
  // TODO: Uncomment for campaign-specific descriptions
  // const config = {
  //   [CAMPAIGN_TYPES.ATTRACTION]: attractionTriggerDescriptions,
  //   [CAMPAIGN_TYPES.NURTURING]: nurturingTriggerDescriptions,
  //   [CAMPAIGN_TYPES.RECRUITMENT]: recruitmentTriggerDescriptions
  // }
  // const descriptions = config[campaignType] || triggerDescriptions
  // return descriptions[triggerType] || ''
  
  return triggerDescriptions[triggerType] || ''
}

/**
 * Get label for a trigger type
 * @param {string} triggerType - Trigger type value
 * @param {string} campaignType - Campaign type
 * @returns {string} Trigger label
 */
export function getTriggerLabel(triggerType, campaignType) {
  const triggerTypes = getTriggerTypes(campaignType)
  const trigger = triggerTypes.find(t => t.value === triggerType)
  return trigger ? trigger.label : triggerType
}

/**
 * Get icon for an action type
 * @param {string} actionType - Action type value
 * @param {string} campaignType - Campaign type (currently not used)
 * @returns {string} Icon name
 * 
 * NOTE: Currently uses common icons for all campaigns
 */
export function getActionIcon(actionType, campaignType) {
  const config = {
    [CAMPAIGN_TYPES.ATTRACTION]: attractionActionIcons,
    [CAMPAIGN_TYPES.NURTURING]: nurturingActionIcons,
    [CAMPAIGN_TYPES.RECRUITMENT]: recruitmentActionIcons
  }
  const icons = config[campaignType] || actionIcons
  return icons[actionType] || 'zap'
}

/**
 * Get description for an action type
 * @param {string} actionType - Action type value
 * @param {string} campaignType - Campaign type (currently not used)
 * @returns {string} Action description
 * 
 * NOTE: Currently uses common descriptions for all campaigns
 */
export function getActionDescription(actionType, campaignType) {
  const config = {
    [CAMPAIGN_TYPES.ATTRACTION]: attractionActionDescriptions,
    [CAMPAIGN_TYPES.NURTURING]: nurturingActionDescriptions,
    [CAMPAIGN_TYPES.RECRUITMENT]: recruitmentActionDescriptions
  }
  const descriptions = config[campaignType] || actionDescriptions
  return descriptions[actionType] || ''
}

/**
 * Get label for an action type
 * @param {string} actionType - Action type value
 * @param {string} campaignType - Campaign type
 * @returns {string} Action label
 */
export function getActionLabel(actionType, campaignType) {
  const actionTypes = getActionTypes(campaignType)
  const action = actionTypes.find(a => a.value === actionType)
  return action ? action.label : actionType
}

// Export everything for direct imports if needed
export {
  // Common (currently in use for all campaigns)
  allTriggerTypes,
  allActionTypes,
  triggerIcons,
  triggerDescriptions,
  actionIcons,
  actionDescriptions,
  // Campaign-specific (ready for future use)
  // Attraction
  attractionTriggerTypes,
  attractionActionTypes,
  attractionTriggerIcons,
  attractionTriggerDescriptions,
  attractionActionIcons,
  attractionActionDescriptions,
  // Nurturing
  nurturingTriggerTypes,
  nurturingActionTypes,
  nurturingTriggerIcons,
  nurturingTriggerDescriptions,
  nurturingActionIcons,
  nurturingActionDescriptions,
  // Recruitment
  recruitmentTriggerTypes,
  recruitmentActionTypes,
  recruitmentTriggerIcons,
  recruitmentTriggerDescriptions,
  recruitmentActionIcons,
  recruitmentActionDescriptions
}
