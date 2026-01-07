import frappe
from frappe import _
from bs4 import BeautifulSoup
from frappe.translate import get_all_translations
from frappe.utils import cstr
# from frappe.utils.modules import get_modules_from_all_apps_for_user
from frappe.utils.telemetry import POSTHOG_HOST_FIELD, POSTHOG_PROJECT_FIELD


@frappe.whitelist(allow_guest=True)
def get_user_info():
    if frappe.session.user == "Guest":
        return None

    user = frappe.db.get_value(
        "User",
        frappe.session.user,
        "username,email,enabled,user_image,full_name",
        as_dict=True,
    )
    
    return user



@frappe.whitelist(allow_guest=True)
def get_translations():
	if frappe.session.user != "Guest":
		language = frappe.db.get_value("User", frappe.session.user, "language")
	else:
		language = frappe.db.get_single_value("System Settings", "language")

	return get_all_translations(language)


@frappe.whitelist()
def get_user_signature():
	user = frappe.session.user
	user_email_signature = (
		frappe.db.get_value(
			"User",
			user,
			"email_signature",
		)
		if user
		else None
	)

	signature = user_email_signature or frappe.db.get_value(
		"Email Account",
		{"default_outgoing": 1, "add_signature": 1},
		"signature",
	)

	if not signature:
		return

	soup = BeautifulSoup(signature, "html.parser")
	html_signature = soup.find("div", {"class": "ql-editor read-mode"})
	_signature = None
	if html_signature:
		_signature = html_signature.renderContents()
	content = ""
	if cstr(_signature) or signature:
		content = f'<br><p class="signature">{signature}</p>'
	return content


@frappe.whitelist()
def get_posthog_settings():
	return {
		"posthog_project_id": frappe.conf.get(POSTHOG_PROJECT_FIELD),
		"posthog_host": frappe.conf.get(POSTHOG_HOST_FIELD),
		"enable_telemetry": frappe.get_system_settings("enable_telemetry"),
		"telemetry_site_age": frappe.utils.telemetry.site_age(),
	}


def check_app_permission():
	if frappe.session.user == "Administrator":
		return True

	# allowed_modules = get_modules_from_all_apps_for_user()
	# allowed_modules = [x["module_name"] for x in allowed_modules]

	# roles = frappe.get_roles()
	# if any(
	# 	role in ["System Manager", "Sales User", "Sales Manager"] for role in roles
	# ):
	# 	return True

	return False
