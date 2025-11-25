<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div class="max-w-full mx-5 px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Left: Back button and Title -->
          <div class="flex items-center space-x-4">
            <Button
              variant="ghost"
              @click="handleBack"
            >
              <template #prefix>
                <FeatherIcon name="arrow-left" class="h-4 w-4" />
              </template>
              {{ __('Back') }}
            </Button>
            
            <div class="h-8 w-px bg-gray-300"></div>
            
            <div>
              <h1 class="text-xl font-semibold text-gray-900">
                {{ isEditMode ? __('Edit Campaign Template') : __('Create Campaign Template') }}
              </h1>
              <p class="text-sm text-gray-500">
                {{ isEditMode ? templateData.template_name : __('Create a new campaign template') }}
              </p>
            </div>
          </div>

          <!-- Right: Actions -->
          <div class="flex items-center space-x-3">
            <!-- Use Template button (only in edit mode) -->
            <Button
              v-if="isEditMode"
              variant="outline"
              @click="handleUseTemplate"
              :loading="usingTemplate"
            >
              <template #prefix>
                <FeatherIcon name="play" class="h-4 w-4" />
              </template>
              {{ __('Use Template') }}
            </Button>
            
            <!-- Save/Update button -->
            <Button
              theme="blue"
              :loading="saving"
              @click="handleSave"
            >
              {{ isEditMode ? __('Update Template') : __('Save Template') }}
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-full mx-5 px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-12">
        <div class="text-red-500 mb-4">
          <FeatherIcon name="alert-circle" class="h-12 w-12 mx-auto" />
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">{{ __('Error Loading Template') }}</h3>
        <p class="text-gray-500 mb-4">{{ error }}</p>
        <Button @click="loadTemplate" variant="outline">
          {{ __('Try Again') }}
        </Button>
      </div>

      <!-- Form Content with Accordion Style -->
      <div v-else class="space-y-4">
        
        <!-- Basic Information - Always Visible -->
        <div class="bg-white rounded-lg shadow">
          <div 
            class="px-6 py-4 border-b border-gray-200 cursor-pointer flex items-center justify-between"
            @click="toggleSection('basic')"
          >
            <div class="flex items-center">
              <FeatherIcon name="info" class="w-5 h-5 mr-3 text-blue-500" />
              <h2 class="text-lg font-medium text-gray-900">{{ __('Basic Information') }}</h2>
            </div>
            <FeatherIcon 
              :name="expandedSections.basic ? 'chevron-up' : 'chevron-down'" 
              class="w-5 h-5 text-gray-400" 
            />
          </div>
          
          <div v-show="expandedSections.basic" class="p-6">
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Template Name -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Template Name') }} <span class="text-red-500">*</span>
              </label>
              <FormControl
                type="text"
                v-model="templateData.template_name"
                :placeholder="__('Enter template name')"
                required
              />
            </div>

            <!-- Campaign Type -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Campaign Type') }} <span class="text-red-500">*</span>
              </label>
              <Select
                v-model="templateData.campaign_type"
                :options="campaignTypeOptions"
                :placeholder="__('Select campaign type')"
              />
            </div>

            <!-- Alias -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Alias') }}
              </label>
              <FormControl
                type="text"
                v-model="templateData.alias"
                :placeholder="__('URL-friendly identifier')"
              />
            </div>

            <!-- Target Type -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Target Type') }}
              </label>
              <Select
                v-model="templateData.target_type"
                :options="targetTypeOptions"
                :placeholder="__('Select target type')"
              />
            </div>
          </div>

          <!-- Description -->
          <div class="mt-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Description') }}
            </label>
            <FormControl
              type="textarea"
              v-model="templateData.description"
              :placeholder="__('Describe what this template does')"
              rows="3"
            />
          </div>

          <!-- Thumbnail -->
          <div class="mt-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Thumbnail') }}
            </label>
            <FormControl
              type="file"
              v-model="templateData.thumbnail"
              accept="image/*"
              :placeholder="__('Upload template thumbnail')"
            />
          </div>
        </div>
        </div>

        <!-- Classification -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-medium text-gray-900 mb-6">{{ __('Classification') }}</h2>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Scope Type -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Scope Type') }} <span class="text-red-500">*</span>
              </label>
              <Select
                v-model="templateData.scope_type"
                :options="scopeTypeOptions"
                :placeholder="__('Select scope')"
              />
            </div>

            <!-- Order Number -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Order Number') }}
              </label>
              <FormControl
                type="number"
                v-model="templateData.order_no"
                :placeholder="__('Display order')"
              />
            </div>

            <!-- Version -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Version') }}
              </label>
              <FormControl
                type="text"
                v-model="templateData.version"
                :placeholder="__('Template version')"
                readonly
              />
            </div>
          </div>

          <!-- Checkboxes -->
          <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="flex items-center">
              <input
                id="is_default"
                type="checkbox"
                v-model="templateData.is_default"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label for="is_default" class="ml-2 block text-sm text-gray-900">
                {{ __('Is Default Template') }}
              </label>
            </div>

            <div class="flex items-center">
              <input
                id="is_premium"
                type="checkbox"
                v-model="templateData.is_premium"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label for="is_premium" class="ml-2 block text-sm text-gray-900">
                {{ __('Is Premium') }}
              </label>
            </div>

            <div class="flex items-center">
              <input
                id="is_suggestion"
                type="checkbox"
                v-model="templateData.is_suggestion"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label for="is_suggestion" class="ml-2 block text-sm text-gray-900">
                {{ __('Show as Suggestion') }}
              </label>
            </div>
          </div>
        </div>

        <!-- Step 1: Campaign Information Template -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-medium text-gray-900 mb-6">{{ __('Step 1: Campaign Information Template') }}</h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Objective -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Campaign Objective') }}
              </label>
              <FormControl
                type="textarea"
                v-model="templateData.campaign_info.objective"
                :placeholder="getCampaignObjectivePlaceholder(templateData.campaign_type)"
                rows="3"
              />
            </div>

            <!-- Target Pool -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Default Target Pool') }}
              </label>
              <FormControl
                type="text"
                v-model="templateData.campaign_info.target_pool"
                :placeholder="__('Default segment or target pool')"
              />
            </div>

            <!-- Campaign Tags -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Default Tags') }}
              </label>
              <FormControl
                type="text"
                v-model="templateData.campaign_info.campaign_tags"
                :placeholder="__('Comma-separated tags')"
              />
              <p class="mt-1 text-xs text-gray-500">
                {{ __('Tags that will be automatically applied to campaigns created from this template') }}
              </p>
            </div>

            <!-- Start Date Strategy -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Start Date Strategy') }}
              </label>
              <Select
                v-model="templateData.campaign_info.start_date"
                :options="startDateOptions"
                :placeholder="__('Select start date strategy')"
              />
            </div>
          </div>
        </div>

        <!-- Step 2: Content & Channels Template -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-medium text-gray-900 mb-6">{{ __('Step 2: Content & Channels Template') }}</h2>
          
          <!-- Channel Selection -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-3">
              {{ __('Default Channels') }}
            </label>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div v-for="channel in getAvailableChannels(templateData.campaign_type)" :key="channel.value" class="flex items-center">
                <input
                  :id="`channel_${channel.value}`"
                  type="checkbox"
                  :value="channel.value"
                  v-model="templateData.content_channels.selected_channels"
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label :for="`channel_${channel.value}`" class="ml-2 block text-sm text-gray-900">
                  {{ channel.label }}
                </label>
              </div>
            </div>
          </div>

          <!-- Content Templates by Channel -->
          <div class="space-y-6">
            <!-- Facebook Content -->
            <div v-if="templateData.content_channels.selected_channels.includes('facebook')" class="border border-gray-200 rounded-lg p-4">
              <h3 class="text-md font-medium text-gray-900 mb-4">{{ __('Facebook Content Template') }}</h3>
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __('Post Text Template') }}
                  </label>
                  <FormControl
                    type="textarea"
                    v-model="templateData.content_channels.facebook_content.post_text"
                    :placeholder="getFacebookContentPlaceholder(templateData.campaign_type)"
                    rows="4"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __('Call to Action') }}
                  </label>
                  <FormControl
                    type="text"
                    v-model="templateData.content_channels.facebook_content.call_to_action"
                    :placeholder="__('Learn More, Apply Now, Contact Us...')"
                  />
                </div>
              </div>
            </div>

            <!-- Zalo Content -->
            <div v-if="templateData.content_channels.selected_channels.includes('zalo')" class="border border-gray-200 rounded-lg p-4">
              <h3 class="text-md font-medium text-gray-900 mb-4">{{ __('Zalo Content Template') }}</h3>
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __('Message Text Template') }}
                  </label>
                  <FormControl
                    type="textarea"
                    v-model="templateData.content_channels.zalo_content.message_text"
                    :placeholder="getZaloContentPlaceholder(templateData.campaign_type)"
                    rows="4"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __('Call to Action') }}
                  </label>
                  <FormControl
                    type="text"
                    v-model="templateData.content_channels.zalo_content.call_to_action"
                    :placeholder="__('Xem thêm, Ứng tuyển ngay, Liên hệ...')"
                  />
                </div>
              </div>
            </div>

            <!-- Landing Page -->
            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="text-md font-medium text-gray-900 mb-4">{{ __('Landing Page Template') }}</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __('Default LadiPage URL') }}
                  </label>
                  <FormControl
                    type="url"
                    v-model="templateData.content_channels.ladipage_url"
                    :placeholder="__('https://ladipage.vn/your-page')"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __('LadiPage ID') }}
                  </label>
                  <FormControl
                    type="text"
                    v-model="templateData.content_channels.ladipage_id"
                    :placeholder="__('LadiPage ID')"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 3: Settings & Automation Template -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-medium text-gray-900 mb-6">{{ __('Step 3: Settings & Automation Template') }}</h2>
          
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Triggers -->
            <div>
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-md font-medium text-gray-900">{{ __('Campaign Triggers') }}</h3>
                <Button
                  variant="outline"
                  size="sm"
                  @click="addCampaignTrigger"
                >
                  <template #prefix>
                    <FeatherIcon name="plus" class="w-4 h-4" />
                  </template>
                  {{ __('Add Trigger') }}
                </Button>
              </div>

              <div v-if="templateData.campaign_settings.triggers && templateData.campaign_settings.triggers.length > 0" class="space-y-4">
                <div
                  v-for="(trigger, index) in templateData.campaign_settings.triggers"
                  :key="index"
                  class="border border-gray-200 rounded-lg p-4"
                >
                  <div class="flex items-center justify-between mb-3">
                    <h4 class="text-sm font-medium text-gray-700">{{ __('Trigger {0}', [index + 1]) }}</h4>
                    <Button
                      variant="ghost"
                      size="sm"
                      theme="red"
                      @click="removeCampaignTrigger(index)"
                    >
                      <FeatherIcon name="trash-2" class="w-4 h-4" />
                    </Button>
                  </div>

                  <div class="grid grid-cols-1 gap-3">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        {{ __('Trigger Type') }}
                      </label>
                      <Select
                        v-model="trigger.trigger_type"
                        :options="getCampaignTriggerOptions(templateData.campaign_type)"
                        :placeholder="__('Select trigger type')"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        {{ __('Trigger Name') }}
                      </label>
                      <FormControl
                        type="text"
                        v-model="trigger.trigger_name"
                        :placeholder="__('Enter trigger name')"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        {{ __('Configuration') }}
                      </label>
                      <FormControl
                        type="textarea"
                        v-model="trigger.trigger_config"
                        :placeholder="getCampaignTriggerConfigPlaceholder(trigger.trigger_type, templateData.campaign_type)"
                        rows="3"
                      />
                    </div>
                  </div>
                </div>
              </div>

              <div v-else class="text-center py-8 text-gray-500">
                <FeatherIcon name="zap" class="w-8 h-8 mx-auto mb-2 text-gray-400" />
                <p class="text-sm">{{ __('No triggers configured') }}</p>
              </div>
            </div>

            <!-- Notification & Tracking Settings -->
            <div class="space-y-6">
              <!-- Notification Settings -->
              <div>
                <h3 class="text-md font-medium text-gray-900 mb-4">{{ __('Notification Settings') }}</h3>
                <div class="space-y-3">
                  <div class="flex items-center">
                    <input
                      id="email_notifications"
                      type="checkbox"
                      v-model="templateData.campaign_settings.notification_settings.email_notifications"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label for="email_notifications" class="ml-2 block text-sm text-gray-900">
                      {{ __('Email Notifications') }}
                    </label>
                  </div>
                  <div class="flex items-center">
                    <input
                      id="sms_notifications"
                      type="checkbox"
                      v-model="templateData.campaign_settings.notification_settings.sms_notifications"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label for="sms_notifications" class="ml-2 block text-sm text-gray-900">
                      {{ __('SMS Notifications') }}
                    </label>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                      {{ __('Webhook URL') }}
                    </label>
                    <FormControl
                      type="url"
                      v-model="templateData.campaign_settings.notification_settings.webhook_url"
                      :placeholder="__('https://your-webhook-url.com')"
                    />
                  </div>
                </div>
              </div>

              <!-- Tracking Settings -->
              <div>
                <h3 class="text-md font-medium text-gray-900 mb-4">{{ __('Tracking Settings') }}</h3>
                <div class="space-y-3">
                  <div class="flex items-center">
                    <input
                      id="track_opens"
                      type="checkbox"
                      v-model="templateData.campaign_settings.tracking_settings.track_opens"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label for="track_opens" class="ml-2 block text-sm text-gray-900">
                      {{ __('Track Email Opens') }}
                    </label>
                  </div>
                  <div class="flex items-center">
                    <input
                      id="track_clicks"
                      type="checkbox"
                      v-model="templateData.campaign_settings.tracking_settings.track_clicks"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label for="track_clicks" class="ml-2 block text-sm text-gray-900">
                      {{ __('Track Link Clicks') }}
                    </label>
                  </div>
                  <div class="flex items-center">
                    <input
                      id="track_conversions"
                      type="checkbox"
                      v-model="templateData.campaign_settings.tracking_settings.track_conversions"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label for="track_conversions" class="ml-2 block text-sm text-gray-900">
                      {{ __('Track Conversions') }}
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Template Actions & Triggers -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-medium text-gray-900 mb-6">{{ __('Advanced Actions & Triggers') }}</h2>
          
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Template Actions -->
            <div>
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-md font-medium text-gray-900">{{ __('Template Actions') }}</h3>
                <Button
                  variant="outline"
                  size="sm"
                  @click="addTemplateAction"
                >
                  <template #prefix>
                    <FeatherIcon name="plus" class="w-4 h-4" />
                  </template>
                  {{ __('Add Action') }}
                </Button>
              </div>

              <div v-if="templateData.template_actions && templateData.template_actions.length > 0" class="space-y-4">
                <div
                  v-for="(action, index) in templateData.template_actions"
                  :key="index"
                  class="border border-gray-200 rounded-lg p-4"
                >
                  <div class="flex items-center justify-between mb-3">
                    <h4 class="text-sm font-medium text-gray-700">{{ __('Action {0}', [index + 1]) }}</h4>
                    <Button
                      variant="ghost"
                      size="sm"
                      theme="red"
                      @click="removeTemplateAction(index)"
                    >
                      <FeatherIcon name="trash-2" class="w-4 h-4" />
                    </Button>
                  </div>

                  <div class="grid grid-cols-1 gap-3">
                    <!-- Action Type -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        {{ __('Action Type') }}
                      </label>
                      <Select
                        v-model="action.action_type"
                        :options="getActionTypeOptions(templateData.campaign_type)"
                        :placeholder="__('Select action type')"
                      />
                    </div>

                    <!-- Action Name -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        {{ __('Action Name') }}
                      </label>
                      <FormControl
                        type="text"
                        v-model="action.action_name"
                        :placeholder="__('Enter action name')"
                      />
                    </div>

                    <!-- Action Config -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        {{ __('Configuration') }}
                      </label>
                      <FormControl
                        type="textarea"
                        v-model="action.action_config"
                        :placeholder="getActionConfigPlaceholder(action.action_type, templateData.campaign_type)"
                        rows="3"
                      />
                    </div>

                    <!-- Order -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        {{ __('Order') }}
                      </label>
                      <FormControl
                        type="number"
                        v-model="action.order_no"
                        :placeholder="__('Execution order')"
                      />
                    </div>

                    <!-- Active -->
                    <div class="flex items-center">
                      <input
                        :id="`action_active_${index}`"
                        type="checkbox"
                        v-model="action.is_active"
                        class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <label :for="`action_active_${index}`" class="ml-2 block text-sm text-gray-900">
                        {{ __('Active') }}
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else class="text-center py-8 text-gray-500">
                <FeatherIcon name="zap" class="w-8 h-8 mx-auto mb-2 text-gray-400" />
                <p class="text-sm">{{ __('No actions configured') }}</p>
                <p class="text-xs">{{ __('Click "Add Action" to get started') }}</p>
              </div>
            </div>

            <!-- Template Triggers -->
            <div>
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-md font-medium text-gray-900">{{ __('Template Triggers') }}</h3>
                <Button
                  variant="outline"
                  size="sm"
                  @click="addTemplateTrigger"
                >
                  <template #prefix>
                    <FeatherIcon name="plus" class="w-4 h-4" />
                  </template>
                  {{ __('Add Trigger') }}
                </Button>
              </div>

              <div v-if="templateData.template_triggers && templateData.template_triggers.length > 0" class="space-y-4">
                <div
                  v-for="(trigger, index) in templateData.template_triggers"
                  :key="index"
                  class="border border-gray-200 rounded-lg p-4"
                >
                  <div class="flex items-center justify-between mb-3">
                    <h4 class="text-sm font-medium text-gray-700">{{ __('Trigger {0}', [index + 1]) }}</h4>
                    <Button
                      variant="ghost"
                      size="sm"
                      theme="red"
                      @click="removeTemplateTrigger(index)"
                    >
                      <FeatherIcon name="trash-2" class="w-4 h-4" />
                    </Button>
                  </div>

                  <div class="grid grid-cols-1 gap-3">
                    <!-- Trigger Type -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        {{ __('Trigger Type') }}
                      </label>
                      <Select
                        v-model="trigger.trigger_type"
                        :options="getTriggerTypeOptions(templateData.campaign_type)"
                        :placeholder="__('Select trigger type')"
                      />
                    </div>

                    <!-- Trigger Name -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        {{ __('Trigger Name') }}
                      </label>
                      <FormControl
                        type="text"
                        v-model="trigger.trigger_name"
                        :placeholder="__('Enter trigger name')"
                      />
                    </div>

                    <!-- Trigger Config -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        {{ __('Configuration') }}
                      </label>
                      <FormControl
                        type="textarea"
                        v-model="trigger.trigger_config"
                        :placeholder="getTriggerConfigPlaceholder(trigger.trigger_type, templateData.campaign_type)"
                        rows="3"
                      />
                    </div>

                    <!-- Order -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        {{ __('Order') }}
                      </label>
                      <FormControl
                        type="number"
                        v-model="trigger.order_no"
                        :placeholder="__('Execution order')"
                      />
                    </div>

                    <!-- Active -->
                    <div class="flex items-center">
                      <input
                        :id="`trigger_active_${index}`"
                        type="checkbox"
                        v-model="trigger.is_active"
                        class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <label :for="`trigger_active_${index}`" class="ml-2 block text-sm text-gray-900">
                        {{ __('Active') }}
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else class="text-center py-8 text-gray-500">
                <FeatherIcon name="play" class="w-8 h-8 mx-auto mb-2 text-gray-400" />
                <p class="text-sm">{{ __('No triggers configured') }}</p>
                <p class="text-xs">{{ __('Click "Add Trigger" to get started') }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Configuration -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-medium text-gray-900 mb-6">{{ __('Additional Configuration') }}</h2>
          
          <!-- Configuration JSON -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Configuration JSON') }}
            </label>
            <FormControl
              type="textarea"
              v-model="templateData.configuration_json"
              :placeholder="__('Enter additional configuration as JSON')"
              rows="6"
            />
            <p class="mt-1 text-sm text-gray-500">
              {{ __('Store additional configuration as JSON format') }}
            </p>
          </div>
        </div>

        <!-- Call to Action -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-medium text-gray-900 mb-6">{{ __('Call to Action') }}</h2>
          
          <div class="space-y-4">
            <!-- Has URL CTA -->
            <div class="flex items-center">
              <input
                id="is_has_url_cta"
                type="checkbox"
                v-model="templateData.is_has_url_cta"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label for="is_has_url_cta" class="ml-2 block text-sm text-gray-900">
                {{ __('Has URL CTA') }}
              </label>
            </div>

            <!-- CTA URL -->
            <div v-if="templateData.is_has_url_cta">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('CTA URL') }}
              </label>
              <FormControl
                type="url"
                v-model="templateData.url_cta"
                :placeholder="__('Enter CTA URL')"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Button, FormControl, Select, FeatherIcon } from 'frappe-ui'
