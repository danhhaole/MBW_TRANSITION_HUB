# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class TalentProfiles(Document):
	pass

	def validate(self):
		# Check trùng talent_id,candidate_id
		self.validate_unique_talent_profiles()

	def after_insert(self):
		#Sau khi insert nếu có postion thì đưa vào TalentProfilesSegment luôn, đối với trường hợp chiến dịch không có thiết lập phân loại
		if self.position:
			create_talentprofiles_segment(self)
			

def create_talentprofiles_segment(self):
	#Tìm talentsegment theo title (position)
	segment = frappe.db.get_value("TalenSegment",{"title":self.position},"name")
	if segment:
		#Kiểm tra tồn tại profile trong segment chưa
		profile_segment_exists = frappe.db.exists("TalentProfilesSegment",{"talent_id":self.name,"segment_id":segment})
		if not profile_segment_exists:
			doc = frappe.get_doc({
				"doctype":"TalentProfilesSegment",
				"talent_id":self.name,
    			"segment_id":segment,
				"added_at": now_datetime(),
				"added_by": frappe.session.user
       		})
			doc.insert(ignore_permissions=True)
			frappe.db.commit()

	return True
#     "talent_id",
#   "segment_id",
#   "match_score",
#   "added_at",
#   "added_by"

	def validate_unique_talent_profiles(self):
		"""
		Kiểm tra xem đã tồn tại TalentProfiles với cùng
		talent_id + candidate_id (ngoại trừ chính nó) hay chưa.
		"""
		filters = {
			"email": self.email
		}

		existing = frappe.db.exists("TalentProfiles", filters)

		if existing and existing != self.name:
			frappe.throw(
            frappe._(
                "A TalentProfiles with Email <b>{0}</b> already exists: <a href='/app/TalentProfiles/{1}'>{1}</a>"
            ).format(self.email, existing),
            title=frappe._("Duplicate TalentProfiles"),
        )
