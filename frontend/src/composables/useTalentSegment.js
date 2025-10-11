import { ref, computed, reactive, watch } from 'vue'
import { useTalentSegmentStore } from '@/stores/talentSegment.js'
import { debounce } from 'lodash'
import { call } from 'frappe-ui'

// Composable chính cho Mira Segment
export const useTalentSegment = () => {
	const talentSegmentStore = useTalentSegmentStore()
	
	// Computed properties from store
	const segments = computed(() => talentSegmentStore.talentSegments)
	const selectedSegment = computed(() => talentSegmentStore.currentTalentSegment)
	const loading = computed(() => talentSegmentStore.loading)
	const error = computed(() => talentSegmentStore.error)
	const success = computed(() => talentSegmentStore.success)
	const stats = computed(() => talentSegmentStore.statistics)
	const filterOptions = computed(() => talentSegmentStore.filterOptions)
	const pagination = computed(() => talentSegmentStore.pagination)

	// Filter state
	const filters = reactive({
		type: talentSegmentStore.typeFilter || 'all',
		searchText: talentSegmentStore.searchText || '',
	})

	// Search state
	const isSearching = ref(false)

	// Computed
	const filteredSegments = computed(() => talentSegmentStore.filteredTalentSegments)
	const segmentCount = computed(() => segments.value?.length || 0)
	const hasData = computed(() => segments.value.length > 0)
	const isEmpty = computed(() => !loading.value && segments.value.length === 0)
	const hasFilters = computed(() => {
		return filters.searchText || (filters.type && filters.type !== 'all')
	})

	// Debounced search
	const debouncedSearch = debounce(() => {
		talentSegmentStore.setPagination(1)
		fetchTalentSegments()
	}, 500)
	
	watch(() => filters.searchText, debouncedSearch)

	// Methods
	const enrichSegmentData = async (segment) => {
		try {
			// Extract skills from criteria JSON field
			let topSkills = []
			console.log(segment)
			if (segment.criteria) {
				try {
					const criteria =
						typeof segment.criteria === 'string'
							? JSON.parse(segment.criteria)
							: segment.criteria

					if (criteria.skills && Array.isArray(criteria.skills)) {
						console.log('Extracted skills from criteria:', criteria.skills)
						topSkills = criteria.skills
					}
				} catch (e) {
					console.error('Error parsing criteria JSON for segment:', segment.name, e)
				}
			}

			// Get candidates for this segment from Mira Talent Pool records
			const candidateSegmentData = await getSegmentTalent(segment.name)
			console.log(candidateSegmentData)
			// Extract candidate info for team members display
			const teamMembers = candidateSegmentData
				.map((item) => ({
					name: item.candidate?.name,
					candidate_name: item.candidate?.full_name || item.candidate?.name,
					email: item.candidate?.email,
					phone: item.candidate?.phone,
					status: item.candidate?.status,
					added_at: item.added_at,
				}))
				.filter((member) => member.name) // Filter out any invalid entries

			segment.topSkills = topSkills
			segment.teamMembers = teamMembers
		} catch (error) {
			console.error('Error enriching segment data for:', segment.name, error)
			segment.topSkills = []
			segment.teamMembers = []
		}

		return segment
	}

	const fetchTalentSegments = async (params = {}) => {
		const options = {
			page: params.page || pagination.value.page,
			limit: params.limit || pagination.value.limit,
			searchText: filters.searchText,
			type: filters.type !== 'all' ? filters.type : undefined,
			orderBy: params.orderBy || talentSegmentStore.orderBy
		}
		
		return await talentSegmentStore.fetchTalentSegments(options)
	}

	const loadSegments = async (params = {}) => {
		return await fetchTalentSegments(params)
	}

	const searchSegments = async (searchText) => {
		isSearching.value = true
		filters.searchText = searchText
		talentSegmentStore.setSearchText(searchText)
		
		try {
			return await talentSegmentStore.searchTalentSegments(searchText)
		} catch (err) {
			console.error('Search error:', err)
			return []
		} finally {
			isSearching.value = false
		}
	}

	const clearSearch = () => {
		filters.searchText = ''
		talentSegmentStore.setSearchText('')
		fetchTalentSegments()
	}

	const setTypeFilter = (type) => {
		filters.type = type
		talentSegmentStore.setTypeFilter(type !== 'all' ? type : '')
		fetchTalentSegments()
	}

	const getSegmentDetails = async (name) => {
		return await talentSegmentStore.fetchTalentSegmentById(name)
	}

	const createSegment = async (segmentData) => {
		return await talentSegmentStore.createTalentSegment(segmentData)
	}

	const updateSegment = async (name, updateData) => {
		return await talentSegmentStore.updateTalentSegment(name, updateData)
	}

	const deleteSegment = async (name) => {
		return await talentSegmentStore.deleteTalentSegment(name)
	}

	const resetState = () => {
		talentSegmentStore.resetFilters()
		filters.type = 'all'
		filters.searchText = ''
	}

	// Pagination methods
	const goToPage = (page) => {
		talentSegmentStore.setPagination(page)
		fetchTalentSegments()
	}

	const nextPage = () => {
		if (pagination.value.has_next) {
			goToPage(pagination.value.page + 1)
		}
	}

	const previousPage = () => {
		if (pagination.value.has_prev) {
			goToPage(pagination.value.page - 1)
		}
	}

	const changeItemsPerPage = (newLimit) => {
		talentSegmentStore.setPagination(1, newLimit)
		fetchTalentSegments()
	}

	// Filter methods
	const updateSearch = debounce((searchText) => {
		filters.searchText = searchText
		talentSegmentStore.setSearchText(searchText)
		talentSegmentStore.setPagination(1)
		fetchTalentSegments()
	}, 400)

	const updateType = (type) => {
		filters.type = type
		talentSegmentStore.setTypeFilter(type !== 'all' ? type : '')
		talentSegmentStore.setPagination(1)
		fetchTalentSegments()
	}

	const clearFilters = () => {
		filters.searchText = ''
		filters.type = 'all'
		talentSegmentStore.resetFilters()
		fetchTalentSegments()
	}

	// Statistics
	const fetchStats = async () => {
		return await talentSegmentStore.fetchStatistics()
	}

	// Initialize
	const initialize = async () => {
		await Promise.all([
			fetchTalentSegments(),
			fetchStats()
		])
	}

	return {
		// State
		segments,
		selectedSegment,
		loading,
		error,
		success,
		stats,
		filterOptions,
		pagination,
		filters,
		isSearching,

		// Computed
		filteredSegments,
		segmentCount,
		hasData,
		isEmpty,
		hasFilters,

		// API Methods
		fetchTalentSegments,
		searchSegments: searchSegments,
		getSegmentDetails,
		createSegment,
		updateSegment,
		deleteSegment,
		fetchStats,

		// Pagination
		goToPage,
		nextPage,
		previousPage,
		changeItemsPerPage,

		// Filters
		updateSearch,
		updateType,
		clearFilters,

		// Legacy methods (for backward compatibility)
		loadSegments,
		clearSearch,
		setTypeFilter,
		resetState,

		// Utils
		calculateEngagementRate: talentSegmentStore.calculateEngagementRate,
		formatDate: talentSegmentStore.formatDate,
		getSegmentTypeColor: talentSegmentStore.getSegmentTypeColor,
		
		// Initialize
		initialize
	}
}