import { useCampaignTemplateStore } from '@/stores/campaignTemplate'
import { useToast } from '@/composables/useToast'

// Composables
const router = useRouter()
const route = useRoute()
const templateStore = useCampaignTemplateStore()
const toast = useToast()

// Reactive state
const loading = ref(false)
const saving = ref(false)
const usingTemplate = ref(false)
const error = ref(null)

// Template data
const templateData = ref({
  // Basic Information
  template_name: '',
  campaign_type: 'ATTRACTION',
  alias: '',
  description: '',
  thumbnail: null,
  target_type: '',
  scope_type: 'PRIVATE',
  order_no: 999,
  version: '1.0',
  is_default: false,
  is_premium: false,
  is_suggestion: false,
  is_has_url_cta: false,
  url_cta: '',
  
  // Step 1: Campaign Information
  campaign_info: {
    objective: '',
    target_pool: '',
    campaign_tags: [],
    start_date: null
  },
  
  // Step 2: Content & Channels
  content_channels: {
    selected_channels: [],
    facebook_content: {
      post_text: '',
      images: [],
      call_to_action: ''
    },
    zalo_content: {
      message_text: '',
      images: [],
      call_to_action: ''
    },
    qr_content: {
      qr_text: '',
      design_template: ''
    },
    ladipage_url: '',
    ladipage_id: '',
    landing_page_config: {}
  },
  
  // Step 3: Settings & Triggers
  campaign_settings: {
    triggers: [],
    automation_rules: [],
    notification_settings: {
      email_notifications: true,
      sms_notifications: false,
      webhook_url: ''
    },
    tracking_settings: {
      track_opens: true,
      track_clicks: true,
      track_conversions: true
    }
  },
  
  // Additional Configuration
  configuration_json: ''
})

