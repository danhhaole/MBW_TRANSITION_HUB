<template>
  <div class="min-h-screen bg-gray-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header>
        <Button variant="solid" theme="gray" @click="openCreateDialog" :loading="loading">
          <template #prefix>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
          </template>
          {{ __('Create New') }}
        </Button>
      </template>
    </LayoutHeader>

    <div class="container mx-auto px-6 py-6">
      <div class="flex items-center justify-between mb-6">
        <div class="relative">
          <input v-model="searchText" type="text" :placeholder="__('Search by job title...')"
            class="block w-60 pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            @input="handleSearchInput" />
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <!-- View mode toggle -->
          <div class="flex rounded-md">
            <button @click="viewMode = 'list'" :class="[
              viewMode === 'list' ? 'bg-black text-white' : 'bg-white text-gray-700 hover:text-gray-500',
              'relative inline-flex items-center px-4 py-2 rounded-l-md border border-gray-300 text-sm font-medium focus:z-10 focus:outline-none focus:ring-1 focus:ring-black focus:border-black'
            ]">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
              </svg>
              {{ __('List') }}
            </button>
            <button @click="viewMode = 'card'" :class="[
              viewMode === 'card' ? 'bg-black text-white' : 'bg-white text-gray-700 hover:text-gray-500',
              'relative inline-flex items-center px-4 py-2 rounded-r-md border border-gray-300 border-l-0 text-sm font-medium focus:z-10 focus:outline-none focus:ring-1 focus:ring-black focus:border-black'
            ]">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
              {{ __('Card') }}
            </button>
          </div>
          <Select v-model="statusFilter" :options="statusOptions" @change="reload" class="min-w-40 text-sm" size="md" variant="outlined" placeholder="All Statuses" />
          <Button variant="outline" theme="gray" @click="reload" :loading="loading" class="flex items-center py-4">
            <template #prefix>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" :class="{ 'animate-spin': loading }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </template>
            {{ __('Refresh') }}
          </Button>
        </div>
      </div>

      <div class="bg-white rounded-lg border border-gray-200">
        <Loading v-if="loading" text="Loading job openings..." />
        <!-- List view -->
        <div v-if="!loading && viewMode === 'list'" class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Job Title') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Status') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Created Date') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Owner') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Actions') }}</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="item in items" :key="item.name" class="hover:bg-gray-50">
                <td class="px-6 py-4">
                  <button class="text-left text-gray-900 text-base hover:underline" @click="view(item)">{{ item.job_title }}</button>
                </td>
                <td class="px-6 py-4">
                  <span :class="badgeClass(item.approval_status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-base font-medium">{{ item.approval_status }}</span>
                </td>
                <td class="px-6 py-4 text-base">{{ formatDate(item.creation) }}</td>
                <td class="px-6 py-4 text-base">{{ item.owner_id }}</td>
                <td class="px-6 py-4 space-x-2">
                  <button @click="view(item)" class="text-gray-600 hover:text-black" title="View">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                  </button>
                  <button @click="edit(item)" class="text-blue-600 hover:text-blue-900" title="Edit">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                  </button>
                  <button @click="remove(item)" class="text-red-600 hover:text-red-900" title="Delete">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                  </button>
                </td>
              </tr>
              <tr v-if="items.length === 0">
                <td colspan="5" class="px-6 py-8 text-center text-gray-500">{{ __('No records') }}</td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination -->
          <div v-if="pagination.pages > 1" class="flex items-center justify-between px-6 py-4 border-t border-gray-200">
            <div class="text-sm text-gray-500">
              {{ __('Display') }} {{ Math.min(((pagination.page - 1) * pagination.limit) + 1, pagination.total) }}-{{ Math.min(pagination.page * pagination.limit, pagination.total) }} {{ __('of') }} {{ pagination.total }} {{ __('records') }}
            </div>
            <div class="flex items-center space-x-2">
              <button
                class="px-3 py-1 rounded border text-sm"
                :class="pagination.page === 1 ? 'text-gray-400 border-gray-200 cursor-not-allowed' : 'text-gray-700 border-gray-300 hover:bg-gray-50'"
                :disabled="pagination.page === 1"
                @click="goToPage(pagination.page - 1)"
              >
                {{ __('Prev') }}
              </button>
              <button
                v-for="p in pagination.pages"
                :key="p"
                class="px-3 py-1 rounded border text-sm"
                :class="p === pagination.page ? 'bg-black text-white border-black' : 'text-gray-700 border-gray-300 hover:bg-gray-50'"
                @click="goToPage(p)"
              >
                {{ p }}
              </button>
              <button
                class="px-3 py-1 rounded border text-sm"
                :class="pagination.page === pagination.pages ? 'text-gray-400 border-gray-200 cursor-not-allowed' : 'text-gray-700 border-gray-300 hover:bg-gray-50'"
                :disabled="pagination.page === pagination.pages"
                @click="goToPage(pagination.page + 1)"
              >
                {{ __('Next') }}
              </button>
            </div>
          </div>
        </div>

        <!-- Card view -->
        <div v-if="!loading && viewMode === 'card'" class="p-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <!-- Job cards -->
          <div v-for="item in items" :key="item.name" class="border rounded-lg p-4 hover:shadow cursor-pointer" @click="view(item)">
            <div class="flex items-start justify-between">
              <h3 class="text-base font-semibold text-gray-900 truncate">{{ item.job_title }}</h3>
              <span :class="badgeClass(item.approval_status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">{{ item.approval_status }}</span>
            </div>
            <p class="text-sm text-gray-500 mt-1">{{ item.department_name }} • {{ item.location_name }}</p>
            <div class="mt-3 text-xs text-gray-500">
              <span>{{ __('Created:') }} {{ formatDate(item.creation) }}</span>
            </div>
            <div class="mt-4 flex items-center justify-end space-x-2">
              <button @click.stop="edit(item)" class="text-blue-600 hover:text-blue-900" title="Edit">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
              </button>
              <button @click.stop="remove(item)" class="text-red-600 hover:text-red-900" title="Delete">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
              </button>
            </div>
          </div>

          <!-- Create New Card at end -->
          <div class="border-2 border-dashed rounded-lg p-6 flex items-center justify-center h-40 cursor-pointer hover:bg-gray-50" @click="openCreateDialog">
            <div class="text-center">
              <div class="mx-auto w-10 h-10 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v12m6-6H6"/></svg>
              </div>
              <div class="mt-3 font-medium">{{ __('Create New Request') }}</div>
              <div class="text-xs text-gray-500">{{ __('Start a new jobopening') }}</div>
            </div>
          </div>

          <!-- Pagination (card view) -->
          <div v-if="pagination.pages > 1" class="col-span-full flex items-center justify-between pt-4">
            <div class="text-sm text-gray-500">
              {{ __('Display') }} {{ Math.min(((pagination.page - 1) * pagination.limit) + 1, pagination.total) }}-{{ Math.min(pagination.page * pagination.limit, pagination.total) }} {{ __('of') }} {{ pagination.total }} {{ __('records') }}
            </div>
            <div class="flex items-center space-x-2">
              <button
                class="px-3 py-1 rounded border text-sm"
                :class="pagination.page === 1 ? 'text-gray-400 border-gray-200 cursor-not-allowed' : 'text-gray-700 border-gray-300 hover:bg-gray-50'"
                :disabled="pagination.page === 1"
                @click="goToPage(pagination.page - 1)"
              >
                {{ __('Prev') }}
              </button>
              <button
                v-for="p in pagination.pages"
                :key="p"
                class="px-3 py-1 rounded border text-sm"
                :class="p === pagination.page ? 'bg-black text-white border-black' : 'text-gray-700 border-gray-300 hover:bg-gray-50'"
                @click="goToPage(p)"
              >
                {{ p }}
              </button>
              <button
                class="px-3 py-1 rounded border text-sm"
                :class="pagination.page === pagination.pages ? 'text-gray-400 border-gray-200 cursor-not-allowed' : 'text-gray-700 border-gray-300 hover:bg-gray-50'"
                :disabled="pagination.page === pagination.pages"
                @click="goToPage(pagination.page + 1)"
              >
                {{ __('Next') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Create Options Dialog -->
      <Dialog v-model="showCreateOptions" :options="{
        title: __('Create Job Opening'),
        size: '4xl',
      }"
      :disableOutsideClickToClose="true"
      >
        <template #body-title>
          <div class="mb-8">
            <h3 class="text-lg font-medium text-gray-900 mb-2">{{ __('Create Job Opening') }}</h3>
            <p class="text-sm text-gray-500">{{ __('Please choose how you want to create a job opening.') }}</p>
          </div>
        </template>

        <template #body-content>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Create with Form Option -->
              <div 
                class="border-2 border-gray-200 rounded-lg p-6 cursor-pointer hover:border-blue-500 hover:shadow-md transition-all duration-200 group"
                @click="openCreateForm"
              >
                <div class="text-center">
                  <div class="mx-auto w-16 h-16 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center mb-4 group-hover:bg-blue-100 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </div>
                  <h4 class="text-lg font-semibold text-gray-900 mb-2">{{ __('Create with Form') }}</h4>
                  <p class="text-sm text-gray-500">{{ __('Fill out information step by step.') }}</p>
                </div>
              </div>

              <!-- Upload Excel/CSV Option -->
              <div 
                class="border-2 border-gray-200 rounded-lg p-6 cursor-pointer hover:border-green-500 hover:shadow-md transition-all duration-200 group"
                @click="openUploadDialog"
              >
                <div class="text-center">
                  <div class="mx-auto w-16 h-16 rounded-full bg-green-50 text-green-600 flex items-center justify-center mb-4 group-hover:bg-green-100 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h4 class="text-lg font-semibold text-gray-900 mb-2">{{ __('Upload Excel/CSV') }}</h4>
                  <p class="text-sm text-gray-500">{{ __('Upload Excel/CSV file to create multiple job openings.') }}</p>
                </div>
              </div>
            </div>
        </template>

        <template #actions>
          <!-- Action Buttons -->
          <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200 mt-8">
            <Button variant="outline" theme="gray" @click="closeCreateOptions">
              {{ __('Cancel') }}
            </Button>
          </div>
        </template>
        
      </Dialog>

      <!-- Job Opening Wizard Dialog -->
      <Dialog v-model="showForm" :options="{
        title: form.name ? __('Edit Job Opening') : __('Create Job Opening'),
        size: '6xl',
      }"
      :disableOutsideClickToClose="true"
      >
        <template #body-title>
          <div>
            <h4 class="text-lg font-medium text-gray-900">{{ __('Basic Information') }}</h4>
            <p class="text-sm text-gray-500">{{ __('Job title, position, and department') }}</p>
          </div>
        </template>
      
        <template #body-content>
          <div class="overflow-y-auto">
            <!-- Basic Information Section -->
            <div class="mb-8">
              <div class="space-y-4">
                <FormControl v-model="form.job_title" type="text" :label="__('Job Title')" :required="true" />
                <!-- Ẩn job_code khỏi form tạo và chỉnh sửa -->
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

            <!-- Job Description Section -->
            <div>
              <div class="flex items-center justify-between mb-6">
                <div>
                  <h4 class="text-lg font-medium text-gray-900">{{ __('Job Description') }}</h4>
                  <p class="text-sm text-gray-500">{{ __('Description, requirements, and responsibilities') }}</p>
                </div>
                <Button
                  variant="outline"
                  size="sm"
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

          </div>
        </template>

        <template #actions>
          <!-- Action Buttons -->
          <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
            <Button variant="outline" theme="gray" @click="closeForm">
              {{ __('Cancel') }}
            </Button>
            <Button
              variant="solid"
              theme="gray"
              :loading="saving"
              @click="save"
            >
              {{ form.name ? __('Update') : __('Create') }}
            </Button>
          </div>
        </template>
      </Dialog>

      <!-- AI Generation Dialog -->
      <Dialog v-model="showAIModal" :options="{
        title: __('Generate Job Description AI'),
        size: '6xl'
      }">
        <template #body-title>
          <div>
            <h4 class="text-lg font-medium text-gray-900">{{ __('Generate Job Description AI') }}</h4>
            <p class="text-sm text-gray-500">{{ __('Generate job description AI') }}</p>
          </div>
        </template>

        <template #body-content>
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
                  <!-- <div>
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
                  </div> -->
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
                      <div class="text-gray-600 mt-1" v-html="formatDescription(aiForm.job_description)"></div>
                    </div>
                    <div v-if="aiForm.job_requirement">
                      <h5 class="font-medium text-gray-800">{{ __('Requirements') }}</h5>
                      <div class="text-gray-600 mt-1" v-html="formatRequirements(aiForm.job_requirement)"></div>
                    </div>
                    <!-- <div v-if="aiForm.job_benefits">
                      <h5 class="font-medium text-gray-800">{{ __('Benefits') }}</h5>
                      <div class="text-gray-600 mt-1" v-html="formatBenefits(aiForm.job_benefits)"></div>
                    </div> -->
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>

        <template #actions>
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
        </template>
      </Dialog>

      <!-- Upload Excel Job Opening Modal -->
      <UploadExcelJobOpeningModal
        v-model="showUploadModal"
        @created="handleJobOpeningsCreated"
        @close="closeUploadModal"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Loading from '@/components/Loading.vue'
