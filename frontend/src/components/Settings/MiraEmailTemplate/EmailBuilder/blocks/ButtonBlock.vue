<template>
  <div 
    :style="{ 
      padding: `${block.props.paddingTop || 12}px ${block.props.paddingRight || 24}px ${block.props.paddingBottom || 12}px ${block.props.paddingLeft || 24}px`,
      'text-align': block.props.align || 'center',
      height: block.props.height ? block.props.height + 'px' : undefined,
      display: 'block'
    }"
    class="button-block-wrapper"
  >
    <a
      :href="block.props.href"
      :style="{
        backgroundColor: block.props.backgroundColor || '#3b82f6',
        color: block.props.color || '#ffffff',
        padding: '12px 24px',
        textDecoration: 'none',
        borderRadius: (block.props.borderRadius || 4) + 'px',
        display: 'inline-block',
        fontFamily: block.props.fontFamily || 'Arial, sans-serif',
        fontSize: (block.props.fontSize || 16) + 'px',
        fontWeight: block.props.fontWeight || 'normal',
        letterSpacing: block.props.letterSpacing ? block.props.letterSpacing + 'px' : '0px',
        width: getButtonWidth(),
        border: getBorderStyle(),
        cursor: 'pointer',
        transition: 'all 0.2s ease'
      }"
      class="button-element"
    >
      {{ block.props.text }}
    </a>
  </div>
</template>

<script setup>
const props = defineProps({
  block: {
    type: Object,
    required: true
  }
})

// Get button width based on width setting
function getButtonWidth() {
  switch (props.block.props.width) {
    case '100%':
      return '100%'
    case 'custom':
      return props.block.props.customWidth ? props.block.props.customWidth + 'px' : 'auto'
    case 'auto':
    default:
      return 'auto'
  }
}

// Get border style
function getBorderStyle() {
  if (!props.block.props.hasBorder) {
    return 'none'
  }
  
  const width = props.block.props.borderWidth || 1
  const color = props.block.props.borderColor || '#000000'
  
  return `${width}px solid ${color}`
}
</script>

<style scoped>
.button-block-wrapper {
  min-height: 40px;
  width: 100%;
}

.button-element {
  transition: all 0.2s ease;
}

.button-element:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}
</style>
