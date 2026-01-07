<template>
	<ActivityHeader
		v-model="tabIndex"
		v-model:showFilesUploader="showFilesUploader"
		:tabs="tabs"
		:title="title"
		:doc="doc"
		:emailBox="emailBox"
		:modalRef="modalRef"
	/>

	<FadedScrollableDiv
		ref="scrollableArea"
		:maskHeight="30"
		class="flex flex-col flex-1 overflow-y-auto"
	>
		<div
			v-if="all_activities?.loading && !activities?.length"
			class="flex flex-1 flex-col items-center justify-center gap-3 text-xl font-medium text-gray-500"
		>
			<LoadingIndicator class="h-6 w-6" />
			<span>{{ __("Loading...") }}</span>
		</div>
		<div v-else-if="activities?.length" class="activities">
			<div v-if="title == 'Comments'" class="pb-5">
				<div v-for="(comment, i) in activities" :key="comment.name || i">
					<div
						class="activity grid grid-cols-[30px_minmax(auto,_1fr)] gap-2 px-3 sm:gap-4 sm:px-10"
					>
						<div
							class="relative flex justify-center after:absolute after:left-[50%] after:top-0 after:-z-10 after:border-l after:border-gray-200"
							:class="i != activities.length - 1 ? 'after:h-full' : 'after:h-4'"
						>
							<div class="z-10 flex h-8 w-7 items-center justify-center bg-white">
								<CommentIcon class="text-gray-800" />
							</div>
						</div>
						<CommentArea class="mb-4" :activity="comment" />
					</div>
				</div>
			</div>

			<div v-else-if="title == 'Attachments'" class="px-3 pb-3 sm:px-10 sm:pb-5">
				<AttachmentArea
					:attachments="activities"
					@reload="all_activities.reload() && scroll()"
				/>
			</div>
			<div
				v-else
				v-for="(activity, i) in activities"
				class="activity px-3 sm:px-10"
				:class="
					['Activity', 'Emails'].includes(title)
						? 'grid grid-cols-[30px_minmax(auto,_1fr)] gap-2 sm:gap-4'
						: ''
				"
			>
				<div
					v-if="['Activity', 'Emails'].includes(title)"
					class="relative flex justify-center before:absolute before:left-[50%] before:top-0 before:-z-10 before:border-l before:border-gray-200"
					:class="[i != activities.length - 1 ? 'before:h-full' : 'before:h-4']"
				>
					<div
						class="z-10 flex h-7 w-7 items-center justify-center bg-white"
						:class="{
							'mt-2.5': ['communication'].includes(activity.activity_type),
							'bg-white': ['added', 'removed', 'changed'].includes(
								activity.activity_type,
							),
							'h-8': [
								'comment',
								'communication',
								'incoming_call',
								'outgoing_call',
							].includes(activity.activity_type),
						}"
					>
						<component
							:is="activity.icon"
							:class="
								['added', 'removed', 'changed'].includes(activity.activity_type)
									? 'text-gray-500'
									: 'text-gray-800'
							"
						/>
					</div>
				</div>
				<div
					class="mb-4"
					:id="activity.name"
					v-else-if="activity.activity_type == 'comment'"
				>
					<CommentArea :activity="activity" />
				</div>
				<div
					class="mb-4 flex flex-col gap-2 py-1.5"
					:id="activity.name"
					v-else-if="activity.activity_type == 'attachment_log'"
				>
					<div class="flex items-center justify-stretch gap-2 text-base">
						<div
							class="inline-flex items-center flex-wrap gap-1.5 text-gray-800 font-medium"
						>
							<span class="font-medium">{{ activity.owner_name }}</span>
							<span class="text-gray-600">{{ __(activity.data.type) }}</span>
							<a
								v-if="activity.data.file_url"
								:href="activity.data.file_url"
								target="_blank"
							>
								<span>{{ activity.data.file_name }}</span>
							</a>
							<span v-else>{{ activity.data.file_name }}</span>
							<FeatherIcon
								v-if="activity.data.is_private"
								name="lock"
								class="size-3"
							/>
						</div>
						<div class="ml-auto whitespace-nowrap">
							<Tooltip :text="dateFormat(activity.creation, dateTooltipFormat)">
								<div class="text-sm text-gray-600">
									{{ __(timeAgo(activity.creation)) }}
								</div>
							</Tooltip>
						</div>
					</div>
				</div>
				<div v-else class="mb-4 flex flex-col gap-2 py-1.5">
					<div class="flex items-center justify-stretch gap-2 text-base">
						<div
							v-if="activity.other_versions"
							class="inline-flex flex-wrap gap-1.5 text-gray-800 font-medium"
						>
							<span>{{ activity.show_others ? __("Hide") : __("Show") }}</span>
							<span> +{{ activity.other_versions.length + 1 }} </span>
							<span>{{ __("changes from") }}</span>
							<span>{{ activity.owner_name }}</span>
							<Button
								class="!size-4"
								variant="ghost"
								@click="activity.show_others = !activity.show_others"
							>
								<template #icon>
									<SelectIcon />
								</template>
							</Button>
						</div>
						<div v-else class="inline-flex items-center flex-wrap gap-1 text-gray-600">
							<span class="font-medium text-gray-800">
								{{ activity.owner_name }}
							</span>
							<span v-if="activity.type">{{ __(activity.type) }}</span>
							<span
								v-if="activity.data.field_label"
								class="max-w-xs truncate font-medium text-gray-800"
							>
								{{ __(activity.data.field_label) }}
							</span>
							<span v-if="activity.value">{{ __(activity.value) }}</span>
							<span
								v-if="activity.data.old_value"
								class="max-w-xs font-medium text-gray-800"
							>
								<div
									class="flex items-center gap-1"
									v-if="activity.options == 'User'"
								>
									<UserAvatar :user="activity.data.old_value" size="xs" />
									{{ getUser(activity.data.old_value).full_name }}
								</div>
								<div class="truncate" v-else>
									{{ activity.data.old_value }}
								</div>
							</span>
							<span v-if="activity.to">{{ __("to") }}</span>
							<span
								v-if="activity.data.value"
								class="max-w-xs font-medium text-gray-800"
							>
								<div
									class="flex items-center gap-1"
									v-if="activity.options == 'User'"
								>
									<UserAvatar :user="activity.data.value" size="xs" />
									{{ getUser(activity.data.value).full_name }}
								</div>
								<div class="truncate" v-else>
									{{ activity.data.value }}
								</div>
							</span>
						</div>

						<div class="ml-auto whitespace-nowrap">
							<Tooltip :text="dateFormat(activity.creation, dateTooltipFormat)">
								<div class="text-sm text-gray-600">
									{{ __(timeAgo(activity.creation)) }}
								</div>
							</Tooltip>
						</div>
					</div>
					<div
						v-if="activity.other_versions && activity.show_others"
						class="flex flex-col gap-0.5"
					>
						<div
							v-for="activity in [activity, ...activity.other_versions]"
							class="flex items-start justify-stretch gap-2 py-1.5 text-base"
						>
							<div class="inline-flex flex-wrap gap-1 text-gray-600">
								<span
									v-if="activity.data.field_label"
									class="max-w-xs truncate text-gray-600"
								>
									{{ __(activity.data.field_label) }}
								</span>
								<FeatherIcon
									name="arrow-right"
									class="mx-1 h-4 w-4 text-gray-600"
								/>
								<span v-if="activity.type">
									{{ startCase(__(activity.type)) }}
								</span>
								<span
									v-if="activity.data.old_value"
									class="max-w-xs font-medium text-gray-800"
								>
									<div
										class="flex items-center gap-1"
										v-if="activity.options == 'User'"
									>
										<UserAvatar :user="activity.data.old_value" size="xs" />
										{{ getUser(activity.data.old_value).full_name }}
									</div>
									<div class="truncate" v-else>
										{{ activity.data.old_value }}
									</div>
								</span>
								<span v-if="activity.to">{{ __("to") }}</span>
								<span
									v-if="activity.data.value"
									class="max-w-xs font-medium text-gray-800"
								>
									<div
										class="flex items-center gap-1"
										v-if="activity.options == 'User'"
									>
										<UserAvatar :user="activity.data.value" size="xs" />
										{{ getUser(activity.data.value).full_name }}
									</div>
									<div class="truncate" v-else>
										{{ activity.data.value }}
									</div>
								</span>
							</div>

							<div class="ml-auto whitespace-nowrap">
								<Tooltip :text="dateFormat(activity.creation, dateTooltipFormat)">
									<div class="text-sm text-gray-600">
										{{ __(timeAgo(activity.creation)) }}
									</div>
								</Tooltip>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div
			v-else
			class="flex flex-1 flex-col items-center justify-center gap-3 text-xl font-medium text-gray-500 py-8"
		>
			<component :is="emptyTextIcon" class="h-10 w-10" />
			<span>{{ __(emptyText) }}</span>

			<Button
				v-if="title == 'Attachments'"
				:label="__('Upload Attachment')"
				@click="showFilesUploader = true"
				class="mt-2"
			/>
			<Button
				v-else-if="title == 'Comments'"
				:label="__('New Comment')"
				@click="emailBox.showComment = true"
				class="mt-2"
			/>
		</div>
	</FadedScrollableDiv>

	<div>
		<CommunicationArea
			ref="emailBox"
			v-if="['Comments', 'Activity'].includes(title)"
			v-model="doc"
			v-model:reload="reload_email"
			:doctype="doctype"
			:hiringCommittee="doc.data?.hiring_committee || doc?.hiring_committee || []"
			@scroll="scroll"
		/>
	</div>
	<FilesUploader
		v-if="doc.data?.name || doc?.name"
		v-model="showFilesUploader"
		:doctype="doctype"
		:docname="doc.data?.name || doc?.name"
		@after="
			() => {
				all_activities.reload();
				changeTabTo('attachments');
			}
		"
	/>
