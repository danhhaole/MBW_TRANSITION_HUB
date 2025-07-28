import frappe
from frappe import _
import json
from bs4 import BeautifulSoup
from frappe.core.api.file import get_max_file_size
from frappe.translate import get_all_translations
from frappe.utils import cstr, split_emails, validate_email_address
# from frappe.utils.modules import get_modules_from_all_apps_for_user
from frappe.utils.telemetry import POSTHOG_HOST_FIELD, POSTHOG_PROJECT_FIELD
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
import base64
import io
import os
from datetime import datetime
from frappe.utils import now_datetime

@frappe.whitelist()
def create_candidate_segment():
    """
    API: tạo CandidateSegment trực tiếp (synchronous).
    """
    data = json.loads(frappe.request.data)
    if not data:
        frappe.throw("Data require")
    
    return {
        "status": "queued",
        "message": "CandidateSegment creation has been queued."
    }

@frappe.whitelist()
def complete_manual_action():
    data = json.loads(frappe.request.data)
    if not data:
        frappe.throw("Data require")
    action_id = data.get("action_id")
    if not action_id:
        frappe.throw("action_id require")
    note = data.get("note",None)
    user = data.get("user",None)
    return {
        "status": "queued",
        "message": "CandidateSegment creation has been queued."
    }

@frappe.whitelist(allow_guest=False)
def create_campaign_with_steps_bg():
    """
    Nhận dữ liệu từ request và đẩy xử lý vào background.
    { 
        campaign_name
        description
        target_segment
        owner_id
        start_date
        end_date
        status
        steps :[
                step_name,
                step_order
                action_type
                delay_in_days
                template
                action_config
            ]
    }
    """
    data = frappe.request.get_json()
    if not data:
        frappe.throw(frappe._("No JSON payload found in request"))

    # enqueue job


    return {
        "status": "queued",
        "message": frappe._("Campaign creation has been scheduled. You will be notified when it's done.")
    }
# API Module for MBW Mira 

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


@frappe.whitelist(allow_guest=True)
def accept_invitation(key: str | None = None):
	if not key:
		frappe.throw("Invalid or expired key")

	result = frappe.db.get_all("CRM Invitation", filters={"key": key}, pluck="name")
	if not result:
		frappe.throw("Invalid or expired key")

	invitation = frappe.get_doc("CRM Invitation", result[0])
	invitation.accept()
	invitation.reload()

	if invitation.status == "Accepted":
		frappe.local.login_manager.login_as(invitation.email)
		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = "/crm"


@frappe.whitelist()
def invite_by_email(emails: str, role: str):
	frappe.only_for(["Sales Manager", "System Manager"])

	if role not in ["System Manager", "Sales Manager", "Sales User"]:
		frappe.throw("Cannot invite for this role")

	if not emails:
		return

	email_string = validate_email_address(emails, throw=False)
	email_list = split_emails(email_string)
	if not email_list:
		return
	existing_members = frappe.db.get_all("User", filters={"email": ["in", email_list]}, pluck="email")
	existing_invites = frappe.db.get_all(
		"CRM Invitation",
		filters={
			"email": ["in", email_list],
			"role": ["in", ["System Manager", "Sales Manager", "Sales User"]],
		},
		pluck="email",
	)

	to_invite = list(set(email_list) - set(existing_members) - set(existing_invites))

	for email in to_invite:
		frappe.get_doc(doctype="CRM Invitation", email=email, role=role).insert(ignore_permissions=True)

	return {
		"existing_members": existing_members,
		"existing_invites": existing_invites,
		"to_invite": to_invite,
	}


@frappe.whitelist()
def get_file_uploader_defaults(doctype: str):
	max_number_of_files = None
	make_attachments_public = False
	if doctype:
		meta = frappe.get_meta(doctype)
		max_number_of_files = meta.get("max_attachments")
		make_attachments_public = meta.get("make_attachments_public")

	return {
		"allowed_file_types": frappe.get_system_settings("allowed_file_extensions"),
		"max_file_size": get_max_file_size(),
		"max_number_of_files": max_number_of_files,
		"make_attachments_public": bool(make_attachments_public),
	}