// Computed
const isEditMode = computed(() => !!route.params.id)
const templateId = computed(() => route.params.id)

// Options
const campaignTypeOptions = [
  { label: __('Attraction'), value: 'ATTRACTION' },
  { label: __('Nurturing'), value: 'NURTURING' },
  { label: __('Recruitment'), value: 'RECRUITMENT' }
]

const targetTypeOptions = [
  { label: __('Talent'), value: 'Talent' },
  { label: __('Talent Pool'), value: 'Talent Pool' },
  { label: __('Applicant'), value: 'Applicant' }
]

const scopeTypeOptions = [
  { label: __('Private'), value: 'PRIVATE' },
  { label: __('Team'), value: 'TEAM' },
  { label: __('Organization'), value: 'ORGANIZATION' },
  { label: __('Public'), value: 'PUBLIC' }
]

const startDateOptions = [
  { label: __('Immediate'), value: 'immediate' },
  { label: __('Next Business Day'), value: 'next_business_day' },
  { label: __('Custom Date'), value: 'custom' },
  { label: __('User Defined'), value: 'user_defined' }
]

// Methods
const loadTemplate = async () => {
  if (!isEditMode.value) return

  loading.value = true
  error.value = null

  try {
    // Use new API that includes social contents
    const data = await templateStore.loadTemplateWithSocialContents(templateId.value)
    
    console.log('📦 Raw data from API:', data)
    
    if (data) {
      // Map API response to templateData structure
      templateData.value = {
        ...templateData.value,
        // Basic Information
        name: data.name,
        template_name: data.template_name || '',
        description: data.description || '',
        template_description: data.description || '',
        campaign_type: data.campaign_type || 'ATTRACTION',
        scope_type: data.scope_type || 'PRIVATE',
        is_default: data.is_default || false,
        is_premium: data.is_premium || false,
        is_suggestion: data.is_suggestion || false,
        is_active: data.is_active || false,
        
        // Campaign Info
        objective: data.objective || '',
        target_pool: data.target_pool || '',
        config_data: data.config_data || '',
        conditions: data.conditions || '',
        candidate_count: data.candidate_count || 0,
        campaign_tags: data.campaign_tags || [],
        
        // Landing Page
        ladipage_url: data.ladipage_url || '',
        ladipage_id: data.ladipage_id || '',
        
        // Social Contents (Step 2)
        selected_channels: data.selected_channels || [],
        facebook_content: data.facebook_content || {},
        zalo_content: data.zalo_content || {},
        email_content: data.email_content || {},
        sms_content: data.sms_content || {},
        
        // Also map to nested structure if needed
        campaign_info: {
          objective: data.objective || '',
          target_pool: data.target_pool || '',
          campaign_tags: data.campaign_tags || [],
          start_date: null
        },
        content_channels: {
          selected_channels: data.selected_channels || [],
          facebook_content: {
            post_text: data.facebook_content?.content || '',
            images: [],
            call_to_action: '',
            image: data.facebook_content?.image || null
          },
          zalo_content: {
            message_text: data.zalo_content?.content || '',
            images: [],
            call_to_action: '',
            image: data.zalo_content?.image || null
          },
          email_content: {
            subject: data.email_content?.subject || '',
            body: data.email_content?.body || data.email_content?.content || '',
            mjml_content: data.email_content?.mjml_content || null,
            block_content: data.email_content?.block_content || null
          },
          qr_content: {
            qr_text: '',
            design_template: ''
          },
          ladipage_url: data.ladipage_url || '',
          ladipage_id: data.ladipage_id || ''
        }
      }
      console.log('✅ Mapped template data:', templateData.value)
    } else {
      // Fallback to old method
      const result = await templateStore.fetchTemplateById(templateId.value)
      if (result.success) {
        templateData.value = { ...templateData.value, ...result.data }
      } else {
        error.value = result.error || __('Failed to load template')
      }
    }
  } catch (err) {
    console.error('Error loading template:', err)
    error.value = __('An error occurred while loading template')
  } finally {
    loading.value = false
  }
}

