<template>
  <div class="min-h-screen bg-gray-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header>
        <Button variant="outline" theme="gray" @click="editCampaign">
            <template #prefix>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                />
              </svg>
            </template>
            {{ __('Edit Campaign') }}
          </Button>
      </template>
    </LayoutHeader>

    <div class="container mx-auto px-6 py-6">
    <!-- Header with Campaign Info -->
    <!-- <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
      <div class="flex justify-between items-start">
        <div class="flex items-start">
          <Button
            variant="ghost"
            theme="gray"
            @click="$router.go(-1)"
            class="mr-4 mt-1"
          >
            <template #prefix>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 19l-7-7 7-7"
                />
              </svg>
            </template>
          </Button>
          <div>
            <h1 class="text-3xl font-bold text-gray-900 mb-3">
              {{ campaign.campaign_name || __('Loading...') }}
            </h1>
            <div class="flex items-center flex-wrap gap-3">
              <span 
                :class="getStatusClasses(campaign.status)"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
              >
                {{ campaign.status }}
              </span>
              <span class="text-sm text-gray-500">
                {{ __('Created:') }} {{ formatDate(campaign.creation) }}
              </span>
              <span class="text-sm text-gray-500">
                {{ __('Modified:') }} {{ formatDate(campaign.modified) }}
              </span>
            </div>
          </div>
        </div>
        
        <div class="flex items-center space-x-3">
        
        </div>
      </div>
    </div> -->

    <!-- Campaign Details Card -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-gray-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
          </svg>
          		<h3 class="text-lg font-medium text-gray-900">{{ __('Campaign Information') }}</h3>
        </div>
      </div>
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-4">
            <div>
              			<label class="text-sm font-medium text-gray-700">{{ __('Campaign Name') }}</label>
			<p class="mt-1 text-sm text-gray-900">{{ campaign.campaign_name || __('None') }}</p>
		</div>
		<div>
			<label class="text-sm font-medium text-gray-700">{{ __('Description') }}</label>
			<p class="mt-1 text-sm text-gray-900">{{ campaign.description || __('None') }}</p>
		</div>
		<div>
			<label class="text-sm font-medium text-gray-700">{{ __('Status') }}</label>
              <div class="mt-1">
                <span 
                  :class="getStatusClasses(campaign.status)"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                >
                  {{ campaign.status }}
                </span>
              </div>
            </div>
            <div>
              			<label class="text-sm font-medium text-gray-700">{{ __('Type') }}</label>
              <div class="mt-1">
                <span 
                  :class="getTypeClasses(campaign.type)"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                >
                  {{ campaign.type }}
                </span>
              </div>
            </div>
            <!-- <div>
              			<label class="text-sm font-medium text-gray-700">{{ __('Job Opening') }}</label>
              <div class="mt-1 flex items-center">
                <button
                  v-if="jobOpening"
                  @click="viewJobOpening"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800 hover:bg-purple-200 cursor-pointer"
                >
                  {{ jobOpening.job_title }}
                </button>
                				<span v-else class="text-sm text-gray-500">{{ __('None') }}</span>
              </div>
            </div> -->
          </div>
          <div class="space-y-4">
            <div>
              			<label class="text-sm font-medium text-gray-700">{{ __('Start Date') }}</label>
			<p class="mt-1 text-sm text-gray-900">{{ formatDate(campaign.start_date) || __('None') }}</p>
		</div>
		<div>
			<label class="text-sm font-medium text-gray-700">{{ __('End Date') }}</label>
			<p class="mt-1 text-sm text-gray-900">{{ formatDate(campaign.end_date) || __('None') }}</p>
		</div>
		<div>
			<label class="text-sm font-medium text-gray-700">{{ __('Created By') }}</label>
			<p class="mt-1 text-sm text-gray-900">{{ campaign.owner_id || __('None') }}</p>
		</div>
		<div>
			<label class="text-sm font-medium text-gray-700">{{ __('Target Segments') }}</label>
              <div class="mt-1 flex items-center">
                <button
                  v-if="targetSegment"
                  @click="viewTargetSegment"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800 hover:bg-purple-200 cursor-pointer"
                >
                  {{ targetSegment.title }}
                </button>
                				<span v-else class="text-sm text-gray-500">{{ __('None') }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabbed Content -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200">
      <!-- Tabs Header -->
      <div class="bg-white rounded-t-lg">
        <nav class="flex px-2 border-b" aria-label="Tabs">
          <button
              v-for="tab in tabs"
              :key="tab.key"
              @click="activeTab = tab.key"
              :class="[
                'flex items-center py-4 px-6 text-sm font-medium border-b-2',
                activeTab === tab.key
                  ? 'border-black text-black'
                  : 'border-transparent text-gray-600 hover:text-black hover:border-black'
              ]"
            >
            <!-- Chart Timeline Icon for Steps -->
            <svg v-if="tab.key === 'steps'" class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
            <!-- Users Icon for Assigned Profiles (Talent Campaign) -->
            <svg v-else-if="tab.key === 'candidates'" class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"/>
            </svg>

            <!-- Lightning Icon for Actions -->
            <svg v-else-if="tab.key === 'actions'" class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>

            <!-- Document Icon for Mira Candidates -->
            <svg v-else-if="tab.key === 'mira_candidates'" class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5l2 2h5a2 2 0 012 2v14a2 2 0 01-2 2z"/>
            </svg>

            <!-- Social Icon for Social -->
            <svg v-else-if="tab.key === 'social'" class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
            </svg>
            <!-- Chart Icon for Analytics -->
            <svg v-else class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>


            <span>{{ tab.label }}</span>

            <!-- Optional count -->
            
          </button>
        </nav>
      </div>

      <!-- Tab Content -->
      <div class="p-6">
        <!-- Campaign Steps Tab -->
        <div v-if="activeTab === 'steps'">
          <div class="flex justify-between items-center mb-4">
            			<h3 class="text-lg font-medium text-gray-900">{{ __('Campaign Steps') }}</h3>
            <button
              @click="openStepModal()"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-black hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
              </svg>
              				{{ __('Add Step') }}
            </button>
          </div>
          
          <!-- Campaign Steps Table -->
          <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
            <table class="min-w-full divide-y divide-gray-300">
              <thead class="bg-gray-50">
                <tr>
                  				<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Order') }}</th>
				<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Step Name') }}</th>
				<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Action Type') }}</th>
				<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Delay (Days)') }}</th>
				<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Actions') }}</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-if="loadingSteps" class="text-center">
                  <td colspan="5" class="px-6 py-4 text-sm text-gray-500">
                    <div class="flex justify-center">
                      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                    </div>
                  </td>
                </tr>
                <tr v-else-if="sortedCampaignSteps.length === 0" class="text-center">
                  <td colspan="5" class="px-6 py-4 text-sm text-gray-500">{{ __('No steps found') }}</td>
                </tr>
                <tr v-else v-for="(step, idx) in sortedCampaignSteps" :key="step.name" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-black">
                      {{ __('Step') }} {{ step.step_order }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {{ step.campaign_step_name }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span 
                      :class="getActionTypeClasses(step.action_type)"
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    >
                      {{ step.action_type }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ step.delay_in_days }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <button @click="openStepModal(step)" class="text-blue-600 hover:text-blue-900" title="Edit Step">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                      </svg>
                    </button>
                    <button @click="moveStepUp(idx)" :disabled="idx === 0" class="text-gray-600 hover:text-black" title="Move Up">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                      </svg>
                    </button>
                    <button @click="moveStepDown(idx)" :disabled="idx === sortedCampaignSteps.length - 1" class="text-gray-600 hover:text-black" title="Move Down">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                      </svg>
                    </button>
                    <!-- <button @click="copyStep(step)" class="text-purple-600 hover:text-purple-900" title="Copy Step">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16h8M8 12h8m-7-8h6a2 2 0 012 2v12a2 2 0 01-2 2H9a2 2 0 01-2-2V6a2 2 0 012-2z"/>
                      </svg>
                    </button> -->
                    <button @click="deleteStep(step)" class="text-red-600 hover:text-red-900" title="Delete Step">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                      </svg>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Other tabs content -->
<div v-if="activeTab === 'candidates'">
  <div class="flex justify-between items-center mb-4">
    <h3 class="text-lg font-medium text-gray-900">{{ __('Talent Campaign') }}</h3>
    <div class="flex items-center space-x-2">
      <!-- Nút mở modal manual -->
      <button
        @click="openCandidateModal()"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-black hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
        </svg>
        {{ __('Add Manual Talent') }}
      </button>
    </div>
  </div>

  <!-- Talent Campaign Table -->
  <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
    <table class="min-w-full divide-y divide-gray-300">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            {{ __('Full Name') }}
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            {{ __('ID') }}
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            {{ __('Email') }}
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            {{ __('Phone') }}
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            {{ __('Source') }}
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            {{ __('Actions') }}
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <!-- Empty -->
        <tr v-if="talentCampaignRecords.length === 0" class="text-center">
          <td colspan="6" class="px-6 py-4 text-sm text-gray-500">
            {{ __('No profiles assigned') }}
          </td>
        </tr>

        <!-- Rows -->
        <tr
          v-else
          v-for="record in talentCampaignRecords"
          :key="record.name"
          class="hover:bg-gray-50"
        >
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
            {{ record.full_name }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            {{ record.name }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            {{ record.email || '-' }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            {{ record.phone || '-' }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm">
            <span
              v-if="record.__source === 'mira_talent'"
              class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
            >
              Talent
              <span v-if="record.segment" class="ml-1 text-xs opacity-75">({{ record.segment }})</span>
            </span>
            <span
              v-else-if="record.__source === 'mira_contact'"
              class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
            >
              Contact
            </span>
            <span
              v-else
              class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-200 text-gray-800"
            >
              Unknown
            </span>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
            <!-- Unassign button -->
            <button
              @click="unassignCandidate(record)"
              class="text-red-600 hover:text-red-900"
              title="Remove from Campaign"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<div v-if="activeTab === 'mira_candidates'">
  <div class="flex justify-between items-center mb-4">
    <h3 class="text-lg font-medium text-gray-900">{{ __('Candidates') }}</h3>
  </div>

  <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
    <table class="min-w-full divide-y divide-gray-300">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Avatar') }}</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Full Name') }}</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Email') }}</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Phone') }}</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Headline') }}</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Source') }}</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Status') }}</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Last Interaction') }}</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-if="loadingMiraCandidates" class="text-center">
          <td colspan="8" class="px-6 py-4">
            <div class="flex justify-center">
              <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            </div>
          </td>
        </tr>
        <tr v-else-if="miraCandidates.length === 0" class="text-center">
          <td colspan="8" class="px-6 py-4 text-sm text-gray-500">
            {{ __('No Candidates found') }}
          </td>
        </tr>
        <tr v-else v-for="c in miraCandidates" :key="c.name" class="hover:bg-gray-50">
          <td class="px-6 py-4 whitespace-nowrap">
            <img v-if="c.avatar" :src="c.avatar" alt="avatar" class="h-8 w-8 rounded-full object-cover"/>
            <div v-else class="h-8 w-8 rounded-full bg-gray-200"></div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ c.full_name }}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ c.email || '-' }}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ c.phone || '-' }}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ c.headline || '-' }}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ c.source || '-' }}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm">
            <span
              :class="{
                'bg-gray-100 text-gray-800': c.status === 'NEW',
                'bg-blue-100 text-blue-800': c.status === 'SOURCED',
                'bg-yellow-100 text-yellow-800': c.status === 'NURTURING',
                'bg-green-100 text-green-800': c.status === 'ENGAGED',
                'bg-red-100 text-red-800': c.status === 'ARCHIVED'
              }"
              class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
            >
              {{ c.status }}
            </span>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            {{ formatDateTime(c.last_interaction) || '-' }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

        
        <div v-if="activeTab === 'actions'">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">{{ __('Campaign Actions') }}</h3>
            <!-- <button
              @click="openActionModal()"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-black hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
              </svg>
              {{ __('Add Action') }}
            </button> -->
          </div>
          
          <!-- Actions Table -->
          <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
            <table class="min-w-full divide-y divide-gray-300">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Campaign Step') }}</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Status') }}</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Scheduled At') }}</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Executed At') }}</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Actions') }}</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-if="loadingActions" class="text-center">
                  <td colspan="5" class="px-6 py-4 text-sm text-gray-500">
                    <div class="flex justify-center">
                      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                    </div>
                  </td>
                </tr>
                <tr v-else-if="actions.length === 0" class="text-center">
                  <td colspan="5" class="px-6 py-4 text-sm text-gray-500">{{ __('No actions found') }}</td>
                </tr>
                <tr v-else v-for="action in actions" :key="action.name" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {{ action.campaign_step }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span 
                      :class="getActionStatusClasses(action.status)"
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    >
                      {{ action.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatDateTime(action.scheduled_at) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatDateTime(action.executed_at) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <button
                      @click="viewActionDetails(action)"
                      class="text-blue-600 hover:text-blue-900"
                      title="View Details"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                      </svg>
                    </button>
                    <button
                      @click="deleteAction(action)"
                      class="text-red-600 hover:text-red-900"
                      title="Delete Action"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                      </svg>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <div v-if="activeTab === 'social'">
          
          <!-- Campaign Social Media Posts -->
          <CampaignSocialList
            :campaign-id="route.params.id"
            :campaign-status="campaign.status"
            :social-pages="socialPages"
            :external-connections="externalConnections"
            :jobOpenings="jobOpeningsList"
            :loading-pages="loadingSocialPages"
            :loading-connections="loadingConnections"
            :loadingJobOpenings="loadingJobOpenings"
            @refresh="loadTalentCampaign"
          />
        </div>
        
        <div v-if="activeTab === 'interactions'">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">{{ __('Campaign Interactions') }}</h3>
          </div>
          
          <!-- Loading State -->
          <div v-if="loadingInteractions" class="flex justify-center items-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span class="ml-2 text-gray-600">{{ __('Loading interactions...') }}</span>
          </div>
          
          <!-- Empty State -->
          <div v-else-if="!interactions.length" class="text-center py-8">
            <FeatherIcon name="activity" class="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 class="text-lg font-medium text-gray-900 mb-2">{{ __('No interactions yet') }}</h3>
            <p class="text-gray-600">{{ __('Interactions will appear here when users engage with your campaign.') }}</p>
          </div>
          
          <!-- Interactions Table -->
          <div v-else class="bg-white shadow overflow-hidden sm:rounded-md">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ __('Type') }}
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ __('Contact') }}
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ __('Action') }}
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ __('Description') }}
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ __('Date') }}
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="interaction in interactions" :key="interaction.name" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                          :class="getInteractionTypeClass(interaction.interaction_type)">
                      {{ formatInteractionType(interaction.interaction_type) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900">
                      {{ interaction.talent_id || interaction.contact_id || __('Unknown') }}
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ interaction.action || '-' }}
                  </td>
                  <td class="px-6 py-4">
                    <div class="text-sm text-gray-900 max-w-xs truncate" :title="interaction.description">
                      {{ interaction.description || '-' }}
                    </div>
                    <div v-if="interaction.url" class="text-xs text-blue-600 truncate max-w-xs" :title="interaction.url">
                      {{ interaction.url }}
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatDateTime(interaction.creation) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <div v-if="activeTab === 'analytics'">
          <h3 class="text-lg font-medium text-gray-900 mb-4">{{ __('Campaign Analytics') }}</h3>
          
          <!-- Stats Cards -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div class="bg-white p-4 rounded-lg shadow border text-center">
              <div class="text-2xl font-bold text-blue-600">{{ campaignSteps.length }}</div>
              <div class="text-sm text-gray-500">{{ __('Total Steps') }}</div>
            </div>
            <div class="bg-white p-4 rounded-lg shadow border text-center">
              <div class="text-2xl font-bold text-green-600">{{ candidateCampaigns.length }}</div>
              <div class="text-sm text-gray-500">{{ __('Assigned Profiles') }}</div>
            </div>
            <div class="bg-white p-4 rounded-lg shadow border text-center">
              <div class="text-2xl font-bold text-yellow-600">{{ getActiveCandidates() }}</div>
              <div class="text-sm text-gray-500">{{ __('Active Profiles') }}</div>
            </div>
            <div class="bg-white p-4 rounded-lg shadow border text-center">
              <div class="text-2xl font-bold text-purple-600">{{ getCompletedCandidates() }}</div>
              <div class="text-sm text-gray-500">{{ __('Completed Profiles') }}</div>
            </div>
          </div>
          
          <!-- Chart placeholder -->
          <div class="bg-white p-6 rounded-lg shadow border">
            <h4 class="text-lg font-medium text-gray-900 mb-4">{{ __('Campaign Progress') }} </h4>
            <div class="text-center p-8">
              <svg class="w-16 h-16 text-gray-300 mx-auto" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
              <p class="text-gray-500 mt-4">
                {{ __('Analytics charts will be implemented here') }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Step Modal with Frappe UI Dialog -->
    <Dialog
      v-model="showStepModal"
      :options="{
        title: stepFormData.name ? 'Edit Campaign Step' : 'Add Campaign Step',
        size: 'lg'
      }"
    >
      <template #body>
        <div class="p-6">

          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ stepFormData.name ? 'Edit Campaign Step' : 'Add Campaign Step' }}
          </h3>
          <div class="space-y-4">
            <!-- Step Name -->
            <FormControl
              v-model="stepFormData.campaign_step_name"
              type="text"
              :label="__('Step Name')"
              :placeholder="__('Enter step name')"
              :required="true"
            />

            <!-- Step Order -->
            <FormControl
              v-model="stepFormData.step_order"
              type="number"
              :label="__('Step Order')"
              :placeholder="__('Enter step order')"
              :required="true"
              :min="1"
              :disabled="true"
            />

            <!-- Action Type -->
            <FormControl
              v-model="stepFormData.action_type"
              type="select"
              :label="__('Action Type')"
              :required="true"
              :options="[{ label: __('Select action type'), value: '' }, ...stepTypeOptions]"
            />

            <!-- Delay in Days -->
            <FormControl
              v-model="stepFormData.delay_in_days"
              type="number"
              :label="__('Delay in Days')"
              :placeholder="__('Enter delay in days')"
              :min="0"
            />

            <!-- Template -->
            <FormControl
              v-model="stepFormData.template"
              type="textarea"
              :label="__('Template')"
              :placeholder="__('Enter template content')"
              :rows="3"
            />

            <!-- Buttons -->
            <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
              <Button
                variant="outline"
                theme="gray"
                @click="closeStepModal"
              >
                {{ __('Cancel') }}
              </Button>
              <Button
                variant="solid"
                theme="gray"
                :loading="savingStep"
                @click="saveStep"
              >
                {{ stepFormData.name ? __('Update') : __('Save') }}
              </Button>
            </div>
          </div>
        </div>
      </template>
    </Dialog>

    <!-- Candidate Assignment Modal with Frappe UI Dialog -->
