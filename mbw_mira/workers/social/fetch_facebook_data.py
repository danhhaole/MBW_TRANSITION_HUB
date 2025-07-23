# talent_pool/talent_pool/doctype/job_opening/job_opening.py
import frappe
from frappe import _
from mbw_mira.integrations.social.facebook_provider import FacebookProvider

def fetch_facebook_data():
    pass


def post_to_facebook(doc, campaign_name):
    if not doc.post_to_facebook or doc.facebook_post_status == 'Posted':
        return

    try:
        campaign = frappe.get_doc("Campaign", campaign_name)
        source_name = campaign.source
        with FacebookProvider(source_name) as provider:
            message = f"New Job Opportunity: {doc.job_title}\n\n{doc.description}\nLocation: {doc.location}\nApply now: {frappe.utils.get_url('/apply-job?job={0}').format(doc.name)}"
            response = provider.post_to_page(doc.facebook_page_id, message)
            post_id = response.get("id")
            frappe.db.set_value('TalentSegmet', doc.name, {
                'facebook_post_id': post_id,
                'facebook_post_status': 'Posted'
            })
            frappe.msgprint(_("Job posted successfully on Facebook: {0}").format(post_id))
    except Exception as e:
        frappe.log_error(f"Failed to post job to Facebook: {str(e)}")
        frappe.throw(_("Error posting job to Facebook: {0}").format(str(e)))

def post_to_feed(doc, campaign_name):
    if not doc.post_to_facebook or doc.facebook_post_status == 'Posted':
        return

    try:
        campaign = frappe.get_doc("Campaign", campaign_name)
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