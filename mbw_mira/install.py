import json
import frappe
from frappe import _
import os
from mbw_mira.scripts.feature_seeder import ensure_roles as ensure_mira_roles
from mbw_mira.scripts.feature_seeder import seed as seed_mbw_features

def after_install():
		# Optional: run automatically on fresh install
		try:
				seed_mira_email_templates_from_json()
				seed_mbw_mira_features_if_ready()
		except Exception:
				frappe.log_error(frappe.get_traceback(), "MIRA: seed templates failed")


def seed_mira_email_templates_from_json():
		"""
		Seed 3 default Mira Email Template records (idempotent by template_id).
		Maps body_html to html_content and body_plain_text to message.
		Stores extra metadata in project_data.
		"""
		templates = [
				{
						"template_id": "EMAIL-JF-WELCOME-001",
						"name": "Email Chào mừng Job Fair & Mời Tải CV",
						"subject": "Cảm ơn bạn, {{candidate_name}}! Cơ hội nghề nghiệp tại XYZ đang chờ bạn!",
						"status": "Active",
						"category": "Activation/Conversion",
						"template_type": "confirm-email",
						"sender_profile": {
								"sender_name": "Đội ngũ Tuyển dụng XYZ",
								"sender_email": "tuyendung@company.com",
						},
						"content": {
								"body_html": """
									<table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
										<tr>
											<td align="center">
												<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
													<tr><td>
														<h2 style="color:#1a1a1a;">Chào mừng Job Fair & Mời Tải CV</h2>
														<p>Chào bạn <strong>{{candidate_name}}</strong>,</p>
														<p>Công ty XYZ rất vui khi bạn đã ghé thăm gian hàng của chúng tôi! Để chúng tôi xem xét hồ sơ của bạn một cách nhanh chóng, hãy tải CV lên qua đường link dưới đây:</p>
														<p><a href="{{CV_UPLOAD_LINK}}" style="display:inline-block;background:#2563eb;color:#ffffff;text-decoration:none;padding:10px 16px;border-radius:6px;">Tải CV Lên Ngay</a></p>
														<p style="color:#6b7280;font-size:13px;">Nếu nút không hiển thị, hãy copy link sau vào trình duyệt: {{CV_UPLOAD_LINK}}</p>
														<p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
													</td></tr>
												</table>
											</td>
										</tr>
									</table>
								""".strip(),
								"body_plain_text": "Chào bạn {{candidate_name}}, cảm ơn bạn đã đăng ký. Vui lòng tải CV lên tại: {{CV_UPLOAD_LINK}}",
						},
						"personalization_config": {
								"candidate_fields": [
										{"variable_name": "candidate_name", "data_field": "full_name"}
								],
								"tracked_links": [
										{
												"variable_name": "CV_UPLOAD_LINK",
												"purpose": "CV Upload Form Access",
										}
								],
						},
				},
				{
						"template_id": "EMAIL-ENRICH-SKILL-002",
						"name": "Nhắc nhở & Thu thập Kỹ năng thay thế",
						"subject": "Bạn có 2 phút không, {{candidate_name}}? Chia sẻ thêm về chuyên môn của bạn!",
						"status": "Active",
						"category": "Data Enrichment/Nurturing",
						"template_type": "invited-email",
						"sender_profile": {
								"sender_name": "Đội ngũ Tuyển dụng XYZ",
								"sender_email": "tuyendung@company.com",
						},
						"content": {
								"body_html": """
									<table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
										<tr>
											<td align="center">
												<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
													<tr><td>
														<h2 style="color:#1a1a1a;">Nhắc nhở & Thu thập Kỹ năng</h2>
														<p>Chúng tôi thấy bạn chưa kịp tải CV lên. Thay vì chờ đợi, bạn có thể dành 2 phút điền vào form ngắn này để chia sẻ về kỹ năng và sở thích.</p>
														<p><a href="{{SKILL_FORM_LINK}}" style="display:inline-block;background:#10b981;color:#ffffff;text-decoration:none;padding:10px 16px;border-radius:6px;">Cập nhật Kỹ năng</a></p>
														<p style="color:#6b7280;font-size:13px;">Nếu nút không hiển thị, hãy copy link sau vào trình duyệt: {{SKILL_FORM_LINK}}</p>
														<p>Việc này giúp chúng tôi dễ dàng tìm thấy cơ hội phù hợp cho bạn!</p>
														<p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
													</td></tr>
												</table>
											</td>
										</tr>
									</table>
								""".strip(),
								"body_plain_text": "Chúng tôi chưa nhận được CV của bạn. Vui lòng cập nhật kỹ năng tại: {{SKILL_FORM_LINK}}",
						},
						"personalization_config": {
								"candidate_fields": [
										{"variable_name": "candidate_name", "data_field": "full_name"}
								],
								"tracked_links": [
										{
												"variable_name": "SKILL_FORM_LINK",
												"purpose": "Skill/Interest Enrichment Form Access",
										}
								],
						},
				},
				{
						"template_id": "EMAIL-ENGAGE-LEVEL-003",
						"name": "Đo lường Mức độ Quan tâm (Scoring)",
						"subject": "{{candidate_name}}, bạn nghĩ sao về cơ hội tại XYZ?",
						"status": "Active",
						"category": "Engagement/Scoring",
						"template_type": "reject-email",
						"sender_profile": {
								"sender_name": "Đội ngũ Tuyển dụng XYZ",
								"sender_email": "tuyendung@company.com",
						},
						"content": {
								"body_html": """
									<table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
										<tr>
											<td align="center">
												<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
													<tr><td>
														<h2 style="color:#1a1a1a;">Đo lường Mức độ Quan tâm</h2>
														<p>Chúng tôi thấy bạn đã xem một số thông tin gần đây của XYZ. Để hiểu rõ hơn về kỳ vọng của bạn, hãy giúp chúng tôi đánh giá mức độ quan tâm của bạn qua khảo sát ngắn (chỉ 30 giây).</p>
														<p><a href="{{INTEREST_FORM_LINK}}" style="display:inline-block;background:#f59e0b;color:#ffffff;text-decoration:none;padding:10px 16px;border-radius:6px;">Đánh giá Mức độ Quan tâm</a></p>
														<p style="color:#6b7280;font-size:13px;">Nếu nút không hiển thị, hãy copy link sau vào trình duyệt: {{INTEREST_FORM_LINK}}</p>
														<p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
													</td></tr>
												</table>
											</td>
										</tr>
									</table>
								""".strip(),
								"body_plain_text": "Hãy đánh giá mức độ quan tâm của bạn qua form này: {{INTEREST_FORM_LINK}}",
						},
						"personalization_config": {
								"candidate_fields": [
										{"variable_name": "candidate_name", "data_field": "full_name"}
								],
								"tracked_links": [
										{
												"variable_name": "INTEREST_FORM_LINK",
												"purpose": "Interest Level Scoring Form Access",
										}
								],
						},
				},
				{
						"template_id": "EMAIL-SUCCESS-CONFIRM-004",
						"name": "Xác nhận Tải CV/Hoàn thành Form thành công",
						"subject": "Thành công! Hồ sơ của bạn đã sẵn sàng tại hệ thống CRM của XYZ.",
						"status": "Active",
						"category": "Confirmation",
						"template_type": "other-email",
						"sender_profile": {
								"sender_name": "Đội ngũ Tuyển dụng XYZ",
								"sender_email": "tuyendung@company.com",
						},
						"content": {
								"body_html": """
									<table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
										<tr>
											<td align="center">
												<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
													<tr><td>
														<h2 style="color:#1a1a1a;">Xác nhận Hoàn tất</h2>
														<p><strong>{{candidate_name}}</strong> thân mến,</p>
														<p>Hồ sơ/CV của bạn đã được tải lên/cập nhật thành công. Đội ngũ tuyển dụng của chúng tôi đang xem xét. Chúng tôi sẽ liên hệ với bạn trong vòng X ngày làm việc.</p>
														<p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
													</td></tr>
												</table>
											</td>
										</tr>
									</table>
								""".strip(),
								"body_plain_text": "Hồ sơ của bạn đã được cập nhật thành công. Chúng tôi sẽ liên hệ trong X ngày làm việc.",
						},
						"personalization_config": {"tracked_links": []},
				},
		]

		for t in templates:
				# Idempotent check by template_id
				exists = frappe.get_all(
						"Mira Email Template",
						filters={"template_id": t["template_id"]},
						pluck="name",
						limit=1,
				)
				if exists:
						continue

				# Build document fields mapped to your DocType
				doc_data = {
						"doctype": "Mira Email Template",
						"template_id": t["template_id"],
						"template_name": t["name"],
						"subject": t.get("subject", ""),
						"html_content": t.get("content", {}).get("body_html", ""),
						"message": t.get("content", {}).get("body_plain_text", ""),
						"template_type": t.get("template_type", ""),
						"is_active": 1,
						# Keep extra metadata for later use in builder/export
						"project_data": json.dumps({
								"status": t.get("status"),
								"category": t.get("category"),
								"sender_profile": t.get("sender_profile"),
								"personalization_config": t.get("personalization_config"),
						}, ensure_ascii=False),
				}

				doc = frappe.get_doc(doc_data)
				doc.insert(ignore_permissions=True)

		frappe.db.commit()
	
