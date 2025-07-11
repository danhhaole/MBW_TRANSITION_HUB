<template>
	<div class="candidate-detail-view container mx-auto w-full p-4 min-h-screen bg-gray-50">
		<!-- Header with Candidate Info -->
		<div class="bg-white rounded-lg border border-gray-200 p-6 mb-6">
			<div class="flex items-center justify-between">
				<div class="flex items-center">
					<button
						@click="$router.go(-1)"
						class="mr-4 p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
					>
						<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M15 19l-7-7 7-7"
							/>
						</svg>
					</button>
					<div class="flex items-center">
						<Avatar
							:shape="'circle'"
							:image="candidate.avatar"
							:label="getAvatarText(candidate.full_name)"
							size="3xl"
							class="mr-4"
						/>
						<div>
							<h1 class="text-3xl font-bold text-blaack mb-2">
								{{ candidate.full_name || 'Loading...' }}
							</h1>
							<div class="flex items-center flex-wrap gap-2">
								<span
									v-if="candidate.status"
									class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
									:class="getStatusClasses(candidate.status)"
								>
									{{ candidate.status }}
								</span>
								<span class="text-sm text-gray-500">
									{{ candidate.email }}
								</span>
								<span class="text-sm text-gray-500">
									{{ candidate.phone }}
								</span>
							</div>
						</div>
					</div>
				</div>

				<div class="flex items-center space-x-3">
					<Button variant="outline" @click="editCandidate">
						<div class="flex items-center">
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
									d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
								/>
							</svg>
							Edit Profile
						</div>
					</Button>
					<Button variant="outline" theme="red" @click="deleteCandidate">
						<div class="flex items-center">
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
									d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
								/>
							</svg>
							Delete
						</div>
					</Button>
				</div>
			</div>
		</div>

		<!-- Candidate Details Card -->
		<div class="bg-white rounded-lg border border-gray-200 mb-6">
			<div class="border-b border-gray-200 px-6 py-4">
				<h3 class="text-lg font-medium text-gray-900 flex items-center">
					<svg
						class="w-5 h-5 mr-2 text-black"
						fill="currentColor"
						viewBox="0 0 20 20"
					>
						<path
							fill-rule="evenodd"
							d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z"
							clip-rule="evenodd"
						/>
					</svg>
					Candidate Information
				</h3>
			</div>
			<div class="p-6">
				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<div class="space-y-4">
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-1"
								>Full Name</label
							>
							<p class="text-gray-900">{{ candidate.full_name || 'N/A' }}</p>
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-1"
								>Email</label
							>
							<p class="text-gray-900">{{ candidate.email || 'N/A' }}</p>
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-1"
								>Phone</label
							>
							<p class="text-gray-900">{{ candidate.phone || 'N/A' }}</p>
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-1"
								>Status</label
							>
							<span
								v-if="candidate.status"
								class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
								:class="getStatusClasses(candidate.status)"
							>
								{{ candidate.status }}
							</span>
							<span v-else class="text-gray-500">N/A</span>
						</div>
					</div>
					<div class="space-y-4">
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-1"
								>Headline</label
							>
							<p class="text-gray-900">{{ candidate.headline || 'N/A' }}</p>
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-1"
								>Source</label
							>
							<p class="text-gray-900">{{ candidate.source || 'N/A' }}</p>
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-1"
								>Last Interaction</label
							>
							<p class="text-gray-900">{{ formatDateTime(candidate.last_interaction) || 'N/A' }}</p>
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-1"
								>Email Opt Out</label
							>
							<span
								v-if="candidate.email_opt_out"
								class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800"
							>
								Opted Out
							</span>
							<span
								v-else
								class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
							>
								Subscribed
							</span>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Tabbed Content -->
		<div class="bg-white rounded-lg border border-gray-200">
			<!-- Tab Navigation -->
			<div class="border-b border-gray-200">
				<nav class="-mb-px flex space-x-8 px-6" aria-label="Tabs">
					<button
						v-for="tab in tabs"
						:key="tab.key"
						@click="activeTab = tab.key"
						:class="[
							'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center',
							activeTab === tab.key
								? 'border-black text-black'
								: 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
						]"
					>
						<component :is="tab.icon" class="w-4 h-4 mr-2" />
						{{ tab.label }} ({{ tab.count }})
					</button>
				</nav>
			</div>

			<!-- Tab Content -->
			<div class="p-6">
				<!-- Campaigns Tab -->
				<div v-if="activeTab === 'campaigns'">
					<div class="flex justify-between items-center mb-6">
						<h3 class="text-lg font-medium text-gray-900">Active Campaigns</h3>
						<Button @click="openCampaignModal()">
							<div class="flex items-center">
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
								Assign to Campaign
							</div>
						</Button>
					</div>

					<!-- Campaign Table -->
					<div
						class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg"
					>
						<table class="min-w-full divide-y divide-gray-300">
							<thead class="bg-gray-50">
								<tr>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Campaign
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Status
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Progress
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Next Action
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Actions
									</th>
								</tr>
							</thead>
							<tbody class="bg-white divide-y divide-gray-200">
								<tr v-if="loadingCampaigns">
									<td
										colspan="5"
										class="px-6 py-4 text-center text-sm text-gray-500"
									>
										Loading...
									</td>
								</tr>
								<tr v-else-if="candidateCampaigns.length === 0">
									<td
										colspan="5"
										class="px-6 py-4 text-center text-sm text-gray-500"
									>
										No campaigns assigned
									</td>
								</tr>
								<tr
									v-else
									v-for="item in candidateCampaigns"
									:key="item.name"
									class="hover:bg-gray-50"
								>
									<td
										class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
									>
										{{ item.campaign_name || item.campaign_id }}
									</td>
									<td class="px-6 py-4 whitespace-nowrap">
										<span
											class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
											:class="getStatusClasses(item.status)"
										>
											{{ item.status }}
										</span>
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
										Step {{ item.current_step_order || 1 }}
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
										{{ formatDateTime(item.next_action_at) || 'N/A' }}
									</td>
									<td
										class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2"
									>
										<Button
											v-if="item.status === 'PAUSED'"
											variant="outline"
											size="sm"
											@click="startCampaign(item)"
										>
											Start
										</Button>
										<Button
											v-if="item.status === 'ACTIVE'"
											variant="outline"
											size="sm"
											@click="pauseCampaign(item)"
										>
											Pause
										</Button>
										<Button
											variant="outline"
											size="sm"
											@click="viewCampaignDetails(item)"
										>
											View
										</Button>
										<Button
											variant="outline"
											theme="red"
											size="sm"
											@click="removeCampaign(item)"
										>
											Remove
										</Button>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>

				<!-- Segments Tab -->
				<div v-if="activeTab === 'segments'">
					<div class="flex justify-between items-center mb-6">
						<h3 class="text-lg font-medium text-gray-900">Candidate Segments</h3>
						<Button @click="openSegmentModal()">
							<div class="flex items-center">
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
								Add to Segment
							</div>
						</Button>
					</div>

					<!-- Segments Table -->
					<div
						class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg"
					>
						<table class="min-w-full divide-y divide-gray-300">
							<thead class="bg-gray-50">
								<tr>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Segment
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Type
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Added At
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Actions
									</th>
								</tr>
							</thead>
							<tbody class="bg-white divide-y divide-gray-200">
								<tr v-if="loadingSegments">
									<td
										colspan="4"
										class="px-6 py-4 text-center text-sm text-gray-500"
									>
										Loading...
									</td>
								</tr>
								<tr v-else-if="candidateSegments.length === 0">
									<td
										colspan="4"
										class="px-6 py-4 text-center text-sm text-gray-500"
									>
										No segments assigned
									</td>
								</tr>
								<tr
									v-else
									v-for="item in candidateSegments"
									:key="item.name"
									class="hover:bg-gray-50"
								>
									<td
										class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
									>
										{{ item.title || item.name }}
									</td>
									<td class="px-6 py-4 whitespace-nowrap">
										<span
											class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
											:class="getTypeClasses(item.type)"
										>
											{{ item.type }}
										</span>
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
										{{ formatDate(item.added_at) }}
									</td>
									<td
										class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2"
									>
										<Button
											variant="outline"
											size="sm"
											@click="viewSegmentDetails(item)"
										>
											View
										</Button>
										<Button
											variant="outline"
											theme="red"
											size="sm"
											@click="removeFromSegment(item)"
										>
											Remove
										</Button>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>

				<!-- Interactions Tab -->
				<div v-if="activeTab === 'interactions'">
					<div class="flex justify-between items-center mb-6">
						<h3 class="text-lg font-medium text-gray-900">Interaction History</h3>
						<Button @click="openInteractionModal()">
							<div class="flex items-center">
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
								Add Interaction
							</div>
						</Button>
					</div>

					<!-- Interactions Timeline -->
					<div v-if="interactions.length > 0" class="flow-root">
						<ul role="list" class="-mb-8">
							<li v-for="(interaction, idx) in interactions" :key="interaction.name">
								<div class="relative pb-8">
									<span
										v-if="idx !== interactions.length - 1"
										class="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
										aria-hidden="true"
									></span>
									<div class="relative flex space-x-3">
										<div>
											<span
												class="h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white"
												:class="
													getInteractionBgClasses(
														interaction.interaction_type,
													)
												"
											>
												<component
													:is="
														getInteractionIcon(
															interaction.interaction_type,
														)
													"
													class="w-4 h-4 text-white"
												/>
											</span>
										</div>
										<div
											class="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4"
										>
											<div>
												<p class="text-sm text-gray-500">
													{{
														formatInteractionType(
															interaction.interaction_type,
														)
													}}
												</p>
												<p class="text-sm text-gray-900">
													{{ interaction.description }}
												</p>
											</div>
											<div
												class="text-right text-sm whitespace-nowrap text-gray-500"
											>
												{{ formatDateTime(interaction.creation) }}
											</div>
										</div>
									</div>
								</div>
							</li>
						</ul>
					</div>

					<!-- Empty state -->
					<div v-else class="text-center py-12">
						<svg
							class="w-12 h-12 mx-auto text-gray-400"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-3.582 8-8 8a8.001 8.001 0 01-7.227-4.612 2.5 2.5 0 00-.673-2.388A8 8 0 0112 4c4.418 0 8 3.582 8 8z"
							/>
						</svg>
						<p class="mt-4 text-sm text-gray-500">No interactions found</p>
					</div>
				</div>

				<!-- Email History Tab -->
				<div v-if="activeTab === 'emails'">
					<div class="flex justify-between items-center mb-6">
						<h3 class="text-lg font-medium text-gray-900">Email History</h3>
						<Button @click="composeEmail()">
							<div class="flex items-center">
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
										d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
									/>
								</svg>
								Compose Email
							</div>
						</Button>
					</div>

					<!-- Email Table -->
					<div
						class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg"
					>
						<table class="min-w-full divide-y divide-gray-300">
							<thead class="bg-gray-50">
								<tr>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Subject
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Status
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Sent Date
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Actions
									</th>
								</tr>
							</thead>
							<tbody class="bg-white divide-y divide-gray-200">
								<tr v-if="loadingEmails">
									<td
										colspan="4"
										class="px-6 py-4 text-center text-sm text-gray-500"
									>
										Loading...
									</td>
								</tr>
								<tr v-else-if="emailLogs.length === 0">
									<td
										colspan="4"
										class="px-6 py-4 text-center text-sm text-gray-500"
									>
										No emails found
									</td>
								</tr>
								<tr
									v-else
									v-for="item in emailLogs"
									:key="item.name"
									class="hover:bg-gray-50"
								>
									<td
										class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
									>
										{{ item.subject }}
									</td>
									<td class="px-6 py-4 whitespace-nowrap">
										<span
											class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
											:class="getEmailStatusClasses(item.status)"
										>
											{{ item.status }}
										</span>
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
										{{ formatDateTime(item.creation) }}
									</td>
									<td
										class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2"
									>
										<Button
											variant="outline"
											size="sm"
											@click="viewEmailDetails(item)"
										>
											View
										</Button>
										<Button
											variant="outline"
											size="sm"
											@click="replyEmail(item)"
										>
											Reply
										</Button>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>

				<!-- Documents Tab -->
				<div v-if="activeTab === 'documents'">
					<div class="flex justify-between items-center mb-6">
						<h3 class="text-lg font-medium text-gray-900">Documents</h3>
						<Button @click="uploadDocument()">
							<div class="flex items-center">
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
										d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
									/>
								</svg>
								Upload Document
							</div>
						</Button>
					</div>

					<!-- Documents Grid -->
					<div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
						<div
							v-for="doc in documents"
							:key="doc.id"
							class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
						>
							<div class="flex items-center justify-between mb-3">
								<component
									:is="getDocumentIcon(doc.type)"
									class="w-8 h-8 text-blue-600"
								/>
								<div class="relative">
									<button
										class="p-1 text-gray-400 hover:text-gray-600"
										@click="toggleDocumentMenu(doc.id)"
									>
										<svg
											class="w-4 h-4"
											fill="currentColor"
											viewBox="0 0 20 20"
										>
											<path
												d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
											/>
										</svg>
									</button>
								</div>
							</div>
							<h4 class="text-sm font-medium text-gray-900 truncate mb-1">
								{{ doc.name }}
							</h4>
							<p class="text-xs text-gray-500">{{ formatFileSize(doc.size) }}</p>
						</div>

						<!-- Empty state -->
						<div v-if="documents.length === 0" class="col-span-full text-center py-12">
							<svg
								class="w-12 h-12 mx-auto text-gray-400"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
								/>
							</svg>
							<p class="mt-4 text-sm text-gray-500">No documents uploaded</p>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Campaign Assignment Dialog -->
		<Dialog
			:model-value="showCampaignModal"
			@update:model-value="showCampaignModal = $event"
			:options="{
				size: 'md',
			}"
		>
			<template #body>
				<div class="p-6 mb-2">
					<div class="space-y-4">
						<!-- Form Header -->
						<div class="flex items-center justify-between border-b border-gray-200 pb-4 mb-2">
							<div class="flex items-center">
								<div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3">
									<svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
									</svg>
								</div>
								<div>
									<h3 class="text-lg font-medium text-gray-900">Assign to Campaign</h3>
									<p class="text-sm text-gray-500">Add candidate to a campaign</p>
								</div>
							</div>
							<Button variant="outline" @click="closeCampaignModal">
								<div class="flex items-center">
									<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
									</svg>
								</div>
							</Button>
						</div>
					</div>
					<div class="space-y-6">
						<div class="space-y-4">
							<FormControl
								v-model="campaignFormData.campaign_id"
								type="select"
								label="Select Campaign"
								:options="availableCampaigns"
								:required="true"
							/>
							<FormControl
								v-model="campaignFormData.status"
								type="select"
								label="Status"
								:options="statusOptions"
								:required="true"
							/>
							<FormControl
								v-model="campaignFormData.current_step_order"
								type="number"
								label="Starting Step"
								:value="1"
								:min="1"
							/>
						</div>
					</div>
					<div class="flex justify-between w-full mt-2">
						<div class="flex items-center text-sm text-gray-500">
							<svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
								<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
							</svg>
							Candidate will be assigned to campaign
						</div>
						<div class="flex space-x-3">
							<Button variant="outline" @click="closeCampaignModal">Cancel</Button>
							<Button :loading="savingCampaign" @click="assignToCampaign">
								<div class="flex items-center">
									<svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
									</svg>
									Assign
								</div>
							</Button>
						</div>
					</div>
				</div>
			</template>
		</Dialog>

		<!-- Segment Assignment Dialog -->
		<Dialog
			:model-value="showSegmentModal"
			@update:model-value="showSegmentModal = $event"
			:options="{
				size: 'md',
			}"
		>
			<template #body>
				<div class="p-6 mb-2">
					<div class="space-y-4">
						<!-- Form Header -->
						<div class="flex items-center justify-between border-b border-gray-200 pb-4 mb-2">
							<div class="flex items-center">
								<div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center mr-3">
									<svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
									</svg>
								</div>
								<div>
									<h3 class="text-lg font-medium text-gray-900">Add to Segment</h3>
									<p class="text-sm text-gray-500">Add candidate to a talent segment</p>
								</div>
							</div>
							<Button variant="outline" @click="closeSegmentModal">
								<div class="flex items-center">
									<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
									</svg>
								</div>
							</Button>
						</div>
					</div>
					<div class="space-y-6">
						<div class="space-y-4">
							<FormControl
								v-model="segmentFormData.segment_id"
								type="select"
								label="Select Segment"
								:options="availableSegments"
								:required="true"
							/>
						</div>
					</div>
					<div class="flex justify-between w-full mt-2">
						<div class="flex items-center text-sm text-gray-500">
							<svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
								<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
							</svg>
							Candidate will be added to segment
						</div>
						<div class="flex space-x-3">
							<Button variant="outline" @click="closeSegmentModal">Cancel</Button>
							<Button :loading="savingSegment" @click="addToSegment">
								<div class="flex items-center">
									<svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
									</svg>
									Add
								</div>
							</Button>
						</div>
					</div>
				</div>
			</template>
		</Dialog>

		<!-- Interaction Modal -->
		<Dialog
			:model-value="showInteractionModal"
			@update:model-value="showInteractionModal = $event"
			:options="{
				size: 'md',
			}"
		>
			<template #body>
				<div class="p-6 mb-2">
					<div class="space-y-4">
						<!-- Form Header -->
						<div class="flex items-center justify-between border-b border-gray-200 pb-4 mb-2">
							<div class="flex items-center">
								<div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center mr-3">
									<svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
									</svg>
								</div>
								<div>
									<h3 class="text-lg font-medium text-gray-900">Add Interaction</h3>
									<p class="text-sm text-gray-500">Record a new interaction with candidate</p>
								</div>
							</div>
							<Button variant="outline" @click="closeInteractionModal">
								<div class="flex items-center">
									<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
									</svg>
								</div>
							</Button>
						</div>
					</div>
					<div class="space-y-6">
						<div class="space-y-4">
							<FormControl
								v-model="interactionFormData.interaction_type"
								type="select"
								label="Interaction Type"
								:options="interactionTypeOptions"
								:required="true"
							/>
							<FormControl
								v-model="interactionFormData.description"
								type="textarea"
								label="Description"
								:required="true"
							/>
							<FormControl
								v-model="interactionFormData.url"
								type="text"
								label="URL (optional)"
							/>
						</div>
					</div>
					<div class="flex justify-between w-full mt-2">
						<div class="flex items-center text-sm text-gray-500">
							<svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
								<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
							</svg>
							Interaction will be recorded
						</div>
						<div class="flex space-x-3">
							<Button variant="outline" @click="closeInteractionModal">Cancel</Button>
							<Button :loading="savingInteraction" @click="saveInteraction">
								<div class="flex items-center">
									<svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
									</svg>
									Save
								</div>
							</Button>
						</div>
					</div>
				</div>
			</template>
		</Dialog>

		<!-- Document Upload Modal -->
		<Dialog
			:model-value="showDocumentModal"
			@update:model-value="showDocumentModal = $event"
			:options="{
				size: 'md',
			}"
		>
			<template #body>
				<div class="p-6 mb-2">
					<div class="space-y-4">
						<!-- Form Header -->
						<div class="flex items-center justify-between border-b border-gray-200 pb-4 mb-2">
							<div class="flex items-center">
								<div class="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center mr-3">
									<svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
									</svg>
								</div>
								<div>
									<h3 class="text-lg font-medium text-gray-900">Upload Document</h3>
									<p class="text-sm text-gray-500">Upload a document for this candidate</p>
								</div>
							</div>
							<Button variant="outline" @click="closeDocumentModal">
								<div class="flex items-center">
									<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
									</svg>
								</div>
							</Button>
						</div>
					</div>
					<div class="space-y-6">
						<div class="space-y-4">
							<div>
								<label class="block text-sm font-medium text-gray-700 mb-2">Select File</label>
								<input
									ref="fileInput"
									type="file"
									@change="handleFileSelect"
									class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
								/>
							</div>
							<FormControl
								v-model="documentFormData.description"
								type="textarea"
								label="Description (optional)"
							/>
						</div>
					</div>
					<div class="flex justify-between w-full mt-2">
						<div class="flex items-center text-sm text-gray-500">
							<svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
								<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
							</svg>
							Document will be uploaded immediately
						</div>
						<div class="flex space-x-3">
							<Button variant="outline" @click="closeDocumentModal">Cancel</Button>
							<Button :loading="uploadingDocument" @click="saveDocument" :disabled="!selectedFile">
								<div class="flex items-center">
									<svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
									</svg>
									Upload
								</div>
							</Button>
						</div>
					</div>
				</div>
			</template>
		</Dialog>

		<!-- Email Compose Modal -->
		<Dialog
			:model-value="showEmailModal"
			@update:model-value="showEmailModal = $event"
			:options="{
				size: 'lg',
			}"
		>
			<template #body>
				<div class="p-6 mb-2">
					<div class="space-y-4">
						<!-- Form Header -->
						<div class="flex items-center justify-between border-b border-gray-200 pb-4 mb-2">
							<div class="flex items-center">
								<div class="w-10 h-10 bg-indigo-100 rounded-full flex items-center justify-center mr-3">
									<svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
									</svg>
								</div>
								<div>
									<h3 class="text-lg font-medium text-gray-900">Compose Email</h3>
									<p class="text-sm text-gray-500">Send an email to the candidate</p>
								</div>
							</div>
							<Button variant="outline" @click="closeEmailModal">
								<div class="flex items-center">
									<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
									</svg>
								</div>
							</Button>
						</div>
					</div>
					<div class="space-y-6">
						<div class="space-y-4">
							<FormControl
								v-model="emailFormData.to"
								type="text"
								label="To"
								:required="true"
							/>
							<FormControl
								v-model="emailFormData.subject"
								type="text"
								label="Subject"
								:required="true"
							/>
							<FormControl
								v-model="emailFormData.content"
								type="textarea"
								label="Message"
								:required="true"
								:rows="8"
							/>
						</div>
					</div>
					<div class="flex justify-between w-full mt-2">
						<div class="flex items-center text-sm text-gray-500">
							<svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
								<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
							</svg>
							Email will be sent immediately
						</div>
						<div class="flex space-x-3">
							<Button variant="outline" @click="closeEmailModal">Cancel</Button>
							<Button :loading="sendingEmail" @click="sendEmail">
								<div class="flex items-center">
									<svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
									</svg>
									Send Email
								</div>
							</Button>
						</div>
					</div>
				</div>
			</template>
		</Dialog>

		<!-- Edit Candidate Modal -->
		<Dialog
			:model-value="showEditModal"
			@update:model-value="showEditModal = $event"
			:options="{
				size: 'xl',
			}"
		>
			<template #body>
				<div class="p-6 mb-2">
					<div class="space-y-4">
						<!-- Form Header -->
						<div
							class="flex items-center justify-between border-b border-gray-200 pb-4 mb-2"
						>
							<div class="flex items-center">
								<Avatar
									:shape="'circle'"
									:image="candidate.full_name"
									:label="getAvatarText(candidate.full_name)"
									size="lg"
									class="mr-4"
								/>
								<div>
									<h3 class="text-lg font-medium text-gray-900">
										{{ candidate.full_name || 'Candidate' }}
									</h3>
									<p class="text-sm text-gray-500">
										Update candidate information
									</p>
								</div>
							</div>
							<Button variant="outline" @click="closeEditModal">
                <div class="flex items-center">

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
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </div>
							</Button>
						</div>
					</div>
					<div class="space-y-6">
						<!-- Form Fields -->
						<div class="space-y-4">
							<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
								<FormControl
									v-model="editFormData.full_name"
									type="text"
									label="Full Name"
									:required="true"
								/>
								<FormControl
									v-model="editFormData.email"
									type="email"
									label="Email"
									:required="true"
								/>
								<FormControl
									v-model="editFormData.phone"
									type="text"
									label="Phone"
								/>
								<FormControl
									v-model="editFormData.headline"
									type="text"
									label="Headline"
								/>
								<FormControl
									v-model="editFormData.cv_original_url"
									type="text"
									label="CV Link"
								/>
								<FormControl
									v-model="editFormData.status"
									type="select"
									label="Status"
									:options="candidateStatusOptions"
								/>
								<FormControl
									v-model="editFormData.source"
									type="text"
									label="Source"
								/>
							</div>
							<FormControl
								v-model="editFormData.ai_summary"
								type="textarea"
								label="AI Summary"
								:rows="3"
							/>
							<FormControl
								v-model="editFormData.skills"
								type="autocomplete"
								label="Skills"
								placeholder="Type to search or add skills..."
								:options="skillsOptions"
								multiple
								:allow-custom="true"
							/>
						</div>
					</div>
					<div class="flex justify-between w-full mt-2">
						<div class="flex items-center text-sm text-gray-500">
							<svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
								<path
									fill-rule="evenodd"
									d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
									clip-rule="evenodd"
								/>
							</svg>
							Changes will be saved immediately
						</div>
						<div class="flex space-x-3">
							<Button variant="outline" @click="closeEditModal"> Cancel </Button>
							<Button :loading="savingCandidate" @click="saveCandidate">
								<div class="flex items-center">
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
											d="M5 13l4 4L19 7"
										/>
									</svg>
									Save Changes
								</div>
							</Button>
						</div>
					</div>
				</div>
			</template>
		</Dialog>
	</div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Dialog, Button, FormControl, Avatar } from 'frappe-ui'
