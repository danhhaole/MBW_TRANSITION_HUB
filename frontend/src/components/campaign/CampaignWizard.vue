<template>
  <div v-if="show" class="fixed inset-0 bg-white z-[9] flex flex-col">
    <!-- Header -->
    <CampaignWizardHeader
      :campaign-name="campaignData.campaign_name"
      :current-step="currentStep"
      :total-steps="steps.length"
      :loading="loading"
      :saving="draftCampaignLoading"
      :finalizing="activating"
      :auto-saving="isAutoSaving"
      :save-success="showSaveSuccess"
      :can-save="true"
      :can-proceed="canProceed"
      :can-finalize="isLastStep"
      :is-edit-mode="isEditMode"
      @exit="closeWizard"
      @back="prevStep"
      @save="saveDraft"
      @save-and-continue="nextStep"
      @finalize="finalizeCampaign"
      @update:campaign-name="updateCampaignName"
    />

    <!-- Stepper -->
    <CampaignWizardStepper
      :steps="steps"
      :current-step="currentStep"
      @step-click="handleStepClick"
    />

    <!-- Content -->
    <CampaignWizardContent :current-step="currentStep">
      <template #default="{ currentStep: step }">
        <div class="space-y-6">
            <!-- Step 1: Campaign Information -->
            <div v-if="step === 1" class="space-y-6 animate-fadeIn">
              <!-- Interaction Methods Selection -->
              <div class="bg-gray-50 rounded-lg p-6">
                <div class="text-center mb-6">
                  <h4 class="text-lg font-semibold mb-2 text-gray-900">
                    {{ __("Choose Interaction Method") }}
                  </h4>
                  <p class="text-sm text-gray-600">
                    {{ __("Choose the interaction method you want to use with the candidate (only one type can be selected)") }}
                  </p>
                 
                </div>

                <!-- Interaction Methods -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <!-- Email Method -->
                  <div
                    class="border rounded-lg p-4 transition-all duration-200"
                    :class="[
                      campaignData.interaction_method === 'EMAIL'
                        ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                        : 'border-gray-200',
                      canEditInteractionMethod 
                        ? 'cursor-pointer hover:border-gray-300 hover:shadow-md'
                        : 'cursor-not-allowed opacity-60'
                    ]"
                    @click="canEditInteractionMethod && (campaignData.interaction_method = 'EMAIL')"
                  >
                    <div class="text-center">
                      <div
                        class="flex items-center justify-center w-10 h-10 rounded-full mx-auto mb-3"
                        :class="
                          campaignData.interaction_method === 'EMAIL'
                            ? 'bg-blue-100 text-blue-600'
                            : 'bg-gray-100 text-gray-400'
                        "
                      >
                        <FeatherIcon name="mail" class="h-5 w-5" />
                      </div>
                      <h5
                        class="text-sm font-semibold mb-1"
                        :class="
                          campaignData.interaction_method === 'EMAIL'
                            ? 'text-blue-900'
                            : 'text-gray-900'
                        "
                      >
                        {{ __("Send Email") }}
                      </h5>
                      <p class="text-xs text-gray-600">
                        {{ __("Create and send email to the candidate") }}
                      </p>
                    </div>
                  </div>

                  <!-- Zalo ZNS Method -->
                  <div
                    class="border rounded-lg p-4 transition-all duration-200"
                    :class="[
                      campaignData.interaction_method === 'ZALO_ZNS'
                        ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                        : 'border-gray-200',
                      canEditInteractionMethod 
                        ? 'cursor-pointer hover:border-gray-300 hover:shadow-md'
                        : 'cursor-not-allowed opacity-60'
                    ]"
                    @click="canEditInteractionMethod && (campaignData.interaction_method = 'ZALO_ZNS')"
                  >
                    <div class="text-center">
                      <div
                        class="flex items-center justify-center w-10 h-10 rounded-full mx-auto mb-3"
                        :class="
                          campaignData.interaction_method === 'ZALO_ZNS'
                            ? 'bg-blue-100 text-blue-600'
                            : 'bg-gray-100 text-gray-400'
                        "
                      >
                        <FeatherIcon name="message-circle" class="h-5 w-5" />
                      </div>
                      <h5
                        class="text-sm font-semibold mb-1"
                        :class="
                          campaignData.interaction_method === 'ZALO_ZNS'
                            ? 'text-blue-900'
                            : 'text-gray-900'
                        "
                      >
                        {{ __("Send Zalo ZNS") }}
                      </h5>
                      <p class="text-xs text-gray-600">
                        {{ __("Send message to the candidate's phone number using Zalo") }}
                      </p>
                    </div>
                  </div>

                  <!-- Zalo Care Method -->
                  <div
                    class="border rounded-lg p-4 transition-all duration-200"
                    :class="[
                      campaignData.interaction_method === 'ZALO_CARE'
                        ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                        : 'border-gray-200',
                      canEditInteractionMethod 
                        ? 'cursor-pointer hover:border-gray-300 hover:shadow-md'
                        : 'cursor-not-allowed opacity-60'
                    ]"
                    @click="canEditInteractionMethod && (campaignData.interaction_method = 'ZALO_CARE')"
                  >
                    <div class="text-center">
                      <div
                        class="flex items-center justify-center w-10 h-10 rounded-full mx-auto mb-3"
                        :class="
                          campaignData.interaction_method === 'ZALO_CARE'
                            ? 'bg-blue-100 text-blue-600'
                            : 'bg-gray-100 text-gray-400'
                        "
                      >
                        <FeatherIcon name="heart" class="h-5 w-5" />
                      </div>
                      <h5
                        class="text-sm font-semibold mb-1"
                        :class="
                          campaignData.interaction_method === 'ZALO_CARE'
                            ? 'text-blue-900'
                            : 'text-gray-900'
                        "
                      >
                        {{ __("Send Zalo Care") }}
                      </h5>
                      <p class="text-xs text-gray-600">
                        {{ __("Send message to the candidate's phone number using Zalo") }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Campaign Information (Original Content) -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __("Campaign Name") }} <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="campaignData.campaign_name"
                  type="text"
                  :placeholder="__('Example: React Candidate Nurturing Q4/2024')"
                  :disabled="false"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  :class="{
                    'border-red-500': !campaignData.campaign_name && currentStep > 1
                  }"
                />
              </div>

              <!-- Status selection -->


              <!-- Start/End Datetime -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __("Start Date/Time") }}
                  </label>
                  <input
                    v-model="campaignData.start_date"
                    type="datetime-local"
                    :min="minScheduledAt"
                    :disabled="isDraftCreated"
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    :class="{
                      'bg-gray-100 cursor-not-allowed': isDraftCreated
                    }"
                  />
                  <p class="mt-1 text-xs text-gray-500">
                    {{ __("Local time") }} ({{ localTzLabel }})
                  </p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __("End Date/Time") }}
                  </label>
                  <input
                    v-model="campaignData.end_date"
                    type="datetime-local"
                    :min="campaignData.start_date || minScheduledAt"
                    :disabled="isDraftCreated"
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    :class="{
                      'bg-gray-100 cursor-not-allowed': isDraftCreated
                    }"
                  />
                  <p class="mt-1 text-xs text-gray-500">
                    {{ __("Local time") }} ({{ localTzLabel }})
                  </p>
                </div>
              </div>


              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __("Objective") }} <span class="text-red-500">*</span>
                </label>
                <textarea
                  v-model="campaignData.description"
                  rows="3"
                  :placeholder="__('Brief description of campaign purpose...')"
                  :disabled="!canEditDescription"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  :class="{
                    'border-red-500': !campaignData.description && currentStep > 1,
                    'bg-gray-100 cursor-not-allowed': !canEditDescription
                  }"
                />
                <!-- Warning when draft is created -->
               
              </div>
            </div>

            <!-- Step 2: Content Design -->
            <div v-if="step === 2" class="animate-fadeIn">
              <div class="space-y-4">
                <div class="text-center mb-6">
                  <h4 class="text-lg font-medium text-gray-900 mb-2">
                    {{ __("Design Content") }}
                  </h4>
                  <p class="text-sm text-gray-600">
                    {{ __("Create the content for your campaign based on the selected interaction method") }}
                  </p>
                </div>

                <!-- Show warning if no interaction method selected -->
                <div v-if="!campaignData.interaction_method" class="text-center py-12">
                  <FeatherIcon name="alert-triangle" class="h-8 w-8 text-yellow-600 mx-auto mb-2" />
                  <h4 class="text-lg font-medium text-yellow-900 mb-2">
                    {{ __("No interaction method selected") }}
                  </h4>
                  <p class="text-yellow-700">
                    {{ __("Please go back to Step 1 to select an interaction method") }}
                  </p>
                </div>

                <!-- Content Editor -->
                <CampaignContentEditor
                  v-else
                  :interaction_type="campaignData.interaction_method"
                  :model-value="contentEditorData"
                  :readonly="!canEditContent"
                  @update:model-value="handleContentUpdate"
                  @save="handleContentSave"
                  @preview="handleContentPreview"
                />
              </div>
            </div>

            <!-- Step 3: Target Segment -->
            <div v-if="step === 3" class="animate-fadeIn">
              <div class="space-y-6">
                <!-- Header -->
                <div class="text-center mb-6">
                  <h4 class="text-lg font-medium text-gray-900 mb-2">
                    {{ __("Target Segment") }}
                  </h4>
                  <p class="text-sm text-gray-600">
                    {{ __("Choose candidates and configure sending strategy") }}
                  </p>
                </div>

                <!-- Segment Selection -->
                <div class="bg-gray-50 rounded-lg p-6">
                  <h5 class="text-md font-medium text-gray-900 mb-4">
                    {{ __("Select Candidates") }}
                  </h5>
                  <p class="text-sm text-gray-600 mb-4">
                    {{ __("Which candidates do you want to send this campaign to?") }}
                  </p>
                  
                  <!-- Segment Options -->
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <!-- Choose Candidates (Segment) -->
                    <div 
                      class="border rounded-lg p-4 bg-white cursor-pointer transition-colors"
                      :class="segmentSelectionMode === 'segment' ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' : 'border-gray-200 hover:border-blue-300'"
                      @click="segmentSelectionMode = 'segment'"
                    >
                      <div class="text-center">
                        <div class="flex items-center justify-center w-12 h-12 rounded-full mx-auto mb-3"
                             :class="segmentSelectionMode === 'segment' ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'">
                          <FeatherIcon name="users" class="h-6 w-6" />
                        </div>
                        <h6 class="text-sm font-semibold mb-1"
                            :class="segmentSelectionMode === 'segment' ? 'text-blue-900' : 'text-gray-900'">
                          {{ __("Choose Candidates (Segment)") }}
                        </h6>
                        <p class="text-xs text-gray-600">
                          {{ __("Use existing candidate segments") }}
                        </p>
                      </div>
                    </div>

                    <!-- Custom Conditions -->
                    <div 
                      class="border rounded-lg p-4 bg-white cursor-pointer transition-colors"
                      :class="segmentSelectionMode === 'conditions' ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' : 'border-gray-200 hover:border-blue-300'"
                      @click="segmentSelectionMode = 'conditions'"
                    >
                      <div class="text-center">
                        <div class="flex items-center justify-center w-12 h-12 rounded-full mx-auto mb-3"
                             :class="segmentSelectionMode === 'conditions' ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'">
                          <FeatherIcon name="filter" class="h-6 w-6" />
                        </div>
                        <h6 class="text-sm font-semibold mb-1"
                            :class="segmentSelectionMode === 'conditions' ? 'text-blue-900' : 'text-gray-900'">
                          {{ __("Custom Conditions") }}
                        </h6>
                        <p class="text-xs text-gray-600">
                          {{ __("Create custom filtering conditions") }}
                        </p>
                      </div>
                    </div>
                  </div>

                  <!-- Segment Selection Content -->
                  <div v-if="segmentSelectionMode === 'segment'">
                    <!-- Use existing PoolConfig component for segment selection -->
                    <component :is="PoolConfig" v-model="configData" />
                  </div>

                  <!-- Custom Conditions Content -->
                  <div v-else-if="segmentSelectionMode === 'conditions'" class="space-y-4">
                    <div class="bg-white rounded-lg border p-4">
                      <h6 class="text-sm font-medium text-gray-900 mb-2">
                        {{ __("Custom Conditions") }}
                      </h6>
                      <p class="text-xs text-gray-600 mb-4">
                        {{ __("Create conditions to filter candidates who will receive your campaign") }}
                      </p>

                      <!-- Logic Selection -->
                      <div class="mb-4">
                        <label class="block text-sm font-medium text-gray-700 mb-2">
                          {{ __("Condition Logic") }}
                        </label>
                        <div class="flex space-x-4">
                          <label class="flex items-center">
                            <input
                              type="radio"
                              v-model="conditionsLogic"
                              value="any"
                              class="mr-2"
                            />
                            <span class="text-sm text-gray-700">{{ __("Any conditions (OR)") }}</span>
                          </label>
                          <label class="flex items-center">
                            <input
                              type="radio"
                              v-model="conditionsLogic"
                              value="all"
                              class="mr-2"
                            />
                            <span class="text-sm text-gray-700">{{ __("All conditions (AND)") }}</span>
                          </label>
                        </div>
                      </div>

                      <!-- Conditions List -->
                      <div v-if="customConditions.length > 0" class="space-y-3 mb-4">
                        <div
                          v-for="(condition, index) in customConditions"
                          :key="index"
                          class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                        >
                          <div class="flex-1 cursor-pointer" @click="editCondition(condition, index)">
                            <span class="text-sm font-medium text-gray-900">
                              {{ getConditionLabel(condition) }}
                            </span>
                            <span class="text-sm text-gray-600 ml-2">
                              {{ condition.operator }} 
                              <span v-if="!['is_empty', 'is_not_empty'].includes(condition.operator)">
                                {{ condition.value }}
                              </span>
                            </span>
                          </div>
                          <div class="flex items-center space-x-2">
                            <Button
                              variant="ghost"
                              size="sm"
                              @click="editCondition(condition, index)"
                              class="text-blue-600 hover:text-blue-700"
                            >
                              <FeatherIcon name="edit" class="h-4 w-4" />
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              @click="removeCondition(index)"
                              class="text-red-600 hover:text-red-700"
                            >
                              <FeatherIcon name="trash-2" class="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      </div>

                      <!-- Add Condition Button -->
                      <Button
                        variant="outline"
                        size="sm"
                        @click="addCondition"
                        class="w-full"
                      >
                        <template #prefix>
                          <FeatherIcon name="plus" class="h-4 w-4" />
                        </template>
                        {{ __("Add Condition") }}
                      </Button>
                    </div>
                  </div>
                </div>

                <!-- Candidate Count -->
                <div class="bg-blue-50 rounded-lg p-4">
                  <h5 class="text-md font-medium text-gray-900 mb-2">
                    {{ __("Candidate Count") }}
                  </h5>
                  <p class="text-sm text-gray-600 mb-2">
                    {{ __("This campaign will be sent to approximately") }}
                  </p>
                  <div class="text-2xl font-bold text-blue-600">
                    {{ computedCandidateCount }} {{ __("candidates") }}
                  </div>
                </div>

                <!-- Sending Strategy -->
                <div class="bg-gray-50 rounded-lg p-6">
                  <h5 class="text-md font-medium text-gray-900 mb-4">
                    {{ __("Sending Strategy") }}
                  </h5>
                  <p class="text-sm text-gray-600 mb-4">
                    {{ __("When do you want to send this campaign?") }}
                  </p>

                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <!-- Send Now -->
                    <div 
                      class="border rounded-lg p-4 bg-white cursor-pointer transition-colors"
                      :class="sendingStrategy === 'now' ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' : 'border-gray-200 hover:border-gray-300'"
                      @click="sendingStrategy = 'now'"
                    >
                      <div class="text-center">
                        <div class="flex items-center justify-center w-12 h-12 rounded-full mx-auto mb-3"
                             :class="sendingStrategy === 'now' ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'">
                          <FeatherIcon name="send" class="h-6 w-6" />
                        </div>
                        <h6 class="text-sm font-semibold mb-1"
                            :class="sendingStrategy === 'now' ? 'text-blue-900' : 'text-gray-900'">
                          {{ __("Send Now") }}
                        </h6>
                        <p class="text-xs text-gray-600">
                          {{ __("Send campaign immediately") }}
                        </p>
                      </div>
                    </div>

                    <!-- Schedule Send -->
                    <div 
                      class="border rounded-lg p-4 bg-white cursor-pointer transition-colors"
                      :class="sendingStrategy === 'scheduled' ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' : 'border-gray-200 hover:border-gray-300'"
                      @click="sendingStrategy = 'scheduled'"
                    >
                      <div class="text-center">
                        <div class="flex items-center justify-center w-12 h-12 rounded-full mx-auto mb-3"
                             :class="sendingStrategy === 'scheduled' ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'">
                          <FeatherIcon name="calendar" class="h-6 w-6" />
                        </div>
                        <h6 class="text-sm font-semibold mb-1"
                            :class="sendingStrategy === 'scheduled' ? 'text-blue-900' : 'text-gray-900'">
                          {{ __("Schedule Send") }}
                        </h6>
                        <p class="text-xs text-gray-600">
                          {{ __("Choose specific time to send campaign") }}
                        </p>
                      </div>
                    </div>
                  </div>

                  <!-- Schedule Date/Time Input -->
                  <div v-if="sendingStrategy === 'scheduled'" class="mt-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                      {{ __("Schedule Date & Time") }}
                    </label>
                    <input
                      type="datetime-local"
                      v-model="campaignData.start_date"
                      class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    />
                  </div>
                </div>
              </div>
            </div>
        </div>
      </template>
    </CampaignWizardContent>

    <!-- Step Form Dialog -->
    <StepFormDialog
      v-model="showStepForm"
      :editing-step="editingStep"
      :campaign-steps="campaignSteps"
      :draft-campaign="draftCampaign"
      @submit="handleStepFormSubmit"
      @cancel="handleStepFormCancel"
    />

    <!-- Social Network Config Modal -->
    <SocialNetworkConfigDialog
      v-model="showSocialConfigModal"
      mode="wizard"
      :social-config="configData.socialConfig"
      :social-pages="socialPages"
      :external-connections="externalConnections"
      :loading-connections="loadingConnections"
      :job-openings-list="jobOpeningsList"
      :loading-pages="loadingPages"
      :loading-job-openings="loadingJobOpenings"
      :min-scheduled-at="minScheduledAt"
      :local-tz-label="localTzLabel"
      :campaign-id="draftCampaign?.data?.name"
      :campaign-social-id="editingSocialId"
      @update:social-config="updateSocialConfig"
      @confirm="confirmSocialConfig"
      @cancel="() => showSocialConfigModal = false"
      @job-opening-change="onSocialJobOpeningChange"
    />

    <!-- Condition Editor Modal -->
    <div v-if="showConditionModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-medium text-gray-900 mb-4">
          {{ editingConditionIndex >= 0 ? __('Edit Condition') : __('Add Condition') }}
        </h3>
        
        <div class="space-y-4">
          <!-- Field Selection -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Field') }}
            </label>
            <select 
              v-model="editingCondition.field"
              @change="updateFieldType"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option value="">{{ __('Select field...') }}</option>
              <option 
                v-for="field in conditionFields" 
                :key="field.value" 
                :value="field.value"
              >
                {{ field.label }}
              </option>
            </select>
          </div>

          <!-- Operator Selection -->
          <div v-if="editingCondition.field">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Operator') }}
            </label>
            <select 
              v-model="editingCondition.operator"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option 
                v-for="operator in getOperatorsForField(editingCondition.fieldType)" 
                :key="operator.value" 
                :value="operator.value"
              >
                {{ operator.label }}
              </option>
            </select>
          </div>

          <!-- Value Input -->
          <div v-if="editingCondition.field && !['is_empty', 'is_not_empty'].includes(editingCondition.operator)">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Value') }}
            </label>
            
            <!-- Text Input -->
            <input
              v-if="editingCondition.fieldType === 'text'"
              type="text"
              v-model="editingCondition.value"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              :placeholder="__('Enter value...')"
            />
            
            <!-- Number Input -->
            <input
              v-else-if="editingCondition.fieldType === 'number'"
              type="number"
              v-model="editingCondition.value"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              :placeholder="__('Enter number...')"
            />
            
            <!-- Date Input -->
            <input
              v-else-if="editingCondition.fieldType === 'date'"
              type="date"
              v-model="editingCondition.value"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
            
            <!-- Select Input -->
            <select
              v-else-if="editingCondition.fieldType === 'select'"
              v-model="editingCondition.value"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option value="">{{ __('Select option...') }}</option>
              <option 
                v-for="option in getFieldOptions(editingCondition.field)" 
                :key="option.value" 
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
          </div>
        </div>

        <!-- Modal Actions -->
        <div class="flex justify-end space-x-3 mt-6">
          <Button
            variant="outline"
            @click="cancelConditionEdit"
          >
            {{ __('Cancel') }}
          </Button>
          <Button
            variant="solid"
            @click="saveCondition"
            :disabled="!editingCondition.field"
          >
            {{ __('Save') }}
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, reactive } from "vue";
import { Button, FeatherIcon } from "frappe-ui";
import CampaignWizardHeader from "./CampaignWizardHeader.vue";
import CampaignWizardStepper from "./CampaignWizardStepper.vue";
import CampaignWizardContent from "./CampaignWizardContent.vue";
import CampaignContentEditor from "./CampaignContentEditor.vue";
import { call } from "frappe-ui";
import PoolConfig from "./PoolConfig.vue";
import FileConfig from "./FileConfig.vue";
import ImageUploader from "@/components/Controls/ImageUploader.vue";
import WorkflowTemplateSelector from "./WorkflowTemplateSelector.vue";
import WorkflowBuilder from "./WorkflowBuilder.vue";
import Link from "@/components/Controls/Link.vue";
import StepFormDialog from "./StepFormDialog.vue";
import SocialNetworkConfigDialog from "./SocialNetworkConfigDialog.vue";

