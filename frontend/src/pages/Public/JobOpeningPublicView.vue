<template>
	<div class="min-h-screen bg-gray-50 w-full">
		<!-- Loading State -->
		<div v-if="loading" class="flex justify-center items-center min-h-screen">
			<div class="animate-spin rounded-full h-32 w-32 border-b-2 border-green-600"></div>
		</div>

		<!-- Error State -->
		<div v-else-if="error" class="flex justify-center items-center min-h-screen">
			<div class="text-center">
				<div class="text-red-600 text-xl mb-4">{{ error }}</div>
				<Button @click="loadJobData" variant="solid">{{ __("Try again") }}</Button>
			</div>
		</div>

		<!-- Main Content -->
		<div v-else-if="jobData" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 lg:py-8">
			<div class="grid grid-cols-1 xl:grid-cols-3 gap-4 sm:gap-6 lg:gap-8">
				<!-- Left -->
				<div class="xl:col-span-2 flex flex-col gap-4 sm:gap-6">
					<!-- Header Card -->
					<div class="card flex flex-col gap-4">
						<h1 class="card-title">
							{{ jobData.job_title }}
						</h1>

						<!-- Info Grid -->
						<div class="info-grid">
							<!-- Salary -->
							<div class="info-item">
								<div class="info-icon">
									<svg fill="currentColor" viewBox="0 0 20 20">
										<path
											d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z"
										/>
										<path
											fill-rule="evenodd"
											d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z"
											clip-rule="evenodd"
										/>
									</svg>
								</div>
								<div>
									<div class="info-label">{{ __("Salary") }}</div>
									<div class="info-value">
										{{
											jobData.jo_min_salary || jobData.jo_max_salary
												? formatSalary(
														jobData.jo_min_salary,
														jobData.jo_max_salary,
														jobData.jo_currency,
													)
												: "Thỏa thuận"
										}}
									</div>
								</div>
							</div>

							<!-- Location -->
							<div class="info-item">
								<div class="info-icon">
									<svg fill="currentColor" viewBox="0 0 20 20">
										<path
											fill-rule="evenodd"
											d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
											clip-rule="evenodd"
										/>
									</svg>
								</div>
								<div>
									<div class="info-label">{{ __("Work location") }}</div>
									<div class="info-value">
										{{ jobData.location_name || "Chưa cập nhật" }}
									</div>
								</div>
							</div>

							<!-- Work form -->
							<div class="info-item">
								<div class="info-icon">
									<svg fill="currentColor" viewBox="0 0 20 20">
										<path
											fill-rule="evenodd"
											d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
											clip-rule="evenodd"
										/>
									</svg>
								</div>
								<div>
									<div class="info-label">{{ __("Work form") }}</div>
									<div class="info-value">
										{{ jobData.jo_work_form || "Chưa cập nhật" }}
									</div>
								</div>
							</div>
						</div>

						<!-- Deadline -->
						<div class="flex items-center space-x-2 text-gray-500">
							<svg class="w-[18px] h-[18px]" fill="currentColor" viewBox="0 0 20 20">
								<path
									fill-rule="evenodd"
									d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
									clip-rule="evenodd"
								/>
							</svg>
							<span class="text-[14px]">
								{{ __("Application deadline") }}:
								{{ formatDate(jobData.closing_date) }}
							</span>
						</div>

						<!-- Apply button (chuẩn theo btn-primary) -->
						<div class="flex">
							<div class="w-full">
								<input type="file" accept=".pdf,.doc,.docx,.txt" class="hidden" />
								<button
									class="btn-primary !h-10 !rounded-sm w-full disabled:!bg-gray-400 disabled:cursor-not-allowed"
									:disabled="isDeadlinePassed"
									@click="showApplyModal = true"
								>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										width="20"
										height="20"
										viewBox="0 0 24 24"
										fill="none"
										stroke="currentColor"
										stroke-width="2"
										stroke-linecap="round"
										stroke-linejoin="round"
										class="lucide lucide-send-icon lucide-send"
									>
										<path
											d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"
										></path>
										<path d="m21.854 2.147-10.94 10.939"></path>
									</svg>
									<span class="font-semibold text-[14px]">
										{{
											isDeadlinePassed
												? __("Deadline passed")
												: __("Leave your contact information")
										}}
									</span>
								</button>
							</div>
						</div>
					</div>

					<!-- Details Card -->
					<div class="card">
						<div class="card-header">
							<div class="w-[6px] h-6 bg-[#00B652]"></div>
							<h2 class="card-title">{{ __("Job opening details") }}</h2>
						</div>

						<div class="mb-6">
							<h3 class="section-title">{{ __("Job description") }}</h3>
							<div
								class="prose prose-sm max-w-none text-gray-700"
								v-html="jobData.description"
							></div>
						</div>

						<div class="mb-6" v-if="jobData.requirements">
							<h3 class="section-title">{{ __("Job requirements") }}</h3>
							<div
								class="prose prose-sm max-w-none text-gray-700"
								v-html="jobData.requirements"
							></div>
						</div>

						<!-- <div v-if="jobData.jo_job_benefits">
							<h3 class="section-title">{{ __("Job benefits") }}</h3>
							<div
								class="prose prose-sm max-w-none text-gray-700"
								v-html="jobData.jo_job_benefits"
							></div>
						</div> -->
					</div>
				</div>

				<!-- Right Sidebar -->
				<div class="xl:col-span-1 flex flex-col gap-4 sm:gap-6">
					<!-- Company Card -->
					<div v-if="jobData.company_details" class="sidebar-card">
						<div class="flex items-start space-x-3 mb-4">
							<div
								class="w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0"
							>
								<img
									:src="
										jobData.company_details.logo ||
										'/assets/mbw_mira/images/mira-logo.png'
									"
									alt="Company Logo"
									class="w-full h-full object-contain rounded-lg"
								/>
							</div>
							<div class="flex-1 min-w-0">
								<p class="font-semibold text-gray-900">
									{{ jobData.company_details.company_name }}
								</p>
							</div>
						</div>

						<div class="space-y-3 mb-4">
							<div
								class="flex items-center space-x-3"
								v-if="jobData.company_details.company_size"
							>
								<svg
									class="w-4 h-4 text-gray-400 flex-shrink-0"
									fill="currentColor"
									viewBox="0 0 20 20"
								>
									<path
										d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"
									></path>
								</svg>
								<div class="min-w-0 flex-1">
									<span class="text-[14px] text-gray-500"
										>{{ __("Company Size") }}:
									</span>
									<span class="text-[14px] text-gray-900 font-medium">{{
										jobData.company_details.company_size
									}}</span>
								</div>
							</div>

							<div
								class="flex items-center space-x-3"
								v-if="jobData.company_details.industry"
							>
								<svg
									class="w-4 h-4 text-gray-400 flex-shrink-0"
									fill="currentColor"
									viewBox="0 0 20 20"
								>
									<path
										d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"
									></path>
								</svg>
								<div class="min-w-0 flex-1">
									<span class="text-[14px] text-gray-500"
										>{{ __("Industry") }}:
									</span>
									<span class="text-[14px] text-gray-900 font-medium">{{
										jobData.company_details.industry
									}}</span>
								</div>
							</div>

							<div
								class="flex items-start space-x-2"
								v-if="jobData.company_details.company_location"
							>
								<svg
									class="w-4 h-4 text-gray-400 flex-shrink-0 mt-0.5"
									fill="currentColor"
									viewBox="0 0 20 20"
								>
									<path
										fill-rule="evenodd"
										d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
										clip-rule="evenodd"
									></path>
								</svg>
								<div class="min-w-0 flex-1">
									<span class="text-[14px] text-gray-500">{{
										__("Location:")
									}}</span>
									<span class="text-[14px] text-gray-900 font-medium">{{
										jobData.company_details.company_location
									}}</span>
								</div>
							</div>
						</div>

						<a
							v-if="jobData.company_details.website"
							:href="jobData.company_details.website"
							target="_blank"
							rel="noopener noreferrer"
							class="btn-link text-[14px] !font-semibold w-full items-center justify-center"
						>
							<span>{{ __("View Company Website") }}</span>
							<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
								<path
									d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"
								></path>
								<path
									d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z"
								></path>
							</svg>
						</a>
					</div>

					<!-- General Info -->
					<div class="sidebar-card">
						<h3 class="card-title mb-3">{{ __("General information") }}</h3>
						<div class="space-y-3">
							<div class="sidebar-item">
								<div class="info-icon">
									<FeatherIcon name="briefcase" class="h-6 w-6" />
								</div>
								<div>
									<span class="info-label">{{ __("Level") }}</span>
									<div class="info-value">{{ jobData.jo_position || "Chưa cập nhật" }}</div>
								</div>
							</div>

							<div class="sidebar-item">
								<div class="info-icon">
									<FeatherIcon name="clock" class="h-6 w-6" />
								</div>
								<div>
									<span class="info-label">{{ __("Work form") }}</span>
									<div class="info-value">{{ jobData.jo_work_form || "Chưa cập nhật" }}</div>
								</div>
							</div>

							<div class="sidebar-item">
								<div class="info-icon">
									<FeatherIcon name="users" class="h-6 w-6" />
								</div>
								<div>
									<span class="info-label">{{ __("Number of positions") }}</span>
									<div class="info-value">
										{{ jobData.number_of_openings || __("Not specified") }}
									</div>
								</div>
							</div>

							<div class="sidebar-item">
								<div class="info-icon">
									<FeatherIcon name="map-pin" class="h-6 w-6" />
								</div>
								<div>
									<span class="info-label">{{ __("Work location") }}</span>
									<div class="info-value">{{ jobData.location_name }}</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Job Benefits -->
					<div v-if="jobData.benefits" class="sidebar-card">
						<h3 class="card-title mb-3">{{ __("Job benefits") }}</h3>
						<div
							class="p-0 text-sm text-gray-700"
							v-html="jobData.benefits"
						></div>
					</div>
				</div>
			</div>
		</div>

		<!-- Apply Modal -->
		<Dialog v-model="showApplyModal" :options="{ size: 'xl' }" :disableOutsideClickToClose="true">
			<template #body-title>
				<h3 class="text-xl font-semibold">
					{{ __("Leave your contact information") }}
				</h3>
			</template>
			<template #body-content>
				<JobApplicationForm
					:jobOpeningId="jobOpeningId"
					:jobData="jobData"
					@success="handleApplicationSuccess"
					@cancel="showApplyModal = false"
				/>
			</template>
		</Dialog>

		<!-- Share Dialog -->
		<ShareDialog
			:modelValue="showShareModal"
			@update:modelValue="showShareModal = $event"
			:jobData="jobData"
			:jobId="jobOpeningId"
		/>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { call, FeatherIcon, Button, Dialog } from "frappe-ui";
