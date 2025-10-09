<template>
	<div class="bg-white min-h-screen">
		<LayoutHeader>
			<template #left-header>
				<Breadcrumbs :items="breadcrumbs" />
			</template>
		</LayoutHeader>
		<div class="flex flex-col lg:flex-row">
			<!-- Left half - Candidate Information -->
			<div class="w-full lg:w-1/3 bg-white p-5 border-r">
				<!-- Avatar and Name -->
				<div class="relative">
					<!-- Edit Button -->
					<div class="absolute top-0 right-0">
						<Button
              @click="openEditDialog"
							variant="ghost"
							size="2xl"
							class="text-gray-500 hover:bg-gray-100 p-2"
						>
							<i class="ti ti-edit text-xl"></i>
						</Button>
					</div>

					<!-- Avatar and Text -->
					<div class="flex flex-col items-center text-center pb-2">
						<div class="mb-3">
							<Avatar
								:image="data.talent_info.avatar"
								:label="data.talent_info.full_name"
								size="2xl"
								class="ring-2 ring-gray-200 mx-auto mb-4 w-32 h-32"
							/>
						</div>
						<h3 class="text-2xl font-semibold text-gray-900 mb-1.5">
							{{ data.talent_info.full_name || 'Chưa có tên' }}
						</h3>
					</div>
				</div>

				<!-- Contact Info -->
				<div class="mt-2 pt-3 border-t border-gray-100">
					<div class="flex items-center mb-4">
						<i class="ti ti-info-circle text-2xl text-blue-500 mr-3"></i>
						<h4 class="text-lg font-semibold text-gray-800">Thông tin liên hệ</h4>
					</div>
					<div class="space-y-3">
						<div
							class="flex items-center text-base text-gray-700 p-3 hover:bg-gray-50 rounded-lg transition-colors"
						>
							<i class="ti ti-mail text-xl text-blue-500 mr-4 w-6 text-center"></i>
							<span class="flex-1">{{
								data.talent_info.email || 'Chưa có email'
							}}</span>
						</div>
						<div
							class="flex items-center text-base text-gray-700 p-3 hover:bg-gray-50 rounded-lg transition-colors"
						>
							<i class="ti ti-phone text-xl text-blue-500 mr-4 w-6 text-center"></i>
							<span class="flex-1">{{
								data.talent_info.phone || 'Chưa có số điện thoại'
							}}</span>
						</div>
						<div
							class="flex items-center text-base text-gray-700 p-3 hover:bg-gray-50 rounded-lg transition-colors"
						>
							<i
								class="ti ti-calendar text-xl text-blue-500 mr-4 w-6 text-center"
							></i>
							<span class="flex-1">{{
								data.talent_info.date_of_birth
									? formatDate(data.talent_info.date_of_birth)
									: 'Chưa cập nhật'
							}}</span>
						</div>

						<!-- Social Media Links -->
						<div v-if="data.talent_info.facebook_profile || data.talent_info.linkedin_profile" 
							class="flex items-center text-base text-gray-700 p-3 hover:bg-gray-50 rounded-lg transition-colors">
							<i class="ti ti-share text-xl text-blue-500 mr-4 w-6 text-center"></i>
							<div class="flex-1 flex gap-4">
								<a v-if="data.talent_info.facebook_profile" 
									:href="data.talent_info.facebook_profile" 
									target="_blank" 
									class="flex items-center text-blue-600">
									<i class="ti ti-brand-facebook text-lg mr-2"></i>
									<p class="hover:underline">Facebook</p>
								</a>
								<a v-if="data.talent_info.linkedin_profile" 
									:href="data.talent_info.linkedin_profile" 
									target="_blank" 
									class="flex items-center text-blue-700">
									<i class="ti ti-brand-linkedin text-lg mr-2"></i>
									<p class="hover:underline">LinkedIn</p>
								</a>
							</div>
						</div>
					</div>
				</div>

				<!-- Skills -->
				<div class="mt-2 pt-3 border-t">
					<div class="flex items-center mb-4">
						<i class="ti ti-tags text-xl text-blue-500 mr-2"></i>
						<h4 class="text-base font-semibold text-gray-800">Kỹ năng</h4>
					</div>
					<div class="flex flex-wrap gap-3">
						<template
							v-if="data.talent_info.skills && data.talent_info.skills.length > 0"
						>
							<span
								v-for="(skill, index) in data.talent_info.skills
									.split(',')
									.slice(0, 6)"
								:key="index"
								class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-blue-50 text-blue-700 border border-blue-100 shadow-sm"
							>
								<i class="ti ti-check text-blue-500 mr-1.5 text-base"></i>
								{{ skill.trim() }}
							</span>
							<span
								v-if="data.talent_info.skills.split(',').length > 6"
								class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-blue-50 text-blue-500 border border-blue-100"
							>
								+{{ data.talent_info.skills.split(',').length - 6 }} kỹ năng khác
							</span>
						</template>
						<div v-else class="w-full text-center py-4">
							<i class="ti ti-mood-sad text-2xl text-gray-300 mb-2 block"></i>
							<span class="text-sm text-gray-400">Chưa cập nhật kỹ năng</span>
						</div>
					</div>
				</div>
			</div>

			<!-- Right half -->
			<div class="w-full lg:w-2/3 bg-white">
				<div class="space-y-4">
					<!-- Tabs header -->
					<Tabs as="div" class="" v-model="tabIndex" :tabs="tabs" />

					<!-- Tab content -->
					<div v-if="tabIndex === 0">
						<div class="overflow-x-auto">
							<table class="w-full text-sm text-left text-gray-500">
								<thead class="text-xs text-gray-700 uppercase bg-gray-50">
									<tr>
										<th scope="col" class="px-6 py-3">Tên chiến dịch</th>
										<th scope="col" class="px-6 py-3">Trạng thái</th>
										<th scope="col" class="px-6 py-3">Thời gian tiếp theo</th>
										<th scope="col" class="px-6 py-3">Hành động</th>
									</tr>
								</thead>
								<tbody>
									<tr
										v-if="data.campaigns && data.campaigns.length > 0"
										v-for="(campaign, index) in data.campaigns"
										:key="index"
										class="bg-white border-b hover:bg-gray-50"
									>
										<td
											class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap"
										>
											{{ campaign.campaign_name }}
										</td>
										<td class="px-6 py-4">
											<span
												:class="[
													'px-2.5 py-0.5 rounded-full text-xs font-medium',
													campaign.status === 'ACTIVE'
														? 'bg-green-100 text-green-800'
														: 'bg-gray-100 text-gray-800',
												]"
											>
												{{
													campaign.status === 'ACTIVE'
														? 'Đang hoạt động'
														: 'Đã kết thúc'
												}}
											</span>
										</td>
										<td class="px-6 py-4">
											{{
												formatDateTime(campaign.next_action_at) ||
												'Chưa cập nhật'
											}}
										</td>
										<td class="px-6 py-4">
											<button class="text-blue-600 hover:text-blue-900">
												Xem chi tiết
											</button>
										</td>
									</tr>
									<tr v-else>
										<td
											colspan="4"
											class="px-6 py-4 text-center text-gray-500"
										>
											Không có dữ liệu
										</td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>

					<div v-else-if="tabIndex === 1">
						<div class="overflow-x-auto">
							<table class="w-full text-sm text-left text-gray-500">
								<thead class="text-xs text-gray-700 uppercase bg-gray-50">
									<tr>
										<th scope="col" class="px-6 py-3">Tên hành động</th>
										<th scope="col" class="px-6 py-3">Chiến dịch</th>
										<th scope="col" class="px-6 py-3">Thời gian</th>
										<th scope="col" class="px-6 py-3">Trạng thái</th>
									</tr>
								</thead>
								<tbody>
									<tr
										v-if="data.actions && data.actions.length > 0"
										v-for="(action, index) in data.actions"
										:key="index"
										class="bg-white border-b hover:bg-gray-50"
									>
										<td class="px-6 py-4 font-medium text-gray-900">
											{{ action.step_name }}
										</td>
										<td class="px-6 py-4">
											{{ action.campaign_name }}
										</td>
										<td class="px-6 py-4">
											{{ formatDateTime(action.scheduled_at) }}
										</td>
										<td class="px-6 py-4">
											<span
												:class="[
													'px-2.5 py-0.5 rounded-full text-xs font-medium',
													action.status === 'EXECUTED'
														? 'bg-green-100 text-green-800'
														: action.status === 'PENDING_MANUAL'
															? 'bg-yellow-100 text-yellow-800'
															: 'bg-gray-100 text-gray-800',
												]"
											>
												{{ getStatusText(action.status) }}
											</span>
										</td>
									</tr>
									<tr v-else>
										<td
											colspan="4"
											class="px-6 py-4 text-center text-gray-500"
										>
											Không có dữ liệu
										</td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>

					<div v-else-if="tabIndex === 2">
						<div class="overflow-x-auto">
							<table class="w-full text-sm text-left text-gray-500">
								<thead class="text-xs text-gray-700 uppercase bg-gray-50">
									<tr>
										<th scope="col" class="px-6 py-3">Tên hành động</th>
										<th scope="col" class="px-6 py-3">Chiến dịch</th>
										<th scope="col" class="px-6 py-3">Thời gian</th>
										<th scope="col" class="px-6 py-3">Trạng thái</th>
									</tr>
								</thead>
								<tbody>
									<tr
										v-if="data.interactions && data.interactions.length > 0"
										v-for="(interaction, index) in data.interactions"
										:key="index"
										class="bg-white border-b hover:bg-gray-50"
									>
										<td class="px-6 py-4 font-medium text-gray-900">
											{{ interaction.step_name }}
										</td>
										<td class="px-6 py-4">
											{{ interaction.campaign_name }}
										</td>
										<td class="px-6 py-4">
											{{ formatDateTime(interaction.creation) }}
										</td>
										<td class="px-6 py-4">
											<span
												:class="[
													'',
													interaction.interaction_type === 'EMAIL_SENT'
														? 'bg-green-100 text-green-800'
														: interaction.interaction_type === 'EMAIL_DELIVERED'
															? 'bg-yellow-100 text-yellow-800'
															: 'bg-gray-100 text-gray-800',
													]"
											>
												{{ getInteractionType(interaction.interaction_type) }}
											</span>
										</td>
									</tr>
									<tr v-else>
										<td
											colspan="4"
											class="px-6 py-4 text-center text-gray-500"
										>
											Không có dữ liệu
										</td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Edit Dialog -->
	<Dialog v-model="showEditDialog" :options="{
    title: __('Edit Talent'),
    size: '2xl'
  }">

    <template #body-content>
      <div class="space-y-4">
        <FormControl
          :label="__('Full Name')"
          v-model="editData.full_name"
          :required="true"
        />

        <FormControl
          :label="__('Email')"
          v-model="editData.email"
          type="email"
          :required="true"
        />
        
        <FormControl
          :label="__('Phone')"
          v-model="editData.phone"
          type="tel"
        />
        
        <FormControl
          :label="__('Linkin')"
          v-model="editData.linkedin_profile"
          type="url"
          :placeholder="__('https://linkedin.com/in/...')"
        >
          <template #prefix>
            <i class="ti ti-brand-linkedin text-gray-400"></i>
          </template>
        </FormControl>
        
        <FormControl
          :label="__('Facebook')"
          v-model="editData.facebook_profile"
          type="url"
          :placeholder="__('https://facebook.com/...')"
        >
          <template #prefix>
            <i class="ti ti-brand-facebook text-gray-400"></i>
          </template>
        </FormControl>
        
        <FormControl
          :label="__('Date of Birth')"
          :model-value="editData.date_of_birth ? editData.date_of_birth.toISOString().split('T')[0] : ''"
          @update:modelValue="val => editData.date_of_birth = val ? new Date(val) : null"
          type="date"
          :max="new Date().toISOString().split('T')[0]"
        />
        
        <FormControl
          :label="__('Skills (separated by commas)')"
          v-model="editData.skills"
          as="textarea"
          rows="2"
          :placeholder="__('Example: React, Node.js, JavaScript')"
        />
      </div>
    </template>
    
    <template #actions>
      <div class="flex justify-end space-x-3">
        <Button variant="ghost" @click="showEditDialog = false">
          Hủy
        </Button>
        <Button variant="solid" @click="saveChanges" :loading="isSaving">
          {{ isSaving ? 'Đang lưu...' : 'Lưu thay đổi' }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Breadcrumbs, Avatar, Dialog, Input, FormControl, call, Tabs } from 'frappe-ui'
