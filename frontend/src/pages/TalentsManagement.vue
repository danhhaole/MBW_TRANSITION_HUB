<template>
	<div class="flex h-screen bg-gray-50">
		<div class="flex-1 flex flex-col overflow-hidden">
			<!-- Layout Header -->
			<LayoutHeader>
				<template #left-header>
					<Breadcrumbs :items="breadcrumbs" />
				</template>
				<template #right-header>
					<Button v-if="canCreate" variant="solid" theme="gray" @click="openDialogTalentOption = true">
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
									d="M12 4v16m8-8H4"
								/>
							</svg>
						</template>
						{{ __('Create Talents') }}
					</Button>
				</template>
			</LayoutHeader>
			<div class="flex-1 overflow-auto">
				<div class="max-w-full mx-2 px-6 py-6">
					<!-- Header -->
					<div class="flex items-center justify-between mb-6">
						<!-- Search and Bulk Actions -->
						<div class="flex items-center gap-2">
							<Input 
								type="text" 
								:placeholder="__('Search talents')" 
								:model-value="talentPoolStore.filters.search"
								@input="handleSearchInput"
								class="w-64"
							>
								<template #prefix>
									<FeatherIcon name="search" class="w-4 h-4 text-gray-400" />
								</template>
							</Input>
						</div>
						<div class="flex items-center gap-2">
							<Button variant="outline" @click="toggleFilters">
								<template #prefix>
									<FeatherIcon name="filter" class="w-4 h-4" />
								</template>
								Filter
								<template #suffix v-if="hasActiveFilters">
									<span class="ml-1 bg-blue-500 text-white rounded-full text-xs px-1.5 py-0.5">
										{{ activeFilterCount }}
									</span>
								</template>
							</Button>
							<Button variant="outline" @click="showSyncHistoryModal = true">
								<template #prefix>
									<FeatherIcon name="clock" class="w-4 h-4" />
								</template>
								{{ __('View History') }}
							</Button>
							<!-- Bulk Delete Button -->
							<Button
								v-if="selectedAllTalent.length > 0"
								variant="solid"
								theme="red"
								@click="showBulkDeleteDialog = true"
								class="flex items-center"
							>
								<template #prefix>
									<FeatherIcon name="trash-2" class="w-4 h-4" />
								</template>
								{{ __('Delete') }} ({{ selectedAllTalent.length }})
							</Button>
							<!-- Refresh Button -->
							<Button
								variant="outline"
								theme="gray"
								@click="handleRefresh"
								:loading="loading"
								class="flex items-center py-4"
							>
								<template #prefix>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										class="h-4 w-4"
										:class="{ 'animate-spin': loading }"
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
								</template>
								{{ __('Refresh') }}
							</Button>
							<!-- Export Excel Button -->
							<Button variant="outline" @click="showExportModal = true">
								<template #prefix>
									<FeatherIcon name="download" class="w-4 h-4" />
								</template>
								{{ __('Export Excel') }}
							</Button>
							<Button variant="outline" @click="showSyncHistoryModal = true">
								<template #prefix>
									<FeatherIcon name="clock" class="w-4 h-4" />
								</template>
								{{ __('View History') }}
							</Button>
						</div>
					</div>
					
					<!-- Filter Panel with ConditionsBuilder -->
					<div v-if="showFilters" class="bg-white rounded-lg border border-gray-200 mb-4 p-4">
						<ConditionsBuilder
							v-model="filterConditions"
							doctype="Mira Talent"
							:title="__('Filter Talents')"
							:description="__('Build advanced filters to find talents matching your criteria')"
							:show-preview="false"
							:validate-on-change="false"
							@change="onConditionsChange"
						/>
						
						<!-- Filter Actions -->
						<div class="flex items-center justify-end mt-4 pt-4 border-t border-gray-200">
							<div class="flex gap-2">
								<Button
									variant="outline"
									size="sm"
									@click="clearFilters"
									:disabled="!hasActiveFilters"
								>
									{{ __('Clear All') }}
								</Button>
								<Button
									variant="solid"
									theme="gray"
									size="sm"
									@click="applyFilters"
								>
									{{ __('Apply Filters') }}
								</Button>
							</div>
						</div>
					</div>
					
					<!-- Main Content -->
					<div class="bg-white rounded-lg border border-gray-200">
						<div v-if="talents.length > 0" class="overflow-x-auto">
							<table class="min-w-full bg-white rounded-lg overflow-hidden">
								<thead class="bg-gray-100">
									<tr>
										<th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">
											<input
												class="rounded border-gray-300"
												type="checkbox"
												:checked="isAllCurrentPageSelected"
												@change="toggleSelectAllTalent"
											/>
										</th>
										<th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">
											{{ __('Name') }}
										</th>
										<th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">
											{{ __('Contact') }}
										</th>
										<th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">
											{{ __('City') }}
										</th>
										<th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">
											{{ __('Skills') }}
										</th>
										<th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">
											{{ __('Source') }}
										</th>
										<th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">
											{{ __('Last Updated') }}
										</th>
										<th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">
											{{ __('Last Interaction') }}
										</th>
										<th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">
											{{ __('Actions') }}
										</th>
									</tr>
								</thead>
								<tbody class="divide-y divide-gray-200">
									<tr
										v-for="talent in talents"
										:key="talent.name"
										class="hover:bg-gray-50"
									>
										<td class="py-4 px-4">
											<input
												class="rounded border-gray-300"
												type="checkbox"
												:checked="
													selectedAllTalent.some(
														(t) => t.name === talent.name,
													)
												"
												@change="toggleSelectTalent(talent)"
											/>
										</td>
										<td class="py-4 px-4">
											<div class="flex items-center">
												<Avatar
													:label="talent.full_name"
													:image="talent.avatar"
													size="md"
													class="mr-3"
												/>
												<div>
													<div class="font-medium text-base text-gray-800">
														{{ talent.full_name }}
													</div>
												</div>
											</div>
										</td>
										<td class="py-4 px-4 text-sm text-gray-700">
											<div>{{ talent.email }}</div>
											<div class="text-gray-500">{{ talent.phone }}</div>
										</td>
										<td class="py-4 px-4 text-sm text-gray-700">
											{{ talent.current_city || '-' }}
										</td>
										<td class="py-4 px-4 text-sm text-gray-700">
											<div class="flex flex-wrap gap-1 max-w-xs">
												<template v-if="talent.skills && processSkills(talent.skills).length > 0">
													<span
														v-if="processSkills(talent.skills).length === 1"
														class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 max-w-[200px]"
														:title="processSkills(talent.skills)[0]"
													>
														<span class="truncate">{{ processSkills(talent.skills)[0] }}</span>
													</span>
													<template v-else>
														<span 
															class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 max-w-[200px]"
															:title="processSkills(talent.skills)[0]"
														>
															<span class="truncate">{{ processSkills(talent.skills)[0] }}</span>
														</span>
														<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-100 text-blue-800">
															+{{ processSkills(talent.skills).length - 1 }}
														</span>
													</template>
												</template>
												<span
													v-else
													class="text-gray-400"
													>-</span
												>
											</div>
										</td>
										<td class="py-4 px-4 text-sm text-gray-700">
											<Badge
												:variant="
													talent.status === 'Active'
														? 'subtle'
														: 'outline'
												"
												:theme="
													talent.status === 'Active'
														? 'green'
														: 'gray'
												"
											>
												{{ talent.source }}
											</Badge>
										</td>
										<td class="py-4 px-4 text-sm text-gray-700">
											{{ talent.modified ? formatDate(talent.modified) : '-' }}
										</td>
										<td class="py-4 px-4 text-sm text-gray-700">
											{{ talent.last_interaction_date ? formatDate(talent.last_interaction_date) : '-' }}
										</td>
										<td class="py-4 px-4">
											<div class="flex items-center space-x-2">
												<button 
													@click="viewTalent(talent)"
													class="text-gray-600 hover:text-blue-600 p-2 rounded-md hover:bg-blue-50 transition-colors"
													:title="__('View Details')"
												>
													<FeatherIcon name="eye" class="h-4 w-4" />
												</button>
												<button 
													@click="deleteTalent(talent)"
													class="text-gray-600 hover:text-red-600 p-2 rounded-md hover:bg-red-50 transition-colors"
													:title="__('Delete')"
												>
													<FeatherIcon name="trash-2" class="h-4 w-4" />
												</button>
											</div>
										</td>
									</tr>
								</tbody>
							</table>
						</div>

						<!-- Empty State -->
						<div v-else class="text-center py-12">
							<div class="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-4">
								<FeatherIcon name="users" class="h-8 w-8 text-gray-400" />
							</div>
							<h3 class="text-lg font-medium text-gray-900 mb-2">{{ __('No talents found') }}</h3>
							<p class="text-gray-500 mb-4" v-if="talentPoolStore.filters.search">
								{{ __('No results for') }} "{{ talentPoolStore.filters.search }}"
							</p>
							<Button
								v-if="canCreate"
								@click="openDialogTalentOption = true"
								theme="gray"
								variant="solid"
								class="text-sm font-medium"
							>
								{{ __('Create Talent') }}
							</Button>
						</div>

						<!-- Pagination Talent-->
						<div
							v-if="visiblePageNumbersTalent.length > 1 || talentPoolStore.pagination.total > talentPoolStore.pagination.limit"
							class="flex items-center justify-between mt-6 p-6 border-t border-gray-200"
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
							<div class="text-sm text-gray-600">
								{{ __('Display') }} {{ talentPoolStore.pagination.showing_from || 1 }}-{{ talentPoolStore.pagination.showing_to || talents.length }} {{ __('of') }} {{ talentPoolStore.pagination.total || talents.length }} {{ __('talents') }}
							</div>
							<div class="flex space-x-1">
								<button 
									@click="goToPageTalent(1)"
									:disabled="talentPoolStore.pagination.page === 1"
									class="px-3 py-1 rounded-md bg-gray-100 text-gray-600 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
								>
									<FeatherIcon name="chevron-left" class="h-5 w-5" />
								</button>
								
								<template v-for="page in visiblePageNumbersTalent" :key="page">
									<button
										v-if="page === '...'"
										class="px-3 py-1 text-gray-500"
										disabled
									>
										...
									</button>
									<button
										v-else
										@click="goToPageTalent(page)"
										:class="talentPoolStore.pagination.page === page ? 'bg-black text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
										class="px-3 py-1 rounded-md"
									>
										{{ page }}
									</button>
								</template>
								
								<button 
									@click="goToPageTalent(talentPoolStore.pagination.page + 1)"
									:disabled="!talentPoolStore.pagination.has_next"
									class="px-3 py-1 rounded-md bg-gray-100 text-gray-600 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
								>
									<FeatherIcon name="chevron-right" class="h-5 w-5" />
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>
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
						<h3 class="text-lg font-semibold text-gray-900">
							{{ __('Create Talent') }}
						</h3>
						<p class="text-sm text-gray-500">
							{{ __('Please choose how you want to create a talent.') }}
						</p>
					</div>
				</template>

				<template #body-content>
					<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
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
								<h4 class="font-medium text-gray-900">
									{{ __('Create with Form') }}
								</h4>
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
								<h4 class="font-medium text-gray-900">
									{{ __('Upload Excel/CSV') }}
								</h4>
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

						<!-- Sync from ATS -->
						<div
							@click="syncFromATS"
							class="border border-gray-200 rounded-lg p-4 cursor-pointer hover:border-orange-500 hover:shadow-sm transition-all"
						>
							<div class="flex flex-col items-center text-center">
								<div
									class="w-12 h-12 rounded-full bg-orange-50 flex items-center justify-center text-orange-600 mb-3"
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
								<h4 class="font-medium text-gray-900">
									{{ __('Sync from ATS') }}
								</h4>
								<p class="text-xs text-gray-500 mt-1">
									{{ __('Import candidates from your ATS system.') }}
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
					size: '3xl',
				}"
			>
				<template #body-content>
					<form @submit.prevent="handleTalentSubmit" class="space-y-4">
						<!-- Essential Information Section -->
						<div class="space-y-6">
							<h4 class="text-lg font-semibold text-gray-900 border-b border-gray-200 pb-3">
								{{ __('Essential Information') }}
							</h4>
							
							<!-- Row 1: Full Name and Gender -->
							<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
								<!-- Full Name -->
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-1">
										Full Name <span class="text-red-500">*</span>
									</label>
									<input
										v-model="newTalent.full_name"
										type="text"
										required
										class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
										placeholder="Enter full name"
									/>
								</div>

								<!-- Gender -->
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-1">
										Gender
									</label>
									<select
										v-model="newTalent.gender"
										class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
									>
										<option value="">Select gender</option>
										<option value="Male">Male</option>
										<option value="Female">Female</option>
										<option value="Other">Other</option>
										<option value="Unknown">Prefer not to say</option>
									</select>
								</div>
							</div>

							<!-- Row 2: Email and Phone -->
							<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
								<!-- Email Input -->
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-1">
										Email <span class="text-red-500">*</span>
									</label>
									<input
										v-model="newTalent.email"
										type="email"
										required
										@blur="checkEmail"
										:class="[
											'block w-full rounded-md shadow-sm text-sm px-3 py-2',
											emailError
												? emailError.includes('blacklist')
													? 'border-yellow-300 text-yellow-900 placeholder-yellow-300 focus:border-yellow-500 focus:outline-none focus:ring-yellow-500'
													: 'border-red-300 text-red-900 placeholder-red-300 focus:border-red-500 focus:outline-none focus:ring-red-500'
												: 'border-gray-300 focus:border-blue-500 focus:ring-blue-500',
										]"
										placeholder="Enter email address"
										aria-invalid="true"
										aria-describedby="email-error"
									/>
									<p
										v-if="emailError"
										:class="[
											'mt-1 text-xs',
											emailError.includes('blacklist') ? 'text-yellow-600' : 'text-red-600'
										]"
										id="email-error"
									>
										{{ emailError }}
									</p>
								</div>

								<!-- Phone -->
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-1">
										Phone
									</label>
									<input
										v-model="newTalent.phone"
										type="tel"
										@blur="checkPhoneNumber"
										:class="[
											'block w-full rounded-md shadow-sm text-sm px-3 py-2',
											phoneError
												? 'border-red-300 text-red-900 placeholder-red-300 focus:border-red-500 focus:outline-none focus:ring-red-500'
												: 'border-gray-300 focus:border-blue-500 focus:ring-blue-500',
										]"
										placeholder="Enter phone number"
										aria-invalid="true"
										aria-describedby="phone-error"
									/>
									<p
										v-if="phoneError"
										class="mt-1 text-xs text-red-600"
										id="phone-error"
									>
										{{ phoneError }}
									</p>
								</div>
							</div>
						</div>

						<!-- Additional Information Section (Collapsible) -->
						<div class="border-t border-gray-200 pt-6">
							<button
								type="button"
								@click="showAdditionalInfo = !showAdditionalInfo"
								class="flex items-center justify-between w-full text-left text-lg font-semibold text-gray-900 hover:text-gray-700 focus:outline-none pb-3"
							>
								<span>{{ __('Additional Information') }}</span>
								<FeatherIcon 
									:name="showAdditionalInfo ? 'chevron-up' : 'chevron-down'" 
									class="h-5 w-5 transition-transform duration-200"
								/>
							</button>
							
							<div v-show="showAdditionalInfo" class="mt-6 space-y-6">
								<!-- Social Media Profiles Section -->
								<div class="bg-gray-50 rounded-md p-3 space-y-3">
									<h5 class="text-sm font-medium text-gray-900 mb-2">Social Media Profiles</h5>
									
									<!-- LinkedIn and Facebook Row -->
									<div class="grid grid-cols-1 md:grid-cols-2 gap-3">
										<!-- LinkedIn Profile -->
										<div>
											<label class="block text-sm font-medium text-gray-700 mb-1">
												<div class="flex items-center">
													<svg class="w-3 h-3 mr-1.5 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
														<path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
													</svg>
													LinkedIn
												</div>
											</label>
											<input
												v-model="newTalent.linkedin_profile"
												type="url"
												class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
												placeholder="https://linkedin.com/in/username"
											/>
										</div>

										<!-- Facebook Profile -->
										<div>
											<label class="block text-sm font-medium text-gray-700 mb-1">
												<div class="flex items-center">
													<svg class="w-3 h-3 mr-1.5 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
														<path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
													</svg>
													Facebook
												</div>
											</label>
											<input
												v-model="newTalent.facebook_profile"
												type="url"
												class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
												placeholder="https://facebook.com/username"
											/>
										</div>
									</div>

									<!-- Zalo Profile -->
									<div>
										<label class="block text-sm font-medium text-gray-700 mb-1">
											<div class="flex items-center">
												<svg class="w-3 h-3 mr-1.5 text-blue-500" fill="currentColor" viewBox="0 0 24 24">
													<path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.568 8.16c-.169-.224-.487-.32-.75-.32-.487 0-.881.394-.881.881 0 .487.394.881.881.881.263 0 .581-.096.75-.32l.169-.224c.056-.075.094-.169.094-.263 0-.169-.075-.32-.169-.431-.056-.056-.094-.131-.094-.204zM12 18.72c-3.722 0-6.72-3.018-6.72-6.72S8.278 5.28 12 5.28s6.72 3.018 6.72 6.72-2.998 6.72-6.72 6.72z"/>
												</svg>
												Zalo
											</div>
										</label>
										<input
											v-model="newTalent.zalo_profile"
											type="text"
											class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
											placeholder="Zalo username or phone number"
										/>
									</div>
								</div>

								<!-- Skills Input -->
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-1">Skills</label>
									<div>
										<div class="flex flex-wrap gap-1 mb-2" v-if="skillTags.length > 0">
											<span
												v-for="(skill, index) in skillTags"
												:key="index"
												class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
											>
												{{ skill }}
												<button
													type="button"
													@click="removeSkill(index)"
													class="ml-1 inline-flex text-blue-400 hover:text-blue-600 focus:outline-none"
												>
													<FeatherIcon name="x" class="h-3 w-3" />
												</button>
											</span>
										</div>
										<input
											v-model="skillInput"
											type="text"
											placeholder="Type a skill and press Enter"
											@keydown.enter.prevent="addSkill"
											@blur="addSkill"
											class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
										/>
									</div>
								</div>

								<!-- Two Column Layout for Company and Experience -->
								<div class="grid grid-cols-1 md:grid-cols-2 gap-3">
									<!-- Latest Company -->
									<div>
										<label class="block text-sm font-medium text-gray-700 mb-1">
											Latest Company
										</label>
										<input
											v-model="newTalent.latest_company"
											type="text"
											class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
											placeholder="Company name"
										/>
									</div>

									<!-- Total Years of Experience -->
									<div>
										<label class="block text-sm font-medium text-gray-700 mb-1">
											Years of Experience
										</label>
										<input
											v-model.number="newTalent.total_years_of_experience"
											type="number"
											min="0"
											step="0.5"
											class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
											placeholder="0"
										/>
									</div>
								</div>

								<!-- Two Column Layout for Role and Source -->
								<div class="grid grid-cols-1 md:grid-cols-2 gap-3">
									<!-- Desired Role -->
									<div>
										<label class="block text-sm font-medium text-gray-700 mb-1">
											Desired Role
										</label>
										<input
											v-model="newTalent.desired_role"
											type="text"
											class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
											placeholder="Enter desired role"
										/>
									</div>

									<!-- Source -->
									<div>
										<label class="block text-sm font-medium text-gray-700 mb-1">Source</label>
										<select
											v-model="newTalent.source"
											class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
										>
											<option
												v-for="source in sourceOptions"
												:key="source"
												:value="source"
											>
												{{ source }}
											</option>
										</select>
									</div>
								</div>

								<!-- Two Column Layout for Position and Current City -->
								<div class="grid grid-cols-1 md:grid-cols-2 gap-3">
									<!-- Position -->
									<!-- <div>
										<label class="block text-sm font-medium text-gray-700 mb-1">
											Position
										</label>
										<input
											v-model="newTalent.position"
											type="text"
											class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
											placeholder="Enter current position"
										/>
									</div> -->

									<!-- Current City -->
									<div>
										<label class="block text-sm font-medium text-gray-700 mb-1">
											Current City
										</label>
										<input
											v-model="newTalent.current_city"
											type="text"
											class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
											placeholder="Enter current city/address"
										/>
									</div>
								</div>

								<!-- New Additional Fields Section -->
								<div class="bg-blue-50 rounded-md p-4 space-y-4">
									<h5 class="text-sm font-medium text-gray-900 mb-3">Professional Assessment</h5>
									
									<!-- Row 1: Availability Date and Expected Salary -->
									<div class="grid grid-cols-1 md:grid-cols-2 gap-3">
										<!-- Availability Date -->
										<div>
											<label class="block text-sm font-medium text-gray-700 mb-1">
												Availability Date
											</label>
											<input
												v-model="newTalent.availability_date"
												type="date"
												class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
											/>
										</div>

										<!-- Expected Salary -->
										<div>
											<label class="block text-sm font-medium text-gray-700 mb-1">
												Expected Salary
											</label>
											<input
												v-model.number="newTalent.expected_salary"
												type="number"
												min="0"
												step="1000000"
												class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
												placeholder="VND"
											/>
										</div>
									</div>

									<!-- Row 2: Hard Skills and Soft Skills -->
									<div class="grid grid-cols-1 md:grid-cols-2 gap-3">
										<!-- Hard Skills -->
										<div>
											<label class="block text-sm font-medium text-gray-700 mb-1">
												Hard Skills
											</label>
											<textarea
												v-model="newTalent.hard_skills"
												rows="2"
												class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
												placeholder="Technical skills, certifications, tools..."
											></textarea>
										</div>

										<!-- Soft Skills -->
										<div>
											<label class="block text-sm font-medium text-gray-700 mb-1">
												Soft Skills
											</label>
											<textarea
												v-model="newTalent.soft_skills"
												rows="2"
												class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
												placeholder="Communication, leadership, teamwork..."
											></textarea>
										</div>
									</div>

									<!-- Domain Expertise -->
									<div>
										<label class="block text-sm font-medium text-gray-700 mb-1">
											Domain Expertise
										</label>
										<textarea
											v-model="newTalent.domain_expertise"
											rows="2"
											class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
											placeholder="Industry knowledge, specialized domains..."
										></textarea>
									</div>

									<!-- Row 3: Assessment Fields -->
									<div class="grid grid-cols-1 md:grid-cols-3 gap-3">
										<!-- Cultural Fit -->
										<div>
											<label class="block text-sm font-medium text-gray-700 mb-1">
												Cultural Fit
											</label>
											<select
												v-model="newTalent.cultural_fit"
												class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
											>
												<option value="">Select fit level</option>
												<option value="High">High</option>
												<option value="Medium">Medium</option>
												<option value="Low">Low</option>
											</select>
										</div>

										<!-- Internal Rating -->
										<div>
											<label class="block text-sm font-medium text-gray-700 mb-1">
												Internal Rating
											</label>
											<select
												v-model="newTalent.internal_rating"
												class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
											>
												<option value="">Select rating</option>
												<option value="A">A - Excellent</option>
												<option value="B">B - Good</option>
												<option value="C">C - Average</option>
											</select>
										</div>

										<!-- Recruitment Readiness -->
										<div>
											<label class="block text-sm font-medium text-gray-700 mb-1">
												Recruitment Readiness
											</label>
											<select
												v-model="newTalent.recruitment_readiness"
												class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
											>
												<option value="">Select readiness</option>
												<option value="Cold">Cold</option>
												<option value="Warm">Warm</option>
												<option value="Hot">Hot</option>
											</select>
										</div>
									</div>
								</div>

								<!-- Resume Upload - Compact Version -->
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-2"
										>Resume</label
									>
									<div v-if="newTalent.resume">
										<!-- Compact file preview -->
										<div class="flex items-center justify-between p-2 border border-gray-200 rounded-md bg-gray-50">
											<div class="flex items-center">
												<FeatherIcon name="file-text" class="h-4 w-4 text-gray-500 mr-2" />
												<span class="text-sm text-gray-900 truncate max-w-xs">
													{{ newTalent.resume }}
												</span>
											</div>
											<div class="flex space-x-1">
												<a
													:href="'/private/files/' + newTalent.resume"
													target="_blank"
													class="p-1 text-gray-500 hover:text-blue-600"
													title="View file"
												>
													<FeatherIcon name="eye" class="h-3 w-3" />
												</a>
												<button
													@click="removeResume"
													class="p-1 text-gray-500 hover:text-red-600"
													title="Remove file"
												>
													<FeatherIcon name="x" class="h-3 w-3" />
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
											private: true,
										}"
										@success="handleFileUploadSuccess"
										@error="handleFileUploadError"
									>
										<template v-slot="{ openFileSelector, uploading, progress }">
											<div
												class="flex items-center justify-center px-4 py-3 border-2 border-gray-300 border-dashed rounded-md cursor-pointer hover:border-blue-500 transition-colors"
												@click="openFileSelector"
											>
												<div class="flex items-center space-x-2">
													<FeatherIcon name="upload" class="h-5 w-5 text-gray-400" />
													<div class="text-sm text-gray-600">
														<span class="font-medium text-blue-600 hover:text-blue-500">
															Upload a file
														</span>
														<span class="text-gray-500"> or drag and drop</span>
													</div>
												</div>
												<div
													v-if="uploading"
													class="ml-4 w-20 bg-gray-200 rounded-full h-2"
												>
													<div
														class="bg-blue-600 h-2 rounded-full"
														:style="`width: ${progress}%`"
													></div>
												</div>
											</div>
										</template>
									</FileUploader>
								</div>

								<!-- Interaction Notes -->
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-1">
										Interaction Notes
									</label>
									<textarea
										v-model="newTalent.interaction_notes"
										rows="2"
										class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
										placeholder="Add any notes from your interaction with this talent"
									></textarea>
								</div>
							</div>
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
								!isEmailValid
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
			<BulkCVUploadModal 
				v-model="showBulkUploadModal" 
				@talent-created="handleBulkUploadSuccess"
			/>

			<!-- ATS Talent Sync Dialog -->
			<ATSTalentSyncDialog
				v-model="showATSTalentSyncDialog"
				@success="handleSyncSuccess"
			/>

			<!-- Sync History Modal -->
			<SyncHistoryModal v-model="showSyncHistoryModal" />

			<!-- Export Talent Modal -->
			<ExportTalentModal
				v-model="showExportModal"
				:filters="buildExportFilters()"
				:total-records="talentPoolStore.pagination.total"
				:current-page-size="talentPoolStore.talents.length"
				@close="showExportModal = false"
			/>

			<!-- Delete Talent Confirmation Dialog -->
			<Dialog
				v-model="showDeleteDialog"
				:options="{
					title: '',
					size: 'sm',
				}"
			>
				<template #body-title>
					<div class="flex items-center gap-3 mb-4">
						<div class="w-12 h-12 rounded-full bg-red-100 flex items-center justify-center">
							<FeatherIcon name="alert-triangle" class="w-6 h-6 text-red-600" />
						</div>
						<div>
							<h3 class="text-lg font-semibold text-gray-900">
								{{ __('Delete talent') }}
							</h3>
						</div>
					</div>
				</template>

				<template #body-content>
					<div class="space-y-4">
						<p class="text-sm text-gray-600">
							{{ __('Bạn có chắc chắn muốn xóa talent này không?') }}
						</p>
						
						<div v-if="talentToDelete" class="bg-gray-50 rounded-lg p-4 space-y-2">
							<div class="flex items-center gap-3">
								<Avatar
									:label="talentToDelete.full_name"
									:image="talentToDelete.avatar"
									size="md"
								/>
								<div>
									<div class="font-medium text-gray-900">{{ talentToDelete.full_name }}</div>
									<div class="text-sm text-gray-500">{{ talentToDelete.email }}</div>
								</div>
							</div>
						</div>

						<div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
							<div class="flex gap-2">
								<FeatherIcon name="alert-circle" class="w-4 h-4 text-yellow-600 mt-0.5 flex-shrink-0" />
								<p class="text-xs text-yellow-800">
									{{ __('Hành động này không thể hoàn tác. Tất cả dữ liệu liên quan sẽ bị xóa.') }}
								</p>
							</div>
						</div>
					</div>
				</template>

				<template #actions>
					<div class="flex justify-end gap-3 pt-4">
						<Button
							variant="outline"
							theme="gray"
							@click="showDeleteDialog = false"
							class="px-4"
						>
							{{ __('Hủy') }}
						</Button>
						<Button
							variant="solid"
							theme="red"
							@click="confirmDeleteTalent"
							:loading="isDeleting"
							class="px-4"
						>
							{{ __('Xóa') }}
						</Button>
					</div>
				</template>
			</Dialog>

			<!-- Bulk Delete Confirmation Dialog -->
			<Dialog
				v-model="showBulkDeleteDialog"
				:options="{
					title: '',
					size: 'md',
				}"
			>
				<template #body-title>
					<div class="flex items-center gap-3 mb-4">
						<div class="w-12 h-12 rounded-full bg-red-100 flex items-center justify-center">
							<FeatherIcon name="alert-triangle" class="w-6 h-6 text-red-600" />
						</div>
						<div>
							<h3 class="text-lg font-semibold text-gray-900">
								{{ __('Delete Multiple Talents') }}
							</h3>
						</div>
					</div>
				</template>

				<template #body-content>
					<div class="space-y-4">
						<p class="text-sm text-gray-600">
							{{ __('Bạn có chắc chắn muốn xóa {0} talent(s) đã chọn không?', [selectedAllTalent.length]) }}
						</p>
						
						<div class="bg-gray-50 rounded-lg p-4 max-h-40 overflow-y-auto">
							<div class="space-y-2">
								<div 
									v-for="talent in selectedAllTalent.slice(0, 5)" 
									:key="talent.name"
									class="flex items-center gap-3"
								>
									<Avatar
										:label="talent.full_name"
										:image="talent.avatar"
										size="sm"
									/>
									<div>
										<div class="font-medium text-sm text-gray-900">{{ talent.full_name }}</div>
										<div class="text-xs text-gray-500">{{ talent.email }}</div>
									</div>
								</div>
								<div v-if="selectedAllTalent.length > 5" class="text-xs text-gray-500 text-center pt-2">
									{{ __('và {0} talent(s) khác...', [selectedAllTalent.length - 5]) }}
								</div>
							</div>
						</div>

						<div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
							<div class="flex gap-2">
								<FeatherIcon name="alert-circle" class="w-4 h-4 text-yellow-600 mt-0.5 flex-shrink-0" />
								<div class="text-xs text-yellow-800">
									<p class="font-medium">{{ __('Lưu ý quan trọng:') }}</p>
									<p>{{ __('Việc xóa sẽ được đưa vào hàng đợi xử lý. Bạn sẽ nhận được thông báo khi quá trình hoàn tất.') }}</p>
									<p>{{ __('Hành động này không thể hoàn tác.') }}</p>
								</div>
							</div>
						</div>
					</div>
				</template>

				<template #actions>
					<div class="flex justify-end gap-3 pt-4">
						<Button
							variant="outline"
							theme="gray"
							@click="showBulkDeleteDialog = false"
							class="px-4"
						>
							{{ __('Hủy') }}
						</Button>
						<Button
							variant="solid"
							theme="red"
							@click="confirmBulkDelete"
							:loading="isBulkDeleting"
							class="px-4"
						>
							{{ __('Xóa {0} talent(s)', [selectedAllTalent.length]) }}
						</Button>
					</div>
				</template>
			</Dialog>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import {
	Breadcrumbs,
	Button,
	Input,
	Card,
	Badge,
	Avatar,
	FeatherIcon,
	FileUploader,
	Dialog,
	call,
} from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import { useRouter } from 'vue-router'
import { useToast } from '@/composables/useToast'
import { useTalentStore } from '@/stores/talent'
import { useBlacklistStore } from '@/stores/blacklist'
import { globalStore } from '@/stores/global';
import UploadExcelTalentModal from '@/components/UploadExcelTalentModal.vue'
import BulkCVUploadModal from '@/components/BulkCVUploadModal.vue'
import ATSTalentSyncDialog from '@/components/ATSTalentSyncDialog.vue'
import SyncHistoryModal from '@/components/SyncHistoryModal.vue'
import ExportTalentModal from '@/components/ExportTalentModal.vue'
import ConditionsBuilder from '@/components/ConditionsFilter/ConditionsBuilder.vue'
import { usePermissionStore } from "@/stores/permission";

