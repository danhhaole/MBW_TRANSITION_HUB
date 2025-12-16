<template>
	<Dialog
		v-model="isOpen"
		:options="{
			size: '4xl',
		}"
	>
		<template #body-title>
			<div class="mb-6">
				<div class="flex items-start justify-between mb-4">
					<div>
						<h3 class="text-lg font-semibold text-gray-900">
							{{ __('Sync Candidates from ATS') }}
						</h3>
						<p class="text-sm text-gray-500 mt-1">
							{{
								__(
									'Import candidate data from your ATS system to create talent profiles.',
								)
							}}
						</p>
					</div>
				</div>
			</div>
		</template>

		<template #body-content>
			<!-- Step Indicator -->
			<div class="mb-8 px-12">
				<div class="flex items-start justify-between w-full">
					<!-- Step 1 -->
					<div class="flex flex-col items-center" style="min-width: 140px">
						<div
							:class="[
								'flex items-center justify-center w-12 h-12 rounded-full border-2 transition-all duration-200',
								currentStep >= 1
									? 'bg-blue-600 border-blue-600 text-white shadow-md'
									: 'border-gray-300 text-gray-400 bg-white',
							]"
						>
							<span v-if="currentStep > 1" class="text-lg">✓</span>
							<span v-else class="text-sm font-semibold">1</span>
						</div>
						<span
							:class="[
								'mt-2 text-sm font-medium text-center',
								currentStep >= 1 ? 'text-gray-900' : 'text-gray-400',
							]"
						>
							{{ __('Select Connection') }}
						</span>
					</div>

					<!-- Connector 1 -->
					<div class="flex-1 pt-6 px-4">
						<div
							:class="[
								'h-0.5 w-full transition-all duration-300',
								currentStep >= 2 ? 'bg-blue-600' : 'bg-gray-300',
							]"
						></div>
					</div>

					<!-- Step 2 -->
					<div class="flex flex-col items-center" style="min-width: 140px">
						<div
							:class="[
								'flex items-center justify-center w-12 h-12 rounded-full border-2 transition-all duration-200',
								currentStep >= 2
									? 'bg-blue-600 border-blue-600 text-white shadow-md'
									: 'border-gray-300 text-gray-400 bg-white',
							]"
						>
							<span v-if="currentStep > 2" class="text-lg">✓</span>
							<span v-else class="text-sm font-semibold">2</span>
						</div>
						<span
							:class="[
								'mt-2 text-sm font-medium text-center',
								currentStep >= 2 ? 'text-gray-900' : 'text-gray-400',
							]"
						>
							{{ __('Filter & Sync') }}
						</span>
					</div>
				</div>
			</div>
			<div class="h-auto">
				<!-- Step 1: Select ATS Connection -->
				<div v-if="currentStep === 1 && !showConnectionForm" class="space-y-4">
					<div class="flex items-center justify-between mb-4">
						<div class="text-sm text-gray-600">
							{{ __('Select an active ATS connection to sync candidates from:') }}
						</div>
						<!-- <Button
              variant="solid"
              theme="gray"
              size="sm"
              @click="showConnectionForm = true"
            >
              <template #prefix>
                <FeatherIcon name="plus" class="h-4 w-4" />
              </template>
              {{ __('Create Connection') }}
            </Button> -->
					</div>

					<!-- Loading State -->
					<div v-if="loadingConnections" class="flex items-center justify-center py-12">
						<LoadingIndicator class="w-8 h-8" />
						<span class="ml-3 text-gray-600">{{ __('Loading connections...') }}</span>
					</div>

					<!-- Connections List -->
					<div
						v-else-if="atsConnections.length > 0"
						class="grid grid-cols-1 md:grid-cols-2 gap-4"
					>
						<div
							v-for="connection in atsConnections"
							:key="connection.name"
							@click="selectConnection(connection)"
							:class="[
								'border rounded-lg p-4 cursor-pointer transition-all',
								selectedConnection?.name === connection.name
									? 'border-blue-500 bg-blue-50 shadow-sm'
									: 'border-gray-200 hover:border-blue-300 hover:shadow-sm',
							]"
						>
							<div class="flex items-start justify-between">
								<div class="flex-1">
									<h4 class="font-medium text-gray-900">
										{{ connection.source_title }}
									</h4>
									<p class="text-sm text-gray-500 mt-1">
										{{ connection.source_name }}
									</p>
									<div class="flex items-center gap-2 mt-2">
										<span
											class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800"
										>
											{{ connection.status }}
										</span>
										<span class="text-xs text-gray-500">{{
											connection.source_type
										}}</span>
									</div>
								</div>
								<div
									v-if="selectedConnection?.name === connection.name"
									class="flex-shrink-0 w-5 h-5 rounded-full bg-blue-600 flex items-center justify-center"
								>
									<svg
										class="w-3 h-3 text-white"
										fill="currentColor"
										viewBox="0 0 20 20"
									>
										<path
											fill-rule="evenodd"
											d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
											clip-rule="evenodd"
										/>
									</svg>
								</div>
							</div>
						</div>
					</div>

					<!-- Empty State -->
					<div v-else class="text-center py-12 border rounded-lg bg-gray-50">
						<FeatherIcon
							name="database"
							class="w-12 h-12 mx-auto mb-4 text-gray-300"
						/>
						<p class="text-gray-500 mb-2">
							{{ __('No active ATS connections found') }}
						</p>
						<p class="text-sm text-gray-400 mb-4">
							{{ __('Please configure an ATS data source first.') }}
						</p>
						<Button variant="solid" theme="gray" @click="showConnectionForm = true">
							<template #prefix>
								<FeatherIcon name="plus" class="h-4 w-4" />
							</template>
							{{ __('Create New Connection') }}
						</Button>
					</div>
				</div>

				<!-- Create Connection Form -->
				<div v-if="currentStep === 1 && showConnectionForm" class="space-y-6">
					<!-- Back Button -->
					<div class="flex items-center gap-2 mb-4">
						<button
							@click="showConnectionForm = false"
							class="flex items-center gap-1 text-sm text-gray-600 hover:text-gray-900"
						>
							<FeatherIcon name="arrow-left" class="h-4 w-4" />
							{{ __('Back to Connections') }}
						</button>
					</div>

					<!-- ATS Info Header -->
					<div class="bg-gray-50 rounded-lg p-4 flex items-start gap-3">
						<div
							class="flex-shrink-0 w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center"
						>
							<FeatherIcon name="briefcase" class="w-6 h-6 text-red-600" />
						</div>
						<div>
							<h4 class="font-medium text-gray-900">MobiWork ATS</h4>
							<p class="text-sm text-gray-500 mt-1">
								{{ __('Connect MobiWork Applicant Tracking System') }}
							</p>
						</div>
					</div>

					<!-- Basic Information Section -->
					<div>
						<h4 class="text-sm font-semibold text-gray-900 mb-4">
							{{ __('Basic Information') }}
						</h4>

						<div class="space-y-4">
							<!-- Connection Title -->
							<div>
								<label class="block text-sm font-medium text-gray-700 mb-1">
									{{ __('Connection Title') }}
									<span class="text-red-500">*</span>
								</label>
								<input
									v-model="formData.source_title"
									type="text"
									class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
									:placeholder="__('Enter connection title')"
								/>
								<p v-if="errors.source_title" class="text-sm text-red-600 mt-1">
									{{ errors.source_title }}
								</p>
							</div>

							<!-- Same Site Checkbox -->
							<div class="flex items-start gap-2">
								<input
									v-model="formData.same_site"
									type="checkbox"
									id="same_site"
									class="mt-1 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
								/>
								<label for="same_site" class="text-sm text-gray-700">
									<span class="font-medium">{{ __('Same Site') }}</span>
									<p class="text-gray-500 mt-0.5">
										{{
											__(
												'Check if this ATS runs on the same site (no need to enter API Base URL)',
											)
										}}
									</p>
								</label>
							</div>
						</div>
					</div>

					<!-- API Configuration Section -->
					<div>
						<div class="flex items-center justify-between mb-4">
							<h4 class="text-sm font-semibold text-gray-900">
								{{ __('API Configuration') }}
							</h4>
						</div>

						<div class="space-y-4">
							<!-- API Base URL (conditional) -->
							<div v-if="!formData.same_site">
								<label class="block text-sm font-medium text-gray-700 mb-1">
									{{ __('API Base URL') }} <span class="text-red-500">*</span>
								</label>
								<input
									v-model="formData.api_base_url"
									type="text"
									class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
									:placeholder="__('https://your-ats-domain.com')"
								/>
								<p v-if="errors.api_base_url" class="text-sm text-red-600 mt-1">
									{{ errors.api_base_url }}
								</p>
							</div>

							<!-- API Key -->
							<div>
								<label class="block text-sm font-medium text-gray-700 mb-1">
									{{ __('API Key') }} <span class="text-red-500">*</span>
								</label>
								<input
									v-model="formData.api_key"
									type="text"
									class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
									:placeholder="__('Enter your API key')"
								/>
								<p v-if="errors.api_key" class="text-sm text-red-600 mt-1">
									{{ errors.api_key }}
								</p>
							</div>

							<!-- API Secret -->
							<div>
								<label class="block text-sm font-medium text-gray-700 mb-1">
									{{ __('API Secret') }} <span class="text-red-500">*</span>
								</label>
								<input
									v-model="formData.api_secret"
									type="password"
									class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
									:placeholder="__('Enter your API secret')"
								/>
								<p v-if="errors.api_secret" class="text-sm text-red-600 mt-1">
									{{ errors.api_secret }}
								</p>
							</div>
						</div>
					</div>

					<!-- Info Box -->
					<div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
						<div class="flex items-start gap-2">
							<FeatherIcon
								name="shield"
								class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0"
							/>
							<div class="text-sm">
								<p class="font-medium text-blue-900">
									{{ __('Secure API Connection') }}
								</p>
								<p class="text-blue-700 mt-1">
									{{
										__(
											'This connection uses API Key authentication for secure data exchange. Your credentials are encrypted and never shared.',
										)
									}}
								</p>
							</div>
						</div>
					</div>
				</div>

				<!-- Step 2: Filter Conditions & Sync -->
				<div v-if="currentStep === 2" class="space-y-4">
					<div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
						<div class="flex items-start">
							<FeatherIcon name="info" class="h-5 w-5 text-blue-600 mt-0.5 mr-2" />
							<div>
								<h4 class="text-sm font-medium text-blue-900">
									{{ __('Selected Connection') }}
								</h4>
								<p class="text-sm text-blue-700 mt-1">
									{{ selectedConnection?.source_title }} ({{
										selectedConnection?.source_name
									}})
								</p>
							</div>
						</div>
					</div>

					<!-- Existing Sync Log Warning -->
					<div
						v-if="existingSyncStatus?.has_sync_log && !syncProgress.isActive"
						class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4"
					>
						<div class="flex items-start">
							<FeatherIcon
								name="alert-circle"
								class="h-5 w-5 text-yellow-600 mt-0.5 mr-2"
							/>
							<div class="flex-1">
								<h4 class="text-sm font-medium text-yellow-900">
									{{ __('Sync Log Already Exists') }}
								</h4>
								<p class="text-sm text-yellow-700 mt-1">
									{{
										__(
											'This connection already has a sync log with status: {0}',
											[existingSyncStatus.status],
										)
									}}
								</p>
								<p class="text-sm text-yellow-700 mt-1">
									{{
										__(
											'Please go to Sync History to Retry or Cancel the existing sync log.',
										)
									}}
								</p>
							</div>
						</div>
					</div>

					<!-- Sync Progress Display -->
					<div
						v-if="syncProgress.isActive"
						class="bg-white border border-gray-200 rounded-lg p-6 space-y-4"
					>
						<div class="flex items-center justify-between">
							<h4 class="text-sm font-semibold text-gray-900">
								{{ __('Sync Progress') }}
							</h4>
							<span
								class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
							>
								{{ __('In Progress') }}
							</span>
						</div>

						<!-- Progress Bar -->
						<div class="space-y-2">
							<div class="flex items-center justify-between text-sm">
								<span class="text-gray-600">
									{{
										__('Processing: {0} / {1}', [
											syncProgress.currentRecord,
											syncProgress.totalRecords,
										])
									}}
								</span>
								<span class="font-medium text-gray-900">
									{{
										syncProgress.totalRecords > 0
											? Math.round(
													(syncProgress.currentRecord /
														syncProgress.totalRecords) *
														100,
												)
											: 0
									}}%
								</span>
							</div>
							<div class="w-full bg-gray-200 rounded-full h-2.5">
								<div
									class="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
									:style="{
										width:
											syncProgress.totalRecords > 0
												? `${(syncProgress.currentRecord / syncProgress.totalRecords) * 100}%`
												: '0%',
									}"
								></div>
							</div>
						</div>

						<!-- Stats -->
						<div class="grid grid-cols-4 gap-3">
							<div class="text-center p-3 bg-green-50 rounded-lg">
								<div class="text-2xl font-bold text-green-600">
									{{ syncProgress.successCount }}
								</div>
								<div class="text-xs text-green-700 mt-1">{{ __('Success') }}</div>
							</div>
							<div class="text-center p-3 bg-red-50 rounded-lg">
								<div class="text-2xl font-bold text-red-600">
									{{ syncProgress.failedCount }}
								</div>
								<div class="text-xs text-red-700 mt-1">{{ __('Failed') }}</div>
							</div>
							<div class="text-center p-3 bg-yellow-50 rounded-lg">
								<div class="text-2xl font-bold text-yellow-600">
									{{ syncProgress.skippedCount || 0 }}
								</div>
								<div class="text-xs text-yellow-700 mt-1">{{ __('Skipped') }}</div>
							</div>
							<div class="text-center p-3 bg-gray-50 rounded-lg">
								<div class="text-2xl font-bold text-gray-600">
									{{ syncProgress.totalRecords }}
								</div>
								<div class="text-xs text-gray-700 mt-1">{{ __('Total') }}</div>
							</div>
						</div>

						<!-- Latest Talent -->
						<div v-if="syncProgress.latestTalent" class="bg-gray-50 rounded-lg p-3">
							<div class="flex items-center gap-2 text-sm">
								<FeatherIcon
									:name="
										syncProgress.latestTalent.action === 'created'
											? 'plus-circle'
											: 'refresh-cw'
									"
									class="h-4 w-4 text-blue-600"
								/>
								<span class="text-gray-600">{{ __('Latest:') }}</span>
								<span class="font-medium text-gray-900">{{
									syncProgress.latestTalent.fullName
								}}</span>
								<span class="text-xs text-gray-500"
									>({{ syncProgress.latestTalent.action }})</span
								>
							</div>
						</div>
					</div>

					<!-- Filter Conditions (hidden during sync) -->
					<div v-if="!syncProgress.isActive">
						<ConditionsBuilder
							ref="conditionsBuilderRef"
							v-model="filterConditions"
							doctype="Mira Talent"
							:custom-fields="talentPoolFields"
							:title="__('Filter Conditions')"
							:description="
								__(
									'Add conditions to filter which candidates to sync. Leave empty to sync all active candidates.',
								)
							"
							:show-preview="false"
							:validate-on-change="true"
							@validate="handleConditionsValidate"
						/>
					</div>
				</div>
			</div>
		</template>

		<template #actions>
			<div class="flex justify-between items-center pt-4 border-t border-gray-200">
				<Button
					v-if="currentStep > 1 && !showConnectionForm"
					variant="outline"
					theme="gray"
					@click="previousStep"
				>
					<template #prefix>
						<FeatherIcon name="chevron-left" class="h-4 w-4" />
					</template>
					{{ __('Back') }}
				</Button>
				<div v-else></div>

				<div class="flex gap-2">
					<Button variant="outline" theme="gray" @click="closeDialog">
						{{ __('Cancel') }}
					</Button>

					<!-- Show Create Connection button when in form view -->
					<Button
						v-if="showConnectionForm"
						variant="solid"
						theme="gray"
						@click="handleCreateConnection"
						:loading="creating"
					>
						{{ __('Connect ATS') }}
					</Button>

					<!-- Show Next button for Step 1 (not in form) -->
					<Button
						v-else-if="currentStep === 1"
						variant="solid"
						theme="gray"
						@click="nextStep"
						:disabled="!canProceed"
					>
						{{ __('Next') }}
						<template #suffix>
							<FeatherIcon name="chevron-right" class="h-4 w-4" />
						</template>
					</Button>

					<!-- Show Sync button for Step 2 -->
					<Button
						v-else-if="currentStep === 2"
						variant="solid"
						theme="gray"
						@click="startSync"
						:loading="syncing"
						:disabled="existingSyncStatus?.has_sync_log || syncProgress.isActive"
					>
						<template #prefix v-if="!syncing">
							<FeatherIcon name="play" class="h-4 w-4" />
						</template>
						{{ syncing ? __('Syncing...') : __('Start Sync') }}
					</Button>
				</div>
			</div>
		</template>
	</Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Dialog, Button, FeatherIcon, LoadingIndicator } from 'frappe-ui'
