<template>
	<div class="min-h-screen bg-gray-50">
		<LayoutHeader>
			<template #left-header>
				<Breadcrumbs :items="breadcrumbs" />
			</template>
			<template #right-header>
				<Button variant="outline" theme="gray" @click="openEditModal">
					<template #prefix>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
							stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
								d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
						</svg>
					</template>
					{{ __('Edit Pool') }}
				</Button>
				<Button variant="outline" theme="red" @click="$router.push('/talent-pools')">
					<template #prefix>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
							stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
								d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
						</svg>
					</template>
					{{ __('Delete') }}
				</Button>
			</template>
		</LayoutHeader>

		<div class="container mx-auto px-6 py-6">
			<!-- Header with Talent Segment Info -->
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
								{{ talentSegment.title || __('Loading...') }}
							</h1>
							<div class="flex items-center flex-wrap gap-3">
																	<span
										class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
									>
										{{ talentSegment.type || __('Active') }}
									</span>
								<span class="text-sm text-gray-500">
									{{ __('Created:') }} {{ formatDate(talentSegment.creation) }}
								</span>
								<span class="text-sm text-gray-500">
									{{ __('Modified:') }} {{ formatDate(talentSegment.modified) }}
								</span>
							</div>
						</div>
					</div>

					<div class="flex items-center space-x-3">
						


					</div>
				</div>
			</div> -->

			<!-- Detailed Analytics Cards -->
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
				<div class="bg-gradient-to-r from-gray-50 to-gray-100 p-6 rounded-lg border border-gray-200">
					<div class="flex items-center">
						<div class="flex-shrink-0">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-600" fill="none"
								viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
									d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
							</svg>
						</div>
						<div class="ml-4">
							<div class="text-2xl font-bold text-blue-900">
								{{ talentSegment.candidate_count || 0 }}
							</div>
							<div class="text-sm text-blue-700">{{ __('Total Talents') }}</div>
						</div>
					</div>
				</div>
				<div class="bg-gradient-to-r from-green-50 to-green-100 p-6 rounded-lg border border-green-200">
					<div class="flex items-center">
						<div class="flex-shrink-0">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-600" fill="none"
								viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
									d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
							</svg>
						</div>
						<div class="ml-4">
							<div class="text-2xl font-bold text-green-900">
								{{candidates.filter(c => c.status === 'ACTIVE').length}}
							</div>
							<div class="text-sm text-green-700">{{ __('Active Talents') }}</div>
						</div>
					</div>
				</div>
				<div class="bg-gradient-to-r from-yellow-50 to-yellow-100 p-6 rounded-lg border border-yellow-200">
					<div class="flex items-center">
						<div class="flex-shrink-0">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-yellow-600" fill="none"
								viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
									d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a1 1 0 011-1h1m-1 4h10m0-4V5a1 1 0 011-1h1m-4 0h.01" />
							</svg>
						</div>
						<div class="ml-4">
							<div class="text-2xl font-bold text-yellow-900">
								{{ relatedCampaigns.length }}
							</div>
							<div class="text-sm text-yellow-700">{{ __('Related Campaigns') }}</div>
						</div>
					</div>
				</div>
				<div class="bg-gradient-to-r from-purple-50 to-purple-100 p-6 rounded-lg border border-purple-200">
					<div class="flex items-center">
						<div class="flex-shrink-0">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-purple-600" fill="none"
								viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
									d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
							</svg>
						</div>
						<div class="ml-4">
							<div class="text-2xl font-bold text-purple-900">
								{{candidates.length > 0 ? Math.round((candidates.filter(c => c.status ===
									'ACTIVE').length /
									candidates.length) * 100) : 0}}%
							</div>
							<div class="text-sm text-purple-700">{{ __('Mira Interaction Rate') }}</div>
						</div>
					</div>
				</div>
			</div>
			

			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
				<!-- Overall Potential Score -->
				<div class="bg-gradient-to-r from-teal-50 to-teal-100 p-6 rounded-lg border border-teal-200">
					<div class="flex items-center">
						<div class="flex-shrink-0">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-teal-600" fill="none"
								viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
									d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
							</svg>
						</div>
						<div class="ml-4">
							<div class="text-2xl font-bold text-teal-900">
								92/100
							</div>
							<!-- <div class="text-sm text-teal-700">{{ __('Overall Potential Score') }}</div> -->
							<div class="text-xs text-teal-600 mt-1">{{ __('Higher than overall score 85/100') }}</div>
						</div>
					</div>
				</div>

				<!-- High Recruitment Readiness Rate -->
				<div class="bg-gradient-to-r from-indigo-50 to-indigo-100 p-6 rounded-lg border border-indigo-200">
					<div class="flex items-center">
						<div class="flex-shrink-0">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-indigo-600" fill="none"
								viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
									d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
							</svg>
						</div>
						<div class="ml-4">
							<div class="text-2xl font-bold text-indigo-900">
								45%
							</div>
							<div class="text-sm text-indigo-700">{{ __('High hiring readiness rate') }}</div>
						</div>
					</div>
				</div>
				
			</div>

			<!-- Advanced Quality Assessment -->
			<div class="mb-8">
				<div class="mb-4">
					<h2 class="text-2xl font-bold text-gray-900">{{ __('Advanced Quality Assessment') }}</h2>
					<p class="text-sm text-gray-600 mt-1">{{ __('In-depth analysis of skills and experience distribution') }}</p>
				</div>
				
				<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
					<!-- Skill Deep Dive Chart -->
					<SkillRadarChart 
						:title="__('Skill Deep Dive')"
						:data="skillsData"
						chartHeight="450px"
					/>
					
					<!-- Experience Distribution Chart -->
					<ExperienceDistributionChart 
						:title="__('Experience vs. Seniority')"
						:data="experienceData"
						chartHeight="450px"
					/>
				</div>
			</div>

			<!-- Readiness & Conversion Focus -->
			<div class="mb-8">
				<div class="mb-4">
					<h2 class="text-2xl font-bold text-gray-900">{{ __('Readiness & Conversion Focus') }}</h2>
					<p class="text-sm text-gray-600 mt-1">{{ __('Identify who needs to be contacted immediately') }}</p>
				</div>
				
				<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
					<!-- Recruitment Priority Matrix -->
					<RecruitmentPriorityBubbleChart 
						:title="__('Recruitment Priority Matrix')"
						:data="recruitmentPriorityData"
						chartHeight="450px"
					/>
					
					<!-- Salary Alignment -->
					<SalaryAlignmentDonutChart 
						:title="__('Salary Alignment')"
						:data="salaryAlignmentData"
						chartHeight="450px"
					/>
				</div>
			</div>

			<!-- Health & Nurturing Action -->
			<div class="mb-8">
				<div class="mb-4">
					<h2 class="text-2xl font-bold text-gray-900">{{ __('Health & Nurturing Action') }}</h2>
					<p class="text-sm text-gray-600 mt-1">{{ __('Manage daily CRM activities and talent engagement') }}</p>
				</div>
				
				<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
					<!-- Talent Requiring Update -->
					<TalentUpdateTable 
						:title="__('Talent Requiring Update')"
						:subtitle="__('Talents needing re-engagement (6+ months inactive)')"
						:data="talentUpdateData"
						tableHeight="450px"
						@contact-talent="handleContactTalent"
					/>
					
					<!-- Quality Source Analysis -->
					<QualitySourceBarChart 
						:title="__('Quality Source Analysis')"
						:data="qualitySourceData"
						chartHeight="450px"
					/>
				</div>
			</div>

			<!-- Action Buttons -->
			<div class="flex flex-wrap gap-3 mb-6">
				<Button variant="solid" theme="blue" @click="showCampaignWizard = true">
					<template #prefix>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
							stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
								d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" />
						</svg>
					</template>
					{{ __('Create Campaign') }}
				</Button>

				<Button variant="solid" theme="green" @click="showAddCandidateModal = true">
					<template #prefix>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
							stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
								d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
						</svg>
					</template>
					{{ __('Add Talent') }}
				</Button>

				<Button variant="solid" theme="gray" @click="showAnalytics = !showAnalytics">
					<template #prefix>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
							stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
								d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
						</svg>
					</template>
					{{ __('Analytics') }}
				</Button>
			</div>

			<!-- Analytics Section (Initially Hidden) -->
			<div v-if="showAnalytics" class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
				<div class="flex items-center justify-between mb-6">
					<h2 class="text-xl font-semibold text-gray-900">{{ __('Segment Analytics') }}</h2>
					<Button variant="ghost" theme="gray" @click="showAnalytics = false">
						<template #prefix>
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
								stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
									d="M6 18L18 6M6 6l12 12" />
							</svg>
						</template>
						{{ __('Close') }}
					</Button>
				</div>

				<!-- Chart placeholder -->
				<div class="bg-gray-50 rounded-lg border border-gray-200 p-8">
					<div class="text-center">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-300 mx-auto mb-4" fill="none"
							viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
								d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
						</svg>
						<h4 class="text-lg font-medium text-gray-600 mb-2">{{ __('Detailed Analysis') }}</h4>
						<p class="text-gray-500">
							{{ __('Analysis and detailed charts will be implemented here') }}
						</p>
					</div>
				</div>
			</div>

			<!-- Talents Section -->
			<div class="bg-white rounded-lg shadow-sm border border-gray-200">
				<div class="p-6">
					<div class="flex justify-between items-center mb-6">
						<h3 class="text-lg font-medium text-gray-900">
							{{ __('Talents in this segment') }}
						</h3>
						<div class="flex items-center space-x-3">
							<div class="relative">
								<input v-model="candidateSearch" type="text" :placeholder="__('Search by name...')"
									class="block w-80 pl-10 pr-8 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
									@input="handleSearchInput" />
								<div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
									<svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor"
										viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
											d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
									</svg>
								</div>

							</div>
							<Button variant="solid" theme="gray" @click="showAddCandidateModal = true">
								<template #prefix>
									<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none"
										viewBox="0 0 24 24" stroke="currentColor">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
											d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
									</svg>
								</template>
								{{ __('Add Talent') }}
							</Button>
						</div>
					</div>

					<!-- Talents Table -->
					<div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
						<table class="min-w-full divide-y divide-gray-300">
							<thead class="bg-gray-50">
								<tr>
									<th scope="col"
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										{{ __('Talent') }}
									</th>
									<th scope="col"
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										{{ __('Skills') }}
									</th>
									<th scope="col"
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										{{ __('Last Contact') }}
									</th>
									<th scope="col"
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										{{ __('Status') }}
									</th>
									<!-- <th scope="col"
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										{{ __('Added') }}
									</th> -->
									<th scope="col"
										class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
										{{ __('Match Score') }}
									</th>
									<th scope="col" class="relative px-6 py-3">
										<span class="">{{ __('Actions') }}</span>
									</th>
								</tr>
							</thead>
							<tbody class="bg-white divide-y divide-gray-200">
								<tr v-if="loadingCandidates">
									<td colspan="6" class="px-6 py-4 text-center text-gray-500">
										<div class="flex justify-center">
											<svg class="animate-spin h-5 w-5 text-blue-500"
												xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
												<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
													stroke-width="4"></circle>
												<path class="opacity-75" fill="currentColor"
													d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
												</path>
											</svg>
										</div>
									</td>
								</tr>
								<tr v-else-if="filteredCandidates.length === 0">
									<td colspan="6" class="px-6 py-4 text-center text-gray-500">
										{{ __('No talents found') }}
									</td>
								</tr>
								<tr v-else v-for="candidate in filteredCandidates" :key="candidate.name"
									class="hover:bg-gray-50">
									<td class="px-6 py-4 whitespace-nowrap">
										<div class="flex items-center">
											<div class="flex-shrink-0 h-8 w-8">
												<div
													class="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center">
													<span class="text-xs font-medium text-white">{{
														candidate.full_name?.charAt(0) || '?'
													}}</span>
												</div>
											</div>
											<div class="ml-3">
												<div class="text-sm font-medium text-gray-900">
													{{ candidate.full_name }}
												</div>
												<div class="text-sm text-gray-500">
													{{ candidate.email }}
												</div>
											</div>
										</div>
									</td>
									<td class="px-6 py-4">
										<div class="flex flex-wrap gap-1">
											<template v-if="Array.isArray(candidate.skills) && candidate.skills.length > 0">
												<span v-for="skill in candidate.skills.slice(0, 4)"
													:key="skill"
													class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
													{{ skill }}
												</span>
												<span v-if="candidate.skills.length > 4"
													class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
													+{{ candidate.skills.length - 4 }}
												</span>
											</template>
											<span v-else class="text-sm text-gray-400">No skills</span>
										</div>
									</td>
									<!-- <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
										{{ formatDateTime(candidate.last_interaction) }}
									</td> -->
									<td class="px-6 py-4 whitespace-nowrap">
										<span :class="getStatusBadgeClass(candidate.status)"
											class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
											{{ candidate.status }}
										</span>
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
										{{ formatDateTime(candidate.added_at) }}
									</td>

									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
										<span :class="getEngagementColor(candidate.match_score)"
											class="font-bold text-center flex items-center justify-center">
											{{ candidate.match_score || 0 }}%
											<!-- {{ console.log(candidate) }} -->
										</span>
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
										<div class="flex items-center space-x-2">
											<Button variant="ghost" theme="gray" size="sm"
												@click="viewCandidateDetails(candidate)">
												<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none"
													viewBox="0 0 24 24" stroke="currentColor">
													<path stroke-linecap="round" stroke-linejoin="round"
														stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
													<path stroke-linecap="round" stroke-linejoin="round"
														stroke-width="2"
														d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
												</svg>
											</Button>
											<Button variant="ghost" theme="blue" size="sm"
												@click="contactCandidate(candidate)">
												<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none"
													viewBox="0 0 24 24" stroke="currentColor">
													<path stroke-linecap="round" stroke-linejoin="round"
														stroke-width="2"
														d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 012 2z" />
												</svg>
											</Button>
											<Button variant="ghost" theme="red" size="sm"
												@click="removeFromSegment(candidate)">
												<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none"
													viewBox="0 0 24 24" stroke="currentColor">
													<path stroke-linecap="round" stroke-linejoin="round"
														stroke-width="2"
														d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
												</svg>
											</Button>
										</div>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>
			</div>
		</div>

		<!-- Add Candidate Modal -->
		<Dialog v-model="showAddCandidateModal" :options="addCandidateDialogOptions">
			<template #body>
				<div class="bg-white px-6 py-6">
					<div class="mb-6 flex items-center justify-between">
						<div>
							<h3 class="text-xl font-semibold leading-6 text-gray-900">
								{{ __('Add Talents to Pool') }}
							</h3>
							<p class="mt-1 text-sm text-gray-500">
								{{ __('Select talents to add to') }} "{{ talentSegment.title }}"
							</p>
						</div>
						<div class="flex items-center gap-1">
							<Button variant="ghost" class="w-7" @click="closeAddCandidateModal">
								<FeatherIcon name="x" class="h-4 w-4" />
							</Button>
						</div>
					</div>

					<div class="space-y-6">
						<!-- Min Score Slider -->
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-3">
								{{ __('Minimum Match Score') }}: {{ minScore }}%
							</label>
							<div class="flex justify-between text-xs text-gray-500 mt-1">
								<span>0%</span>
								<span>50%</span>
								<span>100%</span>
							</div>
							<div class="slider-wrapper">
								<div class="progress-track" :style="{ '--progress': minScore + '%' }"></div>
								<input v-model="minScore" type="range" min="0" max="100" step="5" class="slider"
									@input="handleMinScoreChange" />
							</div>
							<p class="text-xs text-gray-500 mt-5">
								{{ __('Higher score means better skill match with segment criteria') }}
							</p>
						</div>

						<!-- Find Matches Button -->
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-3">
								{{ __('Find Matching Talents') }}
							</label>
							<div class="flex gap-2">
								<Button variant="solid" theme="gray" :loading="loadingSuggestedCandidates"
									@click="loadSuggestedCandidates">
									{{ __('Find Matches') }}
								</Button>
							</div>
						</div>

						<!-- Loading state -->
						<div v-if="loadingSuggestedCandidates"
							class="flex items-center justify-center p-8 border-2 border-dashed border-gray-300 rounded-lg">
							<div class="text-center">
								<svg class="animate-spin h-8 w-8 text-gray-500 mx-auto mb-2"
									xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
									<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
										stroke-width="4"></circle>
									<path class="opacity-75" fill="currentColor"
										d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
									</path>
								</svg>
								<p class="text-sm text-gray-500">
									{{ __('Finding matching talents...') }}
								</p>
							</div>
						</div>

						<!-- Talents List -->
						<div v-else-if="suggestedCandidates.length > 0" class="space-y-4">
							<div class="flex items-center justify-between">
								<h4 class="text-sm font-medium text-gray-900">
									{{ __('Suggested Talents') }} ({{ suggestedCandidates.length }})
								</h4>
								<div class="flex items-center gap-2">
									<Button variant="ghost" theme="gray" size="sm" @click="selectAllCandidates">
										{{ __('Select All') }}
									</Button>
									<Button variant="ghost" theme="gray" size="sm" @click="deselectAllCandidates">
										{{ __('Deselect All') }}
									</Button>
								</div>
							</div>

							<div class="max-h-96 overflow-y-auto border border-gray-200 rounded-lg">
								<div v-for="candidate in filteredSuggestedCandidates" :key="candidate.name"
									class="flex items-center p-4 border-b border-gray-100 hover:bg-gray-50">
									<div class="flex items-center flex-1">
										<input :value="candidate.name" type="checkbox"
											:checked="selectedCandidates.includes(candidate.name)"
											@change="toggleCandidateSelection(candidate.name)"
											class="h-4 w-4 text-gray-600 focus:ring-gray-500 border-gray-300 rounded" />
										<div class="ml-3 flex-1">
											<div class="flex items-center justify-between">
												<div>
													<div class="text-sm font-medium text-gray-900">
														{{ candidate.full_name || candidate.name }}
													</div>
													<div class="text-sm text-gray-500">
														{{ candidate.email }}
													</div>
												</div>
												<div class="flex items-center gap-2">
													<span
														class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
														<span :class="getEngagementColor(candidate.score)">
															{{ candidate.score }}%
														</span>

													</span>
												</div>
											</div>
											<div v-if="candidate.skills && processSkills(candidate.skills).length > 0" class="mt-2">
												<div class="flex flex-wrap gap-1">
													<span v-for="skill in processSkills(candidate.skills).slice(0, 3)"
														:key="skill"
														class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
														{{ skill }}
													</span>
													<span v-if="processSkills(candidate.skills).length > 3"
														class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-600">
														+{{ processSkills(candidate.skills).length - 3 }} {{ __('more') }}
													</span>
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>

						<!-- No candidates found -->
						<div v-else-if="!loadingSuggestedCandidates && suggestedCandidates.length === 0"
							class="text-center p-8 border-2 border-dashed border-gray-300 rounded-lg">
							<svg class="h-12 w-12 text-gray-400 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg"
								fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
									d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
							</svg>
							<h4 class="text-lg font-medium text-gray-600 mb-2">{{ __('No talents found') }}</h4>
							<p class="text-gray-500">
								{{ __('Try adjusting the minimum score or search criteria') }}
							</p>
						</div>

						<!-- Selected Talents Summary -->
						<div class="border border-gray-200 rounded-lg p-4 bg-gray-50">
							<div class="flex items-center justify-between">
								<div>
									<h4 class="text-sm font-medium text-gray-900">
										{{ __('Selected Talents') }} ({{ selectedCandidates.length }})
									</h4>
									<p class="text-sm text-gray-700 mt-1">
										{{ __('Ready to add to pool') }}
									</p>
								</div>
								<Button variant="ghost" theme="gray" size="sm" @click="deselectAllCandidates">
									{{ __('Clear All') }}
								</Button>
							</div>
						</div>
					</div>
				</div>
				<div class="flex justify-end space-x-3 px-6 py-4 bg-gray-50">
					<Button variant="outline" theme="gray" :disabled="savingCandidates" @click="closeAddCandidateModal">
						{{ __('Cancel') }}
					</Button>
					<Button variant="solid" theme="gray" :loading="savingCandidates"
						:disabled="selectedCandidates.length === 0 || savingCandidates" @click="addSelectedCandidatesToSegment">
						<template #prefix>
							<FeatherIcon name="user-plus" class="h-4 w-4" />
						</template>
						{{ savingCandidates ? __('Adding...') : __('Add Selected to pool') }}
					</Button>
				</div>
			</template>
		</Dialog>

		<!-- Campaign Wizard -->
		<CampaignWizard v-model="showCampaignWizard" :preselected-segment="route.params.id"
			@success="handleCampaignCreated" />

		<!-- Edit Talent Pool Dialog -->
		<TalentPoolDialog 
			v-model="showEditTalentSegmentModal" 
			:segment="editingSegmentData"
			@success="handleTalentSegmentUpdated"
			@cancel="handleEditModalClose"
		/>
	</div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { call } from 'frappe-ui'
