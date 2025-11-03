<template>
	<div class="flex h-screen bg-gray-50">
		<!-- Vertical Menu Sidebar -->
		<div class="w-64 bg-white border-r border-gray-200 flex flex-col">
			<!-- Header -->
			<div class="p-6 border-b border-gray-200">
				<h1 class="text-xl font-bold text-gray-900">Talent Manager</h1>
				<p class="text-sm text-gray-500 mt-1">Manage pools & talents</p>
			</div>

			<!-- Menu Items -->
			<nav class="flex-1 p-4">
				<button
					v-for="item in menuItems"
					:key="item.id"
					@click="activeSection = item.id"
					:class="[
						'w-full flex items-center gap-3 px-4 py-3 rounded-lg mb-2 transition-all',
						activeSection === item.id
							? 'bg-blue-50 text-blue-700 shadow-sm'
							: 'text-gray-700 hover:bg-gray-50',
					]"
				>
					<FeatherIcon
						:name="item.icon"
						:class="[
							'w-5 h-5',
							activeSection === item.id ? 'text-blue-600' : 'text-gray-500',
						]"
					/>
					<span
						:class="[
							'flex-1 text-left font-medium',
							activeSection === item.id ? 'text-blue-700' : 'text-gray-700',
						]"
					>
						{{ item.label }}
					</span>
					<Badge
						:variant="activeSection === item.id ? 'subtle' : 'outline'"
						:theme="activeSection === item.id ? 'blue' : 'gray'"
					>
						{{ item.count }}
					</Badge>
				</button>
			</nav>

			<!-- Footer -->
			<div class="p-4 border-t border-gray-200">
				<Button variant="solid" theme="blue" class="w-full" @click="handleNewItem">
					<template #prefix>
						<FeatherIcon name="plus" class="w-4 h-4" />
					</template>
					{{ activeSection === 'pools' ? 'New Pool' : 'Add Talent' }}
				</Button>
			</div>
		</div>

		<!-- Main Content Area -->

		<div class="flex-1 flex flex-col overflow-hidden">
			<!-- Top Bar -->
			<div class="bg-white border-b border-gray-200 px-6 py-4">
				<div class="flex items-center justify-between">
					<div>
						<h2 class="text-2xl font-semibold text-gray-900">
							{{ activeSection === 'pools' ? 'Talent Pools' : 'All Talents' }}
						</h2>
						<p class="text-sm text-gray-500 mt-1">
							{{
								activeSection === 'pools'
									? `Manage your ${segments.length} talent pools`
									: `Browse ${talents.length} talents in your system`
							}}
						</p>
					</div>
					<div class="flex items-center gap-3">
						<Input
							v-if="activeSection === 'pools'"
							type="text"
							:placeholder="`Search pools...`"
							:model-value="talentSegmentStore.searchText"
							@input="handleSearchInput"
							class="w-64"
						>
							<template #prefix>
								<FeatherIcon name="search" class="w-4 h-4 text-gray-400" />
							</template>
						</Input>
						<Button variant="outline">
							<template #prefix>
								<FeatherIcon name="filter" class="w-4 h-4" />
							</template>
							Filter
						</Button>
					</div>
				</div>
			</div>

			<!-- Content List -->
			<div class="flex-1 overflow-auto p-6">
				<!-- Pools Grid View -->
				<div v-if="activeSection === 'pools'">
					<div
						v-if="talentSegmentStore.talentSegments.length > 0"
						class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
					>
						<Card
							v-for="segment in talentSegmentStore.talentSegments"
							:key="segment.name"
							class="hover:shadow-md transition-shadow"
						>
							<!-- Card Header -->
							<div class="flex items-start justify-between">
								<div
									class="w-6 h-6 bg-blue-50 rounded-lg flex items-center justify-center"
								>
									<FeatherIcon name="code" class="w-6 h-6 text-blue-600" />
								</div>
								<Dropdown :options="poolActions(segment)">
									<template #default="{ open }">
										<Button
											variant="ghost"
											icon="more-vertical"
											@click="open"
										/>
									</template>
								</Dropdown>
							</div>
							<h3 class="font-semibold text-gray-900 mt-1 mb-2">
								{{ segment.title }}
							</h3>
							<div class="flex items-center gap-2 mb-3 text-xs text-gray-500">
								<FeatherIcon name="clock" class="w-3 h-3" />
								<span>Last updated: {{ segment.formatted_modified }}</span>
							</div>

							<!-- Card Body -->
							<div class="space-y-3">
								<div>
									<div class="text-xs text-gray-500 mb-1">Candidates</div>
									<div class="text-2xl font-bold text-gray-900">
										{{ segment.candidate_count }}
									</div>
								</div>
								<div>
									<div class="text-xs text-gray-500 mb-1">Engagement Rate</div>
									<div class="flex items-center gap-2">
										<Progress
											:value="segment.engagement_rate"
											class="flex-1"
										/>
										<span class="text-sm font-semibold text-gray-900">
											{{ segment.engagement_rate }}%
										</span>
									</div>
								</div>
								<div>
									<div class="text-xs text-gray-500 mb-1">Top Skills</div>
									<div class="flex flex-wrap gap-2">
										<template
											v-if="parseCriteria(segment.criteria).length > 0"
										>
											<span
												v-for="(skill, index) in parseCriteria(
													segment.criteria,
												)"
												:key="index"
												class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium"
											>
												{{ skill }}
											</span>
										</template>
										<span v-else class="text-gray-500 text-sm">
											{{ __('No skill') }}
										</span>
									</div>
								</div>
							</div>

							<!-- Card Footer -->
							<div class="pt-3">
								<Button
									variant="ghost"
									theme="blue"
									class="w-full justify-start"
									@click="GoDetails(segment)"
								>
									Manage Pool →
								</Button>
							</div>
						</Card>
					</div>
					<div v-else class="text-center py-12">
						<div class="text-gray-500">
							<FeatherIcon
								name="search"
								class="w-12 h-12 mx-auto mb-4 text-gray-300"
							/>
							<p class="text-lg font-medium text-gray-500">
								{{ __('No pools found') }}
							</p>
							<p
								class="text-sm text-gray-400 my-1"
								v-if="talentSegmentStore.searchText"
							>
								{{ __('No results for') }} "{{ talentSegmentStore.searchText }}"
							</p>
							<Button
								variant="solid"
								theme="blue"
								@click="showTalentPoolDialog = true"
							>
								<template #prefix>
									<FeatherIcon name="plus" class="w-4 h-4" />
								</template>
								{{ __('Create New Pool') }}
							</Button>
						</div>
					</div>
				</div>

				<!-- Talents Table View -->
				<Card v-else>
					<div class="overflow-x-auto">
						<table class="w-full">
							<thead class="bg-gray-50 border-b border-gray-200">
								<tr>
									<th class="w-12 p-3">
										<input
											type="checkbox"
											:checked="isAllCurrentPageSelected"
											@change="toggleSelectAllTalent"
										/>
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Name
									</th>
									<!-- <th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Pool
									</th> -->
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Contact
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Skills
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Source
									</th>
									<th
										class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Actions
									</th>
								</tr>
							</thead>
							<tbody class="divide-y divide-gray-200">
								<tr
									v-for="talent in talents"
									:key="talent.name"
									class="hover:bg-gray-50 transition-colors"
								>
									<td class="p-3 text-center">
										<input
											type="checkbox"
											:checked="
												selectedAllTalent.some(
													(t) => t.name === talent.name,
												)
											"
											@change="toggleSelectTalent(talent)"
										/>
									</td>
									<td class="px-6 py-4 whitespace-nowrap">
										<div class="flex items-center gap-3">
											<Avatar
												:label="talent.full_name"
												:image="talent.avatar"
												size="md"
											/>
											<div>
												<div class="font-medium text-gray-900">
													{{ talent.full_name }}
												</div>
												<div class="text-sm text-gray-500">
													{{ talent.experience }}
												</div>
											</div>
										</div>
									</td>
									<!-- <td class="px-6 py-4 whitespace-nowrap">
										<div class="text-sm text-gray-900">{{ talent.pool }}</div>
									</td> -->
									<td class="px-6 py-4 whitespace-nowrap">
										<div class="text-sm text-gray-900">{{ talent.email }}</div>
										<div class="text-sm text-gray-500">{{ talent.phone }}</div>
									</td>
									<td class="px-6 py-4 text-sm text-gray-900">
										<div class="flex flex-wrap gap-1">
											<span
												v-for="skill in processSkills(talent.skills)"
												:key="skill"
												class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 truncate"
											>
												{{ skill }}
											</span>
											<span
												v-if="
													!talent.skills ||
													processSkills(talent.skills).length === 0
												"
												class="text-gray-400"
												>-</span
											>
										</div>
									</td>
									<td class="px-6 py-4 whitespace-nowrap">
										<Badge
											:variant="
												talent.status === 'Active' ? 'subtle' : 'outline'
											"
											:theme="talent.status === 'Active' ? 'green' : 'gray'"
										>
											{{ talent.source }}
										</Badge>
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-right">
										<Button
											variant="ghost"
											theme="blue"
											size="sm"
											@click="viewTalent(talent)"
										>
											<FeatherIcon name="eye" class="h-4 w-4" />
										</Button>
										<Button
											variant="ghost"
											theme="gray"
											size="sm"
											@click="deleteTalent(talent)"
										>
											<FeatherIcon name="trash" class="h-4 w-4" />
										</Button>
									</td>
								</tr>
							</tbody>
						</table>
					</div>

					<!-- Pagination Talent-->
					<div
						class="px-6 py-4 border-t border-gray-200 flex items-center justify-between"
					>
						<div class="flex-1 flex justify-between sm:hidden">
							<Button
								variant="outline"
								theme="gray"
								size="sm"
								:disabled="talentPoolStore.pagination.page === 1"
								@click="previousPageTalent"
							>
								{{ __('Previous') }}
							</Button>
							<Button
								variant="outline"
								theme="gray"
								size="sm"
								:disabled="!talentPoolStore.pagination.has_next"
								@click="nextPageTalent"
							>
								{{ __('Next') }}
							</Button>
						</div>
						<div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
							<div>
								<p class="text-sm text-gray-700">
									{{ __('Showing') }}
									<span class="font-medium">{{
										talentPoolStore.pagination.showing_from || 0
									}}</span>
									{{ __('to') }}
									<span class="font-medium">{{
										talentPoolStore.pagination.showing_to || 0
									}}</span>
									{{ __('of') }}
									<span class="font-medium">{{
										talentPoolStore.pagination.total || 0
									}}</span>
									{{ __('results') }}
								</p>
							</div>
							<div>
								<nav
									class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
									aria-label="Pagination"
								>
									<Button
										variant="outline"
										theme="gray"
										size="sm"
										:disabled="talentPoolStore.pagination.page === 1"
										@click="previousPageTalent"
										class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
									>
										<span class="sr-only">{{ __('Previous') }}</span>
										<FeatherIcon name="chevron-left" class="h-5 w-5" />
									</Button>

									<!-- Page numbers -->
									<template
										v-for="pageNumber in visiblePageNumbersTalent"
										:key="pageNumber"
									>
										<Button
											v-if="pageNumber === '...'"
											variant="ghost"
											theme="gray"
											size="sm"
											disabled
											class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700"
										>
											{{ pageNumber }}
										</Button>
										<Button
											v-else
											variant="outline"
											:theme="
												talentPoolStore.pagination.page === pageNumber
													? 'blue'
													: 'gray'
											"
											size="sm"
											@click="goToPageTalent(pageNumber)"
											class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium"
											:class="
												talentPoolStore.pagination.page === pageNumber
													? 'bg-blue-50 text-blue-600 z-10'
													: 'bg-white text-gray-500 hover:bg-gray-50'
											"
										>
											{{ pageNumber }}
										</Button>
									</template>

									<Button
										variant="outline"
										theme="gray"
										size="sm"
										:disabled="!talentPoolStore.pagination.has_next"
										@click="nextPageTalent"
										class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
									>
										<span class="sr-only">{{ __('Next') }}</span>
										<FeatherIcon name="chevron-right" class="h-5 w-5" />
									</Button>
								</nav>
							</div>
						</div>
					</div>
				</Card>

				<div v-if="activeSection === 'pools' && talentSegmentStore.pagination.pages > 1">
					<!-- Add this after the grid view section -->
					<div
						class="border rounded-lg bg-white mt-2 px-6 py-4 border-t border-gray-200 flex items-center justify-between"
					>
						<!-- Mobile pagination -->
						<div class="flex-1 flex justify-between sm:hidden">
							<Button
								variant="outline"
								theme="gray"
								size="sm"
								:disabled="talentSegmentStore.pagination.page === 1"
								@click="previousPageSegment"
							>
								{{ __('Previous') }}
							</Button>
							<Button
								variant="outline"
								theme="gray"
								size="sm"
								:disabled="!talentSegmentStore.pagination.has_next"
								@click="nextPageSegment"
							>
								{{ __('Next') }}
							</Button>
						</div>

						<!-- Desktop pagination -->
						<div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
							<div>
								<p class="text-sm text-gray-700">
									{{ __('Showing') }}
									<span class="font-medium">{{
										talentSegmentStore.pagination.showing_from || 0
									}}</span>
									{{ __('to') }}
									<span class="font-medium">{{
										talentSegmentStore.pagination.showing_to || 0
									}}</span>
									{{ __('of') }}
									<span class="font-medium">{{
										talentSegmentStore.pagination.total || 0
									}}</span>
									{{ __('results') }}
								</p>
							</div>
							<div>
								<nav
									class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
									aria-label="Pagination"
								>
									<!-- Previous Button -->
									<Button
										variant="outline"
										theme="gray"
										size="sm"
										:disabled="talentSegmentStore.pagination.page === 1"
										@click="previousPageSegment"
										class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
									>
										<span class="sr-only">{{ __('Previous') }}</span>
										<FeatherIcon name="chevron-left" class="h-5 w-5" />
									</Button>

									<!-- Page Numbers -->
									<template
										v-for="pageNumber in visiblePageNumbersSegment"
										:key="pageNumber"
									>
										<Button
											v-if="pageNumber === '...'"
											variant="ghost"
											theme="gray"
											size="sm"
											disabled
											class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700"
										>
											{{ pageNumber }}
										</Button>
										<Button
											v-else
											variant="outline"
											:theme="
												talentSegmentStore.pagination.page === pageNumber
													? 'blue'
													: 'gray'
											"
											size="sm"
											@click="goToPageSegment(pageNumber)"
											class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium"
											:class="
												talentSegmentStore.pagination.page === pageNumber
													? 'bg-blue-50 text-blue-600 z-10'
													: 'bg-white text-gray-500 hover:bg-gray-50'
											"
										>
											{{ pageNumber }}
										</Button>
									</template>

									<!-- Next Button -->
									<Button
										variant="outline"
										theme="gray"
										size="sm"
										:disabled="!talentSegmentStore.pagination.has_next"
										@click="nextPageSegment"
										class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
									>
										<span class="sr-only">{{ __('Next') }}</span>
										<FeatherIcon name="chevron-right" class="h-5 w-5" />
									</Button>
								</nav>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- ============ Seagment =========== -->
		<!-- Create option dialog 3 option segment -->

		<Dialog
			v-model="openDialogSegmentOption"
			:options="{
				title: '',
				size: '3xl',
			}"
		>
			<template #body-title>
				<div class="mb-6">
					<h3 class="text-lg font-semibold text-gray-900">
						{{ __('Create Talent Pool') }}
					</h3>
					<p class="text-sm text-gray-500">
						{{ __('Please choose how you want to create a talent pool.') }}
					</p>
				</div>
			</template>

			<template #body-content>
				<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
					<!-- Create Manually -->
					<div
						@click="openManualSegmentCreation"
						class="border border-gray-200 rounded-lg p-4 cursor-pointer hover:border-blue-500 hover:shadow-sm transition-all"
					>
						<div class="flex flex-col items-center text-center">
							<div
								class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center text-blue-600 mb-3"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="h-6 w-6"
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
							</div>
							<h4 class="font-medium text-gray-900">{{ __('Create Manually') }}</h4>
							<p class="text-xs text-gray-500 mt-1">
								{{ __('Create a new talent pool from scratch.') }}
							</p>
						</div>
					</div>

					<!-- AI Suggestions -->
					<div
						@click="openAISegmentSuggestion"
						class="border border-gray-200 rounded-lg p-4 cursor-pointer hover:border-purple-500 hover:shadow-sm transition-all"
					>
						<div class="flex flex-col items-center text-center">
							<div
								class="w-12 h-12 rounded-full bg-purple-50 flex items-center justify-center text-purple-600 mb-3"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="h-6 w-6"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M13 10V3L4 14h7v7l9-11h-7z"
									/>
								</svg>
							</div>
							<h4 class="font-medium text-gray-900">{{ __('AI Suggestions') }}</h4>
							<p class="text-xs text-gray-500 mt-1">
								{{ __('Get AI-powered pool suggestions.') }}
							</p>
						</div>
					</div>

					<!-- Sync from ATS -->
					<div
						@click="syncFromATS"
						class="border border-gray-200 rounded-lg p-4 cursor-pointer hover:border-green-500 hover:shadow-sm transition-all"
					>
						<div class="flex flex-col items-center text-center">
							<div
								class="w-12 h-12 rounded-full bg-green-50 flex items-center justify-center text-green-600 mb-3"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="h-6 w-6"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
									/>
								</svg>
							</div>
							<h4 class="font-medium text-gray-900">{{ __('Sync from ATS') }}</h4>
							<p class="text-xs text-gray-500 mt-1">
								{{ __('Import pools from your ATS system.') }}
							</p>
						</div>
					</div>
				</div>
			</template>

			<template #actions>
				<div class="flex justify-end pt-4 border-t border-gray-200 mt-6">
					<Button
						variant="outline"
						theme="gray"
						@click="openDialogSegmentOption = false"
						class="px-4"
					>
						{{ __('Cancel') }}
					</Button>
				</div>
			</template>
		</Dialog>

		<!-- Create Edit form segment -->
		<TalentPoolDialog
			v-model="showTalentPoolDialog"
			:segment="selectedPool"
			@success="handlePoolCreated"
			@cancel="showTalentPoolDialog = false"
		/>

		<!-- AI Suggestion Modal -->
		<Dialog
			v-model="showAISuggestionModal"
			:options="{
				title: 'Tạo pool từ gợi ý AI',
				size: '3xl',
			}"
		>
			<template #body-content>
				<div class="space-y-4">
					<!-- URL Input -->
					<div class="flex gap-2">
						<Input
							v-model="companyURL"
							type="text"
							:placeholder="__('Nhập URL website công ty')"
							class="flex-1"
						/>
						<Button
							variant="solid"
							theme="blue"
							:loading="isFetchingPositions"
							@click="fetchAISuggestions"
						>
							<template #prefix>
								<FeatherIcon name="search" class="w-4 h-4" />
							</template>
							{{ __('Lấy thông tin sử dụng AI') }}
						</Button>
					</div>

					<!-- Loading State -->
					<div v-if="isFetchingPositions" class="text-center py-8">
						<LoadingIndicator class="w-8 h-8 mx-auto" />
						<p class="mt-2 text-sm text-gray-600">
							{{ __('Đang tải các vị trí làm việc...') }}
						</p>
					</div>

					<!-- Positions List -->
					<div v-else-if="aiPositions.length > 0" class="border rounded-lg divide-y">
						<!-- Select All header row -->
						<div class="p-4 bg-gray-50 border-b flex items-center">
							<input
								type="checkbox"
								:checked="areAllPositionsSelected"
								@change="toggleAllPositions"
								class="h-4 w-4 text-blue-600 rounded border-gray-300"
							/>
							<span class="ml-3 text-sm font-medium text-gray-700">{{
								__('Select All')
							}}</span>
							<span class="ml-auto text-sm font-medium text-gray-700">{{
								__('Department')
							}}</span>
						</div>

						<!-- Positions list -->
						<div
							v-for="position in aiPositions"
							:key="position.id"
							class="p-4 hover:bg-gray-50 flex items-center"
						>
							<input
								type="checkbox"
								:checked="selectedPositions.includes(position.id)"
								@change="togglePositionSelection(position.id)"
								class="h-4 w-4 text-blue-600 rounded border-gray-300"
							/>
							<span class="ml-3 text-gray-900 font-medium">
								{{ position.title }}
							</span>
							<span class="ml-auto text-sm text-gray-500">
								{{ position.department }}
							</span>
						</div>
					</div>

					<!-- Empty State -->
					<div
						v-else-if="!isFetchingPositions"
						class="text-center py-8 border rounded-lg"
					>
						<p class="text-gray-500">
							{{ __('Nhập URL và nhấn "Lấy thông tin" để xem các vị trí làm việc') }}
						</p>
					</div>
				</div>
			</template>

			<template #actions>
				<div class="flex justify-end space-x-3 pt-4">
					<Button variant="outline" theme="gray" @click="closeAISuggestionModal">
						Hủy
					</Button>
					<Button
						variant="solid"
						theme="blue"
						:disabled="selectedPositions.length === 0"
						@click="createPoolsFromSelection"
					>
						Tạo pool ({{ selectedPositions.length }})
					</Button>
				</div>
			</template>
		</Dialog>

		<Dialog v-model="showDeleteDialog" :options="deleteDialogOptions">
			<template #body>
				<div class="bg-white px-4 pb-6 pt-5 sm:px-6">
					<div class="mb-5 flex items-center justify-between">
						<div>
							<h3 class="text-2xl font-semibold leading-6 text-gray-900">
								{{ __('Confirm Delete') }}
							</h3>
						</div>
						<div class="flex items-center gap-1">
							<Button variant="ghost" class="w-7" @click="showDeleteDialog = false">
								<FeatherIcon name="x" class="h-4 w-4" />
							</Button>
						</div>
					</div>
					<div>
						<div class="sm:flex sm:items-start">
							<div
								class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10"
							>
								<svg
									class="h-6 w-6 text-red-600"
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
									/>
								</svg>
							</div>
							<div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
								<h3 class="text-lg leading-6 font-medium text-gray-900">
									{{ __('Delete Talent Pool') }}
								</h3>
								<div class="mt-2">
									<p class="text-sm text-gray-500">
										{{ __('Are you sure you want to delete') }} "{{
											deletingPool?.title
										}}"? {{ __('This action cannot be undone.') }}
									</p>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="px-4 pb-7 pt-4 sm:px-6">
					<div class="flex justify-end items-center gap-3">
						<Button
							variant="outline"
							theme="gray"
							@click="showDeleteDialog = false"
							:disabled="loading"
						>
							{{ __('Cancel') }}
						</Button>
						<Button
							variant="solid"
							theme="red"
							@click="confirmDelete"
							:loading="loading"
						>
							{{ __('Delete') }}
						</Button>
					</div>
				</div>
			</template>
		</Dialog>

		<!-- ============ Talent =========== -->
		<!-- Create Options Dialog 3 option talent-->
		<Dialog
			v-model="openDialogTalentOption"
			:options="{
				title: '',
				size: '3xl',
			}"
		>
			<template #body-title>
				<div class="mb-6">
					<h3 class="text-lg font-semibold text-gray-900">{{ __('Create Talent') }}</h3>
					<p class="text-sm text-gray-500">
						{{ __('Please choose how you want to create a talent.') }}
					</p>
				</div>
			</template>

			<template #body-content>
				<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
					<!-- Create with Form -->
					<div
						@click="openTalentForm"
						class="border border-gray-200 rounded-lg p-4 cursor-pointer hover:border-blue-500 hover:shadow-sm transition-all"
					>
						<div class="flex flex-col items-center text-center">
							<div
								class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center text-blue-600 mb-3"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="h-6 w-6"
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
							</div>
							<h4 class="font-medium text-gray-900">{{ __('Create with Form') }}</h4>
							<p class="text-xs text-gray-500 mt-1">
								{{ __('Fill out information step by step.') }}
							</p>
						</div>
					</div>

					<!-- Upload Excel/CSV -->
					<div
						@click="openUploadModal"
						class="border border-gray-200 rounded-lg p-4 cursor-pointer hover:border-green-500 hover:shadow-sm transition-all"
					>
						<div class="flex flex-col items-center text-center">
							<div
								class="w-12 h-12 rounded-full bg-green-50 flex items-center justify-center text-green-600 mb-3"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="h-6 w-6"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
									/>
								</svg>
							</div>
							<h4 class="font-medium text-gray-900">{{ __('Upload Excel/CSV') }}</h4>
							<p class="text-xs text-gray-500 mt-1">
								{{ __('Upload Excel/CSV file to create multiple talents.') }}
							</p>
						</div>
					</div>

					<!-- Upload Multiple Profiles Talent -->
					<div
						@click="openUploadMany"
						class="border border-gray-200 rounded-lg p-4 cursor-pointer hover:border-purple-500 hover:shadow-sm transition-all"
					>
						<div class="flex flex-col items-center text-center">
							<div
								class="w-12 h-12 rounded-full bg-purple-50 flex items-center justify-center text-purple-600 mb-3"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="h-6 w-6"
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
							<h4 class="font-medium text-gray-900">
								{{ __('Upload Many') }}
							</h4>
							<p class="text-xs text-gray-500 mt-1">
								{{ __('Upload many profiles.') }}
							</p>
						</div>
					</div>
				</div>
			</template>

			<template #actions>
				<div class="flex justify-end pt-4 border-t border-gray-200 mt-6">
					<Button
						variant="outline"
						theme="gray"
						@click="closeDialogOptions"
						class="px-4"
					>
						{{ __('Cancel') }}
					</Button>
				</div>
			</template>
		</Dialog>

		<!-- Create Talent -->

		<Dialog
			v-model="showTalentForm"
			:options="{
				title: 'Add New Talent',
				size: '2xl',
			}"
		>
			<template #body-content>
				<form @submit.prevent="handleTalentSubmit" class="space-y-4">
					<!-- Full Name -->
					<div>
						<label class="block text-sm font-medium text-gray-700"
							>Full Name <span class="text-red-500">*</span></label
						>
						<input
							v-model="newTalent.full_name"
							type="text"
							required
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
						/>
					</div>

					<!-- Email Input -->
					<div>
						<label class="block text-sm font-medium text-gray-700">
							Email <span class="text-red-500">*</span>
						</label>
						<input
							v-model="newTalent.email"
							type="email"
							required
							@blur="checkEmail"
							:class="[
								'mt-1 block w-full rounded-md shadow-sm sm:text-sm',
								emailError
									? 'border-red-300 text-red-900 placeholder-red-300 focus:border-red-500 focus:outline-none focus:ring-red-500'
									: 'border-gray-300 focus:border-blue-500 focus:ring-blue-500',
							]"
							aria-invalid="true"
							aria-describedby="email-error"
						/>
						<p v-if="emailError" class="mt-1 text-sm text-red-600" id="email-error">
							{{ emailError }}
						</p>
					</div>

					<!-- Phone -->
					<div>
						<label class="block text-sm font-medium text-gray-700">Phone</label>
						<input
							v-model="newTalent.phone"
							type="tel"
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
						/>
					</div>

					<!-- LinkedIn Profile -->
					<div>
						<label class="block text-sm font-medium text-gray-700"
							>LinkedIn Profile <span class="text-red-500">*</span></label
						>
						<div class="mt-1 flex rounded-md shadow-sm">
							<input
								v-model="newTalent.linkedin_profile"
								type="text"
								required
								class="block w-full min-w-0 flex-1 rounded-none rounded-r-md border-gray-300 focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
								placeholder="https://linkedin.com/in/username"
							/>
						</div>
						<p class="mt-1 text-xs text-gray-500">https://linkedin.com/in/username</p>
					</div>

					<!-- Skills Input -->
					<div>
						<label class="block text-sm font-medium text-gray-700">Skills</label>
						<div class="mt-1">
							<div class="flex flex-wrap gap-2 mb-2">
								<span
									v-for="(skill, index) in skillTags"
									:key="index"
									class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
								>
									{{ skill }}
									<button
										type="button"
										@click="removeSkill(index)"
										class="ml-1.5 inline-flex text-blue-400 hover:text-blue-600 focus:outline-none"
									>
										<span class="sr-only">Remove skill</span>
										<svg
											class="h-3.5 w-3.5"
											fill="currentColor"
											viewBox="0 0 20 20"
										>
											<path
												fill-rule="evenodd"
												d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
												clip-rule="evenodd"
											/>
										</svg>
									</button>
								</span>
							</div>
							<input
								v-model="skillInput"
								type="text"
								placeholder="Type a skill and press Enter or Tab"
								@keydown.enter.prevent="addSkill"
								@blur="addSkill"
								class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
							/>
							<p class="mt-1 text-xs text-gray-500">
								Separate skills with commas or press Enter
							</p>
						</div>
					</div>

					<!-- Source (Hidden) -->
					<input type="hidden" v-model="newTalent.source" />

					<!-- Latest Company -->
					<div>
						<label class="block text-sm font-medium text-gray-700"
							>Latest Company</label
						>
						<input
							v-model="newTalent.latest_company"
							type="text"
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
						/>
					</div>

					<!-- Total Years of Experience -->
					<div>
						<label class="block text-sm font-medium text-gray-700"
							>Total Years of Experience <span class="text-red-500">*</span></label
						>
						<input
							v-model.number="newTalent.total_years_of_experience"
							type="number"
							min="0"
							step="0.5"
							required
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
						/>
					</div>

					<!-- Desired Role -->
					<!-- Resume Upload -->
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-1">Resume</label>
						<div v-if="newTalent.resume">
							<!-- Show file preview when a file is uploaded -->
							<div
								class="flex items-center justify-between p-3 border border-gray-200 rounded-md bg-gray-50"
							>
								<div class="flex items-center">
									<FeatherIcon
										name="file-text"
										class="h-5 w-5 text-gray-500 mr-2"
									/>
									<span
										class="text-sm font-medium text-gray-900 truncate max-w-xs"
									>
										{{ newTalent.resume }}
									</span>
								</div>
								<div class="flex space-x-2">
									<a
										:href="'/files/' + newTalent.resume"
										target="_blank"
										class="p-1 text-gray-500 hover:text-blue-600"
										title="View file"
									>
										<FeatherIcon name="eye" class="h-4 w-4" />
									</a>
									<button
										@click="removeResume"
										class="p-1 text-gray-500 hover:text-red-600"
										title="Remove file"
									>
										<FeatherIcon name="x" class="h-4 w-4" />
									</button>
								</div>
							</div>
						</div>
						<FileUploader
							v-else
							:fileTypes="['.pdf', '.doc', '.docx']"
							:upload-args="{
								doctype: 'Mira Talent',
								docname: 'temp',
								private: false,
							}"
							@success="handleFileUploadSuccess"
							@error="handleFileUploadError"
						>
							<template v-slot="{ openFileSelector, uploading, progress }">
								<div
									class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md cursor-pointer hover:border-blue-500 transition-colors"
									@click="openFileSelector"
								>
									<div class="space-y-1 text-center">
										<FeatherIcon
											name="upload"
											class="mx-auto h-12 w-12 text-gray-400"
										/>
										<div class="flex text-sm text-gray-600">
											<span
												class="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500"
											>
												Upload a file
											</span>
											<p class="pl-1">or drag and drop</p>
										</div>
										<p class="text-xs text-gray-500">
											PDF, DOC, DOCX up to 10MB
										</p>
										<div
											v-if="uploading"
											class="w-full bg-gray-200 rounded-full h-2.5"
										>
											<div
												class="bg-blue-600 h-2.5 rounded-full"
												:style="`width: ${progress}%`"
											></div>
										</div>
									</div>
								</div>
							</template>
						</FileUploader>
					</div>

					<!-- Desired Role -->
					<div>
						<label class="block text-sm font-medium text-gray-700">Desired Role</label>
						<input
							v-model="newTalent.desired_role"
							type="text"
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
							placeholder="Enter desired role"
						/>
					</div>

					<!-- Source -->
					<div>
						<label class="block text-sm font-medium text-gray-700">Source</label>
						<select
							v-model="newTalent.source"
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
						>
							<option v-for="source in sourceOptions" :key="source" :value="source">
								{{ source }}
							</option>
						</select>
					</div>

					<!-- Interaction Notes -->
					<div>
						<label class="block text-sm font-medium text-gray-700"
							>Interaction Notes</label
						>
						<textarea
							v-model="newTalent.interaction_notes"
							rows="3"
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
							placeholder="Add any notes from your interaction with this talent"
						></textarea>
					</div>
				</form>
			</template>
			<template #actions>
				<div class="flex justify-end space-x-3 pt-4">
					<button
						type="button"
						@click="showTalentForm = false"
						class="inline-flex justify-center rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
					>
						Cancel
					</button>
					<button
						@click="handleTalentSubmit"
						type="submit"
						:class="[
							'inline-flex justify-center rounded-md border border-transparent py-2 px-4 text-sm font-medium text-white shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2',
							!!emailError ||
							!newTalent.full_name ||
							!newTalent.email ||
							!isEmailValid ||
							!newTalent.linkedin_profile ||
							newTalent.total_years_of_experience === null
								? 'bg-gray-300 cursor-not-allowed'
								: 'bg-gray-700 hover:bg-gray-700 focus:ring-gray-500',
						]"
					>
						{{ __('Save Talent') }}
					</button>
				</div>
			</template>
		</Dialog>

		<!-- Upload CSV/Excel Talent -->
		<UploadExcelTalentModal
			v-model="showUploadModal"
			@created="handleTalentCreated"
			@close="closeUploadModal"
		/>

		<!-- Upload BulkCV Talent -->
		<BulkCVUploadModal v-model="showBulkUploadModal" />
	</div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import {
	Button,
	Input,
	Card,
	Badge,
	Avatar,
	FeatherIcon,
	Dropdown,
	Progress,
	FileUploader,
} from 'frappe-ui'
import TalentPoolDialog from '@/components/talent-segment/TalentPoolDialog.vue'
import { useTalentSegmentStore } from '@/stores/talentSegment'
import { useTalentStore } from '@/stores/talent'
import { useRouter } from 'vue-router'
import { useToast } from '@/composables/useToast'
import UploadExcelTalentModal from '@/components/UploadExcelTalentModal.vue'
import BulkCVUploadModal from '@/components/BulkCVUploadModal.vue'

