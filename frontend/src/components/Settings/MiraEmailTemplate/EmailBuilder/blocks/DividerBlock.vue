<template>
  <div 
    :style="{ 
      padding: `${block.props.paddingTop || 20}px ${block.props.paddingRight || 0}px ${block.props.paddingBottom || 20}px ${block.props.paddingLeft || 0}px`,
      backgroundColor: block.props.backgroundColor !== 'transparent' ? block.props.backgroundColor : undefined,
      display: 'flex',
      justifyContent: getAlignmentStyle()
    }"
    class="divider-block-wrapper"
  >
    <div 
      :style="{
        height: (block.props.height || 4) + 'px',
        backgroundColor: getDividerBackgroundColor(),
        border: getDividerBorder(),
        width: getDividerWidth()
      }" 
      class="divider-line"
    ></div>
  </div>
</template>

<script setup>
const props = defineProps({
  block: {
    type: Object,
    required: true
  }
})

// Get divider background color (for solid style)
function getDividerBackgroundColor() {
  const style = props.block.props.style || 'solid'
  const color = props.block.props.borderColor || '#e5e7eb'
  
  if (style === 'solid') {
    return color // Use backgroundColor for solid
  }
  
  return 'transparent' // No background for dashed/dotted
}

// Get divider border (for dashed/dotted styles)
function getDividerBorder() {
  const style = props.block.props.style || 'solid'
  const color = props.block.props.borderColor || '#e5e7eb'
  const height = props.block.props.height || 4
  
  if (style === 'solid') {
    return 'none' // No border for solid
  }
  
  return `${height}px ${style} ${color}`
}

// Get divider width
function getDividerWidth() {
  if (props.block.props.width === 'custom') {
    return (props.block.props.customWidth || 300) + 'px'
  }
  return props.block.props.width || '100%'
}

// Get alignment style for flexbox
function getAlignmentStyle() {
  switch (props.block.props.align) {
    case 'left':
      return 'flex-start'
    case 'right':
      return 'flex-end'
    case 'center':
    default:
      return 'center'
  }
}
</script>

<style scoped>
.divider-block-wrapper {
  min-height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.divider-line {
  flex-shrink: 0;
}
</style>
