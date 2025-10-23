<template>
	<div class="min-h-screen bg-gray-50">
		<!-- Header -->
		<div class="bg-white border-b border-gray-200 px-6 py-4">
			<div class="flex items-center justify-between">
				<!-- Left: Breadcrumb -->
				<div class="flex items-center space-x-2">
					<Button variant="ghost" size="sm" @click="handleBack">
						<template #prefix>
							<FeatherIcon name="arrow-left" class="h-4 w-4" />
						</template>
					</Button>
					

					<!-- Editable Title -->
					<div class="flex items-center space-x-2">
						<div v-if="!editingTitle" class="flex items-center space-x-2">
							<span class="text-sm text-gray-600">{{
								flowData.title || 'Flow Editor'
							}}</span>
							<Button
								variant="ghost"
								size="sm"
								@click="startEditTitle"
								class="p-1 h-8 w-8"
							>
								<FeatherIcon
									name="edit"
									class="h-4 w-4 text-black hover:text-gray-600"
								/>
							</Button>
						</div>

						<div v-else class="flex items-center space-x-2">
							<FormControl
								v-model="editTitleValue"
								type="text"
								class="text-sm min-w-48"
								@keyup.enter="saveTitle"
								@keyup.escape="cancelEditTitle"
								ref="titleInput"
							/>
							<Button
								variant="ghost"
								size="sm"
								@click="saveTitle"
								class="p-1 h-6 w-8"
							>
								<FeatherIcon name="check" class="h-4 w-4 text-green-600" />
							</Button>
							<Button
								variant="ghost"
								size="sm"
								@click="cancelEditTitle"
								class="p-1 h-6 w-8"
							>
								<FeatherIcon name="x" class="h-4 w-4 text-red-600" />
							</Button>
						</div>
					</div>
				</div>

				<!-- Right: Actions -->
				<div class="flex items-center space-x-3">
					
					<Button 
						:variant="hasUnsavedChanges ? 'solid' : 'outline'" 
						size="sm" 
						@click="handleSave" 
						:loading="saving"
						:class="hasUnsavedChanges ? 'bg-orange-600 hover:bg-orange-700' : ''"
					>
						<template #prefix>
							<FeatherIcon name="save" class="h-4 w-4" />
						</template>
						{{ hasUnsavedChanges ? 'Save*' : 'Save' }}
					</Button>
					<Button variant="solid" theme="green" size="sm">{{ __('Publish') }} </Button>
				</div>
			</div>
		</div>

		<!-- Main Content -->
		<div class="flex h-[calc(100vh-80px)]">
			<!-- Column 1: Triggers & Actions List -->
			<div class="w-80 bg-white border-r border-gray-200 flex flex-col">
				<!-- Triggers Section -->
				<div class="flex-1 p-4 overflow-auto">
					<div class="mb-6">
						<h3 class="text-sm font-medium text-gray-900 mb-3">{{ __('Trigger') }}</h3>
						<p class="text-xs text-gray-500 mb-4">{{ __('Event that triggers this flow') }}</p>

						<!-- Add Trigger Button -->
						<Button
							variant="outline"
							size="sm"
							class="w-full mb-4"
							@click="showAddTrigger = true"
						>
							<template #prefix>
								<FeatherIcon name="plus" class="h-4 w-4" />
							</template>
							{{ __('Add Trigger') }}
						</Button>

						<!-- Triggers List -->
						<div class="space-y-2">
							<div
								v-for="(trigger, index) in flowData.triggers"
								:key="`trigger-${index}`"
								class="group relative p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
								:class="{
									'border-blue-500 bg-blue-50':
										selectedItem?.type === 'trigger' &&
										selectedItem?.index === index,
								}"
								@click="selectItem('trigger', index)"
							>
								<!-- Delete button - appears on hover -->
								<button
									@click.stop="deleteTrigger(index)"
									class="absolute -top-1 -right-2 w-6 h-6 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-200 hover:bg-red-600 flex items-center justify-center"
									:title="__('Delete Trigger')"
								>
									<FeatherIcon name="trash-2" class="h-3 w-3" />
								</button>
								
								<div class="flex items-start space-x-3">
									<div
										class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center"
									>
										<FeatherIcon name="zap" class="h-4 w-4 text-blue-600" />
									</div>
									<div class="flex-1 min-w-0 pr-8">
										<h4 class="text-sm font-medium text-gray-900 truncate">
											{{
												trigger._ui_name ||
												trigger.name ||
												'Trigger không tên'
											}}
										</h4>
										<p class="text-xs text-gray-500 mt-1">
											{{
												trigger._ui_description ||
												trigger.description ||
												'Không có mô tả'
											}}
										</p>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Actions Section -->
					<div>
						<h3 class="text-sm font-medium text-gray-900 mb-3">{{ __('Actions') }}</h3>
						<p class="text-xs text-gray-500 mb-4">{{ __('Actions that will be executed') }}</p>

						<!-- Add Action Button -->
						<Button
							variant="outline"
							size="sm"
							class="w-full mb-4"
							@click="showAddAction = true"
						>
							<template #prefix>
								<FeatherIcon name="plus" class="h-4 w-4" />
							</template>
							{{ __('Add Action') }}
						</Button>

						<!-- Actions List -->
						<div class="space-y-2">
							<div
								v-for="(action, index) in flowData.actions"
								:key="`action-${index}`"
								class="group relative p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
								:class="{
									'border-blue-500 bg-blue-50':
										selectedItem?.type === 'action' &&
										selectedItem?.index === index,
								}"
								@click="selectItem('action', index)"
							>
								<!-- Delete button - appears on hover -->
								<button
									@click.stop="deleteAction(index)"
									class="absolute -top-1 -right-2 w-6 h-6 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-200 hover:bg-red-600 flex items-center justify-center"
									:title="__('Delete Action')"
								>
									<FeatherIcon name="trash-2" class="h-3 w-3" />
								</button>
								
								<div class="flex items-start space-x-3">
									<div
										class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center"
									>
										<FeatherIcon name="play" class="h-4 w-4 text-purple-600" />
									</div>
									<div class="flex-1 min-w-0 pr-8">
										<h4 class="text-sm font-medium text-gray-900 truncate">
											{{
												action._ui_name ||
												action.name ||
												'Action không tên'
											}}
										</h4>
										<p class="text-xs text-gray-500 mt-1">
											{{
												action._ui_description ||
												action.description ||
												'Không có mô tả'
											}}
										</p>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Column 2: Configuration Panel -->
			<div class="flex-1 bg-white border-r border-gray-200 overflow-auto">
				<div class="p-6">
					<!-- Header -->
					<div class="mb-6">
						<div class="flex items-center justify-between">
							<h2 class="text-lg font-medium text-gray-900">
								{{ selectedItem ? getSelectedItemTitle() : __('Select Trigger') }}
							</h2>
							<Button
								v-if="selectedItem"
								variant="ghost"
								size="sm"
								@click="selectedItem = null"
							>
								<FeatherIcon name="x" class="h-4 w-4" />
							</Button>
						</div>
						<p class="text-sm text-gray-500 mt-1">
							{{
								selectedItem
									? getSelectedItemDescription()
									: __('Select a trigger or action to configure')
							}}
						</p>
					</div>

					<!-- Configuration Panel Content -->
					<div v-if="selectedItem" class="space-y-6">
						<!-- Content Editors for Send_Message Actions -->
						<div v-if="selectedItem.type === 'action' && isEmailAction()">
							<h4 class="text-md font-medium text-gray-900 mb-4">{{ __('Email Configuration') }}</h4>
							<EmailEditor
								:content="getEmailContent()"
								@update:content="updateEmailContent"
								:readonly="false"
							/>
							
							<!-- Additional Actions for Email -->
							<div class="mt-6">
								<AdditionalActions
									interaction-type="EMAIL"
									:model-value="getAdditionalActionsData()"
									@update:model-value="updateAdditionalActionsData"
								/>
							</div>
						</div>

						<div v-else-if="selectedItem.type === 'action' && isZaloAction()">
							<h4 class="text-md font-medium text-gray-900 mb-4">{{ __('Zalo Configuration') }}</h4>
							<ZaloEditor
								:content="getZaloContent()"
								@update:content="updateZaloContent"
								:readonly="false"
							/>
							
							<!-- Additional Actions for Zalo -->
							<div class="mt-6">
								<AdditionalActions
									interaction-type="ZALO_CARE"
									:model-value="getAdditionalActionsData()"
									@update:model-value="updateAdditionalActionsData"
								/>
							</div>
						</div>

						<!-- SMS Action -->
						<div v-else-if="selectedItem.type === 'action' && isSMSAction()">
							<h4 class="text-md font-medium text-gray-900 mb-4">{{ __('SMS Configuration') }}</h4>
							<ZaloEditor
								:content="getSMSContent()"
								@update:content="updateSMSContent"
								:readonly="false"
								:available-flows="flows"
							/>
							
							<!-- Additional Actions for SMS -->
							<div class="mt-6">
								<AdditionalActions
									interaction-type="EMAIL"
									:model-value="getAdditionalActionsData()"
									@update:model-value="updateAdditionalActionsData"
								/>
							</div>
						</div>

						<!-- Add Tag Action -->
						<div v-else-if="selectedItem.type === 'action' && isAddTagAction()">
							<h4 class="text-md font-medium text-gray-900 mb-4">	{{ __('Add Tag') }}</h4>
							<div class="space-y-4">
								<!-- Select existing tags -->
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-2">
										{{ __('Select existing tags') }}
									</label>
									
									<!-- Selected tags display -->
									<div v-if="selectedTagsDisplay?.length > 0" class="mb-3">
										<div class="flex flex-wrap gap-2">
											<div
												v-for="tag in selectedTagsDisplay"
												:key="tag.value"
												class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800 border border-blue-200"
											>
												<span>{{ tag.label }}</span>
												<button
													@click="removeSelectedTag(tag.value)"
													class="ml-2 text-blue-600 hover:text-blue-800 focus:outline-none"
												>
													<FeatherIcon name="x" class="h-3 w-3" />
												</button>
											</div>
										</div>
									</div>
									
									<!-- Tag selector -->
									<FormControl
										type="select"
										v-model="selectedTagToAdd"
										:options="availableTagOptions"
										:placeholder="__('Select existing tags')"
										:loading="tagsLoading"
										@change="addSelectedTag"
									/>
								</div>
								
								<!-- Or create new tag -->
								<div class="text-center text-sm text-gray-500">
									{{ __('Or') }}
								</div>
								
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-2">
										{{ __('Create new tag') }}
									</label>
									<div class="flex space-x-2">
										<FormControl
											v-model="newTagName"
											type="text"
											:placeholder="__('New tag name (VD: Webinar MBWN DMS 2110)')"
											class="flex-1"
										/>
										<Button 
											variant="outline" 
											size="sm"
											:loading="creatingTag"
											@click="createNewTag"
										>
											<template #prefix>
												<FeatherIcon name="plus" class="h-4 w-4" />
											</template>
											{{ __('Add') }}
										</Button>
									</div>
								</div>
								
								<p class="text-xs text-gray-500">
									{{ __('Tag will be added to the folder and assigned to the candidate') }}
								</p>
								<p v-if="selectedTagsDisplay.length === 0 && !newTagName.trim()" class="text-red-500 text-xs">
									{{ __('Please select an existing tag or create a new tag') }}
								</p>
							</div>
						</div>

						<!-- Remove Tag Action -->
						<div v-else-if="selectedItem.type === 'action' && isRemoveTagAction()">
							<h4 class="text-md font-medium text-gray-900 mb-4">Xóa Tag</h4>
							<ActionConfig
								action-type="remove_tag"
								:action-data="selectedItemData.parameters"
								@update:action-data="updateActionData"
							/>
						</div>

						<!-- Smart Delay Action -->
						<div v-else-if="selectedItem.type === 'action' && isSmartDelayAction()">
							<h4 class="text-md font-medium text-gray-900 mb-4">{{ __('Smart Delay') }}</h4>
							<div class="space-y-4">
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-2">
										{{ __('Duration') }}
									</label>
									<FormControl
										v-model="selectedItemData.parameters.duration"
										type="text"
										:placeholder="__('VD: 1 day, 2 hours, 30 minutes...')"
										@input="hasUnsavedChanges = true"
									/>
								</div>
							</div>
						</div>

						<!-- Add Custom Field Action -->
						<div v-else-if="selectedItem.type === 'action' && isAddCustomFieldAction()">
							<h4 class="text-md font-medium text-gray-900 mb-4">{{ __('Add Custom Field') }}</h4>
							<div class="space-y-4">
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-2">
										{{ __('Field Name') }}
									</label>
									<FormControl
										v-model="selectedItemData.parameters.field_name"
										type="text"
										:placeholder="__('Enter field name')"
										@input="hasUnsavedChanges = true"
									/>
								</div>
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-2">
										{{ __('Value') }}
									</label>
									<FormControl
										v-model="selectedItemData.parameters.field_value"
										type="text"
										:placeholder="__('Enter value')"
										@input="hasUnsavedChanges = true"
									/>
								</div>
							</div>
						</div>

						<!-- Start Flow Action -->
						<div v-else-if="selectedItem.type === 'action' && isStartFlowAction()">
							<h4 class="text-md font-medium text-gray-900 mb-4">{{ __('Start Flow') }}</h4>
							<div class="space-y-4">
								<!-- Flow Selection -->
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-2">
										{{ __('Flow') }}
									</label>
									
									<!-- Debug info -->
									<!-- <div class="mb-2 p-2 bg-gray-100 rounded text-xs">
										<div>Current flow_id: {{ selectedItemData.parameters?.flow_id }}</div>
										<div>Available options: {{ availableFlowOptions.length }}</div>
										<div>Loading: {{ flowsLoading }}</div>
									</div> -->
									
									<FormControl
										type="select"
										v-model="selectedItemData.parameters.flow_id"
										:options="availableFlowOptions"
										:placeholder="__('Select flow to start')"
										:loading="flowsLoading"
									/>
									<p class="text-xs text-gray-500 mt-1">
										{{ __('Select a different flow to start (cannot select the current flow)') }}
									</p>
								</div>
							</div>
						</div>

						<!-- Subscribe to Sequence Action -->
						<div v-else-if="selectedItem.type === 'action' && isSubscribeSequenceAction()">
							<h4 class="text-md font-medium text-gray-900 mb-4">{{ __('Subscribe to Sequence') }}</h4>
							<div class="space-y-4">
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-2">
										{{ __('Sequence ID') }}
									</label>
									<FormControl
										v-model="selectedItemData.parameters.sequence_id"
										type="text"
										:placeholder="__('Enter sequence ID')"
										@input="hasUnsavedChanges = true"
									/>
								</div>
							</div>
						</div>

						<!-- Generic Parameters for other actions -->
						<div v-else-if="selectedItem.type === 'action'" class="space-y-4">
							<div>
								<h4 class="text-md font-medium text-gray-900 mb-4">{{ __('Parameters') }}</h4>

								<!-- Generic parameters display -->
								<div class="bg-gray-50 p-4 rounded-lg">
									<p class="text-sm text-gray-600 mb-2">{{ __('Action Type') }}: {{ selectedItemData.action_type }}</p>
									<p class="text-sm text-gray-500">{{ __('No UI configuration available for this action type.') }}</p>
								</div>
							</div>
						</div>

						<!-- Trigger Configuration -->
						<div v-else-if="selectedItem.type === 'trigger'" class="space-y-4">
							<TriggerEditor
								:content="selectedItemData"
								@update:content="updateTriggerContent"
								:readonly="false"
							/>
						</div>

						<!-- Action Buttons -->
						<div class="flex justify-end pt-6 border-t border-gray-200">
							<Button variant="outline" @click="handleDeleteItem">
								<template #prefix>
									<FeatherIcon name="trash-2" class="h-4 w-4" />
								</template>
								{{ __('Delete') }}
							</Button>

							<!-- <Button variant="solid" @click="handleSaveItem">
								<template #prefix>
									<FeatherIcon name="save" class="h-4 w-4" />
								</template>
								Lưu
							</Button> -->
						</div>
					</div>

					<!-- Empty State -->
					<div v-else class="text-center py-12">
						<FeatherIcon name="settings" class="mx-auto h-12 w-12 text-gray-400" />
						<h3 class="mt-2 text-sm font-medium text-gray-900">{{ __('Select an item') }}</h3>
						<p class="mt-1 text-sm text-gray-500">
							{{ __('Select a trigger or action from the list on the left to begin configuring.') }}
						</p>
					</div>
				</div>
			</div>

			<!-- Column 3: Mobile Preview -->
			<div class="w-96 bg-gray-100 p-6">
				<div class="text-center mb-4">
					<h3 class="text-sm font-medium text-gray-900">{{ __('Preview') }}</h3>
					<p class="text-xs text-gray-500">{{ __('Preview on mobile') }}</p>
				</div>

				<!-- Mobile Frame - iPhone Style -->
				<div
					class="mx-auto w-80 h-[600px] bg-gradient-to-b from-gray-800 to-gray-900 rounded-[2.5rem] p-1 shadow-2xl border border-gray-700"
				>
					<!-- Outer Frame -->
					<div class="w-full h-full bg-black rounded-[2rem] p-1 relative">
						<!-- Screen -->
						<div
							class="w-full h-full bg-white rounded-[1.8rem] relative overflow-hidden shadow-inner"
						>
							<!-- Dynamic Island (iPhone 14 Pro style) -->
							<div
								class="absolute top-2 left-1/2 transform -translate-x-1/2 w-32 h-6 bg-black rounded-full z-10 shadow-lg"
							>
								<!-- Camera and sensors -->
								<div
									class="absolute top-1.5 left-4 w-2 h-2 bg-gray-800 rounded-full"
								></div>
								<div
									class="absolute top-2 right-4 w-1 h-1 bg-gray-700 rounded-full"
								></div>
							</div>

							<!-- Status Bar -->
							<div
								class="flex justify-between items-center px-6 py-3 bg-white relative z-0"
							>
								<div class="flex items-center space-x-1">
									<span class="text-sm font-semibold">9:41</span>
								</div>
								<div class="flex items-center space-x-1">
									<!-- Signal Bars -->
									<div class="flex items-end space-x-0.5">
										<div class="w-1 h-2 bg-black rounded-full"></div>
										<div class="w-1 h-3 bg-black rounded-full"></div>
										<div class="w-1 h-4 bg-black rounded-full"></div>
										<div class="w-1 h-3 bg-gray-300 rounded-full"></div>
									</div>
									<!-- WiFi -->
									<svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
										<path
											d="M1 9l2 2c4.97-4.97 13.03-4.97 18 0l2-2C16.93 2.93 7.07 2.93 1 9zm8 8l3 3 3-3c-1.65-1.66-4.34-1.66-6 0zm-4-4l2 2c2.76-2.76 7.24-2.76 10 0l2-2C15.14 9.14 8.87 9.14 5 13z"
										/>
									</svg>
									<!-- Battery -->
									<div class="flex items-center">
										<div
											class="w-6 h-3 border border-black rounded-sm relative"
										>
											<div class="w-4 h-full bg-green-500 rounded-sm"></div>
										</div>
										<div
											class="w-0.5 h-1.5 bg-black rounded-r-sm ml-0.5"
										></div>
									</div>
								</div>
							</div>

							<!-- Home Indicator -->
							<div
								class="absolute bottom-2 left-1/2 transform -translate-x-1/2 w-32 h-1 bg-black rounded-full opacity-60 shadow-sm"
							></div>

							<!-- Screen Reflection Effect -->
							<div
								class="absolute inset-0 bg-gradient-to-br from-white/10 via-transparent to-transparent pointer-events-none rounded-[1.8rem]"
							></div>

							<!-- Content -->
							<div class="p-4 h-full overflow-y-auto pb-8">
								<!-- Email Preview -->
								<div
									v-if="
										selectedItem &&
										selectedItem.type === 'action' &&
										isEmailAction()
									"
									:key="`email-${previewKey}`"
									class="space-y-4 mb-6"
								>
									<!-- Email Header -->
									<div class="border-b border-gray-200 pb-3">
										<div class="flex items-center space-x-2 mb-2">
											<FeatherIcon
												name="mail"
												class="h-4 w-4 text-blue-600"
											/>
											<span class="text-xs font-medium text-gray-900"
												>{{ __('Email Preview') }}</span
											>
										</div>
										<div class="text-xs text-gray-500">
											<div>{{ __('From') }}: {{ emailContent.from_email }}</div>
											<div>{{ __('To') }}: {{ emailContent.to_email }}</div>
										</div>
									</div>

									<!-- Email Subject -->
									<div class="bg-gray-50 p-3 rounded-lg">
										<div class="text-xs font-medium text-gray-700 mb-1">
											{{ __('Subject') }}
										</div>
										<div class="text-sm text-gray-900">
											{{
												emailContent.email_subject ||
												__('No subject')
											}}
										</div>
									</div>

									<!-- Email Body -->
									<div class="bg-white border border-gray-200 rounded-lg p-3">
										<div class="text-xs font-medium text-gray-700 mb-2">
											Content:
										</div>
										<div class="text-sm text-gray-800 whitespace-pre-wrap">
											{{
												emailContent.email_content ||
												__('No email content')
											}}
										</div>
									</div>

									<!-- Attachments -->
									<div
										v-if="
											emailContent.attachments &&
											emailContent.attachments.length > 0
										"
										class="space-y-2"
									>
										<div class="text-xs font-medium text-gray-700">
											{{ __('Attachments') }}
										</div>
										<div
											v-for="(file, index) in emailContent.attachments"
											:key="index"
											class="flex items-center space-x-2 text-xs text-gray-600"
										>
											<FeatherIcon name="paperclip" class="h-3 w-3" />
											<span>{{ file.file_name }}</span>
										</div>
									</div>
								</div>

								<!-- Zalo Preview -->
								<div
									v-else-if="
										selectedItem &&
										selectedItem.type === 'action' &&
										isZaloAction()
									"
									:key="`zalo-${previewKey}`"
									class="space-y-4"
								>
									<!-- Zalo Header -->
									<div class="flex items-center space-x-3 mb-4">
										<div
											class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center"
										>
											<span class="text-white text-xs font-bold">Z</span>
										</div>
										<div>
											<div class="text-xs font-medium text-gray-900">
												{{ __('Zalo message') }}
											</div>
											<p class="text-xs text-gray-500">
												{{ __('Today at 10:46 AM') }}
											</p>
										</div>
									</div>

									<!-- Zalo Messages -->
									<div class="space-y-3 mb-6">
										<div
											v-for="(block, index) in zaloContent.blocks"
											:key="block.id || index"
											class="bg-blue-500 text-white p-3 rounded-lg rounded-br-sm max-w-[280px] ml-auto"
										>
											<!-- Image Block -->
											<div v-if="block.type === 'image'" class="mb-2">
												<img
													v-if="block.image"
													:src="
														block.image.file_url || block.image.preview
													"
													class="w-full rounded-lg max-h-32 object-cover"
													:alt="block.image.file_name || 'Zalo image'"
												/>
												<div
													v-else
													class="w-full h-24 bg-white bg-opacity-20 rounded-lg flex items-center justify-center"
												>
													<div class="text-center">
														<FeatherIcon
															name="image"
															class="h-6 w-6 text-blue-100 mx-auto mb-1"
														/>
														<span class="text-xs text-blue-100"
															>Chưa có ảnh</span
														>
													</div>
												</div>
											</div>

											<!-- Text Content -->
											<div v-if="block.text_content" class="text-sm mb-2">
												{{ block.text_content }}
											</div>

											<!-- Website URL -->
											<div v-if="block.website_url" class="mb-2">
												<div class="bg-white bg-opacity-20 rounded-md p-2">
													<div class="flex items-center space-x-2">
														<FeatherIcon
															name="globe"
															class="h-3 w-3 text-blue-100"
														/>
														<span
															class="text-xs text-blue-100 truncate"
															>{{ block.website_url }}</span
														>
													</div>
												</div>
											</div>

											<!-- Phone Number -->
											<div v-if="block.phone_number" class="mb-2">
												<div class="bg-white bg-opacity-20 rounded-md p-2">
													<div class="flex items-center space-x-2">
														<FeatherIcon
															name="phone"
															class="h-3 w-3 text-blue-100"
														/>
														<span class="text-xs text-blue-100">{{
															block.phone_number
														}}</span>
													</div>
												</div>
											</div>

											<!-- Flow Trigger -->
											<div v-if="block.flow_trigger" class="mb-2">
												<div class="bg-white bg-opacity-20 rounded-md p-2">
													<div class="flex items-center space-x-2">
														<FeatherIcon
															name="play-circle"
															class="h-3 w-3 text-blue-100"
														/>
														<span class="text-xs text-blue-100"
															>Start: {{ block.flow_trigger }}</span
														>
													</div>
												</div>
											</div>

											<!-- Timestamp -->
											<div class="text-xs text-blue-100 mt-2 text-right">
												{{
													new Date().toLocaleTimeString('vi-VN', {
														hour: '2-digit',
														minute: '2-digit',
													})
												}}
											</div>
										</div>

										<!-- Empty state if no blocks -->
										<div
											v-if="
												!zaloContent.blocks ||
												zaloContent.blocks.length === 0
											"
											class="bg-blue-500 text-white p-3 rounded-lg rounded-br-sm max-w-[280px] ml-auto"
										>
											<div class="text-sm">Chưa có nội dung tin nhắn</div>
											<div class="text-xs text-blue-100 mt-1 text-right">
												{{
													new Date().toLocaleTimeString('vi-VN', {
														hour: '2-digit',
														minute: '2-digit',
													})
												}}
											</div>
										</div>
									</div>

									<!-- Character Count -->
									<div class="text-xs text-gray-500 text-center">
										{{ totalZaloCharacters }}/2000 ký tự
									</div>
								</div>

								<!-- SMS Preview -->
								<div
									v-else-if="
										selectedItem &&
										selectedItem.type === 'action' &&
										isSMSAction()
									"
									:key="`sms-${previewKey}`"
									class="space-y-4"
								>
									<!-- SMS Header -->
									<div class="flex items-center space-x-3 mb-4">
										<div
											class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center"
										>
											<FeatherIcon name="message-square" class="h-4 w-4 text-white" />
										</div>
										<div>
											<div class="text-xs font-medium text-gray-900">
												{{ __('SMS message') }}
											</div>
											<p class="text-xs text-gray-500">
												{{ __('Today at 10:46 AM') }}
											</p>
										</div>
									</div>

									<!-- SMS Message Bubbles -->
									<div class="space-y-3 mb-6" :class="{ 'opacity-75 transition-opacity duration-200': isPreviewUpdating }">
										<!-- Text Message Bubble -->
										<div v-if="smsContent.message" class="bg-green-500 text-white p-3 rounded-lg rounded-br-sm max-w-[280px] ml-auto">
											<div class="text-sm whitespace-pre-wrap">
												{{ smsContent.message }}
											</div>
											
											<!-- Timestamp -->
											<div class="text-xs text-green-100 mt-2 text-right">
												{{
													new Date().toLocaleTimeString('vi-VN', {
														hour: '2-digit',
														minute: '2-digit',
													})
												}}
											</div>
										</div>

										<!-- Image Bubbles -->
										<div 
											v-for="(image, imageIndex) in smsImages" 
											:key="`sms-image-${image.id || imageIndex}-${image.file_name}`"
											class="bg-green-500 text-white p-2 rounded-lg rounded-br-sm max-w-[280px] ml-auto"
										>
											<img 
												:src="image.file_url" 
												:alt="image.file_name"
												class="w-full rounded-lg max-h-32 object-cover"
											/>
											<div class="text-xs text-green-100 mt-1 text-right">
												{{
													new Date().toLocaleTimeString('vi-VN', {
														hour: '2-digit',
														minute: '2-digit',
													})
												}}
											</div>
										</div>

										<!-- Flow Trigger Bubbles -->
										<div 
											v-for="(block, blockIndex) in smsFlowTriggers" 
											:key="`sms-flow-${block.id || blockIndex}`"
											class="bg-green-500 text-white p-3 rounded-lg rounded-br-sm max-w-[280px] ml-auto"
										>
											<div class="flex items-center space-x-2 mb-2">
												<FeatherIcon
													name="play-circle"
													class="h-4 w-4 text-green-100"
												/>
												<span class="text-sm">{{ __('Start Flow') }}</span>
											</div>
											<div class="text-sm font-medium">
												{{ block.flow_display_name || block.flow_trigger || __('Unknown Flow') }}
											</div>
											<div class="text-xs text-green-100 mt-2 text-right">
												{{
													new Date().toLocaleTimeString('vi-VN', {
														hour: '2-digit',
														minute: '2-digit',
													})
												}}
											</div>
										</div>

										<!-- Empty state -->
										<div v-if="!smsContent.message && (!smsImages || smsImages.length === 0) && (!smsFlowTriggers || smsFlowTriggers.length === 0)" class="bg-green-500 text-white p-3 rounded-lg rounded-br-sm max-w-[280px] ml-auto">
											<div class="text-sm">{{ __('No SMS content') }}</div>
											<div class="text-xs text-green-100 mt-1 text-right">
												{{
													new Date().toLocaleTimeString('vi-VN', {
														hour: '2-digit',
														minute: '2-digit',
													})
												}}
											</div>
										</div>
									</div>

									<!-- Character Count -->
									<div class="text-xs text-gray-500 text-center">
										{{ (smsContent.message || '').length }}/160 characters
									</div>
									
									<!-- Debug Info (temporary) -->
									<!-- <div class="text-xs text-red-500 text-center mt-2" style="font-family: monospace;">
										Debug: "{{ smsContent.message }}"
									</div> -->
								</div>

								<!-- Default Preview -->
								<div v-else class="text-center py-8">
									<FeatherIcon
										name="smartphone"
										class="mx-auto h-12 w-12 text-gray-400 mb-3"
									/>
									<h3 class="text-sm font-medium text-gray-900 mb-1">Preview</h3>
									<p class="text-xs text-gray-500">
										{{ __('Select an action to view the preview') }}
									</p>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Add Trigger Modal -->
		<Dialog v-model="showAddTrigger" :options="{ title: 'Add Trigger', size: 'md' }">
			<template #body-content>
				<div class="space-y-4">
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-2">
							{{ __('Search trigger') }}
						</label>
						<FormControl
							v-model="triggerSearch"
							type="text"
							:placeholder="__('Search trigger')"
						/>
					</div>
					<div class="max-h-60 overflow-y-auto">
						<div class="space-y-2">
							<div
								v-for="trigger in filteredTriggerOptions"
								:key="trigger.id"
								class="relative p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
								:class="{ 'opacity-50 pointer-events-none': addingTrigger }"
								@click="handleAddTrigger(trigger)"
								:disabled="addingTrigger"
							>
								<!-- Loading overlay -->
								<div v-if="addingTrigger" class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75 rounded-lg">
									<div class="flex items-center space-x-2">
										<div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
										<span class="text-sm text-gray-600">{{ __('Adding...') }}</span>
									</div>
								</div>
								
								<h4 class="text-sm font-medium text-gray-900">
									{{ trigger.name }}
								</h4>
								<p class="text-xs text-gray-500">{{ trigger.description }}</p>
							</div>
						</div>
					</div>
				</div>
			</template>
		</Dialog>

		<!-- Add Action Modal -->
		<Dialog v-model="showAddAction" :options="{ title: 'Add Action', size: 'md' }">
			<template #body-content>
				<div class="space-y-4">
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-2">
							{{ __('Search action') }}
						</label>
						<FormControl
							v-model="actionSearch"
							type="text"
							:placeholder="__('Search action')"
						/>
					</div>
					<div class="max-h-60 overflow-y-auto">
						<div class="space-y-2">
							<div
								v-for="action in filteredActionOptions"
								:key="action.value"
								class="relative p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
								:class="{ 'opacity-50 pointer-events-none': addingAction }"
								@click="handleAddAction(action)"
								:disabled="addingAction"
							>
								<!-- Loading overlay -->
								<div v-if="addingAction" class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75 rounded-lg">
									<div class="flex items-center space-x-2">
										<div class="animate-spin rounded-full h-4 w-4 border-b-2 border-purple-600"></div>
										<span class="text-sm text-gray-600">{{ __('Adding...') }}</span>
									</div>
								</div>
								
								<h4 class="text-sm font-medium text-gray-900">
									{{ action.label }}
								</h4>
								<p class="text-xs text-gray-500">{{ action.description }}</p>
							</div>
						</div>
					</div>
				</div>
			</template>
		</Dialog>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMiraFlowStore } from '../stores/miraFlow'
