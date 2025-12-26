<template>
	<div class="min-h-screen bg-gray-50">
		<LayoutHeader>
			<template #left-header>
				<div class="flex flex-col">
					<Breadcrumbs :items="breadcrumbs" />
				</div>
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

		<div class="max-w-full mx-5">
			<!-- Campaign Details Card -->
			<div class="bg-white rounded-lg shadow-sm border border-gray-200 mb-6 mt-6">
				<div class="p-6">
					<div class="flex gap-10">
						<div class="">
							<div>
								<label class="text-sm font-medium text-gray-700">{{
									__('Campaign Name')
								}}</label>
								<p class="mt-2 text-sm text-gray-900">
									{{ campaign.campaign_name || __('None') }}
								</p>
							</div>
						</div>
						<div class="">
							<div>
								<label class="text-sm font-medium text-gray-700">{{
									__('Send Schedule')
								}}</label>
								<p class="mt-2 text-sm text-gray-900">
									{{ formatDate(campaign.start_date) || __('None') }}
								</p>
							</div>
						</div>
						<div>
							<label class="text-sm font-medium text-gray-700">{{
								__('Status')
							}}</label>
							<div class="">
								<span
									:class="getStatusClasses(campaign.status)"
									class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
								>
									{{ campaign.status }}
								</span>
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
									: 'border-transparent text-gray-600 hover:text-black hover:border-black',
							]"
						>
							<!-- Chart Bar Icon for Overview -->
							<svg
								v-if="tab.key === 'overview'"
								class="w-5 h-5 mr-2"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
								/>
							</svg>
							<!-- User Icon for Detail Talent -->
							<svg
								v-else-if="tab.key === 'candidates'"
								class="w-5 h-5 mr-2"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
								/>
							</svg>

							<!-- Lightning Icon for Actions -->
							<svg
								v-else-if="tab.key === 'actions'"
								class="w-5 h-5 mr-2"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M13 10V3L4 14h7v7l9-11h-7z"
								/>
							</svg>

							<!-- Document Icon for Mira Candidates -->
							<svg
								v-else-if="tab.key === 'mira_candidates'"
								class="w-5 h-5 mr-2"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5l2 2h5a2 2 0 012 2v14a2 2 0 01-2 2z"
								/>
							</svg>

							<!-- Social Icon for Social Posts -->
							<svg
								v-else-if="tab.key === 'social_posts'"
								class="w-5 h-5 mr-2"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"
								/>
							</svg>
							<!-- Comment Icon for Comments -->
							<CommentIcon
								v-else-if="tab.key === 'comments'"
								class="w-5 h-5 mr-2"
							/>
							<!-- Chart Icon for Analytics -->
							<svg
								v-else
								class="w-5 h-5 mr-2"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
								/>
							</svg>

							<span>{{ tab.label }}</span>

							<!-- Optional count -->
						</button>
					</nav>
				</div>

				<!-- Tab Content -->
				<div class="p-6">
					<!-- Overview Tab -->
					<div v-if="activeTab === 'overview'">
						<CampaignOverview :campaign-id="route.params.id" />
					</div>

					<!-- Assigned Talent Tab -->
					<div v-else-if="activeTab === 'candidates'">
						<div class="flex justify-between items-center mb-4">
							<h3 class="text-lg font-medium text-gray-900">
								{{ __('Details') }}
							</h3>
							<!-- <div class="flex items-center space-x-2">
								<button
									@click="openCandidateModal()"
									class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-black hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
								>
									<svg
										class="w-4 h-4 mr-2"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M12 6v6m0 0v6m0-6h6m-6 0H6"
										/>
									</svg>
									{{ __('Add Manual Talent') }}
								</button>
							</div> -->
						</div>

						<!-- Filter Buttons -->
						<div class="flex flex-wrap gap-2 mb-4">
							<button
								@click="handleFilterClick('sent')"
								:class="[
									'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
									talentFilter === 'sent'
										? 'bg-purple-100 text-purple-700 border-2 border-purple-500'
										: 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50',
								]"
							>
								{{ __('Sent') }} ({{ filterCounts.sent }})
							</button>
							<button
								@click="handleFilterClick('delivered')"
								:class="[
									'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
									talentFilter === 'delivered'
										? 'bg-purple-100 text-purple-700 border-2 border-purple-500'
										: 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50',
								]"
							>
								{{ __('Delivered') }} ({{ filterCounts.delivered }})
							</button>
							<button
								@click="handleFilterClick('opened')"
								:class="[
									'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
									talentFilter === 'opened'
										? 'bg-purple-100 text-purple-700 border-2 border-purple-500'
										: 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50',
								]"
							>
								{{ __('Opened') }} ({{ filterCounts.opened }})
							</button>
							<button
								@click="handleFilterClick('clicked')"
								:class="[
									'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
									talentFilter === 'clicked'
										? 'bg-purple-100 text-purple-700 border-2 border-purple-500'
										: 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50',
								]"
							>
								{{ __('Clicked') }} ({{ filterCounts.clicked }})
							</button>
							<button
								@click="handleFilterClick('failed')"
								:class="[
									'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
									talentFilter === 'failed'
										? 'bg-purple-100 text-purple-700 border-2 border-purple-500'
										: 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50',
								]"
							>
								{{ __('Failed') }} ({{ filterCounts.failed }})
							</button>
							<button
								@click="handleFilterClick('bounced')"
								:class="[
									'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
									talentFilter === 'bounced'
										? 'bg-purple-100 text-purple-700 border-2 border-purple-500'
										: 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50',
								]"
							>
								{{ __('Bounced') }} ({{ filterCounts.bounced }})
							</button>
							<button
								@click="handleFilterClick('spam')"
								:class="[
									'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
									talentFilter === 'spam'
										? 'bg-purple-100 text-purple-700 border-2 border-purple-500'
										: 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50',
								]"
							>
								{{ __('Spam') }} ({{ filterCounts.spam }})
							</button>
						</div>

						<!-- Talent Campaign Table -->
						<div
							class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg"
						>
							<table class="min-w-full divide-y divide-gray-300">
								<thead class="bg-gray-50">
									<tr>
										<th
											class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
										>
											{{ __('Full Name') }}
										</th>
										<th
											class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
										>
											{{ __('ID') }}
										</th>
										<th
											class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
										>
											{{ __('Email') }}
										</th>
										<th
											class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
										>
											{{ __('Phone') }}
										</th>
										<th
											class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
										>
											{{ __('Source') }}
										</th>
										<th
											class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
										>
											{{ __('Actions') }}
										</th>
									</tr>
								</thead>
								<tbody class="bg-white divide-y divide-gray-200">
									<!-- Empty -->
									<tr
										v-if="talentCampaignRecords.length === 0"
										class="text-center"
									>
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
										<td
											class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
										>
											{{ record.full_name }}
										</td>
										<td
											class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
										>
											{{ record.name }}
										</td>
										<td
											class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
										>
											{{ record.email || '-' }}
										</td>
										<td
											class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
										>
											{{ record.phone || '-' }}
										</td>
										<td class="px-6 py-4 whitespace-nowrap text-sm">
											<span
												v-if="record.__source === 'mira_talent'"
												class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
											>
												Talent
												<span
													v-if="record.segment"
													class="ml-1 text-xs opacity-75"
													>({{ record.segment }})</span
												>
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
										<td
											class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2"
										>
											<!-- Unassign button -->
											<button
												@click="unassignCandidate(record)"
												class="text-red-600 hover:text-red-900"
												title="Remove from Campaign"
											>
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
														d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
													/>
												</svg>
											</button>
										</td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>

					<!-- Comments Tab -->
					<div v-else-if="activeTab === 'comments'" class="flex flex-col h-full overflow-hidden">
						<Activities
							ref="activities"
							doctype="Mira Campaign"
							:tabs="[{ name: 'Comments', label: __('Comments') }]"
							v-model:tabIndex="activitiesTabIndex"
							v-model="campaignDoc"
						/>
					</div>

					<!-- Social Posts Tab -->
					<div v-else-if="activeTab === 'social_posts'">
						<div class="flex justify-between items-center mb-6">
							<h3 class="text-lg font-medium text-gray-900">
								{{ __('Social Media Posts') }}
								<span class="ml-2 text-sm font-normal text-gray-500">({{ socialPosts.length }})</span>
							</h3>
						</div>

						<!-- Loading State -->
						<div v-if="loadingSocialPosts" class="text-center py-8">
							<div class="animate-spin inline-block w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full"></div>
							<p class="mt-2 text-gray-500">{{ __('Loading social posts...') }}</p>
						</div>

						<!-- Empty State -->
						<div v-else-if="socialPosts.length === 0" class="text-center py-12 bg-gray-50 rounded-lg">
							<svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
							</svg>
							<h3 class="mt-2 text-sm font-medium text-gray-900">{{ __('No social posts') }}</h3>
							<p class="mt-1 text-sm text-gray-500">{{ __('No social media posts have been created for this campaign yet.') }}</p>
						</div>

						<!-- Social Posts Cards -->
						<div v-else class="space-y-4">
							<div 
								v-for="post in socialPosts" 
								:key="post.name"
								class="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow overflow-hidden cursor-pointer"
								@click="openPostPreview(post)"
							>
								<div class="flex">
									<!-- Image Section -->
									<div v-if="post.social_media_images" class="flex-shrink-0 w-48 h-48 bg-gray-100">
										<img 
											:src="post.social_media_images" 
											class="w-full h-full object-cover"
											:alt="post.subject || 'Post image'"
										/>
									</div>
									<div v-else class="flex-shrink-0 w-48 h-48 bg-gray-100 flex items-center justify-center">
										<svg class="w-12 h-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
										</svg>
									</div>

									<!-- Content Section -->
									<div class="flex-1 p-5">
										<!-- Header: Platform & Status -->
										<div class="flex items-center justify-between mb-3">
											<div class="flex items-center space-x-3">
												<!-- Platform Badge -->
												<span
													:class="getPlatformClasses(post.platform)"
													class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
												>
													<svg v-if="post.platform?.toLowerCase() === 'facebook'" class="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 24 24">
														<path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
													</svg>
													<svg v-else-if="post.platform?.toLowerCase() === 'instagram'" class="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 24 24">
														<path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
													</svg>
													<svg v-else class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
														<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
													</svg>
													{{ post.platform || 'Social' }}
												</span>

												<!-- Page Name -->
												<span class="text-sm text-gray-600">
													{{ post.social_page_name || '-' }}
												</span>
											</div>

											<!-- Status Badge -->
											<span
												:class="getSocialPostStatusClasses(post.status)"
												class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
											>
												<span 
													class="w-2 h-2 rounded-full mr-2"
													:class="{
														'bg-yellow-500': post.status === 'Pending',
														'bg-blue-500': post.status === 'Processing',
														'bg-green-500': post.status === 'Success',
														'bg-red-500': post.status === 'Failed',
														'bg-gray-500': post.status === 'Cancelled'
													}"
												></span>
												{{ post.status || 'Pending' }}
											</span>
										</div>

										<!-- Subject -->
										<h4 v-if="post.subject" class="text-base font-semibold text-gray-900 mb-2">
											{{ post.subject }}
										</h4>

										<!-- Content Preview -->
										<p class="text-sm text-gray-600 mb-4 line-clamp-3">
											{{ stripHtml(post.template_content) || __('No content') }}
										</p>

										<!-- Error Message -->
										<div v-if="post.error_message" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
											<div class="flex items-start">
												<svg class="w-5 h-5 text-red-500 mr-2 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
												</svg>
												<p class="text-sm text-red-700">{{ post.error_message }}</p>
											</div>
										</div>

										<!-- Footer: Timestamps -->
										<div class="flex items-center justify-between pt-3 border-t border-gray-100">
											<div class="flex items-center space-x-6 text-sm text-gray-500">
												<!-- Scheduled Time -->
												<div class="flex items-center">
													<svg class="w-4 h-4 mr-1.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
														<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
													</svg>
													<span>{{ __('Scheduled') }}: {{ formatDateTime(post.post_schedule_time) || '-' }}</span>
												</div>

												<!-- Executed Time -->
												<div v-if="post.executed_at" class="flex items-center">
													<svg class="w-4 h-4 mr-1.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
														<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
													</svg>
													<span>{{ __('Executed') }}: {{ formatDateTime(post.executed_at) }}</span>
												</div>
											</div>

											<!-- Post ID -->
											<span class="text-xs text-gray-400">{{ post.name }}</span>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>

				</div>
			</div>



			<!-- Candidate Assignment Modal with Frappe UI Dialog -->
			<Dialog v-model="showCandidateModal" :options="{ size: 'md' }">
				<template #body>
					<div class="flex justify-between items-center mb-4 px-6 pt-6">
						<h3 class="text-lg font-medium text-gray-900">
							{{
								candidateFormData.name
									? __('Edit Manual Talent')
									: __('Add Manual Talent')
							}}
						</h3>
						<Button
							variant="outline"
							theme="gray"
							@click="closeCandidateModal"
							class="flex items-center"
						>
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


			<!-- Campaign Wizards for Edit (based on campaign type) -->
			<AttractionCampaignWizard
				v-if="campaign.type === 'ATTRACTION'"
				:show="showEditWizard"
				:campaign-type="campaign.type"
				:edit-campaign-id="campaign.name"
				@close="handleWizardClose"
				@success="handleWizardSuccess"
			/>

			<NurturingCampaignWizard
				v-if="campaign.type === 'NURTURING'"
				:show="showEditWizard"
				:campaign-type="campaign.type"
				:edit-campaign-id="campaign.name"
				@close="handleWizardClose"
				@success="handleWizardSuccess"
			/>

			<RecruitmentCampaignWizard
				v-if="campaign.type === 'RECRUITMENT'"
				:show="showEditWizard"
				:campaign-type="campaign.type"
				:edit-campaign-id="campaign.name"
				@close="handleWizardClose"
				@success="handleWizardSuccess"
			/>

			<!-- Social Post Preview Modal -->
			<Dialog
				v-model="showPostPreview"
				:options="{ size: '4xl' }"
			>
				<template #body>
					<div v-if="selectedPost" class="relative">
						<!-- Close Button -->
						<button
							@click="closePostPreview"
							class="absolute top-4 right-4 z-10 p-2 bg-white rounded-full shadow-md hover:bg-gray-100 transition-colors"
						>
							<svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
							</svg>
						</button>

						<!-- Header -->
						<div class="p-6 border-b border-gray-200">
							<div class="flex items-center justify-between">
								<div class="flex items-center space-x-4">
									<!-- Platform Badge -->
									<span
										:class="getPlatformClasses(selectedPost.platform)"
										class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium"
									>
										<svg v-if="selectedPost.platform?.toLowerCase() === 'facebook'" class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
											<path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
										</svg>
										<svg v-else-if="selectedPost.platform?.toLowerCase() === 'instagram'" class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
											<path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073z"/>
										</svg>
										<svg v-else class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
										</svg>
										{{ selectedPost.platform || 'Social' }}
									</span>

									<!-- Page Name -->
									<div>
										<p class="text-sm text-gray-500">{{ __('Page') }}</p>
										<p class="font-medium text-gray-900">{{ selectedPost.social_page_name || '-' }}</p>
									</div>
								</div>

								<!-- Status Badge -->
								<span
									:class="getSocialPostStatusClasses(selectedPost.status)"
									class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium"
								>
									<span 
										class="w-2.5 h-2.5 rounded-full mr-2"
										:class="{
											'bg-yellow-500': selectedPost.status === 'Pending',
											'bg-blue-500': selectedPost.status === 'Processing',
											'bg-green-500': selectedPost.status === 'Success',
											'bg-red-500': selectedPost.status === 'Failed',
											'bg-gray-500': selectedPost.status === 'Cancelled'
										}"
									></span>
									{{ selectedPost.status || 'Pending' }}
								</span>
							</div>
						</div>

						<!-- Content -->
						<div class="p-6">
							<!-- Preview based on platform -->
							<div v-if="selectedPost.platform?.toLowerCase() === 'facebook'" class="space-y-4">
								<!-- Facebook Post Preview -->
								<h4 class="text-sm font-medium text-gray-500 mb-3">{{ __('Facebook Post Preview') }}</h4>
								<div class="bg-white border border-gray-200 rounded-lg p-4 max-w-lg mx-auto">
									<!-- Facebook Header -->
									<div class="flex items-center mb-3">
										<div class="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
											{{ selectedPost.social_page_name ? selectedPost.social_page_name.charAt(0).toUpperCase() : 'F' }}
										</div>
										<div class="ml-3">
											<p class="font-semibold text-gray-900 text-sm">{{ selectedPost.social_page_name || 'Facebook Page' }}</p>
											<p class="text-xs text-gray-500">{{ formatDateTime(selectedPost.post_schedule_time) || 'Now' }}</p>
										</div>
									</div>
									
									<!-- Post Content -->
									<div class="mb-3">
										<p class="text-gray-800 text-sm whitespace-pre-wrap">{{ stripHtml(selectedPost.template_content) || selectedPost.subject || 'No content' }}</p>
									</div>
									
									<!-- Post Image -->
									<div v-if="selectedPost.social_media_images" class="mb-3">
										<img 
											:src="selectedPost.social_media_images" 
											class="w-full rounded-lg object-cover max-h-80"
											:alt="selectedPost.subject || 'Post image'"
										/>
									</div>
									
									<!-- Facebook Actions -->
									<div class="flex items-center justify-between pt-2 border-t border-gray-200 text-gray-500 text-sm">
										<div class="flex space-x-6">
											<span class="flex items-center">
												<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
												</svg>
												Like
											</span>
											<span class="flex items-center">
												<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
												</svg>
												Comment
											</span>
											<span class="flex items-center">
												<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
												</svg>
												Share
											</span>
										</div>
									</div>
								</div>
							</div>

							<div v-else-if="selectedPost.platform?.toLowerCase() === 'instagram'" class="space-y-4">
								<!-- Instagram Post Preview -->
								<h4 class="text-sm font-medium text-gray-500 mb-3">{{ __('Instagram Post Preview') }}</h4>
								<div class="bg-white border border-gray-200 rounded-lg max-w-sm mx-auto">
									<!-- Instagram Header -->
									<div class="flex items-center p-3 border-b border-gray-100">
										<div class="w-8 h-8 bg-gradient-to-tr from-yellow-400 via-red-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xs">
											{{ selectedPost.social_page_name ? selectedPost.social_page_name.charAt(0).toUpperCase() : 'I' }}
										</div>
										<div class="ml-3 flex-1">
											<p class="font-semibold text-gray-900 text-sm">{{ selectedPost.social_page_name || 'Instagram Account' }}</p>
										</div>
										<svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h.01M12 12h.01M19 12h.01" />
										</svg>
									</div>
									
									<!-- Post Image -->
									<div class="aspect-square bg-gray-100">
										<img 
											v-if="selectedPost.social_media_images"
											:src="selectedPost.social_media_images" 
											class="w-full h-full object-cover"
											:alt="selectedPost.subject || 'Post image'"
										/>
										<div v-else class="w-full h-full flex items-center justify-center text-gray-400">
											<svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
											</svg>
										</div>
									</div>
									
									<!-- Instagram Actions -->
									<div class="p-3">
										<div class="flex items-center justify-between mb-3">
											<div class="flex space-x-4">
												<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
												</svg>
												<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
												</svg>
												<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
												</svg>
											</div>
											<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
											</svg>
										</div>
										
										<!-- Caption -->
										<div class="text-sm">
											<span class="font-semibold">{{ selectedPost.social_page_name || 'account' }}</span>
											<span class="ml-1">{{ stripHtml(selectedPost.template_content) || selectedPost.subject || 'No caption' }}</span>
										</div>
										
										<p class="text-xs text-gray-500 mt-1 uppercase">{{ formatDateTime(selectedPost.post_schedule_time) || 'Now' }}</p>
									</div>
								</div>
							</div>

							<div v-else class="space-y-4">
								<!-- Email Preview -->
								<h4 class="text-sm font-medium text-gray-500 mb-3">{{ __('Email Preview') }}</h4>
								<div class="bg-white border border-gray-200 rounded-lg overflow-hidden">
									<!-- Email Header -->
									<div class="bg-gray-50 px-4 py-3 border-b border-gray-200">
										<div class="flex items-center justify-between text-sm">
											<div>
												<p class="font-medium text-gray-900">{{ selectedPost.subject || 'No Subject' }}</p>
												<p class="text-gray-500">From: {{ selectedPost.social_page_name || 'Campaign' }}</p>
											</div>
											<p class="text-gray-500">{{ formatDateTime(selectedPost.post_schedule_time) || 'Draft' }}</p>
										</div>
									</div>
									
									<!-- Email Content -->
									<div class="p-4">
										<iframe
											v-if="selectedPost.template_content"
											:srcdoc="getEmailPreviewContent(selectedPost)"
											class="w-full h-96 border-0"
											sandbox="allow-same-origin"
										></iframe>
										<div v-else class="p-8 text-center text-gray-400">
											{{ __('No email content') }}
										</div>
									</div>
								</div>
							</div>

							<!-- Timestamps Section (below all previews) -->
							<div class="mt-6 pt-6 border-t border-gray-200">
								<div class="grid grid-cols-2 gap-4">
									<div>
										<h4 class="text-sm font-medium text-gray-500 mb-1">{{ __('Scheduled') }}</h4>
										<p class="text-sm text-gray-900">{{ formatDateTime(selectedPost.post_schedule_time) || '-' }}</p>
									</div>
									<div>
										<h4 class="text-sm font-medium text-gray-500 mb-1">{{ __('Executed') }}</h4>
										<p class="text-sm text-gray-900">{{ formatDateTime(selectedPost.executed_at) || '-' }}</p>
									</div>
									<div>
										<h4 class="text-sm font-medium text-gray-500 mb-1">{{ __('Created') }}</h4>
										<p class="text-sm text-gray-900">{{ formatDateTime(selectedPost.creation) || '-' }}</p>
									</div>
									<div>
										<h4 class="text-sm font-medium text-gray-500 mb-1">{{ __('Post ID') }}</h4>
										<p class="text-sm text-gray-900 font-mono">{{ selectedPost.name }}</p>
									</div>
								</div>

								<!-- Error Message -->
								<div v-if="selectedPost.error_message" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
									<div class="flex items-start">
										<svg class="w-5 h-5 text-red-500 mr-2 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
										</svg>
										<div>
											<h4 class="text-sm font-medium text-red-800 mb-1">{{ __('Error') }}</h4>
											<p class="text-sm text-red-700">{{ selectedPost.error_message }}</p>
										</div>
									</div>
								</div>
							</div>
						</div>

						<!-- Footer -->
						<div class="px-6 py-4 bg-gray-50 border-t border-gray-200 flex justify-end">
							<Button variant="outline" @click="closePostPreview">
								{{ __('Close') }}
							</Button>
						</div>
					</div>
				</template>
			</Dialog>

			<!-- Add Talent/Contact Modal -->
			<Dialog
				v-model="showAddTalentModal"
				:options="{ title: __('Add Talent/Contact to Campaign'), size: 'xl' }"
			>
				<template #body-content>
					<div class="space-y-6">
						<!-- Source Selection -->
						<div>
							<h4 class="text-lg font-medium text-gray-900 mb-4">
								{{ __('Select Source') }}
							</h4>
							<div class="flex space-x-6 mb-4 text-sm">
								<label class="flex items-center space-x-2">
									<input
										type="radio"
										value="mira_contact"
										v-model="searchSource"
									/>
									<span>Contact</span>
								</label>
								<label class="flex items-center space-x-2">
									<input
										type="radio"
										value="mira_talent"
										v-model="searchSource"
									/>
									<span>Talent</span>
								</label>
							</div>
						</div>

						<!-- Segment Filter for Talent -->
						<div v-if="searchSource === 'mira_talent'" class="mb-4">
							<label class="block text-sm font-medium text-gray-700 mb-2">
								{{ __('Filter by Segment (Optional)') }}
							</label>
							<Link
								doctype="Mira Segment"
								v-model="selectedSegment"
								:placeholder="__('Select segment to filter talents...')"
							/>
							<p class="mt-1 text-xs text-gray-500">
								{{ __('Leave empty to show all talents') }}
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
								<summary
									class="px-4 py-2 bg-gray-50 cursor-pointer text-sm font-medium text-gray-700 hover:bg-gray-100"
								>
									{{ __('Advanced Filters') }}
								</summary>
								<div class="p-4 space-y-4">
									<!-- Contact Filters -->
									<div v-if="searchSource === 'mira_contact'" class="space-y-3">
										<h5 class="text-sm font-medium text-gray-900">
											{{ __('Contact Filters') }}
										</h5>
										<div class="flex flex-wrap gap-4">
											<label class="flex items-center space-x-2">
												<input
													type="checkbox"
													v-model="advancedFilters.missingEmail"
													class="rounded"
												/>
												<span class="text-sm">{{
													__('Missing Email')
												}}</span>
											</label>
											<label class="flex items-center space-x-2">
												<input
													type="checkbox"
													v-model="advancedFilters.missingPhone"
													class="rounded"
												/>
												<span class="text-sm">{{
													__('Missing Phone')
												}}</span>
											</label>
										</div>
									</div>

									<!-- Talent Filters -->
									<div v-if="searchSource === 'mira_talent'" class="space-y-3">
										<h5 class="text-sm font-medium text-gray-900">
											{{ __('Talent Filters') }}
										</h5>
										<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
											<div>
												<label
													class="block text-xs font-medium text-gray-700 mb-1"
													>{{ __('Skills') }}</label
												>
												<input
													v-model="advancedFilters.skills"
													type="text"
													placeholder="e.g. JavaScript, Python"
													class="w-full border rounded px-2 py-1 text-sm"
												/>
											</div>
											<div>
												<label
													class="block text-xs font-medium text-gray-700 mb-1"
													>{{ __('Tags') }}</label
												>
												<input
													v-model="advancedFilters.tags"
													type="text"
													placeholder="e.g. Senior, Remote"
													class="w-full border rounded px-2 py-1 text-sm"
												/>
											</div>
											<div>
												<label
													class="block text-xs font-medium text-gray-700 mb-1"
													>{{ __('Min Experience (Years)') }}</label
												>
												<input
													v-model.number="
														advancedFilters.minExperienceYears
													"
													type="number"
													min="0"
													placeholder="0"
													class="w-full border rounded px-2 py-1 text-sm"
												/>
											</div>
											<div>
												<label
													class="block text-xs font-medium text-gray-700 mb-1"
													>{{ __('Max Experience (Years)') }}</label
												>
												<input
													v-model.number="
														advancedFilters.maxExperienceYears
													"
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
							<div
								class="flex justify-between items-center mb-3 text-sm text-gray-600"
							>
								<span
									>{{ __('Showing') }} {{ records.length }} {{ __('of') }}
									{{ totalRecords }} {{ __('records') }}</span
								>
								<div class="flex items-center space-x-3">
									<span v-if="selectedCandidates.length"
										>{{ selectedCandidates.length }} {{ __('selected') }}</span
									>
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
							<div
								class="max-h-80 overflow-y-auto grid grid-cols-1 md:grid-cols-2 gap-3"
							>
								<div
									v-for="r in records"
									:key="r.name"
									class="cursor-pointer border rounded-lg p-3 bg-white shadow-sm flex items-center space-x-3 transition-all"
									:class="{
										'border-blue-500 ring-2 ring-blue-200':
											selectedCandidates.includes(r.name),
										'hover:border-gray-300': !selectedCandidates.includes(
											r.name,
										),
									}"
									@click="toggleCandidate(r.name)"
								>
									<div
										class="w-5 h-5 flex items-center justify-center border rounded-full flex-shrink-0"
										:class="
											selectedCandidates.includes(r.name)
												? 'bg-blue-500 border-blue-500 text-white'
												: 'border-gray-300'
										"
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
										<div class="text-sm font-medium text-gray-900 truncate">
											{{ r.full_name }}
										</div>
										<div class="text-xs text-gray-500 truncate">
											{{ r.name }}
										</div>
										<div v-if="r.email" class="text-xs text-gray-400 truncate">
											{{ r.email }}
										</div>
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
									{{ __('Load More') }} ({{ totalRecords - records.length }}
									{{ __('remaining') }})
								</Button>
							</div>

							<!-- Loading Indicator -->
							<div
								v-if="searchLoading && currentPage === 1"
								class="mt-4 text-center text-gray-500 text-sm"
							>
								<div
									class="animate-spin inline-block w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full mr-2"
								></div>
								{{ __('Loading...') }}
							</div>
						</div>

						<!-- Empty State -->
						<div
							v-else-if="searchSource && !searchLoading"
							class="mt-4 text-center text-gray-500 text-sm border rounded p-4 bg-gray-50"
						>
							{{
								__('No data found, please try again or select a different source.')
							}}
						</div>

						<!-- Initial Loading State -->
						<div
							v-else-if="searchLoading && currentPage === 1"
							class="mt-4 text-center text-gray-500 text-sm"
						>
							<div
								class="animate-spin inline-block w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full mr-2"
							></div>
							{{ __('Loading...') }}
						</div>
					</div>
				</template>

				<template #actions>
					<Button
						variant="solid"
						@click="addToCampaign"
						:loading="addingTooltip"
						:disabled="!selectedCandidates.length"
					>
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
import CampaignOverview from '@/components/campaign/CampaignOverview.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Activities from '@/components/Activities/Activities.vue'
import CommentIcon from '@/components/Icons/CommentIcon.vue'