import ConditionsBuilder from '@/components/ConditionsFilter/ConditionsBuilder.vue'
import { useToast } from '@/composables/useToast'
import { call } from 'frappe-ui'

const props = defineProps({
	modelValue: {
		type: Boolean,
		default: false,
	},
})

const emit = defineEmits(['update:modelValue', 'success'])

const { showSuccess, showError } = useToast()

// State
const currentStep = ref(1)
const isOpen = ref(props.modelValue)
const loadingConnections = ref(false)
const loadingSyncLogs = ref(false)
const syncing = ref(false)
const atsConnections = ref([])
const selectedConnection = ref(null)
const filterConditions = ref([])
const syncLogs = ref([])
const conditionsBuilderRef = ref(null)
const showConnectionForm = ref(false)
const creating = ref(false)
const currentPage = ref(1)
const pageSize = ref(5)
const totalRecords = ref(0)
const conditionsValid = ref(true)
const formData = ref({
	source_title: '',
	source_type: 'ATS',
	source_name: 'MBW ATS',
	same_site: false,
	api_base_url: '',
	auth_method: 'API Key',
	api_key: '',
	api_secret: '',
	sync_direction: 'Both',
	status: 'Active',
	is_active: 1,
	conditions: [],
})
const errors = ref({})
const syncProgress = ref({
	isActive: false,
	syncLogName: null,
	successCount: 0,
	failedCount: 0,
	skippedCount: 0,
	totalRecords: 0,
	currentRecord: 0,
	latestTalent: null,
})
const existingSyncStatus = ref(null)
const checkingSyncStatus = ref(false)

