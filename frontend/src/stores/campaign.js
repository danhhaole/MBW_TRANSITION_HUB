import { defineStore } from 'pinia'
import { call } from '@/utils/api'

export const useCampaignStore = defineStore('campaign', {
  state: () => ({
    campaigns: [],
    currentCampaign: null,
    loading: false,
    error: null
  }),

  actions: {
    async getCampaigns() {
      try {
        this.loading = true
        const response = await call('frappe.client.get_list', {
          args: {
            doctype: 'Campaign',
            fields: ['*'],
            order_by: 'creation desc'
          }
        })
        this.campaigns = response
        return response
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },

    async getCampaign(name) {
      try {
        this.loading = true
        const response = await call('frappe.client.get', {
          args: {
            doctype: 'Campaign',
            name: name
          }
        })
        this.currentCampaign = response
        return response
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },

    async createCampaign(data) {
      try {
        this.loading = true
        const response = await call('frappe.client.insert', {
          args: {
            doc: {
              doctype: 'Campaign',
              ...data
            }
          }
        })
        return response
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateCampaign(name, data) {
      try {
        this.loading = true
        const response = await call('frappe.client.set_value', {
          args: {
            doctype: 'Campaign',
            name: name,
            fieldname: data
          }
        })
        return response
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteCampaign(name) {
      try {
        this.loading = true
        await call('frappe.client.delete', {
          args: {
            doctype: 'Campaign',
            name: name
          }
        })
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
