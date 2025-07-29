import { call } from 'frappe-ui'
import { createResource } from '@/utils/api'

// Get paginated ladi pages with filters
export const getFilteredLadiPages = async (filterOptions = {}) => {
  try {
    const { status, campaign, searchText, page = 1, limit = 20 } = filterOptions
    let filters = {}
    if (status && status !== 'all') {
      filters.status = status
    }
    if (campaign && campaign !== 'all') {
      filters.campaign = campaign
    }

    let options = {
      filters,
      page_length: limit,
      start: (page - 1) * limit,
      or_filters: undefined,
    }

    if (searchText) {
      options.or_filters = [
        ['title', 'like', `%${searchText}%`],
        ['description', 'like', `%${searchText}%`]
      ]
    }

    const response = await getLadiPages(options)
    if (response && Array.isArray(response.data)) {
      return response
    } else {
      throw new Error('Could not load Ladi pages')
    }
  } catch (error) {
    console.error('Failed to get Ladi pages:', error)
    throw error
  }
}

// Get Ladi page details
export const getLadiPageDetails = async (name) => {
  try {
    const response = await getLadiPageByName(name)
    if (response && response.data) {
      return response.data
    } else {
      throw new Error('Could not load Ladi page details')
    }
  } catch (error) {
    console.error('Failed to get Ladi page details:', error)
    throw error
  }
}

// Create new Ladi page with validation
export const createLadiPage = async (formData) => {
  try {
    if (!formData.title || !formData.title.trim()) {
      throw new Error('Title is required')
    }

    const response = await call('frappe.client.insert', {
      doc: {
        doctype: 'LadiPage',
        title: formData.title.trim(),
        description: formData.description || '',
        route: formData.route || '',
        campaign: formData.campaign || null,
        status: formData.status || 'Draft',
        content: formData.content || ''
      }
    })

    if (response) {
      return response
    } else {
      throw new Error('Could not create Ladi page')
    }
  } catch (error) {
    console.error('Failed to create Ladi page:', error)
    throw error
  }
}

// Update Ladi page
export const updateLadiPage = async (name, formData) => {
  try {
    if (!formData.title || !formData.title.trim()) {
      throw new Error('Title is required')
    }

    const response = await call('frappe.client.set_value', {
      doctype: 'LadiPage',
      name,
      fieldname: {
        title: formData.title.trim(),
        description: formData.description || '',
        route: formData.route || '',
        campaign: formData.campaign || null,
        status: formData.status || 'Draft',
        content: formData.content || ''
      }
    })

    if (response) {
      return response
    } else {
      throw new Error('Could not update Ladi page')
    }
  } catch (error) {
    console.error('Failed to update Ladi page:', error)
    throw error
  }
}

// Delete Ladi page
export const deleteLadiPage = async (name) => {
  try {
    const response = await call('frappe.client.delete', {
      doctype: 'LadiPage',
      name
    })
    if (response) {
      return response
    } else {
      throw new Error('Could not delete Ladi page')
    }
  } catch (error) {
    console.error('Failed to delete Ladi page:', error)
    throw error
  }
}

// Helper: Get campaigns for dropdown
export const getCampaignOptions = async () => {
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Campaign',
      fields: ['name', 'campaign_name'],
      filters: { status: 'Active' }
    })
    return response.map(campaign => ({
      value: campaign.name,
      label: campaign.campaign_name
    }))
  } catch (error) {
    console.error('Failed to get campaign options:', error)
    return []
  }
}

// Get status options
export const getStatusOptions = () => {
  return [
    { label: 'Draft', value: 'Draft' },
    { label: 'Published', value: 'Published' },
    { label: 'Archived', value: 'Archived' }
  ]
}

// Format date for display
export const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

// Internal helper functions
const getLadiPages = async (options = {}) => {
  return await call('frappe.client.get_list', {
    doctype: 'LadiPage',
    fields: ['*'],
    ...options
  })
}

const getLadiPageByName = async (name) => {
  return await call('frappe.client.get', {
    doctype: 'LadiPage',
    name
  })
}