<Dialog v-model="showCandidateModal" :options="{ size: 'md' }">
  <template #body>
    <div class="flex justify-between items-center mb-4 px-6 pt-6">
      <h3 class="text-lg font-medium text-gray-900">
        {{ candidateFormData.name ? __('Edit Manual Talent') : __('Add Manual Talent') }}
      </h3>
      <Button variant="outline" theme="gray" @click="closeCandidateModal" class="flex items-center">
        <FeatherIcon name="x" class="w-4 h-4" />
      </Button>
    </div>

    <div class="px-6 pb-6">
      <div class="space-y-4">
        <!-- Full Name -->
        <FormControl
          v-model="candidateFormData.full_name"
          type="text"
          :label="__('Full Name')"
          :required="true"
          :placeholder="__('Enter full name')"
        />

        <!-- Email -->
        <FormControl
          v-model="candidateFormData.email"
          type="email"
          :label="__('Email')"
          :placeholder="__('Enter email address')"
        />

        <!-- Phone -->
        <FormControl
          v-model="candidateFormData.phone_number"
          type="text"
          :label="__('Phone Number')"
          :placeholder="__('Enter phone number')"
        />

        <!-- Buttons -->
        <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
          <Button variant="outline" theme="gray" @click="closeCandidateModal">
            {{ __('Cancel') }}
          </Button>
          <Button
            variant="solid"
            theme="gray"
            :loading="savingCandidate"
            :disabled="!candidateFormData.full_name"
            @click="assignCandidate"
          >
            {{ candidateFormData.name ? __('Update') : __('Save') }}
          </Button>
        </div>
      </div>
    </div>
  </template>
