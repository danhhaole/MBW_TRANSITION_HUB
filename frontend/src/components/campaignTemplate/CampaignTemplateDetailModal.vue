<template>
	<div
		v-if="show"
		class="fixed inset-0 z-50 overflow-y-auto"
		aria-labelledby="modal-title"
		role="dialog"
		aria-modal="true"
	>
		<div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
			<!-- Background overlay -->
			<div
				class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
				@click="$emit('close')"
			></div>

			<!-- Modal panel -->
			<div
				class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full"
			>
				<!-- Loading state -->
				<div v-if="loading" class="p-8">
					<div class="flex justify-center items-center h-64">
						<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
					</div>
				</div>

				<!-- Content -->
				<div v-else-if="template" class="bg-white">
					<!-- Header -->
					<div class="px-6 py-4 border-b border-gray-200">
						<div class="flex items-center justify-between">
							<div class="flex items-center space-x-4">
								<!-- Template Icon -->
								<div class="w-12 h-12 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg flex items-center justify-center">
									<FeatherIcon
										:name="getTemplateIcon(template.campaign_type)"
										class="w-6 h-6 text-blue-500"
									/>
								</div>

								<!-- Template Info -->
								<div>
									<h3 class="text-lg font-medium text-gray-900">
										{{ template.template_name }}
									</h3>
									<div class="flex items-center space-x-2 mt-1">
										<Badge
											:theme="getTypeBadgeTheme(template.campaign_type)"
											size="sm"
										>
											{{ getTypeDisplay(template.campaign_type) }}
										</Badge>
										<Badge
											v-if="template.is_premium"
											theme="purple"
											size="sm"
										>
											{{ __('Premium') }}
										</Badge>
										<Badge
											v-if="template.is_suggestion"
											theme="green"
											size="sm"
										>
											{{ __('Recommended') }}
										</Badge>
									</div>
								</div>
							</div>

							<!-- Close button -->
							<button
								@click="$emit('close')"
								class="text-gray-400 hover:text-gray-600 transition-colors"
							>
								<FeatherIcon name="x" class="w-6 h-6" />
							</button>
						</div>
					</div>

					<!-- Body -->
					<div class="px-6 py-6 max-h-96 overflow-y-auto">
						<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
							<!-- Left Column -->
							<div class="space-y-6">
								<!-- Description -->
								<div v-if="template.description">
									<h4 class="text-sm font-medium text-gray-900 mb-2">
										{{ __('Description') }}
									</h4>
									<p class="text-sm text-gray-600">
										{{ template.description }}
									</p>
								</div>

								<!-- Target Type -->
								<div v-if="template.target_type">
									<h4 class="text-sm font-medium text-gray-900 mb-2">
										{{ __('Target Type') }}
									</h4>
									<p class="text-sm text-gray-600">
										{{ template.target_type }}
									</p>
								</div>

								<!-- Scope -->
								<div>
									<h4 class="text-sm font-medium text-gray-900 mb-2">
										{{ __('Scope') }}
									</h4>
									<Badge
										:theme="getScopeTheme(template.scope_type)"
										size="sm"
									>
										{{ getScopeDisplay(template.scope_type) }}
									</Badge>
								</div>

								<!-- Configuration -->
								<div v-if="template.configuration_json">
									<h4 class="text-sm font-medium text-gray-900 mb-2">
										{{ __('Configuration') }}
									</h4>
									<div class="bg-gray-50 rounded-lg p-3">
										<pre class="text-xs text-gray-600 whitespace-pre-wrap">{{ formatJSON(template.configuration_json) }}</pre>
									</div>
								</div>
							</div>

							<!-- Right Column -->
							<div class="space-y-6">
								<!-- Statistics -->
								<div>
									<h4 class="text-sm font-medium text-gray-900 mb-3">
										{{ __('Statistics') }}
									</h4>
									<div class="grid grid-cols-2 gap-4">
										<div class="bg-gray-50 rounded-lg p-3">
											<div class="text-2xl font-bold text-gray-900">
												{{ template.usage_count || 0 }}
											</div>
											<div class="text-xs text-gray-500">
												{{ __('Times Used') }}
											</div>
										</div>
										<div class="bg-gray-50 rounded-lg p-3">
											<div class="text-2xl font-bold text-gray-900">
												{{ template.campaign_total || 0 }}
											</div>
											<div class="text-xs text-gray-500">
												{{ __('Campaigns Created') }}
											</div>
										</div>
									</div>
								</div>

								<!-- Metadata -->
								<div>
									<h4 class="text-sm font-medium text-gray-900 mb-3">
										{{ __('Metadata') }}
									</h4>
									<div class="space-y-2 text-sm">
										<div class="flex justify-between">
											<span class="text-gray-500">{{ __('Version') }}:</span>
											<span class="text-gray-900">{{ template.version || '1.0' }}</span>
										</div>
										<div class="flex justify-between">
											<span class="text-gray-500">{{ __('Created') }}:</span>
											<span class="text-gray-900">{{ formatDate(template.created_at) }}</span>
										</div>
										<div class="flex justify-between">
											<span class="text-gray-500">{{ __('Modified') }}:</span>
											<span class="text-gray-900">{{ formatDate(template.updated_at) }}</span>
										</div>
										<div v-if="template.last_used_at" class="flex justify-between">
											<span class="text-gray-500">{{ __('Last Used') }}:</span>
											<span class="text-gray-900">{{ formatDate(template.last_used_at) }}</span>
										</div>
									</div>
								</div>

								<!-- CTA -->
								<div v-if="template.is_has_url_cta && template.url_cta">
									<h4 class="text-sm font-medium text-gray-900 mb-2">
										{{ __('Call to Action') }}
									</h4>
									<a
										:href="template.url_cta"
										target="_blank"
										rel="noopener noreferrer"
										class="text-blue-600 hover:text-blue-800 text-sm underline"
									>
										{{ template.url_cta }}
									</a>
								</div>
							</div>
						</div>
					</div>

					<!-- Footer -->
					<div class="px-6 py-4 bg-gray-50 border-t border-gray-200">
						<div class="flex items-center justify-between">
							<div class="text-sm text-gray-500">
								{{ __('Template ID') }}: {{ template.name }}
							</div>

							<div class="flex items-center space-x-3">
								<Button
									variant="outline"
									@click="$emit('close')"
								>
									{{ __('Close') }}
								</Button>
								<Button
									theme="blue"
									@click="handleUseTemplate"
									:loading="loading"
								>
									<template #prefix>
										<FeatherIcon name="play" class="w-4 h-4" />
									</template>
									{{ __('Use Template') }}
								</Button>
							</div>
						</div>
					</div>
				</div>

				<!-- Error state -->
				<div v-else class="p-8 text-center">
					<div class="text-red-500 mb-4">
						<FeatherIcon name="alert-circle" class="h-12 w-12 mx-auto" />
					</div>
					<h3 class="text-lg font-medium text-gray-900 mb-2">
						{{ __('Template Not Found') }}
					</h3>
					<p class="text-gray-500 mb-4">
						{{ __('The requested template could not be loaded.') }}
					</p>
					<Button @click="$emit('close')" variant="outline">
						{{ __('Close') }}
					</Button>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed } from 'vue'