const permission = usePermissionStore()
// Breadcrumbs
const breadcrumbs = [{ label: __('Talent Profiles'), route: { name: 'TalentPool' } }]
const { showSuccess, showError } = useToast()
const router = useRouter()
//Store
const talentPoolStore = useTalentStore()
const blacklistStore = useBlacklistStore()
const { $socket } = globalStore();
const openDialogTalentOption = ref(false) // 4 option dialog
const showTalentForm = ref(false) //create talent dialog
const showAdditionalInfo = ref(false) // control additional info section visibility
const newTalent = ref({
	full_name: '',
	gender: '',
	email: '',
	phone: '',
	linkedin_profile: '',
	facebook_profile: '',
	zalo_profile: '',
	latest_company: '',
	total_years_of_experience: null,
	desired_role: '',
	source: 'Manually',
	position: '',
	current_city: '',
	// internal_rating: 0,
	interaction_notes: '',
	skills: [],
	current_status: 'Active',
	crm_status: 'New',
	resume: null,
})
const sourceOptions = ref([
	'Manually',
	'Zalo',
	'Facebook',
	'LinkedIn',
	'Referral',
	'Headhunter',
	'Nurturing Interaction',
	'Import Excel',
	'Import CV',
	'MBW ATS'
])

const crmStatusOptions = ref([
	'New',
	'Contacted',
	'Qualified',
	'Proposal',
	'Negotiation',
	'Closed Won',
	'Closed Lost',
	'On Hold'
])

