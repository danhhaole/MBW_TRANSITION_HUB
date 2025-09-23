<template>
	<div class="space-y-6">

		<div class="space-y-6">
			<!-- Career Page -->
			<div class="bg-white border border-gray-200 rounded-lg p-4">
				<div class="flex items-start space-x-3">
					<div class="flex-shrink-0 mt-1">
						<Checkbox
							size="md"
							v-model="formData.publish_to_career_page"
							:value="formData.publish_to_career_page"
							class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
						>	
							{{ __('Company Career Page') }}
						</Checkbox>
					</div>
					<div class="flex-1">
						<div class="flex items-center space-x-2">
							<FeatherIcon name="globe" class="h-5 w-5 text-blue-600" />
							<h4 class="text-lg font-medium text-gray-900">{{ __('Company Career Page') }}</h4>
							<span class="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded">{{ __('Recommended') }}</span>
						</div>
						<p class="text-sm text-gray-600 mt-1">
							{{ __('Display on your company\'s career page for direct applications. When published, job status will be set to Open.') }}
						</p>
					</div>
				</div>
			</div>

			<!-- TopCV -->
			<div class="bg-white border border-gray-200 rounded-lg p-4">
				<div class="flex items-start space-x-3">
					<div class="flex-shrink-0 mt-1">
						<Checkbox
							size="md"
							v-model="formData.publish_to_topcv"
							:value="formData.publish_to_topcv"
							class="rounded border-gray-300 text-green-600 focus:ring-green-500"
						>
							{{ __('TopCV') }}
						</Checkbox>
					</div>
					<div class="flex-1">
						<div class="flex items-center space-x-2">
							<div class="w-5 h-5 bg-green-600 rounded flex items-center justify-center">
								<span class="text-white text-xs font-bold">T</span>
							</div>
							<h4 class="text-lg font-medium text-gray-900">{{ __('TopCV') }}</h4>
							<span class="bg-green-100 text-green-800 text-xs font-medium px-2 py-1 rounded">{{ __('Popular') }}</span>
						</div>
						<p class="text-sm text-gray-600 mt-1">
							{{ __('Post to TopCV job portal for wider candidate reach. Synchronization via TopCV ID.') }}
						</p>
						
						<!-- TopCV ID Field - hiện khi checkbox được chọn -->
						<div v-if="formData.publish_to_topcv" class="mt-3">
							<FormControl 
								:label="__('TopCV ID')"
								type="text"
								:placeholder="__('Enter TopCV synchronization ID')"
								:modelValue="formData.top_cv_id"
								@update:modelValue="(value) => emit('update:formData', { top_cv_id: value })"
								required
							/>
							<p class="text-xs text-gray-500 mt-1">
								{{ __('Required for TopCV integration. Contact TopCV support to get your sync ID.') }}
							</p>
						</div>
					</div>
				</div>
			</div>

			<!-- Cal.com -->
			<div class="bg-white border border-gray-200 rounded-lg p-4">
				<div class="flex items-start space-x-3">
					<div class="flex-shrink-0 mt-1">

						<Checkbox
							size="md"
							v-model="formData.enable_calcom_integration"
							:value="formData.enable_calcom_integration"
							class="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
						>
							{{ __('Enable Cal.com Integration') }}
						</Checkbox>
					</div>
					<div class="flex-1">
						<div class="flex items-center space-x-2">
							<FeatherIcon name="calendar" class="h-5 w-5 text-purple-600" />
							<h4 class="text-lg font-medium text-gray-900">{{ __('Cal.com Integration') }}</h4>
							<span class="bg-purple-100 text-purple-800 text-xs font-medium px-2 py-1 rounded">{{ __('Auto') }}</span>
						</div>
						<p class="text-sm text-gray-600 mt-1">
							{{ __('Enable calendar integration for automated interview scheduling') }}
						</p>
						
						<!-- Cal.com Display Field (readonly) - chỉ hiện khi đã có cal_com_id -->
						<div v-if="formData.cal_com_id" class="mt-3">
							<FormControl 
								:label="__('Cal.com URL')"
								type="text"
								:modelValue="formData.cal_com_id"
								readonly
							/>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Publishing Summary -->
		<!-- <div v-if="selectedChannels.length > 0" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
			<h4 class="text-sm font-medium text-blue-900 mb-3">{{ __('Publishing Summary') }}</h4>
			<div class="space-y-2">
				<div class="flex items-center justify-between text-sm">
					<span class="text-blue-800">{{ __('Selected Channels:') }}</span>
					<span class="font-medium text-blue-900">{{ selectedChannels.length }}</span>
				</div>
				<div class="text-xs text-blue-700">
					<span class="font-medium">{{ __('Channels:') }}</span> {{ selectedChannels.join(', ') }}
				</div>
				<div class="flex items-center text-xs text-blue-600">
					<FeatherIcon name="info" class="h-3 w-3 mr-1" />
					<span>{{ __('Publishing will happen automatically after job opening creation') }}</span>
				</div>
			</div>
		</div> -->

		<!-- Channel Performance Insights -->
		<!-- <div class="bg-purple-50 border border-purple-200 rounded-lg p-4">
			<h4 class="text-sm font-medium text-purple-900 mb-3">{{ __('Channel Performance Tips') }}</h4>
			<div class="space-y-2 text-sm text-purple-800">
				<div class="flex items-start space-x-2">
					<FeatherIcon name="target" class="h-4 w-4 text-purple-600 mt-0.5 flex-shrink-0" />
					<span><strong>Career Page:</strong> {{ __('Best for employer branding and direct applications') }}</span>
				</div>
				<div class="flex items-start space-x-2">
					<FeatherIcon name="search" class="h-4 w-4 text-purple-600 mt-0.5 flex-shrink-0" />
					<span><strong>TopCV:</strong> {{ __('High volume of active job seekers in Vietnam') }}</span>
				</div>
				<div class="flex items-start space-x-2">
					<FeatherIcon name="calendar" class="h-4 w-4 text-purple-600 mt-0.5 flex-shrink-0" />
					<span><strong>Cal.com:</strong> {{ __('Streamlined interview scheduling and calendar management') }}</span>
				</div>
			</div>
		</div> -->

		<!-- Quick Actions -->
		<div class="flex flex-wrap gap-2">
			<!-- <Button
				size="sm"
				variant="outline"
				theme="blue"
				@click="selectRecommended"
			>
				{{ __('Select Recommended') }}
			</Button> -->
			<!-- <Button
				size="sm"
				variant="outline"
				theme="gray"
				@click="clearAllChannels"
			>
				{{ __('Clear All') }}
			</Button> -->
		</div>

		<!-- Validation Errors -->
		<div v-if="validationErrors.length > 0" class="bg-red-50 border border-red-200 rounded-lg p-4">
			<h4 class="text-sm font-medium text-red-900 mb-2">{{ __('Please fix the following issues:') }}</h4>
			<ul class="text-sm text-red-700 space-y-1">
				<li v-for="error in validationErrors" :key="error" class="flex items-center">
					<FeatherIcon name="alert-circle" class="h-3 w-3 mr-2 flex-shrink-0" />
					{{ __(error) }}
				</li>
			</ul>
		</div>
	</div>
