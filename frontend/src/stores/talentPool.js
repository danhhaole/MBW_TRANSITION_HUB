import { defineStore } from 'pinia'
import { createResource, call } from 'frappe-ui'

export const useTalentPoolStore = defineStore('talentPool', {
  state: () => ({
    talentPools: [],
    segments: [],
    current: null,
    filters: {
      segmentType: null,
      title: null
    }
  }),

  getters: {
    filteredTalentPools: (state) => {
      let filtered = [...state.talentPools]
      
      if (state.filters.segmentType) {
        filtered = filtered.filter(
          pool => pool.segment_title === state.filters.segmentType
        )
      }
      
      if (state.filters.title) {
        filtered = filtered.filter(
          pool => pool.title.toLowerCase().includes(state.filters.title.toLowerCase())
        )
      }
      
      return filtered
    },
    
    uniqueSegmentTypes: (state) => {
      return state.segments.map(segment => ({
        label: segment.title,
        value: segment.title,
        name: segment.name
      }))
    }
  },
  
  actions: {
    async getTalentPool(name) {
      try {
        const talentPool = await call('frappe.client.get', {
          doctype: 'Mira Talent Pool',
          name: name
        })
        return talentPool
      } catch (error) {
        console.error('Error fetching talent pool:', error)
        throw error
      }
    },
    
    async updateTalentPool(name, data) {
      try {
        await call('frappe.client.set_value', {
          doctype: 'Mira Talent Pool',
          name: name,
          fieldname: data
        })
        await this.refreshTalentPools()
      } catch (error) {
        console.error('Error updating talent pool:', error)
        throw error
      }
    },
    
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

    async TalentPoolDetail(name) {
      try {
        const response = await call('mbw_mira.mbw_mira.doctype.mira_talent_pool.mira_talent_pool.get_talent_pool_detail', {
          name: name
        })
        return response
      } catch (error) {
        console.error('Error fetching talent pool detail:', error)
        throw error
      }
    },

    async initResources() {
      this.talentPoolsResource = createResource({
        url: 'mbw_mira.mbw_mira.doctype.mira_talent_pool.mira_talent_pool.get_talent_pool',
        auto: true,
        onSuccess: (data) => {
          this.talentPools = data
        }
      })
    },

    async updateTalentPoolsSegment({ names, segment_id }) {
      try {
        const response = await call('mbw_mira.mbw_mira.doctype.mira_talent_pool.mira_talent_pool.update_talent_pools_segment', {
          names: names,
          segment_id: segment_id
        })
        
        // Refresh the talent pools to reflect the changes
        await this.refreshTalentPools()
        
        return {
          success: true,
          message: 'Cập nhật segment thành công',
          data: response
        }
      } catch (error) {
        console.error('Error updating talent pools segment:', error)
        throw {
          success: false,
          message: error.message || 'Có lỗi xảy ra khi cập nhật segment',
          error: error
        }
      }
    },

    async getTalentInteractions(talentPoolId) {
      try {
        const response = await call('mbw_mira.mbw_mira.doctype.mira_talent_pool.mira_talent_pool.get_talent_interactions', {
          talent_pool_id: talentPoolId
        });
        return response;
      } catch (error) {
        console.error('Error fetching talent interactions:', error);
        throw error;
      }
    },

    getTalentPools(segmentTitle = '') {
      if (!this.talentPoolsResource) {
        this.initResources()
      }
      const params = {}
      if (segmentTitle) {
        params.segment_title = segmentTitle
      }
      return this.talentPoolsResource.fetch(params)
    },

    setSegmentTypeFilter(segmentId) {
      this.filters.segmentType = segmentId || null
    },
    
    setTitleFilter(title) {
      this.filters.title = title || null
    },
    
    clearFilters() {
      this.filters.segmentType = null
      this.filters.title = null
    },

    async refreshTalentPools() {
      this.talentPools = await this.getTalentPools()
    },
  }
})