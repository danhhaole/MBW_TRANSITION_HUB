import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { call } from 'frappe-ui'

export const useInteractionStore = defineStore('interaction', () => {
  // State
  const interactions = ref([])
  const currentInteraction = ref(null)
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
    type: 'all',
    talent: 'all'
  })
  const statistics = ref({
    total: 0,
    emails: 0,
    calls: 0,
    meetings: 0
  })

  // Getters
  const filteredInteractions = computed(() => {
    let filtered = interactions.value
    
    if (filters.value.search) {
      const searchLower = filters.value.search.toLowerCase()
      filtered = filtered.filter(interaction => 
        interaction.talent_id?.toLowerCase().includes(searchLower) ||
        interaction.action?.toLowerCase().includes(searchLower) ||
        interaction.description?.toLowerCase().includes(searchLower)
      )
    }
    
    if (filters.value.type !== 'all') {
      filtered = filtered.filter(interaction => 
        interaction.interaction_type?.includes(filters.value.type)
      )
    }
    
    return filtered
  })

  const getInteractionById = computed(() => {
    return (id) => interactions.value.find(interaction => interaction.name === id)
  })

  const interactionsByType = computed(() => {
    return (type) => interactions.value.filter(interaction => 
      interaction.interaction_type?.includes(type)
    )
  })

  // Actions
  const fetchInteractions = async (options = {}) => {
    loading.value = true
    error.value = null
    
    try {
      // Build filters - merge store filters with options filters
      const mergedFilters = {
        ...filters.value,
        ...(options.filters || {})
      }
      
      // Build params - options override defaults
      const params = {
        filters: mergedFilters,
        fields: ['name', 'talent_id', 'interaction_type', 'action', 'url', 'description', 'modified'],
        order_by: 'modified desc',
        // Default pagination (can be overridden by options)
        limit_page_length: pagination.value.limit,
        limit_start: (pagination.value.page - 1) * pagination.value.limit,
        // Override with options (if limit_page_length is 0, it means load all)
        ...options
      }

      console.log('[InteractionStore] fetchInteractions params:', params)

      const result = await call('frappe.client.get_list', {
        doctype: 'Mira Interaction',
        ...params
      })
      
      console.log('[InteractionStore] fetchInteractions raw result:', result)
      
      // Handle different response formats
      // Frappe can return: array directly, {data: array}, or {message: array}
      let dataArray = []
      if (Array.isArray(result)) {
        dataArray = result
      } else if (result?.data && Array.isArray(result.data)) {
        dataArray = result.data
      } else if (result?.message && Array.isArray(result.message)) {
        dataArray = result.message
      }
      
      console.log('[InteractionStore] fetchInteractions parsed dataArray:', dataArray)
      
      if (dataArray.length > 0 || (result && !result.error)) {
        interactions.value = dataArray.map(interaction => ({
          ...interaction,
          type_color: getInteractionTypeColor(interaction.interaction_type),
          formatted_modified: formatDate(interaction.modified)
        }))
        
        if (result?.pagination) {
          Object.assign(pagination.value, result.pagination)
        }
        
        // Update statistics
        updateStatistics()
      }
      
      return { 
        success: true, 
        data: interactions.value,
        pagination: result?.pagination || pagination.value
      }
    } catch (err) {
      error.value = parseError(err)
      console.error('Error fetching interactions:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const fetchInteractionById = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      const result = await call('frappe.client.get', { 
        doctype: 'Mira Interaction',
        name: id 
      })
      
      if (result && result.data) {
        currentInteraction.value = {
          ...result.data,
          type_color: getInteractionTypeColor(result.data.interaction_type)
        }
        return { success: true, data: currentInteraction.value }
      }
      
      return { success: false, error: 'Interaction not found' }
    } catch (err) {
      error.value = parseError(err)
      console.error('Error fetching interaction:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const saveInteraction = async (interactionData) => {
    loading.value = true
    error.value = null
    
    try {
      let result

      if (interactionData.name) {
        // Update existing interaction
        const { name, ...fieldsToUpdate } = interactionData

        // Remove empty string values (keep null if intentional)
        Object.keys(fieldsToUpdate).forEach((key) => {
          if (fieldsToUpdate[key] === '') {
            delete fieldsToUpdate[key]
          }
        })

        result = await call('frappe.client.set_value', {
            doctype: 'Mira Interaction',
          name,
          fieldname: fieldsToUpdate
          })
      } else {
        // Create new interaction
        result = await call('frappe.client.insert', {
            doc: {
              doctype: 'Mira Interaction',
              ...interactionData
            }
          })
      }

      console.log('[InteractionStore] saveInteraction raw result:', result)

      // Frappe client usually returns the doc directly (sometimes under .data)
      const doc = result?.data || result
      if (!doc || !doc.name) {
        return { success: false, error: 'Failed to save interaction (no document returned)' }
      }

        const savedInteraction = {
        ...doc,
        type_color: getInteractionTypeColor(doc.interaction_type),
        formatted_modified: formatDate(doc.modified)
        }
        
        if (interactionData.name) {
        // Update existing in local state
        const index = interactions.value.findIndex((interaction) => interaction.name === interactionData.name)
          if (index !== -1) {
            interactions.value[index] = savedInteraction
          }
        } else {
        // Add new to local state
          interactions.value.unshift(savedInteraction)
        }
        
        updateStatistics()
        return { success: true, data: savedInteraction }
    } catch (err) {
      error.value = parseError(err)
      console.error('Error saving interaction:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const deleteInteraction = async (interactionId) => {
    loading.value = true
    error.value = null
    
    try {
      const result = await call('frappe.client.delete', { 
        doctype: 'Mira Interaction',
        name: interactionId 
      })
      
      if (result && result.success) {
        // Remove from local state
        const index = interactions.value.findIndex(interaction => interaction.name === interactionId)
        if (index !== -1) {
          interactions.value.splice(index, 1)
        }
        
        updateStatistics()
        return { success: true }
      }
      
      return { success: false, error: result.error || 'Failed to delete interaction' }
    } catch (err) {
      error.value = parseError(err)
      console.error('Error deleting interaction:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const exportInteractions = async (exportOptions = {}) => {
    loading.value = true
    error.value = null
    
    try {
      const params = {
        filters: filters.value,
        fields: ['name', 'talent_id', 'interaction_type', 'action', 'url', 'description', 'modified'],
        ...exportOptions
      }
      
      // For export, we'll get the data and handle export client-side
      const result = await call('frappe.client.get_list', {
        doctype: 'Mira Interaction',
        ...params,
        limit_page_length: 0 // Get all records for export
      })
      
      if (result && result.success) {
        return { success: true, data: result.data }
      }
      
      return { success: false, error: result.error || 'Failed to export interactions' }
    } catch (err) {
      error.value = parseError(err)
      console.error('Error exporting interactions:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const fetchStatistics = async () => {
    try {
      // Get statistics by counting different types
      const [totalResult, emailResult, callResult, meetingResult] = await Promise.all([
        call('frappe.client.get_count', { doctype: 'Mira Interaction' }),
        call('frappe.client.get_count', { doctype: 'Mira Interaction', filters: { interaction_type: ['like', '%EMAIL%'] } }),
        call('frappe.client.get_count', { doctype: 'Mira Interaction', filters: { interaction_type: ['like', '%CALL%'] } }),
        call('frappe.client.get_count', { doctype: 'Mira Interaction', filters: { interaction_type: ['like', '%MEETING%'] } })
      ])
      
      const result = {
        data: {
          total: totalResult || 0,
          emails: emailResult || 0,
          calls: callResult || 0,
          meetings: meetingResult || 0
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
  const getInteractionTypeColor = (type) => {
    if (!type) return 'gray'
    
    if (type.includes('EMAIL')) return 'blue'
    if (type.includes('CALL')) return 'green'
    if (type.includes('MEETING')) return 'purple'
    if (type.includes('SMS')) return 'orange'
    
    return 'gray'
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

  const updateStatistics = () => {
    statistics.value = {
      total: interactions.value.length,
      emails: interactions.value.filter(i => i.interaction_type?.includes('EMAIL')).length,
      calls: interactions.value.filter(i => i.interaction_type?.includes('CALL')).length,
      meetings: interactions.value.filter(i => i.interaction_type?.includes('MEETING')).length
    }
  }

  // Filter methods
  const setSearch = (searchText) => {
    filters.value.search = searchText
  }

  const setTypeFilter = (type) => {
    filters.value.type = type
  }

  const setTalentFilter = (talent) => {
    filters.value.talent = talent
  }

  const clearFilters = () => {
    filters.value = {
      search: '',
      type: 'all',
      talent: 'all'
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
    interactions,
    currentInteraction,
    loading,
    error,
    pagination,
    filters,
    statistics,
    
    // Getters
    filteredInteractions,
    getInteractionById,
    interactionsByType,
    
    // Actions
    fetchInteractions,
    fetchInteractionById,
    saveInteraction,
    deleteInteraction,
    exportInteractions,
    fetchStatistics,
    
    // Helper methods
    getInteractionTypeColor,
    formatDate,
    parseError,
    updateStatistics,
    
    // Filter methods
    setSearch,
    setTypeFilter,
    setTalentFilter,
    clearFilters,
    setPagination
  }
})
