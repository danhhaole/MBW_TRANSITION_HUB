import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useSequenceStore = defineStore('sequence', {
  state: () => ({
    sequences: [],
    currentSequence: null,
    sequenceSteps: {}, // Cache steps by sequence_id: { [sequence_id]: [steps] }
    loading: false,
    error: null,
    pagination: {
      page: 1,
      limit: 20,
      total: 0,
      has_next: false,
      has_prev: false,
      showing_from: 0,
      showing_to: 0
    },
    filters: {
      search: '',
      status: '',
      owner: ''
    },
    statistics: {
      total: 0,
      active: 0,
      draft: 0,
      paused: 0,
      completed: 0
    }
  }),

  getters: {
    filteredSequences: (state) => {
      let filtered = [...state.sequences]
      
      if (state.filters.search) {
        const search = state.filters.search.toLowerCase()
        filtered = filtered.filter(sequence => 
          sequence.title?.toLowerCase().includes(search) ||
          sequence.name?.toLowerCase().includes(search) ||
          sequence.purpose?.toLowerCase().includes(search)
        )
      }
      
      if (state.filters.status) {
        filtered = filtered.filter(sequence => sequence.status === state.filters.status)
      }
      
      if (state.filters.owner) {
        filtered = filtered.filter(sequence => sequence.owner_id === state.filters.owner)
      }
      
      return filtered
    },

    getSequenceByName: (state) => (name) => {
      return state.sequences.find(sequence => sequence.name === name)
    },

    sequencesByStatus: (state) => (status) => {
      return state.sequences.filter(sequence => sequence.status === status)
    },

    recentSequences: (state) => {
      const sevenDaysAgo = new Date()
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
      
      return state.sequences.filter(sequence => {
        const createdAt = new Date(sequence.created_at || sequence.creation)
        return createdAt >= sevenDaysAgo
      })
    }
  },

  actions: {
    async fetchSequences(options = {}) {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          doctype: 'Mira Sequence',
          fields: [
            'name', 'title', 'purpose', 'status', 'enrollment_count',
            'owner_id', 'created_at', 'steps', 'enrollment_source',
            'creation', 'modified'
          ],
          limit_page_length: options.limit || this.pagination.limit,
          limit_start: options.page ? (options.page - 1) * (options.limit || this.pagination.limit) : 0,
          order_by: options.order_by || 'modified desc'
        }

        // Add filters
        if (options.filters) {
          params.filters = options.filters
        }

        if (this.filters.search) {
          params.or_filters = [
            ['title', 'like', `%${this.filters.search}%`],
            ['name', 'like', `%${this.filters.search}%`],
            ['purpose', 'like', `%${this.filters.search}%`]
          ]
        }

        if (this.filters.status) {
          params.filters = { ...params.filters, status: this.filters.status }
        }

        if (this.filters.owner) {
          params.filters = { ...params.filters, owner_id: this.filters.owner }
        }

        // Try the new combined API first, fallback to old API if it fails
        let result
        try {
          result = await call('mbw_mira.api.doc.get_list_data', params)
          
          if (result && result.success && Array.isArray(result.data)) {
            // Enhance data with display fields
            this.sequences = result.data.map(sequence => {
              // Parse steps JSON to get count
              let stepsCount = 0
              try {
                const steps = sequence.steps ? JSON.parse(sequence.steps) : []
                stepsCount = Array.isArray(steps) ? steps.length : 0
              } catch (e) {
                console.error('Error parsing steps for sequence:', sequence.name, e)
              }

              return {
                ...sequence,
                display_status: this.getStatusDisplay(sequence.status),
                status_color: this.getStatusColor(sequence.status),
                steps_count: stepsCount,
                formatted_created_at: this.formatDate(sequence.created_at || sequence.creation),
                formatted_modified: this.formatRelativeDate(sequence.modified)
              }
            })

            // Update pagination
            this.pagination.total = result.count || 0
            this.pagination.page = options.page || 1
            this.pagination.limit = options.limit || this.pagination.limit
            this.pagination.showing_from = this.pagination.total > 0 ? ((this.pagination.page - 1) * this.pagination.limit) + 1 : 0
            this.pagination.showing_to = Math.min(this.pagination.page * this.pagination.limit, this.pagination.total)
            this.pagination.has_next = this.pagination.showing_to < this.pagination.total
            this.pagination.has_prev = this.pagination.page > 1

            return { success: true, data: this.sequences, count: result.count }
          } else {
            throw new Error('New API returned invalid response')
          }
        } catch (newApiError) {
          console.warn('New API failed, falling back to old API:', newApiError.message)
          
          // Fallback to old separate API calls
          const [listResult, countResult] = await Promise.all([
            call('frappe.client.get_list', params),
            call('frappe.client.get_count', {
              doctype: 'Mira Sequence',
              filters: params.filters,
              or_filters: params.or_filters
            })
          ])

          if (listResult && Array.isArray(listResult)) {
            // Enhance data with display fields
            this.sequences = listResult.map(sequence => {
              // Parse steps JSON to get count
              let stepsCount = 0
              try {
                const steps = sequence.steps ? JSON.parse(sequence.steps) : []
                stepsCount = Array.isArray(steps) ? steps.length : 0
              } catch (e) {
                console.error('Error parsing steps for sequence:', sequence.name, e)
              }

              return {
                ...sequence,
                display_status: this.getStatusDisplay(sequence.status),
                status_color: this.getStatusColor(sequence.status),
                steps_count: stepsCount,
                formatted_created_at: this.formatDate(sequence.created_at || sequence.creation),
                formatted_modified: this.formatRelativeDate(sequence.modified)
              }
            })

            // Update pagination
            this.pagination.total = countResult || 0
            this.pagination.page = options.page || 1
            this.pagination.limit = options.limit || this.pagination.limit
            this.pagination.showing_from = this.pagination.total > 0 ? ((this.pagination.page - 1) * this.pagination.limit) + 1 : 0
            this.pagination.showing_to = Math.min(this.pagination.page * this.pagination.limit, this.pagination.total)
            this.pagination.has_next = this.pagination.showing_to < this.pagination.total
            this.pagination.has_prev = this.pagination.page > 1

            return { success: true, data: this.sequences, count: countResult }
          }
        }

        return { success: false, message: 'No data received' }
      } catch (error) {
        console.error('Error fetching sequences:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchSequenceById(id) {
      this.loading = true
      this.error = null
      
      try {
        // Use new combined API - gets sequence + flows + actions in ONE call
        const result = await call('mbw_mira.mbw_mira.doctype.mira_sequence.mira_sequence.get_sequence_with_flows', {
          sequence_id: id
        })

        if (result && result.name) {
          // Cache steps
          this.sequenceSteps[id] = result.steps || []

          // Enhance data with display fields
          const enhancedSequence = {
            ...result,
            display_status: this.getStatusDisplay(result.status),
            status_color: this.getStatusColor(result.status),
            steps_count: (result.steps || []).length,
            formatted_created_at: this.formatDate(result.created_at || result.creation),
            formatted_modified: this.formatRelativeDate(result.modified)
          }

          this.currentSequence = enhancedSequence
          return { success: true, data: enhancedSequence }
        }

        return { success: false, message: 'Sequence not found' }
      } catch (error) {
        console.error('Error fetching sequence:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async createSequence(sequenceData) {
      this.loading = true
      this.error = null
      
      try {
        const validationResult = this.validateSequence(sequenceData)
        if (!validationResult.isValid) {
          throw new Error(validationResult.message)
        }

        const preparedData = this.prepareSequenceForSave(sequenceData)
        
        const result = await call('frappe.client.insert', {
          doc: {
            doctype: 'Mira Sequence',
            ...preparedData
          }
        })

        if (result && result.name) {
          // Refresh sequences list
          await this.fetchSequences()
          return { success: true, data: result }
        }

        return { success: false, message: 'Failed to create sequence' }
      } catch (error) {
        console.error('Error creating sequence:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async updateSequence(name, sequenceData) {
      this.loading = true
      this.error = null
      
      try {
        const validationResult = this.validateSequence(sequenceData)
        if (!validationResult.isValid) {
          throw new Error(validationResult.message)
        }

        // Prepare sequence data (includes steps JSON with delays)
        const completeSequenceData = {
          title: sequenceData.title?.trim(),
          purpose: sequenceData.purpose?.trim() || '',
          status: sequenceData.status || 'Draft',
          enrollment_source: sequenceData.enrollment_source?.trim() || '',
          steps: sequenceData.steps // Keep steps JSON for delays
        }
        
        // Update sequence basic info
        const result = await call('frappe.client.set_value', {
          doctype: 'Mira Sequence',
          name: name,
          fieldname: completeSequenceData
        })

        if (result) {
          // Refresh sequences list
          await this.fetchSequences()
          return { success: true, data: result }
        }

        return { success: false, message: 'Failed to update sequence' }
      } catch (error) {
        console.error('Error updating sequence:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async deleteSequence(sequenceId) {
      this.loading = true
      this.error = null
      
      try {
        // Check if sequence can be deleted (not Active)
        const sequence = this.getSequenceByName(sequenceId)
        if (sequence && sequence.status === 'Active') {
          throw new Error('Không thể xóa sequence đang hoạt động. Vui lòng tạm dừng sequence trước khi xóa.')
        }

        // Use new API that handles links
        const response = await call('mbw_mira.api.campaign.delete_sequence_with_links', {
          sequence_name: sequenceId,
          force_delete: false
        })

        if (response && response.status === 'success') {
          // Remove from local state
          this.sequences = this.sequences.filter(sequence => sequence.name !== sequenceId)
          delete this.sequenceSteps[sequenceId]
          
          // Update pagination
          this.pagination.total = Math.max(0, this.pagination.total - 1)
          
          return { success: true }
        } else if (response && response.error_type === 'LinkExistsError') {
          // Return the error with linked documents info
          const error = new Error(response.message)
          error.linkedDocuments = response.linked_documents
          error.errorType = 'LinkExistsError'
          throw error
        } else {
          throw new Error(response.message || 'Failed to delete sequence')
        }
      } catch (error) {
        console.error('Error deleting sequence:', error)
        this.error = this.parseError(error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async forceDeleteSequence(sequenceId) {
      this.loading = true
      this.error = null
      
      try {
        const response = await call('mbw_mira.api.campaign.delete_sequence_with_links', {
          sequence_name: sequenceId,
          force_delete: true
        })

        if (response && response.status === 'success') {
          // Remove from local state
          this.sequences = this.sequences.filter(sequence => sequence.name !== sequenceId)
          delete this.sequenceSteps[sequenceId]
          
          // Update pagination
          this.pagination.total = Math.max(0, this.pagination.total - 1)
          
          return { success: true }
        } else {
          throw new Error(response.message || 'Failed to delete sequence')
        }
      } catch (error) {
        console.error('Error force deleting sequence:', error)
        this.error = this.parseError(error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async duplicateSequence(sequenceId) {
      this.loading = true
      this.error = null
      
      try {
        // First get the original sequence
        const originalSequence = await call('frappe.client.get', {
          doctype: 'Mira Sequence',
          name: sequenceId
        })

        if (!originalSequence) {
          throw new Error('Original sequence not found')
        }

        // Parse steps JSON
        let delaySteps = []
        try {
          delaySteps = originalSequence.steps ? JSON.parse(originalSequence.steps) : []
        } catch (e) {
          console.error('Error parsing steps:', e)
        }

        // Get original flows with actions
        const originalFlows = await call('frappe.client.get_list', {
          doctype: 'Mira Flow',
          filters: {
            sequence_id: sequenceId,
            type: 'Sequence'
          },
          fields: ['*'],
          order_by: 'creation asc'
        })

        // Fetch actions for each flow
        const flowsWithActions = await Promise.all(
          (originalFlows || []).map(async (flow) => {
            const flowDetail = await call('frappe.client.get', {
              doctype: 'Mira Flow',
              name: flow.name
            })
            return {
              ...flow,
              actions: flowDetail.action_id || []
            }
          })
        )

        // Prepare duplicate data
        const duplicateData = {
          title: `${originalSequence.title} (Copy)`,
          purpose: originalSequence.purpose,
          status: 'Draft',
          enrollment_source: originalSequence.enrollment_source,
          steps: '[]' // Will update after creating flows
        }

        // Create the duplicate sequence
        const result = await call('frappe.client.insert', {
          doc: {
            doctype: 'Mira Sequence',
            ...duplicateData
          }
        })

        if (result && result.name) {
          const newSteps = []

          // Duplicate all flows with actions
          for (let i = 0; i < flowsWithActions.length; i++) {
            const originalFlow = flowsWithActions[i]
            const delay = delaySteps[i]?.delay || '1 day'

            // Prepare flow doc with actions
            const flowDoc = {
              doctype: 'Mira Flow',
              type: 'Sequence',
              sequence_id: result.name,
              title: originalFlow.title,
              channel: originalFlow.channel,
              status: 'Draft'
            }

            // Copy actions to child table
            if (originalFlow.actions && originalFlow.actions.length > 0) {
              flowDoc.action_id = originalFlow.actions.map(action => ({
                action_type: action.action_type,
                channel_type: action.channel_type,
                action_parameters: action.action_parameters,
                order: action.order || 0
              }))
            }

            // Create flow with actions
            const newFlow = await call('frappe.client.insert', {
              doc: flowDoc
            })

            if (newFlow && newFlow.name) {
              newSteps.push({
                delay: delay,
                flow_id: newFlow.name
              })
            }
          }

          // Update sequence with new steps JSON
          await call('frappe.client.set_value', {
            doctype: 'Mira Sequence',
            name: result.name,
            fieldname: { steps: JSON.stringify(newSteps) }
          })

          // Refresh sequences list
          await this.fetchSequences()
          return { success: true, data: result }
        }

        return { success: false, message: 'Failed to duplicate sequence' }
      } catch (error) {
        console.error('Error duplicating sequence:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async searchSequences(searchText) {
      this.filters.search = searchText
      return await this.fetchSequences({ page: 1 })
    },

    async fetchStatistics() {
      try {
        // Use the main fetchSequences method to get all data for statistics
        // This ensures we use the same API and get accurate statistics
        const currentFilters = { ...this.filters }
        const currentPagination = { ...this.pagination }
        
        // Temporarily clear filters and get all data for accurate statistics
        this.filters = { search: '', status: '', owner: '' }
        
        const result = await this.fetchSequences({
          page: 1,
          limit: 1000, // Get more data for accurate statistics
          order_by: 'modified desc'
        })
        
        // Restore original filters and pagination
        this.filters = currentFilters
        this.pagination = currentPagination
        
        if (result && result.success && result.data) {
          // Calculate statistics from the full dataset
          const statusCounts = { active: 0, draft: 0, paused: 0, completed: 0 }
          result.data.forEach(sequence => {
            const status = sequence.status?.toLowerCase()
            if (statusCounts.hasOwnProperty(status)) {
              statusCounts[status]++
            }
          })
          
          this.statistics = {
            total: result.count || 0,
            ...statusCounts
          }
        }
        
        return this.statistics
      } catch (error) {
        console.error('Error fetching statistics:', error)
        return this.statistics
      }
    },

    async getSequence(name) {
      // Use fetchSequenceById for consistency
      return await this.fetchSequenceById(name)
    },

    // Helper methods
    validateSequence(sequenceData) {
      if (!sequenceData.title || sequenceData.title.trim().length === 0) {
        return { isValid: false, message: 'Tên sequence là bắt buộc' }
      }

      if (sequenceData.title.length > 200) {
        return { isValid: false, message: 'Tên sequence không được vượt quá 200 ký tự' }
      }

      const validStatuses = ['Active', 'Draft', 'Paused', 'Completed']
      if (sequenceData.status && !validStatuses.includes(sequenceData.status)) {
        return { isValid: false, message: 'Trạng thái không hợp lệ' }
      }

      return { isValid: true }
    },

    prepareSequenceForSave(sequenceData) {
      return {
        title: sequenceData.title?.trim(),
        purpose: sequenceData.purpose?.trim() || '',
        status: sequenceData.status || 'Draft',
        enrollment_source: sequenceData.enrollment_source?.trim() || ''
      }
    },

    getStatusDisplay(status) {
      const statusMap = {
        'Active': 'Hoạt động',
        'Draft': 'Nháp',
        'Paused': 'Tạm dừng',
        'Completed': 'Hoàn thành'
      }
      return statusMap[status] || status
    },

    getStatusColor(status) {
      const colorMap = {
        'Active': 'green',
        'Draft': 'gray',
        'Paused': 'yellow',
        'Completed': 'blue'
      }
      return colorMap[status] || 'gray'
    },

    async fetchSequenceSteps(sequenceId) {
      try {
        const result = await call('frappe.client.get_list', {
          doctype: 'Mira Flow',
          filters: {
            sequence_id: sequenceId,
            type: 'Sequence'
          },
          fields: ['*'],
          order_by: 'creation asc'
        })

        if (result) {
          this.sequenceSteps[sequenceId] = result
          return { success: true, data: result }
        }

        return { success: false, data: [] }
      } catch (error) {
        console.error('Error fetching sequence steps:', error)
        return { success: false, error: this.parseError(error), data: [] }
      }
    },

    async createSequenceStep(sequenceId, stepData) {
      try {
        // Validate sequenceId
        if (!sequenceId) {
          throw new Error('sequenceId is required')
        }

        console.log('Creating step for sequence:', sequenceId)
        console.log('Step data:', stepData)

        // Verify sequence exists
        let sequence
        try {
          sequence = await call('frappe.client.get', {
            doctype: 'Mira Sequence',
            name: sequenceId
          })
          console.log('Sequence found:', sequence)
        } catch (error) {
          console.error('Sequence not found in database:', sequenceId)
          console.error('Error:', error)
          throw new Error(`Sequence "${sequenceId}" does not exist in database. Please check if the sequence was created successfully.`)
        }

        if (!sequence || !sequence.name) {
          throw new Error(`Sequence ${sequenceId} not found or invalid`)
        }

        // Prepare flow doc with actions in child table
        const flowDoc = {
          doctype: 'Mira Flow',
          type: 'Sequence',
          sequence_id: sequenceId,
          title: stepData.title || 'New Step',
          channel: stepData.channel || 'Email',
          status: 'Draft'
        }

        // Add action to child table if provided
        if (stepData.action) {
          flowDoc.action_id = [{
            action_type: stepData.action.action_type || 'EMAIL',
            channel_type: stepData.action.channel_type || 'Email',
            action_parameters: JSON.stringify(stepData.action.parameters || {})
          }]
        }

        // Create Mira Flow with actions
        const flowResult = await call('frappe.client.insert', {
          doc: flowDoc
        })

        if (flowResult && flowResult.name) {

          // Update sequence steps JSON to add delay
          const sequence = await call('frappe.client.get', {
            doctype: 'Mira Sequence',
            name: sequenceId
          })

          let steps = []
          try {
            steps = sequence.steps ? JSON.parse(sequence.steps) : []
          } catch (e) {
            console.error('Error parsing steps:', e)
          }

          steps.push({
            delay: stepData.delay || '1 day',
            flow_id: flowResult.name
          })

          await call('frappe.client.set_value', {
            doctype: 'Mira Sequence',
            name: sequenceId,
            fieldname: { steps: JSON.stringify(steps) }
          })

          // Refresh
          await this.fetchSequenceById(sequenceId)
          return { success: true, data: flowResult }
        }

        return { success: false, message: 'Failed to create step' }
      } catch (error) {
        console.error('Error creating step:', error)
        return { success: false, error: this.parseError(error) }
      }
    },

    async updateSequenceStep(flowName, stepData, sequenceId) {
      try {
        // Get current flow to update
        const currentFlow = await call('frappe.client.get', {
          doctype: 'Mira Flow',
          name: flowName
        })

        if (!currentFlow) {
          return { success: false, message: 'Flow not found' }
        }

        // Prepare updated doc
        const updatedDoc = {
          ...currentFlow,
          title: stepData.title || currentFlow.title,
          channel: stepData.channel || currentFlow.channel
        }

        // Update actions if provided
        if (stepData.actions && Array.isArray(stepData.actions)) {
          updatedDoc.action_id = stepData.actions.map(action => ({
            action_type: action.action_type,
            channel_type: action.channel_type,
            action_parameters: typeof action.action_parameters === 'string' 
              ? action.action_parameters 
              : JSON.stringify(action.parameters || {}),
            order: action.order || 0
          }))
        }

        // Use frappe.client.save to update with child table
        const result = await call('frappe.client.save', {
          doc: updatedDoc
        })

        if (result) {
          // Refresh if sequence_id is available
          if (sequenceId) {
            await this.fetchSequenceById(sequenceId)
          }
          return { success: true, data: result }
        }

        return { success: false, message: 'Failed to update step' }
      } catch (error) {
        console.error('Error updating step:', error)
        return { success: false, error: this.parseError(error) }
      }
    },

    async updateFlowTriggers(flowName, triggersData, sequenceId) {
      try {
        console.log('🔄 Updating flow triggers for:', flowName)
        console.log('📝 Triggers data:', triggersData)
        
        // Get current flow
        const currentFlow = await call('frappe.client.get', {
          doctype: 'Mira Flow',
          name: flowName
        })

        if (!currentFlow) {
          return { success: false, message: 'Flow not found' }
        }

        // STEP 1: Create map of existing triggers by trigger_type
        const existingTriggerMap = {}
        ;(currentFlow.trigger_id || []).forEach(trigger => {
          existingTriggerMap[trigger.trigger_type] = trigger
        })

        // STEP 2: Process triggers - reuse existing or create new
        const finalTriggers = []
        const newTriggersData = triggersData.triggers || []
        
        newTriggersData.forEach((newTrigger) => {
          const existingTrigger = existingTriggerMap[newTrigger.trigger_type]
          
          if (existingTrigger) {
            // Reuse existing trigger
            console.log('♻️ Reusing existing trigger:', existingTrigger.name, newTrigger.trigger_type)
            finalTriggers.push({
              ...existingTrigger,
              status: newTrigger.status || 'ACTIVE',
              channel: newTrigger.channel,
              conditions: null
            })
          } else {
            // New trigger
            console.log('✨ New trigger:', newTrigger.trigger_type)
            finalTriggers.push({
              doctype: 'Mira Flow Trigger',
              trigger_type: newTrigger.trigger_type,
              status: newTrigger.status || 'ACTIVE',
              channel: newTrigger.channel,
              conditions: null
            })
          }
        })

        console.log('📝 Final triggers:', finalTriggers)

        // STEP 3: First save - update triggers
        const updatedDoc = {
          ...currentFlow,
          trigger_id: finalTriggers
        }

        const result = await call('frappe.client.save', {
          doc: updatedDoc
        })

        console.log('✅ Step 1 complete - Triggers saved')

        // STEP 4: Get updated flow to get trigger names
        const updatedFlow = await call('frappe.client.get', {
          doctype: 'Mira Flow',
          name: flowName
        })

        // Create trigger map with names
        const triggerMap = {}
        ;(updatedFlow.trigger_id || []).forEach(trigger => {
          triggerMap[trigger.trigger_type] = trigger
        })

        console.log('🔍 Trigger map:', triggerMap)

        // STEP 5: Process actions - keep existing, update, or create new
        const mainActions = (updatedFlow.action_id || []).filter(action => !action.trigger_id)
        console.log('📝 Main actions:', mainActions)

        const finalActions = [...mainActions]

        // Keep existing trigger actions that still have triggers
        ;(updatedFlow.action_id || []).forEach(existingAction => {
          if (existingAction.trigger_id) {
            const trigger = (updatedFlow.trigger_id || []).find(t => t.name === existingAction.trigger_id)
            
            if (trigger) {
              // Check if this trigger has new action data
              const newActionData = (triggersData.trigger_actions || []).find(
                a => a.trigger_type === trigger.trigger_type
              )
              
              if (newActionData) {
                // Update existing action
                console.log('♻️ Updating trigger action:', existingAction.name, trigger.trigger_type)
                finalActions.push({
                  ...existingAction,
                  action_type: newActionData.action_type,
                  channel_type: newActionData.channel_type,
                  action_parameters: newActionData.action_parameters,
                  order: newActionData.order || 0
                })
              } else {
                // Keep existing action as-is
                console.log('♻️ Keeping trigger action:', existingAction.name, trigger.trigger_type)
                finalActions.push(existingAction)
              }
            } else {
              // Trigger was deleted, don't keep this action
              console.log('🗑️ Removing action for deleted trigger:', existingAction.trigger_id)
            }
          }
        })

        // Add new trigger actions (for triggers that don't have actions yet)
        ;(triggersData.trigger_actions || []).forEach((triggerAction) => {
          const trigger = triggerMap[triggerAction.trigger_type]
          
          if (!trigger) {
            console.warn('⚠️ No trigger found for action:', triggerAction.trigger_type)
            return
          }
          
          // Check if we already have action for this trigger
          const alreadyHasAction = finalActions.some(a => a.trigger_id === trigger.name)
          
          if (!alreadyHasAction) {
            console.log('✨ Creating new trigger action for:', triggerAction.trigger_type)
            const linkedAction = {
              doctype: 'Mira Flow Action',
              action_type: triggerAction.action_type,
              channel_type: triggerAction.channel_type,
              action_parameters: triggerAction.action_parameters,
              trigger_id: trigger.name,
              order: triggerAction.order || 0
            }
            finalActions.push(linkedAction)
          }
        })

        console.log('📝 Final actions:', finalActions)

        // STEP 6: Final save - update actions
        const finalDoc = {
          ...updatedFlow,
          action_id: finalActions
        }

        await call('frappe.client.save', {
          doc: finalDoc
        })

        console.log('✅ Step 2 complete - Actions updated')

        // Refresh if sequence_id is available
        if (sequenceId) {
          await this.fetchSequenceById(sequenceId)
        }
        
        return { success: true, data: result }
      } catch (error) {
        console.error('Error updating triggers:', error)
        return { success: false, error: this.parseError(error) }
      }
    },

    async deleteSequenceStep(flowName, sequenceId, stepIndex) {
      try {
        // Delete Mira Flow
        const result = await call('frappe.client.delete', {
          doctype: 'Mira Flow',
          name: flowName
        })

        if (result === undefined) {
          // Update sequence steps JSON to remove the step
          const sequence = await call('frappe.client.get', {
            doctype: 'Mira Sequence',
            name: sequenceId
          })

          let steps = []
          try {
            steps = sequence.steps ? JSON.parse(sequence.steps) : []
          } catch (e) {
            console.error('Error parsing steps:', e)
          }

          // Remove step at index
          if (stepIndex !== undefined && stepIndex >= 0 && stepIndex < steps.length) {
            steps.splice(stepIndex, 1)
          }

          await call('frappe.client.set_value', {
            doctype: 'Mira Sequence',
            name: sequenceId,
            fieldname: { steps: JSON.stringify(steps) }
          })

          // Refresh
          await this.fetchSequenceById(sequenceId)
          return { success: true }
        }

        return { success: false, message: 'Failed to delete step' }
      } catch (error) {
        console.error('Error deleting step:', error)
        return { success: false, error: this.parseError(error) }
      }
    },

    formatDate(dateString) {
      if (!dateString) return ''
      
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
    },

    formatRelativeDate(dateString) {
      if (!dateString) return ''
      
      try {
        const date = new Date(dateString)
        const now = new Date()
        const diffInSeconds = Math.floor((now - date) / 1000)
        
        if (diffInSeconds < 60) return 'Vừa xong'
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} phút trước`
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} giờ trước`
        if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 86400)} ngày trước`
        
        return this.formatDate(dateString)
      } catch (error) {
        return dateString
      }
    },

    parseError(error) {
      if (typeof error === 'string') return error
      if (error?.message) return error.message
      if (error?.exc_type && error?.exc) return `${error.exc_type}: ${error.exc}`
      return 'An unexpected error occurred'
    },

    // Filter methods
    setSearch(searchText) {
      this.filters.search = searchText
    },

    setStatusFilter(status) {
      this.filters.status = status
    },

    setOwnerFilter(owner) {
      this.filters.owner = owner
    },

    clearFilters() {
      this.filters = {
        search: '',
        status: '',
        owner: ''
      }
    }
  }
})
