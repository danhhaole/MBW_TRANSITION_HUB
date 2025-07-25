<template>
  <div class="bg-white min-h-screen text-gray-800 font-sans">
    <!-- Hero Section -->
    <section class="bg-[#C4161C] text-white py-24 px-6 text-center">
      <h1 class="text-5xl font-bold mb-6">Chào mừng đến với MBW</h1>
      <p class="text-xl max-w-4xl mx-auto">
        Chúng tôi là đối tác chuyển đổi số toàn diện cho doanh nghiệp và tổ chức giáo dục, mang lại giải pháp công nghệ linh hoạt, dễ sử dụng và hiệu quả cao.
      </p>
      <button
        @click="showModal = true"
        class="mt-8 bg-white text-[#C4161C] px-8 py-4 rounded-full font-semibold hover:bg-gray-100 transition"
      >
        Tôi quan tâm
      </button>
    </section>

    <!-- Về Chúng Tôi -->
    <section class="py-20 px-6 max-w-6xl mx-auto">
      <div class="text-center mb-16">
        <h2 class="text-3xl font-bold text-[#C4161C] mb-4">Chúng tôi là ai?</h2>
        <p class="text-lg text-gray-700">
          MBW là doanh nghiệp công nghệ tập trung vào phát triển phần mềm quản trị và hệ thống giáo dục, được tin tưởng bởi hàng trăm tổ chức trên toàn quốc.
        </p>
      </div>
      <div class="grid md:grid-cols-3 gap-10">
        <div class="text-center">
          <img src="" class="mx-auto h-20 mb-4" />
          <h3 class="text-xl font-semibold mb-2">Sáng tạo và Linh hoạt</h3>
          <p class="text-gray-600">Sản phẩm của chúng tôi liên tục đổi mới để đáp ứng nhu cầu thực tế.</p>
        </div>
        <div class="text-center">
          <img src="" class="mx-auto h-20 mb-4" />
          <h3 class="text-xl font-semibold mb-2">Hỗ trợ tận tâm</h3>
          <p class="text-gray-600">Đội ngũ tư vấn và kỹ thuật luôn đồng hành với khách hàng 24/7.</p>
        </div>
        <div class="text-center">
          <img src="" class="mx-auto h-20 mb-4" />
          <h3 class="text-xl font-semibold mb-2">Khả năng mở rộng</h3>
          <p class="text-gray-600">Hệ thống được thiết kế linh hoạt, dễ tích hợp và mở rộng.</p>
        </div>
      </div>
    </section>

    <!-- Ứng dụng trong Talent Pool -->
    <section class="bg-gray-50 py-20 px-6">
      <div class="max-w-4xl mx-auto text-center">
        <h2 class="text-3xl font-bold text-[#C4161C] mb-4">Talent Pool - Tương lai tuyển dụng chủ động</h2>
        <p class="text-lg text-gray-700 mb-6">
          MBW cung cấp giải pháp quản lý Talent Pool – nơi doanh nghiệp có thể chủ động xây dựng và nuôi dưỡng mối quan hệ với ứng viên tiềm năng, phục vụ cho chiến lược tuyển dụng lâu dài.
        </p>
        <button
          @click="showModal = true"
          class="bg-[#C4161C] text-white px-8 py-3 rounded-full hover:bg-[#a31215] transition"
        >
          Tôi quan tâm Talent Pool
        </button>
      </div>
    </section>

    <!-- Modal Đăng ký thông tin -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg max-w-md w-full p-6 relative">
        <button
          class="absolute top-2 right-2 text-gray-500 hover:text-red-500"
          @click="showModal = false"
        >
          ✕
        </button>
        <h3 class="text-xl font-bold text-[#C4161C] mb-4">Đăng ký nhận thông tin</h3>
        <form @submit.prevent="submitRegister">
          <div class="mb-4 text-left">
            <label class="block text-sm font-medium">Họ và tên</label>
            <input v-model="register.full_name" required class="w-full mt-1 border rounded px-3 py-2" />
          </div>
          <div class="mb-4 text-left">
            <label class="block text-sm font-medium">Email</label>
            <input v-model="register.email" type="email" required class="w-full mt-1 border rounded px-3 py-2" />
          </div>
          <div class="mb-4 text-left">
            <label class="block text-sm font-medium">Số điện thoại</label>
            <input v-model="register.phone" class="w-full mt-1 border rounded px-3 py-2" />
          </div>
          <button
            type="submit"
            class="bg-[#C4161C] text-white px-6 py-2 rounded hover:bg-[#a31215] transition w-full"
          >
            Gửi thông tin
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showModal = ref(false)
const register = ref({
  full_name: '',
  email: '',
  phone: '',
})

function submitRegister() {
  console.log('Dữ liệu gửi:', register.value)
  // TODO: Gửi thông tin đến Frappe server
  showModal.value = false
}
</script>