import { useCandidateStore } from "@/stores/candidate";
import { useMiraTalentPoolStore } from "@/stores/miraTalentPool";
import { useCampaignStore } from "@/stores/campaign";
import { useCampaignStepStore } from "@/stores/campaignStep";
import { useCampaignTemplateStore } from "@/stores/campaignTemplate";
import { toLocalDatetimeInput, formatDateForDatabase , toIsoIfSet , formatDateForDisplay, getCurrentDatabaseDateTime, } from "@/utils/dateUtils";
import { useCampaignSocialStore } from "@/stores/campaignSocial";
import { useJobOpeningStore } from "@/stores/jobOpening";
import { useCandidateDataSourceStore } from "@/stores/candidateDataSource.js";
import { debounce } from "@/utils/debounce";

import { useToast } from "../../composables/useToast";

// Props & Emits
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  preselectedSegment: {
    type: String,
    default: "",
  },
  // Optional: when provided, wizard will open in edit mode and prefill fields
  editCampaign: {
    type: Object,
    default: null,
  },
  // New prop for editing campaign
  editingCampaign: {
    type: Object,
    default: null,
  },
});


const emit = defineEmits(["update:modelValue", "success", "draft-created"]);

// Reactive state
const show = ref(false);
const currentStep = ref(1);
const loading = ref(false);
const toast = useToast();
const activating = ref(false);

// Edit mode
const isEditMode = computed(() => !!(props.editCampaign || props.editingCampaign));
const editingCampaignData = computed(() => props.editCampaign || props.editingCampaign);

// Fields that can be edited in edit mode
// Logic để disable fields sau khi đã tạo draft campaign - CHỈ CHO SỬA TÊN THÔI
const canEditInteractionMethod = computed(() => {
  // Block nếu đang edit mode HOẶC đã tạo draft campaign
  return !isEditMode.value && !isDraftCreated.value;
});
const canEditDescription = computed(() => {
  // Block nếu đang edit mode HOẶC đã tạo draft campaign  
  return !isEditMode.value && !isDraftCreated.value;
});
const canEditSource = computed(() => !isDraftCreated.value && (!isEditMode.value || editingCampaignData.value?.status === 'DRAFT'));
const canEditSegment = computed(() => !isDraftCreated.value && (!isEditMode.value || editingCampaignData.value?.status === 'DRAFT'));
const canEditContent = computed(() => !isEditMode.value || ['DRAFT', 'PAUSED'].includes(editingCampaignData.value?.status));

// Auto-save debounce timer
const autoSaveTimer = ref(null);
const isAutoSaving = ref(false);
const lastSaveSuccess = ref(false);
const showSaveSuccess = ref(false);
const isUpdatingFromAutoSave = ref(false); // Flag to prevent infinite loop

// Campaign stores
const campaignStore = useCampaignStore();
const campaignStepStore = useCampaignStepStore();
const campaignSocialStore = useCampaignSocialStore();
const campaignTemplateStore = useCampaignTemplateStore();
const candidateDataSourceStore = useCandidateDataSourceStore();
const jobOpeningStore = useJobOpeningStore();

//chọn nguồn
const searchSource = ref(null);
const searchKeyword = ref("");
const selectedSegment = ref("");

// Draft campaign for steps creation
const draftCampaign = ref(null);
const draftCampaignLoading = ref(false);

// Check if draft campaign has been created
const isDraftCreated = computed(() => !!draftCampaign.value);
const records = ref([]);
const selectedCandidates = ref([]);
const miraTalentCampaign = ref({ type: null, records: [] });

// Pagination states
const currentPage = ref(1);
const pageSize = ref(20);
const totalRecords = ref(0);
const searchLoading = ref(false);

// Advanced filters
const advancedFilters = reactive({
  // Contact filters
  missingEmail: false,
  missingPhone: false,
  // Talent filters
  skills: '',
  tags: '',
  minExperienceYears: null,
  maxExperienceYears: null
});

// Form data
const campaignData = ref({
  campaign_name: "",
  description: "",
  type: "GATHERING", // Default single type
  status: "DRAFT",
  interaction_method: "", // New field: 'EMAIL', 'ZALO_ZNS', 'ZALO_CARE'
  target_segment: props.preselectedSegment || "",
  source_type: "", // New field: 'DataSource', 'File', 'Search'
  source_file: "", // For File type
  data_source_id: "", // For DataSource type
  source_config: null, // New field to store file mapping, meta, and URL
  job_opening: "", // Changed from job_opening_id to job_opening
  start_date: "", // datetime-local
  end_date: "", // datetime-local
  mira_talent_campaign: "", // JSON string for MIRA Talent source
  // Content design fields
  email_subject: "", // For EMAIL method
  email_content: "", // For EMAIL method
  message_content: "", // For ZALO methods
  image_url: "", // For image attachments
  attachments: [], // For email attachments
  action_buttons: [], // For interactive buttons
  success_action: "", // Action when success
  failure_action: "", // Action when failure
  // Additional actions fields
  follow_up_actions: [], // Follow-up actions configuration (legacy)
  automation_rules: [], // Automation rules configuration (legacy)
  additional_actions: {}, // New format for additional actions
  criteria: "", // JSON string for custom conditions
});

const selectedSource = ref(props.preselectedSegment ? "search" : "");
const selectedDataSourceType = ref(""); // ATS, JobBoard, SocialNetwork, TalentPool
const selectedDataSourceId = ref(""); // Specific data source ID
const filteredDataSources = ref([]); // Filtered list to show
const connectedDataSources = ref([]); // From External Connection API
const loadingDataSources = ref(false);

// Track data source selection level: 0=source, 1=type, 2=specific
const dataSourceSelectionLevel = ref(0);


// search start