import {
	candidateService,
	candidateCampaignService,
	candidateSegmentService,
	campaignService,
	talentSegmentService,
	interactionService,
	emailLogService,
} from '../services/universalService'
import { processSkills, skillsToString } from '../services/candidateService'

const route = useRoute()
const router = useRouter()

// State
const activeTab = ref('campaigns')
const loading = ref(false)
const loadingCampaigns = ref(false)
const loadingSegments = ref(false)
const loadingInteractions = ref(false)
const loadingEmails = ref(false)

// Data
const candidate = reactive({})
const candidateCampaigns = ref([])
const candidateSegments = ref([])
const interactions = ref([])
const emailLogs = ref([])
const documents = ref([])

// Available options
const availableCampaigns = ref([])
const availableSegments = ref([])

// Modals
const showCampaignModal = ref(false)
const showSegmentModal = ref(false)
const showInteractionModal = ref(false)
const showDocumentModal = ref(false)
const showEmailModal = ref(false)
const showEditModal = ref(false)
const savingCampaign = ref(false)
const savingSegment = ref(false)
const savingInteraction = ref(false)
const uploadingDocument = ref(false)
const sendingEmail = ref(false)
const savingCandidate = ref(false)

// File upload
const fileInput = ref(null)
const selectedFile = ref(null)