// Campaign Wizards based on type
import AttractionCampaignWizard from '@/pages/AttractionCampaignWizard.vue'
import NurturingCampaignWizard from '@/pages/NurturingCampaignWizard.vue'
import RecruitmentCampaignWizard from '@/pages/RecruitmentCampaignWizard.vue'
import moment from 'moment'
import Link from '@/components/Controls/Link.vue'

const route = useRoute()
const router = useRouter()

// Stores
const campaignStore = useCampaignStore()
const campaignStepStore = useCampaignStepStore()
const miraTalentPoolStore = useMiraTalentPoolStore()
const candidateStore = useCandidateStore()
const talentSegmentStore = useTalentSegmentStore()

// State
const activeTab = ref('overview')
const activitiesTabIndex = ref(0) // For Activities component's internal tab management
const loading = ref(false)
const showEditWizard = ref(false)
const loadingSteps = ref(false)
const loadingCandidates = ref(false)
const loadingActions = ref(false)

// Campaign data
const campaign = ref({})
const campaignDoc = computed(() => ({
	data: {
		name: campaign.value.name || route.params.id
	},
	name: campaign.value.name || route.params.id
}))
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

const talentCampaignRecords = ref([]) // dữ liệu resolved từ mira_talent_campaign

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

// Social posts states
const socialPosts = ref([])
const loadingSocialPosts = ref(false)
const showPostPreview = ref(false)
const selectedPost = ref(null)

