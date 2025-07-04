import { 
  getCampaigns, 
  getCampaignByName, 
  createCampaign, 
  updateCampaign, 
  deleteCampaign,
  searchCampaigns,
  getUsers,
  getTalentSegments
} from '@/repositories/campaignRepository'

// Lấy danh sách campaigns với filter
export const getFilteredCampaigns = async (filterOptions = {}) => {
  try {
    const { status, type, isActive, searchText } = filterOptions
    
    let filters = {}
    if (status && status !== 'all') {
      filters.status = status
    }
    if (type && type !== 'all') {
      filters.type = type  
    }
    if (isActive !== undefined) {
      filters.is_active = isActive
    }
    
    let response
    if (searchText) {
      response = await searchCampaigns(searchText)
      // Áp dụng thêm filters nếu có
      if (response.success && response.data && (status !== 'all' || type !== 'all' || isActive !== undefined)) {
        response.data = response.data.filter(campaign => {
          let match = true
          if (status && status !== 'all') match = match && campaign.status === status
          if (type && type !== 'all') match = match && campaign.type === type
          if (isActive !== undefined) match = match && campaign.is_active === isActive
          return match
        })
      }
    } else {
      response = await getCampaigns(filters)
    }

    console.log('Service response:', response)
    
    if (response.success) {
      return response.data || []
    } else {
      throw new Error(response.message || 'Không thể tải danh sách chiến dịch')
    }
  } catch (error) {
    console.error('Failed to get campaigns:', error)
    throw new Error('Không thể tải danh sách chiến dịch')
  }
}

// Lấy chi tiết campaign
export const getCampaignDetails = async (name) => {
  try {
    const response = await getCampaignByName(name)
    if (response.success) {
      return response.data
    } else {
      throw new Error(response.message || 'Không thể tải thông tin chiến dịch')
    }
  } catch (error) {
    console.error('Failed to get campaign details:', error)
    throw new Error('Không thể tải thông tin chiến dịch')
  }
}

// Lấy danh sách users
export const getUserOptions = async () => {
  try {
    const response = await getUsers()
    return response.success ? (response.data || []) : []
  } catch (error) {
    console.error('Failed to get users:', error)
    return []
  }
}

// Lấy danh sách talent segments
export const getTalentSegmentOptions = async () => {
  try {
    const response = await getTalentSegments()
    return response.success ? (response.data || []) : []
  } catch (error) {
    console.error('Failed to get talent segments:', error)
    return []
  }
}

// Tạo mới campaign với validation
export const submitNewCampaign = async (formData) => {
  try {
    // Validation cơ bản
    if (!formData.campaign_name || !formData.campaign_name.trim()) {
      throw new Error('Tên chiến dịch không được để trống')
    }
    
    if (formData.start_date && formData.end_date) {
      const startDate = new Date(formData.start_date)
      const endDate = new Date(formData.end_date)
      if (startDate >= endDate) {
        throw new Error('Ngày kết thúc phải sau ngày bắt đầu')
      }
    }

    const response = await createCampaign({
      campaign_name: formData.campaign_name.trim(),
      description: formData.description || '',
      is_active: formData.is_active || 0,
      owner_id: formData.owner_id || null,
      start_date: formData.start_date || null,
      end_date: formData.end_date || null,
      type: formData.type || 'NURTURING',
      status: formData.status || 'DRAFT',
      target_segment: formData.target_segment || null
    })
    
    if (response.success) {
      return response
    } else {
      throw new Error(response.message || 'Không thể tạo campaign')
    }
  } catch (error) {
    console.error('Failed to create campaign:', error)
    throw error
  }
}

// Cập nhật campaign
export const updateCampaignData = async (name, formData) => {
  try {
    // Validation
    if (!formData.campaign_name || !formData.campaign_name.trim()) {
      throw new Error('Tên chiến dịch không được để trống')
    }
    
    if (formData.start_date && formData.end_date) {
      const startDate = new Date(formData.start_date)
      const endDate = new Date(formData.end_date)
      if (startDate >= endDate) {
        throw new Error('Ngày kết thúc phải sau ngày bắt đầu')
      }
    }

    const updateData = {
      campaign_name: formData.campaign_name.trim(),
      description: formData.description || '',
      is_active: formData.is_active || 0,
      owner_id: formData.owner_id || null,
      start_date: formData.start_date || null,
      end_date: formData.end_date || null,
      type: formData.type || 'NURTURING',
      status: formData.status || 'DRAFT',
      target_segment: formData.target_segment || null
    }

    const response = await updateCampaign(name, updateData)
    if (response.success) {
      return response
    } else {
      throw new Error(response.message || 'Không thể cập nhật campaign')
    }
  } catch (error) {
    console.error('Failed to update campaign:', error)
    throw error
  }
}

// Xóa campaign với confirmation
export const removeCampaign = async (name, campaignName) => {
  try {
    const response = await deleteCampaign(name)
    if (response.success) {
      return response
    } else {
      throw new Error(response.message || `Không thể xóa chiến dịch "${campaignName}"`)
    }
  } catch (error) {
    console.error('Failed to delete campaign:', error)
    throw new Error(`Không thể xóa chiến dịch "${campaignName}"`)
  }
}