// Fetch data with pagination
async function fetchRecords(page = 1) {
  if (!searchSource.value) return;

  searchLoading.value = true;
  try {
    const startIndex = (page - 1) * pageSize.value;
    
    if (searchSource.value === "mira_talent") {
      let filters = [];
      
      // Nếu có segment thì lọc theo segment
      if (selectedSegment.value) {
        // Lấy talent_id từ Mira Talent Pool
        const poolRes = await call("frappe.client.get_list", {
          doctype: "Mira Talent Pool",
          fields: ["talent_id"],
          filters: { segment_id: selectedSegment.value },
          limit_page_length: 1000,
        });
        
        const talentIds = poolRes.map(r => r.talent_id);
        if (!talentIds.length) {
          records.value = [];
          totalRecords.value = 0;
          return;
        }
        
        filters.push(["name", "in", talentIds]);
      }
      
      // Thêm filter tìm kiếm nếu có
      if (searchKeyword.value) {
        filters.push(["full_name", "like", `%${searchKeyword.value}%`]);
      }
      
      // Advanced filters for talents
      if (advancedFilters.skills) {
        filters.push(["skills", "like", `%${advancedFilters.skills}%`]);
      }
      
      if (advancedFilters.tags) {
        filters.push(["tags", "like", `%${advancedFilters.tags}%`]);
      }
      
      if (advancedFilters.minExperienceYears !== null) {
        filters.push(["experience_years", ">=", advancedFilters.minExperienceYears]);
      }
      
      if (advancedFilters.maxExperienceYears !== null) {
        filters.push(["experience_years", "<=", advancedFilters.maxExperienceYears]);
      }
      
      const res = await call("frappe.client.get_list", {
        doctype: "Mira Talent",
        fields: ["name", "full_name", "email", "phone", "skills", "tags", "experience_years"],
        filters: filters,
        limit_start: startIndex,
        limit_page_length: pageSize.value,
      });
      
      // Get total count
      const countRes = await call("frappe.client.get_count", {
        doctype: "Mira Talent",
        filters: filters,
      });
      
      records.value = page === 1 ? res : [...records.value, ...res];
      totalRecords.value = countRes;

    } else if (searchSource.value === "mira_contact") {
      let filters = [];
      
      // Add search filter if exists
      if (searchKeyword.value) {
        filters.push(["full_name", "like", `%${searchKeyword.value}%`]);
      }
      
      // Advanced filters for contacts
      if (advancedFilters.missingEmail) {
        filters.push(["email", "in", ["", null]]);
      }
      
      if (advancedFilters.missingPhone) {
        filters.push(["phone", "in", ["", null]]);
      }
      
      const res = await call("frappe.client.get_list", {
        doctype: "Mira Contact",
        fields: ["name", "full_name", "email", "phone"],
        filters: filters,
        limit_start: startIndex,
        limit_page_length: pageSize.value,
      });
      
      // Get total count
      const countRes = await call("frappe.client.get_count", {
        doctype: "Mira Contact",
        filters: filters,
      });
      
      records.value = page === 1 ? res : [...records.value, ...res];
      totalRecords.value = countRes;
    }
    
    currentPage.value = page;
  } catch (e) {
    console.error("Error fetching records", e);
    records.value = [];
    totalRecords.value = 0;
  } finally {
    searchLoading.value = false;
  }
}


// ✅ bọc fetchRecords bằng debounce
const fetchRecordsDebounced = debounce(fetchRecords, 400);

// Load more records
function loadMoreRecords() {
  if (searchLoading.value) return;
  const nextPage = currentPage.value + 1;
  const maxPages = Math.ceil(totalRecords.value / pageSize.value);
  
  if (nextPage <= maxPages) {
    fetchRecords(nextPage);
  }
}

// Check if can load more
const canLoadMore = computed(() => {
  const maxPages = Math.ceil(totalRecords.value / pageSize.value);
  return currentPage.value < maxPages && !searchLoading.value;
});

function toggleCandidate(name) {
  if (selectedCandidates.value.includes(name)) {
    selectedCandidates.value = selectedCandidates.value.filter((c) => c !== name);
  } else {
    selectedCandidates.value = [...selectedCandidates.value, name];
  }
}

// Select all candidates on current page
function selectAllCurrentPage() {
  const currentPageIds = records.value.map(r => r.name);
  const newSelected = [...new Set([...selectedCandidates.value, ...currentPageIds])];
  selectedCandidates.value = newSelected;
}

// Clear all selected candidates
function clearSelection() {
  selectedCandidates.value = [];
}

// Reset khi đổi nguồn
watch(searchSource, () => {
  selectedCandidates.value = [];
  selectedSegment.value = ""; // ✅ reset cả segment
  records.value = [];
  currentPage.value = 1;
  totalRecords.value = 0;
  miraTalentCampaign.value = { type: searchSource.value, records: [] };
  
  // Reset advanced filters
  Object.keys(advancedFilters).forEach(key => {
    if (typeof advancedFilters[key] === 'boolean') {
      advancedFilters[key] = false;
    } else {
      advancedFilters[key] = key.includes('Years') ? null : '';
    }
  });

  if (searchSource.value) {
    fetchRecords(1);
  }
});

// Watch segment để query mới (chỉ áp dụng cho talent)
watch(selectedSegment, (val) => {
  if (searchSource.value === "mira_talent") {
    selectedCandidates.value = [];
    records.value = [];
    currentPage.value = 1;
    totalRecords.value = 0;
    fetchRecords(1);
  }
});

// Watch candidates để update JSON
watch(
  selectedCandidates,
  (newVal) => {
    miraTalentCampaign.value = {
      type: searchSource.value,
      records: newVal,
      ...(searchSource.value === "mira_talent" && selectedSegment.value
        ? { segment_id: selectedSegment.value }
        : {}),
    };
    console.log("miraTalentCampaign JSON", miraTalentCampaign.value);
  },
  { deep: true }
);

// Watch searchKeyword để trigger debounced fetch
watch(searchKeyword, () => {
  if (!searchSource.value) return;
  currentPage.value = 1;
  records.value = [];
  totalRecords.value = 0;
  fetchRecordsDebounced(1);
});

// Watch advanced filters
watch(advancedFilters, () => {
  if (!searchSource.value) return;
  currentPage.value = 1;
  records.value = [];
  totalRecords.value = 0;
  fetchRecordsDebounced(1);
}, { deep: true });

// search end

// Data for form submission
const configData = ref({
  selectedSegment: props.preselectedSegment || "",
  selectedDataSource: "",
  selectedFile: null,
  uploadedFileUrl: "",
  filePreview: [],
  fileHeaders: [],
  socialConfig: {
    page_id: "",
    scheduled_at: "",
    job_opening: "",
    image: "",
  },
});
const dataSources = ref([]); // All data sources from API

// Campaign Steps State
const campaignSteps = ref([]);
const selectedTemplate = ref(null);
const campaignTemplates = ref([]);
const showStepCreation = ref(false);
const stepCreationMode = ref(""); // 'template' or 'manual'
const showStepForm = ref(false);
const editingStep = ref(null);
// Track originally loaded step IDs to detect deletions in edit mode
const originalStepIds = ref([]);

// Manual Step Job Opening selection state
const stepFormSelectedJobId = ref("");

// Job step state
const jobOpeningsList = ref([]);
const loadingJobOpenings = ref(false);
const selectedJobOpeningDetails = ref(null);

// Target Segment state
const sendingStrategy = ref('now'); // 'now' or 'scheduled'
const candidateCount = ref(0);
const segmentSelectionMode = ref(''); // 'segment' or 'conditions'
const conditionsLogic = ref('any'); // 'any' or 'all'
const customConditions = ref([]);
const showConditionModal = ref(false);
const editingCondition = ref(null);
const editingConditionIndex = ref(-1);

// Watch sendingStrategy to auto-set start_date
watch(sendingStrategy, (newStrategy) => {
  if (newStrategy === 'now') {
    // Set start_date to current time for immediate sending
    campaignData.value.start_date = toLocalDatetimeInput(new Date());
  } else if (newStrategy === 'scheduled' && !campaignData.value.start_date) {
    // Set default scheduled time to 1 hour from now
    const oneHourLater = new Date(Date.now() + 60 * 60 * 1000);
    campaignData.value.start_date = toLocalDatetimeInput(oneHourLater);
  }
});

// Computed candidate count based on selected data
const computedCandidateCount = computed(() => {
  if (selectedSource.value === 'search' && miraTalentCampaign.value.records) {
    return miraTalentCampaign.value.records.length || 0;
  }
  // For other sources, we might need to implement specific logic
  return candidateCount.value;
});

// Watch configData changes to update candidate count
watch(
  () => miraTalentCampaign.value.records,
  (newRecords) => {
    candidateCount.value = newRecords ? newRecords.length : 0;
  },
  { deep: true }
);

// Condition management methods
const addCondition = () => {
  editingCondition.value = {
    id: Date.now(),
    field: '',
    operator: 'equals',
    value: '',
    fieldType: 'text'
  };
  editingConditionIndex.value = -1;
  showConditionModal.value = true;
};

const editCondition = (condition, index) => {
  editingCondition.value = { ...condition };
  editingConditionIndex.value = index;
  showConditionModal.value = true;
};

const saveCondition = () => {
  if (!editingCondition.value.field) return;
  
  if (editingConditionIndex.value >= 0) {
    // Edit existing condition
    customConditions.value[editingConditionIndex.value] = { ...editingCondition.value };
  } else {
    // Add new condition
    customConditions.value.push({ ...editingCondition.value });
  }
  
  showConditionModal.value = false;
  editingCondition.value = null;
  editingConditionIndex.value = -1;
};

const cancelConditionEdit = () => {
  showConditionModal.value = false;
  editingCondition.value = null;
  editingConditionIndex.value = -1;
};

const removeCondition = (index) => {
  customConditions.value.splice(index, 1);
};

const getConditionLabel = (condition) => {
  const fieldLabels = {
    'full_name': __('Full Name'),
    'email': __('Email'),
    'phone': __('Phone'),
    'date_of_birth': __('Date of Birth'),
    'gender': __('Gender'),
    'address': __('Address'),
    'experience_years': __('Years of Experience'),
    'education_level': __('Education Level'),
    'skills': __('Skills'),
    'current_position': __('Current Position'),
    'expected_salary': __('Expected Salary'),
    'created': __('Created Date'),
    'modified': __('Modified Date')
  };
  return fieldLabels[condition.field] || condition.field;
};

// Available condition fields for candidates
const conditionFields = computed(() => [
  { value: 'full_name', label: __('Full Name'), type: 'text' },
  { value: 'email', label: __('Email'), type: 'text' },
  { value: 'phone', label: __('Phone'), type: 'text' },
  { value: 'date_of_birth', label: __('Date of Birth'), type: 'date' },
  { value: 'gender', label: __('Gender'), type: 'select', options: [
    { value: 'Male', label: __('Male') },
    { value: 'Female', label: __('Female') },
    { value: 'Other', label: __('Other') }
  ]},
  { value: 'address', label: __('Address'), type: 'text' },
  { value: 'experience_years', label: __('Years of Experience'), type: 'number' },
  { value: 'education_level', label: __('Education Level'), type: 'select', options: [
    { value: 'High School', label: __('High School') },
    { value: 'Bachelor', label: __('Bachelor') },
    { value: 'Master', label: __('Master') },
    { value: 'PhD', label: __('PhD') }
  ]},
  { value: 'skills', label: __('Skills'), type: 'text' },
  { value: 'current_position', label: __('Current Position'), type: 'text' },
  { value: 'expected_salary', label: __('Expected Salary'), type: 'number' },
  { value: 'created', label: __('Created Date'), type: 'date' },
  { value: 'modified', label: __('Modified Date'), type: 'date' }
]);

// Available operators based on field type
const getOperatorsForField = (fieldType) => {
  const operators = {
    text: [
      { value: 'equals', label: __('Equals') },
      { value: 'not_equals', label: __('Not Equals') },
      { value: 'contains', label: __('Contains') },
      { value: 'not_contains', label: __('Does Not Contain') },
      { value: 'starts_with', label: __('Starts With') },
      { value: 'ends_with', label: __('Ends With') },
      { value: 'is_empty', label: __('Is Empty') },
      { value: 'is_not_empty', label: __('Is Not Empty') }
    ],
    number: [
      { value: 'equals', label: __('Equals') },
      { value: 'not_equals', label: __('Not Equals') },
      { value: 'greater_than', label: __('Greater Than') },
      { value: 'less_than', label: __('Less Than') },
      { value: 'greater_equal', label: __('Greater Than or Equal') },
      { value: 'less_equal', label: __('Less Than or Equal') },
      { value: 'is_empty', label: __('Is Empty') },
      { value: 'is_not_empty', label: __('Is Not Empty') }
    ],
    date: [
      { value: 'equals', label: __('Equals') },
      { value: 'not_equals', label: __('Not Equals') },
      { value: 'after', label: __('After') },
      { value: 'before', label: __('Before') },
      { value: 'is_empty', label: __('Is Empty') },
      { value: 'is_not_empty', label: __('Is Not Empty') }
    ],
    select: [
      { value: 'equals', label: __('Equals') },
      { value: 'not_equals', label: __('Not Equals') },
      { value: 'is_empty', label: __('Is Empty') },
      { value: 'is_not_empty', label: __('Is Not Empty') }
    ]
  };
  return operators[fieldType] || operators.text;
};

// Helper methods for condition modal
const updateFieldType = () => {
  const field = conditionFields.value.find(f => f.value === editingCondition.value.field);
  if (field) {
    editingCondition.value.fieldType = field.type;
    editingCondition.value.operator = 'equals'; // Reset operator
    editingCondition.value.value = ''; // Reset value
  }
};

const getFieldOptions = (fieldValue) => {
  const field = conditionFields.value.find(f => f.value === fieldValue);
  return field?.options || [];
};

// Watch conditions to save to criteria field
watch(
  () => ({ conditions: customConditions.value, logic: conditionsLogic.value }),
  (newCriteria) => {
    if (segmentSelectionMode.value === 'conditions') {
      campaignData.value.criteria = JSON.stringify({
        logic: newCriteria.logic,
        conditions: newCriteria.conditions
      });
    }
  },
  { deep: true }
);

// Removed unused toast helper

// Translation helper function
const __ = (text) => text;

// Steps definition - Updated to 3 steps only
const steps = computed(() => {
  return [
    { number: 1, label: __("Campaign Information") },
    { number: 2, label: __("Content Design") },
    { number: 3, label: __("Target Segment") }
  ];
});

// Source options - 3 fixed choices only
const sources = computed(() => [
  {
    key: "search",
    title: "Search",
    description: "Search and select from Contacts and Talents",
    icon: "search",
    type: "fixed",
    source_type: "Search",
  },
  {
    key: "file",
    title: "File Import",
    description: "Import from CSV/Excel file",
    icon: "upload",
    type: "fixed",
    source_type: "File",
  },
  {
    key: "datasource",
    title: "Data Source",
    description: "Import from external data sources",
    icon: "database",
    type: "fixed",
    source_type: "DataSource",
  },
]);

// Data source type options - Only ATS now
const dataSourceTypes = computed(() => [
  {
    key: "ATS",
    title: "ATS",
    description: "Applicant Tracking System",
    icon: "briefcase",
  },
]);

// Helper function for data source icons
const getDataSourceIcon = (sourceType) => {
  const iconMap = {
    ATS: "database",
  };
  return iconMap[sourceType] || "server";
};

// Source configurations
const sourceConfigs = computed(() => ({
  search: {
    description: __("Search and select candidates from existing talent pools."),
  },
  file: {
    description: __("Import candidates from CSV or Excel files."),
  },
  datasource: {
    description: __(
      "Import candidates from external ATS data sources."
    ),
  },
}));