// Computed
const canProceed = computed(() => {
	if (currentStep.value === 1) {
		return selectedConnection.value !== null
	}
	return true
})

// Watch dialog state
watch(
	() => props.modelValue,
	(newValue) => {
		isOpen.value = newValue
		if (newValue) {
			fetchATSConnections()
		}
	},
)

watch(isOpen, (newValue) => {
	emit('update:modelValue', newValue)
	if (!newValue) {
		// Reset dialog when it's closed
		resetDialog()
	}
})

// Watch selected connection to check sync status
watch(selectedConnection, async (newVal) => {
	if (newVal) {
		await checkExistingSyncStatus()
	} else {
		existingSyncStatus.value = null
	}
})

// Methods
const resetDialog = () => {
	currentStep.value = 1
	selectedConnection.value = null
	filterConditions.value = []
	syncLogs.value = []
	syncing.value = false
	showConnectionForm.value = false
	currentPage.value = 1
	totalRecords.value = 0
	resetFormData()
	resetSyncProgress()
}

const resetSyncProgress = () => {
	syncProgress.value = {
		isActive: false,
		syncLogName: null,
		successCount: 0,
		failedCount: 0,
		skippedCount: 0,
		totalRecords: 0,
		currentRecord: 0,
		latestTalent: null,
	}
}