</Dialog>


    <!-- Action Modal with Frappe UI Dialog -->
    <Dialog
      v-model="showActionModal"
      :options="{
        title: actionFormData.name ? 'Edit Action' : 'Add Action',
        size: 'lg'
      }"
    >
      <template #body>
        <div class="p-6">
          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-4">
              {{ actionFormData.name ? 'Edit Action' : 'Add Action' }}
            </h3>
          </div>
          <div class="space-y-4">
            <!-- Campaign Step -->
            <FormControl
              v-model="actionFormData.campaign_step"
              type="select"
              :label="__('Campaign Step')"
              :required="true"
            />

            <!-- Candidate Campaign -->
            <FormControl
              v-model="actionFormData.candidate_campaign_id"
              type="select"
              :label="__('Candidate')"
              :required="true"
            />

            <!-- Status -->
            <FormControl
              v-model="actionFormData.status"
              type="select"
              :label="__('Status')"
              :required="true"
              :options="[{ label: __('Select status'), value: '' }, ...actionStatusOptions]"
            />

            <!-- Scheduled At -->
            <FormControl
              v-model="actionFormData.scheduled_at"
              type="datetime-local"
              :label="__('Scheduled At')"
            />

            <!-- Executed At -->
            <FormControl
              v-if="actionFormData.status === 'EXECUTED'"
              v-model="actionFormData.executed_at"
              type="datetime-local"
              :label="__('Executed At')"
            />

            <!-- Notes -->
            <FormControl
              v-model="actionFormData.notes"
              type="textarea"
              :label="__('Notes')"
              :placeholder="__('Enter any notes about this action')"
              :rows="3"
            />

            <!-- Buttons -->
            <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
              <Button
                variant="outline"
                theme="gray"
                @click="closeActionModal"
              >
                {{ __('Cancel') }}
              </Button>
              <Button
                variant="solid"
                theme="gray"
                :loading="savingAction"
                @click="saveAction"
              >
                {{ actionFormData.name ? __('Update') : __('Save') }}
              </Button>
            </div>
          </div>
        </div>
      </template>
    </Dialog>
    <!-- Edit Campaign Modal -->
    <CampaignForm
      v-model="showEditCampaignModal"
      :campaign="campaign"
      @success="handleCampaignUpdated"
    />
    
    <!-- Add Talent/Contact Modal -->
    <Dialog v-model="showAddTalentModal" :options="{ title: __('Add Talent/Contact to Campaign'), size: 'xl' }">
      <template #body-content>
        <div class="space-y-6">
          <!-- Source Selection -->
          <div>
            <h4 class="text-lg font-medium text-gray-900 mb-4">{{ __('Select Source') }}</h4>
            <div class="flex space-x-6 mb-4 text-sm">
              <label class="flex items-center space-x-2">
                <input type="radio" value="mira_contact" v-model="searchSource" />
                <span>Contact</span>
              </label>
              <label class="flex items-center space-x-2">
                <input type="radio" value="mira_talent" v-model="searchSource" />
                <span>Talent</span>
              </label>
            </div>
          </div>

          <!-- Segment Filter for Talent -->
          <div v-if="searchSource === 'mira_talent'" class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __("Filter by Segment (Optional)") }}
            </label>
            <Link
              doctype="Mira Segment"
              v-model="selectedSegment"
              :placeholder="__('Select segment to filter talents...')"
            />
            <p class="mt-1 text-xs text-gray-500">
              {{ __("Leave empty to show all talents") }}
            </p>
          </div>

          <!-- Search Box -->
          <div v-if="searchSource" class="mb-4">
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="Search candidates..."
              class="w-full border rounded px-3 py-2 text-sm"
            />
          </div>

          <!-- Advanced Filters -->
          <div v-if="searchSource" class="mb-4">
            <details class="border rounded-lg">
              <summary class="px-4 py-2 bg-gray-50 cursor-pointer text-sm font-medium text-gray-700 hover:bg-gray-100">
                {{ __('Advanced Filters') }}
              </summary>
              <div class="p-4 space-y-4">
                <!-- Contact Filters -->
                <div v-if="searchSource === 'mira_contact'" class="space-y-3">
                  <h5 class="text-sm font-medium text-gray-900">{{ __('Contact Filters') }}</h5>
                  <div class="flex flex-wrap gap-4">
                    <label class="flex items-center space-x-2">
                      <input type="checkbox" v-model="advancedFilters.missingEmail" class="rounded" />
                      <span class="text-sm">{{ __('Missing Email') }}</span>
                    </label>
                    <label class="flex items-center space-x-2">
                      <input type="checkbox" v-model="advancedFilters.missingPhone" class="rounded" />
                      <span class="text-sm">{{ __('Missing Phone') }}</span>
                    </label>
                  </div>
                </div>

                <!-- Talent Filters -->
                <div v-if="searchSource === 'mira_talent'" class="space-y-3">
                  <h5 class="text-sm font-medium text-gray-900">{{ __('Talent Filters') }}</h5>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label class="block text-xs font-medium text-gray-700 mb-1">{{ __('Skills') }}</label>
                      <input
                        v-model="advancedFilters.skills"
                        type="text"
                        placeholder="e.g. JavaScript, Python"
                        class="w-full border rounded px-2 py-1 text-sm"
                      />
                    </div>
                    <div>
                      <label class="block text-xs font-medium text-gray-700 mb-1">{{ __('Tags') }}</label>
                      <input
                        v-model="advancedFilters.tags"
                        type="text"
                        placeholder="e.g. Senior, Remote"
                        class="w-full border rounded px-2 py-1 text-sm"
                      />
                    </div>
                    <div>
                      <label class="block text-xs font-medium text-gray-700 mb-1">{{ __('Min Experience (Years)') }}</label>
                      <input
                        v-model.number="advancedFilters.minExperienceYears"
                        type="number"
                        min="0"
                        placeholder="0"
                        class="w-full border rounded px-2 py-1 text-sm"
                      />
                    </div>
                    <div>
                      <label class="block text-xs font-medium text-gray-700 mb-1">{{ __('Max Experience (Years)') }}</label>
                      <input
                        v-model.number="advancedFilters.maxExperienceYears"
                        type="number"
                        min="0"
                        placeholder="20"
                        class="w-full border rounded px-2 py-1 text-sm"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </details>
          </div>

          <!-- Results List -->
          <div v-if="records.length" class="mt-2">
            <!-- Summary -->
            <div class="flex justify-between items-center mb-3 text-sm text-gray-600">
              <span>{{ __('Showing') }} {{ records.length }} {{ __('of') }} {{ totalRecords }} {{ __('records') }}</span>
              <div class="flex items-center space-x-3">
                <span v-if="selectedCandidates.length">{{ selectedCandidates.length }} {{ __('selected') }}</span>
                <div class="flex space-x-2">
                  <Button 
                    variant="outline" 
                    size="sm" 
                    @click="selectAllCurrentPage"
                    :disabled="records.length === 0"
                  >
                    {{ __('Select All') }}
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm" 
                    @click="clearSelection"
                    :disabled="selectedCandidates.length === 0"
                  >
                    {{ __('Clear All') }}
                  </Button>
                </div>
              </div>
            </div>
            
            <!-- List -->
            <div class="max-h-80 overflow-y-auto grid grid-cols-1 md:grid-cols-2 gap-3">
              <div
                v-for="r in records"
                :key="r.name"
                class="cursor-pointer border rounded-lg p-3 bg-white shadow-sm flex items-center space-x-3 transition-all"
                :class="{
                  'border-blue-500 ring-2 ring-blue-200': selectedCandidates.includes(r.name),
                  'hover:border-gray-300': !selectedCandidates.includes(r.name),
                }"
                @click="toggleCandidate(r.name)"
              >
                <div
                  class="w-5 h-5 flex items-center justify-center border rounded-full flex-shrink-0"
                  :class="selectedCandidates.includes(r.name) ? 'bg-blue-500 border-blue-500 text-white' : 'border-gray-300'"
                >
                  <svg
                    v-if="selectedCandidates.includes(r.name)"
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-3 w-3"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414L8.414 15l-4.121-4.121a1 1 0 111.414-1.414L8.414 12.172l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="text-sm font-medium text-gray-900 truncate">{{ r.full_name }}</div>
                  <div class="text-xs text-gray-500 truncate">{{ r.name }}</div>
                  <div v-if="r.email" class="text-xs text-gray-400 truncate">{{ r.email }}</div>
                </div>
              </div>
            </div>
            
            <!-- Load More Button -->
            <div v-if="canLoadMore" class="mt-4 text-center">
              <Button 
                variant="outline" 
                @click="loadMoreRecords"
                :loading="searchLoading"
                class="text-sm"
              >
                {{ __('Load More') }} ({{ totalRecords - records.length }} {{ __('remaining') }})
              </Button>
            </div>
            
            <!-- Loading Indicator -->
            <div v-if="searchLoading && currentPage === 1" class="mt-4 text-center text-gray-500 text-sm">
              <div class="animate-spin inline-block w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full mr-2"></div>
              {{ __('Loading...') }}
            </div>
          </div>
          
          <!-- Empty State -->
          <div v-else-if="searchSource && !searchLoading" class="mt-4 text-center text-gray-500 text-sm border rounded p-4 bg-gray-50">
            {{ __("No data found, please try again or select a different source.") }}
          </div>
          
          <!-- Initial Loading State -->
          <div v-else-if="searchLoading && currentPage === 1" class="mt-4 text-center text-gray-500 text-sm">
            <div class="animate-spin inline-block w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full mr-2"></div>
            {{ __('Loading...') }}
          </div>
        </div>
      </template>
      
      <template #actions>
        <Button variant="solid" @click="addToCampaign" :loading="addingTooltip" :disabled="!selectedCandidates.length">
          {{ __('Add to Campaign') }} ({{ selectedCandidates.length }})
        </Button>
        <Button variant="ghost" @click="closeCandidateModal">
          {{ __('Cancel') }}
        </Button>
      </template>
    </Dialog>
    
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMiraTalentPoolStore } from '@/stores/miraTalentPool'
import { useCandidateStore } from '@/stores/candidate'
import { useTalentSegmentStore } from '@/stores/talentSegment'
import { useCampaignStore } from '@/stores/campaign'
import { useCampaignStepStore } from '@/stores/campaignStep'
import { Dialog, Breadcrumbs, Button, FormControl, call } from 'frappe-ui'
import { debounce } from 'lodash-es'
import CampaignForm from '@/components/campaign/CampaignForm.vue'
import CampaignSocialList from '@/components/campaign/CampaignSocialList.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import moment from 'moment'
import Link from "@/components/Controls/Link.vue";

