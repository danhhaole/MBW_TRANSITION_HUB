<template>
  <div 
    :style="{ 
      padding: `${block.props.paddingTop || 20}px ${block.props.paddingRight || 20}px ${block.props.paddingBottom || 20}px ${block.props.paddingLeft || 20}px`,
      backgroundColor: block.props.backgroundColor !== 'transparent' ? block.props.backgroundColor : undefined,
      textAlign: block.props.align || 'center'
    }" 
    class="image-block-wrapper"
  >
    <div class="image-container">
      <img 
        :src="block.props.src || getPlaceholderImage()"
        :alt="block.props.alt || 'Image'"
        :style="{
          width: getImageWidth(),
          height: block.props.height ? block.props.height + 'px' : 'auto',
          maxWidth: '100%',
          border: getBorderStyle(),
          borderRadius: (block.props.borderRadius || 0) + 'px',
          display: 'block',
          margin: '0 auto'
        }"
        class="image-element"
      />
    </div>
  </div>
</template>

<script setup>
import { FeatherIcon } from 'frappe-ui'

const props = defineProps({
  block: {
    type: Object,
    required: true
  }
})

// Get image width based on width setting
function getImageWidth() {
  if (props.block.props.widthType === 'fixed') {
    return (props.block.props.width || 600) + 'px'
  }
  return '100%' // Full width
}

// Get border style
function getBorderStyle() {
  if (!props.block.props.hasBorder) {
    return 'none'
  }
  
  const width = props.block.props.borderWidth || 1
  const color = props.block.props.borderColor || '#e5e7eb'
  
  return `${width}px solid ${color}`
}

// Generate placeholder image
function getPlaceholderImage() {
  const width = props.block.props.width || 600
  const height = props.block.props.height || 300
  
  // Create SVG placeholder với icon to hơn
  const svg = `
    <svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="#f3f4f6"/>
      <g transform="translate(${width/2}, ${height/2})">
        <g transform="translate(-80, -60)">
          <rect x="20" y="20" width="120" height="80" fill="#d1d5db" rx="8"/>
          <circle cx="45" cy="45" r="12" fill="#9ca3af"/>
          <polygon points="65,85 85,60 105,70 125,50 140,65 140,100 65,100" fill="#9ca3af"/>
        </g>
      </g>
    </svg>
  `
  
  return `data:image/svg+xml;base64,${btoa(svg)}`
}
</script>

<style scoped>
.image-block-wrapper {
  min-height: 100px;
}

.image-placeholder {
  border: 2px dashed #e5e7eb;
  border-radius: 8px;
  padding: 40px 20px;
  text-align: center;
  background: #fafafa;
  cursor: pointer;
  transition: all 0.2s;
}

.image-placeholder:hover {
  border-color: #3b82f6;
  background: #eff6ff;
}
</style>