const { showSuccess, showError } = useToast()

// Active section
const activeSection = ref('pools')
const router = useRouter()
// Menu items
// Reactive menu items with computed counts
const menuItems = computed(() => [
	{
		id: 'pools',
		label: 'Talent Pools',
		icon: 'layers',
		count: talentSegmentStore.pagination.total,
	},
	{
		id: 'talents',
		label: 'All Talents',
		icon: 'users',
		count: talentPoolStore.pagination.total,
	},
])

// Store
const talentSegmentStore = useTalentSegmentStore()
const talentPoolStore = useTalentStore()

// Pools
const searchPool = ref('')
const openDialogSegmentOption = ref(false)
const showTalentPoolDialog = ref(false)
const selectedPool = ref(null)
const showDeleteDialog = ref(false)
const deletingPool = ref(null)
const loading = ref(false)
const showAISuggestionModal = ref(false)
const companyURL = ref('')
const isFetchingPositions = ref(false)
const aiPositions = ref([])
const selectedPositions = ref([])

// Mock data for positions - replace with actual API call
const mockPositions = [
	{ id: 1, title: 'Frontend Developer', department: 'Engineering' },
	{ id: 2, title: 'Backend Developer', department: 'Engineering' },
	{ id: 3, title: 'Product Manager', department: 'Product' },
	{ id: 4, title: 'UX/UI Designer', department: 'Design' },
	{ id: 5, title: 'Data Scientist', department: 'Data' },
]
const deleteDialogOptions = {
	title: 'Delete Talent Pool',
	size: 'sm',
	modalClass: 'max-w-md',
}
const segments = computed(() => talentSegmentStore.talentSegments)
// Computed property for segment pagination numbers
const visiblePageNumbersSegment = computed(() => {
	const totalPages = Math.ceil(
		talentSegmentStore.pagination.total / talentSegmentStore.pagination.limit,
	)
	const currentPage = talentSegmentStore.pagination.page
	const pageNumbers = []
	const maxVisiblePages = 5

	if (totalPages <= maxVisiblePages) {
		for (let i = 1; i <= totalPages; i++) {
			pageNumbers.push(i)
		}
	} else {
		pageNumbers.push(1)

		let startPage = Math.max(2, currentPage - 1)
		let endPage = Math.min(totalPages - 1, currentPage + 1)

		if (currentPage <= 3) {
			endPage = 4
		} else if (currentPage >= totalPages - 2) {
			startPage = totalPages - 3
		}

		if (startPage > 2) {
			pageNumbers.push('...')
		}

		for (let i = startPage; i <= endPage; i++) {
			pageNumbers.push(i)
		}

		if (endPage < totalPages - 1) {
			pageNumbers.push('...')
		}

		if (totalPages > 1) {
			pageNumbers.push(totalPages)
		}
	}

	return pageNumbers
})

