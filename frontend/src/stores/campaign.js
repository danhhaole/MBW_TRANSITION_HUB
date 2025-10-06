import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useCampaignStore = defineStore('campaign', {
  state: () => ({
    campaigns: [],
    currentCampaign: null,
    loading: false,
    error: null,
    success: false,
    // Pagination state
    pagination: {
      page: 1,
      limit: 10,
      total: 0,
      pages: 1,
      has_next: false,
      has_prev: false,
      showing_from: 0,
      showing_to: 0
    },
    // Filter state
    searchText: '',
    statusFilter: 'all',
    typeFilter: 'all',
    activeFilter: 'all',
    // Options data
    users: [],
    talentSegments: [],
    jobOpenings: [],
    loadingOptions: false
  }),

  getters: {
    // Client-side filtered campaigns
    filteredCampaigns: (state) => {
      let filtered = state.campaigns

      if (state.searchText) {
        filtered = filtered.filter(campaign => 
          campaign.campaign_name.toLowerCase().includes(state.searchText.toLowerCase()) ||
          campaign.description?.toLowerCase().includes(state.searchText.toLowerCase())
        )
      }

      if (state.statusFilter && state.statusFilter !== 'all') {
        filtered = filtered.filter(campaign => campaign.status === state.statusFilter)
      }

      if (state.typeFilter && state.typeFilter !== 'all') {
        filtered = filtered.filter(campaign => campaign.type === state.typeFilter)
      }

      if (state.activeFilter !== 'all') {
        const isActive = state.activeFilter === 'active'
        filtered = filtered.filter(campaign => campaign.is_active === (isActive ? 1 : 0))
      }

      return filtered
    }
  },

  actions: {
    // Reset state
    resetState() {
      this.error = null
      this.success = false
      this.loading = false
    },

    // Set filters
    setSearchText(text) {
      this.searchText = text
    },

    setStatusFilter(status) {
      this.statusFilter = status
    },

    setTypeFilter(type) {
      this.typeFilter = type
    },

    setActiveFilter(active) {
      this.activeFilter = active
    },

    // Load campaigns with filters and pagination
    async getFilteredCampaigns(filterOptions = {}) {
      try {
        this.loading = true
        this.error = null

        const { status, type, isActive, searchText, page = 1, limit = 20 } = filterOptions
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

        let options = {
          filters,
          page_length: limit,
          start: (page - 1) * limit,
          or_filters: undefined,
        }

        if (searchText) {
          options.or_filters = [
            ['campaign_name', 'like', `%${searchText}%`],
            ['description', 'like', `%${searchText}%`]
          ]
        }

        const response = await call('frappe.client.get_list', {
          doctype: 'Campaign',
          fields: ['*'],
          filters: options.filters,
          or_filters: options.or_filters,
          page_length: options.page_length,
          start: options.start,
          order_by: 'creation desc'
        })

        if (response && Array.isArray(response)) {
          // Add computed fields
          this.campaigns = response.map(campaign => ({
            ...campaign,
            displayStatus: this.getCampaignStatusByDate(
              campaign.start_date, 
              campaign.end_date, 
              campaign.status,
              campaign.is_active
            ),
            formattedStartDate: this.formatCampaignDate(campaign.start_date),
            formattedEndDate: this.formatCampaignDate(campaign.end_date)
          }))
          
          // Update pagination info (frappe-ui doesn't return pagination, so we calculate it)
          const total = response.length
          this.pagination = {
            page,
            limit,
            total,
            pages: Math.ceil(total / limit),
            has_next: page * limit < total,
            has_prev: page > 1,
            showing_from: (page - 1) * limit + 1,
            showing_to: Math.min(page * limit, total)
          }
          
          return { data: response, pagination: this.pagination }
        } else {
          throw new Error('Không thể tải danh sách chiến dịch')
        }
      } catch (error) {
        this.error = error.message || 'Có lỗi xảy ra khi tải campaigns'
        console.error('Failed to get campaigns:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // Get campaign details
    async getCampaignDetails(name) {
      try {
        this.loading = true
        this.error = null
        
        const response = await call('frappe.client.get', {
          doctype: 'Campaign',
          name: name
        })
        console.log(response)
        if (response) {
          const campaign = {
            ...response,
            displayStatus: this.getCampaignStatusByDate(
              response.start_date, 
              response.end_date, 
              response.status,
              response.is_active
            ),
            formattedStartDate: this.formatCampaignDate(response.start_date),
            formattedEndDate: this.formatCampaignDate(response.end_date)
          }
          this.currentCampaign = campaign
          return campaign
        } else {
          throw new Error('Không thể tải thông tin chiến dịch')
        }
      } catch (error) {
        this.error = error.message || 'Không thể tải thông tin chiến dịch'
        console.error('Failed to get campaign details:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // Create new campaign with validation
    async submitNewCampaign(formData) {
      try {
        this.loading = true
        this.error = null
        this.success = false

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

        const response = await call('frappe.client.insert', {
          doc: {
            doctype: 'Campaign',
            campaign_name: formData.campaign_name.trim(),
            description: formData.description || '',
            is_active: formData.is_active || 0,
            owner_id: formData.owner_id || null,
            start_date: formData.start_date || null,
            end_date: formData.end_date || null,
            type: formData.type || 'NURTURING',
            status: formData.status || 'DRAFT',
            target_segment: formData.target_segment || null,
            job_opening: formData.job_opening || null,
            ...formData // Include any additional fields
          }
        })

        if (response) {
          this.success = true
          return response
        } else {
          throw new Error('Không thể tạo campaign')
        }
      } catch (error) {
        this.error = error.message
        console.error('Failed to create campaign:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // Update campaign
    async updateCampaignData(name, formData) {
      console.log(formData)
      try {
        this.loading = true
        this.error = null
        this.success = false


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
          target_segment: formData.target_segment || null,
          job_opening: formData.job_opening || null
        }

        const response = await call('frappe.client.set_value', {
          doctype: 'Campaign',
          name: name,
          fieldname: updateData
        })
        if (response) {
          this.success = true
          return response
        } else {
          throw new Error('Không thể cập nhật campaign')
        }
      } catch (error) {
        this.error = error.message
        console.error('Failed to update campaign:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // Delete campaign
    async removeCampaign(name, campaignName) {
      try {
        this.loading = true
        this.error = null

        const response = await call('frappe.client.delete', {
          doctype: 'Campaign',
          name: name
        })
        if (response) {
          return response
        }
      } catch (error) {
        this.error = `Không thể xóa chiến dịch "${campaignName}"`
        console.error('Failed to delete campaign:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // Load options data
    async loadOptions() {
      try {
        this.loadingOptions = true
        const [usersData, segmentsData, jobOpeningsData] = await Promise.all([
          this.getUserOptions(),
          this.getTalentSegmentOptions(),
          this.getJobOpeningOptions()
        ])
        
        this.users = usersData.map(user => ({
          label: user.full_name || user.name,
          value: user.name,
          subtitle: user.email
        }))
        
        this.talentSegments = segmentsData.map(segment => ({
          label: segment.title || segment.name,
          value: segment.name
        }))

        this.jobOpenings = jobOpeningsData.map(j => ({
          label: j.job_title || j.name,
          value: j.name
        }))
      } catch (error) {
        console.error('Failed to load options:', error)
      } finally {
        this.loadingOptions = false
      }
    },

    // Get user options
    async getUserOptions() {
      try {
        const response = await call('frappe.client.get_list', {
          doctype: 'User',
          fields: ['name', 'full_name', 'email'],
          filters: { enabled: 1 },
          limit_page_length: 1000
        })
        return Array.isArray(response) ? response : []
      } catch (error) {
        console.error('Failed to get users:', error)
        return []
      }
    },

    // Get talent segment options
    async getTalentSegmentOptions() {
      try {
        const response = await call('frappe.client.get_list', {
          doctype: 'Mira Segment',
          fields: ['name', 'title'],
          limit_page_length: 1000
        })
        return Array.isArray(response) ? response : []
      } catch (error) {
        console.error('Failed to get talent segments:', error)
        return []
      }
    },

    // Get job opening options
    async getJobOpeningOptions() {
      try {
        const response = await call('frappe.client.get_list', {
          doctype: 'JobOpening',
          fields: ['name', 'job_title'],
          limit_page_length: 1000
        })
        return Array.isArray(response) ? response : []
      } catch (error) {
        console.error('Failed to get job openings:', error)
        return []
      }
    },

    // Utility functions
    formatCampaignDate(dateString) {
      if (!dateString) return 'Chưa xác định'
      
      const date = new Date(dateString)
      return date.toLocaleDateString('vi-VN', {
        year: 'numeric',
        month: '2-digit', 
        day: '2-digit'
      })
    },

    getCampaignStatusByDate(startDate, endDate, currentStatus, isActive) {
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
    },

    // Validate campaign form data
    validateCampaignForm(formData) {
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
    },

    // Search candidates (mock function from service)
    async searchCandidates(source, configData) {
      try {
        // Mock data - same as in service
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
        console.error('Store error searching candidates:', error)
        return []
      }
    }
  }
})
