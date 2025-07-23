# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now, now_datetime, add_days
from mbw_mira.utils import find_candidates_fuzzy

class Campaign(Document):
    pass

    def on_trash(self):
        #Kiểm tra trạng thái là draff hoặc chưa active 
        if self.status == "DRAFT" or not self.is_active:
            #Kiểm tra xem có step chưa để xóa CampaignStep trước
            pass

def delete_campaign_step():
    pass