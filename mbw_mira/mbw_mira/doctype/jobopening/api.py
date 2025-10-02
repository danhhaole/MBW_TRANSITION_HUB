import frappe
from frappe import _
import json
from frappe.utils import today

@frappe.whitelist(allow_guest=True)
def get_public_detail_by_cms():
    """Get job opening details by CMS URL segment (job_url_cms)"""
    try:
        data = frappe.local.form_dict
        job_url_cms = (data.get('job_url_cms') or '').strip()

        if not job_url_cms:
            frappe.throw(_("Missing required parameter: job_url_cms"), frappe.ValidationError)

        # Find job opening by job_url_cms
        job_id = frappe.db.get_value('ATS_JobOpening', {'job_url_cms': job_url_cms}, 'name')
        if not job_id:
            frappe.throw(_("Job opening not found"), frappe.DoesNotExistError)

        # Ensure published
        is_published = frappe.db.get_value("ATS_JobOpening", job_id, "publish_to_career_page")
        if not is_published:
            frappe.throw(_("Job opening is not published"), frappe.PermissionError)

        # Return public fields
        doc = frappe.db.get_value('ATS_JobOpening', job_id, [
            'name', 'jo_public_title', 'jo_position', 'status', 'jo_application_deadline',
            'jo_work_form', 'jo_using_unit', 'jo_location', 'jo_job_description',
            'jo_job_requirement', 'jo_job_benefits', 'jo_currency', 'jo_min_salary',
            'jo_max_salary', 'applicants_applied', 'jo_contact_email',
            'jo_contact_person', 'jo_contact_phone', 'jo_display_quantity', 'job_url_cms'
        ], as_dict=1)

        if not doc:
            frappe.throw(_("Job opening not found"), frappe.DoesNotExistError)

        return doc

    except Exception as e:
        frappe.log_error(f"Error in get_public_detail_by_cms: {str(e)}")
        frappe.throw(_("Job opening not found"), frappe.DoesNotExistError)

@frappe.whitelist(allow_guest=True)
def get_public_detail(name):
    """Get job opening details for public view (guest access allowed)"""
    if not frappe.db.exists("JobOpening", name):
        frappe.throw(_("Job opening not found"), frappe.DoesNotExistError)

    # Get public fields only
    doc = frappe.db.get_value('JobOpening', name, [
        'name', 'job_title', 'job_code', 'description', 'requirements',
        'benefits', 'department_name', 'location_name', 'number_of_openings',
        'posting_date', 'closing_date', 'approval_status', 'total_applicants',
        'image', 'slug', 'meta_title', 'meta_description', 'open_graph_title',
        'open_graph_description', 'job_url_cms'
    ], as_dict=1)

    return doc

@frappe.whitelist(allow_guest=True)
def get_public_detail_by_cms():
    """Get job opening details by CMS URL segment (job_url_cms)"""
    try:
        data = frappe.local.form_dict
        job_url_cms = (data.get('job_url_cms') or '').strip()

        if not job_url_cms:
            frappe.throw(_("Missing required parameter: job_url_cms"), frappe.ValidationError)

        # Find job opening by job_url_cms
        job_id = frappe.db.get_value('JobOpening', {'job_url_cms': job_url_cms}, 'name')
        if not job_id:
            frappe.throw(_("Job opening not found"), frappe.DoesNotExistError)

        # Return public fields
        doc = frappe.db.get_value('JobOpening', job_id, [
            'name', 'job_title', 'job_code', 'description', 'requirements',
            'benefits', 'department_name', 'location_name', 'number_of_openings',
            'posting_date', 'closing_date', 'approval_status', 'total_applicants',
            'image', 'slug', 'meta_title', 'meta_description', 'open_graph_title',
            'open_graph_description', 'job_url_cms'
        ], as_dict=1)

        if not doc:
            frappe.throw(_("Job opening not found"), frappe.DoesNotExistError)

        # Add company details if needed (modify according to your schema)
        # if doc and doc.department_name:  # Example if you want to fetch company by department
        #     company_details = frappe.db.get_value('Company', {'name': doc.company}, 
        #         ['company_name', 'website', 'industry', 'company_size', 'founded_year', 'overview'], 
        #         as_dict=1
        #     )
        #     if company_details:
        #         doc['company_details'] = company_details

        return doc

    except Exception as e:
        frappe.log_error(f"Error in get_public_detail_by_cms: {str(e)}")
        frappe.throw(_("Error retrieving job opening details"), frappe.DoesNotExistError)


@frappe.whitelist(allow_guest=True)
def get_public_detail(name):
    """Get job opening details for public view (guest access allowed)"""
    if not frappe.db.exists("JobOpening", name):
        frappe.throw(_("Job opening not found"), frappe.DoesNotExistError)

    # Get public fields only
    doc = frappe.db.get_value('JobOpening', name, [
        'name', 'job_title', 'job_code', 'description', 'requirements',
        'benefits', 'department_name', 'location_name', 'number_of_openings',
        'posting_date', 'closing_date', 'approval_status', 'total_applicants',
        'image', 'slug', 'meta_title', 'meta_description', 'open_graph_title',
        'open_graph_description', 'job_url_cms', 'owner_id'
    ], as_dict=1)

    if not doc:
        frappe.throw(_("Job opening not found"), frappe.DoesNotExistError)

    # Get owner details if needed
    if doc.owner_id:
        owner = frappe.db.get_value('User', doc.owner_id, 
                                  ['full_name', 'user_image', 'email'], 
                                  as_dict=1)
        if owner:
            doc.owner_details = owner

    return doc