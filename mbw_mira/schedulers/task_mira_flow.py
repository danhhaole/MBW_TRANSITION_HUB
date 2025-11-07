import frappe
from frappe.utils import now_datetime

#Chay quét lấy danh sách action và trigger

def enqueue_for_action(action_type, queue_name):
    tasks = frappe.get_all(
        "Mira Task",
        filters={
            "status": ["in",["Pending","In Pending"]],
            "action_type": action_type,
            "scheduled_at": ("<=", now_datetime())
        },
        fields=["name"],
        order_by="order_task asc"
    )
    print("task",tasks)
    from mbw_mira.workers.task_runner import process_task
    for t in tasks:
        process_task(t.name)
        # frappe.enqueue(
        #     "mbw_mira.workers.task_runner.process_task",
        #     job_id=queue_name,
        #     queue="short",
        #     #timeout=300,
        #     task_id=t.name,
        # )

# ========================
# SCHEDULERS
# ========================

def schedule_message_tasks(): enqueue_for_action("MESSAGE", "mira_message_queue")
def schedule_sms_tasks(): enqueue_for_action("SMS", "mira_sms_queue")
def schedule_email_tasks(): enqueue_for_action("EMAIL", "mira_email_queue")

def schedule_zalo_tasks(): enqueue_for_action("ZALO", "mira_zalo_queue")
def schedule_zalo_care_tasks(): enqueue_for_action("ZALO_CARE", "mira_zalo_care_queue")
def schedule_zalo_zns_tasks(): enqueue_for_action("ZALO_ZNS", "mira_zalo_zns_queue")

def schedule_start_flow_tasks(): enqueue_for_action("START_FLOW", "mira_flow_queue")
def schedule_subscribe_sequence_tasks(): enqueue_for_action("SUBSCRIBE_TO_SEQUENCE", "mira_sequence_queue")
def schedule_unsubscribe_sequence_tasks(): enqueue_for_action("UN_SUBSCRIBE_TO_SEQUENCE", "mira_sequence_queue")

def schedule_smart_delay_tasks(): enqueue_for_action("SMART_DELAY", "mira_delay_queue")
def schedule_ai_call_tasks(): enqueue_for_action("AI_CALL", "mira_ai_queue")

def schedule_add_tag_tasks(): enqueue_for_action("ADD_TAG", "mira_tag_queue")
def schedule_remove_tag_tasks(): enqueue_for_action("REMOVE_TAG", "mira_tag_queue")

def schedule_add_custom_field_tasks(): enqueue_for_action("ADD_CUSTOM_FIELD", "mira_custom_field_queue")
def schedule_remove_custom_field_tasks(): enqueue_for_action("REMOVE_CUSTOM_FIELD", "mira_custom_field_queue")

def schedule_lead_score_tasks(): enqueue_for_action("LEAD_SCORE", "mira_lead_queue")

def schedule_external_request_tasks(): enqueue_for_action("EXTERNAL_REQUEST", "mira_webhook_queue")

def schedule_email_ai_tasks(): enqueue_for_action("EMAIL_AI", "mira_ai_email_queue")
def schedule_content_ai_tasks(): enqueue_for_action("CONTENT_AI", "mira_ai_content_queue")

def schedule_sent_notification_tasks(): enqueue_for_action("SENT_NOTIFICATION", "mira_notify_queue")
def schedule_unsubscribe_tasks(): enqueue_for_action("UNSUBSCRIBE", "mira_unsubscribe_queue")
