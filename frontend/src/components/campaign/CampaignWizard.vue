<template>
  <div>
    <Dialog v-model="show" :options="dialogOptions" :disableOutsideClickToClose="true">
      <template #body>
        <div class="bg-white">
          <!-- Header -->
          <div class="flex justify-between items-center p-6 border-b border-gray-200">
            <h2 class="text-xl font-bold text-gray-900">{{ __(modalTitle) }}</h2>
            <Button theme="gray" variant="ghost" class="w-7 h-7" @click="closeWizard">
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
                  <div
                    class="w-10 h-10 rounded-full border-2 flex items-center justify-center font-semibold transition-all duration-300"
                    :class="getStepIconClass(step.number)"
                  >
                    <FeatherIcon
                      v-if="step.number < currentStep"
                      name="check"
                      class="h-4 w-4"
                    />
                    <span v-else-if="step.number === 4">🎉</span>
                    <span v-else>{{ step.number }}</span>
                  </div>
                  <span
                    class="mt-1 text-xs font-medium text-center transition-all duration-300"
                    :class="getStepLabelClass(step.number)"
                    >{{ step.label }}</span
                  >
                </div>
                <div
                  v-if="index < steps.length - 1"
                  class="flex-grow h-0.5 mx-2 transition-all duration-400"
                  :class="step.number < currentStep ? 'bg-blue-500' : 'bg-gray-300'"
                ></div>
              </template>
            </div>
          </div>

          <!-- Step Content -->
          <div class="p-6">
            <!-- Step 1: Campaign Information -->
            <div v-if="currentStep === 1" class="space-y-4 animate-fadeIn">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __("Campaign Name") }} <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="campaignData.campaign_name"
                  type="text"
                  :placeholder="__('Example: React Candidate Nurturing Q4/2024')"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  :class="{
                    'border-red-500': !campaignData.campaign_name && currentStep > 1,
                  }"
                />
              </div>

              <!-- Status selection -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __("Status") }}
                </label>
                <select
                  v-model="campaignData.status"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  <option value="DRAFT">{{ __("DRAFT") }}</option>
                  <option value="ACTIVE">{{ __("ACTIVE") }}</option>
                  <option value="PAUSED">{{ __("PAUSED") }}</option>
                  <option value="ARCHIVED">{{ __("ARCHIVED") }}</option>
                </select>
              </div>

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
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
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
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  />
                  <p class="mt-1 text-xs text-gray-500">
                    {{ __("Local time") }} ({{ localTzLabel }})
                  </p>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __("Campaign Type") }} <span class="text-red-500">*</span>
                </label>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div
                    class="border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md"
                    :class="
                      campaignData.type === 'NURTURING'
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    "
                    @click="campaignData.type = 'NURTURING'"
                  >
                    <div class="flex items-center">
                      <div
                        class="flex items-center justify-center w-8 h-8 rounded-full mr-3"
                        :class="
                          campaignData.type === 'NURTURING'
                            ? 'bg-blue-100 text-blue-600'
                            : 'bg-gray-100 text-gray-400'
                        "
                      >
                        <FeatherIcon name="heart" class="h-4 w-4" />
                      </div>
                      <div>
                        <div
                          class="text-sm font-medium"
                          :class="
                            campaignData.type === 'NURTURING'
                              ? 'text-blue-900'
                              : 'text-gray-900'
                          "
                        >
                          {{ __("Nurturing") }}
                        </div>
                        <div class="text-xs text-gray-500">
                          {{ __("Long-term candidate engagement") }}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div
                    class="border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md"
                    :class="
                      campaignData.type === 'ATTRACTION'
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    "
                    @click="campaignData.type = 'ATTRACTION'"
                  >
                    <div class="flex items-center">
                      <div
                        class="flex items-center justify-center w-8 h-8 rounded-full mr-3"
                        :class="
                          campaignData.type === 'ATTRACTION'
                            ? 'bg-blue-100 text-blue-600'
                            : 'bg-gray-100 text-gray-400'
                        "
                      >
                        <FeatherIcon name="magnet" class="h-4 w-4" />
                      </div>
                      <div>
                        <div
                          class="text-sm font-medium"
                          :class="
                            campaignData.type === 'ATTRACTION'
                              ? 'text-blue-900'
                              : 'text-gray-900'
                          "
                        >
                          {{ __("Attraction") }}
                        </div>
                        <div class="text-xs text-gray-500">
                          {{ __("Active talent acquisition") }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                  <div
                    class="border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md"
                    :class="
                      campaignData.type === 'RECRUITMENT'
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    "
                    @click="campaignData.type = 'RECRUITMENT'"
                  >
                    <div class="flex items-center">
                      <div
                        class="flex items-center justify-center w-8 h-8 rounded-full mr-3"
                        :class="
                          campaignData.type === 'RECRUITMENT'
                            ? 'bg-blue-100 text-blue-600'
                            : 'bg-gray-100 text-gray-400'
                        "
                      >
                        <FeatherIcon name="heart" class="h-4 w-4" />
                      </div>
                      <div>
                        <div
                          class="text-sm font-medium"
                          :class="
                            campaignData.type === 'RECRUITMENT'
                              ? 'text-blue-900'
                              : 'text-gray-900'
                          "
                        >
                          {{ __("RECRUITMENT CAMPAIGN") }}
                        </div>
                        <div class="text-xs text-gray-500">
                          {{ __("Recruitment Job") }}
                        </div>
                      </div>
                    </div>
                  </div>
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
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  :class="{
                    'border-red-500': !campaignData.description && currentStep > 1,
                  }"
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
                  <FeatherIcon
                    :name="getSourceIcon(source.key)"
                    class="h-8 w-8 mx-auto mb-2 text-gray-400"
                  />
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
                  <FeatherIcon
                    :name="getSourceIcon(selectedSource)"
                    class="h-6 w-6 text-blue-600"
                  />
                  <h4 class="text-lg font-medium text-gray-900">
                    {{ sources.find((s) => s.key === selectedSource)?.title }}
                    {{ __("Manually") }}
                  </h4>
                </div>

                <!-- Data Source Type Selection (when Data Source is selected) -->
                <div
                  v-if="selectedSource === 'datasource' && dataSourceSelectionLevel === 1"
                  class="space-y-4"
                >
                  <h4 class="text-lg font-medium text-gray-900 mb-4">
                    {{ __("Select Data Source Type") }}
                  </h4>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div
                      v-for="sourceType in dataSourceTypes"
                      :key="sourceType.key"
                      class="border rounded-lg p-4 text-center cursor-pointer transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg border-gray-200 hover:border-gray-300"
                      @click="selectDataSourceType(sourceType.key)"
                    >
                      <FeatherIcon
                        :name="sourceType.icon"
                        class="h-8 w-8 mx-auto mb-2 text-gray-400"
                      />
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
                <div
                  v-else-if="
                    selectedSource === 'datasource' && dataSourceSelectionLevel === 2
                  "
                  class="space-y-4"
                >
                  <div class="mb-4">
                    <h4 class="text-lg font-medium text-gray-900">
                      {{ __("Select") }} {{ selectedDataSourceType }} {{ __("Source") }}
                    </h4>
                  </div>

                  <div v-if="filteredDataSources.length === 0" class="text-center py-8">
                    <div class="text-gray-500 mb-2">
                      {{ __("No") }} {{ selectedDataSourceType }}
                      {{ __("sources available") }}
                    </div>
                    <p class="text-xs text-gray-400">
                      {{ __("Use the Back button to choose a different type") }}
                    </p>
                  </div>

                  <div v-else class="grid grid-cols-1 gap-3">
                    <div
                      v-for="dataSource in filteredDataSources"
                      :key="dataSource.name"
                      class="border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md border-gray-200 hover:border-gray-300"
                      @click="selectSpecificDataSource(dataSource)"
                    >
                      <div class="flex items-center">
                        <FeatherIcon
                          :name="getDataSourceIcon(dataSource.source_type)"
                          class="h-6 w-6 mr-3 text-gray-400"
                        />
                        <div class="flex-1">
                          <div class="text-sm font-medium text-gray-900">
                            {{
                              dataSource.source_name ||
                              dataSource.source_title ||
                              dataSource.name
                            }}
                          </div>
                          <div
                            v-if="dataSource.source_title"
                            class="text-xs text-gray-500 italic"
                          >
                            {{ dataSource.source_title }}
                          </div>
                          <div class="text-xs text-gray-500">
                            {{ dataSource.description || __("Connected platform") }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- DataSource Final Configuration (when specific source is selected) -->
                <div
                  v-else-if="
                    selectedSource === 'datasource' && dataSourceSelectionLevel === 3
                  "
                  class="space-y-4"
                >
                  <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div class="flex items-start justify-between">
                      <div class="flex items-start">
                        <FeatherIcon
                          name="check-circle"
                          class="h-5 w-5 text-green-400 mr-3 mt-0.5"
                        />
                        <div>
                          <h4 class="text-sm font-medium text-green-800">
                            {{ __("Data Source Selected") }}
                          </h4>
                          <div class="mt-1 text-sm text-green-700">
                            <strong>{{
                              configData.selectedDataSource?.source_name
                            }}</strong>
                          </div>
                          <div class="text-xs text-green-600 mt-1">
                            {{ __("Type") }}: {{ selectedDataSourceType }}
                          </div>
                        </div>
                      </div>
                      <div class="flex items-center gap-2">
                        <Button
                          v-if="
                            selectedSource === 'datasource' &&
                            selectedDataSourceType === 'SocialNetwork'
                          "
                          variant="ghost"
                          theme="gray"
                          size="sm"
                          class="text-gray-500 hover:text-gray-700"
                          @click="openSocialConfigEditor"
                        >
                          {{ __("Edit") }}
                        </Button>
                        <Button
                          variant="ghost"
                          theme="gray"
                          size="sm"
                          @click="clearDataSourceSelection"
                          class="text-gray-500 hover:text-gray-700"
                        >
                          {{ __("Change") }}
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- File Configuration -->
                <div v-else-if="selectedSource === 'file'">
                  <component :is="FileConfig" v-model="configData" />
                </div>

                <!-- Search Configuration -->
                <div v-else-if="selectedSource === 'search'">
                  <p class="text-sm text-gray-600 mb-4">
                    {{ __("You'll manually set up your search in the next step.") }}
                  </p>
                  <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div class="flex">
                      <FeatherIcon
                        name="info"
                        class="h-5 w-5 text-blue-400 mt-0.5 mr-2"
                      />
                      <div class="text-sm text-blue-800">
                        {{
                          __(
                            "In the next step, you'll choose the talent segments to search manually."
                          )
                        }}
                      </div>
                    </div>
                  </div>
                </div>

                <!-- DataSource Final Configuration -->
                <div v-else-if="selectedSource === 'datasource' && selectedDataSourceId">
                  <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div class="flex items-center justify-between">
                      <div class="flex items-center">
                        <FeatherIcon
                          name="check-circle"
                          class="h-5 w-5 text-green-400 mr-2"
                        />
                        <div>
                          <div class="text-sm font-medium text-green-800">
                            {{ __("Data Source Selected") }}
                          </div>
                          <div class="text-sm text-green-600">
                            {{
                              configData.selectedDataSource?.source_name ||
                              "Selected data source"
                            }}
                          </div>
                        </div>
                      </div>
                      <Button
                        variant="ghost"
                        theme="gray"
                        size="sm"
                        @click="clearDataSourceSelection"
                        class="text-gray-500 hover:text-gray-700"
                      >
                        <FeatherIcon name="x" class="h-4 w-4 mr-1" />
                        {{ __("Change") }}
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Step 3: Select Target Segment -->
            <div v-if="currentStep === 3" class="animate-fadeIn">
              <div class="space-y-4">
                <div class="text-center mb-6">
                  <h4 class="text-lg font-medium text-gray-900 mb-2">
                    {{ __("Select Target Segment") }}
                  </h4>
                  <p class="text-sm text-gray-600">
                    {{
                      __(
                        "Choose the talent segment you want to target with this campaign"
                      )
                    }}
                  </p>
                </div>

                <!-- Use existing PoolConfig component for segment selection -->
                <component :is="PoolConfig" v-model="configData" />
              </div>
            </div>

            <!-- Step 4: Create Campaign Steps -->
            <div v-if="currentStep === 4" class="animate-fadeIn">
              <!-- Steps Creation Mode Selection -->
              <div v-if="!showStepCreation" class="space-y-6">
                <div class="text-center mb-6">
                  <h4 class="text-lg font-medium text-gray-900 mb-2">
                    {{ __("How would you like to create campaign steps?") }}
                  </h4>
                  <p class="text-sm text-gray-600">
                    {{ __("Choose a method to define the workflow for your campaign") }}
                  </p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <!-- Use Template -->
                  <div
                    class="border rounded-lg p-6 text-center cursor-pointer transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg border-gray-200 hover:border-blue-300"
                    @click="selectStepCreationMode('template')"
                  >
                    <div
                      class="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4"
                    >
                      <FeatherIcon name="file-text" class="h-8 w-8 text-blue-600" />
                    </div>
                    <h5 class="text-lg font-medium text-gray-900 mb-2">
                      {{ __("Use Template") }}
                    </h5>
                    <p class="text-sm text-gray-600 mb-4">
                      {{
                        __(
                          "Select from pre-defined campaign templates with ready-made workflows"
                        )
                      }}
                    </p>
                    <div class="text-xs text-blue-600 font-medium">
                      {{ __("Recommended for consistency") }}
                    </div>
                  </div>

                  <!-- Create Manual -->
                  <div
                    class="border rounded-lg p-6 text-center cursor-pointer transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg border-gray-200 hover:border-green-300"
                    @click="selectStepCreationMode('manual')"
                  >
                    <div
                      class="w-16 h-16 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4"
                    >
                      <FeatherIcon name="plus-circle" class="h-8 w-8 text-green-600" />
                    </div>
                    <h5 class="text-lg font-medium text-gray-900 mb-2">
                      {{ __("Create Manually") }}
                    </h5>
                    <p class="text-sm text-gray-600 mb-4">
                      {{
                        __(
                          "Build custom workflow steps from scratch tailored to your needs"
                        )
                      }}
                    </p>
                    <div class="text-xs text-green-600 font-medium">
                      {{ __("Full customization") }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- Template Selection -->
              <div
                v-if="showStepCreation && stepCreationMode === 'template'"
                class="space-y-6"
              >
                <div class="mb-4">
                  <h4 class="text-lg font-medium text-gray-900">
                    {{ __("Select Campaign Template") }}
                  </h4>
                </div>

                <!-- Loading Templates -->
                <div v-if="loading" class="text-center py-8">
                  <div
                    class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"
                  ></div>
                  <p class="text-gray-600">{{ __("Loading templates...") }}</p>
                </div>

                <!-- Template List -->
                <div v-else-if="campaignTemplates.length > 0" class="space-y-4">
                  <div class="text-sm text-gray-600 mb-3">
                    {{ __("Found") }} {{ campaignTemplates.length }} {{ __("templates") }}
                  </div>
                  <div class="grid grid-cols-1 gap-4 max-h-80 overflow-y-auto">
                    <div
                      v-for="template in campaignTemplates"
                      :key="template.name"
                      class="border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md"
                      :class="
                        selectedTemplate?.name === template.name
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      "
                      @click="selectTemplate(template)"
                    >
                      <div class="flex items-center justify-between">
                        <div class="flex-1">
                          <h6 class="text-sm font-medium text-gray-900">
                            {{ template.template_name }}
                          </h6>
                          <p class="text-xs text-gray-500 mt-1">
                            {{ template.description || __("No description") }}
                          </p>
                          <div class="flex items-center mt-2 space-x-2">
                            <span
                              class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800"
                            >
                              {{ template.campaign_type }}
                            </span>
                            <span class="text-xs text-gray-500"
                              >{{ template.step_count || 0 }} {{ __("steps") }}</span
                            >
                          </div>
                        </div>
                        <div
                          v-if="selectedTemplate?.name === template.name"
                          class="text-blue-600"
                        >
                          <FeatherIcon name="check-circle" class="h-5 w-5" />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- No Templates -->
                <div v-else class="text-center py-8">
                  <FeatherIcon
                    name="inbox"
                    class="h-12 w-12 text-gray-400 mx-auto mb-3"
                  />
                  <p class="text-gray-500">{{ __("No campaign templates available") }}</p>
                </div>
              </div>

              <!-- Manual Step Creation -->
              <div
                v-if="showStepCreation && stepCreationMode === 'manual'"
                class="space-y-6"
              >
                <div class="mb-4">
                  <h4 class="text-lg font-medium text-gray-900">
                    {{ __("Create Campaign Steps Manually") }}
                  </h4>
                </div>

                <!-- Current Steps List -->
                <div v-if="campaignSteps.length > 0" class="space-y-3">
                  <h5 class="text-sm font-medium text-gray-900">
                    {{ __("Campaign Steps") }} ({{ campaignSteps.length }})
                  </h5>
                  <div class="space-y-2">
                    <div
                      v-for="(step, index) in campaignSteps"
                      :key="step.id || index"
                      class="flex items-center p-3 bg-gray-50 rounded-lg border hover:bg-gray-100 transition-colors"
                    >
                      <!-- Step Image -->
                      <!-- <div v-if="step.image" class="w-10 h-10 rounded-lg overflow-hidden mr-3 flex-shrink-0">
                        <img 
                          :src="step.image" 
                          :alt="step.campaign_step_name"
                          class="w-full h-full object-cover"
                        />
                      </div>
                      <div v-else class="w-10 h-10 bg-gray-200 rounded-lg mr-3 flex-shrink-0 flex items-center justify-center">
                        <FeatherIcon name="image" class="h-5 w-5 text-gray-400" />
                      </div> -->

                      <span
                        class="flex items-center justify-center w-6 h-6 bg-blue-100 text-blue-800 text-xs font-medium rounded-full mr-3"
                      >
                        {{ step.step_order }}
                      </span>
                      <div class="flex-1">
                        <div class="text-sm font-medium text-gray-900">
                          {{ step.campaign_step_name }}
                        </div>
                        <div class="text-xs text-gray-500">
                          <span v-if="step.scheduled_at"
                            >{{ __("Scheduled at") }}: {{ step.scheduled_at }}</span
                          >
                          <span v-else
                            >{{ __("Delay") }}: {{ step.delay_in_days || 0 }}
                            {{ __("day(s)") }}</span
                          >
                        </div>
                        <div class="text-xs text-gray-500">
                          {{ step.action_type
                          }}{{
                            step.delay_in_days > 0
                              ? ` • ${step.delay_in_days} days delay`
                              : ""
                          }}
                        </div>
                      </div>
                      <div class="flex items-center space-x-2">
                        <Button
                          variant="ghost"
                          theme="gray"
                          size="sm"
                          @click="editManualStep(step)"
                          class="p-1"
                        >
                          <FeatherIcon name="edit" class="h-4 w-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          theme="gray"
                          size="sm"
                          @click="removeStep(step)"
                          class="p-1 text-red-600 hover:text-red-700"
                        >
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
                      {{
                        campaignSteps.length > 0
                          ? __("Add Another Step")
                          : __("Add First Step")
                      }}
                    </div>
                  </Button>
                </div>

                <!-- Empty State -->
                <div
                  v-if="campaignSteps.length === 0 && !showStepForm"
                  class="text-center py-8 border-2 border-dashed border-gray-300 rounded-lg"
                >
                  <FeatherIcon name="zap" class="h-12 w-12 text-gray-400 mx-auto mb-3" />
                  <p class="text-gray-500 mb-4">{{ __("No steps created yet") }}</p>
                  <Button variant="solid" theme="gray" @click="addManualStep">
                    <div class="flex items-center">
                      <FeatherIcon name="plus" class="h-4 w-4 mr-2" />
                      {{ __("Create First Step") }}
                    </div>
                  </Button>
                </div>
              </div>
            </div>

            <!-- Step 5: Review & Activate -->
            <div v-if="currentStep === 5" class="animate-fadeIn space-y-6">
              <!-- Campaign Summary -->
              <div class="text-center py-4">
                <h3 class="text-xl font-bold mb-2 text-gray-900">
                  {{ __("Review Campaign") }}
                </h3>
                <p class="text-sm text-gray-600">
                  {{ __("Review your campaign details and workflow before finalizing") }}
                </p>
              </div>

              <!-- Campaign Info -->
              <div class="bg-gray-50 rounded-lg p-4">
                <h4 class="text-lg font-medium text-gray-900 mb-3">
                  {{ __("Campaign Information") }}
                </h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="text-sm font-medium text-gray-700">{{
                      __("Campaign Name")
                    }}</label>
                    <p class="text-sm text-gray-900">
                      {{ campaignData.campaign_name || __("Untitled Campaign") }}
                    </p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-gray-700">{{
                      __("Type")
                    }}</label>
                    <p class="text-sm text-gray-900">{{ campaignData.type }}</p>
                  </div>
                  <div class="md:col-span-2">
                    <label class="text-sm font-medium text-gray-700">{{
                      __("Description")
                    }}</label>
                    <p class="text-sm text-gray-900">
                      {{ campaignData.description || __("No description") }}
                    </p>
                  </div>
                </div>
              </div>

              <!-- Campaign Steps -->
              <div class="bg-blue-50 rounded-lg p-4">
                <h4 class="text-lg font-medium text-gray-900 mb-3">
                  {{ __("Campaign Workflow") }}
                </h4>
                <div v-if="campaignSteps.length > 0" class="space-y-2">
                  <div
                    v-for="step in campaignSteps"
                    :key="step.id || step.name"
                    class="flex items-center p-3 bg-white rounded border"
                  >
                    <!-- Step Image -->
                    <div
                      v-if="step.image"
                      class="w-8 h-8 rounded overflow-hidden mr-3 flex-shrink-0"
                    >
                      <img
                        :src="step.image"
                        :alt="step.campaign_step_name"
                        class="w-full h-full object-cover"
                      />
                    </div>
                    <div
                      v-else
                      class="w-8 h-8 bg-gray-200 rounded mr-3 flex-shrink-0 flex items-center justify-center"
                    >
                      <FeatherIcon name="image" class="h-4 w-4 text-gray-400" />
                    </div>

                    <span
                      class="flex items-center justify-center w-6 h-6 bg-blue-100 text-blue-800 text-xs font-medium rounded-full mr-3"
                    >
                      {{ step.step_order }}
                    </span>
                    <div class="flex-1">
                      <div class="text-sm font-medium text-gray-900">
                        {{ step.campaign_step_name }}
                      </div>
                      <div class="text-xs text-gray-500">
                        {{ step.action_type
                        }}{{
                          step.delay_in_days > 0
                            ? ` • ${step.delay_in_days} days delay`
                            : ""
                        }}
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="text-center py-4 text-gray-500">
                  {{ __("No steps configured") }}
                </div>
              </div>

              <!-- Template Info -->
              <div v-if="selectedTemplate" class="bg-green-50 rounded-lg p-4">
                <h4 class="text-lg font-medium text-gray-900 mb-2">
                  {{ __("Template Used") }}
                </h4>
                <p class="text-sm text-gray-600">{{ selectedTemplate.template_name }}</p>
                <p class="text-xs text-gray-500">{{ selectedTemplate.description }}</p>
              </div>

              <!-- Status -->
              <div class="text-center">
                <p class="text-sm text-gray-600 mb-2">
                  {{ __("Campaign will be created in DRAFT status with") }}
                  {{ campaignSteps.length }} {{ __("steps") }}
                </p>
                <p class="text-xs text-gray-500">
                  {{
                    __("You can add profiles and activate the campaign after creation")
                  }}
                </p>
              </div>
            </div>

            <!-- Step 6: Select Job Opening -->
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
              {{ __("Back") }}
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
                {{
                  currentStep === 1 && draftCampaignLoading
                    ? __("Creating Campaign...")
                    : __("Continue")
                }}
              </Button>

              <!-- Step 4: Campaign Steps -->
              <Button
                v-if="currentStep === 4 && !showStepCreation"
                variant="solid"
                theme="gray"
                @click="nextStep"
                :disabled="campaignSteps.length === 0 && !selectedTemplate"
              >
                {{ __("Continue to Review") }}
              </Button>

              <Button
                v-if="
                  currentStep === 4 && showStepCreation && stepCreationMode === 'template'
                "
                variant="solid"
                theme="gray"
                @click="nextStep"
                :disabled="!selectedTemplate || campaignSteps.length === 0"
              >
                {{ __("Continue with Template") }}
              </Button>

              <Button
                v-if="
                  currentStep === 4 && showStepCreation && stepCreationMode === 'manual'
                "
                variant="solid"
                theme="gray"
                @click="nextStep"
                :disabled="campaignSteps.length === 0"
              >
                {{ __("Continue with Steps") }}
              </Button>

              <Button
                v-if="currentStep === 5"
                variant="solid"
                theme="gray"
                @click="finalizeCampaign"
                :loading="activating"
              >
                {{ __("Finalize Campaign") }}
              </Button>
            </div>
          </div>
        </div>
      </template>
    </Dialog>

    <!-- Step Form Dialog -->
    <Dialog
      v-model="showStepForm"
      :options="stepFormDialogOptions"
      :disableOutsideClickToClose="true"
    >
      <template #body>
        <div class="bg-white">
          <!-- Header -->
          <div class="flex justify-between items-center p-6 border-b border-gray-200">
            <h2 class="text-xl font-bold text-gray-900">
              {{ editingStep ? __("Edit Step") : __("Add New Step") }}
            </h2>
            <Button
              theme="gray"
              variant="ghost"
              class="w-7 h-7"
              @click="handleStepFormCancel"
            >
              <FeatherIcon name="x" class="h-4 w-4" />
            </Button>
          </div>

          <!-- Step Form Content -->
          <div class="p-6">
            <form @submit.prevent="handleStepFormSubmit" class="space-y-4">
              <!-- Step Name -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __("Step Name") }}
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
                <div
                  v-if="stepFormErrors.campaign_step_name"
                  class="mt-1 text-sm text-red-600"
                >
                  {{ stepFormErrors.campaign_step_name }}
                </div>
              </div>

              <!-- Social Network: Select Page (connected_accounts) -->
              <!-- <div v-if="showStepSocialFields && selectedSource === 'datasource' && selectedDataSourceType === 'SocialNetwork'">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Select Social Page') }}
                </label>
                <select
                  v-model="stepFormSelectedPageId"
                  :disabled="loadingPages || stepFormLoading"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  <option value="">{{ __('Select a page...') }}</option>
                  <option v-for="p in socialPages" :key="p.external_account_id" :value="p.external_account_id">
                    {{ p.account_name }} ({{ p.account_type }})
                  </option>
                </select>
                <p class="mt-1 text-xs text-gray-500">
                  {{ __('Pages come from connected_accounts of External Connection') }}
                </p>
              </div> -->

              <!-- Step Schedule (Datetime) -->
              <!-- <div v-if="showStepSocialFields">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Time Post News') }}
                </label>
                <input
                  ref="scheduledAtInput"
                  v-model="stepFormData.scheduled_at"
                  type="datetime-local"
                  :min="minScheduledAt"
                  :disabled="stepFormLoading"
                  :step="60"
                  @focus="openScheduledAtPicker"
                  @click="openScheduledAtPicker"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
                <p class="mt-1 text-xs text-gray-500">
                  {{ __('Local time') }} ({{ localTzLabel }})
                </p>
                <div v-if="stepFormErrors.scheduled_at" class="mt-1 text-sm text-red-600">
                  {{ stepFormErrors.scheduled_at }}
                </div>
              </div> -->

              <!-- Step Job Opening (optional) -->
              <!-- <div v-if="showStepSocialFields">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Job Opening (optional)') }}
                </label>
                <select
                  v-model="stepFormSelectedJobId"
                  @change="onStepJobChange"
                  :disabled="stepFormLoading || loadingJobOpenings"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  <option value="">{{ __('Select a job opening...') }}</option>
                  <option v-for="job in jobOpeningsList" :key="job.name" :value="job.name">
                    {{ job.job_title }} {{ job.job_code ? `(${job.job_code})` : '' }}
                  </option>
                </select>
                <p class="mt-1 text-xs text-gray-500">
                  {{ __('If selected, the job\'s description, requirements, and benefits will be inserted into Template Content.') }}
                </p>
              </div> -->

              <div class="grid grid-cols-2 gap-4">
                <!-- Action Type -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __("Action Type") }}
                    <span class="text-red-500">*</span>
                  </label>
                  <select
                    v-model="stepFormData.action_type"
                    :disabled="stepFormLoading"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    :class="{ 'border-red-500': stepFormErrors.action_type }"
                  >
                    <option
                      v-for="option in actionTypeOptions"
                      :key="option.value"
                      :value="option.value"
                      :disabled="option.disabled"
                    >
                      {{ option.label }}
                    </option>
                  </select>
                  <div
                    v-if="stepFormErrors.action_type"
                    class="mt-1 text-sm text-red-600"
                  >
                    {{ stepFormErrors.action_type }}
                  </div>
                </div>

                <!-- Step Order -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __("Step Order") }}
                    <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model.number="stepFormData.step_order"
                    type="number"
                    min="1"
                    max="999"
                    :placeholder="__('Order...')"
                    :disabled="true"
                    readonly
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
                  {{ __("Delay (Days)") }}
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
                  {{ __("Number of days to wait before executing this step") }}
                </p>
                <div
                  v-if="stepFormErrors.delay_in_days"
                  class="mt-1 text-sm text-red-600"
                >
                  {{ stepFormErrors.delay_in_days }}
                </div>
              </div>

              <!-- Template Content -->
              <!-- <div v-if="showStepSocialFields && selectedSource === 'datasource' && selectedDataSourceType === 'SocialNetwork'">
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
              </div> -->

              <!-- Action Config -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __("Action Configuration") }}
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
                  {{ __("JSON configuration for the action (optional)") }}
                </p>
                <div
                  v-if="stepFormErrors.action_config_string"
                  class="mt-1 text-sm text-red-600"
                >
                  {{ stepFormErrors.action_config_string }}
                </div>
              </div>

              <!-- Step Image (optional) -->
              <!-- <div v-if="showStepSocialFields">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Step Image (optional)') }}
                </label>
                <div class="space-y-3">
                  <div v-if="stepFormData.image" class="flex items-center space-x-3">
                    <img 
                      :src="stepFormData.image" 
                      alt="Step image preview"
                      class="w-20 h-20 object-cover rounded-lg border border-gray-200"
                    />
                    <div class="flex-1">
                      <p class="text-sm text-gray-600">{{ __('Current image') }}</p>
                      <p class="text-xs text-gray-500 truncate">{{ stepFormData.image }}</p>
                    </div>
                  </div>
                  
                  <ImageUploader
                    :image_url="stepFormData.image"
                    image_type="image/*"
                    @upload="(url, file) => {
                      stepFormData.image = url
                      console.log('Image uploaded:', url)
                    }"
                    @remove="() => {
                      stepFormData.image = ''
                      console.log('Image removed')
                    }"
                  />
                </div>
                <p class="mt-1 text-xs text-gray-500">
                  {{ __('Upload an image to represent this campaign step (optional)') }}
                </p>
              </div> -->
            </form>
          </div>

          <!-- Footer Actions -->
          <div class="flex justify-end space-x-3 p-6 border-t border-gray-200">
            <Button
              type="button"
              variant="outline"
              theme="gray"
              @click="handleStepFormCancel"
              :disabled="stepFormLoading"
            >
              {{ __("Cancel") }}
            </Button>
            <Button
              type="submit"
              variant="solid"
              theme="gray"
              @click="handleStepFormSubmit"
              :loading="stepFormLoading"
              :disabled="stepFormLoading"
            >
              {{ editingStep ? __("Update Step") : __("Add Step") }}
            </Button>
          </div>
        </div>
      </template>
    </Dialog>

    <!-- Social Network Config Modal -->
    <Dialog
      v-model="showSocialConfigModal"
      :options="{ title: __('Social Network Configuration'), size: 'lg' }"
    >
      <template #body>
        <div class="p-6 space-y-4">
          <!-- Modal Header with Close Button -->
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center space-x-2">
              <FeatherIcon name="users" class="h-5 w-5 text-blue-600" />
              <h3 class="text-base font-medium text-gray-900">
                {{ __("Select Page & Schedule") }}
              </h3>
            </div>
            <Button
              theme="gray"
              variant="ghost"
              class="w-7 h-7"
              @click="showSocialConfigModal = false"
            >
              <FeatherIcon name="x" class="h-4 w-4" />
            </Button>
          </div>

          <!-- Select Social Page -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __("Select Social Page") }}
            </label>
            <select
              v-model="configData.socialConfig.page_id"
              :disabled="loadingPages"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option value="">{{ __("Select a page...") }}</option>
              <option
                v-for="p in socialPages"
                :key="p.external_account_id"
                :value="p.external_account_id"
              >
                {{ p.account_name }} ({{ p.account_type }})
              </option>
            </select>
          </div>

          <!-- Schedule -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __("Time Post News") }}
            </label>
            <input
              v-model="configData.socialConfig.scheduled_at"
              type="datetime-local"
              :min="minScheduledAt"
              :step="60"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
            <p class="mt-1 text-xs text-gray-500">
              {{ __("Local time") }} ({{ localTzLabel }})
            </p>
          </div>

          <!-- Job Opening -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __("Job Opening (optional)") }}
            </label>
            <select
              v-model="configData.socialConfig.job_opening"
              :disabled="loadingJobOpenings"
              @change="onSocialJobOpeningChange"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option value="">{{ __("Select a job opening...") }}</option>
              <option v-for="job in jobOpeningsList" :key="job.name" :value="job.name">
                {{ job.job_title }} {{ job.job_code ? `(${job.job_code})` : "" }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __("Template Content") }}
            </label>
            <textarea
              v-model="stepFormData.template_content"
              rows="4"
              :placeholder="__('Enter template content for this step...')"
              :disabled="stepFormLoading"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
            <p class="mt-1 text-sm text-gray-500">
              {{ __("Content template for emails, SMS, or other actions") }}
            </p>
          </div>

          <!-- Image Uploader -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __("Step Image (optional)") }}
            </label>
            <ImageUploader
              :image_url="configData.socialConfig.image"
              image_type="image/*"
              @upload="
                (url) => {
                  configData.socialConfig.image = url;
                }
              "
              @remove="
                () => {
                  configData.socialConfig.image = '';
                }
              "
            />
            <!-- Image URL input -->
            <div class="mt-2">
              <label class="block text-xs font-medium text-gray-500 mb-1">{{
                __("Image URL")
              }}</label>
              <input
                v-model="configData.socialConfig.image"
                type="text"
                placeholder="https://..."
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>
            <!-- Preview -->
            <div v-if="configData.socialConfig.image" class="mt-3">
              <label class="block text-xs font-medium text-gray-500 mb-1">{{
                __("Preview")
              }}</label>
              <img
                :src="configData.socialConfig.image"
                alt="Preview"
                class="max-h-40 rounded border"
              />
            </div>
          </div>

          <!-- Inline Actions (visible even if footer is hidden) -->
          <div class="flex items-center justify-end gap-2 pt-2">
            <Button
              variant="outline"
              theme="gray"
              @click="showSocialConfigModal = false"
              >{{ __("Cancel") }}</Button
            >
            <Button variant="solid" theme="gray" @click="confirmSocialConfig">{{
              __("Continue")
            }}</Button>
          </div>
        </div>
      </template>
      <template #actions>
        <div class="flex items-center gap-2 p-3">
          <Button variant="outline" theme="gray" @click="showSocialConfigModal = false">{{
            __("Cancel")
          }}</Button>
          <Button variant="solid" theme="gray" @click="confirmSocialConfig">{{
            __("Continue")
          }}</Button>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { Dialog, Button, FeatherIcon } from "frappe-ui";
