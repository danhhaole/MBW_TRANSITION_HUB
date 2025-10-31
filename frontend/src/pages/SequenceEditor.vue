<template>
	<div class="min-h-screen bg-gray-50">
		<!-- Header -->
		<LayoutHeader>
			<template #left-header>
				<Breadcrumbs
					:items="[
						{ label: 'Sequences', route: { name: 'SequenceManagement' } },
						{
							label: sequenceData?.title || 'Sequence Editor',
							route: { name: 'SequenceEditor', params: { id: $route.params.id } },
						},
					]"
				/>
			</template>
			<template #right-header>
				<div class="flex items-center space-x-3">
					<Button variant="outline" theme="gray" @click="goBack">
						<div class="flex items-center">
							<FeatherIcon name="arrow-left" class="w-4 h-4 mr-2" />
							{{ __('Back to List') }}
						</div>
					</Button>
					<Button variant="solid" theme="gray" @click="saveSequence" :loading="saving">
						<div class="flex items-center">
							<FeatherIcon name="refresh-cw" class="w-4 h-4 mr-2" />
							{{ __('Sync All Changes') }}
						</div>
					</Button>
				</div>
			</template>
		</LayoutHeader>

		<!-- Main Content -->
		<div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
			<div v-if="loading" class="flex items-center justify-center py-12">
				<div class="text-center">
					<FeatherIcon
						name="loader"
						class="w-8 h-8 animate-spin mx-auto mb-4 text-gray-400"
					/>
					<p class="text-gray-500">{{ __('Loading sequence...') }}</p>
				</div>
			</div>

			<div v-else-if="error" class="text-center py-12">
				<div class="text-red-500 mb-4">
					<FeatherIcon name="alert-circle" class="w-12 h-12 mx-auto mb-4" />
					<h3 class="text-lg font-medium"> {{__('Error Loading Sequence')}}</h3>
					<p class="text-sm mt-2">{{ error }}</p>
				</div>
				<Button variant="outline" theme="gray" @click="goBack"> {{__('Go Back')}} </Button>
			</div>

			<div v-else class="space-y-6">
				<!-- Sequence Header -->
				<!-- <div class="bg-white rounded-lg shadow-sm border p-6">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-2xl font-bold text-gray-900">{{ sequenceData?.title }}</h1>
              <p class="text-gray-500 mt-1">{{ sequenceData?.purpose || 'No description' }}</p>
            </div>
            <div class="flex items-center space-x-3">
              <Badge
                :variant="getStatusVariant(sequenceData?.status)"
                :label="getStatusDisplay(sequenceData?.status)"
              />
              <Button
                variant="outline"
                theme="gray"
                size="sm"
                @click="showSettingsModal = true"
              >
                <FeatherIcon name="settings" class="w-4 h-4 mr-2" />
                {{__('Settings')}}
              </Button>
            </div>
          </div>
        </div> -->

				<!-- Sequence Steps Timeline -->
				<div class="relative">
					<!-- Initial Delay (Before first step) -->
					<div v-if="parsedSteps.length > 0" class="relative text-center mb-12">
						<!-- Đường nối nửa đầu -->
						<div
							class="absolute left-1/2 top-full translate-x-[-50%] w-px h-12 border-l-2 border-dashed border-gray-300 z-0"
						></div>
						<!-- Display Initial Delay -->
						<div
							@click="editInitialDelay"
							class="inline-flex items-center space-x-2 bg-white text-black px-4 py-2 rounded-full text-sm font-medium cursor-pointer hover:bg-blue-100 transition-colors"
						>
							<FeatherIcon name="play" class="w-4 h-4" />
							<span>{{ __('Send after ') }}{{ initialDelay || '1 Ngày' }}</span>
						</div>
					</div>

					<!-- Steps List -->
					<div v-if="parsedSteps.length > 0" class="relative">
						<div
							v-for="(step, index) in parsedSteps"
							:key="index"
							class="relative mb-16"
						>
							<!-- Timeline connector to next step -->

							<!-- Delay Indicator on Timeline -->
							<div
								v-if="index > 0"
								class="absolute left-0 -top-12 flex items-center justify-center w-full z-10"
							>
								<!-- Display Delay -->
								<div
									@click="editDelay(index)"
									class="inline-flex items-center space-x-2 bg-white text-black px-4 py-2 rounded-full text-sm font-medium cursor-pointer hover:bg-orange-100 transition-colors"
								>
									<FeatherIcon name="clock" class="w-4 h-4" />
									<span>{{ __('Wait ') }}{{ step.delay_from_previous || '1 day' }}
										{{ __('then continue') }}</span
									>
								</div>
							</div>

							<!-- Step Block -->
							<div
								class="bg-white rounded-lg shadow-sm border transition-all duration-200 relative z-10"
							>
								<!-- Step Number Circle - Positioned at center -->
								<div
									class="absolute bg-white -left-12 top-6 w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium border border-solid border-blue-500 z-20 shadow-sm"
									:class="getStepIconClass(step.flow?.channel || step.channel)"
								>
									{{ index + 1 }}
								</div>

								<!-- Step Header (Collapsed View) -->
								<div
									class="p-6 pl-12 hover:bg-gray-50 transition-colors group relative"
									@mouseenter="hoveredStep = index"
									@mouseleave="hoveredStep = -1"
								>
									<div class="flex items-center justify-between">
										<div class="flex items-center space-x-4 flex-1">
											<!-- Step Info -->
											<div class="flex-1">
												<!-- Editable Title -->
												<div class="flex items-center group">
													<FeatherIcon
														:name="getStepIcon(step.flow?.channel || step.channel)"
														class="w-4 h-4 mr-2 flex-shrink-0"
													/>
													
													<!-- Display mode -->
													<h3
														v-if="editingTitleIndex !== index"
														class="font-medium text-gray-900 flex items-center"
													>
														{{ getStepTitle(step) }}
														<button
															@click="startEditTitle(index, step)"
															class="ml-2 opacity-0 group-hover:opacity-100 transition-opacity"
														>
															<FeatherIcon
																name="edit"
																class="w-4 h-4 text-black hover:text-blue-600"
															/>
														</button>
													</h3>
													
													<!-- Edit mode -->
													<div
														v-else
														class="flex items-center space-x-2 flex-1"
													>
														<input
															v-model="editingTitleValue"
															@keyup.enter="saveStepTitle(index)"
															@keyup.esc="cancelEditTitle"
															class="flex-1 px-2 py-1 border border-blue-500 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
															autofocus
														/>
														<button
															@click="saveStepTitle(index)"
															class="p-1 text-green-600 hover:bg-green-50 rounded"
														>
															<FeatherIcon name="check" class="w-4 h-4" />
														</button>
														<button
															@click="cancelEditTitle"
															class="p-1 text-red-600 hover:bg-red-50 rounded"
														>
															<FeatherIcon name="x" class="w-4 h-4" />
														</button>
													</div>
												</div>
												
												<p class="text-sm text-gray-500 mt-1">
													{{ getStepDescription(step) }}
												</p>
											</div>
										</div>

										<!-- Actions Menu (Show on hover, hide when editing) -->
										<div
											v-if="hoveredStep === index && expandedStep !== index"
											class="absolute -right-[120px] top-1/2 transform -translate-y-1/2 bg-gray-50 p-2 flex flex-col space-y-1 z-20"
										>
											<button
												@click="editStep(index)"
												class="flex items-center px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
											>
												<FeatherIcon name="edit" class="w-4 h-4 mr-2" />
												{{ __('Edit') }}
											</button>
											<button
												@click="duplicateStep(index)"
												class="flex items-center px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
											>
												<FeatherIcon name="copy" class="w-4 h-4 mr-2" />
												{{ __('Duplicate') }}
											</button>
											<button
												@click="confirmDeleteStep(index)"
												class="flex items-center px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-md transition-colors"
											>
												<FeatherIcon name="trash-2" class="w-4 h-4 mr-2" />
												{{ __('Delete') }}
											</button>
										</div>
									</div>
								</div>

								<!-- Step Content Editor (Expanded View) -->
								<div
									v-if="expandedStep === index"
									class="border-t border-gray-100"
								>
									<div class="p-6 space-y-6">
										<!-- Email Editor -->
										<div v-if="(step.flow?.channel || step.channel) === 'Email'">
											<EmailEditor
												:content="getStepContent(step)"
												@update:content="updateStepContent(index, $event)"
											/>
										</div>

										<!-- Text Content Editor for SMS/Messenger/Zalo -->
										<div
											v-else-if="
												(step.flow?.channel || step.channel) === 'SMS' ||
												(step.flow?.channel || step.channel) === 'Messenger' ||
												(step.flow?.channel || step.channel) === 'Zalo_OA' ||
												(step.flow?.channel || step.channel) === 'Zalo_ZNS' ||
												(step.flow?.channel || step.channel) === 'Zalo'
											"
										>
											<ZaloEditor
												:content="getStepContent(step)"
												@update:content="updateStepContent(index, $event)"
											/>
										</div>

										<!-- Basic fields for all types -->
										<div class="space-y-4 border-t border-gray-100 pt-6">
											<div>
												<label
													class="block text-sm font-medium text-gray-700 mb-2"
												>
													{{ __('Template ID') }}
												</label>
												<FormControl 
													v-model="step.template_id"
													type="text"
													:placeholder="__('Enter template ID')"
												/>
												
											</div>

											<div>
												<label
													class="block text-sm font-medium text-gray-700 mb-2"
												>
													{{ __('Action if Replied') }}
												</label>
												<Select
													v-model="step.action_if_replied"
													:options="replyActionOptions"
													placeholder="Continue"
												/>
											</div>
										</div>

										<!-- Additional Actions -->
										<div class="border-t border-gray-100 pt-6">
											<AdditionalActions
												:interaction-type="
													getInteractionType(step.flow?.channel || step.channel)
												"
												:model-value="getStepAdditionalActions(step)"
												@update:model-value="
													updateStepAdditionalActions(index, $event)
												"
											/>
										</div>
									</div>

									<!-- Action Buttons -->
									<div
										class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex justify-end space-x-3"
									>
										<Button variant="outline" theme="gray" @click="cancelEdit">
											{{ __('Cancel') }}
										</Button>
										<Button
											variant="solid"
											theme="gray"
											@click="saveStepContent(index)"
										>
											{{ __('Save Changes') }}
										</Button>
									</div>
								</div>

								<!-- Dòng nối (gạch gạch gạch) -->
								<div
									v-if="index < parsedSteps.length - 1"
									class="absolute left-1/2 top-full translate-x-[-50%] w-px h-16 border-l-2 border-dashed border-gray-300 z-0"
								></div>
							</div>
						</div>
					</div>

					<!-- Add Step Button -->
					<div class="text-center relative">
						<!-- Timeline line extends to button -->

						<div
							class="border-2 border-dashed border-gray-300 rounded-lg p-8 bg-gray-50 hover:bg-gray-100 transition-colors"
						>
							<Button
								variant="outline"
								theme="blue"
								@click="showAddStepModal = true"
								class="w-full py-3"
							>
								<div class="flex items-center justify-center">
									<FeatherIcon name="plus" class="w-5 h-5 mr-2" />
									{{ __('Add Step') }}
								</div>
							</Button>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Add Step Modal -->
		<AddStepModal
			v-if="showAddStepModal"
			:show="showAddStepModal"
			:existing-steps="parsedSteps"
			@close="showAddStepModal = false"
			@success="handleAddStep"
		/>

		<!-- Delay Edit Modal -->
		<DelayEditModal
			:show="showDelayModal"
			:current-delay="currentEditingDelay"
			:is-initial="editingDelayIndex === 0"
			@save="saveDelayFromModal"
			@cancel="cancelDelayEdit"
			@update:show="showDelayModal = $event"
		/>

		<!-- Delete Confirmation Dialog -->
		<div
			v-if="showDeleteConfirm"
			class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
			@click.self="cancelDelete"
		>
			<div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
				<div class="flex items-start mb-4">
					<div class="flex-shrink-0">
						<FeatherIcon name="alert-triangle" class="w-6 h-6 text-red-600" />
					</div>
					<div class="ml-3 flex-1">
						<h3 class="text-lg font-medium text-gray-900">
							{{ __('Delete Step') }}
						</h3>
						<p class="mt-2 text-sm text-gray-500">
							{{ __('Are you sure you want to delete this step? This action cannot be undone.') }}
						</p>
					</div>
				</div>
				<div class="flex justify-end space-x-3 mt-6">
					<Button
						variant="outline"
						@click="cancelDelete"
						:disabled="deletingStep"
					>
						{{ __('Cancel') }}
					</Button>
					<Button
						variant="solid"
						theme="red"
						@click="removeStep"
						:loading="deletingStep"
						:disabled="deletingStep"
					>
						<div class="flex items-center">
							<FeatherIcon v-if="!deletingStep" name="trash-2" class="w-4 h-4 mr-2" />
							<FeatherIcon v-else name="loader" class="w-4 h-4 mr-2 animate-spin" />
							{{ deletingStep ? __('Deleting...') : __('Delete') }}
						</div>
					</Button>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Button, Select, Badge, FeatherIcon, Breadcrumbs } from 'frappe-ui'
