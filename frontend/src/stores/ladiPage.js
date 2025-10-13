import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useLadiPageStore = defineStore('ladiPage', {
  state: () => ({
    ladiPages: [],
    currentPage: null,
    loading: false,
    error: null,
    pagination: {
      page: 1,
      limit: 10,
      total: 0,
      pages: 1
    },
    filters: {
      search: '',
      published: 'all',
      campaign: 'all'
    }
  }),

  getters: {
    publishedOptions: () => [
      { label: 'All Statuses', value: 'all' },
      { label: 'Published', value: '1' },
      { label: 'Draft', value: '0' }
    ]
  },

  actions: {
    async fetchLadiPages() {
      try {
        this.loading = true
        const { filters, pagination } = this
        const start = (pagination.page - 1) * pagination.limit

        // Prepare filters
        let queryFilters = {}
        if (filters.published !== 'all') queryFilters.published = filters.published
        if (filters.campaign !== 'all') queryFilters.campaign = filters.campaign
        
        // Prepare or_filters for search
        let orFilters
        if (filters.search) {
          orFilters = [
            ['title', 'like', `%${filters.search}%`],
            ['route', 'like', `%${filters.search}%`]
          ]
        }

        // Get data with pagination
        const data = await call('frappe.client.get_list', {
          doctype: 'LadiPage',
          fields: ['*'],
          filters: queryFilters,
          or_filters: orFilters,
          limit_start: start,
          limit_page_length: pagination.limit,
          order_by: 'modified desc'
        })

        // Get total count
        const total = await call('frappe.client.get_count', {
          doctype: 'LadiPage',
          filters: queryFilters
        })

        // Update state
        this.ladiPages = data || []
        this.pagination = {
          ...this.pagination,
          total,
          pages: Math.ceil(total / pagination.limit)
        }

        return data
      } catch (error) {
        this.error = error
        console.error('Error fetching Ladi pages:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchLadiPage(name) {
      try {
        this.loading = true
        const response = await call('frappe.client.get', {
          doctype: 'LadiPage',
          name: name
        })
        this.currentPage = response
        return response
      } catch (error) {
        this.error = error
        console.error('Error fetching Ladi page:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async createLadiPage(data) {
      try {
        this.loading = true
        const response = await call('frappe.client.insert', {
          doc: {
            doctype: 'LadiPage',
            ...data
          }
        })
        await this.fetchLadiPages()
        return response
      } catch (error) {
        this.error = error
        console.error('Error creating Ladi page:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateLadiPage(name, data) {
      try {
        this.loading = true
        const response = await call('frappe.client.set_value', {
          doctype: 'LadiPage',
          name: name,
          fieldname: data
        })
        await this.fetchLadiPages()
        return response
      } catch (error) {
        this.error = error
        console.error('Error updating Ladi page:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async savePageContent(name, content, css) {
      try {
        this.loading = true
        const response = await call('frappe.client.set_value', {
          doctype: 'LadiPage',
          name: name,
          fieldname: {
            content: content,
            css: css
          }
        })
        return response
      } catch (error) {
        this.error = error
        console.error('Error saving page content:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteLadiPage(name) {
      try {
        this.loading = true
        await call('frappe.client.delete', {
          doctype: 'LadiPage',
          name: name
        })
        await this.fetchLadiPages()
      } catch (error) {
        this.error = error
        console.error('Error deleting Ladi page:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchCampaignOptions() {
      try {
        const campaigns = await call('frappe.client.get_list', {
          doctype: "Mira Campaign",
          fields: ['name', 'campaign_name'],
          filters: { status: 'Active' }
        })
        return campaigns.map(campaign => ({
          label: campaign.campaign_name,
          value: campaign.name
        }))
      } catch (error) {
        console.error('Error fetching campaign options:', error)
        return []
      }
    },

    // Filter actions
    setSearchFilter(search) {
      this.filters.search = search
      this.pagination.page = 1
      this.fetchLadiPages()
    },

    setPublishedFilter(published) {
      this.filters.published = published
      this.pagination.page = 1
      this.fetchLadiPages()
    },

    setCampaignFilter(campaign) {
      this.filters.campaign = campaign
      this.pagination.page = 1
      this.fetchLadiPages()
    },

    // Pagination actions
    setPage(page) {
      this.pagination.page = page
      this.fetchLadiPages()
    },

    setItemsPerPage(limit) {
      this.pagination.limit = limit
      this.pagination.page = 1
      this.fetchLadiPages()
    }
  }
})