const route = useRoute()
const router = useRouter()

// Campaign store
const campaignStore = useCampaignStore()
const campaignStepStore = useCampaignStepStore()

// State
const activeTab = ref('steps')
const loading = ref(false)
const loadingSteps = ref(false)
const loadingCandidates = ref(false)
const loadingActions = ref(false)

// Campaign data
const campaign = ref({})
const targetSegment = ref(null)
const campaignSteps = ref([])
const candidateCampaigns = ref([])
const actions = ref([])
const availableCandidates = ref([])

// Modals
const showStepModal = ref(false)
const showCandidateModal = ref(false)
const showEditCampaignModal = ref(false)
const showActionModal = ref(false)
const stepFormValid = ref(false)

const savingStep = ref(false)
const savingCandidate = ref(false)
const assigningAll = ref(false)

const miraCandidates = ref([])
const loadingMiraCandidates = ref(false)

const talentCampaignRecords = ref([])  // dữ liệu resolved từ mira_talent_campaign

// Social media states
const socialPages = ref([])
const externalConnections = ref([])
const jobOpeningsList = ref([])
const loadingSocialPages = ref(false)
const loadingConnections = ref(false)
const loadingJobOpenings = ref(false)

// Interactions states
const interactions = ref([])
const loadingInteractions = ref(false)

const breadcrumbs = computed(() => [
    { label: __('Campaigns'), route: { name: 'CampaignManagement' } },
    { label: campaign.value.campaign_name || __('Loading...'), route: { name: 'CampaignDetailView' } },
])

console.log(campaign)

function normalizeTalentCampaign(raw) {
  if (!raw) return []
  let parsed
  try { parsed = JSON.parse(raw) } catch { return [] }
  if (Array.isArray(parsed)) return parsed
  if (parsed.type && parsed.records) return [parsed]
  return []
}

const campaignSelection = computed(() => normalizeTalentCampaign(campaign.value?.mira_talent_campaign))
const isManualCampaign = computed(() => {
  // true nếu record đang render có source manual (xử lý trong template row)
  return (record) => record.__source === 'manual'
})


// Form data
const stepFormData = reactive({
  name: '',
  campaign_step_name: '',
  step_order: '',
  action_type: '',
  delay_in_days: 0,
  template: '',
  campaign: route.params.id
})

const candidateFormData = reactive({
  name: '',            // optional: để detect edit
  full_name: '',
  email: '',
  phone_number: ''
})

const actionFormData = reactive({
  name: '',
  campaign_step: '',
  candidate_campaign_id: '',
  status: '',
  scheduled_at: '',
  executed_at: '',
  notes: ''
})

