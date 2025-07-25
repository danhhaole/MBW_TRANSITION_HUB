<template>
  <div class="max-w-5xl mx-auto px-4 py-10 space-y-8">
    <h1 class="text-3xl font-bold text-center text-[#b30000]">
      Vì sao chọn MobiWork Việt Nam?
    </h1>

    <div
      v-for="(item, index) in feedItems"
      :key="index"
      class="bg-gradient-to-br from-white via-red-50 to-red-100 p-6 rounded-2xl shadow-xl hover:shadow-2xl transition-shadow duration-300 border border-red-200"
    >
      <div class="flex items-start gap-4">
        <div class="bg-red-500 text-white p-3 rounded-full shadow-lg">
          <FeatherIcon :name="item.icon" class="w-6 h-6" />
        </div>
        <div>
          <h2 class="text-xl font-semibold text-red-800">{{ item.title }}</h2>
          <p class="text-gray-700 mt-2 whitespace-pre-line leading-relaxed">
            {{ item.content }}
          </p>
        </div>
      </div>
    </div>

    <!-- CTA Button -->
    <div class="text-center pt-8">
      <RouterLink :to="`/register?campaign=${campaignId}`">
        <button
          class="bg-gradient-to-r from-red-600 via-red-500 to-red-600 hover:from-red-700 hover:via-red-600 hover:to-red-700 text-white text-lg font-bold px-10 py-4 rounded-full shadow-lg hover:shadow-xl transition-all duration-300"
        >
          🎯 Tham gia ngay cùng MobiWork – Để lại thông tin của bạn
        </button>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { FeatherIcon } from 'frappe-ui'
import { ref, onMounted } from 'vue'

const campaignId = ref('')

// Lấy campaignId từ URL query string
onMounted(() => {
  const params = new URLSearchParams(window.location.search)
  campaignId.value = params.get('campaign') || ''
})

const feedItems = [
  {
    title: 'Môi trường làm việc lý tưởng',
    icon: 'Home',
    content: `Hơn 10 năm phát triển, MobiWork luôn hướng đến việc xây dựng nơi làm việc lý tưởng, nơi nhân viên được lắng nghe, chia sẻ và ghi nhận xứng đáng.`,
  },
  {
    title: 'Lương thưởng cạnh tranh',
    icon: 'BadgeDollarSign',
    content: `- Tiền lương: tương xứng vị trí và năng lực\n- Tăng lương: định kỳ, xét trước hạn với người xuất sắc\n- Thưởng: cuối năm, lễ Tết theo đóng góp`,
  },
  {
    title: 'Phúc lợi hấp dẫn',
    icon: 'HeartHandshake',
    content: `- Thưởng lễ, Tết, tháng 13\n- Hỗ trợ: hiếu hỉ, ốm đau, thai sản\n- Nghỉ mát, thể thao, BHXH - BHYT đầy đủ`,
  },
  {
    title: 'Đào tạo & Phát triển nghề nghiệp',
    icon: 'GraduationCap',
    content: `- Lộ trình nghề nghiệp rõ ràng\n- Đào tạo hội nhập, chuyên môn, kỹ năng\n- Cơ hội phát triển và thăng tiến minh bạch`,
  }
]
</script>