// Lấy campaigns theo trạng thái
export const getCampaignsByStatus = async (status) => {
  try {
    const campaigns = await getFilteredCampaigns({ status })
    return campaigns
  } catch (error) {
    console.error('Failed to get campaigns by status:', error)
    throw error
  }
}

// Tìm kiếm ứng viên theo nguồn và cấu hình
export const searchCandidates = async (source, configData) => {
  try {
    // For now, return mock data but later can integrate with real search API
    const mockCandidates = [
      { 
        id: 'c1', 
        name: 'Nguyễn Văn An', 
        title: 'Senior React Developer', 
        source: 'Nguồn nhân tài', 
        email: 'an.nguyen@email.com',
        experience: 5,
        skills: ['React', 'JavaScript', 'TypeScript']
      },
      { 
        id: 'c2', 
        name: 'Trần Thị Bình', 
        title: 'Fullstack Engineer', 
        source: 'ATS', 
        email: 'binh.tran@email.com',
        experience: 3,
        skills: ['Node.js', 'React', 'MongoDB']
      },
      { 
        id: 'c3', 
        name: 'Lê Hoàng Cường', 
        title: 'Data Scientist', 
        source: 'Web', 
        email: 'cuong.le@email.com',
        experience: 4,
        skills: ['Python', 'Machine Learning', 'SQL']
      },
      { 
        id: 'c4', 
        name: 'Phạm Thị Dung', 
        title: 'React Native Developer', 
        source: 'Nguồn nhân tài', 
        email: 'dung.pham@email.com',
        experience: 2,
        skills: ['React Native', 'JavaScript', 'iOS']
      },
      { 
        id: 'c5', 
        name: 'Hoàng Minh Tú', 
        title: 'Backend Engineer', 
        source: 'ATS', 
        email: 'tu.hoang@email.com',
        experience: 6,
        skills: ['Java', 'Spring Boot', 'PostgreSQL']
      },
      { 
        id: 'c6', 
        name: 'Võ Thị Hương', 
        title: 'Frontend Developer', 
        source: 'Web', 
        email: 'huong.vo@email.com',
        experience: 3,
        skills: ['Vue.js', 'CSS', 'Figma']
      }
    ]
    
    // Filter based on source
    const sourceMap = {
      'pool': 'Nguồn nhân tài',
      'ats': 'ATS', 
      'web': 'Web'
    }
    
    let filteredCandidates = mockCandidates
    
    // Filter by source
    if (source && sourceMap[source]) {
      filteredCandidates = filteredCandidates.filter(candidate => 
        candidate.source === sourceMap[source]
      )
    }
    
    // Apply config filters for pool source
    if (source === 'pool' && configData) {
      if (configData.skills) {
        const searchSkills = configData.skills.toLowerCase().split(',').map(s => s.trim())
        filteredCandidates = filteredCandidates.filter(candidate =>
          candidate.skills.some(skill => 
            searchSkills.some(searchSkill => 
              skill.toLowerCase().includes(searchSkill)
            )
          )
        )
      }
      
      if (configData.experience) {
        const minExp = parseInt(configData.experience)
        if (!isNaN(minExp)) {
          filteredCandidates = filteredCandidates.filter(candidate => 
            candidate.experience >= minExp
          )
        }
      }
    }
    
    return filteredCandidates
  } catch (error) {
    console.error('Service error searching candidates:', error)
    return []
  }
}

// Format ngày tháng hiển thị
export const formatCampaignDate = (dateString) => {
  if (!dateString) return 'Chưa xác định'
  
  const date = new Date(dateString)
  return date.toLocaleDateString('vi-VN', {
    year: 'numeric',
    month: '2-digit', 
    day: '2-digit'
  })
}

// Tính trạng thái campaign dựa trên ngày và is_active
export const getCampaignStatusByDate = (startDate, endDate, currentStatus, isActive) => {
  if (!isActive) return 'PAUSED'
  if (currentStatus === 'DRAFT') return 'DRAFT'
  if (currentStatus === 'ARCHIVED') return 'ARCHIVED'
  
  const now = new Date()
  const start = startDate ? new Date(startDate) : null
  const end = endDate ? new Date(endDate) : null
  
  if (start && end) {
    if (now < start) return 'DRAFT' // Chưa đến ngày bắt đầu
    if (now > end) return 'ARCHIVED' // Đã qua ngày kết thúc
    return 'ACTIVE' // Đang trong thời gian hoạt động
  }
  
  return currentStatus
}

// Validate campaign form data
export const validateCampaignForm = (formData) => {
  const errors = {}
  
  if (!formData.campaign_name || !formData.campaign_name.trim()) {
    errors.campaign_name = 'Tên chiến dịch là bắt buộc'
  } else if (formData.campaign_name.length < 3) {
    errors.campaign_name = 'Tên chiến dịch phải có ít nhất 3 ký tự'
  }
  
  if (formData.start_date && formData.end_date) {
    const startDate = new Date(formData.start_date)
    const endDate = new Date(formData.end_date)
    if (startDate >= endDate) {
      errors.end_date = 'Ngày kết thúc phải sau ngày bắt đầu'
    }
  }
  
  return errors
} 