// Form data
const campaignFormData = reactive({
	candidate_id: route.params.id,
	campaign_id: '',
	status: 'ACTIVE',
	current_step_order: 1,
})

const segmentFormData = reactive({
	candidate_id: route.params.id,
	segment_id: '',
})

const interactionFormData = reactive({
	candidate_id: route.params.id,
	interaction_type: '',
	description: '',
	url: '',
})

const documentFormData = reactive({
	candidate_id: route.params.id,
	description: '',
})

const emailFormData = reactive({
	to: '',
	subject: '',
	content: '',
})

const editFormData = reactive({
	full_name: '',
	email: '',
	phone: '',
	headline: '',
	cv_original_url: '',
	status: '',
	source: '',
	ai_summary: '',
	skills: '',
})

// Options
const statusOptions = [
	{ label: 'Active', value: 'ACTIVE' },
	{ label: 'Paused', value: 'PAUSED' },
	{ label: 'Completed', value: 'COMPLETED' },
	{ label: 'Cancelled', value: 'CANCELLED' },
]

const candidateStatusOptions = [
	{ label: 'New', value: 'NEW' },
	{ label: 'Sourced', value: 'SOURCED' },
	{ label: 'Nurturing', value: 'NURTURING' },
	{ label: 'Engaged', value: 'ENGAGED' },
	{ label: 'Archived', value: 'ARCHIVED' },
]