import { useSequenceStore } from '@/stores/sequence'
import { useToast } from '@/composables/useToast'
import LayoutHeader from '@/components/LayoutHeader.vue'
import AddStepModal from '@/components/sequence/AddStepModal.vue'
import DelayEditModal from '@/components/sequence/DelayEditModal.vue'
import EmailEditor from '@/components/campaign/content-editors/EmailEditor.vue'
import ZaloEditor from '@/components/campaign/content-editors/ZaloEditor.vue'
import AdditionalActions from '@/components/campaign/AdditionalActions.vue'

// Composables
const route = useRoute()
const router = useRouter()
const sequenceStore = useSequenceStore()
const toast = useToast()

// Reactive state
const sequenceData = ref(null)
const loading = ref(true)
const saving = ref(false)
const error = ref(null)
const showAddStepModal = ref(false)
const showSettingsModal = ref(false)
const editingStepIndex = ref(-1)
const expandedStep = ref(-1)
const editingTitleIndex = ref(-1)
const editingTitleValue = ref('')
const hoveredStep = ref(-1)
const showDelayModal = ref(false)
const editingDelayIndex = ref(-1)
const currentEditingDelay = ref('')
const initialDelay = ref('1 Ngày')
const addingStep = ref(false)
const deletingStep = ref(false)
const showDeleteConfirm = ref(false)
const stepToDelete = ref(null)

