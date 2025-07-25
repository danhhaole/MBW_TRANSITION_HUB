<template>
  <Card class="max-w-xl mx-auto mt-10 p-6">
    <template #title>
      Đăng ký ứng tuyển
    </template>

    <form @submit.prevent="submit">
      <div class="space-y-4">
        <Input v-model="form.full_name" label="Họ tên" required />
        <Input v-model="form.email" label="Email" type="email" required />
        <Input v-model="form.phone" label="Số điện thoại" />
        <Input v-model="form.dob" label="Ngày sinh" type="date" />
        <Input v-model="form.headline" label="Tiêu đề hồ sơ" />

        <div v-if="campaignDetails.skills && campaignDetails.skills.length">
          <label class="block font-medium mb-1">Chọn kỹ năng từ campaign</label>
          <div class="flex flex-wrap gap-2">
            <Button
              v-for="skill in campaignDetails.skills"
              :key="'c-' + skill"
              :variant="form.skills.includes(skill) ? 'default' : 'outline'"
              @click.prevent="toggleSkill(skill)"
              size="sm"
            >
              {{ skill }}
            </Button>
          </div>
        </div>

        <div v-if="campaignDetails.segment_skills && campaignDetails.segment_skills.length">
          <label class="block font-medium mt-4 mb-1">Chọn kỹ năng từ phân khúc</label>
          <div class="flex flex-wrap gap-2">
            <Button
              v-for="skill in campaignDetails.segment_skills"
              :key="'s-' + skill"
              :variant="form.skills.includes(skill) ? 'default' : 'outline'"
              @click.prevent="toggleSkill(skill)"
              size="sm"
            >
              {{ skill }}
            </Button>
          </div>
        </div>

        <Input v-model="form.cv_original_url" label="Link CV" placeholder="https://..." />
        <Textarea v-model="form.ai_summary" label="Giới thiệu bản thân" />
      </div>

      <div class="mt-6">
        <Button type="submit" :loading="resource.loading">
          Gửi thông tin
        </Button>
      </div>
    </form>
  </Card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Card, Input, Textarea, Button,  createResource, call } from 'frappe-ui'

const form = ref({
  full_name: '',
  email: '',
  phone: '',
  dob: '',
  headline: '',
  skills: [],
  cv_original_url: '',
  ai_summary: '',
  campaign: ''
})

const campaignDetails = ref({ skills: [], segment_skills: [] })

onMounted(async () => {
  const params = new URLSearchParams(window.location.search)
  form.value.campaign = params.get('campaign') || ''

  if (form.value.campaign) {
    const res = await call('mbw_mira.api.get_campaign_details_for_submit', { campaign_id: form.value.campaign })
    const data = res.message || {}

    campaignDetails.value.skills = data.skills || []

    if (Array.isArray(data.segments)) {
      const segmentSkills = data.segments.flatMap(seg =>
        seg.criteria?.skills || []
      )
      campaignDetails.value.segment_skills = [...new Set(segmentSkills)]
    }
  }
})

const resource = createResource({
  url: 'mbw_mira.api.submit_talent_profile',
  method: 'POST',
  auto: false,
  onSuccess(data) {
    // showToast({ title: 'Thành công', text: 'Thông tin đã được gửi!', type: 'success' })
  },
  onError(error) {
    // showToast({ title: 'Lỗi', text: error.message || 'Gửi thông tin thất bại', type: 'error' })
  }
})

function toggleSkill(skill) {
  const i = form.value.skills.indexOf(skill)
  if (i >= 0) {
    form.value.skills.splice(i, 1)
  } else {
    form.value.skills.push(skill)
  }
}

function submit() {
  const payload = {
    ...form.value
  }
  resource.submit(payload)
}
</script>
