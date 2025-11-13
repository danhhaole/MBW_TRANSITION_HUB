import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useTalentStore = defineStore('talent', {
	state: () => ({
		talents: [],
		currentTalent: null,
		loading: false,
		error: null,
		pagination: {
			page: 1,
			limit: 10,
			total: 0,
			has_next: false,
			has_prev: false,
			showing_from: 0,
			showing_to: 0,
		},
		filters: {
			search: '',
			current_status: '',
			skills: '',
			experience_years: '',
			source: '',
			crm_status: '',
		},
		statistics: {
			total: 0,
			active: 0,
			hired: 0,
			avg_experience: 0,
		},
	}),

	getters: {
		filteredTalents: (state) => {
			let filtered = [...state.talents]

			if (state.filters.search) {
				const search = state.filters.search.toLowerCase()
				filtered = filtered.filter(
					(talent) =>
						talent.full_name?.toLowerCase().includes(search) ||
						talent.email?.toLowerCase().includes(search) ||
						talent.phone?.toLowerCase().includes(search) ||
						talent.skills?.toLowerCase().includes(search),
				)
			}

			if (state.filters.current_status) {
				filtered = filtered.filter(
					(talent) => talent.current_status === state.filters.current_status,
				)
			}

			return filtered
		},

		getTalentByName: (state) => (name) => {
			return state.talents.find((talent) => talent.name === name)
		},

		talentsByStatus: (state) => {
			const statusGroups = {}
			state.talents.forEach((talent) => {
				const status = talent.current_status || 'Unknown'
				if (!statusGroups[status]) {
					statusGroups[status] = []
				}
				statusGroups[status].push(talent)
			})
			return statusGroups
		},

		recentTalents: (state) => {
			const sevenDaysAgo = new Date()
			sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)

			return state.talents.filter((talent) => {
				const createdAt = new Date(talent.creation)
				return createdAt >= sevenDaysAgo
			})
		},
	},

	actions: {
		async fetchTalents(options = {}) {
			this.loading = true
			this.error = null

			try {
				const params = {
					doctype: 'Mira Talent',
					fields: [
						"*"
					],
					limit_page_length: options.limit || this.pagination.limit,
					limit_start: ((options.page || this.pagination.page) - 1) * (options.limit || this.pagination.limit),
					order_by: 'creation desc',
					// Add cache busting parameter
					_cache_bust: Date.now(),
				}

				// Add filters
				if (options.filters) {
					params.filters = options.filters
				}

				// Initialize or_filters array
				if (this.filters.search) {
					if (!params.or_filters) {
						params.or_filters = []
					}
					params.or_filters.push(
						['full_name', 'like', `%${this.filters.search}%`],
						['email', 'like', `%${this.filters.search}%`],
						['phone', 'like', `%${this.filters.search}%`]
					)
				}

				if (this.filters.current_status) {
					params.filters = {
						...params.filters,
						current_status: this.filters.current_status,
					}
				}

				if (this.filters.source) {
					params.filters = {
						...params.filters,
						source: this.filters.source,
					}
				}

				if (this.filters.crm_status) {
					params.filters = {
						...params.filters,
						crm_status: this.filters.crm_status,
					}
				}

				if (this.filters.skills) {
					// Split skills by comma and create individual OR search conditions
					const skillsList = this.filters.skills
						.split(',')
						.map(skill => skill.trim())
						.filter(skill => skill !== '')
					
					if (skillsList.length > 0) {
						// Always use OR filters for skills search (even for single skill)
						if (!params.or_filters) {
							params.or_filters = []
						}
						// Add OR conditions for each skill
						skillsList.forEach(skill => {
							params.or_filters.push(['skills', 'like', `%${skill}%`])
						})
					}
				}

				// Try the new combined API first, fallback to old API if it fails
				let result
				try {
					result = await call('mbw_mira.api.doc.get_list_data', params)

					if (result && result.success && Array.isArray(result.data)) {
						// Enhance data with display fields
						this.talents = result.data.map((talent) => ({
							...talent,
							formatted_created_at: this.formatDate(talent.creation),
							formatted_modified: this.formatRelativeDate(talent.modified),
							status_color: this.getStatusColor(talent.current_status),
							experience_display: this.formatExperience(talent.experience_years),
						}))

						// Update pagination - use data.length when searching to match current page results
						this.pagination.total = this.filters.search ? result.data.length : (result.count || 0)
						this.pagination.page = options.page || 1
						this.pagination.limit = options.limit || this.pagination.limit
						this.pagination.showing_from =
							this.pagination.total > 0
								? (this.pagination.page - 1) * this.pagination.limit + 1
								: 0
						this.pagination.showing_to = Math.min(
							this.pagination.page * this.pagination.limit,
							this.pagination.total,
						)
						this.pagination.has_next =
							this.pagination.showing_to < this.pagination.total
						this.pagination.has_prev = this.pagination.page > 1

						return { success: true, data: this.talents, count: result.count }
					} else {
						throw new Error('New API returned invalid response')
					}
				} catch (newApiError) {
					console.warn('New API failed, falling back to old API:', newApiError.message)

					// Fallback to old separate API calls
					const [listResult, countResult] = await Promise.all([
						call('frappe.client.get_list', params),
						this.filters.search ? Promise.resolve(0) : call('frappe.client.get_count', {
							doctype: 'Mira Talent',
							filters: params.filters,
							or_filters: params.or_filters,
						}),
					])

					if (listResult && Array.isArray(listResult)) {
						// Enhance data with display fields
						this.talents = listResult.map((talent) => ({
							...talent,
							formatted_created_at: this.formatDate(talent.creation),
							formatted_modified: this.formatRelativeDate(talent.modified),
							status_color: this.getStatusColor(talent.current_status),
							experience_display: this.formatExperience(talent.experience_years),
						}))

						// Update pagination - use data.length when searching to match current page results
						this.pagination.total = this.filters.search ? listResult.length : (countResult || 0)
						this.pagination.page = options.page || 1
						this.pagination.limit = options.limit || this.pagination.limit
						this.pagination.showing_from =
							this.pagination.total > 0
								? (this.pagination.page - 1) * this.pagination.limit + 1
								: 0
						this.pagination.showing_to = Math.min(
							this.pagination.page * this.pagination.limit,
							this.pagination.total,
						)
						this.pagination.has_next =
							this.pagination.showing_to < this.pagination.total
						this.pagination.has_prev = this.pagination.page > 1

						return { success: true, data: this.talents, count: countResult }
					}
				}

				return { success: false, message: 'No data received' }
			} catch (error) {
				console.error('Error fetching talents:', error)
				this.error = this.parseError(error)
				return { success: false, error: this.error }
			} finally {
				this.loading = false
			}
		},

		async fetchTalentById(id) {
			this.loading = true
			this.error = null

			try {
				const talentResult = await call('frappe.client.get', {
					doctype: 'Mira Talent',
					name: id,
				})

				if (talentResult && talentResult.name) {
					// Enhance data with display fields
					const enhancedTalent = {
						...talentResult,
						status_color: this.getStatusColor(talentResult.current_status),
						formatted_created_at: this.formatDate(talentResult.creation),
						formatted_modified: this.formatRelativeDate(talentResult.modified),
						experience_display: this.formatExperience(talentResult.experience_years),
					}

					this.currentTalent = enhancedTalent
					return { success: true, data: enhancedTalent }
				}

				return { success: false, message: 'Talent not found' }
			} catch (error) {
				console.error('Error fetching talent:', error)
				this.error = this.parseError(error)
				return { success: false, error: this.error }
			} finally {
				this.loading = false
			}
		},

		async createTalent(talentData) {
			this.loading = true
			this.error = null

			console.log("talentData>>>>>>", talentData);
			

			try {
				const validationResult = this.validateTalent(talentData)
				if (!validationResult.isValid) {
					throw new Error(validationResult.message)
				}

				const preparedData = this.prepareTalentForSave(talentData)

				console.log('Prepared Data>>>>:', preparedData);
				
				const result = await call('frappe.client.insert', {
					doc: {
						doctype: 'Mira Talent',
						...preparedData,
					},
				})

				if (result && result.name) {
					// Refresh talents list
					await this.fetchTalents()
					return { success: true, data: result }
				}

				return { success: false, message: 'Failed to create talent' }
			} catch (error) {
				console.error('Error creating talent:', error)
				this.error = this.parseError(error)
				return { success: false, error: this.error }
			} finally {
				this.loading = false
			}
		},

		async updateTalent(name, talentData) {
			this.loading = true
			this.error = null

			try {
				const validationResult = this.validateTalent(talentData)
				if (!validationResult.isValid) {
					throw new Error(validationResult.message)
				}

				const preparedData = this.prepareTalentForSave(talentData)

				const result = await call('frappe.client.set_value', {
					doctype: 'Mira Talent',
					name: name,
					fieldname: preparedData,
				})

				if (result) {
					// Refresh talents list
					await this.fetchTalents()
					return { success: true, data: result }
				}

				return { success: false, message: 'Failed to update talent' }
			} catch (error) {
				console.error('Error updating talent:', error)
				this.error = this.parseError(error)
				return { success: false, error: this.error }
			} finally {
				this.loading = false
			}
		},

		async deleteTalent(talentId) {
			this.loading = true
			this.error = null

			try {
				const result = await call('frappe.client.delete', {
					doctype: 'Mira Talent',
					name: talentId,
				})

				if (result === undefined) {
					// Remove from local state
					this.talents = this.talents.filter((talent) => talent.name !== talentId)

					// Update pagination
					this.pagination.total = Math.max(0, this.pagination.total - 1)

					return { success: true }
				}

				return { success: false, message: 'Failed to delete talent' }
			} catch (error) {
				console.error('Error deleting talent:', error)
				this.error = this.parseError(error)
				return { success: false, error: this.error }
			} finally {
				this.loading = false
			}
		},

		async searchTalents(searchText) {
			this.filters.search = searchText
			return await this.fetchTalents({ page: 1 })
		},

		async fetchStatistics() {
			try {
				// Try new API first
				try {
					const result = await call('mbw_mira.api.doc.get_list_data', {
						doctype: 'Mira Talent',
						fields: ['name', 'current_status', 'experience_years'],
						limit_page_length: 999999, // Get all for statistics
					})

					if (result && result.success && Array.isArray(result.data)) {
						const talents = result.data
						const total = talents.length
						const active = talents.filter((t) => t.current_status === 'Active').length
						const hired = talents.filter((t) => t.current_status === 'Hired').length
						const avgExperience =
							talents.reduce(
								(sum, t) => sum + (parseFloat(t.experience_years) || 0),
								0,
							) / total || 0

						this.statistics = {
							total,
							active,
							hired,
							avg_experience: Math.round(avgExperience * 10) / 10,
						}
						return this.statistics
					} else {
						throw new Error('New API returned invalid response')
					}
				} catch (newApiError) {
					console.warn(
						'New API failed for statistics, falling back to old API:',
						newApiError.message,
					)

					// Fallback to old API
					const totalResult = await call('frappe.client.get_count', {
						doctype: 'Mira Talent',
					})
					const activeResult = await call('frappe.client.get_count', {
						doctype: 'Mira Talent',
						filters: { current_status: 'Active' },
					})
					const hiredResult = await call('frappe.client.get_count', {
						doctype: 'Mira Talent',
						filters: { current_status: 'Hired' },
					})

					this.statistics = {
						total: totalResult || 0,
						active: activeResult || 0,
						hired: hiredResult || 0,
						avg_experience: 0, // Can't calculate without full data
					}
					return this.statistics
				}
			} catch (error) {
				console.error('Error fetching statistics:', error)
				return this.statistics
			}
		},

		async getTalent(name) {
			try {
				const result = await call('frappe.client.get', {
					doctype: 'Mira Talent',
					name: name,
				})

				if (result) {
					return {
						success: true,
						data: {
							...result,
							formatted_created_at: this.formatDate(result.creation),
							formatted_modified: this.formatRelativeDate(result.modified),
							status_color: this.getStatusColor(result.current_status),
							experience_display: this.formatExperience(result.experience_years),
						},
					}
				}

				return { success: false, error: 'Talent not found' }
			} catch (error) {
				console.error('Error fetching talent:', error)
				return {
					success: false,
					error: this.parseError(error) || 'Failed to fetch talent details',
				}
			}
		},

		async checkEmailExists(email) {
			if (!email) return false
			try {
				const result = await call('frappe.client.get_list', {
					doctype: 'Mira Talent',
					filters: { email: email },
					fields: ['name'],
					limit: 1,
				})
				return result && result.length > 0
			} catch (error) {
				console.error('Error checking email:', error)
				return false
			}
		},

		// Helper methods
		validateTalent(talentData) {
			if (!talentData.full_name || talentData.full_name.trim().length === 0) {
				return { isValid: false, message: 'Full name is required' }
			}

			if (talentData.email && !this.isValidEmail(talentData.email)) {
				return { isValid: false, message: 'Invalid email format' }
			}

			return { isValid: true }
		},

		prepareTalentForSave(talentData) {
			return {
				full_name: talentData.full_name?.trim(),
				email: talentData.email?.trim(),
				phone: talentData.phone?.trim(),
				gender: talentData.gender,
				date_of_birth: talentData.date_of_birth,
				linkedin_profile: talentData.linkedin_profile?.trim(),
				facebook_profile: talentData.facebook_profile?.trim(),
				zalo_profile: talentData.zalo_profile?.trim(),
				current_location: talentData.current_location?.trim(),
				preferred_location: talentData.preferred_location?.trim(),
				skills: talentData.skills?.trim(),
				tags: talentData.tags?.trim(),
				source: talentData.source?.trim(),
				experience_years: parseFloat(talentData.experience_years) || 0,
				education: talentData.education,
				experience: talentData.experience,
				certifications: talentData.certifications,
				languages: talentData.languages,
				resume: talentData.resume || '',
				current_status: talentData.current_status || 'Active',
				notes: talentData.notes?.trim(),
				latest_company: talentData.latest_company?.trim(),
				total_years_of_experience: parseFloat(talentData.total_years_of_experience) || 0,
				desired_role: talentData.desired_role?.trim(),
				interaction_notes: talentData.interaction_notes?.trim(),
			}
		},

		isValidEmail(email) {
			const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
			return emailRegex.test(email)
		},

		getStatusColor(status) {
			switch (status) {
				case 'Active':
					return 'success'
				case 'Passive':
					return 'warning'
				case 'Not Interested':
					return 'error'
				case 'Hired':
					return 'info'
				default:
					return 'default'
			}
		},

		formatExperience(years) {
			if (!years) return 'N/A'
			const num = parseFloat(years)
			if (num === 1) return '1 year'
			return `${num} years`
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
					minute: '2-digit',
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
				if (diffInSeconds < 2592000)
					return `${Math.floor(diffInSeconds / 86400)} ngày trước`

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
			this.filters.current_status = status
		},

		setSkillsFilter(skills) {
			this.filters.skills = skills
		},

		setExperienceFilter(experience) {
			this.filters.experience_years = experience
		},

		setSourceFilter(source) {
			this.filters.source = source
		},

		setCrmStatusFilter(crmStatus) {
			this.filters.crm_status = crmStatus
		},

		setFilters(filterObj) {
			Object.keys(filterObj).forEach(key => {
				if (this.filters.hasOwnProperty(key)) {
					// Handle array format for skills filter (from old logic)
					if (key === 'skills' && Array.isArray(filterObj[key])) {
						// Check if it's the old 'like' format
						if (filterObj[key][0] === 'like' && typeof filterObj[key][1] === 'string') {
							// Old format: ['like', '%python%']
							this.filters[key] = filterObj[key][1].replace(/%/g, '')
						} else {
							this.filters[key] = filterObj[key]
						}
					} else {
						// Direct assignment for string values
						this.filters[key] = filterObj[key]
					}
				}
			})
		},

		clearFilters() {
			this.filters = {
				search: '',
				current_status: '',
				skills: '',
				experience_years: '',
				source: '',
				crm_status: '',
			}
		},
	},
})
