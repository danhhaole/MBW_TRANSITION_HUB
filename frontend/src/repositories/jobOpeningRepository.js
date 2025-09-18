import { call } from 'frappe-ui'

export const getJobOpenings = async (options = {}) => {
  const {
    filters = {},
    or_filters = undefined,
    fields = [
      'name', 'job_title', 'job_code', 'department_name', 'location_name', 'owner_id',
      'number_of_openings', 'posting_date', 'closing_date', 'approval_status', 'total_applicants',
      'creation', 'modified'
    ],
    order_by = 'modified desc',
    page_length = 20,
    start = 0
  } = options
  const data = await call('frappe.client.get_list', {
    doctype: 'JobOpening',
    filters,
    fields,
    order_by,
    limit_start: start,
    limit_page_length: page_length
  })
  const total = await call('frappe.client.get_count', {
    doctype: 'JobOpening',
    filters
  })
  return {
    data: data || [],
    pagination: {
      total: total || 0,
      page: Math.floor(start / page_length) + 1,
      limit: page_length,
      pages: Math.ceil((total || 0) / page_length),
      has_next: (start + page_length) < total,
      has_prev: start > 0,
      showing_from: start + 1,
      showing_to: Math.min(start + page_length, total)
    }
  }
}

export const getJobOpeningByName = async (name) => {
  return await call('frappe.client.get', {
    doctype: 'JobOpening',
    name
  })
}

export const createJobOpening = async (data) => {
  return await call('frappe.client.insert', {
    doc: { doctype: 'JobOpening', ...data }
  })
}

export const updateJobOpening = async (name, data) => {
  return await call('frappe.client.set_value', {
    doctype: 'JobOpening',
    name,
    fieldname: data
  })
}

export const deleteJobOpening = async (name) => {
  return await call('frappe.client.delete', {
    doctype: 'JobOpening',
    name
  })
}

export const searchJobOpenings = async (searchText) => {
  const filters = [
    ['job_title', 'like', `%${searchText}%`]
  ]
  return await getJobOpenings({ filters })
} 