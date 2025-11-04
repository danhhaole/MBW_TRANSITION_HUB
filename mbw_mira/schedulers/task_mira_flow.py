import frappe
#Chay quét lấy danh sách action và trigger

def scan_action_flow():
    try:
        actions = frappe.get_all("Mira Flow Action")
        if actions:
            for tmc in actions:
                tmc.status = 1
    except Exception as e:
        pass