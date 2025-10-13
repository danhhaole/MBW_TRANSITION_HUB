# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime,add_days,cint, get_datetime
import json

class MiraAction(Document):
	pass

	def validate(self):
		check_duplicate_mira_action(self)
		
	def on_update(self):
		"""Khi có event update xử lý các luồng
		"""
		if self.status in ["EXECUTED","FAILED"]:
			update_step_result_talent_campaign(self)


def update_step_result_talent_campaign(doc):
	"""Update trạng thái Mira Talent Campaign khi mira_action đã thực hiện

	Args:
		doc (dict): _description_
	""" 
	#MiraAction có 2 trạng thái này thì update Mira Talent Campaign
	talent_campaign = frappe.get_doc("Mira Talent Campaign", doc.talent_campaign_id)
	if talent_campaign.status != "ACTIVE":
		return

	current_order = talent_campaign.current_step_order
	next_step = frappe.get_all(
		"CampaignStep",
		filters={"campaign": talent_campaign.campaign_id, "step_order": current_order + 1},
		fields=["name", "step_order", "delay_in_days"],
		limit=1,
	)

	if not next_step:
		talent_campaign.status = "COMPLETED"
		talent_campaign.next_mira_action_at = None
	else:
		step_info = next_step[0]
		talent_campaign.current_step_order = step_info.step_order
		talent_campaign.next_mira_action_at = add_days(now_datetime(), step_info.delay_in_days or 0)

	talent_campaign.save()
	return True


def update_current_campaign(self):
	campaign = frappe.get_doc("Campaign",self.campaign)
	current += campaign.current
	if current > campaign.total:
		current = campaign.total
	campaign.update({
		"current":current
    })
	campaign.save(ignore_permissions=True)
	frappe.db.commit()


#Hàm lấy ra mira_action theo mira_action_type trong step campaign
def get_mira_action_worker(step):
	"""Lấy danh sách mira_action có status là SCHEDULED và step tương ứng

	Args:
		step (SEND_EMAIL/SEND_SMS): _description_
	"""
	mira_actions = frappe.get_list("MiraAction",filters={"status":"SCHEDULED", "scheduled_at":["<=", now_datetime()]})
	#Duyệt danh sách mira_actions, tìm step nào có mira_action_type là gửi email
	mira_actions_name =[]
	for mira_action in mira_actions:
		step_exists = frappe.db.exists("CampaignStep",{"name":mira_action.campaign_step, "mira_action_type":step})
		if step_exists:
			mira_actions_name.append(mira_action)
	return mira_actions_name

def check_duplicate_mira_action(doc):
    filters = {
        "talent_campaign_id": doc.talent_campaign_id,
        "campaign_step": doc.campaign_step,
    }

    existing = frappe.db.exists("MiraAction", filters)

    if existing and existing != doc.name:  # ← tránh trùng với chính mình khi update
        frappe.throw(
            frappe._(
                "An MiraAction with Candidate Campaign <b>{0}</b> and Campaign Step <b>{1}</b> already exists: <a href='/app/mira_action/{2}'>{2}</a>"
            ).format(
                doc.talent_campaign_id,
                doc.campaign_step,
                existing
            ),
            title=frappe._("Duplicate MiraAction")
        )

def _map_by(items, key):
    mapped = {}
    for it in items or []:
        mapped[it.get(key)] = it
    return mapped


def _get_enriched_mira_actions(mira_action_rows):
    step_names = [row.get("campaign_step") for row in mira_action_rows if row.get("campaign_step")]
    user_ids = list({row.get("assignee_id") for row in mira_action_rows if row.get("assignee_id")})

    steps = frappe.get_all(
        "CampaignStep",
        filters={"name": ["in", step_names]} if step_names else {},
        fields=["name", "campaign_step_name", "campaign", "mira_action_type"],
    ) if step_names else []
    steps_by_name = _map_by(steps, "name")

    campaign_ids = list({s.get("campaign") for s in steps}) if steps else []
    campaigns = frappe.get_all(
        "Campaign",
        filters={"name": ["in", campaign_ids]} if campaign_ids else {},
        fields=["name", "campaign_name"],
    ) if campaign_ids else []
    campaigns_by_id = _map_by(campaigns, "name")

    users = frappe.get_all(
        "User",
        filters={"name": ["in", user_ids]} if user_ids else {},
        fields=["name", "full_name", "email"],
    ) if user_ids else []
    users_by_id = _map_by(users, "name")

    enriched = []
    for row in mira_action_rows:
        step = steps_by_name.get(row.get("campaign_step"), {})
        camp = campaigns_by_id.get(step.get("campaign"), {})
        user = users_by_id.get(row.get("assignee_id"), {})
        enriched.append({
            **row,
            "campaign_step_name": step.get("campaign_step_name"),
            "mira_action_type": step.get("mira_action_type"),
            "campaign_id": step.get("campaign"),
            "campaign_name": camp.get("campaign_name"),
            "assignee_full_name": user.get("full_name"),
            "assignee_email": user.get("email"),
        })
    return enriched


