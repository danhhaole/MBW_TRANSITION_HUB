# talent_pool/talent_pool/doctype/job_opening/job_opening.py
from urllib.parse import urlparse
import frappe
from frappe import _
from mbw_mira.integrations.social.facebook_provider import FacebookProvider
from frappe.utils import now, add_days, get_datetime, now_datetime, get_url
import json
import secrets
import requests
from typing import Dict, List, Optional, Any

host = frappe.conf.get("socialhub") or "https://socialhub.mbwcloud.com"

def fetch_facebook_data():
    pass


def post_to_facebook(share_name):
    share_doc = frappe.get_doc("Mira Campaign Social",share_name)
    _process_job_share(share_doc)

def post_to_feed(doc, campaign_name):
    if not doc.post_to_facebook or doc.facebook_post_status == 'Posted':
        return

    try:
        campaign = frappe.get_doc("Mira Campaign", campaign_name)
        source_name = campaign.source
        with FacebookProvider(source_name) as provider:
            message = f"New Job Opportunity: {doc.job_title}\n\n{doc.description}\nLocation: {doc.location}\nApply now: {doc.facebook_post_link or frappe.utils.get_url('/apply-job?job={0}').format(doc.name)}"
            response = provider.post_to_feed(
                target_id=doc.facebook_target_id or 'me',
                message=message,
                link=doc.facebook_post_link,
                picture=doc.facebook_post_picture
            )
            post_id = response.get("id")
            frappe.db.set_value('TalentSegmet', doc.name, {
                'facebook_post_id': post_id,
                'facebook_post_status': 'Posted'
            })
            frappe.msgprint(_("Job posted successfully on Facebook: {0}").format(post_id))
    except Exception as e:
        frappe.log_error(f"Failed to post job to Facebook: {str(e)}")
        frappe.throw(_("Error posting job to Facebook: {0}").format(str(e)))
        
        
def _process_job_share(share_doc):
    """
    Internal function to process job sharing
    """
    try:
        connection = frappe.get_doc("Mira External Connection", share_doc.external_connection)
        job = frappe.get_doc("JobOpening", share_doc.job)

        # Parse share_data safely
        share_data = {}
        if share_doc.share_data:
            try:
                share_data = json.loads(share_doc.share_data)
            except (json.JSONDecodeError, TypeError):
                share_data = {}

        # Process based on platform type

        result = _share_to_facebook(connection, job, share_doc, share_data)

        # Update share record with results
        share_doc.status = "Success" if result.get("success") else "Failed"
        share_doc.shared_at = now_datetime() if result.get("success") else None
        share_doc.external_post_id = result.get("post_id")
        share_doc.external_url = result.get("post_url")
        share_doc.target_page_name = result.get("target_page_name")

        if not result.get("success"):
            share_doc.error_message = result.get("error", "Unknown error")

        # Store response data
        if result.get("response_data"):
            share_doc.response_data = json.dumps(result.get("response_data"))

        share_doc.save(ignore_permissions=True)


        return result

    except Exception as e:
        # Update share record with error
        share_doc.status = "Failed"
        share_doc.error_message = str(e)
        share_doc.save(ignore_permissions=True)

        frappe.log_error(f"Error processing job share: {str(e)}")
        return {"success": False, "error": str(e)}


def _share_to_facebook(connection, job, share_doc, share_data):
    """Share job to Facebook via SocialHub API"""
    try:
        # Get Facebook page ID from share_data or connection accounts
        page_id = share_data.get("target_page_id")
        print("page_id>>>>>>>>>>>:", page_id)
        url_image = share_data.get("image_url")
        if url_image and "http" not in url_image:
            url_image = f"{get_url_without_port()}{url_image}"
        if not page_id:
            # Get first active Facebook page from child table
            facebook_account = None
            connection_obj = frappe.get_doc("Mira External Connection", connection.name)
            for account in connection_obj.connected_accounts:
                if account.is_active and account.account_type == "Page":
                    facebook_account = account.external_account_id
                    break
            page_id = facebook_account

        if not page_id:
            return {"success": False, "error": "No Facebook page selected or available"}

        # Prepare post content
        job_url = f"{get_url_without_port()}/mbw_mira/jobs/{job.job_url_cms}?utm_source=facebook&owner={job.jo_contact_email}"
        message = f"{share_doc.message}\n\nApply here: {job_url}"

        # Prepare image URL if available

        # SocialHub API call

        socialhub_url = f"{host}/api/method/mbw_socialhub.api.facebook.publish_post"
        post_data = {
            "page_id": page_id,
            "tenant_name": connection.tenant_name,
            "email": connection.user_email,
            "message": message,
            "url_image": url_image,
        }

        response = requests.post(socialhub_url, json=post_data, timeout=12000)
        response_data = response.json()
        print("page_id", response_data)
        if (
            response.status_code == 200
            and response_data.get("message", {}).get("status") == "success"
        ):
            post_id = response_data.get("message", {}).get("post_id")

            # Get permalink URL
            try:
                permalink_response = requests.get(
                    f"{host}/api/method/mbw_socialhub.api.facebook.get_permalink_post",
                    params={"page_id": page_id, "post_id": post_id},
                    timeout=30,
                )

                post_url = ""
                if permalink_response.status_code == 200:
                    permalink_data = permalink_response.json()
                    if permalink_data.get("message", {}).get("status") == "success":
                        post_url = (
                            permalink_data.get("message", {})
                            .get("data", {})
                            .get("permalink_url", "")
                        )
            except Exception:
                post_url = ""

            return {
                "success": True,
                "post_id": post_id,
                "post_url": post_url,
                "target_page_name": share_data.get("target_page_name", "Facebook Page"),
                "response_data": response_data,
            }
        else:
            error_msg = response_data.get("message", {}).get(
                "message", f"Facebook API error: HTTP {response.status_code}"
            )
            return {
                "success": False,
                "error": error_msg,
                "response_data": response_data,
            }

    except requests.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
def get_url_without_port():
    # Prefer explicit public base URL from config (works with Cloudflare tunnels)
    base = (
        frappe.conf.get("mbw_public_base_url")
        or frappe.conf.get("public_base_url")
        or None
    )
    if base:
        parsed = urlparse(base)
        return f"{parsed.scheme}://{parsed.hostname}"
    # Fallback to site URL without port
    url = get_url()
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.hostname}"