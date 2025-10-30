<template>
	<div class="min-h-screen bg-gray-50">
		<LayoutHeader>
			<template #left-header>
				<Breadcrumbs :items="breadcrumbs" />
			</template>
			<template #right-header>
				<!-- Create Button -->
				<Button
					v-if="viewMode == 'card'"
					variant="solid"
					theme="gray"
					@click="showCreateForm = true"
					:loading="loading"
					class=""
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
								d="M12 6v6m0 0v6m0-6h6m-6 0H6"
							></path>
						</svg>
					</template>
					{{ __('Create Pool') }}
				</Button>
				<Button
					v-if="viewMode == 'list'"
					variant="solid"
					theme="gray"
					@click="openCreateDialog"
					:loading="loading"
					class=""
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
								d="M12 6v6m0 0v6m0-6h6m-6 0H6"
							></path>
						</svg>
					</template>
					{{ __('Create Talent') }}
				</Button>
			</template>
		</LayoutHeader>

		<!-- Main Content -->
		<div class="container mx-auto px-6 py-6">
			<!-- Actions Bar -->
			<div
				class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4"
			>
				<!-- Search -->
				<div class="flex items-center space-x-2">
					<div v-if="viewMode == 'card'" class="flex-1 w-80">
						<FormControl
							v-model="searchQuery"
							type="text"
							:placeholder="__('Search talent pools...')"
							:prefix-icon="'search'"
							:suffix-icon="searchQuery ? 'x' : undefined"
							@input="handleSearch"
							@click-suffix="clearSearch"
							:class="{ 'animate-pulse': isSearching }"
							variant="outline"
						/>
					</div>

					<div v-if="viewMode == 'list'" class="flex items-center space-x-2">
						<div class="w-64">
							<Autocomplete
								:options="uniqueSegmentTypes"
								v-model="selectedSegmentType"
								@update:modelValue="handleSegmentTypeFilter"
								:placeholder="__('Select type')"
								class=""
							>
							</Autocomplete>
						</div>
						<div>
							<Button
								variant="outline"
								@click="showAdvancedFilters = !showAdvancedFilters"
							>
								<template #prefix>
									<svg
										class="w-4 h-4"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"
										/>
									</svg>
								</template>
								{{ __('Advanced Filters') }}
								<template #suffix>
									<svg
										v-if="showAdvancedFilters"
										class="w-4 h-4"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M5 15l7-7 7 7"
										/>
									</svg>
									<svg
										v-else
										class="w-4 h-4"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M19 9l-7 7-7-7"
										/>
									</svg>
								</template>
							</Button>
						</div>
					</div>
				</div>

				<!-- Actions -->
				<div class="flex items-center space-x-4">
					<!-- View mode toggle -->
					<div class="flex rounded-md">
						<button
							@click="viewMode = 'card'"
							:class="[
								viewMode === 'card'
									? 'bg-black text-white'
									: 'bg-white text-gray-700 hover:text-gray-500',
								'relative inline-flex items-center px-4 py-1.5 rounded-l-md border border-gray-300 border-l-0 text-sm font-medium focus:z-10 focus:outline-none focus:ring-1 focus:ring-black focus:border-black',
							]"
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-4 w-4 mr-2"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"
								/>
							</svg>
							{{ __('Card') }}
						</button>
						<button
							@click="viewMode = 'list'"
							:class="[
								viewMode === 'list'
									? 'bg-black text-white'
									: 'bg-white text-gray-700 hover:text-gray-500',
								'relative inline-flex items-center px-4 py-1.5 rounded-r-md border border-gray-300 text-sm font-medium focus:z-10 focus:outline-none focus:ring-1 focus:ring-black focus:border-black',
							]"
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-4 w-4 mr-2"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M4 6h16M4 10h16M4 14h16M4 18h16"
								/>
							</svg>
							{{ __('List') }}
						</button>
					</div>

					<!-- Refresh Button -->
					<Button
						variant="outline"
						theme="gray"
						@click="handleRefresh"
						:loading="loading"
						class="flex items-center"
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
					<Button
						v-if="viewMode == 'list' && selectedNames.length > 0"
						variant="outline"
						theme="gray"
						@click="showEditManyTalentPool = true"
						:loading="loading"
						class="flex items-center"
					>
						<template #prefix>
							<FeatherIcon name="edit" class="w-4 h-4" />
						</template>
						{{ __('Quick edit') }}
					</Button>
				</div>
			</div>

      <!-- Advanced Filters (Collapsible) -->
				<div v-if="showAdvancedFilters" class="py-2 border-t border-slate-200">
					<div class="grid grid-cols-1 md:grid-cols-4 gap-4">
						<FormControl
							type="text"
							placeholder="Search talent name..."
						/>
					</div>
				</div>

			<!-- Loading & Empty State & Main Content -->
			<template v-if="loading && !segments.length">
				<Loading text="Loading talent pools..." />
			</template>
			<template v-else-if="!loading && !segments.length">
				<div class="text-center py-16">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-24 w-24 text-gray-300 mx-auto mb-4"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="1"
							d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
						></path>
					</svg>
					<h3 class="text-xl font-medium text-gray-900 mb-2">
						{{ __('No talent pools yet') }}
					</h3>
					<p class="text-gray-500 mb-6">
						{{ __('Create your first talent pool to start managing candidates') }}
					</p>
					<Button variant="solid" theme="gray" @click="showCreateForm = true">
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
									d="M12 6v6m0 0v6m0-6h6m-6 0H6"
								></path>
							</svg>
						</template>
						{{ __('Create Your First Pool') }}
					</Button>
				</div>
			</template>
			<template v-else>
				<!-- Segments View based on mode -->
				<TalentSegmentCardView
					v-if="viewMode === 'card'"
					:segments="segmentsForCurrentPage"
					:loading="loading"
					@view-details="handleViewDetails"
					@edit="handleEdit"
					@delete="handleDelete"
					@create="showCreateForm = true"
				/>

				<!-- Pagination -->
				<div v-if="totalPages > 1 && viewMode === 'card'" class="mt-8">
					<div
						class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6 rounded-lg shadow"
					>
						<div class="flex-1 flex justify-between sm:hidden">
							<Button
								variant="outline"
								theme="gray"
								@click="previousPage"
								:disabled="pagination.currentPage <= 1"
							>
								{{ __('Previous') }}
							</Button>
							<Button
								variant="outline"
								theme="gray"
								@click="nextPage"
								:disabled="pagination.currentPage >= totalPages"
							>
								{{ __('Next') }}
							</Button>
						</div>
						<div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
							<div>
								<p class="text-sm text-gray-700">
									{{ __('Showing') }}
									<span class="font-medium">{{ paginationStart }}</span>
									{{ __('to') }}
									<span class="font-medium">{{ paginationEnd }}</span>
									{{ __('of') }}
									<span class="font-medium">{{ totalSegments }}</span>
									{{ __('results') }}
								</p>
							</div>
							<div>
								<nav
									class="relative z-0 inline-flex rounded-md -space-x-px"
									aria-label="Pagination"
								>
									<!-- Previous Button -->
									<button
										@click="previousPage"
										:disabled="pagination.currentPage <= 1"
										class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
									>
										<svg
											class="h-5 w-5"
											xmlns="http://www.w3.org/2000/svg"
											viewBox="0 0 20 20"
											fill="currentColor"
										>
											<path
												fill-rule="evenodd"
												d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
												clip-rule="evenodd"
											/>
										</svg>
									</button>

									<!-- Page Numbers -->
									<button
										v-for="page in visiblePages"
										:key="page"
										@click="goToPage(page)"
										:class="[
											'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
											page === pagination.currentPage
												? 'z-10 bg-indigo-50 border-indigo-500 text-indigo-600'
												: 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50',
										]"
									>
										{{ page }}
									</button>

									<!-- Next Button -->
									<button
										@click="nextPage"
										:disabled="pagination.currentPage >= totalPages"
										class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
									>
										<svg
											class="h-5 w-5"
											xmlns="http://www.w3.org/2000/svg"
											viewBox="0 0 20 20"
											fill="currentColor"
										>
											<path
												fill-rule="evenodd"
												d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
												clip-rule="evenodd"
											/>
										</svg>
									</button>
								</nav>
							</div>
						</div>
					</div>
				</div>

				<div v-else-if="viewMode === 'list'" class="overflow-hidden">
					<!-- Loading State -->
					<div v-if="loading" class="flex justify-center items-center py-12">
						<div
							class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"
						></div>
					</div>

					<!-- Empty State -->
					<div v-else-if="!talents.length" class="text-center py-16">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-24 w-24 text-gray-300 mx-auto mb-4"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="1"
								d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
							/>
						</svg>
						<h3 class="text-lg font-medium text-gray-900 mb-1">
							No talent segments found
						</h3>
						<p class="text-gray-500">Get started by creating a new talent segment.</p>
					</div>

					<!-- Table View -->
					<div v-else class="bg-white rounded-lg border border-gray-200 overflow-hidden">
						<div class="overflow-x-auto">
							<table class="min-w-full divide-y divide-gray-200">
								<!-- Table Header -->
								<thead class="bg-gray-50">
									<tr>
										<th class="w-12 p-3">
											<input
												type="checkbox"
												class="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
												:checked="
													selectedAllTalent.length === talents.length &&
													talents.length > 0
												"
												:indeterminate="
													selectedAllTalent.length > 0 &&
													selectedAllTalent.length < talents.length
												"
												@change="toggleSelectAllTalent"
											/>
										</th>
										<th
											class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
										>
											Full Name
										</th>
										<th
											class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
										>
											Contact Email
										</th>
										<th
											class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
										>
											Contact Phone
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
											class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
										>
											Actions
										</th>
									</tr>
								</thead>

								<tbody class="bg-white divide-y divide-gray-200">
									<tr
										v-for="talent in paginatedTalents"
										:key="talent.name"
										class="hover:bg-gray-50 transition-colors duration-200"
									>
										<td class="p-3 text-center">
											<input
												type="checkbox"
												class="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
												:checked="
													selectedAllTalent.some(
														(t) => t.name === talent.name,
													)
												"
												@change="toggleSelectTalent(talent)"
											/>
										</td>
										<td
											class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
										>
											{{ talent.full_name }}
										</td>
										<td
											class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
										>
											{{ talent.email }}
										</td>
										<td
											class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
										>
											{{ talent.phone }}
										</td>
										<td class="px-6 py-4 text-sm text-gray-900">
											<div class="flex flex-wrap gap-1">
												<span
													v-for="skill in processSkills(talent.skills)"
													:key="skill"
													class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
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
											<span
												:class="[
													'px-2 inline-flex text-xs leading-5 font-semibold rounded-full',
													getStatusTheme(talent.current_status),
												]"
											>
												{{ talent.source || 'Not Specified' }}
											</span>
										</td>
										<td
											class="px-6 py-4 whitespace-nowrap text-sm font-medium"
										>
											<div class="flex items-center space-x-2">
												<button
													class="inline-flex items-center justify-center w-8 h-8 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-full transition-colors duration-200"
													@click.stop="handleViewTalent(talent)"
													:title="__('View')"
												>
													<FeatherIcon name="eye" class="h-4 w-4" />
												</button>
												<!-- <button
                          class="inline-flex items-center justify-center w-8 h-8 text-gray-600 hover:text-gray-800 hover:bg-gray-50 rounded-full transition-colors duration-200"
                          @click.stop="handleEditTalent(talent)" :title="__('Edit')">
                          <FeatherIcon name="edit" class="h-4 w-4" />
                        </button> -->
											</div>
										</td>
									</tr>
								</tbody>
							</table>
						</div>

						<!-- Pagination -->
						<div
							v-if="paginationTalent.total > 0"
							class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200"
						>
							<!-- Items per page selector -->
							<div class="flex items-center space-x-2">
								<span class="text-sm text-gray-700">Items per page:</span>
								<div class="w-20">
									<select
										v-model="paginationTalent.limit"
										@change="changeItemsPerPageTalent"
										class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
									>
										<option
											v-for="option in itemsPerPageOptions"
											:key="option"
											:value="option"
										>
											{{ option }}
										</option>
									</select>
								</div>
							</div>

							<!-- Page info -->
							<div class="text-sm text-gray-600">
								Showing {{ paginationTalent.showing_from }} to
								{{ paginationTalent.showing_to }} of
								{{ paginationTalent.total }} talent
							</div>

							<!-- Page navigation -->
							<div class="flex items-center space-x-1">
								<button
									:disabled="!paginationTalent.has_prev"
									@click="goToTalentPage(1)"
									class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
									:title="__('First page')"
								>
									<FeatherIcon name="chevrons-left" class="h-4 w-4" />
								</button>

								<button
									:disabled="!paginationTalent.has_prev"
									@click="goToTalentPage(paginationTalent.page - 1)"
									class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
									:title="__('Previous page')"
								>
									<FeatherIcon name="chevron-left" class="h-4 w-4" />
								</button>

								<span class="mx-3 text-sm text-gray-700">
									Page {{ paginationTalent.page }} /
									{{
										Math.ceil(paginationTalent.total / paginationTalent.limit)
									}}
								</span>

								<button
									:disabled="!paginationTalent.has_next"
									@click="goToTalentPage(paginationTalent.page + 1)"
									class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
									:title="__('Next page')"
								>
									<FeatherIcon name="chevron-right" class="h-4 w-4" />
								</button>

								<button
									:disabled="!paginationTalent.has_next"
									@click="
										goToTalentPage(
											Math.ceil(
												paginationTalent.total / paginationTalent.limit,
											),
										)
									"
									class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
									:title="__('Last page')"
								>
									<FeatherIcon name="chevrons-right" class="h-4 w-4" />
								</button>
							</div>
						</div>
					</div>
				</div>
			</template>

			<!-- Success/Error Toast -->
			<div
				v-if="toast.show"
				:class="[
					'fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg transform transition-all duration-300',
					toast.type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white',
				]"
			>
				<div class="flex items-center">
					<svg
						v-if="toast.type === 'success'"
						class="h-5 w-5 mr-2"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M5 13l4 4L19 7"
						></path>
					</svg>
					<svg
						v-else
						class="h-5 w-5 mr-2"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M6 18L18 6M6 6l12 12"
						></path>
					</svg>
					<span>{{ toast.message }}</span>
				</div>
			</div>
		</div>

		<!-- Create Options Dialog -->
		<Dialog
			v-model="openDialogTalent"
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

					<!-- Upload Single Profile Talent -->
					<div
						@click="openUploadSinge"
						class="border border-gray-200 rounded-lg p-4 cursor-pointer hover:border-blue-400 hover:shadow-sm transition-all"
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
										d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
									/>
								</svg>
							</div>
							<h4 class="font-medium text-gray-900">
								{{ __('Upload Single Profile Talent') }}
							</h4>
							<p class="text-xs text-gray-500 mt-1">
								{{ __('Upload profile and AI extracts data') }}
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
								{{ __('Upload Profiles Talent') }}
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
						@click="closeCreateOptions"
						class="px-4"
					>
						{{ __('Cancel') }}
					</Button>
				</div>
			</template>
		</Dialog>

		<!-- Edit Talent Pool Dialog -->
		<Dialog
			v-model="showDialogTalentPool"
			:options="{
				size: '2xl',
				title: __('Edit Talent Pool'),
			}"
		>
			<template #body-content>
				<div class="space-y-4">
					<!-- Talent Information -->
					<div class="space-y-2">
						<h3 class="text-lg font-medium text-gray-900">
							{{ __('Talent Information') }}
						</h3>
						<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
							<FormControl
								v-model="talentDetails.full_name"
								:label="__('Full Name')"
								type="text"
								required
							/>
							<FormControl
								v-model="talentDetails.contact_email"
								:label="__('Email')"
								type="email"
								required
							/>
							<FormControl
								v-model="talentDetails.contact_phone"
								:label="__('Phone')"
								type="tel"
							/>
							<FormControl
								v-model="matchScore"
								:label="__('Match Score')"
								type="number"
								min="0"
								max="100"
							/>
						</div>
					</div>

					<!-- Segment Assignment -->
					<div class="space-y-2">
						<h3 class="text-lg font-medium text-gray-900">
							{{ __('Segment Assignment') }}
						</h3>
						<Autocomplete
							v-model="selectedSegmentTypeEdit"
							:options="uniqueSegmentTypes"
							:placeholder="__('Select a segment')"
							required
						/>
					</div>
				</div>
			</template>
			<template #actions>
				<div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
					<Button
						variant="outline"
						theme="gray"
						@click="showDialogTalentPool = false"
						:disabled="loading"
					>
						{{ __('Cancel') }}
					</Button>
					<Button
						variant="solid"
						theme="gray"
						@click="updateTalentAndPool"
						:loading="loading"
					>
						{{ __('Save Changes') }}
					</Button>
				</div>
			</template>
		</Dialog>

		<!-- Edit many talent pool -->
		<Dialog
			v-model="showEditManyTalentPool"
			:options="{
				size: '2xl',
				title: __('Edit many talent pool'),
			}"
		>
			<template #body-content>
				<Autocomplete
					v-model="selectedSegmentTypeEdit"
					:options="uniqueSegmentTypes"
					:placeholder="__('Select a segment')"
					required
				/>
			</template>
			<template #actions>
				<div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
					<Button
						variant="outline"
						theme="gray"
						@click="showEditManyTalentPool = false"
						:disabled="loading"
					>
						{{ __('Cancel') }}
					</Button>
					<Button
						variant="solid"
						theme="gray"
						@click="updateManyTalentPool"
						:loading="loading"
					>
						{{ __('Save Changes') }}
					</Button>
				</div>
			</template>
		</Dialog>

		<!-- Create/Edit Dialog - New Component -->
		<TalentPoolDialog
			v-model="showCreateForm"
			:segment="editingSegment"
			@success="handleDialogSuccess"
			@cancel="handleFormClose"
		/>

		<!-- Delete Confirmation Dialog -->
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
											deletingSegment?.title
										}}"? {{ __('This actioncannotbe undone.') }}
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
								placeholder="username"
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

					<!-- Internal Rating -->
					<!-- <div>
        <label class="block text-sm font-medium text-gray-700">Internal Rating</label>
        <div class="mt-1 flex space-x-2">
          <button
            v-for="rating in 5"
            :key="rating"
            type="button"
            @click="newTalent.internal_rating = rating"
            :class="[
              'h-8 w-8 rounded-full flex items-center justify-center',
              newTalent.internal_rating >= rating 
                ? 'bg-yellow-400 text-white' 
                : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
            ]"
          >
            {{ rating }}
          </button>
        </div>
      </div> -->

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
						Save Talent
					</button>
				</div>
			</template>
		</Dialog>

		<!-- Upload Single Talent -->
		<Dialog
			v-model="showSingleTalentDialog"
			:options="{
				title: 'Upload Single Talent Profile',
				size: 'xl',
			}"
			:disableOutsideClickToClose="true"
		>
			<template #body-content>
				<div class="space-y-4 p-4">
						<!-- File Upload Section -->
						<div 
							v-if="!uploadedFile"
							class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center"
						>
						<div class="space-y-2">
							<FileUploader
								:fileTypes="['.pdf']"
								:maxFileSize="10 * 1024 * 1024"
								@success="handleFileUpload"
								@error="handleFileUploadError"
							>
								<template #default="{ openFileSelector }">
									<div @click="openFileSelector" class="space-y-2">
										<div class="flex justify-center">
											<svg
												class="h-12 w-12 text-gray-400"
												fill="none"
												viewBox="0 0 24 24"
												stroke="currentColor"
											>
												<path
													stroke-linecap="round"
													stroke-linejoin="round"
													stroke-width="2"
													d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
												/>
											</svg>
										</div>
										<p class="text-sm text-gray-600">
											<button
												type="button"
												class="font-medium text-blue-600 hover:text-blue-500"
											>
												Upload a file
											</button>
											or drag and drop
										</p>
										<p class="text-xs text-gray-500">PDF up to 10MB</p>
									</div>
								</template>
							</FileUploader>
						</div>
					</div>

					<!-- Uploaded File Display -->
					<div
						v-if="uploadedFile"
						class="bg-green-50 border border-green-200 rounded-lg p-4"
					>
						<div class="flex items-center justify-between">
							<div class="flex items-center space-x-3">
								<div class="flex-shrink-0">
									<svg
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
								<div class="flex-1 min-w-0">
									<p class="text-sm font-medium text-green-900">
										{{ uploadedFile.name }}
									</p>
									<p class="text-xs text-green-700">
										{{ formatFileSize(uploadedFile.size) }} • Uploaded successfully
									</p>
								</div>
							</div>
							<button
								@click="removeUploadedFile"
								:disabled="isProcessing"
								class="flex-shrink-0 text-green-600 hover:text-green-800 disabled:opacity-50 disabled:cursor-not-allowed"
							>
								<svg
									class="h-5 w-5"
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
							</button>
						</div>
					</div>

					<!-- Error Message -->
					<div v-if="errorMessage" class="p-4 bg-red-50 text-red-700 text-sm rounded-lg">
						{{ errorMessage }}
					</div>

					<!-- Extracted Data Form (will be shown after processing) -->
					<div v-if="extractedData" class="space-y-4">
						<h3 class="text-lg font-medium text-gray-900">Extracted Information</h3>
						<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
							<!-- Full Name -->
							<div>
								<label class="block text-sm font-medium text-gray-700"
									>Full Name</label
								>
								<input
									type="text"
									v-model="extractedData.full_name"
									class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
								/>
							</div>

							<!-- Email -->
							<div>
								<label class="block text-sm font-medium text-gray-700"
									>Email</label
								>
								<input
									type="email"
									v-model="extractedData.email"
									class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
								/>
							</div>

							<!-- Phone -->
							<div>
								<label class="block text-sm font-medium text-gray-700"
									>Phone</label
								>
								<input
									type="tel"
									v-model="extractedData.phone"
									class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
								/>
							</div>

							<!-- Skills (comma-separated) -->
							<div class="md:col-span-2">
								<label class="block text-sm font-medium text-gray-700"
									>Skills</label
								>
								<input
									type="text"
									v-model="extractedData.skills"
									class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
									placeholder="e.g., JavaScript, Python, Project Management"
								/>
							</div>

							<!-- Experience -->
							<div class="md:col-span-2">
								<label class="block text-sm font-medium text-gray-700"
									>Experience</label
								>
								<textarea
									v-model="extractedData.experience"
									rows="3"
									class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
									placeholder="Work experience details..."
								></textarea>
							</div>
						</div>

						<!-- Action Buttons -->
						<div class="flex justify-end space-x-3 pt-4">
							<button
								type="button"
								@click="saveTalent"
								class="inline-flex justify-center rounded-md border border-transparent bg-blue-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
							>
								Save Talent
							</button>
						</div>
					</div>
				</div>
			</template>
		</Dialog>

		<!-- Full Screen Processing Overlay (Outside Dialog using Teleport) -->
		<Teleport to="body">
			<div
				v-if="isProcessing && showSingleTalentDialog"
				class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center"
				style="z-index: 99999;"
				@click.stop
			>
				<div class="bg-white rounded-lg p-8 shadow-2xl">
					<div class="flex flex-col items-center space-y-4">
						<div
							class="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-500"
						></div>
						<div class="text-center">
							<p class="text-lg font-medium text-gray-900">
								{{ __('Đang phân tích Resume với AI') }}
							</p>
							<p class="text-sm text-gray-600 mt-2">
								{{ __('Đang trích xuất thông tin từ Resume của bạn...') }}
							</p>
						</div>
					</div>
				</div>
			</div>
		</Teleport>

		<UploadExcelTalentModal
			v-model="showUploadModal"
			@created="handleTalentCreated"
			@close="closeUploadModal"
		/>
		<BulkCVUploadModal v-model="showBulkUploadModal" />
	</div>
	<ToastContainer />
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted, h, reactive, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useTalentSegmentStore } from '@/stores/talentSegment'
import {
	Button,
	Dialog,
	Dropdown,
	FeatherIcon,
	FormControl,
	Breadcrumbs,
	Autocomplete,
	createResource,
	FileUploader,
} from 'frappe-ui'
import TalentSegmentForm from '@/components/talent-segment/TalentSegmentForm.vue'
import TalentPoolDialog from '@/components/talent-segment/TalentPoolDialog.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
// import Autocomplete from '@/components/frappe-ui/Autocomplete.vue'
import TalentSegmentCardView from '@/components/talent-segment/TalentSegmentCardView.vue'
import TalentSegmentListView from '@/components/talent-segment/TalentSegmentListView.vue'
import Loading from '@/components/Loading.vue'
import { ToastContainer } from '@/components/shared'
import { useToast } from '@/composables/useToast'
import { useTalentStore } from '@/stores/talent'
import UploadExcelTalentModal from '@/components/UploadExcelTalentModal.vue'
import BulkCVUploadModal from '@/components/BulkCVUploadModal.vue'