import { useToast } from '@/composables/useToast'
const toast = useToast()
import {Breadcrumbs, Button, Select, FormControl, createResource, TextEditor, Dialog } from 'frappe-ui'
import { getFilteredJobOpenings, submitNewJobOpening, updateJobOpeningData, removeJobOpening, getJobOpeningDetails } from '@/services/jobOpeningService'
import UploadExcelJobOpeningModal from '@/components/UploadExcelJobOpeningModal.vue'

const router = useRouter()
const breadcrumbs = [{ label: __('Job Openings'), route: { name: 'JobOpeningManagement' } }]

const loading = ref(false)
const items = ref([])
const pagination = ref({ page: 1, limit: 10, total: 0, pages: 0, has_next: false, has_prev: false })
const searchText = ref('')
const statusFilter = ref('all')
const viewMode = ref('list')
const showForm = ref(false)
const showCreateOptions = ref(false)
const showUploadModal = ref(false) // Thêm biến này
const saving = ref(false)
const form = reactive({})
const showAIModal = ref(false)
const ownerOptions = ref([])
const emit = defineEmits(['cancel'])

const cancel = () => {
	emit('cancel')
}

const statusOptions = [
  { label: __('All Statuses'), value: 'all' },
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
      console.log("data", data);

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

const reload = async () => {
  loading.value = true
  try {
    const res = await getFilteredJobOpenings({ status: statusFilter.value, searchText: searchText.value, page: pagination.value.page || 1, limit: pagination.value.limit || 10 })
    items.value = res.data
    pagination.value = res.pagination || pagination.value
  } finally {
    loading.value = false
  }
}

// Debounce timer used by input and watcher
let searchTimer = null
const triggerDebouncedReload = () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    // Reset to first page when search text changes
    pagination.value.page = 1
    reload()
  }, 300)
}

