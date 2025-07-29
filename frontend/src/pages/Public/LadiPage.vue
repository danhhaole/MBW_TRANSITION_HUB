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


</style>