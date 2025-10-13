<template>
	<div class="mx-auto">
		<form @submit.prevent="handleSubmit" class="space-y-6">
			<!-- Title -->
			<div>
				<label class="block text-sm font-medium text-gray-700 mb-2">
					{{ __('Segment Name') }} <span class="text-red-500">*</span>
				</label>
				<input v-model="formData.title" type="text" :placeholder="__('Enter segment name...')"
					class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
					:class="{ 'border-red-500': errors.title }" maxlength="100" required />
				<p v-if="errors.title" class="mt-1 text-sm text-red-600">{{ errors.title }}</p>
				<p class="mt-1 text-sm text-gray-500">
					{{ __('This name will be displayed in the segment list') }}
				</p>
			</div>

			<!-- Description -->
			<div>
				<label class="block text-sm font-medium text-gray-700 mb-2">
					{{ __('Description') }}
				</label>
				<textarea v-model="formData.description" rows="3"
					:placeholder="__('Detailed description of this segment...')"
					class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
					:class="{ 'border-red-500': errors.description }" maxlength="500" />
				<p v-if="errors.description" class="mt-1 text-sm text-red-600">
					{{ errors.description }}
				</p>
				<p class="mt-1 text-sm text-gray-500">
					{{ __('Description will help others understand the purpose of the segment') }}
				</p>
			</div>

			<!-- Type and Owner in a row -->
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				<!-- Type -->
				<div>
					<label class="block text-sm font-medium text-gray-700 mb-2">
						{{ __('Segment Type') }} <span class="text-red-500">*</span>
					</label>
					<select v-model="formData.type"
						class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
						:class="{ 'border-red-500': errors.type }" required>
						<option value="">{{ __('Select segment type') }}</option>
						<option v-for="option in typeOptions" :key="option.value" :value="option.value">
							{{ option.title }}
						</option>
					</select>
					<p v-if="errors.type" class="mt-1 text-sm text-red-600">{{ errors.type }}</p>
				</div>

				<!-- Owner -->
				<div>
					<label class="block text-sm font-medium text-gray-700 mb-2">
						{{ __('Manager') }}
					</label>
					<select v-model="formData.owner_id"
						class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
						:class="{ 'border-red-500': errors.owner_id }">
						<option value="">{{ __('Select manager') }}</option>
						<option v-for="user in userOptions" :key="user.name" :value="user.name">
							{{ user.full_name }}
						</option>
					</select>
					<p v-if="errors.owner_id" class="mt-1 text-sm text-red-600">
						{{ errors.owner_id }}
					</p>
				</div>
			</div>



			<!-- AI Configuration (only for DYNAMIC type) -->
			<div class="">


				<!-- Skills Selection -->
				<div class="mb-4">
					<label class="block text-sm font-medium text-gray-700 mb-2">
						{{ __('Skills') }}
					</label>
					<div class="space-y-2">
						<div class="flex flex-wrap gap-2">
							<span v-for="(skill, index) in criteriaForm.skills" :key="index"
								class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
								{{ skill }}
								<button type="button" @click="removeSkill(index)"
									class="ml-1.5 h-4 w-4 rounded-full inline-flex items-center justify-center text-blue-400 hover:bg-blue-200 hover:text-blue-500 focus:outline-none">
									<svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
										<path stroke-linecap="round" stroke-width="1.5" d="m1 1 6 6m0-6-6 6" />
									</svg>
								</button>
							</span>
						</div>

						<!-- Preview của skills sẽ được thêm (optional) -->
						<div v-if="previewSkills.length > 0" class="flex flex-wrap gap-2">
							<span class="text-xs text-gray-500 w-full">{{ __('Will be added:') }}</span>
							<span v-for="(skill, index) in previewSkills" :key="`preview-${index}`"
								class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600 border-2 border-dashed border-gray-300">
								{{ skill }}
							</span>
						</div>
						<input v-model="newSkill" @keydown.enter.prevent="addSkill" type="text"
							:placeholder="__('Enter skills separated by commas (e.g. React, Vue, Pinia...)')"
							class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
						<p class="text-xs text-gray-500">
							{{ __('Tip: You can enter multiple skills at once by separating them with commas') }}
						</p>
					</div>
				</div>
				<!-- Tags -->
				<div class="mb-4">
					<label class="block text-sm font-medium text-gray-700 mb-2">
						{{ __('Tags') }}
					</label>
					<div class="space-y-2">
						<div class="flex flex-wrap gap-2">
							<span v-for="(tag, index) in criteriaForm.tags" :key="index"
								class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
								{{ tag }}
								<button type="button" @click="removeTag(index)"
									class="ml-1.5 h-4 w-4 rounded-full inline-flex items-center justify-center text-blue-400 hover:bg-blue-200 hover:text-blue-500 focus:outline-none">
									<svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
										<path stroke-linecap="round" stroke-width="1.5" d="m1 1 6 6m0-6-6 6" />
									</svg>
								</button>
							</span>
						</div>

						<!-- Preview của skills sẽ được thêm (optional) -->
						<div v-if="previewTags.length > 0" class="flex flex-wrap gap-2">
							<span class="text-xs text-gray-500 w-full">{{ __('Will be added:') }}</span>
							<span v-for="(tag, index) in previewTags" :key="`preview-${index}`"
								class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600 border-2 border-dashed border-gray-300">
								{{ tag }}
							</span>
						</div>
						<input v-model="newTag" @keydown.enter.prevent="addTag" type="text"
							:placeholder="__('Enter Tags separated by commas (e.g. Job Fair 2025...)')"
							class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
						<p class="text-xs text-gray-500">
							{{ __('Tip: You can enter multiple tag at once by separating them with commas') }}
						</p>
					</div>
				</div>
				<div class="mb-4">
					<label class="block text-sm font-medium text-gray-700 mb-2">
						{{ __('Source') }}
					</label>
					<div class="space-y-2">
						<input v-model="criteriaForm.source" type="text"
							:placeholder="__('Enter source (e.g. Hanoi, Ho Chi Minh City...)')"
							class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
					</div>
				</div>
				<!-- Experience Years -->
				<div class="mb-4">
					<label class="block text-sm font-medium text-gray-700 mb-2">
						{{ __('Work Experience') }}
					</label>
					<div class="grid grid-cols-3 gap-3">
						<select v-model="criteriaForm.experienceOperator"
							class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
							<option value=">=">&gt;= {{ __('At least') }}</option>
							<option value="=">=== {{ __('Exactly') }}</option>
							<option value="<=">&lt;= {{ __('Maximum') }}</option>
						</select>
						<div class="col-span-2">
							<input v-model.number="criteriaForm.experienceYears" type="number" min="0" max="50"
								:placeholder="__('Years of experience')"
								class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
						</div>
					</div>
				</div>

				<!-- Education Level -->
				<div class="mb-4">
					<label class="block text-sm font-medium text-gray-700 mb-2">
						{{ __('Education Level') }}
					</label>
					<select v-model="criteriaForm.educationLevel"
						class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
						<option value="">{{ __('No requirement') }}</option>
						<option value="high_school">{{ __('High School') }}</option>
						<option value="diploma">{{ __('Diploma') }}</option>
						<option value="bachelor">{{ __("Bachelor's Degree") }}</option>
						<option value="master">{{ __("Master's Degree") }}</option>
						<option value="phd">{{ __('PhD') }}</option>
					</select>
				</div>

				<!-- Location -->
				<div class="mb-4">
					<label class="block text-sm font-medium text-gray-700 mb-2">
						{{ __('Preferred Work Location') }}
					</label>
					<div class="space-y-2">
						<div class="flex flex-wrap gap-2">
							<span v-for="(location, index) in criteriaForm.locations" :key="index"
								class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
								{{ location }}
								<button type="button" @click="removeLocation(index)"
									class="ml-1.5 h-4 w-4 rounded-full inline-flex items-center justify-center text-green-400 hover:bg-green-200 hover:text-green-500 focus:outline-none">
									<svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
										<path stroke-linecap="round" stroke-width="1.5" d="m1 1 6 6m0-6-6 6" />
									</svg>
								</button>
							</span>
						</div>
						<input v-model="newLocation" @keydown.enter.prevent="addLocation" type="text"
							:placeholder="__('Enter location and press Enter (e.g. Hanoi, Ho Chi Minh City...)')"
							class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
					</div>
				</div>

				<!-- Salary Range -->
				<div class="grid grid-cols-2 gap-4">
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-2">
							{{ __('Minimum Salary') }}
						</label>
						<input v-model.number="criteriaForm.salaryMin" type="number" min="0" step="0.5"
							:placeholder="__('e.g. 15 million VND')"
							class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
					</div>
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-2">
							{{ __('Maximum Salary') }}
						</label>
						<input v-model.number="criteriaForm.salaryMax" type="number" min="0" step="0.5"
							:placeholder="__('e.g. 30 million VND')"
							class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
					</div>
				</div>
			</div>

		</form>
	</div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { Button } from 'frappe-ui'