// Options
const statusOptions = [
	{ label: 'Draft', value: 'Draft' },
	{ label: 'Active', value: 'Active' },
	{ label: 'Paused', value: 'Paused' },
	{ label: 'Completed', value: 'Completed' },
]

const channelOptions = [
	{ label: 'Email', value: 'Email' },
	// { label: 'SMS', value: 'SMS' },
	// { label: 'Messenger', value: 'Messenger' },
	// { label: 'Zalo OA', value: 'Zalo_OA' },
	// { label: 'Zalo ZNS', value: 'Zalo_ZNS' },
	// { label: 'AI Call', value: 'AI_Call' },
]

const replyActionOptions = [
	{ label: 'Continue', value: 'Continue' },
	{ label: 'Stop Sequence', value: 'Stop Sequence' },
]

// Computed
const parsedSteps = computed(() => {
	if (!sequenceData.value?.steps) return []
	return Array.isArray(sequenceData.value.steps) ? sequenceData.value.steps : []
})

// Methods
const loadSequence = async () => {
	loading.value = true
	error.value = null

	try {
		const result = await sequenceStore.fetchSequenceById(route.params.id)
		if (result.success) {
			// Force reactivity by creating new object
			sequenceData.value = JSON.parse(JSON.stringify(result.data))
		} else {
			error.value = result.error || 'Sequence not found'
		}
	} catch (err) {
		console.error('Error loading sequence:', err)
		error.value = 'Failed to load sequence'
	} finally {
		loading.value = false
	}
}