// Pagination methods for segments
const previousPageSegment = () => {
	if (talentSegmentStore.pagination.page > 1) {
		talentSegmentStore.pagination.page--
		fetchSegments()
	}
}

const nextPageSegment = () => {
	if (talentSegmentStore.pagination.has_next) {
		talentSegmentStore.pagination.page++
		fetchSegments()
	}
}

const goToPageSegment = (pageNumber) => {
	if (pageNumber !== '...' && pageNumber !== talentSegmentStore.pagination.page) {
		talentSegmentStore.pagination.page = pageNumber
		fetchSegments()
	}
}

// Update your fetchSegments method to include pagination
const fetchSegments = async () => {
	await talentSegmentStore.fetchTalentSegments({
		page: talentSegmentStore.pagination.page,
		limit: talentSegmentStore.pagination.limit,
		searchText: talentSegmentStore.searchText, // Include current search text
	})
}
// Talents
const openDialogTalentOption = ref(false) // 4 option dialog
const showTalentForm = ref(false) //create talent dialog
const newTalent = ref({
	full_name: '',
	email: '',
	phone: '',
	linkedin_profile: '',
	latest_company: '',
	total_years_of_experience: null,
	desired_role: '',
	source: 'NEW',
	// internal_rating: 0,
	interaction_notes: '',
	skills: [],
	current_status: 'Active',
	resume: null,
})
const sourceOptions = ref([
	'NEW',
	'Referral',
	'LinkedIn',
	'Job Board',
	'Website',
	'Agency',
	'Campus',
	'Other',
])
const skillInput = ref('')
const skillTags = ref([])
const talents = computed(() => talentPoolStore.talents)
// Talent checkall
const selectedAllTalent = ref([])
const currentPageTalentIds = computed(() => talents.value.map((t) => t.name))
const isAllCurrentPageSelected = computed(() => {
	if (!talents.value.length) return false
	return talents.value.every((talent) =>
		selectedAllTalent.value.some((t) => t.name === talent.name),
	)
})
const toggleSelectAllTalent = () => {
	const currentPageIds = currentPageTalentIds.value
	const allCurrentPageSelected = currentPageIds.every((id) =>
		selectedAllTalent.value.some((t) => t.name === id),
	)

	if (allCurrentPageSelected) {
		// Remove only current page's talents from selection
		selectedAllTalent.value = selectedAllTalent.value.filter(
			(t) => !currentPageIds.includes(t.name),
		)
	} else {
		// Add current page's talents to selection, avoiding duplicates
		const newSelections = talents.value.filter(
			(t) => !selectedAllTalent.value.some((st) => st.name === t.name),
		)
		selectedAllTalent.value = [...selectedAllTalent.value, ...newSelections]
	}
}

