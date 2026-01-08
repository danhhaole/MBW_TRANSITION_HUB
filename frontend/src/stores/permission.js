import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { call } from "frappe-ui";
import { usersStore } from "@/stores/user";

export const usePermissionStore = defineStore("transition_hub-permission", () => {
	const userFeatures = ref([]);   
	const featureMap = ref({});     
	const roles = ref([]);
	const { userResource } = usersStore();
	const isReady = ref(false); // flag load xong

	async function loadFeatures() {
		try {
			const res = await call("mbw_transition_hub.api.roles.get_user_features");

			try {
				await userResource.fetch();
			} catch (err) {
				console.warn("⚠️ Không thể fetch userResource:", err);
			}


			let resRoles = [];
			if (userResource.data && userResource.data !== "Guest") {
				try {
					resRoles = await call("mbw_transition_hub.api.roles.get_user_roles", {
						user: userResource.data,
					});
				} catch (err) {
					console.warn("⚠️ Không thể lấy roles:", err);
				}
			}
			roles.value = resRoles || [];

			// admin full quyền
			if (roles.value.includes("Administrator") || roles.value.includes("System Manager")) {
				// featureMap.value = Object.fromEntries(
				// 	Object.keys(DOCTYPE_FEATURE_MAP).map(dt => [dt, "full"])
				// );
				isReady.value = true;
				return;
			}
		

			userFeatures.value = res.features || [];
			const map = {};
			for (const [doctype, features] of Object.entries(DOCTYPE_FEATURE_MAP)) {
				for (const [featureName, level] of Object.entries(features)) {
					if (userFeatures.value.includes(featureName)) {
						map[doctype] = level;
						break;
					}
				}
			}
			console.log("featureMap", featureMap);
			
			featureMap.value = map;
		} catch (error) {
			console.error("❌ Lỗi khi loadFeatures:", error);
		} finally {
			isReady.value = true;
		}
	}

	// ⚡ auto reactive version của can()
	function can(doctype, level) {
		return computed(() => {
			if (!isReady.value) return false;
			if (roles.value.includes("Administrator") || roles.value.includes("System Manager")) {
				console.log("✅ Admin or System Manager")
				return true;
			}
			const perm = featureMap.value[doctype];
			
			return perm === level || perm === "full";
		});
	}

	return {
		userFeatures,
		featureMap,
		loadFeatures,
		can,
		roles,
		isReady,
	};
});