import { useTagStore } from '../stores/tag'
import { useToast } from '../composables/useToast'

// Components
import { Button, FormControl, Dialog, FeatherIcon } from 'frappe-ui'
import EmailEditor from '../components/campaign/content-editors/EmailEditor.vue'
import ZaloEditor from '../components/campaign/content-editors/ZaloEditor.vue'
import TriggerEditor from '../components/campaign/content-editors/TriggerEditor.vue'
import Link from '../components/Controls/Link.vue'
import ActionConfig from '../components/campaign/ActionConfig.vue'
import AdditionalActions from '../components/campaign/AdditionalActions.vue'
import { storeToRefs } from 'pinia'

// Router
const route = useRoute()
const router = useRouter()

// Store
const flowStore = useMiraFlowStore()
const { flows, loading: flowsLoading } = storeToRefs(flowStore)
const tagStore = useTagStore()
const { tags, loading: tagsLoading } = storeToRefs(tagStore)

// Toast
const toast = useToast()

// Translation function
const __ = (text) => text

// Reactive data
const saving = ref(false)
const selectedItem = ref(null)
const selectedItemData = ref({})
const showAddTrigger = ref(false)
const showAddAction = ref(false)
const triggerSearch = ref('')
const actionSearch = ref('')
const editingTitle = ref(false)
const editTitleValue = ref('')
const previewKey = ref(0) // Key to force preview re-render
const titleInput = ref(null)
const hasUnsavedChanges = ref(false)