const toggleSelectTalent = (talent) => {
	const index = selectedAllTalent.value.findIndex((t) => t.name === talent.name)
	if (index === -1) {
		selectedAllTalent.value.push(talent)
	} else {
		selectedAllTalent.value.splice(index, 1)
	}
}

const visiblePageNumbersTalent = computed(() => {
	const totalPages = Math.ceil(
		talentPoolStore.pagination.total / talentPoolStore.pagination.limit,
	)
	const currentPage = talentPoolStore.pagination.page
	const pageNumbers = []
	const maxVisiblePages = 5 // Number of page numbers to show

	if (totalPages <= maxVisiblePages) {
		// Show all pages if total pages is less than maxVisiblePages
		for (let i = 1; i <= totalPages; i++) {
			pageNumbers.push(i)
		}
	} else {
		// Always show first page
		pageNumbers.push(1)

		// Calculate start and end page numbers
		let startPage = Math.max(2, currentPage - 1)
		let endPage = Math.min(totalPages - 1, currentPage + 1)

		// Adjust if we're at the start or end
		if (currentPage <= 3) {
			endPage = 4
		} else if (currentPage >= totalPages - 2) {
			startPage = totalPages - 3
		}

		// Add ellipsis after first page if needed
		if (startPage > 2) {
			pageNumbers.push('...')
		}

		// Add middle pages
		for (let i = startPage; i <= endPage; i++) {
			pageNumbers.push(i)
		}

		// Add ellipsis before last page if needed
		if (endPage < totalPages - 1) {
			pageNumbers.push('...')
		}

		// Always show last page
		pageNumbers.push(totalPages)
	}

	return pageNumbers
})

