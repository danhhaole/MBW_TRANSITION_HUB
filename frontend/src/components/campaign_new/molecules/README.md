# Campaign Molecules

Shared molecules được sử dụng trong các campaign wizards.

## 📦 Available Molecules

### **Content Editors**

#### **FacebookContentEditor.vue** ⭐ NEW
Reusable Facebook post content editor với image upload và page selection.

**Props:**
- `title` (String) - Custom title
- `content` (String) - Post content
- `image` (String) - Image URL
- `pageId` (String) - Selected Facebook page ID
- `link` (String) - Optional link URL
- `placeholder` (String) - Textarea placeholder
- `rows` (Number) - Textarea rows (default: 6)
- `required` (Boolean) - Mark fields as required
- `showPageSelector` (Boolean) - Show page selector (default: true)
- `showLinkInput` (Boolean) - Show link input (default: false)
- `pageOptions` (Array) - Facebook page options
- `showError` (Boolean) - Show validation errors

**Emits:**
- `update:content` - Content changed
- `update:image` - Image changed
- `update:pageId` - Page selection changed
- `update:link` - Link changed

**Usage:**
```vue
<FacebookContentEditor
  :content="facebookContent.content"
  :image="facebookContent.image"
  :page-id="facebookContent.page_id"
  :show-page-selector="true"
  @update:content="facebookContent.content = $event"
  @update:image="facebookContent.image = $event"
  @update:page-id="facebookContent.page_id = $event"
/>
```

---

#### **ZaloContentEditor.vue** ⭐ NEW
Reusable Zalo post content editor với image upload và OA selection.

**Props:**
- `title` (String) - Custom title
- `content` (String) - Post content
- `image` (String) - Image URL
- `oaId` (String) - Selected Zalo OA ID
- `link` (String) - Optional link URL
- `messageType` (String) - Message type (text/zns/care)
- `placeholder` (String) - Textarea placeholder
- `rows` (Number) - Textarea rows (default: 6)
- `required` (Boolean) - Mark fields as required
- `showOASelector` (Boolean) - Show OA selector (default: false)
- `showLinkInput` (Boolean) - Show link input (default: false)
- `showMessageType` (Boolean) - Show message type selector (default: false)
- `oaOptions` (Array) - Zalo OA options
- `messageTypeOptions` (Array) - Message type options
- `showError` (Boolean) - Show validation errors

**Emits:**
- `update:content` - Content changed
- `update:image` - Image changed
- `update:oaId` - OA selection changed
- `update:link` - Link changed
- `update:messageType` - Message type changed

**Usage:**
```vue
<ZaloContentEditor
  :content="zaloContent.content"
  :image="zaloContent.image"
  :show-oa-selector="true"
  :show-message-type="true"
  @update:content="zaloContent.content = $event"
  @update:image="zaloContent.image = $event"
  @update:oa-id="zaloContent.oa_id = $event"
/>
```

---

### **Form Components**

### **1. CampaignBasicInfo.vue**
Form nhập thông tin cơ bản của campaign.

**Props:**
- `campaignName` (String) - Tên campaign
- `objective` (String) - Mục tiêu campaign
- `showError` (Boolean) - Hiển thị validation errors

**Emits:**
- `update:campaignName` - Khi campaign name thay đổi
- `update:objective` - Khi objective thay đổi

**Usage:**
```vue
<CampaignBasicInfo
  :campaign-name="campaignData.campaign_name"
  :objective="campaignData.objective"
  :show-error="showValidationError"
  @update:campaign-name="campaignData.campaign_name = $event"
  @update:objective="campaignData.objective = $event"
/>
```

---

### **2. ChannelSelector.vue**
Grid selector cho communication channels (Email, Zalo, SMS, etc.)

**Props:**
- `modelValue` (String) - Selected channel value
- `title` (String) - Tiêu đề
- `description` (String) - Mô tả
- `channels` (Array) - Danh sách channels available
- `disabled` (Boolean) - Disable selection

**Emits:**
- `update:modelValue` - Khi channel được chọn

**Channel Object Structure:**
```javascript
{
  value: 'EMAIL',
  icon: 'mail',
  title: 'Email',
  description: 'Send personalized emails'
}
```

**Usage:**
```vue
<ChannelSelector
  v-model="selectedChannel"
  :title="'Select Channel'"
  :description="'Choose communication method'"
  :channels="availableChannels"
/>
```

---

### **3. TargetSegmentSelector.vue** ⭐ NEW
Component để chọn target audience - có 2 modes:
- **Segment Mode**: Chọn từ existing segments (sử dụng PoolConfig)
- **Conditions Mode**: Tạo custom filtering conditions (sử dụng ConditionsBuilder)

**Props:**
- `title` (String) - Tiêu đề
- `description` (String) - Mô tả
- `selectionMode` (String) - 'segment' hoặc 'conditions'
- `configData` (Object) - Data cho PoolConfig
- `conditions` (Array) - Custom conditions
- `candidateCount` (Number) - Số lượng candidates

**Emits:**
- `update:selectionMode` - Khi mode thay đổi
- `update:configData` - Khi config data thay đổi
- `update:conditions` - Khi conditions thay đổi
- `validate` - Khi validation xảy ra
- `change` - Khi có thay đổi