import { useTalentSegmentStore } from '@/stores/talentSegment'
import { call } from 'frappe-ui'

// Store initialization
const talentSegmentStore = useTalentSegmentStore()

// Translation helper function


// Props
const props = defineProps({
	segment: {
		type: Object,
		default: null,
	},
	visible: {
		type: Boolean,
		default: true,
	},
})

// Emits
const emit = defineEmits(['success', 'cancel'])

// Local state
const loading = ref(false)
const loadingUsers = ref(false)
const userOptions = ref([])
const errors = ref({})

// Form fields for new skills and locations
const newSkill = ref('')
const newLocation = ref('')
const newTag = ref('')

const formData = ref({
	title: '',
	description: '',
	type: 'MANUAL',
	owner_id: '',
	candidate_count: 0,
	criteria: '{}',
})

// Criteria form for better UX
const criteriaForm = ref({
	skills: [],
	tags:[],
	source:"",
	experienceOperator: '>=',
	experienceYears: null,
	locations: [],
	educationLevel: '',
	salaryMin: null,
	salaryMax: null,
})

// Type options
const typeOptions = [
	{
		title: __('Manual'),
		value: 'MANUAL',
	},
	{
		title: __('Automatic'),
		value: 'DYNAMIC',
	},
]

// Computed
const isEditing = computed(() => !!props.segment)

