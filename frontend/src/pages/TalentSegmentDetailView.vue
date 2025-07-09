<template>
  <div class="min-h-screen bg-gray-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
    </LayoutHeader>

    <div class="container mx-auto px-6 py-6">
      <!-- Header with Talent Segment Info -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div class="flex justify-between items-start">
          <div class="flex items-start">
            <Button
              variant="ghost"
              theme="gray"
              @click="$router.go(-1)"
              class="mr-4 mt-1"
            >
              <template #prefix>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </template>
            </Button>
            <div>
              <h1 class="text-3xl font-bold text-gray-900 mb-3">
                {{ talentSegment.title || 'Loading...' }}
              </h1>
              <div class="flex items-center flex-wrap gap-3">
                <span 
                  :class="getBadgeClass(talentSegment.type)"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                >
                  {{ talentSegment.type }}
                </span>
                <span class="text-sm text-gray-500">
                  Created: {{ formatDate(talentSegment.creation) }}
                </span>
                <span class="text-sm text-gray-500">
                  Modified: {{ formatDate(talentSegment.modified) }}
                </span>
              </div>
            </div>
          </div>
          
          <div class="flex items-center space-x-3">
            <Button
              variant="outline"
              theme="gray"
              @click="editTalentSegment"
            >
              <template #prefix>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </template>
              Edit Segment
            </Button>
            <Button
              variant="outline"
              theme="red"
              @click="deleteTalentSegment"
            >
              <template #prefix>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </template>
              Delete
            </Button>
          </div>
        </div>
      </div>

      <!-- Talent Segment Details Card -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div class="flex items-center mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <h2 class="text-xl font-semibold text-gray-900">Talent Segment Information</h2>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-4">
            <div>
              <span class="text-sm font-medium text-gray-500">Title:</span>
              <p class="mt-1 text-sm text-gray-900">{{ talentSegment.title || 'N/A' }}</p>
            </div>
            <div>
              <span class="text-sm font-medium text-gray-500">Description:</span>
              <p class="mt-1 text-sm text-gray-900">{{ talentSegment.description || 'N/A' }}</p>
            </div>
            <div>
              <span class="text-sm font-medium text-gray-500">Type:</span>
              <div class="mt-1">
                <span 
                  :class="getBadgeClass(talentSegment.type)"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                >
                  {{ talentSegment.type }}
                </span>
              </div>
            </div>
          </div>
          <div class="space-y-4">
            <div>
              <span class="text-sm font-medium text-gray-500">Owner:</span>
              <p class="mt-1 text-sm text-gray-900">{{ talentSegment.owner_id || 'N/A' }}</p>
            </div>
            <div>
              <span class="text-sm font-medium text-gray-500">Candidate Count:</span>
              <div class="mt-1">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {{ talentSegment.candidate_count || 0 }} candidates
                </span>
              </div>
            </div>
            <div>
              <span class="text-sm font-medium text-gray-500">Created By:</span>
              <p class="mt-1 text-sm text-gray-900">{{ talentSegment.owner || 'N/A' }}</p>
            </div>
          </div>
        </div>
        
        <!-- Criteria (if available) -->
        <div v-if="talentSegment.criteria" class="mt-6">
          <span class="text-sm font-medium text-gray-500">Criteria:</span>
          <div class="mt-2 bg-gray-50 rounded-lg border border-gray-200 p-4">
            <pre class="text-sm text-gray-900 whitespace-pre-wrap">{{ formatCriteria(talentSegment.criteria) }}</pre>
          </div>
        </div>
      </div>

      <!-- Tabbed Content -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <!-- Tab Navigation -->
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8 px-6" aria-label="Tabs">
            <button
              @click="activeTab = 'candidates'"
              :class="[
                activeTab === 'candidates'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center'
              ]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
              </svg>
              Candidates ({{ candidates.length }})
            </button>
            <button
              @click="activeTab = 'campaigns'"
              :class="[
                activeTab === 'campaigns'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center'
              ]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Related Campaigns
            </button>
            <button
              @click="activeTab = 'analytics'"
              :class="[
                activeTab === 'analytics'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center'
              ]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Analytics
            </button>
          </nav>
        </div>
        <!-- Tab Content -->
        <div class="p-6">
          <!-- Candidates Tab -->
          <div v-if="activeTab === 'candidates'">
            <div class="flex justify-between items-center mb-6">
              <h3 class="text-lg font-medium text-gray-900">Candidates in this Segment</h3>
              <div class="flex items-center space-x-3">
                <div class="relative">
                  <input
                    v-model="candidateSearch"
                    type="text"
                    placeholder="Search candidates..."
                    class="block w-80 pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  />
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                  </div>
                </div>
                <Button
                  variant="solid"
                  theme="gray"
                  @click="openAddCandidateModal()"
                >
                  <template #prefix>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                  </template>
                  Add Candidate
                </Button>
              </div>
            </div>
            
            <!-- Candidates Table -->
            <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
              <table class="min-w-full divide-y divide-gray-300">
                <thead class="bg-gray-50">
                  <tr>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Candidate
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Skills
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Last Contact
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Added At
                    </th>
                    <th scope="col" class="relative px-6 py-3">
                      <span class="sr-only">Actions</span>
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="loadingCandidates">
                    <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                      <div class="flex justify-center">
                        <svg class="animate-spin h-5 w-5 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                      </div>
                    </td>
                  </tr>
                  <tr v-else-if="filteredCandidates.length === 0">
                    <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                      No candidates found
                    </td>
                  </tr>
                  <tr v-else v-for="candidate in filteredCandidates" :key="candidate.name" class="hover:bg-gray-50">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="flex-shrink-0 h-8 w-8">
                          <div class="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center">
                            <span class="text-xs font-medium text-white">{{ candidate.candidate_name?.charAt(0) || '?' }}</span>
                          </div>
                        </div>
                        <div class="ml-3">
                          <div class="text-sm font-medium text-gray-900">{{ candidate.candidate_name }}</div>
                          <div class="text-sm text-gray-500">{{ candidate.email }}</div>
                        </div>
                      </div>
                    </td>
                    <td class="px-6 py-4">
                      <div class="flex flex-wrap gap-1">
                        <span
                          v-for="skill in processSkills(candidate.skills)"
                          :key="skill"
                          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                        >
                          {{ skill }}
                        </span>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {{ formatDateTime(candidate.last_contact) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="getStatusBadgeClass(candidate.status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                        {{ candidate.status }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {{ formatDateTime(candidate.added_at) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div class="flex items-center space-x-2">
                        <Button
                          variant="ghost"
                          theme="gray"
                          size="sm"
                          @click="viewCandidateDetails(candidate)"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                          </svg>
                        </Button>
                        <Button
                          variant="ghost"
                          theme="blue"
                          size="sm"
                          @click="contactCandidate(candidate)"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                          </svg>
                        </Button>
                        <Button
                          variant="ghost"
                          theme="red"
                          size="sm"
                          @click="removeFromSegment(candidate)"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </Button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Related Campaigns Tab -->
          <div v-else-if="activeTab === 'campaigns'">
            <div class="flex justify-between items-center mb-6">
              <h3 class="text-lg font-medium text-gray-900">Related Campaigns</h3>
              <Button
                variant="solid"
                theme="gray"
                @click="showCampaignWizard = true"
              >
                <template #prefix>
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                </template>
                Create Campaign
              </Button>
            </div>
            
            <!-- Related Campaigns Table -->
            <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
              <table class="min-w-full divide-y divide-gray-300">
                <thead class="bg-gray-50">
                  <tr>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Campaign Name
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Start Date
                    </th>
                    <th scope="col" class="relative px-6 py-3">
                      <span class="sr-only">Actions</span>
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="loadingCampaigns">
                    <td colspan="4" class="px-6 py-4 text-center text-gray-500">
                      <div class="flex justify-center">
                        <svg class="animate-spin h-5 w-5 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                      </div>
                    </td>
                  </tr>
                  <tr v-else-if="relatedCampaigns.length === 0">
                    <td colspan="4" class="px-6 py-4 text-center text-gray-500">
                      No campaigns found
                    </td>
                  </tr>
                  <tr v-else v-for="campaign in relatedCampaigns" :key="campaign.name" class="hover:bg-gray-50">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm font-medium text-gray-900">{{ campaign.campaign_name }}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="getStatusBadgeClass(campaign.status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                        {{ campaign.status }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {{ formatDateTime(campaign.start_date) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <Button
                        variant="ghost"
                        theme="blue"
                        size="sm"
                        @click="viewCampaignDetails(campaign)"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                      </Button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Analytics Tab -->
          <div v-else-if="activeTab === 'analytics'">
            <h3 class="text-lg font-medium text-gray-900 mb-6">Segment Analytics</h3>
            
            <!-- Stats Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <div class="bg-white p-6 rounded-lg border border-gray-200 text-center">
                <div class="text-3xl font-bold text-blue-600">{{ talentSegment.candidate_count || 0 }}</div>
                <div class="text-sm text-gray-500 mt-1">Total Candidates</div>
              </div>
              <div class="bg-white p-6 rounded-lg border border-gray-200 text-center">
                <div class="text-3xl font-bold text-green-600">{{ getActiveCandidates() }}</div>
                <div class="text-sm text-gray-500 mt-1">Active Candidates</div>
              </div>
              <div class="bg-white p-6 rounded-lg border border-gray-200 text-center">
                <div class="text-3xl font-bold text-yellow-600">{{ relatedCampaigns.length }}</div>
                <div class="text-sm text-gray-500 mt-1">Related Campaigns</div>
              </div>
              <div class="bg-white p-6 rounded-lg border border-gray-200 text-center">
                <div class="text-3xl font-bold text-purple-600">{{ getEngagementRate() }}%</div>
                <div class="text-sm text-gray-500 mt-1">Engagement Rate</div>
              </div>
            </div>
            
            <!-- Chart placeholder -->
            <div class="bg-white p-8 rounded-lg border border-gray-200">
              <h4 class="text-lg font-medium text-gray-900 mb-6">Segment Analytics</h4>
              <div class="text-center py-12">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-300 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <p class="text-gray-500">
                  Analytics charts will be implemented here
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Add Candidate Modal -->
      <Dialog v-model="showAddCandidateModal" :options="{ title: 'Add Candidate to Segment', size: 'md' }">
        <template #body>
          <div class="space-y-4">
            <div>
              <label for="candidate-select" class="block text-sm font-medium text-gray-700 mb-2">
                Select Candidate *
              </label>
              <select
                id="candidate-select"
                v-model="candidateFormData.candidate_id"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                required
              >
                <option value="">Choose a candidate...</option>
                <option
                  v-for="candidate in availableCandidates"
                  :key="candidate.value"
                  :value="candidate.value"
                >
                  {{ candidate.title }}
                </option>
              </select>
            </div>
          </div>
        </template>
        <template #actions>
          <Button variant="outline" theme="gray" @click="closeAddCandidateModal">
            Cancel
          </Button>
          <Button
            variant="solid"
            theme="blue"
            :loading="savingCandidate"
            :disabled="!candidateFormData.candidate_id"
            @click="addCandidateToSegment"
          >
            Add Candidate
          </Button>
        </template>
      </Dialog>

      <!-- Campaign Wizard -->
      <CampaignWizard
        v-model="showCampaignWizard"
        :preselected-segment="route.params.id"
        @success="handleCampaignCreated"
      />

      <!-- Edit Talent Segment Modal -->
      <Dialog v-model="showEditTalentSegmentModal" :options="editSegmentDialogOptions">
        <template #body>
          <div class="bg-white px-4 pb-6 pt-5 sm:px-6">
            <div class="mb-5 flex items-center justify-between">
              <div>
                <h3 class="text-2xl font-semibold leading-6 text-gray-900">
                  Edit Talent Pool
                </h3>
              </div>
              <div class="flex items-center gap-1">
                <Button variant="ghost" class="w-7" @click="showEditTalentSegmentModal = false">
                  <FeatherIcon name="x" class="h-4 w-4" />
                </Button>
              </div>
            </div>
            <div class="max-h-[60vh] overflow-y-auto">
              <TalentSegmentForm 
                :segment="editingSegmentData" 
                @success="handleTalentSegmentUpdated" 
                @cancel="handleEditModalClose" 
              />
            </div>
          </div>
        </template>
      </Dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  talentSegmentService,
  candidateSegmentService,
  candidateCampaignService,
  candidateService,
  campaignService
} from '../services/universalService'
import { processSkills } from '../services/candidateService'
import { usersStore } from '@/stores/users'
import { Button, Dialog, Breadcrumbs, FeatherIcon } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import CampaignWizard from '@/components/campaign/CampaignWizard.vue'
import TalentSegmentForm from '@/components/talent-segment/TalentSegmentForm.vue'
import moment from 'moment'

const { getUser } = usersStore()
const route = useRoute()
const router = useRouter()

// Breadcrumbs
const breadcrumbs = [
  { label: 'Talent Pools', route: { name: 'TalentSegments' } },
  { label: 'Detail', route: { name: 'TalentSegmentDetail' } }
]

// State
const activeTab = ref('candidates')
const loading = ref(false)
const loadingCandidates = ref(false)
const loadingCampaigns = ref(false)

// Data
const talentSegment = reactive({})
const candidates = ref([])
const relatedCampaigns = ref([])
const availableCandidates = ref([])

// Modals
const showAddCandidateModal = ref(false)
const showCampaignWizard = ref(false)
const showEditTalentSegmentModal = ref(false)
const editingSegmentData = ref(null)
const savingCandidate = ref(false)

// Search
const candidateSearch = ref('')

// Form data
const candidateFormData = reactive({
  candidate_id: '',
  segment_id: route.params.id
})

// Computed
const filteredCandidates = computed(() => {
  if (!candidateSearch.value) return candidates.value
  const search = candidateSearch.value.toLowerCase()
  return candidates.value.filter(candidate => 
    candidate.candidate_name?.toLowerCase().includes(search) ||
    candidate.email?.toLowerCase().includes(search)
  )
})

// Dialog options
const editSegmentDialogOptions = computed(() => ({
  title: 'Edit Talent Pool',
  size: '4xl'
}))

// Methods
const loadTalentSegment = async () => {
  loading.value = true
  try {
    const result = await talentSegmentService.getFormData(route.params.id)
    if (result.success) {
      Object.assign(talentSegment, result.data)
    }
  } catch (error) {
    console.error('Error loading talent segment:', error)
  } finally {
    loading.value = false
  }
}

const loadCandidates = async () => {
  loadingCandidates.value = true
  try {
    // First, get all CandidateSegment records for this segment
    const candidateSegmentResult = await candidateSegmentService.getList({
      filters: { segment_id: route.params.id },
      fields: ['name', 'candidate_id', 'added_at', 'added_by']
    })
    
    if (candidateSegmentResult.success && candidateSegmentResult.data.length > 0) {
      // Get candidate IDs from the relationship
      const candidateIds = candidateSegmentResult.data.map(cs => cs.candidate_id)
      
      // Then get the actual candidate data
      const candidateResult = await candidateService.getList({
        filters: { name: ['in', candidateIds] },
        fields: ['name', 'candidate_name', 'email', 'skills', 'last_contact', 'status']
      })
      
      if (candidateResult.success) {
        // Merge the data - add segment relationship info to candidate data
        candidates.value = candidateResult.data.map(candidate => {
          const segmentRelation = candidateSegmentResult.data.find(cs => cs.candidate_id === candidate.name)
          return {
            ...candidate,
            added_at: segmentRelation?.added_at,
            added_by: segmentRelation?.added_by,
            candidate_segment_id: segmentRelation?.name
          }
        })
      }
    } else {
      candidates.value = []
    }
  } catch (error) {
    console.error('Error loading candidates:', error)
    candidates.value = []
  } finally {
    loadingCandidates.value = false
  }
}

const loadRelatedCampaigns = async () => {
  loadingCampaigns.value = true
  try {
    // First get candidates in this segment
    const candidateSegmentResult = await candidateSegmentService.getList({
      filters: { segment_id: route.params.id },
      fields: ['candidate_id']
    })
    
    if (candidateSegmentResult.success && candidateSegmentResult.data.length > 0) {
      const candidateIds = candidateSegmentResult.data.map(cs => cs.candidate_id)
      
      // Then get campaigns that have these candidates through CandidateCampaign
      const candidateCampaignResult = await candidateCampaignService.getList({
        filters: { candidate_id: ['in', candidateIds] },
        fields: ['campaign_id']
      })
      
      if (candidateCampaignResult.success && candidateCampaignResult.data.length > 0) {
        const campaignIds = [...new Set(candidateCampaignResult.data.map(cc => cc.campaign_id))]
        
        // Get the actual campaign data
        const campaignResult = await campaignService.getList({
          filters: { name: ['in', campaignIds] },
          fields: ['name', 'campaign_name', 'status', 'start_date']
        })
        
        if (campaignResult.success) {
          relatedCampaigns.value = campaignResult.data
        }
      }
    } else {
      relatedCampaigns.value = []
    }
  } catch (error) {
    console.error('Error loading related campaigns:', error)
    relatedCampaigns.value = []
  } finally {
    loadingCampaigns.value = false
  }
}

const loadAvailableCandidates = async () => {
  try {
    // Get all candidates
    const allCandidatesResult = await candidateService.getList({
      fields: ['name', 'candidate_name'],
      page_length: 1000
    })
    
    if (allCandidatesResult.success) {
      // Get candidates already in this segment
      const existingCandidateSegments = await candidateSegmentService.getList({
        filters: { segment_id: route.params.id },
        fields: ['candidate_id']
      })
      
      const existingCandidateIds = existingCandidateSegments.success 
        ? existingCandidateSegments.data.map(cs => cs.candidate_id)
        : []
      
      // Filter out candidates already in the segment
      const availableCandidatesData = allCandidatesResult.data.filter(
        candidate => !existingCandidateIds.includes(candidate.name)
      )
      
      availableCandidates.value = availableCandidatesData.map(item => ({
        title: item.candidate_name || item.name,
        value: item.name
      }))
    }
  } catch (error) {
    console.error('Error loading candidates:', error)
  }
}

// Candidate methods
const openAddCandidateModal = () => {
  candidateFormData.candidate_id = ''
  showAddCandidateModal.value = true
}

const closeAddCandidateModal = () => {
  showAddCandidateModal.value = false
}

const addCandidateToSegment = async () => {
  if (!candidateFormData.candidate_id) return

  savingCandidate.value = true
  try {
    // Create a new CandidateSegment relationship
    const candidateSegmentData = {
      candidate_id: candidateFormData.candidate_id,
      segment_id: route.params.id,
      added_at: moment().format("YYYY-MM-DD HH:mm:ss"),
      added_by: getUser()?.name || 'Administrator'
    }
    
    const result = await candidateSegmentService.save(candidateSegmentData)
    if (result.success) {
      closeAddCandidateModal()
      await loadCandidates()
      await loadTalentSegment()
    }
  } catch (error) {
    console.error('Error adding candidate:', error)
  } finally {
    savingCandidate.value = false
  }
}

const viewCandidateDetails = (candidate) => {
  router.push(`/candidates/${candidate.name}`)
}

const contactCandidate = (candidate) => {
  // Implementation for contacting candidate
  console.log('Contact candidate:', candidate)
}

const removeFromSegment = async (candidate) => {
  if (confirm('Are you sure you want to remove this candidate from the segment?')) {
    try {
      // Delete the CandidateSegment relationship
      if (candidate.candidate_segment_id) {
        const result = await candidateSegmentService.delete(candidate.candidate_segment_id)
        if (result.success) {
          await loadCandidates()
          // Update the segment's candidate count
          await loadTalentSegment()
        }
      }
    } catch (error) {
      console.error('Error removing candidate:', error)
    }
  }
}

// Assign all candidates from segment
const handleCampaignCreated = async (event) => {
  console.log('Campaign created successfully:', event)
  // Reload related campaigns
  await loadRelatedCampaigns()
}

const handleTalentSegmentUpdated = async () => {
  console.log('Talent segment updated successfully')
  showEditTalentSegmentModal.value = false
  // Reload talent segment data
  await loadTalentSegment()
}

const createCampaignFromSegment = () => {
  // This method is kept for backward compatibility but now opens wizard
  showCampaignWizard.value = true
}

const viewCampaignDetails = (campaign) => {
  router.push(`/campaigns/${campaign.name}`)
}

// Utility methods
const getBadgeClass = (type) => {
  const badges = {
    'DYNAMIC': 'bg-blue-100 text-blue-800',
    'MANUAL': 'bg-purple-100 text-purple-800',
    'default': 'bg-green-100 text-green-800'
  }
  return badges[type] || badges.default
}

const getStatusBadgeClass = (status) => {
  const badges = {
    'ACTIVE': 'bg-green-100 text-green-800',
    'PAUSED': 'bg-yellow-100 text-yellow-800',
    'COMPLETED': 'bg-blue-100 text-blue-800',
    'CANCELLED': 'bg-red-100 text-red-800',
    'Draft': 'bg-gray-100 text-gray-800'
  }
  return badges[status] || badges['Draft']
}

const getTypeColor = (type) => {
  const colors = {
    'DYNAMIC': 'blue',
    'MANUAL': 'green'
  }
  return colors[type] || 'grey'
}

const getStatusColor = (status) => {
  const colors = {
    'ACTIVE': 'success',
    'PAUSED': 'warning',
    'COMPLETED': 'primary',
    'CANCELLED': 'error',
    'Draft': 'grey'
  }
  return colors[status] || 'grey'
}

const getSkillColor = (skill) => {
  const colors = ['primary', 'secondary', 'success', 'info', 'warning', 'error']
  const hash = skill.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0)
    return a & a
  }, 0)
  return colors[Math.abs(hash) % colors.length]
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

const formatCriteria = (criteria) => {
  if (!criteria) return ''
  try {
    return JSON.stringify(JSON.parse(criteria), null, 2)
  } catch {
    return criteria
  }
}

const getActiveCandidates = () => {
  return candidates.value.filter(item => item.status === 'ACTIVE').length
}

const getEngagementRate = () => {
  // Calculate engagement rate based on candidates data
  if (candidates.value.length === 0) return 0
  const activeCount = getActiveCandidates()
  return Math.round((activeCount / candidates.value.length) * 100)
}

const editTalentSegment = () => {
  // Ensure we have loaded segment data before opening modal
  if (Object.keys(talentSegment).length === 0) {
    console.warn('Talent segment data not loaded yet')
    return
  }
  // Open edit modal with current segment data
  editingSegmentData.value = talentSegment
  showEditTalentSegmentModal.value = true
}

const deleteTalentSegment = async () => {
  if (confirm('Are you sure you want to delete this talent segment?')) {
    try {
      const result = await talentSegmentService.delete(route.params.id)
      if (result.success) {
        router.push('/talent-segments')
      }
    } catch (error) {
      console.error('Error deleting talent segment:', error)
    }
  }
}

const handleEditModalClose = () => {
  showEditTalentSegmentModal.value = false
  // Reset editing data to trigger form reset
  editingSegmentData.value = null
}

// Lifecycle
onMounted(async () => {
  await loadTalentSegment()
  await loadCandidates()
  await loadRelatedCampaigns()
  await loadAvailableCandidates()
})
</script>

<style scoped>
.talent-segment-detail-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>