**Usage:**
```vue
<TargetSegmentSelector
  :title="'Select Target Audience'"
  :description="'Choose candidates for this campaign'"
  :selection-mode="segmentMode"
  :config-data="configData"
  :conditions="customConditions"
  :candidate-count="totalCandidates"
  @update:selection-mode="segmentMode = $event"
  @update:config-data="configData = $event"
  @update:conditions="customConditions = $event"
  @validate="handleValidate"
  @change="handleChange"
/>
```

**Features:**
- ✅ Visual card selector cho mode selection
- ✅ Integration với PoolConfig component
- ✅ Integration với ConditionsBuilder component
- ✅ Real-time candidate count display
- ✅ Validation support

---

### **4. SendingStrategy.vue** ⭐ NEW
Component để chọn sending strategy - gửi ngay hoặc schedule.

**Props:**
- `title` (String) - Tiêu đề
- `description` (String) - Mô tả
- `strategy` (String) - 'now' hoặc 'scheduled'
- `scheduledDate` (String) - Scheduled date/time

**Emits:**
- `update:strategy` - Khi strategy thay đổi
- `update:scheduledDate` - Khi scheduled date thay đổi

**Usage:**
```vue
<SendingStrategy
  :title="'When to Send?'"
  :description="'Choose sending time'"
  :strategy="sendingStrategy"
  :scheduled-date="scheduledDate"
  @update:strategy="sendingStrategy = $event"
  @update:scheduled-date="scheduledDate = $event"
/>
```

**Features:**
- ✅ Visual card selector cho strategy
- ✅ Datetime picker cho scheduled sending
- ✅ Auto-clear scheduled date khi chọn "Send Now"
- ✅ Info box với helpful messages

---

## 🎯 Usage in Campaign Types

### **Attraction Campaign**
```vue
<!-- Step 1 -->
<CampaignBasicInfo ... />
<Link doctype="Mira Segment" ... />  <!-- Target Pool -->
```

### **Nurturing Campaign**
```vue
<!-- Step 1 -->
<CampaignBasicInfo ... />
<TargetSegmentSelector ... />  <!-- Segment or Conditions -->
```

### **Recruitment Campaign**
```vue
<!-- Step 1 -->
<CampaignBasicInfo ... />
<TargetSegmentSelector ... />  <!-- Candidate Selection -->
```

---

## 📊 Component Dependencies

### **TargetSegmentSelector**
Requires:
- `@/components/campaign/PoolConfig.vue` - Existing component for segment selection
- `@/components/ConditionsFilter/ConditionsBuilder.vue` - Existing component for custom conditions
- `FeatherIcon` from frappe-ui

### **SendingStrategy**
Requires:
- `FormControl` from frappe-ui
- `FeatherIcon` from frappe-ui

---

## 🔄 Migration from Old CampaignWizard

### **Old Code (CampaignWizard.vue)**
```vue
<!-- Lines 282-377: Target Segment -->
<div class="bg-gray-50 rounded-lg p-6">
  <!-- Segment selection mode -->
  <!-- PoolConfig component -->
  <!-- ConditionsBuilder component -->
  <!-- Candidate count -->
</div>

<!-- Lines 380-443: Sending Strategy -->
<div class="bg-gray-50 rounded-lg p-6">
  <!-- Send now / Schedule -->
  <!-- Datetime picker -->
</div>
```

### **New Code (Molecules)**
```vue
<!-- Use TargetSegmentSelector molecule -->
<TargetSegmentSelector
  :selection-mode="segmentMode"
  :config-data="configData"
  :conditions="conditions"
  :candidate-count="count"
  @update:selection-mode="segmentMode = $event"
  @update:config-data="configData = $event"
  @update:conditions="conditions = $event"
/>

<!-- Use SendingStrategy molecule -->
<SendingStrategy
  :strategy="strategy"
  :scheduled-date="date"
  @update:strategy="strategy = $event"
  @update:scheduled-date="date = $event"
/>
```

---

## ✅ Benefits

1. **Reusability** - Dùng lại ở nhiều campaign types
2. **Maintainability** - Sửa 1 chỗ, áp dụng cho tất cả
3. **Consistency** - UI/UX consistent across campaigns
4. **Testability** - Dễ test từng molecule độc lập
5. **Scalability** - Dễ thêm features mới

---

## 📝 Next Steps

1. ✅ Tạo TargetSegmentSelector molecule
2. ✅ Tạo SendingStrategy molecule
3. ✅ Update Nurturing Step1 để dùng TargetSegmentSelector
4. ✅ Update Recruitment Step1 để dùng TargetSegmentSelector
5. ⏳ Update Step3 của các campaigns để dùng SendingStrategy
6. ⏳ Add validation logic
7. ⏳ Add tests

---

## 🐛 Known Issues

- ⚠️ Candidate count calculation chưa implement
- ⚠️ Validation cho conditions chưa hoàn chỉnh

---

## 📚 Related Files

- `/components/campaign/PoolConfig.vue` - Segment selection component ✅
- `/components/ConditionsFilter/ConditionsBuilder.vue` - Custom conditions builder ✅
- `/components/campaign/CampaignWizard.vue` - Old wizard (reference)
