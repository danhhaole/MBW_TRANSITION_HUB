<template>
  <Dialog
    v-model="localShow"
    :options="{
      title: __('Edit Action'),
      size: '4xl'
    }"
  >
    <template #body-content>
      <div v-if="localAction" class="space-y-6">
        <!-- Action Type Header -->
        <div class="flex items-center space-x-3 pb-4 border-b border-gray-200">
          <div class="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
            <FeatherIcon :name="getActionIcon(localAction.action_type)" class="h-5 w-5 text-blue-600" />
          </div>
          <div>
            <h3 class="text-base font-semibold text-gray-900">{{ getActionLabel(localAction.action_type) }}</h3>
            <p class="text-xs text-gray-500">{{ getActionDescription(localAction.action_type) }}</p>
          </div>
        </div>

        <!-- Action Type Selector -->
        <div class="grid grid-cols-2 gap-4">
          <FormControl
            type="select"
            :label="__('Action Type')"
            v-model="localAction.action_type"
            :options="actionTypeOptions"
            @change="handleActionTypeChange"
            required
          />
          <FormControl
            v-if="needsChannelForAction(localAction.action_type)"
            type="select"
            :label="__('Channel')"
            v-model="localAction.channel_type"
            :options="channelOptions"
          />
        </div>

        <!-- Content Editors based on Action Type -->
        <!-- 
          NOTE: Based on documentation, only 8 action types are active:
          1. EMAIL ✅
          2. MESSAGE ✅
          3. UPDATE_FIELD_VALUE ✅
          4. ADD_TAG ✅
          5. REMOVE_TAG ✅
          6. CHANGE_STATUS ✅
          7. STOP_TRACKING ✅
          8. INTERNAL_NOTIFICATION ✅
          9. HANDOFF_TO_ATS ✅
          
          The following action types are kept for future use but NOT in actionTypeOptions:
          - ADD_CUSTOM_FIELD
          - EXTERNAL_REQUEST
          - AI_CALL
          - FACEBOOK
          - SMS
          - ZALO
          - SMART_DELAY
          - REMOVE_CUSTOM_FIELD
          - SENT_NOTIFICATION
          - UNSUBSCRIBE
        -->
        <div class="space-y-4">
          <!-- EMAIL Action -->
          <div v-if="localAction.action_type === 'EMAIL'" class="space-y-4">
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="mail" class="h-4 w-4 text-blue-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-blue-900">
                    {{ __('Send Email') }}
                  </p>
                  <p class="text-xs text-blue-700">
                    {{ __('This action will send an email to talent when triggered') }}
                  </p>
                </div>
              </div>
            </div>
            
            <EmailContentEditor
              :content="emailContent"
              @update:content="handleEmailContentUpdate"
            />
            
            <!-- Sender Account Selection -->
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __('Sender Account') }}
                <span class="text-red-500">*</span>
              </label>
              <Autocomplete
                v-model="selectedSenderAccount"
                :options="emailAccountOptions"
                :placeholder="__('Select email account...')"
              />
              <p class="text-xs text-gray-500 mt-1">
                {{ __('Select the email account to send from') }}
              </p>
            </div>
          </div>

          <!-- MESSAGE Action (Zalo/SMS) -->
          <div v-else-if="localAction.action_type === 'MESSAGE'" class="space-y-4">
            <FormControl
              type="select"
              :label="__('Message Channel')"
              v-model="localAction.channel_type"
              :options="messageChannelOptions"
              required
            />
            
            <!-- Zalo Content Editor -->
            <div v-if="localAction.channel_type === 'Zalo'">
              <ZaloContentEditor
                :content="localAction.content || { blocks: [] }"
                @update:content="localAction.content = $event"
              />
            </div>
            
            <!-- SMS Content -->
            <div v-else-if="localAction.channel_type === 'SMS'">
              <FormControl
                type="textarea"
                :label="__('SMS Message')"
                v-model="localAction.content"
                :placeholder="__('Enter SMS message...')"
                rows="4"
                :maxlength="160"
                required
              />
              <div class="flex justify-between items-center mt-2">
                <p class="text-xs text-gray-500">
                  {{ __('Keep it short and clear (max 160 characters)') }}
                </p>
                <span class="text-xs text-gray-500">
                  {{ (localAction.content?.length || 0) }}/160
                </span>
              </div>
            </div>
          </div>

          <!-- ADD_CUSTOM_FIELD Action -->
          <div v-else-if="localAction.action_type === 'ADD_CUSTOM_FIELD'" class="space-y-4">
            <div class="bg-purple-50 border border-purple-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="edit-3" class="h-4 w-4 text-purple-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-purple-900">
                    {{ __('Update Talent Field') }}
                  </p>
                  <p class="text-xs text-purple-700">
                    {{ __('This action will update a field value in talent profile when triggered') }}
                  </p>
                </div>
              </div>
            </div>
            
            <!-- Field Selection -->
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __('Select Field') }}
                <span class="text-red-500">*</span>
              </label>
              <Autocomplete
                v-model="selectedFieldName"
                :options="talentFieldOptions"
                :placeholder="__('Search and select field...')"
              />
              <p class="text-xs text-gray-500 mt-1">
                {{ __('Choose which field to update in talent profile') }}
              </p>
            </div>
            
            <!-- Show selected field info -->
            <div v-if="selectedField" class="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-medium text-gray-700">{{ __('Field Type') }}:</span>
                  <span class="text-xs text-gray-600">{{ selectedField.fieldtype }}</span>
                </div>
                <div v-if="selectedField.description" class="text-xs text-gray-500">
                  {{ selectedField.description }}
                </div>
              </div>
            </div>
            
            <!-- Field Value Input (dynamic based on field type) -->
            <div v-if="selectedField">
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __('Field Value') }}
                <span class="text-red-500">*</span>
              </label>
              
              <!-- Select field -->
              <FormControl
                v-if="selectedField.fieldtype === 'Select'"
                type="select"
                v-model="localAction.field_value"
                :options="getSelectOptions(selectedField.options)"
                :placeholder="__('Select value...')"
                required
              />
              
              <!-- Date field -->
              <FormControl
                v-else-if="selectedField.fieldtype === 'Date'"
                type="date"
                v-model="localAction.field_value"
                :placeholder="__('Select date...')"
                required
              />
              
              <!-- Float/Currency field -->
              <FormControl
                v-else-if="['Float', 'Currency', 'Int'].includes(selectedField.fieldtype)"
                type="number"
                v-model="localAction.field_value"
                :placeholder="__('Enter number...')"
                required
              />
              
              <!-- Check field -->
              <FormControl
                v-else-if="selectedField.fieldtype === 'Check'"
                type="checkbox"
                v-model="localAction.field_value"
              />
              
              <!-- Text area fields -->
              <FormControl
                v-else-if="['Text', 'Small Text', 'Long Text'].includes(selectedField.fieldtype)"
                type="textarea"
                v-model="localAction.field_value"
                :placeholder="__('Enter value...')"
                rows="3"
                required
              />
              
              <!-- Default: Data field -->
              <FormControl
                v-else
                type="text"
                v-model="localAction.field_value"
                :placeholder="__('Enter value...')"
                required
              />
              
              <p class="text-xs text-gray-500 mt-1">
                {{ __('This value will be set to the selected field') }}
              </p>
            </div>
          </div>

          <!-- ADD_TAG Action -->
          <div v-else-if="localAction.action_type === 'ADD_TAG'" class="space-y-4">
            <div class="bg-green-50 border border-green-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="plus-circle" class="h-4 w-4 text-green-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-green-900">
                    {{ __('Add Tag to Talent') }}
                  </p>
                  <p class="text-xs text-green-700">
                    {{ __('This action will add the selected tag to talent profile when triggered') }}
                  </p>
                </div>
              </div>
            </div>
            
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __('Select Tag to Add') }}
                <span class="text-red-500">*</span>
              </label>
              <Autocomplete
                v-model="selectedTagId"
                :options="tagOptions"
                :placeholder="__('Search and select tag to add...')"
              />
              <p class="text-xs text-gray-500 mt-1">
                {{ __('Choose the tag that will be added to talent') }}
              </p>
            </div>
            
            <!-- Show selected tag info -->
            <div v-if="selectedTag" class="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <div class="flex items-center space-x-2">
                <div 
                  class="w-4 h-4 rounded"
                  :style="{ backgroundColor: selectedTag.color || '#6B7280' }"
                ></div>
                <div class="flex-1">
                  <p class="text-sm font-medium text-gray-900">{{ selectedTag.title }}</p>
                  <p class="text-xs text-gray-500">{{ selectedTag.name }}</p>
                </div>
                <div class="text-xs text-green-600 font-medium">
                  {{ __('Will be added') }}
                </div>
              </div>
            </div>
          </div>

          <!-- REMOVE_TAG Action -->
          <div v-else-if="localAction.action_type === 'REMOVE_TAG'" class="space-y-4">
            <div class="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="minus-circle" class="h-4 w-4 text-red-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-red-900">
                    {{ __('Remove Tag from Talent') }}
                  </p>
                  <p class="text-xs text-red-700">
                    {{ __('This action will remove the selected tag from talent profile when triggered') }}
                  </p>
                </div>
              </div>
            </div>
            
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __('Select Tag to Remove') }}
                <span class="text-red-500">*</span>
              </label>
              <Autocomplete
                v-model="selectedTagId"
                :options="tagOptions"
                :placeholder="__('Search and select tag to remove...')"
              />
              <p class="text-xs text-gray-500 mt-1">
                {{ __('Choose the tag that will be removed from talent') }}
              </p>
            </div>
            
            <!-- Show selected tag info -->
            <div v-if="selectedTag" class="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <div class="flex items-center space-x-2">
                <div 
                  class="w-4 h-4 rounded"
                  :style="{ backgroundColor: selectedTag.color || '#6B7280' }"
                ></div>
                <div class="flex-1">
                  <p class="text-sm font-medium text-gray-900">{{ selectedTag.title }}</p>
                  <p class="text-xs text-gray-500">{{ selectedTag.name }}</p>
                </div>
                <div class="text-xs text-red-600 font-medium">
                  {{ __('Will be removed') }}
                </div>
              </div>
            </div>
          </div>

          <!-- EXTERNAL_REQUEST Action -->
          <div v-else-if="localAction.action_type === 'EXTERNAL_REQUEST'" class="space-y-4">
            <div class="bg-indigo-50 border border-indigo-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="bell" class="h-4 w-4 text-indigo-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-indigo-900">
                    {{ __('Send Internal Notification') }}
                  </p>
                  <p class="text-xs text-indigo-700">
                    {{ __('This action will send a notification to selected team members') }}
                  </p>
                </div>
              </div>
            </div>
            
            <FormControl
              type="text"
              :label="__('Notification Title')"
              v-model="localAction.notification_title"
              :placeholder="__('Enter notification title...')"
              required
            />
            
            <FormControl
              type="textarea"
              :label="__('Notification Message')"
              v-model="localAction.notification_message"
              :placeholder="__('Enter the message to send...')"
              rows="4"
              required
            />
            
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __('Recipients') }}
                <span class="text-red-500">*</span>
              </label>
              <Autocomplete
                v-model="selectedRecipients"
                :options="userOptions"
                :placeholder="__('Search and select users...')"
                multiple
              />
              <p class="text-xs text-gray-500 mt-1">
                {{ __('Select one or more users to receive this notification') }}
              </p>
            </div>
            
            <div v-if="recipientUsers.length > 0" class="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <p class="text-xs font-medium text-gray-700 mb-2">
                {{ __('Selected Recipients') }} ({{ recipientUsers.length }})
              </p>
              <div class="flex flex-wrap gap-2">
                <div v-for="user in recipientUsers" :key="user.name" 
                     class="flex items-center space-x-1 bg-white border border-gray-300 rounded-full px-2 py-1">
                  <div class="h-5 w-5 rounded-full bg-indigo-500 text-white flex items-center justify-center text-xs">
                    {{ user.full_name?.charAt(0) || 'U' }}
                  </div>
                  <span class="text-xs text-gray-900">{{ user.full_name || user.name }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- AI_CALL Action -->
          <div v-else-if="localAction.action_type === 'AI_CALL'" class="space-y-4">
            <FormControl
              type="text"
              :label="__('ATS System')"
              v-model="localAction.ats_system"
              :placeholder="__('Enter ATS system name...')"
              required
            />
            <FormControl
              type="textarea"
              :label="__('Handoff Data (JSON)')"
              v-model="localAction.handoff_data"
              :placeholder="__('Enter handoff data as JSON...')"
              rows="4"
            />
          </div>

          <!-- FACEBOOK Action -->
          <div v-else-if="localAction.action_type === 'FACEBOOK'" class="space-y-4">
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="facebook" class="h-4 w-4 text-blue-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-blue-900">
                    {{ __('Send Facebook Message') }}
                  </p>
                  <p class="text-xs text-blue-700">
                    {{ __('This action will send a message via Facebook Messenger') }}
                  </p>
                </div>
              </div>
            </div>
            
            <MessengerContentEditor
              :content="localAction.content || { blocks: [] }"
              @update:content="localAction.content = $event"
            />
          </div>

          <!-- SMS Action -->
          <div v-else-if="localAction.action_type === 'SMS'" class="space-y-4">
            <div class="bg-green-50 border border-green-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="smartphone" class="h-4 w-4 text-green-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-green-900">
                    {{ __('Send SMS') }}
                  </p>
                  <p class="text-xs text-green-700">
                    {{ __('This action will send an SMS message to talent') }}
                  </p>
                </div>
              </div>
            </div>
            
            <FormControl
              type="textarea"
              :label="__('SMS Message')"
              v-model="localAction.content"
              :placeholder="__('Enter SMS message...')"
              rows="4"
              :maxlength="160"
              required
            />
            <div class="flex justify-between items-center mt-2">
              <p class="text-xs text-gray-500">
                {{ __('Keep it short and clear (max 160 characters)') }}
              </p>
              <span class="text-xs text-gray-500">
                {{ (localAction.content?.length || 0) }}/160
              </span>
            </div>
          </div>

          <!-- ZALO Action -->
          <div v-else-if="localAction.action_type === 'ZALO'" class="space-y-4">
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="message-square" class="h-4 w-4 text-blue-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-blue-900">
                    {{ __('Send Zalo Message') }}
                  </p>
                  <p class="text-xs text-blue-700">
                    {{ __('This action will send a message via Zalo') }}
                  </p>
                </div>
              </div>
            </div>
            
            <ZaloContentEditor
              :content="localAction.content || { blocks: [] }"
              @update:content="localAction.content = $event"
            />
          </div>

          <!-- INTERNAL_NOTIFICATION Action -->
          <div v-else-if="localAction.action_type === 'INTERNAL_NOTIFICATION'" class="space-y-4">
            <div class="bg-purple-50 border border-purple-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="bell-ring" class="h-4 w-4 text-purple-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-purple-900">
                    {{ __('Send Internal Notification') }}
                  </p>
                  <p class="text-xs text-purple-700">
                    {{ __('This action will send a notification to team members') }}
                  </p>
                </div>
              </div>
            </div>
            
            <FormControl
              type="text"
              :label="__('Notification Title')"
              v-model="localAction.notification_title"
              :placeholder="__('Enter notification title...')"
              required
            />
            
            <FormControl
              type="textarea"
              :label="__('Notification Message')"
              v-model="localAction.notification_message"
              :placeholder="__('Enter the message...')"
              rows="4"
              required
            />
            
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __('Recipients') }}
                <span class="text-red-500">*</span>
              </label>
              <Autocomplete
                v-model="selectedRecipients"
                :options="userOptions"
                :placeholder="__('Search and select users...')"
                multiple
              />
              <p class="text-xs text-gray-500 mt-1">
                {{ __('Select one or more users to receive this notification') }}
              </p>
            </div>
            
            <div v-if="recipientUsers.length > 0" class="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <p class="text-xs font-medium text-gray-700 mb-2">
                {{ __('Selected Recipients') }} ({{ recipientUsers.length }})
              </p>
              <div class="flex flex-wrap gap-2">
                <div v-for="user in recipientUsers" :key="user.name" 
                     class="flex items-center space-x-1 bg-white border border-gray-300 rounded-full px-2 py-1">
                  <div class="h-5 w-5 rounded-full bg-purple-500 text-white flex items-center justify-center text-xs">
                    {{ user.full_name?.charAt(0) || 'U' }}
                  </div>
                  <span class="text-xs text-gray-900">{{ user.full_name || user.name }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- SMART_DELAY Action -->
          <div v-else-if="localAction.action_type === 'SMART_DELAY'" class="space-y-4">
            <div class="bg-indigo-50 border border-indigo-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="clock" class="h-4 w-4 text-indigo-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-indigo-900">
                    {{ __('Smart Delay') }}
                  </p>
                  <p class="text-xs text-indigo-700">
                    {{ __('Intelligently delay next action based on talent behavior') }}
                  </p>
                </div>
              </div>
            </div>
            
            <FormControl
              type="number"
              :label="__('Delay Duration (minutes)')"
              v-model="localAction.delay_duration"
              :placeholder="__('Enter delay in minutes...')"
              required
            />
            
            <FormControl
              type="select"
              :label="__('Delay Type')"
              v-model="localAction.delay_type"
              :options="[
                { label: __('Fixed Delay'), value: 'fixed' },
                { label: __('Smart Delay'), value: 'smart' },
                { label: __('Wait Until Time'), value: 'wait_until' }
              ]"
            />
          </div>

          <!-- REMOVE_CUSTOM_FIELD Action -->
          <div v-else-if="localAction.action_type === 'REMOVE_CUSTOM_FIELD'" class="space-y-4">
            <div class="bg-orange-50 border border-orange-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="minus-square" class="h-4 w-4 text-orange-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-orange-900">
                    {{ __('Remove Custom Field') }}
                  </p>
                  <p class="text-xs text-orange-700">
                    {{ __('Remove a custom field from talent profile') }}
                  </p>
                </div>
              </div>
            </div>
            
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __('Select Field to Remove') }}
                <span class="text-red-500">*</span>
              </label>
              <Autocomplete
                v-model="selectedFieldName"
                :options="talentFieldOptions"
                :placeholder="__('Search and select field...')"
              />
              <p class="text-xs text-gray-500 mt-1">
                {{ __('Choose which field to remove from talent profile') }}
              </p>
            </div>
          </div>

          <!-- SENT_NOTIFICATION Action -->
          <div v-else-if="localAction.action_type === 'SENT_NOTIFICATION'" class="space-y-4">
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="bell" class="h-4 w-4 text-blue-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-blue-900">
                    {{ __('Send Notification') }}
                  </p>
                  <p class="text-xs text-blue-700">
                    {{ __('Send a notification to users or talent') }}
                  </p>
                </div>
              </div>
            </div>
            
            <FormControl
              type="text"
              :label="__('Notification Title')"
              v-model="localAction.notification_title"
              :placeholder="__('Enter notification title...')"
              required
            />
            
            <FormControl
              type="textarea"
              :label="__('Notification Message')"
              v-model="localAction.notification_message"
              :placeholder="__('Enter notification message...')"
              rows="4"
              required
            />
          </div>

          <!-- UPDATE_FIELD_VALUE Action -->
          <div v-else-if="localAction.action_type === 'UPDATE_FIELD_VALUE'" class="space-y-4">
            <div class="bg-purple-50 border border-purple-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="edit" class="h-4 w-4 text-purple-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-purple-900">
                    {{ __('Update Field Value') }}
                  </p>
                  <p class="text-xs text-purple-700">
                    {{ __('Update a specific field value in talent profile') }}
                  </p>
                </div>
              </div>
            </div>
            
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __('Select Field') }}
                <span class="text-red-500">*</span>
              </label>
              <Autocomplete
                v-model="selectedFieldName"
                :options="talentFieldOptions"
                :placeholder="__('Search and select field...')"
              />
            </div>
            
            <FormControl
              type="text"
              :label="__('New Value')"
              v-model="localAction.field_value"
              :placeholder="__('Enter new value...')"
              required
            />
          </div>

          <!-- CHANGE_STATUS Action -->
          <div v-else-if="localAction.action_type === 'CHANGE_STATUS'" class="space-y-4">
            <div class="bg-green-50 border border-green-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="toggle-right" class="h-4 w-4 text-green-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-green-900">
                    {{ __('Change Status') }}
                  </p>
                  <p class="text-xs text-green-700">
                    {{ __('Change talent status (Active, Paused, Completed, Cancelled)') }}
                  </p>
                </div>
              </div>
            </div>
            
            <FormControl
              type="select"
              :label="__('New Status')"
              v-model="localAction.new_status"
              :options="[
                { label: __('Active'), value: 'ACTIVE' },
                { label: __('Paused'), value: 'PAUSED' },
                { label: __('Completed'), value: 'COMPLETED' },
                { label: __('Cancelled'), value: 'CANCELLED' }
              ]"
              required
            />
            
            <FormControl
              type="textarea"
              :label="__('Reason (Optional)')"
              v-model="localAction.status_reason"
              :placeholder="__('Enter reason for status change...')"
              rows="2"
            />
          </div>

          <!-- STOP_TRACKING Action -->
          <div v-else-if="localAction.action_type === 'STOP_TRACKING'" class="space-y-4">
            <div class="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="user-minus" class="h-4 w-4 text-red-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-red-900">
                    {{ __('Stop Tracking') }}
                  </p>
                  <p class="text-xs text-red-700">
                    {{ __('Stop tracking this talent in the system') }}
                  </p>
                </div>
              </div>
            </div>
            
            <FormControl
              type="textarea"
              :label="__('Reason (Optional)')"
              v-model="localAction.stop_reason"
              :placeholder="__('Enter reason for stopping tracking...')"
              rows="2"
            />
            
            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
              <div class="flex items-start">
                <FeatherIcon name="alert-triangle" class="h-4 w-4 text-yellow-600 mt-0.5 mr-2" />
                <p class="text-xs text-yellow-800">
                  {{ __('Warning: This will permanently stop tracking this talent. This action cannot be undone.') }}
                </p>
              </div>
            </div>
          </div>

          <!-- HANDOFF_TO_ATS Action -->
          <div v-else-if="localAction.action_type === 'HANDOFF_TO_ATS'" class="space-y-4">
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="send" class="h-4 w-4 text-blue-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-blue-900">
                    {{ __('Handoff to ATS') }}
                  </p>
                  <p class="text-xs text-blue-700">
                    {{ __('Transfer talent to ATS system for recruitment process') }}
                  </p>
                </div>
              </div>
            </div>
            
            <FormControl
              type="text"
              :label="__('ATS System')"
              v-model="localAction.ats_system"
              :placeholder="__('Enter ATS system name...')"
              required
            />
            
            <FormControl
              type="textarea"
              :label="__('Transfer Notes')"
              v-model="localAction.transfer_notes"
              :placeholder="__('Enter notes for ATS team...')"
              rows="3"
            />
            
            <FormControl
              type="textarea"
              :label="__('Handoff Data (JSON)')"
              v-model="localAction.handoff_data"
              :placeholder="__('Enter additional data as JSON...')"
              rows="4"
            />
          </div>

          <!-- UNSUBSCRIBE Action -->
          <div v-else-if="localAction.action_type === 'UNSUBSCRIBE'" class="space-y-4">
            <div class="bg-gray-50 border border-gray-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="user-x" class="h-4 w-4 text-gray-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-gray-900">
                    {{ __('Unsubscribe') }}
                  </p>
                  <p class="text-xs text-gray-700">
                    {{ __('Unsubscribe talent from campaign communications') }}
                  </p>
                </div>
              </div>
            </div>
            
            <FormControl
              type="textarea"
              :label="__('Unsubscribe Reason (Optional)')"
              v-model="localAction.unsubscribe_reason"
              :placeholder="__('Enter unsubscribe reason...')"
              rows="2"
            />
          </div>

          <!-- Default fallback for other action types -->
          <div v-else class="space-y-4">
            <div class="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <p class="text-sm text-gray-700">
                {{ __('Configuration for this action type will be available soon.') }}
              </p>
            </div>
          </div>
        </div>

        <!-- Delay Configuration -->
        <div class="pt-4 border-t border-gray-200">
          <DelaySelector
            v-model="localAction.delay_minutes"
            :label="__('Delay')"
            :optional="true"
          />
        </div>
      </div>
    </template>

    <template #actions>
      <div class="flex justify-end space-x-2">
        <Button variant="outline" @click="cancel">
          {{ __('Cancel') }}
        </Button>
        <Button variant="solid" theme="blue" @click="save">
          {{ __('Save Action') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { FeatherIcon, Button, FormControl, Dialog, Autocomplete, call } from 'frappe-ui'
import DelaySelector from './DelaySelector.vue'
import ZaloContentEditor from './ZaloContentEditor.vue'
import MessengerContentEditor from './MessengerContentEditor.vue'
import EmailContentEditor from './EmailContentEditor.vue'
import { allActionTypes, actionIcons, actionDescriptions } from '../../../config/campaigns/commonConfig'
import { convertEmailBuilderToHtml } from '@/utils/emailBuilderConverter.js'
import { getDefaultEmailTemplate, getDefaultEmailTemplateCss } from '@/utils/emailTemplates'


// Helper: detect old "email-default-css" wrapper CSS that should NOT be used as css_content
const isLegacyWrapperCss = (css) => {
  if (!css || typeof css !== 'string') return false
  const trimmed = css.trim()
  if (!trimmed) return false
  // Heuristic: legacy wrapper CSS always contains these snippets
  return trimmed.includes('background-color: #f4f4f4; color: #111111; font-family: Arial, sans-serif;')
    && trimmed.includes('table { border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; }')
}

// Helper: strip <style id="email-default-css">...</style> from HTML template_content
const stripEmailDefaultStyleTag = (html) => {
  if (!html || typeof html !== 'string') return html
  try {
    return html.replace(/<style[^>]*id=["']email-default-css["'][^>]*>[\s\S]*?<\/style>/i, '').trim()
  } catch (e) {
    return html
  }
}

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  action: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:show', 'save', 'cancel'])

// Local state
const localShow = computed({
  get: () => props.show,
  set: (value) => emit('update:show', value)
})

const localAction = ref({})

// Tags state
const tags = ref([])
const loadingTags = ref(false)

// Talent fields state
const talentFields = ref([])
const loadingTalentFields = ref(false)

// Flows state
const flows = ref([])
const loadingFlows = ref(false)

// Users state
const users = ref([])
const loadingUsers = ref(false)

// Email Accounts state
const emailAccounts = ref([])
const loadingEmailAccounts = ref(false)

// Computed tag options for Autocomplete
const tagOptions = computed(() => {
  return tags.value.map(tag => ({
    label: tag.title,
    value: tag.name,
    description: tag.name,
    color: tag.color
  }))
})

// Selected tag for Autocomplete v-model
const selectedTagId = computed({
  get: () => {
    // Return the tag_id string for Autocomplete
    return localAction.value.tag_id
  },
  set: (value) => {
    // Handle when Autocomplete sets value
    handleTagSelect(value)
  }
})

// Selected tag info
const selectedTag = computed(() => {
  if (!localAction.value.tag_id) return null
  const tagId = typeof localAction.value.tag_id === 'object' ? localAction.value.tag_id.value : localAction.value.tag_id
  return tags.value.find(tag => tag.name === tagId)
})

// Email content object for EmailContentEditor
const emailContent = computed(() => ({
  email_subject: localAction.value.email_subject || '',
  email_content: localAction.value.email_content || localAction.value.content || '',  // Legacy field
  block_content: localAction.value.block_content || '',        // EmailBuilder format
  // IMPORTANT: strip legacy <style id="email-default-css"> from HTML before sending to EmailBuilder
  template_content: stripEmailDefaultStyleTag(
    localAction.value.template_content || getDefaultEmailTemplate().trim()
  ),
  mjml_content: localAction.value.mjml_content || '',          // MJML format
  // css_content: ignore legacy wrapper CSS; let EmailBuilder manage real block CSS (like Step2)
  css_content: isLegacyWrapperCss(localAction.value.css_content)
    ? ''
    : (localAction.value.css_content || ''),
  attachments: localAction.value.attachments || [],
  sender_account: localAction.value.sender_account || null
}))

// Helper: extract CSS inside <style>...</style> from an HTML string
const extractCssFromHtml = (html) => {
  if (!html || typeof html !== 'string') return ''
  try {
    const match = html.match(/<style[^>]*>([\s\S]*?)<\/style>/i)
    if (match && match[1]) {
      return match[1].trim()
    }
  } catch (e) {
    // ignore parse errors
  }
  return ''
}

// Handle email content update from EmailContentEditor
const handleEmailContentUpdate = (content) => {
  console.log('📧 [ActionEditor] Email content updated:', content)
  console.log('📧 [ActionEditor] CSS content in update:', {
    hasCss: !!content.css_content,
    cssLength: content.css_content?.length || 0,
    cssPreview: content.css_content?.substring(0, 100) + '...'
  })
  
  // Save all content formats
  localAction.value.email_subject = content.email_subject
  localAction.value.email_content = content.email_content        // Legacy field
  localAction.value.block_content = content.block_content        // EmailBuilder format
  localAction.value.template_content = content.template_content  // HTML format
  localAction.value.mjml_content = content.mjml_content          // MJML format
  localAction.value.css_content = content.css_content || ''      // CSS content for styling
  localAction.value.attachments = content.attachments
  localAction.value.sender_account = content.sender_account
  
  console.log('📧 [ActionEditor] Updated action fields:', {
    email_subject: localAction.value.email_subject,
    block_content: localAction.value.block_content?.substring(0, 100) + '...',
    template_content: localAction.value.template_content?.substring(0, 100) + '...',
    mjml_content: localAction.value.mjml_content?.substring(0, 100) + '...',
    css_content: localAction.value.css_content?.substring(0, 100) + '...',
    cssLength: localAction.value.css_content?.length || 0
  })
}

// Computed talent field options for Autocomplete
const talentFieldOptions = computed(() => {
  return talentFields.value
    .filter(field => {
      // Filter out system fields and child tables
      return !field.fieldname.startsWith('_') && 
             !['Table', 'Section Break', 'Column Break', 'HTML', 'Button'].includes(field.fieldtype)
    })
    .map(field => ({
      label: field.label,
      value: field.fieldname,
      description: field.fieldtype,
      fieldtype: field.fieldtype
    }))
})

// Selected field for ADD_CUSTOM_FIELD
const selectedFieldName = computed({
  get: () => localAction.value.field_name,
  set: (value) => {
    // If value is object from Autocomplete, extract fieldname
    const fieldname = typeof value === 'object' ? value.value : value
    localAction.value.field_name = fieldname
    
    // Find field metadata
    const field = talentFields.value.find(f => f.fieldname === fieldname)
    if (field) {
      console.log('📝 Field selected:', field)
    }
  }
})

// Get selected field metadata
const selectedField = computed(() => {
  if (!localAction.value.field_name) return null
  const fieldname = typeof localAction.value.field_name === 'object' 
    ? localAction.value.field_name.value 
    : localAction.value.field_name
  return talentFields.value.find(f => f.fieldname === fieldname)
})

// Helper to parse Select field options
const getSelectOptions = (optionsString) => {
  if (!optionsString) return []
  const lines = optionsString.split('\n').filter(line => line.trim())
  return lines.map(line => ({
    label: line.trim(),
    value: line.trim()
  }))
}

// Computed flow options for Autocomplete
const flowOptions = computed(() => {
  return flows.value.map(flow => ({
    label: flow.title || flow.name,
    value: flow.name,
    description: `${flow.type || 'Flow'} - ${flow.status || 'Unknown'}`,
    status: flow.status,
    type: flow.type
  }))
})

// Selected flow for START_FLOW/STOP_FLOW
const selectedFlowId = computed({
  get: () => localAction.value.flow_id,
  set: (value) => {
    // If value is object from Autocomplete, extract flow ID
    const flowId = typeof value === 'object' ? value.value : value
    localAction.value.flow_id = flowId
    
    // Find flow metadata
    const flow = flows.value.find(f => f.name === flowId)
    if (flow) {
      console.log('🔄 Flow selected:', flow)
    }
  }
})

// Get selected flow metadata
const selectedFlow = computed(() => {
  if (!localAction.value.flow_id) return null
  const flowId = typeof localAction.value.flow_id === 'object' 
    ? localAction.value.flow_id.value 
    : localAction.value.flow_id
  return flows.value.find(f => f.name === flowId)
})

// Computed user options for Autocomplete
const userOptions = computed(() => {
  return users.value.map(user => ({
    label: user.full_name || user.name,
    value: user.name,
    description: user.email || user.name,
    full_name: user.full_name,
    email: user.email
  }))
})

// Computed email account options for Autocomplete
const emailAccountOptions = computed(() => {
  return emailAccounts.value.map(account => ({
    label: account.email_account_name || account.name,
    value: account.name,
    description: account.email_id || account.name
  }))
})

// Selected sender account for EMAIL action
const selectedSenderAccount = computed({
  get: () => localAction.value.sender_account,
  set: (value) => {
    const accountId = typeof value === 'object' ? value.value : value
    localAction.value.sender_account = accountId
    console.log('📧 Sender account selected:', accountId)
  }
})

// Selected assignee for SENT_NOTIFICATION (single user)
const selectedAssignee = computed({
  get: () => localAction.value.assignee,
  set: (value) => {
    const userId = typeof value === 'object' ? value.value : value
    localAction.value.assignee = userId
    
    const user = users.value.find(u => u.name === userId)
    if (user) {
      console.log('👤 Assignee selected:', user)
    }
  }
})

// Get selected assignee user metadata
const selectedAssigneeUser = computed(() => {
  if (!localAction.value.assignee) return null
  const userId = typeof localAction.value.assignee === 'object' 
    ? localAction.value.assignee.value 
    : localAction.value.assignee
  return users.value.find(u => u.name === userId)
})

// Selected recipients for EXTERNAL_REQUEST (multiple users)
const selectedRecipients = computed({
  get: () => {
    // Parse recipients if it's a string (comma-separated)
    if (typeof localAction.value.recipients === 'string') {
      return localAction.value.recipients.split(',').map(r => r.trim()).filter(Boolean)
    }
    // If it's already an array
    return localAction.value.recipients || []
  },
  set: (value) => {
    // Value can be array of user IDs or array of objects
    let userIds = []
    if (Array.isArray(value)) {
      userIds = value.map(v => typeof v === 'object' ? v.value : v)
    } else if (value) {
      userIds = [typeof value === 'object' ? value.value : value]
    }
    
    // Store as comma-separated string
    localAction.value.recipients = userIds.join(',')
    console.log('👥 Recipients selected:', userIds)
  }
})

// Get selected recipient users metadata
const recipientUsers = computed(() => {
  const recipients = selectedRecipients.value
  if (!recipients || recipients.length === 0) return []
  
  return recipients.map(userId => {
    return users.value.find(u => u.name === userId)
  }).filter(Boolean)
})

// Load tags from API
const loadTags = async () => {
  try {
    loadingTags.value = true
    const result = await call('frappe.client.get_list', {
      doctype: 'Mira Tag',
      fields: ['name', 'title', 'color', 'order'],
      order_by: '`order` asc',
      limit_page_length: 0
    })
    
    if (result) {
      tags.value = result
      console.log('✅ Loaded tags:', tags.value)
    }
  } catch (error) {
    console.error('❌ Error loading tags:', error)
  } finally {
    loadingTags.value = false
  }
}

// Handle tag selection
const handleTagSelect = (selectedValue) => {
  console.log('🏷️ Tag selected:', selectedValue)
  
  // If selectedValue is an object (from Autocomplete), extract the value
  const tagName = typeof selectedValue === 'object' ? selectedValue.value : selectedValue
  
  const tag = tags.value.find(t => t.name === tagName)
  if (tag) {
    localAction.value.tag_id = tag.name      // Store only the tag name (ID)
    localAction.value.tag_name = tag.title
    localAction.value.tag_color = tag.color
    console.log('✅ Tag data set:', { tag_id: tag.name, tag_name: tag.title, tag_color: tag.color })
  }
}

// Load Mira Talent fields from doctype metadata
const loadTalentFields = async () => {
  try {
    loadingTalentFields.value = true
    const result = await call('frappe.client.get', {
      doctype: 'DocType',
      name: 'Mira Talent'
    })
    
    if (result && result.fields) {
      talentFields.value = result.fields
      console.log('✅ Loaded Mira Talent fields:', talentFields.value.length)
    }
  } catch (error) {
    console.error('❌ Error loading Mira Talent fields:', error)
  } finally {
    loadingTalentFields.value = false
  }
}

// Load Mira Flows from API
const loadFlows = async () => {
  try {
    loadingFlows.value = true
    const result = await call('frappe.client.get_list', {
      doctype: 'Mira Flow',
      fields: ['name', 'title', 'description', 'status', 'type', 'campaign_id'],
      filters: [['status', '!=', 'Archived']],
      order_by: 'modified desc',
      limit_page_length: 100
    })
    
    if (result) {
      flows.value = result
      console.log('✅ Loaded flows:', flows.value.length)
    }
  } catch (error) {
    console.error('❌ Error loading flows:', error)
  } finally {
    loadingFlows.value = false
  }
}

// Load system users from API
const loadUsers = async () => {
  try {
    loadingUsers.value = true
    const result = await call('frappe.client.get_list', {
      doctype: 'User',
      fields: ['name', 'full_name', 'email', 'user_image'],
      filters: [['enabled', '=', 1]],
      order_by: 'full_name asc',
      limit_page_length: 0
    })
    
    if (result) {
      users.value = result
      console.log('✅ Loaded users:', users.value.length)
    }
  } catch (error) {
    console.error('❌ Error loading users:', error)
  } finally {
    loadingUsers.value = false
  }
}

// Load email accounts from API
const loadEmailAccounts = async () => {
  try {
    loadingEmailAccounts.value = true
    const result = await call('frappe.client.get_list', {
      doctype: 'Email Account',
      fields: ['name', 'email_account_name', 'email_id', 'enable_outgoing'],
      filters: [['enable_outgoing', '=', 1]],
      order_by: 'email_account_name asc',
      limit_page_length: 0
    })
    
    if (result) {
      emailAccounts.value = result
      console.log('✅ Loaded email accounts:', emailAccounts.value.length)
    }
  } catch (error) {
    console.error('❌ Error loading email accounts:', error)
  } finally {
    loadingEmailAccounts.value = false
  }
}

// Load tags on mount
onMounted(() => {
  loadTags()
  loadTalentFields()
  loadFlows()
  loadUsers()
  loadEmailAccounts()
})

// Watch for action changes
watch(() => props.action, (newAction) => {
  console.log('👀 ActionEditor received action prop:', newAction)
  if (newAction) {
    localAction.value = { ...newAction }
    
    // If action is EMAIL, seed default HTML only when really empty.
    // CSS will be managed by EmailEditor/EmailBuilder (getCss) like in Step2.
    if (localAction.value.action_type === 'EMAIL') {
      const hasTemplate = localAction.value.template_content && localAction.value.template_content.trim() !== ''
      const hasBlock = localAction.value.block_content && localAction.value.block_content.trim() !== ''
      if (!hasTemplate && !hasBlock) {
        localAction.value.template_content = getDefaultEmailTemplate().trim()
        localAction.value.css_content = ''
        console.log('🎨 [ActionEditor] Seeded default email template HTML for empty EMAIL action (no css_content)')
      }
    }
    
    // Unpack action_parameters into top-level fields for form binding
    if (newAction.action_parameters) {
      const params = typeof newAction.action_parameters === 'string'
        ? JSON.parse(newAction.action_parameters)
        : newAction.action_parameters
      
      // Merge parameters into localAction for easier form binding
      Object.assign(localAction.value, params)
      
      // Ensure EMAIL still has css_content after params merge
      if (localAction.value.action_type === 'EMAIL') {
        if (!localAction.value.css_content || !localAction.value.css_content.trim()) {
          localAction.value.css_content = getDefaultEmailTemplateCss()
          console.log('🎨 [ActionEditor] Applied default CSS after params merge')
        }
      }

      console.log('📦 Unpacked action_parameters:', params)
    }
    
    console.log('📝 ActionEditor localAction set to:', localAction.value)
    
    // Log tag-specific fields for debugging
    if (newAction.action_type === 'ADD_TAG' || newAction.action_type === 'REMOVE_TAG') {
      console.log('🏷️ Tag fields:', {
        tag_id: localAction.value.tag_id,
        tag_name: localAction.value.tag_name,
        tag_color: localAction.value.tag_color
      })
    }
  }
}, { immediate: true, deep: true })

// Action type options - Imported from commonConfig (9 action types based on documentation)
const actionTypeOptions = allActionTypes

const channelOptions = [
  { label: __('Email'), value: 'Email' },
  { label: __('SMS'), value: 'SMS' },
  { label: __('Zalo'), value: 'Zalo' },
  { label: __('Messenger'), value: 'Messenger' }
]

const messageChannelOptions = [
  { label: __('Zalo'), value: 'Zalo' },
  { label: __('SMS'), value: 'SMS' }
]

// Helper functions - Using imported config from commonConfig
const getActionIcon = (actionType) => {
  return actionIcons[actionType] || 'zap'
}

const getActionLabel = (actionType) => {
  const action = actionTypeOptions.find(a => a.value === actionType)
  return action ? action.label : actionType
}

const getActionDescription = (actionType) => {
  return actionDescriptions[actionType] || ''
}

const needsChannelForAction = (actionType) => {
  return ['EMAIL', 'MESSAGE'].includes(actionType)
}

const handleActionTypeChange = () => {
  // Reset action-specific fields when type changes
  const actionType = localAction.value.action_type
  
  // Clear previous fields
  delete localAction.value.email_subject
  delete localAction.value.email_content
  delete localAction.value.attachments
  delete localAction.value.sender_account
  delete localAction.value.field_name
  delete localAction.value.field_value
  delete localAction.value.field_type
  delete localAction.value.field_label
  delete localAction.value.tag_id
  delete localAction.value.tag_name
  delete localAction.value.tag_color
  delete localAction.value.flow_id
  delete localAction.value.flow_title
  delete localAction.value.flow_type
  delete localAction.value.flow_status
  delete localAction.value.flow_parameters
  delete localAction.value.task_title
  delete localAction.value.task_subject
  delete localAction.value.task_description
  delete localAction.value.task_priority
  delete localAction.value.task_due_date
  delete localAction.value.assignee
  delete localAction.value.assignee_name
  delete localAction.value.assignee_email
  delete localAction.value.notification_title
  delete localAction.value.notification_message
  delete localAction.value.recipients
  delete localAction.value.recipient_names
  delete localAction.value.recipient_count
  delete localAction.value.ats_system
  delete localAction.value.handoff_data
  delete localAction.value.unsubscribe_reason
  
  // Set default channel based on action type
  if (actionType === 'EMAIL') {
    localAction.value.channel_type = 'Email'
    // Seed default template when switching to EMAIL without existing content
    const hasTemplate = localAction.value.template_content && localAction.value.template_content.trim() !== ''
    const hasBlock = localAction.value.block_content && localAction.value.block_content.trim() !== ''
    if (!hasTemplate && !hasBlock) {
      localAction.value.template_content = getDefaultEmailTemplate()
      localAction.value.css_content = ''
      localAction.value.email_content = ''
      localAction.value.block_content = ''
    }
  } else if (actionType === 'MESSAGE') {
    localAction.value.channel_type = 'Zalo'
  }
}

// Methods
const save = async () => {
  // Build action parameters based on action type
  const actionParams = {}
  
  switch (localAction.value.action_type) {
    case 'EMAIL':
      actionParams.email_subject = localAction.value.email_subject
      actionParams.block_content = localAction.value.block_content        // EmailBuilder format
      actionParams.template_content = localAction.value.template_content  // HTML format
      actionParams.mjml_content = localAction.value.mjml_content          // MJML format
      actionParams.css_content = localAction.value.css_content || ''      // CSS content for styling
      actionParams.attachments = localAction.value.attachments || []
      actionParams.sender_account = localAction.value.sender_account || null
      
      // Convert block_content to HTML for email_content (for backward compatibility and email sending)
      if (localAction.value.block_content) {
        try {
          const design = JSON.parse(localAction.value.block_content)
          
          // Force left alignment as per user request to match CampaignTable behavior
          // Ensure emailSettings exists before setting contentAlign
          if (!design.emailSettings) {
            design.emailSettings = {
              backgroundColor: '#ffffff',
              contentWidth: 600,
              contentAlign: 'left',
              fontFamily: 'Arial, sans-serif'
            }
          } else {
            design.emailSettings.contentAlign = 'left'
          }
          
          const htmlFormat = convertEmailBuilderToHtml(design)
          actionParams.email_content = htmlFormat.html  // Converted HTML
          console.log('📧 [ActionEditor] Converted block_content to HTML for email_content with left alignment')
        } catch (e) {
          console.warn('Failed to convert block_content to HTML:', e)
          actionParams.email_content = localAction.value.email_content || ''  // Fallback
        }
      } else {
        actionParams.email_content = localAction.value.email_content || ''  // Legacy field
      }
      break
    case 'MESSAGE':
      actionParams.channel = localAction.value.channel_type
      actionParams.content = localAction.value.content
      break
    case 'ADD_CUSTOM_FIELD':
      actionParams.field_name = localAction.value.field_name
      actionParams.field_value = localAction.value.field_value
      // Include field type and label for backend validation
      if (selectedField.value) {
        actionParams.field_type = selectedField.value.fieldtype
        actionParams.field_label = selectedField.value.label
      }
      break
    case 'ADD_TAG':
    case 'REMOVE_TAG':
      actionParams.tag_id = localAction.value.tag_id
      actionParams.tag_name = localAction.value.tag_name
      actionParams.tag_color = localAction.value.tag_color
      break
    case 'START_FLOW':
    case 'STOP_FLOW':
      actionParams.flow_id = localAction.value.flow_id
      // Include flow metadata for reference
      if (selectedFlow.value) {
        actionParams.flow_title = selectedFlow.value.title
        actionParams.flow_type = selectedFlow.value.type
        actionParams.flow_status = selectedFlow.value.status
      }
      break
    case 'SENT_NOTIFICATION':
      actionParams.task_subject = localAction.value.task_subject
      actionParams.task_description = localAction.value.task_description
      actionParams.assignee = localAction.value.assignee
      actionParams.task_priority = localAction.value.task_priority
      actionParams.task_due_date = localAction.value.task_due_date
      // Include assignee metadata for display
      if (selectedAssigneeUser.value) {
        actionParams.assignee_name = selectedAssigneeUser.value.full_name
        actionParams.assignee_email = selectedAssigneeUser.value.email
      }
      break
    case 'EXTERNAL_REQUEST':
      actionParams.notification_title = localAction.value.notification_title
      actionParams.notification_message = localAction.value.notification_message
      actionParams.recipients = localAction.value.recipients
      // Include recipients metadata for display
      if (recipientUsers.value.length > 0) {
        actionParams.recipient_names = recipientUsers.value.map(u => u.full_name || u.name).join(', ')
        actionParams.recipient_count = recipientUsers.value.length
      }
      break
    case 'AI_CALL':
      actionParams.ats_system = localAction.value.ats_system
      actionParams.handoff_data = localAction.value.handoff_data
      break
    case 'UNSUBSCRIBE':
      actionParams.unsubscribe_reason = localAction.value.unsubscribe_reason
      break
    case 'UPDATE_FIELD_VALUE':
      actionParams.field_name = localAction.value.field_name
      actionParams.field_value = localAction.value.field_value
      // Include field type and label for backend validation
      if (selectedField.value) {
        actionParams.field_type = selectedField.value.fieldtype
        actionParams.field_label = selectedField.value.label
      }
      break
    case 'CHANGE_STATUS':
      actionParams.new_status = localAction.value.new_status
      actionParams.status_reason = localAction.value.status_reason
      break
    case 'STOP_TRACKING':
      actionParams.stop_reason = localAction.value.stop_reason
      break
    case 'INTERNAL_NOTIFICATION':
      actionParams.notification_title = localAction.value.notification_title
      actionParams.notification_message = localAction.value.notification_message
      actionParams.recipients = localAction.value.recipients || selectedRecipients.value
      // Include recipients metadata for display
      if (recipientUsers.value && recipientUsers.value.length > 0) {
        actionParams.recipient_names = recipientUsers.value.map(u => u.full_name || u.name).join(', ')
        actionParams.recipient_count = recipientUsers.value.length
      }
      break
    case 'HANDOFF_TO_ATS':
      actionParams.ats_system = localAction.value.ats_system
      actionParams.transfer_notes = localAction.value.transfer_notes
      actionParams.handoff_data = localAction.value.handoff_data
      break
  }
  
  // Set action parameters
  localAction.value.action_parameters = actionParams

  // INTEGRATED TEST EMAIL LOGIC (User request)
  // No prompt here anymore (User request: auto-send on save handled by parent or backend)
  
  console.log('📤 ActionEditor saving action:', localAction.value)
  
  console.log('📤 ActionEditor emitting save:', {
    action_type: localAction.value.action_type,
    action_parameters: actionParams,
    full_action: localAction.value
  })
  
  emit('save', { ...localAction.value })
}

const cancel = () => {
  emit('cancel')
}

const sendTestEmail = async () => {
  if (localAction.value.action_type !== 'EMAIL') return

  const subject = localAction.value.email_subject || 'Test Email'
  // Build content similarly to save()
  let content = ''
  if (localAction.value.block_content) {
    try {
      const design = JSON.parse(localAction.value.block_content)
      
      // Force left alignment (same as save())
      if (!design.emailSettings) {
        design.emailSettings = {
          backgroundColor: '#ffffff',
          contentWidth: 600,
          contentAlign: 'left',
          fontFamily: 'Arial, sans-serif'
        }
      } else {
        design.emailSettings.contentAlign = 'left'
      }
      
      const htmlFormat = convertEmailBuilderToHtml(design)
      content = htmlFormat.html
    } catch (e) {
      content = localAction.value.email_content || ''
    }
  } else {
    content = localAction.value.email_content || ''
  }

  if (!content) {
    // try fallback or show error
    console.warn('No content to send')
  }

  // Ask for recipient
  const userEmail = window.frappe?.session?.user_email || ''
  const recipient = prompt(__('Enter email address to send test to:'), userEmail)
  if (!recipient) return

  try {
    const res = await call('mbw_mira.api.campaign.send_test_email', {
      recipient,
      subject,
      content
    })
    if (res.status === 'success') {
      // Use frappe-ui toast if possible or console/alert
      alert(res.message)
    } else {
      alert(res.message)
    }
  } catch (e) {
    console.error(e)
    alert('Failed to send test email')
  }
}
</script>
