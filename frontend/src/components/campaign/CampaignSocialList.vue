<template>
  <div class="bg-white">
    <!-- Header -->
    <div class="pb-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <h3 class="text-lg font-medium text-gray-900">
            {{ __('Media Posts') }}
          </h3>
        </div>
        <Dropdown :options="dropdownActions" @click.stop>
          <template v-slot="{ open }">
            <Button variant="solid" theme="gray" size="sm" :disabled="loading">
              <template #prefix>
                <FeatherIcon name="plus" class="h-4 w-4" />
              </template>
              <span>{{ __("New") }}</span>
              <template #suffix>
                <FeatherIcon
                  :name="open ? 'chevron-up' : 'chevron-down'"
                  class="h-4 w-4"
                />
              </template>
            </Button>
          </template>
        </Dropdown>
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
							<FeatherIcon 
								:name="getPlatformIcon(social.platform)" 
								class="h-4 w-4 text-blue-600" 
							/>
							<span class="text-sm font-medium text-gray-900">
								{{ social.social_page_name || __('Unknown Page') }}
							</span>
							<span 
								class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
								:class="getStatusClass(social.status)"
							>
								{{ social.status || 'Pending' }}
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

		<!-- Social Network Config Dialog -->
		<SocialNetworkConfigDialog
			v-model="showCreateDialog"
			:social-config="currentSocialConfig"
			:social-pages="socialPages"
			:external-connections="externalConnections"
			:loading-connections="loadingConnections"
			:job-openings-list="jobOpeningsList"
			:loading-pages="loadingPages"
			:loading-job-openings="loadingJobOpenings"
			:min-scheduled-at="minScheduledAt"
			:local-tz-label="localTzLabel"
			:campaign-social-id="editingSocialId"
			:mode="'detail'"
			@confirm="handleSocialConfirm"
			@cancel="handleSocialCancel"
		/>

		<!-- QR Code Dialog -->
		<Dialog v-model="showQrDialog" :options="{ title: __('Campaign QR Code'), size: 'md' }">
			<template #body-content>
				<div class="p-6 text-center">
					<div v-if="qrData.image" class="mb-4">
						<img :src="qrData.image" alt="QR Code" class="mx-auto max-w-xs" />
					</div>
					<div v-else class="mb-4">
						<div class="w-48 h-48 bg-gray-200 rounded-lg mx-auto flex items-center justify-center">
							<FeatherIcon name="qr-code" class="h-12 w-12 text-gray-400" />
						</div>
					</div>
					
					<div class="space-y-2">
						<p class="text-sm font-medium text-gray-900">{{ __('Scan to view job opening') }}</p>
						<p class="text-xs text-gray-500 break-all">{{ qrData.url }}</p>
					</div>
					
					<div class="mt-6 flex justify-end space-x-3">
						<Button variant="ghost" @click="showQrDialog = false">
							{{ __('Close') }}
						</Button>
					</div>
				</div>
			</template>
		</Dialog>
	</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { Button, FeatherIcon, Dropdown, Dialog, call } from 'frappe-ui'
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
	externalConnections: {
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
	loadingConnections: {
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
const showCreateDialog = ref(false)
const editingSocialId = ref(null)
const showQrDialog = ref(false)
const qrData = ref({ url: '', image: '' })

const currentSocialConfig = ref({
	page_id: '',
	scheduled_at: '',
	job_opening: '',
	image: '',
})

// Dropdown actions
const dropdownActions = computed(() => [
	{
		label: __('Add Post'),
		icon: 'plus',
		onClick: openCreateDialog
	},
	{
		label: __('Generate QR Code'),
		icon: 'qr-code',
		onClick: handleShowQr
	}
])

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
	showCreateDialog.value = true
}

// QR Code functions
const handleShowQr = async () => {
	try {
		// Get current router base URL
		const baseUrl = window.location.origin
		
		// Build job URL using current router base
		const jobUrl = `${baseUrl}/mbw_mira/jobs/tuyen-lap-trinh-vien-python`
		
		const res = await call('mbw_mira.api.campaign.get_job_qrcode', {
			campaign_id: props.campaignId,
			target_url: jobUrl
		})
		
		qrData.value = res || { url: jobUrl, image: '' }
		showQrDialog.value = true
	} catch (e) {
		console.error('Error generating QR code:', e)
		// Fallback with current router base URL
		const baseUrl = window.location.origin
		const fallbackUrl = `${baseUrl}/mbw_mira/jobs/tuyen-lap-trinh-vien-python`
		qrData.value = { 
			url: fallbackUrl, 
			image: '' 
		}
		showQrDialog.value = true
	}
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
	showCreateDialog.value = false
	loadCampaignSocials() // Refresh the list
	emit('refresh')
}

const handleSocialCancel = () => {
	showCreateDialog.value = false
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

const getPlatformIcon = (platform) => {
	switch (platform?.toLowerCase()) {
		case 'facebook':
			return 'facebook'
		case 'linkedin':
			return 'linkedin'
		case 'twitter':
			return 'twitter'
		case 'instagram':
			return 'instagram'
		default:
			return 'share-2'
	}
}

const getStatusClass = (status) => {
	switch (status?.toLowerCase()) {
		case 'success':
			return 'bg-green-100 text-green-800'
		case 'failed':
			return 'bg-red-100 text-red-800'
		case 'processing':
			return 'bg-yellow-100 text-yellow-800'
		case 'cancelled':
			return 'bg-gray-100 text-gray-800'
		case 'pending':
		default:
			return 'bg-blue-100 text-blue-800'
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
