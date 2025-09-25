import json
import requests
import frappe
from typing import Optional, Tuple
from frappe.utils import now_datetime, add_to_date
import pytz
from datetime import datetime

from mbw_mira.api.external_connections import (
	get_url_without_port,
	host as SOCIALHUB_HOST,
)



def run():
	"""
	Auto-share theo lịch cho các step của Campaign:
	- Ưu tiên CampaignStep.scheduled_at nếu có
	- Nếu không có, dùng Campaign.start_date + delay_in_days (theo step)
	- Chỉ đăng nếu thời điểm (<= now) và chưa đăng
	- Lấy page_id từ Campaign.select_pages và ghép với External Connection
	- Nội dung lấy từ CampaignStep.template; ảnh từ CampaignStep.image
	- Sau khi đăng, cập nhật shared_at/shared_post_id vào CampaignStep
	"""
	# Sử dụng timezone Việt Nam
	vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
	now_dt = now_datetime()
	
	# Convert Frappe time to Vietnam timezone
	if now_dt.tzinfo:
		now_vietnam = now_dt.astimezone(vietnam_tz)
	else:
		# Nếu Frappe time là naive, assume UTC
		now_utc = now_dt.replace(tzinfo=pytz.UTC)
		now_vietnam = now_utc.astimezone(vietnam_tz)
	
	# Convert to naive datetime for MySQL compatibility
	now_naive = now_vietnam.replace(tzinfo=None)
	print(f"🔄 Auto-share scheduler running at {now_vietnam} (Vietnam time)")
	print(f"🔄 Naive datetime for DB: {now_naive}")

	campaigns = _get_active_datasource_campaigns(now_dt)
	print(f"📊 Found {len(campaigns)} active campaigns")
	
	for c in campaigns:
		print(f"🎯 Processing campaign: {c.get('name')}")
		pages = _parse_select_pages(c.get("select_pages"))
		if not pages:
			print(f"⚠️ No pages configured for campaign {c.get('name')}")
			continue
		
		steps = _get_pending_steps(c["name"])
		print(f"📝 Found {len(steps)} steps for campaign {c.get('name')}")
		
		any_success = False
		for step in steps:
			should_post, scheduled_time = _should_post_step(step, now_dt)
			if not should_post:
				print(f"⏭️ Skipping step {step.get('name')} - not ready to post")
				continue
			
			print(f"📤 Posting step {step.get('name')} at {scheduled_time}")
			message = (step.get("template") or "").strip()
			url_image = step.get("image") or ""
			random_images = [
				"https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=1200",
				"https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d?w=1200",
				"https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=1200"
			]
			if (not url_image) or ("http" not in url_image):
				import random
				url_image = random.choice(random_images)
			
			step_success = False
			# Ưu tiên page_id được chỉ định ngay trong CampaignStep.action_config
			page_ids = []
			try:
				cfg = step.get("action_config") or {}
				if isinstance(cfg, str):
					import json as _json
					cfg = _json.loads(cfg)
				target_pid = cfg.get("target_page_id") or cfg.get("page_id")
				if target_pid:
					page_ids = [target_pid]
			except Exception:
				page_ids = []
			
			# Nếu không có page_id ở step thì fallback sang pages từ
			# Campaign.select_pages
			iter_pages = (
				page_ids if page_ids else [
					p.get("page_id") or p.get("external_account_id")
					for p in pages
				]
			)
			for pid in iter_pages:
				page_id = pid
				if not page_id:
					continue
				conn = _find_connection_by_page(page_id)
				if not conn:
					print(f"⚠️ No connection found for page {page_id}")
					continue
				
				print(f"📱 Publishing to page {page_id}")
				ok, post_id = _publish_facebook_post(
					page_id=page_id,
					tenant_name=conn.get("tenant_name"),
					email=conn.get("user_email"),
					message=message,
					url_image=url_image,
				)
				
				if ok:
					print(f"✅ Successfully posted to page {page_id}, post_id: {post_id}")
					step_success = True
					# Cập nhật shared_at và shared_post_id vào CampaignStep với thời gian thực
					try:
						frappe.db.set_value(
							"CampaignStep",
							step["name"],
							{
								"shared_at": now_naive,  # Sử dụng naive datetime
								"shared_post_id": post_id
							},
						)
						print(
							f"📝 Updated CampaignStep {step['name']} with shared_at: {now_naive}"
						)
					except Exception as e:
						print(f"❌ Error updating CampaignStep {step['name']}: {e}")
				else:
					print(f"❌ Failed to post to page {page_id}")
			
			any_success = any_success or step_success
			if step_success:
				print(f"✅ Step {step.get('name')} posted successfully")
		
		if any_success:
			# Cập nhật Campaign.last_shared_at để theo dõi tiến độ
			try:
				frappe.db.set_value(
					"Campaign",
					c["name"],
					{"last_shared_at": now_naive},  # Sử dụng naive datetime
				)
				print(f"📊 Updated Campaign {c['name']} last_shared_at: {now_naive}")
			except Exception as e:
				print(f"❌ Error updating Campaign {c['name']}: {e}")


