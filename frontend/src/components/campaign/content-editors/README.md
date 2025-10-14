# Campaign Content Editors

## Overview
Modular content editors for different interaction types in campaign creation.

## Components

### 1. CampaignContentEditor.vue
Main component that renders the appropriate editor based on interaction type.

**Props:**
- `interaction_type`: 'EMAIL' | 'ZALO_ZNS' | 'ZALO_CARE'
- `modelValue`: Object containing content data
- `readonly`: Boolean for read-only mode

**Events:**
- `update:modelValue`: Emitted when content changes
- `save`: Emitted when save button clicked
- `preview`: Emitted when preview button clicked

### 2. EmailEditor.vue
Rich email content editor with subject and body fields.

**Features:**
- Email subject input
- Rich text content area with variable insertion
- Variable buttons for [Candidate Name], [Job Title], [Company]
- Live preview toggle
- Character counter

### 3. ZaloZnsEditor.vue
Zalo ZNS message editor with action buttons.

**Features:**
- Message content textarea (640 char limit)
- Action buttons management (max 3)
- Button types: URL, Phone, Flow
- Live message preview
- Character counter with color coding

### 4. ZaloCareEditor.vue
Zalo Care message editor with image support.

**Features:**
- Image upload/URL input
- Message content textarea
- Action buttons (same as ZNS)
- Live preview with image
- File upload handling

## Usage

```vue
<template>
  <CampaignContentEditor
    :interaction_type="'EMAIL'"
    :model-value="contentData"
    @update:model-value="handleUpdate"
    @save="handleSave"
    @preview="handlePreview"
  />
</template>

<script setup>
import CampaignContentEditor from './CampaignContentEditor.vue'

const contentData = ref({
  email_subject: '',
  email_content: '',
  message_content: '',
  image_url: '',
  action_buttons: []
})

const handleUpdate = (newContent) => {
  contentData.value = newContent
}

const handleSave = () => {
  console.log('Saving:', contentData.value)
}

const handlePreview = () => {
  console.log('Previewing:', contentData.value)
}
</script>
```

## Data Structure

### Email Content
```javascript
{
  email_subject: "Job Opportunity at Company",
  email_content: "Hello [Candidate Name]...",
  success_action: "mark_interested",
  failure_action: "retry_later"
}
```

### Zalo Content
```javascript
{
  message_content: "Hello! We have an opportunity...",
  image_url: "https://example.com/image.jpg", // For Care only
  action_buttons: [
    {
      title: "Learn More",
      type: "url",
      value: "https://company.com/jobs"
    },
    {
      title: "Call Us",
      type: "phone", 
      value: "+84901234567"
    }
  ],
  success_action: "schedule_interview",
  failure_action: "mark_uninterested"
}
```

## Integration

The editors are integrated into CampaignWizard at Step 4:
- Automatically renders based on selected interaction_method
- Saves content to campaign data
- Supports both create and edit modes
- Respects readonly permissions