</template>
<script setup>
import ActivityHeader from "@/components/Activities/ActivityHeader.vue";
import CommentArea from "@/components/Activities/CommentArea.vue";
import AttachmentArea from "@/components/Activities/AttachmentArea.vue";
import UserAvatar from "@/components/UserAvatar.vue";
import ActivityIcon from "@/components/Icons/ActivityIcon.vue";
import CommentIcon from "@/components/Icons/CommentIcon.vue";
import AttachmentIcon from "@/components/Icons/AttachmentIcon.vue";
import DetailsIcon from "@/components/Icons/DetailsIcon.vue";
import DotIcon from "@/components/Icons/DotIcon.vue";
import SelectIcon from "@/components/Icons/SelectIcon.vue";
import LoadingIndicator from "@/components/Icons/LoadingIndicator.vue";
import FadedScrollableDiv from "@/components/FadedScrollableDiv.vue";
import CommunicationArea from "@/components/CommunicationArea.vue";
import FilesUploader from "@/components/FilesUploader/FilesUploader.vue";
import { timeAgo, dateFormat, dateTooltipFormat, startCase } from "@/utils";
import { globalStore } from "@/stores/global";
import { usersStore } from "@/stores/users";
import { Button, Tooltip, createResource } from "frappe-ui";
import {
	ref,
	computed,
	h,
	markRaw,
	watch,
	nextTick,
	onMounted,
	onBeforeUnmount,
} from "vue";
import { useRoute } from "vue-router";
import { FeatherIcon } from "frappe-ui";