@frappe.whitelist()
def get_my_mira_actions(page=1, limit=20, search="", assigned_to="@me", include_unassigned=1, include_scheduled_as_pending=1):
    """
    Trả về dữ liệu danh sách "Công việc của tôi" giống UI trong ảnh:
    - pending: các MiraAction có status = PENDING_MANUAL, người được giao = @me
    - completed: các MiraAction có status = EXECUTED, người được giao = @me
    - all: tất cả mira_action của người dùng
    Có phân trang độc lập cho mỗi tab.
    """
    try:
        start = (cint(page) - 1) * cint(limit)
        
        # Kiểm tra quyền Administrator
        current_user = frappe.session.user
        is_admin = current_user == "Administrator" or "Administrator" in frappe.get_roles(current_user)
        
        base_fields = [
            "name",
            "campaign_step",
            "status",
            "talent_campaign_id",
            "assignee_id",
            "scheduled_at",
            "executed_at",
            "result",
            "creation",
            "modified",
        ]

        # Filter cơ bản: chỉ lấy 2 trạng thái PENDING_MANUAL và EXECUTED
        common_filters = {
            "status": ["in", ["PENDING_MANUAL", "EXECUTED"]]
        }
        
        # Nếu không phải Administrator, filter theo assignee_id
        if not is_admin:
            common_filters["assignee_id"] = current_user

        # Xử lý search
        search_condition = []
        if search:
            search_condition = [
                {"name": ["like", f"%{search}%"]},
                {"talent_campaign_id": ["like", f"%{search}%"]},
            ]

        # Pending: chỉ lấy PENDING_MANUAL
        pending_filters = common_filters.copy()
        pending_filters["status"] = "PENDING_MANUAL"
        
        pending_rows = frappe.get_list(
            "MiraAction",
            fields=base_fields,
            filters=pending_filters,
            or_filters=search_condition if search else None,
            order_by="creation desc",
            start=start,
            page_length=cint(limit),
        ) or []
        pending_total = len(
            frappe.get_list("MiraAction", filters=pending_filters, or_filters=search_condition if search else None)
        )

        # Completed: chỉ lấy EXECUTED
        completed_filters = common_filters.copy()
        completed_filters["status"] = "EXECUTED"
        
        completed_rows = frappe.get_list(
            "MiraAction",
            fields=base_fields,
            filters=completed_filters,
            or_filters=search_condition if search else None,
            order_by="executed_at desc, creation desc",
            start=start,
            page_length=cint(limit),
        ) or []
        completed_total = len(
            frappe.get_list("MiraAction", filters=completed_filters, or_filters=search_condition if search else None)
        )

        # All: lấy cả PENDING_MANUAL và EXECUTED
        all_rows = frappe.get_list(
            "MiraAction",
            fields=base_fields,
            filters=common_filters,
            or_filters=search_condition if search else None,
            order_by="status asc, creation desc",  # Sắp xếp để pending lên trước
            start=start,
            page_length=cint(limit),
        ) or []
        all_total = len(
            frappe.get_list("MiraAction", filters=common_filters, or_filters=search_condition if search else None)
        )

        # Enrich with step/campaign/user info
        pending = _get_enriched_mira_actions(pending_rows)
        completed = _get_enriched_mira_actions(completed_rows)
        all_mira_actions = _get_enriched_mira_actions(all_rows)

        def paginate(total):
            pages = (total + cint(limit) - 1) // cint(limit) if cint(limit) > 0 else 1
            current = (start // cint(limit)) + 1 if cint(limit) > 0 else 1
            return {
                "page": current,
                "limit": cint(limit),
                "total": total,
                "pages": pages,
                "has_next": current < pages,
                "has_prev": current > 1,
                "showing_from": 0 if total == 0 else start + 1,
                "showing_to": min(start + cint(limit), total),
            }

        return {
            "success": True,
            "all": all_mira_actions,
            "pending": pending,
            "completed": completed,
            "pagination": {
                "all": paginate(all_total),
                "pending": paginate(pending_total),
                "completed": paginate(completed_total),
            },
        }

    except Exception as e:
        frappe.log_error(f"Error in get_my_mira_actions: {str(e)}")
        return {"success": False, "error": str(e)}
@frappe.whitelist()
def update_mira_action(name, data=None, **kwargs):
    """
    Cập nhật MiraAction từ modal "Chỉnh sửa hành động" như ảnh.
    Hỗ trợ truyền vào data (JSON string/object) hoặc từng tham số kwargs.
    Các trường hỗ trợ: status, scheduled_at, executed_at, result, assignee_id, campaign_step, talent_campaign_id
    """
    try:
        if not name:
            return {"success": False, "error": "MiraAction name is required"}

        payload = {}
        if data:
            if isinstance(data, str):
                payload = json.loads(data)
            else:
                payload = dict(data)

        # merge kwargs (direct params) over data
        for k, v in kwargs.items():
            if v is not None:
                payload[k] = v

        # normalize datetime fields
        for dt_field in ["executed_at", "scheduled_at"]:
            if dt_field in payload and isinstance(payload[dt_field], str) and payload[dt_field].strip():
                try:
                    dt = get_datetime(payload[dt_field])
                    # Lưu ở định dạng 'YYYY-MM-DD HH:MM:SS' (không timezone)
                    payload[dt_field] = dt.strftime('%Y-%m-%d %H:%M:%S')
                except Exception:
                    # keep original if cannot parse; DB will validate
                    pass

        # nếu cập nhật status EXECUTED mà chưa truyền executed_at, set executed_at = now
        if payload.get("status") == "EXECUTED" and not payload.get("executed_at"):
            payload["executed_at"] = get_datetime().strftime('%Y-%m-%d %H:%M:%S')

        # parse result if given as string
        if "result" in payload and isinstance(payload["result"], str):
            try:
                payload["result"] = json.loads(payload["result"]) if payload["result"].strip() else None
            except Exception:
                # giữ nguyên chuỗi nếu không phải JSON hợp lệ
                pass

        doc = frappe.get_doc("MiraAction", name)
        doc.update(payload)
        doc.save()

        return {"success": True, "data": doc.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error in update_mira_action: {str(e)}")
        return {"success": False, "error": str(e)}


		
