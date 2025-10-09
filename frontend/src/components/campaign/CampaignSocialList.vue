<template>
	<div class="bg-white rounded-lg shadow-sm border border-gray-200">
		<!-- Header -->
		<div class="px-6 py-4 border-b border-gray-200">
			<div class="flex items-center justify-between">
				<div class="flex items-center space-x-2">
					<FeatherIcon name="share-2" class="h-5 w-5 text-blue-600" />
					<h3 class="text-lg font-medium text-gray-900">
						{{ __('Social Media Posts') }}
					</h3>
				</div>
				<Button
					variant="solid"
					theme="gray"
					size="sm"
					@click="openCreateDialog"
					:disabled="loading"
				>
					<div class="flex items-center">
						<FeatherIcon name="plus" class="h-4 w-4 mr-1" />
						{{ __('Add Post') }}
					</div>
				</Button>
			</div>
		</div>

		<!-- Loading State -->
		<div v-if="loading" class="p-6">
			<div class="animate-pulse space-y-4">
				<div v-for="i in 3" :key="i" class="flex space-x-4">
					<div class="w-12 h-12 bg-gray-200 rounded-lg"></div>
					<div class="flex-1 space-y-2">
						<div class="h-4 bg-gray-200 rounded w-3/4"></div>
						<div class="h-3 bg-gray-200 rounded w-1/2"></div>
					</div>
				</div>
			</div>
		</div>

		<!-- Empty State -->
		<div v-else-if="!campaignSocials.length" class="p-6 text-center">
			<FeatherIcon name="share-2" class="h-12 w-12 text-gray-400 mx-auto mb-4" />
			<h3 class="text-sm font-medium text-gray-900 mb-2">
				{{ __('No social media posts') }}
			</h3>
			<p class="text-sm text-gray-500 mb-4">
				{{ __('Create your first social media post for this campaign.') }}
			</p>
			<Button variant="solid" theme="gray" size="sm" @click="openCreateDialog">
				<div class="flex items-center">
					<FeatherIcon name="plus" class="h-4 w-4 mr-1" />
					{{ __('Add Post') }}
				</div>
			</Button>
		</div>

		<!-- Social Posts List -->
		<div v-else class="divide-y divide-gray-200">
			<div
				v-for="social in campaignSocials"
				:key="social.name"
				class="p-6 hover:bg-gray-50 transition-colors"
			>
				<div class="flex items-start justify-between">
					<div class="flex-1">
						<!-- Page Info -->
						<div class="flex items-center space-x-2 mb-2">
							<FeatherIcon name="facebook" class="h-4 w-4 text-blue-600" />
							<span class="text-sm font-medium text-gray-900">
								{{ social.social_page_name || __('Unknown Page') }}
							</span>
							<span class="text-xs text-gray-500">
								{{ formatDate(social.post_schedule_time) }}
							</span>
						</div>

						<!-- Content Preview -->
						<div class="mb-3">
							<div
								class="text-sm text-gray-700 prose prose-sm max-w-none line-clamp-3"
								v-html="social.template_content || __('No content')"
							></div>
						</div>

						<!-- Image Preview -->
						<div v-if="social.social_media_images" class="mb-3">
							<img
								:src="social.social_media_images"
								:alt="__('Post image')"
								class="w-20 h-20 object-cover rounded-lg border border-gray-200"
							/>
						</div>

						<!-- Meta Info -->
						<div class="flex items-center space-x-4 text-xs text-gray-500">
							<span>{{ __('Created') }}: {{ formatDate(social.creation) }}</span>
							<span v-if="social.modified !== social.creation">
								{{ __('Modified') }}: {{ formatDate(social.modified) }}
							</span>
						</div>
					</div>

					<!-- Actions -->
					<div class="flex items-center space-x-2 ml-4">
						<Button
							variant="outline"
							theme="gray"
							size="sm"
							@click="editSocial(social)"
						>
							<FeatherIcon name="edit-2" class="h-3 w-3" />
						</Button>
						<Button
							variant="outline"
							theme="red"
							size="sm"
							@click="deleteSocial(social)"
							:loading="deleting === social.name"
						>
							<FeatherIcon name="trash-2" class="h-3 w-3" />
						</Button>
					</div>
				</div>
			</div>
		</div>

		<!-- Social Network Config Dialog -->
		<SocialNetworkConfigDialog
			v-model="showSocialDialog"
			:social-config="currentSocialConfig"
			:social-pages="socialPages"
			:jobOpeningsList="props.jobOpenings"
			:loading-pages="loadingPages"
			:loading-job-openings="loadingJobOpenings"
			:campaign-id="campaignId"
			:campaign-social-id="editingSocialId"
			:mode="'detail'"
			@confirm="handleSocialConfirm"
			@cancel="handleSocialCancel"
		/>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { Button, FeatherIcon } from 'frappe-ui'
