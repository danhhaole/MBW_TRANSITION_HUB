<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="$emit('close')"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
              <FeatherIcon name="alert-triangle" class="h-6 w-6 text-red-600" />
            </div>
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                {{ title }}
              </h3>
              <div class="mt-2">
                <p class="text-sm text-gray-500">
                  {{ message }}
                </p>
              </div>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <Button
            variant="solid"
            theme="red"
            @click="$emit('confirm')"
            :loading="loading"
            class="w-full sm:w-auto sm:ml-3"
          >
            Xóa
          </Button>
          <Button
            variant="outline"
            theme="gray"
            @click="$emit('close')"
            class="mt-3 w-full sm:mt-0 sm:w-auto"
          >
            Hủy
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Button, FeatherIcon } from 'frappe-ui'

// Props
defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Xác nhận xóa'
  },
  message: {
    type: String,
    default: 'Bạn có chắc chắn muốn xóa? Hành động này không thể hoàn tác.'
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Emits
defineEmits(['close', 'confirm'])
</script>
