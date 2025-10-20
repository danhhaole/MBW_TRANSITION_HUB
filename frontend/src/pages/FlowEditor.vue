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
					<span class="text-gray-400">/</span>

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
					<Button variant="outline" size="sm">
						<template #prefix>
							<FeatherIcon name="eye" class="h-4 w-4" />
						</template>
						Danh sách
					</Button>
					<Button variant="outline" size="sm">
						<template #prefix>
							<FeatherIcon name="edit" class="h-4 w-4" />
						</template>
						Biểu đồ
					</Button>
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
						{{ hasUnsavedChanges ? 'Lưu*' : 'Lưu' }}
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
								class="p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
								:class="{
									'border-blue-500 bg-blue-50':
										selectedItem?.type === 'trigger' &&
										selectedItem?.index === index,
								}"
								@click="selectItem('trigger', index)"
							>
								<div class="flex items-start space-x-3">
									<div
										class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center"
									>
										<FeatherIcon name="zap" class="h-4 w-4 text-blue-600" />
									</div>
									<div class="flex-1 min-w-0">
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
								class="p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
								:class="{
									'border-blue-500 bg-blue-50':
										selectedItem?.type === 'action' &&
										selectedItem?.index === index,
								}"
								@click="selectItem('action', index)"
							>
								<div class="flex items-start space-x-3">
									<div
										class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center"
									>
										<FeatherIcon name="play" class="h-4 w-4 text-purple-600" />
									</div>
									<div class="flex-1 min-w-0">
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
							<h4 class="text-md font-medium text-gray-900 mb-4">Cấu hình Email</h4>
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
							<h4 class="text-md font-medium text-gray-900 mb-4">Cấu hình Zalo</h4>
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
							<h4 class="text-md font-medium text-gray-900 mb-4">Cấu hình SMS</h4>
							<ZaloEditor
								:content="getSMSContent()"
								@update:content="updateSMSContent"
								:readonly="false"
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
							<h4 class="text-md font-medium text-gray-900 mb-4">Thêm Tag</h4>
							<ActionConfig
								action-type="add_tag"
								:action-data="selectedItemData.parameters"
								@update:action-data="updateActionData"
							/>
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
							<h4 class="text-md font-medium text-gray-900 mb-4">Delay Thông Minh</h4>
							<div class="space-y-4">
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-2">
										Thời gian chờ
									</label>
									<FormControl
										v-model="selectedItemData.parameters.duration"
										type="text"
										placeholder="VD: 1 day, 2 hours, 30 minutes..."
										@input="hasUnsavedChanges = true"
									/>
								</div>
							</div>
						</div>

						<!-- Add Custom Field Action -->
						<div v-else-if="selectedItem.type === 'action' && isAddCustomFieldAction()">
							<h4 class="text-md font-medium text-gray-900 mb-4">Thêm Trường Tùy Chỉnh</h4>
							<div class="space-y-4">
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-2">
										Tên trường
									</label>
									<FormControl
										v-model="selectedItemData.parameters.field_name"
										type="text"
										placeholder="Nhập tên trường..."
										@input="hasUnsavedChanges = true"
									/>
								</div>
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-2">
										Giá trị
									</label>
									<FormControl
										v-model="selectedItemData.parameters.field_value"
										type="text"
										placeholder="Nhập giá trị..."
										@input="hasUnsavedChanges = true"
									/>
								</div>
							</div>
						</div>

						<!-- Start Flow Action -->
						<div v-else-if="selectedItem.type === 'action' && isStartFlowAction()">
							<h4 class="text-md font-medium text-gray-900 mb-4">Bắt Đầu Flow</h4>
							<div class="space-y-4">
								<div>
									<Link
										doctype="Mira Flow"
										:filters="getFlowFilters()"
										:model-value="selectedItemData.parameters.flow_id"
										@update:model-value="updateFlowId"
										label="Chọn Flow"
										placeholder="Tìm kiếm flow..."
									/>
									<p class="text-xs text-gray-500 mt-1">
										Chọn flow khác để bắt đầu (không thể chọn flow hiện tại)
									</p>
								</div>
							</div>
						</div>

						<!-- Subscribe to Sequence Action -->
						<div v-else-if="selectedItem.type === 'action' && isSubscribeSequenceAction()">
							<h4 class="text-md font-medium text-gray-900 mb-4">Đăng Ký Sequence</h4>
							<div class="space-y-4">
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-2">
										Sequence ID
									</label>
									<FormControl
										v-model="selectedItemData.parameters.sequence_id"
										type="text"
										placeholder="Nhập ID của sequence..."
										@input="hasUnsavedChanges = true"
									/>
								</div>
							</div>
						</div>

						<!-- Generic Parameters for other actions -->
						<div v-else-if="selectedItem.type === 'action'" class="space-y-4">
							<div>
								<h4 class="text-md font-medium text-gray-900 mb-4">Tham số</h4>

								<!-- Generic parameters display -->
								<div class="bg-gray-50 p-4 rounded-lg">
									<p class="text-sm text-gray-600 mb-2">Action Type: {{ selectedItemData.action_type }}</p>
									<p class="text-sm text-gray-500">Chưa có UI cấu hình cho action type này.</p>
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
												>Email Preview</span
											>
										</div>
										<div class="text-xs text-gray-500">
											<div>From: your-company@example.com</div>
											<div>To: customer@example.com</div>
										</div>
									</div>

									<!-- Email Subject -->
									<div class="bg-gray-50 p-3 rounded-lg">
										<div class="text-xs font-medium text-gray-700 mb-1">
											Subject:
										</div>
										<div class="text-sm text-gray-900">
											{{
												emailContent.email_subject ||
												'Chưa có tiêu đề email'
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
		<Dialog v-model="showAddTrigger" :options="{ title: 'Thêm Trigger', size: 'md' }">
			<template #body-content>
				<div class="space-y-4">
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-2">
							{{ __('Search trigger') }}
						</label>
						<FormControl
							v-model="triggerSearch"
							type="text"
							placeholder="{{ __('Search trigger') }}"
						/>
					</div>
					<div class="max-h-60 overflow-y-auto">
						<div class="space-y-2">
							<div
								v-for="trigger in filteredTriggerOptions"
								:key="trigger.id"
								class="p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50"
								@click="addTrigger(trigger)"
							>
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
		<Dialog v-model="showAddAction" :options="{ title: 'Thêm Action', size: 'md' }">
			<template #body-content>
				<div class="space-y-4">
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-2">
							{{ __('Search action') }}
						</label>
						<FormControl
							v-model="actionSearch"
							type="text"
							placeholder="{{ __('Search action') }}"
						/>
					</div>
					<div class="max-h-60 overflow-y-auto">
						<div class="space-y-2">
							<div
								v-for="action in filteredActionOptions"
								:key="action.value"
								class="p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50"
								@click="addAction(action)"
							>
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
import { useToast } from '../composables/useToast'

// Components
import { Button, FormControl, Dialog, FeatherIcon } from 'frappe-ui'
import EmailEditor from '../components/campaign/content-editors/EmailEditor.vue'
import ZaloEditor from '../components/campaign/content-editors/ZaloEditor.vue'
import TriggerEditor from '../components/campaign/content-editors/TriggerEditor.vue'
import Link from '../components/Controls/Link.vue'
import ActionConfig from '../components/campaign/ActionConfig.vue'
import AdditionalActions from '../components/campaign/AdditionalActions.vue'

// Router
const route = useRoute()
const router = useRouter()

// Store
const flowStore = useMiraFlowStore()

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
		name: 'Khi tạo mới',
		description: 'Kích hoạt khi tạo mới record',
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
		name: 'Khi cập nhật',
		description: 'Kích hoạt khi cập nhật record',
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
		name: 'Khi thêm tag',
		description: 'Kích hoạt khi thêm tag cho record',
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
		name: 'Khi thay đổi trạng thái',
		description: 'Kích hoạt khi thay đổi trạng thái record',
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
		name: 'Khi hoàn thành sequence',
		description: 'Kích hoạt khi hoàn thành một sequence',
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
		name: 'Theo lịch trình',
		description: 'Kích hoạt theo thời gian đã lên lịch',
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
		name: 'Khi đạt điểm số',
		description: 'Kích hoạt khi đạt điểm số nhất định',
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
		name: 'Sự kiện tùy chỉnh',
		description: 'Kích hoạt bởi sự kiện tùy chỉnh',
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
		description: 'Kích hoạt khi form được submit',
		icon: 'file-text',
		event_type: 'Form_Submitted',
		criteria: { form_name: '' },
	},
	{
		id: 'schedule',
		name: 'Schedule',
		description: 'Kích hoạt theo lịch trình',
		icon: 'clock',
		event_type: 'Schedule_Trigger',
		criteria: { schedule: '' },
	},
]