const saveSequence = async () => {
	saving.value = true

	try {
		// Prepare steps JSON (delays only)
		const stepsJson = parsedSteps.value.map(step => ({
			delay: step.delay || '1 day',
			flow_id: step.flow?.name || null
		}))

		// Update sequence with steps JSON
		const result = await sequenceStore.updateSequence(route.params.id, {
			...sequenceData.value,
			steps: JSON.stringify(stepsJson)
		})
		
		if (result.success) {
			toast.success('Sequence saved successfully!')
		} else {
			toast.error(result.error || 'Failed to save sequence')
		}
	} catch (error) {
		console.error('Error saving sequence:', error)
		toast.error('Failed to save sequence')
	} finally {
		saving.value = false
	}
}

// Handle add step from modal
const handleAddStep = async (newStep) => {
	if (addingStep.value) return
	
	try {
		addingStep.value = true
		
		// Use sequenceData.value.name as fallback
		const sequenceId = sequenceData.value?.name || route.params.id

		if (!sequenceId || sequenceId === '0') {
			toast.error('Invalid sequence ID. Please reload the page.')
			return
		}

		// Create step with action
		const stepData = {
			...newStep,
			delay: newStep.delay || '1 day',
			action: newStep.action || {
				action_type: 'EMAIL',
				channel_type: newStep.channel || 'Email',
				parameters: {}
			}
		}

		// Create step (Mira Flow + update steps JSON)
		const result = await sequenceStore.createSequenceStep(sequenceId, stepData)
		if (result.success) {
			// Reload sequence data
			await loadSequence()
			toast.success('Step added successfully!')
			showAddStepModal.value = false
		} else {
			toast.error(result.error || 'Failed to add step')
		}
	} catch (error) {
		console.error('Error adding step:', error)
		toast.error('Failed to add step')
	} finally {
		addingStep.value = false
	}
}