// Tag management
const newTagName = ref('')
const creatingTag = ref(false)
const selectedTagToAdd = ref('')

// Loading states for modal items
const addingTrigger = ref(false)
const addingAction = ref(false)

// Flow data
const flowData = ref({
	name: '',
	title: '',
	description: '',
	status: 'Draft',
	triggers: [],
	actions: [],
})

// Options
const triggerTypeOptions = [
	{ label: 'Webhook', value: 'webhook' },
	{ label: 'Schedule', value: 'schedule' },
	{ label: 'Manual', value: 'manual' },
	{ label: 'Event', value: 'event' },
]

const actionTypeOptions = [
	{ label: 'Send Email', value: 'send_email' },
	{ label: 'Send SMS', value: 'send_sms' },
	{ label: 'Create Record', value: 'create_record' },
	{ label: 'Update Record', value: 'update_record' },
	{ label: 'HTTP Request', value: 'http_request' },
]

const availableTriggers = [
	{
		id: 'on_create',
		name: 'On Create',
		description: 'Trigger when creating a new record',
		icon: 'plus-circle',
		event_type: 'ON_CREATE',
		trigger_type: 'on_create',
		sequence_id: '',
		connected_account: '',
		channels: [],
		conditions: [],
	},
	{
		id: 'on_update',
		name: 'On Update',
		description: 'Trigger when updating a record',
		icon: 'edit',
		event_type: 'ON_UPDATE',
		trigger_type: 'on_update',
		sequence_id: '',
		connected_account: '',
		channels: [],
		conditions: [],
	},
	{
		id: 'on_tag_added',
		name: 'On Tag Added',
		description: 'Trigger when a tag is added to a record',
		icon: 'tag',
		event_type: 'ON_TAG_ADDED',
		trigger_type: 'on_tag_added',
		sequence_id: '',
		connected_account: '',
		channels: [],
		conditions: [],
	},
	{
		id: 'on_status_changed',
		name: 'On Status Changed',
		description: 'Trigger when a record status changes',
		icon: 'refresh-cw',
		event_type: 'ON_STATUS_CHANGED',
		trigger_type: 'on_status_changed',
		sequence_id: '',
		connected_account: '',
		channels: [],
		conditions: [],
	},
	{
		id: 'on_sequence_completed',
		name: 'On Sequence Completed',
		description: 'Trigger when a sequence is completed',
		icon: 'check-circle',
		event_type: 'ON_SEQUENCE_COMPLETED',
		trigger_type: 'on_sequence_completed',
		sequence_id: '',
		connected_account: '',
		channels: [],
		conditions: [],
	},
	{
		id: 'on_scheduled_time',
		name: 'On Scheduled Time',
		description: 'Trigger when a scheduled time is reached',
		icon: 'clock',
		event_type: 'ON_SCHEDULED_TIME',
		trigger_type: 'on_scheduled_time',
		sequence_id: '',
		connected_account: '',
		channels: [],
		conditions: [],
	},
	{
		id: 'on_score_reached',
		name: 'On Score Reached',
		description: 'Trigger when a score is reached',
		icon: 'target',
		event_type: 'ON_SCORE_REACHED',
		trigger_type: 'on_score_reached',
		sequence_id: '',
		connected_account: '',
		channels: [],
		conditions: [],
	},
	{
		id: 'custom_event',
		name: 'Custom Event',
		description: 'Trigger by a custom event',
		icon: 'settings',
		event_type: 'CUSTOM_EVENT',
		trigger_type: 'custom_event',
		sequence_id: '',
		connected_account: '',
		channels: [],
		conditions: [],
	},
	{
		id: 'form_submit',
		name: 'Form Submitted',
		description: 'Trigger when a form is submitted',
		icon: 'file-text',
		event_type: 'Form_Submitted',
		criteria: { form_name: '' },
	},
	{
		id: 'schedule',
		name: 'Schedule',
		description: 'Trigger by a schedule',
		icon: 'clock',
		event_type: 'Schedule_Trigger',
		criteria: { schedule: '' },
	},
]