const availableActions = [
	{
		label: 'Gửi Email',
		value: 'send_email',
		description: 'Gửi email cho khách hàng',
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
		label: 'Gửi SMS',
		value: 'send_sms',
		description: 'Gửi tin nhắn SMS',
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
		label: 'Gửi Zalo',
		value: 'send_zalo',
		description: 'Gửi tin nhắn Zalo',
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
		label: 'Delay thông minh',
		value: 'smart_delay',
		description: 'Chờ một khoảng thời gian trước action tiếp theo',
		action_type: 'SMART_DELAY',
		parameters: { duration: '1 day' },
	},
	{
		label: 'Thêm Tag',
		value: 'add_tag',
		description: 'Thêm tag cho khách hàng',
		action_type: 'ADD_TAG',
		parameters: { tag_name: '' },
	},
	{
		label: 'Xóa Tag',
		value: 'remove_tag',
		description: 'Xóa tag khỏi khách hàng',
		action_type: 'REMOVE_TAG',
		parameters: { tag_name: '' },
	},
	{
		label: 'Thêm trường tùy chỉnh',
		value: 'add_custom_field',
		description: 'Thêm trường dữ liệu tùy chỉnh',
		action_type: 'ADD_CUSTOM_FIELD',
		parameters: { field_name: '', field_value: '' },
	},
	{
		label: 'Bắt đầu Flow',
		value: 'start_flow',
		description: 'Bắt đầu một flow khác',
		action_type: 'START_FLOW',
		parameters: { flow_id: '' },
	},
	{
		label: 'Đăng ký Sequence',
		value: 'subscribe_to_sequence',
		description: 'Đăng ký khách hàng vào sequence',
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
		'ON_CREATE': 'Khi tạo mới',
		'ON_UPDATE': 'Khi cập nhật', 
		'ON_TAG_ADDED': 'Khi thêm tag',
		'ON_STATUS_CHANGED': 'Khi thay đổi trạng thái',
		'ON_SEQUENCE_COMPLETED': 'Khi hoàn thành sequence',
		'ON_SCHEDULED_TIME': 'Theo lịch trình',
		'ON_SCORE_REACHED': 'Khi đạt điểm số',
		'CUSTOM_EVENT': 'Sự kiện tùy chỉnh'
	}
	return triggerMap[triggerType] || triggerType
}

