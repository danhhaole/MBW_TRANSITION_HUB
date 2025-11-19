<template>
  <div 
    class="unlayer-editor-container"
    :style="{ height: minHeight, minHeight: minHeight }"
  >
    <EmailEditor 
      ref="editorRef" 
      :appearance="appearance" 
      :min-height="minHeight"
      :project-id="null"
      :locale="locale" 
      :tools="tools" 
      :options="options" 
      @load="onEditorLoad" 
      @ready="onEditorReady" 
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch, nextTick } from 'vue'
import { EmailEditor } from 'vue-email-editor'
import { call } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: [String, Object],
    default: null
  },
  minHeight: {
    type: String,
    default: '500px'
  }
})

const emit = defineEmits(['update:modelValue', 'ready'])

const editorRef = ref(null)

// Config
const appearance = reactive({ 
  theme: 'light',
  panels: {
    tools: {
      dock: 'right'
    }
  }
})
const locale = 'en'
const tools = reactive({ 
  image: { 
    enabled: true,
    properties: {
      src: {
        value: {
          url: '',
          // Don't use default Unlayer storage
          autoWidth: false,
          width: '100%'
        }
      }
    }
  },
  video: { enabled: true },
  button: { enabled: true }
})
const options = reactive({
  features: {
    textEditor: {
      spellChecker: true
    },
    // Disable stock file storage to force custom upload
    stockImages: {
      enabled: false
    },
    // Disable default image upload (S3)
    imageEditor: {
      enabled: true
    },
     fileUpload: {
      enabled: false
    }
  },
  displayMode: 'email',
  safeHtml: false,
  // Force custom file upload
  customJS: [],
  // Disable project settings that might include S3 config
  projectId: null,
  // Important: This tells Unlayer to use custom callback
  fileUpload: {
    enabled: false  // Disable built-in S3 upload
  }
})

// Track if callback is registered
let callbackRegistered = false

function onEditorLoad() {
  console.log('📦 [Unlayer] Editor Loaded (instance created)')
  
  // CRITICAL: Register callback immediately - BEFORE editor is fully ready
  // This ensures our callback is registered before any S3 config is loaded
  const editor = editorRef.value?.editor
  console.log('🎯 [Unlayer] Editor instance on load:', editor)
  
  if (editor) {
    // Check available methods
    console.log('🔍 [Unlayer] Has registerCallback?', typeof editor.registerCallback)
    console.log('🔍 [Unlayer] Has registerProvider?', typeof editor.registerProvider)
    console.log('📋 [Unlayer] Available methods:', Object.keys(editor).filter(k => k.includes('register') || k.includes('upload')))
    
    // CRITICAL: Try ALL provider types to see which one works
    if (editor.registerProvider && !callbackRegistered) {
      console.log('🔧 [Unlayer] Registering providers for ALL file types...')
      
      // Register for 'image' type
      registerImageUploadProvider(editor, 'image')
      
      // Also try 'file' type (might be what Unlayer uses)
      registerImageUploadProvider(editor, 'file')
      
      // And try callback as backup
      if (editor.registerCallback) {
        registerImageUploadCallback(editor)
      }
      
      callbackRegistered = true
    }
    // Fallback to registerCallback only
    else if (editor.registerCallback && !callbackRegistered) {
      console.log('🔧 [Unlayer] Using registerCallback (legacy API)')
      registerImageUploadCallback(editor)
      callbackRegistered = true
    }
  }
}

// Register image upload callback - EXACT format from Unlayer docs
function registerImageUploadCallback(editor) {
  if (!editor || !editor.registerCallback) {
    console.warn('⚠️ [Unlayer] Cannot register callback - method not available')
    return
  }
  
  console.log('🔧 [Unlayer] Registering custom image upload callback...')
  
  // EXACT format from docs: https://docs.unlayer.com/docs/custom-file-storage
  editor.registerCallback('file', function(file, done) {
    console.log('📸 [Unlayer] ============================================')
    console.log('📸 [Unlayer] IMAGE CALLBACK TRIGGERED!')
    console.log('📸 [Unlayer] File:', file)
    console.log('📸 [Unlayer] ============================================')
    
    var imageFile = file.attachments[0]
    
    // Read file as base64
    var reader = new FileReader()
    reader.onload = function(e) {
      var fileContent = e.target.result.split(',')[1] // Get base64 part
      
      console.log('📤 [Unlayer] Uploading with frappe-ui call...')
      
      // Use frappe-ui call method
      call('mbw_mira.api.file_upload.upload_email_image_base64', {
        filename: imageFile.name,
        content: fileContent
      })
      .then((response) => {
        console.log('📦 [Unlayer] Response:', response)
        
        // Get file URL from response
        var fileUrl = response.file_url
        
        console.log('✅ [Unlayer] Uploaded to:', fileUrl)
        
        // Pass URL back to Unlayer
        done({ progress: 100, url: fileUrl })
      })
      .catch((error) => {
        console.error('❌ [Unlayer] Upload failed:', error)
        alert('Failed to upload image: ' + error.message)
      })
    }
    
    reader.onerror = function(error) {
      console.error('❌ [Unlayer] File read error:', error)
      alert('Failed to read file')
    }
    
    reader.readAsDataURL(imageFile)
  })

  console.log('Editor object:', editor?.registerCallback);
  
  console.log('✅ [Unlayer] Custom image upload callback registered successfully!')
  
  // Verify callback was registered by checking editor internals (if available)
  if (editor._callbacks && editor._callbacks.image) {
    console.log('✅✅ [Unlayer] Confirmed: image callback exists in editor._callbacks')
  } else {
    console.log('⚠️ [Unlayer] Warning: Cannot verify callback registration')
  }
  
  // Also register selectImage callback (for URL-based image picker)
  editor.registerCallback('selectImage', function(data, done) {
    console.log('🖼️ [Unlayer] selectImage callback triggered (URL picker)')
    // Cancel for now - can implement file browser later
    done({ url: '' })
  })
  
  console.log('ℹ️ [Unlayer] Images will now upload to Frappe file storage instead of S3')
  console.log('🧪 [Unlayer] Try uploading an image now to test the custom callback')
}