const availableActions = [
	{
		label: 'Send Email',
		value: 'send_email',
		description: 'Send email to customer',
		action_type: 'MESSAGE',
		parameters: {
			channel: 'Email',
			template_id: '',
			email_content: {
				email_subject: '',
				email_content: '',
				attachments: [],
			},
		},
	},
	{
		label: 'Send SMS',
		value: 'send_sms',
		description: 'Send SMS to customer',
		action_type: 'SMS',
		parameters: {
			channel: 'SMS',
			template_id: '',
			sms_content: {
				message: '',
			},
		},
	},
	{
		label: 'Send Zalo',
		value: 'send_zalo',
		description: 'Send Zalo message to customer',
		action_type: 'ZALO',
		parameters: {
			channel: 'Zalo',
			template_id: '',
			zalo_content: {
				blocks: [
					{
						id: 1,
						type: 'text',
						text_content: '',
					},
				],
			},
		},
	},
	{
		label: 'Smart Delay',
		value: 'smart_delay',
		description: 'Wait for a certain amount of time before the next action',
		action_type: 'SMART_DELAY',
		parameters: { duration: '1 day' },
	},
	{
		label: 'Add Tag',
		value: 'add_tag',
		description: 'Add tag to customer',
		action_type: 'ADD_TAG',
		parameters: { tag_name: '' },
	},
	{
		label: 'Remove Tag',
		value: 'remove_tag',
		description: 'Remove tag from customer',
		action_type: 'REMOVE_TAG',
		parameters: { tag_name: '' },
	},
	{
		label: 'Add Custom Field',
		value: 'add_custom_field',
		description: 'Add custom field to customer',
		action_type: 'ADD_CUSTOM_FIELD',
		parameters: { field_name: '', field_value: '' },
	},
	{
		label: 'Start Flow',
		value: 'start_flow',
		description: 'Start another flow',
		action_type: 'START_FLOW',
		parameters: { flow_id: '' },
	},
	{
		label: 'Subscribe to Sequence',
		value: 'subscribe_to_sequence',
		description: 'Subscribe customer to sequence',
		action_type: 'SUBSCRIBE_TO_SEQUENCE',
		parameters: { sequence_id: '' },
	},
]

// Computed
const filteredTriggerOptions = computed(() => {
	if (!triggerSearch.value) return availableTriggers
	return availableTriggers.filter(
		(trigger) =>
			trigger.name.toLowerCase().includes(triggerSearch.value.toLowerCase()) ||
			trigger.description.toLowerCase().includes(triggerSearch.value.toLowerCase()),
	)
})

const filteredActionOptions = computed(() => {
	if (!actionSearch.value) return availableActions
	return availableActions.filter(
		(action) =>
			action.label.toLowerCase().includes(actionSearch.value.toLowerCase()) ||
			action.description.toLowerCase().includes(actionSearch.value.toLowerCase()),
	)
})

// Methods
const loadFlow = async () => {
	const flowId = route.params.id
	console.log('Loading flow with ID:', flowId)

	if (!flowId) {
		console.error('No flow ID provided')
		toast.error('Không tìm thấy ID flow')
		router.push({ name: 'FlowManagement' })
		return
	}

	try {
		console.log('Calling fetchFlowById...')
		const result = await flowStore.fetchFlowById(flowId)
		console.log('fetchFlowById result:', result)

		if (result && result.success && result.data) {
			const flow = result.data
			console.log('Flow data received:', flow)

			// Process child table data
			const processedTriggers = flow.triggers ? flow.triggers.map(trigger => ({
				// Map child table fields to UI format
				...trigger,
				_ui_name: getDefaultTriggerName(trigger.trigger_type),
				_ui_description: getDefaultTriggerDescription(trigger.trigger_type),
				_ui_type: trigger.trigger_type,
				// Map backend fields to frontend format
				event_type: trigger.trigger_type,
				trigger_type: mapTriggerType(trigger.trigger_type),
				Conditional_Split: (() => {
					try {
						return trigger.conditions ? JSON.parse(trigger.conditions) : []
					} catch (error) {
						console.warn('Error parsing trigger conditions:', error)
						return []
					}
				})(),
				connected_account: trigger.owner_id,
				channels: trigger.channel ? [trigger.channel] : [],
				// Override name for display
				name: getDefaultTriggerName(trigger.trigger_type),
				description: getDefaultTriggerDescription(trigger.trigger_type)
			})) : []

			const processedActions = flow.actions ? flow.actions.map(action => ({
				// Map child table fields to UI format
				...action,
				_ui_name: getDefaultActionName(action.action_type),
				_ui_description: getDefaultActionDescription(action.action_type),
				_ui_type: action.action_type,
				// Map backend fields to frontend format
				action_order: action.order,
				parameters: (() => {
					try {
						return action.action_parameters ? JSON.parse(action.action_parameters) : {}
					} catch (error) {
						console.warn('Error parsing action parameters:', error)
						return {}
					}
				})(),
				// Override name for display
				name: getDefaultActionName(action.action_type),
				description: getDefaultActionDescription(action.action_type)
			})) : []

			flowData.value = {
				name: flow.name,
				title: flow.title || '',
				description: flow.description || '',
				status: flow.status || 'Draft',
				triggers: processedTriggers,
				actions: processedActions,
			}

			console.log('Flow data set:', flowData.value)
			console.log('Processed triggers:', processedTriggers)
			console.log('Processed actions:', processedActions)
		} else {
			console.error('Invalid result:', result)
			toast.error('Không thể tải thông tin flow')
			router.push({ name: 'FlowManagement' })
		}
	} catch (error) {
		console.error('Error loading flow:', error)
		toast.error('Có lỗi xảy ra khi tải flow')
		router.push({ name: 'FlowManagement' })
	}
}

// Helper functions for mapping backend data to frontend format
const getDefaultTriggerName = (triggerType) => {
	const triggerMap = {
		'ON_CREATE': 'On Create',
		'ON_UPDATE': 'On Update', 
		'ON_TAG_ADDED': 'On Tag Added',
		'ON_STATUS_CHANGED': 'On Status Changed',
		'ON_SEQUENCE_COMPLETED': 'On Sequence Completed',
		'ON_SCHEDULED_TIME': 'On Scheduled Time',
		'ON_SCORE_REACHED': 'On Score Reached',
		'CUSTOM_EVENT': 'Custom Event'
	}
	return triggerMap[triggerType] || triggerType
}