import { call } from "frappe-ui";
import PoolConfig from "./PoolConfig.vue";
import FileConfig from "./FileConfig.vue";
import ImageUploader from "@/components/Controls/ImageUploader.vue";

import {
  campaignService,
  candidateService,
  candidateSegmentService,
  campaignStepService,
} from "@/services/universalService";
import { campaignTemplateDirectService } from "@/services/campaignTemplateDirectService.js";
import {
  getFilteredJobOpenings,
  getJobOpeningDetails,
} from "@/services/jobOpeningService";
import candidateDataSourceRepository from "@/repositories/candidateDataSourceRepository";

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
});

const emit = defineEmits(["update:modelValue", "success", "draft-created"]);

// Reactive state
const show = ref(false);
const currentStep = ref(1);
const loading = ref(false);
const activating = ref(false);

// Form data
const campaignData = ref({
  campaign_name: "",
  description: "",
  type: "", // Will be selected by user
  status: "DRAFT",
  target_segment: props.preselectedSegment || "",
  source_type: "", // New field: 'DataSource', 'File', 'Search'
  source_file: "", // For File type
  data_source_id: "", // For DataSource type
  source_config: null, // New field to store file mapping, meta, and URL
  job_opening: "", // Changed from job_opening_id to job_opening
  start_date: "", // datetime-local
  end_date: "", // datetime-local
});