// Load candidates from segment
const loadCandidatesFromSegment = async (segmentId) => {
  try {
    // Get candidates from target segment through Mira Talent Pool
    const candidateSegmentResult = await miraTalentPoolStore.getList({
      filters: { segment_id: segmentId },
      fields: ["talent_id"],
    });

    if (candidateSegmentResult.success && candidateSegmentResult.data.length > 0) {
      const candidateIds = candidateSegmentResult.data.map((cs) => cs.talent_id);

      // Get the actual candidate data
      const candidateResult = await candidateStore.getList({
        filters: { name: ["in", candidateIds] },
        fields: ["name", "full_name", "email", "skills", "status"],
      });

      if (candidateResult.success) {
        return candidateResult.data.map((candidate) => ({
          id: candidate.name,
          name: candidate.full_name || candidate.name,
          title: candidate.email || "Candidate",
          source: "Talent Segment",
          email: candidate.email,
          skills: processSkills(candidate.skills),
        }));
      }
    }
    return [];
  } catch (error) {
    console.error("Error loading candidates from segment:", error);
    return [];
  }
};

// Validation rules
const rules = {
  required: (value) => !!value || __("This field is required"),
};

// Dialog options
const dialogOptions = computed(() => ({
  title: modalTitle.value,
  size: "2xl",
}));

// Computed (legacy - use isEditMode instead)
const isEditing = computed(() => isEditMode.value);

const modalTitle = computed(() => {
  if (isEditing.value) {
    return __("Edit Campaign");
  }
  return steps.value.find((step) => step.id === currentStep.value)?.title || "Create New Campaign";
});

const step1Valid = computed(() => {
  // In edit mode, be more lenient with validation - just need campaign name
  if (isEditMode.value) {
    return !!campaignData.value.campaign_name;
  }
  
  // In create mode, require all fields
  return !!(
    campaignData.value.campaign_name &&
    campaignData.value.description &&
    campaignData.value.interaction_method
  );
});

const canProceed = computed(() => {
  // Always allow clicking Continue - validation happens on click
  return true;
});

// Check if current step is the last step
const isLastStep = computed(() => {
  return currentStep.value === steps.value.length;
});

// Content editor data
const contentEditorData = computed(() => ({
  email_subject: campaignData.value.email_subject,
  email_content: campaignData.value.email_content,
  attachments: campaignData.value.attachments || [],
  message_content: campaignData.value.message_content,
  image_url: campaignData.value.image_url,
  action_buttons: campaignData.value.action_buttons || [],
  success_action: campaignData.value.success_action,
  failure_action: campaignData.value.failure_action,
  additional_actions: campaignData.value.additional_actions || {}
}));

const onSocialJobOpeningChange = async () => {
  console.log("Đã thay đổi job opening");
  const jobId = configData.value.socialConfig?.job_opening;
  console.log("ID job đã chọn:", jobId);

  if (!jobId) {
    console.log("Chưa chọn job");
    return;
  }

  try {
    console.log("Đang lấy chi tiết job...");
    const details = await getJobOpeningDetails(jobId);
    console.log("Chi tiết job:", details);

    if (details) {
      const blockBody = buildJobDetailsForTemplate(details);
      console.log("Nội dung mẫu đã tạo:", blockBody);

      // Template content will be handled by the dialog component
      console.log("Template content generated:", blockBody);
    }
  } catch (error) {
    console.error("Lỗi khi tải chi tiết công việc:", error);
  }
};
// Methods
const getStepClass = (stepNumber) => {
  if (stepNumber < currentStep.value) return "completed";
  if (stepNumber === currentStep.value) return "active";
  return "";
};

// Load data sources from API
const loadDataSources = async () => {
  loadingDataSources.value = true;
  try {
    console.log("🔍 Loading data sources from API...");
    const response = await candidateDataSourceStore.fetchDataSources({
      filters: { is_active: 1 },
      fields: [
        'name',
        'source_name', 
        'source_title',
        'notes',
        'source_type',
        'is_active'
      ],
      order_by: 'modified desc',
      page_length: 200
    });
    console.log("📊 Data sources response:", response);

    if (response && response.success) {
      dataSources.value = response.data || [];
      console.log(
        `✅ Loaded ${dataSources.value.length} data sources:`,
        dataSources.value
      );
    } else {
      console.error(
        "❌ Failed to load data sources:",
        response?.error || "Unknown error"
      );
      dataSources.value = [];
    }

    // Load connected external connections as data sources from backend
    try {
      const ec = await call(
        "mbw_mira.api.external_connections.get_connected_data_sources",
        {}
      );
      if (ec && ec.status === "success" && Array.isArray(ec.data)) {
        connectedDataSources.value = ec.data.map((item) => ({
          name: item.name,
          source_name: item.source_name,
          source_title: item.source_title,
          description: item.description,
          source_type: item.source_type,
        }));
      } else if (Array.isArray(ec)) {
        connectedDataSources.value = ec;
      } else {
        connectedDataSources.value = [];
      }
    } catch (e) {
      console.warn("⚠️ Failed to load connected external data sources", e);
      connectedDataSources.value = [];
    }
  } catch (error) {
    console.error("💥 Error loading data sources:", error);
    dataSources.value = [];
  } finally {
    loadingDataSources.value = false;
    console.log("🏁 Data sources loading finished. Count:", dataSources.value.length);
  }
};

// Styling methods for Tailwind CSS
const getStepIconClass = (stepNumber) => {
  if (stepNumber < currentStep.value) return "border-blue-500 bg-blue-500 text-white";
  if (stepNumber === currentStep.value) return "border-blue-500 bg-blue-500 text-white";
  return "border-gray-300 text-gray-400";
};

const getStepLabelClass = (stepNumber) => {
  if (stepNumber < currentStep.value) return "text-gray-600";
  if (stepNumber === currentStep.value) return "text-gray-900 font-semibold";
  return "text-gray-400";
};

const getSourceIcon = (sourceKey) => {
  const icons = {
    search: "search",
    file: "upload",
    datasource: "database",
  };
  return icons[sourceKey] || "circle";
};

const selectSource = (sourceKey) => {
  console.log("🎯 Selecting source:", sourceKey);
  console.log("📊 Available sources:", sources.value);

  selectedSource.value = sourceKey;

  // Reset data source selections when selecting new source
  selectedDataSourceType.value = "";
  selectedDataSourceId.value = "";
  filteredDataSources.value = [];
  dataSourceSelectionLevel.value = 0; // Reset level

  // Find selected source info
  const source = sources.value.find((s) => s.key === sourceKey);
  console.log("🎯 Found source:", source);

  if (source) {
    campaignData.value.source_type = source.source_type;
    console.log("🔄 Updated campaignData.source_type to:", source.source_type);

    if (source.source_type !== "DataSource") {
      campaignData.value.data_source_id = "";
      configData.value.selectedDataSource = "";
    }

    if (source.source_type === "File") {
      // Reset file selection
      campaignData.value.source_file = "";
      configData.value.selectedFile = null;
    }

    // Load data sources if datasource is selected
    if (source.key === "datasource") {
      console.log("🔄 Loading data sources for datasource selection...");
      // ✅ Since only ATS is available, auto-select it and skip type selection
      selectedDataSourceType.value = "ATS";
      dataSourceSelectionLevel.value = 2; // Skip type selection, go directly to source list
      loadDataSources();
    } else {
      dataSourceSelectionLevel.value = 0; // Reset to source level for other types
    }
  }

  console.log("✅ selectedSource now:", selectedSource.value);
};

const selectDataSourceType = (sourceType) => {
  console.log("🎯 Selecting data source type:", sourceType);
  console.log("📊 Available data sources:", dataSources.value);

  selectedDataSourceType.value = sourceType;
  selectedDataSourceId.value = "";
  dataSourceSelectionLevel.value = 2; // ✅ Move to specific source selection to show the list

  // Only ATS type is supported now
  if (sourceType === "ATS") {
    filteredDataSources.value = dataSources.value.filter(
      (ds) => ds.source_type === "ATS"
    );
  } else {
    console.warn("Unsupported source type:", sourceType);
    filteredDataSources.value = [];
  }
  console.log("✅ Filtered data sources:", filteredDataSources.value);
  console.log(" selectedDataSourceType now:", selectedDataSourceType.value);
  console.log("🎯 dataSourceSelectionLevel now:", dataSourceSelectionLevel.value);
};

const selectSpecificDataSource = async (dataSource) => {
  selectedDataSourceId.value = dataSource.name;
  campaignData.value.data_source_id = dataSource.name;
  configData.value.selectedDataSource = dataSource;
  dataSourceSelectionLevel.value = 3; // ✅ Specific data source selected - confirmed level

  // ATS data sources don't need additional configuration
  console.log("✅ ATS data source selected:", dataSource.name);
};

const clearDataSourceSelection = () => {
  console.log("🔄 Clearing data source selection...");
  selectedDataSourceId.value = "";
  campaignData.value.data_source_id = "";
  configData.value.selectedDataSource = "";
  dataSourceSelectionLevel.value = 2; // Go back to source list
  console.log("✅ Data source selection cleared");
};

// Campaign Steps Methods
const selectStepCreationMode = async (mode) => {
  stepCreationMode.value = mode;
  showStepCreation.value = true;

  if (mode === "template") {
    await loadCampaignTemplates();
  }
};

const loadCampaignTemplates = async () => {
  loading.value = true;
  try {
    const result = await campaignTemplateStore.fetchTemplates({
      filters: { is_active: 1 },
      page_length: 50,
    });

    console.log("🔍 Campaign templates result:", result);

    // Extract data array from response
    let templates = [];

    if (result && result.success && result.data && Array.isArray(result.data)) {
      templates = result.data; // ✅ Lấy array từ result.data.data
      console.log("✅ Found templates in result.data.data");
    } else if (result && result.data && Array.isArray(result.data)) {
      templates = result.data; // Fallback: direct array
      console.log("✅ Found templates in result.data (fallback)");
    } else if (result && Array.isArray(result)) {
      templates = result; // Fallback: result is direct array
      console.log("✅ Result is direct array (fallback)");
    } else {
      templates = [];
      console.log("❌ No valid templates array found");
    }

    campaignTemplates.value = templates;
    console.log(`✅ Loaded ${campaignTemplates.value.length} campaign templates`);
  } catch (error) {
    console.error("❌ Error loading campaign templates:", error);
    campaignTemplates.value = [];
  } finally {
    loading.value = false;
  }
};

const selectTemplate = async (template) => {
  selectedTemplate.value = template;

  // Load template steps and create campaign steps
  try {
    loading.value = true;
    console.log("🔍 Loading template steps for:", template.name);
    const templateData = await campaignTemplateStore.fetchTemplateById(template.name);

    console.log("📋 Template data loaded:", templateData);

    if (templateData.success && templateData.data.steps?.length > 0) {
      console.log(`✅ Found ${templateData.data.steps.length} template steps`);

      // Create CampaignStep records from template steps
      const campaignStepPromises = templateData.data.steps.map((templateStep) => {
        return createCampaignStepFromTemplate(templateStep);
      });

      const createdSteps = await Promise.all(campaignStepPromises);
      campaignSteps.value = createdSteps.filter((step) => step !== null);

      console.log(
        `📝 Prepared ${campaignSteps.value.length} campaign steps from template:`,
        campaignSteps.value
      );
    } else {
      console.log("⚠️ No template steps found");
      campaignSteps.value = [];
    }
  } catch (error) {
    console.error("❌ Error creating steps from template:", error);
    toast.error(__("Failed to create steps from template. Please try again."));
  } finally {
    loading.value = false;
  }
};

const createCampaignStepFromTemplate = async (templateStep) => {
  try {
    // Prepare step data for display (not creating DB record yet - will be done in finalize)
    const stepData = {
      campaign_step_name: templateStep.campaign_step_name,
      step_order: templateStep.step_order,
      action_type: templateStep.action_type,
      delay_in_days: templateStep.delay_in_days || 0,
      template_content: templateStep.template_content || "",
      image: templateStep.image || "", // Include image from template
      action_config: templateStep.action_config || null,
      status: "DRAFT",
      is_active: true,
      fromTemplate: true, // Mark as created from template
    };

    console.log("Prepared campaign step from template:", stepData);
    return stepData;
  } catch (error) {
    console.error("Error preparing campaign step from template:", error);
    return null;
  }
};

// Action type options for step form
const actionTypeOptions = [
  { label: __("Select action type..."), value: "", disabled: true },
  { label: __("Send Email"), value: "SEND_EMAIL" },
  { label: __("Send SMS"), value: "SEND_SMS" },
  // { label: __("Post to Facebook"), value: "POST_TO_FACEBOOK" },
  // { label: __("Post to Zalo"), value: "POST_TO_ZALO" },
  { label: __("Manual Call"), value: "MANUAL_CALL" },
  { label: __("Manual Task"), value: "MANUAL_TASK" },
];

const addManualStep = () => {
  console.log("🔍 addManualStep called");
  console.log("🔍 draftCampaign.value:", draftCampaign.value);
  console.log("🔍 showStepCreation:", showStepCreation.value);
  console.log("🔍 stepCreationMode:", stepCreationMode.value);
  console.log("🔍 showStepForm:", showStepForm.value);

  // In edit mode we can add steps directly to existing campaign
  if (!draftCampaign.value && !props.editCampaign?.name) {
    console.error("❌ Campaign context not found");
    toast.error(__("Campaign context not found. Please try again."));
    return;
  }

  console.log("✅ Draft campaign exists, proceeding...");

  // Reset form and show inline form
  stepFormSelectedJobId.value = "";
  editingStep.value = null;
  showStepForm.value = true;

  console.log("✅ Form opened, showStepForm:", showStepForm.value);
};

const editManualStep = (step) => {
  editingStep.value = step;
  showStepForm.value = true;
};

