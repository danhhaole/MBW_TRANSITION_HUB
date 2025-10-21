import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    tasks: [],
    activeCampaigns: [],
    completedCampaigns: [],
    loading: false,
    tasksLoading: false,
    campaignsLoading: false,
    completedLoading: false,
    error: null,
    statistics: {
      totalTasks: 0,
      urgentTasks: 0,
      activeCampaigns: 0,
      completedToday: 0
    }
  }),

  getters: {
    urgentTasks: (state) => {
      return state.tasks.filter(
        (task) =>
          (task.dueDate === 'Hôm nay' || task.dueDate === 'Quá hạn') &&
          task.status === 'PENDING_MANUAL'
      )
    }
  },

  actions: {
    // Load Tasks from Action doctype
    async fetchTasks() {
      try {
        this.tasksLoading = true
        this.error = null

        // Try new API first
        let result
        try {
          result = await call('mbw_mira.api.doc.get_list_data', {
            doctype: 'Mira Action',
            filters: {
              status: ['in', ['PENDING_MANUAL']],
            },
            fields: [
              'name',
              'status',
              'scheduled_at',
              'executed_at',
              'talent_campaign_id',
              'campaign_step',
              'assignee_id',
            ],
            order_by: 'scheduled_at asc',
            limit_page_length: 10,
          })

          if (!result || !result.success) {
            throw new Error('New API returned invalid response')
          }
        } catch (newApiError) {
          console.warn('New API failed, falling back to old API:', newApiError.message)
          
          // Fallback to old API
          result = await call('frappe.client.get_list', {
            doctype: 'Mira Action',
            filters: {
              status: ['in', ['PENDING_MANUAL']],
            },
            fields: [
              'name',
              'status',
              'scheduled_at',
              'executed_at',
              'talent_campaign_id',
              'campaign_step',
              'assignee_id',
            ],
            order_by: 'scheduled_at asc',
            limit_page_length: 10,
          })

          // Wrap in success format for consistency
          if (result && Array.isArray(result)) {
            result = { success: true, data: result }
          }
        }

        if (result && result.success && result.data) {
          // Transform actions to tasks format
          this.tasks = result.data.map(action => ({
            id: action.name,
            title: this.getActionTitle(action.status),
            type: action.status,
            status: action.status,
            dueDate: this.formatDueDate(action.scheduled_at),
            candidate: action.talent_campaign_id ? 'Loading...' : 'No candidate',
            campaign: action.campaign_step || 'Unknown',
            assignee: action.assignee_id || 'Unassigned',
            scheduledAt: action.scheduled_at,
            executedAt: action.executed_at,
            talentCampaignId: action.talent_campaign_id
          }))

          // Update statistics
          this.statistics.totalTasks = this.tasks.length
          this.statistics.urgentTasks = this.urgentTasks.length
        }

        return { success: true, data: this.tasks }
      } catch (error) {
        console.error('Error fetching tasks:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.tasksLoading = false
      }
    },

    // Load Active Campaigns
    async fetchActiveCampaigns() {
      try {
        this.campaignsLoading = true
        this.error = null

        // Try new API first
        let result
        try {
          result = await call('mbw_mira.api.doc.get_list_data', {
            doctype: 'Mira Campaign',
            filters: { status: 'ACTIVE', is_active: 1 },
            fields: ['name', 'campaign_name', 'status', 'start_date', 'end_date'],
            order_by: 'creation desc',
            limit_page_length: 6,
          })

          if (!result || !result.success) {
            throw new Error('New API returned invalid response')
          }
        } catch (newApiError) {
          console.warn('New API failed, falling back to old API:', newApiError.message)
          
          // Fallback to old API
          result = await call('frappe.client.get_list', {
            doctype: 'Mira Campaign',
            filters: { status: 'ACTIVE', is_active: 1 },
            fields: ['name', 'campaign_name', 'status', 'start_date', 'end_date'],
            order_by: 'creation desc',
            limit_page_length: 6,
          })

          // Wrap in success format for consistency
          if (result && Array.isArray(result)) {
            result = { success: true, data: result }
          }
        }

        if (result && result.success && result.data) {
          // Transform campaigns with stats
          this.activeCampaigns = result.data.map(campaign => ({
            id: campaign.name,
            name: campaign.campaign_name,
            status: campaign.status,
            progress: Math.floor(Math.random() * 100), // Mock progress for now
            totalTasks: Math.floor(Math.random() * 50) + 10, // Mock data
            completedTasks: Math.floor(Math.random() * 30) + 5, // Mock data
            startDate: campaign.start_date,
            endDate: campaign.end_date
          }))

          // Update statistics
          this.statistics.activeCampaigns = this.activeCampaigns.length
        }

        return { success: true, data: this.activeCampaigns }
      } catch (error) {
        console.error('Error fetching active campaigns:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.campaignsLoading = false
      }
    },

    // Load Completed Campaigns (recently completed)
    async fetchCompletedCampaigns() {
      try {
        this.completedLoading = true
        this.error = null

        // Try new API first  
        let result
        try {
          result = await call('mbw_mira.api.doc.get_list_data', {
            doctype: 'Mira Action',
            filters: { status: 'EXECUTED' },
            fields: ['name', 'executed_at', 'talent_campaign_id'],
            order_by: 'executed_at desc',
            limit_page_length: 20,
          })

          if (!result || !result.success) {
            throw new Error('New API returned invalid response')
          }
        } catch (newApiError) {
          console.warn('New API failed, falling back to old API:', newApiError.message)
          
          // Fallback to old API
          result = await call('frappe.client.get_list', {
            doctype: 'Mira Action',
            filters: { status: 'EXECUTED' },
            fields: ['name', 'executed_at', 'talent_campaign_id'],
            order_by: 'executed_at desc',
            limit_page_length: 20,
          })

          // Wrap in success format for consistency
          if (result && Array.isArray(result)) {
            result = { success: true, data: result }
          }
        }

        if (result && result.success && result.data) {
          // Group by campaign and get campaign details
          const campaignMap = new Map()

          for (const action of result.data) {
            if (action.talent_campaign_id) {
              // For now, create mock completed campaigns
              // In real implementation, you'd fetch campaign details
              const campaignId = `campaign_${Math.floor(Math.random() * 100)}`
              if (!campaignMap.has(campaignId)) {
                campaignMap.set(campaignId, {
                  id: campaignId,
                  name: `Campaign ${campaignId}`,
                  completedTasks: 1,
                  lastCompleted: action.executed_at,
                })
              } else {
                campaignMap.get(campaignId).completedTasks++
              }
            }
          }

          this.completedCampaigns = Array.from(campaignMap.values())
            .sort((a, b) => new Date(b.lastCompleted) - new Date(a.lastCompleted))
            .slice(0, 5)

          // Update statistics
          this.statistics.completedToday = this.completedCampaigns.length
        }

        return { success: true, data: this.completedCampaigns }
      } catch (error) {
        console.error('Error fetching completed campaigns:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.completedLoading = false
      }
    },

    // Update task status
    async updateTaskStatus(taskId, newStatus) {
      try {
        this.loading = true
        this.error = null

        const result = await call('frappe.client.set_value', {
          doctype: 'Mira Action',
          name: taskId,
          fieldname: 'status',
          value: newStatus
        })

        if (result) {
          // Update local task
          const taskIndex = this.tasks.findIndex(task => task.id === taskId)
          if (taskIndex !== -1) {
            this.tasks[taskIndex].status = newStatus
          }
          
          return { success: true }
        }

        return { success: false, error: 'Failed to update task' }
      } catch (error) {
        console.error('Error updating task:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    // Refresh all dashboard data
    async refreshAll() {
      try {
        this.loading = true
        this.error = null

        const results = await Promise.allSettled([
          this.fetchTasks(),
          this.fetchActiveCampaigns(),
          this.fetchCompletedCampaigns()
        ])

        // Check if any failed
        const failures = results.filter(result => result.status === 'rejected')
        if (failures.length > 0) {
          console.warn('Some dashboard data failed to load:', failures)
        }

        return { success: true }
      } catch (error) {
        console.error('Error refreshing dashboard:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    // Helper methods
    getActionTitle(status) {
      const titleMap = {
        'PENDING_MANUAL': 'Manual Review Required',
        'PENDING_APPROVAL': 'Approval Required',
        'SCHEDULED': 'Scheduled Task',
        'EXECUTED': 'Completed Task'
      }
      return titleMap[status] || status
    },

    formatDueDate(scheduledAt) {
      if (!scheduledAt) return 'No due date'
      
      const now = new Date()
      const scheduled = new Date(scheduledAt)
      const diffTime = scheduled - now
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays < 0) return 'Quá hạn'
      if (diffDays === 0) return 'Hôm nay'
      if (diffDays === 1) return 'Ngày mai'
      if (diffDays <= 7) return `${diffDays} ngày nữa`
      
      return scheduled.toLocaleDateString('vi-VN')
    },

    parseError(error) {
      if (typeof error === 'string') return error
      if (error?.message) return error.message
      if (error?.exc_type && error?.exc) return `${error.exc_type}: ${error.exc}`
      return 'An unexpected error occurred'
    }
  }
})
