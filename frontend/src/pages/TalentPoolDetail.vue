<template>
    <div class="bg-gray-50 min-h-screen p-4 lg:p-8">
      <LayoutHeader>
        <template #left-header>
          <Breadcrumbs :items="breadcrumbs" />
        </template>
      </LayoutHeader>
      <div class="flex flex-col lg:flex-row gap-6 w-full">
        <!-- LEFT: Candidate Info -->
        <div class="bg-white rounded-2xl shadow p-6 w-full lg:w-1/3 h-fit relative">
          <!-- Source Badge -->
          <div v-if="data.source" class="absolute top-4 left-6">
            <span class="px-3 py-1 bg-blue-100 text-blue-700 text-xs font-medium rounded">
              {{ data.source }}
            </span>
          </div>
          
          <!-- Edit Button -->
          <button 
            @click="openEditDialog"
            class="absolute top-4 right-4 p-2 rounded-full hover:bg-gray-100 text-gray-500 hover:text-gray-700 transition-colors"
            :title="__('Edit')"
          >
            <i class="ti ti-pencil"></i>
          </button>
          
          <!-- Avatar -->
          <div class="flex flex-col items-center text-center">
            <Avatar
              :label="data.full_name"
              :title="data.full_name"
              size="3xl"
              class="w-20 h-20 text-3xl font-semibold"
            />
            <h2 class="mt-4 text-lg font-semibold text-gray-800">
              {{ data.full_name || 'N/A' }}
            </h2>
            <p class="text-sm text-gray-500" v-if="data.title">
              {{ data.title }}
            </p>
          </div>
  
          <!-- Contact -->
          <div class="mt-6 border-t">
            <h3 class="text-sm font-semibold text-gray-700 my-3">
              THÔNG TIN LIÊN HỆ
            </h3>
            <ul class="text-sm text-gray-600 space-y-2">
              <li class="flex items-center gap-2" v-if="data.contact_email">
                <i class="ti ti-mail text-gray-500"></i>
                <a :href="'mailto:' + data.contact_email" class="hover:text-blue-600">
                  {{ data.contact_email }}
                </a>
              </li>
              <li class="flex items-center gap-2" v-if="data.contact_phone">
                <i class="ti ti-phone text-gray-500"></i>
                <a :href="'tel:' + data.contact_phone" class="hover:text-blue-600">
                  {{ data.contact_phone }}
                </a>
              </li>
              <li class="flex items-center gap-2" v-if="data.linkedin_profile">
                <i class="ti ti-brand-linkedin text-gray-500"></i>
                <a :href="data.linkedin_profile" target="_blank" class="hover:text-blue-600">
                  LinkedIn
                </a>
              </li>
              <li class="flex items-center gap-2" v-if="data.facebook_profile">
                <i class="ti ti-brand-facebook text-gray-500"></i>
                <a :href="data.facebook_profile" target="_blank" class="hover:text-blue-600">
                  Facebook
                </a>
              </li>
              <!-- <li class="flex items-center gap-2" v-if="data.zalo_profile">
                <i class="ti ti-brand-zalo text-gray-500"></i>
                <a :href="data.zalo_profile" target="_blank" class="hover:text-blue-600">
                  Zalo
                </a>
              </li> -->
            </ul>
          </div>
  
          <!-- Skills -->
          <div class="mt-6 border-t" v-if="data.skills">
            <h3 class="text-sm font-semibold text-gray-700 my-3">KỸ NĂNG</h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="(skill, index) in data.skills.split(',').map(s => s.trim())"
                :key="index"
                class="px-3 py-1 bg-purple-100 text-purple-700 text-xs font-medium rounded"
              >
                {{ skill }}
              </span>
            </div>
          </div>
  
          <!-- Summary -->
          <div class="mt-6 border-t" v-if="false">
            <h3 class="text-sm font-semibold text-gray-700 my-3">AI TÓM TẮT</h3>
            <p class="text-sm text-gray-600 leading-relaxed">
              <!-- AI Summary content will go here -->
            </p>
          </div>
        </div>
  
        <!-- RIGHT: Interaction Journey -->
        <div class="bg-white rounded-2xl shadow p-6 flex-1">
          <h3 class="text-base font-semibold text-gray-800 mb-2">
            Hành trình Tương tác
          </h3>
          <p class="text-sm text-gray-500 mb-6">
            Chiến dịch:
            <span class="font-medium">Nuôi dưỡng ứng viên React Quý 4/2025</span>
          </p>
  
          <div class="space-y-8 relative">
            <!-- Timeline Line -->
            <div class="absolute left-4 top-0 bottom-0 w-px bg-gray-200"></div>
  
            <!-- Step 1 -->
            <div class="relative pl-10">
              <div
                class="absolute left-0 top-1 w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center"
              >
                <i class="ti ti-mail"></i>
              </div>
              <h4 class="font-semibold text-gray-800">Gửi Email Chào mừng</h4>
              <p class="text-xs text-gray-500 mb-1">20/06/2025</p>
              <p class="text-sm text-gray-600">
                Hệ thống đã tự động gửi email giới thiệu về chiến dịch.
              </p>
            </div>
  
            <!-- Step 2 -->
            <div class="relative pl-10">
              <div
                class="absolute left-0 top-1 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center"
              >
                <i class="ti ti-eye"></i>
              </div>
              <h4 class="font-semibold text-gray-800">Ứng viên đã mở Email</h4>
              <p class="text-xs text-gray-500 mb-1">21/06/2025</p>
              <p class="text-sm text-gray-600">
                Email được mở trên thiết bị di động.
              </p>
            </div>
  
            <!-- Step 3 -->
            <div class="relative pl-10">
              <div
                class="absolute left-0 top-1 w-8 h-8 bg-yellow-500 text-white rounded-full flex items-center justify-center"
              >
                <i class="ti ti-phone"></i>
              </div>
              <h4 class="font-semibold text-gray-800">Tác vụ: Gọi điện thoại</h4>
              <p class="text-xs text-gray-500 mb-2">24/06/2025</p>
  
              <div class="bg-gray-50 border border-gray-200 rounded-xl p-4">
                <p class="text-sm text-gray-700 mb-3 font-medium">Kịch bản gợi ý:</p>
                <ul class="text-sm text-gray-600 list-disc list-inside space-y-1 mb-4">
                  <li>Chào anh An, em là [Tên] từ công ty ABC.</li>
                  <li>Thấy anh có quan tâm đến email của bên em.</li>
                  <li>Hỏi thêm về định hướng và chia sẻ thêm về cơ hội.</li>
                </ul>
  
                <div class="mb-3">
                  <p class="text-sm text-gray-700 mb-1">Cập nhật kết quả:</p>
                  <div class="flex flex-wrap gap-2">
                    <button
                      class="px-3 py-1 text-xs rounded-full border border-gray-300 hover:bg-gray-100"
                    >
                      Đã trả lời
                    </button>
                    <button
                      class="px-3 py-1 text-xs rounded-full border border-gray-300 hover:bg-gray-100"
                    >
                      Không nghe máy
                    </button>
                    <button
                      class="px-3 py-1 text-xs rounded-full bg-purple-600 text-white"
                    >
                      Để lại lời nhắn
                    </button>
                  </div>
                </div>
  
                <textarea
                  rows="2"
                  placeholder="Ghi chú..."
                  class="w-full border border-gray-300 rounded-lg text-sm p-2 mb-3 focus:outline-none focus:ring-1 focus:ring-purple-500"
                ></textarea>
  
                <button
                  class="w-full bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium py-2 rounded-lg"
                >
                  Hoàn thành tác vụ
                </button>
              </div>
            </div>
  
            <!-- Step 4 -->
            <div class="relative pl-10">
              <div
                class="absolute left-0 top-1 w-8 h-8 bg-gray-600 text-white rounded-full flex items-center justify-center"
              >
                <i class="ti ti-send"></i>
              </div>
              <h4 class="font-semibold text-gray-800">Gửi Email Follow-up</h4>
              <p class="text-xs text-gray-500 mb-1">27/06/2025</p>
              <p class="text-sm text-gray-600">
                Hệ thống được lên lịch gửi email thứ hai nếu không có phản hồi sau
                cuộc gọi.
              </p>
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
            v-model="editData.contact_email"
            type="email"
            :required="true"
          />
          
          <FormControl
            :label="__('Phone')"
            v-model="editData.contact_phone"
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
          <Button variant="solid" @click="saveChanges">
            Lưu thay đổi
          </Button>
        </div>
      </template>
    </Dialog>
  </template>
  
