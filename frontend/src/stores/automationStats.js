import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

/**
 * Store để quản lý automation statistics
 * Cache stats globally để tránh re-fetch mỗi lần navigate
 */
export const useAutomationStatsStore = defineStore('automationStats', {
  state: () => ({
    stats: {
      campaigns: { total: 0, active: 0, draft: 0, paused: 0, completed: 0 },
      flows: { total: 0, active: 0, draft: 0, paused: 0, archived: 0 },
      sequences: { total: 0, active: 0, draft: 0, paused: 0, completed: 0 },
      flowTemplates: { total: 0, system: 0, my: 0 }
    },
    loading: false,
    error: null,
    lastFetched: null, // Timestamp của lần fetch cuối
    cacheDuration: 5 * 60 * 1000 // 5 phút cache
  }),

  getters: {
    campaignCount: (state) => state.stats.campaigns?.total || 0,
    flowCount: (state) => state.stats.flows?.total || 0,
    sequenceCount: (state) => state.stats.sequences?.total || 0,
    flowTemplateCount: (state) => state.stats.flowTemplates?.total || 0,
    
    /**
     * Check xem cache còn valid không
     */
    isCacheValid: (state) => {
      if (!state.lastFetched) return false
      const now = Date.now()
      return (now - state.lastFetched) < state.cacheDuration
    },

    /**
     * Get all counts
     */
    allCounts: (state) => ({
      campaigns: state.stats.campaigns?.total || 0,
      flows: state.stats.flows?.total || 0,
      sequences: state.stats.sequences?.total || 0,
      flowTemplates: state.stats.flowTemplates?.total || 0
    })
  },

  actions: {
    /**
     * Fetch automation stats từ API
     * Chỉ fetch nếu cache đã hết hạn
     * @param {boolean} force - Force refresh bỏ qua cache
     */
    async fetchStats(force = false) {
      // Nếu cache còn valid và không force refresh, skip
      if (!force && this.isCacheValid) {
        console.log('📊 Using cached automation stats')
        return this.stats
      }

      try {
        this.loading = true
        this.error = null

        console.log('🔄 Fetching automation stats from API...')
        const result = await call('mbw_mira.api.automation_stats.get_automation_stats')

        if (result && result.success) {
          // Merge with default values to ensure all properties exist
          this.stats = {
            campaigns: result.data.campaigns || { total: 0, active: 0, draft: 0, paused: 0, completed: 0 },
            flows: result.data.flows || { total: 0, active: 0, draft: 0, paused: 0, archived: 0 },
            sequences: result.data.sequences || { total: 0, active: 0, draft: 0, paused: 0, completed: 0 },
            flowTemplates: result.data.flowTemplates || { total: 0, system: 0, my: 0 }
          }
          this.lastFetched = Date.now()
          console.log('✅ Automation stats fetched:', this.allCounts)
          return this.stats
        } else {
          throw new Error(result?.error || 'Failed to fetch automation stats')
        }
      } catch (err) {
        this.error = err.message
        console.error('❌ Error fetching automation stats:', err)
        
        // Return cached data nếu có, hoặc default values
        return this.stats
      } finally {
        this.loading = false
      }
    },

    /**
     * Refresh stats - force fetch bỏ qua cache
     * Gọi sau khi create/delete operations
     */
    async refreshStats() {
      console.log('🔄 Force refreshing automation stats...')
      return await this.fetchStats(true)
    },

    /**
     * Increment count cho một doctype
     * Gọi sau khi create thành công
     * @param {string} type - 'campaigns' | 'flows' | 'sequences'
     */
    incrementCount(type) {
      if (this.stats[type]) {
        this.stats[type].total++
        this.stats[type].draft++ // Mặc định tạo mới là Draft
        console.log(`➕ Incremented ${type} count:`, this.stats[type].total)
      }
    },

    /**
     * Decrement count cho một doctype
     * Gọi sau khi delete thành công
     * @param {string} type - 'campaigns' | 'flows' | 'sequences'
     * @param {string} status - Status của record bị xóa
     */
    decrementCount(type, status = null) {
      if (this.stats[type] && this.stats[type].total > 0) {
        this.stats[type].total--
        
        // Decrement status count nếu có
        if (status && this.stats[type][status.toLowerCase()] > 0) {
          this.stats[type][status.toLowerCase()]--
        }
        
        console.log(`➖ Decremented ${type} count:`, this.stats[type].total)
      }
    },

    /**
     * Update count khi status thay đổi
     * @param {string} type - 'campaigns' | 'flows' | 'sequences'
     * @param {string} oldStatus - Status cũ
     * @param {string} newStatus - Status mới
     */
    updateStatusCount(type, oldStatus, newStatus) {
      if (!this.stats[type]) return

      const oldKey = oldStatus?.toLowerCase()
      const newKey = newStatus?.toLowerCase()

      // Decrement old status
      if (oldKey && this.stats[type][oldKey] > 0) {
        this.stats[type][oldKey]--
      }

      // Increment new status
      if (newKey && this.stats[type][newKey] !== undefined) {
        this.stats[type][newKey]++
      }

      console.log(`🔄 Updated ${type} status: ${oldStatus} → ${newStatus}`)
    },

    /**
     * Clear cache - force fetch lần sau
     */
    clearCache() {
      this.lastFetched = null
      console.log('🗑️ Automation stats cache cleared')
    },

    /**
     * Reset về default values
     */
    reset() {
      this.stats = {
        campaigns: { total: 0, active: 0, draft: 0, paused: 0, completed: 0 },
        flows: { total: 0, active: 0, draft: 0, paused: 0, archived: 0 },
        sequences: { total: 0, active: 0, draft: 0, paused: 0, completed: 0 },
        flowTemplates: { total: 0, system: 0, my: 0 }
      }
      this.lastFetched = null
      this.error = null
      console.log('🔄 Automation stats reset')
    }
  }
})
