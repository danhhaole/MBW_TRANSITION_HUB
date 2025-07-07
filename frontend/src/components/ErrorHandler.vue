<template>
  <v-snackbar
    v-model="show"
    :color="error.needsRefresh ? 'warning' : 'error'"
    :timeout="error.needsRefresh ? 10000 : 5000"
    top
    multi-line
  >
    <div class="d-flex align-center">
      <v-icon left>
        {{ error.needsRefresh ? 'mdi-refresh' : 'mdi-alert-circle' }}
      </v-icon>
      <div>
        <div class="font-weight-medium mb-1">
          {{ error.needsRefresh ? 'Lỗi Bảo Mật' : 'Có Lỗi Xảy Ra' }}
        </div>
        <div class="text-caption">
          {{ error.message }}
        </div>
      </div>
    </div>
    
    <template #action>
      <v-btn
        v-if="error.needsRefresh"
        color="white"
        text
        @click="handleRefresh"
      >
        Refresh
      </v-btn>
      <v-btn
        color="white"
        icon
        @click="show = false"
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  error: {
    type: Object,
    default: () => ({})
  },
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'refresh'])

const show = ref(false)

watch(() => props.modelValue, (newVal) => {
  show.value = newVal
})

watch(show, (newVal) => {
  emit('update:modelValue', newVal)
})

const handleRefresh = () => {
  emit('refresh')
  window.location.reload()
}
</script>

<style scoped>
.v-snackbar {
  max-width: 400px;
}
</style> 