const handleSave = async () => {
  // Validate required fields
  if (!templateData.value.template_name?.trim()) {
    toast.error(__('Template name is required'))
    return
  }

  if (!templateData.value.campaign_type) {
    toast.error(__('Campaign type is required'))
    return
  }

  saving.value = true

  try {
    let result
    
    // Prepare data for API - map content_channels to flat structure
    const saveData = {
      ...templateData.value,
      // Map content_channels to API format
      selected_channels: templateData.value.content_channels?.selected_channels || templateData.value.selected_channels || [],
      facebook_content: {
        content: templateData.value.content_channels?.facebook_content?.post_text || '',
        image: templateData.value.content_channels?.facebook_content?.image || null
      },
      zalo_content: {
        content: templateData.value.content_channels?.zalo_content?.message_text || '',
        image: templateData.value.content_channels?.zalo_content?.image || null
      },
      email_content: {
        subject: templateData.value.content_channels?.email_content?.subject || '',
        body: templateData.value.content_channels?.email_content?.body || '',
        content: templateData.value.content_channels?.email_content?.body || '',
        mjml_content: templateData.value.content_channels?.email_content?.mjml_content || null,
        block_content: templateData.value.content_channels?.email_content?.block_content || null
      },
      ladipage_url: templateData.value.content_channels?.ladipage_url || templateData.value.ladipage_url || '',
      ladipage_id: templateData.value.content_channels?.ladipage_id || templateData.value.ladipage_id || ''
    }
    
    console.log('💾 Saving template data:', saveData)
    
    if (isEditMode.value) {
      result = await templateStore.updateTemplate(templateId.value, saveData)
      
      // Save social contents if any channels selected
      const selectedChannels = saveData.selected_channels || []
      if (result.success && selectedChannels.length > 0) {
        await templateStore.saveSocialContents(templateId.value, saveData)
      }
    } else {
      result = await templateStore.createTemplate(saveData)
    }

    if (result.success) {
      toast.success(
        isEditMode.value 
          ? __('Template updated successfully') 
          : __('Template created successfully')
      )
      
      // Navigate back to template management
      router.push({ name: 'CampaignTemplateManagement' })
    } else {
      toast.error(result.error || __('Failed to save template'))
    }
  } catch (err) {
    console.error('Error saving template:', err)
    toast.error(__('An error occurred while saving template'))
  } finally {
    saving.value = false
  }
}

