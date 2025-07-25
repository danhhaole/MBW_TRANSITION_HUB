<template>
    <div v-if="visible" class="table-loading">
        <div class="spinner"></div>
        <span v-if="text" class="text-gray-500">{{ __(text) }}</span>
    </div>
</template>

<script setup>
defineProps({
    visible: {
        type: Boolean,
        default: true
    },
    text: {
        type: String,
        default: 'Loading...'
    }
})
</script>

<style scoped>
.table-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    color: #6b7280;
    font-size: 0.875rem;
}

.spinner {
    width: 32px;
    height: 32px;
    border: 3px solid #f3f4f6;
    border-top: 3px solid #6b7280;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 0.75rem;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}
</style>