import { Button, Badge, FeatherIcon } from 'frappe-ui'

// Props
const props = defineProps({
	show: {
		type: Boolean,
		default: false
	},
	template: {
		type: Object,
		default: null
	},
	loading: {
		type: Boolean,
		default: false
	}
})

// Emits
const emit = defineEmits(['close', 'use-template'])

// Methods
const handleUseTemplate = () => {
	emit('use-template', props.template)
}

const getTemplateIcon = (type) => {
	const iconMap = {
		ATTRACTION: 'user-plus',
		NURTURING: 'heart',
		RECRUITMENT: 'briefcase',
	}
	return iconMap[type] || 'file'
}

const getTypeBadgeTheme = (type) => {
	const themeMap = {
		ATTRACTION: 'blue',
		NURTURING: 'green',
		RECRUITMENT: 'purple',
	}
	return themeMap[type] || 'gray'
}

const getTypeDisplay = (type) => {
	const displayMap = {
		ATTRACTION: 'Attraction',
		NURTURING: 'Nurturing',
		RECRUITMENT: 'Recruitment',
	}
	return displayMap[type] || type
}

const getScopeTheme = (scope) => {
	const themeMap = {
		PRIVATE: 'gray',
		TEAM: 'blue',
		ORGANIZATION: 'green',
		PUBLIC: 'purple',
	}
	return themeMap[scope] || 'gray'
}

const getScopeDisplay = (scope) => {
	const displayMap = {
		PRIVATE: 'Private',
		TEAM: 'Team',
		ORGANIZATION: 'Organization',
		PUBLIC: 'Public',
	}
	return displayMap[scope] || scope
}

const formatDate = (dateString) => {
	if (!dateString) return 'N/A'
	
	try {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short',
			day: 'numeric',
			hour: '2-digit',
			minute: '2-digit'
		})
	} catch (e) {
		return dateString
	}
}

const formatJSON = (jsonString) => {
	if (!jsonString) return ''
	
	try {
		const parsed = JSON.parse(jsonString)
		return JSON.stringify(parsed, null, 2)
	} catch (e) {
		return jsonString
	}
}
</script>