import JobApplicationForm from "@/components/JobApplicationForm.vue";
import ShareDialog from "@/components/ShareDialog.vue";

const route = useRoute();
const jobOpeningId = computed(() => {
	// Ưu tiên lấy từ API theo job_url_cms, còn id chỉ dùng fallback hoặc cho apply
	if (route.name === "JobOpeningPublicViewCMS") {
		return null;
	}
	// if (route.name === "JobOpeningPublicViewSEO") {
	// 	const jobSlug = route.params.jobSlug;
	// 	const jobId = jobSlug.split("-").pop();
	// 	return jobId;
	// }
	return route.params.id;
});

// State
const loading = ref(true);
const error = ref(null);
const jobData = ref(null);
const showApplyModal = ref(false);
const showShareModal = ref(false);

// Computed
const isDeadlinePassed = computed(() => {
	if (!jobData.value?.closing_date) return false;
	const deadline = new Date(jobData.value.closing_date);
	const now = new Date();
	return deadline < now;
});

// Methods
const loadJobData = async () => {
	try {
		loading.value = true;
		error.value = null;

		let response;
		if (route.name === "JobOpeningPublicViewCMS") {
			response = await call(
				"mbw_mira.mbw_mira.doctype.jobopening.api.get_public_detail_by_cms",
				{
					job_url_cms: route.params.jobUrlCms,
				},
			);
		} 
		// else if (route.name === "JobOpeningPublicViewSEO") {
		// 	response = await call(
		// 		"mbw_mira.mbw_mira.doctype.jobopening.api.get_public_detail_by_slug",
		// 		{
		// 			country_code: route.params.country,
		// 			location_slug: route.params.location,
		// 			job_slug: route.params.jobSlug,
		// 		},
		// 	);
		// }
		 else {
			response = await call("mbw_mira.mbw_mira.doctype.jobopening.api.get_public_detail", {
				name: jobOpeningId.value,
			});
		}

		console.log("response", response);
		
		if (response) {
			jobData.value = response;
			// Track UTM parameters if present
			trackUTMParameters();
		} else {
			error.value = __("Job not found");
		}
	} catch (err) {
		console.error("Error loading job data:", err);
		error.value = __("Error loading job data");
	} finally {
		loading.value = false;
	}
};