import { useCampaignSocialStore } from '@/stores/campaignSocial'
import SocialNetworkConfigDialog from './SocialNetworkConfigDialog.vue'

// Props
const props = defineProps({
	campaignId: {
		type: String,
		required: true,
	},
	socialPages: {
		type: Array,
		default: () => [],
	},
	jobOpenings: {
		type: Array,
		default: () => [],
	},
	loadingPages: {
		type: Boolean,
		default: false,
	},
	loadingJobOpenings: {
		type: Boolean,
		default: false,
	},
})

console.log(props.jobOpenings)

// Emits
const emit = defineEmits(['refresh'])

// Translation helper
const __ = (text) => text

// Store
const campaignSocialStore = useCampaignSocialStore()

// Reactive state
const loading = ref(false)
const deleting = ref(null)
const showSocialDialog = ref(false)
const editingSocialId = ref(null)
const currentSocialConfig = ref({
	page_id: '',
	scheduled_at: '',
	job_opening: '',
	image: '',
	template_content: '',
})

// Computed
const campaignSocials = computed(() =>
	campaignSocialStore.getCampaignSocialsByCampaign(props.campaignId),
)

// Methods
const loadCampaignSocials = async () => {
	if (!props.campaignId) return

	loading.value = true
	try {
		await campaignSocialStore.fetchCampaignSocials({
			campaign_id: props.campaignId,
		})
	} catch (error) {
		console.error('Error loading campaign socials:', error)
	} finally {
		loading.value = false
	}
}

const openCreateDialog = () => {
	editingSocialId.value = null
	currentSocialConfig.value = {
		page_id: '',
		scheduled_at: '',
		job_opening: '',
		image: '',
		template_content: '',
	}
	showSocialDialog.value = true
}

const editSocial = async (social) => {
	try {
		// Load full social data
		const fullSocial = await campaignSocialStore.getCampaignSocial(social.name)

		editingSocialId.value = social.name
		currentSocialConfig.value = {
			page_id: fullSocial.social_page_id || '',
			scheduled_at: fullSocial.post_schedule_time || '',
			job_opening: '', // This might need to be loaded from campaign
			image: fullSocial.social_media_images || '',
			template_content: fullSocial.template_content || '',
		}
		showSocialDialog.value = true
	} catch (error) {
		console.error('Error loading social for edit:', error)
		alert(__('Failed to load social post data'))
	}
}

const deleteSocial = async (social) => {
	if (!confirm(__('Are you sure you want to delete this social media post?'))) {
		return
	}

	deleting.value = social.name
	try {
		await campaignSocialStore.deleteCampaignSocial(social.name)
		emit('refresh')
	} catch (error) {
		console.error('Error deleting social:', error)
		alert(__('Failed to delete social media post'))
	} finally {
		deleting.value = null
	}
}

const handleSocialConfirm = (config) => {
	showSocialDialog.value = false
	loadCampaignSocials() // Refresh the list
	emit('refresh')
}

const handleSocialCancel = () => {
	showSocialDialog.value = false
	editingSocialId.value = null
}

const formatDate = (dateString) => {
	if (!dateString) return __('Not set')

	try {
		const date = new Date(dateString)
		return date.toLocaleString()
	} catch (error) {
		return __('Invalid date')
	}
}

// Lifecycle
onMounted(() => {
	loadCampaignSocials()
})

// Watch for campaign ID changes
watch(
	() => props.campaignId,
	() => {
		if (props.campaignId) {
			loadCampaignSocials()
		}
	},
	{ immediate: true },
)
</script>

<style scoped>
.line-clamp-3 {
	display: -webkit-box;
	-webkit-line-clamp: 3;
	line-clamp: 3;
	-webkit-box-orient: vertical;
	overflow: hidden;
}
</style>
