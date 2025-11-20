<template>
  <div v-if="block || showEmailSettings" class="properties-panel bg-white border-l border-gray-200 w-80 overflow-y-auto">
    <div class="p-4">
      <!-- Header -->
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-sm font-semibold text-gray-800">
          <FeatherIcon :name="showEmailSettings ? 'settings' : 'edit-3'" class="w-4 h-4 mr-2 inline" />
          {{ showEmailSettings ? 'Email Settings' : 'Properties' }}
        </h3>
        <Button
          icon="x"
          variant="ghost"
          size="sm"
          @click="$emit('close')"
        />
      </div>

      <!-- Email Settings -->
      <template v-if="showEmailSettings">
        <div class="space-y-4">
          <!-- Background Color -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Background Color</label>
            <div class="flex items-center gap-2">
              <input
                type="color"
                :value="emailSettings.backgroundColor"
                @input="updateEmailSetting('backgroundColor', $event.target.value)"
                class="w-10 h-8 rounded border border-gray-300"
              />
              <input
                type="text"
                :value="emailSettings.backgroundColor"
                @input="updateEmailSetting('backgroundColor', $event.target.value)"
                class="flex-1 px-3 py-2 border border-gray-300 rounded text-sm"
                placeholder="#ffffff"
              />
            </div>
          </div>


          <!-- Content Alignment -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Content Alignment</label>
            <div class="flex gap-2">
              <Button
                :variant="emailSettings.contentAlign === 'left' ? 'solid' : 'outline'"
                size="sm"
                @click="$emit('set-email-align', 'left')"
              >
                <FeatherIcon name="align-left" class="w-4 h-4" />
              </Button>
              <Button
                :variant="emailSettings.contentAlign === 'center' ? 'solid' : 'outline'"
                size="sm"
                @click="$emit('set-email-align', 'center')"
              >
                <FeatherIcon name="align-center" class="w-4 h-4" />
              </Button>
              <Button
                :variant="emailSettings.contentAlign === 'right' ? 'solid' : 'outline'"
                size="sm"
                @click="$emit('set-email-align', 'right')"
              >
                <FeatherIcon name="align-right" class="w-4 h-4" />
              </Button>
            </div>
          </div>

          <!-- Font Family -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Default Font Family</label>
            <select
              :value="emailSettings.fontFamily"
              @change="updateEmailSetting('fontFamily', $event.target.value)"
              class="w-full px-3 py-2 border border-gray-300 rounded text-sm"
            >
              <option value="Arial, sans-serif">Arial</option>
              <option value="Helvetica, sans-serif">Helvetica</option>
              <option value="Georgia, serif">Georgia</option>
              <option value="Times New Roman, serif">Times New Roman</option>
              <option value="Courier, monospace">Courier</option>
              <option value="Verdana, sans-serif">Verdana</option>
            </select>
          </div>
        </div>
      </template>
      
      <!-- Block Properties -->
      <template v-else-if="block">
      
        <!-- Text Block Properties -->
      <template v-if="block.type === 'text'">
        <!-- Content -->
        <FormControl
          type="textarea"
          v-model="block.props.content"
          @change="$emit('change')"
          label="Content"
          :rows="4"
        />

        <!-- Dimension Section -->
        <div class="border-t pt-4 mt-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <FeatherIcon name="maximize-2" class="w-4 h-4 mr-2" />
            Dimension
          </h4>
          
          <!-- Height -->
          <FormControl
            type="number"
            v-model="block.props.height"
            @change="$emit('change')"
            label="Height"
            placeholder="Auto"
          />
          
          <!-- Padding -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Padding</label>
            <div class="grid grid-cols-2 gap-2">
              <FormControl
                type="number"
                v-model="block.props.paddingTop"
                @change="$emit('change')"
                placeholder="Top"
                size="sm"
              />
              <FormControl
                type="number"
                v-model="block.props.paddingBottom"
                @change="$emit('change')"
                placeholder="Bottom"
                size="sm"
              />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <FormControl
                type="number"
                v-model="block.props.paddingLeft"
                @change="$emit('change')"
                placeholder="Left"
                size="sm"
              />
              <FormControl
                type="number"
                v-model="block.props.paddingRight"
                @change="$emit('change')"
                placeholder="Right"
                size="sm"
              />
            </div>
          </div>
        </div>

        <!-- Typography Section -->
        <div class="border-t pt-4 mt-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <FeatherIcon name="type" class="w-4 h-4 mr-2" />
            Typography
          </h4>
          
          <!-- Text Type -->
          <FormControl
            type="select"
            v-model="block.props.textType"
            @change="$emit('change')"
            label="Text type"
            :options="[
              { label: 'Paragraph', value: 'paragraph' },
              { label: 'Heading 1', value: 'h1' },
              { label: 'Heading 2', value: 'h2' },
              { label: 'Heading 3', value: 'h3' }
            ]"
          />
          
          <!-- Font Family -->
          <FormControl
            type="select"
            v-model="block.props.fontFamily"
            @change="$emit('change')"
            label="Font"
            :options="[
              { label: 'Arial', value: 'Arial, sans-serif' },
              { label: 'Helvetica', value: 'Helvetica, sans-serif' },
              { label: 'Georgia', value: 'Georgia, serif' },
              { label: 'Times New Roman', value: 'Times New Roman, serif' },
              { label: 'Courier', value: 'Courier, monospace' },
              { label: 'Verdana', value: 'Verdana, sans-serif' }
            ]"
          />
          
          <!-- Font Size -->
          <FormControl
            type="number"
            v-model="block.props.fontSize"
            @change="$emit('change')"
            label="Size"
            placeholder="16"
          />
          
          <!-- Text Color -->
          <FormControl
            type="color"
            v-model="block.props.color"
            @change="$emit('change')"
            label="Color"
          />
          
          <!-- Line Height -->
          <FormControl
            type="select"
            v-model="block.props.lineHeight"
            @change="$emit('change')"
            label="Line height"
            :options="[
              { label: '1.0', value: '1.0' },
              { label: '1.2', value: '1.2' },
              { label: '1.4', value: '1.4' },
              { label: '1.5', value: '1.5' },
              { label: '1.6', value: '1.6' },
              { label: '2.0', value: '2.0' }
            ]"
          />
          
          <!-- Font Style -->
          <FormControl
            type="select"
            v-model="block.props.fontStyle"
            @change="$emit('change')"
            label="Style"
            :options="[
              { label: 'Normal', value: 'normal' },
              { label: 'Italic', value: 'italic' }
            ]"
          />
          
          <!-- Letter Spacing -->
          <FormControl
            type="number"
            v-model="block.props.letterSpacing"
            @change="$emit('change')"
            label="Letter spacing"
            placeholder="0"
          />
          
          <!-- Font Weight Buttons -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Weight</label>
            <div class="flex gap-2">
              <Button
                :variant="block.props.fontWeight === 'bold' ? 'solid' : 'outline'"
                size="sm"
                @click="toggleFontWeight('bold')"
              >
                <FeatherIcon name="bold" class="w-4 h-4" />
              </Button>
              <Button
                :variant="block.props.fontStyle === 'italic' ? 'solid' : 'outline'"
                size="sm"
                @click="toggleFontStyle('italic')"
              >
                <FeatherIcon name="italic" class="w-4 h-4" />
              </Button>
              <Button
                :variant="block.props.textDecoration === 'underline' ? 'solid' : 'outline'"
                size="sm"
                @click="toggleTextDecoration('underline')"
              >
                <FeatherIcon name="underline" class="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>

        <!-- Block Section -->
        <div class="border-t pt-4 mt-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <FeatherIcon name="square" class="w-4 h-4 mr-2" />
            Block
          </h4>
          
          <!-- Background Color -->
          <FormControl
            type="color"
            v-model="block.props.backgroundColor"
            @change="$emit('change')"
            label="Background color"
          />
          
          <!-- Text Alignment -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Align</label>
            <div class="flex gap-1">
              <Button
                :variant="block.props.textAlign === 'left' ? 'solid' : 'outline'"
                size="sm"
                @click="setTextAlign('left')"
              >
                <FeatherIcon name="align-left" class="w-4 h-4" />
              </Button>
              <Button
                :variant="block.props.textAlign === 'center' ? 'solid' : 'outline'"
                size="sm"
                @click="setTextAlign('center')"
              >
                <FeatherIcon name="align-center" class="w-4 h-4" />
              </Button>
              <Button
                :variant="block.props.textAlign === 'right' ? 'solid' : 'outline'"
                size="sm"
                @click="setTextAlign('right')"
              >
                <FeatherIcon name="align-right" class="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </template>

      <!-- Button Block Properties -->
      <template v-if="block.type === 'button'">
        <!-- Content -->
        <FormControl
          type="text"
          v-model="block.props.text"
          @change="$emit('change')"
          label="Button Text"
        />
        
        <FormControl
          type="text"
          v-model="block.props.href"
          @change="$emit('change')"
          label="Link URL"
          placeholder="https://"
        />

        <!-- Dimension Section -->
        <div class="border-t pt-4 mt-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <FeatherIcon name="maximize-2" class="w-4 h-4 mr-2" />
            Dimension
          </h4>
          
          <!-- Width -->
          <FormControl
            type="select"
            v-model="block.props.width"
            @change="$emit('change')"
            label="Width"
            :options="[
              { label: 'Auto', value: 'auto' },
              { label: 'Full width', value: '100%' },
              { label: 'Custom', value: 'custom' }
            ]"
          />
          
          <!-- Custom Width -->
          <FormControl
            v-if="block.props.width === 'custom'"
            type="number"
            v-model="block.props.customWidth"
            @change="$emit('change')"
            label="Custom Width (px)"
            placeholder="200"
          />
          
          <!-- Height -->
          <FormControl
            type="number"
            v-model="block.props.height"
            @change="$emit('change')"
            label="Height (px)"
            placeholder="Auto"
          />
          
          <!-- Padding -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Padding</label>
            <div class="grid grid-cols-2 gap-2">
              <FormControl
                type="number"
                v-model="block.props.paddingTop"
                @change="$emit('change')"
                placeholder="Top"
                size="sm"
              />
              <FormControl
                type="number"
                v-model="block.props.paddingBottom"
                @change="$emit('change')"
                placeholder="Bottom"
                size="sm"
              />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <FormControl
                type="number"
                v-model="block.props.paddingLeft"
                @change="$emit('change')"
                placeholder="Left"
                size="sm"
              />
              <FormControl
                type="number"
                v-model="block.props.paddingRight"
                @change="$emit('change')"
                placeholder="Right"
                size="sm"
              />
            </div>
          </div>
        </div>

        <!-- Typography Section -->
        <div class="border-t pt-4 mt-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <FeatherIcon name="type" class="w-4 h-4 mr-2" />
            Typography
          </h4>
          
          <!-- Font Family -->
          <FormControl
            type="select"
            v-model="block.props.fontFamily"
            @change="$emit('change')"
            label="Font"
            :options="[
              { label: 'Arial', value: 'Arial, sans-serif' },
              { label: 'Helvetica', value: 'Helvetica, sans-serif' },
              { label: 'Georgia', value: 'Georgia, serif' },
              { label: 'Times New Roman', value: 'Times New Roman, serif' },
              { label: 'Courier', value: 'Courier, monospace' },
              { label: 'Verdana', value: 'Verdana, sans-serif' }
            ]"
          />
          
          <!-- Font Size -->
          <FormControl
            type="number"
            v-model="block.props.fontSize"
            @change="$emit('change')"
            label="Size (px)"
            placeholder="16"
          />
          
          <!-- Text Color -->
          <FormControl
            type="color"
            v-model="block.props.color"
            @change="$emit('change')"
            label="Text Color"
          />
          
          <!-- Font Weight -->
          <FormControl
            type="select"
            v-model="block.props.fontWeight"
            @change="$emit('change')"
            label="Font Weight"
            :options="[
              { label: 'Normal', value: 'normal' },
              { label: 'Bold', value: 'bold' },
              { label: '300', value: '300' },
              { label: '400', value: '400' },
              { label: '500', value: '500' },
              { label: '600', value: '600' },
              { label: '700', value: '700' }
            ]"
          />
          
          <!-- Letter Spacing -->
          <FormControl
            type="number"
            v-model="block.props.letterSpacing"
            @change="$emit('change')"
            label="Letter spacing (px)"
            placeholder="0"
          />
        </div>

        <!-- Border Section -->
        <div class="border-t pt-4 mt-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <FeatherIcon name="square" class="w-4 h-4 mr-2" />
            Border
          </h4>
          
          <!-- Border Toggle -->
          <div class="flex items-center space-x-2 mb-3">
            <input
              type="checkbox"
              v-model="block.props.hasBorder"
              @change="$emit('change')"
              class="rounded"
            />
            <label class="text-sm font-medium text-gray-700">Enable Border</label>
          </div>
          
          <template v-if="block.props.hasBorder">
            <!-- Border Width -->
            <FormControl
              type="number"
              v-model="block.props.borderWidth"
              @change="$emit('change')"
              label="Border Width (px)"
              placeholder="1"
            />
            
            <!-- Border Color -->
            <FormControl
              type="color"
              v-model="block.props.borderColor"
              @change="$emit('change')"
              label="Border Color"
            />
            
            <!-- Border Radius -->
            <FormControl
              type="number"
              v-model="block.props.borderRadius"
              @change="$emit('change')"
              label="Border Radius (px)"
              placeholder="4"
            />
          </template>
        </div>

        <!-- Block Section -->
        <div class="border-t pt-4 mt-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <FeatherIcon name="layout" class="w-4 h-4 mr-2" />
            Block
          </h4>
          
          <!-- Background Color -->
          <FormControl
            type="color"
            v-model="block.props.backgroundColor"
            @change="$emit('change')"
            label="Background Color"
          />
          
          <!-- Button Alignment -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Align</label>
            <div class="flex gap-1">
              <Button
                :variant="block.props.align === 'left' ? 'solid' : 'outline'"
                size="sm"
                @click="setButtonAlign('left')"
              >
                <FeatherIcon name="align-left" class="w-4 h-4" />
              </Button>
              <Button
                :variant="block.props.align === 'center' ? 'solid' : 'outline'"
                size="sm"
                @click="setButtonAlign('center')"
              >
                <FeatherIcon name="align-center" class="w-4 h-4" />
              </Button>
              <Button
                :variant="block.props.align === 'right' ? 'solid' : 'outline'"
                size="sm"
                @click="setButtonAlign('right')"
              >
                <FeatherIcon name="align-right" class="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </template>

      <!-- Image Block Properties -->
      <template v-if="block.type === 'image'">
        <!-- Image Settings Section -->
        <div class="border-t pt-4 mt-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <FeatherIcon name="image" class="w-4 h-4 mr-2" />
            Image settings
          </h4>
          
          <!-- Link Address -->
          <FormControl
            type="text"
            v-model="block.props.href"
            @change="$emit('change')"
            label="Link address"
            placeholder="https://"
          />
          
          <!-- File Upload -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Select file</label>
            
            <!-- Show uploaded file info -->
            <div v-if="block.props.src && block.props.fileName" class="border rounded-lg p-3 bg-gray-50">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <FeatherIcon name="image" class="w-4 h-4 text-green-600" />
                  <div>
                    <p class="text-sm font-medium text-gray-900">{{ block.props.fileName }}</p>
                    <p class="text-xs text-gray-500">{{ formatFileSize(block.props.fileSize) }}</p>
                  </div>
                </div>
                <div class="flex space-x-1">
                  <Button
                    size="sm"
                    variant="ghost"
                    @click="changeImage()"
                  >
                    <FeatherIcon name="edit-2" class="w-3 h-3" />
                  </Button>
                  <Button
                    size="sm"
                    variant="ghost"
                    @click="removeImage()"
                  >
                    <FeatherIcon name="trash-2" class="w-3 h-3" />
                  </Button>
                </div>
              </div>
            </div>
            
            <!-- File uploader (show when no file or changing) -->
            <FileUploader
              v-if="!block.props.src || showUploader"
              :fileTypes="['image/*']"
              :validateFile="(file) => {
                if (file.size > 5000000) {
                  return 'File size should be less than 5MB'
                }
              }"
              @success="(file) => {
                block.props.src = file.file_url
                block.props.fileName = file.file_name
                block.props.fileSize = file.file_size
                showUploader = false
                $emit('change')
              }"
            >
              <template #default="{ uploading, progress, error, openFileSelector }">
                <div>
                  <Button
                    @click="openFileSelector()"
                    :loading="uploading"
                    variant="outline"
                    class="w-full"
                  >
                    <template v-if="uploading">
                      Uploading {{ progress }}%
                    </template>
                    <template v-else>
                      <div class="flex items-center">
                        <FeatherIcon name="upload" class="w-4 h-4 mr-2" />
                        {{ block.props.src ? 'Change file' : 'Select file' }}
                      </div>
                    </template>
                  </Button>
                  <div v-if="error" class="text-red-500 text-xs mt-1">{{ error }}</div>
                </div>
              </template>
            </FileUploader>
          </div>
          
          <!-- Alt Text -->
          <FormControl
            type="text"
            v-model="block.props.alt"
            @change="$emit('change')"
            label="Alt text"
            placeholder="Brief description of your image"
          />
          
          <!-- Full Width on Mobile -->
          <div class="flex items-center space-x-2 mt-2">
            <input
              type="checkbox"
              v-model="block.props.fullWidthMobile"
              @change="$emit('change')"
              class="rounded"
            />
            <label class="text-sm font-medium text-gray-700">Full width on mobile</label>
          </div>
        </div>

        <!-- Dimension Section -->
        <div class="border-t pt-4 mt-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <FeatherIcon name="maximize-2" class="w-4 h-4 mr-2" />
            Dimension
          </h4>
          
          <!-- Width Type -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Width</label>
            <div class="flex gap-2">
              <Button
                :variant="block.props.widthType === 'fixed' ? 'solid' : 'outline'"
                size="sm"
                @click="setImageWidthType('fixed')"
              >
                Fixed
              </Button>
              <Button
                :variant="block.props.widthType === 'full' ? 'solid' : 'outline'"
                size="sm"
                @click="setImageWidthType('full')"
              >
                Full width
              </Button>
            </div>
          </div>
          
          <!-- Fixed Width Input -->
          <FormControl
            v-if="block.props.widthType === 'fixed'"
            type="number"
            v-model="block.props.width"
            @change="$emit('change')"
            label="Width (px)"
            placeholder="600"
            class="mt-2"
          />
          
          <!-- Height -->
          <FormControl
            type="number"
            v-model="block.props.height"
            @change="$emit('change')"
            label="Height (px)"
            placeholder="Auto"
            class="mt-2"
          />
          
          <!-- Padding -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Padding</label>
            <div class="grid grid-cols-2 gap-2">
              <FormControl
                type="number"
                v-model="block.props.paddingTop"
                @change="$emit('change')"
                placeholder="Top"
                size="sm"
              />
              <FormControl
                type="number"
                v-model="block.props.paddingBottom"
                @change="$emit('change')"
                placeholder="Bottom"
                size="sm"
              />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <FormControl
                type="number"
                v-model="block.props.paddingLeft"
                @change="$emit('change')"
                placeholder="Left"
                size="sm"
              />
              <FormControl
                type="number"
                v-model="block.props.paddingRight"
                @change="$emit('change')"
                placeholder="Right"
                size="sm"
              />
            </div>
          </div>
        </div>

        <!-- Border Section -->
        <div class="border-t pt-4 mt-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <FeatherIcon name="square" class="w-4 h-4 mr-2" />
            Border
          </h4>
          
          <!-- Border Toggle -->
          <div class="flex items-center space-x-2 mb-3">
            <input
              type="checkbox"
              v-model="block.props.hasBorder"
              @change="$emit('change')"
              class="rounded"
            />
            <label class="text-sm font-medium text-gray-700">Border</label>
          </div>
          
          <template v-if="block.props.hasBorder">
            <!-- Border Width -->
            <FormControl
              type="number"
              v-model="block.props.borderWidth"
              @change="$emit('change')"
              label="Border Width (px)"
              placeholder="1"
            />
            
            <!-- Border Color -->
            <FormControl
              type="color"
              v-model="block.props.borderColor"
              @change="$emit('change')"
              label="Border Color"
            />
          </template>
          
          <!-- Corner Radius -->
          <FormControl
            type="number"
            v-model="block.props.borderRadius"
            @change="$emit('change')"
            label="Corner radius (px)"
            placeholder="0"
          />
        </div>

        <!-- Block Section -->
        <div class="border-t pt-4 mt-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <FeatherIcon name="layout" class="w-4 h-4 mr-2" />
            Block
          </h4>
          
          <!-- Background Color -->
          <FormControl
            type="color"
            v-model="block.props.backgroundColor"
            @change="$emit('change')"
            label="Background color"
          />
          
          <!-- Image Alignment -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Align</label>
            <div class="flex gap-1">
              <Button
                :variant="block.props.align === 'left' ? 'solid' : 'outline'"
                size="sm"
                @click="setImageAlign('left')"
              >
                <FeatherIcon name="align-left" class="w-4 h-4" />
              </Button>
              <Button
                :variant="block.props.align === 'center' ? 'solid' : 'outline'"
                size="sm"
                @click="setImageAlign('center')"
              >
                <FeatherIcon name="align-center" class="w-4 h-4" />
              </Button>
              <Button
                :variant="block.props.align === 'right' ? 'solid' : 'outline'"
                size="sm"
                @click="setImageAlign('right')"
              >
                <FeatherIcon name="align-right" class="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </template>

      <!-- Divider Block Properties -->
      <template v-if="block.type === 'divider'">
        <!-- Line Section -->
        <div class="border-t pt-4 mt-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <FeatherIcon name="minus" class="w-4 h-4 mr-2" />
            Line
          </h4>
          
          <!-- Height -->
          <FormControl
            type="number"
            v-model="block.props.height"
            @change="$emit('change')"
            label="Height (px)"
            placeholder="4"
          />
          
          <!-- Style -->
          <FormControl
            type="select"
            v-model="block.props.style"
            @change="$emit('change')"
            label="Style"
            :options="[
              { label: 'Solid', value: 'solid' },
              { label: 'Dashed', value: 'dashed' },
              { label: 'Dotted', value: 'dotted' }
            ]"
          />
          
          <!-- Color -->
          <FormControl
            type="color"
            v-model="block.props.borderColor"
            @change="$emit('change')"
            label="Color"
          />
        </div>

        <!-- Dimension Section -->
        <div class="border-t pt-4 mt-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <FeatherIcon name="maximize-2" class="w-4 h-4 mr-2" />
            Dimension
          </h4>
          
          <!-- Width -->
          <FormControl
            type="select"
            v-model="block.props.width"
            @change="$emit('change')"
            label="Width"
            :options="[
              { label: '100%', value: '100%' },
              { label: '75%', value: '75%' },
              { label: '50%', value: '50%' },
              { label: '25%', value: '25%' },
              { label: 'Custom', value: 'custom' }
            ]"
          />
          
          <!-- Custom Width -->
          <FormControl
            v-if="block.props.width === 'custom'"
            type="number"
            v-model="block.props.customWidth"
            @change="$emit('change')"
            label="Custom Width (px)"
            placeholder="300"
          />
          
          <!-- Padding -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Padding</label>
            <div class="grid grid-cols-2 gap-2">
              <FormControl
                type="number"
                v-model="block.props.paddingTop"
                @change="$emit('change')"
                placeholder="Top"
                size="sm"
              />
              <FormControl
                type="number"
                v-model="block.props.paddingBottom"
                @change="$emit('change')"
                placeholder="Bottom"
                size="sm"
              />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <FormControl
                type="number"
                v-model="block.props.paddingLeft"
                @change="$emit('change')"
                placeholder="Left"
                size="sm"
              />
              <FormControl
                type="number"
                v-model="block.props.paddingRight"
                @change="$emit('change')"
                placeholder="Right"
                size="sm"
              />
            </div>
          </div>
        </div>

        <!-- Block Section -->
        <div class="border-t pt-4 mt-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <FeatherIcon name="square" class="w-4 h-4 mr-2" />
            Block
          </h4>
          
          <!-- Background Color -->
          <FormControl
            type="color"
            v-model="block.props.backgroundColor"
            @change="$emit('change')"
            label="Background color"
          />
          
          <!-- Divider Alignment -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Align</label>
            <div class="flex gap-1">
              <Button
                :variant="block.props.align === 'left' ? 'solid' : 'outline'"
                size="sm"
                @click="setDividerAlign('left')"
              >
                <FeatherIcon name="align-left" class="w-4 h-4" />
              </Button>
              <Button
                :variant="block.props.align === 'center' ? 'solid' : 'outline'"
                size="sm"
                @click="setDividerAlign('center')"
              >
                <FeatherIcon name="align-center" class="w-4 h-4" />
              </Button>
              <Button
                :variant="block.props.align === 'right' ? 'solid' : 'outline'"
                size="sm"
                @click="setDividerAlign('right')"
              >
                <FeatherIcon name="align-right" class="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </template>

      <!-- Spacer Block Properties -->
      <template v-if="block.type === 'spacer'">
        <!-- Height -->
        <FormControl
          type="number"
          v-model="block.props.height"
          @change="$emit('change')"
          label="Height (px)"
          placeholder="40"
        />
        
        <!-- Background Color -->
        <FormControl
          type="color"
          v-model="block.props.backgroundColor"
          @change="$emit('change')"
          label="Background Color"
        />
      </template>

      <!-- Common Padding Property (only for blocks without individual padding) -->
      <FormControl
        v-if="block.props.padding !== undefined && block.type !== 'button' && block.type !== 'text' && block.type !== 'divider' && block.type !== 'spacer' && block.type !== 'image'"
        type="number"
        v-model="block.props.padding"
        @change="$emit('change')"
        label="Padding (px)"
      />
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FormControl, Button, FileUploader, FeatherIcon } from 'frappe-ui'