// Track UTM parameters for analytics
const trackUTMParameters = async () => {
	const urlParams = new URLSearchParams(window.location.search);
	const utmSource = urlParams.get("utm_source");
	const utmMedium = urlParams.get("utm_medium");
	const utmCampaign = urlParams.get("utm_campaign");
	const utmContent = urlParams.get("utm_content");

	if (utmSource || utmMedium || utmCampaign || utmContent) {
		// Store UTM data in localStorage for tracking
		const utmData = {
			utm_source: utmSource,
			utm_medium: utmMedium,
			utm_campaign: utmCampaign,
			utm_content: utmContent,
			job_id: jobData.value?.name || jobOpeningId.value,
			timestamp: new Date().toISOString(),
		};

		localStorage.setItem("job_utm_data", JSON.stringify(utmData));

		// Send UTM data to backend for tracking
		try {
			await call("mbw_mira.mbw_mira.doctype.jobopening.api.track_utm_visit", {
				job_id: jobOpeningId.value,
				utm_source: utmSource,
				utm_medium: utmMedium,
				utm_campaign: utmCampaign,
				utm_content: utmContent,
				session_id: generateSessionId(),
			});
			console.log("UTM Parameters tracked and saved to database:", utmData);
		} catch (error) {
			console.error("Error tracking UTM parameters:", error);
		}
	}
};