// Composable cho quản lý ứng viên trong segment
export const useTalentSegmentCandidates = (segmentId) => {
	const talentSegmentStore = useTalentSegmentStore()
	
	const candidates = computed(() => talentSegmentStore.getSegmentTalents(segmentId))
	const loading = computed(() => talentSegmentStore.loading)
	const error = computed(() => talentSegmentStore.error)
	const success = computed(() => talentSegmentStore.success)
	const pagination = computed(() => talentSegmentStore.talentPoolPagination)

	const candidateCount = computed(() => candidates.value?.length || 0)

	const loadCandidates = async (options = {}) => {
		if (!segmentId) return
		return await talentSegmentStore.fetchSegmentTalents(segmentId, options)
	}

	const addCandidate = async (candidateId) => {
		return await talentSegmentStore.addTalentToSegment(segmentId, candidateId)
	}

	const removeCandidate = async (candidateId) => {
		return await talentSegmentStore.removeTalentFromSegment(segmentId, candidateId)
	}

	return {
		candidates,
		loading,
		error,
		success,
		pagination,
		candidateCount,
		loadCandidates,
		addCandidate,
		removeCandidate,
	}
}

// Composable cho form management
export const useTalentSegmentForm = (initialData = null) => {
	const form = ref({
		title: initialData?.title || '',
		description: initialData?.description || '',
		type: initialData?.type || 'MANUAL',
		criteria: initialData?.criteria || null,
		owner_id: initialData?.owner_id || null,
		candidate_count: initialData?.candidate_count || 0,
	})

	const formErrors = ref({})
	const isValid = ref(false)
	const users = ref([])
	const loadingOptions = ref(false)

	// Validation rules theo Vuetify
	const titleRules = [
		(v) => !!v || 'Tên phân khúc là bắt buộc',
		(v) => (v && v.length >= 3) || 'Tên phân khúc phải có ít nhất 3 ký tự',
		(v) => (v && v.length <= 200) || 'Tên phân khúc không được quá 200 ký tự',
	]

	const descriptionRules = [(v) => !v || v.length <= 1000 || 'Mô tả không được quá 1000 ký tự']

	const typeRules = [(v) => !!v || 'Loại phân khúc là bắt buộc']

	const criteriaRules = [
		(v) => {
			if (!v) return true
			try {
				if (typeof v === 'string') {
					JSON.parse(v)
				}
				return true
			} catch (e) {
				return 'Tiêu chí phải là JSON hợp lệ'
			}
		},
	]

	// Type options
	const typeOptions = [
		{ title: 'Tự động (AI)', value: 'DYNAMIC' },
		{ title: 'Thủ công', value: 'MANUAL' },
	]

	// Load options data
	const loadOptions = async () => {
		loadingOptions.value = true
		try {
			const usersData = await call('frappe.client.get_list', {
				doctype: 'User',
				fields: ['name', 'full_name', 'email'],
				filters: { enabled: 1 },
				limit_page_length: 1000
			})

			users.value = (usersData || []).map((user) => ({
				title: user.full_name || user.name,
				value: user.name,
				subtitle: user.email,
			}))
		} catch (error) {
			console.error('Failed to load options:', error)
		} finally {
			loadingOptions.value = false
		}
	}

	// Validate form
	const validateForm = () => {
		const talentSegmentStore = useTalentSegmentStore()
		const validation = talentSegmentStore.validateTalentSegment(form.value)
		formErrors.value = validation.errors
		isValid.value = validation.isValid
		return validation.isValid
	}

	// Reset form
	const resetForm = () => {
		form.value = {
			title: '',
			description: '',
			type: 'MANUAL',
			criteria: null,
			owner_id: null,
			candidate_count: 0,
		}
		formErrors.value = {}
		isValid.value = false
	}

	// Set form data
	const setFormData = (data) => {
		form.value = {
			title: data.title || '',
			description: data.description || '',
			type: data.type || 'MANUAL',
			criteria: data.criteria || null,
			owner_id: data.owner_id || null,
			candidate_count: data.candidate_count || 0,
		}
	}

	return {
		form,
		formErrors,
		isValid,
		users,
		loadingOptions,
		titleRules,
		descriptionRules,
		typeRules,
		criteriaRules,
		typeOptions,
		loadOptions,
		validateForm,
		resetForm,
		setFormData,
	}
}