const handleUseTemplate = async () => {
  if (!isEditMode.value) return

  usingTemplate.value = true

  try {
    const result = await templateStore.useTemplate(
      templateId.value,
      `${templateData.value.template_name} - ${new Date().toLocaleString()}`
    )

    if (result.success) {
      toast.success(__('Campaign created successfully from template!'))
      router.push(`/campaigns/${result.campaign_name}/edit`)
    } else {
      toast.error(result.error || __('Failed to create campaign from template'))
    }
  } catch (err) {
    console.error('Error using template:', err)
    toast.error(__('An error occurred while creating campaign'))
  } finally {
    usingTemplate.value = false
  }
}

const handleBack = () => {
  router.push({ name: 'CampaignTemplateManagement' })
}

// Actions & Triggers Methods
const addTemplateAction = () => {
  templateData.value.template_actions.push({
    action_type: '',
    action_name: '',
    action_config: '',
    order_no: templateData.value.template_actions.length + 1,
    is_active: true
  })
}

const removeTemplateAction = (index) => {
  templateData.value.template_actions.splice(index, 1)
}

const addTemplateTrigger = () => {
  templateData.value.template_triggers.push({
    trigger_type: '',
    trigger_name: '',
    trigger_config: '',
    order_no: templateData.value.template_triggers.length + 1,
    is_active: true
  })
}

