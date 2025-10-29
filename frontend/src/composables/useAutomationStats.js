import { ref, computed } from 'vue'
import { call } from 'frappe-ui'

/**
 * Composable để lấy statistics cho Automation pages
 * Tái sử dụng được cho Campaign, Flow, Sequence
 */
export function useAutomationStats() {
  // State
  const stats = ref({
    campaigns: { total: 0, active: 0, draft: 0, paused: 0, completed: 0 },
    flows: { total: 0, active: 0, draft: 0, paused: 0, archived: 0 },
    sequences: { total: 0, active: 0, draft: 0, paused: 0, completed: 0 }
  })
  
  const loading = ref(false)
  const error = ref(null)

  // Computed
  const campaignCount = computed(() => stats.value.campaigns.total)
  const flowCount = computed(() => stats.value.flows.total)
  const sequenceCount = computed(() => stats.value.sequences.total)

  /**
   * Lấy counts đơn giản cho nhiều doctypes
   * @param {Array<string>} doctypes - Danh sách doctype names
   * @returns {Promise<Object>} Object với doctype names làm keys và counts làm values
   */
  const getDocTypeCounts = async (doctypes = ['Mira Campaign', 'Mira Flow', 'Mira Sequence']) => {
    try {
      loading.value = true
      error.value = null

      const result = await call('mbw_mira.api.automation_stats.get_automation_counts', {
        doctypes: doctypes
      })

      if (result && result.success) {
        return result.data
      } else {
        throw new Error(result?.error || 'Failed to fetch counts')
      }
    } catch (err) {
      error.value = err.message
      console.error('Error fetching doctype counts:', err)
      return {}
    } finally {
      loading.value = false
    }
  }

  /**
   * Lấy detailed statistics cho tất cả automation doctypes
   * Bao gồm breakdown theo status
   * @returns {Promise<Object>} Detailed statistics object
   */
  const fetchAutomationStats = async () => {
    try {
      loading.value = true
      error.value = null

      const result = await call('mbw_mira.api.automation_stats.get_automation_stats')

      if (result && result.success) {
        stats.value = result.data
        return result.data
      } else {
        throw new Error(result?.error || 'Failed to fetch automation stats')
      }
    } catch (err) {
      error.value = err.message
      console.error('Error fetching automation stats:', err)
      
      // Return default values on error
      return {
        campaigns: { total: 0, active: 0, draft: 0, paused: 0, completed: 0 },
        flows: { total: 0, active: 0, draft: 0, paused: 0, archived: 0 },
        sequences: { total: 0, active: 0, draft: 0, paused: 0, completed: 0 }
      }
    } finally {
      loading.value = false
    }
  }

  /**
   * Refresh statistics
   */
  const refreshStats = async () => {
    return await fetchAutomationStats()
  }

  return {
    // State
    stats,
    loading,
    error,
    
    // Computed
    campaignCount,
    flowCount,
    sequenceCount,
    
    // Methods
    getDocTypeCounts,
    fetchAutomationStats,
    refreshStats
  }
}