// Filter state
const showFilters = ref(false)
const filterConditions = ref([])
const filters = ref({
	skills: '',
	source: '',
	crm_status: ''
})
const canCreate = permission.can("Mira Talent", "create")
const loading = computed(() => talentPoolStore.loading)
const skillInput = ref('')
const skillTags = ref([])
// Force reactivity by creating a reactive reference
const forceUpdate = ref(0)
// Track deleted talents to prevent them from reappearing
const deletedTalentIds = ref(new Set())

const talents = computed(() => {
	// Access forceUpdate to trigger reactivity
	forceUpdate.value
	// Filter out deleted talents
	return talentPoolStore.talents.filter(talent => 
		!deletedTalentIds.value.has(talent.name)
	)
})
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

const handleSearchInput = (event) => {
	// Clear any existing timeout
	if (searchTimeout.value) {
		clearTimeout(searchTimeout.value)
	}

	// Set a new timeout to fetch after user stops typing (500ms delay)
	searchTimeout.value = setTimeout(() => {
		// Reset to first page when searching
		talentPoolStore.pagination.page = 1
		talentPoolStore.setSearch(event)
		// Force refresh with updated search text
		talentPoolStore.fetchTalents({
			page: 1,
			limit: talentPoolStore.pagination.limit,
		})
	}, 500)
}

