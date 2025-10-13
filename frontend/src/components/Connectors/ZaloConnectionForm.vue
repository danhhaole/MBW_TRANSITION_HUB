<template>
  <div class="zalo-connection-form p-4">
    <div v-if="!isEdit" class="space-y-6">
      

      <!-- Basic Information -->
      <div class="space-y-4">
        <h4 class="font-medium text-gray-900 border-b pb-2">
          {{ __("Thông tin cơ bản") }}
        </h4>

        <div class="grid grid-cols-1 gap-4">
          <!-- <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{__('Tenant Name *')}}
            </label>
            <input v-model="formData.tenant_name" type="text"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              :placeholder="__('VD: https://hireos.fastwork.vn')" required />
          </div> -->

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __("Email người dùng *") }}
            </label>
            <input
              v-model="formData.user_email"
              type="email"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              :placeholder="__('user@company.com')"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __("Họ và tên *") }}
            </label>
            <input
              v-model="formData.full_name"
              type="text"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              :placeholder="__('Nhập họ và tên')"
              required
            />
          </div>
        </div>
      </div>

      <!-- Webhook Configuration -->
      <div class="space-y-4">
        <h4 class="font-medium text-gray-900 border-b pb-2">
          {{ __("Cấu hình Webhook") }}
        </h4>

        <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
          <div class="flex items-start">
            <FeatherIcon
              name="alert-triangle"
              class="w-4 h-4 text-yellow-600 mr-2 mt-0.5"
            />
            <div class="text-sm text-yellow-800">
              <p class="font-medium mb-1">{{ __("Lưu ý quan trọng:") }}</p>
              <p>
                {{
                  __(
                    "Đảm bảo URL webhook có thể truy cập từ internet để SocialHub gửi callback."
                  )
                }}
              </p>
            </div>
          </div>
        </div>

        <!-- <div class="grid grid-cols-1 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{__('Webhook URL *')}}
            </label>
            <input v-model="formData.hook_url" type="url"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              :placeholder="defaultHookUrl" required />
            <p class="text-xs text-gray-500 mt-1">
              {{__('URL nhận callback xác thực từ SocialHub')}}
            </p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{__('Redirect URL *')}}
            </label>
            <input v-model="formData.redirect_url" type="url"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              :placeholder="defaultRedirectUrl" required />
            <p class="text-xs text-gray-500 mt-1">
              {{__('URL chuyển hướng sau khi xác thực thành công')}}
            </p>
          </div>
        </div> -->
      </div>

      <!-- Broadcasting Settings -->
      <div class="space-y-4">
        <h4 class="font-medium text-gray-900 border-b pb-2">
          {{ __("Cài đặt Broadcasting") }}
        </h4>

        <div class="flex items-center space-x-2">
          <input
            id="enable-broadcasting"
            v-model="formData.enable_broadcasting"
            type="checkbox"
            class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />
          <label for="enable-broadcasting" class="text-sm text-gray-700">
            {{ __("Cho phép gửi tin broadcast đến followers") }}
          </label>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __("Giới hạn tin/ngày") }}
            </label>
            <input
              v-model="formData.daily_message_limit"
              type="number"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="1000"
              min="1"
            />
            <p class="text-xs text-gray-500 mt-1">
              {{ __("Để trống nếu không giới hạn") }}
            </p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __("Ưu tiên tin nhắn") }}
            </label>
            <select
              v-model="formData.message_priority"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="high">{{ __("Cao") }}</option>
              <option value="normal">{{ __("Bình thường") }}</option>
              <option value="low">{{ __("Thấp") }}</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Advanced Settings -->
      <div class="space-y-4">
        <h4 class="font-medium text-gray-900 border-b pb-2">
          {{ __("Cài đặt nâng cao") }}
        </h4>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __("Tần suất đồng bộ") }}
            </label>
            <select
              v-model="formData.sync_frequency"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="Hourly">{{ __("Every hour") }}</option>
              <option value="Every 5 minutes">{{ __("Every 5 minutes") }}</option>
              <option value="Every 15 minutes">{{ __("Every 15 minutes") }}</option>
              <option value="Every 30 minutes">{{ __("Every 30 minutes") }}</option>
              <option value="Daily">{{ __("Daily") }}</option>
              <option value="Real-time">{{ __("Real-time") }}</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __("Số lần thử lại tối đa") }}
            </label>
            <input
              v-model="formData.max_retries"
              type="number"
              min="1"
              max="5"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="3"
            />
          </div>
        </div>

        <div class="flex items-center space-x-2">
          <input
            id="debug-mode"
            v-model="formData.debug_mode"
            type="checkbox"
            class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />
          <label for="debug-mode" class="text-sm text-gray-700">
            {{ __("Bật chế độ debug để ghi log chi tiết") }}
          </label>
        </div>
      </div>

      <!-- Expected Permissions -->
      <div class="space-y-4">
        <h4 class="font-medium text-gray-900 border-b pb-2">
          {{ __("Quyền truy cập Zalo") }}
        </h4>

        <div class="bg-blue-50 rounded-lg p-4">
          <p class="text-sm text-blue-900 mb-3">
            {{ __("Các quyền sau sẽ được yêu cầu khi xác thực Zalo OA:") }}
          </p>

          <div class="grid grid-cols-1 gap-3">
            <div
              v-for="permission in zaloPermissions"
              :key="permission.value"
              class="flex items-start space-x-2"
            >
              <FeatherIcon name="check" class="w-4 h-4 text-green-600 mt-0.5" />
              <div>
                <div class="text-sm font-medium text-gray-900">
                  {{ __(permission.label) }}
                </div>
                <div class="text-xs text-gray-600">{{ __(permission.description) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Mode - Connected OA Management -->
    <div v-else class="space-y-6">
      <!-- Connection Status -->
      <div class="flex items-center p-4 bg-green-50 rounded-lg">
        <FeatherIcon name="check-circle" class="w-8 h-8 text-green-600 mr-3" />
        <div class="flex-1">
          <h4 class="font-medium text-green-900">{{ __("Zalo OA đã kết nối") }}</h4>
          <p class="text-sm text-green-700">
            {{ __("OA:") }}
            {{ existingConnection?.account_name || __("Zalo Official Account") }}
          </p>
          <p class="text-xs text-green-600 mt-1">
            {{ __("ID:") }} {{ existingConnection?.oa_id || __("N/A") }}
          </p>
          <p class="text-xs text-green-600">
            {{ __("Đồng bộ lần cuối:") }} {{ formatDate(existingConnection?.last_sync) }}
          </p>
        </div>
        <Button variant="ghost" size="sm" @click="syncNow" :loading="syncing">
          <template #prefix>
            <FeatherIcon name="refresh-cw" class="w-4 h-4" />
          </template>
          {{ __("Đồng bộ") }}
        </Button>
      </div>

      <!-- OA Information -->
      <div class="space-y-4">
        <h4 class="font-medium text-gray-900 border-b pb-2">
          {{ __("Thông tin Zalo OA") }}
        </h4>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="bg-white border border-gray-200 rounded-lg p-4">
            <div class="flex items-center space-x-3 mb-3">
              <div
                class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center"
              >
                <FeatherIcon name="message-circle" class="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <h5 class="font-medium text-gray-900">
                  {{ oaInfo.name || __("Zalo OA") }}
                </h5>
                <p class="text-sm text-gray-600">
                  {{ oaInfo.description || __("Official Account") }}
                </p>
              </div>
            </div>

            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-600">{{ __("OA ID:") }}</span>
                <span class="font-mono">{{ oaInfo.oa_id || __("N/A") }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">{{ __("Trạng thái:") }}</span>
                <Badge variant="solid" theme="green" size="sm">{{
                  __("Hoạt động")
                }}</Badge>
              </div>
            </div>
          </div>

          <div class="bg-white border border-gray-200 rounded-lg p-4">
            <h5 class="font-medium text-gray-900 mb-3">{{ __("Thống kê") }}</h5>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-600">{{ __("Followers:") }}</span>
                <span class="font-semibold">{{ oaStmira.followers || __("N/A") }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">{{ __("Tin gửi hôm nay:") }}</span>
                <span class="font-semibold">{{ oaStmira.messages_today || "0" }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">{{ __("Template được duyệt:") }}</span>
                <span class="font-semibold">{{
                  oaStmira.approved_templates || "0"
                }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Message Templates -->
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <h4 class="font-medium text-gray-900">{{ __("Message Templates") }}</h4>
          <Button
            variant="outline"
            size="sm"
            @click="refreshTemplates"
            :loading="refreshingTemplates"
          >
            <template #prefix>
              <FeatherIcon name="refresh-cw" class="w-4 h-4" />
            </template>
            {{ __("Làm mới") }}
          </Button>
        </div>

        <div v-if="messageTemplates.length > 0" class="space-y-3">
          <div
            v-for="template in messageTemplates"
            :key="template.id"
            class="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:border-gray-300 transition-colors"
          >
            <div class="flex items-center space-x-3">
              <div
                class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center"
              >
                <FeatherIcon name="message-square" class="w-4 h-4 text-green-600" />
              </div>
              <div>
                <div class="font-medium text-gray-900">{{ template.name }}</div>
                <div class="text-sm text-gray-600">
                  {{ template.content?.substring(0, 50) }}...
                </div>
              </div>
            </div>

            <div class="flex items-center space-x-2">
              <Badge
                :variant="template.status === 'approved' ? 'solid' : 'outline'"
                theme="green"
                size="sm"
              >
                {{ template.status === "approved" ? __("Đã duyệt") : __("Chờ duyệt") }}
              </Badge>
              <Dropdown :options="getTemplateActions(template)">
                <template #default="{ open }">
                  <Button variant="ghost" size="sm" @click="open">
                    <FeatherIcon name="more-vertical" class="w-4 h-4" />
                  </Button>
                </template>
              </Dropdown>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-8">
          <FeatherIcon
            name="message-square"
            class="w-12 h-12 text-gray-400 mx-auto mb-3"
          />
          <h3 class="text-lg font-medium text-gray-900 mb-2">
            {{ __("Chưa có template") }}
          </h3>
          <p class="text-gray-600 mb-4">
            {{ __("Chưa có message template nào được tìm thấy.") }}
          </p>
          <Button
            variant="outline"
            @click="refreshTemplates"
            :loading="refreshingTemplates"
          >
            <template #prefix>
              <FeatherIcon name="refresh-cw" class="w-4 h-4" />
            </template>
            {{ __("Làm mới Templates") }}
          </Button>
        </div>
      </div>

      <!-- Settings Update -->
      <div class="space-y-4">
        <h4 class="font-medium text-gray-900 border-b pb-2">
          {{ __("Cập nhật cài đặt") }}
        </h4>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __("Tần suất đồng bộ") }}
            </label>
            <select
              v-model="formData.sync_frequency"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="Hourly">{{ __("Every hour") }}</option>
              <option value="Every 5 minutes">{{ __("Every 5 minutes") }}</option>
              <option value="Every 15 minutes">{{ __("Every 15 minutes") }}</option>
              <option value="Every 30 minutes">{{ __("Every 30 minutes") }}</option>
              <option value="Daily">{{ __("Daily") }}</option>
              <option value="Real-time">{{ __("Real-time") }}</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __("Giới hạn tin/ngày") }}
            </label>
            <input
              v-model="formData.daily_message_limit"
              type="number"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="1000"
            />
          </div>
        </div>

        <div class="space-y-3">
          <div class="flex items-center space-x-2">
            <input
              id="enable-broadcasting-edit"
              v-model="formData.enable_broadcasting"
              type="checkbox"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <label for="enable-broadcasting-edit" class="text-sm text-gray-700">
              {{ __("Cho phép broadcast đến followers") }}
            </label>
          </div>

          <div class="flex items-center space-x-2">
            <input
              id="auto-sync-templates"
              v-model="formData.auto_sync_templates"
              type="checkbox"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <label for="auto-sync-templates" class="text-sm text-gray-700">
              {{ __("Tự động đồng bộ templates") }}
            </label>
          </div>

          <div class="flex items-center space-x-2">
            <input
              id="debug-mode-edit"
              v-model="formData.debug_mode"
              type="checkbox"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <label for="debug-mode-edit" class="text-sm text-gray-700">
              {{ __("Bật chế độ debug") }}
            </label>
          </div>
        </div>
      </div>

      <!-- Danger Zone -->
      <div class="space-y-4 pt-6 border-t border-red-200">
        <h4 class="font-medium text-red-900">{{ __("Vùng nguy hiểm") }}</h4>

        <div class="bg-red-50 border border-red-200 rounded-lg p-4">
          <div class="flex items-start">
            <FeatherIcon name="alert-triangle" class="w-5 h-5 text-red-600 mr-3 mt-0.5" />
            <div class="flex-1">
              <h5 class="font-medium text-red-900">{{ __("Ngắt kết nối Zalo OA") }}</h5>
              <p class="text-sm text-red-700 mt-1">
                {{
                  __(
                    "Hành động này sẽ xóa kết nối với Zalo OA và dừng tất cả hoạt động tự động."
                  )
                }}
              </p>
              <Button
                variant="ghost"
                class="mt-3 text-red-600 hover:bg-red-100"
                @click="confirmDisconnect"
              >
                {{ __("Ngắt kết nối Zalo OA") }}
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex justify-end space-x-3 pt-6 border-t">
      <Button variant="ghost" @click="$emit('cancel')">
        {{ __("Hủy") }}
      </Button>

      <Button
        variant="solid"
        @click="handleSubmit"
        :loading="submitting"
        :disabled="!isFormValid"
      >
        {{ isEdit ? __("Cập nhật cài đặt") : __("Kết nối Zalo OA") }}
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from "vue";
import { Button, Badge, Dropdown, FeatherIcon, call } from "frappe-ui";
import useToast from "@/composables/useToast";

// Props
const props = defineProps({
  platform: {
    type: Object,
    required: true,
  },
  connectionType: {
    type: String,
    required: true,
  },
  isEdit: {
    type: Boolean,
    default: false,
  },
  existingConnection: {
    type: Object,
    default: null,
  },
  modelValue: {
    type: Object,
    default: () => ({}),
  },
});
import { usersStore } from "@/stores/user";
// Emits
const emit = defineEmits(["submit", "cancel", "update:modelValue"]);
const { userResource, allUsers, getUser } = usersStore();
// Toasts
const {
  success: toastSuccess,
  error: toastError,
  warning: toastWarning,
  info: toastInfo,
} = useToast();
// Reactive data
const submitting = ref(false);
const syncing = ref(false);
const refreshingTemplates = ref(false);
const messageTemplates = ref([]);
const oaInfo = ref({});
const oaStmira = ref({});

const formData = reactive({
  tenant_name: "",
  user_email: getUser?.data?.email,
  full_name: getUser?.data?.full_name,
  hook_url: "",
  redirect_url: "",
  enable_broadcasting: true,
  daily_message_limit: 1000,
  message_priority: "normal",
  sync_frequency: "Hourly",
  max_retries: 3,
  debug_mode: false,
  auto_sync_templates: true,
});

// Computed
const defaultHookUrl = computed(() => {
  return `${window.location.origin}/api/method/mbw_mira.api.external_connections.handle_webhook`;
});

const defaultRedirectUrl = computed(() => {
  return `${window.location.origin}/mbw_mira/connectors`;
});

const isFormValid = computed(() => {
  if (props.isEdit) {
    return true; // For edit mode, basic validation
  }

  return (
    formData.user_email &&
    formData.full_name &&
    formData.hook_url &&
    formData.redirect_url
  );
});

const zaloPermissions = [
  {
    label: __("Thông tin OA"),
    value: "oa_info",
    description: __("Truy cập thông tin cơ bản của Official Account"),
  },
  {
    label: __("Gửi tin nhắn"),
    value: "send_message",
    description: __("Gửi tin nhắn đến người dùng"),
  },
  {
    label: __("Quản lý followers"),
    value: "manage_followers",
    description: __("Truy cập và quản lý danh sách người theo dõi"),
  },
  {
    label: __("Broadcast messages"),
    value: "broadcast",
    description: __("Gửi tin nhắn broadcast đến nhiều người dùng"),
  },
];

// Methods
const handleSubmit = async () => {
  if (!isFormValid.value) return;

  try {
    submitting.value = true;

    const submitData = {
      ...formData,
      hook_url: formData.hook_url || defaultHookUrl.value,
      redirect_url: formData.redirect_url || defaultRedirectUrl.value,
    };

    emit("submit", submitData);
  } catch (error) {
    console.error("Error submitting form:", error);
  } finally {
    submitting.value = false;
  }
};

const syncNow = async () => {
  try {
    syncing.value = true;

    let response = await call("mbw_mira.api.external_connections.sync_accounts", {
      connection_id: props.existingConnection.connection_id,
      force_sync: true,
    });
    if (response && response.status == "success") {
      toastSuccess(`${__("Thành công")}: ${__("Đồng bộ Zalo OA thành công")}`);

      await loadOAInfo();
    } else {
      toastError(`${__("Lỗi")}: ${__("Đồng bộ Zalo OA thất bại")}`);
    }
  } catch (error) {
    console.error("Error syncing:", error);
    toastError(`${__("Lỗi")}: ${__("Đồng bộ Zalo OA thất bại")}`);
  } finally {
    syncing.value = false;
  }
};

const refreshTemplates = async () => {
  try {
    refreshingTemplates.value = true;
    await loadMessageTemplates();

    toastSuccess(`${__("Thành công")}: ${__("Làm mới templates thành công")}`);
  } catch (error) {
    console.error("Error refreshing templates:", error);
    toastError(`${__("Lỗi")}: ${__("Làm mới templates thất bại")}`);
  } finally {
    refreshingTemplates.value = false;
  }
};

const loadOAInfo = async () => {
  if (!props.existingConnection) return;

  try {
    const response = await call("mbw_mira.api.external_connections.get_account_details", {
      connection_id: props.existingConnection.connection_id,
    });

    oaInfo.value = response.oa_info || {};
    oaStmira.value = response.oa_stmira || {};
  } catch (error) {
    console.error("Error loading OA info:", error);
  }
};

const loadMessageTemplates = async () => {
  if (!props.existingConnection) return;

  try {
    // Mock data - replace with actual API call
    messageTemplates.value = [
      {
        id: "template_1",
        name: __("Thông báo tuyển dụng"),
        content: __("Chúng tôi đang tuyển dụng vị trí {{job_title}}. Ứng tuyển ngay!"),
        status: "approved",
      },
      {
        id: "template_2",
        name: __("Lời chào ứng viên"),
        content: __("Xin chào! Cảm ơn bạn đã quan tâm đến vị trí {{job_title}}."),
        status: "pending",
      },
    ];
  } catch (error) {
    console.error("Error loading templates:", error);
  }
};

const getTemplateActions = (template) => {
  return [
    {
      label: __("Xem chi tiết"),
      icon: "eye",
      onClick: () => viewTemplate(template),
    },
    {
      label: __("Sử dụng template"),
      icon: "copy",
      onClick: () => useTemplate(template),
    },
  ];
};

const viewTemplate = (template) => {
  // Implement template viewing
  toastInfo(`${__("Thông tin")}: ${__("Chức năng xem template sẽ được triển khai")}`);
};

const useTemplate = (template) => {
  // Implement template usage
  toastInfo(
    `${__("Thông tin")}: ${__("Template ")}"${template.name}"${__(" đã được sao chép")}`
  );
};

const confirmDisconnect = () => {
  if (
    confirm(
      __("Bạn có chắc chắn muốn ngắt kết nối Zalo OA? Hành động này không thể hoàn tác.")
    )
  ) {
    emit("submit", { action: "disconnect" });
  }
};

const formatDate = (dateString) => {
  if (!dateString) return __("Chưa bao giờ");
  return new Date(dateString).toLocaleString("vi-VN");
};

// Lifecycle
onMounted(() => {
  if (props.isEdit && props.existingConnection) {
    // Populate form with existing data
    Object.assign(formData, {
      tenant_name: props.existingConnection.tenant_name || window.location.origin,
      user_email: props.existingConnection.user_email || "",
      full_name: props.existingConnection.full_name || "",
      hook_url: props.existingConnection.hook_url || defaultHookUrl.value,
      redirect_url: props.existingConnection.redirect_url || defaultRedirectUrl.value,
      sync_frequency: props.existingConnection.sync_frequency || "Hourly",
      daily_message_limit: props.existingConnection.daily_message_limit || 1000,
      max_retries: props.existingConnection.max_retries || 3,
      debug_mode: props.existingConnection.debug_mode || false,
      enable_broadcasting: props.existingConnection.enable_broadcasting !== false,
      auto_sync_templates: props.existingConnection.auto_sync_templates !== false,
    });

    loadOAInfo();
    loadMessageTemplates();
  } else {
    // Set defaults for new connection
    formData.hook_url = defaultHookUrl.value;
    formData.redirect_url = defaultRedirectUrl.value;
  }

  // Initialize parent with form data
  emit("update:modelValue", { ...formData });
});

// Watch for changes and emit to parent
import { watch } from "vue";

watch(
  formData,
  (newValue) => {
    emit("update:modelValue", { ...newValue });
  },
  { deep: true }
);

// Watch for parent updates
watch(
  () => props.modelValue,
  (newValue) => {
    if (newValue && Object.keys(newValue).length > 0) {
      Object.assign(formData, newValue);
    }
  },
  { deep: true }
);
</script>

<style scoped>
.zalo-connection-form {
  max-height: 70vh;
  overflow-y: auto;
  padding-right: 8px;
}

/* Custom scrollbar */
.zalo-connection-form::-webkit-scrollbar {
  width: 6px;
}

.zalo-connection-form::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.zalo-connection-form::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.zalo-connection-form::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