const getDefaultTriggerDescription = (triggerType) => {
	const descriptionMap = {
		'ON_CREATE': 'Kích hoạt khi tạo mới record',
		'ON_UPDATE': 'Kích hoạt khi cập nhật record',
		'ON_TAG_ADDED': 'Kích hoạt khi thêm tag',
		'ON_STATUS_CHANGED': 'Kích hoạt khi thay đổi trạng thái',
		'ON_SEQUENCE_COMPLETED': 'Kích hoạt khi hoàn thành sequence',
		'ON_SCHEDULED_TIME': 'Kích hoạt theo lịch trình',
		'ON_SCORE_REACHED': 'Kích hoạt khi đạt điểm số',
		'CUSTOM_EVENT': 'Kích hoạt bởi sự kiện tùy chỉnh'
	}
	return descriptionMap[triggerType] || 'Không có mô tả'
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
		'MESSAGE': 'Gửi tin nhắn',
		'SMS': 'Gửi SMS',
		'EMAIL': 'Gửi Email',
		'ZALO': 'Gửi Zalo',
		'ZALO_CARE': 'Zalo Care',
		'START_FLOW': 'Bắt đầu Flow',
		'SUBSCRIBE_TO_SEQUENCE': 'Đăng ký Sequence',
		'UN_SUBSCRIBE_TO_SEQUENCE': 'Hủy đăng ký Sequence',
		'SMART_DELAY': 'Delay thông minh',
		'AI_CALL': 'Gọi AI',
		'ADD_TAG': 'Thêm Tag',
		'REMOVE_TAG': 'Xóa Tag',
		'ADD_CUSTOM_FIELD': 'Thêm trường tùy chỉnh',
		'REMOVE_CUSTOM_FIELD': 'Xóa trường tùy chỉnh',
		'LEAD_SCORE': 'Tính điểm Lead',
		'EXTERNAL_REQUEST': 'Gọi API ngoài',
		'EMAIL_AI': 'Email AI',
		'CONTENT_AI': 'Nội dung AI',
		'SENT_NOTIFICATION': 'Gửi thông báo'
	}
	return actionMap[actionType] || actionType
}