import { useCampaignStore } from '@/stores/campaign'
import { useCandidateStore } from '@/stores/candidate'
import { useTalentSegmentStore } from '@/stores/talentSegment'
import { useMiraTalentPoolStore } from '@/stores/miraTalentPool'
import { usersStore } from '@/stores/users'
import { Button, Dialog, Breadcrumbs, FeatherIcon } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import CampaignWizard from '@/components/campaign/CampaignWizard.vue'
import TalentPoolDialog from '@/components/talent-segment/TalentPoolDialog.vue'
import SkillRadarChart from '@/components/charts/SkillRadarChart.vue'
import ExperienceDistributionChart from '@/components/charts/ExperienceDistributionChart.vue'
import RecruitmentPriorityBubbleChart from '@/components/charts/RecruitmentPriorityBubbleChart.vue'
import SalaryAlignmentDonutChart from '@/components/charts/SalaryAlignmentDonutChart.vue'
import TalentUpdateTable from '@/components/charts/TalentUpdateTable.vue'
import QualitySourceBarChart from '@/components/charts/QualitySourceBarChart.vue'
import { processSkills } from '@/stores/candidate'
import moment from 'moment'



// Store initialization
const campaignStore = useCampaignStore()
const candidateStore = useCandidateStore()
const talentSegmentStore = useTalentSegmentStore()
const miraTalentPoolStore = useMiraTalentPoolStore()
const { getUser } = usersStore()
const route = useRoute()
const router = useRouter()

