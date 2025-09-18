import { defineStore } from 'pinia'
import { call } from '@/utils/api'

export const useJobOpeningStore = defineStore('jobOpening', {
  state: () => ({
    openings: [],
    current: null,
    loading: false,
    error: null
  }),

  actions: {
    async getOpenings() {
      try {
        this.loading = true
        const response = await call('frappe.client.get_list', {
          args: {
            doctype: 'JobOpening',
            fields: ['*'],
            order_by: 'modified desc'
          }
        })
        this.openings = response
        return response
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },

    async getOpening(name) {
      try {
        this.loading = true
        const response = await call('frappe.client.get', {
          args: {
            doctype: 'JobOpening',
            name
          }
        })
        this.current = response
        return response
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },

    async createOpening(data) {
      try {
        this.loading = true
        return await call('frappe.client.insert', {
          args: { doc: { doctype: 'JobOpening', ...data } }
        })
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateOpening(name, data) {
      try {
        this.loading = true
        return await call('frappe.client.set_value', {
          args: { doctype: 'JobOpening', name, fieldname: data }
        })
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteOpening(name) {
      try {
        this.loading = true
        await call('frappe.client.delete', { args: { doctype: 'JobOpening', name } })
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    }
  }
}) 