// Custom fields for Talent Pool filtering - Advanced Conditions
const talentPoolFields = [
	{
		label: __('Status'),
		fieldname: 'status',
		fieldtype: 'Select',
		options:
			'Hired\nOffer Sent\nOffer Accepted\nFinal Interview Passed\nScreening Passed\nQualified\nTalent Pool',
		value: 'status',
	},
  {
		label: __('Minimum Required Fields'),
		fieldname: 'minimum_required_fields',
		fieldtype: 'Select',
		options:
			'Full Name\nEmail\nPhone\nSource',
		value: 'minimum_required_fields',
	},
	{ label: __('Skills'), fieldname: 'skills', fieldtype: 'Small Text', value: 'skills' },
  { label: __('Tags'), fieldname: 'tags', fieldtype: 'Small Text', value: 'tags' },
  { label: __('Experience Level'), fieldname: 'experience_level', fieldtype: 'Int', value: 'experience_level' },
  { label: __('Score'), fieldname: 'score', fieldtype: 'Int', value: 'score' },
	// { label: __('Created On'), fieldname: 'creation', fieldtype: 'Datetime', value: 'creation' },
	// { label: __('Modified On'), fieldname: 'modified', fieldtype: 'Datetime', value: 'modified' },
]

const checkExistingSyncStatus = async () => {
	if (!selectedConnection.value) return

	checkingSyncStatus.value = true
	try {
		const response = await call('mbw_mira.api.sync_segment.check_sync_status', {
			data_source_name: selectedConnection.value.name,
			sync_type: 'Candidate to Talent',
		})

		existingSyncStatus.value = response
	} catch (error) {
		console.error('Error checking sync status:', error)
		existingSyncStatus.value = null
	} finally {
		checkingSyncStatus.value = false
	}
}