const getDefaultTriggerDescription = (triggerType) => {
	const descriptionMap = {
		'ON_CREATE': 'Trigger when creating a record',
		'ON_UPDATE': 'Trigger when updating a record',
		'ON_TAG_ADDED': 'Trigger when adding a tag',
		'ON_STATUS_CHANGED': 'Trigger when changing status',
		'ON_SEQUENCE_COMPLETED': 'Trigger when completing a sequence',
		'ON_SCHEDULED_TIME': 'Trigger by a schedule',
		'ON_SCORE_REACHED': 'Trigger when reaching a score',
		'CUSTOM_EVENT': 'Trigger by a custom event'
	}
	return descriptionMap[triggerType] || 'No description'
}

const mapTriggerType = (backendType) => {
	const typeMap = {
		'ON_CREATE': 'on_create',
		'ON_UPDATE': 'on_update',
		'ON_TAG_ADDED': 'on_tag_added',
		'ON_STATUS_CHANGED': 'on_status_changed',
		'ON_SEQUENCE_COMPLETED': 'on_sequence_completed',
		'ON_SCHEDULED_TIME': 'on_scheduled_time',
		'ON_SCORE_REACHED': 'on_score_reached',
		'CUSTOM_EVENT': 'custom_event'
	}
	return typeMap[backendType] || backendType
}

const getDefaultActionName = (actionType) => {
	const actionMap = {
		'MESSAGE': 'Send Message',
		'SMS': 'Send SMS',
		'EMAIL': 'Send Email',
		'ZALO': 'Send Zalo',
		'ZALO_CARE': 'Zalo Care',
		'START_FLOW': 'Start Flow',
		'SUBSCRIBE_TO_SEQUENCE': 'Subscribe to Sequence',
		'UN_SUBSCRIBE_TO_SEQUENCE': 'Unsubscribe from Sequence',
		'SMART_DELAY': 'Smart Delay',
		'AI_CALL': 'Call AI',
		'ADD_TAG': 'Add Tag',
		'REMOVE_TAG': 'Remove Tag',
		'ADD_CUSTOM_FIELD': 'Add Custom Field',
		'REMOVE_CUSTOM_FIELD': 'Remove Custom Field',
		'LEAD_SCORE': 'Lead Score',
		'EXTERNAL_REQUEST': 'External Request',
		'EMAIL_AI': 'Email AI',
		'CONTENT_AI': 'Content AI',
		'SENT_NOTIFICATION': 'Send Notification'
	}
	return actionMap[actionType] || actionType
}

const getDefaultActionDescription = (actionType) => {
	const descriptionMap = {
		'MESSAGE': 'Send message to customer',
		'SMS': 'Send SMS',
		'EMAIL': 'Send Email',
		'ZALO': 'Send Zalo',
		'ZALO_CARE': 'Send Zalo Care',
		'START_FLOW': 'Start another flow',
		'SUBSCRIBE_TO_SEQUENCE': 'Subscribe customer to sequence',
		'UN_SUBSCRIBE_TO_SEQUENCE': 'Unsubscribe customer from sequence',
		'SMART_DELAY': 'Smart delay based on conditions',
		'AI_CALL': 'Call AI to process',
		'ADD_TAG': 'Add tag to customer',
		'REMOVE_TAG': 'Remove tag from customer',
		'ADD_CUSTOM_FIELD': 'Add custom field to customer',
		'REMOVE_CUSTOM_FIELD': 'Remove custom field from customer',
		'LEAD_SCORE': 'Lead Score',
		'EXTERNAL_REQUEST': 'External Request',
		'EMAIL_AI': 'Email AI',
		'CONTENT_AI': 'Content AI',
		'SENT_NOTIFICATION': 'Send Notification'
	}
	return descriptionMap[actionType] || 'No description'
}

// Ensure UI fields exist for display
const ensureUIFields = (items, type) => {
	return items.map((item, index) => {
		// If UI fields already exist, return as is
		if (item._ui_name && item._ui_description) {
			return item
		}

		// Create UI fields based on backend data
		if (type === 'trigger') {
			const triggerOption = availableTriggers.find(
				(t) =>
					t.event_type === item.event_type || t.source_platform === item.source_platform,
			)

			return {
				...item,
				_ui_name:
					item._ui_name ||
					triggerOption?.label ||
					`${item.source_platform} ${item.event_type}`,
				_ui_description:
					item._ui_description || triggerOption?.description || 'Trigger tự động',
				_ui_type: item._ui_type || item.event_type,
			}
		} else {
			const actionOption = availableActions.find(
				(a) =>
					a.action_type === item.action_type &&
					a.parameters?.channel === item.parameters?.channel,
			)

			return {
				...item,
				_ui_name: item._ui_name || actionOption?.label || `${item.action_type}`,
				_ui_description:
					item._ui_description || actionOption?.description || 'Hành động tự động',
				_ui_type: item._ui_type || item.action_type,
			}
		}
	})
}

// Migrate old format to new backend format
const migrateToNewFormat = (items, type) => {
	console.log(`Migrating ${type}s:`, items)

	if (!Array.isArray(items)) {
		console.error(`Items is not an array for ${type}:`, items)
		return []
	}

	return items.map((item, index) => {
		console.log(`Processing ${type} ${index}:`, item)

		// If already in new format, return as is
		if (type === 'trigger' && item.trigger_id) {
			console.log('Already in new trigger format')
			return item
		}
		if (type === 'action' && item.action_order !== undefined) {
			console.log('Already in new action format')
			return item
		}

		// Migrate old format to new format
		if (type === 'trigger') {
			// Find matching trigger option for proper name/description
			const triggerOption = availableTriggers.find(
				(t) =>
					t.event_type === (item.type || item.event_type) ||
					t.value === (item.type || item.event_type),
			)

			const migrated = {
				trigger_id: `TGR${String(Date.now() + index).slice(-6)}`,
				source_platform:
					item.source_platform || triggerOption?.source_platform || 'Manual',
				event_type: item.type || item.event_type || 'Manual_Trigger',
				criteria: item.config || item.criteria || {},
				_ui_name: item.name || triggerOption?.label || 'Trigger không tên',
				_ui_description:
					item.description || triggerOption?.description || 'Không có mô tả',
				_ui_type: item.type || 'manual',
			}
			console.log('Migrated trigger:', migrated)
			return migrated
		} else {
			// Find matching action option for proper name/description
			const actionOption = availableActions.find(
				(a) =>
					a.action_type === (item.type || item.action_type) ||
					a.value === (item.type || item.action_type),
			)

			const migrated = {
				action_order: index + 1,
				action_type: item.type || item.action_type || 'Send_Message',
				parameters: item.config || item.parameters || {},
				_ui_name: item.name || actionOption?.label || 'Action không tên',
				_ui_description: item.description || actionOption?.description || 'Không có mô tả',
				_ui_type: item.type || 'send_message',
			}
			console.log('Migrated action:', migrated)
			return migrated
		}
	})
}

const selectItem = (type, index) => {
	console.log('selectItem called with:', type, index)
	selectedItem.value = { type, index }
	const item =
		type === 'trigger' ? flowData.value.triggers[index] : flowData.value.actions[index]

	console.log('Selected item:', item)

	// Deep clone to avoid reference issues
	selectedItemData.value = JSON.parse(JSON.stringify(item))

	// Ensure parameters object exists
	if (type === 'action' && !selectedItemData.value.parameters) {
		selectedItemData.value.parameters = {}
	}

	// Ensure criteria object exists for triggers
	if (type === 'trigger' && !selectedItemData.value.criteria) {
		selectedItemData.value.criteria = {}
	}
	
	console.log('selectedItem.value:', selectedItem.value)
	console.log('selectedItemData.value:', selectedItemData.value)
}

const getSelectedItemTitle = () => {
	if (!selectedItem.value) return ''
	const { type, index } = selectedItem.value
	const item =
		type === 'trigger' ? flowData.value.triggers[index] : flowData.value.actions[index]
	return (
		item?._ui_name || item?.name || `${type === 'trigger' ? 'Trigger' : 'Action'} ${index + 1}`
	)
}

const getSelectedItemDescription = () => {
	if (!selectedItem.value) return ''
	const { type, index } = selectedItem.value
	const item =
		type === 'trigger' ? flowData.value.triggers[index] : flowData.value.actions[index]
	return item?._ui_description || item?.description || 'Không có mô tả'
}

// Immediate loading handlers
const handleAddTrigger = (triggerOption) => {
	if (addingTrigger.value) return // Already processing
	addingTrigger.value = true
	
	// Close dialog immediately when starting
	showAddTrigger.value = false
	triggerSearch.value = ''
	
	// Use setTimeout to ensure DOM updates immediately
	setTimeout(() => addTrigger(triggerOption), 0)
}

const handleAddAction = (actionOption) => {
	if (addingAction.value) return // Already processing
	addingAction.value = true
	
	// Close dialog immediately when starting
	showAddAction.value = false
	actionSearch.value = ''
	
	// Use setTimeout to ensure DOM updates immediately
	setTimeout(() => addAction(actionOption), 0)
}

const addTrigger = async (triggerOption) => {
	try {
		// Generate unique name with auto-numbering
		const baseName = triggerOption.name
		const existingTriggers = flowData.value.triggers.filter((t) =>
			t._ui_name.startsWith(baseName),
		)
		const displayName =
			existingTriggers.length > 0 ? `${baseName} ${existingTriggers.length + 1}` : baseName

		const newTrigger = {
			// Backend format fields
			event_type: triggerOption.event_type,
			trigger_type: triggerOption.trigger_type,
			target_type: 'Talent',
			status: 'ACTIVE',
			Conditional_Split: [],
			
			// Explicitly set null values for optional fields
			owner_id: null,
			tags: null,
			is_sharing: 0,
			schedule_time: null,
			channel: null,

			// UI display fields (for internal use)
			_ui_name: displayName,
			_ui_description: triggerOption.description,
			_ui_type: triggerOption.trigger_type,

			// For display in list
			name: displayName,
			description: triggerOption.description,
		}
		
		// Add to local state
		flowData.value.triggers.push(newTrigger)
		
		// Auto-save immediately
		const result = await flowStore.updateFlow(flowData.value.name, flowData.value)
		if (result.success) {
			toast.success(`Added and saved trigger: ${displayName}`)
		} else {
			toast.error('Error saving trigger')
		}
		
		// Dialog already closed in handler
	} catch (error) {
		console.error('Error saving trigger:', error)
		toast.error('Error saving trigger')
	} finally {
		addingTrigger.value = false
	}
}