// Method to fetch talents with pagination
const fetchTalents = async () => {
	await talentPoolStore.fetchTalents({
		page: talentPoolStore.pagination.page,
		limit: talentPoolStore.pagination.limit,
	})
}
// Add these methods to your component
const previousPageTalent = () => {
	if (talentPoolStore.pagination.page > 1) {
		talentPoolStore.pagination.page--
		fetchTalents()
	}
}

const nextPageTalent = () => {
	if (talentPoolStore.pagination.has_next) {
		talentPoolStore.pagination.page++
		fetchTalents()
	}
}

const goToPageTalent = (pageNumber) => {
	if (pageNumber !== '...' && pageNumber !== talentPoolStore.pagination.page) {
		talentPoolStore.pagination.page = pageNumber
		fetchTalents()
	}
}
const showUploadModal = ref(false)
const showBulkUploadModal = ref(false)
const isEmailValid = computed(() => {
	const email = newTalent.value.email
	if (!email) return true // Empty is valid until submit
	const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
	return emailRegex.test(email)
})
const parseCriteria = (criteria) => {
	try {
		if (!criteria) return []
		// Parse JSON string
		const parsed = JSON.parse(criteria)
		if (!Array.isArray(parsed)) return []

		// Lấy phần tử đầu tiên: ["skills", "==", "React, Python"]
		const item = parsed[0]
		if (!Array.isArray(item) || item.length < 3) return []

		// Lấy giá trị "React, Python" -> tách bằng dấu phẩy
		return item[2].split(',').map((s) => s.trim())
	} catch (e) {
		console.error('Error parsing criteria:', e)
		return []
	}
}