// Validation
const validateForm = () => {
	errors.value = {}

	if (!formData.value.title || formData.value.title.trim().length < 3) {
		errors.value.title = __('Segment name must be at least 3 characters')
	}

	if (formData.value.title && formData.value.title.length > 100) {
		errors.value.title = __('Segment name cannot exceed 100 characters')
	}

	if (formData.value.description && formData.value.description.length > 500) {
		errors.value.description = __('Description cannot exceed 500 characters')
	}

	if (!formData.value.type) {
		errors.value.type = __('Segment type is required')
	}

	if (formData.value.candidate_count < 0) {
		errors.value.candidate_count = __('Number of candidates must be >= 0')
	}

	return Object.keys(errors.value).length === 0
}

// Convert form to JSON criteria
const convertFormToCriteria = () => {
	const criteria = {}

	if (criteriaForm.value.skills?.length > 0) {
		criteria.skills = criteriaForm.value.skills
	}

	if (criteriaForm.value.tags?.length > 0) {
		criteria.tags = criteriaForm.value.tags
	}

	if (criteriaForm.value.experienceYears !== null && criteriaForm.value.experienceYears !== '') {
		criteria.experienceYears = `${criteriaForm.value.experienceOperator}${criteriaForm.value.experienceYears}`
	}

	if (criteriaForm.value.locations?.length > 0) {
		criteria.locations = criteriaForm.value.locations
	}

	if (criteriaForm.value.educationLevel) {
		criteria.educationLevel = criteriaForm.value.educationLevel
	}
	if (criteriaForm.value.source !== null){
		criteria.source = criteriaForm.value.source
	}

	if (criteriaForm.value.salaryMin !== null || criteriaForm.value.salaryMax !== null) {
		const salaryRange = {}
		if (criteriaForm.value.salaryMin !== null && criteriaForm.value.salaryMin !== '') {
			salaryRange.min = criteriaForm.value.salaryMin
		}
		if (criteriaForm.value.salaryMax !== null && criteriaForm.value.salaryMax !== '') {
			salaryRange.max = criteriaForm.value.salaryMax
		}
		if (Object.keys(salaryRange).length > 0) {
			criteria.salaryRange = salaryRange
		}
	}

	return JSON.stringify(criteria)
}

