import { useDashboardStore } from '@/stores/dashboard'
import { useToast } from '@/composables/useToast'
import { storeToRefs } from 'pinia'

export const useDashboard = () => {
  const dashboardStore = useDashboardStore()
  const toast = useToast()

  // Use store state with reactivity
  const {
    tasks,
    activeCampaigns,
    completedCampaigns,
    loading,
    tasksLoading,
    campaignsLoading,
    completedLoading,
    statistics,
    urgentTasks
  } = storeToRefs(dashboardStore)

  // Load all dashboard data
  const loadDashboardData = async () => {
    try {
      const result = await dashboardStore.refreshAll()
      if (!result.success) {
        toast.error('Failed to load some dashboard data')
      }
      return result
    } catch (error) {
      console.error('Error loading dashboard data:', error)
      toast.error('Failed to load dashboard data')
      return { success: false, error: error.message }
    }
  }

  // Load tasks only
  const loadTasks = async () => {
    try {
      const result = await dashboardStore.fetchTasks()
      if (!result.success) {
        toast.error(result.error || 'Failed to load tasks')
      }
      return result
    } catch (error) {
      console.error('Error loading tasks:', error)
      toast.error('Failed to load tasks')
      return { success: false, error: error.message }
    }
  }

  // Load active campaigns only
  const loadActiveCampaigns = async () => {
    try {
      const result = await dashboardStore.fetchActiveCampaigns()
      if (!result.success) {
        toast.error(result.error || 'Failed to load active campaigns')
      }
      return result
    } catch (error) {
      console.error('Error loading active campaigns:', error)
      toast.error('Failed to load active campaigns')
      return { success: false, error: error.message }
    }
  }

  // Load completed campaigns only
  const loadCompletedCampaigns = async () => {
    try {
      const result = await dashboardStore.fetchCompletedCampaigns()
      if (!result.success) {
        toast.error(result.error || 'Failed to load completed campaigns')
      }
      return result
    } catch (error) {
      console.error('Error loading completed campaigns:', error)
      toast.error('Failed to load completed campaigns')
      return { success: false, error: error.message }
    }
  }

  // Update task status
  const updateTaskStatus = async (taskId, newStatus) => {
    try {
      const result = await dashboardStore.updateTaskStatus(taskId, newStatus)
      
      if (result.success) {
        toast.success('Task updated successfully')
      } else {
        toast.error(result.error || 'Failed to update task')
      }
      
      return result
    } catch (error) {
      console.error('Error updating task:', error)
      toast.error('Failed to update task')
      return { success: false, error: error.message }
    }
  }

  // Helper functions
  const getDueDateBadgeColor = (dueDate) => {
    switch (dueDate) {
      case 'Hôm nay':
      case 'Quá hạn':
        return 'bg-red-100 text-red-800'
      case 'Ngày mai':
        return 'bg-yellow-100 text-yellow-800'
      default:
        return 'bg-blue-100 text-blue-800'
    }
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    
    try {
      const date = new Date(dateString)
      return date.toLocaleDateString('vi-VN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch (error) {
      return dateString
    }
  }

  return {
    // State
    tasks,
    activeCampaigns,
    completedCampaigns,
    loading,
    tasksLoading,
    campaignsLoading,
    completedLoading,
    statistics,
    urgentTasks,
    
    // Methods
    loadDashboardData,
    loadTasks,
    loadActiveCampaigns,
    loadCompletedCampaigns,
    updateTaskStatus,
    
    // Helpers
    getDueDateBadgeColor,
    formatDate
  }
}