// Breadcrumbs
const breadcrumbs = computed(() => {
	console.log('Breadcrumbs computed, route params:', route.params)
	return [
		{ label: __('Talent Pools'), route: { name: 'SegmentPool' } },
		{ label: talentSegment.title || __('Loading...'), route: { name: 'TalentSegmentDetail' } },
	]
})

// State

const loading = ref(false)
const loadingCandidates = ref(false)
const loadingCampaigns = ref(false)

// Data
const talentSegment = reactive({})
const candidates = ref([])
const relatedCampaigns = ref([])

// Chart data - Fake data for demonstration
const skillsData = ref([
	{ name: 'Python', value: 85 },
	{ name: 'Machine Learning', value: 72 },
	{ name: 'Data Analysis', value: 90 },
	{ name: 'SQL', value: 78 },
	{ name: 'Deep Learning', value: 65 },
	{ name: 'NLP', value: 58 },
	{ name: 'TensorFlow', value: 70 },
	{ name: 'PyTorch', value: 62 }
])

const experienceData = ref([
	{ name: '0-2 years', value: 15 },
	{ name: '3-5 years', value: 28 },
	{ name: '6-10 years', value: 35 },
	{ name: '11-15 years', value: 18 },
	{ name: '15+ years', value: 12 }
])

// Recruitment Priority Matrix data - Bubble Chart
const recruitmentPriorityData = ref([
	{ 
		name: 'High Priority', 
		value: [7, 2, 42], // [timeline_days, readiness_index, talent_count]
		readinessLabel: 'High',
		timelineLabel: '0-10 days',
		color: '#10B981' // Green
	},
	{ 
		name: 'Quick Win', 
		value: [15, 2, 28], 
		readinessLabel: 'High',
		timelineLabel: '11-20 days',
		color: '#34D399'
	},
	{ 
		name: 'Medium Priority', 
		value: [30, 1, 35], 
		readinessLabel: 'Medium',
		timelineLabel: '21-40 days',
		color: '#FBBF24' // Yellow
	},
	{ 
		name: 'Consider', 
		value: [45, 1, 22], 
		readinessLabel: 'Medium',
		timelineLabel: '41-60 days',
		color: '#FCD34D'
	},
	{ 
		name: 'Low Priority', 
		value: [60, 0, 18], 
		readinessLabel: 'Low',
		timelineLabel: '61-80 days',
		color: '#F87171' // Red
	},
	{ 
		name: 'Long Term', 
		value: [75, 0, 12], 
		readinessLabel: 'Low',
		timelineLabel: '80+ days',
		color: '#EF4444'
	}
])