const loadTalentCampaign = async () => {
  try {
    let all = []

    // 1. Load from Mira Talent Campaign table
    try {
      const talentCampaignRes = await call("frappe.client.get_list", {
        doctype: "Mira Talent Campaign",
        fields: ["name", "talent_id", "status"],
        filters: [["campaign_id", "=", route.params.id]],
        limit_page_length: 1000,
      })
      
      if (talentCampaignRes.length > 0) {
        const talentIds = talentCampaignRes.map(tc => tc.talent_id)
        const talentRes = await call("frappe.client.get_list", {
          doctype: "Mira Talent",
          fields: ["name", "full_name", "email", "phone"],
          filters: [["name", "in", talentIds]],
          limit_page_length: 1000,
        })
        
        // Merge talent data with campaign data
        const talentData = talentRes.map(talent => {
          const campaignRecord = talentCampaignRes.find(tc => tc.talent_id === talent.name)
          return {
            ...talent,
            campaign_record_id: campaignRecord.name,
            status: campaignRecord.status,
            segment: campaignRecord.segment,
            __source: "mira_talent"
          }
        })
        
        all.push(...talentData)
      }
    } catch (err) {
      console.error("Error loading Mira Talent Campaign:", err)
    }

    // 2. Load from Mira Contact Campaign table
    try {
      const contactCampaignRes = await call("frappe.client.get_list", {
        doctype: "Mira Contact Campaign",
        fields: ["name", "contact_id", "status"],
        filters: [["campaign_id", "=", route.params.id]],
        limit_page_length: 1000,
      })
      
      if (contactCampaignRes.length > 0) {
        const contactIds = contactCampaignRes.map(cc => cc.contact_id)
        const contactRes = await call("frappe.client.get_list", {
          doctype: "Mira Contact",
          fields: ["name", "full_name", "email", "phone"],
          filters: [["name", "in", contactIds]],
          limit_page_length: 1000,
        })
        
        // Merge contact data with campaign data
        const contactData = contactRes.map(contact => {
          const campaignRecord = contactCampaignRes.find(cc => cc.contact_id === contact.name)
          return {
            ...contact,
            campaign_record_id: campaignRecord.name,
            status: campaignRecord.status,
            __source: "mira_contact"
          }
        })
        
        all.push(...contactData)
      }
    } catch (err) {
      console.error("Error loading Mira Contact Campaign:", err)
    }

    talentCampaignRecords.value = all
    console.log('Loaded talent campaign records:', all)
  } catch (err) {
    console.error("Error loading Talent Campaign:", err)
    talentCampaignRecords.value = []
  }
}

// Load external connections for social media configuration
const loadExternalConnections = async () => {
  loadingConnections.value = true
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Mira External Connection',
      fields: ['name', 'tenant_name', 'platform_type', 'connection_status'],
      filters: [['connection_status', '=', 'Connected']],
      limit_page_length: 100
    })
    externalConnections.value = response || []
    console.log('✅ Loaded external connections:', externalConnections.value.length)
  } catch (error) {
    console.error('❌ Error loading external connections:', error)
    externalConnections.value = []
  } finally {
    loadingConnections.value = false
  }
}

// Load social pages for social media configuration
const loadSocialPages = async () => {
  loadingSocialPages.value = true
  try {
    // Since Mira External Connection Account is a child table, 
    // we need to get it through the parent Mira External Connection
    const response = await call('mbw_mira.api.external_connections.get_all_accounts')
    socialPages.value = response || []
    console.log('✅ Loaded social pages:', socialPages.value.length)
  } catch (error) {
    console.error('❌ Error loading social pages:', error)
    socialPages.value = []
  } finally {
    loadingSocialPages.value = false
  }
}

// Load job openings for social media posts
const loadJobOpenings = async () => {
  loadingJobOpenings.value = true
  try {
    const response = await call('frappe.client.get_list', {
      doctype: "Mira Job Opening",
      fields: ['name', 'job_title', 'job_code'],
      order_by: 'creation desc',
      limit_page_length: 100
    })
    jobOpeningsList.value = response || []
    console.log('✅ Loaded job openings:', jobOpeningsList.value.length)
  } catch (error) {
    console.error('❌ Error loading job openings:', error)
    jobOpeningsList.value = []
  } finally {
    loadingJobOpenings.value = false
  }
}

// Loading states for actions
const savingAction = ref(false)

// Options
const stepTypeOptions = [
  { label: __('Send Email'), value: 'SEND_EMAIL' },
  { label: __('Send SMS'), value: 'SEND_SMS' },
  { label: __('Manual Call'), value: 'MANUAL_CALL' },
  { label: __('Manual Task'), value: 'MANUAL_TASK' }
]

const statusOptions = [
  { label: __('Active'), value: 'ACTIVE' },
  { label: __('Paused'), value: 'PAUSED' },
  { label: __('Completed'), value: 'COMPLETED' },
  { label: __('Cancelled'), value: 'CANCELLED' }
]

const actionStatusOptions = [
  { label: __('Scheduled'), value: 'SCHEDULED' },
  { label: __('Executed'), value: 'EXECUTED' },
  { label: __('Skipped'), value: 'SKIPPED' },
  { label: __('Failed'), value: 'FAILED' },
  { label: __('Pending Manual'), value: 'PENDING_MANUAL' }
]

// Computed properties
const tabs = computed(() => {
  const baseTabs = [
    {
      key: 'steps',
      label: __('Campaign Steps'),
      count: campaignSteps.value.length
    },
    {
      key: 'candidates',
      label: __('Assigned Talent'),
      count: candidateCampaigns.value.length
    },
    {
      key: 'mira_candidates',
      label: __('Candidates'),
      count: miraCandidates.value.length
    },
    {
      key: 'actions',
      label: __('Actions'),
      count: actions.value.length
    },
    {
      key: 'social',
      label: __('Media Posts'),
      count: 0
    },
    {
      key: 'interactions',
      label: __('Interactions'),
      count: interactions.value.length
    },
    {
      key: 'analytics',
      label: __('Analytics'),
      count: 0
    }
  ]

  // Chỉ hiển thị tab Social Media khi source_type là DataSource
  // if (campaign.value.source_type === 'DataSource') {
  //   baseTabs.splice(4, 0, {
  //     key: 'social',
  //     label: __('Media Posts'),
  //     count: 0 // Will be updated when we have social posts count
  //   })
  // }

  return baseTabs
})

// Always sort campaignSteps by step_order ascending
const sortedCampaignSteps = computed(() => {
  return [...campaignSteps.value].sort((a, b) => a.step_order - b.step_order)
})