</template>

<script setup>
import { computed, provide, watch } from 'vue'
import { FeatherIcon, Button, FormControl, Checkbox } from 'frappe-ui'

const props = defineProps({
	formData: {
		type: Object,
		required: true
	}
})

console.log("formData", props.formData)

const emit = defineEmits(['update:formData'])

// Alias for clarity
const formData = computed(() => props.formData || {})

// Create reactive data for provide
const providedData = ref(formData.value)

// Watch for formData changes to update provided data
watch(formData, (newData) => {
	console.log('🔄 Channels formData changed:', newData)
	providedData.value = newData
}, { deep: true, immediate: true })

// Provide data for Field components
provide('data', providedData)
provide('doctype', 'JobOpening')
provide('preview', false)

// Computed properties
const selectedChannels = computed(() => {
	const channels = []
	
	if (formData.value.publish_to_career_page) {
		channels.push(__('Career Page'))
	}
	if (formData.value.publish_to_topcv) {
		channels.push(__('TopCV'))
	}
	if (formData.value.enable_calcom_integration) {
		channels.push(__('Cal.com'))
	}
	
	return channels
})

// Validation
const validationErrors = computed(() => {
	const errors = []
	
	// Validation cho TopCV ID
	if (formData.value.publish_to_topcv && (!formData.value.top_cv_id || formData.value.top_cv_id.trim() === '')) {
		errors.push(__('TopCV ID is required when TopCV publishing is enabled'))
	}
	
	return errors
})

// Expose validation for parent component
const isValid = computed(() => validationErrors.value.length === 0)

// Methods
const selectRecommended = () => {
	const updates = {
		publish_to_career_page: 1,
		publish_to_topcv: 1,
		enable_calcom_integration: 1  // ✅ Bao gồm Cal.com trong recommended
	}
	emit('update:formData', updates)
}

const clearAllChannels = () => {
	const updates = {
		publish_to_career_page: 0,
		publish_to_topcv: 0,
		enable_calcom_integration: 0,
		top_cv_id: ''
	}
	emit('update:formData', updates)
}

// Watch for TopCV unchecking to clear ID
watch(() => formData.value.publish_to_topcv, (newValue) => {
	if (!newValue && formData.value.top_cv_id) {
		emit('update:formData', { top_cv_id: '' })
	}
})

// Expose validation to parent
defineExpose({
	isValid,
	validationErrors
})
</script> 