const handleRefresh = async () => {
	// Clear deleted tracking on manual refresh
	deletedTalentIds.value.clear()
	console.log('Manual refresh - cleared deleted talents tracking')
	
	await talentPoolStore.fetchTalents({
		page: talentPoolStore.pagination.page,
		limit: talentPoolStore.pagination.limit,
	})
	
	forceUpdate.value++
}

// Filter functions
const toggleFilters = () => {
	showFilters.value = !showFilters.value
}

// Handle conditions change
const onConditionsChange = (conditions) => {
	console.log('Conditions changed:', conditions)
	filterConditions.value = conditions
}

// Apply filters with conditions
const applyFilters = async () => {
	// Reset to first page when applying filters
	talentPoolStore.pagination.page = 1
	
	// Clear all filters first
	talentPoolStore.clearFilters()
	
	// Set conditions in store
	talentPoolStore.setConditions(filterConditions.value)
	
	// Fetch talents with new conditions
	await talentPoolStore.fetchTalents({
		page: 1,
		limit: talentPoolStore.pagination.limit,
		conditions: filterConditions.value
	})
}

// Clear all filters
const clearFilters = async () => {
	// Reset conditions
	filterConditions.value = []
	
	// Reset old filter values for backward compatibility
	filters.value = {
		skills: '',
		source: '',
		crm_status: ''
	}
	
	// Clear filters in store
	talentPoolStore.clearFilters()
	
	// Reset to first page
	talentPoolStore.pagination.page = 1
	
	// Fetch talents without filters
	await talentPoolStore.fetchTalents({
		page: 1,
		limit: talentPoolStore.pagination.limit
	})
}

