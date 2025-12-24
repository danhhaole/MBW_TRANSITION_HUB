<template>
	<div class="space-y-6">
		<!-- Statistics Cards -->
		<div class="grid grid-cols-1 md:grid-cols-4 gap-6">
			<div class="bg-blue-50 rounded-lg p-6">
				<div class="flex items-center">
					<div class="p-3 rounded-full bg-blue-100">
						<FeatherIcon name="briefcase" class="w-6 h-6 text-blue-600" />
					</div>
					<div class="ml-4">
						<p class="text-sm font-medium text-blue-600">
							{{ __('Total Interactions (Open/Click)') }}
						</p>
						<p class="text-2xl font-bold text-blue-900">{{ totalInteractions }}</p>
					</div>
				</div>
			</div>

			<div class="bg-green-50 rounded-lg p-6">
				<div class="flex items-center">
					<div class="p-3 rounded-full bg-green-100">
						<FeatherIcon name="check-circle" class="w-6 h-6 text-green-600" />
					</div>
					<div class="ml-4">
						<p class="text-sm font-medium text-green-600">
							{{ __('Time to MQL (Days)') }}
						</p>
						<p class="text-2xl font-bold text-green-900">{{ engagementTimeline }}</p>
					</div>
				</div>
			</div>

			<div class="bg-purple-50 rounded-lg p-6">
				<div class="flex items-center">
					<div class="p-3 rounded-full bg-purple-100">
						<FeatherIcon name="star" class="w-6 h-6 text-purple-600" />
					</div>
					<div class="ml-4">
						<p class="text-sm font-medium text-purple-600">
							{{ __('Engagement Score') }}
						</p>
						<p class="text-2xl font-bold text-purple-900">{{ engagementScore }}/100</p>
					</div>
				</div>
			</div>

			<div class="bg-orange-50 rounded-lg p-6">
				<div class="flex items-center">
					<div class="p-3 rounded-full bg-orange-100">
						<FeatherIcon name="clock" class="w-6 h-6 text-orange-600" />
					</div>
					<div class="ml-4">
						<p class="text-sm font-medium text-orange-600">
							{{ __('Last Interaction Date') }}
						</p>
						<p class="text-xl font-bold text-orange-900">{{ lastInteractionDate }}</p>
					</div>
				</div>
			</div>
		</div>

		<!-- Resume Summary Section -->
		<div v-if="talent.resume_summary" class="bg-white rounded-lg border border-gray-200 p-6">
			<div class="flex items-center justify-between mb-4">
				<h3 class="text-lg font-medium text-gray-900">Profile Summary</h3>
				<span
					class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
					:class="talent.resume_extract ? 'bg-orange-100 text-orange-800' : 'bg-blue-100 text-blue-800'"
				>
					<FeatherIcon :name="talent.resume_extract ? 'file-text' : 'user'" class="w-3 h-3 mr-1" />
					{{ talent.resume_extract ? 'Generated from CV' : 'Profile Summary' }}
				</span>
			</div>

			<div class="prose max-w-none text-gray-600">
				<template v-if="isValidJson(talent.resume_summary)">
					<template v-if="parsedResumeSummary?.summary">
						<p class="mb-4">{{ parsedResumeSummary.summary }}</p>
					</template>
					
					<template v-if="parsedResumeSummary?.skills?.length">
						<h4 class="text-sm font-medium text-gray-800 mt-4 mb-2">Key Skills</h4>
						<div class="flex flex-wrap gap-2">
							<span v-for="(skill, index) in parsedResumeSummary.skills" :key="index" 
								class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
								{{ skill }}
							</span>
						</div>
					</template>

					<template v-if="parsedResumeSummary?.technical_stack?.length">
						<h4 class="text-sm font-medium text-gray-800 mt-4 mb-2">Technical Stack</h4>
						<div class="flex flex-wrap gap-2">
							<span v-for="(tech, index) in parsedResumeSummary.technical_stack" :key="'tech-'+index"
								class="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-green-100 text-green-800">
								{{ tech }}
							</span>
						</div>
					</template>

					<template v-if="parsedResumeSummary?.achievements?.length">
						<h4 class="text-sm font-medium text-gray-800 mt-4 mb-2">Key Achievements</h4>
						<ul class="list-disc pl-5 space-y-1">
							<li v-for="(achievement, index) in parsedResumeSummary.achievements" :key="'ach-'+index">
								{{ achievement }}
							</li>
						</ul>
					</template>
				</template>
				<template v-else>
					{{ talent.resume_summary }}
				</template>
			</div>
		</div>

		<!-- CV Extract Section -->
		<div v-if="talent.resume_extract" class="bg-white rounded-lg border border-gray-200 p-6 mt-6">
			<div class="flex items-center justify-between mb-4">
				<h3 class="text-lg font-medium text-gray-900">CV Details</h3>
				<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
					<FeatherIcon name="file-text" class="w-3 h-3 mr-1" />
					Extracted from CV
				</span>
			</div>

			<template v-if="isValidJson(talent.resume_extract)">
				<template v-if="parsedResumeExtract">
					<!-- Personal Info -->
					<template v-if="parsedResumeExtract.personal_info">
						<h4 class="text-sm font-medium text-gray-800 mb-2">Personal Information</h4>
						<div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-600 mb-4">
							<template v-if="parsedResumeExtract.personal_info.name">
								<div>Full Name:</div>
								<div class="font-medium">{{ parsedResumeExtract.personal_info.name }}</div>
							</template>
							<template v-if="parsedResumeExtract.personal_info.email">
								<div>Email:</div>
								<div>{{ parsedResumeExtract.personal_info.email }}</div>
							</template>
							<template v-if="parsedResumeExtract.personal_info.phone">
								<div>Phone:</div>
								<div>{{ parsedResumeExtract.personal_info.phone }}</div>
							</template>
						</div>
					</template>

					<!-- Work Experience -->
					<template v-if="parsedResumeExtract.work_experience?.length">
						<h4 class="text-sm font-medium text-gray-800 mt-6 mb-3">Work Experience</h4>
						<div class="space-y-4">
							<div v-for="(exp, idx) in parsedResumeExtract.work_experience" :key="'exp-'+idx" class="border-l-2 border-gray-200 pl-4">
								<div class="font-medium">{{ exp.position || 'Unspecified Position' }}</div>
								<div class="text-sm text-blue-600">{{ exp.company || 'Unspecified Company' }}</div>
								<div class="text-xs text-gray-500 mb-2">
									{{ formatDateRange(exp.start_date, exp.end_date) }}
								</div>
								<p v-if="exp.summary" class="text-sm text-gray-600 mt-1">{{ exp.summary }}</p>
							</div>
						</div>
					</template>

					<!-- Education -->
					<template v-if="parsedResumeExtract.education?.length">
						<h4 class="text-sm font-medium text-gray-800 mt-6 mb-3">Education</h4>
						<div class="space-y-3">
							<div v-for="(edu, idx) in parsedResumeExtract.education" :key="'edu-'+idx" class="text-sm">
								<div class="font-medium">{{ edu.degree || 'Unspecified Degree' }}</div>
								<div class="text-gray-600">{{ edu.institution || 'Unspecified Institution' }}</div>
								<div class="text-xs text-gray-500">
									{{ formatDateRange(edu.start_date, edu.end_date) }}
									<span v-if="edu.gpa"> • GPA: {{ edu.gpa }}</span>
								</div>
							</div>
						</div>
					</template>

					<!-- Skills -->
					<template v-if="parsedResumeExtract.skills?.length">
						<h4 class="text-sm font-medium text-gray-800 mt-6 mb-3">Skills</h4>
						<div class="flex flex-wrap gap-2">
							<span
								v-for="(skill, idx) in parsedResumeExtract.skills"
								:key="'skill-' + idx"
								class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
							>
								<span class="font-semibold">
									{{ getSkillName(skill) }}
								</span>
								<span
									v-if="getSkillDetails(skill)"
									class="ml-1 text-[11px] font-normal text-gray-600"
								>
									- {{ getSkillDetails(skill) }}
								</span>
							</span>
						</div>
					</template>
				</template>
				<pre v-else class="text-sm text-gray-600 bg-gray-50 p-4 rounded overflow-auto">{{ formatJson(talent.resume_extract) }}</pre>
			</template>
		</div>

		<!-- Fallback if no resume data is available -->
		<div
			v-if="!talent.resume_summary && !talent.resume_extract"
			class="bg-white rounded-lg border border-gray-200 p-8 text-center"
		>
			<div class="flex flex-col items-center justify-center">
				<FeatherIcon name="file-text" class="w-12 h-12 text-gray-400 mb-3" />
				<h3 class="text-lg font-medium text-gray-900 mb-1">No Resume Data Available</h3>
				<p class="text-gray-500 text-sm max-w-sm">
					Upload a resume to see the extracted information and summary here.
				</p>
			</div>
		</div>

		<!-- Skills Assessment -->
		<div class="bg-white rounded-lg border border-gray-200 p-6">
			<h3 class="text-lg font-medium text-gray-900 mb-4">{{ __('Skills Assessment') }}</h3>
			<div class="space-y-3">
				<!-- Hard Skills -->
				<div class="text-sm">
					<span class="font-medium text-gray-900">{{ __('Hard Skills') }}:</span>
					<span class="text-gray-600 ml-2">{{ talent.hard_skills || __('None') }}</span>
				</div>

				<!-- Soft Skills -->
				<div class="text-sm">
					<span class="font-medium text-gray-900">{{ __('Soft Skills') }}:</span>
					<span class="text-gray-600 ml-2">{{ talent.soft_skills || __('None') }}</span>
				</div>

				<!-- Domain Expertise -->
				<div class="text-sm">
					<span class="font-medium text-gray-900">{{ __('Domain Expertise') }}:</span>
					<span class="text-gray-600 ml-2">{{
						talent.domain_expertise || __('None')
					}}</span>
				</div>

				<!-- Cultural Fit -->
				<div class="text-sm">
					<span class="font-medium text-gray-900">{{ __('Cultural Fit') }}:</span>
					<span class="text-gray-600 ml-2">{{ talent.cultural_fit || __('None') }}</span>
				</div>

				<!-- Internal Rating -->
				<div class="text-sm">
					<span class="font-medium text-gray-900">{{ __('Internal Rating') }}:</span>
					<span class="text-gray-600 ml-2">{{
						talent.internal_rating || __('None')
					}}</span>
				</div>

				<!-- Availability Date & Expected Salary -->
				<div class="text-sm">
					<span class="font-medium text-gray-900">{{ __('Availability Date') }}:</span>
					<span class="text-gray-600 ml-2">{{
						formatDate(talent.availability_date)
					}}</span>
					<span class="text-gray-400 mx-2">|</span>
					<span class="font-medium text-gray-900">{{ __('Expected Salary') }}:</span>
					<span class="text-gray-600 ml-2">{{
						formatCurrency(talent.expected_salary)
					}}</span>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { FeatherIcon, call } from 'frappe-ui'