const getDefaultActionDescription = (actionType) => {
	const descriptionMap = {
		'MESSAGE': 'Gửi tin nhắn cho khách hàng',
		'SMS': 'Gửi tin nhắn SMS',
		'EMAIL': 'Gửi email cho khách hàng',
		'ZALO': 'Gửi tin nhắn Zalo',
		'ZALO_CARE': 'Gửi tin nhắn Zalo Care',
		'START_FLOW': 'Bắt đầu một flow khác',
		'SUBSCRIBE_TO_SEQUENCE': 'Đăng ký khách hàng vào sequence',
		'UN_SUBSCRIBE_TO_SEQUENCE': 'Hủy đăng ký khách hàng khỏi sequence',
		'SMART_DELAY': 'Delay thông minh dựa trên điều kiện',
		'AI_CALL': 'Gọi AI để xử lý',
		'ADD_TAG': 'Thêm tag cho khách hàng',
		'REMOVE_TAG': 'Xóa tag khỏi khách hàng',
		'ADD_CUSTOM_FIELD': 'Thêm trường dữ liệu tùy chỉnh',
		'REMOVE_CUSTOM_FIELD': 'Xóa trường dữ liệu tùy chỉnh',
		'LEAD_SCORE': 'Tính toán điểm số lead',
		'EXTERNAL_REQUEST': 'Gọi API bên ngoài',
		'EMAIL_AI': 'Tạo email bằng AI',
		'CONTENT_AI': 'Tạo nội dung bằng AI',
		'SENT_NOTIFICATION': 'Gửi thông báo hệ thống'
	}
	return descriptionMap[actionType] || 'Không có mô tả'
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

const addTrigger = async (triggerOption) => {
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
	try {
		const result = await flowStore.updateFlow(flowData.value.name, flowData.value)
		if (result.success) {
			toast.success(`Đã thêm và lưu trigger: ${displayName}`)
		} else {
			toast.error('Có lỗi khi lưu trigger')
		}
	} catch (error) {
		console.error('Error saving trigger:', error)
		toast.error('Có lỗi khi lưu trigger')
	}
	
	showAddTrigger.value = false
	triggerSearch.value = ''
}

const addAction = async (actionOption) => {
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
	try {
		const result = await flowStore.updateFlow(flowData.value.name, flowData.value)
		if (result.success) {
			toast.success(`Đã thêm và lưu action: ${actionOption.label}`)
		} else {
			toast.error('Có lỗi khi lưu action')
		}
	} catch (error) {
		console.error('Error saving action:', error)
		toast.error('Có lỗi khi lưu action')
	}
	
	showAddAction.value = false
	actionSearch.value = ''
}

const handleSaveItem = () => {
	if (!selectedItem.value) return

	const { type, index } = selectedItem.value
	if (type === 'trigger') {
		flowData.value.triggers[index] = { ...selectedItemData.value }
	} else {
		flowData.value.actions[index] = { ...selectedItemData.value }
	}

	toast.success('Đã lưu thay đổi')
}

const handleDeleteItem = () => {
	if (!selectedItem.value) return

	if (confirm('Bạn có chắc chắn muốn xóa mục này không?')) {
		const { type, index } = selectedItem.value
		if (type === 'trigger') {
			flowData.value.triggers.splice(index, 1)
		} else {
			flowData.value.actions.splice(index, 1)
		}

		selectedItem.value = null
		selectedItemData.value = {}
		toast.success('Đã xóa thành công')
	}
}

const handleSave = async () => {
	if (!flowData.value.name) {
		toast.error('Không tìm thấy thông tin flow')
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
			toast.success('Flow đã được lưu thành công')
			hasUnsavedChanges.value = false
		} else {
			toast.error(result.error || 'Có lỗi xảy ra khi lưu flow')
		}
	} catch (error) {
		console.error('Error saving flow:', error)
		toast.error('Có lỗi xảy ra khi lưu flow')
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
	isEditingTitle.value = true
}

const saveTitle = async () => {
	if (!editTitleValue.value.trim()) {
		toast.error('Tên flow không được để trống')
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
			toast.success('Đã cập nhật tên flow')
		} else {
			// Revert on error
			flowData.value.title = oldTitle
			toast.error(result.error || 'Có lỗi xảy ra khi cập nhật tên')
		}
	} catch (error) {
		// Revert on error
		flowData.value.title = oldTitle
		console.error('Error updating title:', error)
		toast.error('Có lỗi xảy ra khi cập nhật tên')
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
	console.log('emailContent computed called', selectedItemData.value.parameters?.email_content)
	if (!selectedItemData.value.parameters?.email_content) {
		return {
			email_subject: '',
			email_content: '',
			attachments: [],
		}
	}
	return selectedItemData.value.parameters.email_content
})