import { useRouter } from 'vue-router'
import { useTalentPoolStore } from '@/stores/talentPool'
import { ref, reactive, onMounted, nextTick, computed } from 'vue'
import { useToast } from '@/composables/useToast'
const tabs = [
	{ label: 'Campaigns', value: 0 },
	{ label: 'Actions', value: 1 },
	{ label: 'Interactions', value: 2 },
]
const tabIndex = ref(0)
const talentPoolStore = useTalentPoolStore()
const route = useRouter()
const toast = useToast()
const data = reactive({
	// Talent Pool info
	talent_info: {},

	// Interactions
	interactions: [],

	// Action
	actions: [],
})
const showEditDialog = ref(false)
const editData = reactive({})
const editForm = ref(null)
const isSaving = ref(false)

const breadcrumbs = computed(() => [
	{ label: __('Talent Pools Details'), route: { name: 'TalentSegments' } },
	{ label: data.talent_info.full_name || __('Job Detail'), route: { name: 'TalentPoolDetail' } },
])

const formatDate = (date) => {
	if (!date) return '-'
	return new Date(date).toLocaleDateString('vi-VN', {
		year: 'numeric',
		month: '2-digit',
		day: '2-digit',
	})
}

const formatDateTime = (dateString) => {
	if (!dateString) return ''
	const date = new Date(dateString)
	return date.toLocaleDateString('vi-VN', {
		day: '2-digit',
		month: '2-digit',
		year: 'numeric',
		hour: '2-digit',
		minute: '2-digit',
	})
}

