<template>
  <div class="min-h-screen bg-gray-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header>
        <div class="flex space-x-3">
          <Button variant="solid" theme="blue" @click="create">
            <template #prefix>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
            </template>
            {{ __('Create New') }}
          </Button>
          <Button variant="outline" theme="gray" @click="edit">
            <template #prefix>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </template>
            {{ __('Edit') }}
          </Button>
        </div>
      </template>
    </LayoutHeader>

    <div class="container mx-auto px-6 py-6">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <h1 class="text-2xl font-bold mb-4">{{ data.job_title || __('Loading...') }}</h1>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-3">
            <div>
              <label class="text-sm text-gray-600">{{ __('Job Code') }}</label>
              <p class="text-sm">{{ data.job_code || '-' }}</p>
            </div>
            <div>
              <label class="text-sm text-gray-600">{{ __('Department') }}</label>
              <p class="text-sm">{{ data.department_name || '-' }}</p>
            </div>
            <div>
              <label class="text-sm text-gray-600">{{ __('Location') }}</label>
              <p class="text-sm">{{ data.location_name || '-' }}</p>
            </div>
            <div>
              <label class="text-sm text-gray-600">{{ __('Status') }}</label>
              <div class="mt-1">
                <span :class="badgeClass(data.approval_status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">{{ data.approval_status }}</span>
              </div>
            </div>
          </div>
          <div class="space-y-3">
            <div>
              <label class="text-sm text-gray-600">{{ __('Posting Date') }}</label>
              <p class="text-sm">{{ formatDate(data.posting_date) || '-' }}</p>
            </div>
            <div>
              <label class="text-sm text-gray-600">{{ __('Closing Date') }}</label>
              <p class="text-sm">{{ formatDate(data.closing_date) || '-' }}</p>
            </div>
            <div>
              <label class="text-sm text-gray-600">{{ __('Owner') }}</label>
              <p class="text-sm">{{ data.owner_id || '-' }}</p>
            </div>
            <div>
              <label class="text-sm text-gray-600">{{ __('Total Applicants') }}</label>
              <p class="text-sm">{{ data.total_applicants || 0 }}</p>
            </div>
          </div>
        </div>
        <div class="mt-6">
          <label class="text-sm text-gray-600">{{ __('Description') }}</label>
          <div class="prose" v-html="data.description"></div>
        </div>
        <div class="mt-6">
          <label class="text-sm text-gray-600">{{ __('Requirements') }}</label>
          <div class="prose" v-html="data.requirements"></div>
        </div>
        <div class="mt-6">
          <label class="text-sm text-gray-600">{{ __('Benefits') }}</label>
          <div class="prose" v-html="data.benefits"></div>
        </div>
      </div>

      <!-- Job Opening Wizard Modal -->
      <div v-if="showForm" class="fixed inset-0 z-50 overflow-y-auto">
        <div class="flex items-center justify-center min-h-screen p-4 text-center">
          <!-- Background overlay - KHÔNG cho phép click để đóng -->
          <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>

          <!-- Modal panel -->
          <div class="relative w-full max-w-6xl mx-auto bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all">
            <div class="flex h-[600px] relative">
              <!-- Close button -->
              <button
                @click="closeForm"
                class="absolute top-4 right-4 z-10 p-2 text-gray-900 rounded-full transition-colors"
                title="Close"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>

              <!-- Left Panel - Steps -->
              <div class="w-80 bg-gray-50 p-6 border-r border-gray-200">
                <div class="mb-6">
                  <h3 class="text-lg font-semibold text-gray-900">
                    {{ isEditMode ? __('Edit Job Opening') : __('Create Job Opening') }}
                  </h3>
                  <p class="text-sm text-gray-500 mt-1">
                    {{ __('Complete 2 simple steps to') }} {{ isEditMode ? __('update your job opening') : __('create your job opening') }}
                  </p>
                </div>

                <!-- Step 1 -->
                <div class="flex items-center mb-4">
                  <div :class="[
                    'flex items-center justify-center w-8 h-8 rounded-full text-sm font-medium',
                    currentStep >= 1 ? 'bg-green-500 text-white' : 'bg-gray-300 text-gray-600'
                  ]">
                    <svg v-if="currentStep > 1" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    <span v-else>1</span>
                  </div>
                  <div class="ml-3">
                    <p class="text-sm font-medium text-gray-900">{{ __('Basic Information') }}</p>
                    <p class="text-xs text-gray-500">{{ __('Job title, position, and department') }}</p>
                  </div>
                </div>

                <!-- Step 2 -->
                <div class="flex items-center mb-6">
                  <div :class="[
                    'flex items-center justify-center w-8 h-8 rounded-full text-sm font-medium',
                    currentStep >= 2 ? 'bg-blue-500 text-white' : 'bg-gray-300 text-gray-600'
                  ]">
                    <svg v-if="currentStep > 2" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    <span v-else>2</span>
                  </div>
                  <div class="ml-3">
                    <p class="text-sm font-medium text-gray-900">{{ __('Job Description') }}</p>
                    <p class="text-xs text-gray-500">{{ __('Description, requirements, and responsibilities') }}</p>
                  </div>
                </div>

                <!-- Progress Bar -->
                <div class="mt-6">
                  <div class="flex justify-between text-xs text-gray-500 mb-1">
                    <span>{{ __('Progress') }}</span>
                    <span>{{ currentStep }}/2</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-500 h-2 rounded-full transition-all duration-300" :style="{ width: `${(currentStep / 2) * 100}%` }"></div>
                  </div>
                </div>
              </div>

              <!-- Right Panel - Content -->
              <div class="flex-1 p-6 overflow-auto">
                <!-- Step 1: Basic Information -->
                <div v-if="currentStep === 1">
                  <div class="mb-6">
                    <h4 class="text-lg font-medium text-gray-900">{{ __('Basic Information') }}</h4>
                    <p class="text-sm text-gray-500">{{ __('Job title, position, and department') }}</p>
                  </div>

                  <div class="space-y-4">
                    <FormControl v-model="form.job_title" type="text" :label="__('Job Title')" :required="true" />
                    <FormControl v-model="form.job_code" type="text" :label="__('Job Code')" />
                    <div class="grid grid-cols-2 gap-4">
                      <FormControl v-model="form.department_name" type="text" :label="__('Department')" />
                      <FormControl v-model="form.location_name" type="text" :label="__('Location')" />
                    </div>
                    <FormControl v-model="form.number_of_openings" type="number" :label="__('Number Of Openings')" />
                    <div class="grid grid-cols-2 gap-4">
                      <FormControl v-model="form.posting_date" type="date" :label="__('Posting Date')" />
                      <FormControl v-model="form.closing_date" type="date" :label="__('Closing Date')" />
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                      <FormControl v-model="form.approval_status" type="select" :label="__('Status')" :options="statusOptions" />
                      <FormControl v-model="form.owner_id" type="select" :label="__('Owner')" :options="ownerOptions" />
                    </div>
                  </div>
                </div>

                <!-- Step 2: Job Description -->
                <div v-if="currentStep === 2">
                  <div class="flex items-center justify-between mb-6">
                    <div>
                      <h4 class="text-lg font-medium text-gray-900">{{ __('Job Description') }}</h4>
                      <p class="text-sm text-gray-500">{{ __('Description, requirements, and responsibilities') }}</p>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      class="mr-10"
                      theme="blue"
                      @click="openAIModal"
                    >
                      <template #prefix>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                      </template>
                      {{ __('AI Generation') }}
                    </Button>
                  </div>

                  <div class="space-y-4">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Job Description') }}</label>
                      <TextEditor
                        ref="descriptionEditor"
                        variant="outline"
                        editor-class="!prose-sm !max-w-full overflow-auto !w-full min-h-[120px] max-h-[150px] py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 hover:shadow-sm focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400 text-gray-800 transition-colors"
                        :bubbleMenu="true"
                        :fixedMenu="true"
                        :content="form.description"
                        :placeholder="__('Provide a detailed description of the job responsibilities and day-to-day tasks')"
                        @change="form.description = $event"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Job Requirements') }}</label>
                      <TextEditor
                        ref="requirementsEditor"
                        variant="outline"
                        editor-class="!prose-sm !max-w-full overflow-auto !w-full min-h-[120px] max-h-[150px] py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 hover:shadow-sm focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400 text-gray-800 transition-colors"
                        :bubbleMenu="true"
                        :fixedMenu="true"
                        :content="form.requirements"
                        :placeholder="__('Specify required qualifications, skills, experience, and education')"
                        @change="form.requirements = $event"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Benefits') }}</label>
                      <TextEditor
                        ref="benefitsEditor"
                        variant="outline"
                        editor-class="!prose-sm !max-w-full overflow-auto !w-full min-h-[120px] max-h-[150px] py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 hover:shadow-sm focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400 text-gray-800 transition-colors"
                        :bubbleMenu="true"
                        :fixedMenu="true"
                        :content="form.benefits"
                        :placeholder="__('Highlight the benefits and what makes this role attractive')"
                        @change="form.benefits = $event"
                      />
                    </div>
                  </div>
                </div>

                <!-- Navigation Buttons -->
                <div class="flex justify-between pt-6 border-t border-gray-200 mt-6">
                  <Button
                    v-if="currentStep > 1"
                    variant="outline"
                    theme="gray"
                    @click="previousStep"
                  >
                    <template #prefix>
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                      </svg>
                    </template>
                    {{ __('Previous') }}
                  </Button>
                  <div v-else></div>

                  <div class="flex space-x-3">
                    <Button variant="outline" theme="gray" @click="closeForm">
                      {{ __('Cancel') }}
                    </Button>
                    <Button
                      v-if="currentStep < 2"
                      variant="solid"
                      theme="blue"
                      @click="nextStep"
                    >
                      {{ __('Next') }}
                      <template #suffix>
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                        </svg>
                      </template>
                    </Button>
                    <Button
                      v-else
                      variant="solid"
                      theme="blue"
                      :loading="saving"
                      @click="save"
                    >
                      {{ isEditMode ? __('Update') : __('Create') }}
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI Generation Modal -->
      <div v-if="showAIModal" class="fixed inset-0 z-[60] overflow-y-auto">
        <div class="flex items-center justify-center min-h-screen p-4 text-center">
          <!-- Background overlay -->
          <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="closeAIModal"></div>

          <!-- Modal panel -->
          <div class="relative w-full max-w-6xl mx-auto bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all">
            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <div class="sm:flex sm:items-start">
                <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
                  <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg leading-6 font-medium text-gray-900">
                      {{ __('Generate Job Description AI') }}
                    </h3>
                    <button
                      @click="closeAIModal"
                      class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition-colors"
                      title="Close"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>

                  <!-- Scrollable content area -->
                  <div class="max-h-[80vh] overflow-y-auto">
                    <div class="p-6">
                      <div class="grid grid-cols-2 gap-6">
                        <!-- Left Panel - Input Configuration -->
                        <div class="space-y-6">
                          <div>
                            <FormControl
                              v-model="aiForm.job_title"
                              type="text"
                              :label="__('Job Title')"
                              :placeholder="__('job_title')"
                              @input="updateMainFormJobTitle"
                            />
                          </div>

                          <div>
                            <FormControl
                              type="select"
                              v-model="aiForm.tone"
                              :options="[
                                { label: __('Professional'), value: __('Professional') },
                                { label: __('Friendly'), value: __('Friendly') },
                                { label: __('Creative'), value: __('Creative') },
                                { label: __('Formal'), value: __('Formal') },
                                { label: __('Casual'), value: __('Casual') }
                              ]"
                              variant="outline"
                              :placeholder="__('Select Tone')"
                              :label="__('Tone')"
                            />
                          </div>

                          <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Thẻ chú thích') }}</label>
                            <textarea
                              v-model="aiForm.comments"
                              rows="4"
                              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                              :placeholder="__('Write your comments here. Example: I want to create a job description for a software engineer with 3 years of experience in React and Node.js.')"
                            ></textarea>
                          </div>

                          <div class="pt-4">
                            <Button
                              variant="solid"
                              theme="gray"
                              @click="generateAIContent"
                              :loading="aiGenerating"
                              class="w-full"
                            >
                              {{ __('Generate') }}
                            </Button>
                          </div>
                        </div>

                        <!-- Right Panel - Rich Text Editors -->
                        <div class="space-y-6">
                          <!-- Job Description -->
                          <div>
                            <div class="flex items-center justify-between mb-2">
                              <label class="block text-sm font-medium text-gray-700">{{ __('Job Description') }}</label>
                              <Button
                                v-if="aiForm.job_description"
                                variant="outline"
                                size="sm"
                                theme="blue"
                                @click="rewriteWithAI('job_description')"
                                :loading="rewritingSection === 'job_description'"
                              >
                                <template #prefix>
                                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                  </svg>
                                </template>
                                {{ __('Rewrite with AI') }}
                              </Button>
                            </div>
                            <TextEditor
                              ref="aiDescriptionEditor"
                              variant="outline"
                              editor-class="!prose-sm !max-w-full overflow-auto !w-full min-h-[200px] max-h-[300px] py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 hover:shadow-sm focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400 text-gray-800 transition-colors"
                              :bubbleMenu="true"
                              :fixedMenu="true"
                              :content="aiForm.job_description"
                              :placeholder="__('Job Description')"
                              @change="aiForm.job_description = $event"
                            />
                          </div>

                          <!-- Job Requirement -->
                          <div>
                            <div class="flex items-center justify-between mb-2">
                              <label class="block text-sm font-medium text-gray-700">{{ __('Job Requirement') }}</label>
                              <Button
                                v-if="aiForm.job_requirement"
                                variant="outline"
                                size="sm"
                                theme="blue"
                                @click="rewriteWithAI('job_requirement')"
                                :loading="rewritingSection === 'job_requirement'"
                              >
                                <template #prefix>
                                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                  </svg>
                                </template>
                                {{ __('Rewrite with AI') }}
                              </Button>
                            </div>
                            <TextEditor
                              ref="aiRequirementEditor"
                              variant="outline"
                              editor-class="!prose-sm !max-w-full overflow-auto !w-full min-h-[200px] max-h-[300px] py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 hover:shadow-sm focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400 text-gray-800 transition-colors"
                              :bubbleMenu="true"
                              :fixedMenu="true"
                              :content="aiForm.job_requirement"
                              :placeholder="__('Job Requirement')"
                              @change="aiForm.job_requirement = $event"
                            />
                          </div>

                          <!-- Job Benefits -->
                          <div>
                            <div class="flex items-center justify-between mb-2">
                              <label class="block text-sm font-medium text-gray-700">{{ __('Job Benefits') }}</label>
                              <Button
                                v-if="aiForm.job_benefits"
                                variant="outline"
                                size="sm"
                                theme="blue"
                                @click="rewriteWithAI('job_benefits')"
                                :loading="rewritingSection === 'job_benefits'"
                              >
                                <template #prefix>
                                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                  </svg>
                                </template>
                                {{ __('Rewrite with AI') }}
                              </Button>
                            </div>
                            <TextEditor
                              ref="aiBenefitsEditor"
                              variant="outline"
                              editor-class="!prose-sm !max-w-full overflow-auto !w-full min-h-[200px] max-h-[300px] py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 hover:shadow-sm focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400 text-gray-800 transition-colors"
                              :bubbleMenu="true"
                              :fixedMenu="true"
                              :content="aiForm.job_benefits"
                              :placeholder="__('Job Benefits')"
                              @change="aiForm.job_benefits = $event"
                            />
                          </div>
                        </div>
                      </div>

                      <!-- Job Posting Preview Section -->
                      <div v-if="aiForm.job_description || aiForm.job_requirement || aiForm.job_benefits" class="mt-6">
                        <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
                          <div class="flex items-center justify-between mb-3">
                            <h4 class="text-sm font-medium text-gray-900">{{ __('Job Posting Preview') }}</h4>
                            <Button
                              size="sm"
                              variant="ghost"
                              @click="showPreview = !showPreview"
                            >
                              <svg v-if="showPreview" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                              </svg>
                              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                              </svg>
                            </Button>
                          </div>
                          <div v-if="showPreview" class="space-y-4 text-sm">
                            <div v-if="aiForm.job_description">
                              <h5 class="font-medium text-gray-800">{{ __('Job Description') }}</h5>
                              <div class="text-gray-600 mt-1" v-html="aiForm.job_description"></div>
                            </div>
                            <div v-if="aiForm.job_requirement">
                              <h5 class="font-medium text-gray-800">{{ __('Requirements') }}</h5>
                              <div class="text-gray-600 mt-1" v-html="aiForm.job_requirement"></div>
                            </div>
                            <div v-if="aiForm.job_benefits">
                              <h5 class="font-medium text-gray-800">{{ __('Benefits') }}</h5>
                              <div class="text-gray-600 mt-1" v-html="aiForm.job_benefits"></div>
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- Action Buttons -->
                      <div v-if="aiForm.job_description || aiForm.job_requirement || aiForm.job_benefits" class="flex justify-between items-center pt-6 border-t border-gray-200 mt-6">
                        <div class="flex space-x-3">
                          <Button variant="outline" theme="gray" @click="previousAIVersion">
                            {{ __('Bản trước') }}
                          </Button>
                          <Button variant="outline" theme="gray" @click="nextAIVersion">
                            {{ __('Bản sau') }}
                          </Button>
                        </div>
                        <div class="flex items-center space-x-3">
                          <!-- Success indicator -->
                          <div v-if="contentApplied" class="flex items-center text-green-600 text-sm">
                            <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                            </svg>
                            {{ __('Đã áp dụng vào form') }}
                          </div>
                          <Button
                            variant="solid"
                            theme="gray"
                            @click="useGeneratedContent"
                            class="bg-gray-800 text-white hover:bg-gray-900"
                          >
                            {{ __('Use Generated Content') }}
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Dialog, Breadcrumbs, Button, FormControl, TextEditor, createResource } from 'frappe-ui'
import { getJobOpeningDetails, updateJobOpeningData } from '@/services/jobOpeningService'