// Generate unique session ID
const generateSessionId = () => {
	return "session_" + Date.now() + "_" + Math.random().toString(36).substr(2, 9);
};

const formatDate = (dateString) => {
	if (!dateString) return "Không xác định";
	const date = new Date(dateString);
	return date.toLocaleDateString("vi-VN", {
		year: "numeric",
		month: "long",
		day: "numeric",
	});
};

const formatSalary = (minSalary, maxSalary, currency = "VND") => {
	if (!minSalary && !maxSalary) return "Thỏa thuận";

	const formatNumber = (num) => {
		if (num >= 1000000) {
			return (num / 1000000).toFixed(0) + " triệu";
		}
		return num.toLocaleString("vi-VN");
	};

	if (minSalary && maxSalary) {
		return `${formatNumber(minSalary)} - ${formatNumber(maxSalary)} ${currency}`;
	} else if (minSalary) {
		return `Từ ${formatNumber(minSalary)} ${currency}`;
	} else if (maxSalary) {
		return `Lên đến ${formatNumber(maxSalary)} ${currency}`;
	}

	return "Thỏa thuận";
};

const getDaysLeft = (deadline) => {
	if (!deadline) return "Không xác định";

	const deadlineDate = new Date(deadline);
	const today = new Date();
	const diffTime = deadlineDate - today;
	const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

	if (diffDays < 0) {
		return "Đã hết hạn";
	} else if (diffDays === 0) {
		return "Hết hạn hôm nay";
	} else if (diffDays === 1) {
		return "Còn 1 ngày";
	} else {
		return `Còn ${diffDays} ngày`;
	}
};