const interactionTypeOptions = [
	{ label: 'Email Sent', value: 'EMAIL_SENT' },
	{ label: 'Email Delivered', value: 'EMAIL_DELIVERED' },
	{ label: 'Email Bounced', value: 'EMAIL_BOUNCED' },
	{ label: 'Email Opened', value: 'EMAIL_OPENED' },
	{ label: 'Email Clicked', value: 'EMAIL_CLICKED' },
	{ label: 'Phone Call', value: 'PHONE_CALL' },
	{ label: 'Meeting', value: 'MEETING' },
	{ label: 'Note', value: 'NOTE' },
]

const skillsOptions = [
	// Programming Languages
	{ label: 'JavaScript', value: 'javascript' },
	{ label: 'TypeScript', value: 'typescript' },
	{ label: 'Python', value: 'python' },
	{ label: 'Java', value: 'java' },
	{ label: 'C#', value: 'csharp' },
	{ label: 'C++', value: 'cpp' },
	{ label: 'PHP', value: 'php' },
	{ label: 'Go', value: 'go' },
	{ label: 'Rust', value: 'rust' },
	{ label: 'Ruby', value: 'ruby' },
	{ label: 'Swift', value: 'swift' },
	{ label: 'Kotlin', value: 'kotlin' },
	
	// Frontend Frameworks
	{ label: 'React', value: 'react' },
	{ label: 'Vue.js', value: 'vuejs' },
	{ label: 'Angular', value: 'angular' },
	{ label: 'Next.js', value: 'nextjs' },
	{ label: 'Nuxt.js', value: 'nuxtjs' },
	{ label: 'Svelte', value: 'svelte' },
	
	// Backend Frameworks
	{ label: 'Node.js', value: 'nodejs' },
	{ label: 'Express.js', value: 'expressjs' },
	{ label: 'Django', value: 'django' },
	{ label: 'Flask', value: 'flask' },
	{ label: 'Spring Boot', value: 'springboot' },
	{ label: 'Laravel', value: 'laravel' },
	{ label: 'ASP.NET', value: 'aspnet' },
	{ label: 'FastAPI', value: 'fastapi' },
	
	// Databases
	{ label: 'MySQL', value: 'mysql' },
	{ label: 'PostgreSQL', value: 'postgresql' },
	{ label: 'MongoDB', value: 'mongodb' },
	{ label: 'Redis', value: 'redis' },
	{ label: 'SQLite', value: 'sqlite' },
	{ label: 'Oracle', value: 'oracle' },
	{ label: 'SQL Server', value: 'sqlserver' },
	
	// Cloud & DevOps
	{ label: 'AWS', value: 'aws' },
	{ label: 'Azure', value: 'azure' },
	{ label: 'Google Cloud', value: 'gcp' },
	{ label: 'Docker', value: 'docker' },
	{ label: 'Kubernetes', value: 'kubernetes' },
	{ label: 'Jenkins', value: 'jenkins' },
	{ label: 'CI/CD', value: 'cicd' },
	{ label: 'Terraform', value: 'terraform' },
	
	// Tools & Technologies
	{ label: 'Git', value: 'git' },
	{ label: 'Linux', value: 'linux' },
	{ label: 'Agile', value: 'agile' },
	{ label: 'Scrum', value: 'scrum' },
	{ label: 'REST API', value: 'restapi' },
	{ label: 'GraphQL', value: 'graphql' },
	{ label: 'Microservices', value: 'microservices' },
	{ label: 'Machine Learning', value: 'ml' },
	{ label: 'Data Science', value: 'datascience' },
	{ label: 'AI', value: 'ai' },
]

