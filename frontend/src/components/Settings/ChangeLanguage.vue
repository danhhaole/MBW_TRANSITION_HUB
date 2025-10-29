<template>
	<Dialog
		v-model="showLanguage"
		:options="{ size: 'lg', position: 'top' }"
		class="z-50"
	>
		<template #body>
			<div>
				<div class="flex flex-col p-2 border-b relative">
					<h1 class="mb-3 px-2 pt-2 text-lg font-semibold text-ink-gray-9">
						{{ __('Select language') }}
					</h1>
					<Button
						class="absolute right-5 top-3.5"
						variant="ghost"
						icon="x"
						@click="showLanguage = false"
					/>
				</div>
				<div
					class="flex flex-1 flex-col overflow-y-auto bg-surface-modal mb-4 px-4 pt-3"
				>
					<Autocomplete
						:options="optionsLanguage"
						v-model="single"
						placeholder="Select language"
						:hideSearch="true"
					>
						<template #prefix>
							<img :src="single.image" class="mr-2 h-4.5 w-7" />
						</template>
						<template #item-prefix="{ option }">
							<img :src="option.image.toString()" class="h-4.5 w-7 mr-2" />
						</template>
					</Autocomplete>
				</div>
			</div>
		</template>
	</Dialog>
</template>
<script setup>
import {
	showLanguage,
	defaultLanguage,
	fetchLanguage,
	changeLanguage,
} from '@/composables/language.js'
import { Dialog, Button, Autocomplete } from 'frappe-ui'
import { ref, watch, computed, onMounted } from 'vue'
import { sessionStore } from '@/stores/session'
const { user } = sessionStore()

const optionsLanguage = computed(() => [
	{
		label: __('Vietnamese'),
		value: 'vi',
		image: '/assets/mbw_ats/images/icon_flag_vi.svg',
	},
	{
		label: __('English'),
		value: 'en',
		image: '/assets/mbw_ats/images/icon_flag_en.svg',
	},
])
const single = ref()

onMounted(() => {
	let lang = localStorage.getItem('lang')
	if (user) {
		if (!lang) {
			fetchLanguage.fetch()
		} else {
			changeLanguage.submit({ lang })
		}
	}
})

const setDefaultLanguage = (lang) => {
	localStorage.setItem('lang', lang)
	defaultLanguage.value = lang
}

watch(
	defaultLanguage,
	(val) => {
		single.value = optionsLanguage.value.find((item) => item.value === val)
	},
	{
		immediate: true,
	},
)

watch(single, (val) => {
	if (val.value === defaultLanguage.value) return

	setDefaultLanguage(val.value)
	if (user) {
		changeLanguage.submit(
			{ lang: val.value },
			{
				onSuccess: () => {
					window.location.reload()
				},
			},
		)
	} else {
		window.location.reload()
	}
})
</script>
