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
					<Button variant="solid" size="sm" @click="handleSave" :loading="saving">
						<template #prefix>
							<FeatherIcon name="save" class="h-4 w-4" />
						</template>
						Lưu lại
					</Button>
					<Button variant="solid" theme="green" size="sm"> Xuất bản </Button>
				</div>
			</div>
		</div>

		<!-- Main Content -->
		<div class="flex h-[calc(100vh-80px)]">
			<!-- Column 1: Triggers & Actions List -->
			<div class="w-80 bg-white border-r border-gray-200 flex flex-col">
				<!-- Triggers Section -->
				<div class="flex-1 p-4">
					<div class="mb-6">
						<h3 class="text-sm font-medium text-gray-900 mb-3">Trigger</h3>
						<p class="text-xs text-gray-500 mb-4">Sự kiện kích hoạt flow này</p>

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
							Thêm Trigger
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
						<h3 class="text-sm font-medium text-gray-900 mb-3">Hành động</h3>
						<p class="text-xs text-gray-500 mb-4">Những hành động sẽ được thực hiện</p>

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
							Thêm hành động
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
								{{ selectedItem ? getSelectedItemTitle() : 'Chọn Trigger' }}
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
									: 'Chọn một trigger hoặc action để cấu hình'
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
						</div>

						<div v-else-if="selectedItem.type === 'action' && isZaloAction()">
							<h4 class="text-md font-medium text-gray-900 mb-4">Cấu hình Zalo</h4>
							<ZaloEditor
								:content="getZaloContent()"
								@update:content="updateZaloContent"
								:readonly="false"
							/>
						</div>

						<!-- Generic Parameters for other actions -->
						<div v-else-if="selectedItem.type === 'action'" class="space-y-4">
							<div>
								<h4 class="text-md font-medium text-gray-900 mb-4">Tham số</h4>

								<!-- Template ID for Send_Message -->
								<div v-if="selectedItemData.action_type === 'Send_Message'">
									<label class="block text-sm font-medium text-gray-700 mb-2"
										>Template ID</label
									>
									<FormControl
										v-model="selectedItemData.parameters.template_id"
										type="text"
										placeholder="Nhập template ID..."
									/>
								</div>

								<!-- Duration for Wait -->
								<div v-if="selectedItemData.action_type === 'Wait'">
									<label class="block text-sm font-medium text-gray-700 mb-2"
										>Thời gian chờ</label
									>
									<FormControl
										v-model="selectedItemData.parameters.duration"
										type="text"
										placeholder="VD: 1 day, 2 hours, 30 minutes..."
									/>
								</div>

								<!-- Tag Name for Tag actions -->
								<div
									v-if="
										selectedItemData.action_type === 'Assign_Tag' ||
										selectedItemData.action_type === 'Remove_Tag'
									"
								>
									<label class="block text-sm font-medium text-gray-700 mb-2"
										>Tên Tag</label
									>
									<FormControl
										v-model="selectedItemData.parameters.tag_name"
										type="text"
										placeholder="Nhập tên tag..."
									/>
								</div>

								<!-- Field for Update_Field -->
								<div
									v-if="selectedItemData.action_type === 'Update_Field'"
									class="space-y-4"
								>
									<div>
										<label class="block text-sm font-medium text-gray-700 mb-2"
											>Tên trường</label
										>
										<FormControl
											v-model="selectedItemData.parameters.field_name"
											type="text"
											placeholder="Nhập tên trường..."
										/>
									</div>
									<div>
										<label class="block text-sm font-medium text-gray-700 mb-2"
											>Giá trị</label
										>
										<FormControl
											v-model="selectedItemData.parameters.field_value"
											type="text"
											placeholder="Nhập giá trị..."
										/>
									</div>
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
								Xóa
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
						<h3 class="mt-2 text-sm font-medium text-gray-900">Chưa chọn mục nào</h3>
						<p class="mt-1 text-sm text-gray-500">
							Chọn một trigger hoặc action từ danh sách bên trái để bắt đầu cấu hình.
						</p>
					</div>
				</div>
			</div>

			<!-- Column 3: Mobile Preview -->
			<div class="w-96 bg-gray-100 p-6">
				<div class="text-center mb-4">
					<h3 class="text-sm font-medium text-gray-900">Preview</h3>
					<p class="text-xs text-gray-500">Xem trước trên điện thoại</p>
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
												'Chưa có nội dung email'
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
											Attachments:
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
												Zalo Message
											</div>
											<p class="text-xs text-gray-500">
												Hôm nay lúc 10:46 sáng
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
										Chọn một action gửi tin nhắn để xem preview
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
							Tìm kiếm trigger
						</label>
						<FormControl
							v-model="triggerSearch"
							type="text"
							placeholder="Tìm kiếm trigger..."
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
							Tìm kiếm action
						</label>
						<FormControl
							v-model="actionSearch"
							type="text"
							placeholder="Tìm kiếm action..."
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
		id: 'subscribe_sequence',
		name: 'Đăng ký Sequence',
		description: 'Kích hoạt khi khách hàng đăng ký sequence',
		icon: 'user-plus',
		event_type: 'Subscribe_Sequence',
		trigger_type: 'subscribe_sequence',
		sequence_id: '',
		connected_account: '',
		channels: [],
		conditions: [],
	},
	{
		id: 'unsubscribe_sequence',
		name: 'Hủy đăng ký Sequence',
		description: 'Kích hoạt khi khách hàng hủy đăng ký sequence',
		icon: 'user-minus',
		event_type: 'Unsubscribe_Sequence',
		trigger_type: 'unsubscribe_sequence',
		sequence_id: '',
		connected_account: '',
		channels: [],
		conditions: [],
	},
	{
		id: 'new_subscriber_all',
		name: 'Đăng ký mới (Tất cả kênh)',
		description: 'Kích hoạt khi có khách hàng mới đăng ký',
		icon: 'users',
		event_type: 'New_Subscriber_All',
		trigger_type: 'new_subscriber_all',
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
		value: 'Send_Message_Email',
		description: 'Gửi email cho khách hàng',
		action_type: 'Send_Message',
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
		label: 'Gửi Zalo',
		value: 'Send_Message_Zalo',
		description: 'Gửi tin nhắn Zalo',
		action_type: 'Send_Message',
		parameters: {
			channel: 'SMS',
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
		label: 'Chờ (Wait)',
		value: 'Wait',
		description: 'Chờ một khoảng thời gian trước action tiếp theo',
		action_type: 'Wait',
		parameters: { duration: '1 day' },
	},
	{
		label: 'Gán Tag',
		value: 'Assign_Tag',
		description: 'Gán tag cho khách hàng',
		action_type: 'Assign_Tag',
		parameters: { tag_name: '' },
	},
	{
		label: 'Bỏ Tag',
		value: 'Remove_Tag',
		description: 'Bỏ tag khỏi khách hàng',
		action_type: 'Remove_Tag',
		parameters: { tag_name: '' },
	},
	{
		label: 'Cập nhật trường',
		value: 'Update_Field',
		description: 'Cập nhật giá trị trường của khách hàng',
		action_type: 'Update_Field',
		parameters: { field_name: '', field_value: '' },
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

			try {
				const rawTriggers = parseJsonField(flow.triggers) || []
				const rawActions = parseJsonField(flow.actions) || []

				// First migrate old format, then ensure UI fields
				const migratedTriggers = migrateToNewFormat(rawTriggers, 'trigger')
				const migratedActions = migrateToNewFormat(rawActions, 'action')

				flowData.value = {
					name: flow.name,
					title: flow.title || '',
					description: flow.description || '',
					status: flow.status || 'Draft',
					triggers: ensureUIFields(migratedTriggers, 'trigger'),
					actions: ensureUIFields(migratedActions, 'action'),
				}

				console.log('Flow data set:', flowData.value)
			} catch (migrationError) {
				console.error('Error during migration:', migrationError)
				// Fallback to simple format without migration
				const rawTriggers = parseJsonField(flow.triggers) || []
				const rawActions = parseJsonField(flow.actions) || []

				flowData.value = {
					name: flow.name,
					title: flow.title || '',
					description: flow.description || '',
					status: flow.status || 'Draft',
					triggers: ensureUIFields(rawTriggers, 'trigger'),
					actions: ensureUIFields(rawActions, 'action'),
				}
				console.log('Using fallback flow data:', flowData.value)
			}
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

const parseJsonField = (field) => {
	console.log('Parsing field:', field, 'Type:', typeof field)
	if (!field) {
		console.log('Field is empty, returning []')
		return []
	}
	if (typeof field === 'string') {
		try {
			const parsed = JSON.parse(field)
			console.log('Parsed JSON:', parsed)
			return parsed
		} catch (error) {
			console.error('JSON parse error:', error)
			return []
		}
	}
	const result = Array.isArray(field) ? field : []
	console.log('Returning field as is:', result)
	return result
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
	selectedItem.value = { type, index }
	const item =
		type === 'trigger' ? flowData.value.triggers[index] : flowData.value.actions[index]

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

const addTrigger = (triggerOption) => {
	// Check for existing triggers of same type for auto-numbering
	const existingCount = flowData.value.triggers.filter(
		(t) => t.event_type === triggerOption.event_type || t._ui_type === triggerOption.id,
	).length

	const baseName = triggerOption.name
	const displayName = existingCount > 0 ? `${baseName} ${existingCount + 1}` : baseName

	const newTrigger = {
		// Backend format fields
		trigger_id: `TGR${String(Date.now()).slice(-6)}`, // Generate unique ID
		source_platform: triggerOption.source_platform || 'Manual',
		event_type: triggerOption.event_type || triggerOption.id,
		criteria: triggerOption.criteria || {},

		// Copy all trigger option fields
		...triggerOption,

		// UI display fields (for internal use)
		_ui_name: displayName,
		_ui_description: triggerOption.description,
		_ui_type: triggerOption.id,
		name: displayName,
		description: triggerOption.description,
	}
	flowData.value.triggers.push(newTrigger)
	showAddTrigger.value = false
	triggerSearch.value = ''
	toast.success(`Đã thêm trigger: ${displayName}`)
}

const addAction = (actionOption) => {
	const newAction = {
		// Backend format fields
		action_order: flowData.value.actions.length + 1, // Auto increment order
		action_type: actionOption.action_type || actionOption.value,
		parameters: actionOption.parameters || {},

		// UI display fields (for internal use)
		_ui_name: actionOption.label,
		_ui_description: actionOption.description,
		_ui_type: actionOption.value,
	}
	flowData.value.actions.push(newAction)
	showAddAction.value = false
	actionSearch.value = ''
	toast.success('Đã thêm action mới')
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
			triggers: JSON.stringify(flowData.value.triggers),
			actions: JSON.stringify(flowData.value.actions),
		}

		const result = await flowStore.updateFlow(flowData.value.name, updateData)

		if (result.success) {
			toast.success('Flow đã được lưu thành công')
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
	editingTitle.value = true

	// Focus input after DOM update
	nextTick(() => {
		if (titleInput.value) {
			titleInput.value.focus()
			titleInput.value.select()
		}
	})
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
	return (
		selectedItemData.value.action_type === 'Send_Message' &&
		selectedItemData.value.parameters?.channel === 'Email'
	)
}

const isZaloAction = () => {
	return (
		selectedItemData.value.action_type === 'Send_Message' &&
		selectedItemData.value.parameters?.channel === 'SMS'
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
	return emailContent.value
}

const getZaloContent = () => {
	return zaloContent.value
}

const updateEmailContent = (content) => {
	console.log('updateEmailContent called with:', content)
	if (!selectedItemData.value.parameters) {
		selectedItemData.value.parameters = {}
	}
	selectedItemData.value.parameters.email_content = content
	selectedItemData.value.parameters.template_id = `EMAIL_${Date.now()}`

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
