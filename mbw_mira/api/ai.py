import frappe
import json
import requests


AI_BASEURL_V2 = frappe.conf.get("ai_baseurl_v2") or "https://aihub.fastwork.vn/hr_agent"

def request_data(**kwargs):
    # headers = {"Content-type": "application/json","x-api-key":"6Bwunlw3Fm1J23tGKZjb/WJXwBDI3gRY971+VUFOU+w="}
    body = kwargs.get("body")
    print('========================= body: ', body, flush=True)
    endpoint = kwargs.get("endpoint")
    url = f"{AI_BASEURL_V2}/{endpoint}"
    print('========================= url: ', url, flush=True)
    return requests.post(url, json=body)

@frappe.whitelist()
# TODO: Tạo JD(đã chạy)
def generate_job_description_v2():
    try:
        data = frappe.request.data
        if not data:
            frappe.throw(frappe._("No data received"))

        payload = json.loads(data)
        jobTitle = payload.get("jobTitle", "")
        if jobTitle == "":
            frappe.throw(frappe._("JobTitle require"))
        tone = payload.get("tone", "")
        comments = payload.get("comments", "")

        jd = generate_job_func(jobTitle=jobTitle, tone=tone, comments=comments)

        return jd
    except Exception as e:
        frappe.throw(str(e))

def generate_job_func(**kwargs):
    try:
        # url_jd = f"{AI_BASEURL_V2}/api/ai/generate-job-description"
        jobTitle = kwargs.get("jobTitle", "")
        tone = kwargs.get("tone", "")
        comments = kwargs.get("comments", "")

        if jobTitle == "":
            frappe.throw(frappe._("JobTitle require"))
        if tone == "":
            frappe.throw(frappe._("tone require"))

        if get_company_profile() and get_company_profile().company_name:
            company_profile = json.dumps(get_company_profile())
            comments += f" {company_profile}"
        comments += " .Thay ký tự \n thành <br />"
        body = {"jobTitle": jobTitle, "tone": tone, "comments": comments}
        response = request_data(endpoint="/api/v1/jd_generate", body=body)

        if response.status_code == 200:
            jd_data = response.json()
            jobDescription = jd_data.get("jobDescription", "")
            jobRequirements = jd_data.get("jobRequirements", "")
            jobResponsibilities = jd_data.get("jobResponsibilities", "")
            return {
                "jobDescription": jobDescription,
                "jobRequirements": jobRequirements,
                "jobResponsibilities": jobResponsibilities
            }
        else:
            frappe.throw(response.text)
            frappe.error_log(response.text)

    except Exception as e:
        frappe.throw(f"{str(e)}")
        frappe.error_log(f"{str(e)}")

"""Lấy thông tin Company profile"""
def get_company_profile():
    try:
        com = frappe.db.get_value("Company Profile", as_dict=1)
        return com
    except Exception as e:
        return ""