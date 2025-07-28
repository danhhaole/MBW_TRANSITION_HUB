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
            <!-- Users Icon for Candidates -->
            <svg v-else-if="tab.key === 'candidates'" class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"/>
            </svg>
            <!-- Lightning Icon for Actions -->
            <svg v-else-if="tab.key === 'actions'" class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
            <!-- Chart Icon for Analytics -->
            <svg v-else class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
            {{ tab.label }} ({{ tab.count }})
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
            <h3 class="text-lg font-medium text-gray-900">{{ __('Assigned Profiles') }}</h3>
            <div class="flex items-center space-x-2">
              <button
                v-if="campaign.target_segment && availableCandidates.length > 0"
                @click="assignAllFromSegment"
                :disabled="assigningAll"
                class="inline-flex items-center px-4 py-2 border border-green-300 text-sm font-medium rounded-lg text-green-700 bg-white hover:bg-green-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
              >
                <svg v-if="assigningAll" class="animate-spin -ml-1 mr-2 h-4 w-4 text-green-700" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                </svg>
                {{ __('Assign All from Segment') }}  ({{ availableCandidates.length }})
              </button>
              <button
                @click="openCandidateModal()"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-black hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
                </svg>
                {{ __('Assign Profile') }}
              </button>
            </div>
          </div>
          
          <!-- Candidate Campaigns Table -->
          <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
            <table class="min-w-full divide-y divide-gray-300">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Profile') }}</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Status') }}</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Current Step') }}</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Enrolled At') }}</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Actions') }}</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-if="loadingCandidates" class="text-center">
                  <td colspan="5" class="px-6 py-4 text-sm text-gray-500">
                    <div class="flex justify-center">
                      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-black"></div>
                    </div>
                  </td>
                </tr>
                <tr v-else-if="candidateCampaigns.length === 0" class="text-center">
                  <td colspan="5" class="px-6 py-4 text-sm text-gray-500">{{ __('No profiles assigned') }}</td>
                </tr>
                <tr v-else v-for="candidate in candidateCampaigns" :key="candidate.name" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="flex-shrink-0 h-8 w-8">
                        <div class="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center">
                          <span class="text-sm font-medium text-blue-600">
                            							{{ candidate.talent_id?.charAt(0)?.toUpperCase() || 'C' }}
                          </span>
                        </div>
                      </div>
                      <div class="ml-3">
                        						<div class="text-sm font-medium text-gray-900">{{ candidate.talent_id }}</div>
                        <div class="text-sm text-gray-500">{{ __('Profile') }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span 
                      :class="getStatusClasses(candidate.status)"
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    >
                      {{ candidate.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {{ __('Step') }} {{ candidate.current_step_order }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatDate(candidate.enrolled_at) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <button
                      v-if="candidate.status === 'Draft' || candidate.status === 'Paused'"
                      @click="startCandidateCampaign(candidate)"
                      class="text-green-600 hover:text-green-900"
                      title="Start Campaign"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h8m2-10a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                    </button>
                    <button
                      v-if="candidate.status === 'Active'"
                      @click="pauseCandidateCampaign(candidate)"
                      class="text-yellow-600 hover:text-yellow-900"
                      title="Pause Campaign"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                    </button>
                    <button
                      @click="viewCandidateDetails(candidate)"
                      class="text-blue-600 hover:text-blue-900"
                      title="View Details"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                      </svg>
                    </button>
                    <button
                      @click="unassignCandidate(candidate)"
                      class="text-red-600 hover:text-red-900"
                      title="Unassign Candidate"
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
        
        <div v-if="activeTab === 'actions'">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">{{ __('Campaign Actions') }}</h3>
            <button
              @click="openActionModal()"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-black hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
              </svg>
              {{ __('Add Action') }}
            </button>
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
    <Dialog
      v-model="showCandidateModal"
      :options="{
        size: 'md'
      }"
    >
      <template #body>
        <div class="flex justify-between items-center mb-4 px-6 pt-6">
          <h3 class="text-lg font-medium text-gray-900">
            {{ __('Assign Profile to Campaign') }}
          </h3>
          <Button variant="outline" theme="gray" @click="closeCandidateModal" class="flex items-center">
           <FeatherIcon name="x" class="w-4 h-4" />
          </Button>
        </div>
        <div class="px-6 pb-6">
          <div class="space-y-4">
            <!-- Candidate Selection -->
            <FormControl
              v-model="candidateFormData.talent_id"
              type="select"
              :label="__('Select Candidate')"
              :required="true"
              :options="[{ label: __('Choose a candidate'), value: '' }, ...availableCandidates]"
              :help="availableCandidates.length === 0 ? (campaign.target_segment ? __('No available candidates found. All candidates from the target segment are already assigned.') : __('No available candidates found.')) : ''"
            />

            <!-- Status -->
            <FormControl
              v-model="candidateFormData.status"
              type="select"
              :label="__('Initial Status')"
              :required="true"
              :options="statusOptions"
            />

            <!-- Starting Step -->
            <FormControl
              v-model="candidateFormData.current_step_order"
              type="select"
              :label="__('Starting Step')"
              :required="true"
              :options="campaignSteps.map(step => ({ label: `Step ${step.step_order}: ${step.campaign_step_name}`, value: step.step_order }))"
              :help="campaignSteps.length === 0 ? __('No campaign steps found. Please add steps first.') : ''"
            />

            <!-- Buttons -->
            <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
              <Button
                variant="outline"
                theme="gray"
                @click="closeCandidateModal"
              >
                {{ __('Cancel') }}
              </Button>
              <Button
                variant="solid"
                theme="gray"
                :loading="savingCandidate"
                :disabled="!candidateFormData.talent_id || campaignSteps.length === 0"
                @click="assignCandidate"
              >
                {{ __('Assign Candidate') }}
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
              :options="[{ label: __('Select campaign step'), value: '' }, ...campaignSteps.map(step => ({ label: `Step ${step.step_order}: ${step.campaign_step_name}`, value: step.name }))]"
            />

            <!-- Candidate Campaign -->
            <FormControl
              v-model="actionFormData.candidate_campaign_id"
              type="select"
              :label="__('Candidate')"
              :required="true"
              									:options="[{ label: __('Select candidate'), value: '' }, ...candidateCampaigns.map(cc => ({ label: cc.talent_id, value: cc.name }))]"
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
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  campaignService, 
  campaignStepService, 
  candidateCampaignService,
  candidateService,
  candidateSegmentService,
  talentSegmentService,
  actionService
} from '../services/universalService'
import { Dialog, Breadcrumbs, Button, FormControl } from 'frappe-ui'
import CampaignForm from '@/components/campaign/CampaignForm.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import moment from 'moment'



const route = useRoute()
const router = useRouter()
const campaign = reactive({})

// Breadcrumbs
const breadcrumbs = computed(() => [
    { label: __('Campaigns'), route: { name: 'CampaignManagement' } },
    { label: campaign.campaign_name || __('Loading...'), route: { name: 'CampaignDetailView' } },
])


// State
const activeTab = ref('steps')
const loading = ref(false)
const loadingSteps = ref(false)
const loadingCandidates = ref(false)
const loadingActions = ref(false)

// Campaign data

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
  talent_id: '',
  campaign_id: route.params.id,
  status: 'ACTIVE',
  current_step_order: 1
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

// Table headers
const stepHeaders = [
  { label: 'Step Order', key: 'step_order' },
  { label: 'Step Name', key: 'campaign_step_name' },
  { label: 'Action Type', key: 'action_type' },
  { label: 'Delay (Days)', key: 'delay_in_days' },
  { label: 'Actions', key: 'actions', sortable: false }
]

const candidateHeaders = [
  	{ label: 'Candidate', key: 'talent_id' },
  { label: 'Status', key: 'status' },
  { label: 'Current Step', key: 'current_step_order' },
  { label: 'Enrolled At', key: 'enrolled_at' },
  { label: 'Actions', key: 'actions', sortable: false }
]

const actionHeaders = [
  { label: 'Campaign Step', key: 'campaign_step' },
  { label: 'Status', key: 'status' },
  { label: 'Scheduled At', key: 'scheduled_at' },
  { label: 'Executed At', key: 'executed_at' },
  { label: 'Actions', key: 'actions', sortable: false }
]

// Computed properties
const tabs = computed(() => [
  {
    key: 'steps',
    		label: __('Campaign Steps'),
    count: campaignSteps.value.length
  },
  {
    key: 'candidates',
    		label: __('Assigned Profiles'),
    count: candidateCampaigns.value.length
  },
  {
    key: 'actions',
    		label: __('Actions'),
    count: actions.value.length
  },
  {
    key: 'analytics',
    		label: __('Analytics'),
    count: 0
  }
])

// 1. Always sort campaignSteps by step_order ascending
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
    'ATTRACTION': 'bg-blue-100 text-blue-800'
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

// Methods
const loadCampaign = async () => {
  loading.value = true
  try {
    const result = await campaignService.getFormData(route.params.id)
    if (result.success) {
      Object.assign(campaign, result.data)
      // Load target segment if exists
      if (campaign.target_segment) {
        await loadTargetSegment()
      }
    }
  } catch (error) {
    console.error('Error loading campaign:', error)
  } finally {
    loading.value = false
  }
}

const loadTargetSegment = async () => {
  if (!campaign.target_segment) return
  
  try {
    const result = await talentSegmentService.getFormData(campaign.target_segment)
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
    const result = await campaignStepService.getList({
      filters: { campaign: route.params.id },
      fields: ['name', 'campaign_step_name', 'step_order', 'action_type', 'delay_in_days']
    })
    if (result.success) {
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
    const result = await candidateCampaignService.getList({
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
    // Load actions for this campaign through TalentProfilesCampaign
    const candidateCampaignsResult = await candidateCampaignService.getList({
      filters: { campaign_id: route.params.id },
      fields: ['name']
    })
    
    if (candidateCampaignsResult.success && candidateCampaignsResult.data.length > 0) {
      const candidateCampaignIds = candidateCampaignsResult.data.map(cc => cc.name)
      
      const result = await actionService.getList({
        filters: { candidate_campaign_id: ['in', candidateCampaignIds] },
        fields: ['name', 'campaign_step', 'status', 'scheduled_at', 'executed_at']
      })
      
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
    if (!campaign.target_segment) {
      // If no target segment, show all candidates
      const result = await candidateService.getList({
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
      // Get candidates from target segment through TalentProfilesSegment
      const candidateSegmentResult = await candidateSegmentService.getList({
        filters: { segment_id: campaign.target_segment },
        fields: ['talent_id']
      })
      
      if (candidateSegmentResult.success && candidateSegmentResult.data.length > 0) {
        const candidateIds = candidateSegmentResult.data.map(cs => cs.talent_id)
        
        // Get candidates already in this campaign
        const existingCandidateCampaigns = await candidateCampaignService.getList({
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
          const candidateResult = await candidateService.getList({
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

const saveStep = async () => {
  console.log('Saving step with data:', stepFormData)

  savingStep.value = true
  try {
    const result = await campaignStepService.save(stepFormData, stepFormData.name)
    if (result.success) {
      closeStepModal()
      loadCampaignSteps()
    }
  } catch (error) {
    console.error('Error saving step:', error)
  } finally {
    savingStep.value = false
  }
}

const deleteStep = async (step) => {
  if (confirm('Are you sure you want to delete this step?')) {
    try {
      const result = await campaignStepService.delete(step.name)
      if (result.success) {
        // Sau khi xóa, lấy lại danh sách step và cập nhật lại step_order liên tục
        await loadCampaignSteps()
        // Dồn lại thứ tự
        const steps = sortedCampaignSteps.value
        for (let i = 0; i < steps.length; i++) {
          if (steps[i].step_order !== i + 1) {
            steps[i].step_order = i + 1
            await campaignStepService.save(steps[i], steps[i].name)
          }
        }
        await loadCampaignSteps()
      }
    } catch (error) {
      console.error('Error deleting step:', error)
    }
  }
}

// 4. Add methods for move up/down/copy
const moveStepUp = async (idx) => {
  if (idx === 0) return
  const steps = sortedCampaignSteps.value
  const stepA = steps[idx]
  const stepB = steps[idx - 1]
  // Swap step_order
  const temp = stepA.step_order
  stepA.step_order = stepB.step_order
  stepB.step_order = temp
  // Save both
  await campaignStepService.save(stepA, stepA.name)
  await campaignStepService.save(stepB, stepB.name)
  await loadCampaignSteps()
}
const moveStepDown = async (idx) => {
  const steps = sortedCampaignSteps.value
  if (idx === steps.length - 1) return
  const stepA = steps[idx]
  const stepB = steps[idx + 1]
  // Swap step_order
  const temp = stepA.step_order
  stepA.step_order = stepB.step_order
  stepB.step_order = temp
  // Save both
  await campaignStepService.save(stepA, stepA.name)
  await campaignStepService.save(stepB, stepB.name)
  await loadCampaignSteps()
}
const copyStep = async (step) => {
  // Tạo step mới với thông tin giống step cũ, step_order = max + 1
  const maxOrder = Math.max(...campaignSteps.value.map(s => s.step_order), 0)
  const newStep = {
    ...step,
    name: undefined,
    step_order: maxOrder + 1,
    campaign_step_name: step.campaign_step_name + ' (Copy)'
  }
  await campaignStepService.save(newStep)
  await loadCampaignSteps()
}

// Candidate methods
const openCandidateModal = async () => {
  Object.keys(candidateFormData).forEach(key => {
    candidateFormData[key] = ''
  })
  candidateFormData.campaign_id = route.params.id
  candidateFormData.status = 'ACTIVE'
  candidateFormData.current_step_order = 1
  
  // Reload available candidates to get most up-to-date list
  await loadAvailableCandidates()
  
  showCandidateModal.value = true
}

const closeCandidateModal = () => {
  showCandidateModal.value = false
}

const assignCandidate = async () => {
  console.log('Assigning candidate:', candidateFormData)
  if (!candidateFormData.talent_id) return

  savingCandidate.value = true
  try {
    const result = await candidateCampaignService.save(candidateFormData)
    if (result.success) {
      closeCandidateModal()
      loadCandidateCampaigns()
    }
  } catch (error) {
    console.error('Error assigning candidate:', error)
  } finally {
    savingCandidate.value = false
  }
}

const startCandidateCampaign = async (item) => {
  try {
    const result = await candidateCampaignService.save(
      { ...item, status: 'ACTIVE' },
      item.name
    )
    if (result.success) {
      loadCandidateCampaigns()
    }
  } catch (error) {
    console.error('Error starting campaign:', error)
  }
}

const pauseCandidateCampaign = async (item) => {
  try {
    const result = await candidateCampaignService.save(
      { ...item, status: 'PAUSED' },
      item.name
    )
    if (result.success) {
      loadCandidateCampaigns()
    }
  } catch (error) {
    console.error('Error pausing campaign:', error)
  }
}

const unassignCandidate = async (item) => {
  if (confirm('Are you sure you want to unassign this candidate?')) {
    try {
      const result = await candidateCampaignService.delete(item.name)
      if (result.success) {
        loadCandidateCampaigns()
      }
    } catch (error) {
      console.error('Error unassigning candidate:', error)
    }
  }
}

const viewCandidateDetails = (item) => {
  		router.push(`/candidates/${item.talent_id}`)
}

// Assign all candidates from segment
const assignAllFromSegment = async () => {
  if (!confirm(`Are you sure you want to assign all ${availableCandidates.value.length} candidates from the target segment to this campaign?`)) {
    return
  }
  
  assigningAll.value = true
  try {
            // Create TalentProfilesCampaign records for all available candidates
    const promises = availableCandidates.value.map(candidate => 
      candidateCampaignService.save({
        talent_id: candidate.value,
        campaign_id: route.params.id,
        status: 'ACTIVE',
        current_step_order: 1,
        enrolled_at: moment().format("YYYY-MM-DD HH:mm:ss")
      })
    )
    
    await Promise.all(promises)
    
    // Reload data
    await loadCandidateCampaigns()
    await loadAvailableCandidates()
    
    console.log('Successfully assigned all candidates from segment')
  } catch (error) {
    console.error('Error assigning all candidates:', error)
  } finally {
    assigningAll.value = false
  }
}

// Action methods
const openActionModal = (action = null) => {
  if (action) {
    Object.assign(actionFormData, action)
  } else {
    Object.keys(actionFormData).forEach(key => {
      actionFormData[key] = ''
    })
  }
  showActionModal.value = true
}

const closeActionModal = () => {
  showActionModal.value = false
  Object.keys(actionFormData).forEach(key => {
    actionFormData[key] = ''
  })
}

const saveAction = async () => {
  savingAction.value = true
  try {
    const result = await actionService.save(actionFormData, actionFormData.name)
    if (result.success) {
      closeActionModal()
      loadActions()
    }
  } catch (error) {
    console.error('Error saving action:', error)
  } finally {
    savingAction.value = false
  }
}

const viewActionDetails = (action) => {
  // Implementation for viewing action details
  openActionModal(action)
}

const deleteAction = async (action) => {
  if (confirm('Are you sure you want to delete this action?')) {
    try {
      const result = await actionService.delete(action.name)
      if (result.success) {
        loadActions()
      }
    } catch (error) {
      console.error('Error deleting action:', error)
    }
  }
}

// Utility methods
const getStatusColor = (status) => {
  const colors = {
    'ACTIVE': 'success',
    'PAUSED': 'warning',
    'COMPLETED': 'primary',
    'CANCELLED': 'error',
    'DRAFT': 'grey',
    'ARCHIVED': 'grey'
  }
  return colors[status] || 'grey'
}

const getTypeColor = (type) => {
  const colors = {
    'NURTURING': 'purple',
    'ATTRACTION': 'blue'
  }
  return colors[type] || 'grey'
}

const getStepTypeColor = (type) => {
  const colors = {
    'SEND_EMAIL': 'blue',
    'SEND_SMS': 'green',
    'MANUAL_CALL': 'orange',
    'MANUAL_TASK': 'purple'
  }
  return colors[type] || 'grey'
}

const getActionTypeColor = (type) => {
  const colors = {
    'SEND_EMAIL': 'blue',
    'SEND_SMS': 'green',
    'MANUAL_CALL': 'orange',
    'MANUAL_TASK': 'purple'
  }
  return colors[type] || 'grey'
}

const getActionStatusColor = (status) => {
  const colors = {
    'SCHEDULED': 'info',
    'EXECUTED': 'success',
    'SKIPPED': 'warning',
    'FAILED': 'error',
    'PENDING_MANUAL': 'orange'
  }
  return colors[status] || 'grey'
}

const formatDateTime = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const getActiveCandidates = () => {
  return candidateCampaigns.value.filter(item => item.status === 'ACTIVE').length
}

const getCompletedCandidates = () => {
  return candidateCampaigns.value.filter(item => item.status === 'COMPLETED').length
}

const editCampaign = () => {
  // Ensure we have loaded campaign data before opening modal
  if (Object.keys(campaign).length === 0) {
    console.warn('Campaign data not loaded yet')
    return
  }
  // Open edit modal with current campaign data
  showEditCampaignModal.value = true
}

const handleCampaignUpdated = async () => {
  console.log('Campaign updated successfully')
  // Reload campaign data
  await loadCampaign()
}

const deleteCampaign = async () => {
  if (confirm('Are you sure you want to delete this campaign?')) {
    try {
      const result = await campaignService.delete(route.params.id)
      if (result.success) {
        router.push('/campaigns')
      }
    } catch (error) {
      console.error('Error deleting campaign:', error)
    }
  }
}

const viewTargetSegment = () => {
  if (targetSegment.value) {
    router.push(`/talent-segments/${targetSegment.value.name}/detail`)
  }
}

// Lifecycle
onMounted(async () => {
  await loadCampaign()
  await loadCampaignSteps()
  await loadCandidateCampaigns()
  await loadActions()
  await loadAvailableCandidates()
})
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