const showUploadModal = ref(false)
const talentStore = useTalentStore()
const toastMessage = useToast()
const router = useRouter()

const { showToast, showSuccess, showError } = useToast()
import { useTalentPoolStore } from '@/stores/talentPool'

// Refs
const talentPoolStore = useTalentPoolStore()
const talentSegmentStore = useTalentSegmentStore()
let title = __('Talent Pools')
const breadcrumbs = [{ label: title, route: { name: 'TalentSegments' } }]

const fileInput = ref(null)
const uploadedFile = ref(null)
const isProcessing = ref(false)
const errorMessage = ref('')
const extractedData = ref(null)
const showAdvancedFilters = ref(false)

const showSingleTalentDialog = ref(false)
const showBulkUploadModal = ref(false)
const showDialogTalentPool = ref(false)
const showEditManyTalentPool = ref(false)
// Use filtered talent pools from store
const talentPools = computed(() => talentPoolStore.filteredTalentPools)
const uniqueSegmentTypes = computed(() => talentPoolStore.uniqueSegmentTypes)
const selectedSegmentType = ref('')
const selectedSegmentTypeEdit = ref('')
const openDialogTalent = ref(false)

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

const removeResume = () => {
	if (confirm('Are you sure you want to remove this resume?')) {
		if (newTalent.value.resume?.url) {
			URL.revokeObjectURL(newTalent.value.resume.url)
		}
		newTalent.value.resume = ''
		showSuccess('Resume removed successfully!')
	}
}

