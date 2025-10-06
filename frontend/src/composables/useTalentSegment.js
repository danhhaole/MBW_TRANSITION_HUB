import { ref, computed, reactive } from 'vue'
import {
	getFilteredTalentSegments,
	getTalentSegmentDetails,
	createNewTalentSegment,
	updateTalentSegmentDetails,
	deleteTalentSegmentById,
	getSegmentTalent,
	addCandidateToTalentSegment,
	removeCandidateFromTalentSegment,
	getUserOptions,
	calculateEngagementRate,
	formatDate,
	getSegmentTypeColor,
	validateTalentSegmentForm,
} from '@/services/talentSegmentService'

// Composable chính cho Mira Segment
export const useTalentSegment = () => {
	const segments = ref([])
	const selectedSegment = ref(null)
	const loading = ref(false)
	const error = ref(null)
	const success = ref(false)

	// Filter state
	const filters = reactive({
		type: 'all',
		searchText: '',
	})

	// Search state
	const isSearching = ref(false)
	const searchDebounceTimeout = ref(null)

	// Computed
	const filteredSegments = computed(() => {
		let result = segments.value || []

		if (filters.type && filters.type !== 'all') {
			result = result.filter((segment) => segment.type === filters.type)
		}

		return result
	})

	const segmentCount = computed(() => segments.value?.length || 0)

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

	const loadSegments = async (params = {}) => {
		loading.value = true
		error.value = null
		try {
			const filterParams = {
				type: filters.type !== 'all' ? filters.type : undefined,
				searchText: filters.searchText || undefined,
				page: params.page || 1,
				limit: params.limit || 20,
			}

			console.log('Loading segments with params:', filterParams)
			const result = await getFilteredTalentSegments(filterParams)
			console.log('result', result)
			// Trả về data và total cho component sử dụng
			const data = result.data || []
			const total = result.pagination.total

			// KHÔNG set segments.value ở đây nếu có params
			// Để component tự xử lý
			if (!params.page) {
				// Chỉ set nếu không có pagination params
				segments.value = data
			}

			return {
				data: data,
				total: total,
			}
		} catch (err) {
			console.error('Error loading segments:', err)
			error.value = err.message
			return { data: [], total: 0 }
		} finally {
			loading.value = false
		}
	}

	const searchSegments = async (searchText) => {
		if (searchDebounceTimeout.value) {
			clearTimeout(searchDebounceTimeout.value)
		}

		searchDebounceTimeout.value = setTimeout(async () => {
			isSearching.value = true
			filters.searchText = searchText

			try {
				await loadSegments()
			} catch (err) {
				console.error('Search error:', err)
				error.value = err.message
			} finally {
				isSearching.value = false
			}
		}, 500) // 500ms debounce
	}

	const clearSearch = () => {
		filters.searchText = ''
		loadSegments()
	}

	const setTypeFilter = (type) => {
		filters.type = type
		loadSegments()
	}

	const getSegmentDetails = async (name) => {
		loading.value = true
		error.value = null
		try {
			const data = await getTalentSegmentDetails(name)
			selectedSegment.value = data
			return data
		} catch (err) {
			error.value = err.message
			throw err
		} finally {
			loading.value = false
		}
	}

	const createSegment = async (segmentData) => {
		loading.value = true
		error.value = null
		success.value = false

		try {
			const validation = validateTalentSegmentForm(segmentData)
			if (!validation.isValid) {
				error.value = Object.values(validation.errors)[0]
				return false
			}

			const newSegment = await createNewTalentSegment(segmentData)
			success.value = true
			await loadSegments() // Refresh list
			return newSegment
		} catch (err) {
			error.value = err.message
			return false
		} finally {
			loading.value = false
		}
	}

	const updateSegment = async (name, updateData) => {
		loading.value = true
		error.value = null
		success.value = false

		try {
			const validation = validateTalentSegmentForm(updateData)
			if (!validation.isValid) {
				error.value = Object.values(validation.errors)[0]
				return false
			}

			const updatedSegment = await updateTalentSegmentDetails(name, updateData)
			success.value = true
			await loadSegments() // Refresh list
			if (selectedSegment.value && selectedSegment.value.name === name) {
				selectedSegment.value = { ...selectedSegment.value, ...updateData }
			}
			return updatedSegment
		} catch (err) {
			error.value = err.message
			return false
		} finally {
			loading.value = false
		}
	}

	const deleteSegment = async (name) => {
		loading.value = true
		error.value = null
		success.value = false

		try {
			await deleteTalentSegmentById(name)
			success.value = true
			await loadSegments() // Refresh list
			if (selectedSegment.value && selectedSegment.value.name === name) {
				selectedSegment.value = null
			}
			return true
		} catch (err) {
			error.value = err.message
			return false
		} finally {
			loading.value = false
		}
	}

	const resetState = () => {
		segments.value = []
		selectedSegment.value = null
		error.value = null
		success.value = false
		filters.type = 'all'
		filters.searchText = ''
	}

	return {
		// State
		segments,
		selectedSegment,
		loading,
		error,
		success,
		filters,
		isSearching,

		// Computed
		filteredSegments,
		segmentCount,

		// Methods
		loadSegments,
		searchSegments,
		clearSearch,
		setTypeFilter,
		getSegmentDetails,
		createSegment,
		updateSegment,
		deleteSegment,
		resetState,

		// Utils
		calculateEngagementRate,
		formatDate,
		getSegmentTypeColor,
	}
}

// Composable cho quản lý ứng viên trong segment
export const useTalentSegmentCandidates = (segmentId) => {
	const candidates = ref([])
	const loading = ref(false)
	const error = ref(null)
	const success = ref(false)

	const candidateCount = computed(() => candidates.value?.length || 0)

	const loadCandidates = async () => {
		if (!segmentId) return

		loading.value = true
		error.value = null
		try {
			const data = await getSegmentTalent(segmentId)
			candidates.value = data
		} catch (err) {
			error.value = err.message
			candidates.value = []
		} finally {
			loading.value = false
		}
	}

	const addCandidate = async (candidateId) => {
		loading.value = true
		error.value = null
		success.value = false

		try {
			await addCandidateToTalentSegment(segmentId, candidateId)
			success.value = true
			await loadCandidates() // Refresh list
			return true
		} catch (err) {
			error.value = err.message
			return false
		} finally {
			loading.value = false
		}
	}

	const removeCandidate = async (candidateId) => {
		loading.value = true
		error.value = null
		success.value = false

		try {
			await removeCandidateFromTalentSegment(segmentId, candidateId)
			success.value = true
			await loadCandidates() // Refresh list
			return true
		} catch (err) {
			error.value = err.message
			return false
		} finally {
			loading.value = false
		}
	}

	return {
		candidates,
		loading,
		error,
		success,
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
			const usersData = await getUserOptions()

			users.value = usersData.map((user) => ({
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
		const validation = validateTalentSegmentForm(form.value)
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