const confirmDeleteStep = (index) => {
	stepToDelete.value = index
	showDeleteConfirm.value = true
}

const removeStep = async () => {
	if (deletingStep.value || stepToDelete.value === null) return
	
	try {
		deletingStep.value = true
		const index = stepToDelete.value
		const stepToRemove = parsedSteps.value[index]
		
		if (!stepToRemove || !stepToRemove.flow) {
			toast.error('Invalid step')
			return
		}

		// Delete step (Mira Flow + update steps JSON)
		const result = await sequenceStore.deleteSequenceStep(
			stepToRemove.flow.name,
			route.params.id,
			index
		)
		
		if (result.success) {
			// Reload sequence data
			await loadSequence()
			toast.success('Step removed successfully!')
			showDeleteConfirm.value = false
			stepToDelete.value = null
		} else {
			toast.error(result.error || 'Failed to remove step')
		}
	} catch (error) {
		console.error('Error removing step:', error)
		toast.error('Failed to remove step')
	} finally {
		deletingStep.value = false
	}
}

const cancelDelete = () => {
	showDeleteConfirm.value = false
	stepToDelete.value = null
}

const moveStepUp = async (index) => {
	if (index === 0) return

	// Note: Reordering would require updating creation timestamps or adding an order field
	// For now, we'll keep this as a placeholder
	toast.info('Step reordering will be implemented with order field')
}

const moveStepDown = async (index) => {
	if (index === parsedSteps.value.length - 1) return

	// Note: Reordering would require updating creation timestamps or adding an order field
	// For now, we'll keep this as a placeholder
	toast.info('Step reordering will be implemented with order field')
}

const getStatusVariant = (status) => {
	const variantMap = {
		Active: 'success',
		Draft: 'gray',
		Paused: 'warning',
		Completed: 'blue',
	}
	return variantMap[status] || 'gray'
}

const getStatusDisplay = (status) => {
	const statusMap = {
		Active: 'Hoạt động',
		Draft: 'Nháp',
		Paused: 'Tạm dừng',
		Completed: 'Hoàn thành',
	}
	return statusMap[status] || status
}

// Timeline specific methods
const getStepIcon = (channel) => {
	const iconMap = {
		Email: 'mail',
		SMS: 'message-square',
		Messenger: 'message-circle',
		Zalo_OA: 'message-circle',
		Zalo_ZNS: 'message-circle',
		Zalo: 'message-circle',
		AI_Call: 'phone',
	}
	return iconMap[channel] || 'send'
}