<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Breadcrumbs, Avatar, Dialog, Input, FormControl } from 'frappe-ui'
import { useRouter } from 'vue-router'
import { useTalentPoolStore } from '@/stores/talentPool'
import { ref, reactive, onMounted, nextTick } from 'vue'
import { useToast } from '@/composables/useToast'


const talentPoolStore = useTalentPoolStore()
const route = useRouter()
const toast = useToast()
const data = reactive({})
const showEditDialog = ref(false)
const editData = reactive({})
const editForm = ref(null)
let title = __('Talent Pools Details')
const breadcrumbs = [{ label: title, route: { name: 'TalentPoolDetail' } }]

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString()
}

const openEditDialog = () => {
  Object.assign(editData, JSON.parse(JSON.stringify(data)))
  showEditDialog.value = true
  // Focus the first input field when dialog opens
  nextTick(() => {
    if (editForm.value) {
      console.log("editForm.value", editForm.value);
      const firstInput = editForm.value.querySelector('input')
      if (firstInput) firstInput.focus()
    }
  })
}

const saveChanges = async () => {
  try {
    await talentPoolStore.updateTalentPool(data.name, editData)
    Object.assign(data, editData)
    showEditDialog.value = false
    toast.success('Đã cập nhật thông tin ứng viên')
  } catch (error) {
    console.error('Error updating talent pool:', error)
    toast.error('Có lỗi xảy ra khi cập nhật thông tin')
  }
}

onMounted(async () => {
  try {
    const id = route.currentRoute.value.params.id
    if (id) {
      const res = await talentPoolStore.TalentPoolDetail(id)
      Object.assign(data, res)
    }
  } catch (error) {
    console.error('Error fetching talent pool details:', error)
    toast.error('Không thể tải thông tin ứng viên')
  }
})

</script>
  
<style scoped>
@import "https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css";
</style>
  