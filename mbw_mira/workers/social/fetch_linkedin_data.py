import frappe
from frappe import _
from mbw_mira.integrations.social.linkedin_provider import LinkedInProvider

def fetch_linkedin_data():
    pass


def post_to_linkedin(doc, campaign_name):
    if not doc.post_to_linkedin or doc.linkedin_post_status == 'Posted':
        return

    try:
        campaign = frappe.get_doc("Mira Campaign", campaign_name)
        source_name = campaign.source
        with LinkedInProvider(source_name) as provider:
            job_data = {
                "title": doc.job_title,
                "description": doc.description,
                "location": doc.location,
                "employment_type": doc.employment_type or "FULL_TIME",
                "company": f"urn:li:organization:{doc.company_page_id}"
            }
            response = provider.post_job(job_data)
            job_id = response.get("id")
            frappe.db.set_value('TalentSegmet', doc.name, {
                'linkedin_job_id': job_id,
                'linkedin_post_status': 'Posted'
            })
            frappe.msgprint(_("Job posted successfully on LinkedIn: {0}").format(job_id))
    except Exception as e:
        frappe.log_error(f"Failed to post job to LinkedIn: {str(e)}")
        frappe.throw(_("Error posting job to LinkedIn: {0}").format(str(e)))

def post_to_share(doc, campaign_name):
    if not doc.post_to_linkedin or doc.linkedin_post_status == 'Posted':
        return

    try:
        campaign = frappe.get_doc("Mira Campaign", campaign_name)
        source_name = campaign.source
        with LinkedInProvider(source_name) as provider:
            message = f"New Job Opportunity: {doc.job_title}\n\n{doc.description}\nLocation: {doc.location}\nApply now: {doc.linkedin_post_link or frappe.utils.get_url('/apply-job?job={0}').format(doc.name)}"
            response = provider.post_share(
                message=message,
                link=doc.linkedin_post_link,
                visibility="PUBLIC",
                author_urn=doc.linkedin_author_urn
            )
            post_id = response.get("id")
            frappe.db.set_value('TalentSegmet', doc.name, {
                'linkedin_post_id': post_id,
                'linkedin_post_status': 'Posted'
            })
            frappe.msgprint(_("Job posted successfully on LinkedIn: {0}").format(post_id))
    except Exception as e:
        frappe.log_error(f"Failed to post job to LinkedIn: {str(e)}")
        frappe.throw(_("Error posting job to LinkedIn: {0}").format(str(e)))