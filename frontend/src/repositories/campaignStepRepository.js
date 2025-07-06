import { createResource } from 'frappe-ui'

/**
 * Campaign Step Repository
 * Xử lý tất cả các API calls liên quan đến Campaign Step
 */

// Get paginated campaign steps with filters and search
export const getCampaignSteps = (params = {}) => {
  const resource = createResource({
    url: 'mbw_mira.api.campaign_step.get_campaign_steps_paginated',
    method: 'POST',
    auto: false
  })
  
  return resource.fetch({
    page: params.page || 1,
    limit: params.limit || 10,
    search: params.search || '',
    campaign: params.campaign || '',
    action_type: params.action_type || '',
    order_by: params.order_by || 'step_order asc'
  }).then(response => {
    if (response && typeof response === 'object') {
      return {
        data: response.data || [],
        pagination: response.pagination || {
          page: 1,
          limit: 10,
          total: 0,
          pages: 0,
          has_next: false,
          has_prev: false,
          showing_from: 0,
          showing_to: 0
        }
      }
    }
    
    return {
      data: Array.isArray(response) ? response : [],
      pagination: {
        page: params.page || 1,
        limit: params.limit || 10,
        total: Array.isArray(response) ? response.length : 0,
        pages: 1,
        has_next: false,
        has_prev: false,
        showing_from: 1,
        showing_to: Array.isArray(response) ? response.length : 0
      }
    }
  }).catch(error => {
    console.error('Error fetching campaign steps:', error)
    throw error
  })
}

// Get campaign step statistics
export const getCampaignStepStats = () => {
  const resource = createResource({
    url: 'mbw_mira.api.campaign_step.get_campaign_step_stats',
    method: 'GET',
    auto: false
  })
  
  return resource.fetch().catch(error => {
    console.error('Error fetching campaign step stats:', error)
    return {}
  })
}

// Search campaign steps for autocomplete
export const searchCampaignSteps = (query, limit = 10) => {
  const resource = createResource({
    url: 'mbw_mira.api.campaign_step.search_campaign_steps',
    method: 'POST',
    auto: false
  })
  
  return resource.fetch({
    query,
    limit
  }).then(response => {
    return Array.isArray(response) ? response : []
  }).catch(error => {
    console.error('Error searching campaign steps:', error)
    return []
  })
}

// Get campaign step by ID/name
export const getCampaignStepByName = (name) => {
  const resource = createResource({
    url: 'mbw_mira.api.campaign_step.get_campaign_step_by_name',
    method: 'POST',
    auto: false
  })
  
  return resource.fetch({ name }).catch(error => {
    console.error('Error fetching campaign step:', error)
    throw error
  })
}

// Create new campaign step
export const createCampaignStep = (data) => {
  const resource = createResource({
    url: 'mbw_mira.api.campaign_step.create_campaign_step',
    method: 'POST',
    auto: false
  })

  resource.update({
    params: {
        data: data
    }
  })
  
  return resource.fetch().catch(error => {
    console.error('Error creating campaign step:', error)
    throw error
  })
}

// Update campaign step
export const updateCampaignStep = (name, data) => {
  const resource = createResource({
    url: 'mbw_mira.api.campaign_step.update_campaign_step',
    method: 'POST',
    auto: false
  })
  
  return resource.fetch({ name, data }).catch(error => {
    console.error('Error updating campaign step:', error)
    throw error
  })
}

// Delete campaign step
export const deleteCampaignStep = (name) => {
  const resource = createResource({
    url: 'mbw_mira.api.campaign_step.delete_campaign_step',
    method: 'POST',
    auto: false
  })
  
  return resource.fetch({ name }).catch(error => {
    console.error('Error deleting campaign step:', error)
    throw error
  })
}

// Get filter options
export const getCampaignStepFilterOptions = () => {
  const resource = createResource({
    url: 'mbw_mira.api.campaign_step.get_campaign_step_filter_options',
    method: 'GET',
    auto: false
  })
  
  return resource.fetch().catch(error => {
    console.error('Error fetching filter options:', error)
    return {}
  })
}

// Get steps by campaign
export const getStepsByCampaign = (campaign) => {
  const resource = createResource({
    url: 'mbw_mira.api.campaign_step.get_steps_by_campaign',
    method: 'POST',
    auto: false
  })
  
  return resource.fetch({ campaign }).catch(error => {
    console.error('Error fetching steps by campaign:', error)
    throw error
  })
}

// Reorder campaign steps
export const reorderCampaignSteps = (campaign, stepOrders) => {
  const resource = createResource({
    url: 'mbw_mira.api.campaign_step.reorder_campaign_steps',
    method: 'POST',
    auto: false
  })
  
  return resource.fetch({ campaign, step_orders: stepOrders }).catch(error => {
    console.error('Error reordering campaign steps:', error)
    throw error
  })
}

// Get campaigns for dropdown
export const getCampaigns = () => {
  const resource = createResource({
    url: 'mbw_mira.api.campaign.get_campaigns_paginated',
    method: 'POST',
    auto: false
  })
  
  return resource.fetch({
    page: 1,
    limit: 1000,
    search: '',
    filters: {}
  }).then(response => {
    if (response && response.data) {
      return response.data.map(campaign => ({
        value: campaign.name,
        label: campaign.campaign_name
      }))
    }
    return []
  }).catch(error => {
    console.error('Error fetching campaigns:', error)
    return []
  })
}

// Get action types
export const getActionTypes = () => {
  return Promise.resolve([
    { value: 'SEND_EMAIL', label: 'Send Email' },
    { value: 'SEND_SMS', label: 'Send SMS' },
    { value: 'MANUAL_CALL', label: 'Manual Call' },
    { value: 'MANUAL_TASK', label: 'Manual Task' }
  ])
}
