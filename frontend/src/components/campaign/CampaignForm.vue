<template>
  <v-dialog 
    v-model="dialog" 
    max-width="700px" 
    persistent
    @keydown.esc="handleCancel"
  >
    <v-card>
      <v-card-title class="text-h5 pa-4">
        <v-icon class="mr-2" color="primary">mdi-bullhorn</v-icon>
        {{ isEdit ? 'Chỉnh sửa chiến dịch' : 'Tạo chiến dịch mới' }}
      </v-card-title>

      <v-divider />

      <v-card-text class="pa-6">
        <v-form ref="formRef" v-model="isFormValid" @submit.prevent="handleSubmit">
          <v-row>
            <!-- Tên chiến dịch -->
            <v-col cols="12">
              <v-text-field
                v-model="form.campaign_name"
                label="Tên chiến dịch *"
                :rules="campaignNameRules"
                variant="outlined"
                density="comfortable"
                required
                prepend-inner-icon="mdi-format-title"
                placeholder="Nhập tên chiến dịch"
                counter="200"
                maxlength="200"
              />
            </v-col>

            <!-- Mô tả -->
            <v-col cols="12">
              <v-textarea
                v-model="form.description"
                label="Mô tả"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-text"
                placeholder="Nhập mô tả chi tiết về chiến dịch..."
                rows="3"
                auto-grow
                counter="1000"
                maxlength="1000"
              />
            </v-col>

            <!-- Trạng thái và Loại -->
            <v-col cols="12" md="6">
              <v-select
                v-model="form.status"
                :items="statusOptions"
                label="Trạng thái"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-flag"
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-select
                v-model="form.type"
                :items="typeOptions"
                label="Loại chiến dịch"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-tag"
              />
            </v-col>

            <!-- Kích hoạt -->
            <v-col cols="12" md="6">
              <v-select
                v-model="form.is_active"
                :items="activeOptions"
                label="Trạng thái hoạt động"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-power"
              />
            </v-col>

            <!-- Chủ sở hữu -->
            <v-col cols="12" md="6">
              <v-select
                v-model="form.owner_id"
                :items="users"
                label="Chủ sở hữu"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-account"
                :loading="loadingOptions"
                clearable
                no-data-text="Không có dữ liệu"
              >
                <template #item="{ props, item }">
                  <v-list-item v-bind="props">
                    <template #subtitle>
                      {{ item.raw.subtitle }}
                    </template>
                  </v-list-item>
                </template>
              </v-select>
            </v-col>

            <!-- Phân khúc mục tiêu -->
            <v-col cols="12">
              <v-select
                v-model="form.target_segment"
                :items="talentSegments"
                label="Phân khúc mục tiêu"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-target"
                :loading="loadingOptions"
                clearable
                no-data-text="Không có dữ liệu"
              />
            </v-col>

            <!-- Ngày bắt đầu -->
            <v-col cols="12" md="6">
              <v-text-field
                v-model="form.start_date"
                label="Ngày bắt đầu"
                type="date"
                variant="outlined"
                density="comfortable"
                :rules="dateRules"
                prepend-inner-icon="mdi-calendar-start"
              />
            </v-col>

            <!-- Ngày kết thúc -->
            <v-col cols="12" md="6">
              <v-text-field
                v-model="form.end_date"
                label="Ngày kết thúc"
                type="date"
                variant="outlined"
                density="comfortable"
                :rules="endDateRules"
                prepend-inner-icon="mdi-calendar-end"
              />
            </v-col>
          </v-row>

          <!-- Thông báo lỗi -->
          <v-alert
            v-if="error"
            type="error"
            variant="tonal"
            class="mt-4"
            :text="error"
            closable
            @click:close="error = null"
          />

          <!-- Thông báo thành công -->
          <v-alert
            v-if="success"
            type="success"
            variant="tonal"
            class="mt-4"
            text="Thao tác thành công!"
          />
        </v-form>
      </v-card-text>

      <v-divider />

      <v-card-actions class="pa-4">
        <v-spacer />
        
        <v-btn
          variant="outlined"
          color="grey"
          @click="handleCancel"
          :disabled="loading"
        >
          Hủy bỏ
        </v-btn>

        <v-btn
          variant="flat"
          color="primary"
          :loading="loading"
          :disabled="!isFormValid || loading"
          @click="handleSubmit"
          class="ml-2"
        >
          <v-icon class="mr-2">mdi-content-save</v-icon>
          {{ isEdit ? 'Cập nhật' : 'Tạo mới' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useCampaignForm, useCampaignCRUD } from '@/composables/useCampaign.js'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  campaign: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'success', 'cancel'])

// Refs
const formRef = ref()
const isFormValid = ref(false)

// Computed
const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const isEdit = computed(() => !!props.campaign)

// Composables
const {
  form,
  users,
  talentSegments,
  loadingOptions,
  campaignNameRules,
  dateRules,
  endDateRules,
  typeOptions,
  statusOptions,
  activeOptions,
  loadOptions,
  validateForm,
  resetForm,
  setFormData
} = useCampaignForm()

const {
  loading,
  error,
  success,
  createCampaign,
  updateCampaign,
  resetState
} = useCampaignCRUD()

// Watch for campaign changes (edit mode)
watch(() => props.campaign, (newCampaign) => {
  if (newCampaign) {
    setFormData(newCampaign)
  } else {
    resetForm()
  }
}, { immediate: true })

// Watch dialog open/close
watch(dialog, (isOpen) => {
  if (isOpen) {
    resetState()
    loadOptions() // Load users and talent segments
    if (props.campaign) {
      setFormData(props.campaign)
    } else {
      resetForm()
    }
  }
})

// Methods
const handleSubmit = async () => {
  if (!formRef.value) return
  
  const { valid } = await formRef.value.validate()
  if (!valid) return

  let result = false
  
  if (isEdit.value) {
    result = await updateCampaign(props.campaign.name, form.value)
  } else {
    result = await createCampaign(form.value)
  }

  if (result) {
    emit('success', {
      action: isEdit.value ? 'update' : 'create',
      data: form.value
    })
    
    // Đóng dialog sau 1 giây để user thấy thông báo success
    setTimeout(() => {
      dialog.value = false
    }, 1000)
  }
}

const handleCancel = () => {
  resetState()
  emit('cancel')
  dialog.value = false
}

// Load options on mount
onMounted(() => {
  loadOptions()
})

// Expose methods for parent component
defineExpose({
  resetForm,
  validateForm
})
</script>

<style scoped>
.v-card-title {
  background-color: rgb(var(--v-theme-surface-variant));
}
</style> 