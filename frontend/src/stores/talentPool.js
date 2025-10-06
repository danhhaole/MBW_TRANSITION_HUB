import { defineStore } from 'pinia'
import { createResource, call } from 'frappe-ui'

export const useTalentPoolStore = defineStore('talentPool', {
  state: () => ({
    talentPools: [],
    segments: [],
    current: null,
    filters: {
      segmentType: null
    }
  }),

  getters: {
    filteredTalentPools: (state) => {
      let filtered = [...state.talentPools]
      
      if (state.filters.segmentType) {
        filtered = filtered.filter(
          pool => pool.segment_id === state.filters.segmentType
        )
      }
      
      return filtered
    },
    
    uniqueSegmentTypes: (state) => {
      return state.segments.map(segment => ({
        id: segment.name,
        title: segment.title
      }))
    }
  },
  
  actions: {
    async fetchSegments() {
      try {
        const response = await call('frappe.client.get_list', {
          doctype: 'Mira Segment',
          fields: ['name', 'title'],
          order_by: 'creation desc'
        })
        this.segments = response
        return response
      } catch (error) {
        console.error('Error fetching segments:', error)
        throw error
      }
    },
  
    // Call this in your component's onMounted or setup
    async initResources() {
      this.talentPoolsResource = createResource({
        url: 'mbw_mira.mbw_mira.doctype.mira_talent_pool.mira_talent_pool.get_talent_pool',
        auto: true,
        onSuccess: (data) => {
          this.talentPools = data
        }
      })
      
      // Fetch segments when initializing
      await this.fetchSegments()
    },

    getTalentPools() {
      if (!this.talentPoolsResource) {
        this.initResources()
      }
      return this.talentPoolsResource.fetch()
    },

    setSegmentTypeFilter(segmentId) {
      this.filters.segmentType = segmentId || null
    },
    
    clearFilters() {
      this.filters.segmentType = null
    },

    refreshTalentPools() {
      return this.getTalentPools()
    }
  }
})