const zaloContent = computed(() => {
	if (!selectedItemData.value.parameters?.zalo_content) {
		return {
			blocks: [
				{
					id: 1,
					type: 'text',
					text_content: '',
				},
			],
		}
	}
	return selectedItemData.value.parameters.zalo_content
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
}

const updateZaloContent = (content) => {
	console.log('updateZaloContent called with:', content)
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
			flowData.value.actions[index] = { ...selectedItemData.value }
		}
	}

	// Force preview re-render
	previewKey.value++
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

const updateFlowId = (flowId) => {
	if (selectedItemData.value.parameters) {
		selectedItemData.value.parameters.flow_id = flowId
		hasUnsavedChanges.value = true
		
		// Sync with main flow data
		if (selectedItem.value) {
			const { type, index } = selectedItem.value
			if (type === 'action') {
				flowData.value.actions[index] = { ...selectedItemData.value }
			}
		}
	}
}

// Action data update function
const updateActionData = (newData) => {
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

// Watch for selectedItemData changes to ensure preview updates
watch(
	() => selectedItemData.value,
	(newValue) => {
		console.log('selectedItemData changed:', newValue)
		// Force reactivity by triggering nextTick
		nextTick()
	},
	{ deep: true, immediate: true },
)

// Computed properties will automatically update preview when content changes

// Lifecycle
onMounted(() => {
	loadFlow()
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
