<template>
  <div class="web-config">
    <v-row>
      <v-col cols="12">
        <v-text-field
          v-model="data.keywords"
          label="Từ khóa tìm kiếm"
          placeholder="Senior Golang Developer Hanoi"
          variant="outlined"
          density="compact"
        />
      </v-col>
    </v-row>
    
    <v-row>
      <v-col cols="12">
        <div class="text-subtitle-2 mb-2">Nguồn thu thập</div>
        <div class="d-flex flex-wrap gap-2">
          <v-checkbox
            v-for="source in webSources"
            :key="source.value"
            v-model="data.sources"
            :value="source.value"
            :label="source.text"
            density="compact"
            hide-details
          />
        </div>
      </v-col>
    </v-row>
    
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="data.maxResults"
          label="Số lượng tối đa"
          type="number"
          placeholder="100"
          variant="outlined"
          density="compact"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-select
          v-model="data.timeRange"
          :items="timeRanges"
          label="Khoảng thời gian"
          variant="outlined"
          density="compact"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

// Props & Emits
const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue'])

// Data
const data = ref({
  keywords: '',
  sources: [],
  maxResults: 100,
  timeRange: '',
  ...props.modelValue
})

// Options
const webSources = [
  { text: 'LinkedIn', value: 'linkedin' },
  { text: 'TopCV', value: 'topcv' },
  { text: 'VietnamWorks', value: 'vietnamworks' },
  { text: 'CareerBuilder', value: 'careerbuilder' },
  { text: 'Indeed', value: 'indeed' },
  { text: 'GitHub', value: 'github' }
]

const timeRanges = [
  { title: 'Tuần qua', value: '7d' },
  { title: 'Tháng qua', value: '30d' },
  { title: '3 tháng qua', value: '90d' },
  { title: '6 tháng qua', value: '180d' },
  { title: 'Năm qua', value: '365d' }
]

// Watch for changes
watch(data, (newData) => {
  emit('update:modelValue', newData)
}, { deep: true })
</script> 