def _get_active_datasource_campaigns(now_dt):
	"""Lấy các campaign đang hoạt động và có thể đăng bài"""
	filters = {
		"is_active": 1,
		"source_type": "DataSource",
		"start_date": ("<=", now_dt),
	}
	return frappe.get_all(
		"Campaign",
		filters=filters,
		fields=[
			"name",
			"campaign_name",
			"start_date",
			"end_date",
			"select_pages",
			"last_shared_at",
		],
	)


def _parse_select_pages(value) -> list:
	"""Parse select_pages JSON từ Campaign"""
	if not value:
		return []
	try:
		return value if isinstance(value, list) else json.loads(value)
	except Exception:
		return []


def _get_pending_steps(campaign_name: str) -> list:
	"""Lấy các step chưa được đăng bài"""
	steps = frappe.get_all(
		"CampaignStep",
		filters={"campaign": campaign_name},
		fields=[
			"campaign_step_name",
			"campaign",
			"template",
			"image",
			"step_order",
			"action_config",
			"delay_in_days",
			"scheduled_at",
			"shared_at",
		],
		order_by="step_order asc",
	)
	
	# Parse action_config nếu là string
	for s in steps:
		if s.get("action_config") and isinstance(s["action_config"], str):
			try:
				s["action_config"] = json.loads(s["action_config"])
			except Exception:
				pass
	
	return steps


def _should_post_step(step, now_dt) -> Tuple[bool, Optional[str]]:
	"""
	Kiểm tra xem step có nên được đăng bài không:
	- Ưu tiên CampaignStep.scheduled_at nếu có
	- Nếu không có, dùng Campaign.start_date + delay_in_days
	- Chỉ đăng nếu chưa đăng (shared_at = null)
	"""
	# Nếu đã đăng rồi thì skip
	if step.get("shared_at"):
		return False, None
	
	# Ưu tiên scheduled_at nếu có
	scheduled_at = step.get("scheduled_at")
	if scheduled_at:
		print(f"📅 Step {step.get('name')} has scheduled_at: {scheduled_at}")
		# Convert scheduled_at to Vietnam timezone for comparison
		vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
		if isinstance(scheduled_at, str):
			# Parse string to datetime
			scheduled_naive = datetime.strptime(scheduled_at, "%Y-%m-%d %H:%M:%S")
			scheduled_vietnam = vietnam_tz.localize(scheduled_naive)
		else:
			# Assume scheduled_at is already a datetime
			if scheduled_at.tzinfo:
				scheduled_vietnam = scheduled_at.astimezone(vietnam_tz)
			else:
				scheduled_vietnam = vietnam_tz.localize(scheduled_at)
		
		print(f"📅 Scheduled time (Vietnam): {scheduled_vietnam}")
		print(f"📅 Current time (Vietnam): {now_dt}")
		# Ensure both datetimes have timezone info
		if now_dt.tzinfo is None:
			now_vietnam = vietnam_tz.localize(now_dt)
		else:
			now_vietnam = now_dt.astimezone(vietnam_tz)
		should_post = scheduled_vietnam <= now_vietnam
		print(f"📅 Should post: {should_post}")
		return should_post, scheduled_at
	
	# Fallback: dùng delay_in_days từ campaign start_date
	# Lấy campaign start_date
	campaign_name = step.get("campaign")
	if not campaign_name:
		return False, None
	
	campaign_start = frappe.db.get_value("Campaign", campaign_name, "start_date")
	if not campaign_start:
		return False, None
	
	try:
		delay_days = step.get("delay_in_days") or 0
		delay = int(delay_days)
	except Exception:
		delay = 0
	
	candidate_time = add_to_date(campaign_start, days=delay)
	print(
		f"⏰ Step {step.get('name')} calculated time: {candidate_time} "
		f"(delay: {delay} days)"
	)
	
	return candidate_time <= now_dt, candidate_time