const handleStepFormSubmit = (event) => {
  const { stepData, isEditing, editingStepId } = event;
  
  // Attach selected social page to step metadata (kept in action_config)
  if (
    selectedSource.value === "datasource" &&
    selectedDataSourceType.value === "SocialNetwork"
  ) {
    const pageId = configData.value.socialConfig?.page_id;
    if (pageId) {
      stepData.action_config = stepData.action_config || {};
      stepData.action_config.target_page_id = pageId;
    }
  }

  if (isEditing) {
    // Editing existing step
    const index = campaignSteps.value.findIndex((s) => s.id === editingStepId);
    if (index !== -1) {
      campaignSteps.value[index] = {
        ...stepData,
        id: editingStepId,
        campaign: draftCampaign.value?.data?.name || draftCampaign.value?.name,
      };
    }
  } else {
    // Adding new step
    const newStep = {
      id: Date.now(), // Temporary ID
      campaign: draftCampaign.value?.data?.name || draftCampaign.value?.name,
      fromTemplate: false, // Mark as manually created
      ...stepData,
    };
    campaignSteps.value.push(newStep);
    console.log("📝 Added manual campaign step:", newStep);
  }

  // Sort steps by order
  campaignSteps.value.sort((a, b) => a.step_order - b.step_order);

  // Reset editing state
  editingStep.value = null;

  console.log("Step saved:", stepData);
};

const handleStepFormCancel = () => {
  showStepForm.value = false;
  editingStep.value = null;
};

// Method to update social config from the dialog
const updateSocialConfig = (newConfig) => {
  configData.value.socialConfig = { ...newConfig };
};

const removeStep = (step) => {
  if (confirm(__("Are you sure you want to delete this step?"))) {
    const index = campaignSteps.value.findIndex((s) => s.id === step.id);
    if (index !== -1) {
      campaignSteps.value.splice(index, 1);
      console.log("Step removed:", step);
    }
  }
};

const nextStep = async () => {
  // Validate current step before proceeding
  if (!validateCurrentStep()) {
    return; // Don't proceed if validation fails
  }

  // Save data for current step
  await saveCurrentStepData();

  // Create draft campaign when moving from step 1 to step 2 (only in create mode and first time)
  if (currentStep.value === 1 && !isEditMode.value && !draftCampaign.value) {
    try {
      await createDraftCampaign();
    } catch (error) {
      // Don't proceed if draft creation fails
      return;
    }
  }

  // Load job openings when moving to step 2 (formerly step 3)
  if (currentStep.value === 2) {
    await loadJobOpenings();
  }

  // In edit mode, max step is 3. In create mode, max step is 4
  const maxStep = isEditMode.value ? 3 : 4;
  
  if (currentStep.value < maxStep) {
    currentStep.value++;
  }
};

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
  }
};

// Removed unused candidate search helpers and state to simplify component

// Helpers for inserting job details into template
const stripHtml = (html) => {
  if (!html || typeof html !== "string") return "";
  return html
    .replace(/<[^>]*>/g, "")
    .replace(/&nbsp;/g, " ")
    .trim();
};

const buildJobDetailsForTemplate = (details) => {
  console.log("details>>>", details);
  if (!details) return "";
  const parts = [];
  if (details.description)
    parts.push(`${__("Description")}:\n${stripHtml(details.description)}`);
  if (details.requirements)
    parts.push(`${__("Requirements")}:\n${stripHtml(details.requirements)}`);
  if (details.benefits) parts.push(`${__("Benefits")}:\n${stripHtml(details.benefits)}`);
  return parts.join("\n\n");
};

// Called when job opening is chosen in the Manual Step form
const onStepJobChange = async () => {
  if (!stepFormSelectedJobId.value) {
    return;
  }
  try {
    const details = await getJobOpeningDetails(stepFormSelectedJobId.value);
    if (!details) {
      return;
    }
    const blockBody = buildJobDetailsForTemplate(details);
    console.log("Job details template generated:", blockBody);
    // Template content will be handled by the dialog component
  } catch (e) {
    console.error("Failed to build job details for step template:", e);
  }
};

// Job step methods
const loadJobOpenings = async () => {
  console.log('🔄 CampaignWizard: Starting loadJobOpenings...');
  loadingJobOpenings.value = true;
  try {
    const result = await jobOpeningStore.fetchJobOpenings({
      limit: 50,
    });

    console.log('📊 CampaignWizard: Job openings result>>>', result);

    if (result) {
      jobOpeningsList.value = result.data || [];
      console.log('✅ CampaignWizard: jobOpeningsList updated:', jobOpeningsList.value.length, 'items');
    } else {
      jobOpeningsList.value = [];
      console.log('⚠️ CampaignWizard: No job openings result');
    }
  } catch (error) {
    console.error('❌ CampaignWizard: Error loading job openings:', error);
    jobOpeningsList.value = [];
  } finally {
    loadingJobOpenings.value = false;
    console.log('🏁 CampaignWizard: loadJobOpenings finished. Loading state:', loadingJobOpenings.value);
  }
};

// const onJobOpeningChange = async () => {
//   console.log("selectedJobOpeningId.value>>>", selectedJobOpeningId.value);

//   if (!selectedJobOpeningId.value) {
//     selectedJobOpeningDetails.value = null;
//     campaignData.value.job_opening = "";
//     return;
//   }

//   campaignData.value.job_opening = selectedJobOpeningId.value;

//   try {
//     const details = await getJobOpeningDetails(selectedJobOpeningId.value);

//     console.log("details>>>", details);

//     if (details) {
//       selectedJobOpeningDetails.value = details;
//     } else {
//       selectedJobOpeningDetails.value = null;
//     }
//   } catch (error) {
//     console.error("Error loading job details:", error);
//     selectedJobOpeningDetails.value = null;
//   }
// };

// Helper function để tạo step với delay
const createStepWithDelay = async (step, index, total) => {
  // Thêm delay nhỏ giữa các step để tránh conflict
  if (index > 0) {
    await new Promise((resolve) => setTimeout(resolve, 100)); // 100ms delay
  }

  const campaignNameForSteps =
    draftCampaign.value?.data?.name || props.editCampaign?.name;
  console.log(`🔍 using campaign name for step:`, campaignNameForSteps);
  const payload = {
    campaign: campaignNameForSteps,
    campaign_step_name: step.campaign_step_name,
    step_order: step.step_order,
    action_type: step.action_type,
    delay_in_days: step.delay_in_days || 0,
    template: step.template_content || "",
    image: step.image || "",
    scheduled_at: step.scheduled_at ? formatDateForDatabase(step.scheduled_at) : null,
    action_config:
      step.action_config ||
      (stepFormSelectedPageId.value
        ? {
            page_id: stepFormSelectedPageId.value,
            template_content: step.template_content || "",
            image: step.image || "",
          }
        : null),
    status: "DRAFT",
    is_active: 1,
  };

  console.log(`📝 Creating CampaignStep ${index + 1}/${total} with payload:`, payload);
  console.log(`🖼️ Image field in payload:`, payload.image);

  console.log(`🔍 Calling campaignStepStore.createCampaignStep with payload:`, payload);
  const result = await campaignStepStore.createCampaignStep(payload);
  console.log(`✅ Step ${index + 1} created:`, result);
  console.log(`🔍 Step ${index + 1} campaign field:`, result.data?.campaign);
  console.log(`🖼️ Step ${index + 1} image field:`, result.data?.image);
  console.log(`🔍 Step ${index + 1} campaign field:`, result.data?.campaign);

  return result;
};

// Create campaign records for talents or contacts
const createCampaignRecords = async (campaignName) => {
  if (!miraTalentCampaign.value.records || miraTalentCampaign.value.records.length === 0) {
    return;
  }

  const recordType = miraTalentCampaign.value.type;
  let doctype = '';
  let recordField = '';
  
  if (recordType === 'mira_talent') {
    doctype = 'Mira Talent Campaign';
    recordField = 'talent_id';
  } else if (recordType === 'mira_contact') {
    doctype = 'Mira Contact Campaign';
    recordField = 'contact_id';
  } else {
    console.warn('Unknown record type:', recordType);
    return;
  }

  console.log(`Creating ${doctype} records for campaign:`, campaignName);
  
  try {
    // Use bulk insert API for better performance
    const bulkData = miraTalentCampaign.value.records.map(recordId => ({
      doctype: doctype,
      campaign_id: campaignName,
      [recordField]: recordId,
      status: 'ACTIVE',
      ...(recordType === 'mira_talent' && miraTalentCampaign.value.segment_id 
        ? { segment: miraTalentCampaign.value.segment_id } 
        : {})
    }));
    
    // Call custom bulk insert API
    const result = await call('mbw_mira.api.campaign.bulk_create_campaign_records', {
      records: bulkData,
      doctype: doctype
    });
    
    console.log(`Successfully created ${result.length || bulkData.length} ${doctype} records`);
    return result;
  } catch (error) {
    console.error(`Error creating ${doctype} records:`, error);
    
    // Fallback to individual inserts if bulk fails
    console.log('Falling back to individual inserts...');
    try {
      const promises = miraTalentCampaign.value.records.map(async (recordId) => {
        const payload = {
          campaign_id: campaignName,
          [recordField]: recordId,
          status: 'ACTIVE',
          ...(recordType === 'mira_talent' && miraTalentCampaign.value.segment_id 
            ? { segment: miraTalentCampaign.value.segment_id } 
            : {})
        };
        
        return await call('frappe.client.insert', {
          doc: {
            doctype: doctype,
            ...payload
          }
        });
      });
      
      const results = await Promise.all(promises);
      console.log(`Successfully created ${results.length} ${doctype} records via fallback`);
      return results;
    } catch (fallbackError) {
      console.error(`Fallback also failed:`, fallbackError);
      throw fallbackError;
    }
  }
};