const formatTime = (dateString) => {
	if (!dateString) return ''
	const date = new Date(dateString)
	return date.toLocaleTimeString('vi-VN', {
		hour: '2-digit',
		minute: '2-digit',
	})
}

const getStatusText = (status) => {
	const statusMap = {
		SCHEDULED: 'Đã lên lịch',
		EXECUTED: 'Đã thực hiện',
		SKIPPED: 'Đã bỏ qua',
		FAILED: 'Thất bại',
		PENDING_MANUAL: 'Chờ xử lý thủ công',
		PENDING: 'Đang chờ',
	}
	return statusMap[status] || status
}

const getInteractionType = (type) => {
	const typeMap = {
		EMAIL_SENT: 'Đã gửi email',
		EMAIL_DELIVERED: 'Email đã gửi thành công',
		EMAIL_BOUNCED: 'Email bị trả lại',
		EMAIL_OPENED: 'Đã mở email',
		EMAIL_CLICKED: 'Đã nhấp vào liên kết trong email',
		EMAIL_UNSUBSCRIBED: 'Đã hủy đăng ký email',
		EMAIL_REPLIED: 'Đã trả lời email',
		PAGE_VISITED: 'Đã truy cập trang',
		FORM_SUBMITTED: 'Đã gửi biểu mẫu',
		DOWNLOAD_TRIGGERED: 'Đã tải xuống tài liệu',
		CHAT_STARTED: 'Đã bắt đầu trò chuyện',
		CHAT_MESSAGE_SENT: 'Đã gửi tin nhắn chat',
		CHAT_COMPLETED: 'Đã kết thúc trò chuyện',
		CALL_MISSED: 'Cuộc gọi nhỡ',
		CALL_COMPLETED: 'Đã hoàn thành cuộc gọi',
		SMS_SENT: 'Đã gửi SMS',
		SMS_DELIVERED: 'SMS đã gửi thành công',
		SMS_REPLIED: 'Đã trả lời SMS',
		APPLICATION_SUBMITTED: 'Đã nộp đơn ứng tuyển',
		DOCUMENT_UPLOADED: 'Đã tải lên tài liệu',
		TEST_STARTED: 'Đã bắt đầu bài kiểm tra',
		TEST_COMPLETED: 'Đã hoàn thành bài kiểm tra',
		INTERVIEW_CONFIRMED: 'Đã xác nhận phỏng vấn',
		INTERVIEW_RESCHEDULED: 'Đã đổi lịch phỏng vấn'
	}
	return typeMap[type] || type
}