// Salary Alignment data - Donut Chart
const salaryAlignmentData = ref([
	{ 
		name: 'In-Budget', 
		value: 58,
		color: '#10B981' // Green - phù hợp ngân sách
	},
	{ 
		name: 'Slightly Over-Budget', 
		value: 28,
		color: '#FBBF24' // Yellow - vượt ngân sách một chút
	},
	{ 
		name: 'Under-Budget', 
		value: 14,
		color: '#3B82F6' // Blue - dưới ngân sách
	}
])

// Talent Requiring Update data - Table
const talentUpdateData = ref([
	{
		name: 'Nguyen Van A',
		title: 'Senior Data Scientist',
		lastInteraction: '2023-12-15',
		daysSince: 328,
		status: 'Passive',
		source: 'LinkedIn'
	},
	{
		name: 'Tran Thi B',
		title: 'ML Engineer',
		lastInteraction: '2024-01-20',
		daysSince: 292,
		status: 'Interested',
		source: 'Referral'
	},
	{
		name: 'Le Van C',
		title: 'Data Analyst',
		lastInteraction: '2023-11-10',
		daysSince: 363,
		status: 'Considering',
		source: 'Headhunter'
	},
	{
		name: 'Pham Thi D',
		title: 'Python Developer',
		lastInteraction: '2024-02-05',
		daysSince: 276,
		status: 'Passive',
		source: 'LinkedIn'
	},
	{
		name: 'Hoang Van E',
		title: 'AI Engineer',
		lastInteraction: '2023-10-25',
		daysSince: 379,
		status: 'Inactive',
		source: 'Career Fair'
	},
	{
		name: 'Vu Thi F',
		title: 'Data Engineer',
		lastInteraction: '2024-01-08',
		daysSince: 304,
		status: 'Passive',
		source: 'LinkedIn'
	}
])

