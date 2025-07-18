<template>
	<div class="min-h-screen bg-gray-50">
		<LayoutHeader>
			<template #left-header>
				<Breadcrumbs :items="breadcrumbs" />
			</template>
			<template #right-header>
				<Button variant="outline" theme="gray" @click="showEditTalentSegmentModal = true">
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
							{{ __('Edit Pool') }}
						</Button>
						<Button variant="outline" theme="red" @click="$router.push('/talent-segments')">
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
										d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
									/>
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
									class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
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
				<div
					class="bg-gradient-to-r from-blue-50 to-blue-100 p-6 rounded-lg border border-blue-200"
				>
					<div class="flex items-center">
						<div class="flex-shrink-0">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-8 w-8 text-blue-600"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
								/>
							</svg>
						</div>
						<div class="ml-4">
							<div class="text-2xl font-bold text-blue-900">
								{{ talentSegment.candidate_count || 0 }}
							</div>
							<div class="text-sm text-blue-700">{{ __('Total Candidates') }}</div>
						</div>
					</div>
				</div>
				<div
					class="bg-gradient-to-r from-green-50 to-green-100 p-6 rounded-lg border border-green-200"
				>
					<div class="flex items-center">
						<div class="flex-shrink-0">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-8 w-8 text-green-600"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
								/>
							</svg>
						</div>
						<div class="ml-4">
							<div class="text-2xl font-bold text-green-900">
								{{ candidates.filter(c => c.status === 'ACTIVE').length }}
							</div>
							<div class="text-sm text-green-700">{{ __('Active Candidates') }}</div>
						</div>
					</div>
				</div>
				<div
					class="bg-gradient-to-r from-yellow-50 to-yellow-100 p-6 rounded-lg border border-yellow-200"
				>
					<div class="flex items-center">
						<div class="flex-shrink-0">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-8 w-8 text-yellow-600"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a1 1 0 011-1h1m-1 4h10m0-4V5a1 1 0 011-1h1m-4 0h.01"
								/>
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
				<div
					class="bg-gradient-to-r from-purple-50 to-purple-100 p-6 rounded-lg border border-purple-200"
				>
					<div class="flex items-center">
						<div class="flex-shrink-0">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-8 w-8 text-purple-600"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
								/>
							</svg>
						</div>
						<div class="ml-4">
							<div class="text-2xl font-bold text-purple-900">
								{{ candidates.length > 0 ? Math.round((candidates.filter(c => c.status === 'ACTIVE').length / candidates.length) * 100) : 0 }}%
							</div>
							<div class="text-sm text-purple-700">{{ __('Interaction Rate') }}</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Action Buttons -->
			<div class="flex flex-wrap gap-3 mb-6">
				<Button variant="solid" theme="blue" @click="showCampaignWizard = true">
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
								d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z"
							/>
						</svg>
					</template>
					{{ __('Create Campaign') }}
				</Button>

				<Button variant="solid" theme="green" @click="showAddCandidateModal = true">
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
								d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
							/>
						</svg>
					</template>
					{{ __('Add Candidate') }}
				</Button>

				<Button variant="solid" theme="gray" @click="showAnalytics = !showAnalytics">
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
								d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
							/>
						</svg>
					</template>
					{{ __('Analytics') }}
				</Button>
			</div>

			<!-- Analytics Section (Initially Hidden) -->
			<div
				v-if="showAnalytics"
				class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6"
			>
				<div class="flex items-center justify-between mb-6">
					<h2 class="text-xl font-semibold text-gray-900">{{ __('Segment Analytics') }}</h2>
					<Button variant="ghost" theme="gray" @click="showAnalytics = false">
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
									d="M6 18L18 6M6 6l12 12"
								/>
							</svg>
						</template>
						{{ __('Close') }}
					</Button>
				</div>

				<!-- Chart placeholder -->
				<div class="bg-gray-50 rounded-lg border border-gray-200 p-8">
					<div class="text-center">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-16 w-16 text-gray-300 mx-auto mb-4"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="1"
								d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
							/>
						</svg>
						<h4 class="text-lg font-medium text-gray-600 mb-2">{{ __('Detailed Analysis') }}</h4>
						<p class="text-gray-500">
							{{ __('Analysis and detailed charts will be implemented here') }}
						</p>
					</div>
				</div>
			</div>

			<!-- Candidates Section -->
			<div class="bg-white rounded-lg shadow-sm border border-gray-200">
				<div class="p-6">
					<div class="flex justify-between items-center mb-6">
						<h3 class="text-lg font-medium text-gray-900">
							{{ __('Candidates in this segment') }}
						</h3>
						<div class="flex items-center space-x-3">
							<div class="relative">
								<input
									v-model="candidateSearch"
									type="text"
									:placeholder="__('Search by name...')"
									class="block w-80 pl-10 pr-8 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
									@input="handleSearchInput"
								/>
								<div
									class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
								>
									<svg
										class="h-5 w-5 text-gray-400"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
										></path>
									</svg>
								</div>
								<!-- Search loading indicator -->
								<div
									v-if="searchLoading"
									class="absolute inset-y-0 right-0 pr-3 flex items-center"
								>
									<svg
										class="animate-spin h-4 w-4 text-blue-500"
										xmlns="http://www.w3.org/2000/svg"
										fill="none"
										viewBox="0 0 24 24"
									>
										<circle
											class="opacity-25"
											cx="12"
											cy="12"
											r="10"
											stroke="currentColor"
											stroke-width="4"
										></circle>
										<path
											class="opacity-75"
											fill="currentColor"
											d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
										></path>
									</svg>
								</div>
							</div>
							<Button variant="solid" theme="gray" @click="showAddCandidateModal = true">
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
											d="M12 6v6m0 0v6m0-6h6m-6 0H6"
										/>
									</svg>
								</template>
								{{ __('Add Candidate') }}
							</Button>
						</div>
					</div>

					<!-- Candidates Table -->
					<div
						class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg"
					>
						<table class="min-w-full divide-y divide-gray-300">
							<thead class="bg-gray-50">
								<tr>
									<th
										scope="col"
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										{{ __('Candidate') }}
									</th>
									<th
										scope="col"
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										{{ __('Skills') }}
									</th>
									<th
										scope="col"
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										{{ __('Last Contact') }}
									</th>
									<th
										scope="col"
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										{{ __('Status') }}
									</th>
									<th
										scope="col"
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										{{ __('Added') }}
									</th>
									<th scope="col" class="relative px-6 py-3">
										<span class="sr-only">{{ __('Actions') }}</span>
									</th>
								</tr>
							</thead>
							<tbody class="bg-white divide-y divide-gray-200">
								<tr v-if="loadingCandidates">
									<td colspan="6" class="px-6 py-4 text-center text-gray-500">
										<div class="flex justify-center">
											<svg
												class="animate-spin h-5 w-5 text-blue-500"
												xmlns="http://www.w3.org/2000/svg"
												fill="none"
												viewBox="0 0 24 24"
											>
												<circle
													class="opacity-25"
													cx="12"
													cy="12"
													r="10"
													stroke="currentColor"
													stroke-width="4"
												></circle>
												<path
													class="opacity-75"
													fill="currentColor"
													d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
												></path>
											</svg>
										</div>
									</td>
								</tr>
								<tr v-else-if="filteredCandidates.length === 0">
									<td colspan="6" class="px-6 py-4 text-center text-gray-500">
										{{ __('No candidates found') }}
									</td>
								</tr>
								<tr
									v-else
									v-for="candidate in filteredCandidates"
									:key="candidate.name"
									class="hover:bg-gray-50"
								>
									<td class="px-6 py-4 whitespace-nowrap">
										<div class="flex items-center">
											<div class="flex-shrink-0 h-8 w-8">
												<div
													class="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center"
												>
													<span class="text-xs font-medium text-white">{{
														candidate.candidate_name?.charAt(0) || '?'
													}}</span>
												</div>
											</div>
											<div class="ml-3">
												<div class="text-sm font-medium text-gray-900">
													{{ candidate.candidate_name }}
												</div>
												<div class="text-sm text-gray-500">
													{{ candidate.email }}
												</div>
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
										<span
											:class="getStatusBadgeClass(candidate.status)"
											class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
										>
											{{ candidate.status }}
										</span>
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
										{{ formatDateTime(candidate.added_at) }}
									</td>
									<td
										class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
									>
										<div class="flex items-center space-x-2">
											<Button
												variant="ghost"
												theme="gray"
												size="sm"
												@click="viewCandidateDetails(candidate)"
											>
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
														d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
													/>
													<path
														stroke-linecap="round"
														stroke-linejoin="round"
														stroke-width="2"
														d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
													/>
												</svg>
											</Button>
											<Button
												variant="ghost"
												theme="blue"
												size="sm"
												@click="contactCandidate(candidate)"
											>
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
														d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 012 2z"
													/>
												</svg>
											</Button>
											<Button
												variant="ghost"
												theme="red"
												size="sm"
												@click="removeFromSegment(candidate)"
											>
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
														d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
													/>
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
								{{ __('Add Candidate to Segment') }}
							</h3>
							<p class="mt-1 text-sm text-gray-500">
								{{ __('Select candidate to add to') }} "{{ talentSegment.title }}"
							</p>
						</div>
						<div class="flex items-center gap-1">
							<Button variant="ghost" class="w-7" @click="closeAddCandidateModal">
								<FeatherIcon name="x" class="h-4 w-4" />
							</Button>
						</div>
					</div>

					<div class="space-y-6">
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-3">
								{{ __('Select Candidate') }} <span class="text-red-500">*</span>
							</label>

							<!-- Loading state -->
							<div
								v-if="loadingAvailableCandidates"
								class="flex items-center justify-center p-8 border-2 border-dashed border-gray-300 rounded-lg"
							>
								<div class="text-center">
									<svg
										class="animate-spin h-8 w-8 text-blue-500 mx-auto mb-2"
										xmlns="http://www.w3.org/2000/svg"
										fill="none"
										viewBox="0 0 24 24"
									>
										<circle
											class="opacity-25"
											cx="12"
											cy="12"
											r="10"
											stroke="currentColor"
											stroke-width="4"
										></circle>
										<path
											class="opacity-75"
											fill="currentColor"
											d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
										></path>
									</svg>
									<p class="text-sm text-gray-500">
										{{ __('Loading available candidates...') }}
									</p>
								</div>
							</div>

							<!-- Autocomplete -->
							<div v-else>
								<Autocomplete
									v-model="candidateFormData.candidate_id"
									:options="availableCandidates"
									:placeholder="__('Search and select candidate...')"
									@change="handleCandidateSelection"
								/>
							</div>

							<p class="mt-2 text-xs text-gray-500">
								{{ __('Only display candidates not already in this segment') }}
							</p>

							<!-- No candidates available message -->
							<div
								v-if="
									!loadingAvailableCandidates && availableCandidates.length === 0
								"
								class="mt-3 p-3 bg-yellow-50 border border-yellow-200 rounded-md"
							>
								<div class="flex">
									<svg
										class="h-5 w-5 text-yellow-400"
										xmlns="http://www.w3.org/2000/svg"
										viewBox="0 0 20 20"
										fill="currentColor"
									>
										<path
											fill-rule="evenodd"
											d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
											clip-rule="evenodd"
										/>
									</svg>
									<div class="ml-3">
										<p class="text-sm text-yellow-800">
											{{ __('No available candidates to add. All candidates are already in this segment.') }}
										</p>
									</div>
								</div>
							</div>
						</div>

						<!-- Selected Candidate Preview -->
						<div
							v-if="selectedCandidatePreview"
							class="border border-gray-200 rounded-lg p-4 bg-gradient-to-r from-blue-50 to-indigo-50"
						>
							<div class="flex items-start space-x-4">
								<div class="flex-shrink-0">
									<div
										class="h-12 w-12 rounded-full bg-gradient-to-r from-blue-500 to-indigo-600 flex items-center justify-center shadow-md"
									>
										<span class="text-lg font-medium text-white">
											{{
												selectedCandidatePreview.candidate_name
													?.charAt(0)
													?.toUpperCase() || '?'
											}}
										</span>
									</div>
								</div>
								<div class="flex-grow min-w-0">
									<div class="text-base font-semibold text-gray-900">
										{{
											selectedCandidatePreview.candidate_name ||
											__('Candidate not specified')
										}}
									</div>
									<div class="text-sm text-gray-600 flex items-center mt-1">
										<svg
											xmlns="http://www.w3.org/2000/svg"
											class="h-4 w-4 mr-1"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"
											/>
										</svg>
										{{
											selectedCandidatePreview.email || __('No email')
										}}
									</div>
									<div
										v-if="
											selectedCandidatePreview.skills &&
											processSkills(selectedCandidatePreview.skills).length >
												0
										"
										class="mt-3"
									>
										<div class="text-xs font-medium text-gray-500 mb-2">
											{{ __('Skills:') }}
										</div>
										<div class="flex flex-wrap gap-1">
											<span
												v-for="skill in processSkills(
													selectedCandidatePreview.skills,
												).slice(0, 4)"
												:key="skill"
												class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 border border-blue-200"
											>
												{{ skill }}
											</span>
											<span
												v-if="
													processSkills(selectedCandidatePreview.skills)
														.length > 4
												"
												class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600 border border-gray-200"
											>
												+{{
													processSkills(selectedCandidatePreview.skills)
														.length - 4
												}}
												{{ __('other skills') }}
											</span>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="flex justify-end space-x-3 px-6 py-4 bg-gray-50">
					<Button variant="outline" theme="gray" @click="closeAddCandidateModal">
						{{ __('Cancel') }}
					</Button>
					<Button
						variant="solid"
						theme="gray"
						:loading="savingCandidate"
						:disabled="
							!candidateFormData.candidate_id ||
							loadingAvailableCandidates ||
							availableCandidates.length === 0
						"
						@click="addCandidateToSegment"
					>
						<template #prefix>
							<FeatherIcon name="user-plus" class="h-4 w-4" />
						</template>
						{{ savingCandidate ? __('Adding...') : __('Add to Segment') }}
					</Button>
				</div>
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
								{{ __('Edit Pool') }}
							</h3>
						</div>
						<div class="flex items-center gap-1">
							<Button
								variant="ghost"
								class="w-7"
								@click="showEditTalentSegmentModal = false"
							>
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
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
	talentSegmentService,
	candidateSegmentService,
	candidateCampaignService,
	candidateService,
	campaignService,
} from '../services/universalService'
import { processSkills } from '../services/candidateService'
import { usersStore } from '@/stores/users'
import { Button, Dialog, Breadcrumbs, FeatherIcon, Autocomplete } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import CampaignWizard from '@/components/campaign/CampaignWizard.vue'
import TalentSegmentForm from '@/components/talent-segment/TalentSegmentForm.vue'
import moment from 'moment'