const props = defineProps({
  block: {
    type: Object,
    default: null
  },
  showEmailSettings: {
    type: Boolean,
    default: false
  },
  emailSettings: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['close', 'change', 'update-email-settings', 'set-email-align'])

// Reactive data
const showUploader = ref(false)

// Toggle methods for text styling
function toggleFontWeight(weight) {
  if (!props.block) return
  props.block.props.fontWeight = props.block.props.fontWeight === weight ? 'normal' : weight
  emit('change')
}

function toggleFontStyle(style) {
  if (!props.block) return
  props.block.props.fontStyle = props.block.props.fontStyle === style ? 'normal' : style
  emit('change')
}

function toggleTextDecoration(decoration) {
  if (!props.block) return
  props.block.props.textDecoration = props.block.props.textDecoration === decoration ? 'none' : decoration
  emit('change')
}

function setTextAlign(align) {
  if (!props.block) return
  props.block.props.textAlign = align
  emit('change')
}

function setButtonAlign(align) {
  if (!props.block) return
  props.block.props.align = align
  emit('change')
}

function setDividerAlign(align) {
  if (!props.block) return
  props.block.props.align = align
  emit('change')
}

function setImageWidthType(type) {
  if (!props.block) return
  props.block.props.widthType = type
  emit('change')
}

function setImageAlign(align) {
  if (!props.block) return
  props.block.props.align = align
  emit('change')
}

// Image management methods
function changeImage() {
  showUploader.value = true
}

function removeImage() {
  if (!props.block) return
  props.block.props.src = ''
  props.block.props.fileName = ''
  props.block.props.fileSize = null
  showUploader.value = false
  emit('change')
}

function formatFileSize(bytes) {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

// Email settings method
function updateEmailSetting(key, value) {
  emit('update-email-settings', { [key]: value })
}
</script>