const resetFormData = () => {
	formData.value = {
		source_title: '',
		source_type: 'ATS',
		source_name: 'MBW ATS',
		same_site: false,
		api_base_url: '',
		auth_method: 'API Key',
		api_key: '',
		api_secret: '',
		sync_direction: 'Both',
		status: 'Active',
		is_active: 1,
	}
	errors.value = {}
}

const validateForm = () => {
	errors.value = {}

	if (!formData.value.source_title) {
		errors.value.source_title = __('Connection title is required')
	}

	if (!formData.value.same_site && !formData.value.api_base_url) {
		errors.value.api_base_url = __('API Base URL is required when not using same site')
	}

	if (!formData.value.api_key) {
		errors.value.api_key = __('API Key is required')
	}

	if (!formData.value.api_secret) {
		errors.value.api_secret = __('API Secret is required')
	}

	return Object.keys(errors.value).length === 0
}

const handleCreateConnection = async () => {
	if (!validateForm()) {
		showError(__('Please fill in all required fields'))
		return
	}

	creating.value = true
	try {
		const response = await call('frappe.client.insert', {
			doc: {
				doctype: 'Mira Data Source',
				...formData.value,
			},
		})

		if (response) {
			showSuccess(__('ATS connection created successfully'))
			// Hide form and reload connections
			showConnectionForm.value = false
			await fetchATSConnections()
			// Auto-select the newly created connection
			selectedConnection.value = response
			resetFormData()
		}
	} catch (error) {
		console.error('Error creating ATS connection:', error)
		showError(error.message || __('Failed to create ATS connection'))
	} finally {
		creating.value = false
	}
}