// Convert JSON criteria to form
const parseCriteriaToForm = (criteriaJson) => {
	try {
		const criteria = JSON.parse(criteriaJson || '{}')

		criteriaForm.value = {
			skills: criteria.skills || [],
			tags:criteria.tags || [],
			source:criteria.source || '',
			experienceOperator: '>=',
			experienceYears: null,
			locations: criteria.locations || [],
			educationLevel: criteria.educationLevel || '',
			salaryMin: criteria.salaryRange?.min || null,
			salaryMax: criteria.salaryRange?.max || null,
		}

		// Parse experience years
		if (criteria.experienceYears) {
			const expStr = criteria.experienceYears.toString()
			const match = expStr.match(/^([><=]+)(.+)$/)
			if (match) {
				criteriaForm.value.experienceOperator = match[1]
				criteriaForm.value.experienceYears = parseInt(match[2])
			}
		}
	} catch (error) {
		console.error('Error parsing criteria JSON:', error)
		criteriaForm.value = {
			skills: [],
			tags:[],
			source:"",
			experienceOperator: '>=',
			experienceYears: null,
			locations: [],
			educationLevel: '',
			salaryMin: null,
			salaryMax: null,
		}
	}
}

// Skills management - Enhanced version
const addSkill = () => {
	if (!newSkill.value.trim()) return;

	// Tách chuỗi bằng dấu phẩy và xử lý từng skill
	const skillsToAdd = newSkill.value
		.split(',')
		.map(skill => skill.trim())
		.filter(skill => skill.length > 0) // Loại bỏ string rỗng
		.filter(skill => !criteriaForm.value.skills.includes(skill)); // Loại bỏ skill đã tồn tại

	// Thêm tất cả skills vào mảng
	criteriaForm.value.skills.push(...skillsToAdd);

	// Clear input
	newSkill.value = '';
};

// Nếu bạn muốn hỗ trợ thêm cả dấu chấm phẩy hoặc các ký tự khác
const addSkillAdvanced = () => {
	if (!newSkill.value.trim()) return;

	// Hỗ trợ nhiều loại separator: dấu phẩy, chấm phẩy, pipe
	const skillsToAdd = newSkill.value
		.split(/[,;|]/) // Regex để split bằng nhiều ký tự
		.map(skill => skill.trim())
		.filter(skill => skill.length > 0)
		.filter(skill => !criteriaForm.value.skills.includes(skill));

	criteriaForm.value.skills.push(...skillsToAdd);
	newSkill.value = '';
};

// Hoặc nếu muốn realtime preview khi user đang typing
const previewSkills = computed(() => {
	if (!newSkill.value.trim()) return [];

	return newSkill.value
		.split(',')
		.map(skill => skill.trim())
		.filter(skill => skill.length > 0);
});

const removeSkill = (index) => {
	criteriaForm.value.skills.splice(index, 1)
}

//Tags
const addTag = () => {
	if (!newTag.value.trim()) return;

	// Tách chuỗi bằng dấu phẩy và xử lý từng skill
	const tagsToAdd = newTag.value
		.split(',')
		.map(tag => tag.trim())
		.filter(tag => tag.length > 0) // Loại bỏ string rỗng
		.filter(tag => !criteriaForm.value.tags.includes(tag)); // Loại bỏ skill đã tồn tại

	// Thêm tất cả skills vào mảng
	criteriaForm.value.tags.push(...tagsToAdd);

	// Clear input
	newTag.value = '';
};
const previewTags = computed(() => {
	if (!newTag.value.trim()) return [];

	return newTag.value
		.split(',')
		.map(tag => tag.trim())
		.filter(tag => tag.length > 0);
});