// Xử lý việc mở dialog để tạo mới
const handleNewItem = () => {
	console.log('Create new>>>>', activeSection.value)
	if (activeSection.value == 'pools') {
		openDialogSegmentOption.value = true
		selectedPool.value = null
	} else {
		openDialogTalentOption.value = true
	}
}

const openManualSegmentCreation = () => {
	openDialogSegmentOption.value = false
	showTalentPoolDialog.value = true
}

const openAISegmentSuggestion = () => {
	// Add your AI suggestion logic here
	console.log('Open AI Suggestion')
	openDialogSegmentOption.value = false
	showAISuggestionModal.value = true
	// Reset state when opening modal
	companyURL.value = ''
	aiPositions.value = []
	selectedPositions.value = []
}

//FAKE
const areAllPositionsSelected = computed(() => {
	return (
		aiPositions.value.length > 0 &&
		aiPositions.value.every((pos) => selectedPositions.value.includes(pos.id))
	)
})

const toggleAllPositions = () => {
	if (areAllPositionsSelected.value) {
		// If all are selected, deselect all
		selectedPositions.value = []
	} else {
		// Otherwise select all positions
		selectedPositions.value = aiPositions.value.map((pos) => pos.id)
	}
}

const closeAISuggestionModal = () => {
	showAISuggestionModal.value = false
}