const handleApplicationSuccess = () => {
	showApplyModal.value = false;
	// Reload job data to update applicants count
	loadJobData();
};

// Lifecycle
onMounted(() => {
	loadJobData();
});
</script>

<style scoped>
/* TopCV-inspired styling */
.prose {
	color: #374151;
	line-height: 1.7;
	font-size: 14px;
}

.prose h1,
.prose h2,
.prose h3,
.prose h4,
.prose h5,
.prose h6 {
	color: #111827;
	font-weight: 600;
	margin-top: 1.5em;
	margin-bottom: 0.5em;
}

.prose p {
	margin-bottom: 1em;
}

.prose ul,
.prose ol {
	margin-bottom: 1em;
	padding-left: 1.5em;
}

.prose li {
	margin-bottom: 0.5em;
	position: relative;
}

.prose ul li::before {
	content: "•";
	color: #16a34a;
	font-weight: bold;
	position: absolute;
	left: -1em;
}

.prose strong {
	color: #111827;
	font-weight: 600;
}

/* Custom scrollbar for content areas */
.prose::-webkit-scrollbar {
	width: 6px;
}

.prose::-webkit-scrollbar-track {
	background: #f1f5f9;
	border-radius: 3px;
}

.prose::-webkit-scrollbar-thumb {
	background: #cbd5e1;
	border-radius: 3px;
}

.prose::-webkit-scrollbar-thumb:hover {
	background: #94a3b8;
}

/* Hover effects for cards */
.bg-white:hover {
	box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
	transition: box-shadow 0.2s ease-in-out;
}

/* Button animations */
.bg-green-600:hover {
	transform: translateY(-1px);
	transition: all 0.2s ease-in-out;
}

/* Icon animations */
.w-10.h-10:hover {
	transform: scale(1.05);
	transition: transform 0.2s ease-in-out;
}

/* Responsive adjustments */
@media (max-width: 768px) {
	.prose {
		font-size: 13px;
	}

	.grid-cols-2 {
		grid-template-columns: 1fr;
	}

	.md\\:grid-cols-4 {
		grid-template-columns: repeat(2, 1fr);
	}
}

.card {
	border-radius: 0.75rem;
	--tw-bg-opacity: 1;
	background-color: rgb(255 255 255 / var(--tw-bg-opacity, 1));
	padding: 1.5rem;
	box-shadow: 0 4px 12px #00000014;
}

.card-title {
	font-size: 18px;
	font-weight: 700;
	--tw-text-opacity: 1;
	color: rgb(23 23 23 / var(--tw-text-opacity, 1));
}

.card-header {
	margin-bottom: 1rem;
	display: flex;
	align-items: center;
}

.info-grid {
	display: grid;
	grid-template-columns: repeat(1, minmax(0, 1fr));
	gap: 1rem;
}

@media (min-width: 1024px) {
	.info-grid {
		grid-template-columns: repeat(3, minmax(0, 1fr));
	}
}

@media (min-width: 640px) {
	.info-grid {
		grid-template-columns: repeat(3, minmax(0, 1fr));
	}

	.btn-primary {
		flex: none;
		padding-left: 1.5rem;
		padding-right: 1.5rem;
		font-size: 14px;
		line-height: 1.15;
		letter-spacing: 0.02em;
		font-weight: 420;
	}

	.card-header {
		margin-bottom: 1.5rem;
	}

	.sidebar-card {
		padding: 1.5rem;
	}
}

.info-item {
	padding: 0.75rem;
	display: flex;
	align-items: center;
}

