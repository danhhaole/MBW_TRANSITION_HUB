import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useTalentDetailStore = defineStore('talentDetail', {
  state: () => ({
    talent: null,
    activities: [],
    calls: [],
    notes: [],
    tasks: [],
    attachments: [],
    loading: false,
    error: null,
    activeTab: 'activities'
  }),

  getters: {
    talentName: (state) => state.talent?.full_name || '',
    talentEmail: (state) => state.talent?.email || '',
    talentPhone: (state) => state.talent?.phone || '',
    talentStatus: (state) => state.talent?.current_status || '',
    talentSkills: (state) => state.talent?.skills || '',
    talentTags: (state) => state.talent?.tags || '',
    
    // Activity counts
    activityCount: (state) => state.activities.length,
    commentCount: (state) => state.activities.filter(a => a.activity_type === 'comment').length,
    attachmentCount: (state) => state.attachments.length,
    
    // Formatted data
    formattedActivities: (state) => {
      return state.activities.map(activity => ({
        ...activity,
        timeAgo: formatTimeAgo(activity.creation),
        formattedDate: formatDate(activity.creation)
      }))
    }
  },

  actions: {
    async fetchTalent(name) {
      this.loading = true
      this.error = null
      
      try {
        // Fetch talent details using frappe client API
        const talentResult = await call('frappe.client.get', {
          doctype: 'Mira Talent',
          name: name
        })
        
        if (talentResult) {
          this.talent = talentResult
        } else {
          throw new Error('Failed to fetch talent')
        }
        
        // Fetch activities
        await this.fetchActivities(name)
        
      } catch (err) {
        this.error = err.message
        console.error('Error fetching talent:', err)
      } finally {
        this.loading = false
      }
    },

    async fetchActivities(name) {
      try {
        const result = await call('mbw_mira.api.activities.get_activities', {
          name: name
        })
        
        if (result && Array.isArray(result)) {
          const [activities, calls, notes, tasks, attachments] = result
          this.activities = activities || []
          this.calls = calls || []
          this.notes = notes || []
          this.tasks = tasks || []
          this.attachments = attachments || []
        }
      } catch (err) {
        console.error('Error fetching activities:', err)
        // Don't throw error, just log it
      }
    },

    async addComment(name, content) {
      try {
        const result = await call('frappe.desk.form.utils.add_comment', {
          reference_doctype: 'Mira Talent',
          reference_name: name,
          content: content
        })
        
        if (result) {
          // Refresh activities to show new comment
          await this.fetchActivities(name)
          return { success: true }
        }
      } catch (err) {
        console.error('Error adding comment:', err)
        return { success: false, message: err.message }
      }
    },

    async updateTalent(name, data) {
      try {
        // Update talent using frappe client API
        const result = await call('frappe.client.save', {
          doctype: 'Mira Talent',
          name: name,
          ...data
        })
        
        if (result) {
          this.talent = { ...this.talent, ...result }
          // Refresh activities to show changes
          await this.fetchActivities(name)
          return { success: true }
        } else {
          throw new Error('Failed to update talent')
        }
      } catch (err) {
        console.error('Error updating talent:', err)
        return { success: false, message: err.message }
      }
    },

    setActiveTab(tab) {
      this.activeTab = tab
    },

    clearTalent() {
      this.talent = null
      this.activities = []
      this.calls = []
      this.notes = []
      this.tasks = []
      this.attachments = []
      this.error = null
      this.activeTab = 'activities'
    }
  }
})

// Helper functions
function formatTimeAgo(dateStr) {
  if (!dateStr) return ''
  
  const date = new Date(dateStr)
  const now = new Date()
  const diffInSeconds = Math.floor((now - date) / 1000)
  
  if (diffInSeconds < 60) return 'Just now'
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`
  if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 86400)} days ago`
  
  return formatDate(dateStr)
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString('vi-VN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (error) {
    return dateStr
  }
}
