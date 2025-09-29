import { 
  getJobOpenings,
  getJobOpeningByName,
  createJobOpening,
  updateJobOpening,
  deleteJobOpening,
  searchJobOpenings
} from '@/repositories/jobOpeningRepository'

export const getFilteredJobOpenings = async (filterOptions = {}) => {
  try {
    const { status, searchText, page = 1, limit = 20 } = filterOptions

    // Build filters as an array of conditions for Frappe get_list
    const filterArray = []
    if (status && status !== 'all') {
      filterArray.push(['approval_status', '=', status])
    }
    if (searchText && searchText.trim()) {
      filterArray.push(['job_title', 'like', `%${searchText.trim()}%`])
    }

    const options = {
      filters: filterArray.length ? filterArray : {},
      fields: [
        'name', 'job_title', 'job_code', 'department_name', 'location_name', 'owner_id',
        'number_of_openings', 'posting_date', 'closing_date', 'approval_status', 'total_applicants',
        'creation', 'modified'
      ],
      page_length: limit,
      start: (page - 1) * limit,
      order_by: 'modified desc'
    }

    const response = await getJobOpenings(options)
    if (response && Array.isArray(response.data)) {
      return response
    } else {
      throw new Error('Không thể tải danh sách Job Openings')
    }
  } catch (e) {
    console.error('Failed to get job openings:', e)
    throw new Error('Không thể tải danh sách Job Openings')
  }
}

export const getJobOpeningDetails = async (name) => {
  const response = await getJobOpeningByName(name)
  if (response) return response
  throw new Error('Không thể tải thông tin Job Opening')
}

export const submitNewJobOpening = async (formData) => {
  if (!formData.job_title || !formData.job_title.trim()) {
    throw new Error('Tiêu đề công việc không được để trống')
  }
  const payload = {
    job_title: formData.job_title.trim(),
    // Không gửi job_code để server tự sinh
    description: formData.description || '',
    requirements: formData.requirements || '',
    benefits: formData.benefits || '',
    department_name: formData.department_name || '',
    location_name: formData.location_name || '',
    owner_id: formData.owner_id || null,
    number_of_openings: formData.number_of_openings || 1,
    posting_date: formData.posting_date || null,
    closing_date: formData.closing_date || null,
    approval_status: formData.approval_status || 'Draft'
  }
  const response = await createJobOpening(payload)
  if (response) return response
  throw new Error('Không thể tạo Job Opening')
}

export const updateJobOpeningData = async (name, formData) => {
  if (!formData.job_title || !formData.job_title.trim()) {
    throw new Error('Tiêu đề công việc không được để trống')
  }
  const data = {
    job_title: formData.job_title.trim(),
    job_code: formData.job_code || '',
    description: formData.description || '',
    requirements: formData.requirements || '',
    benefits: formData.benefits || '',
    department_name: formData.department_name || '',
    location_name: formData.location_name || '',
    owner_id: formData.owner_id || null,
    number_of_openings: formData.number_of_openings || 1,
    posting_date: formData.posting_date || null,
    closing_date: formData.closing_date || null,
    approval_status: formData.approval_status || 'Draft'
  }
  const response = await updateJobOpening(name, data)
  if (response) return response
  throw new Error('Không thể cập nhật Job Opening')
}

export const removeJobOpening = async (name, title) => {
  try {
    const response = await deleteJobOpening(name)
    if (response) return response
  } catch (error) {
    console.error('Failed to delete Job Opening:', error)
    throw new Error(`Không thể xóa Job Opening "${title}"`)
  }
} 