const { getUser } = usersStore()
const route = useRoute()
const router = useRouter()

// Breadcrumbs
const breadcrumbs = computed(() => {
	console.log('Breadcrumbs computed, route params:', route.params)
	return [
		{ label: __('Applicant Pools'), route: { name: 'TalentSegments' } },
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
const availableCandidates = ref([])
const availableCandidatesData = ref([]) // Store full candidate data for preview

// Modals
const showAddCandidateModal = ref(false)
const showCampaignWizard = ref(false)
const showEditTalentSegmentModal = ref(false)
const editingSegmentData = ref(null)
const savingCandidate = ref(false)
const showAnalytics = ref(false)

// Search
const candidateSearch = ref('')
const searchLoading = ref(false)
const searchResults = ref([]) // Store search-specific results

// Loading states
const loadingAvailableCandidates = ref(false)

// Form data
const candidateFormData = reactive({
	candidate_id: '',
	segment_id: route.params.id,
})

// Computed
const filteredCandidates = computed(() => {
	// If we have search results from API, use those instead
	if (candidateSearch.value && candidateSearch.value.trim().length >= 2) {
		console.log('Using API search results:', searchResults.value.length)
		return searchResults.value
	}
	
	// Otherwise show all candidates
	console.log('Showing all candidates:', candidates.value.length)
	return candidates.value
})

// Dialog options
const addCandidateDialogOptions = computed(() => ({
	title: __('Add Candidate to Segment'),
	size: 'lg',
}))

// Selected candidate preview for the modal
const selectedCandidatePreview = computed(() => {
	if (!candidateFormData.candidate_id) return null
	return (
		availableCandidatesData.value.find((c) => c.name === candidateFormData.candidate_id) ||
		null
	)
})

// Dialog options
const editSegmentDialogOptions = computed(() => ({
	title: __('Edit Applicant Pool'),
	size: '4xl',
}))

// Add watcher with debounce for API search
let searchTimeout = null
watch(candidateSearch, (newValue) => {
	console.log('candidateSearch changed to:', newValue)
	
	// Clear previous timeout
	if (searchTimeout) {
		clearTimeout(searchTimeout)
	}
	
	// Debounce search - wait 500ms after user stops typing
	searchTimeout = setTimeout(async () => {
		if (newValue && newValue.trim().length >= 2) {
			await searchCandidatesAPI(newValue.trim())
		} else {
			// Clear search results if query is empty
			searchResults.value = []
		}
	}, 500)
})

// Methods
const handleSearchInput = async (event) => {
	console.log('Search input event:', event.target.value)
	// The watcher will handle the actual search with debounce
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
		'ACTIVE': 'bg-green-100 text-green-800',
		'INACTIVE': 'bg-gray-100 text-gray-800',
		'PENDING': 'bg-yellow-100 text-yellow-800',
		'CONTACTED': 'bg-blue-100 text-blue-800',
		'REJECTED': 'bg-red-100 text-red-800',
	}
	return statusClasses[status] || 'bg-gray-100 text-gray-800'
}

const loadTalentSegment = async () => {
	loading.value = true
	console.log('loadTalentSegment called with ID:', route.params.id)
	try {
		const result = await talentSegmentService.getFormData(route.params.id)
		console.log('Talent segment API result:', result)
		if (result.success) {
			Object.assign(talentSegment, result.data)
			console.log('Talent segment data assigned:', talentSegment)
		} else {
			console.error('Failed to load talent segment:', result.error)
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
		// First, get all CandidateSegment records for this segment
		console.log('Fetching candidate segments...')
		const candidateSegmentResult = await candidateSegmentService.getList({
			filters: { segment_id: route.params.id },
			fields: ['name', 'candidate_id', 'added_at', 'added_by'],
		})
		console.log('CandidateSegment API result:', candidateSegmentResult)

		if (candidateSegmentResult.success && candidateSegmentResult.data.length > 0) {
			// Get candidate IDs from the relationship
			const candidateIds = candidateSegmentResult.data.map((cs) => cs.candidate_id)

			// Then get the actual candidate data
			const candidateResult = await candidateService.getList({
				filters: { name: ['in', candidateIds] },
				fields: ['name', 'candidate_name', 'email', 'skills', 'last_contact', 'status'],
			})

			if (candidateResult.success) {
				// Merge the data - add segment relationship info to candidate data
				candidates.value = candidateResult.data.map((candidate) => {
					const segmentRelation = candidateSegmentResult.data.find(
						(cs) => cs.candidate_id === candidate.name,
					)
					return {
						...candidate,
						added_at: segmentRelation?.added_at,
						added_by: segmentRelation?.added_by,
						candidate_segment_id: segmentRelation?.name,
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
		const candidateSegmentResult = await candidateSegmentService.getList({
			filters: { segment_id: route.params.id },
			fields: ['candidate_id'],
		})

		if (candidateSegmentResult.success && candidateSegmentResult.data.length > 0) {
			const candidateIds = candidateSegmentResult.data.map((cs) => cs.candidate_id)

			// Then get campaigns that have these candidates through CandidateCampaign
			const candidateCampaignResult = await candidateCampaignService.getList({
				filters: { candidate_id: ['in', candidateIds] },
				fields: ['campaign_id'],
			})

			if (candidateCampaignResult.success && candidateCampaignResult.data.length > 0) {
				const campaignIds = [
					...new Set(candidateCampaignResult.data.map((cc) => cc.campaign_id)),
				]

				// Get the actual campaign data
				const campaignResult = await campaignService.getList({
					filters: { name: ['in', campaignIds] },
					fields: ['name', 'campaign_name', 'status', 'start_date'],
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
	loadingAvailableCandidates.value = true
	try {
		// Get all candidates with more fields for preview
		const allCandidatesResult = await candidateService.getList({
			fields: ['name', 'candidate_name', 'email', 'skills'],
			page_length: 1000,
		})

		if (allCandidatesResult.success) {
			// Get candidates already in this segment
			const existingCandidateSegments = await candidateSegmentService.getList({
				filters: { segment_id: route.params.id },
				fields: ['candidate_id'],
			})

			const existingCandidateIds = existingCandidateSegments.success
				? existingCandidateSegments.data.map((cs) => cs.candidate_id)
				: []

			// Filter out candidates already in the segment
			const availableCandidatesFiltered = allCandidatesResult.data.filter(
				(candidate) => !existingCandidateIds.includes(candidate.name),
			)

			// Store full candidate data for preview
			availableCandidatesData.value = availableCandidatesFiltered

			// Create options for autocomplete
			availableCandidates.value = availableCandidatesFiltered.map((item) => ({
				title: item.candidate_name || item.name,
				value: item.name,
			}))
		}
	} catch (error) {
		console.error('Error loading candidates:', error)
	} finally {
		loadingAvailableCandidates.value = false
	}
}

// Candidate methods
const handleCandidateSelection = (candidateId) => {
	candidateFormData.candidate_id = candidateId
}

const closeAddCandidateModal = () => {
	showAddCandidateModal.value = false
	candidateFormData.candidate_id = ''
	availableCandidates.value = []
	availableCandidatesData.value = []
}

const addCandidateToSegment = async () => {
	if (!candidateFormData.candidate_id) return

	savingCandidate.value = true
	try {
		// Create a new CandidateSegment relationship
		const candidateSegmentData = {
			candidate_id: candidateFormData.candidate_id.title,
			segment_id: route.params.id,
			added_at: moment().format('YYYY-MM-DD HH:mm:ss'),
			added_by: getUser()?.name || 'Administrator',
		}

		const result = await candidateSegmentService.save(candidateSegmentData)
		if (result.success) {
			// Show success message
			const candidateName = selectedCandidatePreview.value?.candidate_name || 'Candidate'
			console.log(`${candidateName} has been successfully added to the segment!`)

			closeAddCandidateModal()
			await loadCandidates()
			await loadTalentSegment()
		} else {
			console.error('Failed to add candidate to segment:', result.error)
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

// Search API method
const searchCandidatesAPI = async (searchQuery) => {
	if (!searchQuery || searchQuery.trim().length < 2) {
		searchResults.value = []
		return
	}

	searchLoading.value = true
	console.log('Searching candidates via API with query:', searchQuery)
	
	try {
		// Get all CandidateSegment records for this segment first
		const candidateSegmentResult = await candidateSegmentService.getList({
			filters: { segment_id: route.params.id },
			fields: ['name', 'candidate_id', 'added_at', 'added_by'],
		})

		if (candidateSegmentResult.success && candidateSegmentResult.data.length > 0) {
			const candidateIds = candidateSegmentResult.data.map((cs) => cs.candidate_id)

			// Search candidates with API filters - search by full_name only
			const searchResult = await candidateService.getList({
				filters: { 
					name: ['in', candidateIds],
					full_name: ['like', `%${searchQuery}%`]
				},
				fields: ['name', 'candidate_name', 'email', 'skills', 'last_contact', 'status'],
			})

			console.log('Search API result:', searchResult)

			if (searchResult.success) {
				// Merge with segment relationship data
				searchResults.value = searchResult.data.map((candidate) => {
					const segmentRelation = candidateSegmentResult.data.find(
						(cs) => cs.candidate_id === candidate.name,
					)
					return {
						...candidate,
						added_at: segmentRelation?.added_at,
						added_by: segmentRelation?.added_by,
						candidate_segment_id: segmentRelation?.name,
					}
				})
			} else {
				console.error('Search API failed:', searchResult.error)
				searchResults.value = []
			}
		} else {
			searchResults.value = []
		}
	} catch (error) {
		console.error('Error searching candidates:', error)
		searchResults.value = []
	} finally {
		searchLoading.value = false
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
</script>

<style scoped>
.talent-segment-detail-view {
	max-width: 1200px;
	margin: 0 auto;
	padding: 20px;
}
</style>