def install_test():
	insert_component()
	insert_all_script_data()
	insert_all_pages()
	insert_builder_settings()

def insert_component():
	file_name = "builder_components.json"
	insert_component_data(file_name)

def insert_all_script_data():
	file_name = "builder_scripts.json"
	read_script_module_path(file_name)

def insert_all_pages():
	file_name = "builder_pages.json"
	read_page_module_path(file_name)

def insert_builder_settings():
	file_name = "builder_settings.json"
	read_builder_settings_module_path(file_name)

def insert_component_data(file_name):
	path = frappe.get_app_path("mbw_mira")
	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>2",path)
	file_path = os.path.join(path,'json_data_v2',file_name)
	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>3",file_path)
	if os.path.exists(file_path):
		with open(file_path, 'r') as f:
			out = json.load(f)
		for i in out:
			try:
				# if(not frappe.db.exists({"doctype": "Component", "name": i.get('component_id')})):
				frappe.get_doc(i).insert()
			except frappe.NameError:
				pass
			except Exception as e:
				frappe.log_error(frappe.get_traceback(), file_name)
				
def read_script_module_path(file_name):
	path = frappe.get_app_path("mbw_mira")
	file_path = os.path.join(path,'json_data_v2',file_name)
	if os.path.exists(file_path):
		with open(file_path, 'r') as f:
			out = json.load(f)
		for i in out:
			try:
				if(not frappe.db.exists({"doctype": i.get('doctype'), "name": i.get('__name')})):
					script_doc = frappe.get_doc(i).insert()
					frappe.db.sql("""UPDATE `tabBuilder Client Script` SET 
								name=%(c_name)s WHERE name=%(s_name)s""",{"c_name":i.get('__name'),"s_name":script_doc.name})
					frappe.db.commit()
			except Exception as e:
				frappe.log_error(frappe.get_traceback(), "read_script_module_path")