// Tab icons as SVG components
const CampaignIcon = {
	render() {
		return h(
			'svg',
			{
				class: 'w-4 h-4',
				fill: 'none',
				stroke: 'currentColor',
				viewBox: '0 0 24 24',
			},
			[
				h('path', {
					'stroke-linecap': 'round',
					'stroke-linejoin': 'round',
					'stroke-width': '2',
					d: 'M13 10V3L4 14h7v7l9-11h-7z',
				}),
			],
		)
	},
}

const SegmentIcon = {
	render() {
		return h(
			'svg',
			{
				class: 'w-4 h-4',
				fill: 'none',
				stroke: 'currentColor',
				viewBox: '0 0 24 24',
			},
			[
				h('path', {
					'stroke-linecap': 'round',
					'stroke-linejoin': 'round',
					'stroke-width': '2',
					d: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z',
				}),
			],
		)
	},
}

const InteractionIcon = {
	render() {
		return h(
			'svg',
			{
				class: 'w-4 h-4',
				fill: 'none',
				stroke: 'currentColor',
				viewBox: '0 0 24 24',
			},
			[
				h('path', {
					'stroke-linecap': 'round',
					'stroke-linejoin': 'round',
					'stroke-width': '2',
					d: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-3.582 8-8 8a8.001 8.001 0 01-7.227-4.612 2.5 2.5 0 00-.673-2.388A8 8 0 0112 4c4.418 0 8 3.582 8 8z',
				}),
			],
		)
	},
}

