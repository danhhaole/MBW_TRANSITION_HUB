<template>
  <div v-if="loading" class="flex justify-center items-center min-h-screen text-gray-500 text-xl">
    {{ __('Loading content...') }}
  </div>

  <div v-else-if="pageData" class="ladi-page-container">
    <!-- Inject HTML content with proper styling -->
    <div v-html="fullHtml" class="ladi-page-content"></div>
  </div>

  <div v-else class="flex justify-center items-center min-h-screen">
    <div class="text-center p-6">
      <div class="text-red-500 text-xl mb-4">{{ __('Page not found') }}</div>
      <p class="text-gray-600">{{ __('The requested page could not be found.') }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { call } from 'frappe-ui'

const pageData = ref(null)
const loading = ref(true)

const route = useRoute()

// Computed full HTML with proper structure
const fullHtml = computed(() => {
  if (!pageData.value) return ''
  
  return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>${pageData.value.title || 'Ladi Page'}</title>
      <style>
        ${pageData.value.css || ''}
        
        /* Reset and base styles */
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }
        
        html, body {
          height: 100%;
          width: 100%;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          line-height: 1.6;
          color: #333;
        }
        
        /* Ensure content is properly contained */
        .ladi-page-content {
          width: 100%;
          min-height: 100vh;
          overflow-x: hidden;
          position: relative;
        }
        
        /* Header fixes */
        header, .header, [class*="header"] {
          position: relative !important;
          top: auto !important;
          left: auto !important;
          right: auto !important;
          width: 100% !important;
          z-index: 1000;
        }
        
        /* Footer fixes */
        footer, .footer, [class*="footer"] {
          position: relative !important;
          bottom: auto !important;
          left: auto !important;
          right: auto !important;
          width: 100% !important;
          z-index: 1000;
        }
        
        /* Navigation fixes */
        nav, .nav, [class*="nav"] {
          position: relative !important;
          width: 100% !important;
        }
        
        /* Fixed positioning fixes */
        [style*="position: fixed"] {
          position: relative !important;
        }
        
        /* Absolute positioning fixes */
        [style*="position: absolute"] {
          position: relative !important;
        }
        
        /* Responsive images */
        img {
          max-width: 100%;
          height: auto;
        }
        
        /* Fix for common layout issues */
        .container {
          width: 100%;
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 15px;
        }
        
        /* Flexbox fixes */
        .flex, [class*="flex"] {
          display: flex !important;
        }
        
        /* Grid fixes */
        .grid, [class*="grid"] {
          display: grid !important;
        }
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {
          .container {
            padding: 0 10px;
          }
          
          header, .header, [class*="header"] {
            position: relative !important;
          }
          
          footer, .footer, [class*="footer"] {
            position: relative !important;
          }
        }
        
        /* Ensure proper stacking */
        * {
          z-index: auto;
        }
        
        header, .header, [class*="header"] {
          z-index: 1000 !important;
        }
        
        footer, .footer, [class*="footer"] {
          z-index: 1000 !important;
        }
      </style>
      <script src="https://cdn.tailwindcss.com"><\/script>
    </head>
    <body>
      <div class="ladi-page-content">
        ${pageData.value.content || ''}
      </div>
    </body>
    </html>
  `
})

function injectStyleToHead(cssContent) {
  const id = 'ladi-style'
  const oldStyle = document.getElementById(id)
  if (oldStyle) oldStyle.remove()

  if (cssContent) {
    const styleEl = document.createElement('style')
    styleEl.setAttribute('id', id)
    styleEl.innerHTML = cssContent
    document.head.appendChild(styleEl)
  }
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
    console.log('Loading page with slug:', slug)
    
    const res = await call('mbw_mira.api.get_landing_page_html', { slug })

    if (res && (res.html || res.content)) {
      console.log('Page data loaded:', res)
      pageData.value = {
        title: res.title || 'Ladi Page',
        content: res.content || res.html || '',
        css: res.css || ''
      }
      
      // Inject CSS if available
      if (res.css) {
        injectStyleToHead(res.css)
      }
      
      // Inject Tailwind for custom blocks
      // injectTailwindCDN()
    } else {
      console.log('No page data found for slug:', slug)
      pageData.value = null
    }

  } catch (err) {
    console.error('Error loading Landing Page:', err)
    pageData.value = null
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.ladi-page-container {
  width: 100%;
  min-height: 100vh;
  background: white;
}

.ladi-page-content {
  width: 100%;
  min-height: 100vh;
}

/* Ensure iframe content is properly displayed */
.ladi-page-content :deep(*) {
  max-width: 100%;
}

/* Fix for any overflow issues */
.ladi-page-content :deep(body) {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

/* Header and footer specific fixes */
.ladi-page-content :deep(header),
.ladi-page-content :deep(.header),
.ladi-page-content :deep([class*="header"]) {
  position: relative !important;
  top: auto !important;
  left: auto !important;
  right: auto !important;
  width: 100% !important;
  z-index: 1000 !important;
}

.ladi-page-content :deep(footer),
.ladi-page-content :deep(.footer),
.ladi-page-content :deep([class*="footer"]) {
  position: relative !important;
  bottom: auto !important;
  left: auto !important;
  right: auto !important;
  width: 100% !important;
  z-index: 1000 !important;
}

/* Navigation fixes */
.ladi-page-content :deep(nav),
.ladi-page-content :deep(.nav),
.ladi-page-content :deep([class*="nav"]) {
  position: relative !important;
  width: 100% !important;
}

/* Container fixes */
.ladi-page-content :deep(.container),
.ladi-page-content :deep([class*="container"]) {
  width: 100% !important;
  max-width: 1200px !important;
  margin: 0 auto !important;
  padding: 0 15px !important;
}

/* Wrapper fixes */
.ladi-page-content :deep(.wrapper),
.ladi-page-content :deep([class*="wrapper"]) {
  width: 100% !important;
  position: relative !important;
}

/* Responsive fixes */
@media (max-width: 768px) {
  .ladi-page-content {
    padding: 0;
  }
  
  .ladi-page-content :deep(.container),
  .ladi-page-content :deep([class*="container"]) {
    padding: 0 10px !important;
  }
}
</style>