const closeDialog = () => {
	isOpen.value = false
	emit('update:modelValue', false)
}

const selectConnection = (connection) => {
	selectedConnection.value = connection
}

const previousStep = () => {
	if (currentStep.value > 1) {
		currentStep.value--
	}
}

const nextStep = async () => {
	if (currentStep.value === 1) {
		// Move to filter conditions & sync
		currentStep.value = 2
	}
}

const fetchATSConnections = async () => {
	loadingConnections.value = true
	try {
		const response = await call('frappe.client.get_list', {
			doctype: 'Mira Data Source',
			filters: {
				source_type: 'ATS',
				is_active: 1,
				status: 'Active',
			},
			fields: ['name', 'source_title', 'source_name', 'source_type', 'status'],
			limit_page_length: 50,
		})

		atsConnections.value = response || []
	} catch (error) {
		console.error('Error fetching ATS connections:', error)
		showError(__('Failed to load ATS connections'))
	} finally {
		loadingConnections.value = false
	}
}

// Clean filter conditions - remove empty/incomplete conditions
const cleanFilterConditions = (conditions) => {
	if (!conditions || conditions.length === 0) return []

	const cleaned = []
	
	for (let i = 0; i < conditions.length; i++) {
		const item = conditions[i]
		
		// If it's a conjunction (string), add it
		if (typeof item === 'string' && (item === 'and' || item === 'or')) {
			cleaned.push(item)
			continue
		}
		
		// If it's an array (condition or group)
		if (Array.isArray(item)) {
			// Check if it's a nested group
			if (item.length > 0 && Array.isArray(item[0])) {
				// Recursively clean nested group
				const cleanedGroup = cleanFilterConditions(item)
				if (cleanedGroup.length > 0) {
					cleaned.push(cleanedGroup)
				}
			} else {
				// It's a simple condition [field, operator, value]
				const [field, operator, value] = item
				
				// Only include if field and value are present
				if (field && value) {
					cleaned.push(item)
				}
			}
		}
	}
	
	// Remove trailing conjunctions
	while (cleaned.length > 0 && typeof cleaned[cleaned.length - 1] === 'string') {
		cleaned.pop()
	}
	
	// Remove leading conjunctions
	while (cleaned.length > 0 && typeof cleaned[0] === 'string') {
		cleaned.shift()
	}
	
	return cleaned
}

