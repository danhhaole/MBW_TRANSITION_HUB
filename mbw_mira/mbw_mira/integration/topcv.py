import frappe
import hmac
import hashlib
import json
import requests
import mimetypes
from frappe import _
from frappe.utils import get_url_to_form
from frappe.utils.file_manager import save_file
import re
from mbw_mira.api.ai import (
    extract_cv_backend
)

# Thay thế bằng secret key của bạn từ TopCV
TOPCV_BASEURL = frappe.conf.get("topcv_baseurl") or "https://partner.topcv.vn"#"https://api-srp.qc.topcv.me/api"


@frappe.whitelist()
def connect_topcv():
    try:
        #Lấy dữ liệu từ request
        if frappe.request.method != "POST":
            frappe.throw(_("Only POST method is allowed"))
        data = frappe.request.data
        if not data:
            frappe.throw(_("No data received"))
        
        payload = json.loads(data)
        secret_key = payload.get('secret_key_topcv')
        if not secret_key:
            frappe.throw(_("Secret key required"))
            return _("Secret key required")
        access_token = payload.get('access_token_topcv')
        if not access_token:
            frappe.throw(_("Access token required"))
            return _("Access token required")
        
        headers = {
            #"Authorization": "Bearer tkoBjKTFTNfFDzkmGe0z9ppUusIeexVy",
            "Secret-Key":secret_key,
            "Content-Type":"application/json",
            "Host":"171.244.57.245"
        }
        body ={
            "employer_api_key":access_token
        }
        response = requests.post(f"{TOPCV_BASEURL}/api/connect",json=body,headers=headers)
        
        if response.status_code == 200:
            top_success = response.json()
            doc = frappe.get_doc({
                "doctype":"MIRA_Integrations",
                "active_topcv":True,
                "access_token_topcv":access_token,
                "secret_key_topcv":secret_key,
                "api_access_token":top_success.get("data").get("access_token"),
                "status_topcv":True
            })
            doc.save(ignore_permissions=True)
            frappe.db.commit()  
        else:
            #print(response.text)
            frappe.log_error(f"Connect error: {response.text}")
            frappe.throw("Connect error")
            return {"message": "Connect error"}
            
            
    except Exception as e:
        frappe.log_error(f"TopCV Connect Error: {str(e)}")
        frappe.throw(_("TopCV Connect Error"))
        return {"message": "Connect error"}

@frappe.whitelist()
def disconnect_topcv():
    try:
        #Lấy dữ liệu từ request
        if frappe.request.method != "PUT":
            frappe.throw(_("Only PUT method is allowed"))
        
        doc = frappe.get_doc("MIRA_Integrations")
        
        secret_key = doc.get('secret_key_topcv')
        if not secret_key:
            frappe.throw(_("Secret key required"))
        access_token = doc.get('access_token_topcv')
        if not access_token:
            frappe.throw(_("Access token required"))
        
        headers = {
            "Authorization": f"Bearer {doc.api_access_token}",
            "Secret-Key":secret_key,
            "Content-Type":"application/json",
            "Host":"171.244.57.245"
        }
        body ={
            "employer_api_key":access_token
        }
        response = requests.put(f"{TOPCV_BASEURL}/api/disconnect",json=body,headers=headers)
        
        if response.status_code == 200:
            top_success = response.json()
            doc = frappe.get_doc({
                "doctype":"MIRA_Integrations",
                "active_topcv":0,
                "access_token_topcv":"",
                "secret_key_topcv":"",
                "api_access_token":"",
                "status_topcv":0
            })
            doc.save(ignore_permissions=True)
            frappe.db.commit()
        else:
            frappe.log_error(response.text)
            frappe.throw(response.text)
            return {"message": "Disconnect error"}
            
            
    except Exception as e:
        frappe.log_error(f"TopCV Disconnect Error: {str(e)}")
        frappe.throw(_("TopCV Disconnect Error"))
        return {"message": "Disconnect error"}


@frappe.whitelist(allow_guest=True)
def handle_topcv_webhook():
    """Xử lý webhook từ TopCV"""
    try:
        # Lấy dữ liệu từ request
        if frappe.request.method != "POST":
            frappe.throw(_("Only POST method is allowed"))

        data = frappe.request.data
        if not data:
            frappe.throw(_("No data received"))

        payload = json.loads(data)
        signature = payload.get("signature")
        #print(payload)
        # Xác minh chữ ký
        if not verify_signature(payload, signature):
            frappe.log_error("Invalid signature")

        event_type = payload.get("event_type")

        if event_type == "apply":
            handle_new_application(payload)
        elif event_type == "job_approved":
            handle_job_approved(payload)
        elif event_type == "job_rejected":
            handle_job_rejected(payload)
        else:
            frappe.throw(_("Unknown event type: {0}").format(event_type))
        

    except Exception as e:
        frappe.log_error(f"TopCV Webhook Error: {str(e)}")
        frappe.throw("Lỗi webhook")