const removeTemplateTrigger = (index) => {
  templateData.value.template_triggers.splice(index, 1)
}

// Campaign-specific methods
const addCampaignTrigger = () => {
  templateData.value.campaign_settings.triggers.push({
    trigger_type: '',
    trigger_name: '',
    trigger_config: '',
    order_no: templateData.value.campaign_settings.triggers.length + 1,
    is_active: true
  })
}

const removeCampaignTrigger = (index) => {
  templateData.value.campaign_settings.triggers.splice(index, 1)
}

// Get available channels based on campaign type
const getAvailableChannels = (campaignType) => {
  const baseChannels = [
    { label: __('Facebook'), value: 'facebook' },
    { label: __('Zalo'), value: 'zalo' },
    { label: __('Email'), value: 'email' },
    { label: __('SMS'), value: 'sms' }
  ]

  switch (campaignType) {
    case 'ATTRACTION':
      return [
        ...baseChannels,
        { label: __('LinkedIn'), value: 'linkedin' },
        { label: __('Website'), value: 'website' }
      ]
    case 'NURTURING':
      return [
        ...baseChannels,
        { label: __('WhatsApp'), value: 'whatsapp' },
        { label: __('Telegram'), value: 'telegram' }
      ]
    case 'RECRUITMENT':
      return [
        ...baseChannels,
        { label: __('Job Boards'), value: 'job_boards' },
        { label: __('Career Page'), value: 'career_page' }
      ]
    default:
      return baseChannels
  }
}

