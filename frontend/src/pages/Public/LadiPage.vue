<template>
  <div v-if="loading" class="flex justify-center items-center min-h-screen text-gray-500 text-xl">
    Đang tải nội dung...
  </div>

  <div v-else-if="html" v-html="html" class="ladi-page-content"></div>

  <div v-else class="text-center p-6 text-red-500">
    Không tìm thấy nội dung Landing Page.
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { call } from 'frappe-ui'

const html = ref('')
const css = ref('')
const loading = ref(true)

const route = useRoute()

function injectStyleToHead(cssContent) {
  const id = 'ladi-style'
  const oldStyle = document.getElementById(id)
  if (oldStyle) oldStyle.remove()

  const styleEl = document.createElement('style')
  styleEl.setAttribute('id', id)
  styleEl.innerHTML = cssContent
  document.head.appendChild(styleEl)
}

function injectTailwindCDN() {
  const id = 'tailwind-cdn'
  if (!document.getElementById(id)) {
    const script = document.createElement('script')
    script.setAttribute('id', id)
    script.src = 'https://cdn.tailwindcss.com'
    document.head.appendChild(script)
  }
}

onMounted(async () => {
  try {
    const slug = route.params.slug || 'default-slug'
    const res = await call('mbw_mira.api.get_landing_page_html', { slug })

    if (res?.html) {
      console.log(res.html)
      html.value =res.html
    }

    if (res?.css) {
      css.value = res.css
      injectStyleToHead(css.value)
    }

    // Nếu các block cần Tailwind: gọi dòng dưới
    injectTailwindCDN()

  } catch (err) {
    console.error('Lỗi khi tải Landing Page:', err)
    html.value = '<div class="text-red-500">Không tải được nội dung trang.</div>'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.ladi-page-content {
  min-height: 100vh;
  background: white;
}
</style>