// Handle file selection
const handleFileChange = (event) => {
	const file = event.target.files[0]
	if (file) {
		handleFileUpload(file)
	}
}

// Handle file upload
const handleFileUpload = async (file) => {
	console.log('File uploaded successfully:', file)
	
	// Store uploaded file info
	uploadedFile.value = {
		name: file.file_name || file.name,
		url: file.file_url || file.url,
		size: file.file_size || file.size
	}

	// Extract CV with the correct file name
	extractCV(file.name)
}

// Extract CV using the provided function
const extractCV = async (fileName) => {
	console.log('Starting Resume extraction for:', fileName)

	loadingFunctions.setLoading({
		title: 'Đang phân tích Resume',
		message: 'AI đang trích xuất thông tin từ Resume của bạn...',
		showProgress: false,
	})

	isProcessing.value = true
	errorMessage.value = ''

	const extractCVResource = createResource({
		url: 'mbw_mira.api.ai.extract_cv_url',
		params: {
			file_name: fileName,
		},
		onSuccess(data) {
			console.log('Resume extraction successful:', data)
			if (data && data.data) {
				// viết tiếp vào đây xử lý map data để gán dữ liệu vào extractedData
				extractedData.value = mapExtractedDataToForm(data.data)

				// Cập nhật form nếu cần
				if (extractedData.value) {
					newTalent.value = {
						...newTalent.value,
						...extractedData.value,
					}
				}
			} else {
				errorMessage.value = 'No data returned from Resume extraction'
			}
			isProcessing.value = false
			loadingFunctions.clearLoading()
		},
		onError(error) {
			console.error('Error extracting Resume:', error)
			errorMessage.value =
				error.messages?.[0] || error.message || 'Failed to extract Resume information'
			isProcessing.value = false
			loadingFunctions.clearLoading()
		},
		auto: true,
	})
}