const props = defineProps({
	talent: {
		type: Object,
		required: true,
	},
})

const totalInteractions = ref(0)
const engagementTimeline = ref(0)
const engagementScore = ref(0)

// Helper for internationalization
const __ = (text) => text

// Helper function to format currency
const formatCurrency = (amount) => {
	if (!amount) return __('None')
	const num = parseFloat(amount)
	if (isNaN(num)) return __('None')

	return new Intl.NumberFormat('vi-VN', {
		style: 'currency',
		currency: 'VND',
		minimumFractionDigits: 0,
		maximumFractionDigits: 0,
	}).format(num)
}

// Helper function to format date
const formatDate = (dateStr) => {
	if (!dateStr) return __('None')
	try {
		const date = new Date(dateStr)
		return date.toLocaleDateString('vi-VN', {
			year: 'numeric',
			month: '2-digit',
			day: '2-digit',
		})
	} catch (error) {
		return __('None')
	}
}

// Computed để lấy talent ID
const talentId = computed(() => props.talent?.name)

// Computed để format last interaction date
const lastInteractionDate = computed(() => {
	const lastDate = props.talent?.last_interaction_date
	if (!lastDate) return __('Not yet interacted')

	try {
		const date = new Date(lastDate)
		return date.toLocaleDateString('vi-VN', {
			year: 'numeric',
			month: '2-digit',
			day: '2-digit',
		})
	} catch (error) {
		return __('Not yet interacted')
	}
})