def _find_connection_by_page(page_id: str) -> Optional[dict]:
	"""Tìm External Connection dựa trên page_id"""
	row = frappe.db.get_value(
		"External Connection Account",
		{"external_account_id": page_id, "is_active": 1},
		["parent"],
		as_dict=True,
	)
	print(f"🔍 Found row in External Connection Account: {row}")
	if not row or not row.get("parent"):
		return None
	
	conn = frappe.db.get_value(
		"External Connection",
		row["parent"],
		[
			"name",
			"tenant_name",
			"user_email",
			"platform_type",
		],
		as_dict=True,
	)
	print(f"🔍 Found External Connection: {conn}")
	return conn


def _publish_facebook_post(
	page_id: str,	
	tenant_name: str,
	email: str,
	message: str,
	url_image: str,
) -> Tuple[bool, Optional[str]]:
	"""Đăng bài lên Facebook qua SocialHub API"""
	try:
		endpoint = (
			f"{SOCIALHUB_HOST}/api/method/mbw_socialhub.api.facebook.publish_post"
		)
		payload = {
			"page_id": page_id,
			"tenant_name": tenant_name,
			"email": email,
			"message": message,
			"url_image": url_image,
		}
		
		print(f"🌐 Calling SocialHub API: {endpoint}")
		print(f"📋 Payload: {json.dumps(payload, indent=2)}")
		
		resp = requests.post(endpoint, json=payload, timeout=30)
		print(f"📡 Response status: {resp.status_code}")
		
		if resp.status_code != 200:
			print(f"❌ HTTP error: {resp.status_code}")
			return False, None
		
		data = resp.json()
		print(f"📄 Response data: {json.dumps(data, indent=2)}")
		
		msg = data.get("message", {}) if isinstance(data, dict) else {}
		status = msg.get("status")
		post_id = msg.get("post_id")
		detail = msg.get("message")
		print(
			f"🔎 Response parsed -> status: {status}, "
			f"post_id: {post_id}, message: {detail}"
		)
		
		ok = status == "success"
		post_id = post_id if ok else None
		
		return ok, post_id
	except Exception as e:
		print(f"❌ Exception in _publish_facebook_post: {e}")
		return False, None


@frappe.whitelist()
def test_publish_post(
	page_id: str,
	tenant_name: str,
	email: str,
	message: Optional[str] = None,
	url_image: Optional[str] = None,
) -> dict:
	"""Test đăng 1 post với ảnh thật qua SocialHub.
	- Cung cấp page_id, tenant_name, email theo External Connection của bạn
	- Có thể truyền message và url_image; nếu không truyền sẽ dùng mặc định.
	"""
	try:
		default_image = "https://scontent.fhan2-3.fna.fbcdn.net/v/t39.30808-6/554383116_122098597533040742_9073985765290279057_n.jpg?stp=dst-jpg_p526x296_tt6&_nc_cat=111&ccb=1-7&_nc_sid=127cfc&_nc_ohc=uFw_ABYnrkwQ7kNvwHoP3eh&_nc_oc=AdnVx66QgcRwiQjvecdu8bUi1YK7p66haOs4ikG5H5p4CyNRCrYShjTLozc9LxgBuVE&_nc_zt=23&_nc_ht=scontent.fhan2-3.fna&_nc_gid=0wP4lc6AsBzb89gFCYqR-w&oh=00_AfaueNRkcSUg3PpjweT36RJnCmK287RaJGNyYuVuxZwJOg&oe=68DAA77E"
		default_message = "Test post từ auto_share_social_posts.test_publish_post"
		img = (url_image or default_image).strip()
		msg = (message or default_message).strip()
		ok, post_id = _publish_facebook_post(
			page_id=page_id,
			tenant_name=tenant_name,
			email=email,
			message=msg,
			url_image=img,
		)
		return {
			"success": bool(ok),
			"post_id": post_id,
			"used_image": img,
			"message": "Posted successfully" if ok else "Failed to post"
		}
	except Exception as e:
		frappe.log_error(f"test_publish_post error: {e}")
		return {"success": False, "error": str(e)}