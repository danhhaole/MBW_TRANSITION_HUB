<template>
  <div v-if="loading" class="flex justify-center items-center min-h-screen text-gray-500 text-xl">
    {{ __('Loading content...') }}
  </div>

  <div v-else-if="pageData" class="ladi-page-container">
    <!-- Render only content, not full HTML document -->
    <div v-html="pageData.content" class="ladi-page-content"></div>
  </div>

  <div v-else class="flex justify-center items-center min-h-screen">
    <div class="text-center p-6">
      <div class="text-red-500 text-xl mb-4">{{ __('Page not found') }}</div>
      <p class="text-gray-600">{{ __('The requested page could not be found.') }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { call } from 'frappe-ui'

const pageData = ref(null)
const loading = ref(true)
const route = useRoute()

// Function to safely inject CSS without conflicts
function injectStyleToHead(cssContent) {
  const id = 'ladi-style'
  const oldStyle = document.getElementById(id)
  if (oldStyle) oldStyle.remove()

  if (cssContent) {
    // Clean and sanitize CSS
    const sanitizedCSS = sanitizeCSS(cssContent)
    const styleEl = document.createElement('style')
    styleEl.setAttribute('id', id)
    styleEl.innerHTML = sanitizedCSS
    document.head.appendChild(styleEl)
  }
}

// Function to sanitize CSS and prevent conflicts
function sanitizeCSS(css) {
  // Remove any potential conflicts with existing styles
  let sanitized = css
  
  // Add scoping to prevent global conflicts
  sanitized = sanitized.replace(/body\s*{/g, '.ladi-page-content {')
  sanitized = sanitized.replace(/html\s*{/g, '.ladi-page-content {')
  
  // Ensure navbar styles are preserved
  sanitized += `
    /* Ensure navbar functionality */
    .ladi-page-content nav,
    .ladi-page-content header {
      position: relative !important;
      width: 100% !important;
      z-index: 1000 !important;
    }
  `
  
  return sanitized
}

// Function to extract and clean HTML content
function extractCleanHTML(htmlString) {
  if (!htmlString) return ''
  
  // If it's a full HTML document, extract only body content
  const bodyMatch = htmlString.match(/<body[^>]*>([\s\S]*?)<\/body>/i)
  if (bodyMatch) {
    return bodyMatch[1]
  }
  
  // If it contains DOCTYPE, extract everything after head
  const docMatch = htmlString.match(/<!DOCTYPE[^>]*>[\s\S]*?<\/head>\s*([\s\S]*?)(?:<\/html>)?$/i)
  if (docMatch) {
    return docMatch[1].replace(/<\/?body[^>]*>/gi, '')
  }
  
  // Otherwise return as is
  return htmlString
}

// Function to extract CSS from HTML
function extractCSS(htmlString) {
  if (!htmlString) return ''
  
  const cssMatches = htmlString.match(/<style[^>]*>([\s\S]*?)<\/style>/gi)
  if (cssMatches) {
    return cssMatches
      .map(match => match.replace(/<\/?style[^>]*>/gi, ''))
      .join('\n')
  }
  
  return ''
}

// Cleanup function
function cleanup() {
  const styleEl = document.getElementById('ladi-style')
  if (styleEl) {
    styleEl.remove()
  }
}

onMounted(async () => {
  try {
    const slug = route.params.slug || 'default-slug'
    console.log('Loading page with slug:', slug)
    
    const res = await call('mbw_mira.api.get_landing_page_html', { slug })
    
    // Debug response structure
    console.log('API Response:', res)
    
    if (res && (res.html || res.content)) {
      const rawHTML = res.content || res.html || ''
      
      // Extract CSS from HTML if not provided separately
      let cssContent = res.css || extractCSS(rawHTML)
      
      // Extract clean HTML content
      const cleanHTML = extractCleanHTML(rawHTML)
      
      console.log('Processed data:', {
        hasCSS: !!cssContent,
        hasHTML: !!cleanHTML,
        htmlLength: cleanHTML.length
      })

      pageData.value = {
        title: res.title || 'Ladi Page',
        content: cleanHTML,
        css: cssContent
      }
      
      // Wait for DOM update then inject CSS
      await nextTick()
      
      if (cssContent) {
        console.log('Injecting CSS to head')
        injectStyleToHead(cssContent)
      }
      
      // Additional DOM fixes after render
      await nextTick()
      fixNavbarAfterRender()
      
    } else {
      console.log('No page data found for slug:', slug)
      pageData.value = null
    }

  } catch (err) {
    console.error('Error loading Landing Page:', err)
    console.error('Error details:', err.message)
    pageData.value = null
  } finally {
    loading.value = false
  }
})

// Function to fix navbar issues after render
function fixNavbarAfterRender() {
  setTimeout(() => {
    const container = document.querySelector('.ladi-page-content')
    if (!container) return
    
    // Fix navbar layout issues
    const navElements = container.querySelectorAll('nav, header')
    navElements.forEach(nav => {
      // Ensure proper flex layout
      const style = window.getComputedStyle(nav)
      if (style.display !== 'flex') {
        nav.style.display = 'flex'
        nav.style.alignItems = 'center'
        nav.style.justifyContent = 'space-between'
      }
      
      // Fix navigation links
      const navLinks = nav.querySelector('.nav-links, ul')
      if (navLinks) {
        navLinks.style.display = 'flex'
        navLinks.style.listStyle = 'none'
        navLinks.style.gap = '1rem'
        navLinks.style.alignItems = 'center'
        navLinks.style.margin = '0'
        navLinks.style.padding = '0'
      }
    })
    
    console.log('Navbar fixes applied')
  }, 100)
}

// Cleanup on unmount
onUnmounted(() => {
  cleanup()
})
</script>

<style scoped>
.ladi-page-container {
  width: 100%;
  min-height: 100vh;
  background: white;
  position: relative;
}

.ladi-page-content {
  width: 100%;
  min-height: 100vh;
  position: relative;
}

/* Critical navbar fixes */
.ladi-page-content :deep(header),
.ladi-page-content :deep(nav) {
  position: relative !important;
  width: 100% !important;
  z-index: 1000 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  flex-wrap: wrap !important;
  padding: 1rem 2rem !important;
  box-sizing: border-box !important;
}

/* Logo fixes */
.ladi-page-content :deep(.logo) {
  display: flex !important;
  align-items: center !important;
  gap: 0.5rem !important;
  font-size: 1.5rem !important;
  font-weight: bold !important;
  color: inherit !important;
  text-decoration: none !important;
  flex-shrink: 0 !important;
}

/* Navigation links container */
.ladi-page-content :deep(.nav-links),
.ladi-page-content :deep(nav ul),
.ladi-page-content :deep(header ul) {
  display: flex !important;
  list-style: none !important;
  gap: 1rem !important;
  align-items: center !important;
  margin: 0 !important;
  padding: 0 !important;
  flex-wrap: wrap !important;
}

/* Individual navigation items */
.ladi-page-content :deep(.nav-links li),
.ladi-page-content :deep(nav ul li),
.ladi-page-content :deep(header ul li) {
  display: flex !important;
  align-items: center !important;
}

/* Navigation links */
.ladi-page-content :deep(.nav-links a),
.ladi-page-content :deep(nav a),
.ladi-page-content :deep(header a) {
  color: inherit !important;
  text-decoration: none !important;
  font-weight: 500 !important;
  padding: 0.5rem 1rem !important;
  border-radius: 0.5rem !important;
  transition: all 0.3s ease !important;
  white-space: nowrap !important;
}

/* Button styles in navbar */
.ladi-page-content :deep(.nav-cta),
.ladi-page-content :deep(.get-started-btn),
.ladi-page-content :deep(nav .btn),
.ladi-page-content :deep(header .btn) {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.5rem !important;
  padding: 0.75rem 1.5rem !important;
  border-radius: 50px !important;
  font-weight: 600 !important;
  text-decoration: none !important;
  transition: all 0.3s ease !important;
  border: none !important;
  cursor: pointer !important;
}

/* Responsive images */
.ladi-page-content :deep(img) {
  max-width: 100% !important;
  height: auto !important;
  display: block !important;
}

/* Container fixes */
.ladi-page-content :deep(.container) {
  width: 100% !important;
  max-width: 1200px !important;
  margin: 0 auto !important;
  padding: 0 1rem !important;
  box-sizing: border-box !important;
}

/* Section spacing */
.ladi-page-content :deep(section) {
  width: 100% !important;
  box-sizing: border-box !important;
}

/* Prevent overflow issues */
.ladi-page-content :deep(*) {
  box-sizing: border-box !important;
}

/* Mobile responsive fixes */
@media (max-width: 768px) {
  .ladi-page-content :deep(header),
  .ladi-page-content :deep(nav) {
    padding: 1rem !important;
    flex-direction: column !important;
    gap: 1rem !important;
  }
  
  .ladi-page-content :deep(.nav-links),
  .ladi-page-content :deep(nav ul),
  .ladi-page-content :deep(header ul) {
    width: 100% !important;
    justify-content: center !important;
    flex-wrap: wrap !important;
    gap: 0.5rem !important;
  }
  
  .ladi-page-content :deep(.container) {
    padding: 0 0.5rem !important;
  }
  
  .ladi-page-content :deep(.logo) {
    margin-bottom: 0.5rem !important;
  }
}

/* Fix for fixed/sticky headers */
.ladi-page-content :deep(header[style*="fixed"]),
.ladi-page-content :deep(nav[style*="fixed"]),
.ladi-page-content :deep(.fixed) {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  width: 100% !important;
  z-index: 1000 !important;
}

/* Ensure proper text rendering */
.ladi-page-content :deep(h1),
.ladi-page-content :deep(h2),
.ladi-page-content :deep(h3),
.ladi-page-content :deep(h4),
.ladi-page-content :deep(h5),
.ladi-page-content :deep(h6) {
  line-height: 1.2 !important;
  margin-bottom: 1rem !important;
}

.ladi-page-content :deep(p) {
  line-height: 1.6 !important;
  margin-bottom: 1rem !important;
}

/* Animation preservation */
.ladi-page-content :deep([class*="animate"]),
.ladi-page-content :deep([style*="animation"]) {
  animation-play-state: running !important;
}

/* Gradient text fixes */
.ladi-page-content :deep([style*="background-clip: text"]) {
  -webkit-background-clip: text !important;
  background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
}

/* Flexbox layout preservation */
.ladi-page-content :deep(.hero-buttons),
.ladi-page-content :deep(.buttons),
.ladi-page-content :deep([class*="btn-group"]) {
  display: flex !important;
  gap: 1rem !important;
  flex-wrap: wrap !important;
  justify-content: center !important;
  align-items: center !important;
}
</style>