const addAction = async (actionOption) => {
	try {
		// Prepare default parameters based on action type
		let defaultParameters = { ...actionOption.parameters } || {}
		
		// Ensure proper structure for different action types
		if (actionOption.action_type === 'SMS' || actionOption.value === 'send_sms') {
			defaultParameters = {
				...defaultParameters,
				sms_content: {
					blocks: [
						{
							id: 1,
							type: 'text',
							text_content: '',
						},
					],
				},
				template_id: ''
			}
		} else if (actionOption.action_type === 'ADD_TAG' || actionOption.value === 'add_tag') {
			defaultParameters = {
				...defaultParameters,
				tag_name: ''
			}
		} else if (actionOption.action_type === 'REMOVE_TAG' || actionOption.value === 'remove_tag') {
			defaultParameters = {
				...defaultParameters,
				tag_name: ''
			}
		} else if (actionOption.action_type === 'SMART_DELAY' || actionOption.value === 'smart_delay') {
			defaultParameters = {
				...defaultParameters,
				duration: '1 day'
			}
		} else if (actionOption.action_type === 'ADD_CUSTOM_FIELD' || actionOption.value === 'add_custom_field') {
			defaultParameters = {
				...defaultParameters,
				field_name: '',
				field_value: ''
			}
		} else if (actionOption.action_type === 'START_FLOW' || actionOption.value === 'start_flow') {
			defaultParameters = {
				...defaultParameters,
				flow_id: ''
			}
		} else if (actionOption.action_type === 'SUBSCRIBE_TO_SEQUENCE' || actionOption.value === 'subscribe_to_sequence') {
			defaultParameters = {
				...defaultParameters,
				sequence_id: ''
			}
		}

		const newAction = {
			// Backend format fields
			action_order: flowData.value.actions.length + 1, // Auto increment order
			action_type: actionOption.action_type || actionOption.value,
			channel_type: actionOption.parameters?.channel || null,
			parameters: defaultParameters,
			
			// Link fields - explicitly set to null
			next_flow: null,
			sequence: null,
			
			// Other fields
			delay_minutes: 0,
			condition: null,

			// UI display fields (for internal use)
			_ui_name: actionOption.label,
			_ui_description: actionOption.description,
			_ui_type: actionOption.value,
		}
		
		// Add to local state
		flowData.value.actions.push(newAction)
		
		// Auto-save immediately
		const result = await flowStore.updateFlow(flowData.value.name, flowData.value)
		if (result.success) {
			toast.success(`Added and saved action: ${actionOption.label}`)
		} else {
			toast.error('Error saving action')
		}
		
		// Dialog already closed in handler
	} catch (error) {
		console.error('Error saving action:', error)
		toast.error('Error saving action')
	} finally {
		addingAction.value = false
	}
}

const handleSaveItem = () => {
	if (!selectedItem.value) return

	const { type, index } = selectedItem.value
	if (type === 'trigger') {
		flowData.value.triggers[index] = { ...selectedItemData.value }
	} else {
		flowData.value.actions[index] = { ...selectedItemData.value }
	}

	toast.success('Saved changes')
}

const handleDeleteItem = () => {
	if (!selectedItem.value) return

	if (confirm('Are you sure you want to delete this item?')) {
		const { type, index } = selectedItem.value
		if (type === 'trigger') {
			flowData.value.triggers.splice(index, 1)
		} else {
			flowData.value.actions.splice(index, 1)
		}

		selectedItem.value = null
		selectedItemData.value = {}
		hasUnsavedChanges.value = true
		toast.success('Deleted successfully')
	}
}

// Delete trigger from list (with hover button)
const deleteTrigger = async (index) => {
	if (confirm('Bạn có chắc chắn muốn xóa trigger này?')) {
		// If deleting currently selected trigger, clear selection
		if (selectedItem.value?.type === 'trigger' && selectedItem.value?.index === index) {
			selectedItem.value = null
			selectedItemData.value = {}
		}
		
		// Remove trigger
		flowData.value.triggers.splice(index, 1)
		hasUnsavedChanges.value = true
		
		// Auto-save
		try {
			const result = await flowStore.updateFlow(flowData.value.name, flowData.value)
			if (result.success) {
				toast.success('Đã xóa trigger thành công')
			} else {
				toast.error('Lỗi khi xóa trigger')
			}
		} catch (error) {
			console.error('Error deleting trigger:', error)
			toast.error('Lỗi khi xóa trigger')
		}
	}
}

// Delete action from list (with hover button)
const deleteAction = async (index) => {
	if (confirm('Bạn có chắc chắn muốn xóa action này?')) {
		// If deleting currently selected action, clear selection
		if (selectedItem.value?.type === 'action' && selectedItem.value?.index === index) {
			selectedItem.value = null
			selectedItemData.value = {}
		}
		
		// Remove action
		flowData.value.actions.splice(index, 1)
		hasUnsavedChanges.value = true
		
		// Auto-save
		try {
			const result = await flowStore.updateFlow(flowData.value.name, flowData.value)
			if (result.success) {
				toast.success('Đã xóa action thành công')
			} else {
				toast.error('Lỗi khi xóa action')
			}
		} catch (error) {
			console.error('Error deleting action:', error)
			toast.error('Lỗi khi xóa action')
		}
	}
}

const handleSave = async () => {
	if (!flowData.value.name) {
		toast.error('Flow not found')
		return
	}

	saving.value = true

	try {
		console.log('Flow data to save:', flowData.value)

		// Keep UI fields for display purposes
		console.log('Triggers to save:', flowData.value.triggers)
		console.log('Actions to save:', flowData.value.actions)

		const updateData = {
			title: flowData.value.title,
			description: flowData.value.description,
			status: flowData.value.status,
			// Pass child table data as arrays (not JSON strings)
			triggers: flowData.value.triggers,
			actions: flowData.value.actions,
		}

		const result = await flowStore.updateFlow(flowData.value.name, updateData)

		if (result.success) {
			toast.success('Flow saved successfully')
			hasUnsavedChanges.value = false
		} else {
			toast.error(result.error || 'Error saving flow')
		}
	} catch (error) {
		console.error('Error saving flow:', error)
		toast.error('Error saving flow')
	} finally {
		saving.value = false
	}
}

const handleBack = () => {
	router.push({ name: 'FlowManagement' })
}


// Title editing methods
const startEditTitle = () => {
	editTitleValue.value = flowData.value.title || ''
	editingTitle.value = true
}

const saveTitle = async () => {
	if (!editTitleValue.value.trim()) {
		toast.error('Flow name cannot be empty')
		return
	}

	const oldTitle = flowData.value.title
	flowData.value.title = editTitleValue.value.trim()
	editingTitle.value = false

	// Auto save title change
	try {
		const result = await flowStore.updateFlow(flowData.value.name, {
			title: flowData.value.title,
		})

		if (result.success) {
			toast.success('Flow name updated successfully')
		} else {
			// Revert on error
			flowData.value.title = oldTitle
			toast.error(result.error || 'Error updating flow name')
		}
	} catch (error) {
		// Revert on error
		flowData.value.title = oldTitle
		console.error('Error updating title:', error)
		toast.error('Error updating flow name')
	}
}

const cancelEditTitle = () => {
	editingTitle.value = false
	editTitleValue.value = ''
}

// Content Editor Methods
const isEmailAction = () => {
	if (!selectedItem.value || selectedItem.value.type !== 'action') {
		console.log('isEmailAction: no selectedItem or not action type')
		return false
	}
	const action = flowData.value.actions[selectedItem.value.index]
	console.log('isEmailAction: checking action', action)
	const result = action && (
		action.action_type === 'MESSAGE' || 
		action._ui_type === 'send_email' ||
		(action.action_type === 'Send_Message' && action.parameters?.channel === 'Email')
	)
	console.log('isEmailAction result:', result)
	return result
}

const isZaloAction = () => {
	if (!selectedItem.value || selectedItem.value.type !== 'action') return false
	const action = flowData.value.actions[selectedItem.value.index]
	return action && (
		action.action_type === 'ZALO' ||
		(action.action_type === 'Send_Message' && action.parameters?.channel === 'Zalo')
	)
}

const isSMSAction = () => {
	if (!selectedItem.value || selectedItem.value.type !== 'action') return false
	const action = flowData.value.actions[selectedItem.value.index]
	return action && (
		action.action_type === 'SMS' ||
		action._ui_type === 'send_sms'
	)
}

const isAddTagAction = () => {
	if (!selectedItem.value || selectedItem.value.type !== 'action') return false
	const action = flowData.value.actions[selectedItem.value.index]
	return action && (
		action.action_type === 'ADD_TAG' ||
		action._ui_type === 'add_tag'
	)
}

const isRemoveTagAction = () => {
	if (!selectedItem.value || selectedItem.value.type !== 'action') return false
	const action = flowData.value.actions[selectedItem.value.index]
	return action && (
		action.action_type === 'REMOVE_TAG' ||
		action._ui_type === 'remove_tag'
	)
}

const isSmartDelayAction = () => {
	if (!selectedItem.value || selectedItem.value.type !== 'action') return false
	const action = flowData.value.actions[selectedItem.value.index]
	return action && (
		action.action_type === 'SMART_DELAY' ||
		action._ui_type === 'smart_delay'
	)
}

const isAddCustomFieldAction = () => {
	if (!selectedItem.value || selectedItem.value.type !== 'action') return false
	const action = flowData.value.actions[selectedItem.value.index]
	return action && (
		action.action_type === 'ADD_CUSTOM_FIELD' ||
		action._ui_type === 'add_custom_field'
	)
}

const isStartFlowAction = () => {
	if (!selectedItem.value || selectedItem.value.type !== 'action') return false
	const action = flowData.value.actions[selectedItem.value.index]
	return action && (
		action.action_type === 'START_FLOW' ||
		action._ui_type === 'start_flow'
	)
}

const isSubscribeSequenceAction = () => {
	if (!selectedItem.value || selectedItem.value.type !== 'action') return false
	const action = flowData.value.actions[selectedItem.value.index]
	return action && (
		action.action_type === 'SUBSCRIBE_TO_SEQUENCE' ||
		action._ui_type === 'subscribe_to_sequence'
	)
}

const emailContent = computed(() => {
	// Prevent re-compute during updates to avoid recursive triggers
	if (isUpdatingSelectedItemData.value) {
		return emailContentCache.value || {
			email_subject: '',
			email_content: '',
			attachments: [],
		}
	}
	
	console.log('emailContent computed called', selectedItemData.value.parameters?.email_content)
	const result = selectedItemData.value.parameters?.email_content || {
		email_subject: '',
		email_content: '',
		attachments: [],
	}
	emailContentCache.value = result
	return result
})

// Cache for email content
const emailContentCache = ref(null)

const zaloContent = computed(() => {
	// Prevent re-compute during updates to avoid recursive triggers
	if (isUpdatingSelectedItemData.value) {
		return zaloContentCache.value || {
			blocks: [
				{
					id: 1,
					type: 'text',
					text_content: '',
				},
			],
		}
	}
	
	const result = selectedItemData.value.parameters?.zalo_content || {
		blocks: [
			{
				id: 1,
				type: 'text',
				text_content: '',
			},
		],
	}
	zaloContentCache.value = result
	return result
})

// Cache for zalo content
const zaloContentCache = ref(null)

// Cache for SMS content to prevent unnecessary re-computation
const smsContentCache = ref(null)
const lastSmsContentHash = ref('')

// Separate cache for images to prevent unnecessary re-render
const smsImagesCache = ref([])
const lastImagesHash = ref('')

// SMS Flow Triggers cache
const smsFlowTriggersCache = ref([])
const lastSmsFlowTriggersHash = ref('')