// CSS classes for status and types
const getStatusClasses = (status) => {
  const classes = {
    'ACTIVE': 'bg-green-100 text-green-800',
    'PAUSED': 'bg-yellow-100 text-yellow-800',
    'COMPLETED': 'bg-blue-100 text-blue-800',
    'CANCELLED': 'bg-red-100 text-red-800',
    'DRAFT': 'bg-gray-100 text-gray-800',
    'ARCHIVED': 'bg-gray-100 text-gray-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getTypeClasses = (type) => {
  const classes = {
    'NURTURING': 'bg-purple-100 text-purple-800',
    'ATTRACTION': 'bg-blue-100 text-blue-800',
    'RECRUITMENT': 'bg-green-100 text-green-800',
    'REFERRAL': 'bg-orange-100 text-orange-800',
    'GATHERING': 'bg-gray-100 text-gray-800'
  }
  return classes[type] || 'bg-gray-100 text-gray-800'
}

const getActionTypeClasses = (type) => {
  const classes = {
    'SEND_EMAIL': 'bg-blue-100 text-blue-800',
    'SEND_SMS': 'bg-green-100 text-green-800',
    'MANUAL_CALL': 'bg-orange-100 text-orange-800',
    'MANUAL_TASK': 'bg-purple-100 text-purple-800'
  }
  return classes[type] || 'bg-gray-100 text-gray-800'
}

const getActionStatusClasses = (status) => {
  const classes = {
    'SCHEDULED': 'bg-blue-100 text-blue-800',
    'EXECUTED': 'bg-green-100 text-green-800',
    'SKIPPED': 'bg-yellow-100 text-yellow-800',
    'FAILED': 'bg-red-100 text-red-800',
    'PENDING_MANUAL': 'bg-orange-100 text-orange-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

// Interaction helper functions
const getInteractionTypeClass = (type) => {
  const classes = {
    'EMAIL_SENT': 'bg-blue-100 text-blue-800',
    'EMAIL_DELIVERED': 'bg-green-100 text-green-800',
    'EMAIL_BOUNCED': 'bg-red-100 text-red-800',
    'EMAIL_OPENED': 'bg-purple-100 text-purple-800',
    'EMAIL_CLICKED': 'bg-indigo-100 text-indigo-800',
    'EMAIL_UNSUBSCRIBED': 'bg-gray-100 text-gray-800',
    'EMAIL_REPLIED': 'bg-emerald-100 text-emerald-800',
    'PAGE_VISITED': 'bg-cyan-100 text-cyan-800',
    'FORM_SUBMITTED': 'bg-teal-100 text-teal-800',
    'DOWNLOAD_TRIGGERED': 'bg-orange-100 text-orange-800',
    'CHAT_STARTED': 'bg-pink-100 text-pink-800',
    'CHAT_MESSAGE_SENT': 'bg-rose-100 text-rose-800',
    'CHAT_COMPLETED': 'bg-green-100 text-green-800',
    'CALL_MISSED': 'bg-red-100 text-red-800',
    'CALL_COMPLETED': 'bg-green-100 text-green-800',
    'SMS_SENT': 'bg-blue-100 text-blue-800',
    'SMS_DELIVERED': 'bg-green-100 text-green-800',
    'SMS_REPLIED': 'bg-emerald-100 text-emerald-800',
    'APPLICATION_SUBMITTED': 'bg-purple-100 text-purple-800',
    'DOCUMENT_UPLOADED': 'bg-yellow-100 text-yellow-800',
    'TEST_STARTED': 'bg-orange-100 text-orange-800',
    'TEST_COMPLETED': 'bg-green-100 text-green-800',
    'INTERVIEW_CONFIRMED': 'bg-blue-100 text-blue-800',
    'INTERVIEW_RESCHEDULED': 'bg-yellow-100 text-yellow-800'
  }
  return classes[type] || 'bg-gray-100 text-gray-800'
}

const formatInteractionType = (type) => {
  const labels = {
    'EMAIL_SENT': 'Email Sent',
    'EMAIL_DELIVERED': 'Email Delivered',
    'EMAIL_BOUNCED': 'Email Bounced',
    'EMAIL_OPENED': 'Email Opened',
    'EMAIL_CLICKED': 'Email Clicked',
    'EMAIL_UNSUBSCRIBED': 'Email Unsubscribed',
    'EMAIL_REPLIED': 'Email Replied',
    'PAGE_VISITED': 'Page Visited',
    'FORM_SUBMITTED': 'Form Submitted',
    'DOWNLOAD_TRIGGERED': 'Download Triggered',
    'CHAT_STARTED': 'Chat Started',
    'CHAT_MESSAGE_SENT': 'Chat Message Sent',
    'CHAT_COMPLETED': 'Chat Completed',
    'CALL_MISSED': 'Call Missed',
    'CALL_COMPLETED': 'Call Completed',
    'SMS_SENT': 'SMS Sent',
    'SMS_DELIVERED': 'SMS Delivered',
    'SMS_REPLIED': 'SMS Replied',
    'APPLICATION_SUBMITTED': 'Application Submitted',
    'DOCUMENT_UPLOADED': 'Document Uploaded',
    'TEST_STARTED': 'Test Started',
    'TEST_COMPLETED': 'Test Completed',
    'INTERVIEW_CONFIRMED': 'Interview Confirmed',
    'INTERVIEW_RESCHEDULED': 'Interview Rescheduled'
  }
  return labels[type] || type
}

// Methods
const loadCampaign = async () => {
  loading.value = true
  try {
    const result = await campaignStore.getCampaignDetails(route.params.id)
    if (result) {
      Object.assign(campaign.value, result)
      // Load target segment if exists
      if (campaign.value.target_segment) {
        await loadTargetSegment()
      }
    }
    await loadTalentCampaign()
  } catch (error) {
    console.error('Error loading campaign:', error)
  } finally {
    loading.value = false
  }
}

const loadTargetSegment = async () => {
  if (!campaign.value.target_segment) return
  
  try {
    const result = await talentSegmentStore.getFormData(campaign.value.target_segment)
    if (result.success) {
      targetSegment.value = result.data
    }
  } catch (error) {
    console.error('Error loading target segment:', error)
  }
}

const loadCampaignSteps = async () => {
  loadingSteps.value = true
  try {
    const result = await campaignStepStore.getFilteredCampaignSteps({
      campaign: route.params.id,
      limit: 1000
    })
    if (result && result.data) {
      campaignSteps.value = result.data
    }
  } catch (error) {
    console.error('Error loading campaign steps:', error)
  } finally {
    loadingSteps.value = false
  }
}

const loadCandidateCampaigns = async () => {
  loadingCandidates.value = true
  try {
    const result = await miraTalentPoolStore.getList({
      filters: { campaign_id: route.params.id },
      fields: ['name', 'talent_id', 'status', 'current_step_order', 'enrolled_at']
    })
    if (result.success) {
      candidateCampaigns.value = result.data
    }
  } catch (error) {
    console.error('Error loading candidate campaigns:', error)
  } finally {
    loadingCandidates.value = false
  }
}

const loadActions = async () => {
  loadingActions.value = true
  try {
    const candidateCampaignsResult = await miraTalentPoolStore.getList({
      filters: { campaign_id: route.params.id },
      fields: ['name']
    })
    if (candidateCampaignsResult.success && candidateCampaignsResult.data.length > 0) {
      const candidateCampaignIds = candidateCampaignsResult.data.map(cc => cc.name)
      const result = await call(getList({
        filters: { candidate_campaign_id: ['in', candidateCampaignIds] },
        fields: ['name', 'campaign_step', 'status', 'scheduled_at', 'executed_at']
      }))
      if (result.success) {
        actions.value = result.data
      }
    } else {
      actions.value = []
    }
  } catch (error) {
    console.error('Error loading actions:', error)
    actions.value = []
  } finally {
    loadingActions.value = false
  }
}

const loadAvailableCandidates = async () => {
  try {
    if (!campaign.value.target_segment) {
      // If no target segment, show all candidates
      const result = await candidateStore.getList({
        fields: ['name', 'full_name'],
        page_length: 1000
      })
      if (result.success) {
        availableCandidates.value = result.data.map(item => ({
          label: item.full_name || item.name,
          value: item.name
        }))
      }
    } else {
      // Get candidates from target segment through Mira Talent Pool
      const candidateSegmentResult = await miraTalentPoolStore.getList({
        filters: { segment_id: campaign.value.target_segment },
        fields: ['talent_id']
      })
      if (candidateSegmentResult.success && candidateSegmentResult.data.length > 0) {
        const candidateIds = candidateSegmentResult.data.map(cs => cs.talent_id)
        // Get candidates already in this campaign
        const existingCandidateCampaigns = await miraTalentPoolStore.getList({
          filters: { campaign_id: route.params.id },
          fields: ['talent_id']
        })
        const existingCandidateIds = existingCandidateCampaigns.success
          ? existingCandidateCampaigns.data.map(cc => cc.talent_id)
          : []
        // Filter out candidates already in campaign
        const availableCandidateIds = candidateIds.filter(
          id => !existingCandidateIds.includes(id)
        )
        if (availableCandidateIds.length > 0) {
          const candidateResult = await candidateStore.getList({
            filters: { name: ['in', availableCandidateIds] },
            fields: ['name', 'full_name']
          })
          if (candidateResult.success) {
            availableCandidates.value = candidateResult.data.map(item => ({
              label: item.full_name + ' (' + item.name + ')',
              value: item.name
            }))
          }
        } else {
          availableCandidates.value = []
        }
      } else {
        availableCandidates.value = []
      }
    }
  } catch (error) {
    console.error('Error loading candidates:', error)
  }
}

// Step methods
const openStepModal = (step = null) => {
  if (step) {
    Object.assign(stepFormData, step)
  } else {
    Object.keys(stepFormData).forEach(key => {
      stepFormData[key] = ''
    })
    stepFormData.campaign = route.params.id
    // Gán step_order = max + 1
    const maxOrder = Math.max(...campaignSteps.value.map(s => s.step_order), 0)
    stepFormData.step_order = maxOrder + 1
  }
  showStepModal.value = true
}

const closeStepModal = () => {
  showStepModal.value = false
  Object.keys(stepFormData).forEach(key => {
    stepFormData[key] = ''
  })
}

// Add Talent/Contact Modal States
const showAddTalentModal = ref(false)
const searchSource = ref(null)
const searchKeyword = ref('')
const selectedSegment = ref('')
const records = ref([])
const selectedCandidates = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const totalRecords = ref(0)
const searchLoading = ref(false)
const addingTooltip = ref(false)

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
})

// Existing records in campaign (to exclude)
const existingRecords = ref({
  talents: [],
  contacts: []
})

// Load existing records to exclude from search
const loadExistingRecords = async () => {
  try {
    // Load existing talents
    const talentCampaignRes = await call('frappe.client.get_list', {
      doctype: 'Mira Talent Campaign',
      fields: ['talent_id'],
      filters: [['campaign_id', '=', route.params.id]],
      limit_page_length: 1000,
    })
    existingRecords.value.talents = talentCampaignRes.map(tc => tc.talent_id)
    
    // Load existing contacts
    const contactCampaignRes = await call('frappe.client.get_list', {
      doctype: 'Mira Contact Campaign',
      fields: ['contact_id'],
      filters: [['campaign_id', '=', route.params.id]],
      limit_page_length: 1000,
    })
    existingRecords.value.contacts = contactCampaignRes.map(cc => cc.contact_id)
    
    console.log('Existing records loaded:', existingRecords.value)
  } catch (error) {
    console.error('Error loading existing records:', error)
  }
}

// Candidate methods
const openCandidateModal = async (record = null) => {
  showAddTalentModal.value = true
  // Load existing records first
  await loadExistingRecords()
  // Reset search state
  searchSource.value = null
  searchKeyword.value = ''
  selectedSegment.value = ''
  records.value = []
  selectedCandidates.value = []
  currentPage.value = 1
  totalRecords.value = 0
  // Reset advanced filters
  Object.keys(advancedFilters).forEach(key => {
    if (typeof advancedFilters[key] === 'boolean') {
      advancedFilters[key] = false
    } else {
      advancedFilters[key] = key.includes('Years') ? null : ''
    }
  })
}


const closeCandidateModal = () => {
  showAddTalentModal.value = false
  // Reset search state
  searchSource.value = null
  searchKeyword.value = ''
  selectedSegment.value = ''
  records.value = []
  selectedCandidates.value = []
  currentPage.value = 1
  totalRecords.value = 0
}

// Search functions (copied from CampaignWizard)
const fetchRecords = async (page = 1) => {
  if (!searchSource.value) return

  searchLoading.value = true
  try {
    const startIndex = (page - 1) * pageSize.value
    
    if (searchSource.value === 'mira_talent') {
      let filters = []
      
      // Exclude existing talents in campaign
      if (existingRecords.value.talents.length > 0) {
        filters.push(['name', 'not in', existingRecords.value.talents])
      }
      
      // Filter by segment if selected
      if (selectedSegment.value) {
        const poolRes = await call('frappe.client.get_list', {
          doctype: 'Mira Talent Pool',
          fields: ['talent_id'],
          filters: { segment_id: selectedSegment.value },
          limit_page_length: 1000,
        })
        
        const talentIds = poolRes.map(r => r.talent_id)
        if (!talentIds.length) {
          records.value = []
          totalRecords.value = 0
          return
        }
        
        filters.push(['name', 'in', talentIds])
      }
      
      // Add search filter if exists
      if (searchKeyword.value) {
        filters.push(['full_name', 'like', `%${searchKeyword.value}%`])
      }
      
      // Advanced filters for talents
      if (advancedFilters.skills) {
        filters.push(['skills', 'like', `%${advancedFilters.skills}%`])
      }
      
      if (advancedFilters.tags) {
        filters.push(['tags', 'like', `%${advancedFilters.tags}%`])
      }
      
      if (advancedFilters.minExperienceYears !== null) {
        filters.push(['experience_years', '>=', advancedFilters.minExperienceYears])
      }
      
      if (advancedFilters.maxExperienceYears !== null) {
        filters.push(['experience_years', '<=', advancedFilters.maxExperienceYears])
      }
      
      const res = await call('frappe.client.get_list', {
        doctype: 'Mira Talent',
        fields: ['name', 'full_name', 'email', 'phone', 'skills', 'tags', 'experience_years'],
        filters: filters,
        limit_start: startIndex,
        limit_page_length: pageSize.value,
      })
      
      const countRes = await call('frappe.client.get_count', {
        doctype: 'Mira Talent',
        filters: filters,
      })
      
      records.value = page === 1 ? res : [...records.value, ...res]
      totalRecords.value = countRes

    } else if (searchSource.value === 'mira_contact') {
      let filters = []
      
      // Exclude existing contacts in campaign
      if (existingRecords.value.contacts.length > 0) {
        filters.push(['name', 'not in', existingRecords.value.contacts])
      }
      
      // Add search filter if exists
      if (searchKeyword.value) {
        filters.push(['full_name', 'like', `%${searchKeyword.value}%`])
      }
      
      // Advanced filters for contacts
      if (advancedFilters.missingEmail) {
        filters.push(['email', 'in', ['', null]])
      }
      
      if (advancedFilters.missingPhone) {
        filters.push(['phone', 'in', ['', null]])
      }
      
      const res = await call('frappe.client.get_list', {
        doctype: 'Mira Contact',
        fields: ['name', 'full_name', 'email', 'phone'],
        filters: filters,
        limit_start: startIndex,
        limit_page_length: pageSize.value,
      })
      
      const countRes = await call('frappe.client.get_count', {
        doctype: 'Mira Contact',
        filters: filters,
      })
      
      records.value = page === 1 ? res : [...records.value, ...res]
      totalRecords.value = countRes
    }
    
    currentPage.value = page
  } catch (e) {
    console.error('Error fetching records', e)
    records.value = []
    totalRecords.value = 0
  } finally {
    searchLoading.value = false
  }
}

const loadMoreRecords = () => {
  if (searchLoading.value) return
  const nextPage = currentPage.value + 1
  const maxPages = Math.ceil(totalRecords.value / pageSize.value)
  
  if (nextPage <= maxPages) {
    fetchRecords(nextPage)
  }
}

const canLoadMore = computed(() => {
  const maxPages = Math.ceil(totalRecords.value / pageSize.value)
  return currentPage.value < maxPages && !searchLoading.value
})

const toggleCandidate = (name) => {
  if (selectedCandidates.value.includes(name)) {
    selectedCandidates.value = selectedCandidates.value.filter((c) => c !== name)
  } else {
    selectedCandidates.value = [...selectedCandidates.value, name]
  }
}

// Select all candidates on current page
const selectAllCurrentPage = () => {
  const currentPageIds = records.value.map(r => r.name)
  const newSelected = [...new Set([...selectedCandidates.value, ...currentPageIds])]
  selectedCandidates.value = newSelected
}

// Clear all selected candidates
const clearSelection = () => {
  selectedCandidates.value = []
}

// Add selected candidates to campaign
const addToCampaign = async () => {
  if (!selectedCandidates.value.length) {
    alert(__('Please select at least one candidate'))
    return
  }
  
  addingTooltip.value = true
  try {
    const recordType = searchSource.value
    let doctype = ''
    let recordField = ''
    
    if (recordType === 'mira_talent') {
      doctype = 'Mira Talent Campaign'
      recordField = 'talent_id'
    } else if (recordType === 'mira_contact') {
      doctype = 'Mira Contact Campaign'
      recordField = 'contact_id'
    }
    
    try {
      // Use bulk insert API for better performance
      const bulkData = selectedCandidates.value.map(recordId => ({
        doctype: doctype,
        campaign_id: route.params.id,
        [recordField]: recordId,
        status: 'ACTIVE',
        ...(recordType === 'mira_talent' && selectedSegment.value 
          ? { segment: selectedSegment.value } 
          : {})
      }))
      
      // Call custom bulk insert API
      await call('mbw_mira.api.campaign.bulk_create_campaign_records', {
        records: bulkData,
        doctype: doctype
      })
    } catch (bulkError) {
      console.log('Bulk insert failed, falling back to individual inserts...')
      
      // Fallback to individual inserts
      const promises = selectedCandidates.value.map(async (recordId) => {
        const payload = {
          campaign_id: route.params.id,
          [recordField]: recordId,
          status: 'ACTIVE',
          ...(recordType === 'mira_talent' && selectedSegment.value 
            ? { segment: selectedSegment.value } 
            : {})
        }
        
        return await call('frappe.client.insert', {
          doc: {
            doctype: doctype,
            ...payload
          }
        })
      })
      
      await Promise.all(promises)
    }
    
    // Reload data and close modal
    await loadTalentCampaign()
    closeCandidateModal()
    
    console.log(`Successfully added ${selectedCandidates.value.length} records to campaign`)
  } catch (error) {
    console.error('Error adding to campaign:', error)
    alert(__('Error adding records to campaign. Please try again.'))
  } finally {
    addingTooltip.value = false
  }
}

// Watch functions for search
watch(searchSource, () => {
  selectedCandidates.value = []
  selectedSegment.value = ''
  records.value = []
  currentPage.value = 1
  totalRecords.value = 0
  
  if (searchSource.value) {
    fetchRecords(1)
  }
})

watch(selectedSegment, (val) => {
  if (searchSource.value === 'mira_talent') {
    selectedCandidates.value = []
    records.value = []
    currentPage.value = 1
    totalRecords.value = 0
    fetchRecords(1)
  }
})

// Debounced search
const fetchRecordsDebounced = debounce(fetchRecords, 400)

watch(searchKeyword, () => {
  if (!searchSource.value) return
  currentPage.value = 1
  records.value = []
  totalRecords.value = 0
  fetchRecordsDebounced(1)
})

// Watch advanced filters
watch(advancedFilters, () => {
  if (!searchSource.value) return
  currentPage.value = 1
  records.value = []
  totalRecords.value = 0
  fetchRecordsDebounced(1)
}, { deep: true })

// Action methods
const openActionModal = () => {
  Object.keys(actionFormData).forEach(key => {
    actionFormData[key] = ''
  })
  showActionModal.value = true
}

const closeActionModal = () => {
  showActionModal.value = false
  Object.keys(actionFormData).forEach(key => {
    actionFormData[key] = ''
  })
}

const loadMiraCandidates = async () => {
  loadingMiraCandidates.value = true
  try {
    const res = await call("frappe.client.get_list", {
      doctype: "Mira Candidate",
      fields: [
        "name",
        "full_name",
        "email",
        "phone",
        "avatar",
        "headline",
        "source",
        "skills",
        "status",
        "last_interaction"
      ],
      filters: { campaign_id: route.params.id },
      limit_page_length: 100
    })
    miraCandidates.value = res
  } catch (err) {
    console.error("Error loading Mira Candidates:", err)
    miraCandidates.value = []
  } finally {
    loadingMiraCandidates.value = false
  }
}

// Load interactions for the campaign
const loadInteractions = async () => {
  loadingInteractions.value = true
  try {
    const res = await call("frappe.client.get_list", {
      doctype: "Mira Interaction",
      fields: [
        "name",
        "talent_id",
        "contact_id",
        "campaign_id",
        "interaction_type",
        "action",
        "url",
        "description",
        "creation",
        "modified"
      ],
      filters: { campaign_id: route.params.id },
      order_by: "creation desc",
      limit_page_length: 100
    })
    interactions.value = res || []
  } catch (err) {
    console.error("Error loading interactions:", err)
    interactions.value = []
  } finally {
    loadingInteractions.value = false
  }
}

// Watch tabs to ensure activeTab is always valid
watch(tabs, (newTabs) => {
  const tabKeys = newTabs.map(tab => tab.key)
  if (!tabKeys.includes(activeTab.value)) {
    // Nếu activeTab hiện tại không còn tồn tại, chuyển về tab đầu tiên
    activeTab.value = tabKeys[0] || 'steps'
  }
}, { immediate: true })

// Load initial data
// Watch activeTab to load data when needed
watch(activeTab, (newTab) => {
  if (newTab === 'social') {
    console.log(' Switching to social tab, ensuring data is loaded...');
    if (externalConnections.value.length === 0) {
      loadExternalConnections();
    }
    if (socialPages.value.length === 0) {
      loadSocialPages();
    }
    if (jobOpeningsList.value.length === 0) {
      loadJobOpenings();
    }
  } else if (newTab === 'interactions') {
    console.log(' Switching to interactions tab, loading data...');
    if (interactions.value.length === 0) {
      loadInteractions();
    }
  }
});
onMounted(() => {
  loadCampaign()
  loadCampaignSteps()
  loadMiraCandidates()
  loadTalentCampaign()
  loadCandidateCampaigns()
  loadActions()
  loadAvailableCandidates()
  loadExternalConnections()
  loadSocialPages()
  loadJobOpenings()
  loadInteractions()
})

// Watchers
watch(() => route.params.id, (newId, oldId) => {
  if (newId !== oldId) {
    loadCampaign()
    loadCampaignSteps()
    loadCandidateCampaigns()
    loadActions()
    loadAvailableCandidates()
  }
})

// Handlers
const handleCampaignUpdated = (updatedCampaign) => {
  Object.assign(campaign.value, updatedCampaign)
  showEditCampaignModal.value = false
}

// Utility functions
const formatDate = (date) => {
  if (!date) return ''
  return moment(date).format('DD/MM/YYYY HH:mm')
}

const formatDateTime = (date) => {
  if (!date) return ''
  return moment(date).format('DD/MM/YYYY HH:mm:ss')
}

const editCampaign = () => {
  showEditCampaignModal.value = true
}

const getActiveCandidates = () => {
  return candidateCampaigns.value.filter(c => c.status === 'ACTIVE').length
}

const getCompletedCandidates = () => {
  return candidateCampaigns.value.filter(c => c.status === 'COMPLETED').length
}

const saveStep = async () => {
  savingStep.value = true
  try {
    // Nếu có name thì update, còn không thì insert
    let result
    console.log(stepFormData.name)
    if (stepFormData.name) {
      console.log("Update")
      result = await campaignStepStore.updateCampaignStep(stepFormData.name, stepFormData)
    } else {
      console.log("Insert")
      result = await campaignStepStore.createCampaignStep(stepFormData)
    }

    if (result) {
      await loadCampaignSteps()
      closeStepModal()
    } else {
      console.error('Error saving step:', result)
    }
  } catch (err) {
    console.error('Error saving step:', err)
  } finally {
    savingStep.value = false
  }
}

// Thêm mới hoặc update
const assignCandidate = async () => {
  savingCandidate.value = true
  try {
    let current = normalizeTalentCampaign(campaign.value.mira_talent_campaign)

    let manualBlock = current.find(b => b.type === "manual")
    if (!manualBlock) {
      manualBlock = { type: "manual", records: [] }
      current.push(manualBlock)
    }

    if (candidateFormData.name) {
      // edit
      const idx = manualBlock.records.findIndex(r => r.name === candidateFormData.name)
      if (idx !== -1) {
        manualBlock.records[idx] = { ...candidateFormData }
      }
    } else {
      // add mới
      manualBlock.records.push({
        name: "MTL-" + Date.now(),
        full_name: candidateFormData.full_name,
        email: candidateFormData.email,
        phone_number: candidateFormData.phone_number
      })
    }

    await call("frappe.client.set_value", {
      doctype: "Mira Campaign",
      name: route.params.id,
      fieldname: "mira_talent_campaign",
      value: JSON.stringify(current)
    })

    campaign.value.mira_talent_campaign = JSON.stringify(current)
    await loadTalentCampaign()
    closeCandidateModal()
  } catch (err) {
    console.error("Error saving manual talent:", err)
  } finally {
    savingCandidate.value = false
  }
}




const saveAction = () => {
  // TODO: Implement save action
}

const deleteStep = async (step) => {
  try {
    if (confirm(`Bạn có chắc chắn muốn xóa bước "${step.campaign_step_name}"?`)) {
      await campaignStepStore.deleteCampaignStep(step.name)
      await loadCampaignSteps() // Reload danh sách sau khi xóa
    }
  } catch (error) {
    console.error('Error deleting step:', error)
  }
}

const moveStepUp = async (index) => {
  if (index <= 0) return // Không thể move up step đầu tiên
  
  try {
    const currentStep = campaignSteps.value[index]
    const previousStep = campaignSteps.value[index - 1]
    
    // Swap step_order
    const tempOrder = currentStep.step_order
    currentStep.step_order = previousStep.step_order
    previousStep.step_order = tempOrder
    
    // Update cả 2 steps (chỉ step_order)
    await Promise.all([
      campaignStepStore.updateStepOrder(currentStep.name, currentStep.step_order),
      campaignStepStore.updateStepOrder(previousStep.name, previousStep.step_order)
    ])
    
    await loadCampaignSteps() // Reload để cập nhật thứ tự
  } catch (error) {
    console.error('Error moving step up:', error)
  }
}

const moveStepDown = async (index) => {
  if (index >= campaignSteps.value.length - 1) return // Không thể move down step cuối cùng
  
  try {
    const currentStep = campaignSteps.value[index]
    const nextStep = campaignSteps.value[index + 1]
    
    // Swap step_order
    const tempOrder = currentStep.step_order
    currentStep.step_order = nextStep.step_order
    nextStep.step_order = tempOrder
    
    // Update cả 2 steps (chỉ step_order)
    await Promise.all([
      campaignStepStore.updateStepOrder(currentStep.name, currentStep.step_order),
      campaignStepStore.updateStepOrder(nextStep.name, nextStep.step_order)
    ])
    
    await loadCampaignSteps() // Reload để cập nhật thứ tự
  } catch (error) {
    console.error('Error moving step down:', error)
  }
}

const assignAllFromSegment = () => {
  // TODO: Implement assign all from segment
}

const startCandidateCampaign = (candidate) => {
  // TODO: Implement start candidate campaign
}

const pauseCandidateCampaign = (candidate) => {
  // TODO: Implement pause candidate campaign
}

const viewCandidateDetails = (candidate) => {
  // TODO: Implement view candidate details
}

const unassignCandidate = async (record) => {
  if (!confirm(__('Are you sure you want to remove this record from the campaign?'))) {
    return
  }
  
  try {
    // Delete from the appropriate campaign table based on source
    if (record.__source === 'mira_talent') {
      await call('frappe.client.delete', {
        doctype: 'Mira Talent Campaign',
        name: record.campaign_record_id
      })
    } else if (record.__source === 'mira_contact') {
      await call('frappe.client.delete', {
        doctype: 'Mira Contact Campaign',
        name: record.campaign_record_id
      })
    }
    
    // Reload the data
    await loadTalentCampaign()
    
    console.log('Successfully removed record from campaign')
  } catch (err) {
    console.error('Error unassigning candidate:', err)
    alert(__('Error removing record from campaign. Please try again.'))
  }
}



const viewActionDetails = (action) => {
  // TODO: Implement view action details
}

const deleteAction = (action) => {
  // TODO: Implement delete action
}

const viewTargetSegment = () => {
  // TODO: Implement view target segment
}
</script>

<style scoped>
.campaign-detail-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  border-radius: 8px;
}

.v-card {
  border-radius: 8px;
}

.v-chip {
  font-weight: 500;
}

.v-data-table {
  border-radius: 8px;
}
</style>