const { $socket } = globalStore();
const { getUser } = usersStore();

const props = defineProps({
	doctype: {
		type: String,
		default: "Mira Campaign",
	},
	tabs: {
		type: Array,
		default: () => [],
	},
});

const route = useRoute();
const doc = defineModel();
const reload = defineModel("reload");
const tabIndex = defineModel("tabIndex");

const currentDocname = computed(() => doc.value?.data?.name || doc.value?.name);
const currentDoctype = computed(() => props.doctype);

const subscribedDoc = ref(null);

function subscribeDocRoom(doctype, docname) {
	if (!doctype || !docname || !$socket) return;
	if (subscribedDoc.value?.doctype === doctype && subscribedDoc.value?.docname === docname)
		return;

	if (subscribedDoc.value?.doctype && subscribedDoc.value?.docname) {
		$socket.emit(
			"doc_unsubscribe",
			subscribedDoc.value.doctype,
			subscribedDoc.value.docname,
		);
	}

	$socket.emit("doc_subscribe", doctype, docname);
	subscribedDoc.value = { doctype, docname };
}

function unsubscribeDocRoom() {
	if (!subscribedDoc.value?.doctype || !subscribedDoc.value?.docname || !$socket) return;
	$socket.emit(
		"doc_unsubscribe",
		subscribedDoc.value.doctype,
		subscribedDoc.value.docname,
	);
	subscribedDoc.value = null;
}

const reload_email = ref(false);
const modalRef = ref(null);
const showFilesUploader = ref(false);

const title = computed(() => props.tabs?.[tabIndex.value]?.name || "Activity");

