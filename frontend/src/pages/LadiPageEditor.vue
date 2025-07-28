<template>
    <div class="h-screen w-full">
        <div ref="editorContainer" class="h-[90vh] border" />
        <div class="p-2">
            <button @click="exportHtml" class="bg-blue-600 text-white px-4 py-2 rounded">Export & Submit</button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import grapesjs from 'grapesjs'
import pluginWebpage from 'grapesjs-preset-webpage';
import pluginExport from 'grapesjs-plugin-export';
import pluginNavbar from 'grapesjs-navbar';
import pluginCustomCode from 'grapesjs-custom-code';
import pluginFlexbox from 'grapesjs-blocks-flexbox';
import pluginForms from 'grapesjs-plugin-forms';
import pluginCountdown from 'grapesjs-component-countdown';
import pluginTabs from 'grapesjs-tabs';
import 'grapesjs/dist/css/grapes.min.css'
import { loadLadiTailwindBlocks } from '@/utils/ladi-style-tailwind-blocks'

const editorContainer = ref(null)
let editor = null

onMounted(() => {
    editor = grapesjs.init({
        container: editorContainer.value,
        plugins: [
            pluginWebpage,
            pluginExport,
            pluginNavbar,
            pluginCustomCode,
            pluginFlexbox,
            pluginForms,
            pluginCountdown,
            pluginTabs
        ],
        pluginsOpts: {
            [pluginWebpage]: {},
            [pluginExport]: {},
            [pluginNavbar]: {},
            [pluginCustomCode]: {},
            [pluginFlexbox]: {},
            [pluginForms]: {},
            [pluginCountdown]: {},
            [pluginTabs]: {}
        }
    });
    // Gọi thủ công sau khi editor load
  editor.on('load', () => {
    loadLadiTailwindBlocks(editor);  // nếu bạn dùng preset custom
  });
});



function exportHtml() {
    const html = editor.getHtml()
    const css = editor.getCss()
    const fullHtml = `
      <html>
        <head>
          <style>${css}</style>
        </head>
        <body>${html}</body>
      </html>
    `

    // Submit API Frappe (ví dụ lưu content hoặc insert)
    fetch('/api/method/your.custom.method', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ html: fullHtml })
    })
        .then(res => res.json())
        .then(data => {
            alert('Đã lưu thành công!')
        })
        .catch(err => {
            console.error('Gửi thất bại', err)
        })
}
</script>
<style>
.gjs-devices-c {
    padding: 0px;
}

.gjs-pn-devices select,
.gjs-field select,
.gjs-btn,
.gjs-input {
    all: unset;
    font-family: sans-serif;
    font-size: 14px;
    padding: 1px 1px;
    background: #2c2c2c;
    color: #fff;
    border: 1px solid #555;
    border-radius: 4px;
    text-align: justify;
}
</style>