// Quality Source Analysis data - Bar Chart
const qualitySourceData = ref([
	{
		name: 'Referral',
		value: 78,
		totalTalents: 45,
		color: '#10B981',
		colorEnd: '#34D399'
	},
	{
		name: 'Headhunter',
		value: 65,
		totalTalents: 38,
		color: '#3B82F6',
		colorEnd: '#60A5FA'
	},
	{
		name: 'LinkedIn',
		value: 52,
		totalTalents: 67,
		color: '#8B5CF6',
		colorEnd: '#A78BFA'
	},
	{
		name: 'Career Fair',
		value: 45,
		totalTalents: 28,
		color: '#F59E0B',
		colorEnd: '#FBBF24'
	},
	{
		name: 'Job Board',
		value: 38,
		totalTalents: 52,
		color: '#EF4444',
		colorEnd: '#F87171'
	}
])

// Modals
const showAddCandidateModal = ref(false)
const showCampaignWizard = ref(false)
const showEditTalentSegmentModal = ref(false)
const editingSegmentData = ref(null)
const savingCandidates = ref(false)
const showAnalytics = ref(false)

// Search and filtering
const candidateSearch = ref('')
const minScore = ref(50)
const suggestedCandidates = ref([])
const selectedCandidates = ref([])
const loadingSuggestedCandidates = ref(false)