@frappe.whitelist(allow_guest=True)
def get_campaign_qrcode():
    data = frappe.local.form_dict or frappe.request.json
    campaign_id = data.get("campaign_id")
    origin = frappe.request.headers.get("Origin")
    
    if not campaign_id:
        frappe.throw("Missing campaign_id")

    # Lấy campaign
    campaign = frappe.db.get_value("Campaign", campaign_id,["*"],as_dict=1)

    if not campaign.is_active or campaign.status != "ACTIVE":
        frappe.throw("Campaign is not active")

    # URL form đăng ký
    protocol = frappe.request.scheme
    host = frappe.request.host
    origin = frappe.request.headers.get("Origin")
    base_url = f"{protocol}://{host}"
    if origin:
        base_url = origin
    register_url = f"{base_url}/mbw_mira/register?campaign={campaign.name}"

    # Tạo QR code
    qr = qrcode.QRCode(
        version=2,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(register_url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Encode base64
    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    return {
        "url": register_url,
        "image": f"data:image/png;base64,{img_base64}"
    }

@frappe.whitelist(allow_guest=True)
def submit_talent_profile():

    # Lấy dữ liệu từ JSON body
    data = frappe.local.form_dict or frappe.request.json
    if not data:
        frappe.throw(_("No data submitted"))

    # Các trường bắt buộc
    required_fields = ["campaign", "full_name", "email"]
    for field in required_fields:
        if not data.get(field):
            frappe.throw(_(f"Missing required field: {field}"))

    campaign_id = data["campaign"]

    # Tránh permission error, dùng get_value thay vì get_doc
    campaign = frappe.db.get_value("Campaign", campaign_id, ["name", "is_active"], as_dict=True)
    if not campaign or not campaign.is_active:
        frappe.throw(_("This campaign is not active"))

    # 1. Check trùng email trong cùng campaign
    existing = frappe.db.exists(
        "TalentProfiles",
        {"email": data["email"], "source": campaign_id}
    )
    if existing:
        return {
            "success": False,
            "message": "You have already submitted your profile for this campaign."
        }

    # 2. Chống spam gửi liên tục trong vòng 60s
    recent = frappe.db.sql("""
        SELECT name FROM `tabTalentProfiles`
        WHERE email = %s
        AND creation > NOW() - INTERVAL 60 SECOND
        LIMIT 1
    """, (data["email"],))
    if recent:
        return {
            "success": False,
            "message": _("You have recently submitted. Please wait a moment before submitting again.")
        }
    # 3. Xây dữ liệu hồ sơ
    profile_fields = {
        "doctype": "TalentProfiles",
        "full_name": data["full_name"],
        "email": data["email"],
        "source": campaign_id,
        "status": "NEW",        
        "last_interaction": datetime.now(),
    }

    optional_fields = [
        "phone", "dob", "avatar", "headline", "skills","position",
        "cv_original_url", "portfolio_url", "linkedin_url", ""
    ]
    for field in optional_fields:
        if field in data and data[field] not in [None, ""]:
            profile_fields[field] = data[field]

    # Trường JSON
    if "profile_data" in data:
        try:
            profile_fields["profile_data"] = (
                json.loads(data["profile_data"])
                if isinstance(data["profile_data"], str)
                else data["profile_data"]
            )
        except Exception:
            profile_fields["profile_data"] = {}

    # 4. Tạo và lưu hồ sơ (public)
    try:
        profile = frappe.get_doc(profile_fields)
        profile.insert(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        print("error", e)
        frappe.throw(e)

    return {
        "success": True,
        "message": "Submitted successfully",
        "talent_profile_id": profile.name
    }

def try_parse_json(value):
    try:
        return json.loads(value) if isinstance(value, str) else value
    except Exception:
        return None

@frappe.whitelist(allow_guest=True)
def submit_application():
    data = frappe.local.form_dict or frappe.request.json
    if not data:
        frappe.throw(_("No data submitted"))

    # Lấy các trường chính
    email = data.get("email")
    full_name = data.get("full_name")
    campaign_id = data.get("campaign_id")
    position = data.get("position")
    resume = data.get("resume")  # file URL hoặc file token
    segment_id = data.get("segment_id")

     # 2. Chống spam gửi liên tục trong vòng 60s
    recent = frappe.db.sql("""
        SELECT name FROM `tabTalentProfiles`
        WHERE email = %s
        AND creation > NOW() - INTERVAL 60 SECOND
        LIMIT 1
    """, (data["email"],))
    if recent:
        return {
            "success": False,
            "message": _("You have recently submitted. Please wait a moment before submitting again.")
        }

    if not email or not campaign_id:
        frappe.throw(_("Email and campaign_id are required."))

    # 1. Kiểm tra campaign hợp lệ
    campaign = frappe.db.get_value("Campaign", campaign_id, ["name", "is_active"], as_dict=True)
    if not campaign or not campaign.is_active:
        frappe.throw(_("This campaign is not active"))

    # 2. Tìm hoặc tạo TalentProfiles
    profile_name = frappe.db.get_value("TalentProfiles", {"email": email})
    now = now_datetime()

    if not profile_name:
        profile = frappe.get_doc({
            "doctype": "TalentProfiles",
            "email": email,
            "full_name": full_name,
            "source": campaign_id,
            "status": "HIRED",
            "last_interaction": now,
        })
        profile.insert(ignore_permissions=True)
        frappe.db.commit()
    else:
        profile = frappe.get_doc("TalentProfiles", profile_name)
        profile.status = "HIRED"
        profile.last_interaction = now
        profile.save(ignore_permissions=True)
        frappe.db.commit()
    # 3. Check duplicate ApplicantPool
    existing_app = frappe.db.exists(
        "ApplicantPool",
        {
            "talent_id": profile.name,
            "campaign_id": campaign_id,
            "position": position or ""
        }
    )
    if existing_app:
        return {
            "success": False,
            "message": "You have already applied for this campaign and position."
        }

    # 4. Tạo ApplicantPool record
    applicant = frappe.get_doc({
        "doctype": "ApplicantPool",
        "talent_id": profile.name,
        "campaign_id": campaign_id,
        "segment_id": segment_id,
        "application_date": now,
        "position": position,
        "resume": resume,
        "application_status": "New"
    })
    applicant.insert(ignore_permissions=True)
    frappe.db.commit()

    # 5. Ghi nhận tương tác - tránh spam (nếu đã có gần đây thì bỏ qua)
    recent = frappe.db.exists("Interaction", {
        "talent_id": profile.name,
        "interaction_type": "APPLICATION_SUBMITTED",
        "reference_doctype": "ApplicantPool",
        "reference_name": applicant.name
    })

    if not recent:
        interaction = frappe.get_doc({
            "doctype": "Interaction",
            "talent_id": profile.name,
            "interaction_type": "APPLICATION_SUBMITTED",
            "description": f"{profile.full_name} applied to campaign {campaign_id} for position {position}",
            "reference_doctype": "ApplicantPool",
            "reference_name": applicant.name
        })
        interaction.insert(ignore_permissions=True)
        frappe.db.commit()
    return {
        "success": True,
        "message": "Application submitted successfully"
    }


@frappe.whitelist(allow_guest=True)
def get_campaign_details_for_submit():
    data = frappe.local.form_dict or frappe.request.json
    campaign_id = data.get("campaign_id")

    if not campaign_id:
        frappe.throw(_("Missing campaign_id"))

    # Lấy thông tin campaign (tránh quyền)
    campaign = frappe.db.get_value(
        "Campaign",
        campaign_id,
        ["name", "campaign_name", "start_date", "end_date", "status", "source", "target_segment","criteria"],
        as_dict=True
    )

    if not campaign:
        frappe.throw(_("Campaign not found"))

    # Parse target_segment nếu là MultiSelect field (dạng comma-separated string)
    segment_names = []
    if campaign.target_segment:
        if isinstance(campaign.target_segment, str):
            segment_names = [s.strip() for s in campaign.target_segment.split(",") if s.strip()]
        elif isinstance(campaign.target_segment, list):
            segment_names = campaign.target_segment

    # Lấy danh sách TalentSegment (tránh quyền)
    segments = []
    if segment_names:
        segments = frappe.db.get_all(
            "TalentSegment",
            filters={"name": ["in", segment_names]},
            fields=["name", "title", "description", "criteria", "type"]
        )
    else:
        segments = frappe.db.get_all(
            "TalentSegment",
            fields=["name", "title", "description", "criteria", "type"]
        )
    if segments:
        # Nếu cần parse criteria từ JSON string
        for seg in segments:
            if seg.get("criteria"):
                try:
                    seg["criteria"] = json.loads(seg["criteria"])
                except Exception:
                    seg["criteria"] = {}

    return {
        "campaign": campaign,
        "segments": segments
    }