import { defineStore } from 'pinia'
import { call } from '@/utils/api'

export const useLadiPageStore = defineStore('ladipage', {
  state: () => ({
    ladiPages: [],
    currentPage: null,
    loading: false,
    error: null
  }),

  actions: {
    async getLadiPages() {
      try {
        this.loading = true
        const response = await call('frappe.client.get_list', {
          args: {
            doctype: 'LadiPage',
            fields: ['*'],
            order_by: 'creation desc'
          }
        })
        this.ladiPages = response
        return response
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },

    async getLadiPage(name) {
      try {
        this.loading = true
        const response = await call('frappe.client.get', {
          args: {
            doctype: 'LadiPage',
            name: name
          }
        })
        this.currentPage = response
        return response
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },

    async createLadiPage(data) {
      try {
        this.loading = true
        const response = await call('frappe.client.insert', {
          args: {
            doc: {
              doctype: 'LadiPage',
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

    async updateLadiPage(name, data) {
      try {
        this.loading = true
        const response = await call('frappe.client.set_value', {
          args: {
            doctype: 'LadiPage',
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

    async deleteLadiPage(name) {
      try {
        this.loading = true
        await call('frappe.client.delete', {
          args: {
            doctype: 'LadiPage',
            name: name
          }
        })
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },

    async uploadThumbnail(file) {
      try {
        this.loading = true
        const formData = new FormData()
        formData.append('file', file)
        const response = await call('upload_file', {
          args: { file: formData }
        })
        return response.file_url
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