// Computed
const filteredCandidates = computed(() => {
	// For now, just return all candidates since we removed the search functionality
	// from the main candidates table
	return candidates.value
})

const filteredSuggestedCandidates = computed(() => {
	// No longer filtering by search since we removed the search input
	return suggestedCandidates.value
})

// Dialog options
const addCandidateDialogOptions = computed(() => ({
	title: __('Add Talents to Segment'),
	size: '3xl',
}))

// Dialog options - No longer needed, TalentPoolDialog handles its own options



// Watch modal state to clear data when modal opens
watch(showAddCandidateModal, (newValue) => {
	if (newValue) {
		console.log('Modal opened, clearing previous data...')
		// Clear previous data when modal opens
		suggestedCandidates.value = []
		selectedCandidates.value = []
		minScore.value = 50
	}
})

// Watch edit modal state and data
watch(showEditTalentSegmentModal, (newValue) => {
	console.log('Edit modal state changed:', newValue)
	if (newValue) {
		console.log('Edit modal opened with data:', editingSegmentData.value)
	}
})

watch(editingSegmentData, (newValue) => {
	console.log('editingSegmentData changed:', newValue)
}, { deep: true })

// Methods
const handleSearchInput = (event) => {
	console.log('Search input event:', event.target.value)
	// Currently disabled - search functionality removed from main table
}

const handleMinScoreChange = () => {
	console.log('Min score changed to:', minScore.value)
	// No longer auto-reload when score changes - user must click "Find Matches"
}

const loadSuggestedCandidates = async () => {
	loadingSuggestedCandidates.value = true
	try {
		console.log('Loading suggested candidates with min score:', minScore.value)
		const result = await call('mbw_mira.mbw_mira.doctype.mira_segment.mira_segment.find_talentprofile_by_segment', {
			segment_id: route.params.id,
			min_score: minScore.value
		})

		if (result && result.length) {
			suggestedCandidates.value = result
			console.log('Loaded suggested candidates:', result.length)
		} else {
			console.error('Failed to load suggested candidates:', result?.error)
			suggestedCandidates.value = []
		}
	} catch (error) {
		console.error('Error loading suggested candidates:', error)
		suggestedCandidates.value = []
	} finally {
		loadingSuggestedCandidates.value = false
	}
}

const toggleCandidateSelection = (candidateId) => {
	const index = selectedCandidates.value.indexOf(candidateId)
	if (index > -1) {
		selectedCandidates.value.splice(index, 1)
	} else {
		selectedCandidates.value.push(candidateId)
	}
	console.log('Selected candidates:', selectedCandidates.value)
}

const selectAllCandidates = () => {
	selectedCandidates.value = filteredSuggestedCandidates.value.map(c => c.name)
	console.log('Selected all candidates:', selectedCandidates.value.length)
}

const deselectAllCandidates = () => {
	selectedCandidates.value = []
	console.log('Deselected all candidates')
}

