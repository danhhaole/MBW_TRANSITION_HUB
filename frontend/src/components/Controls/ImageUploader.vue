<template>
  <FileUploader
    :file-types="image_type"
    class="text-base"
    @success="
      (file) => {
        $emit('upload', file.file_url, file.file)
      }
    "
  >
    <template v-slot="{ progress, uploading, openFileSelector }">
      <div class="flex items-end space-x-1">
        <Button type="button" @click="openFileSelector">
          {{
            uploading
              ? `Uploading ${progress}%`
              : image_url
                ? 'Change'
                : 'Upload'
          }}
        </Button>
        <Button v-if="image_url" type="button" @click="$emit('remove')">Remove</Button>
      </div>
    </template>
  </FileUploader>
</template>
<script setup>
import { FileUploader, Button } from 'frappe-ui'

const prop = defineProps({
  image_url: String,
  image_type: {
    type: String,
    default: 'image/*',
  },
  label: {
    type: String,
    default: '',
  },
})
const emit = defineEmits(['upload', 'remove'])
</script>
