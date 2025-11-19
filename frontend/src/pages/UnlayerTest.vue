<template>
  <div class="p-8">
    <h1 class="text-2xl font-bold mb-4">Unlayer Test Page</h1>
    
    <div class="mb-4 flex gap-2">
      <button @click="loadSimpleDesign" class="px-4 py-2 bg-blue-500 text-white rounded">
        Load Simple Design
      </button>
      <button @click="loadHtmlDesign" class="px-4 py-2 bg-green-500 text-white rounded">
        Load HTML Design
      </button>
      <button @click="saveCurrentDesign" class="px-4 py-2 bg-purple-500 text-white rounded">
        Save Design
      </button>
      <button @click="exportCurrentHtml" class="px-4 py-2 bg-orange-500 text-white rounded">
        Export HTML
      </button>
    </div>

    <div class="mb-4">
      <h2 class="font-bold mb-2">Console Output:</h2>
      <pre class="bg-gray-100 p-4 rounded overflow-auto max-h-40">{{ consoleOutput }}</pre>
    </div>

    <EmailEditor 
      ref="emailEditor"
      :min-height="'600px'"
      :project-id="0"
      @load="onLoad"
      @ready="onReady"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { EmailEditor } from 'vue-email-editor'
import { createUnlayerDesignFromHtml } from '@/components/Settings/MiraEmailTemplate/unlayerHelper'

const emailEditor = ref(null)
const consoleOutput = ref('')

function log(message, data = null) {
  const timestamp = new Date().toLocaleTimeString()
  consoleOutput.value += `[${timestamp}] ${message}\n`
  if (data) {
    consoleOutput.value += JSON.stringify(data, null, 2) + '\n'
  }
  console.log(message, data)
}

function onLoad() {
  log('✅ Editor LOAD event fired')
}

function onReady() {
  log('✅ Editor READY event fired')
  log('Editor instance:', emailEditor.value?.editor ? 'EXISTS' : 'NULL')
}

function loadSimpleDesign() {
  const simpleDesign = {
    counters: {
      u_row: 1,
      u_column: 1,
      u_content_text: 1
    },
    body: {
      id: 'body',
      rows: [
        {
          id: 'row_1',
          cells: [1],
          columns: [
            {
              id: 'column_1',
              contents: [
                {
                  id: 'content_text_1',
                  type: 'text',
                  values: {
                    containerPadding: '10px',
                    _meta: {
                      htmlID: 'u_content_text_1',
                      htmlClassNames: 'u_content_text'
                    },
                    color: '#000000',
                    textAlign: 'left',
                    lineHeight: '140%',
                    linkStyle: {
                      inherit: true,
                      linkColor: '#0000ee',
                      linkHoverColor: '#0000ee',
                      linkUnderline: true,
                      linkHoverUnderline: true
                    },
                    text: '<p style="font-size: 14px; line-height: 140%;"><strong>Hello World!</strong></p><p style="font-size: 14px; line-height: 140%;">This is a simple text block.</p>'
                  }
                }
              ],
              values: {
                backgroundColor: '',
                padding: '0px',
                border: {},
                _meta: {
                  htmlID: 'u_column_1',
                  htmlClassNames: 'u_column'
                }
              }
            }
          ],
          values: {
            displayCondition: null,
            columns: false,
            backgroundColor: '',
            columnsBackgroundColor: '',
            backgroundImage: {
              url: '',
              fullWidth: true,
              repeat: false,
              center: true,
              cover: false
            },
            padding: '0px',
            hideDesktop: false,
            _meta: {
              htmlID: 'u_row_1',
              htmlClassNames: 'u_row'
            },
            selectable: true,
            draggable: true,
            duplicatable: true,
            deletable: true,
            hideable: true
          }
        }
      ],
      values: {
        contentWidth: '600px',
        fontFamily: {
          label: 'Arial',
          value: 'arial,helvetica,sans-serif'
        },
        textColor: '#000000',
        backgroundColor: '#e7e7e7',
        backgroundImage: {
          url: '',
          fullWidth: true,
          repeat: false,
          center: true,
          cover: false
        },
        _meta: {
          htmlID: 'u_body',
          htmlClassNames: 'u_body'
        }
      }
    },
    schemaVersion: 16
  }

  log('Loading simple design...')
  if (emailEditor.value?.editor) {
    emailEditor.value.editor.loadDesign(simpleDesign)
    log('✅ Simple design loaded')
  } else {
    log('❌ Editor not ready')
  }
}

function loadHtmlDesign() {
  const htmlContent = '<p>Dear {{ full_name }},</p><p>Welcome to our platform!</p><p>Best regards,<br>The Team</p>'
  const htmlDesign = createUnlayerDesignFromHtml(htmlContent)
  
  log('Loading HTML design...')
  log('Design structure:', htmlDesign)
  
  if (emailEditor.value?.editor) {
    emailEditor.value.editor.loadDesign(htmlDesign)
    log('✅ HTML design loaded')
  } else {
    log('❌ Editor not ready')
  }
}

function saveCurrentDesign() {
  if (emailEditor.value?.editor) {
    emailEditor.value.editor.saveDesign((design) => {
      log('💾 Current design saved:', design)
    })
  } else {
    log('❌ Editor not ready')
  }
}

function exportCurrentHtml() {
  if (emailEditor.value?.editor) {
    emailEditor.value.editor.exportHtml((data) => {
      log('📤 Exported HTML:')
      log('HTML length:', data.html.length)
      log('Design:', data.design)
    })
  } else {
    log('❌ Editor not ready')
  }
}
</script>
