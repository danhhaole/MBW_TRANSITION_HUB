# Campaign Wizard - Full Screen Layout

Đã chuyển đổi CampaignWizard từ dialog sang full-screen layout theo yêu cầu.

## Các component đã tạo:

### 1. CampaignWizardHeader.vue
- **Chức năng**: Header với nút Exit, Back, tên campaign có thể edit, và các nút Save/Continue
- **Props**:
  - `campaignName`: Tên campaign hiện tại
  - `currentStep`: Bước hiện tại
  - `totalSteps`: Tổng số bước
  - `loading`, `saving`, `finalizing`: Trạng thái loading
  - `canSave`, `canProceed`, `canFinalize`: Điều kiện cho phép thực hiện action
- **Events**:
  - `@exit`: Thoát wizard
  - `@back`: Quay lại bước trước
  - `@save`: Lưu draft
  - `@save-and-continue`: Lưu và tiếp tục
  - `@finalize`: Hoàn thành campaign
  - `@update:campaign-name`: Cập nhật tên campaign

### 2. CampaignWizardStepper.vue
- **Chức năng**: Hiển thị các bước với icon, label và trạng thái
- **Props**:
  - `steps`: Array các bước với `number`, `label`, `description` (optional)
  - `currentStep`: Bước hiện tại
- **Features**:
  - Animation smooth khi chuyển bước
  - Icon check cho bước đã hoàn thành
  - Emoji 🎉 cho bước cuối
  - Hover effects

### 3. CampaignWizardContent.vue
- **Chức năng**: Container cho nội dung các bước với animation
- **Props**:
  - `currentStep`: Bước hiện tại
- **Features**:
  - Fade transition giữa các bước
  - Custom scrollbar
  - Responsive layout

### 4. CampaignWizardFixed.vue
- **Chức năng**: Version hoàn chỉnh của wizard với layout mới
- **Layout**:
  ```
  ┌─────────────────────────────────────────┐
  │ Header (Exit, Back, Name, Save, Continue) │
  ├─────────────────────────────────────────┤
  │ Stepper (Step 1 → Step 2 → Step 3 → Step 4) │
  ├─────────────────────────────────────────┤
  │                                         │
  │            Content Area                 │
  │         (Scrollable)                    │
  │                                         │
  └─────────────────────────────────────────┘
  ```

### 5. CampaignWizardDemo.vue
- **Chức năng**: Component demo để test wizard
- **Usage**:
  ```vue
  <CampaignWizardDemo />
  ```

## Cách sử dụng:

### Sử dụng CampaignWizardFixed:
```vue
<template>
  <div>
    <Button @click="openWizard">Create Campaign</Button>
    
    <CampaignWizardFixed
      v-model="showWizard"
      @success="onSuccess"
      @draft-created="onDraftCreated"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CampaignWizardFixed from './CampaignWizardFixed.vue'

const showWizard = ref(false)

const openWizard = () => {
  showWizard.value = true
}

const onSuccess = (data) => {
  console.log('Campaign created:', data)
}
</script>
```

## Thay đổi chính:

1. **Layout**: Từ dialog modal → Full-screen overlay với `fixed inset-0`
2. **Header**: Tách riêng với các nút như trong hình mẫu
3. **Stepper**: Tách riêng với animation và styling tốt hơn
4. **Content**: Tách riêng với scroll và transition smooth
5. **Structure**: Modular, dễ maintain và customize

## Lưu ý:

- File `CampaignWizard.vue` gốc vẫn có lỗi cấu trúc template (thiếu thẻ đóng div)
- Sử dụng `CampaignWizardFixed.vue` cho layout mới hoàn chỉnh
- Có thể tích hợp logic từ file gốc vào CampaignWizardFixed theo nhu cầu
- Header có thể edit tên campaign inline
- Responsive design cho mobile và desktop

## Next Steps:

1. Tích hợp đầy đủ logic từ CampaignWizard.vue gốc
2. Thêm validation và error handling
3. Tối ưu performance và UX
4. Test trên các screen size khác nhau
