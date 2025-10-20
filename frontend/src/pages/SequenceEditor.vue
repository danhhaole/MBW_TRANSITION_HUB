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
							Back to List
						</div>
					</Button>
					<Button variant="solid" theme="blue" @click="saveSequence" :loading="saving">
						<div class="flex items-center">
							<FeatherIcon name="save" class="w-4 h-4 mr-2" />
							Save Changes
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
					<p class="text-gray-500">Loading sequence...</p>
				</div>
			</div>

			<div v-else-if="error" class="text-center py-12">
				<div class="text-red-500 mb-4">
					<FeatherIcon name="alert-circle" class="w-12 h-12 mx-auto mb-4" />
					<h3 class="text-lg font-medium">Error Loading Sequence</h3>
					<p class="text-sm mt-2">{{ error }}</p>
				</div>
				<Button variant="outline" theme="gray" @click="goBack"> Go Back </Button>
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
                Settings
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
							<span>Bắt đầu gửi sau {{ initialDelay || '1 Ngày' }}</span>
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
									<span
										>Chờ {{ step.delay_from_previous || '1 day' }} rồi tiếp
										tục</span
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
									:class="getStepIconClass(step.channel)"
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
										<div class="flex items-center space-x-4">
											<!-- Step Info -->
											<div>
												<h3
													class="font-medium text-gray-900 flex items-center"
												>
													<FeatherIcon
														:name="getStepIcon(step.channel)"
														class="w-4 h-4 mr-2"
													/>
													{{ getStepTitle(step) }}
												</h3>
												<p class="text-sm text-gray-500 mt-1">
													{{ getStepDescription(step) }}
												</p>
											</div>
										</div>

										<!-- Actions Menu (Show on hover) -->
										<div
											v-if="hoveredStep === index"
											class="absolute -right-[130px] top-1/2 transform -translate-y-1/2 bg-gray-50 p-2 flex flex-col space-y-1 z-20"
										>
											<button
												@click="editStep(index)"
												class="flex items-center px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
											>
												<FeatherIcon name="edit" class="w-4 h-4 mr-2" />
												Chỉnh sửa
											</button>
											<button
												@click="duplicateStep(index)"
												class="flex items-center px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
											>
												<FeatherIcon name="copy" class="w-4 h-4 mr-2" />
												Nhân bản
											</button>
											<button
												@click="removeStep(index)"
												class="flex items-center px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-md transition-colors"
											>
												<FeatherIcon name="trash-2" class="w-4 h-4 mr-2" />
												Xóa
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
										<div v-if="step.channel === 'Email'">
											<EmailEditor
												:content="getStepContent(step)"
												@update:content="updateStepContent(index, $event)"
											/>
										</div>

										<!-- Text Content Editor for SMS/Messenger/Zalo -->
										<div
											v-else-if="
												step.channel === 'SMS' ||
												step.channel === 'Messenger' ||
												step.channel === 'Zalo_OA' ||
												step.channel === 'Zalo_ZNS'
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
													Template ID
												</label>
												<input
													v-model="step.template_id"
													type="text"
													class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
													placeholder="Enter template ID"
												/>
											</div>

											<div>
												<label
													class="block text-sm font-medium text-gray-700 mb-2"
												>
													Action if Replied
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
													getInteractionType(step.channel)
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
											Hủy
										</Button>
										<Button
											variant="solid"
											theme="blue"
											@click="saveStepContent(index)"
										>
											Lưu thay đổi
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
									Thêm tin nhắn mới
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
const hoveredStep = ref(-1)
const showDelayModal = ref(false)
const editingDelayIndex = ref(-1)
const currentEditingDelay = ref('')
const initialDelay = ref('1 Ngày')

// Options
const statusOptions = [
	{ label: 'Draft', value: 'Draft' },
	{ label: 'Active', value: 'Active' },
	{ label: 'Paused', value: 'Paused' },
	{ label: 'Completed', value: 'Completed' },
]

const channelOptions = [
	{ label: 'Email', value: 'Email' },
	{ label: 'SMS', value: 'SMS' },
	{ label: 'Messenger', value: 'Messenger' },
	{ label: 'Zalo OA', value: 'Zalo_OA' },
	{ label: 'Zalo ZNS', value: 'Zalo_ZNS' },
	{ label: 'AI Call', value: 'AI_Call' },
]

const replyActionOptions = [
	{ label: 'Continue', value: 'Continue' },
	{ label: 'Stop Sequence', value: 'Stop Sequence' },
]

// Computed
const parsedSteps = computed(() => {
	if (!sequenceData.value?.steps) return []

	try {
		const steps =
			typeof sequenceData.value.steps === 'string'
				? JSON.parse(sequenceData.value.steps)
				: sequenceData.value.steps
		return Array.isArray(steps) ? steps : []
	} catch (error) {
		console.error('Error parsing steps:', error)
		return []
	}
})