// Convert frontend filter format to backend-friendly format
const convertFiltersForBackend = (conditions) => {
	if (!conditions || conditions.length === 0) return null
	
	const result = {
		conditions: [],
		logic: 'AND' // Default logic
	}
	
	const processConditions = (items, parentLogic = 'AND') => {
		const processed = []
		let currentLogic = parentLogic
		
		for (let i = 0; i < items.length; i++) {
			const item = items[i]
			
			// If it's a conjunction
			if (typeof item === 'string' && (item === 'and' || item === 'or')) {
				currentLogic = item.toUpperCase()
				continue
			}
			
			// If it's an array
			if (Array.isArray(item)) {
				// Check if it's a nested group
				if (item.length > 0 && Array.isArray(item[0])) {
					// Process nested group
					const nestedResult = processConditions(item, currentLogic)
					if (nestedResult.length > 0) {
						processed.push({
							type: 'group',
							logic: currentLogic,
							conditions: nestedResult
						})
					}
				} else {
					// Simple condition [field, operator, value]
					const [field, operator, value] = item
					
					if (field && value) {
						// Parse comma-separated values for IN operator
						let parsedValue = value
						if (operator === 'in' || operator === 'not in') {
							parsedValue = value.split(',').map(v => v.trim()).filter(v => v)
						}
						
						processed.push({
							type: 'condition',
							field: field,
							operator: operator,
							value: parsedValue,
							logic: currentLogic
						})
					}
				}
			}
		}
		
		return processed
	}
	
	result.conditions = processConditions(conditions)
	
	return result.conditions.length > 0 ? result : null
}

