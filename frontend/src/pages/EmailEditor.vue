<template>
    <div class="email-editor-wrapper">
        <EmailEditor ref="editorRef" :appearance="appearance" :min-height="'800px'" :project-id="projectId"
            :locale="locale" :tools="tools" :options="options" @load="onEditorLoad" @ready="onEditorReady" />

        <div class="editor-actions">
            <button @click="saveDesign" class="btn">Save Design</button>
            <button @click="exportHtml" class="btn">Export HTML</button>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { EmailEditor } from 'vue-email-editor';

const editorRef = ref(null);

// Config
const appearance = reactive({ theme: 'light' });
const minHeight = '800px';
const locale = 'en';
const projectId = 0;
const tools = reactive({ image: { enabled: true } });
const options = reactive({});

// Optional: Auto resize iframe on load
function onEditorReady() {
    console.log('Editor Ready');

    const iframe = document.querySelector('iframe');
    if (iframe) {
        iframe.style.height = '800px';       // 👈 fix cứng
        iframe.style.minHeight = '800px';    // 👈 đề phòng unlayer tự resize
        iframe.style.maxHeight = 'none';
        iframe.style.width = '100%';
    }
}

function onEditorLoad() {
    console.log('Editor Loaded');
    // editorRef.value.editor.loadDesign(myDesignJson); // nếu cần load sẵn
}

function saveDesign() {
    editorRef.value.editor.saveDesign((design) => {
        console.log('Design JSON:', design);
        // gửi lên server nếu cần
    });
}

function exportHtml() {
    editorRef.value.editor.exportHtml((data) => {
        console.log('Exported HTML:', data.html);
        // render hoặc preview HTML
    });
}
</script>

<style scoped>
.email-editor-wrapper {
    height: 100vh;
    display: flex;
    flex-direction: column;
}

.editor-actions {
    padding: 1rem;
    background-color: #f9f9f9;
    border-top: 1px solid #ccc;
    display: flex;
    gap: 10px;
}

.btn {
    padding: 8px 16px;
    background-color: #3490dc;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.btn:hover {
    background-color: #2779bd;
}
</style>