// Finalize: create (draft flow) or update (edit flow)
const finalizeCampaign = async () => {
  activating.value = true;

  try {
    const editingCampaign = props.editCampaign || props.editingCampaign;
    console.log('🔍 finalizeCampaign debug:', {
      isEditing: isEditing.value,
      isEditMode: isEditMode.value,
      editCampaign: props.editCampaign,
      editingCampaign: props.editingCampaign,
      editingCampaignName: editingCampaign?.name
    });

    // EDIT MODE: update campaign fields only for now
    if (isEditMode.value && editingCampaign?.name) {
      // Prepare payload: map inputs and normalize dates
      const startISO = campaignData.value.start_date
        ? formatDateForDatabase(campaignData.value.start_date)
        : null;
      const endISO = campaignData.value.end_date
        ? formatDateForDatabase(campaignData.value.end_date)
        : null;

        console.log(miraTalentCampaign.value);

      // First update the campaign with basic info
      const updatePayload = {
        campaign_name: campaignData.value.campaign_name,
        description: campaignData.value.description,
        status: campaignData.value.status || "DRAFT",
        start_date: startISO,
        end_date: endISO,
        target_segment: campaignData.value.target_segment || null,
        source_type: campaignData.value.source_type || "",
        source_file: campaignData.value.source_file || "",
        source_config: campaignData.value.source_config || null,
        mira_talent_campaign: stringifyIfNeeded(
         miraTalentCampaign.value || null
        ),
        criteria: campaignData.value.criteria || null, // Add criteria field
        // Add social media fields
        social_page_id: configData.value.socialConfig?.page_id || "",
        social_page_name:
          socialPages.value.find(
            (p) => p.external_account_id === configData.value.socialConfig?.page_id
          )?.account_name || "",
        post_schedule_time: configData.value.socialConfig?.scheduled_at 
          ? formatDateForDatabase(configData.value.socialConfig.scheduled_at)
          : "",
        template_content: configData.value.socialConfig?.template_content || "",
        social_media_images: configData.value.socialConfig?.image 
          ? (Array.isArray(configData.value.socialConfig.image) 
              ? JSON.stringify(configData.value.socialConfig.image) 
              : configData.value.socialConfig.image)
          : "",
        
      };

      // Save or update campaign steps
      const keptIds = new Set();
      for (let i = 0; i < campaignSteps.value.length; i++) {
        const s = campaignSteps.value[i];
        const stepPayload = {
          campaign: editingCampaign.name,
          campaign_step_name: s.campaign_step_name,
          action_type: s.action_type,
          step_order: s.step_order || i + 1,
          delay_in_days: s.delay_in_days || 0,
          template: s.template_content || "",
          image: s.image || "",
          scheduled_at: s.scheduled_at || "",
        };

        if (s.id) {
          keptIds.add(s.id);
          await campaignStepStore.updateCampaignStep(s.id, stepPayload);
        } else {
          const created = await campaignStepStore.createCampaignStep(stepPayload);
          if (created?.name) keptIds.add(created.name);
        }
      }

      // Delete removed steps
      for (const oldId of originalStepIds.value) {
        if (!keptIds.has(oldId)) {
          try {
            await campaignStepStore.deleteCampaignStep(oldId);
          } catch (e) {
            console.warn("Delete step failed", oldId, e);
          }
        }
      }

      // 2) Update campaign fields
      await campaignStore.updateCampaignData(editingCampaign.name, updatePayload);

      emit("success", {
        action: "updated",
        data: { name: editingCampaign.name, ...updatePayload },
      });
      return;
    }

    if (!draftCampaign.value) {
      throw new Error(__("No draft campaign found"));
    }

    // 1) Tạo tất cả steps trước
    let stepCount = 0;
    if (campaignSteps.value.length > 0) {
      try {
        console.log(
          `🔄 Starting to create ${campaignSteps.value.length} campaign steps...`
        );

        // Tạo từng step một cách tuần tự
        for (let i = 0; i < campaignSteps.value.length; i++) {
          const step = campaignSteps.value[i];

          console.log(
            `🔍 draftCampaign.value.name::::`,
            draftCampaign.value.campaign_name
          );
          console.log(`🔍 draftCampaign.value:`, draftCampaign.value);

          // Kiểm tra xem draftCampaign có tồn tại không
          if (!draftCampaign.value || !draftCampaign.value.data.name) {
            console.error("❌ draftCampaign.value.name is missing:", draftCampaign.value);
            throw new Error("Draft campaign not found or missing name");
          }

          const payload = {
            campaign: draftCampaign.value.data.name, // ✅ ID của Campaign doctype
            campaign_step_name: step.campaign_step_name,
            step_order: step.step_order,
            action_type: step.action_type,
            delay_in_days: step.delay_in_days || 0,
            template: step.template_content || "",
            image: step.image || "",
            scheduled_at: step.scheduled_at ? formatDateForDatabase(step.scheduled_at) : null,
            action_config: step.action_config || null,
            status: "DRAFT",
            is_active: 1,
          };
          console.log("🔍 payload>>>>>>>>>>>>>>>>>>>>>>>>>>:", payload);

          console.log(
            `📝 Creating step ${i + 1}/${campaignSteps.value.length}:`,
            step.campaign_step_name
          );
          console.log(`🔗 Campaign ID:`, payload.campaign);
          console.log(`📋 Step ${i + 1} payload:`, payload);

          try {
            console.log(`🔍 Calling campaignStepStore.createCampaignStep with payload:`, payload);
            const result = await campaignStepStore.createCampaignStep(payload);

            if (result) {
              stepCount++;
              console.log(`✅ Step ${i + 1} created successfully:`, result);
              console.log(`🔗 Step ${i + 1} campaign field:`, result?.campaign);
              console.log(
                `📝 Step ${i + 1} campaign_step_name:`,
                result?.campaign_step_name
              );
            } else {
              console.error(`❌ Step ${i + 1} creation failed:`, result);
            }
          } catch (stepError) {
            console.error(`❌ Error creating step ${i + 1}:`, stepError);
            // Tiếp tục với step tiếp theo thay vì dừng hoàn toàn
          }

          // Thêm delay nhỏ giữa các step để tránh conflict
          if (i < campaignSteps.value.length - 1) {
            await new Promise((resolve) => setTimeout(resolve, 200)); // 200ms delay
          }
        }

        console.log(
          `📊 Final result: Created ${stepCount}/${campaignSteps.value.length} campaign steps`
        );
      } catch (e) {
        console.error("❌ Create steps failed", e);
        toast.error(__("Failed to create steps. Please try again."));
        return;
      }
    }

    // Build select_pages JSON from steps if SocialNetwork and pages selected
    let selectPages = [];
    if (
      selectedSource.value === "datasource" &&
      selectedDataSourceType.value === "SocialNetwork"
    ) {
      // Aggregate unique page ids referenced in steps
      const pageIds = new Set();
      campaignSteps.value.forEach((s) => {
        const pageId = s?.action_config?.target_page_id;
        if (pageId) pageIds.add(pageId);
      });
      selectPages = Array.from(pageIds).map((pid) => ({ page_id: pid }));
    }

    // 2) Update campaign sau khi đã có step
    const startISO =
      formatDateForDatabase(campaignData.value.start_date) || getCurrentDatabaseDateTime();
    const endISO =
      formatDateForDatabase(campaignData.value.end_date) ||
      addTimeToDate(new Date(), 30, 'days');

    console.log("🔍 Finalizing campaign with source_type values:");
    console.log("  - draftCampaign.source_type:", draftCampaign.value.source_type);
    console.log("  - campaignData.source_type:", campaignData.value.source_type);
    console.log("  - selectedSource:", selectedSource.value);

    const campaignUpdatePayload = {
      campaign_name:
        campaignData.value.campaign_name || draftCampaign.value.campaign_name,
      description: campaignData.value.description || draftCampaign.value.description,
      type: campaignData.value.type || draftCampaign.value.type,
      status: campaignData.value.status || draftCampaign.value.status || "DRAFT",
      start_date: startISO,
      end_date: endISO,
      is_active: false,
      source_type:
        draftCampaign.value.source_type || campaignData.value.source_type || "Gathering",
      template_used: selectedTemplate.value?.name || null,
      steps_count: stepCount,
      source_file:
        campaignData.value.source_file || draftCampaign.value.source_file || "",
      source_config:
        campaignData.value.source_config || draftCampaign.value.source_config || null,
      target_segment:
        campaignData.value.target_segment || draftCampaign.value.target_segment || null,
      job_opening:
        campaignData.value.job_opening || draftCampaign.value.job_opening || null,
      select_pages: selectPages.length ? JSON.stringify(selectPages) : null,
      // Add social media fields
      social_page_id:
        configData.value.socialConfig?.page_id ||
        draftCampaign.value.social_page_id ||
        "",
      social_page_name:
        socialPages.value.find(
          (p) => p.external_account_id === configData.value.socialConfig?.page_id
        )?.account_name ||
        draftCampaign.value.social_page_name ||
        "",
      post_schedule_time:
        configData.value.socialConfig?.scheduled_at ||
        draftCampaign.value.post_schedule_time ||
        "",
      template_content:
        configData.value.socialConfig?.template_content ||
        draftCampaign.value.template_content ||
        "",
      social_media_images:
        configData.value.socialConfig?.image ||
        draftCampaign.value.social_media_images ||
        "",
      mira_talent_campaign: JSON.stringify(
        Array.isArray(miraTalentCampaign.value)
          ? miraTalentCampaign.value
          : miraTalentCampaign.value
            ? [miraTalentCampaign.value]
            : []
      ),
    };
    
    // Add file data if source is file
    if (selectedSource.value === "file" && configData.value.sourceTarget) {
      campaignUpdatePayload.source_target = configData.value.sourceTarget;
    }

    console.log(" Campaign update payload:", campaignUpdatePayload);

    const campaignResult = await campaignStore.updateCampaignData(
      draftCampaign.value.data.name,
      campaignUpdatePayload
    );

    console.log("📋 Campaign update result:", campaignResult);

    if (!campaignResult) {
      throw new Error("Failed to finalize campaign");
    }

    // 3) Create campaign records for selected talents/contacts
    if (selectedSource.value === 'search' && miraTalentCampaign.value.records?.length > 0) {
      try {
        await createCampaignRecords(draftCampaign.value.data.name);
        console.log('✅ Campaign records created successfully');
      } catch (recordError) {
        console.error('❌ Error creating campaign records:', recordError);
        // Don't fail the entire process, just log the error
      }
    }

    // 4) Done
    emit("success", { action: "create", data: campaignResult });
    closeWizard();
  } catch (error) {
    console.error("Error finalizing campaign:", error);

    let msg = __("An error occurred while finalizing the campaign");
    if (error.message.includes("campaign_name"))
      msg = __("Campaign name is invalid or already exists");
    else if (error.message.includes("validation"))
      msg = __("Input data is not in the correct format");
    else if (error.message.includes("network") || error.message.includes("fetch"))
      msg = __("Network connection error, please try again");
    else if (error.message) msg = error.message;

    toast.error(msg);
  } finally {
    activating.value = false;
  }
};

// Method to update campaign name from header
const updateCampaignName = (newName) => {
  campaignData.value.campaign_name = newName;
  // Auto-save will be triggered by watcher
};

// Handle stepper click to navigate between steps
const handleStepClick = (stepNumber) => {
  // Only allow navigation to completed steps or current step
  if (stepNumber <= currentStep.value) {
    currentStep.value = stepNumber;
  }
};

// Debounced auto-save function (like Google Drive)
const debouncedAutoSave = () => {
  if (autoSaveTimer.value) {
    clearTimeout(autoSaveTimer.value);
  }
  
  autoSaveTimer.value = setTimeout(async () => {
    await autoSave();
  }, 2000); // Auto-save after 2 seconds of inactivity
};

const stringifyIfNeeded = (value) => {
  if (Array.isArray(value)) {
    return JSON.stringify(value);
  }
  return value;
};


// Auto-save function (like Google Drive)
const autoSave = async () => {
  try {
    const campaignId = draftCampaign.value?.data?.name || editingCampaignData.value?.name;
    
    if (!campaignId || isAutoSaving.value) return;

    // Set flags to prevent infinite loop
    isAutoSaving.value = true;
    isUpdatingFromAutoSave.value = true;

    // Prepare mira_talent_campaign config for step 2 (Content Design)
    let miraTalentCampaignConfig = null;
    if (currentStep.value === 2) {
      miraTalentCampaignConfig = {
        interaction_method: campaignData.value.interaction_method,
        content_config: {
          email_subject: campaignData.value.email_subject,
          email_content: campaignData.value.email_content,
          attachments: campaignData.value.attachments || [],
          message_content: campaignData.value.message_content,
          image_url: campaignData.value.image_url,
          action_buttons: campaignData.value.action_buttons || [],
          success_action: campaignData.value.success_action,
          failure_action: campaignData.value.failure_action,
        },
        additional_actions: campaignData.value.additional_actions || existingConfig?.additional_actions || {},
        step: currentStep.value,
        updated_at: new Date().toISOString(),
        auto_saved: true
      };
    }

    const updateData = {
      campaign_name: campaignData.value.campaign_name,
      description: campaignData.value.description,
      type: campaignData.value.type,
      status: campaignData.value.status,
      interaction_method: campaignData.value.interaction_method,
      start_date: campaignData.value.start_date,
      end_date: campaignData.value.end_date,
      target_segment: campaignData.value.target_segment,
      source_type: campaignData.value.source_type,
      data_source_id: campaignData.value.data_source_id,
      email_subject: campaignData.value.email_subject,
      email_content: campaignData.value.email_content,
      message_content: campaignData.value.message_content,
      success_action: campaignData.value.success_action,
      failure_action: campaignData.value.failure_action,
      // Save mira_talent_campaign config as JSON for step 2
      ...(miraTalentCampaignConfig && {
        mira_talent_campaign: JSON.stringify(miraTalentCampaignConfig)
      })
    };
    
    await campaignStore.updateCampaignData(campaignId, updateData);
    console.log('✅ Auto-saved successfully');
    if (miraTalentCampaignConfig) {
      console.log('📝 Auto-saved mira_talent_campaign config:', miraTalentCampaignConfig);
    }
    
    // Show success indicator
    lastSaveSuccess.value = true;
    showSaveSuccess.value = true;
    
    // Hide success indicator after 3 seconds
    setTimeout(() => {
      showSaveSuccess.value = false;
    }, 3000);
    
  } catch (error) {
    console.error('❌ Auto-save error:', error);
    lastSaveSuccess.value = false;
    showSaveSuccess.value = false;
    // Don't show alert for auto-save errors to avoid interrupting user
  } finally {
    isAutoSaving.value = false;
    // Reset flag after a short delay to allow any pending updates to complete
    setTimeout(() => {
      isUpdatingFromAutoSave.value = false;
    }, 100);
  }
};

// Validate current step before proceeding
const validateCurrentStep = () => {
  if (currentStep.value === 1) {
    // Step 1: Validate campaign info
    const errors = [];
    
    if (!campaignData.value.campaign_name?.trim()) {
      errors.push(__("Campaign name is required"));
    }
    
    if (!isEditMode.value && !campaignData.value.description?.trim()) {
      errors.push(__("Description is required"));
    }
    
    if (!campaignData.value.interaction_method) {
      errors.push(__("Please select an interaction method"));
    }
    
    if (errors.length > 0) {
      // Hiển thị từng lỗi riêng biệt
      errors.forEach(error => {
        toast.error(error);
      });
      return false;
    }
    
    return true;
  }
  
  if (currentStep.value === 2) {
    // Step 2: Validate target segment selection
    // Add validation if needed
    return true;
  }
  
  if (currentStep.value === 3) {
    // Step 3: Validate content design
    // Add validation if needed
    return true;
  }
  
  // Other steps - add validation as needed
  return true;
};

const saveCurrentStepData = async () => {
  try {
    const campaignId = draftCampaign.value?.data?.name || editingCampaignData.value?.name;
    
    if (!campaignId) {
      console.warn('⚠️ No campaign ID available for saving');
      return;
    }

    console.log('💾 Saving current step data for campaign:', campaignId);
    
    // Prepare mira_talent_campaign config - preserve existing data and update for current step
    let miraTalentCampaignConfig = null;
    
    // Try to get existing config first
    let existingConfig = null;
    try {
      if (draftCampaign.value?.data?.mira_talent_campaign) {
        existingConfig = JSON.parse(draftCampaign.value.data.mira_talent_campaign);
      } else if (editingCampaignData.value?.mira_talent_campaign) {
        existingConfig = JSON.parse(editingCampaignData.value.mira_talent_campaign);
      }
    } catch (e) {
      console.warn('Failed to parse existing mira_talent_campaign:', e);
    }
    
    if (currentStep.value === 2) {
      // For step 2, create/update the config
      miraTalentCampaignConfig = {
        ...existingConfig, // Preserve existing data
        interaction_method: campaignData.value.interaction_method,
        content_config: {
          email_subject: campaignData.value.email_subject,
          email_content: campaignData.value.email_content,
          attachments: campaignData.value.attachments || [],
          message_content: campaignData.value.message_content,
          image_url: campaignData.value.image_url,
          action_buttons: campaignData.value.action_buttons || [],
          success_action: campaignData.value.success_action,
          failure_action: campaignData.value.failure_action,
        },
        additional_actions: campaignData.value.additional_actions || existingConfig?.additional_actions || {},
        step: currentStep.value,
        updated_at: new Date().toISOString()
      };
    } else if (existingConfig) {
      // For other steps, preserve existing config but don't overwrite
      miraTalentCampaignConfig = existingConfig;
    }
    
    const updateData = {
      campaign_name: campaignData.value.campaign_name,
      description: campaignData.value.description,
      interaction_method: campaignData.value.interaction_method,
      start_date: formatDateForDatabase(campaignData.value.start_date),
      end_date: formatDateForDatabase(campaignData.value.end_date),
      // Content design fields
      email_subject: campaignData.value.email_subject,
      email_content: campaignData.value.email_content,
      attachments: JSON.stringify(campaignData.value.attachments || []),
      message_content: campaignData.value.message_content,
      image_url: campaignData.value.image_url,
      action_buttons: JSON.stringify(campaignData.value.action_buttons || []),
      success_action: campaignData.value.success_action,
      failure_action: campaignData.value.failure_action,
      // Save mira_talent_campaign config as JSON
      ...(miraTalentCampaignConfig && {
        mira_talent_campaign: JSON.stringify(miraTalentCampaignConfig)
      })
    };
    
    await campaignStore.updateCampaignData(campaignId, updateData);
    
    // Show success indicator
    lastSaveSuccess.value = true;
    setTimeout(() => {
      lastSaveSuccess.value = false;
    }, 2000);
    
    console.log('✅ Current step data saved successfully');
    if (miraTalentCampaignConfig) {
      console.log('📝 Saved mira_talent_campaign config:', miraTalentCampaignConfig);
    }
  } catch (error) {
    console.error('❌ Error saving step data:', error);
    toast.error(__('Failed to save data. Please try again.'));
    throw error; // Re-throw to prevent step change
  }
};

// Content editor handlers
const handleContentUpdate = (updatedContent) => {
  // Prevent infinite loop: skip if update is from auto-save or currently auto-saving
  if (isAutoSaving.value || isUpdatingFromAutoSave.value) {
    console.log('⏭️ Skipping content update - auto-save cycle in progress');
    return;
  }
  
  // Update campaign data with content from editor
  Object.assign(campaignData.value, updatedContent);
  
  // Store additional_actions as-is (don't convert to follow_up_actions/automation_rules)
  if (updatedContent.additional_actions) {
    campaignData.value.additional_actions = updatedContent.additional_actions;
  }
  
  console.log('📝 Content updated:', updatedContent);
  console.log('📝 Additional actions:', campaignData.value.additional_actions);
  
  // Auto-save when content is updated in step 2
  if (currentStep.value === 2 && draftCampaign.value?.data?.name) {
    // Debounced auto-save to avoid too many API calls
    debouncedAutoSave();
  }
};