const addSelectedCandidatesToSegment = async () => {
	// Prevent double execution
	if (selectedCandidates.value.length === 0 || savingCandidates.value) {
		console.log('Skipping - already saving or no candidates selected')
		return
	}

	console.log('Adding selected candidates to segment:', selectedCandidates.value)
	console.log('Suggested candidates:', suggestedCandidates.value)
	savingCandidates.value = true

	try {
		// Prepare data for bulk insert - convert to plain array to avoid proxy issues
		const candidateIds = [...selectedCandidates.value]
		console.log('Candidate IDs to add:', candidateIds, 'Length:', candidateIds.length)
		
		const segmentData = candidateIds.map(candidateId => ({
			talent_id: candidateId,
			segment_id: route.params.id,
			added_at: moment().format('YYYY-MM-DD HH:mm:ss'),
			added_by: getUser()?.name || 'Administrator',
			match_score: suggestedCandidates.value.find(c => c.name === candidateId)?.score || 0
		}))

		console.log('Bulk insert data:', segmentData, 'Length:', segmentData.length)

		const result = await miraTalentPoolStore.bulkInsertTalents(segmentData)

		console.log('Bulk insert result:', result)

		if (result && result.status === 'completed') {
			console.log('Bulk insert successful:', result)

			// Show success message
			const successCount = result.summary?.success || 0
			const duplicateCount = result.summary?.duplicate || 0
			const failCount = result.summary?.fail || 0

			console.log(`Successfully added ${successCount} candidates, ${duplicateCount} duplicates, ${failCount} failed`)

			// Close modal and reload data
			closeAddCandidateModal()
			await loadCandidates()
			await loadTalentSegment()
		} else {
			console.error('Failed to bulk insert candidates:', result)
		}
	} catch (error) {
		console.error('Error adding candidates:', error)
	} finally {
		savingCandidates.value = false
	}
}

// Utility functions using moment.js
const formatDate = (dateString) => {
	if (!dateString) return 'N/A'
	return moment(dateString).format('MMM DD, YYYY')
}

const formatDateTime = (dateString) => {
	if (!dateString) return 'N/A'
	return moment(dateString).format('MMM DD, YYYY HH:mm')
}

const getStatusBadgeClass = (status) => {
	const statusClasses = {
		'ACTIVE': 'bg-gray-100 text-gray-800',
		'INACTIVE': 'bg-gray-100 text-gray-800',
		'PENDING': 'bg-gray-100 text-gray-800',
		'CONTACTED': 'bg-gray-100 text-gray-800',
		'REJECTED': 'bg-gray-100 text-gray-800',
	}
	return statusClasses[status] || 'bg-gray-100 text-gray-800'
}

const loadTalentSegment = async () => {
	loading.value = true
	console.log('loadTalentSegment called with ID:', route.params.id)
	try {
		const result = await talentSegmentStore.fetchTalentSegmentById(route.params.id)
		console.log('Talent segment API result:', result)
		if (result && result.name) {
			Object.assign(talentSegment, result)
			console.log('Talent segment data assigned:', talentSegment)
		} else {
			console.error('Failed to load talent segment:', result?.error)
		}
	} catch (error) {
		console.error('Error loading talent segment:', error)
	} finally {
		loading.value = false
	}
}