const showUploadModal = ref(false)
const showBulkUploadModal = ref(false)
const showATSTalentSyncDialog = ref(false)
const showSyncHistoryModal = ref(false)
const showExportModal = ref(false)
const showDeleteDialog = ref(false)
const talentToDelete = ref(null)
const isDeleting = ref(false)
const showBulkDeleteDialog = ref(false)
const isBulkDeleting = ref(false)
const searchTimeout = ref(null)
const emailError = ref('')
const phoneError = ref('')
const isEmailValid = computed(() => {
	const email = newTalent.value.email
	if (!email) return true // Empty is valid until submit
	const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
	return emailRegex.test(email)
})

// Filter computed properties
const hasActiveFilters = computed(() => {
	return filterConditions.value.length > 0
})

const activeFilterCount = computed(() => {
	// Count actual filter conditions (exclude conjunction strings like 'and', 'or')
	const countConditions = (conditions) => {
		let count = 0
		for (const item of conditions) {
			if (typeof item === 'string') {
				// Skip conjunction strings ('and', 'or')
				continue
			} else if (Array.isArray(item)) {
				if (item.length === 3 && typeof item[0] === 'string' && item[0] !== '') {
					// This is a valid condition triplet [field, operator, value]
					count++
				} else {
					// This is a nested group, count recursively
					count += countConditions(item)
				}
			}
		}
		return count
	}
	
	return countConditions(filterConditions.value)
})

