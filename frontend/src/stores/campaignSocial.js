import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useCampaignSocialStore = defineStore('campaignSocial', {
  state: () => ({
    campaignSocials: [],
    loading: false,
    error: null,
    success: false
  }),

  getters: {
    // Get campaign socials by campaign_id
    getCampaignSocialsByCampaign: (state) => (campaignId) => {
      return state.campaignSocials.filter(social => social.campaign_id === campaignId)
    },

    // Get single campaign social by name
    getCampaignSocialByName: (state) => (name) => {
      return state.campaignSocials.find(social => social.name === name)
    }
  },

  actions: {
    // Fetch campaign socials with filters
    async fetchCampaignSocials(filters = {}) {
      this.loading = true
      this.error = null
      
      try {
        const response = await call('frappe.client.get_list', {
          doctype: 'CampaignSocial',
          fields: [
            'name',
            'campaign_id',
            'social_page_id', 
            'social_page_name',
            'post_schedule_time',
            'template_content',
            'social_media_images',
            'creation',
            'modified'
          ],
          filters: filters,
          order_by: 'creation desc'
        })

        this.campaignSocials = response || []
        this.success = true
        return response
      } catch (error) {
        console.error('Error fetching campaign socials:', error)
        this.error = error.message || 'Failed to fetch campaign socials'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Create new campaign social
    async createCampaignSocial(data) {
      this.loading = true
      this.error = null
      
      try {
        const response = await call('frappe.client.insert', {
          doc: {
            doctype: 'CampaignSocial',
            ...data
          }
        })

        // Add to local state
        this.campaignSocials.unshift(response)
        this.success = true
        
        console.log('✅ Campaign Social created:', response.name)
        return response
      } catch (error) {
        console.error('❌ Error creating campaign social:', error)
        this.error = error.message || 'Failed to create campaign social'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Update campaign social
    async updateCampaignSocial(name, data) {
      this.loading = true
      this.error = null
      
      try {
        const response = await call('frappe.client.set_value', {
          doctype: 'CampaignSocial',
          name: name,
          fieldname: data
        })

        // Update local state
        const index = this.campaignSocials.findIndex(social => social.name === name)
        if (index !== -1) {
          this.campaignSocials[index] = { ...this.campaignSocials[index], ...data }
        }

        this.success = true
        console.log('✅ Campaign Social updated:', name)
        return response
      } catch (error) {
        console.error('❌ Error updating campaign social:', error)
        this.error = error.message || 'Failed to update campaign social'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Delete campaign social
    async deleteCampaignSocial(name) {
      this.loading = true
      this.error = null
      
      try {
        await call('frappe.client.delete', {
          doctype: 'CampaignSocial',
          name: name
        })

        // Remove from local state
        this.campaignSocials = this.campaignSocials.filter(social => social.name !== name)
        this.success = true
        
        console.log('✅ Campaign Social deleted:', name)
        return true
      } catch (error) {
        console.error('❌ Error deleting campaign social:', error)
        this.error = error.message || 'Failed to delete campaign social'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Get single campaign social by name
    async getCampaignSocial(name) {
      this.loading = true
      this.error = null
      
      try {
        const response = await call('frappe.client.get', {
          doctype: 'CampaignSocial',
          name: name
        })

        this.success = true
        return response
      } catch (error) {
        console.error('❌ Error fetching campaign social:', error)
        this.error = error.message || 'Failed to fetch campaign social'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Create default campaign social when campaign is created
    async createDefaultCampaignSocial(campaignId, socialConfig = {}) {
      const defaultData = {
        campaign_id: campaignId,
        social_page_id: socialConfig.page_id || '',
        social_page_name: socialConfig.page_name || '',
        post_schedule_time: socialConfig.scheduled_at || null,
        template_content: socialConfig.template_content || '',
        social_media_images: socialConfig.image || ''
      }

      return await this.createCampaignSocial(defaultData)
    },

    // Bulk create campaign socials
    async bulkCreateCampaignSocials(campaignId, socialConfigs) {
      this.loading = true
      this.error = null
      
      try {
        const promises = socialConfigs.map(config => 
          this.createDefaultCampaignSocial(campaignId, config)
        )
        
        const results = await Promise.all(promises)
        this.success = true
        
        console.log(`✅ Created ${results.length} campaign socials for campaign:`, campaignId)
        return results
      } catch (error) {
        console.error('❌ Error bulk creating campaign socials:', error)
        this.error = error.message || 'Failed to bulk create campaign socials'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Clear state
    clearState() {
      this.campaignSocials = []
      this.error = null
      this.success = false
    },

    // Clear error
    clearError() {
      this.error = null
    }
  }
})