// Get campaign objective placeholder
const getCampaignObjectivePlaceholder = (campaignType) => {
  const placeholders = {
    'ATTRACTION': 'Attract potential candidates through engaging content and targeted outreach. Build brand awareness and generate interest in our company culture and opportunities.',
    'NURTURING': 'Nurture existing leads and candidates through personalized communication. Build relationships and keep candidates engaged throughout the hiring process.',
    'RECRUITMENT': 'Actively recruit qualified candidates for specific positions. Focus on direct outreach and conversion to applications.'
  }
  return placeholders[campaignType] || 'Define the main objective and goals for this campaign template.'
}

// Get Facebook content placeholder
const getFacebookContentPlaceholder = (campaignType) => {
  const placeholders = {
    'ATTRACTION': '🚀 Join our amazing team! We\'re looking for talented individuals who are passionate about innovation and growth.\n\n✨ What we offer:\n- Competitive salary\n- Flexible working hours\n- Great team culture\n\n#Hiring #JoinUs #CareerOpportunity',
    'NURTURING': '👋 Hi there! Thanks for your interest in our company. We\'d love to keep you updated about exciting opportunities that match your skills.\n\nStay connected with us for:\n📈 Career tips\n💼 Job openings\n🎯 Industry insights',
    'RECRUITMENT': '🎯 We\'re actively hiring for [Position Name]!\n\n📋 Requirements:\n- [Skill 1]\n- [Skill 2]\n- [Experience level]\n\n💰 Competitive package + benefits\n📍 [Location]\n\nReady to take the next step in your career?'
  }
  return placeholders[campaignType] || 'Enter your Facebook post content template here...'
}

// Get Zalo content placeholder
const getZaloContentPlaceholder = (campaignType) => {
  const placeholders = {
    'ATTRACTION': 'Chào bạn! 👋\n\nChúng tôi đang tìm kiếm những tài năng xuất sắc để gia nhập đội ngũ. Bạn có muốn khám phá cơ hội nghề nghiệp tuyệt vời tại công ty chúng tôi không?\n\n🌟 Môi trường làm việc chuyên nghiệp\n💰 Mức lương cạnh tranh\n📈 Cơ hội phát triển',
    'NURTURING': 'Xin chào! 😊\n\nCảm ơn bạn đã quan tâm đến công ty chúng tôi. Chúng tôi sẽ thường xuyên cập nhật những cơ hội việc làm phù hợp với bạn.\n\nHãy theo dõi để nhận:\n✅ Thông tin tuyển dụng mới\n✅ Chia sẻ kinh nghiệm nghề nghiệp',
    'RECRUITMENT': '🎯 Tuyển dụng vị trí [Tên vị trí]!\n\n📌 Yêu cầu:\n- [Kỹ năng 1]\n- [Kỹ năng 2]\n- [Kinh nghiệm]\n\n💼 Lương thỏa thuận + phúc lợi hấp dẫn\n📍 [Địa điểm làm việc]\n\nSẵn sàng ứng tuyển ngay?'
  }
  return placeholders[campaignType] || 'Nhập nội dung tin nhắn Zalo mẫu tại đây...'
}

// Get campaign trigger options
const getCampaignTriggerOptions = (campaignType) => {
  return getTriggerTypeOptions(campaignType)
}

// Get campaign trigger config placeholder
const getCampaignTriggerConfigPlaceholder = (triggerType, campaignType) => {
  return getTriggerConfigPlaceholder(triggerType, campaignType)
}