const openEditDialog = () => {
  // Ensure date is a Date object or null
  const dateOfBirth = data.talent_info.date_of_birth 
    ? new Date(data.talent_info.date_of_birth)
    : null
    
  // Copy current talent info to edit form
  Object.assign(editData, {
    full_name: data.talent_info.full_name || '',
    email: data.talent_info.email || '',
    phone: data.talent_info.phone || '',
    linkedin_profile: data.talent_info.linkedin_profile || '',
    facebook_profile: data.talent_info.facebook_profile || '',
    skills: data.talent_info.skills || '',
    date_of_birth: dateOfBirth
  })
  showEditDialog.value = true
}

const saveChanges = async () => {
  try {
    isSaving.value = true
    
    // Format date to YYYY-MM-DD for Frappe if it exists
    const formattedDate = editData.date_of_birth 
      ? editData.date_of_birth.toISOString().split('T')[0]
      : null
      
    // Update the talent information
    await call('frappe.client.set_value', {
      doctype: 'Mira Talent',
      name: data.talent_info.id,
      fieldname: {
        full_name: editData.full_name,
        email: editData.email,
        phone: editData.phone,
        date_of_birth: formattedDate,
        linkedin_profile: editData.linkedin_profile,
        facebook_profile: editData.facebook_profile,
        skills: editData.skills
      }
    })
    
    // Update local data
    Object.assign(data.talent_info, {
      full_name: editData.full_name,
      email: editData.email,
      phone: editData.phone,
      date_of_birth: editData.date_of_birth,
      linkedin_profile: editData.linkedin_profile,
      facebook_profile: editData.facebook_profile,
      skills: editData.skills
    })
    
    toast.success('Cập nhật thông tin thành công')
    showEditDialog.value = false
  } catch (error) {
    console.error('Error saving talent info:', error)
    toast.error('Có lỗi xảy ra khi lưu thông tin')
  } finally {
    isSaving.value = false
  }
}

onMounted(async () => {
	try {
		const id = route.currentRoute.value.params.id
		if (id) {
			const response = await talentPoolStore.getTalentDetailView(id)
			if (response.success) {
				Object.assign(data, response.data)
			}
      console.log('data detail>>>>>>', data)
		}
	} catch (error) {
		console.error('Error fetching data:', error)
		toast.error('Có lỗi xảy ra khi tải dữ liệu')
	}
})
</script>

<style scoped>
@import 'https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css';
</style>