const getStepIconClass = (channel) => {
	const classMap = {
		Email: 'text-blue-600 border-blue-500',
		SMS: 'text-green-600 border-green-500',
		Messenger: 'text-purple-600 border-purple-500',
		Zalo_OA: 'text-blue-600 border-blue-500',
		Zalo_ZNS: 'text-blue-600 border-blue-500',
		Zalo: 'text-blue-600 border-blue-500',
		AI_Call: 'text-orange-600 border-orange-500',
	}
	return classMap[channel] || 'text-gray-600 border-gray-500'
}

const getStepTitle = (step) => {
	// Use flow title if available, otherwise generate from channel
	if (step.flow && step.flow.title) {
		return step.flow.title
	}

	const channel = step.flow?.channel || step.channel
	const titleMap = {
		Email: 'Send Email',
		// SMS: 'Send SMS',
		// Messenger: 'Send Messenger Message',
		// Zalo_OA: 'Send Zalo OA Message',
		// Zalo_ZNS: 'Send Zalo ZNS Message',
		// AI_Call: 'Make AI Call',
	}
	return titleMap[channel] || `Send ${channel}`
}

const getStepDescription = (step) => {
	if (step.template_id) {
		return `Using template: ${step.template_id}`
	}
	const channel = step.flow?.channel || step.channel || 'message'
	return `Send a ${channel.toLowerCase()} message to the contact`
}

// Step management methods
const toggleStep = (index) => {
	expandedStep.value = expandedStep.value === index ? -1 : index
}

const getStepContent = (step) => {
	// Get content from flow.actions[0].action_parameters
	let actionParams = {}
	if (step.flow && step.flow.actions && step.flow.actions.length > 0) {
		try {
			actionParams = JSON.parse(step.flow.actions[0].action_parameters || '{}')
		} catch (e) {
			console.error('Error parsing action parameters:', e)
		}
	}

	if (step.flow?.channel === 'Email') {
		return {
			email_subject: actionParams.subject || '',
			email_content: actionParams.content || '',
			attachments: actionParams.attachments || [],
		}
	} else {
		// For SMS/Messenger/Zalo - use ZaloEditor format
		return {
			blocks: actionParams.blocks || [
				{
					id: 1,
					type: 'text',
					text_content: actionParams.message_content || '',
				},
			],
		}
	}
}

const updateStepContent = (index, content) => {
	// Don't mutate during render - just update the flow directly
	const step = parsedSteps.value[index]
	if (!step || !step.flow) return

	// Update flow content locally
	if (content.email_subject !== undefined || content.email_content !== undefined) {
		// Update email action parameters
		if (!step.flow.actions) {
			step.flow.actions = []
		}
		if (step.flow.actions.length === 0) {
			step.flow.actions.push({
				action_type: 'EMAIL',
				channel_type: 'Email',
				action_parameters: JSON.stringify({})
			})
		}
		
		const params = JSON.parse(step.flow.actions[0].action_parameters || '{}')
		
		// Only update if value actually changed
		let changed = false
		if (content.email_subject !== undefined && params.subject !== content.email_subject) {
			params.subject = content.email_subject
			changed = true
		}
		if (content.email_content !== undefined && params.content !== content.email_content) {
			params.content = content.email_content
			changed = true
		}
		
		if (changed) {
			step.flow.actions[0].action_parameters = JSON.stringify(params)
		}
	}
}

const duplicateStep = async (index) => {
	try {
		const stepToDuplicate = parsedSteps.value[index]
		if (!stepToDuplicate || !stepToDuplicate.flow) {
			toast.error('Invalid step')
			return
		}

		// Prepare new step data
		const newStepData = {
			title: stepToDuplicate.flow.title + ' (Copy)',
			channel: stepToDuplicate.flow.channel,
			delay: stepToDuplicate.delay || '1 day',
			action: stepToDuplicate.flow.actions?.[0] ? {
				action_type: stepToDuplicate.flow.actions[0].action_type,
				channel_type: stepToDuplicate.flow.actions[0].channel_type,
				parameters: JSON.parse(stepToDuplicate.flow.actions[0].action_parameters || '{}')
			} : null
		}

		// Create new step
		const result = await sequenceStore.createSequenceStep(route.params.id, newStepData)
		if (result.success) {
			// Reload sequence data
			await loadSequence()
			toast.success('Step duplicated successfully!')
		} else {
			toast.error(result.error || 'Failed to duplicate step')
		}
	} catch (error) {
		console.error('Error duplicating step:', error)
		toast.error('Failed to duplicate step')
	}
}