const route = useRoute()
const data = reactive({})
const showForm = ref(false)
const saving = ref(false)
const form = reactive({})
const isEditMode = ref(true)
const currentStep = ref(1)
const showAIModal = ref(false)
const ownerOptions = ref([])

// AI Generation Modal
const aiGenerating = ref(false)
const rewritingSection = ref(null)
const aiHistory = ref([])
const currentAIIndex = ref(-1)
const contentApplied = ref(false)
const showPreview = ref(true)
const aiForm = reactive({
  job_title: '',
  tone: __('Professional'),
  comments: '',
  job_description: '',
  job_requirement: '',
  job_benefits: ''
})

const breadcrumbs = computed(() => [
  { label: __('Job Openings'), route: { name: 'JobOpeningManagement' } },
  { label: data.job_title || __('Loading...'), route: { name: 'JobOpeningDetailView' } }
])

const statusOptions = [
  { label: 'Draft', value: 'Draft' },
  { label: 'Pending Approval', value: 'Pending Approval' },
  { label: 'Approved', value: 'Approved' },
  { label: 'Rejected', value: 'Rejected' }
]

// Load owners for dropdown
const loadOwners = async () => {
  try {
    // Replace with your actual API call to get users
    const response = await fetch('/api/method/frappe.desk.reportview.get', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        doctype: 'User',
        fields: ['name', 'full_name'],
        filters: [['enabled', '=', 1]],
        limit_page_length: 100
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      
      // Xử lý dữ liệu từ cấu trúc {keys: [...], values: [...]}
      if (data.message && data.message.values) {
        ownerOptions.value = data.message.values.map(user => ({
          label: user[1] || user[0], // full_name hoặc name
          value: user[0] // name
        }))
      } else if (Array.isArray(data.message)) {
        // Fallback cho cấu trúc array thông thường
        ownerOptions.value = data.message.map(user => ({
          label: user.full_name || user.name,
          value: user.name
        }))
      }
    }
  } catch (error) {
    console.error('Error loading owners:', error)
    // Fallback options
    ownerOptions.value = [
      { label: __('Select Owner'), value: '' },
      { label: 'Administrator', value: 'Administrator' }
    ]
  }
}