// Function để đếm interactions
const fetchInteractionCount = async () => {
	if (!talentId.value) return

	try {
		// Sử dụng frappe.client.get_list để query interactions
		const interactions = await call('frappe.client.get_list', {
			doctype: 'Mira Interaction',
			filters: {
				talent_id: talentId.value,
				interaction_type: ['in', ['EMAIL_OPENED', 'ON_LINK_CLICK', 'ZALO_CLICK']],
			},
			fields: ['name'],
			limit_page_length: 0, // Lấy tất cả records để đếm
		})

		totalInteractions.value = interactions ? interactions.length : 0
	} catch (error) {
		console.error('Error fetching interaction count:', error)
		totalInteractions.value = 0
	}
}

// Function để lấy engagement summary
const fetchEngagementSummary = async () => {
	if (!talentId.value) return

	try {
		// Lấy engagement summary cho talent
		const summaries = await call('frappe.client.get_list', {
			doctype: 'Mira Engagement Summary',
			filters: {
				talent_id: talentId.value,
			},
			fields: ['engagement_timeline', 'total_score'],
			limit_page_length: 1,
			order_by: 'creation desc', // Lấy record mới nhất
		})

		if (summaries && summaries.length > 0) {
			const summary = summaries[0]
			engagementTimeline.value = summary.engagement_timeline || 0
			engagementScore.value = summary.total_score || 0
		} else {
			engagementTimeline.value = 0
			engagementScore.value = 0
		}
	} catch (error) {
		console.error('Error fetching engagement summary:', error)
		engagementTimeline.value = 0
		engagementScore.value = 0
	}
}

