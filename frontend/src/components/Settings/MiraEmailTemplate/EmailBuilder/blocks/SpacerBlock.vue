<template>
  <div 
    class="spacer-block"
    :style="{ 
      height: block.props.height + 'px',
      backgroundColor: block.props.backgroundColor !== 'transparent' ? block.props.backgroundColor : undefined
    }"
  >
    <div class="spacer-content">
      <div class="spacer-line"></div>
      <span class="spacer-label">Spacer ({{ block.props.height }}px)</span>
      <div class="spacer-line"></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  block: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.spacer-block {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 20px;
}

.spacer-content {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0 20px;
}

.spacer-line {
  flex: 1;
  height: 0;
  border-top: 2px dotted #cbd5e1;
}

.spacer-label {
  padding: 0 12px;
  font-size: 11px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  white-space: nowrap;
}
</style>