const cancelEdit = () => {
	expandedStep.value = -1
}

const saveStepContent = async (index) => {
	try {
		const stepToSave = parsedSteps.value[index]
		if (!stepToSave || !stepToSave.flow) {
			toast.error('Invalid step')
			return
		}

		// Prepare step data for update
		const stepData = {
			title: stepToSave.flow.title,
			channel: stepToSave.flow.channel,
			actions: stepToSave.flow.actions || []
		}

		// Update step in Mira Flow
		const result = await sequenceStore.updateSequenceStep(
			stepToSave.flow.name,
			stepData,
			route.params.id
		)
		
		if (result.success) {
			// Reload sequence data
			await loadSequence()
			expandedStep.value = -1
			toast.success('Step saved successfully!')
		} else {
			toast.error(result.error || 'Failed to save step')
		}
	} catch (error) {
		console.error('Error saving step:', error)
		toast.error('Failed to save step')
	}
}

// Additional Actions methods
const getInteractionType = (channel) => {
	const typeMap = {
		Email: 'EMAIL',
		Zalo_OA: 'ZALO_CARE',
		Zalo_ZNS: 'ZALO_ZNS',
		SMS: 'ZALO_ZNS', // SMS uses same format as ZNS
		Messenger: 'ZALO_CARE', // Use CARE format for Messenger
		AI_Call: 'ZALO_CARE', // Use CARE format for AI Call
	}
	return typeMap[channel] || 'EMAIL'
}

const getStepAdditionalActions = (step) => {
	// Get additional actions from flow.trigger_id
	if (!step.flow || !step.flow.trigger_id) return {}
	
	console.log('📖 LOADING Additional Actions from triggers:', step.flow.trigger_id)
	
	const additionalActions = {}
	const triggers = Array.isArray(step.flow.trigger_id) ? step.flow.trigger_id : []
	
	triggers.forEach(trigger => {
		try {
			// Parse conditions to get action data
			const conditions = JSON.parse(trigger.conditions || '{}')
			
			// Convert trigger_type back to key
			const triggerKey = getTriggerKeyFromType(trigger.trigger_type)
			
			console.log(`Converting back: ${trigger.trigger_type} -> ${triggerKey}`, conditions)
			
			if (triggerKey) {
				additionalActions[triggerKey] = {
					type: conditions.action_type,
					data: conditions.action_data || {},
					configured: conditions.configured || false
				}
			} else {
				console.warn(`No mapping for trigger_type: ${trigger.trigger_type}`)
			}
		} catch (e) {
			console.error('Error parsing trigger conditions:', e)
		}
	})
	
	console.log('Final additionalActions:', additionalActions)
	
	return additionalActions
}

// Helper to convert trigger_type back to key
const getTriggerKeyFromType = (triggerType) => {
	const keyMap = {
		'ON_EMAIL_REPLY': 'reply',
		'ON_LINK_CLICK': 'link_click',
		'ON_EMAIL_OPEN': 'email_open',
		'ON_EMAIL_BOUNCE': 'bounce',
		'ON_UNSUBSCRIBE': 'unsubscribe',
		'ON_SEND_SUCCESS': 'send_success',
		'ON_SEND_FAILED': 'send_failed',
		'ON_USER_RESPONSE': 'user_response'
	}
	return keyMap[triggerType]
}