// Add this to your methods or in the setup function
// Check if a string is valid JSON
const isValidJson = (str) => {
	try {
		JSON.parse(str);
		return true;
	} catch (e) {
		return false;
	}
}

// Format JSON string with indentation
const formatJson = (jsonString) => {
	try {
		const json = typeof jsonString === 'string' ? JSON.parse(jsonString) : jsonString;
		return JSON.stringify(json, null, 2);
	} catch (e) {
		return jsonString; // Return as is if not valid JSON
	}
}

// Format date range for display
const formatDateRange = (startDate, endDate) => {
	if (!startDate && !endDate) return 'Date not specified';
	
	const format = (dateStr) => {
		if (!dateStr) return 'Present';
		const date = new Date(dateStr);
		return isNaN(date) ? dateStr : date.toLocaleDateString('vi-VN', { month: 'short', year: 'numeric' });
	};
	
	return `${format(startDate)} - ${format(endDate)}`;
};

// Parse resume summary JSON
const parsedResumeSummary = computed(() => {
	try {
		const summary = props.talent?.resume_summary;
		if (!summary) return null;
		return typeof summary === 'string' ? JSON.parse(summary) : summary;
	} catch (e) {
		console.error('Error parsing resume summary:', e);
		return null;
	}
});

// Parse resume extract JSON
const parsedResumeExtract = computed(() => {
	try {
		const extract = props.talent?.resume_extract;
		if (!extract) return null;
		const data = typeof extract === 'string' ? JSON.parse(extract) : extract;
		// Handle nested data structure if present
		return data.data || data;
	} catch (e) {
		console.error('Error parsing resume extract:', e);
		return null;
	}
});

// Helpers to safely read skill data which may be a string or an object
const getSkillName = (skill) => {
	if (!skill) return '';
	return typeof skill === 'string' ? skill : skill.name || '';
};

const getSkillDetails = (skill) => {
	if (!skill || typeof skill === 'string') return '';
	return skill.details || '';
};

// Fetch data khi component mount
onMounted(() => {
	fetchInteractionCount()
	fetchEngagementSummary()
})

// Watch talent changes để update count
watch(
	talentId,
	(newTalentId) => {
		if (newTalentId) {
			fetchInteractionCount()
			fetchEngagementSummary()
		}
	},
	{ immediate: true },
)
</script>