const selectedSource = ref(props.preselectedSegment ? "search" : "");
const selectedDataSourceType = ref(""); // ATS, JobBoard, SocialNetwork, TalentPool
const selectedDataSourceId = ref(""); // Specific data source ID
const filteredDataSources = ref([]); // Filtered list to show
const connectedDataSources = ref([]); // From External Connection API
const loadingDataSources = ref(false);

// Track data source selection level: 0=source, 1=type, 2=specific
const dataSourceSelectionLevel = ref(0);

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

// Step Form State
const stepFormData = ref({
  campaign: "",
  campaign_step_name: "",
  action_type: "",
  step_order: 1,
  delay_in_days: 0,
  template_content: "",
  action_config_string: "",
  image: "", // Sử dụng tên field đúng theo doctype
  scheduled_at: "",
});

const stepFormErrors = ref({});
const stepFormLoading = ref(false);

// Manual Step Job Opening selection state
const stepFormSelectedJobId = ref("");

// Job step state
const jobOpeningsList = ref([]);
const loadingJobOpenings = ref(false);
const selectedJobOpeningDetails = ref(null);

// Removed unused toast helper

// Translation helper function
const __ = (text) => text;

// Steps definition
const steps = [
  { number: 1, label: "Information" },
  { number: 2, label: "Select Source" },
  { number: 3, label: "Target Segment" },
  { number: 4, label: "Campaign Steps" },
  { number: 5, label: "Review & Activate" },
  // { number: 6, label: 'Job' }
];

