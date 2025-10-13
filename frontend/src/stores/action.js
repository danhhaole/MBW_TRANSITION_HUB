import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { call } from 'frappe-ui'

export const useActionStore = defineStore('action', () => {
  // State
  const actions = ref([])
  const currentAction = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({
    page: 1,
    limit: 10,
    total: 0,
    pages: 1,
    has_next: false,
    has_prev: false,
    showing_from: 0,
    showing_to: 0
  })
  const filters = ref({
    search: '',
    status: 'all',
    campaign: 'all',
    assignee: 'all'
  })
  const statistics = ref({
    total: 0,
    pending: 0,
    executed: 0,
    failed: 0,
    skipped: 0
  })

  // Getters
  const filteredActions = computed(() => {
    let filtered = actions.value
    
    if (filters.value.search) {
      const searchLower = filters.value.search.toLowerCase()
      filtered = filtered.filter(action => 
        action.talent_campaign_id?.toLowerCase().includes(searchLower) ||
        action.campaign_step?.toLowerCase().includes(searchLower) ||
        action.assignee_id?.toLowerCase().includes(searchLower)
      )
    }
    
    if (filters.value.status !== 'all') {
      filtered = filtered.filter(action => action.status === filters.value.status)
    }
    
    return filtered
  })

  const getActionById = computed(() => {
    return (id) => actions.value.find(action => action.name === id)
  })

  const actionsByStatus = computed(() => {
    return (status) => actions.value.filter(action => action.status === status)
  })

  // Actions
  const fetchActions = async (options = {}) => {
    loading.value = true
    error.value = null
    
    try {
      const params = {
        page: pagination.value.page,
        limit: pagination.value.limit,
        filters: {
          ...filters.value,
          ...options.filters
        },
        fields: ['name', 'talent_campaign_id', 'campaign_step', 'status', 'scheduled_at', 'executed_at', 'result', 'assignee_id'],
        order_by: 'modified desc',
        ...options
      }

      const result = await call('frappe.client.get_list', {
        doctype: 'Action',
        ...params
      })
      
      if (result && result.data) {
        actions.value = result.data.map(action => ({
          ...action,
          display_status: getStatusDisplay(action.status),
          status_color: getStatusColor(action.status),
          formatted_scheduled_at: formatDate(action.scheduled_at),
          formatted_executed_at: formatDate(action.executed_at)
        }))
        
        if (result.pagination) {
          Object.assign(pagination.value, result.pagination)
        }
      }
      
      return { success: true, data: actions.value }
    } catch (err) {
      error.value = parseError(err)
      console.error('Error fetching actions:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const fetchActionById = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      const result = await call('frappe.client.get', { 
        doctype: 'Action',
        name: id 
      })
      
      if (result && result.data) {
        currentAction.value = {
          ...result.data,
          display_status: getStatusDisplay(result.data.status),
          status_color: getStatusColor(result.data.status)
        }
        return { success: true, data: currentAction.value }
      }
      
      return { success: false, error: 'Action not found' }
    } catch (err) {
      error.value = parseError(err)
      console.error('Error fetching action:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const executeAction = async (actionData) => {
    loading.value = true
    error.value = null
    
    try {
      const result = await call('frappe.client.set_value', {
        doctype: 'Action',
        name: actionData.name,
        fieldname: 'status',
        value: 'EXECUTED'
      })
      
      if (result && result.success) {
        // Update local action if it exists
        const index = actions.value.findIndex(action => action.name === actionData.name)
        if (index !== -1) {
          actions.value[index] = {
            ...actions.value[index],
            status: 'EXECUTED',
            executed_at: new Date().toISOString(),
            display_status: getStatusDisplay('EXECUTED'),
            status_color: getStatusColor('EXECUTED')
          }
        }
        
        return { success: true, data: result.data }
      }
      
      return { success: false, error: result.error || 'Failed to execute action' }
    } catch (err) {
      error.value = parseError(err)
      console.error('Error executing action:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const deleteAction = async (actionId) => {
    loading.value = true
    error.value = null
    
    try {
      const result = await call('frappe.client.delete', { 
        doctype: 'Action',
        name: actionId 
      })
      
      if (result && result.success) {
        // Remove from local state
        const index = actions.value.findIndex(action => action.name === actionId)
        if (index !== -1) {
          actions.value.splice(index, 1)
        }
        
        return { success: true }
      }
      
      return { success: false, error: result.error || 'Failed to delete action' }
    } catch (err) {
      error.value = parseError(err)
      console.error('Error deleting action:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const exportActions = async (exportOptions = {}) => {
    loading.value = true
    error.value = null
    
    try {
      const params = {
        filters: filters.value,
        fields: ['name', 'talent_campaign_id', 'campaign_step', 'status', 'scheduled_at', 'executed_at', 'result', 'assignee_id'],
        ...exportOptions
      }
      
      // For export, we'll get the data and handle export client-side
      const result = await call('frappe.client.get_list', {
        doctype: 'Action',
        ...params,
        limit_page_length: 0 // Get all records for export
      })
      
      if (result && result.success) {
        return { success: true, data: result.data }
      }
      
      return { success: false, error: result.error || 'Failed to export actions' }
    } catch (err) {
      error.value = parseError(err)
      console.error('Error exporting actions:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const fetchStatistics = async () => {
    try {
      // Get statistics by counting different statuses
      const [totalResult, pendingResult, executedResult, failedResult, skippedResult] = await Promise.all([
        call('frappe.client.get_count', { doctype: 'Action' }),
        call('frappe.client.get_count', { doctype: 'Action', filters: { status: 'SCHEDULED' } }),
        call('frappe.client.get_count', { doctype: 'Action', filters: { status: 'EXECUTED' } }),
        call('frappe.client.get_count', { doctype: 'Action', filters: { status: 'FAILED' } }),
        call('frappe.client.get_count', { doctype: 'Action', filters: { status: 'SKIPPED' } })
      ])
      
      const result = {
        data: {
          total: totalResult || 0,
          pending: pendingResult || 0,
          executed: executedResult || 0,
          failed: failedResult || 0,
          skipped: skippedResult || 0
        }
      }
      
      if (result && result.data) {
        statistics.value = result.data
        return { success: true, data: statistics.value }
      }
      
      return { success: false, error: 'Failed to fetch statistics' }
    } catch (err) {
      console.error('Error fetching statistics:', err)
      return { success: false, error: parseError(err) }
    }
  }

  // Helper methods
  const getStatusDisplay = (status) => {
    const statusMap = {
      'SCHEDULED': 'Scheduled',
      'EXECUTED': 'Executed', 
      'SKIPPED': 'Skipped',
      'FAILED': 'Failed'
    }
    return statusMap[status] || status
  }

  const getStatusColor = (status) => {
    const colorMap = {
      'SCHEDULED': 'blue',
      'EXECUTED': 'green',
      'SKIPPED': 'orange', 
      'FAILED': 'red'
    }
    return colorMap[status] || 'gray'
  }

  const formatDate = (dateString) => {
    if (!dateString) return ''
    return new Date(dateString).toLocaleDateString('vi-VN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const parseError = (error) => {
    if (typeof error === 'string') return error
    if (error?.message) return error.message
    if (error?.error) return error.error
    return 'An unknown error occurred'
  }

  // Filter methods
  const setSearch = (searchText) => {
    filters.value.search = searchText
  }

  const setStatusFilter = (status) => {
    filters.value.status = status
  }

  const setCampaignFilter = (campaign) => {
    filters.value.campaign = campaign
  }

  const setAssigneeFilter = (assignee) => {
    filters.value.assignee = assignee
  }

  const clearFilters = () => {
    filters.value = {
      search: '',
      status: 'all',
      campaign: 'all', 
      assignee: 'all'
    }
  }

  const setPagination = (page, limit = null) => {
    pagination.value.page = page
    if (limit) {
      pagination.value.limit = limit
    }
  }

  return {
    // State
    actions,
    currentAction,
    loading,
    error,
    pagination,
    filters,
    statistics,
    
    // Getters
    filteredActions,
    getActionById,
    actionsByStatus,
    
    // Actions
    fetchActions,
    fetchActionById,
    executeAction,
    deleteAction,
    exportActions,
    fetchStatistics,
    
    // Helper methods
    getStatusDisplay,
    getStatusColor,
    formatDate,
    parseError,
    
    // Filter methods
    setSearch,
    setStatusFilter,
    setCampaignFilter,
    setAssigneeFilter,
    clearFilters,
    setPagination
  }
})