.info-icon {
	display: flex;
	height: 2.5rem;
	width: 2.5rem;
	flex-shrink: 0;
	align-items: center;
	justify-content: center;
	border-radius: 9999px;
	--tw-bg-opacity: 1;
	background-color: rgb(228 250 235 / var(--tw-bg-opacity, 1));
}

.info-icon svg {
	height: 1.5rem;
	width: 1.5rem;
	--tw-text-opacity: 1;
	color: rgb(39 143 94 / var(--tw-text-opacity, 1));
}

.btn-primary {
	background-color: #00b652 !important;
	color: #fff;
	transition: all 0.2s;
	display: flex;
	justify-content: center;
	align-items: center;
}

.btn-primary > :not([hidden]) ~ :not([hidden]) {
	--tw-space-x-reverse: 0;
	margin-right: calc(0.5rem * var(--tw-space-x-reverse));
	margin-left: calc(0.5rem * calc(1 - var(--tw-space-x-reverse)));
}

.section-title {
	margin-bottom: 0.75rem;
	font-size: 16px;
	line-height: 1.15;
	letter-spacing: 0.02em;
	font-weight: 600;
	--tw-text-opacity: 1;
	color: rgb(23 23 23 / var(--tw-text-opacity, 1));
}

.card-header > :not([hidden]) ~ :not([hidden]) {
	--tw-space-x-reverse: 0;
	margin-right: calc(0.5rem * var(--tw-space-x-reverse));
	margin-left: calc(0.5rem * calc(1 - var(--tw-space-x-reverse)));
}

.sidebar-card {
    border-radius: .75rem;
    --tw-bg-opacity: 1;
    background-color: rgb(255 255 255 / var(--tw-bg-opacity, 1));
    padding: 1rem;
    --tw-shadow: 0px 1px 2px rgba(0, 0, 0, .1);
    --tw-shadow-colored: 0px 1px 2px var(--tw-shadow-color);
    box-shadow: var(--tw-ring-offset-shadow, 0 0 #0000),var(--tw-ring-shadow, 0 0 #0000),var(--tw-shadow);
}

.space-x-3>:not([hidden])~:not([hidden]) {
    --tw-space-x-reverse: 0;
    margin-right: calc(.75rem * var(--tw-space-x-reverse));
    margin-left: calc(.75rem * calc(1 - var(--tw-space-x-reverse)));
}

.btn-link {
    font-size: 13px;
    line-height: 1.15;
    letter-spacing: .02em;
    font-weight: 420;
    --tw-text-opacity: 1;
    color: rgb(39 143 94 / var(--tw-text-opacity, 1));
    transition-property: color,background-color,border-color,text-decoration-color,fill,stroke;
    transition-timing-function: cubic-bezier(.4,0,.2,1);
    transition-duration: .15s;
    display: flex;
}

.sidebar-item {
    display: flex;
    align-items: center;
}

.info-label {
    font-size: 14px;
    --tw-text-opacity: 1;
    color: rgb(82 82 82 / var(--tw-text-opacity, 1));
}

.info-value {
    font-size: 14px;
    font-weight: 500;
    --tw-text-opacity: 1;
    color: rgb(23 23 23 / var(--tw-text-opacity, 1));
}

.sidebar-item>:not([hidden])~:not([hidden]) {
    --tw-space-x-reverse: 0;
    margin-right: calc(.75rem * var(--tw-space-x-reverse));
    margin-left: calc(.75rem * calc(1 - var(--tw-space-x-reverse)));
}

.info-item>:not([hidden])~:not([hidden]) {
    --tw-space-x-reverse: 0;
    margin-right: calc(.75rem * var(--tw-space-x-reverse));
    margin-left: calc(.75rem * calc(1 - var(--tw-space-x-reverse)));
}

.btn-link>:not([hidden])~:not([hidden]) {
    --tw-space-x-reverse: 0;
    margin-right: calc(.5rem * var(--tw-space-x-reverse));
    margin-left: calc(.5rem * calc(1 - var(--tw-space-x-reverse)));
}
</style>