const loadCandidates = async () => {
	loadingCandidates.value = true
	console.log('loadCandidates called with segment ID:', route.params.id)
	try {
		// First, get all Mira Talent Pool records for this segment
		console.log('Fetching candidate segments...')
		const candidateSegmentResult = await call('frappe.client.get_list', {
			doctype: 'Mira Talent Pool',
			filters: { segment_id: route.params.id },
			fields: ['name', 'talent_id', 'added_at', 'added_by', 'match_score'],
		})
		console.log('Mira Talent Pool API result:', candidateSegmentResult)

		if (candidateSegmentResult && candidateSegmentResult.length > 0) {
			// Get candidate IDs from the relationship
			const candidateIds = candidateSegmentResult.map((cs) => cs.talent_id)
			console.log('Mira Talent Pool records found:', candidateSegmentResult)
			console.log('Extracted talent_ids:', candidateIds)

			// Then get the actual candidate data using universal service
			const candidateResult = await candidateStore.fetchCandidates({
				filters: { name: ['in', candidateIds] },
				limit: 1000,
				fields: ['name', 'full_name', 'email', 'phone', 'skills']
			})
			console.log('Mira Contact API result:>>>>>>>>>>>>>>>>>:  ', candidateResult)

			if (candidateResult && candidateResult.data && candidateResult.data.length) {
				// Merge the data - add segment relationship info to candidate data
				candidates.value = candidateResult.data.map((candidate) => {
					const segmentRelation = candidateSegmentResult.find(
						(cs) => cs.talent_id === candidate.name,
					)
					// Process skills to ensure it's an array
				console.log('Raw skills for', candidate.full_name, ':', candidate.skills, 'Type:', typeof candidate.skills)
				const processedSkills = processSkills(candidate.skills)
				console.log('Processed skills:', processedSkills, 'Type:', typeof processedSkills, 'IsArray:', Array.isArray(processedSkills))
				
				return {
					...candidate,
					skills: processedSkills, // Override with processed skills
						added_at: segmentRelation?.added_at,
						added_by: segmentRelation?.added_by,
						candidate_segment_id: segmentRelation?.name,
						match_score: segmentRelation?.match_score
					}
				})
				console.log('Loaded candidates:', candidates.value.length, candidates.value)
			}
		} else {
			candidates.value = []
			console.log('No candidates found for this segment')
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
		const candidateSegmentResult = await call('frappe.client.get_list', {
			doctype: 'Mira Talent Pool',
			filters: { segment_id: route.params.id },
			fields: ['talent_id'],
		})

		if (candidateSegmentResult && candidateSegmentResult.length > 0) {
			const candidateIds = candidateSegmentResult.map((cs) => cs.talent_id)

			// Then get campaigns that have these candidates through Mira Talent Campaign
			const candidateCampaignResult = await call('frappe.client.get_list', {
				doctype: 'Mira Talent Campaign',
				filters: { talent_id: ['in', candidateIds] },
				fields: ['campaign_id'],
			})

			if (candidateCampaignResult && candidateCampaignResult.length > 0) {
				const campaignIds = [
					...new Set(candidateCampaignResult.map((cc) => cc.campaign_id)),
				]

				// Get the actual campaign data
				const campaignResult = await campaignStore.fetchCampaigns({
					limit: 1000,
					page: 1
				})

				if (campaignResult && campaignResult.data) {
					// Filter campaigns by the campaignIds we need
					const filteredCampaigns = campaignResult.data.filter(campaign => 
						campaignIds.includes(campaign.name)
					)
					relatedCampaigns.value = filteredCampaigns
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



const closeAddCandidateModal = () => {
	showAddCandidateModal.value = false
	selectedCandidates.value = []
	suggestedCandidates.value = []
	minScore.value = 50
	console.log('Modal closed, cleared candidate data')
}



const viewCandidateDetails = (candidate) => {
	router.push(`/talents/${candidate.name}`)
}

const contactCandidate = (candidate) => {
	// Implementation for contacting candidate
	console.log('Contact candidate:', candidate)
}

const removeFromSegment = async (candidate) => {
	if (confirm('Are you sure you want to remove this candidate from the segment?')) {
		try {
			// Delete the Mira Talent Pool relationship
			if (candidate.candidate_segment_id) {
				const result = await miraTalentPoolStore.delete(candidate.candidate_segment_id)
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



// Additional methods
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

const handleEditModalClose = () => {
	showEditTalentSegmentModal.value = false
}

const openEditModal = () => {
	// Set the current talent segment data to the editing variable
	editingSegmentData.value = JSON.parse(JSON.stringify(talentSegment))
	console.log('Opening edit modal with data:', editingSegmentData.value)
	console.log('Original talentSegment:', talentSegment)
	showEditTalentSegmentModal.value = true
}

const handleContactTalent = (talent) => {
	console.log('Contact talent:', talent)
	// TODO: Implement contact talent functionality
	// This could open a modal, navigate to talent detail, or trigger an email/call action
	alert(`Contacting ${talent.name}...`)
}

// Lifecycle
onMounted(async () => {
	console.log('=== TalentSegmentDetailView mounted ===')
	console.log('Route params:', route.params)
	console.log('Route path:', route.path)
	console.log('Route name:', route.name)

	try {
		console.log('Loading talent segment...')
		await loadTalentSegment()
		console.log('Loading candidates...')
		await loadCandidates()
		console.log('Loading related campaigns...')
		await loadRelatedCampaigns()
		console.log('=== All data loaded successfully ===')
	} catch (error) {
		console.error('Error in onMounted:', error)
	}
})

const getEngagementColor = (score) => {
	return score >= 80 ? 'text-green-500' : score >= 60 ? 'text-yellow-500' : 'text-red-500'
}
</script>

<style scoped>
.talent-segment-detail-view {
	max-width: 1200px;
	margin: 0 auto;
	padding: 20px;
}

/* Custom slider styles */
/* Wrapper để chứa slider và background gradient */
.slider-wrapper {
	position: relative;
	width: 100%;
	height: 8px;
	margin-bottom: 4px;
}

/* Progress track */
.progress-track {
	position: absolute;
	top: 0;
	left: 0;
	height: 8px;
	border-radius: 4px;
	background: linear-gradient(to right, #3b82f6 var(--progress), #e5e7eb var(--progress));
	width: 100%;
	z-index: 1;
}

/* Custom slider styles */
.slider {
	-webkit-appearance: none;
	appearance: none;
	width: 100%;
	height: 8px;
	background: transparent;
	cursor: pointer;
	position: relative;
	z-index: 2;
}

/* Track styles với gradient background */
.slider::-webkit-slider-track {
	height: 8px;
	border-radius: 4px;
	background: transparent;
}

.slider::-moz-range-track {
	height: 8px;
	border-radius: 4px;
	background: transparent;
}

/* Thumb styles với màu động */
.slider::-webkit-slider-thumb {
	-webkit-appearance: none;
	appearance: none;
	height: 20px;
	width: 20px;
	border-radius: 50%;
	background: #3b82f6;
	cursor: pointer;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
	transition: all 0.2s ease;
}

.slider::-moz-range-thumb {
	height: 20px;
	width: 20px;
	border-radius: 50%;
	background: #3b82f6;
	cursor: pointer;
	border: none;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
	transition: all 0.2s ease;
}

/* Hover effects */
.slider::-webkit-slider-thumb:hover {
	transform: scale(1.1);
	background: #2563eb;
}

.slider::-moz-range-thumb:hover {
	transform: scale(1.1);
	background: #2563eb;
}
</style>
