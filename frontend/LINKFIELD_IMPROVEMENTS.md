# LinkField Component - Unified Solution

## Tổng quan

Đã hợp nhất 3 LinkField components thành **1 component duy nhất** với **3 modes** hoạt động thông minh, hiển thị đúng format: **name** (tên bản ghi) trên trên và **description** (trường phụ) bên dưới.

**Đặc điểm chính**: 
- ✅ **1 Component duy nhất** - `LinkField.vue`
- ✅ **3 Modes thông minh** - simple, auto, custom
- ✅ **Toàn bộ logic gói gọn** - không cần composable
- ✅ **Auto-detect behavior** - dựa trên props

## Component Architecture

### LinkField.vue - The Only Component You Need

```vue
<LinkField
  v-model="value"
  doctype="User"
  display-field="full_name"  <!-- Tự động chuyển sang custom mode -->
  mode="auto"                <!-- Hoặc chỉ định mode explicitly -->
  :filters="[]"
  label="Chọn User"
  @change="handleChange"
/>
```

## 3 Modes Hoạt động

### 1. **Simple Mode** - Core API
```vue
<LinkField doctype="User" mode="simple" />
```
- ✅ Sử dụng `frappe.desk.search.search_link` (core API)
- ✅ Nhanh nhất, đơn giản nhất
- ✅ Tương thích hoàn toàn với core Frappe
- ✅ Không cần chỉ định display-field

### 2. **Auto Mode** - Smart Detection (Default)
```vue
<LinkField doctype="User" />
<!-- hoặc -->
<LinkField doctype="User" mode="auto" />
```
- ✅ Tự động detect display field từ meta
- ✅ Sử dụng `frappe.client.get_list` với meta information
- ✅ Fallback logic thông minh cho description
- ✅ **Mode mặc định** khi không chỉ định gì

### 3. **Custom Mode** - Full Control
```vue
<LinkField 
  doctype="User" 
  display-field="full_name"
  search-field="email"
  mode="custom" 
/>
```
- ✅ Chỉ định chính xác display field
- ✅ Sử dụng custom API `search_link_custom`
- ✅ Hỗ trợ search-field tùy chỉnh
- ✅ **Auto-activate** khi có `display-field` prop

## Auto-detect Logic

Component sẽ tự động chọn mode dựa trên props:

```js
// Auto-detect rules:
if (props.mode !== 'auto') {
  return props.mode  // Sử dụng mode được chỉ định
}

if (props.displayField) {
  return 'custom'    // Có display-field → custom mode
}

return 'simple'      // Mặc định → simple mode
```

## API Backend

**File**: `apps/mbw_mira/mbw_mira/api/link_search.py`

- ✅ Backup logic từ core `search.py` của Frappe
- ✅ Function `build_for_autosuggest_custom` 
- ✅ API `search_link_custom` với `display_field` parameter
- ✅ Relevance sorting và field type validation
- ✅ Auto-detect display field dựa trên doctype

## Cách sử dụng

### Basic Usage (Auto Mode)
```vue
<template>
  <LinkField
    v-model="selectedUser"
    doctype="User"
    label="Chọn User"
    placeholder="Nhập tên user..."
  />
</template>
```

### Custom Display Field
```vue
<template>
  <LinkField
    v-model="selectedCustomer"
    doctype="Customer"
    display-field="customer_name"
    search-field="customer_name"
    label="Chọn Customer"
    :filters="[['disabled', '!=', 1]]"
  />
</template>
```

### Simple Mode (Core API)
```vue
<template>
  <LinkField
    v-model="selectedCampaign"
    doctype="Campaign"
    mode="simple"
    label="Chọn Campaign"
    :filters="[['is_active', '=', 1]]"
  />
</template>
```

### With Filters và Eval
```vue
<template>
  <LinkField
    v-model="selectedItem"
    doctype="Item"
    display-field="item_name"
    :filters="[
      ['enabled', '=', 1],
      ['country', '=', 'eval:doc.country_id']
    ]"
    :doc="currentDoc"
    label="Chọn Item"
  />
</template>
```

## Props Reference

```js
props: {
  // Required
  doctype: String,              // DocType cần search
  
  // Mode Control  
  mode: String,                 // 'auto' | 'simple' | 'custom'
  displayField: String,         // Field hiển thị description (auto → custom mode)
  searchField: String,          // Field để search (custom mode)
  
  // Data & Filters
  modelValue: String,           // v-model value
  filters: Array,               // Filters cho query
  doc: Object,                  // Để eval filters
  
  // UI Props
  label: String,                // Label hiển thị
  placeholder: String,          // Placeholder text
  size: String,                 // Size của input
  variant: String,              // Variant của input
  
  // Features
  hideMe: Boolean,              // Ẩn "@me" option cho User
  onCreate: Function,           // Callback tạo mới
  showClear: Boolean,           // Hiển thị nút clear
}
```

## Hiển thị Format

### Khi đã chọn (Selection)
- Hiển thị **name** của bản ghi (VD: `"USR-2024-001"`)

### Trong dropdown
- **Dòng 1**: Name của bản ghi (VD: `"USR-2024-001"`)
- **Dòng 2**: Description từ display_field (VD: `"Nguyễn Văn A"`)