const handleContentSave = async () => {
  console.log('💾 Saving content from editor');
  await saveCurrentStepData();
};

const handleContentPreview = (content) => {
  console.log('👁️ Previewing content:', content);
  // TODO: Implement preview modal
  toast.info(__('Preview feature will be implemented soon'));
};

// Method to save campaign in edit mode
const saveEditCampaign = async () => {
  const editingCampaign = props.editCampaign || props.editingCampaign;
  if (!editingCampaign?.name) {
    throw new Error('No campaign to edit');
  }

  // Prepare payload: map inputs and normalize dates
  const startISO = campaignData.value.start_date
    ? formatDateForDatabase(campaignData.value.start_date)
    : null;
  const endISO = campaignData.value.end_date
    ? formatDateForDatabase(campaignData.value.end_date)
    : null;

  // First update the campaign with basic info
  const updatePayload = {
    campaign_name: campaignData.value.campaign_name,
    description: campaignData.value.description,
    status: campaignData.value.status || "DRAFT",
    start_date: startISO,
    end_date: endISO,
    target_segment: campaignData.value.target_segment || null,
    source_type: campaignData.value.source_type || "",
    source_file: campaignData.value.source_file || "",
    source_config: campaignData.value.source_config || null,
    mira_talent_campaign: stringifyIfNeeded(
     miraTalentCampaign.value || null
    ),
    criteria: campaignData.value.criteria || null, // Add criteria field
    // Add social media fields
    social_page_id: configData.value.socialConfig?.page_id || "",
    social_page_name:
      socialPages.value.find(
        (p) => p.external_account_id === configData.value.socialConfig?.page_id
      )?.account_name || "",
    post_schedule_time: configData.value.socialConfig?.scheduled_at 
      ? formatDateForDatabase(configData.value.socialConfig.scheduled_at)
      : "",
    template_content: configData.value.socialConfig?.template_content || "",
    social_media_images: configData.value.socialConfig?.image 
      ? (Array.isArray(configData.value.socialConfig.image) 
          ? JSON.stringify(configData.value.socialConfig.image) 
          : configData.value.socialConfig.image)
      : "",
  };

  // Save or update campaign steps
  const keptIds = new Set();
  for (let i = 0; i < campaignSteps.value.length; i++) {
    const s = campaignSteps.value[i];
    const stepPayload = {
      campaign: editingCampaign.name,
      campaign_step_name: s.campaign_step_name,
      action_type: s.action_type,
      step_order: s.step_order || i + 1,
      delay_in_days: s.delay_in_days || 0,
      template: s.template_content || "",
      image: s.image || "",
      scheduled_at: s.scheduled_at || "",
    };

    if (s.id) {
      keptIds.add(s.id);
      await campaignStepStore.updateCampaignStep(s.id, stepPayload);
    } else {
      const created = await campaignStepStore.createCampaignStep(stepPayload);
      if (created?.name) keptIds.add(created.name);
    }
  }

  // Delete removed steps
  for (const oldId of originalStepIds.value) {
    if (!keptIds.has(oldId)) {
      try {
        await campaignStepStore.deleteCampaignStep(oldId);
      } catch (e) {
        console.warn("Delete step failed", oldId, e);
      }
    }
  }

  // Update campaign fields
  await campaignStore.updateCampaignData(editingCampaign.name, updatePayload);

  emit("success", {
    action: "updated",
    data: { name: editingCampaign.name, ...updatePayload },
  });
};

// Method to save draft (legacy - kept for compatibility)
const saveDraft = async () => {
  try {
    // In edit mode, save the entire campaign
    if (isEditMode.value) {
      await saveEditCampaign();
      toast.success(__('Campaign saved successfully'));
    } else {
      // In create mode, just save current step data
      await saveCurrentStepData();
      toast.success(__('Draft saved successfully'));
    }
  } catch (error) {
    console.error('Save failed:', error);
    toast.error(__('Failed to save: ') + error.message);
  }
};

const closeWizard = () => {
  show.value = false;
  // Reset state
  currentStep.value = 1;
  campaignData.value = {
    campaign_name: "",
    description: "",
    type: "",
    status: "DRAFT",
    interaction_method: "",
    start_date: "",
    end_date: "",
    target_segment: "",
    source_type: "Gathering",
    source_file: null,
    source_config: null,
    data_source_id: null,
    email_subject: "",
    email_content: "",
    attachments: [],
    message_content: "",
    image_url: "",
    action_buttons: [],
    success_action: "",
    failure_action: "",
    // Additional actions fields
    follow_up_actions: [],
    automation_rules: [],
    additional_actions: {},
  };
  selectedSource.value = props.preselectedSegment ? "search" : "";
  selectedDataSourceType.value = "";
  selectedDataSourceId.value = "";
  configData.value = {
    selectedSegment: props.preselectedSegment || "",
    selectedDataSource: "",
    selectedFile: null,
    uploadedFileUrl: "",
    filePreview: [],
    fileHeaders: [],
    socialConfig: {
      page_id: "",
      scheduled_at: "",
      job_opening: "",
      image: "",
    },
  };
  filteredDataSources.value = [];
  // cleaned: removed deprecated showCandidates/selectedCandidates
  loading.value = false;
  activating.value = false;

  // Reset new campaign steps states
  campaignSteps.value = [];
  selectedTemplate.value = null;
  campaignTemplates.value = [];
  showStepCreation.value = false;
  stepCreationMode.value = "";
  showStepForm.value = false;
  editingStep.value = null;
  // Step form state is now handled by the dialog component
  draftCampaign.value = null;

  // Reset job step states
  jobOpeningsList.value = [];
  loadingJobOpenings.value = false;
  selectedJobOpeningDetails.value = null;

  // Reset search states
  searchSource.value = null;
  searchKeyword.value = "";
  selectedSegment.value = "";
  records.value = [];
  selectedCandidates.value = [];
  miraTalentCampaign.value = { type: null, records: [] };
  currentPage.value = 1;
  pageSize.value = 20;
  totalRecords.value = 0;
  searchLoading.value = false;
};

// Load data sources on component mount
onMounted(async () => {
  console.log("🚀 CampaignWizard mounted, loading initial data...");
  await loadDataSources();
  console.log("✅ Initial data loading completed");
});

// Create draft campaign when moving from step 1
const createDraftCampaign = async () => {
  if (draftCampaign.value) return; // Already created
  console.log("🔍 draftCampaign.value>>>>>>>>>>>>>>>>>>>>>>>>>>:", draftCampaign.value);
  draftCampaignLoading.value = true;
  try {
    console.log("🔧 Creating draft campaign with user input...");
    // Map selectedSource to source_type (DataSource | File | Search)
    const sourceTypeMap = { datasource: "DataSource", file: "File", search: "Search" };
    const mappedSourceType = selectedSource.value 
      ? sourceTypeMap[selectedSource.value] || campaignData.value.source_type || "Search"
      : "Gathering"; // Không chọn nguồn thì để Gathering
    
    console.log("🔍 Draft campaign source_type mapping:");
    console.log("  - selectedSource:", selectedSource.value);
    console.log("  - campaignData.source_type:", campaignData.value.source_type);
    console.log("  - mappedSourceType:", mappedSourceType);

    const startISO =
      formatDateForDatabase(campaignData.value.start_date) || getCurrentDatabaseDateTime();
    const endISO =
      formatDateForDatabase(campaignData.value.end_date) ||
      addTimeToDate(new Date(), 30, 'days');

    const draftPayload = {
      campaign_name:
        campaignData.value.campaign_name ||
        __("Draft Campaign") + " " + new Date().toLocaleString(),
      description:
        campaignData.value.description || __("Draft campaign - to be configured"),
      type: campaignData.value.type || "NURTURING",
      status: campaignData.value.status || "DRAFT",
      start_date: startISO,
      end_date: endISO,
      is_active: false,
      source_type: mappedSourceType,
      criteria: campaignData.value.criteria || null, // Add criteria field
      // Add social media fields
      social_page_id: configData.value.socialConfig?.page_id || "",
      social_page_name:
        socialPages.value.find(
          (p) => p.external_account_id === configData.value.socialConfig?.page_id
        )?.account_name || "",
      post_schedule_time: configData.value.socialConfig?.scheduled_at || "",
      template_content: configData.value.socialConfig?.template_content || "",
      social_media_images: configData.value.socialConfig?.image || "",
      // Add search data for manual selection
      ...(selectedSource.value === "search" && miraTalentCampaign.value.records.length > 0
        ? {
            mira_talent_campaign: JSON.stringify(miraTalentCampaign.value),
            source_config: JSON.stringify({
              source_target: miraTalentCampaign.value.type || 'mira_contact',
              segment_id: miraTalentCampaign.value.segment_id || '',
              selected_records: miraTalentCampaign.value.records || []
            })
          }
        : {}),
    };
    console.log("🔍 draftPayload>>>>>>>>>>>>>>>>>>>>>>>>>>:", draftPayload);
    
    // Test API connection first
    const connectionOk = await campaignStore.testApiConnection();
    if (!connectionOk) {
      throw new Error('API connection failed. Please check your network connection.');
    }
    
    try {
      // Try custom API first, then fallback to standard method
      console.log("🔄 Attempting to create campaign via custom API...")
      let result;
      
      try {
        result = await campaignStore.createCampaignViaCustomAPI(draftPayload);
        console.log("✅ Custom API success:", result);
      } catch (customApiError) {
        console.log("⚠️ Custom API failed, trying standard method...", customApiError.message);
        result = await campaignStore.submitNewCampaign(draftPayload);
        console.log("✅ Standard API success:", result);
      }
      
      console.log("🔍 Final result:", result);
      
      if (result && result.success && result.data) {
        draftCampaign.value = { data: result.data };
        console.log("✅ Draft campaign created:", result.data.name);
      } else if (result && result.name) {
        // Handle direct response format
        draftCampaign.value = { data: result };
        console.log("✅ Draft campaign created:", result.name);
      } else {
        throw new Error('Invalid response from server');
      }

      // Sync start/end back to UI (convert ISO -> datetime-local string)
      try {
        if (draftCampaign.value.data.start_date) {
          const d = new Date(draftCampaign.value.data.start_date);
          campaignData.value.start_date = toLocalDatetimeInput(d);
        }
        if (draftCampaign.value.data.end_date) {
          const d2 = new Date(draftCampaign.value.data.end_date);
          campaignData.value.end_date = toLocalDatetimeInput(d2);
        }
      } catch (e) {
        console.warn("Failed to map campaign dates to inputs", e);
      }

      // Mira Campaign Social will be created later when social config is confirmed

      // Emit event to refresh the campaign list
      emit("draft-created", draftCampaign.value);
    } catch (apiError) {
      console.error("❌ API Error creating draft campaign:", apiError);
      throw new Error("Failed to create draft campaign: " + (apiError.message || 'Unknown error'));
    }
  } catch (error) {
    console.error("❌ Error creating draft campaign:", error);
    toast.error(__("Failed to create draft campaign. Please try again."));

    // Prevent moving to next step if draft creation fails
    throw error;
  } finally {
    draftCampaignLoading.value = false;
  }
};

// Watch configData để đồng bộ mapping file vào campaignData.source_config khi chọn nguồn là file
watch(
  [configData, selectedSource],
  ([cfg, src]) => {
    if (src !== "file") return;

    const mappingEntries = Object.entries(cfg?.mapping || {}).filter(([, f]) => f);
    if (!mappingEntries.length) return;

    const field_mapping = mappingEntries.map(([column_name, field_name]) => ({
      column_name,
      field_name,
    }));

    campaignData.value.source_file = cfg?.selectedFile?.name || ""; // để BE biết file
    
    // Ensure source_type is set correctly for file
    campaignData.value.source_type = "File";
    
    console.log('📁 Updated source_file:', campaignData.value.source_file);
    console.log('🎯 Updated source_type:', campaignData.value.source_type);
    
    // Determine doctype based on sourceTarget
    const metaDoctype = cfg?.sourceTarget === 'talent' ? 'Mira Talent' : 'Mira Contact';
    
    campaignData.value.source_config = JSON.stringify({
      file_name: cfg?.selectedFile?.name || "",
      meta_doctype: metaDoctype,
      source_target: cfg?.sourceTarget || 'contact', // Add source_target field
      field_mapping,
    });
  },
  { deep: true }
);

// When the manual step form opens, ensure job openings list is loaded
watch(showStepForm, async (val) => {
  if (val && jobOpeningsList.value.length === 0) {
    await loadJobOpenings();
  }
  // Also load social pages when SocialNetwork selected
  if (
    val &&
    selectedSource.value === "datasource" &&
    selectedDataSourceType.value === "SocialNetwork"
  ) {
    await loadSocialPages();
    // Auto-fill from socialConfig
    if (configData.value.socialConfig) {
      stepFormSelectedPageId.value = configData.value.socialConfig.page_id || "";
      stepFormSelectedJobId.value = configData.value.socialConfig.job_opening || "";
      // Other social config data is now handled by the dialog components
    }
  }
});

// Load existing steps for edit mode
const loadExistingSteps = async (campaignName) => {
  try {
    const result = await campaignStepStore.getFilteredCampaignSteps({
      campaign: campaignName,
      order_by: "step_order asc",
      limit: 1000
    });
    const rows = result?.data || result?.data?.data || [];
    campaignSteps.value = (rows || []).map((r) => ({
      id: r.name,
      campaign_step_name: r.campaign_step_name,
      action_type: r.action_type,
      step_order: r.step_order,
      delay_in_days: r.delay_in_days,
      template_content: r.template,
      image: r.image || "",
      scheduled_at: r.scheduled_at || "",
      fromTemplate: false,
    }));
    originalStepIds.value = (rows || []).map((r) => r.name);
  } catch (e) {
    console.warn("Failed to load existing campaign steps", e);
    campaignSteps.value = [];
  } finally {
    // no-op
  }
};

// Watchers
// Sync v-model from parent to internal state
watch(
  () => props.modelValue,
  (newVal) => {
    show.value = newVal;
  }
);

