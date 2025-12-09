<template>
  <div
    :style="{
      padding: `${block.props.paddingTop || 8}px ${block.props.paddingRight || 16}px ${block.props.paddingBottom || 8}px ${block.props.paddingLeft || 16}px`,
      backgroundColor: block.props.backgroundColor !== 'transparent' ? block.props.backgroundColor : undefined,
      height: block.props.height ? block.props.height + 'px' : undefined
    }"
    class="text-block-wrapper"
  >
    <component
      :is="getTextElement()"
      :style="{
        fontSize: block.props.fontSize + 'px',
        color: block.props.color,
        lineHeight: block.props.lineHeight || '1.4',
        fontFamily: block.props.fontFamily || 'Arial, sans-serif',
        fontStyle: block.props.fontStyle || 'normal',
        fontWeight: block.props.fontWeight || 'normal',
        textDecoration: block.props.textDecoration || 'none',
        letterSpacing: block.props.letterSpacing ? block.props.letterSpacing + 'px' : '0px',
        textAlign: block.props.textAlign || 'left',
        margin: 0,
        whiteSpace: 'pre-wrap'

      }"
      class="text-block-content"
    >
      {{ block.props.content }}
    </component>
  </div>
</template>

<script setup>
const props = defineProps({
  block: {
    type: Object,
    required: true
  }
})

// Get appropriate HTML element based on text type
function getTextElement() {
  switch (props.block.props.textType) {
    case 'h1':
      return 'h1'
    case 'h2':
      return 'h2'
    case 'h3':
      return 'h3'
    case 'paragraph':
    default:
      return 'p'
  }
}
</script>

<style scoped>
.text-block-wrapper {
  min-height: 40px;
}

.text-block-content {
  border: 1px dashed #e5e7eb;
  padding: 8px;
  border-radius: 4px;
  min-height: 30px;
  background: #fafafa;
}

.text-block-content:empty::before {
  content: 'Enter your text here...';
  color: #9ca3af;
}
</style>