// Input handler (fires immediately on input, debounced)
const handleSearchInput = () => {
  triggerDebouncedReload()
}

// Also react if searchText changes via code
watch(searchText, () => {
  triggerDebouncedReload()
})

const openCreateDialog = () => {
  showCreateOptions.value = true // Thay đổi từ showForm.value = true
}

const openCreateForm = () => {
  Object.keys(form).forEach(k => delete form[k])
  
  // Set default dates
  const now = new Date()
  
  // Posting Date: đầu tháng hiện tại (ngày 1)
  const postingDate = new Date(now.getFullYear(), now.getMonth(), 1)
  
  // Closing Date: cuối tháng hiện tại
  // Cách này sẽ tự động tính đúng ngày cuối tháng
  const closingDate = new Date(now.getFullYear(), now.getMonth() + 1, 0)
  
  // Format thành YYYY-MM-DD và đảm bảo là local time
  const formatDate = (date) => {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  }
  
  form.posting_date = formatDate(postingDate)
  form.closing_date = formatDate(closingDate)
  
  console.log('Setting dates:', {
    posting: form.posting_date,
    closing: form.closing_date
  })
  
  showCreateOptions.value = false
  showForm.value = true
}

const openUploadDialog = () => {
  showCreateOptions.value = false
  showUploadModal.value = true
}