## Tính năng nổi bật

1. ✅ **Unified**: 1 component thay cho 3 component
2. ✅ **Smart**: Auto-detect mode dựa trên props
3. ✅ **Flexible**: 3 levels of customization
4. ✅ **Self-contained**: Toàn bộ logic trong component
5. ✅ **Performance**: Debounced search, optimized API calls
6. ✅ **Consistent**: Cùng format hiển thị ở mọi mode
7. ✅ **Backward compatible**: Hoạt động với existing code

## Migration Guide

### Từ 3 components cũ:

```vue
<!-- Từ -->
<EasyLinkField doctype="User" />
<LinkField doctype="User" />  
<LinkFieldCustom doctype="User" display-field="full_name" />

<!-- Thành -->
<LinkField doctype="User" mode="simple" />
<LinkField doctype="User" mode="auto" />
<LinkField doctype="User" display-field="full_name" />
```

### Import changes:

```vue
<!-- Từ -->
<script setup>
import EasyLinkField from './EasyLinkField.vue'
import LinkField from './LinkField.vue'
import LinkFieldCustom from './LinkFieldCustom.vue'
</script>

<!-- Thành -->
<script setup>
import LinkField from './LinkField.vue'
</script>
```

## Performance Comparison

| Mode | API Used | Speed | Use Case |
|------|----------|-------|----------|
| Simple | `frappe.desk.search.search_link` | ⚡⚡⚡ Fastest | Quick lookup, existing behavior |
| Auto | `frappe.client.get_list` + meta | ⚡⚡ Fast | Smart default, most cases |
| Custom | `search_link_custom` | ⚡ Controlled | Precise control, complex scenarios |

## File Structure

```
apps/mbw_mira/frontend/src/components/
├── LinkField.vue           # The ONLY component you need
└── LinkFieldDemo.vue       # Demo với 3 modes

apps/mbw_mira/mbw_mira/api/
└── link_search.py          # Custom API backend

// Đã xóa:
❌ LinkFieldCustom.vue      # Merged into LinkField.vue
❌ EasyLinkField.vue        # Merged into LinkField.vue  
❌ useLinkFieldCustom.js    # Logic moved to component
❌ useLinkField.js          # Logic moved to component
```

## Examples by DocType

```vue
<!-- User với full_name -->
<LinkField doctype="User" display-field="full_name" />

<!-- Customer tự động detect customer_name -->
<LinkField doctype="Customer" />

<!-- Campaign với filters -->
<LinkField 
  doctype="Campaign" 
  display-field="campaign_name"
  :filters="[['status', '=', 'Active']]" 
/>

<!-- Simple mode cho performance -->
<LinkField doctype="Item" mode="simple" />
```

## Test & Demo

Sử dụng `LinkFieldDemo.vue` để test:
- ✅ So sánh 3 modes
- ✅ Test với nhiều doctype
- ✅ Theo dõi behavior changes
- ✅ Performance comparison

## Lợi ích

1. ✅ **Simplicity**: 1 component thay cho 3
2. ✅ **Intelligence**: Auto-detect behavior
3. ✅ **Maintainability**: Ít file hơn, logic tập trung
4. ✅ **Performance**: Optimized cho từng use case
5. ✅ **Flexibility**: Vẫn có thể control fine-grained

## Kế hoạch tiếp theo

1. 🔄 Add caching mechanism
2. 🔄 Performance optimization cho large datasets
3. 🔄 Advanced filtering features
4. 🔄 Unit tests coverage
5. 🔄 TypeScript support

## Key Changes & Architecture

### 1. Unified Component Architecture

**Single Component**: `LinkField.vue` - Hợp nhất 3 components thành 1
- ✅ **3 Modes trong 1**: Simple, Auto, Custom
- ✅ **Auto-detect behavior**: Thông minh chọn mode dựa trên props
- ✅ **Self-contained**: Toàn bộ logic gói gọn, không cần composable
- ✅ **Backward compatible**: Hoạt động với code cũ

### 2. Smart Mode System

#### Mode 1: Simple (Core API)
- ✅ Sử dụng `frappe.desk.search.search_link`
- ✅ Fastest performance
- ✅ Core compatibility
- ✅ Activate: `mode="simple"`

#### Mode 2: Auto (Smart Detection) - Default
- ✅ Auto-detect display field từ meta
- ✅ Sử dụng `frappe.client.get_list`
- ✅ Fallback logic thông minh
- ✅ Activate: default hoặc `mode="auto"`

#### Mode 3: Custom (Full Control)
- ✅ Chỉ định display field
- ✅ Sử dụng `search_link_custom` API
- ✅ Search field customization
- ✅ Activate: có `display-field` prop

### 3. Cleanup & Consolidation

#### Removed Files:
- ❌ `LinkFieldCustom.vue` → Merged into `LinkField.vue`
- ❌ `EasyLinkField.vue` → Merged into `LinkField.vue`
- ❌ `useLinkFieldCustom.js` → Logic moved to component
- ❌ `useLinkField.js` → Logic moved to component

#### Current Structure:
- ✅ `LinkField.vue` - The only component
- ✅ `LinkFieldDemo.vue` - Demo với 3 modes
- ✅ `link_search.py` - Custom API backend



 