// Get action type options based on campaign type
const getActionTypeOptions = (campaignType) => {
  const baseActions = [
    { label: __('Send Email'), value: 'SEND_EMAIL' },
    { label: __('Send SMS'), value: 'SEND_SMS' },
    { label: __('Update Status'), value: 'UPDATE_STATUS' },
    { label: __('Add Tag'), value: 'ADD_TAG' },
    { label: __('Remove Tag'), value: 'REMOVE_TAG' }
  ]

  switch (campaignType) {
    case 'ATTRACTION':
      return [
        ...baseActions,
        { label: __('Create Lead'), value: 'CREATE_LEAD' },
        { label: __('Send Welcome Message'), value: 'SEND_WELCOME' },
        { label: __('Subscribe Newsletter'), value: 'SUBSCRIBE_NEWSLETTER' },
        { label: __('Track Page View'), value: 'TRACK_PAGE_VIEW' }
      ]
    case 'NURTURING':
      return [
        ...baseActions,
        { label: __('Send Follow-up'), value: 'SEND_FOLLOWUP' },
        { label: __('Schedule Call'), value: 'SCHEDULE_CALL' },
        { label: __('Send Resource'), value: 'SEND_RESOURCE' },
        { label: __('Update Score'), value: 'UPDATE_SCORE' }
      ]
    case 'RECRUITMENT':
      return [
        ...baseActions,
        { label: __('Schedule Interview'), value: 'SCHEDULE_INTERVIEW' },
        { label: __('Send Assessment'), value: 'SEND_ASSESSMENT' },
        { label: __('Update Application Status'), value: 'UPDATE_APPLICATION' },
        { label: __('Send Offer'), value: 'SEND_OFFER' }
      ]
    default:
      return baseActions
  }
}

// Get trigger type options based on campaign type
const getTriggerTypeOptions = (campaignType) => {
  const baseTriggers = [
    { label: __('Time Based'), value: 'TIME_BASED' },
    { label: __('Event Based'), value: 'EVENT_BASED' },
    { label: __('Status Change'), value: 'STATUS_CHANGE' },
    { label: __('Tag Added'), value: 'TAG_ADDED' },
    { label: __('Tag Removed'), value: 'TAG_REMOVED' }
  ]

  switch (campaignType) {
    case 'ATTRACTION':
      return [
        ...baseTriggers,
        { label: __('Form Submitted'), value: 'FORM_SUBMITTED' },
        { label: __('Page Visited'), value: 'PAGE_VISITED' },
        { label: __('Email Opened'), value: 'EMAIL_OPENED' },
        { label: __('Link Clicked'), value: 'LINK_CLICKED' }
      ]
    case 'NURTURING':
      return [
        ...baseTriggers,
        { label: __('Email Replied'), value: 'EMAIL_REPLIED' },
        { label: __('Call Completed'), value: 'CALL_COMPLETED' },
        { label: __('Resource Downloaded'), value: 'RESOURCE_DOWNLOADED' },
        { label: __('Score Threshold'), value: 'SCORE_THRESHOLD' }
      ]
    case 'RECRUITMENT':
      return [
        ...baseTriggers,
        { label: __('Application Submitted'), value: 'APPLICATION_SUBMITTED' },
        { label: __('Interview Scheduled'), value: 'INTERVIEW_SCHEDULED' },
        { label: __('Assessment Completed'), value: 'ASSESSMENT_COMPLETED' },
        { label: __('Offer Accepted'), value: 'OFFER_ACCEPTED' }
      ]
    default:
      return baseTriggers
  }
}

// Get action config placeholder
const getActionConfigPlaceholder = (actionType, campaignType) => {
  const templates = {
    'SEND_EMAIL': `{
  "template_id": "email_template_001",
  "subject": "Welcome to our platform",
  "delay_minutes": 0
}`,
    'SEND_SMS': `{
  "message": "Thank you for your interest!",
  "delay_minutes": 5
}`,
    'CREATE_LEAD': `{
  "source": "campaign",
  "priority": "medium",
  "assign_to": "sales_team"
}`,
    'SCHEDULE_INTERVIEW': `{
  "interview_type": "phone",
  "duration_minutes": 30,
  "auto_schedule": true
}`,
    'SEND_FOLLOWUP': `{
  "template_id": "followup_template_001",
  "delay_days": 3,
  "max_attempts": 3
}`
  }

  return templates[actionType] || `{
  "key": "value",
  "delay_minutes": 0
}`
}

// Get trigger config placeholder
const getTriggerConfigPlaceholder = (triggerType, campaignType) => {
  const templates = {
    'TIME_BASED': `{
  "delay_minutes": 60,
  "repeat": false,
  "timezone": "UTC"
}`,
    'FORM_SUBMITTED': `{
  "form_id": "contact_form",
  "required_fields": ["email", "name"]
}`,
    'EMAIL_OPENED': `{
  "email_template_id": "welcome_email",
  "track_opens": true
}`,
    'APPLICATION_SUBMITTED': `{
  "job_id": "required",
  "auto_acknowledge": true
}`,
    'SCORE_THRESHOLD': `{
  "min_score": 80,
  "score_type": "engagement"
}`
  }

  return templates[triggerType] || `{
  "condition": "value",
  "threshold": 1
}`
}

// Lifecycle
onMounted(() => {
  if (isEditMode.value) {
    loadTemplate()
  }
})
</script>