const smsContent = computed(() => {
	// Create a hash of the SMS content to detect actual changes
	const currentHash = JSON.stringify({
		selectedItem: selectedItem.value,
		smsContent: selectedItemData.value.parameters?.sms_content
	})
	
	// Return cached result if content hasn't changed
	if (lastSmsContentHash.value === currentHash && smsContentCache.value) {
		return smsContentCache.value
	}
	
	console.log('🔍 SMS Content Debug - Computing new content')
	
	// Get SMS content directly from action (most reliable)
	if (selectedItem.value?.type === 'action') {
		const action = flowData.value.actions[selectedItem.value.index]
		console.log('🔍 Direct action data:', action)
		
		if (action?.parameters?.sms_content?.blocks) {
			// SMS content is stored in blocks format (like Zalo) - only process text content
			let fullMessage = ''
			
			action.parameters.sms_content.blocks.forEach(block => {
				// Text content
				if (block.text_content) {
					fullMessage += block.text_content + '\n'
				}
				
				// Website URL (can be in any block type)
				if (block.website_url) {
					fullMessage += `🌐 ${block.website_url}\n`
				}
				
				// Phone number (can be in any block type)  
				if (block.phone_number) {
					fullMessage += `📞 ${block.phone_number}\n`
				}
				
				// Flow trigger (can be in any block type)
				if (block.flow_trigger) {
					// Use display name from block first, then fallback to flow ID
					const flowName = block.flow_display_name || block.flow_trigger
					fullMessage += `▶️ ${flowName}\n`
				}
				
				// Skip image blocks - they're handled separately
			})
			
			console.log('🔍 Extracted SMS text content:', fullMessage.trim())
			const result = { 
				message: fullMessage.trim()
			}
			
			// Cache the result
			smsContentCache.value = result
			lastSmsContentHash.value = currentHash
			return result
		}
		
		if (action?.parameters?.sms_content?.message) {
			// Direct message format
			return action.parameters.sms_content
		}
	}
	
	// Try selectedItemData as fallback
	if (selectedItemData.value.parameters?.sms_content?.blocks) {
		let fullMessage = ''
		
		selectedItemData.value.parameters.sms_content.blocks.forEach(block => {
			// Text content
			if (block.text_content) {
				fullMessage += block.text_content + '\n'
			}
			
			// Website URL (can be in any block type)
			if (block.website_url) {
				fullMessage += `🌐 ${block.website_url}\n`
			}
			
			// Phone number (can be in any block type)  
			if (block.phone_number) {
				fullMessage += `📞 ${block.phone_number}\n`
			}
			
			// Flow trigger (can be in any block type)
			if (block.flow_trigger) {
				// Use display name from block first, then fallback to flow ID
				const flowName = block.flow_display_name || block.flow_trigger
				fullMessage += `▶️ ${flowName}\n`
			}
			
			// Skip image blocks - they're handled separately
		})
		
		const result = { 
			message: fullMessage.trim()
		}
		
		// Cache the result
		smsContentCache.value = result
		lastSmsContentHash.value = currentHash
		return result
	}
	
	if (selectedItemData.value.parameters?.sms_content?.message) {
		const result = selectedItemData.value.parameters.sms_content
		smsContentCache.value = result
		lastSmsContentHash.value = currentHash
		return result
	}
	
	console.log('🔍 No SMS content found, returning empty')
	const result = { message: '' }
	smsContentCache.value = result
	lastSmsContentHash.value = currentHash
	return result
})

// Separate computed for SMS images to prevent unnecessary re-render
const smsImages = computed(() => {
	// Create hash only for image-related data
	const imageHash = JSON.stringify({
		selectedItem: selectedItem.value,
		imageBlocks: selectedItemData.value.parameters?.sms_content?.blocks?.filter(block => block.type === 'image')
	})
	
	// Return cached images if nothing changed
	if (lastImagesHash.value === imageHash && smsImagesCache.value) {
		return smsImagesCache.value
	}
	
	let images = []
	
	// Get images from action data
	if (selectedItem.value?.type === 'action') {
		const action = flowData.value.actions[selectedItem.value.index]
		
		if (action?.parameters?.sms_content?.blocks) {
			action.parameters.sms_content.blocks.forEach(block => {
				if (block.type === 'image' && block.image) {
					images.push({
						id: block.id,
						file_url: block.image.file_url,
						file_name: block.image.file_name
					})
				}
			})
		}
	}
	
	// Try fallback
	if (images.length === 0 && selectedItemData.value.parameters?.sms_content?.blocks) {
		selectedItemData.value.parameters.sms_content.blocks.forEach(block => {
			if (block.type === 'image' && block.image) {
				images.push({
					id: block.id,
					file_url: block.image.file_url,
					file_name: block.image.file_name
				})
			}
		})
	}
	
	// Cache the result
	smsImagesCache.value = images
	lastImagesHash.value = imageHash
	return images
})

const getEmailContent = () => {
	if (!selectedItem.value || selectedItem.value.type !== 'action') return {}
	const action = flowData.value.actions[selectedItem.value.index]
	return action?.parameters?.email_content || {
		email_subject: '',
		email_content: '',
		attachments: []
	}
}

const getZaloContent = () => {
	return zaloContent.value
}

const getSMSContent = () => {
	if (!selectedItem.value || selectedItem.value.type !== 'action') return {}
	const action = flowData.value.actions[selectedItem.value.index]
	return action?.parameters?.sms_content || {
		blocks: [
			{
				id: 1,
				type: 'text',
				text_content: '',
			},
		],
	}
}

const updateEmailContent = (content) => {
	console.log('updateEmailContent called with:', content)
	if (!selectedItem.value || selectedItem.value.type !== 'action') return
	
	// Prevent recursive calls
	if (isUpdatingSelectedItemData.value) {
		console.log('⏭️ Skipping updateEmailContent - already updating')
		return
	}
	
	safeUpdateSelectedItemData(() => {
		const actionIndex = selectedItem.value.index
		const action = flowData.value.actions[actionIndex]
		
		if (action) {
			if (!action.parameters) action.parameters = {}
			action.parameters.email_content = content
			action.parameters.template_id = `EMAIL_${Date.now()}`
			
			// Chỉ update local state, không auto-save
			console.log('Email content updated locally')
			hasUnsavedChanges.value = true
			
			// Sync với selectedItemData để đảm bảo consistency
			if (selectedItemData.value) {
				if (!selectedItemData.value.parameters) selectedItemData.value.parameters = {}
				selectedItemData.value.parameters.email_content = content
				selectedItemData.value.parameters.template_id = action.parameters.template_id
			}
		}

		// Update the flow data as well to ensure persistence
		if (selectedItem.value) {
			const { type, index } = selectedItem.value
			if (type === 'action') {
				flowData.value.actions[index] = { ...selectedItemData.value }
			}
		}

		// Force preview re-render
		previewKey.value++
	})
}

const updateZaloContent = (content) => {
	console.log('updateZaloContent called with:', content)
	
	// Prevent recursive calls
	if (isUpdatingSelectedItemData.value) {
		console.log('⏭️ Skipping updateZaloContent - already updating')
		return
	}
	
	safeUpdateSelectedItemData(() => {
		if (!selectedItemData.value.parameters) {
			selectedItemData.value.parameters = {}
		}
		selectedItemData.value.parameters.zalo_content = content
		selectedItemData.value.parameters.template_id = `ZALO_${Date.now()}`
		hasUnsavedChanges.value = true

		// Update the flow data as well to ensure persistence
		if (selectedItem.value) {
			const { type, index } = selectedItem.value
			if (type === 'action') {
				flowData.value.actions[index].parameters.zalo_content = content
				flowData.value.actions[index].parameters.template_id = selectedItemData.value.parameters.template_id
			}
		}

		// Force preview re-render
		previewKey.value++
	})
}

const updateSMSContent = (content) => {
	console.log('updateSMSContent called with:', content)
	if (!selectedItem.value || selectedItem.value.type !== 'action') return
	
	const actionIndex = selectedItem.value.index
	const action = flowData.value.actions[actionIndex]
	
	if (action) {
		if (!action.parameters) action.parameters = {}
		action.parameters.sms_content = content
		action.parameters.template_id = `SMS_${Date.now()}`
		
		// Chỉ update local state, không auto-save
		console.log('SMS content updated locally')
		hasUnsavedChanges.value = true
		
		// Sync với selectedItemData để đảm bảo consistency
		if (selectedItemData.value) {
			if (!selectedItemData.value.parameters) selectedItemData.value.parameters = {}
			selectedItemData.value.parameters.sms_content = content
			selectedItemData.value.parameters.template_id = action.parameters.template_id
		}
		
		// Force preview update
		previewKey.value++
	}

	// Update the flow data as well to ensure persistence
	if (selectedItem.value) {
		const { type, index } = selectedItem.value
		if (type === 'action') {
			flowData.value.actions[index] = { ...selectedItemData.value }
		}
	}

	// Force preview re-render
	previewKey.value++
}

// Flow selection functions
const getFlowFilters = () => {
	// Exclude current flow to prevent infinite loop
	return [['name', '!=', flowData.value.name]]
}

const availableFlowOptions = computed(() => {
	console.log('🔍 Computing availableFlowOptions:', {
		flowsValue: flows.value,
		flowsLength: flows.value?.length,
		currentFlowName: flowData.value.name,
		flowsLoading: flowsLoading.value
	})
	
	if (!flows.value || flows.value.length === 0) {
		console.log('❌ No flows available')
		return []
	}
	
	// Filter out current flow to prevent infinite loop
	const availableFlows = flows.value.filter(flow => flow.name !== flowData.value.name)
	
	console.log('✅ Available flows after filter:', availableFlows)
	
	const options = availableFlows.map(flow => ({
		label: flow.title || flow.name,
		value: flow.name,
		description: flow.description || ''
	}))
	
	console.log('🎯 Final flow options:', options)
	return options
})

// Tag options for select (exclude already selected)
const availableTagOptions = computed(() => {
	const selectedValues = selectedItemData.value.parameters?.selected_tags || []
	const options = tags.value
		.filter(tag => !selectedValues.includes(tag.name))
		.map(tag => ({
			label: tag.title || tag.name,
			value: tag.name
		}))
	
	console.log('🏷️ Available tag options:', options)
	return options
})

// Display selected tags with proper labels
const selectedTagsDisplay = computed(() => {
	const selectedValues = selectedItemData.value.parameters?.selected_tags || []
	return selectedValues.map(value => {
		const tag = tags.value.find(t => t.name === value)
		return {
			label: tag ? (tag.title || tag.name) : value,
			value: value
		}
	})
})

// SMS Flow Triggers - separate computed for flow trigger blocks
const smsFlowTriggers = computed(() => {
	const currentHash = JSON.stringify({
		selectedItem: selectedItem.value,
		flowTriggerBlocks: selectedItemData.value.parameters?.sms_content?.blocks?.filter(block => block.type === 'flow_trigger')
	})
	
	// Return cached flow triggers if nothing changed
	if (lastSmsFlowTriggersHash.value === currentHash && smsFlowTriggersCache.value) {
		return smsFlowTriggersCache.value
	}
	
	// Process flow trigger blocks
	const blocks = selectedItemData.value.parameters?.sms_content?.blocks || []
	const flowTriggers = blocks.filter(block => block.type === 'flow_trigger' && block.flow_trigger)
	
	// Cache the result
	smsFlowTriggersCache.value = flowTriggers
	lastSmsFlowTriggersHash.value = currentHash
	
	console.log('🔄 SMS Flow Triggers computed:', flowTriggers)
	return flowTriggers
})