const changeTabTo = (tabName) => {
	const tabNames = props.tabs?.map((tab) => tab.name?.toLowerCase());
	const index = tabNames?.indexOf(tabName);
	if (index == -1) return;
	tabIndex.value = index;
};

const scrollableArea = ref(null);

function getScrollableEl() {
	return scrollableArea.value?.$el || scrollableArea.value;
}

function captureScrollState() {
	const el = getScrollableEl();
	if (!el) return null;
	const distanceToBottom = el.scrollHeight - (el.scrollTop + el.clientHeight);
	return {
		scrollTop: el.scrollTop,
		scrollHeight: el.scrollHeight,
		atBottom: distanceToBottom < 40,
	};
}

async function restoreScrollState(state) {
	const el = getScrollableEl();
	if (!el || !state) return;
	await nextTick();
	if (state.atBottom) {
		el.scrollTop = el.scrollHeight;
	} else {
		el.scrollTop = state.scrollTop;
	}
}

const all_activities = createResource({
	url: "mbw_transition_hub.api.activities.get_activities",
	params: { name: currentDocname.value },
	cache: () => ["activity", currentDocname.value],
	auto: true,
	transform: ([versions, calls, notes, tasks, attachments]) => {
		return { versions, calls, notes, tasks, attachments };
	},
});

const _rawReloadActivities = all_activities.reload.bind(all_activities);
all_activities.reload = async (...args) => {
	const state = captureScrollState();
	const result = await _rawReloadActivities(...args);
	await restoreScrollState(state);
	return result;
};

watch(currentDocname, (name) => {
	if (name) {
		all_activities.params = { name: name };
		all_activities.reload();
	}
}, { immediate: true });

// Scroll to bottom when component mounts or when switching to this tab
onMounted(() => {
	nextTick(() => {
		const hash = route.hash.slice(1) || null;
		let tabNames = props.tabs?.map((tab) => tab.name?.toLowerCase());
		
		// On mount: scroll to bottom for Activity/Comments tabs
		if (hash && tabNames?.includes(hash.toLowerCase())) {
			// Hash is a tab name - scroll to bottom
			scroll();
		} else if (hash) {
			// Hash is a specific element ID - scroll to that element
			scroll(hash);
		} else {
			// No hash - scroll to bottom by default
			scroll();
		}
	});
});

// Track if component is mounted
const isMounted = ref(false);
onMounted(() => {
	isMounted.value = true;
});
onBeforeUnmount(() => {
	isMounted.value = false;
});

// Debounce scroll to prevent race conditions when switching tabs quickly
let scrollTimeout = null;

// Watch tabIndex to scroll when switching to Activity/Comments tab
watch(
	tabIndex,
	(newIndex, oldIndex) => {
		// Cancel any pending scroll
		if (scrollTimeout) {
			clearTimeout(scrollTimeout);
			scrollTimeout = null;
		}
		
		if (newIndex !== oldIndex && isMounted.value) {
			const currentTabName = props.tabs?.[newIndex]?.name;
			// If switching to Activity, Comments, or Attachments tab, scroll to bottom
			if (['Activity', 'Comments', 'Attachments'].includes(currentTabName)) {
				scrollTimeout = setTimeout(() => {
					if (isMounted.value) {
						scroll();
					}
					scrollTimeout = null;
				}, 100);
			}
		}
	}
);

function handleSocketConnect() {
	subscribeDocRoom(currentDoctype.value, currentDocname.value);
}

function handleNewComment(data) {
    if (data.reference_doctype !== currentDoctype.value || data.reference_name !== currentDocname.value) return;
    
    // Check duplication
    if (all_activities.data?.versions?.some(c => c.name === data.name)) return;

    if (all_activities.data?.versions) {
        all_activities.data.versions.unshift(data);
    } else {
        all_activities.reload();
    }
}

onMounted(() => {
	$socket?.on?.("connect", handleSocketConnect);
    $socket?.on?.("mbw_transition_hub:comment_added", handleNewComment);
});

onBeforeUnmount(() => {
	$socket?.off?.("connect", handleSocketConnect);
    $socket?.off?.("mbw_transition_hub:comment_added", handleNewComment);
	unsubscribeDocRoom();
});

watch(
	[currentDoctype, currentDocname],
	([doctype, docname]) => {
		if (doctype && docname) {
			subscribeDocRoom(doctype, docname);
		}
	},
	{ immediate: true },
);

