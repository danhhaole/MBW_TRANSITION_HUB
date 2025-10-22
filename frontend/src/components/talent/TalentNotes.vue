<template>
  <div class="space-y-6">
    <!-- Add Note Form -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Add Note</h3>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Note</label>
          <textarea 
            v-model="newNote"
            rows="4"
            class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Add a note about this talent..."
          ></textarea>
        </div>
        <div class="flex items-center space-x-4">
          <div class="flex items-center">
            <input
              id="private-note"
              v-model="isPrivate"
              type="checkbox"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            >
            <label for="private-note" class="ml-2 block text-sm text-gray-700">
              Private note (only visible to you)
            </label>
          </div>
        </div>
        <div class="flex justify-end">
          <Button @click="addNote" :disabled="!newNote.trim()">
            <template #prefix>
              <FeatherIcon name="plus" class="h-4 w-4" />
            </template>
            Add Note
          </Button>
        </div>
      </div>
    </div>

    <!-- Notes List -->
    <div class="bg-white rounded-lg border border-gray-200">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">Notes & Comments</h3>
      </div>
      <div class="divide-y divide-gray-200">
        <div v-for="note in notes" :key="note.id" class="p-6">
          <div class="flex items-start space-x-4">
            <div class="flex-shrink-0">
              <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-medium">
                {{ getUserInitials(note.author) }}
              </div>
            </div>
            <div class="flex-1">
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center space-x-2">
                  <p class="text-sm font-medium text-gray-900">{{ note.author }}</p>
                  <Badge v-if="note.isPrivate" theme="red" variant="subtle" class="text-xs">
                    Private
                  </Badge>
                </div>
                <div class="flex items-center space-x-2">
                  <p class="text-xs text-gray-500">{{ note.timeAgo }}</p>
                  <Dropdown :options="getNoteActions(note)" placement="bottom-end">
                    <template #default="{ open }">
                      <Button variant="ghost" size="sm" class="p-1">
                        <FeatherIcon name="more-horizontal" class="w-4 h-4" />
                      </Button>
                    </template>
                  </Dropdown>
                </div>
              </div>
              <div class="prose prose-sm max-w-none">
                <p class="text-gray-700 whitespace-pre-wrap">{{ note.content }}</p>
              </div>
              <div v-if="note.attachments && note.attachments.length" class="mt-3 flex flex-wrap gap-2">
                <div
                  v-for="attachment in note.attachments"
                  :key="attachment.name"
                  class="flex items-center space-x-2 bg-gray-50 rounded-lg px-3 py-2"
                >
                  <FeatherIcon name="paperclip" class="w-4 h-4 text-gray-400" />
                  <span class="text-sm text-gray-700">{{ attachment.file_name }}</span>
                  <Button variant="ghost" size="sm" @click="downloadAttachment(attachment)">
                    <FeatherIcon name="download" class="w-3 h-3" />
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Note Categories -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Note Categories</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="text-center p-4 bg-blue-50 rounded-lg">
          <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
            <FeatherIcon name="user" class="w-4 h-4 text-blue-600" />
          </div>
          <p class="text-sm font-medium text-blue-900">Personal</p>
          <p class="text-xs text-blue-600">{{ getNotesCount('personal') }} notes</p>
        </div>
        
        <div class="text-center p-4 bg-green-50 rounded-lg">
          <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
            <FeatherIcon name="briefcase" class="w-4 h-4 text-green-600" />
          </div>
          <p class="text-sm font-medium text-green-900">Professional</p>
          <p class="text-xs text-green-600">{{ getNotesCount('professional') }} notes</p>
        </div>
        
        <div class="text-center p-4 bg-purple-50 rounded-lg">
          <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-2">
            <FeatherIcon name="phone" class="w-4 h-4 text-purple-600" />
          </div>
          <p class="text-sm font-medium text-purple-900">Interview</p>
          <p class="text-xs text-purple-600">{{ getNotesCount('interview') }} notes</p>
        </div>
        
        <div class="text-center p-4 bg-orange-50 rounded-lg">
          <div class="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-2">
            <FeatherIcon name="star" class="w-4 h-4 text-orange-600" />
          </div>
          <p class="text-sm font-medium text-orange-900">Feedback</p>
          <p class="text-xs text-orange-600">{{ getNotesCount('feedback') }} notes</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FeatherIcon, Button, Badge, Dropdown } from 'frappe-ui'

const props = defineProps({
  talent: {
    type: Object,
    required: true
  }
})

const newNote = ref('')
const isPrivate = ref(false)

// Mock notes data
const notes = ref([
  {
    id: 1,
    content: 'Candidate has excellent technical skills in Vue.js and React. Very responsive during our initial conversation.',
    author: 'Sarah Wilson',
    timeAgo: '2 hours ago',
    isPrivate: false,
    category: 'professional',
    attachments: []
  },
  {
    id: 2,
    content: 'Phone interview went well. Candidate showed strong problem-solving skills and good communication. Recommended for technical round.',
    author: 'Mike Johnson',
    timeAgo: '1 day ago',
    isPrivate: false,
    category: 'interview',
    attachments: [
      { name: 'interview_notes.pdf', file_name: 'Interview Notes.pdf' }
    ]
  },
  {
    id: 3,
    content: 'Personal note: Remember to follow up on salary expectations. Candidate mentioned flexibility on remote work.',
    author: 'Jane Smith',
    timeAgo: '3 days ago',
    isPrivate: true,
    category: 'personal',
    attachments: []
  },
  {
    id: 4,
    content: 'Great feedback from the technical team. Code quality is excellent and candidate demonstrated good understanding of our tech stack.',
    author: 'Tech Team',
    timeAgo: '1 week ago',
    isPrivate: false,
    category: 'feedback',
    attachments: []
  }
])

const getUserInitials = (name) => {
  if (!name) return 'U'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const getNotesCount = (category) => {
  return notes.value.filter(note => note.category === category).length
}

const getNoteActions = (note) => {
  return [
    {
      label: 'Edit',
      icon: 'edit',
      onClick: () => editNote(note)
    },
    {
      label: 'Delete',
      icon: 'trash-2',
      onClick: () => deleteNote(note)
    }
  ]
}

const addNote = () => {
  if (!newNote.value.trim()) return
  
  notes.value.unshift({
    id: Date.now(),
    content: newNote.value,
    author: 'Current User',
    timeAgo: 'Just now',
    isPrivate: isPrivate.value,
    category: 'personal',
    attachments: []
  })
  
  // Reset form
  newNote.value = ''
  isPrivate.value = false
}

const editNote = (note) => {
  // TODO: Implement edit functionality
  console.log('Edit note:', note)
}

const deleteNote = (note) => {
  // TODO: Implement delete functionality
  const index = notes.value.findIndex(n => n.id === note.id)
  if (index > -1) {
    notes.value.splice(index, 1)
  }
}

const downloadAttachment = (attachment) => {
  // TODO: Implement download functionality
  console.log('Download attachment:', attachment)
}
</script>
