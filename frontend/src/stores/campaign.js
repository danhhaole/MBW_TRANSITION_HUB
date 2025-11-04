import { defineStore } from 'pinia'
import { call } from 'frappe-ui'
import { debugApiCall } from '@/utils/debugApi'

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
    loadingOptions: false,
    // Statistics
    statistics: {
      total: 0,
      active: 0,
      draft: 0,
      paused: 0,
      archived: 0
    }
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

        // Try the new combined API first, fallback to old API if it fails
        let result
        try {
          result = await call('mbw_mira.api.doc.get_list_data', {
            doctype: "Mira Campaign",
            fields: ['*'],
            filters: options.filters,
            or_filters: options.or_filters,
            limit_page_length: options.page_length,
            limit_start: options.start,
            order_by: 'creation desc'
          })
          
          if (result && result.success && Array.isArray(result.data)) {
            // Add computed fields
            this.campaigns = result.data.map(campaign => ({
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
            
            // Update pagination info with correct total count
            const total = result.count || 0
            this.pagination = {
              page,
              limit,
              total,
              pages: Math.ceil(total / limit),
              has_next: page * limit < total,
              has_prev: page > 1,
              showing_from: total > 0 ? (page - 1) * limit + 1 : 0,
              showing_to: Math.min(page * limit, total)
            }
            
            return { data: result.data, pagination: this.pagination, count: result.count }
          } else {
            throw new Error('New API returned invalid response')
          }
        } catch (newApiError) {
          console.warn('New API failed, falling back to old API:', newApiError.message)
          
          // Fallback to old separate API calls
          const [response, countResult] = await Promise.all([
            call('frappe.client.get_list', {
              doctype: "Mira Campaign",
              fields: ['*'],
              filters: options.filters,
              or_filters: options.or_filters,
              page_length: options.page_length,
              start: options.start,
              order_by: 'creation desc'
            }),
            call('frappe.client.get_count', {
              doctype: "Mira Campaign",
              filters: options.filters,
              or_filters: options.or_filters
            })
          ])

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
            
            // Update pagination info with correct total count
            const total = countResult || 0
            this.pagination = {
              page,
              limit,
              total,
              pages: Math.ceil(total / limit),
              has_next: page * limit < total,
              has_prev: page > 1,
              showing_from: total > 0 ? (page - 1) * limit + 1 : 0,
              showing_to: Math.min(page * limit, total)
            }
            
            return { data: response, pagination: this.pagination, count: countResult }
          }
        }

        return { success: false, message: 'No data received' }
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
          doctype: "Mira Campaign",
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

        console.log('🚀 Calling API with data:', {
          doctype: "Mira Campaign",
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
          ...formData
        })

        try {
          const response = await debugApiCall('frappe.client.insert', {
            doc: {
              doctype: "Mira Campaign",
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
              criteria: formData.criteria || null, // Add criteria field
              ...formData // Include any additional fields
            }
          })

          console.log('✅ API Response received:', response)
          console.log('Response type:', typeof response)
          console.log('Response keys:', response ? Object.keys(response) : 'null')

          if (response && response.name) {
            this.success = true
            return {
              success: true,
              data: response
            }
          } else {
            throw new Error('Không thể tạo campaign - Invalid response')
          }
        } catch (apiError) {
          console.error('❌ API Error details:', {
            error: apiError,
            message: apiError?.message,
            stack: apiError?.stack,
            response: apiError?.response,
            status: apiError?.status
          })
          
          // Handle different types of errors
          if (apiError?.message?.includes('exc_type')) {
            throw new Error('Server error occurred: ' + apiError.message)
          } else if (apiError?.response?.data?.message) {
            throw new Error(apiError.response.data.message)
          } else if (apiError?.message) {
            throw new Error(apiError.message)
          } else {
            throw new Error('Không thể tạo campaign - Network or server error')
          }
        }
      } catch (error) {
        this.error = error.message
        console.error('Failed to create campaign:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // Test method to check API connection
    async testApiConnection() {
      try {
        console.log('🧪 Testing API connection...')
        const response = await call('frappe.client.get_list', {
          doctype: 'Mira Campaign',
          limit_page_length: 1
        })
        console.log('✅ API connection test successful:', response)
        return true
      } catch (error) {
        console.error('❌ API connection test failed:', error)
        return false
      }
    },

    // Alternative create method using custom API endpoint
    async createCampaignViaCustomAPI(formData) {
      this.setLoading(true)
      
      try {
        console.log('🔄 Using custom API endpoint...')
        
        const response = await debugApiCall('mbw_mira.api.campaign.create_campaign', {
          campaign_data: {
            campaign_name: formData.campaign_name?.trim(),
            description: formData.description || '',
            type: formData.type || 'NURTURING',
            status: formData.status || 'DRAFT',
            is_active: formData.is_active || 0,
            start_date: formData.start_date || null,
            end_date: formData.end_date || null,
            target_segment: formData.target_segment || null,
            job_opening: formData.job_opening || null,
            criteria: formData.criteria || null, // Add criteria field
            source_type: formData.source_type || 'Search',
            ...formData
          }
        })

        console.log('✅ Custom API response:', response)
        
        if (response && (response.name || response.success)) {
          this.success = true
          return {
            success: true,
            data: response.data || response
          }
        } else {
          throw new Error('Invalid response from custom API')
        }
      } catch (error) {
        console.error('❌ Custom API failed, falling back to direct insert...')
        // Fallback to direct insert
        return await this.submitNewCampaign(formData)
      } finally {
        this.setLoading(false)
      }
    },

    // Update campaign
    async updateCampaignData(name, formData) {
      console.log('📋 updateCampaignData received formData:', formData)
      
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
          campaign_name: formData.campaign_name?.trim(),
          description: formData.description || '',
          is_active: formData.is_active || 0,
          owner_id: formData.owner_id || null,
          start_date: formData.start_date || null,
          end_date: formData.end_date || null,
          type: formData.type || 'NURTURING',
          status: formData.status || 'DRAFT',
          target_segment: formData.target_segment || null,
          job_opening: formData.job_opening || null,
          criteria: formData.criteria || null, // Add criteria field
          // Add missing source fields
          source_type: formData.source_type || 'Gathering',
          source_file: formData.source_file || null,
          source_config: formData.source_config || null,
          data_source_id: formData.data_source_id || null,
          // Add template and steps fields
          template_used: formData.template_used || null,
          steps_count: formData.steps_count || null,
          select_pages: formData.select_pages || null,
          // Add social media fields
          social_page_id: formData.social_page_id || null,
          social_page_name: formData.social_page_name || null,
          post_schedule_time: formData.post_schedule_time || null,
          template_content: formData.template_content || null,
          social_media_images: formData.social_media_images || null,
          mira_talent_campaign: formData.mira_talent_campaign || null,
          // Add source target for file imports
          source_target: formData.source_target || null
        }

        console.log('🚀 Sending updateData to API:', updateData)
        console.log('🎯 source_type being sent:', updateData.source_type)
        console.log('📁 source_file being sent:', updateData.source_file)

        const response = await call('frappe.client.set_value', {
          doctype: "Mira Campaign",
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
        console.error('❌ Failed to update campaign:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // Update campaign basic info (for CampaignForm modal)
    async updateCampaignBasicInfo(name, formData) {
      console.log('📋 updateCampaignBasicInfo received formData:', formData)
      
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
          campaign_name: formData.campaign_name?.trim(),
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

        console.log('🚀 Sending basic updateData to API:', updateData)

        const response = await call('frappe.client.set_value', {
          doctype: "Mira Campaign",
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
        console.error('❌ Failed to update campaign basic info:', error)
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

        // Try using new API that handles links
        const response = await call('mbw_mira.api.campaign.delete_campaign_with_links', {
          campaign_name: name,
          force_delete: false
        })
        
        if (response && response.status === 'success') {
          return response
        } else if (response && response.error_type === 'LinkExistsError') {
          // Return the error with linked documents info
          const error = new Error(response.message)
          error.linkedDocuments = response.linked_documents
          error.errorType = 'LinkExistsError'
          throw error
        } else {
          throw new Error(response.message || 'Failed to delete campaign')
        }
      } catch (error) {
        this.error = `Không thể xóa chiến dịch "${campaignName}"`
        console.error('Failed to delete campaign:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // Force delete campaign with all linked documents
    async forceRemoveCampaign(name, campaignName) {
      try {
        this.loading = true
        this.error = null

        const response = await call('mbw_mira.api.campaign.delete_campaign_with_links', {
          campaign_name: name,
          force_delete: true
        })
        
        if (response && response.status === 'success') {
          return response
        } else {
          throw new Error(response.message || 'Failed to delete campaign')
        }
      } catch (error) {
        this.error = `Không thể xóa chiến dịch "${campaignName}"`
        console.error('Failed to force delete campaign:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // Fetch statistics
    async fetchStatistics() {
      try {
        // Try new API first - get all campaigns to calculate statistics
        try {
          const result = await call('mbw_mira.api.doc.get_list_data', {
            doctype: 'Mira Campaign',
            fields: ['status', 'is_active'],
            limit_page_length: 1000
          })

          if (result && result.success) {
            // Count by status
            const statusCounts = { active: 0, draft: 0, paused: 0, archived: 0 }
            if (result.data && Array.isArray(result.data)) {
              result.data.forEach(item => {
                // Use displayStatus logic to get accurate status
                const displayStatus = this.getCampaignStatusByDate(
                  item.start_date, 
                  item.end_date, 
                  item.status,
                  item.is_active
                ).toLowerCase()
                
                if (statusCounts.hasOwnProperty(displayStatus)) {
                  statusCounts[displayStatus]++
                }
              })
            }

            this.statistics = {
              total: result.count || 0,
              ...statusCounts
            }
            return this.statistics
          } else {
            throw new Error('New API returned invalid response')
          }
        } catch (newApiError) {
          console.warn('New API failed for statistics, falling back to old API:', newApiError.message)
          
          // Fallback to old separate API calls
          const [totalResult, activeResult, draftResult, pausedResult, archivedResult] = await Promise.all([
            call('frappe.client.get_count', { doctype: 'Mira Campaign' }),
            call('frappe.client.get_count', { doctype: 'Mira Campaign', filters: { status: 'ACTIVE', is_active: 1 } }),
            call('frappe.client.get_count', { doctype: 'Mira Campaign', filters: { status: 'DRAFT' } }),
            call('frappe.client.get_count', { doctype: 'Mira Campaign', filters: { status: 'PAUSED' } }),
            call('frappe.client.get_count', { doctype: 'Mira Campaign', filters: { status: 'ARCHIVED' } })
          ])

          this.statistics = {
            total: totalResult || 0,
            active: activeResult || 0,
            draft: draftResult || 0,
            paused: pausedResult || 0,
            archived: archivedResult || 0
          }
          return this.statistics
        }
      } catch (error) {
        console.error('Error fetching statistics:', error)
        return this.statistics
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
          doctype: "Mira Job Opening",
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
    },

    // Create or update Mira Flow for campaign
    async createOrUpdateCampaignFlow(campaignId, campaignData) {
      try {
        // Check if flow already exists for this campaign
        const existingFlows = await call('frappe.client.get_list', {
          doctype: 'Mira Flow',
          filters: {
            campaign_id: campaignId,
            type: 'Campaign'
          },
          fields: ['name'],
          limit: 1
        })
        
        const flowExists = existingFlows && existingFlows.length > 0
        const flowId = flowExists ? existingFlows[0].name : null
        
        // Prepare action parameters based on interaction method
        const actionParameters = {}
        
        console.log('🔍 Preparing action parameters for:', campaignData.interaction_method)
        console.log('🔍 campaignData:', {
          message_content: campaignData.message_content,
          action_buttons: campaignData.action_buttons,
          email_subject: campaignData.email_subject,
          email_content: campaignData.email_content
        })
        
        if (campaignData.interaction_method === 'EMAIL') {
          actionParameters.subject = campaignData.email_subject || ''
          actionParameters.content = campaignData.email_content || ''
          actionParameters.attachments = campaignData.attachments || []
        } else if (campaignData.interaction_method === 'ZALO_ZNS' || campaignData.interaction_method === 'SMS') {
          // ZNS and SMS use blocks structure from ZaloEditor
          actionParameters.blocks = campaignData.blocks || []
          console.log('🔍 ZNS/SMS actionParameters:', actionParameters)
        } else if (campaignData.interaction_method === 'ZALO_CARE') {
          // ZALO_CARE also uses blocks structure
          actionParameters.blocks = campaignData.blocks || []
          actionParameters.image_url = campaignData.image_url || ''
        }
        
        console.log('🔍 Final actionParameters:', actionParameters)
        
        // Helper to convert interaction method to channel
        const getChannelFromInteractionMethod = (method) => {
          const channelMap = {
            'EMAIL': 'Email',
            'ZALO_ZNS': 'SMS',
            'ZALO_CARE': 'Zalo',
            'SMS': 'SMS',
            'AI_CALL': 'AI_Call'
          }
          return channelMap[method] || 'Email'
        }
        
        // Helper to convert trigger key to trigger_type
        const getTriggerTypeFromKey = (key) => {
          const typeMap = {
            'email_open': 'ON_EMAIL_OPEN',
            'link_click': 'ON_LINK_CLICK',
            'send_success': 'ON_SEND_SUCCESS',
            'send_failed': 'ON_SEND_FAILED',
            'user_response': 'ON_USER_RESPONSE'
          }
          return typeMap[key] || 'CUSTOM_EVENT'
        }
        
        // Helper to convert action type to backend format
        const normalizeActionType = (type) => {
          if (!type) return ''
          
          // Map frontend action types to backend enum values
          const actionTypeMap = {
            'add_tag': 'ADD_TAG',
            'remove_tag': 'REMOVE_TAG',
            'add_to_sequence': 'SUBSCRIBE_TO_SEQUENCE',
            'subscribe_to_sequence': 'SUBSCRIBE_TO_SEQUENCE',
            'unsubscribe_from_sequence': 'UN_SUBSCRIBE_TO_SEQUENCE',
            'un_subscribe_to_sequence': 'UN_SUBSCRIBE_TO_SEQUENCE',
            'start_flow': 'START_FLOW',
            'next_flow': 'START_FLOW', // next_flow in UI maps to START_FLOW
            'add_custom_field': 'ADD_CUSTOM_FIELD',
            'remove_custom_field': 'REMOVE_CUSTOM_FIELD',
            'update_field': 'ADD_CUSTOM_FIELD', // Update field is same as add custom field
            'lead_score': 'LEAD_SCORE',
            'external_request': 'EXTERNAL_REQUEST',
            'smart_delay': 'SMART_DELAY',
            'message': 'MESSAGE',
            'sms': 'SMS',
            'email': 'EMAIL',
            'send_email': 'EMAIL', // Send email maps to EMAIL
            'send_sms': 'SMS', // Send SMS maps to SMS
            'send_message': 'MESSAGE', // Send message maps to MESSAGE
            'zalo': 'ZALO',
            'zalo_care': 'ZALO_CARE',
            'zalo_zns': 'ZALO_ZNS',
            'send_zalo': 'ZALO', // Send zalo maps to ZALO
            'ai_call': 'AI_CALL',
            'email_ai': 'EMAIL_AI',
            'content_ai': 'CONTENT_AI',
            'sent_notification': 'SENT_NOTIFICATION',
            'send_notification': 'SENT_NOTIFICATION' // Send notification maps to SENT_NOTIFICATION
          }
          
          // If already uppercase, check if it needs mapping
          if (type === type.toUpperCase()) {
            // Check common uppercase variations
            const upperMap = {
              'SEND_EMAIL': 'EMAIL',
              'SEND_SMS': 'SMS',
              'SEND_MESSAGE': 'MESSAGE',
              'SEND_ZALO': 'ZALO',
              'SEND_NOTIFICATION': 'SENT_NOTIFICATION'
            }
            return upperMap[type] || type
          }
          
          // Convert to lowercase for lookup
          const lowerType = type.toLowerCase()
          return actionTypeMap[lowerType] || type.toUpperCase()
        }
        
        // Prepare flow data
        const flowData = {
          title: campaignData.campaign_name || 'Campaign Flow',
          type: 'Campaign',
          campaign_id: campaignId,
          channel: getChannelFromInteractionMethod(campaignData.interaction_method),
          status: 'Draft',
          // Action will be set later (reuse existing or create new)
          action_id: []
        }
        
        // Prepare new action data
        const newAction = {
          doctype: 'Mira Flow Action',
          action_type: campaignData.interaction_method || 'EMAIL',
          channel_type: getChannelFromInteractionMethod(campaignData.interaction_method),
          action_parameters: JSON.stringify(actionParameters),
          order: 0
        }
        
        // Convert additional_actions to triggers and their actions
        if (campaignData.additional_actions && Object.keys(campaignData.additional_actions).length > 0) {
          // Create triggers (without action data in conditions)
          flowData.trigger_id = Object.entries(campaignData.additional_actions).map(([triggerKey, actionData]) => ({
            doctype: 'Mira Flow Trigger',
            trigger_type: getTriggerTypeFromKey(triggerKey),
            status: 'ACTIVE',
            channel: flowData.channel,
            conditions: null // Don't store action data here anymore
          }))
          
          // Create actions for each trigger (if configured)
          flowData.trigger_actions = Object.entries(campaignData.additional_actions)
            .filter(([triggerKey, actionData]) => actionData.configured && actionData.type)
            .map(([triggerKey, actionData]) => ({
              doctype: 'Mira Flow Action',
              trigger_type: getTriggerTypeFromKey(triggerKey), // Temporary key to link later
              action_type: normalizeActionType(actionData.type),
              channel_type: flowData.channel,
              action_parameters: JSON.stringify(actionData.data || {}),
              order: 0
            }))
          
          console.log('🔍 Converted additional_actions to triggers:', flowData.trigger_id)
          console.log('🔍 Converted additional_actions to trigger actions:', flowData.trigger_actions)
        } else {
          // If no additional_actions, set empty arrays
          flowData.trigger_id = []
          flowData.trigger_actions = []
          console.log('🔍 No additional_actions, will delete all triggers and actions')
        }
        
        let result
        if (flowExists) {
          // Update existing flow
          const existingFlow = await call('frappe.client.get', {
            doctype: 'Mira Flow',
            name: flowId
          })
          
          console.log('🔍 Existing flow:', existingFlow)
          console.log('🔍 Existing action_id:', existingFlow.action_id)
          console.log('🔍 Existing trigger_id:', existingFlow.trigger_id)
          
          // STEP 1: Prepare main action (campaign email/zalo action)
          let mainAction
          const existingMainAction = (existingFlow.action_id || []).find(a => !a.trigger_id)
          if (existingMainAction) {
            console.log('♻️ Reusing existing main action:', existingMainAction.name)
            mainAction = {
              ...existingMainAction,
              ...newAction,
              name: existingMainAction.name
            }
          } else {
            console.log('✨ Creating new main action')
            mainAction = newAction
          }
          
          // STEP 2: Create map of existing triggers by trigger_type
          const existingTriggerMap = {}
          ;(existingFlow.trigger_id || []).forEach(trigger => {
            existingTriggerMap[trigger.trigger_type] = trigger
          })
          
          // STEP 3: Process triggers - separate new and existing
          const finalTriggers = []
          const newTriggersToCreate = []
          
          ;(flowData.trigger_id || []).forEach((newTrigger) => {
            const existingTrigger = existingTriggerMap[newTrigger.trigger_type]
            
            if (existingTrigger) {
              // Reuse existing trigger
              console.log('♻️ Reusing existing trigger:', existingTrigger.name, newTrigger.trigger_type)
              finalTriggers.push({
                ...existingTrigger,
                ...newTrigger,
                name: existingTrigger.name
              })
            } else {
              // Mark as new trigger (will be created)
              console.log('✨ New trigger to create:', newTrigger.trigger_type)
              finalTriggers.push(newTrigger)
              newTriggersToCreate.push(newTrigger.trigger_type)
            }
          })
          
          // STEP 4: First save - update triggers
          const updatedDoc = {
            ...existingFlow,
            title: flowData.title,
            type: flowData.type,
            campaign_id: flowData.campaign_id,
            channel: flowData.channel,
            status: flowData.status,
            // Keep existing actions for now
            action_id: existingFlow.action_id || [],
            // Update triggers
            trigger_id: finalTriggers
          }
          
          console.log('📝 Step 1: Saving triggers first')
          console.log('📝 Triggers to save:', finalTriggers)
          
          console.log('📝 Updating flow with data:', updatedDoc)
          console.log('📝 Action parameters:', actionParameters)
          console.log('📝 action_id to save (combined):', updatedDoc.action_id)
          console.log('📝 Number of actions:', updatedDoc.action_id.length)
          
          result = await call('frappe.client.save', {
            doc: updatedDoc
          })
          
          console.log('✅ Step 1 complete - Triggers saved:', result)
          
          // STEP 5: Get updated flow to get trigger names (especially for new triggers)
          const updatedFlow = await call('frappe.client.get', {
            doctype: 'Mira Flow',
            name: flowId
          })
          
          console.log('🔍 Updated flow with trigger names:', updatedFlow.trigger_id)
          
          // STEP 6: Build trigger map with names
          const updatedTriggerMap = {}
          ;(updatedFlow.trigger_id || []).forEach(trigger => {
            updatedTriggerMap[trigger.trigger_type] = trigger
          })
          
          // STEP 7: Process actions - link with triggers
          const finalActions = [mainAction] // Start with main action
          
          // Get list of trigger types that should have actions (configured ones)
          const configuredTriggerTypes = (flowData.trigger_actions || []).map(a => a.trigger_type)
          
          // Keep existing trigger actions that still have triggers (even if not in flowData.trigger_actions)
          // This prevents deleting actions when user just adds a new trigger without configuring it
          ;(updatedFlow.action_id || []).forEach(existingAction => {
            if (existingAction.trigger_id) {
              // Find the trigger for this action
              const trigger = (updatedFlow.trigger_id || []).find(t => t.name === existingAction.trigger_id)
              
              if (trigger) {
                // Check if this trigger type is being updated
                const newActionData = (flowData.trigger_actions || []).find(
                  a => a.trigger_type === trigger.trigger_type
                )
                
                if (newActionData) {
                  // Update existing action with new data
                  console.log('♻️ Updating existing trigger action:', existingAction.name, trigger.trigger_type)
                  finalActions.push({
                    ...existingAction,
                    ...newActionData,
                    name: existingAction.name,
                    trigger_id: trigger.name
                  })
                } else {
                  // Keep existing action as-is (trigger still exists but no new data)
                  console.log('♻️ Keeping existing trigger action:', existingAction.name, trigger.trigger_type)
                  finalActions.push(existingAction)
                }
              } else {
                // Trigger was deleted, don't include this action
                console.log('🗑️ Removing action for deleted trigger:', existingAction.trigger_id)
              }
            }
          })
          
          // Add new trigger actions (for triggers that don't have actions yet)
          ;(flowData.trigger_actions || []).forEach((triggerAction) => {
            const trigger = updatedTriggerMap[triggerAction.trigger_type]
            
            if (!trigger) {
              console.warn('⚠️ No trigger found for action:', triggerAction.trigger_type)
              return
            }
            
            // Check if we already processed this action above
            const alreadyProcessed = finalActions.some(a => a.trigger_id === trigger.name)
            
            if (!alreadyProcessed) {
              console.log('✨ Creating new trigger action for:', triggerAction.trigger_type)
              const action = {
                ...triggerAction,
                trigger_id: trigger.name
              }
              delete action.trigger_type // Remove temporary key
              finalActions.push(action)
            }
          })
          
          // STEP 8: Final save - update actions
          console.log('📝 Step 2: Saving actions with trigger_id links')
          console.log('📝 Final actions:', finalActions)
          
          result = await call('frappe.client.save', {
            doc: {
              ...updatedFlow,
              action_id: finalActions
            }
          })
          
          console.log('✅ Step 2 complete - Actions saved with trigger links')
        } else {
          // Create new flow
          console.log('✨ Creating new flow')
          
          // First, create flow with main action and triggers
          result = await call('frappe.client.insert', {
            doc: {
              doctype: 'Mira Flow',
              ...flowData,
              action_id: [newAction], // Main action only
              trigger_id: flowData.trigger_id || []
            }
          })
          
          console.log('✅ Created new flow:', result)
          
          // If there are trigger actions, update flow to add them with trigger_id links
          if (flowData.trigger_actions && flowData.trigger_actions.length > 0) {
            console.log('🔗 Linking trigger actions to triggers')
            
            // Get the created flow to get trigger names
            const createdFlow = await call('frappe.client.get', {
              doctype: 'Mira Flow',
              name: result.name
            })
            
            // Create map of triggers by trigger_type
            const triggerMap = {}
            ;(createdFlow.trigger_id || []).forEach(trigger => {
              triggerMap[trigger.trigger_type] = trigger
            })
            
            // Create actions with trigger_id links
            const triggerActions = flowData.trigger_actions.map(action => {
              const trigger = triggerMap[action.trigger_type]
              const linkedAction = {
                ...action,
                trigger_id: trigger?.name // Link to created trigger
              }
              delete linkedAction.trigger_type // Remove temporary key
              return linkedAction
            })
            
            console.log('📝 Trigger actions to add:', triggerActions)
            
            // Update flow with trigger actions
            result = await call('frappe.client.save', {
              doc: {
                ...createdFlow,
                action_id: [...createdFlow.action_id, ...triggerActions]
              }
            })
            
            console.log('✅ Updated flow with trigger actions')
          }
        }
        
        console.log('✅ Campaign flow saved:', result)
        return { success: true, data: result }
      } catch (error) {
        console.error('❌ Error saving campaign flow:', error)
        return { success: false, error: error.message }
      }
    },

    // Load campaign flow data
    async loadCampaignFlow(campaignId, interactionMethod) {
      try {
        const flows = await call('frappe.client.get_list', {
          doctype: 'Mira Flow',
          filters: {
            campaign_id: campaignId,
            type: 'Campaign'
          },
          fields: ['name'],
          limit: 1
        })
        
        if (!flows || flows.length === 0) {
          return { success: false, message: 'No flow found' }
        }
        
        const flowDoc = await call('frappe.client.get', {
          doctype: 'Mira Flow',
          name: flows[0].name
        })
        
        console.log('📖 Loading content from Flow:', flowDoc)
        console.log('📖 Flow action_id:', flowDoc.action_id)
        
        const contentData = {}
        
        // Parse action parameters
        if (flowDoc.action_id && flowDoc.action_id.length > 0) {
          const mainAction = flowDoc.action_id[0]
          console.log('📖 Main action:', mainAction)
          console.log('📖 Action parameters (raw):', mainAction.action_parameters)
          
          // Use action_type from flow if interactionMethod is not provided
          const methodToUse = interactionMethod || mainAction.action_type
          console.log('📖 Interaction method (param):', interactionMethod)
          console.log('📖 Action type (from flow):', mainAction.action_type)
          console.log('📖 Method to use:', methodToUse)
          
          // Return interaction_method so caller can use it
          contentData.interaction_method = mainAction.action_type
          
          try {
            const params = JSON.parse(mainAction.action_parameters || '{}')
            console.log('📖 Parsed params:', params)
            
            if (methodToUse === 'EMAIL') {
              contentData.email_subject = params.subject || ''
              contentData.email_content = params.content || ''
              contentData.attachments = params.attachments || []
              console.log('📖 Set email data:', { 
                email_subject: contentData.email_subject, 
                email_content: contentData.email_content 
              })
            } else if (methodToUse === 'ZALO_ZNS' || methodToUse === 'SMS') {
              // ZNS and SMS use blocks structure
              contentData.blocks = params.blocks || []
              console.log('📖 Set ZNS/SMS data:', { 
                blocks: contentData.blocks 
              })
            } else if (methodToUse === 'ZALO_CARE') {
              // ZALO_CARE uses blocks structure
              contentData.blocks = params.blocks || []
              contentData.image_url = params.image_url || ''
              console.log('📖 Set Zalo Care data:', { 
                blocks: contentData.blocks,
                image_url: contentData.image_url 
              })
            }
          } catch (e) {
            console.error('❌ Failed to parse action parameters:', e)
            console.error('❌ Raw action_parameters:', mainAction.action_parameters)
          }
        }
        
        // Parse triggers and their actions to additional_actions
        if (flowDoc.trigger_id && flowDoc.trigger_id.length > 0) {
          const additionalActions = {}
          
          // Helper to convert trigger_type back to key
          const getTriggerKeyFromType = (triggerType) => {
            const keyMap = {
              'ON_EMAIL_OPEN': 'email_open',
              'ON_LINK_CLICK': 'link_click',
              'ON_SEND_SUCCESS': 'send_success',
              'ON_SEND_FAILED': 'send_failed',
              'ON_USER_RESPONSE': 'user_response'
            }
            return keyMap[triggerType]
          }
          
          // Helper to convert action_type back to frontend format
          const denormalizeActionType = (type) => {
            const typeMap = {
              'ADD_TAG': 'add_tag',
              'REMOVE_TAG': 'remove_tag',
              'SUBSCRIBE_TO_SEQUENCE': 'add_to_sequence',
              'UN_SUBSCRIBE_TO_SEQUENCE': 'unsubscribe_from_sequence',
              'START_FLOW': 'next_flow', // START_FLOW in UI is "next_flow"
              'ADD_CUSTOM_FIELD': 'update_field',
              'REMOVE_CUSTOM_FIELD': 'remove_custom_field',
              'LEAD_SCORE': 'lead_score',
              'EXTERNAL_REQUEST': 'external_request',
              'SMART_DELAY': 'smart_delay',
              'MESSAGE': 'message',
              'SMS': 'sms',
              'EMAIL': 'send_email', // EMAIL action in trigger context is "send_email"
              'ZALO': 'zalo',
              'ZALO_CARE': 'zalo_care',
              'ZALO_ZNS': 'zalo_zns',
              'AI_CALL': 'ai_call',
              'EMAIL_AI': 'email_ai',
              'CONTENT_AI': 'content_ai',
              'SENT_NOTIFICATION': 'sent_notification'
            }
            return typeMap[type] || type.toLowerCase()
          }
          
          // Create map of actions by trigger_id
          const actionsByTriggerId = {}
          ;(flowDoc.action_id || []).forEach(action => {
            if (action.trigger_id) {
              actionsByTriggerId[action.trigger_id] = action
            }
          })
          
          console.log('📖 Actions by trigger_id:', actionsByTriggerId)
          
          // Build additional_actions from triggers and their actions
          flowDoc.trigger_id.forEach(trigger => {
            try {
              const triggerKey = getTriggerKeyFromType(trigger.trigger_type)
              if (!triggerKey) {
                console.warn('⚠️ Unknown trigger type:', trigger.trigger_type)
                return
              }
              
              // Find action for this trigger
              const triggerAction = actionsByTriggerId[trigger.name]
              
              if (triggerAction) {
                // Parse action parameters
                const actionParams = JSON.parse(triggerAction.action_parameters || '{}')
                
                additionalActions[triggerKey] = {
                  type: denormalizeActionType(triggerAction.action_type),
                  data: actionParams,
                  configured: true // If action exists, it's configured
                }
                
                console.log('✅ Loaded trigger action:', triggerKey, additionalActions[triggerKey])
              } else {
                // Trigger exists but no action configured yet
                additionalActions[triggerKey] = {
                  type: '',
                  data: {},
                  configured: false
                }
                
                console.log('⚠️ Trigger without action:', triggerKey)
              }
            } catch (e) {
              console.error('❌ Failed to parse trigger:', trigger, e)
            }
          })
          
          contentData.additional_actions = additionalActions
          console.log('📖 Final additional_actions:', additionalActions)
        }
        
        console.log('✅ Content loaded from Flow')
        console.log('✅ Final contentData:', contentData)
        return { success: true, data: contentData }
      } catch (error) {
        console.error('❌ Error loading campaign flow:', error)
        return { success: false, error: error.message }
      }
    }
  }
})