const startSync = async () => {
	if (!selectedConnection.value) {
		showError(__('Please select a connection'))
		return
	}

	syncing.value = true
	try {
		// Clean and convert filter conditions before sending
		const cleanedFilters = cleanFilterConditions(filterConditions.value)
		const backendFilters = convertFiltersForBackend(cleanedFilters)
		
		console.log('=== FILTER PROCESSING ===')
		console.log('Original:', JSON.stringify(filterConditions.value, null, 2))
		console.log('Cleaned:', JSON.stringify(cleanedFilters, null, 2))
		console.log('Backend format:', JSON.stringify(backendFilters, null, 2))
		console.log('========================')
		
		const response = await call('mbw_mira.api.sync_segment.sync_candidates', {
			data_source_name: selectedConnection.value.name,
			filters: backendFilters
		})

		if (response.status === 'success') {
			showSuccess(
				response.message ||
					__('Sync started successfully. The process is running in the background.'),
			)

			// Initialize sync progress tracking
			syncProgress.value.isActive = true
			syncProgress.value.syncLogName = response.sync_log_name

			emit('success')
			// Don't close dialog immediately - let user see progress
			// closeDialog()
		} else {
			showError(response.message || __('Sync failed'))
			syncing.value = false
		}
	} catch (error) {
		console.error('Error starting sync:', error)
		showError(error.message || __('Failed to start sync'))
		syncing.value = false
	}
}

const handleConditionsValidate = (validation) => {
	conditionsValid.value = validation.isValid
}

// Setup socket listeners for realtime sync progress
import { globalStore } from '@/stores/global'
const { $socket } = globalStore()

if ($socket) {
	$socket.on('candidate_sync_progress', (data) => {
		if (syncProgress.value.isActive && data.sync_log_name === syncProgress.value.syncLogName) {
			syncProgress.value.successCount = data.success_count
			syncProgress.value.failedCount = data.failed_count
			syncProgress.value.skippedCount = data.skipped_count || 0
			syncProgress.value.totalRecords = data.total_records
			syncProgress.value.currentRecord = data.current_record

			if (data.talent_full_name) {
				syncProgress.value.latestTalent = {
					name: data.talent_name,
					fullName: data.talent_full_name,
					action: data.action,
				}
			}
		}
	})

	$socket.on('candidate_sync_complete', (data) => {
		if (syncProgress.value.isActive && data.sync_log_name === syncProgress.value.syncLogName) {
			syncProgress.value.successCount = data.success_count
			syncProgress.value.failedCount = data.failed_count
			syncProgress.value.skippedCount = data.skipped_count || 0
			syncProgress.value.totalRecords = data.total_records

			// Mark sync as complete
			syncing.value = false

			// Show completion message
			if (data.status === 'Completed') {
				showSuccess(
					__('Sync completed successfully! {0} talents synced.', [data.success_count]),
				)
			} else if (data.status === 'Partially Completed') {
				showSuccess(
					__('Sync completed with some errors. Success: {0}, Failed: {1}', [
						data.success_count,
						data.failed_count,
					]),
				)
			} else if (data.status === 'Failed') {
				showError(__('Sync failed: {0}', [data.details]))
			}

			// Close dialog after a short delay
			setTimeout(() => {
				closeDialog()
			}, 2000)
		}
	})
}
</script>