def read_page_module_path(file_name):
	path = frappe.get_app_path("mbw_mira")
	file_path = os.path.join(path,'json_data_v2',file_name)
	if os.path.exists(file_path):
		with open(file_path, 'r') as f:
			out = json.load(f)
			out_json = {}
		for index,i in enumerate(out):
			try:
				if i.get('client_scripts') :
					out_json[i.get('page_title')] = i['client_scripts']
					del i['client_scripts']
				if(not frappe.db.exists({"doctype": i.get('doctype'), "page_title": i.get('page_title')})):
					page_doc = frappe.get_doc(i).insert()
					frappe.db.set_value(i.get('doctype'), page_doc.get('name'), 'route', i.get('route'))
					# frappe.log_error(title="out_json[index]", message=out_json)
					if(out_json[i.get('page_title')]):
						for child_index,script in enumerate(out_json[i.get('page_title')]): 
							# frappe.log_error(title="queryyyy", message=f"""INSERT INTO `tabBuilder Page Client Script` (name,builder_script,parent,parentfield,parenttype)
							# VALUES ('{script.get('builder_script')}','{script.get('builder_script')}','{page_doc.name}','client_scripts','Builder Page') """)
							frappe.db.sql(f"""INSERT INTO `tabBuilder Page Client Script` (name,builder_script,parent,parentfield,parenttype)
							VALUES ('{script.get('builder_script') + str(index) + str(child_index)}','{script.get('builder_script')}','{page_doc.name}','client_scripts','Builder Page') """)
			except Exception as e:
				frappe.log_error(frappe.get_traceback(), "read_page_module_path")
		frappe.db.set_value("Website Settings","Website Settings","home_page","f-landing")

def read_builder_settings_module_path(file_name):
	path = frappe.get_app_path("mbw_mira")
	file_path = os.path.join(path,'json_data_v2',file_name)
	if os.path.exists(file_path):
		out = ''
		with open(file_path, 'r') as f:
			out = json.load(f)
		try:
			frappe.get_doc(out).insert()
		except frappe.NameError:
			pass
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), file_name)

def seed_mbw_mira_features_if_ready():
	"""Gọi seeder: tạo Role → Feature → Link. Bỏ qua nếu thiếu DocType."""
	try:
		need = [
			"MBW Feature Settings",
			"MBW Feature Setting Detail",
			"MBW Feature Role Permission",
		]
		missing = [dt for dt in need if not frappe.db.exists("DocType", dt)]
		if missing:
			print("⏭️ Skip seeding MBW ATS features (missing DocTypes):", ", ".join(missing))
			print("   → Chạy bench migrate rồi gọi lại sau: bench --site <site> execute mbw_ats.scripts.feature_seeder.seed")
			return

		print("=== Seed MBW ATS Features (import module) ===")
		ensure_mira_roles()
		seed_mbw_features()
		print("✅ Done seeding MBW Mira Features")

	except Exception as e:
		frappe.log_error(f"Seed MBW ATS features failed: {e}", "MBW Mira Install")
		print(f"❌ Seed MBW ATS features failed: {e}")