const removeTag = (index) => {
	criteriaForm.value.tags.splice(index, 1)
}

// Locations management
const addLocation = () => {
	if (
		newLocation.value.trim() &&
		!criteriaForm.value.locations.includes(newLocation.value.trim())
	) {
		criteriaForm.value.locations.push(newLocation.value.trim())
		newLocation.value = ''
	}
}

const removeLocation = (index) => {
	criteriaForm.value.locations.splice(index, 1)
}

const resetForm = () => {
	formData.value = {
		title: '',
		description: '',
		type: 'MANUAL',
		owner_id: '',
		candidate_count: 0,
		criteria: '{}',
	}

	criteriaForm.value = {
		skills: [],
		tags:[],
		source:"",
		experienceOperator: '>=',
		experienceYears: null,
		locations: [],
		educationLevel: '',
		salaryMin: null,
		salaryMax: null,
	}

	console.log(formData.value)

	errors.value = {}
}

const loadUserOptions = async () => {
	loadingUsers.value = true
	try {
		const result = await call('frappe.client.get_list', {
			doctype: 'User',
			fields: ['name', 'full_name', 'email'],
			limit_page_length: 100
		})
		if (result && result.length) {
			userOptions.value = result
		}
	} catch (error) {
		console.error('Error loading users:', error)
	} finally {
		loadingUsers.value = false
	}
}

// Event handlers
const handleSubmit = async () => {
	if (!validateForm()) {
		return
	}

	loading.value = true

	try {
		// Convert criteria form to JSON string
		formData.value.criteria = convertFormToCriteria()

		let result
		if (isEditing.value) {
			result = await call('frappe.client.set_value', {
				doctype: 'Mira Segment',
				name: props.segment.name,
				fieldname: formData.value
			})
		} else {
			result = await call('frappe.client.insert', {
				doc: {
					doctype: 'Mira Segment',
					...formData.value
				}
			})
		}

		if (result && (result.name || result.message === 'success')) {
			emit('success', result)
			resetForm()
		} else {
			throw new Error(result?.message || 'Operation failed')
		}
	} catch (error) {
		console.error('Error saving segment:', error)
		// You might want to show an error toast here
	} finally {
		loading.value = false
	}
}

const handleCancel = () => {
	emit('cancel')
	resetForm()
}

// Initialize form when segment prop changes
watch(
	() => props.segment,
	(newSegment) => {
		if (newSegment) {
			formData.value = {
				title: newSegment.title || '',
				description: newSegment.description || '',
				type: newSegment.type || 'MANUAL',
				owner_id: newSegment.owner_id || '',
				candidate_count: newSegment.candidate_count || 0,
				criteria: newSegment.criteria || '{}',
			}

			// Parse criteria to form 
			parseCriteriaToForm(newSegment.criteria)
		} else {
			resetForm()
		}
	},
	{ immediate: true },
)

watch(
	() => props.visible,
	(newVisible) => {
		console.log(!newVisible)
		if (!newVisible) {
			// Reset form when modal becomes visible
			resetForm()
		}
	},
)

// Load users on mount
onMounted(() => {
	loadUserOptions()
})

defineExpose({ handleSubmit })
</script>

<style scoped>
/* Custom form styles - using valid CSS properties */
.form-control:focus {
	box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
	border-color: rgb(59, 130, 246);
}

.error-input {
	border-color: rgb(239, 68, 68);
	box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.5);
}

/* Skill and location chips */
.chip {
	display: inline-flex;
	align-items: center;
	padding: 0.125rem 0.625rem;
	border-radius: 9999px;
	font-size: 0.75rem;
	font-weight: 500;
}

.chip-remove {
	margin-left: 0.375rem;
	height: 1rem;
	width: 1rem;
	border-radius: 9999px;
	display: inline-flex;
	align-items: center;
	justify-content: center;
}

.chip-remove:focus {
	outline: none;
}
</style>