const closeCreateOptions = () => {
  showCreateOptions.value = false
}

const closeUploadModal = () => {
  showUploadModal.value = false
}

const handleJobOpeningsCreated = async (result) => {
  toast.success(__('Successfully created {{count}} job openings', { count: result.success }))
  await reload()
}

const stripHtml = (html) => {
  if (!html || typeof html !== 'string') return ''
  return html.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim()
}

// Format Job Description - tách paragraph và bullet points với dấu -
const formatDescription = (text) => {
  if (!text) return ''
  
  const cleanText = stripHtml(text)
  
  // Tìm phần đầu tiên (paragraph đầu) và phần bullet points
  const lines = cleanText.split('\n').filter(line => line.trim())
  
  if (lines.length === 0) return `<p>${cleanText}</p>`
  
  const result = []
  let inBulletSection = false
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim()
    
    // Kiểm tra nếu bắt đầu bullet points (có dấu -, •, *, hoặc số)
    if (line.match(/^[-•*\d+\.]/) || line.match(/^-/) || i > 2) {
      if (!inBulletSection) {
        inBulletSection = true
      }
      // Loại bỏ ký tự bullet cũ và thêm lại với format chuẩn
      const cleanLine = line.replace(/^[-•*\s*\d+\.\s*]+/, '').trim()
      if (cleanLine) {
        result.push(`<p>- ${cleanLine}</p>`)
      }
    } else {
      // Paragraph thường
      if (line) {
        result.push(`<p class="leading-relaxed">${line}</p>`)
      }
    }
  }
  
  // Nếu không có bullet points, trả về paragraph đơn
  if (!inBulletSection) {
    return `<p class="leading-relaxed">${cleanText}</p>`
  }
  
  // Chia thành paragraph đầu và bullet section
  const paragraphs = result.filter(item => !item.includes('- '))
  const bullets = result.filter(item => item.includes('- '))
  
  return paragraphs.join('') + 
         (bullets.length > 0 ? `<div class="space-y-2 mt-4">${bullets.join('')}</div>` : '')
}