// Methods
const loadSequence = async () => {
	loading.value = true
	error.value = null

	try {
		const result = await sequenceStore.fetchSequenceById(route.params.id)
		if (result.success) {
			sequenceData.value = { ...result.data }
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
		// Update steps JSON
		sequenceData.value.steps = JSON.stringify(parsedSteps.value)

		const result = await sequenceStore.updateSequence(route.params.id, sequenceData.value)
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

const addStep = () => {
	const newStep = {
		step_order: parsedSteps.value.length + 1,
		delay_from_previous: '0 minutes',
		channel: 'Email',
		template_id: '',
		action_if_replied: 'Continue',
		related_action: '',
	}

	const currentSteps = [...parsedSteps.value, newStep]
	sequenceData.value.steps = JSON.stringify(currentSteps)
}

const removeStep = (index) => {
	const currentSteps = parsedSteps.value.filter((_, i) => i !== index)
	// Update step orders
	currentSteps.forEach((step, i) => {
		step.step_order = i + 1
	})
	sequenceData.value.steps = JSON.stringify(currentSteps)
}

const moveStepUp = (index) => {
	if (index === 0) return

	const currentSteps = [...parsedSteps.value]
	const temp = currentSteps[index]
	currentSteps[index] = currentSteps[index - 1]
	currentSteps[index - 1] = temp

	// Update step orders
	currentSteps.forEach((step, i) => {
		step.step_order = i + 1
	})

	sequenceData.value.steps = JSON.stringify(currentSteps)
}

const moveStepDown = (index) => {
	if (index === parsedSteps.value.length - 1) return

	const currentSteps = [...parsedSteps.value]
	const temp = currentSteps[index]
	currentSteps[index] = currentSteps[index + 1]
	currentSteps[index + 1] = temp

	// Update step orders
	currentSteps.forEach((step, i) => {
		step.step_order = i + 1
	})

	sequenceData.value.steps = JSON.stringify(currentSteps)
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
		Zalo_OA: 'phone',
		Zalo_ZNS: 'smartphone',
		AI_Call: 'phone-call',
	}
	return iconMap[channel] || 'mail'
}

const getStepIconClass = (channel) => {
	const classMap = {
		// Email: 'bg-blue-100 text-blue-600',
		// SMS: 'bg-yellow-100 text-yellow-600',
		// Messenger: 'bg-purple-100 text-purple-600',
		// Zalo_OA: 'bg-green-100 text-green-600',
		// Zalo_ZNS: 'bg-indigo-100 text-indigo-600',
		// AI_Call: 'bg-red-100 text-red-600',
	}
	return classMap[channel] || 'bg-white text-blue-600'
}

const getStepTitle = (step) => {
	const titleMap = {
		Email: 'Send Email',
		SMS: 'Send SMS',
		Messenger: 'Send Messenger Message',
		Zalo_OA: 'Send Zalo OA Message',
		Zalo_ZNS: 'Send Zalo ZNS Message',
		AI_Call: 'Make AI Call',
	}
	return titleMap[step.channel] || `Send ${step.channel}`
}

const getStepDescription = (step) => {
	if (step.template_id) {
		return `Using template: ${step.template_id}`
	}
	return `Send a ${step.channel?.toLowerCase()} message to the contact`
}

// Step management methods
const toggleStep = (index) => {
	expandedStep.value = expandedStep.value === index ? -1 : index
}

const getStepContent = (step) => {
	if (step.channel === 'Email') {
		return {
			email_subject: step.email_subject || '',
			email_content: step.email_content || '',
			attachments: step.attachments || [],
		}
	} else {
		// For SMS/Messenger/Zalo - use ZaloEditor format
		return {
			blocks: step.blocks || [
				{
					id: 1,
					type: 'text',
					text_content: step.message_content || '',
				},
			],
		}
	}
}

const updateStepContent = (index, content) => {
	const currentSteps = [...parsedSteps.value]
	if (currentSteps[index]) {
		// Update all content fields
		Object.assign(currentSteps[index], content)
		sequenceData.value.steps = JSON.stringify(currentSteps)
	}
}

const duplicateStep = (index) => {
	const currentSteps = [...parsedSteps.value]
	const stepToDuplicate = { ...currentSteps[index] }
	stepToDuplicate.step_order = currentSteps.length + 1

	currentSteps.push(stepToDuplicate)

	// Update step orders
	currentSteps.forEach((step, i) => {
		step.step_order = i + 1
	})

	sequenceData.value.steps = JSON.stringify(currentSteps)
	toast.success('Step duplicated successfully')
}

const cancelEdit = () => {
	expandedStep.value = -1
}

const saveStepContent = (index) => {
	// Content is already saved via updateStepContent
	expandedStep.value = -1
	toast.success('Step content saved successfully')
}

// Additional Actions methods
const getInteractionType = (channel) => {
	const typeMap = {
		Email: 'EMAIL',
		Zalo_OA: 'ZALO_CARE',
		Zalo_ZNS: 'ZALO_ZNS',
		SMS: 'ZALO_ZNS', // Use ZNS format for SMS
		Messenger: 'ZALO_CARE', // Use CARE format for Messenger
		AI_Call: 'ZALO_CARE', // Use CARE format for AI Call
	}
	return typeMap[channel] || 'EMAIL'
}

const getStepAdditionalActions = (step) => {
	return step.additional_actions || {}
}

const updateStepAdditionalActions = (index, actions) => {
	const currentSteps = [...parsedSteps.value]
	if (currentSteps[index]) {
		currentSteps[index].additional_actions = actions
		sequenceData.value.steps = JSON.stringify(currentSteps)
	}
}

const handleAddStep = (newStep) => {
	const currentSteps = [...parsedSteps.value, newStep]
	// Update step orders
	currentSteps.forEach((step, i) => {
		step.step_order = i + 1
	})
	sequenceData.value.steps = JSON.stringify(currentSteps)
	toast.success('Step added successfully')
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

const saveDelayFromModal = (newDelay) => {
	if (editingDelayIndex.value === 0) {
		// Initial delay
		initialDelay.value = newDelay
		toast.success('Initial delay updated successfully')
	} else {
		// Step delay
		const currentSteps = [...parsedSteps.value]
		if (currentSteps[editingDelayIndex.value]) {
			currentSteps[editingDelayIndex.value].delay_from_previous = newDelay
			sequenceData.value.steps = JSON.stringify(currentSteps)
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