// Thêm hàm này cùng cấp với các hàm khác trong component
const mapExtractedDataToForm = (apiData) => {
	if (!apiData) return null

	// Xử lý skills
	const processSkills = (skills) => {
		if (!skills || !Array.isArray(skills)) return []

		// Create an array to store all skill names
		const allSkills = []

		skills.forEach((skill) => {
			if (skill.details) {
				// Split skills by comma, trim whitespace, and add to the array
				const skillList = skill.details
					.split(',')
					.map((s) => s.trim())
					.filter((s) => s.length > 0)

				allSkills.push(...skillList)
			}
		})

		return allSkills
	}

	// Map dữ liệu từ API sang form data
	const mappedData = {
		full_name: apiData.personal_info?.can_full_name || '',
		email: apiData.personal_info?.can_email || '',
		phone: apiData.personal_info?.can_phone || '',
		current_city: apiData.personal_info?.address || '',
		education: apiData.education,
		work_experience:
			apiData.work_experience?.map((exp) => ({
				company: exp.work_experience_place || '',
				job_title: exp.work_experience_role || '',
				start_date: exp.work_experience_start || '',
				end_date: exp.work_experience_end || '',
				description: exp.responsibilities?.join('\n• ') || '',
			})) || [],
		skills: processSkills(apiData.skills),
		// Giữ nguyên các phần khác
		projects:
			apiData.projects
				?.map((proj) => ({
					name: proj.projects_name || '',
					description: proj.descriptions || '',
					technologies: proj.technologies?.filter((t) => t) || [],
				}))
				.filter((proj) => proj.name) || [],
		activities:
			apiData.activities?.map((act) => ({
				organization: act.organization || '',
				position: act.position || '',
				start_date: act.start_date || '',
				end_date: act.end_date || '',
				description: act.descriptions || '',
			})) || [],
	}

	return mappedData
}