const load = async () => {
  const res = await getJobOpeningDetails(route.params.id)
  Object.assign(data, res)
}

const edit = () => { 
  isEditMode.value = true
  currentStep.value = 1
  Object.assign(form, data); 
  showForm.value = true 
}

const create = () => {
  isEditMode.value = false
  currentStep.value = 1
  Object.assign(form, {
    job_title: '',
    job_code: '',
    department_name: '',
    location_name: '',
    number_of_openings: '',
    posting_date: '',
    closing_date: '',
    approval_status: 'Draft',
    owner_id: '',
    description: '',
    requirements: '',
    benefits: ''
  })
  showForm.value = true
}

const nextStep = () => {
  if (currentStep.value < 2) {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const closeForm = () => {
  showForm.value = false
  currentStep.value = 1
}

const save = async () => {
  saving.value = true
  try {
    if (isEditMode.value) {
      await updateJobOpeningData(form.name, form)
    } else {
      // Logic để tạo mới job opening
      // await createJobOpening(form)
      console.log('Creating new job opening:', form)
    }
    closeForm()
    await load()
  } finally {
    saving.value = false
  }
}

// AI Generation functions
const generateAIContent = async () => {
  aiGenerating.value = true
  try {
    // Reset all fields before generation
    aiForm.job_description = ""
    aiForm.job_requirement = ""
    aiForm.job_benefits = ""

    // Call AI API
    const generateJobDescription = createResource({
      url: "mbw_mira.api.ai.generate_job_description_v2",
      method: "POST",
      params: {
        jobTitle: aiForm.job_title || "",
        tone: aiForm.tone || "Professional",
        comments: aiForm.comments || "",
      },
      onSuccess(data) {
        console.log("Job Description Generated Successfully:", data)
      },
      onError(error) {
        console.error("Error Generating Job Description:", error)
        throw error
      },
      auto: false,
    })

    await generateJobDescription.fetch()
    const apiData = generateJobDescription.data

    // Kiểm tra dữ liệu trả về từ API
    if (!apiData) {
      throw new Error("Dữ liệu API trả về không hợp lệ")
    }

    // Map dữ liệu từ API vào form
    aiForm.job_description = apiData.jobDescription || ""
    aiForm.job_requirement = apiData.jobRequirements || ""
    aiForm.job_benefits = apiData.jobResponsibilities || ""

    // Lưu vào history
    aiHistory.value.push({
      job_description: aiForm.job_description,
      job_requirement: aiForm.job_requirement,
      job_benefits: aiForm.job_benefits
    })
    currentAIIndex.value = aiHistory.value.length - 1

  } catch (error) {
    console.error('Error generating AI content:', error)
    alert('Có lỗi xảy ra khi tạo nội dung AI. Vui lòng thử lại.')
  } finally {
    aiGenerating.value = false
  }
}

const rewriteWithAI = async (section) => {
  rewritingSection.value = section
  try {
    // Call AI API để rewrite section cụ thể
    const generateJobDescription = createResource({
      url: "mbw_mira.api.ai.generate_job_description_v2",
      method: "POST",
      params: {
        jobTitle: aiForm.job_title || "",
        tone: aiForm.tone || "Professional",
        comments: `${aiForm.comments} Rewrite only the ${section} section.`,
      },
      onSuccess(data) {
        console.log("Section Rewritten Successfully:", data)
      },
      onError(error) {
        console.error("Error Rewriting Section:", error)
        throw error
      },
      auto: false,
    })

    await generateJobDescription.fetch()
    const apiData = generateJobDescription.data

    if (apiData) {
      // Cập nhật section cụ thể
      if (section === 'job_description') {
        aiForm.job_description = apiData.jobDescription || ""
      } else if (section === 'job_requirement') {
        aiForm.job_requirement = apiData.jobRequirements || ""
      } else if (section === 'job_benefits') {
        aiForm.job_benefits = apiData.jobResponsibilities || ""
      }
    }

  } catch (error) {
    console.error('Error rewriting section:', error)
    alert('Có lỗi xảy ra khi viết lại section. Vui lòng thử lại.')
  } finally {
    rewritingSection.value = null
  }
}

const useGeneratedContent = () => {
  // Cập nhật form chính với dữ liệu AI
  form.description = aiForm.job_description
  form.requirements = aiForm.job_requirement
  form.benefits = aiForm.job_benefits

  // Đánh dấu đã áp dụng
  contentApplied.value = true

  // Reset sau 3 giây
  setTimeout(() => {
    contentApplied.value = false
  }, 3000)

  // Đóng modal AI nhưng giữ modal tạo job mở
  showAIModal.value = false
}

const previousAIVersion = () => {
  if (currentAIIndex.value > 0) {
    currentAIIndex.value--
    const version = aiHistory.value[currentAIIndex.value]
    aiForm.job_description = version.job_description
    aiForm.job_requirement = version.job_requirement
    aiForm.job_benefits = version.job_benefits
  }
}

const nextAIVersion = () => {
  if (currentAIIndex.value < aiHistory.value.length - 1) {
    currentAIIndex.value++
    const version = aiHistory.value[currentAIIndex.value]
    aiForm.job_description = version.job_description
    aiForm.job_requirement = version.job_requirement
    aiForm.job_benefits = version.job_benefits
  }
}

const openAIModal = () => {
  showAIModal.value = true

  // Copy dữ liệu từ form chính vào AI form
  aiForm.job_title = form.job_title || ''
  aiForm.tone = __('Professional')
  aiForm.comments = ''
}

const closeAIModal = () => {
  showAIModal.value = false
}

const updateMainFormJobTitle = () => {
  // Đồng bộ job_title từ AI form về main form
  form.job_title = aiForm.job_title
}

const badgeClass = (status) => ({
  'Draft': 'bg-gray-100 text-gray-800',
  'Pending Approval': 'bg-yellow-100 text-yellow-800',
  'Approved': 'bg-green-100 text-green-800',
  'Rejected': 'bg-red-100 text-red-800'
}[status] || 'bg-gray-100 text-gray-800')

const formatDate = (date) => date ? new Date(date).toLocaleDateString('vi-VN', { year: 'numeric', month: '2-digit', day: '2-digit' }) : ''

onMounted(async () => {
  await loadOwners()
  await load()
})
</script>