def verify_signature(payload, received_signature):
    """Xác minh chữ ký HMAC_SHA256"""
    event_type = payload.get("event_type")

    if event_type == "apply":
        data_string = f"event_type={event_type}&job_id={payload.get('job_id')}&candidate_phone={payload.get('candidate_phone')}&candidate_id={payload.get('candidate_id')}"
    elif event_type in ["job_approved", "job_rejected"]:
        data_string = f"event_type={event_type}&job_id={payload.get('job_id')}&recruitment_campaign_id={payload.get('recruitment_campaign_id')}"
    else:
        return False
    doc = frappe.get_doc("MIRA_Integrations")
    TOPCV_SECRET_KEY = doc.get("api_access_token")
    # Tạo chữ ký
    computed_signature = hmac.new(
        key=TOPCV_SECRET_KEY.encode("utf-8"),
        msg=data_string.encode("utf-8"),
        digestmod=hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(computed_signature, received_signature)

def handle_new_application(payload):
    """Xử lý sự kiện ứng tuyển mới"""
    try:
        # Kiểm tra ứng viên đã tồn tại qua email
        candidate = frappe.get_all(
            "Candidate",
            filters={"can_email": payload.get("candidate_email")},
            fields=["name"],
            limit=1,
        )

        # Lấy ra job_opening
        job = frappe.get_doc(doctype="Mira Job Opening",filters={"top_cv_id":payload.get("job_id")})

        if not candidate:
            # Tạo mới ứng viên
            candidate_doc = frappe.get_doc(
                {
                    "doctype": "Candidate",
                    "can_full_name": payload.get("candidate_name"),
                    "can_email": payload.get("candidate_email"),
                    "can_phone": payload.get("candidate_phone"),
                    "can_gender": payload.get(
                        "gender"
                    ),  # Lưu ý: API TopCV ghi 'genger' thay vì 'gender'
                    "candidatesource_id": "TopCV",
                    "can_id": payload.get("candidate_id"),
                    "can_application_date": payload.get("apply_at"),
                }
            )
            if job:
                candidate_doc.job_opening_id = job.name
            frappe.flags.ignore_webhook_sync = True
            candidate_doc.save(ignore_permissions=True)  
            frappe.db.commit()

            file_url = payload.get("download_url")     
            cv_url = payload.get("cv_url")
            if file_url:               
                file_response = requests.get(file_url)
                content_disposition = file_response.headers.get("Content-Disposition", "")

                if "filename=" in content_disposition:
                    match = re.search(r'filename="?([^"]+)"?', content_disposition)
                    if match:
                        file_name = match.group(1)

                    if not file_name:
                        file_name = cv_url.split("/").pop().split("#").shift()

                    if file_response.status_code == 200:
                        # Lưu file vào hệ thống và liên kết với ứng viên
                        mime_type = file_response.headers.get("Content-Type", "")
                        file_saved =save_file_candidate(candidate_doc.name,file_name,file_response.content,mime_type)

                        # Xử lý gói API extract cv
                        print("queued")
                        enqueue_cv_extraction(file_saved.name, candidate_doc.name)

    except Exception as e:
        frappe.log_error(f"Error handling new application: {str(e)}")
        raise

def handle_job_approved(payload):
    """Xử lý sự kiện tin tuyển dụng được duyệt"""
    try:
        # Cập nhật trạng thái tin tuyển dụng
        job_opening = frappe.get_all(
            "Mira Job Opening",
            filters={"topcv_job_id": payload.get("job_id")},
            fields=["name"],
            limit=1
        )

        if job_opening:
            job_doc = frappe.get_doc("Mira Job Opening", job_opening[0].name)
            job_doc.status = "Approved"
            job_doc.recruitment_campaign_id = payload.get("recruitment_campaign_id")
            job_doc.save(ignore_permissions=True)
            frappe.db.commit()
        else:
            frappe.log_error(f"Job Opening with TopCV job_id {payload.get('job_id')} not found")

    except Exception as e:
        frappe.log_error(f"Error handling job approved: {str(e)}")
        raise

def handle_job_rejected(payload):
    """Xử lý sự kiện tin tuyển dụng bị từ chối"""
    try:
        # Cập nhật trạng thái tin tuyển dụng
        job_opening = frappe.get_all(
            "Mira Job Opening",
            filters={"topcv_job_id": payload.get("job_id")},
            fields=["name"],
            limit=1
        )

        if job_opening:
            job_doc = frappe.get_doc("Mira Job Opening", job_opening[0].name)
            job_doc.status = "Rejected"
            job_doc.recruitment_campaign_id = payload.get("recruitment_campaign_id")
            job_doc.reject_reason = payload.get("reject_reason")
            job_doc.save(ignore_permissions=True)
            frappe.db.commit()
        else:
            frappe.log_error(f"Job Opening with TopCV job_id {payload.get('job_id')} not found")

    except Exception as e:
        frappe.log_error(f"Error handling job rejected: {str(e)}")
        raise


# Save file to candidate
def save_file_candidate(dn,file_name,content,mime_type):
    extension = mimetypes.guess_extension(mime_type)
    file_type = extension.upper()
    file_saved = save_file(
        fname=file_name,
        content=content,
        dt="Candidate",
        dn=dn,
        is_private=0
    )
    # Lưu MIME type vào record
    file_saved.file_type = file_type
    frappe.db.commit()
    #Update lại cv
    doc = frappe.get_doc("Candidate",dn)
    doc.can_cv = file_saved.file_url
    frappe.flags.ignore_webhook_sync = True
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return file_saved

def enqueue_cv_extraction(file_name, candidate_name):
    frappe.enqueue(
        method="mbw_mira.api.ai.extract_and_update_candidate",
        file_name=file_name,
        candidate_name=candidate_name,
        queue="short",
        timeout=300,
        now=True,
        job_name=f"Extract CV for {candidate_name}"
    )