const EmailIcon = {
	render() {
		return h(
			'svg',
			{
				class: 'w-4 h-4',
				fill: 'none',
				stroke: 'currentColor',
				viewBox: '0 0 24 24',
			},
			[
				h('path', {
					'stroke-linecap': 'round',
					'stroke-linejoin': 'round',
					'stroke-width': '2',
					d: 'M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
				}),
			],
		)
	},
}

const DocumentIcon = {
	render() {
		return h(
			'svg',
			{
				class: 'w-4 h-4',
				fill: 'none',
				stroke: 'currentColor',
				viewBox: '0 0 24 24',
			},
			[
				h('path', {
					'stroke-linecap': 'round',
					'stroke-linejoin': 'round',
					'stroke-width': '2',
					d: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
				}),
			],
		)
	},
}

// Computed
const tabs = computed(() => [
	{
		key: 'campaigns',
		label: 'Active Campaigns',
		count: candidateCampaigns.value.length,
		icon: CampaignIcon,
	},
	{
		key: 'segments',
		label: 'Segments',
		count: candidateSegments.value.length,
		icon: SegmentIcon,
	},
	{
		key: 'interactions',
		label: 'Interactions',
		count: interactions.value.length,
		icon: InteractionIcon,
	},
	{
		key: 'emails',
		label: 'Email History',
		count: emailLogs.value.length,
		icon: EmailIcon,
	},
	{
		key: 'documents',
		label: 'Documents',
		count: documents.value.length,
		icon: DocumentIcon,
	},
])

// Methods
const getAvatarText = (name) => {
	if (!name) return '?'
	return name.charAt(0).toUpperCase()
}

const getStatusClasses = (status) => {
	const statusClasses = {
		ACTIVE: 'bg-green-100 text-green-800',
		PAUSED: 'bg-yellow-100 text-yellow-800',
		COMPLETED: 'bg-blue-100 text-blue-800',
		CANCELLED: 'bg-red-100 text-red-800',
		NEW: 'bg-blue-100 text-blue-800',
		SOURCED: 'bg-yellow-100 text-yellow-800',
		NURTURING: 'bg-orange-100 text-orange-800',
		ENGAGED: 'bg-green-100 text-green-800',
		ARCHIVED: 'bg-gray-100 text-gray-800',
	}
	return statusClasses[status] || 'bg-gray-100 text-gray-800'
}

const getTypeClasses = (type) => {
	const typeClasses = {
		DYNAMIC: 'bg-blue-100 text-blue-800',
		MANUAL: 'bg-green-100 text-green-800',
	}
	return typeClasses[type] || 'bg-gray-100 text-gray-800'
}

const getEmailStatusClasses = (status) => {
	const statusClasses = {
		Success: 'bg-green-100 text-green-800',
		Failed: 'bg-red-100 text-red-800',
		Fallback: 'bg-yellow-100 text-yellow-800',
	}
	return statusClasses[status] || 'bg-gray-100 text-gray-800'
}

const getInteractionBgClasses = (type) => {
	const colors = {
		EMAIL_SENT: 'bg-blue-500',
		EMAIL_DELIVERED: 'bg-green-500',
		EMAIL_BOUNCED: 'bg-red-500',
		EMAIL_OPENED: 'bg-blue-600',
		EMAIL_CLICKED: 'bg-green-600',
		DEFAULT: 'bg-gray-500',
	}
	return colors[type] || colors.DEFAULT
}

const getInteractionIcon = (type) => {
	const iconMap = {
		EMAIL_SENT: {
			render() {
				return h('svg', { class: 'w-4 h-4', fill: 'currentColor', viewBox: '0 0 20 20' }, [
					h('path', {
						d: 'M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z',
					}),
					h('path', { d: 'M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z' }),
				])
			},
		},
		EMAIL_DELIVERED: {
			render() {
				return h('svg', { class: 'w-4 h-4', fill: 'currentColor', viewBox: '0 0 20 20' }, [
					h('path', {
						'fill-rule': 'evenodd',
						d: 'M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z',
						'clip-rule': 'evenodd',
					}),
				])
			},
		},
		EMAIL_BOUNCED: {
			render() {
				return h('svg', { class: 'w-4 h-4', fill: 'currentColor', viewBox: '0 0 20 20' }, [
					h('path', {
						'fill-rule': 'evenodd',
						d: 'M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z',
						'clip-rule': 'evenodd',
					}),
				])
			},
		},
		EMAIL_OPENED: {
			render() {
				return h('svg', { class: 'w-4 h-4', fill: 'currentColor', viewBox: '0 0 20 20' }, [
					h('path', { d: 'M10 12a2 2 0 100-4 2 2 0 000 4z' }),
					h('path', {
						'fill-rule': 'evenodd',
						d: 'M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z',
						'clip-rule': 'evenodd',
					}),
				])
			},
		},
		EMAIL_CLICKED: {
			render() {
				return h('svg', { class: 'w-4 h-4', fill: 'currentColor', viewBox: '0 0 20 20' }, [
					h('path', {
						'fill-rule': 'evenodd',
						d: 'M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z',
						'clip-rule': 'evenodd',
					}),
				])
			},
		},
	}

	return iconMap[type] || iconMap['EMAIL_SENT']
}