// Existing watcher: emit back to parent and handle open initialization
watch(show, async (newVal) => {
  emit("update:modelValue", newVal);
  if (!newVal && draftCampaign.value) {
    // Clean up draft campaign if wizard is closed without completion
    // TODO: Optionally delete draft campaign
  }
  // Khi mở wizard lần đầu, set mặc định start_date = now và end_date = start_date + 30 ngày nếu chưa có
  if (newVal) {
    try {
      // Prefill when editing
      if (props.editCampaign || props.editingCampaign) {
        const ec = props.editCampaign || props.editingCampaign;
        // Fetch full campaign doc to get select_pages/source_config
        let full = null;
        try {
          full = await campaignStore.getCampaignDetails(ec.name);
        } catch (e) {
          full = null;
        }
        campaignData.value.campaign_name = ec.campaign_name || ec.name || "";
        campaignData.value.description = ec.description || "";
        campaignData.value.type = ec.type || "MARKETING";
        campaignData.value.status = ec.status || campaignData.value.status;
        campaignData.value.interaction_method = ec.interaction_method || "EMAIL"; // Default fallback
        campaignData.value.target_segment =
          ec.target_segment || campaignData.value.target_segment || "";
        campaignData.value.criteria = ec.criteria || ""; // Load criteria from database
        
        // Parse and restore custom conditions if exists
        if (ec.criteria) {
          try {
            const parsedCriteria = JSON.parse(ec.criteria);
            conditionsLogic.value = parsedCriteria.logic || 'any';
            customConditions.value = parsedCriteria.conditions || [];
            segmentSelectionMode.value = 'conditions'; // Set to conditions mode
          } catch (e) {
            console.warn('Failed to parse criteria:', e);
            customConditions.value = [];
            conditionsLogic.value = 'any';
          }
        } else {
          // Reset conditions if no criteria
          customConditions.value = [];
          conditionsLogic.value = 'any';
          segmentSelectionMode.value = ''; // Reset selection mode
        }
        campaignData.value.start_date =
          ec.start_date || campaignData.value.start_date || "";
        campaignData.value.end_date = ec.end_date || campaignData.value.end_date || "";
        
        // Content design fields
        campaignData.value.email_subject = ec.email_subject || "";
        campaignData.value.email_content = ec.email_content || "";
        try {
          campaignData.value.attachments = ec.attachments ? JSON.parse(ec.attachments) : [];
        } catch (e) {
          console.warn('Failed to parse attachments:', e);
          campaignData.value.attachments = [];
        }
        campaignData.value.message_content = ec.message_content || "";
        campaignData.value.image_url = ec.image_url || "";
        try {
          campaignData.value.action_buttons = ec.action_buttons ? JSON.parse(ec.action_buttons) : [];
        } catch (e) {
          console.warn('Failed to parse action_buttons:', e);
          campaignData.value.action_buttons = [];
        }
        campaignData.value.success_action = ec.success_action || "";
        campaignData.value.failure_action = ec.failure_action || "";
        
        // Load mira_talent_campaign config if exists
        if (ec.mira_talent_campaign) {
          try {
            const miraTalentConfig = JSON.parse(ec.mira_talent_campaign);
            console.log('📝 Loading mira_talent_campaign config:', miraTalentConfig);
            
            // Restore content config if available
            if (miraTalentConfig.content_config) {
              const contentConfig = miraTalentConfig.content_config;
              campaignData.value.email_subject = contentConfig.email_subject || campaignData.value.email_subject;
              campaignData.value.email_content = contentConfig.email_content || campaignData.value.email_content;
              campaignData.value.attachments = contentConfig.attachments || campaignData.value.attachments;
              campaignData.value.message_content = contentConfig.message_content || campaignData.value.message_content;
              campaignData.value.image_url = contentConfig.image_url || campaignData.value.image_url;
              campaignData.value.action_buttons = contentConfig.action_buttons || campaignData.value.action_buttons;
              campaignData.value.success_action = contentConfig.success_action || campaignData.value.success_action;
              campaignData.value.failure_action = contentConfig.failure_action || campaignData.value.failure_action;
            }
            
            // Restore additional actions if available
            if (miraTalentConfig.additional_actions) {
              campaignData.value.additional_actions = miraTalentConfig.additional_actions;
              // Also restore legacy fields for backward compatibility
              campaignData.value.follow_up_actions = miraTalentConfig.additional_actions.follow_up_actions || [];
              campaignData.value.automation_rules = miraTalentConfig.additional_actions.automation_rules || [];
            }
            
            console.log('✅ Successfully loaded mira_talent_campaign config');
          } catch (e) {
            console.warn('Failed to parse mira_talent_campaign:', e);
          }
        }
        
        // Source hints
        if (ec.source_type) {
          campaignData.value.source_type = ec.source_type;
          // Best-effort map to selectedSource UI key
          if (ec.source_type === "File") {
            selectedSource.value = "file";
          } else if (ec.data_source_id) {
            selectedSource.value = "datasource";
            selectedDataSourceId.value = ec.data_source_id;
            campaignData.value.data_source_id = ec.data_source_id;
            // Assume selection completed in edit mode
            dataSourceSelectionLevel.value = 3;
          } else {
            selectedSource.value = "search";
          }
        }
        // Restore selectedDataSource object and load pages for SocialNetwork
        if (!dataSources.value || dataSources.value.length === 0) {
          await loadDataSources();
        }
        if (selectedDataSourceId.value) {
          const ds = (dataSources.value || []).find(
            (d) => d.name === selectedDataSourceId.value
          );
          if (ds) {
            configData.value.selectedDataSource = ds;
            await loadSocialPages();
          }
        }
        // Restore selected page from campaign.select_pages if present
        try {
          const sp = full?.data?.select_pages;
          let pages = null;
          if (typeof sp === "string") {
            pages = JSON.parse(sp);
          } else if (Array.isArray(sp)) {
            pages = sp;
          }
          if (Array.isArray(pages) && pages.length > 0) {
            const first = pages[0];
            if (first?.page_id) {
              stepFormSelectedPageId.value = first.page_id;
              configData.value.socialConfig = {
                ...(configData.value.socialConfig || {}),
                page_id: first.page_id,
              };
            }
          }
        } catch (e) {}
        // After prefill, load existing steps and jump to Review step (Step 4) so user sees them
        loadExistingSteps(ec.name).then(() => {
          if (campaignSteps.value && campaignSteps.value.length > 0) {
            currentStep.value = 4;
            showStepCreation.value = true;
            stepCreationMode.value = "manual";
          }
        });
      }
      if (!campaignData.value.start_date) {
        const now = new Date();
        campaignData.value.start_date = toLocalDatetimeInput(now);
      }
      if (!campaignData.value.end_date) {
        const base = campaignData.value.start_date
          ? new Date(campaignData.value.start_date)
          : new Date();
        const plus30 = new Date(base.getTime() + 30 * 24 * 60 * 60 * 1000);
        campaignData.value.end_date = toLocalDatetimeInput(plus30);
      }
    } catch (e) {
      console.warn("Failed to initialize start/end dates", e);
    }
  }
});

// Đồng bộ target_segment với configData.selectedSegment
watch(
  () => configData.value.selectedSegment,
  (val) => {
    campaignData.value.target_segment = val;
  }
);

// Social pages state
const socialPages = ref([]);
const externalConnections = ref([]);
const loadingPages = ref(false);
const loadingConnections = ref(false);
const stepFormSelectedPageId = ref("");
const scheduledAtInput = ref(null);

// Load external connections for social media configuration
const loadExternalConnections = async () => {
  try {
    loadingConnections.value = true;
    const response = await call('frappe.client.get_list', {
      doctype: 'Mira External Connection',
      fields: ['name', 'tenant_name', 'platform_type', 'connection_status'],
      filters: [['connection_status', '=', 'Connected']],
      limit_page_length: 100
    });
    externalConnections.value = response || [];
    console.log('✅ Campaign Wizard: Loaded external connections:', externalConnections.value.length);
  } catch (error) {
    console.error('❌ Campaign Wizard: Error loading external connections:', error);
    externalConnections.value = [];
  } finally {
    loadingConnections.value = false;
  }
};

// Load pages from External Connection connected_accounts
const loadSocialPages = async () => {
  try {
    loadingPages.value = true;
    socialPages.value = [];
    // Expect connectedDataSources has the selected External Connection
    const selected = configData.value.selectedDataSource;
    if (!selected || !selected.name) return;
    // Fetch accounts for this connection
    const res = await call("mbw_mira.api.external_connections.get_account_details", {
      connection_id: selected.name,
    });
    if (res && res.status === "success") {
      const accounts = Array.isArray(res.data) ? res.data : res.data ? [res.data] : [];
      // Only active pages/users; prefer Page
      socialPages.value = accounts.filter((a) => a.connection_status !== "Revoked");
    }
  } catch (e) {
    console.warn("Failed to load social pages", e);
    socialPages.value = [];
  } finally {
    loadingPages.value = false;
  }
};

// Timezone helpers
const pad2 = (n) => String(n).padStart(2, "0");

const minScheduledAt = computed(() => toLocalDatetimeInput(new Date()));
const localTzLabel = Intl.DateTimeFormat().resolvedOptions().timeZone || "Local";

// Note: toIsoIfSet is now imported from @/utils/dateUtils


const openScheduledAtPicker = (e) => {
  try {
    // Ưu tiên gọi trên target nếu có
    if (e && e.target && typeof e.target.showPicker === "function") {
      e.target.showPicker();
      return;
    }
    // Gọi trên ref nếu hỗ trợ
    if (
      scheduledAtInput.value &&
      typeof scheduledAtInput.value.showPicker === "function"
    ) {
      scheduledAtInput.value.showPicker();
    }
  } catch (err) {
    // Trình duyệt không hỗ trợ showPicker, bỏ qua
  }
};

// State for Social Network configuration modal
const showSocialConfigModal = ref(false);
const editingSocialId = ref(null);

// Workflow state
const selectedWorkflowTemplate = ref(null);
const showWorkflowBuilder = ref(false);
const isCustomWorkflow = ref(false);
const workflowSteps = ref([]);

// Workflow methods
const onTemplateSelected = (data) => {
  selectedWorkflowTemplate.value = data.template;
  isCustomWorkflow.value = data.isCustom;
  showWorkflowBuilder.value = true;
  console.log('Template selected:', data);
};

const backToTemplates = () => {
  showWorkflowBuilder.value = false;
  selectedWorkflowTemplate.value = null;
  isCustomWorkflow.value = false;
};

const onWorkflowComplete = (data) => {
  workflowSteps.value = data.steps;
  console.log('Workflow completed:', data);
  // Auto advance to next step
  nextStep();
};

const confirmSocialConfig = async () => {
  try {
    // Nếu đã chọn job opening ở bước 2, chuẩn bị trước nội dung template
    const jobId = configData.value.socialConfig?.job_opening;
    if (jobId) {
      try {
        const details = await getJobOpeningDetails(jobId);
        const blockBody = buildJobDetailsForTemplate(details);
        // Lưu sẵn để dùng ở các step khác (Step 4 đã bị comment out)
        configData.value.socialConfig.template_content = blockBody || "";
      } catch (e) {
        console.warn("Failed to build template from job opening at step 2", e);
        configData.value.socialConfig.template_content = "";
      }
    }
    
    // Create Mira Campaign Social when social config is confirmed
    if (draftCampaign.value?.data?.name && configData.value.socialConfig) {
      try {
        console.log('🔧 Creating Mira Campaign Social from social config...');
        // Get external_connection from selected data source in wizard mode
        const selectedConnection = configData.value.selectedDataSource?.name || 
                                 configData.value.socialConfig.external_connection || '';
        
        // Ensure social pages are loaded
        if (socialPages.value.length === 0 && configData.value.selectedDataSource) {
          console.log('🔄 Social pages not loaded, loading now...');
          await loadSocialPages();
        }
        
        // Find selected page info
        const selectedPage = socialPages.value.find(
          (p) => p.external_account_id === configData.value.socialConfig.page_id
        );
        
        console.log('🔍 Creating social post with data:', {
          page_id: configData.value.socialConfig.page_id,
          socialPages: socialPages.value,
          selectedPage: selectedPage,
          page_name: selectedPage?.account_name || 'Unknown Page'
        });

        const result = await campaignSocialStore.createDefaultCampaignSocial(
          draftCampaign.value.data.name,
          {
            external_connection: selectedConnection,
            platform: configData.value.selectedDataSource?.platform_type || 
                     externalConnections.value.find(
                       (conn) => conn.name === selectedConnection
                     )?.platform_type || '',
            page_id: configData.value.socialConfig.page_id || '',
            page_name: selectedPage?.account_name || 'Unknown Page',
            scheduled_at: configData.value.socialConfig.scheduled_at || null,
            template_content: configData.value.socialConfig.template_content || '',
            image: configData.value.socialConfig.image || ''
          }
        );

        console.log('✅ Mira Campaign Social created from social config:', result);
        
        // Store the social post ID for editing
        if (result && result.name) {
          editingSocialId.value = result.name;
          console.log('✅ Mira Campaign Social created, ID:', result.name);
        } else {
          console.log('✅ Mira Campaign Social created from social config');
        }
      } catch (socialError) {
        console.warn('⚠️ Failed to create Mira Campaign Social from social config:', socialError);
      }
    }
  } finally {
    // Đóng modal
    showSocialConfigModal.value = false;
  }
};

// Hide step form fields for SocialNetwork (moved to modal)
// Modified to always hide these fields as per requirement
const showStepSocialFields = computed(() => false);

const openSocialConfigEditor = async () => {
  if (
    selectedSource.value === "datasource" &&
    selectedDataSourceType.value === "SocialNetwork"
  ) {
    await loadSocialPages();
    if (jobOpeningsList.value.length === 0) {
      await loadJobOpenings();
    }
    
    // Set external_connection from selectedDataSource
    if (!configData.value.socialConfig) {
      configData.value.socialConfig = {};
    }
    configData.value.socialConfig.external_connection = configData.value.selectedDataSource?.name || '';
    
    if (!configData.value.socialConfig?.scheduled_at) {
      const now = new Date();
      const plus30m = new Date(now.getTime() + 30 * 60 * 1000);
      configData.value.socialConfig.scheduled_at = toLocalDatetimeInput(plus30m);
    }
    
    // Clear editing ID when opening for new creation
    if (!editingSocialId.value) {
      editingSocialId.value = null;
    }
    
    showSocialConfigModal.value = true;
  }
};

// Removed auto-save watchers - now save only on step change

</script>

<style scoped>
/* Custom animations for Tailwind */
.animate-fadeIn {
  animation: fadeIn 0.5s forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Custom hover effects */
.hover\:-translate-y-0\.5:hover {
  transform: translateY(-2px);
}

.hover\:shadow-lg:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
</style>
