import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    // Existing state
    tasks: [],
    activeCampaigns: [],
    completedCampaigns: [],
    loading: false,
    tasksLoading: false,
    campaignsLoading: false,
    completedLoading: false,
    error: null,
    
    // Marketing metrics state
    marketingMetrics: {
      totalTalentPool: 0,
      newTalents: 0,
      hotTalents: 0, // MQL
      convertedTalents: 0, // SQL
      costPerLead: 0,
      loading: false
    },
    
    // Funnel data
    funnelData: {
      sent: 0,
      opened: 0,
      clicked: 0,
      mql: 0,
      sql: 0,
      loading: false
    },
    
    // Source attribution
    sourceData: [],
    sourceLoading: false,
    
    // Campaign performance
    campaignPerformance: [],
    campaignPerformanceLoading: false,
    
    // Top campaigns with latest interactions
    topCampaignsWithLatestInteractions: [],
    topCampaignsLoading: false,
    
    // Conversion by source
    conversionBySource: [],
    conversionLoading: false,
    
    //Task
    taskListData :[],

    // Time range for data
    timeRange: '90d',
    
    statistics: {
      totalTalent: 0,
      totalNewTalent: 0,
      totalTalentHot: 0,
      totalTalentConvert: 0,
      totalTasks: 0,
      urgentTasks: 0,
      activeCampaigns: 0,
      completedToday: 0,
      
    }
  }),

  getters: {
    urgentTasks: (state) => {
      return state.tasks.filter(
        (task) =>
          (task.dueDate === 'Hôm nay' || task.dueDate === 'Quá hạn') &&
          task.status === 'PENDING_MANUAL'
      )
    },
    
    // Get date range based on timeRange
    dateRange: (state) => {
      const now = new Date()
      const ranges = {
        '30d': new Date(now.setDate(now.getDate() - 30)),
        '90d': new Date(now.setDate(now.getDate() - 90)),
        'ytd': new Date(now.getFullYear(), 0, 1),
        'q4': new Date(now.getFullYear(), 9, 1) // Oct 1
      }
      return ranges[state.timeRange] || ranges['90d']
    },
    
    // Get days count based on timeRange for API calls
    daysFromTimeRange: (state) => {
      const now = new Date()
      switch(state.timeRange) {
        case '30d': 
          return 30
        case '90d': 
          return 90
        case 'ytd': {
          const startOfYear = new Date(now.getFullYear(), 0, 1)
          return Math.floor((now - startOfYear) / (1000 * 60 * 60 * 24))
        }
        case 'q4': {
          const startOfQ4 = new Date(now.getFullYear(), 9, 1) // Oct 1
          return Math.floor((now - startOfQ4) / (1000 * 60 * 60 * 24))
        }
        default: 
          return 90
      }
    }
  },

  actions: {
    // ==================== MARKETING METRICS ====================
    
    /**
     * Fetch KPI metrics for marketing dashboard using new APIs
     */
    async fetchMarketingMetrics(timeRange = null) {
      try {
        this.marketingMetrics.loading = true
        if (timeRange) this.timeRange = timeRange
        
        const days = this.daysFromTimeRange
        
        // Fetch total talent pool size (no filter)
        const totalResult = await call('mbw_mira.api.dashboard.get_total_talents_count')
        this.marketingMetrics.totalTalentPool = totalResult?.count || 0
        this.statistics.totalTalent = this.marketingMetrics.totalTalentPool
        
        // Fetch new talents in time range (filtered by creation)
        const newTalentsResult = await call('mbw_mira.api.dashboard.get_new_talents_count', {
          days: days
        })
        this.marketingMetrics.newTalents = newTalentsResult?.count || 0
        this.statistics.totalNewTalent = this.marketingMetrics.newTalents
        
        // Fetch hot talents (MQL) - talents with NURTURING campaigns and both EMAIL_OPENED + ON_LINK_CLICK
        const hotTalentsResult = await call('mbw_mira.api.dashboard.get_nurturing_engaged_talents_count', {
          days: days
        })
        this.marketingMetrics.hotTalents = hotTalentsResult?.count || 0
        this.statistics.totalTalentHot = this.marketingMetrics.hotTalents
        
        // Fetch converted talents (SQL) - talents with RECRUITMENT campaigns (filtered by modified)
        const convertedResult = await call('mbw_mira.api.dashboard.get_recruitment_talents_count', {
          days: days
        })
        this.marketingMetrics.convertedTalents = convertedResult?.count || 0
        this.statistics.totalTalentConvert = this.marketingMetrics.convertedTalents
        
        // Calculate Cost Per Lead (mock calculation)
        // In real implementation, fetch from campaign budget
        const totalCost = 0 // Mock total marketing cost
        this.marketingMetrics.costPerLead = this.marketingMetrics.newTalents > 0
          ? (totalCost / this.marketingMetrics.newTalents).toFixed(2)
          : 0
        
        return { success: true, data: this.marketingMetrics }
      } catch (error) {
        console.error('Error fetching marketing metrics:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.marketingMetrics.loading = false
      }
    },
    
    /**
     * Fetch funnel data (email campaign funnel) using new nurturing funnel API
     */
    async fetchFunnelData(timeRange = null) {
      try {
        this.funnelData.loading = true
        if (timeRange) this.timeRange = timeRange
        
        const days = this.daysFromTimeRange
        
        // Use the new nurturing funnel API
        const funnelResult = await call('mbw_mira.api.dashboard.get_nurturing_funnel_data', {
          days: days
        })
        
        if (funnelResult) {
          this.funnelData.sent = funnelResult.sent?.count || 0
          this.funnelData.opened = funnelResult.opened?.count || 0
          this.funnelData.clicked = funnelResult.clicked?.count || 0
          this.funnelData.mql = funnelResult.mql?.count || 0
          this.funnelData.sql = funnelResult.sql?.count || 0
          
          // Store percentages for potential future use
          this.funnelData.sentPercentage = funnelResult.sent?.percentage || 100.0
          this.funnelData.openedPercentage = funnelResult.opened?.percentage || 0.0
          this.funnelData.clickedPercentage = funnelResult.clicked?.percentage || 0.0
          this.funnelData.mqlPercentage = funnelResult.mql?.percentage || 0.0
          this.funnelData.sqlPercentage = funnelResult.sql?.percentage || 0.0
        }
        
        return { success: true, data: this.funnelData }
      } catch (error) {
        console.error('Error fetching funnel data:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.funnelData.loading = false
      }
    },
    
    /**
     * Fetch source attribution data
     */
    async fetchSourceData(timeRange = null) {
      try {
        this.sourceLoading = true
        if (timeRange) this.timeRange = timeRange
        
        const fromDate = this.dateRange
        
        // Get talents grouped by source
        const talentsResult = await call('mbw_mira.api.doc.get_list_data', {
          doctype: 'Mira Talent',
          filters: {
            creation: ['>=', fromDate.toISOString()]
          },
          fields: ['name', 'source'],
          limit_page_length: 0
        })
        
        const talents = talentsResult?.data || []
        
        // Group by source
        const sourceMap = new Map()
        talents.forEach(talent => {
          const source = talent.source || 'Unknown'
          sourceMap.set(source, (sourceMap.get(source) || 0) + 1)
        })
        
        // Transform to array format
        this.sourceData = Array.from(sourceMap.entries()).map(([name, value]) => ({
          name,
          value,
          percentage: talents.length > 0 ? ((value / talents.length) * 100).toFixed(1) : 0
        }))
        
        return { success: true, data: this.sourceData }
      } catch (error) {
        console.error('Error fetching source data:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.sourceLoading = false
      }
    },
    
    /**
     * Fetch campaign performance (CTR)
     */
    async fetchCampaignPerformance(timeRange = null) {
      try {
        this.campaignPerformanceLoading = true
        if (timeRange) this.timeRange = timeRange
        
        const fromDate = this.dateRange
        
        // Get campaigns with action stats
        const campaignsResult = await call('mbw_mira.api.doc.get_list_data', {
          doctype: 'Mira Campaign',
          filters: {
            is_active: 1,
            status:"ACTIVE",
            start_date: ['<=', fromDate.toISOString()]
          },
          fields: ['name', 'campaign_name', 'status'],
          limit_page_length: 5
        })
        
        const campaigns = campaignsResult?.data || []
        
        // For each campaign, get action stats
        this.campaignPerformance = await Promise.all(
          campaigns.map(async (campaign) => {
            // Get total sent actions for this campaign
            const sentResult = await call('mbw_mira.api.doc.get_list_data', {
              doctype: 'Mira Action',
              filters: {
                campaign_id: campaign.name,
                action_type: ['in', ['EMAIL', 'MESSAGE']]
              },
              fields: ['name'],
              limit_page_length: 0
            })
            
            const totalSent = sentResult?.total_count || 0
            
            // Mock click data - in real implementation, get from metadata
            const clicks = Math.floor(totalSent * (Math.random() * 0.15 + 0.05))
            const ctr = totalSent > 0 ? ((clicks / totalSent) * 100).toFixed(2) : 0
            
            return {
              name: campaign.campaign_name,
              campaignId: campaign.name,
              sent: totalSent,
              clicks,
              ctr: parseFloat(ctr)
            }
          })
        )
        
        // Sort by CTR descending
        this.campaignPerformance.sort((a, b) => b.ctr - a.ctr)
        
        return { success: true, data: this.campaignPerformance }
      } catch (error) {
        console.error('Error fetching campaign performance:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.campaignPerformanceLoading = false
      }
    },
    
    /**
     * Fetch top 5 campaigns with latest interactions
     */
    async fetchTopCampaignsWithLatestInteractions(timeRange = null) {
      try {
        this.topCampaignsLoading = true
        if (timeRange) this.timeRange = timeRange
        
        const days = this.daysFromTimeRange
        
        // Call the new API
        const result = await call('mbw_mira.api.dashboard.get_top_campaigns_with_latest_interactions', {
          days: days
        })
        
        if (result && Array.isArray(result)) {
          this.topCampaignsWithLatestInteractions = result
        } else {
          this.topCampaignsWithLatestInteractions = []
        }
        
        return { success: true, data: this.topCampaignsWithLatestInteractions }
      } catch (error) {
        console.error('Error fetching top campaigns with latest interactions:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.topCampaignsLoading = false
      }
    },
    
    /**
     * Fetch conversion rates by source
     */
    async fetchConversionBySource(timeRange = null) {
      try {
        this.conversionLoading = true
        if (timeRange) this.timeRange = timeRange
        
        const fromDate = this.dateRange
        
        // Get all talents with source
        const talentsResult = await call('mbw_mira.api.doc.get_list_data', {
          doctype: 'Mira Talent',
          filters: {
            creation: ['>=', fromDate.toISOString()]
          },
          fields: ['name', 'source', 'crm_status'],
          limit_page_length: 0
        })
        
        const talents = talentsResult?.data || []
        
        // Group by source
        const sourceMap = new Map()
        talents.forEach(talent => {
          const source = talent.source || 'Unknown'
          if (!sourceMap.has(source)) {
            sourceMap.set(source, { total: 0, converted: 0 })
          }
          const stats = sourceMap.get(source)
          stats.total++
          if (['SQL', 'CONVERTED', 'QUALIFIED', 'HIRED'].includes(talent.crm_status)) {
            stats.converted++
          }
        })
        
        // Transform to array format
        this.conversionBySource = Array.from(sourceMap.entries())
          .map(([source, stats]) => ({
            channel: source,
            total: stats.total,
            hired: stats.converted,
            rate: stats.total > 0 ? ((stats.converted / stats.total) * 100).toFixed(1) : 0
          }))
          .sort((a, b) => parseFloat(b.rate) - parseFloat(a.rate))
        
        return { success: true, data: this.conversionBySource }
      } catch (error) {
        console.error('Error fetching conversion by source:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.conversionLoading = false
      }
    },
    
    /**
     * Fetch task list data for hot leads
     */
    async fetchTaskListData(timeRange = null) {
      try {
        if (timeRange) this.timeRange = timeRange
        
        // Get pending manual tasks for hot leads
        const tasksResult = await call('mbw_mira.api.doc.get_list_data', {
          doctype: 'Mira Action',
          filters: {
            status: 'PENDING_MANUAL'
          },
          fields: ['name', 'scheduled_at', 'talent_campaign_id', 'campaign_social', 'assignee_id'],
          order_by: 'scheduled_at asc',
          limit_page_length: 10
        })
        
        if (tasksResult && tasksResult.success && tasksResult.data) {
          this.taskListData = tasksResult.data.map(task => ({
            id: task.name,
            title: 'Manual Review Required',
            description: `Campaign: ${task.campaign_social || 'Unknown'}`,
            dueDate: this.formatDueDate(task.scheduled_at),
            priority: 'high',
            assignee: task.assignee_id || 'Unassigned',
            status: task.status
          }))
        }
        
        return { success: true, data: this.taskListData }
      } catch (error) {
        console.error('Error fetching task list data:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      }
    },
    
    /**
     * Refresh all marketing dashboard data
     */
    async refreshMarketingDashboard(timeRange = null) {
      try {
        this.loading = true
        this.error = null
        
        const results = await Promise.allSettled([
          this.fetchMarketingMetrics(timeRange),
          this.fetchFunnelData(timeRange),
          this.fetchSourceData(timeRange),
          this.fetchCampaignPerformance(timeRange),
          this.fetchTopCampaignsWithLatestInteractions(timeRange),
          this.fetchConversionBySource(timeRange),
          this.fetchTaskListData(timeRange)
        ])
        
        // Check if any failed
        const failures = results.filter(result => result.status === 'rejected')
        if (failures.length > 0) {
          console.warn('Some marketing data failed to load:', failures)
        }
        
        return { success: true }
      } catch (error) {
        console.error('Error refreshing marketing dashboard:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },
    
    // ==================== EXISTING ACTIONS ====================
    
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
              'campaign_social',
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
              'campaign_social',
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
            campaign: action.campaign_social || 'Unknown',
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