const handleTalentCreated = async (result) => {
	showSuccess(`Successfully created ${result.success} talent`)
	await talentStore.fetchTalents()
}

const closeUploadModal = () => {
	showUploadModal.value = false
}

const openUploadModal = () => {
	openDialogTalent.value = false
	showUploadModal.value = true
}

const openUploadSinge = () => {
	openDialogTalent.value = false
	showSingleTalentDialog.value = true
}

const openUploadMany = () => {
	openDialogTalent.value = false
	showBulkUploadModal.value = true
}

// Format file size helper
const formatFileSize = (bytes) => {
	if (!bytes) return '0 B'
	const k = 1024
	const sizes = ['B', 'KB', 'MB', 'GB']
	const i = Math.floor(Math.log(bytes) / Math.log(k))
	return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Remove uploaded file
const removeUploadedFile = () => {
	uploadedFile.value = null
	extractedData.value = null
	errorMessage.value = ''
}

// Close single talent dialog and reset state
const closeSingleTalentDialog = () => {
	showSingleTalentDialog.value = false
	uploadedFile.value = null
	extractedData.value = null
	errorMessage.value = ''
	isProcessing.value = false
}

const showTalentForm = ref(false)
const newTalent = ref({
	full_name: '',
	email: '',
	phone: '',
	linkedin_profile: '',
	facebook_profile: '',
	skills: [],
	source: 'NEW',
})
const skillInput = ref('')
const skillTags = ref([])

const emailError = ref('')
const isEmailValid = computed(() => {
	const email = newTalent.value.email
	if (!email) return true // Empty is valid until submit
	const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
	return emailRegex.test(email)
})

const checkEmail = async () => {
	if (!newTalent.value.email) {
		emailError.value = ''
		return
	}

	if (!isEmailValid.value) {
		emailError.value = 'Please enter a valid email address'
		return
	}

	try {
		const exists = await talentStore.checkEmailExists(newTalent.value.email)
		emailError.value = exists ? 'This email is already in use' : ''
	} catch (error) {
		console.error('Error checking email:', error)
		emailError.value = ''
	}
}

const talents = computed(() => talentStore.talents)
// const paginationTalent = computed(() => talentStore.pagination)
const filtersTalent = computed(() => talentStore.filters)
const statisticsTalent = computed(() => talentStore.statistics)

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

// Add these methods to your component
const openTalentForm = () => {
	// Reset form
	newTalent.value = {
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
	}
	skillTags.value = []
	skillInput.value = ''
	emailError.value = ''

	// Close the create options dialog and open the form
	openDialogTalent.value = false
	showTalentForm.value = true
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

const handleTalentSubmit = async () => {
	try {
		// Validate required fields
		if (!newTalent.value.full_name) {
			showError('Full name is required')
			return
		}

		if (!newTalent.value.email) {
			showError('Email is required')
			return
		}

		// Validate email format
		const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
		if (!emailRegex.test(newTalent.value.email)) {
			showError('Please enter a valid email address')
			return
		}

		// Check for duplicate email
		const emailExists = await talentStore.checkEmailExists(newTalent.value.email)
		if (emailExists) {
			showError('This email is already in use. Please use a different email address.')
			return
		}

		// Validate required fields
		if (!newTalent.value.linkedin_profile) {
			showError('LinkedIn profile is required')
			return
		}

		// Validate LinkedIn URL format
		try {
			const url = new URL(newTalent.value.linkedin_profile)
			if (!url.hostname.includes('linkedin.com')) {
				showError(
					'Please enter a valid LinkedIn profile URL (e.g., https://linkedin.com/in/username)',
				)
				return
			}
		} catch (e) {
			showError('Please enter a valid URL for LinkedIn profile')
			return
		}

		if (
			newTalent.value.total_years_of_experience === null ||
			newTalent.value.total_years_of_experience === ''
		) {
			showError('Total years of experience is required')
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
			await talentStore.createTalent(formDataObject)

			// Show success message
			showSuccess('Talent created successfully!')

			// Close the form
			showTalentForm.value = false

			// Refresh the talents list
			await fetchTalents()

			// Reset the form
			// openTalentForm();
		} catch (error) {
			console.error('Error creating talent:', error)
			showError(error.message || 'Failed to create talent. Please try again.')
		}
	} catch (error) {
		console.error('Error creating talent:', error)
		showError(error.message || 'Failed to create talent. Please try again.')
	}
}

const saveTalent = async () => {
	try {
		const formData = new FormData()

		console.log('extractedData', extractedData.value)
		formData.append('full_name', extractedData.value.full_name || '')
		formData.append('email', extractedData.value.email || '')
		formData.append('phone', extractedData.value.phone || '')
		formData.append('skills', extractedData.value.skills || '')
		formData.append('source', 'NEW')

		// Convert FormData to a plain object
		const formDataObject = Object.fromEntries(formData)

		console.log('Submitting talent data:', formDataObject)

		// Call the API to create the talent with the plain object
		await talentStore.createTalent(formDataObject)

		// Show success message
		showSuccess('Talent created successfully!')

		// Close the form
		showSingleTalentDialog.value = false

		// Refresh the talents list
		await fetchTalents()
	} catch (error) {
		console.error('Error saving talent:', error)
		showError(error.message || 'Failed to save talent. Please try again.')
	}
}

//Checkbox many
const items = ref([])
const selectedAll = ref([])
const selectedNames = computed(() => selectedAll.value.map((i) => i.name))

// Toggle chọn tất cả
const toggleSelectAll = (event) => {
	if (event.target.checked) {
		selectedAll.value = [...segments.value] // clone danh sách segments
	} else {
		selectedAll.value = []
	}
	console.log('Selected names (after toggle all):', selectedNames.value)
}

// Toggle từng item
const toggleSelect = (item) => {
	const index = selectedAll.value.findIndex((s) => s.name === item.name)
	if (index > -1) {
		selectedAll.value.splice(index, 1)
	} else {
		selectedAll.value.push(item)
	}
	console.log('Selected names:', selectedNames.value)
}
onMounted(async () => {
	await talentPoolStore.getTalentPools()
	await talentPoolStore.fetchSegments()
	await talentSegmentStore.fetchTalentSegments()
	// Add keyboard event listener
	document.addEventListener('keydown', handleKeyDown)
})

const handleSegmentTypeFilter = (option) => {
	const value = typeof option === 'object' ? option?.value || '' : option
	console.log('Selected segment type value:', value)

	selectedSegmentType.value = value
	listPagination.value.currentPage = 1
	talentPoolStore.getTalentPools(value)
}

const matchScore = computed({
	get: () => currentTalentPool.value?.match_score || 0,
	set: (value) => {
		if (currentTalentPool.value) {
			currentTalentPool.value.match_score = parseInt(value) || 0
		}
	},
})

const currentTalentPool = ref(null)
const talentDetails = ref({
	full_name: '',
	contact_email: '',
	contact_phone: '',
})
const view = (item) => router.push(`/talent-pool/${item.name}`)

const handleEditTalentPool = async (pool) => {
	try {
		console.log('data pool>>>>>>>:', pool)
		currentTalentPool.value = { ...pool }
		talentDetails.value = {
			full_name: pool.full_name,
			contact_email: pool.contact_email,
			contact_phone: pool.contact_phone,
		}
		selectedSegmentTypeEdit.value = pool.title
		showDialogTalentPool.value = true
	} catch (error) {
		console.error('Error preparing talent pool edit:', error)
		showError('Failed to load talent pool details')
	}
}

const updateTalentAndPool = async () => {
	console.log('data pool update>>>>>>>:', currentTalentPool.value)

	if (!currentTalentPool.value) return

	try {
		// Update talent information
		await call('frappe.client.set_value', {
			doctype: 'Mira Talent',
			name: currentTalentPool.value.talent_id,
			fieldname: {
				full_name: talentDetails.value.full_name,
				email: talentDetails.value.contact_email,
				phone: talentDetails.value.contact_phone,
			},
		})

		// Update talent pool segment assignment if changed
		if (selectedSegmentTypeEdit.value?.name !== currentTalentPool.value.segment_id) {
			await talentPoolStore.updateTalentPool(currentTalentPool.value.name, {
				segment_id: selectedSegmentTypeEdit.value?.name,
				match_score: currentTalentPool.value.match_score,
			})
		}

		showSuccess('Talent information updated successfully')
		showDialogTalentPool.value = false
		await talentPoolStore.refreshTalentPools()
	} catch (error) {
		console.error('Error updating talent and pool:', error)
		showError('Failed to update talent information')
	}
}

const updateManyTalentPool = async () => {
	if (!selectedSegmentTypeEdit.value?.name) {
		toastMessage.error('Vui lòng chọn segment')
		return
	}

	try {
		const result = await talentPoolStore.updateTalentPoolsSegment({
			names: selectedNames.value,
			segment_id: selectedSegmentTypeEdit.value.name,
		})

		if (result.success) {
			// Close the dialog and show success message
			showEditManyTalentPool.value = false
			selectedSegmentTypeEdit.value = ''
			toastMessage.success(result.message || __('Update successfully'))

			// Clear selection after successful update
			selectedAll.value = []
		}
	} catch (error) {
		console.error('Error updating talent pools segment:', error)
		toastMessage.error(error.message || __('Update failed'))
	}
}

const openCreateDialog = () => {
	openDialogTalent.value = true
}

const closeCreateOptions = () => {
	openDialogTalent.value = false
}

// Dialog handlers
const handleDialogSuccess = async () => {
	// Refresh the talent pools list
	await talentPoolStore.getTalentPools()
	await talentSegmentStore.fetchTalentSegments()
	showCreateForm.value = false
	editingSegment.value = null
}
// Composables
const segments = computed(() => talentSegmentStore.filteredTalentSegments)
const loading = computed(() => talentSegmentStore.loading)
const error = computed(() => talentSegmentStore.error)
const success = computed(() => talentSegmentStore.success)

// Local state
const currentTab = ref('pools')
const viewMode = ref('list') // Default to card view
const showCreateForm = ref(false)
const showDeleteDialog = ref(false)
const editingSegment = ref(null)
const deletingSegment = ref(null)
const searchQuery = ref('')
const formRef = ref(null)

// Talent list state
const selectedAllTalent = ref([])
const itemsPerPageOptions = [10, 20, 50, 100]

// Pagination state for talents
const paginationTalent = ref({
	page: 1,
	limit: 10,
	total: 0,
	has_next: false,
	has_prev: false,
	showing_from: 0,
	showing_to: 0,
})

// Computed properties for talent list
const paginatedTalents = computed(() => {
	const start = (paginationTalent.value.page - 1) * paginationTalent.value.limit
	const end = start + paginationTalent.value.limit
	return talents.value.slice(start, end)
})

// Talent list methods
const toggleSelectAllTalent = () => {
	if (selectedAllTalent.value.length === talents.value.length) {
		selectedAllTalent.value = []
	} else {
		selectedAllTalent.value = [...talents.value]
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

const goToTalentPage = (page) => {
	if (
		page < 1 ||
		page > Math.ceil(paginationTalent.value.total / paginationTalent.value.limit)
	) {
		return
	}
	paginationTalent.value.page = page
	fetchTalents()
}

const changeItemsPerPageTalent = () => {
	paginationTalent.value.page = 1
	fetchTalents()
}

const handleViewTalent = (talent) => {
	// Implement view talent logic
	console.log('View talent:', talent)
	router.push({ name: 'TalentDetail', params: { id: talent.name } })
}

const handleEditTalent = (talent) => {
	// Implement edit talent logic
	console.log('Edit talent:', talent)
}

// Helper methods
const processSkills = (skills) => {
	if (!skills) return []
	if (Array.isArray(skills)) return skills
	return skills
		.split(',')
		.map((skill) => skill.trim())
		.filter(Boolean)
}

const getStatusTheme = (status) => {
	const statusThemes = {
		Active: 'bg-green-100 text-green-800',
		Hired: 'bg-blue-100 text-blue-800',
		Inactive: 'bg-gray-100 text-gray-800',
		'On Leave': 'bg-yellow-100 text-yellow-800',
		Terminated: 'bg-red-100 text-red-800',
	}
	return statusThemes[status] || 'bg-gray-100 text-gray-800'
}

// Fetch talents with pagination
const fetchTalents = async () => {
	try {
		const result = await talentStore.fetchTalents({
			page: paginationTalent.value.page,
			limit: paginationTalent.value.limit,
			filters: {
				...(searchQuery.value && { search: searchQuery.value }),
			},
		})

		if (result && result.success) {
			paginationTalent.value = {
				...paginationTalent.value,
				total: result.count || 0,
				has_next: talentStore.pagination.has_next,
				has_prev: talentStore.pagination.has_prev,
				showing_from: talentStore.pagination.showing_from,
				showing_to: talentStore.pagination.showing_to,
			}
		}
	} catch (error) {
		console.error('Error fetching talents:', error)
		showError(error.message || 'Failed to fetch talents')
	}
}

const loadingFunctions = inject('loadingFunctions', {
	setLoading: () => {},
	clearLoading: () => {},
	showSavingLoading: () => {},
	showCreatingLoading: () => {},
	withLoading: async (fn) => await fn(),
})

// Fetch talents on component mount
onMounted(() => {
	fetchTalents()
	console.log('Loading functions injected:', loadingFunctions)
})

function handleFormSubmit() {
	if (formRef.value) {
		formRef.value.handleSubmit()
	}
}

// Pagination state
const pagination = ref({
	currentPage: 1,
	itemsPerPage: 8, // 3x3 grid
	total: 0,
})

// Toast state
const toast = ref({
	show: false,
	message: '',
	type: 'success',
})

// Navigation tabs
const navigationTabs = [
	{ label: 'Dashboard', value: 'dashboard' },
	{ label: 'Talent Pools', value: 'pools' },
	{ label: 'Candidates', value: 'candidates' },
	{ label: 'Campaigns', value: 'campaigns' },
	{ label: 'AI Timeline', value: 'ai-timeline' },
	{ label: 'Analytics', value: 'analytics' },
]

// Debug mode - can be enabled via query parameter ?debug=true or localStorage
const isDebugMode = computed(() => {
	// Check URL query parameter
	const urlParams = new URLSearchParams(window.location.search)
	if (urlParams.get('debug') === 'true') return true

	// Check localStorage for persistent debug mode
	return localStorage.getItem('talent-segment-debug') === 'true'
})

// Dialog options
const createDialogOptions = computed(() => ({
	title: editingSegment.value ? __('Edit Talent Pool') : __('Create Talent Pool'),
	size: '3xl',
}))

const deleteDialogOptions = computed(() => ({
	title: __('Confirm Delete'),
	size: 'sm',
}))

// Pagination computed properties
const totalSegments = ref(0) // Thêm biến này để lưu tổng số records từ server
const totalPages = computed(() => Math.ceil(totalSegments.value / pagination.value.itemsPerPage))

const loadSegmentsWithPagination = async () => {
	try {
		// Sử dụng store thay vì composable
		const result = await talentSegmentStore.fetchTalentSegments({
			page: pagination.value.currentPage,
			limit: pagination.value.itemsPerPage,
		})

		if (result) {
			// Store trả về { data, pagination }
			totalSegments.value = result.pagination.total
			pagination.value.total = result.pagination.total
		}

		console.log(`Loaded ${segments.value.length} segments, total: ${totalSegments.value}`)
	} catch (err) {
		console.error('Error loading segments:', err)
		showError(err.message || 'Failed to load segments')
	}
}

const enrichSegmentData = async (segment) => {
	try {
		// Extract skills from criteria JSON field
		let topSkills = []
		if (segment.criteria) {
			try {
				const criteria =
					typeof segment.criteria === 'string'
						? JSON.parse(segment.criteria)
						: segment.criteria

				if (criteria.skills && Array.isArray(criteria.skills)) {
					topSkills = criteria.skills
				}
			} catch (e) {
				console.error('Error parsing criteria JSON for segment:', segment.name, e)
			}
		}

		// For now, just add the skills
		segment.topSkills = topSkills
		segment.teamMembers = [] // Empty for now

		return segment
	} catch (error) {
		console.error('Error enriching segment data for:', segment.name, error)
		segment.topSkills = []
		segment.teamMembers = []
		return segment
	}
}

// const paginatedSegments = computed(() => {
//      const start = (pagination.value.currentPage - 1) * pagination.value.itemsPerPage
//      const end = start + pagination.value.itemsPerPage
//      return segments.value.slice(start, end)
// })

const paginationStart = computed(() => {
	return totalSegments.value === 0
		? 0
		: (pagination.value.currentPage - 1) * pagination.value.itemsPerPage + 1
})

const paginationEnd = computed(() => {
	const end = pagination.value.currentPage * pagination.value.itemsPerPage
	return Math.min(end, totalSegments.value)
})

const visiblePages = computed(() => {
	const total = totalPages.value
	const current = pagination.value.currentPage
	const delta = 2 // Number of pages to show around current page

	const range = []
	const rangeWithDots = []

	for (let i = Math.max(2, current - delta); i <= Math.min(total - 1, current + delta); i++) {
		range.push(i)
	}

	if (current - delta > 2) {
		rangeWithDots.push(1, '...')
	} else {
		rangeWithDots.push(1)
	}

	rangeWithDots.push(...range)

	if (current + delta < total - 1) {
		rangeWithDots.push('...', total)
	} else {
		rangeWithDots.push(total)
	}

	return rangeWithDots.filter((page, index, array) => {
		// Remove duplicates and ensure we don't show 1 twice
		return array.indexOf(page) === index && page !== '...' && page > 0 && page <= total
	})
})

// Pagination methods
const goToPage = (page) => {
	if (page >= 1 && page <= totalPages.value) {
		pagination.value.currentPage = page
	}
}

const nextPage = () => {
	if (pagination.value.currentPage < totalPages.value) {
		pagination.value.currentPage++
	}
}

const previousPage = () => {
	if (pagination.value.currentPage > 1) {
		pagination.value.currentPage--
	}
}

// Search handling - using store
const clearSearch = () => {
	searchQuery.value = ''
	talentSegmentStore.setSearchText('')
	talentSegmentStore.fetchTalentSegments()
}

// Utility functions
const formatLastUpdated = (dateStr) => {
	if (!dateStr) return 'Never'
	const date = new Date(dateStr)
	const now = new Date()
	const diffTime = Math.abs(now - date)
	const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

	if (diffDays === 1) return '1 day ago'
	if (diffDays < 7) return `${diffDays} days ago`
	if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
	return `${Math.floor(diffDays / 30)} months ago`
}

const formatDate = (dateString) => {
	return new Date(dateString).toLocaleString()
}

// Card View Pagination
const cardPagination = ref({
	currentPage: 1,
	itemsPerPage: 10,
})

// List View Pagination
const listPagination = ref({
	currentPage: 1,
	itemsPerPage: 10,
})

// Computed properties for card view pagination
const cardTotalPages = computed(() => {
	return Math.ceil(segments.value.length / cardPagination.value.itemsPerPage)
})

const cardVisiblePages = computed(() => {
	return getVisiblePages(cardPagination.value.currentPage, cardTotalPages.value)
})

// Computed properties for list view pagination
const listTotalPages = computed(() => {
	return Math.ceil(talentPools.value.length / listPagination.value.itemsPerPage)
})

const paginatedTalentPools = computed(() => {
	const start = (listPagination.value.currentPage - 1) * listPagination.value.itemsPerPage
	const end = start + listPagination.value.itemsPerPage
	return talentPools.value.slice(start, end)
})

const listVisiblePages = computed(() => {
	return getVisiblePages(listPagination.value.currentPage, listTotalPages.value)
})

// Helper function to get visible pages with ellipsis
const getVisiblePages = (currentPage, total) => {
	const pages = []
	const maxVisiblePages = 5
	if (total <= maxVisiblePages) {
		for (let i = 1; i <= total; i++) {
			pages.push(i)
		}
	} else {
		pages.push(1)
		let start = Math.max(2, currentPage - 1)
		let end = Math.min(total - 1, currentPage + 1)
		if (currentPage <= 3) {
			end = 4
		} else if (currentPage >= total - 2) {
			start = total - 3
		}
		if (start > 2) {
			pages.push('...')
		}
		for (let i = start; i <= end; i++) {
			if (i > 1 && i < total) {
				pages.push(i)
			}
		}
		if (end < total - 1) {
			pages.push('...')
		}
		if (total > 1) {
			pages.push(total)
		}
	}
	return pages
}

// Card View Pagination Methods
const goToCardPage = (page) => {
	if (page >= 1 && page <= cardTotalPages.value) {
		cardPagination.value.currentPage = page
	}
}

const nextCardPage = () => {
	if (cardPagination.value.currentPage < cardTotalPages.value) {
		cardPagination.value.currentPage++
	}
}

const previousCardPage = () => {
	if (cardPagination.value.currentPage > 1) {
		cardPagination.value.currentPage--
	}
}

// List View Pagination Methods
const goToListPage = (page) => {
	if (page >= 1 && page <= listTotalPages.value) {
		listPagination.value.currentPage = page
		// Scroll to top of the list when changing pages
		window.scrollTo({ top: 0, behavior: 'smooth' })
	}
}

const nextListPage = () => {
	if (listPagination.value.currentPage < listTotalPages.value) {
		listPagination.value.currentPage++
		// Scroll to top of the list when changing pages
		window.scrollTo({ top: 0, behavior: 'smooth' })
	}
}

const previousListPage = () => {
	if (listPagination.value.currentPage > 1) {
		listPagination.value.currentPage--
		// Scroll to top of the list when changing pages
		window.scrollTo({ top: 0, behavior: 'smooth' })
	}
}

const getDropdownOptions = (segment) => {
	return [
		{
			group: 'Actions',
			items: [
				{
					label: 'Edit',
					icon: () => h(FeatherIcon, { name: 'edit', class: 'h-4 w-4' }),
					onClick: () => handleEdit(segment),
				},
				{
					label: 'View Details',
					icon: () => h(FeatherIcon, { name: 'eye', class: 'h-4 w-4' }),
					onClick: () => handleViewDetails(segment),
				},
			],
		},
		{
			group: 'Danger',
			items: [
				{
					label: 'Delete',
					icon: () => h(FeatherIcon, { name: 'trash-2', class: 'h-4 w-4' }),
					onClick: () => handleDelete(segment),
				},
			],
		},
	]
}

const getGradientClass = (type) => {
	const gradients = {
		DYNAMIC: 'bg-gradient-to-r from-blue-500 to-indigo-600',
		MANUAL: 'bg-gradient-to-r from-purple-500 to-pink-500',
		default: 'bg-gradient-to-r from-green-500 to-teal-500',
	}
	return gradients[type] || gradients.default
}

const getBadgeClass = (type) => {
	const badges = {
		DYNAMIC: 'bg-blue-100 text-blue-800',
		MANUAL: 'bg-purple-100 text-purple-800',
		default: 'bg-green-100 text-green-800',
	}
	return badges[type] || badges.default
}

const getProgressBarClass = (rate) => {
	if (rate >= 70) return 'bg-green-500'
	if (rate >= 40) return 'bg-yellow-500'
	return 'bg-red-500'
}

const getAvatarClass = (index) => {
	const colors = ['bg-green-500', 'bg-yellow-500', 'bg-purple-500', 'bg-pink-500', 'bg-blue-500']
	return colors[index % colors.length]
}

const getInitials = (name) => {
	if (!name) return '??'
	return name
		.split(' ')
		.map((n) => n[0])
		.join('')
		.toUpperCase()
		.slice(0, 2)
}

// Event handlers
const viewSegmentDetail = (segmentId) => {
	if (!segmentId) return
	router.push({
		name: 'TalentSegmentDetail',
		params: { id: segmentId },
	})
}

const handleFormSuccess = async () => {
	showCreateForm.value = false
	editingSegment.value = null
	await talentSegmentStore.fetchTalentSegments() // Dùng store
	showSuccess(__('Talent pool has been saved successfully'))
}

const handleFormClose = () => {
	showCreateForm.value = false
	// Reset editing segment to trigger form reset
	editingSegment.value = null
}

const handleRefresh = async () => {
	selectedAll.value = []
	const currentFilter = selectedSegmentType.value
	await talentStore.fetchTalents()
	await talentSegmentStore.fetchTalentSegments()
	await talentPoolStore.getTalentPools(currentFilter)
	showSuccess(__('Data refreshed'))
}

const handleSearch = async (query) => {
	talentSegmentStore.setSearchText(query)
	await talentSegmentStore.fetchTalentSegments()
}

const handleEdit = (segment) => {
	editingSegment.value = segment
	showCreateForm.value = true
}

const handleDelete = (segment) => {
	deletingSegment.value = segment
	showDeleteDialog.value = true
}

const handleViewDetails = (segment) => {
	router.push(`/talent-segments/${segment.name}`)
}

const confirmDelete = async () => {
	if (deletingSegment.value) {
		try {
			await talentSegmentStore.deleteTalentSegment(deletingSegment.value.name)
			showSuccess(__('Talent segment deleted successfully'))
			showDeleteDialog.value = false
			deletingSegment.value = null
		} catch (error) {
			showError(error.message || __('Failed to delete talent segment'))
		}
	}
}

// Keyboard shortcuts
const handleKeyDown = (event) => {
	// Ctrl+Shift+D to toggle debug mode
	if (event.ctrlKey && event.shiftKey && event.key === 'D') {
		event.preventDefault()
		const currentDebug = localStorage.getItem('talent-segment-debug') === 'true'
		localStorage.setItem('talent-segment-debug', !currentDebug ? 'true' : 'false')
		console.log('Debug mode toggled via keyboard:', !currentDebug)
		// Force reactivity update
		window.location.reload()
	}
}

// Watchers
watch(
	() => talentSegmentStore.searchText,
	(newValue) => {
		searchQuery.value = newValue
	},
)

watch(
	() => segments.value.length,
	() => {
		pagination.value.total = segments.value.length
	},
)

watch(
	() => [error.value, success.value],
	([errorVal, successVal]) => {
		if (errorVal) {
			showError(errorVal)
		} else if (successVal) {
			showSuccess(__('Operation successful!'))
		}
	},
)

watch(
	() => pagination.value.currentPage,
	() => {
		talentSegmentStore.fetchTalentSegments({
			page: pagination.value.currentPage,
			limit: pagination.value.itemsPerPage,
		})
	},
)

// Reset editingSegment when dialog closes
watch(
	() => showCreateForm.value,
	(isOpen) => {
		if (!isOpen) {
			// Reset editing segment when dialog is closed
			editingSegment.value = null
		}
	},
)

onUnmounted(() => {
	// Remove keyboard event listener
	document.removeEventListener('keydown', handleKeyDown)
})

// Thêm computed mới để chỉ push nút create ở trang cuối
const segmentsForCurrentPage = computed(() => {
	const arr = segments.value.slice() // Dùng segments.value thay vì paginatedSegments
	if (
		pagination.value.currentPage === totalPages.value &&
		segments.value.length < pagination.value.itemsPerPage
	) {
		arr.push({ isCreateButton: true })
	}
	return arr
})
</script>

<style scoped>
/* Custom animation classes */
.card-hover {
	transition: all 0.3s ease;
}

.card-hover:hover {
	transform: translateY(-2px);
}

/* Skill badge styling */
.skill-badge {
	background-color: #e0e7ff;
	color: #4338ca;
	border-radius: 9999px;
	padding: 0.25rem 0.75rem;
	font-size: 0.75rem;
	font-weight: 500;
	display: inline-block;
	margin-right: 0.5rem;
	margin-bottom: 0.5rem;
}

/* Loading animation */
@keyframes pulse {
	0%,
	100% {
		opacity: 1;
	}

	50% {
		opacity: 0.5;
	}
}

.animate-pulse {
	height: 36px !important;
	animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Custom scrollbar */
.overflow-x-auto::-webkit-scrollbar {
	height: 4px;
}

.overflow-x-auto::-webkit-scrollbar-track {
	background: #f1f5f9;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
	background: #cbd5e1;
	border-radius: 4px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
	background: #94a3b8;
}
</style>
