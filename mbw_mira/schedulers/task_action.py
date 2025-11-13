import frappe
from datetime import datetime

def send_email_action_campaign():
    """
    Process scheduled SEND_EMAIL actions:
    - Find actions with status=SCHEDULED, scheduled_at<=now
    - action_type='SEND_EMAIL'
    - Enqueue worker job
    """
    now = datetime.now()
    actions = frappe.get_all(
        "Mira Action",
        filters={
            "status": "SCHEDULED",
            "action_type":"SEND_EMAIL",
            "scheduled_at": ["<=", now],
        },
        fields=["name"]
    )

    for a in actions:
        frappe.enqueue(
                "mbw_mira.workers.process_action.process_email_action",
                queue="short",
                action_name=a.name
            )
            
    return True

# def send_zalo_action_campaign():
#     """
#     Process scheduled SEND_ZALO actions:
#     - Find actions with status=SCHEDULED, scheduled_at<=now
#     - action_type='SEND_ZALO'
#     - Enqueue worker job
#     """
#     now = datetime.now()
#     actions = frappe.get_all(
#         "Mira Action",
#         filters={
#             "status": "SCHEDULED",
#             "action_type":"SEND_ZALO",
#             "scheduled_at": ["<=", now],
#         },
#         fields=["name"]
#     )

#     for a in actions:
#         frappe.enqueue(
#                 "mbw_mira.workers.process_action.process_zalo_action",
#                 queue="short",
#                 action_name=a.name
#             )
            
#     return True

# def post_facebook_action_campaign():
#     """
#     Process scheduled POST_FACEBOOK actions:
#     - Find actions with status=SCHEDULED, scheduled_at<=now
#     - action_type='POST_FACEBOOK'
#     - Enqueue worker job
#     """
#     now = datetime.now()
#     actions = frappe.get_all(
#         "Mira Action",
#         filters={
#             "status": "SCHEDULED",
#             "action_type":"POST_FACEBOOK",
#             "scheduled_at": ["<=", now],
#         },
#         fields=["name"]
#     )

#     for a in actions:
#         frappe.enqueue(
#                 "mbw_mira.workers.process_action.process_facebook_action",
#                 queue="short",
#                 action_name=a.name
#             )
            
#     return True

# def post_topcv_action_campaign():
#     """
#     Process scheduled POST_TOPCV actions:
#     - Find actions with status=SCHEDULED, scheduled_at<=now
#     - action_type='POST_TOPCV'
#     - Enqueue worker job
#     """
#     now = datetime.now()
#     actions = frappe.get_all(
#         "Mira Action",
#         filters={
#             "status": "SCHEDULED",
#             "action_type":"POST_TOPCV",
#             "scheduled_at": ["<=", now],
#         },
#         fields=["name"]
#     )

#     for a in actions:
#         frappe.enqueue(
#                 "mbw_mira.workers.process_action.process_topcv_action",
#                 queue="short",
#                 action_name=a.name
#             )
            
#     return True