const processSkills = (skills) => {
	if (!skills) return []
	if (Array.isArray(skills)) return skills.join(',')
	return skills.replace('[','').replace(']','')
		.split(',')
		.map((skill) => decodeURIComponent(skill.trim()))
		.filter(Boolean)
}

const formatDate = (dateString) => {
	if (!dateString) return '-'
	
	const date = new Date(dateString)
	const now = new Date()
	
	// Get date parts without time for accurate comparison
	const dateOnly = new Date(date.getFullYear(), date.getMonth(), date.getDate())
	const nowOnly = new Date(now.getFullYear(), now.getMonth(), now.getDate())
	
	// Calculate difference in days
	const diffTime = nowOnly.getTime() - dateOnly.getTime()
	const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
	
	// If same date, show "Today"
	if (diffDays === 0) return 'Hôm nay'
	// If 1 day ago, show "Yesterday"  
	if (diffDays === 1) return 'Hôm qua'
	// If less than 7 days, show "X days ago"
	if (diffDays > 0 && diffDays < 7) return `${diffDays} ngày trước`
	
	// Otherwise show formatted date
	return date.toLocaleDateString('vi-VN', {
		day: '2-digit',
		month: '2-digit',
		year: 'numeric'
	})
}

const closeDialogOptions = () => {
	openDialogTalentOption.value = false
}

