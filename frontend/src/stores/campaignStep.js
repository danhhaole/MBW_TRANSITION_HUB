import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useCampaignStepStore = defineStore('campaignStep', {
  state: () => ({
    campaignSteps: [],
    currentCampaignStep: null,
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
    // Filters
    searchText: '',
    campaignFilter: '',
    actionTypeFilter: '',
    orderBy: 'step_order asc'
  }),

  getters: {
    filteredCampaignSteps: (state) => {
      let filtered = [...state.campaignSteps]
      
      if (state.searchText) {
        const search = state.searchText.toLowerCase()
        filtered = filtered.filter(step => 
          step.step_name?.toLowerCase().includes(search) ||
          step.description?.toLowerCase().includes(search) ||
          step.action_type?.toLowerCase().includes(search)
        )
      }
      
      if (state.campaignFilter && state.campaignFilter !== 'all') {
        filtered = filtered.filter(step => step.campaign === state.campaignFilter)
      }
      
      if (state.actionTypeFilter && state.actionTypeFilter !== 'all') {
        filtered = filtered.filter(step => step.action_type === state.actionTypeFilter)
      }
      
      return filtered
    },

    totalCampaignSteps: (state) => state.campaignSteps.length,
    
    hasNextPage: (state) => state.pagination.has_next,
    hasPrevPage: (state) => state.pagination.has_prev
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

    setCampaignFilter(campaign) {
      this.campaignFilter = campaign
    },

    setActionTypeFilter(actionType) {
      this.actionTypeFilter = actionType
    },

    setOrderBy(orderBy) {
      this.orderBy = orderBy
    },

    // Get filtered campaign steps with pagination
    async getFilteredCampaignSteps(filterOptions = {}) {
      try {
        this.loading = true
        this.error = null

        const { 
          page = 1, 
          limit = 10, 
          search = '', 
          campaign = '', 
          action_type = '', 
          order_by = 'step_order asc' 
        } = filterOptions

        const response = await call('mbw_mira.mbw_mira.doctype.campaignstep.campaignstep.get_campaign_steps_paginated', {
          page,
          limit,
          search,
          campaign,
          action_type,
          order_by
        })

        if (response && response.data) {
          this.campaignSteps = response.data
          
          // Update pagination info
          this.pagination = {
            page,
            limit,
            total: response.pagination?.total || response.data.length,
            pages: response.pagination?.pages || Math.ceil(response.data.length / limit),
            has_next: response.pagination?.has_next || false,
            has_prev: response.pagination?.has_prev || false,
            showing_from: response.pagination?.showing_from || ((page - 1) * limit + 1),
            showing_to: response.pagination?.showing_to || Math.min(page * limit, response.data.length)
          }
          
          return { data: response.data, pagination: this.pagination }
        } else {
          throw new Error('Không thể tải danh sách bước chiến dịch')
        }
      } catch (error) {
        this.error = error.message || 'Có lỗi xảy ra khi tải campaign steps'
        console.error('Failed to get campaign steps:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // Get campaign step details
    async getCampaignStepDetails(name) {
      try {
        this.loading = true
        this.error = null
        
        const response = await call('frappe.client.get', {
          doctype: 'CampaignStep',
          name: name
        })
        
        if (response) {
          this.currentCampaignStep = response
          return response
        } else {
          throw new Error('Không thể tải thông tin bước chiến dịch')
        }
      } catch (error) {
        this.error = error.message || 'Không thể tải thông tin bước chiến dịch'
        console.error('Failed to get campaign step details:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // Create new campaign step
    async createCampaignStep(formData) {
      try {
        this.loading = true
        this.error = null
        this.success = false

        // Validation
        if (!formData.campaign_step_name || !formData.campaign_step_name.trim()) {
          throw new Error('Tên bước không được để trống')
        }
        if (!formData.campaign) {
          throw new Error('Chiến dịch không được để trống')
        }
        if (!formData.action_type) {
          throw new Error('Loại hành động không được để trống')
        }

        const response = await call('frappe.client.insert', {
          doc: {
            doctype: 'CampaignStep',
            campaign_step_name: formData.campaign_step_name.trim(),
            description: formData.description || '',
            campaign: formData.campaign,
            action_type: formData.action_type,
            step_order: formData.step_order || 1,
            is_active: formData.is_active !== undefined ? formData.is_active : 1,
            delay_days: formData.delay_days || 0,
            template_content: formData.template_content || '',
            action_config: JSON.stringify(formData.action_config),
            ...formData // Include any additional fields
          }
        })

        if (response) {
          this.success = true
          return response
        } else {
          throw new Error('Không thể tạo bước chiến dịch')
        }
      } catch (error) {
        this.error = error.message
        console.error('Failed to create campaign step:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // Update campaign step
    async updateCampaignStep(name, formData) {
      console.log(name)
      try {
        this.loading = true
        this.error = null
        this.success = false
        console.log(formData)
        // Validation
        if (!formData.campaign_step_name || !formData.campaign_step_name.trim()) {
          throw new Error('Tên bước không được để trống')
        }

        const updateData = {
          campaign_step_name: formData.campaign_step_name.trim(),
          description: formData.description || '',
          campaign: formData.campaign,
          action_type: formData.action_type,
          step_order: formData.step_order || 1,
          is_active: formData.is_active !== undefined ? formData.is_active : 1,
          delay_days: formData.delay_days || 0,
          template_content: formData.template_content || '',
          action_config: formData.action_config ? JSON.stringify(formData.action_config) : '',
          ...formData
        }

        const response = await call('frappe.client.set_value', {
          doctype: 'CampaignStep',
          name: name,
          fieldname: updateData
        })
        
        if (response) {
          this.success = true
          return response
        } else {
          throw new Error('Không thể cập nhật bước chiến dịch')
        }
      } catch (error) {
        this.error = error.message
        console.error('Failed to update campaign step:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // Update only step order (lightweight update)
    async updateStepOrder(name, stepOrder) {
      try {
        const response = await call('frappe.client.set_value', {
          doctype: 'CampaignStep',
          name: name,
          fieldname: 'step_order',
          value: stepOrder
        })
        return response
      } catch (error) {
        console.error('Failed to update step order:', error)
        throw error
      }
    },

    // Delete campaign step
    async deleteCampaignStep(name) {
      try {
        this.loading = true
        this.error = null

        const response = await call('frappe.client.delete', {
          doctype: 'CampaignStep',
          name: name
        })
        
        if (response) {
          return response
        }
      } catch (error) {
        this.error = `Không thể xóa bước chiến dịch "${name}"`
        console.error('Failed to delete campaign step:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // Get campaigns for dropdown
    async getCampaignOptions() {
      try {
        const response = await call('frappe.client.get_list', {
          doctype: 'Campaign',
          fields: ['name', 'campaign_name'],
          limit_page_length: 1000,
          order_by: 'campaign_name asc'
        })
        return Array.isArray(response) ? response.map(campaign => ({
          label: campaign.campaign_name || campaign.name,
          value: campaign.name
        })) : []
      } catch (error) {
        console.error('Failed to get campaign options:', error)
        return []
      }
    },

    // Utility functions
    formatStepOrder(order) {
      return order ? `Bước ${order}` : 'Chưa xác định'
    },

    getActionTypeLabel(actionType) {
      const labels = {
        'EMAIL': 'Gửi Email',
        'SMS': 'Gửi SMS',
        'CALL': 'Gọi điện',
        'MEETING': 'Cuộc họp',
        'TASK': 'Nhiệm vụ',
        'NOTE': 'Ghi chú',
        'FOLLOW_UP': 'Theo dõi'
      }
      return labels[actionType] || actionType
    },

    getActionTypeColor(actionType) {
      const colors = {
        'EMAIL': 'bg-blue-100 text-blue-800',
        'SMS': 'bg-green-100 text-green-800',
        'CALL': 'bg-yellow-100 text-yellow-800',
        'MEETING': 'bg-purple-100 text-purple-800',
        'TASK': 'bg-orange-100 text-orange-800',
        'NOTE': 'bg-gray-100 text-gray-800',
        'FOLLOW_UP': 'bg-indigo-100 text-indigo-800'
      }
      return colors[actionType] || 'bg-gray-100 text-gray-800'
    },

    // Validate campaign step form
    validateCampaignStepForm(formData) {
      const errors = {}
      
      if (!formData.campaign_step_name || !formData.campaign_step_name.trim()) {
        errors.campaign_step_name = 'Tên bước là bắt buộc'
      } else if (formData.campaign_step_name.length < 3) {
        errors.campaign_step_name = 'Tên bước phải có ít nhất 3 ký tự'
      }
      
      if (!formData.campaign) {
        errors.campaign = 'Chiến dịch là bắt buộc'
      }
      
      if (!formData.action_type) {
        errors.action_type = 'Loại hành động là bắt buộc'
      }
      
      if (formData.step_order && (isNaN(formData.step_order) || formData.step_order < 1)) {
        errors.step_order = 'Thứ tự bước phải là số dương'
      }
      
      if (formData.delay_days && (isNaN(formData.delay_days) || formData.delay_days < 0)) {
        errors.delay_days = 'Số ngày trễ phải là số không âm'
      }
      
      return errors
    }
  }
})
