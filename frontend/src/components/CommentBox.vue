<template>
  <TextEditor
    ref="textEditor"
    :editor-class="['prose-sm max-w-none', editable && 'min-h-[7rem]']"
    :content="content"
    @change="editable ? (content = $event) : null"
    :starterkit-options="{ heading: { levels: [2, 3, 4, 5, 6] } }"
    :placeholder="placeholder"
    :editable="editable"
    :mentions="users"
  >
    <template v-slot:editor="{ editor }">
      <EditorContent
        :class="[
          editable &&
            'sm:mx-10 mx-4 max-h-[50vh] overflow-y-auto border-t py-3',
        ]"
        :editor="editor"
      />
    </template>
    <template v-slot:bottom>
      <div v-if="editable" class="flex flex-col gap-2">
        <div class="flex flex-wrap gap-2 sm:px-10 px-4">
          <AttachmentItem
            v-for="a in attachments"
            :key="a.file_url"
            :label="a.file_name"
          >
            <template #suffix>
              <FeatherIcon
                class="h-3.5"
                name="x"
                @click.stop="removeAttachment(a)"
              />
            </template>
          </AttachmentItem>
        </div>
        <div
          class="flex justify-between gap-2 overflow-hidden border-t sm:px-10 px-4 py-2.5"
        >
          <div class="flex gap-1 items-center overflow-x-auto">
            <TextEditorBubbleMenu :buttons="textEditorMenuButtons" />
            <IconPicker
              v-model="emoji"
              v-slot="{ togglePopover }"
              @update:modelValue="() => appendEmoji()"
            >
              <Button variant="ghost" @click="togglePopover()">
                <template #icon>
                  <SmileIcon class="h-4" />
                </template>
              </Button>
            </IconPicker>
            <FileUploader
              :upload-args="{
                doctype: doctype,
                docname: modelValue.name,
                private: true,
              }"
              @success="(f) => attachments.push(f)"
            >
              <template #default="{ openFileSelector }">
                <Button
                  theme="gray"
                  variant="ghost"
                  @click="openFileSelector()"
                >
                  <template #icon>
                    <AttachmentIcon class="h-4" />
                  </template>
                </Button>
              </template>
            </FileUploader>
          </div>
          <div class="mt-2 flex items-center justify-end space-x-2 sm:mt-0">
            <Button v-bind="discardButtonProps || {}" :label="__('Discard')" />
            <Button
              variant="solid"
              v-bind="submitButtonProps || {}"
              :label="__('Comment')"
            />
          </div>
        </div>
      </div>
    </template>
  </TextEditor>
</template>
<script setup>
import IconPicker from '@/components/IconPicker.vue'
import SmileIcon from '@/components/Icons/SmileIcon.vue'
import AttachmentIcon from '@/components/Icons/AttachmentIcon.vue'
import AttachmentItem from '@/components/AttachmentItem.vue'
import { usersStore } from '@/stores/users'
import { sessionStore } from '@/stores/session'
import { TextEditorBubbleMenu, TextEditor, FileUploader, createResource } from 'frappe-ui'
import { capture } from '@/telemetry'
import { EditorContent } from '@tiptap/vue-3'
import { ref, computed, watch } from 'vue'

const props = defineProps({
  placeholder: {
    type: String,
    default: null,
  },
  editable: {
    type: Boolean,
    default: true,
  },
  doctype: {
    type: String,
    default: 'Mira Campaign',
  },
  editorProps: {
    type: Object,
    default: () => ({}),
  },
  submitButtonProps: {
    type: Object,
    default: () => ({}),
  },
  discardButtonProps: {
    type: Object,
    default: () => ({}),
  },
  hiringCommittee: {
    type: Array,
    default: () => [],
  },
})

const modelValue = defineModel()
const attachments = defineModel('attachments')
const content = defineModel('content')

const { users: usersList, getUser } = usersStore()
const session = sessionStore()

const textEditor = ref(null)
const emoji = ref('')

const editor = computed(() => {
  return textEditor.value.editor
})

function appendEmoji() {
  editor.value.commands.insertContent(emoji.value)
  editor.value.commands.focus()
  emoji.value = ''
  capture('emoji_inserted_in_comment', { emoji: emoji.value })
}

function removeAttachment(attachment) {
  attachments.value = attachments.value.filter((a) => a !== attachment)
}

const allowedUsersResource = createResource({
	url: "mbw_mira.api.roles.get_users_with_doctype_access",
	cache: ["allowed_users", props.doctype],
  auto: true,
	makeParams(values) {
		return {
			doctype: props.doctype,
		};
	},
});

watch(
	() => props.doctype,
	(newVal) => {
		if (newVal) {
			allowedUsersResource.fetch({ doctype: newVal });
		}
	},
	{ immediate: true },
);

const users = computed(() => {
	const currentUser = session.user; // User name hiện tại (ví dụ: "Administrator")
	const currentUserObj = getUser();
	const currentUserEmail = currentUserObj?.email; // Email của user hiện tại

	// Ưu tiên dùng hiringCommittee nếu có (trong Job Opening)
	if (props.hiringCommittee && props.hiringCommittee.length > 0) {
		return props.hiringCommittee
			.filter((member) => {
				// Bỏ qua user hiện tại (so sánh cả name và email)
				return member.user !== currentUser && member.user !== currentUserEmail;
			})
			.map((member) => ({
				label: getUser(member.user)?.full_name?.trimEnd() || member.user,
				value: member.user,
			}));
	}

	// Filter users theo danh sách từ backend
	if (allowedUsersResource.data) {
		return allowedUsersResource.data
			.filter((user) => {
				// Bỏ qua user hiện tại (so sánh cả name và email)
				return user.name !== currentUser && user.name !== currentUserEmail && 
				       user.email !== currentUser && user.email !== currentUserEmail;
			})
			.map((user) => ({
				label: user.full_name?.trimEnd() || user.name,
				value: user.name,
			}));
	}

	return [];
});

defineExpose({ editor })

const textEditorMenuButtons = [
  'Paragraph',
  ['Heading 2', 'Heading 3', 'Heading 4', 'Heading 5', 'Heading 6'],
  'Separator',
  'Bold',
  'Italic',
  'Separator',
  'Bullet List',
  'Numbered List',
  'Separator',
  'Align Left',
  'Align Center',
  'Align Right',
  'FontColor',
  'Separator',
  'Image',
  'Video',
  'Link',
  'Blockquote',
  'Code',
  'Horizontal Rule',
  [
    'InsertTable',
    'AddColumnBefore',
    'AddColumnAfter',
    'DeleteColumn',
    'AddRowBefore',
    'AddRowAfter',
    'DeleteRow',
    'MergeCells',
    'SplitCell',
    'ToggleHeaderColumn',
    'ToggleHeaderRow',
    'ToggleHeaderCell',
    'DeleteTable',
  ],
]
</script>