// Talent filter states
const talentFilter = ref('sent') // Default filter
const filterCounts = ref({
	sent: 0,
	delivered: 0,
	opened: 0,
	clicked: 0,
	failed: 0,
	bounced: 0,
	spam: 0,
})

// Get campaign type route name based on campaign type
const getCampaignTypeRoute = (type) => {
	const routeMap = {
		'ATTRACTION': 'AttractionCampaign',
		'NURTURING': 'NurtureCampaign',
		'RECRUITMENT': 'RecruitmentCampaign'
	}
	return routeMap[type] || 'CampaignManagement'
}

const breadcrumbs = computed(() => {
	// Get campaign type from storage or campaign object
	const campaignType = campaign.value?.type || localStorage.getItem(`campaign_${route.params.id}_type`)
	
	// Determine route name based on campaign type
	const campaignsRouteName = campaignType ? getCampaignTypeRoute(campaignType) : 'CampaignManagement'
	
	return [
		{ label: __('Campaigns'), route: { name: campaignsRouteName } },
		{
			label: campaign.value.campaign_name || __('Loading...'),
			route: { name: 'CampaignDetailView' },
		},
	]
})

console.log(campaign)

function normalizeTalentCampaign(raw) {
	if (!raw) return []
	let parsed
	try {
		parsed = JSON.parse(raw)
	} catch {
		return []
	}
	if (Array.isArray(parsed)) return parsed
	if (parsed.type && parsed.records) return [parsed]
	return []
}