const openTalentForm = () => {
	showTalentForm.value = true
	showAdditionalInfo.value = false // Reset additional info section to closed
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
	newTalent.value.resume = file.file_url

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

const removeSkill = (index) => {
	skillTags.value.splice(index, 1)
}

const checkEmail = async () => {
	if (!newTalent.value.email) {
		emailError.value = ''
		return
	}

	// Validate email format first
	const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
	if (!emailRegex.test(newTalent.value.email)) {
		emailError.value = 'Please enter a valid email address'
		return
	}

	// Check for blacklist
	try {
		const result = await call('frappe.client.get_list', {
			doctype: 'Mira BlackList',
			filters: { email: newTalent.value.email },
			fields: ['name', 'email', 'tag'],
			limit: 1
		})

		if (result && result.length > 0) {
			const blacklistEntry = result[0]
			const tagInfo = blacklistEntry.tag ? ` (${blacklistEntry.tag})` : ''
			emailError.value = `⚠️ This email is in the blacklist${tagInfo}. Please verify before proceeding.`
			return
		}
	} catch (error) {
		console.error('Error checking blacklist:', error)
	}

	// Check for duplicate email
	try {
		const emailExists = await talentPoolStore.checkEmailExists(newTalent.value.email)
		if (emailExists) {
			emailError.value = 'This email is already in use. Please use a different email address.'
		} else {
			emailError.value = ''
		}
	} catch (error) {
		console.error('Error checking email:', error)
		emailError.value = ''
	}
}

/**
 * Validate phone number with extensible country support
 * @param {string} phoneNumber - Phone number to validate
 * @param {string} country - Country code (default: 'VN' for Vietnam)
 * @returns {Object} - { isValid: boolean, error: string }
 */
const validatePhoneNumber = (phoneNumber, country = 'VN') => {
	if (!phoneNumber || phoneNumber.trim() === '') {
		return { isValid: true, error: '' } // Phone is optional
	}

	// Remove all spaces and special characters except + for validation
	const cleanedPhone = phoneNumber.replace(/[\s\-()]/g, '')

	// Country-specific validation patterns
	const validationPatterns = {
		// Vietnam: 10-11 digits, or starts with +84
		VN: {
			patterns: [
				/^\+84[0-9]{9,10}$/, // +84 followed by 9-10 digits
				/^84[0-9]{9,10}$/, // 84 followed by 9-10 digits
				/^0[0-9]{9,10}$/, // Starts with 0, followed by 9-10 digits (total 10-11 digits)
				/^[0-9]{10,11}$/ // 10-11 digits
			],
			errorMessage: 'Số điện thoại không hợp lệ. Vui lòng nhập số điện thoại Việt Nam (10-11 số hoặc bắt đầu từ +84)'
		},
		// Add more countries here as needed
		// US: {
		//   patterns: [/^\+1[0-9]{10}$/, /^1[0-9]{10}$/, /^[0-9]{10}$/],
		//   errorMessage: 'Invalid US phone number. Please enter 10 digits or +1 followed by 10 digits'
		// },
		// ... other countries
	}

	// Get validation pattern for the specified country
	const countryValidation = validationPatterns[country]

	if (!countryValidation) {
		return {
			isValid: false,
			error: `Validation not supported for country: ${country}`
		}
	}

	// Check if phone matches any of the country's patterns
	const isValid = countryValidation.patterns.some(pattern => pattern.test(cleanedPhone))

	return {
		isValid,
		error: isValid ? '' : countryValidation.errorMessage
	}
}

// Phone validation handler
const checkPhoneNumber = () => {
	if (!newTalent.value.phone || newTalent.value.phone.trim() === '') {
		phoneError.value = ''
		return
	}

	const validation = validatePhoneNumber(newTalent.value.phone, 'VN')
	phoneError.value = validation.error
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

		// Check for blacklist
		try {
			const blacklistResult = await call('frappe.client.get_list', {
				doctype: 'Mira BlackList',
				filters: { email: newTalent.value.email },
				fields: ['name', 'email', 'tag'],
				limit: 1
			})

			if (blacklistResult && blacklistResult.length > 0) {
				const blacklistEntry = blacklistResult[0]
				const tagInfo = blacklistEntry.tag ? ` (${blacklistEntry.tag})` : ''
				showError(__(`This email is in the blacklist${tagInfo}. Cannot create talent with blacklisted email.`))
				return
			}
		} catch (error) {
			console.error('Error checking blacklist:', error)
		}

		// Check for duplicate email
		const emailExists = await talentPoolStore.checkEmailExists(newTalent.value.email)
		if (emailExists) {
			showError(__('This email is already in use. Please use a different email address.'))
			return
		}

		// Validate phone number if provided
		if (newTalent.value.phone && newTalent.value.phone.trim()) {
			const phoneValidation = validatePhoneNumber(newTalent.value.phone, 'VN')
			if (!phoneValidation.isValid) {
				showError(phoneValidation.error)
				return
			}
		}

		// Validate LinkedIn URL format if provided
		if (newTalent.value.linkedin_profile && newTalent.value.linkedin_profile.trim()) {
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
		}

		try {
			// Create FormData for file upload
			const formData = new FormData()

			console.log('newTalent', newTalent.value)

			// Get the resume file if it exists
			const resumeFile = newTalent.value.resume

			// Manually append each field to ensure they're included
			formData.append('full_name', newTalent.value.full_name || '')
			formData.append('gender', newTalent.value.gender || '')
			formData.append('email', newTalent.value.email || '')
			formData.append('phone', newTalent.value.phone || '')
			formData.append('linkedin_profile', newTalent.value.linkedin_profile || '')
			formData.append('facebook_profile', newTalent.value.facebook_profile || '')
			formData.append('zalo_profile', newTalent.value.zalo_profile || '')
			formData.append('latest_company', newTalent.value.latest_company || '')
			formData.append(
				'total_years_of_experience',
				newTalent.value.total_years_of_experience || '',
			)
			formData.append('desired_role', newTalent.value.desired_role || '')
			formData.append('source', newTalent.value.source || 'Manually')
			formData.append('position', newTalent.value.position || '')
			formData.append('current_city', newTalent.value.current_city || '')
			formData.append('interaction_notes', newTalent.value.interaction_notes || '')
			formData.append('skills', skillTags.value.join(', '))
			formData.append('current_status', newTalent.value.current_status || 'Active')
			formData.append('crm_status', newTalent.value.crm_status || 'New')

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
				gender: '',
				email: '',
				phone: '',
				linkedin_profile: '',
				facebook_profile: '',
				zalo_profile: '',
				latest_company: '',
				total_years_of_experience: null,
				desired_role: '',
				source: 'Manually',
				position: '',
				current_city: '',
				interaction_notes: '',
				skills: [],
				current_status: 'Active',
				crm_status: 'New',
				resume: null,
			}
			// Refresh the talents list
			await talentPoolStore.fetchTalents({
				page: talentPoolStore.pagination.page,
				limit: talentPoolStore.pagination.limit,
			})
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
	showSuccess(`Successfully imported ${result.success} talent(s)`)
	// Refresh the talents list to show newly imported talents
	await talentPoolStore.fetchTalents({
		page: talentPoolStore.pagination.page,
		limit: talentPoolStore.pagination.limit,
	})
	// Force reactivity update
	forceUpdate.value++
}

const openUploadMany = () => {
	console.log('Open upload many')
	openDialogTalentOption.value = false
	showBulkUploadModal.value = true
}

const syncFromATS = () => {
	openDialogTalentOption.value = false
	showATSTalentSyncDialog.value = true
}

const handleSyncSuccess = async () => {
	showSuccess(__('Sync started successfully. You will be notified when the process completes.'))
}

const handleBulkUploadSuccess = async () => {
	// Refresh the talents list when a new talent is created from bulk CV upload
	await talentPoolStore.fetchTalents({
		page: talentPoolStore.pagination.page,
		limit: talentPoolStore.pagination.limit,
	})
	forceUpdate.value++
}

const viewTalent = (talent) => {
	console.log('View talent', talent.name)
	router.push({ name: 'TalentDetail', params: { id: talent.name } })
}

const deleteTalent = (talent) => {
	talentToDelete.value = talent
	showDeleteDialog.value = true
}

const confirmDeleteTalent = async () => {
	if (!talentToDelete.value) return
	
	isDeleting.value = true
	try {
		// Call API to delete talent
		const response = await call('mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.delete_talent', {
			name: talentToDelete.value.name
		})
		
		if (response.status === 'success') {
			showSuccess(response.message || __('Talent deleted successfully'))
			showDeleteDialog.value = false
			talentToDelete.value = null
			// Refresh the talents list
			await talentPoolStore.fetchTalents({
				page: talentPoolStore.pagination.page,
				limit: talentPoolStore.pagination.limit,
			})
		} else {
			showError(response.message || __('Failed to delete talent'))
		}
	} catch (error) {
		console.error('Error deleting talent:', error)
		showError(__('An error occurred while deleting the talent'))
	} finally {
		isDeleting.value = false
	}
}

// Bulk delete function
const confirmBulkDelete = async () => {
	if (!selectedAllTalent.value.length) return
	
	isBulkDeleting.value = true
	try {
		// Extract talent names for the API call
		const talentNames = selectedAllTalent.value.map(talent => talent.name)
		
		// Call API to delete multiple talents
		const response = await call('mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.delete_multiple_talents', {
			names: talentNames
		})
		
		if (response.status === 'success') {
			showSuccess(response.message || __('Bulk delete request submitted successfully'))
			showBulkDeleteDialog.value = false
			// Clear selections
			selectedAllTalent.value = []
			// Refresh the talents list
			await talentPoolStore.fetchTalents({
				page: talentPoolStore.pagination.page,
				limit: talentPoolStore.pagination.limit,
			})
		} else {
			showError(response.message || __('Failed to submit bulk delete request'))
		}
	} catch (error) {
		console.error('Error bulk deleting talents:', error)
		showError(__('An error occurred while deleting the talents'))
	} finally {
		isBulkDeleting.value = false
	}
}

// Socket listener for bulk delete completion and sync completion
const setupSocketListeners = () => {
	$socket.on('bulk_remove_talent_complete', async (data) => {
		console.log('Bulk delete completed:', data)
		
		if (data.status === 'success') {
			if (data.queued > 0) {
				console.log('Bulk delete success - removing talents optimistically')
				console.log('Talents to remove:', data.queued_talents)
				
				// Add deleted talent IDs to global tracking
				if (data.queued_talents && Array.isArray(data.queued_talents)) {
					data.queued_talents.forEach(talentId => {
						deletedTalentIds.value.add(talentId)
						console.log(`Added talent ${talentId} to deleted list`)
					})
					
					// Update pagination total
					talentPoolStore.pagination.total -= data.queued_talents.length
					
					// Force UI update - computed property will automatically filter deleted talents
					forceUpdate.value++
					selectedAllTalent.value = []
					
					console.log('Optimistic update completed - deleted talents tracked')
					showSuccess(`Successfully deleted ${data.queued} talent(s)`)
				}
				
				// Polling mechanism to check if deletion is complete on server
				let pollCount = 0
				const maxPolls = 10 // Maximum 10 polls (30 seconds)
				
				const pollForDeletion = async () => {
					pollCount++
					console.log(`Polling attempt ${pollCount} to verify deletion...`)
					
					try {
						// Fetch fresh data from server (this will update the store)
						await talentPoolStore.fetchTalents({
							page: talentPoolStore.pagination.page,
							limit: talentPoolStore.pagination.limit,
						})
						
						// Check which deleted talents no longer exist on server
						const talentsStillOnServer = []
						const talentsReallyDeleted = []
						
						data.queued_talents.forEach(talentId => {
							const stillExists = talentPoolStore.talents.some(t => t.name === talentId)
							if (stillExists) {
								talentsStillOnServer.push(talentId)
							} else {
								talentsReallyDeleted.push(talentId)
							}
						})
						
						// Remove talents that are confirmed deleted from our tracking
						talentsReallyDeleted.forEach(talentId => {
							deletedTalentIds.value.delete(talentId)
							console.log(`Talent ${talentId} confirmed deleted on server`)
						})
						
						if (talentsStillOnServer.length > 0 && pollCount < maxPolls) {
							console.log(`${talentsStillOnServer.length} talents still exist on server, polling again in 3 seconds...`)
							setTimeout(pollForDeletion, 3000)
						} else {
							console.log('All deletions verified on server or max polls reached')
							forceUpdate.value++
						}
					} catch (error) {
						console.error('Error polling for deletion:', error)
					}
				}
				
				// Start polling after 5 seconds
				setTimeout(pollForDeletion, 5000)
			}
			if (data.failed > 0) {
				showError(`Failed to queue ${data.failed} talent(s) for deletion`)
			}
		} else {
			showError(data.message || 'Bulk delete operation failed')
		}
	})
	
	// Socket listener for sync completion
	$socket.on('candidate_sync_complete', async (data) => {
		console.log('Candidate sync completed:', data)
		
		if (data.sync_type === 'Candidate to Talent') {
			// Refresh talents list
			await talentPoolStore.fetchTalents({
				page: talentPoolStore.pagination.page,
				limit: talentPoolStore.pagination.limit,
			})
			
			// Force UI update to ensure reactivity
			forceUpdate.value++
			
			// Show notification based on status
			if (data.status === 'Completed') {
				showSuccess(`Đồng bộ hoàn tất! Đã xử lý ${data.success_count || 0} bản ghi thành công.`)
			} else if (data.status === 'Partially Completed') {
				showSuccess(`Đồng bộ hoàn tất một phần! Thành công: ${data.success_count || 0}, Thất bại: ${data.failed_count || 0}`)
			} else if (data.status === 'Failed') {
				showError(`Đồng bộ thất bại: ${data.details || 'Lỗi không xác định'}`)
			}
		}
	})
}

// Cleanup socket listeners
const cleanupSocketListeners = () => {
	if ($socket) {
		$socket.off('bulk_remove_talent_complete')
		$socket.off('candidate_sync_complete')
	}
}

// Build filters for export
const buildExportFilters = () => {
	const exportFilters = {}
	
	// Add search filter
	if (talentPoolStore.filters.search) {
		exportFilters.search = talentPoolStore.filters.search
	}
	
	// Add skills filter
	if (talentPoolStore.filters.skills) {
		exportFilters.skills = talentPoolStore.filters.skills
	}
	
	// Add source filter
	if (talentPoolStore.filters.source) {
		exportFilters.source = talentPoolStore.filters.source
	}
	
	// Add crm_status filter
	if (talentPoolStore.filters.crm_status) {
		exportFilters.crm_status = talentPoolStore.filters.crm_status
	}
	
	return exportFilters
}

onMounted(async () => {
	setupSocketListeners()
	await talentPoolStore.fetchTalents({
		page: talentPoolStore.pagination.page,
		limit: talentPoolStore.pagination.limit,
	})
})

onUnmounted(() => {
	if (searchTimeout.value) {
		clearTimeout(searchTimeout.value)
	}
	cleanupSocketListeners()
})
</script>