const fetchAISuggestions = async () => {
	if (!companyURL.value.trim()) {
		// Show error message
		return
	}

	isFetchingPositions.value = true
	selectedPositions.value = []

	try {
		// TODO: Replace with actual API call
		// const response = await fetchAISuggestedPositions(companyURL.value)
		// aiPositions.value = response.data.positions

		// Mock API call
		await new Promise((resolve) => setTimeout(resolve, 1000))
		aiPositions.value = mockPositions
	} catch (error) {
		console.error('Error fetching AI suggestions:', error)
		// Show error message to user
	} finally {
		isFetchingPositions.value = false
	}
}

const togglePositionSelection = (positionId) => {
	const index = selectedPositions.value.indexOf(positionId)
	if (index === -1) {
		selectedPositions.value.push(positionId)
	} else {
		selectedPositions.value.splice(index, 1)
	}
}

const createPoolsFromSelection = async () => {
	if (selectedPositions.value.length === 0) return

	try {
		const selectedPositionData = aiPositions.value.filter((p) =>
			selectedPositions.value.includes(p.id),
		)

		// TODO: Replace with actual API call to create pools
		// await createPools(selectedPositionData)

		// Mock API call
		await new Promise((resolve) => setTimeout(resolve, 1000))

		// Show success message
		console.log('Created pools for positions:', selectedPositionData)

		// Close modal and refresh pools list
		closeAISuggestionModal()
		await fetchSegments() // Assuming this refreshes your pools list
	} catch (error) {
		console.error('Error creating pools:', error)
		// Show error message to user
	}
}

const syncFromATS = async () => {
	// Add your ATS sync logic here
	console.log('Sync from ATS')
}

const poolActions = (pool) => [
	{
		label: 'Edit Pool',
		icon: 'edit',
		onClick: () => handleEditPool(pool),
	},
	{
		label: 'Delete Pool',
		icon: 'trash-2',
		onClick: () => handleDetelePoool(pool),
	},
]

const handlePoolCreated = async () => {
	await talentSegmentStore.fetchTalentSegments()
	showTalentPoolDialog.value = false
	selectedPool.value = null
}

const GoDetails = (pool) => {
	console.log('Manage pool', pool.name)
	router.push(`/talent-segments/${pool.name}`)
}

const handleEditPool = (pool) => {
	console.log('Edit pool', pool)
	selectedPool.value = pool
	showTalentPoolDialog.value = true
}

const handleDetelePoool = (pool) => {
	deletingPool.value = pool
	showDeleteDialog.value = true
}

const confirmDelete = async () => {
	if (deletingPool.value) {
		try {
			loading.value = true
			await talentSegmentStore.deleteTalentSegment(deletingPool.value.name)
			showSuccess(__('Talent pool deleted successfully'))
			showDeleteDialog.value = false
			deletingPool.value = null
			await talentSegmentStore.fetchTalentSegments()
		} catch (error) {
			console.error('Error deleting pool:', error)
			showError(error.message || __('Failed to delete talent pool'))
		} finally {
			loading.value = false
		}
	}
}

