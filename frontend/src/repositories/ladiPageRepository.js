import { createResource } from 'frappe-ui'

// Get paginated ladi pages
export const getLadiPages = async (options = {}) => {
  const {
    filters = {},
    or_filters = undefined,
    fields = ['name', 'title', 'description', 'route', 'campaign', 'status', 'creation', 'modified'],
    order_by = 'modified desc',
    page_length = 20,
    start = 0
  } = options

  const resource = createResource({
    url: 'mbw_mira.api.ladipage.get_ladi_pages',
    method: 'POST',
    auto: false
  })

  const data = await resource.fetch({
    filters,
    or_filters,
    fields,
    order_by,
    limit_start: start,
    limit_page_length: page_length
  })

  return {
    data: data || [],
    pagination: {
      total: data?.length || 0,
      page: Math.floor(start / page_length) + 1,
      limit: page_length,
      pages: Math.ceil((data?.length || 0) / page_length),
      has_next: (start + page_length) < (data?.length || 0),
      has_prev: start > 0,
      showing_from: start + 1,
      showing_to: Math.min(start + page_length, data?.length || 0)
    }
  }
}

// Get ladi page details by name
export const getLadiPageByName = async (name) => {
  const resource = createResource({
    url: 'mbw_mira.api.ladipage.get_ladi_page_by_name',
    method: 'POST',
    auto: false
  })
  
  return await resource.fetch({ name })
}

// Create new ladi page
export const createLadiPage = async (data) => {
  const resource = createResource({
    url: 'mbw_mira.api.ladipage.create_ladi_page',
    method: 'POST',
    auto: false
  })
  
  return await resource.fetch({ data })
}

// Update existing ladi page
export const updateLadiPage = async (name, data) => {
  const resource = createResource({
    url: 'mbw_mira.api.ladipage.update_ladi_page',
    method: 'POST',
    auto: false
  })
  
  return await resource.fetch({ name, data })
}

// Delete ladi page
export const deleteLadiPage = async (name) => {
  const resource = createResource({
    url: 'mbw_mira.api.ladipage.delete_ladi_page',
    method: 'POST',
    auto: false
  })
  
  return await resource.fetch({ name })
}

// Get statistics about ladi pages
export const getLadiPageStats = async () => {
  const resource = createResource({
    url: 'mbw_mira.api.ladipage.get_ladi_page_stats',
    method: 'GET',
    auto: false
  })
  
  return await resource.fetch()
}

// Search ladi pages
export const searchLadiPages = async (query, limit = 10) => {
  const resource = createResource({
    url: 'mbw_mira.api.ladipage.search_ladi_pages',
    method: 'POST',
    auto: false
  })
  
  return await resource.fetch({ query, limit })
}

// Get filter options
export const getLadiPageFilterOptions = async () => {
  const resource = createResource({
    url: 'mbw_mira.api.ladipage.get_filter_options',
    method: 'GET',
    auto: false
  })
  
  return await resource.fetch()
}

// Reorder ladi pages
export const reorderLadiPages = async (pageOrders) => {
  const resource = createResource({
    url: 'mbw_mira.api.ladipage.reorder_ladi_pages',
    method: 'POST',
    auto: false
  })
  
  return await resource.fetch({ page_orders: pageOrders })
}