const getFlowNameById = async (flowId) => {
	if (!flowId) return null
	
	try {
		// Try to get flow from store first (if cached)
		const cachedFlow = flowStore.flows?.find(flow => flow.name === flowId)
		if (cachedFlow) {
			return cachedFlow.title || cachedFlow.name
		}
		
		// If not cached, fetch from API
		const result = await flowStore.fetchFlowById(flowId)
		if (result?.success && result?.data) {
			return result.data.title || result.data.name || flowId
		}
	} catch (error) {
		console.error('Error fetching flow name:', error)
	}
	
	// Fallback to flow ID
	return flowId
}

// updateFlowId method removed - now using watcher for automatic sync

const updateSMSFlowTrigger = (flowId) => {
	console.log('updateSMSFlowTrigger called with:', flowId)
	
	if (selectedItemData.value.parameters) {
		selectedItemData.value.parameters.flow_trigger_id = flowId
		hasUnsavedChanges.value = true
		
		// Update SMS content blocks with flow trigger
		if (selectedItemData.value.parameters.sms_content?.blocks) {
			// Find or create flow trigger block
			let flowBlock = selectedItemData.value.parameters.sms_content.blocks.find(block => block.type === 'flow_trigger')
			if (!flowBlock) {
				flowBlock = {
					id: Date.now(),
					type: 'flow_trigger',
					flow_trigger: flowId
				}
				selectedItemData.value.parameters.sms_content.blocks.push(flowBlock)
			} else {
				flowBlock.flow_trigger = flowId
			}
		}
		
		// Sync with main flow data
		if (selectedItem.value) {
			const { type, index } = selectedItem.value
			if (type === 'action') {
				flowData.value.actions[index] = { ...selectedItemData.value }
			}
		}
		
		// Force preview update
		previewKey.value++
	}
}

// Tag management methods
const addSelectedTag = () => {
	if (!selectedTagToAdd.value) return
	
	if (!selectedItemData.value.parameters) {
		selectedItemData.value.parameters = {}
	}
	
	if (!selectedItemData.value.parameters.selected_tags) {
		selectedItemData.value.parameters.selected_tags = []
	}
	
	if (!selectedItemData.value.parameters.selected_tags.includes(selectedTagToAdd.value)) {
		selectedItemData.value.parameters.selected_tags.push(selectedTagToAdd.value)
		hasUnsavedChanges.value = true
		
		// Sync with main flow data
		if (selectedItem.value) {
			const { type, index } = selectedItem.value
			if (type === 'action') {
				flowData.value.actions[index] = { ...selectedItemData.value }
			}
		}
	}
	
	selectedTagToAdd.value = ''
}

const removeSelectedTag = (tagValue) => {
	if (!selectedItemData.value.parameters?.selected_tags) return
	
	const index = selectedItemData.value.parameters.selected_tags.indexOf(tagValue)
	if (index > -1) {
		selectedItemData.value.parameters.selected_tags.splice(index, 1)
		hasUnsavedChanges.value = true
		
		// Sync with main flow data
		if (selectedItem.value) {
			const { type, index: actionIndex } = selectedItem.value
			if (type === 'action') {
				flowData.value.actions[actionIndex] = { ...selectedItemData.value }
			}
		}
	}
}

// Create new tag
const createNewTag = async () => {
	if (!newTagName.value.trim()) {
		toast.error('Vui lòng nhập tên tag')
		return
	}

	try {
		creatingTag.value = true
		const result = await tagStore.createTag({
			title: newTagName.value.trim()
		})

		if (result.success) {
			toast.success('Tạo tag thành công')
			
			// Add to selected tags
			if (!selectedItemData.value.parameters) {
				selectedItemData.value.parameters = {}
			}
			if (!selectedItemData.value.parameters.selected_tags) {
				selectedItemData.value.parameters.selected_tags = []
			}
			selectedItemData.value.parameters.selected_tags.push(result.data.name)
			hasUnsavedChanges.value = true
			
			// Sync with main flow data
			if (selectedItem.value) {
				const { type, index } = selectedItem.value
				if (type === 'action') {
					flowData.value.actions[index] = { ...selectedItemData.value }
				}
			}
			
			newTagName.value = ''
		} else {
			toast.error(result.error || 'Không thể tạo tag')
		}
	} catch (error) {
		console.error('Error creating tag:', error)
		toast.error('Không thể tạo tag')
	} finally {
		creatingTag.value = false
	}
}

// Action data update function
const updateActionData = (newData) => {
	// Prevent recursive calls
	if (isUpdatingSelectedItemData.value) {
		console.log('⏭️ Skipping updateActionData - already updating')
		return
	}
	
	safeUpdateSelectedItemData(() => {
		if (selectedItemData.value.parameters) {
			Object.assign(selectedItemData.value.parameters, newData)
			hasUnsavedChanges.value = true
			
			// Sync with main flow data
			if (selectedItem.value) {
				const { type, index } = selectedItem.value
				if (type === 'action') {
					flowData.value.actions[index] = { ...selectedItemData.value }
				}
			}
		}
	})
}

// AdditionalActions support functions
const getAdditionalActionsData = () => {
	if (!selectedItem.value || selectedItem.value.type !== 'action') return {}
	
	const action = flowData.value.actions[selectedItem.value.index]
	if (!action || !action.parameters) return {}
	
	// Return the additional_actions data from parameters
	return action.parameters.additional_actions || {}
}

const updateAdditionalActionsData = (newData) => {
	if (!selectedItem.value || selectedItem.value.type !== 'action') return
	
	// Prevent recursive calls
	if (isUpdatingSelectedItemData.value) {
		console.log('⏭️ Skipping updateAdditionalActionsData - already updating')
		return
	}
	
	safeUpdateSelectedItemData(() => {
		const actionIndex = selectedItem.value.index
		const action = flowData.value.actions[actionIndex]
		
		if (action) {
			if (!action.parameters) action.parameters = {}
			action.parameters.additional_actions = newData
			
			// Sync with selectedItemData
			if (selectedItemData.value.parameters) {
				selectedItemData.value.parameters.additional_actions = newData
			}
			
			hasUnsavedChanges.value = true
			
			// Sync with main flow data
			flowData.value.actions[actionIndex] = { ...action }
		}
	})
}

const updateTriggerContent = (content) => {
	console.log('updateTriggerContent called with:', content)

	// Update selectedItemData with new content
	Object.assign(selectedItemData.value, content)

	// Update the flow data as well to ensure persistence
	if (selectedItem.value) {
		const { type, index } = selectedItem.value
		if (type === 'trigger') {
			flowData.value.triggers[index] = { ...selectedItemData.value }
		}
	}
}

const totalZaloCharacters = computed(() => {
	if (!selectedItem.value || selectedItem.value.type !== 'action' || !isZaloAction()) {
		return 0
	}

	const content = zaloContent.value
	if (!content.blocks || !Array.isArray(content.blocks)) {
		return 0
	}

	return content.blocks.reduce((total, block) => {
		let blockTotal = 0

		// Count text content
		if (block.text_content) {
			blockTotal += block.text_content.length
		}

		// Count website URL (if exists, add some characters for display)
		if (block.website_url) {
			blockTotal += block.website_url.length + 10 // +10 for formatting
		}

		// Count phone number (if exists)
		if (block.phone_number) {
			blockTotal += block.phone_number.length + 5 // +5 for formatting
		}

		// Count flow trigger (if exists)
		if (block.flow_trigger) {
			blockTotal += block.flow_trigger.length + 8 // +8 for "Start: " prefix
		}

		// Count image blocks (images take up space in message)
		if (block.type === 'image' && block.image) {
			blockTotal += 50 // Estimate for image display space
		}

		return total + blockTotal
	}, 0)
})

const getTotalZaloCharacters = () => {
	return totalZaloCharacters.value
}

// Debounced preview update
const debouncedPreviewUpdate = ref(null)
const isPreviewUpdating = ref(false)
const isUpdatingSelectedItemData = ref(false) // Flag to prevent recursive updates

// Helper function to safely update selectedItemData without triggering recursive watcher
const safeUpdateSelectedItemData = (updateFn) => {
	isUpdatingSelectedItemData.value = true
	try {
		updateFn()
	} finally {
		// Reset flag after a delay to allow watcher to settle
		setTimeout(() => {
			isUpdatingSelectedItemData.value = false
		}, 300)
	}
}

// WATCHER REMOVED - Causing recursive updates
// Preview updates are now handled manually in update functions via previewKey.value++
// This prevents the recursive loop caused by deep watching selectedItemData

// Watchers
watch(
	() => selectedItemData.value.parameters?.flow_id,
	(newFlowId) => {
		// Prevent recursive updates
		if (isUpdatingSelectedItemData.value) {
			console.log('⏭️ Skipping flow_id watcher - already updating')
			return
		}
		
		if (newFlowId && selectedItem.value?.type === 'action') {
			console.log('Flow ID changed to:', newFlowId)
			hasUnsavedChanges.value = true
			
			// Sync with main flow data
			const { type, index } = selectedItem.value
			if (type === 'action') {
				if (!flowData.value.actions[index].parameters) {
					flowData.value.actions[index].parameters = {}
				}
				flowData.value.actions[index].parameters.flow_id = newFlowId
			}
			
			// Force preview update
			previewKey.value++
		}
	}
)

// Computed properties will automatically update preview when content changes

// Lifecycle
onMounted(async () => {
	await loadFlow()
	
	// Load available flows for Start Flow action
	try {
		console.log('🌊 Loading flows for Start Flow action...')
		const result = await flowStore.fetchFlows()
		console.log('🌊 Flows fetch result:', result)
		console.log('🌊 Flows in store after fetch:', flows.value)
		console.log('🌊 Flows loading state:', flowsLoading.value)
		
		// If no flows loaded, add some test data for debugging
		if (!flows.value || flows.value.length === 0) {
			console.log('⚠️ No flows found, adding test data for debugging')
			// This is temporary for debugging - remove in production
			flowStore.flows = [
				{ name: 'test-flow-1', title: 'Test Flow 1', status: 'Active', description: 'Test flow for debugging' },
				{ name: 'test-flow-2', title: 'Test Flow 2', status: 'Draft', description: 'Another test flow' },
				{ name: 'test-flow-3', title: 'Test Flow 3', status: 'Active', description: 'Third test flow' }
			]
			console.log('🧪 Added test flows:', flowStore.flows)
		}
	} catch (error) {
		console.error('❌ Error loading flows:', error)
	}
	
	// Load tags for Add Tag action
	try {
		await tagStore.fetchTags()
	} catch (error) {
		console.error('Error loading tags:', error)
	}
})
</script>

<style scoped>
/* Custom scrollbar for better UX */
::-webkit-scrollbar {
	width: 6px;
}

::-webkit-scrollbar-track {
	background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
	background: #c1c1c1;
	border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
	background: #a8a8a8;
}
</style>
