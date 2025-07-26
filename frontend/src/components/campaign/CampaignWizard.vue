<template>
  <Dialog v-model="show" :options="dialogOptions">
    <template #body>
      <div class="bg-white">
        <!-- Header -->
        <div class="flex justify-between items-center p-6 border-b border-gray-200">
          <h2 class="text-xl font-bold text-gray-900">{{ __(modalTitle) }}</h2>
          <Button
            theme="gray"
            variant="ghost"
            class="w-7 h-7"
            @click="closeWizard"
          >
            <FeatherIcon name="x" class="h-4 w-4" />
          </Button>
        </div>

        <!-- Stepper -->
        <div class="p-6 pb-4">
          <div class="flex items-center">
            <template v-for="(step, index) in steps" :key="step.number">
              <div
                class="flex flex-col items-center min-w-[80px]"
                :class="getStepClass(step.number)"
              >
                <div class="w-10 h-10 rounded-full border-2 flex items-center justify-center font-semibold transition-all duration-300"
                     :class="getStepIconClass(step.number)">
                  <FeatherIcon v-if="step.number < currentStep" name="check" class="h-4 w-4" />
                  <span v-else-if="step.number === 4">🎉</span>
                  <span v-else>{{ step.number }}</span>
                </div>
                <span class="mt-1 text-xs font-medium text-center transition-all duration-300"
                      :class="getStepLabelClass(step.number)">{{ step.label }}</span>
              </div>
              <div
                v-if="index < steps.length - 1"
                class="flex-grow h-0.5 mx-2 transition-all duration-400"
                :class="step.number < currentStep ? 'bg-blue-500' : 'bg-gray-300'"
              />
            </template>
          </div>
        </div>

        <!-- Step Content -->
        <div class="p-6">
          <!-- Step 1: Campaign Information -->
          <div v-if="currentStep === 1" class="space-y-4 animate-fadeIn">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Campaign Name') }} <span class="text-red-500">*</span>
              </label>
              <input
                v-model="campaignData.campaign_name"
                type="text"
                :placeholder="__('Example: React Candidate Nurturing Q4/2024')"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                :class="{ 'border-red-500': !campaignData.campaign_name && currentStep > 1 }"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Campaign Type') }} <span class="text-red-500">*</span>
              </label>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div
                  class="border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md"
                  :class="campaignData.type === 'NURTURING' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
                  @click="campaignData.type = 'NURTURING'"
                >
                  <div class="flex items-center">
                    <div class="flex items-center justify-center w-8 h-8 rounded-full mr-3"
                         :class="campaignData.type === 'NURTURING' ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-400'">
                      <FeatherIcon name="heart" class="h-4 w-4" />
                    </div>
                    <div>
                      <div class="text-sm font-medium" :class="campaignData.type === 'NURTURING' ? 'text-blue-900' : 'text-gray-900'">
                        {{ __('Nurturing') }}
                      </div>
                      <div class="text-xs text-gray-500">
                        {{ __('Long-term candidate engagement') }}
                      </div>
                    </div>
                  </div>
                </div>
                
                <div
                  class="border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md"
                  :class="campaignData.type === 'ATTRACTION' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
                  @click="campaignData.type = 'ATTRACTION'"
                >
                  <div class="flex items-center">
                    <div class="flex items-center justify-center w-8 h-8 rounded-full mr-3"
                         :class="campaignData.type === 'ATTRACTION' ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-400'">
                      <FeatherIcon name="magnet" class="h-4 w-4" />
                    </div>
                    <div>
                      <div class="text-sm font-medium" :class="campaignData.type === 'ATTRACTION' ? 'text-blue-900' : 'text-gray-900'">
                        {{ __('Attraction') }}
                      </div>
                      <div class="text-xs text-gray-500">
                        {{ __('Active talent acquisition') }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Objective') }} <span class="text-red-500">*</span>
              </label>
              <textarea
                v-model="campaignData.description"
                rows="3"
                :placeholder="__('Brief description of campaign purpose...')"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                :class="{ 'border-red-500': !campaignData.description && currentStep > 1 }"
              />
            </div>
          </div>

          <!-- Step 2: Select Source -->
          <div v-if="currentStep === 2" class="animate-fadeIn">
            <!-- Source Selection -->
            <div v-if="!selectedSource" class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div
                v-for="source in sources"
                :key="source.key"
                class="border rounded-lg p-4 text-center cursor-pointer transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg border-gray-200 hover:border-gray-300"
                @click="selectSource(source.key)"
              >
                <FeatherIcon :name="getSourceIcon(source.key)" class="h-8 w-8 mx-auto mb-2 text-gray-400" />
                <div class="text-sm font-medium mb-1 text-gray-900">
                  {{ source.title }}
                </div>
                <div class="text-xs text-gray-500">
                  {{ source.description }}
                </div>
              </div>
            </div>

            <!-- Source Configuration -->
            <div v-else class="space-y-4">
              <div class="flex items-center space-x-2 mb-4">
                <FeatherIcon :name="getSourceIcon(selectedSource)" class="h-6 w-6 text-blue-600" />
                <h4 class="text-lg font-medium text-gray-900">
                  {{ sources.find(s => s.key === selectedSource)?.title }} {{ __('Configuration') }}
                </h4>
              </div>

              <!-- Data Source Type Selection (when Data Source is selected) -->
              <div v-if="selectedSource === 'datasource' && dataSourceSelectionLevel === 1" class="space-y-4">
                <h4 class="text-lg font-medium text-gray-900 mb-4">{{ __('Select Data Source Type') }}</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div
                    v-for="sourceType in dataSourceTypes"
                    :key="sourceType.key"
                    class="border rounded-lg p-4 text-center cursor-pointer transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg border-gray-200 hover:border-gray-300"
                    @click="selectDataSourceType(sourceType.key)"
                  >
                    <FeatherIcon :name="sourceType.icon" class="h-8 w-8 mx-auto mb-2 text-gray-400" />
                    <div class="text-sm font-medium mb-1 text-gray-900">
                      {{ sourceType.title }}
                    </div>
                    <div class="text-xs text-gray-500">
                      {{ sourceType.description }}
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Specific Data Source Selection (when type is selected) -->
              <div v-else-if="selectedSource === 'datasource' && dataSourceSelectionLevel === 2" class="space-y-4">
                <div class="mb-4">
                  <h4 class="text-lg font-medium text-gray-900">
                    {{ __('Select') }} {{ selectedDataSourceType }} {{ __('Source') }}
                  </h4>
                </div>
                
                <div v-if="filteredDataSources.length === 0" class="text-center py-8">
                  <div class="text-gray-500 mb-2">{{ __('No') }} {{ selectedDataSourceType }} {{ __('sources available') }}</div>
                  <p class="text-xs text-gray-400">{{ __('Use the Back button to choose a different type') }}</p>
                </div>
                
                <div v-else class="grid grid-cols-1 gap-3">
                  <div
                    v-for="dataSource in filteredDataSources"
                    :key="dataSource.name"
                    class="border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md border-gray-200 hover:border-gray-300"
                    @click="selectSpecificDataSource(dataSource)"
                  >
                    <div class="flex items-center">
                      <FeatherIcon :name="getDataSourceIcon(dataSource.source_type)" class="h-6 w-6 mr-3 text-gray-400" />
                      <div class="flex-1">
                        <div class="text-sm font-medium text-gray-900">
                          {{ dataSource.source_name }}
                        </div>
                        <div v-if="dataSource.source_title" class="text-xs text-gray-500 italic">
                          {{ dataSource.source_title }}
                        </div>
                        <div class="text-xs text-gray-500">
                          {{ dataSource.description || __('External data source') }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- DataSource Final Configuration (when specific source is selected) -->
              <div v-else-if="selectedSource === 'datasource' && dataSourceSelectionLevel === 3" class="space-y-4">
                <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div class="flex items-start">
                    <FeatherIcon name="check-circle" class="h-5 w-5 text-green-400 mr-3 mt-0.5" />
                    <div>
                      <h4 class="text-sm font-medium text-green-800">
                        {{ __('Data Source Selected') }}
                      </h4>
                      <div class="mt-1 text-sm text-green-700">
                        <strong>{{ configData.selectedDataSource?.source_name }}</strong>
                      </div>
                      <div class="text-xs text-green-600 mt-1">
                        {{ __('Type') }}: {{ selectedDataSourceType }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- File Configuration -->
              <div v-else-if="selectedSource === 'file'">
                <component
                  :is="FileConfig"
                  v-model="configData"
                />
              </div>
              
              <!-- Search Configuration -->
              <div v-else-if="selectedSource === 'search'">
                <p class="text-sm text-gray-600 mb-4">
                  {{ __('Search configuration will be handled in the next step when selecting target segment.') }}
                </p>
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div class="flex">
                    <FeatherIcon name="info" class="h-5 w-5 text-blue-400 mt-0.5 mr-2" />
                    <div class="text-sm text-blue-800">
                      {{ __('You will be able to select specific talent segments in the next step.') }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- DataSource Final Configuration -->
              <div v-else-if="selectedSource === 'datasource' && selectedDataSourceId">
                <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div class="flex items-center">
                    <FeatherIcon name="check-circle" class="h-5 w-5 text-green-400 mr-2" />
                    <div>
                      <div class="text-sm font-medium text-green-800">
                        {{ __('Data Source Selected') }}
                      </div>
                      <div class="text-sm text-green-600">
                        {{ configData.selectedDataSource?.source_name || 'Selected data source' }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Step 3: Select Target Segment -->
          <div v-if="currentStep === 3" class="animate-fadeIn">
            <div class="space-y-4">
              <div class="text-center mb-6">
                <h4 class="text-lg font-medium text-gray-900 mb-2">{{ __('Select Target Segment') }}</h4>
                <p class="text-sm text-gray-600">{{ __('Choose the talent segment you want to target with this campaign') }}</p>
              </div>
              
              <!-- Use existing PoolConfig component for segment selection -->
              <component
                :is="PoolConfig"
                v-model="configData"
              />
            </div>
          </div>

          <!-- Step 4: Create Campaign Steps -->
          <div v-if="currentStep === 4" class="animate-fadeIn">
            <!-- Steps Creation Mode Selection -->
            <div v-if="!showStepCreation" class="space-y-6">
              <div class="text-center mb-6">
                <h4 class="text-lg font-medium text-gray-900 mb-2">{{ __('How would you like to create campaign steps?') }}</h4>
                <p class="text-sm text-gray-600">{{ __('Choose a method to define the workflow for your campaign') }}</p>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Use Template -->
                <div
                  class="border rounded-lg p-6 text-center cursor-pointer transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg border-gray-200 hover:border-blue-300"
                  @click="selectStepCreationMode('template')"
                >
                  <div class="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <FeatherIcon name="file-text" class="h-8 w-8 text-blue-600" />
                  </div>
                  <h5 class="text-lg font-medium text-gray-900 mb-2">{{ __('Use Template') }}</h5>
                  <p class="text-sm text-gray-600 mb-4">{{ __('Select from pre-defined campaign templates with ready-made workflows') }}</p>
                  <div class="text-xs text-blue-600 font-medium">{{ __('Recommended for consistency') }}</div>
                </div>
                
                <!-- Create Manual -->
                <div
                  class="border rounded-lg p-6 text-center cursor-pointer transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg border-gray-200 hover:border-green-300"
                  @click="selectStepCreationMode('manual')"
                >
                  <div class="w-16 h-16 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <FeatherIcon name="plus-circle" class="h-8 w-8 text-green-600" />
                  </div>
                  <h5 class="text-lg font-medium text-gray-900 mb-2">{{ __('Create Manually') }}</h5>
                  <p class="text-sm text-gray-600 mb-4">{{ __('Build custom workflow steps from scratch tailored to your needs') }}</p>
                  <div class="text-xs text-green-600 font-medium">{{ __('Full customization') }}</div>
                </div>
              </div>
            </div>

            <!-- Template Selection -->
            <div v-if="showStepCreation && stepCreationMode === 'template'" class="space-y-6">
              <div class="mb-4">
                <h4 class="text-lg font-medium text-gray-900">{{ __('Select Campaign Template') }}</h4>
              </div>
              
              <!-- Loading Templates -->
              <div v-if="loading" class="text-center py-8">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
                <p class="text-gray-600">{{ __('Loading templates...') }}</p>
              </div>
              
              <!-- Template List -->
              <div v-else-if="campaignTemplates.length > 0" class="space-y-4">
                <div class="text-sm text-gray-600 mb-3">
                  {{ __('Found') }} {{ campaignTemplates.length }} {{ __('templates') }}
                </div>
                <div class="grid grid-cols-1 gap-4 max-h-80 overflow-y-auto">
                  <div
                    v-for="template in campaignTemplates"
                    :key="template.name"
                    class="border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md"
                    :class="selectedTemplate?.name === template.name ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
                    @click="selectTemplate(template)"
                  >
                    <div class="flex items-center justify-between">
                      <div class="flex-1">
                        <h6 class="text-sm font-medium text-gray-900">{{ template.template_name }}</h6>
                        <p class="text-xs text-gray-500 mt-1">{{ template.description || __('No description') }}</p>
                        <div class="flex items-center mt-2 space-x-2">
                          <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800">
                            {{ template.campaign_type }}
                          </span>
                          <span class="text-xs text-gray-500">{{ template.step_count || 0 }} {{ __('steps') }}</span>
                        </div>
                      </div>
                      <div v-if="selectedTemplate?.name === template.name" class="text-blue-600">
                        <FeatherIcon name="check-circle" class="h-5 w-5" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- No Templates -->
              <div v-else class="text-center py-8">
                <FeatherIcon name="inbox" class="h-12 w-12 text-gray-400 mx-auto mb-3" />
                <p class="text-gray-500">{{ __('No campaign templates available') }}</p>
              </div>
            </div>

            <!-- Manual Step Creation -->
            <div v-if="showStepCreation && stepCreationMode === 'manual'" class="space-y-6">
              <div class="mb-4">
                <h4 class="text-lg font-medium text-gray-900">{{ __('Create Campaign Steps Manually') }}</h4>
              </div>
              
              <!-- Step Form -->
              <div v-if="showStepForm" class="bg-white border border-gray-200 rounded-lg p-6">
                <div class="flex items-center justify-between mb-4">
                  <h5 class="text-lg font-medium text-gray-900">
                    {{ editingStep ? __('Edit Step') : __('Add New Step') }}
                  </h5>
                  <Button variant="ghost" theme="gray" @click="handleStepFormCancel" class="text-sm">
                    <FeatherIcon name="x" class="h-4 w-4" />
                  </Button>
                </div>
                
                <form @submit.prevent="handleStepFormSubmit" class="space-y-4">
                  <!-- Step Name -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                      {{ __('Step Name') }}
                      <span class="text-red-500">*</span>
                    </label>
                    <input
                      v-model="stepFormData.campaign_step_name"
                      type="text"
                      :placeholder="__('Enter step name...')"
                      :disabled="stepFormLoading"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                      :class="{ 'border-red-500': stepFormErrors.campaign_step_name }"
                    />
                    <div v-if="stepFormErrors.campaign_step_name" class="mt-1 text-sm text-red-600">
                      {{ stepFormErrors.campaign_step_name }}
                    </div>
                  </div>

                  <div class="grid grid-cols-2 gap-4">
                    <!-- Action Type -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-2">
                        {{ __('Action Type') }}
                        <span class="text-red-500">*</span>
                      </label>
                      <select
                        v-model="stepFormData.action_type"
                        :disabled="stepFormLoading"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        :class="{ 'border-red-500': stepFormErrors.action_type }"
                      >
                        <option v-for="option in actionTypeOptions" :key="option.value" :value="option.value" :disabled="option.disabled">
                          {{ option.label }}
                        </option>
                      </select>
                      <div v-if="stepFormErrors.action_type" class="mt-1 text-sm text-red-600">
                        {{ stepFormErrors.action_type }}
                      </div>
                    </div>

                    <!-- Step Order -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-2">
                        {{ __('Step Order') }}
                        <span class="text-red-500">*</span>
                      </label>
                      <input
                        v-model.number="stepFormData.step_order"
                        type="number"
                        min="1"
                        max="999"
                        :placeholder="__('Order...')"
                        :disabled="stepFormLoading"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        :class="{ 'border-red-500': stepFormErrors.step_order }"
                      />
                      <div v-if="stepFormErrors.step_order" class="mt-1 text-sm text-red-600">
                        {{ stepFormErrors.step_order }}
                      </div>
                    </div>
                  </div>

                  <!-- Delay -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                      {{ __('Delay (Days)') }}
                    </label>
                    <input
                      v-model.number="stepFormData.delay_in_days"
                      type="number"
                      min="0"
                      max="365"
                      :placeholder="__('0 for immediate execution')"
                      :disabled="stepFormLoading"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                      :class="{ 'border-red-500': stepFormErrors.delay_in_days }"
                    />
                    <p class="mt-1 text-sm text-gray-500">
                      {{ __('Number of days to wait before executing this step') }}
                    </p>
                    <div v-if="stepFormErrors.delay_in_days" class="mt-1 text-sm text-red-600">
                      {{ stepFormErrors.delay_in_days }}
                    </div>
                  </div>

                  <!-- Template Content -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                      {{ __('Template Content') }}
                    </label>
                    <textarea
                      v-model="stepFormData.template_content"
                      rows="4"
                      :placeholder="__('Enter template content for this step...')"
                      :disabled="stepFormLoading"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    />
                    <p class="mt-1 text-sm text-gray-500">
                      {{ __('Content template for emails, SMS, or other actions') }}
                    </p>
                  </div>

                  <!-- Action Config -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                      {{ __('Action Configuration') }}
                    </label>
                    <textarea
                      v-model="stepFormData.action_config_string"
                      rows="3"
                      :placeholder="__('Enter JSON configuration...')"
                      :disabled="stepFormLoading"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm font-mono text-sm"
                      :class="{ 'border-red-500': stepFormErrors.action_config_string }"
                    />
                    <p class="mt-1 text-sm text-gray-500">
                      {{ __('JSON configuration for the action (optional)') }}
                    </p>
                    <div v-if="stepFormErrors.action_config_string" class="mt-1 text-sm text-red-600">
                      {{ stepFormErrors.action_config_string }}
                    </div>
                  </div>

                  <!-- Form Actions -->
                  <div class="flex justify-end space-x-3">
                    <Button
                      type="button"
                      variant="outline"
                      theme="gray"
                      @click="handleStepFormCancel"
                      :disabled="stepFormLoading"
                    >
                      {{ __('Cancel') }}
                    </Button>
                    <Button
                      type="submit"
                      variant="solid"
                      theme="gray"
                      :loading="stepFormLoading"
                      :disabled="stepFormLoading"
                    >
                      {{ editingStep ? __('Update Step') : __('Add Step') }}
                    </Button>
                  </div>
                </form>
              </div>
              
              <!-- Current Steps List -->
              <div v-if="campaignSteps.length > 0" class="space-y-3">
                <h5 class="text-sm font-medium text-gray-900">{{ __('Campaign Steps') }} ({{ campaignSteps.length }})</h5>
                <div class="space-y-2">
                  <div v-for="(step, index) in campaignSteps" :key="step.id || index" 
                       class="flex items-center p-3 bg-gray-50 rounded-lg border hover:bg-gray-100 transition-colors">
                    <span class="flex items-center justify-center w-6 h-6 bg-blue-100 text-blue-800 text-xs font-medium rounded-full mr-3">
                      {{ step.step_order }}
                    </span>
                    <div class="flex-1">
                      <div class="text-sm font-medium text-gray-900">{{ step.campaign_step_name }}</div>
                      <div class="text-xs text-gray-500">{{ step.action_type }}{{ step.delay_in_days > 0 ? ` • ${step.delay_in_days} days delay` : '' }}</div>
                    </div>
                    <div class="flex items-center space-x-2">
                      <Button variant="ghost" theme="gray" size="sm" @click="editManualStep(step)" class="p-1">
                        <FeatherIcon name="edit" class="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" theme="gray" size="sm" @click="removeStep(step)" class="p-1 text-red-600 hover:text-red-700">
                        <FeatherIcon name="trash-2" class="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Add Step Button -->
              <div v-if="!showStepForm" class="text-center">
                <Button variant="outline" theme="gray" @click="addManualStep">
                  <div class="flex items-center">
                    <FeatherIcon name="plus" class="h-4 w-4 mr-2" />
                    {{ campaignSteps.length > 0 ? __('Add Another Step') : __('Add First Step') }}
                  </div>
                </Button>
              </div>
              
              <!-- Empty State -->
              <div v-if="campaignSteps.length === 0 && !showStepForm" class="text-center py-8 border-2 border-dashed border-gray-300 rounded-lg">
                <FeatherIcon name="zap" class="h-12 w-12 text-gray-400 mx-auto mb-3" />
                <p class="text-gray-500 mb-4">{{ __('No steps created yet') }}</p>
                <Button variant="solid" theme="gray" @click="addManualStep">
                  <div class="flex items-center">
                    <FeatherIcon name="plus" class="h-4 w-4 mr-2" />
                    {{ __('Create First Step') }}
                  </div>
                </Button>
              </div>
            </div>
          </div>

          <!-- Step 5: Review & Activate -->
          <div v-if="currentStep === 5" class="animate-fadeIn space-y-6">
            <!-- Campaign Summary -->
            <div class="text-center py-4">
              <h3 class="text-xl font-bold mb-2 text-gray-900">{{ __('Review Campaign') }}</h3>
              <p class="text-sm text-gray-600">{{ __('Review your campaign details and workflow before finalizing') }}</p>
            </div>
            
            <!-- Campaign Info -->
            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="text-lg font-medium text-gray-900 mb-3">{{ __('Campaign Information') }}</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="text-sm font-medium text-gray-700">{{ __('Campaign Name') }}</label>
                  <p class="text-sm text-gray-900">{{ campaignData.campaign_name || __('Untitled Campaign') }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-700">{{ __('Type') }}</label>
                  <p class="text-sm text-gray-900">{{ campaignData.type }}</p>
                </div>
                <div class="md:col-span-2">
                  <label class="text-sm font-medium text-gray-700">{{ __('Description') }}</label>
                  <p class="text-sm text-gray-900">{{ campaignData.description || __('No description') }}</p>
                </div>
              </div>
            </div>
            
            <!-- Campaign Steps -->
            <div class="bg-blue-50 rounded-lg p-4">
              <h4 class="text-lg font-medium text-gray-900 mb-3">{{ __('Campaign Workflow') }}</h4>
              <div v-if="campaignSteps.length > 0" class="space-y-2">
                <div v-for="step in campaignSteps" :key="step.id || step.name" 
                     class="flex items-center p-3 bg-white rounded border">
                  <span class="flex items-center justify-center w-6 h-6 bg-blue-100 text-blue-800 text-xs font-medium rounded-full mr-3">
                    {{ step.step_order }}
                  </span>
                  <div class="flex-1">
                    <div class="text-sm font-medium text-gray-900">{{ step.campaign_step_name }}</div>
                    <div class="text-xs text-gray-500">{{ step.action_type }}{{ step.delay_in_days > 0 ? ` • ${step.delay_in_days} days delay` : '' }}</div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-4 text-gray-500">
                {{ __('No steps configured') }}
              </div>
            </div>
            
            <!-- Template Info -->
            <div v-if="selectedTemplate" class="bg-green-50 rounded-lg p-4">
              <h4 class="text-lg font-medium text-gray-900 mb-2">{{ __('Template Used') }}</h4>
              <p class="text-sm text-gray-600">{{ selectedTemplate.template_name }}</p>
              <p class="text-xs text-gray-500">{{ selectedTemplate.description }}</p>
            </div>
            
            <!-- Status -->
            <div class="text-center">
              <p class="text-sm text-gray-600 mb-2">
                {{ __('Campaign will be created in DRAFT status with') }} {{ campaignSteps.length }} {{ __('steps') }}
              </p>
              <p class="text-xs text-gray-500">
                {{ __('You can add profiles and activate the campaign after creation') }}
              </p>
            </div>
          </div>
        </div>

        <!-- Footer Actions -->
        <div class="flex justify-between items-center p-4 border-t border-gray-200">
          <Button
            v-if="currentStep > 1"
            variant="outline"
            theme="gray"
            @click="prevStep"
            :disabled="loading"
          >
            {{ __('Back') }}
          </Button>
          
          <div v-else></div>
          
          <div class="flex space-x-3">
            <Button
              v-if="currentStep < 4"
              variant="solid"
              theme="gray"
              @click="nextStep"
              :disabled="!canProceed"
              :loading="currentStep === 1 && draftCampaignLoading"
            >
              {{ currentStep === 1 && draftCampaignLoading ? __('Creating Campaign...') : __('Continue') }}
            </Button>
            
            <!-- Step 4: Campaign Steps -->
            <Button
              v-if="currentStep === 4 && !showStepCreation"
              variant="solid"
              theme="gray"
              @click="nextStep"
              :disabled="campaignSteps.length === 0 && !selectedTemplate"
            >
              {{ __('Continue to Review') }}
            </Button>
            
            <Button
              v-if="currentStep === 4 && showStepCreation && stepCreationMode === 'template'"
              variant="solid"
              theme="gray"
              @click="nextStep"
              :disabled="!selectedTemplate || campaignSteps.length === 0"
            >
              {{ __('Continue with Template') }}
            </Button>
            
            <Button
              v-if="currentStep === 4 && showStepCreation && stepCreationMode === 'manual'"
              variant="solid"
              theme="gray"
              @click="nextStep"
              :disabled="campaignSteps.length === 0"
            >
              {{ __('Continue with Steps') }}
            </Button>
            
            <Button
              v-if="currentStep === 5"
              variant="solid"
              theme="gray"
              @click="finalizeCampaign"
              :loading="activating"
            >
              {{ __('Finalize Campaign') }}
            </Button>
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { Dialog, Button, FeatherIcon } from 'frappe-ui'
import PoolConfig from './PoolConfig.vue'
import AtsConfig from './AtsConfig.vue'
import WebConfig from './WebConfig.vue'
import FileConfig from './FileConfig.vue'

import { submitNewCampaign, searchCandidates } from '@/services/campaignService'
import { 
  campaignService, 
  candidateService, 
  candidateSegmentService, 
  talentSegmentService,
  candidateCampaignService,
  campaignStepService
} from '@/services/universalService'
import { campaignTemplateDirectService } from '@/services/campaignTemplateDirectService.js'
import { campaignTemplateStepDirectService } from '@/services/campaignTemplateStepDirectService.js'
import { processSkills } from '@/services/candidateService'
import candidateDataSourceRepository from '@/repositories/candidateDataSourceRepository'
import moment from 'moment'

// Props & Emits
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  preselectedSegment: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'success', 'draft-created'])

// Reactive state
const show = ref(false)
const currentStep = ref(1)
const loading = ref(false)
const activating = ref(false)
const showCandidates = ref(false)

// Form data
const campaignData = ref({
  campaign_name: '',
  description: '',
  type: '', // Will be selected by user
  status: 'DRAFT',
  target_segment: props.preselectedSegment || '',
  source_type: '', // New field: 'DataSource', 'File', 'Search'
  source_file: '', // For File type
  data_source_id: '', // For DataSource type
  source_config: null // New field to store file mapping, meta, and URL
})

const selectedSource = ref(props.preselectedSegment ? 'search' : '')
const selectedDataSourceType = ref('') // ATS, JobBoard, SocialNetwork, TalentPool
const selectedDataSourceId = ref('') // Specific data source ID
const filteredDataSources = ref([])
const loadingDataSources = ref(false)

// Track data source selection level: 0=source, 1=type, 2=specific
const dataSourceSelectionLevel = ref(0)

// Data for form submission
const configData = ref({
  selectedSegment: props.preselectedSegment || '',
  selectedDataSource: '',
  selectedFile: null,
  uploadedFileUrl: '',
  filePreview: [],
  fileHeaders: []
})
const selectedCandidates = ref(new Set())
const realCandidates = ref([]) // Replace mockCandidates
const dataSources = ref([]) // All data sources from API

// Campaign Steps State
const campaignSteps = ref([])
const selectedTemplate = ref(null)
const campaignTemplates = ref([])
const showStepCreation = ref(false)
const stepCreationMode = ref('') // 'template' or 'manual'
const showStepForm = ref(false)
const editingStep = ref(null)

// Step Form State  
const stepFormData = ref({
  campaign_step_name: '',
  action_type: '',
  step_order: 1,
  delay_in_days: 0,
  template_content: '',
  action_config_string: ''
})

const stepFormErrors = ref({})
const stepFormLoading = ref(false)

// Translation helper function
const __ = (text) => text

// Steps definition
const steps = [
  { number: 1, label: 'Information' },
  { number: 2, label: 'Select Source' },
  { number: 3, label: 'Target Segment' },
  { number: 4, label: 'Campaign Steps' },
  { number: 5, label: 'Review & Activate' }
]

// Source options - 3 fixed choices only
const sources = computed(() => [
  {
    key: 'search',
    title: 'Search',
    description: 'Search and select candidates',
    icon: 'search',
    type: 'fixed',
    source_type: 'Search'
  },
  {
    key: 'file',
    title: 'File Import',
    description: 'Import from CSV/Excel file',
    icon: 'upload',
    type: 'fixed',
    source_type: 'File'
  },
  {
    key: 'datasource',
    title: 'Data Source',
    description: 'Import from external data sources',
    icon: 'database',
    type: 'fixed',
    source_type: 'DataSource'
  }
])

// Data source type options
const dataSourceTypes = computed(() => [
  { key: 'ATS', title: 'ATS', description: 'Applicant Tracking System', icon: 'briefcase' },
  { key: 'JobBoard', title: 'Job Board', description: 'Job posting platforms', icon: 'clipboard' },
  { key: 'SocialNetwork', title: 'Social Network', description: 'LinkedIn, Facebook, etc.', icon: 'users' },
  { key: 'TalentPool', title: 'Talent Pool', description: 'External talent pools', icon: 'user-check' }
])

// Helper function for data source icons
const getDataSourceIcon = (sourceType) => {
  const iconMap = {
    'ATS': 'database',
    'JobBoard': 'briefcase',
    'SocialNetwork': 'users',
    'TalentPool': 'user-check'
  }
  return iconMap[sourceType] || 'server'
}

// Source configurations
const sourceConfigs = computed(() => ({
  search: {
    description: __('Search and select candidates from existing talent pools.')
  },
  file: {
    description: __('Import candidates from CSV or Excel files.')
  },
  datasource: {
    description: __('Import candidates from external data sources (ATS, Job Board, Social Network, etc.).')
  }
}))

// Mock candidates (will be updated by search)
const mockCandidates = ref([])

// Load candidates from segment
const loadCandidatesFromSegment = async (segmentId) => {
  try {
    // Get candidates from target segment through TalentProfilesSegment
    const candidateSegmentResult = await candidateSegmentService.getList({
      filters: { segment_id: segmentId },
      fields: ['talent_id']
    })
    
    if (candidateSegmentResult.success && candidateSegmentResult.data.length > 0) {
      const candidateIds = candidateSegmentResult.data.map(cs => cs.talent_id)
      
      // Get the actual candidate data
      const candidateResult = await candidateService.getList({
        filters: { name: ['in', candidateIds] },
        fields: ['name', 'candidate_name', 'email', 'skills', 'status']
      })
      
      if (candidateResult.success) {
        return candidateResult.data.map(candidate => ({
          id: candidate.name,
          name: candidate.candidate_name || candidate.name,
          title: candidate.email || 'Candidate',
          source: 'Talent Segment',
          email: candidate.email,
          skills: processSkills(candidate.skills)
        }))
      }
    }
    return []
  } catch (error) {
    console.error('Error loading candidates from segment:', error)
    return []
  }
}

// Load candidates from data source
const loadCandidatesFromDataSource = async (dataSourceId) => {
  try {
    // TODO: Implement this function to find TalentPool records with matching data_source_id
    // and convert them to candidates format
    console.log('Loading candidates from data source:', dataSourceId)
    
    // For now, return empty array - this will be implemented later
    return []
  } catch (error) {
    console.error('Error loading candidates from data source:', error)
    return []
  }
}

// Validation rules
const rules = {
  required: value => !!value || __('This field is required')
}

// Dialog options
const dialogOptions = computed(() => ({
  title: modalTitle.value,
  size: '2xl'
}))

// Computed
const modalTitle = computed(() => {
  const titles = {
    1: 'Campaign Information',
    2: 'Select Data Source',
    3: 'Select Target Segment',
    4: 'Create Campaign Steps',
    5: 'Review & Activate'
  }
  return titles[currentStep.value] || 'Create New Campaign'
})

const step1Valid = computed(() => {
  return !!(campaignData.value.campaign_name && campaignData.value.description && campaignData.value.type)
})

const canProceed = computed(() => {
  if (currentStep.value === 1) return step1Valid.value
  if (currentStep.value === 2) {
    if (!selectedSource.value) return false
    
    // For datasource: need specific data source selected (level 3)
    if (selectedSource.value === 'datasource') {
      return dataSourceSelectionLevel.value === 3 && !!selectedDataSourceId.value
    }
    
    // For file: need file uploaded (if any)
    if (selectedSource.value === 'file') {
      return true // File config handled by component
    }
    
    // For search: can proceed immediately
    if (selectedSource.value === 'search') {
      return true
    }
    
    return !!selectedSource.value
  }
  // Bước 3: luôn cho phép qua, không bắt buộc chọn segment
  if (currentStep.value === 3) return true
  return true
})

const canProceedToSearch = computed(() => {
  if (!selectedSource.value) return false
  
  if (selectedSource.value === 'datasource') {
    return !!(selectedDataSourceType.value && selectedDataSourceId.value)
  }
  
  return true
})

// Methods
const getStepClass = (stepNumber) => {
  if (stepNumber < currentStep.value) return 'completed'
  if (stepNumber === currentStep.value) return 'active'
  return ''
}

// Load data sources from API
const loadDataSources = async () => {
  loadingDataSources.value = true
  try {
    console.log('🔍 Loading data sources from API...')
    const response = await candidateDataSourceRepository.getDataSources()
    console.log('📊 Data sources response:', response)
    
    if (response && response.success) {
      dataSources.value = response.data_sources || []
      console.log(`✅ Loaded ${dataSources.value.length} data sources:`, dataSources.value)
    } else {
      console.error('❌ Failed to load data sources:', response?.error || 'No success flag')
      dataSources.value = []
    }
  } catch (error) {
    console.error('💥 Error loading data sources:', error)
    dataSources.value = []
  } finally {
    loadingDataSources.value = false
    console.log('🏁 Data sources loading finished. Count:', dataSources.value.length)
  }
}

const getConfigComponent = (source) => {
  if (source === 'search') return PoolConfig // Use pool config for search
  if (source === 'file') return FileConfig
  if (source === 'datasource' && selectedDataSourceId.value) {
    // Show appropriate config based on data source type
    const dataSource = configData.value.selectedDataSource
    if (dataSource && dataSource.source_type === 'ATS') {
      return AtsConfig
    }
    // Add other config components for different data source types as needed
    return AtsConfig // Default to ATS config for now
  }
  return null
}

// Styling methods for Tailwind CSS
const getStepIconClass = (stepNumber) => {
  if (stepNumber < currentStep.value) return 'border-blue-500 bg-blue-500 text-white'
  if (stepNumber === currentStep.value) return 'border-blue-500 bg-blue-500 text-white'
  return 'border-gray-300 text-gray-400'
}

const getStepLabelClass = (stepNumber) => {
  if (stepNumber < currentStep.value) return 'text-gray-600'
  if (stepNumber === currentStep.value) return 'text-gray-900 font-semibold'
  return 'text-gray-400'
}

const getSourceIcon = (sourceKey) => {
  const icons = {
    pool: 'users',
    ats: 'refresh-cw',
    web: 'globe'
  }
  return icons[sourceKey] || 'circle'
}

const selectSource = (sourceKey) => {
  console.log('🎯 Selecting source:', sourceKey)
  console.log('📊 Available sources:', sources.value)
  
  selectedSource.value = sourceKey
  
  // Reset data source selections when selecting new source
  selectedDataSourceType.value = ''
  selectedDataSourceId.value = ''
  filteredDataSources.value = []
  dataSourceSelectionLevel.value = 0 // Reset level
  
  // Find selected source info
  const source = sources.value.find(s => s.key === sourceKey)
  console.log('🎯 Found source:', source)
  
  if (source) {
    campaignData.value.source_type = source.source_type
    
    if (source.source_type !== 'DataSource') {
      campaignData.value.data_source_id = ''
      configData.value.selectedDataSource = ''
    }
    
    if (source.source_type === 'File') {
      // Reset file selection
      campaignData.value.source_file = ''
      configData.value.selectedFile = null
    }
    
    // Load data sources if datasource is selected
    if (source.key === 'datasource') {
      console.log('🔄 Loading data sources for datasource selection...')
      dataSourceSelectionLevel.value = 1  // Move to type selection level
      loadDataSources()
    } else {
      dataSourceSelectionLevel.value = 0  // Reset to source level for other types
    }
  }
  
  console.log('✅ selectedSource now:', selectedSource.value)
}

const selectDataSourceType = (sourceType) => {
  console.log('🎯 Selecting data source type:', sourceType)
  console.log('📊 Available data sources:', dataSources.value)
  
  selectedDataSourceType.value = sourceType
  selectedDataSourceId.value = ''
  dataSourceSelectionLevel.value = 2 // ✅ Move to specific source selection to show the list
  
  // Filter data sources by type
  filteredDataSources.value = dataSources.value.filter(ds => ds.source_type === sourceType)
  
  console.log('✅ Filtered data sources:', filteredDataSources.value)
  console.log('🎯 selectedDataSourceType now:', selectedDataSourceType.value)
  console.log('🎯 dataSourceSelectionLevel now:', dataSourceSelectionLevel.value)
}

const selectSpecificDataSource = (dataSource) => {
  selectedDataSourceId.value = dataSource.name
  campaignData.value.data_source_id = dataSource.name
  configData.value.selectedDataSource = dataSource
  dataSourceSelectionLevel.value = 3 // ✅ Specific data source selected - confirmed level
}

// Campaign Steps Methods
const selectStepCreationMode = async (mode) => {
  stepCreationMode.value = mode
  showStepCreation.value = true
  
  if (mode === 'template') {
    await loadCampaignTemplates()
  }
}

const loadCampaignTemplates = async () => {
  loading.value = true
  try {
    const result = await campaignTemplateDirectService.getList({
      filters: { is_active: 1 },
      limit: 50
    })

    console.log('🔍 Campaign templates result:', result)
    
    // Extract data array from response
    let templates = []
    
    if (result && result.success && result.data && result.data.data && Array.isArray(result.data.data)) {
      templates = result.data.data  // ✅ Lấy array từ result.data.data
      console.log('✅ Found templates in result.data.data')
    } else if (result && result.data && Array.isArray(result.data)) {
      templates = result.data  // Fallback: direct array
      console.log('✅ Found templates in result.data (fallback)')
    } else if (result && Array.isArray(result)) {
      templates = result  // Fallback: result is direct array
      console.log('✅ Result is direct array (fallback)')
    } else {
      templates = []
      console.log('❌ No valid templates array found')
    }
    
    campaignTemplates.value = templates
    console.log(`✅ Loaded ${campaignTemplates.value.length} campaign templates`)
    
  } catch (error) {
    console.error('❌ Error loading campaign templates:', error)
    campaignTemplates.value = []
  } finally {
    loading.value = false
  }
}

const selectTemplate = async (template) => {
  selectedTemplate.value = template
  
  // Load template steps and create campaign steps
  try {
    loading.value = true
    console.log('🔍 Loading template steps for:', template.name)
    const templateData = await campaignTemplateDirectService.getById(template.name)
    
    console.log('📋 Template data loaded:', templateData)
    
    if (templateData.success && templateData.data.steps?.length > 0) {
      console.log(`✅ Found ${templateData.data.steps.length} template steps`)
      
      // Create CampaignStep records from template steps
      const campaignStepPromises = templateData.data.steps.map(templateStep => {
        return createCampaignStepFromTemplate(templateStep)
      })
      
      const createdSteps = await Promise.all(campaignStepPromises)
      campaignSteps.value = createdSteps.filter(step => step !== null)
      
      console.log(`📝 Prepared ${campaignSteps.value.length} campaign steps from template:`, campaignSteps.value)
    } else {
      console.log('⚠️ No template steps found')
      campaignSteps.value = []
    }
  } catch (error) {
    console.error('❌ Error creating steps from template:', error)
    alert(__('Failed to create steps from template. Please try again.'))
  } finally {
    loading.value = false
  }
}

const createCampaignStepFromTemplate = async (templateStep) => {
  try {
    // Prepare step data for display (not creating DB record yet - will be done in finalize)
    const stepData = {
      id: Date.now() + Math.random(), // Temporary unique ID for UI
      campaign: draftCampaign.value?.name,
      campaign_step_name: templateStep.campaign_step_name,
      step_order: templateStep.step_order,
      action_type: templateStep.action_type,
      delay_in_days: templateStep.delay_in_days || 0,
      template_content: templateStep.template_content || '',
      action_config: templateStep.action_config || null,
      status: 'DRAFT',
      is_active: true,
      fromTemplate: true // Mark as created from template
    }
    
    console.log('Prepared campaign step from template:', stepData)
    return stepData
  } catch (error) {
    console.error('Error preparing campaign step from template:', error)
    return null
  }
}

// Action type options for step form
const actionTypeOptions = [
  { label: __('Select action type...'), value: '', disabled: true },
  { label: __('Send Email'), value: 'SEND_EMAIL' },
  { label: __('Send SMS'), value: 'SEND_SMS' },
  { label: __('Manual Call'), value: 'MANUAL_CALL' },
  { label: __('Manual Task'), value: 'MANUAL_TASK' }
]

const addManualStep = () => {
  // Ensure draft campaign exists
  if (!draftCampaign.value) {
    alert(__('Draft campaign not found. Please go back to step 1 and try again.'))
    return
  }
  
  // Reset form and show inline form
  resetStepForm()
  editingStep.value = null
  showStepForm.value = true
}

const editManualStep = (step) => {
  // Load step data into form
  setStepFormData(step)
  editingStep.value = step
  showStepForm.value = true
}

const resetStepForm = () => {
  stepFormData.value = {
    campaign_step_name: '',
    action_type: '',
    step_order: campaignSteps.value.length + 1,
    delay_in_days: 0,
    template_content: '',
    action_config_string: ''
  }
  stepFormErrors.value = {}
}

const setStepFormData = (step) => {
  stepFormData.value = {
    campaign_step_name: step.campaign_step_name || '',
    action_type: step.action_type || '',
    step_order: step.step_order || campaignSteps.value.length + 1,
    delay_in_days: step.delay_in_days || 0,
    template_content: step.template_content || '',
    action_config_string: step.action_config_string || (step.action_config ? JSON.stringify(step.action_config, null, 2) : '')
  }
  stepFormErrors.value = {}
}

const validateStepForm = () => {
  stepFormErrors.value = {}
  
  if (!stepFormData.value.campaign_step_name?.trim()) {
    stepFormErrors.value.campaign_step_name = __('Step name is required')
  }
  
  if (!stepFormData.value.action_type?.trim()) {
    stepFormErrors.value.action_type = __('Action type is required')
  }
  
  if (!stepFormData.value.step_order || stepFormData.value.step_order < 1) {
    stepFormErrors.value.step_order = __('Step order must be at least 1')
  }
  
  if (stepFormData.value.delay_in_days < 0) {
    stepFormErrors.value.delay_in_days = __('Delay cannot be negative')
  }
  
  // Validate JSON config if provided
  if (stepFormData.value.action_config_string?.trim()) {
    try {
      JSON.parse(stepFormData.value.action_config_string)
    } catch (e) {
      stepFormErrors.value.action_config_string = __('Invalid JSON format')
    }
  }
  
  return Object.keys(stepFormErrors.value).length === 0
}

const handleStepFormSubmit = () => {
  if (!validateStepForm()) return
  
  stepFormLoading.value = true
  
  try {
    const stepData = {
      campaign_step_name: stepFormData.value.campaign_step_name.trim(),
      action_type: stepFormData.value.action_type,
      step_order: stepFormData.value.step_order,
      delay_in_days: stepFormData.value.delay_in_days,
      template_content: stepFormData.value.template_content?.trim() || '',
      action_config: stepFormData.value.action_config_string?.trim() ? 
        (() => {
          try {
            return JSON.parse(stepFormData.value.action_config_string)
          } catch {
            return stepFormData.value.action_config_string
          }
        })() : null
    }
    
    if (editingStep.value) {
      // Editing existing step
      const index = campaignSteps.value.findIndex(s => s.id === editingStep.value.id)
      if (index !== -1) {
        campaignSteps.value[index] = { ...stepData, id: editingStep.value.id, campaign: draftCampaign.value?.name }
      }
    } else {
      // Adding new step
      const newStep = {
        id: Date.now(), // Temporary ID
        campaign: draftCampaign.value?.name,
        fromTemplate: false, // Mark as manually created
        ...stepData
      }
      campaignSteps.value.push(newStep)
      console.log('📝 Added manual campaign step:', newStep)
    }
    
    // Sort steps by order
    campaignSteps.value.sort((a, b) => a.step_order - b.step_order)
    
    // Close form
    showStepForm.value = false
    editingStep.value = null
    
    console.log('Step saved:', stepData)
  } finally {
    stepFormLoading.value = false
  }
}

const handleStepFormCancel = () => {
  showStepForm.value = false
  editingStep.value = null
  resetStepForm()
}

const removeStep = (step) => {
  if (confirm(__('Are you sure you want to delete this step?'))) {
    const index = campaignSteps.value.findIndex(s => s.id === step.id)
    if (index !== -1) {
      campaignSteps.value.splice(index, 1)
      console.log('Step removed:', step)
    }
  }
}

const nextStep = async () => {
  // Create draft campaign when moving from step 1 to step 2
  if (currentStep.value === 1) {
    try {
      await createDraftCampaign()
    } catch (error) {
      // Don't proceed if draft creation fails
      return
    }
  }
  
  if (currentStep.value < 5) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 1) {
    // Smart back logic for step 2 - handle multi-level navigation
    if (currentStep.value === 2) {
      console.log('🔙 Back in step 2. Current state:', {
        selectedSource: selectedSource.value,
        selectedDataSourceType: selectedDataSourceType.value,
        selectedDataSourceId: selectedDataSourceId.value,
        dataSourceSelectionLevel: dataSourceSelectionLevel.value
      })
      
      // Level 3: Specific data source selected → Go back to source list
      if (selectedSource.value === 'datasource' && dataSourceSelectionLevel.value === 3) {
        console.log('🔙 Level 3 → Level 2: Going back to data source list')
        selectedDataSourceId.value = ''
        configData.value.selectedDataSource = ''
        campaignData.value.data_source_id = ''
        dataSourceSelectionLevel.value = 2 // Move back to source list
        return
      }
      
      // Level 2: Data source list shown → Go back to type selection
      if (selectedSource.value === 'datasource' && dataSourceSelectionLevel.value === 2) {
        console.log('🔙 Level 2 → Level 1: Going back to data source type selection')
        selectedDataSourceType.value = ''
        filteredDataSources.value = []
        dataSourceSelectionLevel.value = 1 // Move back to type selection
        return
      }
      
      // Level 1: Data source type selection → Go back to source selection  
      if (selectedSource.value === 'datasource' && dataSourceSelectionLevel.value === 1) {
        console.log('🔙 Level 1 → Level 0: Going back to source selection')
        selectedDataSourceType.value = ''
        dataSourceSelectionLevel.value = 0 // Move back to source selection
        return
      }
      
      // Level 0: Source selected → Go back to source selection (preserve data)
      if (selectedSource.value) {
        console.log('🔙 Level 0 → Clearing source: Going back to source selection (preserving data)')
        selectedSource.value = ''
        dataSourceSelectionLevel.value = 0 // Reset to initial level
        // Don't reset these - preserve user selections:
        // selectedDataSourceType.value = ''
        // selectedDataSourceId.value = ''
        // filteredDataSources.value = []
        // configData.value.selectedDataSource = ''
        // configData.value.selectedFile = null
        // configData.value.uploadedFileUrl = ''
        return
      }
      
      // Level 0: No source selected → Go to previous step
      console.log('🔙 Level 0 → Previous step')
    }
    
    // Smart back logic for step 4 - handle sub-navigation
    if (currentStep.value === 4) {
      // If in step creation mode, go back to mode selection
      if (showStepCreation.value) {
        console.log('🔙 Step 4: showStepCreation → false')
        showStepCreation.value = false
        showStepForm.value = false
        editingStep.value = null
        return
      }
      
      // Standard cleanup for step 4
      showCandidates.value = false
      selectedCandidates.value.clear()
    }
    currentStep.value--
  }
}

const handleSearch = async () => {
  // For data source selection, handle step by step
  if (selectedSource.value === 'datasource') {
    if (!selectedDataSourceType.value) {
      // This shouldn't happen due to disabled state, but just in case
      return
    }
    if (!selectedDataSourceId.value) {
      // This shouldn't happen due to disabled state, but just in case
      return
    }
  }
  
  loading.value = true
  
  try {
    let candidates = []
    
    switch (selectedSource.value) {
      case 'search':
        // Load candidates from selected segment (old pool logic)
        const segmentId = configData.value.selectedSegment || props.preselectedSegment
        if (segmentId) {
          candidates = await loadCandidatesFromSegment(segmentId)
          campaignData.value.target_segment = segmentId
        }
        break
        
      case 'file':
        // Handle file import
        if (configData.value.uploadedFileUrl) {
          // File has been uploaded successfully
          console.log('Processing uploaded file:', configData.value.uploadedFileUrl)
          
          // TODO: Parse CSV/Excel file from URL and extract candidates
          // For now, show empty candidates list until file parsing is implemented
          candidates = []
          
          console.log('File uploaded successfully, URL:', configData.value.uploadedFileUrl)
        } else {
          console.log('No file uploaded yet')
          candidates = []
        }
        break
        
      case 'datasource':
        // Handle data source sync
        if (selectedDataSourceId.value) {
          console.log('Syncing from data source:', selectedDataSourceId.value)
          // TODO: Find TalentPools with matching data source and load candidates
          candidates = await loadCandidatesFromDataSource(selectedDataSourceId.value)
        }
        break
        
      default:
        // Fallback to existing search API for compatibility
        candidates = await searchCandidates(selectedSource.value, configData.value)
    }
    
    // Update candidates list
    mockCandidates.value = candidates
    
    loading.value = false
    showCandidates.value = true
  } catch (error) {
    console.error('Error searching candidates:', error)
    loading.value = false
    alert(__('Error searching candidates. Please try again.'))
  }
}

const toggleCandidate = (candidateId) => {
  if (selectedCandidates.value.has(candidateId)) {
    selectedCandidates.value.delete(candidateId)
  } else {
    selectedCandidates.value.add(candidateId)
  }
}

const getSearchButtonText = () => {
  if (selectedSource.value === 'search') return __('Search')
  if (selectedSource.value === 'file') return __('Process File')
  if (selectedSource.value === 'datasource') {
    if (!selectedDataSourceType.value) return __('Select Source Type')
    if (!selectedDataSourceId.value) return __('Select Specific Source')
    return __('Sync Data')
  }
  return __('Continue')
}

// Helper: tạo toàn bộ CampaignStep trước
const createAllSteps = async () => {
  if (!draftCampaign.value) throw new Error('No draft campaign')

  const promises = campaignSteps.value.map(step => {
    const payload = {
      campaign: draftCampaign.value.name,
      campaign_step_name: step.campaign_step_name,
      step_order: step.step_order,
      action_type: step.action_type,
      delay_in_days: step.delay_in_days || 0,
      template_content: step.template_content || '',
      action_config: step.action_config || null,
      status: 'DRAFT',
      is_active: 1
    }
    return campaignStepService.save(payload)
  })

  const results = await Promise.all(promises)
  // cập nhật lại list steps bằng bản ghi server trả về (nếu cần cho UI)
  campaignSteps.value = results
    .filter(r => r?.success)
    .map(r => r.data)

  return campaignSteps.value.length
}

// Finalize: tạo step trước, update campaign sau
const finalizeCampaign = async () => {
  activating.value = true

  try {
    if (!draftCampaign.value) {
      throw new Error(__('No draft campaign found'))
    }

    // 1) Tạo tất cả steps trước
    let stepCount = 0
    if (campaignSteps.value.length > 0) {
      // try {
      //   stepCount = await createAllSteps()
      // } catch (e) {
      //   console.error('❌ Create steps failed', e)
      //   alert(__('Failed to create steps. Please try again.'))
      //   return
      // }
    }
    console.log("campaignData.value", campaignData.value)
    // 2) Update campaign sau khi đã có step
    const campaignUpdatePayload = {
      campaign_name: campaignData.value.campaign_name || draftCampaign.value.campaign_name,
      description:   campaignData.value.description   || draftCampaign.value.description,
      type:          campaignData.value.type,
      status: 'DRAFT',
      start_date: new Date().toISOString().split('T')[0],
      end_date:   new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      is_active: false,
      source_type: campaignData.value.source_type || 'Template',
      template_used: selectedTemplate.value?.name || null,
      steps_count: stepCount,
      source_file: campaignData.value.source_file || '',
      source_config: campaignData.value.source_config || null,
      campaign_steps: campaignSteps.value,
      target_segment: campaignData.value.target_segment || null
    }

    const campaignResult = await campaignService.save(
      campaignUpdatePayload,
      draftCampaign.value.name
    )

    if (!campaignResult.success) {
      throw new Error(campaignResult.message || 'Failed to finalize campaign')
    }

    // 3) Done
    emit('success', { action: 'create', data: campaignResult.data })
    closeWizard()
  } catch (error) {
    console.error('Error finalizing campaign:', error)

    let msg = __('An error occurred while finalizing the campaign')
    if (error.message.includes('campaign_name')) msg = __('Campaign name is invalid or already exists')
    else if (error.message.includes('validation')) msg = __('Input data is not in the correct format')
    else if (error.message.includes('network') || error.message.includes('fetch')) msg = __('Network connection error, please try again')
    else if (error.message) msg = error.message

    alert(msg)
  } finally {
    activating.value = false
  }
}


// const finalizeCampaign = async () => {
//   activating.value = true
  
//   try {
//     if (!draftCampaign.value) {
//       throw new Error(__('No draft campaign found'))
//     }
    
//     console.log('🚀 Starting campaign finalization...')
//     console.log('📋 Draft Campaign:', draftCampaign.value)
//     console.log('📝 Campaign Steps to create:', campaignSteps.value)
    
//     // Update the draft campaign with final details
//     const campaignUpdatePayload = {
//       campaign_name: campaignData.value.campaign_name || draftCampaign.value.campaign_name,
//       description: campaignData.value.description || draftCampaign.value.description,
//       type: campaignData.value.type,
//       status: 'DRAFT',
//       start_date: new Date().toISOString().split('T')[0],
//       end_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
//       is_active: false,
//       source_type: campaignData.value.source_type || 'Template',
//       template_used: selectedTemplate.value?.name || null,
//       steps_count: campaignSteps.value.length,
//       source_file: campaignData.value.source_file || '',
//       source_config: campaignData.value.source_config || null
//     }
    
//     console.log('Finalizing campaign with payload:', campaignUpdatePayload)
    
//     // Update campaign using universal service
//     const campaignResult = await campaignService.save(campaignUpdatePayload, draftCampaign.value.name)
    
//     if (campaignResult.success) {
//       // Save all campaign steps (if any were created from template or manual)
//       if (campaignSteps.value.length > 0) {
//         console.log(`Saving ${campaignSteps.value.length} campaign steps`)
        
//         try {
//           // Create CampaignStep records for each step
//           const stepPromises = campaignSteps.value.map(async (step) => {
//             const stepPayload = {
//               campaign: draftCampaign.value.name,
//               campaign_step_name: step.campaign_step_name,
//               step_order: step.step_order,
//               action_type: step.action_type,
//               delay_in_days: step.delay_in_days || 0,
//               template_content: step.template_content || '',
//               action_config: step.action_config || null,
//               status: 'DRAFT',
//               is_active: 1
//             }
            
//             console.log('Creating CampaignStep:', stepPayload)
//             const result = await campaignStepService.save(stepPayload)
            
//             if (result.success) {
//               console.log(`✅ CampaignStep created:`, result.data.name)
//               return result.data
//             } else {
//               console.error(`❌ Failed to create CampaignStep:`, result.error)
//               throw new Error(`Failed to create step "${step.campaign_step_name}": ${result.error}`)
//             }
//           })
          
//           // Wait for all steps to be created
//           const createdSteps = await Promise.all(stepPromises)
//           console.log(`✅ All ${createdSteps.length} campaign steps created successfully`)
          
//         } catch (stepError) {
//           console.error('❌ Error creating campaign steps:', stepError)
//           // Don't fail the entire campaign creation, just log the error
//           alert(__('Campaign created successfully, but some steps failed to save. You can add steps manually later.') + '\n\nError: ' + stepError.message)
//         }
//       }
      
//       emit('success', {
//         action: 'create',
//         data: campaignResult.data
//       })
      
//       closeWizard()
//     } else {
//       throw new Error(campaignResult.message || 'Failed to finalize campaign')
//     }
//   } catch (error) {
//     console.error('Error finalizing campaign:', error)
    
//     let errorMessage = __('An error occurred while finalizing the campaign')
    
//     if (error.message.includes('campaign_name')) {
//       errorMessage = __('Campaign name is invalid or already exists')
//     } else if (error.message.includes('validation')) {
//       errorMessage = __('Input data is not in the correct format')
//     } else if (error.message.includes('network') || error.message.includes('fetch')) {
//       errorMessage = __('Network connection error, please try again')
//     } else if (error.message) {
//       errorMessage = error.message
//     }
    
//     alert(errorMessage)
//   } finally {
//     activating.value = false
//   }
// }

const closeWizard = () => {
  show.value = false
  // Reset state
  currentStep.value = 1
  campaignData.value = {
    campaign_name: '',
    description: '',
    type: '',
    status: 'DRAFT',
    target_segment: props.preselectedSegment || '',
    source_type: '',
    source_file: '',
    data_source_id: '',
    source_config: null
  }
  selectedSource.value = props.preselectedSegment ? 'search' : ''
  selectedDataSourceType.value = ''
  selectedDataSourceId.value = ''
  configData.value = {
    selectedSegment: props.preselectedSegment || '',
    selectedDataSource: '',
    selectedFile: null,
    uploadedFileUrl: '',
    filePreview: [],
    fileHeaders: []
  }
  filteredDataSources.value = []
  selectedCandidates.value.clear()
  showCandidates.value = false
  loading.value = false
  activating.value = false
  
  // Reset new campaign steps states
  campaignSteps.value = []
  selectedTemplate.value = null
  campaignTemplates.value = []
  showStepCreation.value = false
  stepCreationMode.value = ''
  showStepForm.value = false
  editingStep.value = null
  stepFormData.value = {
    campaign_step_name: '',
    action_type: '',
    step_order: 1,
    delay_in_days: 0,
    template_content: '',
    action_config_string: ''
  }
  stepFormErrors.value = {}
  stepFormLoading.value = false
  draftCampaign.value = null
  
  // Reset candidates
  mockCandidates.value = []
}

// Load data sources on component mount
onMounted(async () => {
  console.log('🚀 CampaignWizard mounted, loading initial data...')
  await loadDataSources()
  console.log('✅ Initial data loading completed')
})

// Draft campaign for steps creation
const draftCampaign = ref(null)
const draftCampaignLoading = ref(false)

// Create draft campaign when moving from step 1
const createDraftCampaign = async () => {
  if (draftCampaign.value) return // Already created
  
  draftCampaignLoading.value = true
  try {
    console.log('🔧 Creating draft campaign with user input...')
    const draftPayload = {
      campaign_name: campaignData.value.campaign_name || (__('Draft Campaign') + ' ' + new Date().toLocaleString()),
      description: campaignData.value.description || __('Draft campaign - to be configured'),
      type: campaignData.value.type || 'NURTURING',
      status: 'DRAFT',
      start_date: new Date().toISOString().split('T')[0],
      end_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      is_active: false
    }
    
    const result = await campaignService.save(draftPayload)
    if (result.success) {
      draftCampaign.value = result.data
      console.log('✅ Draft campaign created:', draftCampaign.value.name)
      
      // Emit event to refresh the campaign list
      emit('draft-created', draftCampaign.value)
    } else {
      throw new Error(result.message || 'Failed to create draft campaign')
    }
  } catch (error) {
    console.error('❌ Error creating draft campaign:', error)
    alert(__('Failed to create draft campaign. Please try again.'))
    
    // Prevent moving to next step if draft creation fails
    throw error
  } finally {
    draftCampaignLoading.value = false
  }
}

// Watch configData để đồng bộ mapping file vào campaignData.source_config khi chọn nguồn là file
watch(
  [configData, selectedSource],
  ([cfg, src]) => {
    if (src !== 'file') return

    const mappingEntries = Object.entries(cfg?.mapping || {}).filter(([, f]) => f)
    if (!mappingEntries.length) return

    const field_mapping = mappingEntries.map(([column_name, field_name]) => ({ column_name, field_name }))

    campaignData.value.source_file = cfg?.selectedFile?.name || '' // để BE biết file
    campaignData.value.source_config = JSON.stringify({
      file_name: cfg?.selectedFile?.name || '',
      meta_doctype: 'TalentProfiles',          // đổi nếu khác
      field_mapping
    })
  },
  { deep: true }
)

// Watchers
watch(() => props.modelValue, (newVal) => {
  show.value = newVal
})

watch(show, (newVal) => {
  emit('update:modelValue', newVal)
  if (!newVal && draftCampaign.value) {
    // Clean up draft campaign if wizard is closed without completion
    // TODO: Optionally delete draft campaign
  }
})

// Đồng bộ target_segment với configData.selectedSegment
watch(() => configData.value.selectedSegment, (val) => {
  campaignData.value.target_segment = val
})
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