// Source options - 3 fixed choices only
const sources = computed(() => [
  {
    key: "search",
    title: "Search",
    description: "Search and select candidates",
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

// Data source type options
const dataSourceTypes = computed(() => [
  {
    key: "ATS",
    title: "ATS",
    description: "Applicant Tracking System",
    icon: "briefcase",
  },
  {
    key: "JobBoard",
    title: "Job Board",
    description: "Job posting platforms",
    icon: "clipboard",
  },
  {
    key: "SocialNetwork",
    title: "Social Network",
    description: "LinkedIn, Facebook, etc.",
    icon: "users",
  },
  {
    key: "TalentPool",
    title: "Talent Pool",
    description: "External talent pools",
    icon: "user-check",
  },
]);

// Helper function for data source icons
const getDataSourceIcon = (sourceType) => {
  const iconMap = {
    ATS: "database",
    JobBoard: "briefcase",
    SocialNetwork: "users",
    TalentPool: "user-check",
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
      "Import candidates from external data sources (ATS, Job Board, Social Network, etc.)."
    ),
  },
}));

// Load candidates from segment
const loadCandidatesFromSegment = async (segmentId) => {
  try {
    // Get candidates from target segment through Mira Talent Pool
    const candidateSegmentResult = await candidateSegmentService.getList({
      filters: { segment_id: segmentId },
      fields: ["talent_id"],
    });

    if (candidateSegmentResult.success && candidateSegmentResult.data.length > 0) {
      const candidateIds = candidateSegmentResult.data.map((cs) => cs.talent_id);

      // Get the actual candidate data
      const candidateResult = await candidateService.getList({
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

// Computed
const isEditing = computed(() => !!props.editCampaign);

const modalTitle = computed(() => {
  if (isEditing.value) {
    return __("Edit Campaign");
  }
  const titles = {
    1: "Campaign Information",
    2: "Select Data Source",
    3: "Select Target Segment",
    4: "Create Campaign Steps",
    5: "Review & Activate",
    // 6: 'Select Job Opening'
  };
  return titles[currentStep.value] || "Create New Campaign";
});

const step1Valid = computed(() => {
  return !!(
    campaignData.value.campaign_name &&
    campaignData.value.description &&
    campaignData.value.type
  );
});

const canProceed = computed(() => {
  if (currentStep.value === 1) return step1Valid.value;
  if (currentStep.value === 2) {
    if (!selectedSource.value) return false;

    // For datasource: need specific data source selected (level 3)
    if (selectedSource.value === "datasource") {
      if (
        isEditing.value &&
        (selectedDataSourceId.value || campaignData.value.data_source_id)
      ) {
        return true;
      }
      return dataSourceSelectionLevel.value === 3 && !!selectedDataSourceId.value;
    }

    // For file: need file uploaded (if any)
    if (selectedSource.value === "file") {
      return true; // File config handled by component
    }

    // For search: can proceed immediately
    if (selectedSource.value === "search") {
      return true;
    }

    return !!selectedSource.value;
  }
  // Bước 3: luôn cho phép qua, không bắt buộc chọn segment
  if (currentStep.value === 3) return true;
  // Bước 6: cần chọn job opening
  // if (currentStep.value === 6) return !!selectedJobOpeningId.value
  return true;
});

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

      stepFormData.value = {
        ...stepFormData.value,
        template_content: blockBody,
      };
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
    const response = await candidateDataSourceRepository.getDataSources();
    console.log("📊 Data sources response:", response);

    if (response && response.success) {
      dataSources.value = response.data_sources || [];
      console.log(
        `✅ Loaded ${dataSources.value.length} data sources:`,
        dataSources.value
      );
    } else {
      console.error(
        "❌ Failed to load data sources:",
        response?.error || "No success flag"
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
      dataSourceSelectionLevel.value = 1; // Move to type selection level
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

  // Khi chọn SocialNetwork: chỉ hiển thị danh sách nền tảng đã kết nối từ External Connection
  if (sourceType === "SocialNetwork") {
    filteredDataSources.value = connectedDataSources.value.filter(
      (ds) => ds.source_type === "SocialNetwork"
    );
  } else {
    // Mặc định: gộp internal và external theo loại
    const internal = dataSources.value.filter((ds) => ds.source_type === sourceType);
    const external = connectedDataSources.value.filter(
      (ds) => ds.source_type === sourceType
    );
    filteredDataSources.value = [...external, ...internal];
  }

  console.log("✅ Filtered data sources:", filteredDataSources.value);
  console.log(" selectedDataSourceType now:", selectedDataSourceType.value);
  console.log("🎯 dataSourceSelectionLevel now:", dataSourceSelectionLevel.value);
};

const selectSpecificDataSource = (dataSource) => {
  selectedDataSourceId.value = dataSource.name;
  campaignData.value.data_source_id = dataSource.name;
  configData.value.selectedDataSource = dataSource;
  dataSourceSelectionLevel.value = 3; // ✅ Specific data source selected - confirmed level

  // Nếu là SocialNetwork thì mở modal cấu hình
  if (
    selectedSource.value === "datasource" &&
    selectedDataSourceType.value === "SocialNetwork"
  ) {
    loadSocialPages();
    if (jobOpeningsList.value.length === 0) {
      loadJobOpenings();
    }
    if (!configData.value.socialConfig?.scheduled_at) {
      const now = new Date();
      const plus30m = new Date(now.getTime() + 30 * 60 * 1000);
      configData.value.socialConfig.scheduled_at = toLocalDatetimeInput(plus30m);
    }
    showSocialConfigModal.value = true;
  }
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
    const result = await campaignTemplateDirectService.getList({
      filters: { is_active: 1 },
      limit: 50,
    });

    console.log("🔍 Campaign templates result:", result);

    // Extract data array from response
    let templates = [];

    if (
      result &&
      result.success &&
      result.data &&
      result.data.data &&
      Array.isArray(result.data.data)
    ) {
      templates = result.data.data; // ✅ Lấy array từ result.data.data
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
    const templateData = await campaignTemplateDirectService.getById(template.name);

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
    alert(__("Failed to create steps from template. Please try again."));
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
  { label: __("Post to Facebook"), value: "POST_TO_FACEBOOK" },
  { label: __("Post to Zalo"), value: "POST_TO_ZALO" },
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
    alert(__("Campaign context not found. Please try again."));
    return;
  }

  console.log("✅ Draft campaign exists, proceeding...");

  // Reset form and show inline form
  resetStepForm();
  stepFormSelectedJobId.value = "";
  editingStep.value = null;
  showStepForm.value = true;

  console.log("✅ Form opened, showStepForm:", showStepForm.value);
};

const editManualStep = (step) => {
  // Load step data into form
  setStepFormData(step);
  editingStep.value = step;
  showStepForm.value = true;
};

const resetStepForm = () => {
  stepFormData.value = {
    // campaign: '',
    campaign_step_name: "",
    action_type: "",
    step_order: campaignSteps.value.length + 1,
    delay_in_days: 0,
    template_content: "",
    action_config_string: "",
    image: "", // Reset image field
    scheduled_at: "",
  };
  stepFormErrors.value = {};
  stepFormSelectedJobId.value = "";
};

const setStepFormData = (step) => {
  stepFormData.value = {
    campaign: draftCampaign.value?.data?.name || props.editCampaign?.name || "",
    campaign_step_name: step.campaign_step_name || "",
    action_type: step.action_type || "",
    step_order: step.step_order || campaignSteps.value.length + 1,
    delay_in_days: step.delay_in_days || 0,
    template_content: step.template_content || "",
    action_config_string:
      step.action_config_string ||
      (step.action_config ? JSON.stringify(step.action_config, null, 2) : ""),
    image: step.image || "", // Load existing image
    scheduled_at: step.scheduled_at || "",
  };
  stepFormErrors.value = {};
  // Do not carry over previous job opening selection when editing/adding
  stepFormSelectedJobId.value = "";
};

const validateStepForm = () => {
  stepFormErrors.value = {};

  if (!stepFormData.value.campaign_step_name?.trim()) {
    stepFormErrors.value.campaign_step_name = __("Step name is required");
  }

  if (!stepFormData.value.action_type?.trim()) {
    stepFormErrors.value.action_type = __("Action type is required");
  }

  // step_order optional: nếu trống/không hợp lệ sẽ để BE tự gán
  if (stepFormData.value.step_order != null && stepFormData.value.step_order < 1) {
    stepFormErrors.value.step_order = __("Step order must be at least 1");
  }

  if (stepFormData.value.delay_in_days < 0) {
    stepFormErrors.value.delay_in_days = __("Delay cannot be negative");
  }

  // scheduled_at must not be in the past
  if (stepFormData.value.scheduled_at) {
    try {
      const selected = new Date(stepFormData.value.scheduled_at);
      const now = new Date();
      if (selected.getTime() < now.getTime() - 60000) {
        // allow 1m drift
        stepFormErrors.value.scheduled_at = __("Scheduled time cannot be in the past");
      }
    } catch (e) {
      stepFormErrors.value.scheduled_at = __("Invalid datetime");
    }
  }

  // Validate JSON config if provided
  if (stepFormData.value.action_config_string?.trim()) {
    try {
      JSON.parse(stepFormData.value.action_config_string);
    } catch (e) {
      stepFormErrors.value.action_config_string = __("Invalid JSON format");
    }
  }

  return Object.keys(stepFormErrors.value).length === 0;
};

const handleStepFormSubmit = () => {
  if (!validateStepForm()) return;

  stepFormLoading.value = true;

  try {
    // Fallback: if SocialNetwork and fields empty, use socialConfig
    if (
      selectedSource.value === "datasource" &&
      selectedDataSourceType.value === "SocialNetwork"
    ) {
      if (!stepFormSelectedPageId.value && configData.value.socialConfig?.page_id) {
        stepFormSelectedPageId.value = configData.value.socialConfig.page_id;
      }
      if (
        !stepFormData.value.scheduled_at &&
        configData.value.socialConfig?.scheduled_at
      ) {
        stepFormData.value.scheduled_at = configData.value.socialConfig.scheduled_at;
      }
      if (!stepFormSelectedJobId.value && configData.value.socialConfig?.job_opening) {
        stepFormSelectedJobId.value = configData.value.socialConfig.job_opening;
      }
      if (!stepFormData.value.image && configData.value.socialConfig?.image) {
        stepFormData.value.image = configData.value.socialConfig.image;
      }
    }

    const scheduledIso = stepFormData.value.scheduled_at
      ? toIsoIfSet(stepFormData.value.scheduled_at)
      : "";
    const stepData = {
      campaign: draftCampaign.value?.data?.name || draftCampaign.value?.name, // ✅ Sửa: Đảm bảo có campaign
      campaign_step_name: stepFormData.value.campaign_step_name.trim(),
      action_type: stepFormData.value.action_type,
      // step_order: chỉ gửi nếu hợp lệ, để BE auto-increment khi thiếu
      delay_in_days: stepFormData.value.delay_in_days,
      template_content: stepFormData.value.template_content?.trim() || "",
      image: stepFormData.value.image || "", // Include image với tên field đúng
      scheduled_at: scheduledIso,
      action_config: stepFormData.value.action_config_string?.trim()
        ? (() => {
            try {
              return JSON.parse(stepFormData.value.action_config_string);
            } catch {
              return stepFormData.value.action_config_string;
            }
          })()
        : null,
    };

    if (
      Number.isFinite(stepFormData.value.step_order) &&
      stepFormData.value.step_order > 0
    ) {
      stepData.step_order = stepFormData.value.step_order;
    }

    // Attach selected social page to step metadata (kept in action_config)
    if (
      selectedSource.value === "datasource" &&
      selectedDataSourceType.value === "SocialNetwork"
    ) {
      const pageId =
        stepFormSelectedPageId.value || configData.value.socialConfig?.page_id;
      if (pageId) {
        stepData.action_config = stepData.action_config || {};
        stepData.action_config.target_page_id = pageId;
      }
    }

    if (editingStep.value) {
      // Editing existing step
      const index = campaignSteps.value.findIndex((s) => s.id === editingStep.value.id);
      if (index !== -1) {
        campaignSteps.value[index] = {
          ...stepData,
          id: editingStep.value.id,
          campaign: draftCampaign.value?.data?.name || draftCampaign.value?.name,
        };
      }
    } else {
      // Adding new step
      const newStep = {
        id: Date.now(), // Temporary ID
        campaign: draftCampaign.value?.data?.name || draftCampaign.value?.name, // ✅ Sửa: Đảm bảo có campaign
        fromTemplate: false, // Mark as manually created
        ...stepData,
      };
      campaignSteps.value.push(newStep);
      console.log("📝 Added manual campaign step:", newStep);
    }

    // Sort steps by order
    campaignSteps.value.sort((a, b) => a.step_order - b.step_order);

    // Close form and reset transient selections
    showStepForm.value = false;
    editingStep.value = null;
    stepFormSelectedJobId.value = "";
    stepFormSelectedPageId.value = "";

    console.log("Step saved:", stepData);
  } finally {
    stepFormLoading.value = false;
  }
};

const handleStepFormCancel = () => {
  showStepForm.value = false;
  editingStep.value = null;
  resetStepForm();
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
  // Create draft campaign when moving from step 1 to step 2 (only in create mode)
  if (currentStep.value === 1 && !isEditing.value) {
    try {
      await createDraftCampaign();
    } catch (error) {
      // Don't proceed if draft creation fails
      return;
    }
  }

  // Load job openings when moving to step 2
  if (currentStep.value === 2) {
    await loadJobOpenings();
  }

  if (currentStep.value < 5) {
    currentStep.value++;
  }
};

const prevStep = () => {
  if (currentStep.value > 1) {
    // Smart back logic for step 2 - handle multi-level navigation
    if (currentStep.value === 2) {
      console.log("🔙 Back in step 2. Current state:", {
        selectedSource: selectedSource.value,
        selectedDataSourceType: selectedDataSourceType.value,
        selectedDataSourceId: selectedDataSourceId.value,
        dataSourceSelectionLevel: dataSourceSelectionLevel.value,
      });

      // Level 3: Specific data source selected → Go back to source list
      if (selectedSource.value === "datasource" && dataSourceSelectionLevel.value === 3) {
        console.log("🔙 Level 3 → Level 2: Going back to data source list");
        selectedDataSourceId.value = "";
        configData.value.selectedDataSource = "";
        campaignData.value.data_source_id = "";
        dataSourceSelectionLevel.value = 2; // Move back to source list
        return;
      }

      // Level 2: Data source list shown → Go back to type selection
      if (selectedSource.value === "datasource" && dataSourceSelectionLevel.value === 2) {
        console.log("🔙 Level 2 → Level 1: Going back to data source type selection");
        selectedDataSourceType.value = "";
        filteredDataSources.value = [];
        dataSourceSelectionLevel.value = 1; // Move back to type selection
        return;
      }

      // Level 1: Data source type selection → Go back to source selection
      if (selectedSource.value === "datasource" && dataSourceSelectionLevel.value === 1) {
        console.log("🔙 Level 1 → Level 0: Going back to source selection");
        selectedDataSourceType.value = "";
        dataSourceSelectionLevel.value = 0; // Move back to source selection
        return;
      }

      // Level 0: Source selected → Go back to source selection (preserve data)
      if (selectedSource.value) {
        console.log(
          "🔙 Level 0 → Clearing source: Going back to source selection (preserving data)"
        );
        selectedSource.value = "";
        dataSourceSelectionLevel.value = 0; // Reset to initial level
        // Don't reset these - preserve user selections:
        // selectedDataSourceType.value = ''
        // selectedDataSourceId.value = ''
        // filteredDataSources.value = []
        // configData.value.selectedDataSource = ''
        // configData.value.selectedFile = null
        // configData.value.uploadedFileUrl = ''
        return;
      }

      // Level 0: No source selected → Go to previous step
      console.log("🔙 Level 0 → Previous step");
    }

    // Smart back logic for step 4 - handle sub-navigation
    if (currentStep.value === 4) {
      // If in step creation mode, go back to mode selection
      if (showStepCreation.value) {
        console.log("🔙 Step 4: showStepCreation → false");
        showStepCreation.value = false;
        showStepForm.value = false;
        editingStep.value = null;
        return;
      }

      // Standard cleanup for step 4
      // cleaned: removed deprecated showCandidates/selectedCandidates
    }
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
    stepFormData.value.template_content = "";
    return;
  }
  try {
    const details = await getJobOpeningDetails(stepFormSelectedJobId.value);
    if (!details) {
      stepFormData.value.template_content = "";
      return;
    }
    const blockBody = buildJobDetailsForTemplate(details);
    stepFormData.value.template_content = blockBody || "";
  } catch (e) {
    console.error("Failed to build job details for step template:", e);
    stepFormData.value.template_content = "";
  }
};

// Job step methods
const loadJobOpenings = async () => {
  loadingJobOpenings.value = true;
  try {
    const result = await getFilteredJobOpenings({
      limit: 50,
    });

    console.log("result>>>", result);

    if (result) {
      jobOpeningsList.value = result.data || [];
    } else {
      jobOpeningsList.value = [];
    }
  } catch (error) {
    console.error("Error loading job openings:", error);
    jobOpeningsList.value = [];
  } finally {
    loadingJobOpenings.value = false;
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
    scheduled_at: step.scheduled_at ? toIsoIfSet(step.scheduled_at) : null,
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

  console.log(`🔍 Calling campaignStepService.save with payload:`, payload);
  const result = await campaignStepService.save(payload);
  console.log(`✅ Step ${index + 1} created:`, result);
  console.log(`🔍 Step ${index + 1} campaign field:`, result.data?.campaign);
  console.log(`🖼️ Step ${index + 1} image field:`, result.data?.image);
  console.log(`🔍 Step ${index + 1} campaign field:`, result.data?.campaign);

  return result;
};

// Finalize: create (draft flow) or update (edit flow)
const finalizeCampaign = async () => {
  activating.value = true;

  try {
    // EDIT MODE: update campaign fields only for now
    if (isEditing.value && props.editCampaign?.name) {
      // Prepare payload: map inputs and normalize dates
      const startISO = campaignData.value.start_date
        ? new Date(campaignData.value.start_date).toISOString()
        : null;
      const endISO = campaignData.value.end_date
        ? new Date(campaignData.value.end_date).toISOString()
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
        // Add social media fields
        social_page_id: configData.value.socialConfig?.page_id || "",
        social_page_name:
          socialPages.value.find(
            (p) => p.external_account_id === configData.value.socialConfig?.page_id
          )?.account_name || "",
        post_schedule_time: configData.value.socialConfig?.scheduled_at 
          ? new Date(configData.value.socialConfig.scheduled_at).toISOString() 
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
          campaign: props.editCampaign.name,
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
          await campaignStepService.save(stepPayload, s.id);
        } else {
          const created = await campaignStepService.save(stepPayload);
          if (created?.data?.name) keptIds.add(created.data.name);
        }
      }

      // Delete removed steps
      for (const oldId of existingIds) {
        if (!keptIds.has(oldId)) {
          try {
            await campaignStepService.delete(oldId);
          } catch (e) {
            console.warn("Delete step failed", oldId, e);
          }
        }
      }

      // 2) Update campaign fields
      await campaignService.save(updatePayload, props.editCampaign.name);

      emit("success", {
        action: "updated",
        data: { name: props.editCampaign.name, ...updatePayload },
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
            scheduled_at: step.scheduled_at ? toIsoIfSet(step.scheduled_at) : null,
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
            console.log(`🔍 Calling campaignStepService.save with payload:`, payload);
            const result = await campaignStepService.save(payload);

            if (result?.success) {
              stepCount++;
              console.log(`✅ Step ${i + 1} created successfully:`, result.data);
              console.log(`🔗 Step ${i + 1} campaign field:`, result.data?.campaign);
              console.log(
                `📝 Step ${i + 1} campaign_step_name:`,
                result.data?.campaign_step_name
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
        alert(__("Failed to create steps. Please try again."));
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
      toIsoIfSet(campaignData.value.start_date) || new Date().toISOString();
    const endISO =
      toIsoIfSet(campaignData.value.end_date) ||
      new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString();

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
        campaignData.value.source_type || draftCampaign.value.source_type || "Template",
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
    };

    console.log(" Campaign update payload:", campaignUpdatePayload);

    const campaignResult = await campaignService.save(
      campaignUpdatePayload,
      draftCampaign.value.data.name
    );

    console.log("📋 Campaign update result:", campaignResult);

    if (!campaignResult.success) {
      throw new Error(campaignResult.message || "Failed to finalize campaign");
    }

    // 3) Done
    emit("success", { action: "create", data: campaignResult.data });
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

    alert(msg);
  } finally {
    activating.value = false;
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
    target_segment: props.preselectedSegment || "",
    source_type: "",
    source_file: "",
    data_source_id: "",
    source_config: null,
    job_opening: "",
    start_date: "",
    end_date: "",
    last_scheduled_at: "",
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
  stepFormData.value = {
    campaign: "",
    campaign_step_name: "",
    action_type: "",
    step_order: 1,
    delay_in_days: 0,
    template_content: "",
    action_config_string: "",
    image: "", // Reset image field
    scheduled_at: "",
  };
  stepFormErrors.value = {};
  stepFormLoading.value = false;
  draftCampaign.value = null;

  // Reset job step states
  jobOpeningsList.value = [];
  loadingJobOpenings.value = false;
  selectedJobOpeningDetails.value = null;

  // Reset candidates
  // Removed: deprecated mockCandidates state
};

// Load data sources on component mount
onMounted(async () => {
  console.log("🚀 CampaignWizard mounted, loading initial data...");
  await loadDataSources();
  console.log("✅ Initial data loading completed");
});

// Draft campaign for steps creation
const draftCampaign = ref(null);
const draftCampaignLoading = ref(false);

// Create draft campaign when moving from step 1
const createDraftCampaign = async () => {
  if (draftCampaign.value) return; // Already created
  console.log("🔍 draftCampaign.value>>>>>>>>>>>>>>>>>>>>>>>>>>:", draftCampaign.value);
  draftCampaignLoading.value = true;
  try {
    console.log("🔧 Creating draft campaign with user input...");
    // Map selectedSource to source_type (DataSource | File | Search)
    const sourceTypeMap = { datasource: "DataSource", file: "File", search: "Search" };
    const mappedSourceType =
      sourceTypeMap[selectedSource.value] || campaignData.value.source_type || "Search";

    const startISO =
      toIsoIfSet(campaignData.value.start_date) || new Date().toISOString();
    const endISO =
      toIsoIfSet(campaignData.value.end_date) ||
      new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString();

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
      // Add social media fields
      social_page_id: configData.value.socialConfig?.page_id || "",
      social_page_name:
        socialPages.value.find(
          (p) => p.external_account_id === configData.value.socialConfig?.page_id
        )?.account_name || "",
      post_schedule_time: configData.value.socialConfig?.scheduled_at || "",
      template_content: configData.value.socialConfig?.template_content || "",
      social_media_images: configData.value.socialConfig?.image || "",
    };
    console.log("🔍 draftPayload>>>>>>>>>>>>>>>>>>>>>>>>>>:", draftPayload);
    const result = await campaignService.save(draftPayload);
    console.log("🔍 result>>>>>>>>>>>>>>>>>>>>>>>>>>:", result);
    if (result.success) {
      draftCampaign.value = result.data;
      console.log("✅ Draft campaign created:", draftCampaign.value.data.name);

      // Sync start/end back to UI (convert ISO -> datetime-local string)
      try {
        if (draftCampaign.value.start_date) {
          const d = new Date(draftCampaign.value.start_date);
          campaignData.value.start_date = toLocalDatetimeInput(d);
        }
        if (draftCampaign.value.end_date) {
          const d2 = new Date(draftCampaign.value.end_date);
          campaignData.value.end_date = toLocalDatetimeInput(d2);
        }
      } catch (e) {
        console.warn("Failed to map campaign dates to inputs", e);
      }

      // Emit event to refresh the campaign list
      emit("draft-created", draftCampaign.value);
    } else {
      throw new Error(result.message || "Failed to create draft campaign");
    }
  } catch (error) {
    console.error("❌ Error creating draft campaign:", error);
    alert(__("Failed to create draft campaign. Please try again."));

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
    campaignData.value.source_config = JSON.stringify({
      file_name: cfg?.selectedFile?.name || "",
      meta_doctype: "Mira Prospect", // đổi nếu khác
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
      stepFormData.value.scheduled_at = configData.value.socialConfig.scheduled_at || "";
      stepFormSelectedJobId.value = configData.value.socialConfig.job_opening || "";
      if (configData.value.socialConfig.image) {
        stepFormData.value.image = configData.value.socialConfig.image;
      }
      // Template content
      if (
        !stepFormData.value.template_content &&
        configData.value.socialConfig.template_content
      ) {
        stepFormData.value.template_content =
          configData.value.socialConfig.template_content;
      }
    }
  }
});

// Load existing steps for edit mode
const loadExistingSteps = async (campaignName) => {
  try {
    const result = await campaignStepService.getList({
      filters: { campaign: campaignName },
      fields: [
        "name",
        "campaign",
        "campaign_step_name",
        "action_type",
        "step_order",
        "delay_in_days",
        "template",
        "image",
        "scheduled_at",
      ],
      order_by: "step_order asc",
      page_length: 1000,
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
      if (props.editCampaign) {
        const ec = props.editCampaign;
        // Fetch full campaign doc to get select_pages/source_config
        let full = null;
        try {
          full = await campaignService.getFormData(ec.name);
        } catch (e) {
          full = null;
        }
        campaignData.value.campaign_name = ec.campaign_name || ec.name || "";
        campaignData.value.description = ec.description || "";
        campaignData.value.type = ec.type || "";
        campaignData.value.status = ec.status || campaignData.value.status;
        campaignData.value.target_segment =
          ec.target_segment || campaignData.value.target_segment || "";
        campaignData.value.start_date =
          ec.start_date || campaignData.value.start_date || "";
        campaignData.value.end_date = ec.end_date || campaignData.value.end_date || "";
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
        // After prefill, load existing steps and jump to Step 4 so user sees them
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
const loadingPages = ref(false);
const stepFormSelectedPageId = ref("");
const scheduledAtInput = ref(null);

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
const toLocalDatetimeInput = (d = new Date()) => {
  const year = d.getFullYear();
  const month = pad2(d.getMonth() + 1);
  const day = pad2(d.getDate());
  const hours = pad2(d.getHours());
  const minutes = pad2(d.getMinutes());
  return `${year}-${month}-${day}T${hours}:${minutes}`;
};
const minScheduledAt = computed(() => toLocalDatetimeInput(new Date()));
const localTzLabel = Intl.DateTimeFormat().resolvedOptions().timeZone || "Local";

// Helpers for datetime-local -> ISO
const toIsoIfSet = (localStr) => {
  try {
    if (!localStr) return null;

    // Parse ngày giờ local mà không convert timezone
    const [datePart, timePart] = localStr.split("T");
    const [year, month, day] = datePart.split("-").map(Number);
    const [hours, minutes] = timePart.split(":").map(Number);

    // Format thành ISO string mà không thay đổi timezone
    const isoString = `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(
      2,
      "0"
    )}T${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:00`;

    return isoString;
  } catch {
    return null;
  }
};

// Add step form dialog options
const stepFormDialogOptions = computed(() => ({
  title: editingStep.value ? __("Edit Step") : __("Add New Step"),
  size: "lg",
}));

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

const confirmSocialConfig = async () => {
  try {
    // Nếu đã chọn job opening ở bước 2, chuẩn bị trước nội dung template
    const jobId = configData.value.socialConfig?.job_opening;
    if (jobId) {
      try {
        const details = await getJobOpeningDetails(jobId);
        const blockBody = buildJobDetailsForTemplate(details);
        // Lưu sẵn để dùng ở Step 4
        configData.value.socialConfig.template_content = blockBody || "";
      } catch (e) {
        console.warn("Failed to build template from job opening at step 2", e);
        configData.value.socialConfig.template_content = "";
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
    if (!configData.value.socialConfig?.scheduled_at) {
      const now = new Date();
      const plus30m = new Date(now.getTime() + 30 * 60 * 1000);
      configData.value.socialConfig.scheduled_at = toLocalDatetimeInput(plus30m);
    }
    showSocialConfigModal.value = true;
  }
};
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