// Format Requirements - bullet points với dấu •
const formatRequirements = (text) => {
  if (!text) return ''
  
  const cleanText = stripHtml(text)
  
  // Tách thành các mục dựa trên xuống dòng và các dấu phân cách
  const lines = cleanText.split(/[\n\r]+/).filter(line => line.trim())
  
  if (lines.length === 0) return `<p>${cleanText}</p>`
  
  const result = []
  
  for (const line of lines) {
    const trimmedLine = line.trim()
    if (trimmedLine) {
      // Loại bỏ các ký tự bullet cũ và thêm lại với format chuẩn •
      const cleanLine = trimmedLine.replace(/^[-•*\s*\d+\.\s*]+/, '').trim()
      if (cleanLine) {
        result.push(`<li>• ${cleanLine}</li>`)
      }
    }
  }
  
  return result.length > 0 ? `<ul class="list-none space-y-3 text-gray-700">${result.join('')}</ul>` : `<p>${cleanText}</p>`
}

const closeForm = () => {
  showForm.value = false
}

const save = async () => {
  // Validate required fields before saving
  if (!form.job_title || form.job_title.trim() === '') {
    toast.error(__('Please enter Job Title'))
    return
  }

  saving.value = true
  try {
    if (form.name) {
      await updateJobOpeningData(form.name, form)
      toast.success(__('Job opening has been updated successfully'))
    } else {
      const res = await submitNewJobOpening(form)
      Object.assign(form, res)
      toast.success(__('Job opening has been created successfully'))
    }
    showForm.value = false
    await reload()
  } catch (error) {
    toast.error(__('An error occurred while saving job opening.'), error)
  } finally {
    saving.value = false
  }
}

const edit = async (item) => {
  loading.value = true
  try {
    const detail = await getJobOpeningDetails(item.name)
    Object.assign(form, detail)
    showForm.value = true
  } finally {
    loading.value = false
  }
}

const view = (item) => router.push(`/job-openings/${item.name}`)
const remove = async (item) => { if (confirm('Delete this record?')) { await removeJobOpening(item.name, item.job_title); await reload() } }

const badgeClass = (status) => ({
  'Draft': 'bg-gray-100 text-gray-800',
  'Pending Approval': 'bg-yellow-100 text-yellow-800',
  'Approved': 'bg-green-100 text-green-800',
  'Rejected': 'bg-red-100 text-red-800'
}[status] || 'bg-gray-100 text-gray-800')

const formatDate = (date) => date ? new Date(date).toLocaleDateString('vi-VN', { year: 'numeric', month: '2-digit', day: '2-digit' }) : ''

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

// Sửa hàm mở modal AI
const openAIModal = () => {
  showAIModal.value = true

  // Copy dữ liệu từ form chính vào AI form
  aiForm.job_title = form.job_title || ''
  aiForm.tone = __('Professional')
  aiForm.comments = ''
  
  // Copy existing job data to AI form if in edit mode
  if (form.description) aiForm.job_description = form.description
  if (form.requirements) aiForm.job_requirement = form.requirements
  if (form.benefits) aiForm.job_benefits = form.benefits
  
  // Reset AI history when opening with new data
  aiHistory.value = [{
    job_description: aiForm.job_description || '',
    job_requirement: aiForm.job_requirement || '',
    job_benefits: aiForm.job_benefits || ''
  }]
  currentAIIndex.value = 0
}

// Cập nhật hàm đóng modal AI
const closeAIModal = () => {
  showAIModal.value = false
}

const updateMainFormJobTitle = () => {
  // Đồng bộ job_title từ AI form về main form
  form.job_title = aiForm.job_title
}

const goToPage = async (page) => {
  if (!pagination.value.pages) return
  if (page < 1 || page > pagination.value.pages) return
  if (page === pagination.value.page) return
  pagination.value.page = page
  await reload()
}

onMounted(async () => {
  await loadOwners()
  await reload()
})

// Xóa các event listener không cần thiết
</script>