const getDocumentIcon = (type) => {
	const iconMap = {
		pdf: {
			render() {
				return h('svg', { class: 'w-8 h-8', fill: 'currentColor', viewBox: '0 0 20 20' }, [
					h('path', {
						'fill-rule': 'evenodd',
						d: 'M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z',
						'clip-rule': 'evenodd',
					}),
				])
			},
		},
		doc: {
			render() {
				return h('svg', { class: 'w-8 h-8', fill: 'currentColor', viewBox: '0 0 20 20' }, [
					h('path', {
						'fill-rule': 'evenodd',
						d: 'M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z',
						'clip-rule': 'evenodd',
					}),
				])
			},
		},
		image: {
			render() {
				return h('svg', { class: 'w-8 h-8', fill: 'currentColor', viewBox: '0 0 20 20' }, [
					h('path', {
						'fill-rule': 'evenodd',
						d: 'M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z',
						'clip-rule': 'evenodd',
					}),
				])
			},
		},
	}

	return iconMap[type] || iconMap['doc']
}

const formatDate = (date) => {
	if (!date) return ''
	return new Date(date).toLocaleDateString('en-US', {
		year: 'numeric',
		month: 'short',
		day: 'numeric',
	})
}

const formatDateTime = (date) => {
	if (!date) return ''
	return new Date(date).toLocaleDateString('en-US', {
		year: 'numeric',
		month: 'short',
		day: 'numeric',
		hour: '2-digit',
		minute: '2-digit',
	})
}

const formatFileSize = (size) => {
	if (size < 1024) return size + ' B'
	if (size < 1024 * 1024) return (size / 1024).toFixed(1) + ' KB'
	return (size / (1024 * 1024)).toFixed(1) + ' MB'
}

const formatInteractionType = (type) => {
	const labels = {
		EMAIL_SENT: 'Email Sent',
		EMAIL_DELIVERED: 'Email Delivered',
		EMAIL_BOUNCED: 'Email Bounced',
		EMAIL_OPENED: 'Email Opened',
		EMAIL_CLICKED: 'Link Clicked',
	}
	return labels[type] || type.replace(/_/g, ' ')
}

// Load data methods
const loadCandidate = async () => {
	loading.value = true
	try {
		const result = await candidateService.getFormData(route.params.id)
		if (result.success) {
			Object.assign(candidate, result.data)
		}
	} catch (error) {
		console.error('Error loading candidate:', error)
	} finally {
		loading.value = false
	}
}

const loadCandidateCampaigns = async () => {
	loadingCampaigns.value = true
	try {
		const result = await candidateCampaignService.getList({
			filters: { candidate_id: route.params.id },
			fields: [
				'name',
				'campaign_id',
				'campaign_name',
				'status',
				'current_step_order',
				'next_action_at',
			],
		})
		if (result.success) {
			candidateCampaigns.value = result.data
		}
	} catch (error) {
		console.error('Error loading candidate campaigns:', error)
	} finally {
		loadingCampaigns.value = false
	}
}

const loadCandidateSegments = async () => {
	loadingSegments.value = true
	try {
		const candidateSegmentResult = await candidateSegmentService.getList({
			filters: { candidate_id: route.params.id },
			fields: ['name', 'segment_id', 'added_at', 'added_by'],
		})

		if (candidateSegmentResult.success && candidateSegmentResult.data.length > 0) {
			const segmentIds = candidateSegmentResult.data.map((cs) => cs.segment_id)

			const segmentResult = await talentSegmentService.getList({
				filters: { name: ['in', segmentIds] },
				fields: ['name', 'title', 'description', 'type', 'candidate_count'],
			})

			if (segmentResult.success) {
				candidateSegments.value = segmentResult.data.map((segment) => {
					const segmentRelation = candidateSegmentResult.data.find(
						(cs) => cs.segment_id === segment.name,
					)
					return {
						...segment,
						added_at: segmentRelation?.added_at,
						added_by: segmentRelation?.added_by,
						candidate_segment_id: segmentRelation?.name,
					}
				})
			}
		} else {
			candidateSegments.value = []
		}
	} catch (error) {
		console.error('Error loading candidate segments:', error)
		candidateSegments.value = []
	} finally {
		loadingSegments.value = false
	}
}

const loadInteractions = async () => {
	loadingInteractions.value = true
	try {
		const result = await interactionService.getList({
			filters: { candidate_id: route.params.id },
			fields: ['name', 'interaction_type', 'description', 'url', 'creation'],
			order_by: 'creation desc',
		})
		if (result.success) {
			interactions.value = result.data
		}
	} catch (error) {
		console.error('Error loading interactions:', error)
	} finally {
		loadingInteractions.value = false
	}
}

const loadEmailLogs = async () => {
	loadingEmails.value = true
	try {
		const candidateEmail = candidate.email
		let filters = {}

		if (candidateEmail) {
			filters.recipients = ['like', `%${candidateEmail}%`]
		} else {
			emailLogs.value = []
			loadingEmails.value = false
			return
		}

		const result = await emailLogService.getList({
			filters: filters,
			fields: ['name', 'subject', 'content', 'status', 'creation'],
			order_by: 'creation desc',
		})
		if (result.success) {
			emailLogs.value = result.data
		}
	} catch (error) {
		console.error('Error loading email logs:', error)
	} finally {
		loadingEmails.value = false
	}
}

const loadAvailableCampaigns = async () => {
	try {
		const result = await campaignService.getList({
			fields: ['name', 'campaign_name'],
			page_length: 1000,
		})
		if (result.success) {
			availableCampaigns.value = result.data.map((item) => ({
				label: item.campaign_name || item.name,
				value: item.name,
			}))
		}
	} catch (error) {
		console.error('Error loading campaigns:', error)
	}
}

const loadAvailableSegments = async () => {
	try {
		const result = await talentSegmentService.getList({
			fields: ['name', 'segment_name'],
			page_length: 1000,
		})
		if (result.success) {
			availableSegments.value = result.data.map((item) => ({
				label: item.segment_name || item.name,
				value: item.name,
			}))
		}
	} catch (error) {
		console.error('Error loading segments:', error)
	}
}

// Campaign methods
const openCampaignModal = () => {
	Object.keys(campaignFormData).forEach((key) => {
		if (key !== 'candidate_id') {
			campaignFormData[key] = ''
		}
	})
	campaignFormData.status = 'ACTIVE'
	campaignFormData.current_step_order = 1
	showCampaignModal.value = true
}

const closeCampaignModal = () => {
	showCampaignModal.value = false
}

const assignToCampaign = async () => {
	savingCampaign.value = true
	try {
		const result = await candidateCampaignService.save(campaignFormData)
		if (result.success) {
			closeCampaignModal()
			loadCandidateCampaigns()
		}
	} catch (error) {
		console.error('Error assigning to campaign:', error)
	} finally {
		savingCampaign.value = false
	}
}