const updateStepAdditionalActions = async (index, additionalActions) => {
	try {
		const stepToUpdate = parsedSteps.value[index]
		if (!stepToUpdate || !stepToUpdate.flow) {
			toast.error('Invalid step')
			return
		}

		console.log('📝 SAVING Additional Actions:')
		console.log('Input additionalActions:', additionalActions)

		// Convert additional actions to triggers
		// Each additional action becomes a trigger with its corresponding action
		const triggers = Object.entries(additionalActions).map(([triggerKey, actionData]) => {
			console.log(`Converting: ${triggerKey} ->`, actionData)
			const triggerType = getTriggerType(triggerKey)
			console.log(`Trigger type: ${triggerType}`)
			
			return {
				trigger_type: triggerType, // Use actual trigger type (now supported in DocType)
				status: 'ACTIVE',
				channel: stepToUpdate.flow.channel,
				// Store action data in conditions
				conditions: JSON.stringify({
					action_type: actionData.type,
					action_data: actionData.data,
					configured: actionData.configured
				})
			}
		})
		
		console.log('Final triggers to save:', triggers)

		// Update flow with triggers
		const result = await sequenceStore.updateFlowTriggers(
			stepToUpdate.flow.name,
			triggers,
			route.params.id
		)
		
		if (result.success) {
			// Reload sequence data
			await loadSequence()
			toast.success('Additional actions saved!')
		} else {
			toast.error(result.error || 'Failed to save additional actions')
		}
	} catch (error) {
		console.error('Error saving additional actions:', error)
		toast.error('Failed to save additional actions')
	}
}

const startEditTitle = (index, step) => {
	editingTitleIndex.value = index
	editingTitleValue.value = step.flow?.title || 'New Step'
}

const cancelEditTitle = () => {
	editingTitleIndex.value = -1
	editingTitleValue.value = ''
}

const saveStepTitle = async (index) => {
	try {
		const step = parsedSteps.value[index]
		if (!step || !step.flow) {
			toast.error('Invalid step')
			return
		}

		const newTitle = editingTitleValue.value.trim()
		if (!newTitle) {
			toast.error('Title cannot be empty')
			return
		}

		// Update flow title
		const result = await sequenceStore.updateSequenceStep(
			step.flow.name,
			{ title: newTitle },
			route.params.id
		)

		if (result.success) {
			await loadSequence()
			toast.success('Step title updated!')
			cancelEditTitle()
		} else {
			toast.error(result.error || 'Failed to update title')
		}
	} catch (error) {
		console.error('Error updating title:', error)
		toast.error('Failed to update title')
	}
}

// Helper to convert trigger key to trigger_type
const getTriggerType = (key) => {
	const typeMap = {
		// Old keys (for backward compatibility)
		'reply': 'ON_EMAIL_REPLY',
		'click': 'ON_LINK_CLICK',
		'open': 'ON_EMAIL_OPEN',
		'bounce': 'ON_EMAIL_BOUNCE',
		'unsubscribe': 'ON_UNSUBSCRIBE',
		// New keys from AdditionalActions component
		'email_open': 'ON_EMAIL_OPEN',
		'link_click': 'ON_LINK_CLICK',
		'send_success': 'ON_SEND_SUCCESS',
		'send_failed': 'ON_SEND_FAILED',
		'user_response': 'ON_USER_RESPONSE'
	}
	return typeMap[key] || 'CUSTOM_EVENT'
}

const editDelay = (index) => {
	editingDelayIndex.value = index
	currentEditingDelay.value = parsedSteps.value[index].delay_from_previous || '1 day'
	showDelayModal.value = true
}

const editInitialDelay = () => {
	editingDelayIndex.value = 0
	currentEditingDelay.value = initialDelay.value
	showDelayModal.value = true
}

const saveDelayFromModal = async (newDelay) => {
	if (editingDelayIndex.value === 0) {
		// Initial delay
		initialDelay.value = newDelay
		toast.success('Initial delay updated successfully')
	} else {
		// Step delay - update in steps JSON
		const stepToUpdate = parsedSteps.value[editingDelayIndex.value]
		if (stepToUpdate) {
			// Update local state
			stepToUpdate.delay = newDelay
			
			// Save to sequence
			await saveSequence()
			toast.success('Delay updated successfully')
		}
	}
	showDelayModal.value = false
	editingDelayIndex.value = -1
}

const cancelDelayEdit = () => {
	showDelayModal.value = false
	editingDelayIndex.value = -1
	currentEditingDelay.value = ''
}

const editStep = (index) => {
	expandedStep.value = index
	hoveredStep.value = -1 // Hide hover menu
}

const goBack = () => {
	router.push({ name: 'SequenceManagement' })
}

// Lifecycle
onMounted(() => {
	loadSequence()
})
</script>