// NEW: registerProvider API (if available)
function registerImageUploadProvider(editor, providerType = 'image') {
  if (!editor || !editor.registerProvider) {
    console.warn('⚠️ [Unlayer] registerProvider not available')
    return
  }
  
  console.log(`🔧 [Unlayer] Registering PROVIDER for type: "${providerType}"...`)
  
  editor.registerProvider(providerType, {
    upload: function(file, done) {
      console.log('📸 [Unlayer] ============================================')
      console.log(`📸 [Unlayer] PROVIDER UPLOAD TRIGGERED! (type: ${providerType})`)
      console.log('📸 [Unlayer] File:', file)
      console.log('📸 [Unlayer] ============================================')
      
      // Read file as base64
      const reader = new FileReader()
      reader.onload = function(e) {
        const fileContent = e.target.result.split(',')[1]
        
        console.log('📤 [Unlayer] Uploading to Frappe...')
        
        call('mbw_mira.api.file_upload.upload_email_image_base64', {
          filename: file.name,
          content: fileContent
        })
        .then((response) => {
          console.log('📦 [Unlayer] Response:', response)
          const fileUrl = response.file_url
          console.log('✅ [Unlayer] Uploaded to:', fileUrl)
          done({ progress: 100, url: fileUrl })
        })
        .catch((error) => {
          console.error('❌ [Unlayer] Upload failed:', error)
          done({ progress: 0, error: error.message })
        })
      }
      
      reader.onerror = function(error) {
        console.error('❌ [Unlayer] File read error:', error)
        done({ progress: 0, error: 'Failed to read file' })
      }
      
      reader.readAsDataURL(file)
    }
  })
  
  console.log(`✅ [Unlayer] PROVIDER for "${providerType}" registered successfully!`)
}

function onEditorReady() {
  const editor = editorRef.value?.editor
  
  if (!editor) {
    console.error('[Unlayer] Editor instance not found')
    return
  }
  
  // Load existing design if provided
  if (props.modelValue) {
    // Minimal delay to ensure editor iframe is ready
    setTimeout(() => {
      try {
        const design = typeof props.modelValue === 'string' 
          ? JSON.parse(props.modelValue) 
          : props.modelValue
        
        // Validate it's a proper Unlayer design structure
        if (design && design.body && Array.isArray(design.body.rows)) {
          // Deep clone to remove Vue Proxy and make it serializable
          const plainDesign = JSON.parse(JSON.stringify(design))
          editor.loadDesign(plainDesign)
        }
      } catch (error) {
        console.warn('[Unlayer] Failed to load design:', error.message)
      }
    }, 50) // Minimal delay for iframe readiness
  }
  
  // Emit ready event to parent
  emit('ready', editor)
}

// Export methods for parent component
function saveDesign() {
  return new Promise((resolve, reject) => {
    if (!editorRef.value?.editor) {
      reject(new Error('Editor not ready'))
      return
    }
    
    editorRef.value.editor.saveDesign((design) => {
      emit('update:modelValue', design)
      resolve(design)
    })
  })
}

function exportHtml() {
  return new Promise((resolve, reject) => {
    if (!editorRef.value?.editor) {
      reject(new Error('Editor not ready'))
      return
    }
    
    editorRef.value.editor.exportHtml((data) => {
      resolve({ html: data.html, design: data.design })
    })
  })
}

// Watch for external changes
watch(() => props.modelValue, (newValue, oldValue) => {
  // Only reload if value actually changed and editor is ready
  if (newValue && newValue !== oldValue && editorRef.value?.editor) {
    try {
      const design = typeof newValue === 'string' 
        ? JSON.parse(newValue) 
        : newValue
      
      // Validate it's a proper Unlayer design structure
      if (design && design.body && Array.isArray(design.body.rows)) {
        // Deep clone to remove Vue Proxy
        const plainDesign = JSON.parse(JSON.stringify(design))
        editorRef.value.editor.loadDesign(plainDesign)
      }
    } catch (error) {
      console.warn('[Unlayer] Failed to reload design:', error.message)
    }
  }
})

// Expose methods to parent
defineExpose({
  saveDesign,
  exportHtml,
  editor: editorRef
})
</script>

<style scoped>
.unlayer-editor-container {
  width: 100%;
  position: sticky;
  top: 0;
  z-index: 10;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.unlayer-editor-container :deep(iframe) {
  border: none;
  display: block;
  width: 100% !important;
  height: 100% !important;
}

.unlayer-editor-container :deep(.unlayer-editor) {
  height: 100% !important;
}
</style>