const campaignSelection = computed(() =>
	normalizeTalentCampaign(campaign.value?.mira_talent_campaign),
)
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
	campaign: route.params.id,
})

const candidateFormData = reactive({
	name: '', // optional: để detect edit
	full_name: '',
	email: '',
	phone_number: '',
})

const actionFormData = reactive({
	name: '',
	campaign_step: '',
	candidate_campaign_id: '',
	status: '',
	scheduled_at: '',
	executed_at: '',
	notes: '',
})

const loadTalentCampaign = async () => {
	try {
		let all = []

		// 1. Load from Mira Talent Campaign table
		try {
			const talentCampaignRes = await call('frappe.client.get_list', {
				doctype: 'Mira Talent Campaign',
				fields: ['name', 'talent_id', 'status'],
				filters: [['campaign_id', '=', route.params.id]],
				limit_page_length: 1000,
			})

			if (talentCampaignRes.length > 0) {
				const talentIds = talentCampaignRes.map((tc) => tc.talent_id)
				const talentRes = await call('frappe.client.get_list', {
					doctype: 'Mira Talent',
					fields: ['name', 'full_name', 'email', 'phone'],
					filters: [['name', 'in', talentIds]],
					limit_page_length: 1000,
				})

				// Merge talent data with campaign data
				const talentData = talentRes.map((talent) => {
					const campaignRecord = talentCampaignRes.find(
						(tc) => tc.talent_id === talent.name,
					)
					return {
						...talent,
						campaign_record_id: campaignRecord.name,
						status: campaignRecord.status,
						segment: campaignRecord.segment,
						__source: 'mira_talent',
					}
				})

				all.push(...talentData)
			}
		} catch (err) {
			console.error('Error loading Mira Talent Campaign:', err)
		}

		// 2. Load from Mira Contact Campaign table
		try {
			// const contactCampaignRes = await call('frappe.client.get_list', {
			// 	doctype: 'Mira Contact Campaign',
			// 	fields: ['name', 'contact_id', 'status'],
			// 	filters: [['campaign_id', '=', route.params.id]],
			// 	limit_page_length: 1000,
			// })

			// if (contactCampaignRes.length > 0) {
			// 	const contactIds = contactCampaignRes.map((cc) => cc.contact_id)
			// 	const contactRes = await call('frappe.client.get_list', {
			// 		doctype: 'Mira Contact',
			// 		fields: ['name', 'full_name', 'email', 'phone'],
			// 		filters: [['name', 'in', contactIds]],
			// 		limit_page_length: 1000,
			// 	})

			// 	// Merge contact data with campaign data
			// 	const contactData = contactRes.map((contact) => {
			// 		const campaignRecord = contactCampaignRes.find(
			// 			(cc) => cc.contact_id === contact.name,
			// 		)
			// 		return {
			// 			...contact,
			// 			campaign_record_id: campaignRecord.name,
			// 			status: campaignRecord.status,
			// 			__source: 'mira_contact',
			// 		}
			// 	})

			// 	all.push(...contactData)
			// }
		} catch (err) {
			console.error('Error loading Mira Contact Campaign:', err)
		}

		talentCampaignRecords.value = all
		console.log('Loaded talent campaign records:', all)
	} catch (err) {
		console.error('Error loading Talent Campaign:', err)
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
			limit_page_length: 100,
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
			doctype: 'Mira Job Opening',
			fields: ['name', 'job_title', 'job_code'],
			order_by: 'creation desc',
			limit_page_length: 100,
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
	{ label: __('Manual Task'), value: 'MANUAL_TASK' },
]

const statusOptions = [
	{ label: __('Active'), value: 'ACTIVE' },
	{ label: __('Paused'), value: 'PAUSED' },
	{ label: __('Completed'), value: 'COMPLETED' },
	{ label: __('Cancelled'), value: 'CANCELLED' },
]

const actionStatusOptions = [
	{ label: __('Scheduled'), value: 'SCHEDULED' },
	{ label: __('Executed'), value: 'EXECUTED' },
	{ label: __('Skipped'), value: 'SKIPPED' },
	{ label: __('Failed'), value: 'FAILED' },
	{ label: __('Pending Manual'), value: 'PENDING_MANUAL' },
]

// Computed properties
const tabs = computed(() => {
	const baseTabs = [
		{
			key: 'overview',
			label: __('Overview'),
			count: 0,
		},
		{
			key: 'candidates',
			label: __('Detail Talent'),
			count: candidateCampaigns.value.length,
		},
		{
			key: 'social_posts',
			label: __('Social Posts'),
			count: socialPosts.value.length,
		},
		{
			key: 'comments',
			label: __('Comments'),
			count: 0,
		},
	]

	return baseTabs
})

// Always sort campaignSteps by step_order ascending
const sortedCampaignSteps = computed(() => {
	return [...campaignSteps.value].sort((a, b) => a.step_order - b.step_order)
})

// CSS classes for status and types
const getStatusClasses = (status) => {
	const classes = {
		ACTIVE: 'bg-green-100 text-green-800',
		PAUSED: 'bg-yellow-100 text-yellow-800',
		COMPLETED: 'bg-blue-100 text-blue-800',
		CANCELLED: 'bg-red-100 text-red-800',
		DRAFT: 'bg-gray-100 text-gray-800',
		ARCHIVED: 'bg-gray-100 text-gray-800',
	}
	return classes[status] || 'bg-gray-100 text-gray-800'
}

const getTypeClasses = (type) => {
	const classes = {
		NURTURING: 'bg-purple-100 text-purple-800',
		ATTRACTION: 'bg-blue-100 text-blue-800',
		RECRUITMENT: 'bg-green-100 text-green-800',
		REFERRAL: 'bg-orange-100 text-orange-800',
		GATHERING: 'bg-gray-100 text-gray-800',
	}
	return classes[type] || 'bg-gray-100 text-gray-800'
}

const getActionTypeClasses = (type) => {
	const classes = {
		SEND_EMAIL: 'bg-blue-100 text-blue-800',
		SEND_SMS: 'bg-green-100 text-green-800',
		MANUAL_CALL: 'bg-orange-100 text-orange-800',
		MANUAL_TASK: 'bg-purple-100 text-purple-800',
	}
	return classes[type] || 'bg-gray-100 text-gray-800'
}

const getActionStatusClasses = (status) => {
	const classes = {
		SCHEDULED: 'bg-blue-100 text-blue-800',
		EXECUTED: 'bg-green-100 text-green-800',
		SKIPPED: 'bg-yellow-100 text-yellow-800',
		FAILED: 'bg-red-100 text-red-800',
		PENDING_MANUAL: 'bg-orange-100 text-orange-800',
	}
	return classes[status] || 'bg-gray-100 text-gray-800'
}

const getPlatformClasses = (platform) => {
	const classes = {
		facebook: 'bg-blue-100 text-blue-800',
		Facebook: 'bg-blue-100 text-blue-800',
		instagram: 'bg-pink-100 text-pink-800',
		Instagram: 'bg-pink-100 text-pink-800',
		linkedin: 'bg-blue-100 text-blue-800',
		LinkedIn: 'bg-blue-100 text-blue-800',
		twitter: 'bg-sky-100 text-sky-800',
		Twitter: 'bg-sky-100 text-sky-800',
		tiktok: 'bg-gray-900 text-white',
		TikTok: 'bg-gray-900 text-white',
	}
	return classes[platform] || 'bg-gray-100 text-gray-800'
}

const getSocialPostStatusClasses = (status) => {
	const classes = {
		Pending: 'bg-yellow-100 text-yellow-800',
		Processing: 'bg-blue-100 text-blue-800',
		Success: 'bg-green-100 text-green-800',
		Failed: 'bg-red-100 text-red-800',
		Cancelled: 'bg-gray-100 text-gray-800',
	}
	return classes[status] || 'bg-gray-100 text-gray-800'
}

// Interaction helper functions
const getInteractionTypeClass = (type) => {
	const classes = {
		EMAIL_SENT: 'bg-blue-100 text-blue-800',
		EMAIL_DELIVERED: 'bg-green-100 text-green-800',
		EMAIL_BOUNCED: 'bg-red-100 text-red-800',
		EMAIL_OPENED: 'bg-purple-100 text-purple-800',
		EMAIL_CLICKED: 'bg-indigo-100 text-indigo-800',
		EMAIL_UNSUBSCRIBED: 'bg-gray-100 text-gray-800',
		EMAIL_REPLIED: 'bg-emerald-100 text-emerald-800',
		PAGE_VISITED: 'bg-cyan-100 text-cyan-800',
		FORM_SUBMITTED: 'bg-teal-100 text-teal-800',
		DOWNLOAD_TRIGGERED: 'bg-orange-100 text-orange-800',
		CHAT_STARTED: 'bg-pink-100 text-pink-800',
		CHAT_MESSAGE_SENT: 'bg-rose-100 text-rose-800',
		CHAT_COMPLETED: 'bg-green-100 text-green-800',
		CALL_MISSED: 'bg-red-100 text-red-800',
		CALL_COMPLETED: 'bg-green-100 text-green-800',
		SMS_SENT: 'bg-blue-100 text-blue-800',
		SMS_DELIVERED: 'bg-green-100 text-green-800',
		SMS_REPLIED: 'bg-emerald-100 text-emerald-800',
		APPLICATION_SUBMITTED: 'bg-purple-100 text-purple-800',
		DOCUMENT_UPLOADED: 'bg-yellow-100 text-yellow-800',
		TEST_STARTED: 'bg-orange-100 text-orange-800',
		TEST_COMPLETED: 'bg-green-100 text-green-800',
		INTERVIEW_CONFIRMED: 'bg-blue-100 text-blue-800',
		INTERVIEW_RESCHEDULED: 'bg-yellow-100 text-yellow-800',
	}
	return classes[type] || 'bg-gray-100 text-gray-800'
}

const formatInteractionType = (type) => {
	const labels = {
		EMAIL_SENT: 'Email Sent',
		EMAIL_DELIVERED: 'Email Delivered',
		EMAIL_BOUNCED: 'Email Bounced',
		EMAIL_OPENED: 'Email Opened',
		EMAIL_CLICKED: 'Email Clicked',
		EMAIL_UNSUBSCRIBED: 'Email Unsubscribed',
		EMAIL_REPLIED: 'Email Replied',
		PAGE_VISITED: 'Page Visited',
		FORM_SUBMITTED: 'Form Submitted',
		DOWNLOAD_TRIGGERED: 'Download Triggered',
		CHAT_STARTED: 'Chat Started',
		CHAT_MESSAGE_SENT: 'Chat Message Sent',
		CHAT_COMPLETED: 'Chat Completed',
		CALL_MISSED: 'Call Missed',
		CALL_COMPLETED: 'Call Completed',
		SMS_SENT: 'SMS Sent',
		SMS_DELIVERED: 'SMS Delivered',
		SMS_REPLIED: 'SMS Replied',
		APPLICATION_SUBMITTED: 'Application Submitted',
		DOCUMENT_UPLOADED: 'Document Uploaded',
		TEST_STARTED: 'Test Started',
		TEST_COMPLETED: 'Test Completed',
		INTERVIEW_CONFIRMED: 'Interview Confirmed',
		INTERVIEW_RESCHEDULED: 'Interview Rescheduled',
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
			
			// Save campaign type to localStorage for breadcrumb navigation
			if (campaign.value.type) {
				localStorage.setItem(`campaign_${route.params.id}_type`, campaign.value.type)
			}
			
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
			limit: 1000,
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
		const result = await call('frappe.client.get_list', {
			doctype: 'Mira Talent Campaign',
			filters: { campaign_id: route.params.id },
			fields: ['name', 'talent_id', 'status', 'current_step_order', 'enrolled_at'],
		})
		if (result) {
			candidateCampaigns.value = result || []
		}
	} catch (error) {
		console.error('Error loading candidate campaigns:', error)
		candidateCampaigns.value = []
	} finally {
		loadingCandidates.value = false
	}
}

const loadActions = async () => {
	loadingActions.value = true
	try {
		const candidateCampaignsResult = await call('frappe.client.get_list', {
			doctype: 'Mira Talent Campaign',
			filters: { campaign_id: route.params.id },
			fields: ['name'],
		})
		if (candidateCampaignsResult && candidateCampaignsResult.length > 0) {
			const candidateCampaignIds = candidateCampaignsResult.map((cc) => cc.name)
			// Use correct field name: talent_campaign_id (not candidate_campaign_id) and campaign_social (not campaign_step)
			const result = await call('frappe.client.get_list', {
				doctype: 'Mira Action',
				filters: { talent_campaign_id: ['in', candidateCampaignIds] },
				fields: ['name', 'campaign_social', 'action_type', 'status', 'scheduled_at', 'executed_at', 'talent_campaign_id'],
			})
			if (result) {
				actions.value = result || []
			} else {
				actions.value = []
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
			const result = await call('frappe.client.get_list', {
				doctype: 'Mira Talent',
				fields: ['name', 'full_name'],
				limit_page_length: 1000,
			})
			if (result) {
				availableCandidates.value = result.map((item) => ({
					label: item.full_name || item.name,
					value: item.name,
				}))
			}
		} else {
			// Get candidates from target segment through Mira Talent Pool
			const candidateSegmentResult = await call('frappe.client.get_list', {
				doctype: 'Mira Talent Pool',
				filters: { segment_id: campaign.value.target_segment },
				fields: ['talent_id'],
			})
			if (candidateSegmentResult && candidateSegmentResult.length > 0) {
				const candidateIds = candidateSegmentResult.map((cs) => cs.talent_id).filter(Boolean)
				// Get candidates already in this campaign
				const existingCandidateCampaigns = await call('frappe.client.get_list', {
					doctype: 'Mira Talent Campaign',
					filters: { campaign_id: route.params.id },
					fields: ['talent_id'],
				})
				const existingCandidateIds = existingCandidateCampaigns
					? existingCandidateCampaigns.map((cc) => cc.talent_id).filter(Boolean)
					: []
				// Filter out candidates already in campaign
				const availableCandidateIds = candidateIds.filter(
					(id) => !existingCandidateIds.includes(id),
				)
				if (availableCandidateIds.length > 0) {
					const candidateResult = await call('frappe.client.get_list', {
						doctype: 'Mira Talent',
						filters: { name: ['in', availableCandidateIds] },
						fields: ['name', 'full_name'],
					})
					if (candidateResult) {
						availableCandidates.value = candidateResult.map((item) => ({
							label: item.full_name + ' (' + item.name + ')',
							value: item.name,
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
		availableCandidates.value = []
	}
}

// Step methods
const openStepModal = (step = null) => {
	if (step) {
		Object.assign(stepFormData, step)
	} else {
		Object.keys(stepFormData).forEach((key) => {
			stepFormData[key] = ''
		})
		stepFormData.campaign = route.params.id
		// Gán step_order = max + 1
		const maxOrder = Math.max(...campaignSteps.value.map((s) => s.step_order), 0)
		stepFormData.step_order = maxOrder + 1
	}
	showStepModal.value = true
}

const closeStepModal = () => {
	showStepModal.value = false
	Object.keys(stepFormData).forEach((key) => {
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
	maxExperienceYears: null,
})

// Existing records in campaign (to exclude)
const existingRecords = ref({
	talents: [],
	contacts: [],
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
		existingRecords.value.talents = talentCampaignRes.map((tc) => tc.talent_id)

		// Load existing contacts
		const contactCampaignRes = await call('frappe.client.get_list', {
			doctype: 'Mira Contact Campaign',
			fields: ['contact_id'],
			filters: [['campaign_id', '=', route.params.id]],
			limit_page_length: 1000,
		})
		existingRecords.value.contacts = contactCampaignRes.map((cc) => cc.contact_id)

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
	Object.keys(advancedFilters).forEach((key) => {
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

				const talentIds = poolRes.map((r) => r.talent_id)
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
				fields: [
					'name',
					'full_name',
					'email',
					'phone',
					'skills',
					'tags',
					'experience_years',
				],
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
	const currentPageIds = records.value.map((r) => r.name)
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
			const bulkData = selectedCandidates.value.map((recordId) => ({
				doctype: doctype,
				campaign_id: route.params.id,
				[recordField]: recordId,
				status: 'ACTIVE',
				...(recordType === 'mira_talent' && selectedSegment.value
					? { segment: selectedSegment.value }
					: {}),
			}))

			// Call custom bulk insert API
			await call('mbw_mira.api.campaign.bulk_create_campaign_records', {
				records: bulkData,
				doctype: doctype,
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
						: {}),
				}

				return await call('frappe.client.insert', {
					doc: {
						doctype: doctype,
						...payload,
					},
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
watch(
	advancedFilters,
	() => {
		if (!searchSource.value) return
		currentPage.value = 1
		records.value = []
		totalRecords.value = 0
		fetchRecordsDebounced(1)
	},
	{ deep: true },
)

// Action methods
const openActionModal = () => {
	Object.keys(actionFormData).forEach((key) => {
		actionFormData[key] = ''
	})
	showActionModal.value = true
}

const closeActionModal = () => {
	showActionModal.value = false
	Object.keys(actionFormData).forEach((key) => {
		actionFormData[key] = ''
	})
}

const loadMiraCandidates = async () => {
	loadingMiraCandidates.value = true
	try {
		// const res = await call('frappe.client.get_list', {
		// 	doctype: 'Mira Candidate',
		// 	fields: [
		// 		'name',
		// 		'full_name',
		// 		'email',
		// 		'phone',
		// 		'avatar',
		// 		'headline',
		// 		'source',
		// 		'skills',
		// 		'status',
		// 		'last_interaction',
		// 	],
		// 	filters: { campaign_id: route.params.id },
		// 	limit_page_length: 100,
		// })
		miraCandidates.value = []
	} catch (err) {
		console.error('Error loading Mira Candidates:', err)
		miraCandidates.value = []
	} finally {
		loadingMiraCandidates.value = false
	}
}

// Load interactions for the campaign
const loadInteractions = async () => {
	loadingInteractions.value = true
	try {
		// Use backend API endpoint for safer query
		const response = await call('mbw_mira.api.interaction.get_campaign_interactions', {
			campaign_id: route.params.id,
			limit: 100
		})
		
		if (response && response.status === 'success') {
			interactions.value = response.interactions || []
		} else {
			interactions.value = []
		}
	} catch (err) {
		console.error('Error loading interactions:', err)
		interactions.value = []
	} finally {
		loadingInteractions.value = false
	}
}

// Load social posts for the campaign
const loadSocialPosts = async () => {
	loadingSocialPosts.value = true
	try {
		const res = await call('frappe.client.get_list', {
			doctype: 'Mira Campaign Social',
			fields: [
				'name',
				'campaign_id',
				'social_page_id',
				'social_page_name',
				'external_connection',
				'platform',
				'post_schedule_time',
				'executed_at',
				'template_content',
				'css_content',
				'subject',
				'social_media_images',
				'status',
				'retry_count',
				'error_message',
				'share_at',
				'creation',
				'modified',
			],
			filters: { campaign_id: route.params.id },
			order_by: 'creation desc',
			limit_page_length: 100,
		})
		socialPosts.value = res || []
		console.log('✅ Loaded social posts:', socialPosts.value.length)
	} catch (err) {
		console.error('Error loading social posts:', err)
		socialPosts.value = []
	} finally {
		loadingSocialPosts.value = false
	}
}

// Load filter counts for talent list from API
const loadFilterCounts = async () => {
	try {
		const response = await call('mbw_mira.api.interaction.get_campaign_filter_counts', {
			campaign_id: route.params.id
		})
		
		if (response.status === 'success' && response.filter_counts) {
			filterCounts.value = {
				sent: response.filter_counts.sent || 0,
				delivered: response.filter_counts.delivered || 0,
				opened: response.filter_counts.opened || 0,
				clicked: response.filter_counts.clicked || 0,
				failed: response.filter_counts.failed || 0,
				bounced: response.filter_counts.bounced || 0,
				spam: response.filter_counts.spam || 0,
			}
		}
	} catch (error) {
		console.error('Error loading filter counts:', error)
	}
}

// Watch tabs to ensure activeTab is always valid
watch(
	tabs,
	(newTabs) => {
		const tabKeys = newTabs.map((tab) => tab.key)
		if (!tabKeys.includes(activeTab.value)) {
			// Nếu activeTab hiện tại không còn tồn tại, chuyển về tab đầu tiên
			activeTab.value = tabKeys[0] || 'overview'
		}
	},
	{ immediate: true },
)

// Watch route hash to switch to comments tab
watch(
	() => route.hash,
	(newHash) => {
		if (newHash === '#comments') {
			activeTab.value = 'comments'
		}
	},
	{ immediate: true }
)

// Load initial data
// Watch activeTab to load data when needed
watch(activeTab, (newTab) => {
	if (newTab === 'social') {
		console.log(' Switching to social tab, ensuring data is loaded...')
		if (externalConnections.value.length === 0) {
			loadExternalConnections()
		}
		if (socialPages.value.length === 0) {
			loadSocialPages()
		}
		if (jobOpeningsList.value.length === 0) {
			loadJobOpenings()
		}
	} else if (newTab === 'interactions') {
		console.log(' Switching to interactions tab, loading data...')
		if (interactions.value.length === 0) {
			loadInteractions()
		}
	} else if (newTab === 'social_posts') {
		console.log(' Switching to social posts tab, loading data...')
		if (socialPosts.value.length === 0) {
			loadSocialPosts()
		}
	}
})
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
	loadFilterCounts()
})

// Watchers
watch(
	() => route.params.id,
	(newId, oldId) => {
		if (newId !== oldId) {
			loadCampaign()
			loadCampaignSteps()
			loadCandidateCampaigns()
			loadActions()
			loadAvailableCandidates()
			loadFilterCounts()
			loadTalentCampaign()
		}
	},
)

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

// Strip HTML tags and decode entities for preview
const stripHtml = (html) => {
	if (!html) return ''
	// Create a temporary element to decode HTML entities
	const doc = new DOMParser().parseFromString(html, 'text/html')
	return doc.body.textContent || ''
}

// Combine css_content and template_content for email preview
const getEmailPreviewContent = (post) => {
	if (!post) return ''
	
	const templateContent = post.template_content || ''
	const cssContent = post.css_content || ''
	
	// If no CSS content, return template content as is
	if (!cssContent) {
		return templateContent
	}
	
	// Combine CSS and HTML content
	return `
		<!DOCTYPE html>
		<html>
		<head>
			<meta charset="UTF-8">
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<style>
				${cssContent}
			</style>
		</head>
		<body>
			${templateContent}
		</body>
		</html>
	`
}

// Open post preview modal
const openPostPreview = (post) => {
	selectedPost.value = post
	showPostPreview.value = true
}

// Close post preview modal
const closePostPreview = () => {
	showPostPreview.value = false
	selectedPost.value = null
}

const editCampaign = () => {
	showEditWizard.value = true
}

const handleWizardClose = () => {
	showEditWizard.value = false
}

const handleWizardSuccess = async () => {
	showEditWizard.value = false
	await loadCampaign()
	await loadCampaignSteps()
}

const getActiveCandidates = () => {
	return candidateCampaigns.value.filter((c) => c.status === 'ACTIVE').length
}

const getCompletedCandidates = () => {
	return candidateCampaigns.value.filter((c) => c.status === 'COMPLETED').length
}

const saveStep = async () => {
	savingStep.value = true
	try {
		// Nếu có name thì update, còn không thì insert
		let result
		console.log(stepFormData.name)
		if (stepFormData.name) {
			console.log('Update')
			result = await campaignStepStore.updateCampaignStep(stepFormData.name, stepFormData)
		} else {
			console.log('Insert')
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

		let manualBlock = current.find((b) => b.type === 'manual')
		if (!manualBlock) {
			manualBlock = { type: 'manual', records: [] }
			current.push(manualBlock)
		}

		if (candidateFormData.name) {
			// edit
			const idx = manualBlock.records.findIndex((r) => r.name === candidateFormData.name)
			if (idx !== -1) {
				manualBlock.records[idx] = { ...candidateFormData }
			}
		} else {
			// add mới
			manualBlock.records.push({
				name: 'MTL-' + Date.now(),
				full_name: candidateFormData.full_name,
				email: candidateFormData.email,
				phone_number: candidateFormData.phone_number,
			})
		}

		await call('frappe.client.set_value', {
			doctype: 'Mira Campaign',
			name: route.params.id,
			fieldname: 'mira_talent_campaign',
			value: JSON.stringify(current),
		})

		campaign.value.mira_talent_campaign = JSON.stringify(current)
		await loadTalentCampaign()
		closeCandidateModal()
	} catch (err) {
		console.error('Error saving manual talent:', err)
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
			campaignStepStore.updateStepOrder(previousStep.name, previousStep.step_order),
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
			campaignStepStore.updateStepOrder(nextStep.name, nextStep.step_order),
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
				name: record.campaign_record_id,
			})
		} else if (record.__source === 'mira_contact') {
			await call('frappe.client.delete', {
				doctype: 'Mira Contact Campaign',
				name: record.campaign_record_id,
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

// Handle filter click for talent list
const handleFilterClick = (filterType) => {
	console.log('Filter clicked:', filterType)
	talentFilter.value = filterType
	
	// TODO: Implement actual filtering logic when doctype is ready
	// This will filter talentCampaignRecords based on the selected filter
	// For now, just log the filter type
	console.log('Current filter:', talentFilter.value)
	console.log('Filter counts:', filterCounts.value)
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