watch(
	() => route.hash.slice(1),
	(newValue, oldValue) => {
		if (newValue && newValue !== oldValue) {
			let tabNames = props.tabs?.map((tab) => tab.name?.toLowerCase());
			// Only scroll if hash is a specific element ID (not a tab name)
			if (!tabNames?.includes(newValue.toLowerCase())) {
				scroll(newValue);
			}
		}
	},
	{ immediate: false },
);

function get_activities() {
	if (!all_activities.data?.versions) return [];
	return all_activities.data.versions || [];
}

const activities = computed(() => {
	let _activities = [];
	if (title.value == "Activity") {
		_activities = get_activities();
	} else if (title.value == "Comments") {
		if (!all_activities.data?.versions) return [];
		_activities = all_activities.data.versions.filter(
			(activity) => activity.activity_type === "comment",
		);
	} else if (title.value == "Attachments") {
		if (!all_activities.data?.attachments) return [];
		return sortByCreation(all_activities.data.attachments);
	}

	_activities.forEach((activity) => {
		activity.icon = timelineIcon(activity.activity_type, activity.is_lead);

		if (
			activity.activity_type == "incoming_call" ||
			activity.activity_type == "outgoing_call" ||
			activity.activity_type == "communication"
		)
			return;

		update_activities_details(activity);

		if (activity.other_versions) {
			activity.show_others = false;
			activity.other_versions.forEach((other_version) => {
				update_activities_details(other_version);
			});
		}
	});
	return sortByCreation(_activities);
});

function sortByCreation(list) {
	return list.sort((a, b) => new Date(a.creation) - new Date(b.creation));
}

function update_activities_details(activity) {
	activity.owner_name = getUser(activity.owner).full_name;
	activity.type = "";
	activity.value = "";
	activity.to = "";

	if (activity.activity_type == "creation") {
		activity.type = activity.data;
	} else if (activity.activity_type == "added") {
		activity.type = "added";
		activity.value = "as";
	} else if (activity.activity_type == "removed") {
		activity.type = "removed";
		activity.value = "value";
	} else if (activity.activity_type == "changed") {
		activity.type = "changed";
		activity.value = "from";
		activity.to = "to";
	}
}

const emptyText = computed(() => {
	let text = "No Activities";
	if (title.value == "Comments") {
		text = "No Comments";
	} else if (title.value == "Attachments") {
		text = "No Attachments";
	} else if (title.value == "Data") {
		text = "No Data";
	}
	return text;
});

const emptyTextIcon = computed(() => {
	let icon = ActivityIcon;

	if (title.value == "Comments") {
		icon = CommentIcon;
	} else if (title.value == "Attachments") {
		icon = AttachmentIcon;
	} else if (title.value == "Data") {
		icon = DetailsIcon;
	}

	return h(icon, { class: "text-gray-500" });
});

function timelineIcon(activity_type, is_lead) {
	let icon;
	switch (activity_type) {
		case "creation":
			icon = DotIcon;
			break;
		case "comment":
			icon = CommentIcon;
			break;
		case "attachment_log":
			icon = AttachmentIcon;
			break;
		default:
			icon = DotIcon;
	}

	return markRaw(icon);
}

const emailBox = ref(null);

watch([reload, reload_email], ([reload_value, reload_email_value]) => {
	if (reload_value || reload_email_value) {
		all_activities.reload();
		reload.value = false;
		reload_email.value = false;
	}
});

function scroll(hash) {
	if (["tasks", "notes"].includes(route.hash?.slice(1))) return;
	setTimeout(() => {
		const scrollContainer = getScrollableEl();
		if (!scrollContainer) return;
		
		let el;
		if (!hash) {
			// Smooth scroll to bottom of the scrollable container
			scrollContainer.scrollTo({
				top: scrollContainer.scrollHeight,
				behavior: "smooth"
			});
		} else {
			el = document.getElementById(hash);
			if (el) {
				// Calculate position relative to scroll container and scroll there
				const containerRect = scrollContainer.getBoundingClientRect();
				const elRect = el.getBoundingClientRect();
				const relativeTop = elRect.top - containerRect.top + scrollContainer.scrollTop;
				scrollContainer.scrollTo({
					top: relativeTop - 50, // 50px offset from top
					behavior: "smooth"
				});
				el.focus();
			}
		}
	}, 500);
}

watch(
	() => doc,
	(newVal) => {
		if (newVal) {
			all_activities.reload();
		}
	},
	{ immediate: true, deep: true },
);

defineExpose({ emailBox, all_activities });
</script>