const handleSearchInput = (event) => {
	// Clear any existing timeout
	if (searchPool.value) {
		clearTimeout(searchPool.value)
	}

	// Set a new timeout to fetch after user stops typing (500ms delay)
	searchPool.value = setTimeout(() => {
		// Reset to first page when searching
		talentSegmentStore.pagination.page = 1
		talentSegmentStore.setSearchText(event)
		// Force refresh with updated search text
		talentSegmentStore.fetchTalentSegments({
			page: 1,
			limit: talentSegmentStore.pagination.limit,
			searchText: event, // Pass search text directly to the API
		})
	}, 500)
}
const processSkills = (skills) => {
	if (!skills) return []
	if (Array.isArray(skills)) return skills
	return skills
		.split(',')
		.map((skill) => skill.trim())
		.filter(Boolean)
}

const closeDialogOptions = () => {
	openDialogTalentOption.value = false
}

const openTalentForm = () => {
	showTalentForm.value = true
	openDialogTalentOption.value = false
}

// Upload file resume
const handleFileUploadSuccess = (file) => {
	console.log('File uploaded successfully:', file)

	// Validate file size (10MB = 10 * 1024 * 1024 bytes)
	const maxSize = 10 * 1024 * 1024
	if (file.file_size > maxSize) {
		showError('File size exceeds the maximum limit of 10MB')
		return
	}

	// Update the resume field with the file name
	newTalent.value.resume = file.file_name

	// Show success message
	showSuccess('Resume uploaded successfully!')
}

// Handle file upload error
const handleFileUploadError = (error) => {
	console.error('File upload error:', error)
	showError('Failed to upload file. Please try again.')
}

// Remove resume
const removeResume = () => {
	if (confirm('Are you sure you want to remove this resume?')) {
		if (newTalent.value.resume?.url) {
			URL.revokeObjectURL(newTalent.value.resume.url)
		}
		newTalent.value.resume = ''
		showSuccess('Resume removed successfully!')
	}
}

const addSkill = () => {
	if (!skillInput.value.trim()) return

	// Split by comma and trim each skill
	const skillsToAdd = skillInput.value
		.split(',')
		.map((skill) => skill.trim())
		.filter((skill) => skill !== '')

	// Add each skill if it doesn't already exist
	skillsToAdd.forEach((skill) => {
		const normalizedSkill = skill.toLowerCase()
		if (!skillTags.value.some((s) => s.toLowerCase() === normalizedSkill)) {
			skillTags.value.push(skill)
		}
	})

	skillInput.value = ''
}

// Handle talent submit talent (create talent)
const handleTalentSubmit = async () => {
	try {
		// Validate required fields
		if (!newTalent.value.full_name) {
			showError(__('Full name is required'))
			return
		}

		if (!newTalent.value.email) {
			showError(__('Email is required'))
			return
		}

		// Validate email format
		const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
		if (!emailRegex.test(newTalent.value.email)) {
			showError('Please enter a valid email address')
			return
		}

		// Check for duplicate email
		const emailExists = await talentPoolStore.checkEmailExists(newTalent.value.email)
		if (emailExists) {
			showError(__('This email is already in use. Please use a different email address.'))
			return
		}

		// Validate required fields
		if (!newTalent.value.linkedin_profile) {
			showError(__('LinkedIn profile is required'))
			return
		}

		// Validate LinkedIn URL format
		try {
			const url = new URL(newTalent.value.linkedin_profile)
			if (!url.hostname.includes('linkedin.com')) {
				showError(
					__(
						'Please enter a valid LinkedIn profile URL (e.g., https://linkedin.com/in/username)',
					),
				)
				return
			}
		} catch (e) {
			showError(__('Please enter a valid URL for LinkedIn profile'))
			return
		}

		if (
			newTalent.value.total_years_of_experience === null ||
			newTalent.value.total_years_of_experience === ''
		) {
			showError(__('Total years of experience is required'))
			return
		}

		try {
			// Create FormData for file upload
			const formData = new FormData()

			console.log('newTalent', newTalent.value)

			// Get the resume file if it exists
			const resumeFile = newTalent.value.resume

			// Manually append each field to ensure they're included
			formData.append('full_name', newTalent.value.full_name || '')
			formData.append('email', newTalent.value.email || '')
			formData.append('phone', newTalent.value.phone || '')
			formData.append('linkedin_profile', newTalent.value.linkedin_profile || '')
			formData.append('latest_company', newTalent.value.latest_company || '')
			formData.append(
				'total_years_of_experience',
				newTalent.value.total_years_of_experience || '',
			)
			formData.append('desired_role', newTalent.value.desired_role || '')
			formData.append('source', newTalent.value.source || 'NEW')
			formData.append('interaction_notes', newTalent.value.interaction_notes || '')
			formData.append('skills', skillTags.value.join(', '))
			formData.append('current_status', newTalent.value.current_status || 'Active')

			// Add the resume file if it exists
			if (resumeFile) {
				formData.append('resume', resumeFile)
			}

			// Convert FormData to a plain object
			const formDataObject = Object.fromEntries(formData)

			console.log('Submitting talent data:', formDataObject)

			// Call the API to create the talent with the plain object
			await talentPoolStore.createTalent(formDataObject)

			// Show success message
			showSuccess('Talent created successfully!')

			// Close the form
			showTalentForm.value = false
			//Reset form
			newTalent.value = {
				full_name: '',
				email: '',
				phone: '',
				linkedin_profile: '',
				latest_company: '',
				total_years_of_experience: null,
				desired_role: '',
				source: 'NEW',
				interaction_notes: '',
				skills: [],
				current_status: 'Active',
				resume: null,
			}
			// Refresh the talents list
			await talentPoolStore.fetchTalents()
		} catch (error) {
			console.error('Error creating talent:', error)
			showError(error.message || __('Failed to create talent. Please try again.'))
		}
	} catch (error) {
		console.error('Error creating talent:', error)
		showError(error.message || __('Failed to create talent. Please try again.'))
	}
}

const openUploadModal = () => {
	console.log('Open upload modal')
	openDialogTalentOption.value = false
	showUploadModal.value = true
}

const closeUploadModal = () => {
	showUploadModal.value = false
}

const handleTalentCreated = async (result) => {
	showSuccess(`Successfully created ${result.success} talent`)
	await talentPoolStore.fetchTalents()
}

const openUploadMany = () => {
	console.log('Open upload many')
	openDialogTalentOption.value = false
	showBulkUploadModal.value = true
}

const viewTalent = (talent) => {
	console.log('View talent', talent.name)
	router.push({ name: 'TalentDetail', params: { id: talent.name } })
}

const deleteTalent = (talent) => {
	console.log('Delete talent', talent.name)
}

onMounted(async () => {
	await talentSegmentStore.fetchTalentSegments()
	await talentPoolStore.fetchTalents()
})

onUnmounted(() => {
	if (searchPool.value) {
		clearTimeout(searchPool.value)
	}
})
</script>

<style scoped>
/* Custom styles nếu cần */
</style>