// Segment methods
const openSegmentModal = () => {
	segmentFormData.segment_id = ''
	showSegmentModal.value = true
}

const closeSegmentModal = () => {
	showSegmentModal.value = false
}

const addToSegment = async () => {
	savingSegment.value = true
	try {
		const result = await candidateSegmentService.save(segmentFormData)
		if (result.success) {
			closeSegmentModal()
			loadCandidateSegments()
		}
	} catch (error) {
		console.error('Error adding to segment:', error)
	} finally {
		savingSegment.value = false
	}
}

// Action methods
const startCampaign = async (item) => {
	try {
		const result = await candidateCampaignService.save(
			{ ...item, status: 'ACTIVE' },
			item.name,
		)
		if (result.success) {
			loadCandidateCampaigns()
		}
	} catch (error) {
		console.error('Error starting campaign:', error)
	}
}

const pauseCampaign = async (item) => {
	try {
		const result = await candidateCampaignService.save(
			{ ...item, status: 'PAUSED' },
			item.name,
		)
		if (result.success) {
			loadCandidateCampaigns()
		}
	} catch (error) {
		console.error('Error pausing campaign:', error)
	}
}

const viewCampaignDetails = (item) => {
	router.push(`/campaigns/${item.campaign_id}`)
}

const removeCampaign = async (item) => {
	if (confirm('Are you sure you want to remove this candidate from the campaign?')) {
		try {
			const result = await candidateCampaignService.delete(item.name)
			if (result.success) {
				loadCandidateCampaigns()
			}
		} catch (error) {
			console.error('Error removing campaign:', error)
		}
	}
}

const viewSegmentDetails = (item) => {
	router.push(`/talent-segments/${item.name}/detail`)
}

const removeFromSegment = async (item) => {
	if (confirm('Are you sure you want to remove this candidate from the segment?')) {
		try {
			const result = await candidateSegmentService.delete(item.candidate_segment_id)
			if (result.success) {
				loadCandidateSegments()
			}
		} catch (error) {
			console.error('Error removing from segment:', error)
		}
	}
}

const editCandidate = () => {
	// Populate form with current candidate data
	Object.assign(editFormData, {
		full_name: candidate.full_name || '',
		email: candidate.email || '',
		phone: candidate.phone || '',
		headline: candidate.headline || '',
		cv_original_url: candidate.cv_original_url || '',
		status: candidate.status || '',
		source: candidate.source || '',
		ai_summary: candidate.ai_summary || '',
		skills: processSkills(candidate.skills),
	})
	showEditModal.value = true
}

const closeEditModal = () => {
	showEditModal.value = false
}

const saveCandidate = async () => {
	savingCandidate.value = true
	try {
		// Prepare data for saving
		const saveData = { ...editFormData }

		// Convert skills array to text string for backend storage
		saveData.skills = skillsToString(saveData.skills)

		const result = await candidateService.save(saveData, route.params.id)
		if (result.success) {
			// Update local candidate data
			Object.assign(candidate, result.data)
			closeEditModal()
			// Show success message
			console.log('Candidate updated successfully')
		}
	} catch (error) {
		console.error('Error saving candidate:', error)
	} finally {
		savingCandidate.value = false
	}
}

const deleteCandidate = async () => {
	if (confirm('Are you sure you want to delete this candidate?')) {
		try {
			const result = await candidateService.delete(route.params.id)
			if (result.success) {
				router.push('/candidates')
			}
		} catch (error) {
			console.error('Error deleting candidate:', error)
		}
	}
}

// Interaction methods
const openInteractionModal = () => {
	Object.keys(interactionFormData).forEach((key) => {
		if (key !== 'candidate_id') {
			interactionFormData[key] = ''
		}
	})
	showInteractionModal.value = true
}

const closeInteractionModal = () => {
	showInteractionModal.value = false
}

const saveInteraction = async () => {
	savingInteraction.value = true
	try {
		const result = await interactionService.save(interactionFormData)
		if (result.success) {
			closeInteractionModal()
			loadInteractions()
		}
	} catch (error) {
		console.error('Error saving interaction:', error)
	} finally {
		savingInteraction.value = false
	}
}

// Document methods
const uploadDocument = () => {
	documentFormData.description = ''
	selectedFile.value = null
	showDocumentModal.value = true
}

const closeDocumentModal = () => {
	showDocumentModal.value = false
}

const handleFileSelect = (event) => {
	selectedFile.value = event.target.files[0]
}

const saveDocument = async () => {
	if (!selectedFile.value) return

	uploadingDocument.value = true
	try {
		// Implementation would depend on your file upload service
		// This is a placeholder for the actual implementation
		console.log('Uploading document:', selectedFile.value)
		closeDocumentModal()
		// loadDocuments() // You would need to implement this method
	} catch (error) {
		console.error('Error uploading document:', error)
	} finally {
		uploadingDocument.value = false
	}
}

// Email methods
const composeEmail = () => {
	emailFormData.to = candidate.email || candidate.candidate_email || ''
	emailFormData.subject = ''
	emailFormData.content = ''
	showEmailModal.value = true
}

const closeEmailModal = () => {
	showEmailModal.value = false
}

const sendEmail = async () => {
	sendingEmail.value = true
	try {
		// Implementation would depend on your email service
		// This is a placeholder for the actual implementation
		console.log('Sending email:', emailFormData)
		closeEmailModal()
		loadEmailLogs()
	} catch (error) {
		console.error('Error sending email:', error)
	} finally {
		sendingEmail.value = false
	}
}

const viewEmailDetails = (item) => {
	// Implementation for viewing email details
	console.log('View email details:', item)
}

const replyEmail = (item) => {
	emailFormData.to = candidate.email || candidate.candidate_email || ''
	emailFormData.subject = `Re: ${item.subject}`
	emailFormData.content = ''
	showEmailModal.value = true
}

const toggleDocumentMenu = (docId) => {
	// Implementation for document menu
	console.log('Toggle document menu for:', docId)
}

// Lifecycle
onMounted(async () => {
	await loadCandidate()
	await loadCandidateCampaigns()
	await loadCandidateSegments()
	await loadInteractions()
	await loadEmailLogs()
	await loadAvailableCampaigns()
	await loadAvailableSegments()
})
</script>

<style scoped>
/* Custom transitions */
.candidate-detail-view button {
	transition: all 0.2s ease-in-out;
}

.candidate-detail-view .hover\:shadow-md:hover {
	box-shadow:
		0 4px 6px -1px rgba(0, 0, 0, 0.1),
		0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
</style>
