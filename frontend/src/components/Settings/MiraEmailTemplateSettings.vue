<template>
  <div class="flex h-full flex-col">
    <component
      :is="currentStep.component"
      :templateData="selectedTemplate"
      @updateStep="updateStep"
    />
  </div>
</template>

<script setup>
import { ref, provide, markRaw } from 'vue'
import { createResource } from 'frappe-ui'
import MiraEmailTemplateList from './MiraEmailTemplate/MiraEmailTemplateList.vue'
import NewMiraEmailTemplate from './MiraEmailTemplate/NewMiraEmailTemplate.vue'
import EditMiraEmailTemplate from './MiraEmailTemplate/EditMiraEmailTemplate.vue'

const steps = {
  'template-list': {
    component: markRaw(MiraEmailTemplateList),
  },
  'new-template': {
    component: markRaw(NewMiraEmailTemplate),
  },
  'edit-template': {
    component: markRaw(EditMiraEmailTemplate),
  },
}

const currentStep = ref(steps['template-list'])
const selectedTemplate = ref(null)

// Resource for managing Mira Email Templates
const templates = createResource({
  url: 'frappe.client.get_list',
  params: {
    doctype: 'Mira Email Template',
    fields: [
      'name',
      'template_name',
      'template_type',
      'subject',
      'message',
      'email_design_json',
      'is_active',
      'default_template',
      'auto_send',
      'created_by',
      'created_time',
    ],
    order_by: 'modified desc',
    limit_page_length: 100,
  },
  auto: true,
})

// Resource for updating template fields
templates.setValue = createResource({
  url: 'frappe.client.set_value',
  makeParams(values) {
    return {
      doctype: 'Mira Email Template',
      name: values.name,
      fieldname: values,
    }
  },
  onSuccess() {
    templates.reload()
  },
})

// Resource for inserting new template
templates.insert = createResource({
  url: 'frappe.client.insert',
  makeParams(values) {
    return {
      doc: {
        doctype: 'Mira Email Template',
        ...values,
      },
    }
  },
  onSuccess() {
    templates.reload()
  },
})

// Resource for deleting template
templates.delete = createResource({
  url: 'frappe.client.delete',
  makeParams(name) {
    return {
      doctype: 'Mira Email Template',
      name: name,
    }
  },
  onSuccess() {
    templates.reload()
  },
})

provide('templates', templates)

function updateStep(step, data = null) {
  currentStep.value = steps[step]
  selectedTemplate.value = data
}
</script>
