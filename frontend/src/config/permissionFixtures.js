/**
 * DOCTYPE_FEATURE_MAP for MBW Mira
 * Maps DocTypes to their corresponding features and permission levels
 * 
 * Permission Levels:
 * - "full": Full access (create, read, write, delete, all operations)
 * - "create": Creation access (create, read, write)
 * - "view": View only access (read only)
 * - "manage": Management access (read, write, no delete)
 * - "delete": Delete access (read, delete)
 * - "report": Reporting access (read, export, report)
 * - "share": Sharing access (read, share, email)
 * - "execute": Execution access (read, write, email)
 */
export const DOCTYPE_FEATURE_MAP = {
  // ==================== CAMPAIGN FEATURES ====================
  "Mira Campaign": {
    mira_campaign_full_access: "full",
    mira_campaign_creation: "create",
    mira_campaign_view_only: "view",
    mira_campaign_management: "manage",
    mira_campaign_file_management: "view",
    mira_campaign_sharing: "share",
    mira_campaign_reporting: "report"
  },

  "Mira Segment": {
    mira_segment_full_access: "full",
    mira_segment_creation: "create",
    mira_segment_view_only: "view",
    mira_segment_management: "manage",
    mira_segment_delete: "delete",
    mira_segment_reporting: "report",
    mira_segment_sync_ats: "create"
  },

  "Mira Data Source": {
    mira_datasource_full_access: "full",
    mira_datasource_creation: "create",
    mira_datasource_view_only: "view",
    mira_datasource_management: "manage",
    mira_datasource_delete: "delete",
    mira_datasource_reporting: "report"
  },

  "File": {
    mira_campaign_file_management: "full"
  },

  // ==================== TALENT FEATURES ====================
  "Mira Talent": {
    mira_talent_full_access: "full",
    mira_talent_creation: "create",
    mira_talent_view_only: "view",
    mira_talent_management: "manage",
    mira_talent_delete: "delete",
    mira_talent_reporting: "report",
    mira_talent_import: "create",
    mira_talent_export: "report",
    mira_interaction_full_access: "view",
    mira_interaction_creation: "view",
    mira_interaction_view_only: "view",
    mira_interaction_management: "view",
    mira_interaction_delete: "view",
    mira_interaction_reporting: "view",
    mira_interaction_analytics: "view"
  },

  "User": {
    mira_talent_full_access: "view",
    mira_talent_creation: "view",
    mira_talent_view_only: "view",
    mira_talent_management: "view",
    mira_campaign_template_full_access: "view",
    mira_campaign_template_creation: "view",
    mira_campaign_template_view_only: "view",
    mira_campaign_template_management: "view",
    mira_campaign_template_use: "view",
    mira_action_full_access: "view",
    mira_action_creation: "view",
    mira_action_view_only: "view",
    mira_action_management: "view",
    mira_action_delete: "view",
    mira_action_reporting: "view",
    mira_action_execution: "view"
  },

  // ==================== CAMPAIGN TEMPLATE FEATURES ====================
  "Mira Campaign Template": {
    mira_campaign_template_full_access: "full",
    mira_campaign_template_creation: "create",
    mira_campaign_template_view_only: "view",
    mira_campaign_template_management: "manage",
    mira_campaign_template_delete: "delete",
    mira_campaign_template_use: "view"
  },

  "Mira Action Template": {
    mira_campaign_template_full_access: "full",
    mira_campaign_template_creation: "create",
    mira_campaign_template_view_only: "view",
    mira_campaign_template_management: "full",
    mira_campaign_template_use: "view"
  },

  "Mira Trigger Template": {
    mira_campaign_template_full_access: "full",
    mira_campaign_template_creation: "create",
    mira_campaign_template_view_only: "view",
    mira_campaign_template_management: "full",
    mira_campaign_template_use: "view"
  },

  // ==================== INTERACTION FEATURES ====================
  "Mira Interaction": {
    mira_interaction_full_access: "full",
    mira_interaction_creation: "create",
    mira_interaction_view_only: "view",
    mira_interaction_management: "manage",
    mira_interaction_delete: "delete",
    mira_interaction_reporting: "report",
    mira_interaction_analytics: "report"
  },

  "Mira Campaign": {
    mira_interaction_full_access: "view",
    mira_interaction_creation: "view",
    mira_interaction_view_only: "view",
    mira_interaction_management: "view",
    mira_interaction_delete: "view",
    mira_interaction_reporting: "view",
    mira_interaction_analytics: "view"
  },

  "Email Template": {
    mira_interaction_full_access: "view",
    mira_interaction_creation: "view",
    mira_interaction_view_only: "view",
    mira_interaction_management: "view",
    mira_interaction_delete: "view",
    mira_interaction_reporting: "view",
    mira_interaction_analytics: "view"
  },

  // ==================== ACTION FEATURES ====================
  "Mira Action": {
    mira_action_full_access: "full",
    mira_action_creation: "create",
    mira_action_view_only: "view",
    mira_action_management: "manage",
    mira_action_delete: "delete",
    mira_action_reporting: "report",
    mira_action_execution: "execute"
  },

  "Mira Talent Campaign": {
    mira_action_full_access: "view",
    mira_action_creation: "view",
    mira_action_view_only: "view",
    mira_action_management: "view",
    mira_action_delete: "view",
    mira_action_reporting: "view",
    mira_action_execution: "view"
  },

  "Mira Campaign Social": {
    mira_action_full_access: "view",
    mira_action_creation: "view",
    mira_action_view_only: "view",
    mira_action_management: "view",
    mira_action_delete: "view",
    mira_action_reporting: "view",
    mira_action_execution: "view"
  }
};
  