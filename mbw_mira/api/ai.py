import frappe
import json
import requests
import time
import filetype
import base64
from frappe.utils import get_files_path
from frappe import _
from frappe.utils.file_manager import save_file

AI_BASEURL = frappe.conf.get("ai_baseurl") or "https://aihub.fastwork.vn/hr_agent/"
AI_BASEURL_V2 = (
    frappe.conf.get("ai_baseurl_v2") or "https://aihub.fastwork.vn/hr_agent/"
)


# AI_BASEURL_V2 = frappe.conf.get("ai_baseurl_v2") or "https://aihub.fastwork.vn/hr_agent"

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


@frappe.whitelist()
def generate_job_description(
    job_title,
    industry,
    experience_required,
    skills_required,
    additional_info,
    rewrite_request=None,
):
    url = f"{AI_BASEURL}/v2/genai/hr-assistants/job-description/generate"

    if experience_required is None:
        frappe.throw(frappe._("Experience Required is required"))
    if skills_required is None:
        frappe.throw(frappe._("Skills Required is required"))
    if job_title is None:
        frappe.throw(frappe._("Job Title is required"))
    if industry is None:
        frappe.throw(frappe._("Industry is required"))
    if additional_info is None:
        frappe.throw(frappe._("Additional Info is required"))

    headers = {
        "Content-Type": "application/json",
        "topcv_assistant_id": "X5lMjLOTtqJ0v14yj8zix3vT",
        "other_assistant_id": "X5lMoK7W2Q87cb1sYg3liuXY",
        "Authorization": "Bearer tkoBjKTFTNfFDzkmGe0z9ppUusIeexVy",
        "x-api-key": "6Bwunlw3Fm1J23tGKZjb/WJXwBDI3gRY971+VUFOU+w=",
    }

    payload = {
        "jd_assistant_id": "X5lMyuVIiuh122toZXrVtCGk",
        "job_title": job_title,
        "industry": industry,
        "experience_required": experience_required,
        "skills_required": skills_required,
        "additional_info": additional_info,
        "rewrite_request": rewrite_request,
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            frappe.log_error(
                f"API Error {response.status_code}: {response.text}",
                "Job Description API",
            )
            return {"error": response.text}
    except Exception as e:
        frappe.log_error(f"Exception: {str(e)}", "Job Description API")
        return {"error": str(e)}


def extract_cv_backend(file_name):
    # url_extract_ai = f"{AI_BASEURL}/v2/genai/hr-assistants/cv-extraction/pdf-upload"
    url_extract_ai = f"{AI_BASEURL_V2}/api/v1/cv_extract"

    if not file_name:
        frappe.throw("Missing 'file_name' in request parameters.")

    headers = {"x-api-key": "6Bwunlw3Fm1J23tGKZjb/WJXwBDI3gRY971+VUFOU+w="}

    try:
        file_name = frappe.db.get_value("File", {"name": file_name}, "file_name")

        file_path = get_files_path(file_name)

        with open(file_path, "rb") as f:
            files = {"file": (file_name, f, "application/pdf")}
            response = requests.post(url_extract_ai, files=files, headers=headers)
        if response.status_code == 200:
            data = frappe.parse_json(response.json())
            if data and data.data:
                if data and data.data and "personal_info" in data.data:
                    personal_info = {
                        "name": "can_full_name",
                        "email": "can_email",
                        "phone": "can_phone",
                    }
                    data.data["personal_info"] = rename_keys(
                        data.data["personal_info"], personal_info
                    )

                if "work_experience" in data.data:
                    work_experience = {
                        "company": "work_experience_place",
                        "position": "work_experience_role",
                        "start_date": "work_experience_start",
                        "end_date": "work_experience_end",
                        "descriptions": "work_experience_detail",
                    }
                    data.data["work_experience"] = rename_keys_in_list(
                        data.data["work_experience"], work_experience
                    )

                if "projects" in data.data:
                    projects = {
                        "name": "projects_name",
                        "tasks": "project_description",
                        "start_date": "project_start_date",
                        "end_date": "project_end_date",
                        "position": "project_role",
                    }
                    data.data["projects"] = rename_keys_in_list(
                        data.data["projects"], projects
                    )

                if "skills" in data.data:
                    skill = {
                        "name": "can_skill_name",
                    }
                    data.data["skills"] = rename_keys_in_list(
                        data.data["skills"], skill
                    )

                # Xử lý ảnh avatar nếu có
                if "avatar" in data and data["avatar"]:
                    try:
                        data.data["can_avatar"] = upload_base64_without_filename(
                            data["avatar"],
                            "Candidate",
                            data.data["personal_info"].get("can_full_name", "unknown"),
                        )
                    except Exception as avatar_error:
                        frappe.log_error(str(avatar_error), "CV Avatar Upload Error")
                        data.data["can_avatar"] = None
                    finally:
                        del data["avatar"]
                else:
                    data.data["can_avatar"] = None

            return data
        else:
            frappe.log_error("Error extract")
            return ""

    except frappe.DoesNotExistError:
        frappe.log_error("File does not exists")
        return ""

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "CV Upload API")
        return ""


def get_file_stream_from_url(url):
    response = requests.get(url, stream=True)
    response.raise_for_status()  # ném lỗi nếu HTTP trả về lỗi
    return response.raw  # Trả về stream


@frappe.whitelist(allow_guest=True)
def extract_cv_url():
    # url_extract_ai = f"{AI_BASEURL}/v2/genai/hr-assistants/cv-extraction/pdf-upload"
    url_extract_ai = f"{AI_BASEURL_V2}/api/v1/cv_extract"
    file_name = frappe.form_dict.get("file_name")
    if not file_name:
        frappe.throw("Missing 'file_name' in request parameters.")

    headers = {"x-api-key": "6Bwunlw3Fm1J23tGKZjb/WJXwBDI3gRY971+VUFOU+w="}

    try:
        # Lấy cả file_name và file_url từ database
        file_info = frappe.db.get_value(
            "File", {"name": file_name}, ["file_name", "file_url"], as_dict=True
        )

        if not file_info:
            return {
                "status": "error",
                "error_message": f"File record not found: {file_name}",
            }

        # Sử dụng file_url để tạo đường dẫn file thực tế
        file_url = file_info.file_url
        if not file_url:
            return {
                "status": "error",
                "error_message": "File URL not found in database",
            }

        # Chuyển từ file_url thành file path
        # file_url: "/files/CVTran-Dong-Phuongpdf (1)_174885418994688b.pdf"
        # file_path: "./sites/ats.local/public/files/CVTran-Dong-Phuongpdf (1)_174885418994688b.pdf"

        import os

        if file_url.startswith("/files/"):
            # Lấy tên file thực tế từ URL
            actual_filename = file_url.replace("/files/", "")
            # Tạo đường dẫn đầy đủ
            file_path = get_files_path(actual_filename)
        else:
            # Fallback: thử dùng file_name gốc
            file_path = get_files_path(file_info.file_name)

        # Kiểm tra file có tồn tại không
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "error_message": f"File does not exist at path: {file_path}",
                "debug_info": {
                    "file_url": file_url,
                    "file_name": file_info.file_name,
                    "calculated_path": file_path,
                },
            }

        # Debug log
        frappe.log_error(f"Processing file: {file_path}", "CV Extract Debug")

        # Xác định MIME type dựa trên extension
        file_extension = actual_filename.lower().split(".")[-1]
        mime_type = {
            "pdf": "application/pdf",
            "doc": "application/msword",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }.get(file_extension, "application/octet-stream")

        with open(file_path, "rb") as f:
            files = {"file": (actual_filename, f, mime_type)}
            response = requests.post(url_extract_ai, files=files, headers=headers)

        if response.status_code == 200:
            data = frappe.parse_json(response.json())
            if data and data.get("data"):
                if "personal_info" in data.data:
                    personal_info = {
                        "name": "can_full_name",
                        "email": "can_email",
                        "phone": "can_phone",
                    }
                    data.data["personal_info"] = rename_keys(
                        data.data["personal_info"], personal_info
                    )

                if "work_experience" in data.data:
                    work_experience = {
                        "company": "work_experience_place",
                        "position": "work_experience_role",
                        "start_date": "work_experience_start",
                        "end_date": "work_experience_end",
                        "descriptions": "work_experience_detail",
                    }
                    data.data["work_experience"] = rename_keys_in_list(
                        data.data["work_experience"], work_experience
                    )

                if "projects" in data.data:
                    projects = {
                        "name": "projects_name",
                        "tasks": "project_description",
                        "start_date": "project_start_date",
                        "end_date": "project_end_date",
                        "position": "project_role",
                    }
                    data.data["projects"] = rename_keys_in_list(
                        data.data["projects"], projects
                    )

                if "skills" in data.data:
                    skill = {
                        "name": "can_skill_name",
                    }
                    data.data["skills"] = rename_keys_in_list(
                        data.data["skills"], skill
                    )

                if "certificate" in data.data:
                    certificate = {
                        "organization": "",
                        "name": "",
                        "start_date": "",
                        "end_date": "",
                        "descriptions": "",
                    }

                # Xử lý ảnh avatar nếu có
                if "avatar" in data and data["avatar"]:
                    try:
                        data.data["can_avatar"] = upload_base64_without_filename(
                            data["avatar"],
                            "Candidate",
                            data.data["personal_info"].get("can_full_name", "unknown"),
                        )
                    except Exception as avatar_error:
                        frappe.log_error(str(avatar_error), "CV Avatar Upload Error")
                        data.data["can_avatar"] = None
                    finally:
                        del data["avatar"]
                else:
                    data.data["can_avatar"] = None

            return data
        else:
            frappe.log_error(
                f"CV Upload API Error {response.status_code}: {response.text}",
                "CV Upload API",
            )
            return {
                "error": "CV extraction failed",
                "status_code": response.status_code,
                "response": response.text,
            }

    except frappe.DoesNotExistError:
        return {"error": "File not found", "file_name": file_name}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "CV Upload API")
        return {
            "error": "Unhandled error occurred while processing the CV.",
            "details": str(e),
        }


def rename_keys(data, rename_map):
    return {rename_map.get(k, k): v for k, v in data.items()}


def rename_keys_in_list(data_list, rename_map):
    return [{rename_map.get(k, k): v for k, v in item.items()} for item in data_list]


def upload_base64_without_filename(
    base64_data,
    attached_to_doctype=None,
    attached_to_name=None,
    attached_to_field=None,
    is_private=0,
):
    try:
        # Validate attached_to_name parameter
        if attached_to_name is not None:
            if not isinstance(attached_to_name, (str, int)):
                attached_to_name = str(attached_to_name) if attached_to_name else None
            elif isinstance(attached_to_name, str) and not attached_to_name.strip():
                attached_to_name = None

        # Giải mã base64 thành bytes
        file_content = base64.b64decode(base64_data)

        # Đoán file type từ nội dung
        kind = filetype.guess(file_content)
        if kind:
            extension = kind.extension  # vd: 'pdf', 'docx'
            mime_type = kind.mime  # vd: 'application/pdf'
        else:
            extension = "bin"
            mime_type = "application/octet-stream"

        # Tạo file name tạm thời
        file_name = f"cv_extracted_{int(time.time())}.{extension}"

        # Format file_type as uppercase short form
        file_type = extension.upper()

        # Lưu file vào hệ thống vật lý + metadata
        saved_file = save_file(
            fname=file_name,
            content=file_content,
            dt=attached_to_doctype,
            dn=attached_to_name,
            is_private=is_private,
        )

        # Lưu MIME type vào record
        saved_file.file_type = file_type
        saved_file.save(ignore_permissions=True)
        frappe.db.commit()
        # saved_file.submit()

        return saved_file.file_url

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Upload Extracted CV Error")
        frappe.throw(_("Lỗi khi upload file từ extract CV: {0}").format(str(e)))


def extract_and_update_candidate(file_name, candidate_name):
    data = extract_cv_backend(file_name)
    if not data:
        frappe.log_error("No data returned from CV extraction", "CV Extraction Error")
        return

    try:
        candidate = frappe.get_doc("Candidate", candidate_name)
        extracted = data.get("data", {})

        def update_field(fieldname, value):
            if not candidate.get(fieldname) and value:
                candidate.set(fieldname, value)

        personal_info = extracted.get("personal_info", {})

        # Cập nhật các trường chính
        update_field("can_full_name", personal_info.get("can_full_name"))
        update_field("can_email", personal_info.get("can_email"))
        update_field("can_phone", personal_info.get("can_phone"))
        update_field("can_dob", personal_info.get("can_dob"))
        update_field("can_gender", personal_info.get("can_gender"))
        update_field("can_region", personal_info.get("can_region"))
        update_field("can_address", personal_info.get("can_address"))
        update_field("can_avatar", extracted.get("can_avatar"))

        # Xử lý học vấn: chỉ lấy phần tử đầu tiên nếu là list
        education = extracted.get("education", {})
        if isinstance(education, list) and education:
            education = education[0]
        elif not isinstance(education, dict):
            education = {}

        update_field("educationlevel_id", education.get("level"))
        update_field("institution_id", education.get("institution"))
        update_field("major_id", education.get("major"))

        # Hàm thêm bảng con nếu chưa có
        def set_child_table(table_field, items, mapping):
            if not candidate.get(table_field) and items:
                for row in items:
                    child = candidate.append(table_field, {})
                    for src, dest in mapping.items():
                        if row.get(src):
                            child.set(dest, row.get(src))

        # Work Experience
        set_child_table(
            "candidate_work_experience",
            extracted.get("work_experience", []),
            {
                "work_experience_place": "work_experience_place",
                "work_experience_role": "work_experience_role",
                "work_experience_start": "work_experience_start",
                "work_experience_end": "work_experience_end",
                "work_experience_detail": "work_experience_detail",
            },
        )

        # Projects
        set_child_table(
            "candidate_project",
            extracted.get("projects", []),
            {
                "projects_name": "project_name",
                "project_description": "project_description",
                "project_start_date": "project_start_date",
                "project_end_date": "project_end_date",
                "project_role": "project_role",
            },
        )

        # Skills
        set_child_table(
            "candidate_skill",
            extracted.get("skills", []),
            {"can_skill_name": "can_skill_name"},
        )

        # Certifications
        set_child_table(
            "candidate_certification",
            extracted.get("certifications", []),
            {
                "certification_name": "certification_name",
                "certification_organization": "organization",
                "certification_year": "year",
            },
        )

        # # Awards
        # set_child_table("candidate_award", extracted.get("awards", []), {
        #     "award_name": "award_name",
        #     "award_year": "year",
        #     "award_description": "description"
        # })

        # # Courses
        # set_child_table("candidate_course", extracted.get("courses", []), {
        #     "course_name": "course_name",
        #     "course_organization": "organization",
        #     "course_year": "year"
        # })

        candidate.save(ignore_permissions=True)
        frappe.db.commit()

    except Exception:
        frappe.log_error(frappe.get_traceback(), "Update Candidate Failed")


# def request_data(**kwargs):
#     headers = {
#         "Content-type": "application/json",
#         "x-api-key": "6Bwunlw3Fm1J23tGKZjb/WJXwBDI3gRY971+VUFOU+w=",
#     }
#     body = kwargs.get("body")
#     endpoint = kwargs.get("endpoint")
#     url = f"{AI_BASEURL_V2}/{endpoint}"
#     return requests.post(url, json=body, headers=headers)


"""JD Mới

    - jobTitle: String - Vị trí công việc
    - tone: String - Phong cách viết
    - comments: string - Mô tả
"""


# @frappe.whitelist()
# # TODO: Tạo JD(đã chạy)
# def generate_job_description_v2():
#     try:
#         data = frappe.request.data
#         if not data:
#             frappe.throw(frappe._("No data received"))

#         payload = json.loads(data)
#         jobTitle = payload.get("jobTitle", "")
#         if jobTitle == "":
#             frappe.throw(frappe._("JobTitle require"))
#         tone = payload.get("tone", "")
#         comments = payload.get("comments", "")

#         jd = generate_job_func(jobTitle=jobTitle, tone=tone, comments=comments)

#         return jd
#     except Exception as e:
#         frappe.throw(str(e))


# def generate_job_func(**kwargs):
#     try:
#         # url_jd = f"{AI_BASEURL_V2}/api/ai/generate-job-description"
#         jobTitle = kwargs.get("jobTitle", "")
#         tone = kwargs.get("tone", "")
#         comments = kwargs.get("comments", "")

#         if jobTitle == "":
#             frappe.throw(frappe._("JobTitle require"))
#         if tone == "":
#             frappe.throw(frappe._("tone require"))

#         if get_company_profile() and get_company_profile().company_name:
#             company_profile = json.dumps(get_company_profile())
#             comments += f" {company_profile}"
#         comments += " .Thay ký tự \n thành <br />"
#         body = {"jobTitle": jobTitle, "tone": tone, "comments": comments}
#         response = request_data(endpoint="/api/v1/jd_generate", body=body)

#         if response.status_code == 200:
#             jd_data = response.json()
#             jobDescription = jd_data.get("jobDescription", "")
#             jobRequirements = jd_data.get("jobRequirements", "")
#             jobResponsibilities = jd_data.get("jobResponsibilities", "")
#             return {
#                 "jobDescription": jobDescription,
#                 "jobRequirements": jobRequirements,
#                 "jobResponsibilities": jobResponsibilities,
#             }
#         else:
#             frappe.throw(response.text)
#             frappe.error_log(response.text)

#     except Exception as e:
#         frappe.throw(f"{str(e)}")
#         frappe.error_log(f"{str(e)}")


"""Refine jd
"""


@frappe.whitelist()
def jd_section_refine():
    try:
        data = frappe.request.data
        if not data:
            frappe.throw(frappe._("No data received"))

        payload = json.loads(data)
        originalJD = payload.get("originalJD", "")
        fieldsToRewrite = payload.get("fieldsToRewrite")
        if originalJD == "":
            frappe.throw(frappe._("originalJD require"))
        if not fieldsToRewrite:
            frappe.throw(frappe._("fieldsToRewrite require"))
        comments = payload.get("comments", "")

        jd = jd_section_refine_func(
            originalJD=originalJD, fieldsToRewrite=fieldsToRewrite, comments=comments
        )

        return jd
    except Exception as e:
        frappe.throw(str(e))


def jd_section_refine_func(**kwargs):
    try:
        # url_jd = f"{AI_BASEURL_V2}/api/ai/generate-job-description"
        originalJD = kwargs.get("originalJD", "")
        fieldsToRewrite = kwargs.get("fieldsToRewrite", "")
        comments = kwargs.get("comments", "")

        if originalJD == "":
            frappe.throw(frappe._("originalJD require"))
        if fieldsToRewrite == "":
            frappe.throw(frappe._("fieldsToRewrite require"))

        if get_company_profile() and get_company_profile().company_name:
            company_profile = json.dumps(get_company_profile())
            comments += f" {company_profile}"
        comments += " .Thay ký tự \n thành <br />"
        body = {
            "originalJD": originalJD,
            "fieldsToRewrite": fieldsToRewrite,
            "comments": comments,
        }
        response = request_data(endpoint="/api/v1/jd_section_refine", body=body)

        if response.status_code == 200:
            jd_data = response.json()
            jobDescription = jd_data.get("jobDescription", "")
            jobRequirements = jd_data.get("jobRequirements", "")
            jobResponsibilities = jd_data.get("jobResponsibilities", "")
            return {
                "jobDescription": jobDescription,
                "jobRequirements": jobRequirements,
                "jobResponsibilities": jobResponsibilities,
            }
        else:
            frappe.throw(response.json())
            frappe.error_log(response.json())

    except Exception as e:
        frappe.throw(f"{str(e)}")
        frappe.error_log(f"{str(e)}")


"""
    Câu hỏi phỏng vấn
    "interviewQuestionsCount": int, // số lượng câu hỏi phỏng vấn
    "jobOpening": "str", // vị trí tuyển dụng
    "tone": "str", // phong cách viết
    "comments": "str", // mô tả bổ sung
    "type": "str", // loại nội dung
    "level": "str", // cấp độ 
    "format": "str", // định dạng 
    "category": "str", // danh mục 
    "isGenerateAnswers": boolean //có tạo sẵn câu trả lời hay không

"""


@frappe.whitelist()
def generate_interview_questions():
    try:
        data = frappe.request.data
        if not data:
            frappe.throw(frappe._("No data received"))

        payload = json.loads(data)
        interviewQuestionsCount = payload.get("interviewQuestionsCount", 0)
        jobOpening = payload.get("jobOpening", "")
        tone = payload.get("tone", "")
        comments = payload.get("comments", "")
        type = payload.get("type", "")
        format = payload.get("format", "")
        level = payload.get("level", "")
        category = payload.get("category", "")
        isGenerateAnswers = payload.get("isGenerateAnswers", False)
        if interviewQuestionsCount == 0:
            frappe.throw("interviewQuestionsCount require")
        if not jobOpening:
            frappe.throw("jobOpening require")
        quizz = generate_interview_func(
            interviewQuestionsCount=interviewQuestionsCount,
            jobOpening=jobOpening,
            tone=tone,
            comments=comments,
            type=type,
            format=format,
            level=level,
            category=category,
            isGenerateAnswers=isGenerateAnswers,
        )

        return quizz
    except Exception as e:
        frappe.throw(str(e))


def generate_interview_func(**kwargs):
    try:
        interviewQuestionsCount = kwargs.get("interviewQuestionsCount", 0)
        jobOpening = kwargs.get("jobOpening", "")
        tone = kwargs.get("tone", "")
        comments = kwargs.get("comments", "")
        type = kwargs.get("type", "")
        level = kwargs.get("level", "")
        format = kwargs.get("format", "")
        category = kwargs.get("category", "")
        isGenerateAnswers = kwargs.get("isGenerateAnswers", False)
        isKnockoutQuestions = kwargs.get("isKnockoutQuestions", False)

        comments += " .Thay ký tự \n thành <br />"
        if interviewQuestionsCount == 0:
            frappe.throw("interviewQuestionsCount require")
        if not jobOpening:
            frappe.throw("jobOpening require")

        body = {
            "interviewQuestionsCount": interviewQuestionsCount,
            "jobOpening": jobOpening,
            "tone": tone,
            "comments": comments,
            "type": type,
            "level": level,
            "format": format,
            "category": category,
            "isGenerateAnswers": isGenerateAnswers,
        }

        response = request_data(endpoint="/api/v1/interview_questions", body=body)
        if response.status_code == 200:
            quiz = response.json()
            quiz_list = []
            interviewQuestions = quiz.get("interviewQuestions")
            for item in interviewQuestions:
                doc_data = convert_api_question_to_frappe_doc(
                    item, isKnockoutQuestions, jobOpening
                )
                doc = frappe.new_doc("LMS Question")
                for key, val in doc_data.items():
                    if hasattr(doc, key):
                        setattr(doc, key, val)
                doc.insert(ignore_permissions=True)
                frappe.db.commit()
                quiz_list.append(doc.as_dict())
            return quiz_list
        else:
            frappe.throw("Lỗi tạo question")
            frappe.log_error(response.text)
    except Exception as e:
        frappe.throw(str(e))
        frappe.log_error(str(e))


"""Tạo gọi ý tiêu chí đánh giá
"""


@frappe.whitelist()
# TODO: Tạo gọi ý tiêu chí đánh giá(đã chạy)
def evaluation_criteria_generate():
    try:
        data = frappe.request.data
        if not data:
            frappe.throw(frappe._("No data received"))

        payload = json.loads(data)
        job_id = payload.get("job_id")
        evaluation = evaluation_criteria_generate_func(job_id=job_id)
        return evaluation
    except Exception as e:
        frappe.throw(str(e))


def evaluation_criteria_generate_func(**kwargs):
    try:
        job_id = kwargs.get("job_id")
        if not job_id:
            frappe.throw("job_id require")

        skill_doc = frappe.db.get_all("ATS_Skill")
        skills = [skill["name"] for skill in skill_doc]
        jo_job = frappe.db.get_value(
            "JobOpening",
            job_id,
            ["jo_job_description", "jo_job_requirement", "jo_job_benefits"],
            as_dict=1,
        )
        job_description = f"{jo_job.jo_job_description}.{jo_job.jo_job_benefits}"
        job_description += " .Thay ký tự \n thành <br />"
        body = {"job_description": job_description}
        response = request_data(
            endpoint="/api/v1/evaluation_criteria_generate", body=body
        )
        if response.status_code == 200:
            evaluation = response.json()
            return {"rules": evaluation.get("rules")}
        else:
            # Fix: Convert dict to string before throwing
            error_response = (
                response.json()
                if response.headers.get("content-type", "").startswith(
                    "application/json"
                )
                else response.text
            )
            frappe.throw(f"API Error {response.status_code}: {str(error_response)}")
    except Exception as e:
        frappe.throw(str(e))


def convert_api_question_to_frappe_doc(
    q: dict, is_knockout: bool = False, position: str = ""
) -> dict:
    q_type = q.get("type", "").strip().lower()
    doc = {
        "doctype": "LMS Question",
        "question": q.get("question"),
        "position": position,
        "type": "",  # Choices / User Input / Open Ended
        "multiple": 0,
        "is_knockout": 1 if is_knockout else 0,  # Set knockout flag
        "option_1": "",
        "option_2": "",
        "option_3": "",
        "option_4": "",
        "is_correct_1": 0,
        "is_correct_2": 0,
        "is_correct_3": 0,
        "is_correct_4": 0,
        "explanation_1": "",
        "explanation_2": "",
        "explanation_3": "",
        "explanation_4": "",
        "possibility_1": "",
        "possibility_2": "",
        "possibility_3": "",
        "possibility_4": "",
    }

    # --- TRẮC NGHIỆM ---
    if q_type in ["trắc nghiệm", "đúng sai", "choices"]:
        doc["type"] = "Choices"
        options = q.get("options", [])
        correct_answer = q.get("correctAnswer", "").strip().upper()

        for i in range(min(4, len(options))):
            label, text = (
                options[i].split(". ", 1) if ". " in options[i] else ("", options[i])
            )
            doc[f"option_{i+1}"] = text.strip()
            doc[f"is_correct_{i+1}"] = int(label.strip().upper() == correct_answer)
            doc[f"explanation_{i+1}"] = ""  # Có thể gán logic sinh giải thích ở đây

    # --- TỰ LUẬN ---
    elif q_type in ["tự luận", "user input"]:
        doc["type"] = "User Input"
        correct_text = q.get("correctAnswer", "").strip()

        if correct_text:
            # Tách thành các câu ngắn, hoặc đưa toàn bộ vào possibility_1 nếu không phân tách được
            if "\n" in correct_text:
                parts = [p.strip() for p in correct_text.split("\n") if p.strip()]
            else:
                parts = [correct_text]  # fallback toàn bộ

            for i in range(min(4, len(parts))):
                doc[f"possibility_{i+1}"] = parts[i]

        # Tránh lỗi nếu API không trả correctAnswer
        if not any(doc[f"possibility_{i}"] for i in range(1, 5)):
            doc["possibility_1"] = "Đáp án đang cập nhật."

    # --- CÂU HỎI MỞ ---
    elif q_type in ["câu hỏi mở", "open ended"]:
        doc["type"] = "Open Ended"

    return doc


"""Gen email
    "emailType": "str", // loại email (ví dụ: thư mời phỏng vấn)
    "tone": "str", // phong cách viết (ví dụ: Professional)
    "comments": "str", // ghi chú bổ sung (ví dụ: ngày giờ, ước lượng thời gian, hướng dẫn di chuyển)
    "variable": [
        { "Candidate:FirstName": "str" }, // tên ứng viên
        { "Job:Title": "str" } // vị trí công việc
    ]

"""


@frappe.whitelist()
# TODO: Tạo email template(đã chạy)
def generate_email_template():
    try:
        data = frappe.request.data
        if not data:
            frappe.throw(frappe._("No data received"))

        payload = json.loads(data)
        emailType = payload.get("emailType", "")
        tone = payload.get("tone", "")
        comments = payload.get("comments", "")
        variable = payload.get("variable", "")

        email_temp = generate_email_func(
            emailType=emailType, tone=tone, comments=comments, variable=variable
        )
        return email_temp
    except Exception as e:
        frappe.throw(str(e))


def generate_email_func(**kwargs):
    try:
        emailType = kwargs.get("emailType", "")
        tone = kwargs.get("tone", "")
        comments = kwargs.get("comments", "")
        variable = kwargs.get("variable", "")
        if get_company_profile() and get_company_profile().company_name:
            company_profile = json.dumps(get_company_profile())
            comments += f" {company_profile}"
        comments += " .Thay ký tự \n thành <br />"
        body = {
            "emailType": emailType,
            "tone": tone,
            "comments": comments,
            "variable": variable,
        }

        response = request_data(endpoint="/api/v1/email_generate", body=body)
        if response.status_code == 200:
            email_temp = response.json()
            return {
                "emailTemplate": email_temp.get("emailTemplate", ""),
                "emailSubject": email_temp.get("emailSubject", ""),
            }
        else:
            frappe.throw(f"Lỗi tạo email template {response.json()}")
            frappe.log_error(response.text)
    except Exception as e:
        frappe.throw(str(e))
        frappe.log_error(str(e))


"""Extract CV mới
"""



def extract_cv_backend_v2(file_name):
    url_extract_ai = f"{AI_BASEURL_V2}/api/v1/cv_extract"
    if not file_name:
        frappe.throw("Missing 'file_name' in request parameters.")

    headers = {}

    try:
        file_doc = frappe.db.get_value(
            "File", {"file_name": file_name}, ["file_name"], as_dict=1
        )

        file_path = get_files_path(file_doc.get("file_name"))

        with open(file_path, "rb") as f:
            files = {"file": (file_name, f, "application/pdf")}
            response = requests.post(url_extract_ai, files=files, headers=headers)
        if response.status_code == 200:
            data = frappe.parse_json(response.json())
            if data and data.data:
                if "personal_info" in data.data:
                    personal_info = {
                        "name": "can_full_name",
                        "email": "can_email",
                        "phone": "can_phone",
                    }
                    data.data["personal_info"] = rename_keys(
                        data.data["personal_info"], personal_info
                    )

                if "work_experience" in data.data:
                    work_experience = {
                        "company": "work_experience_place",
                        "position": "work_experience_role",
                        "start_date": "work_experience_start",
                        "end_date": "work_experience_end",
                        "descriptions": "work_experience_detail",
                    }
                    data.data["work_experience"] = rename_keys_in_list(
                        data.data["work_experience"], work_experience
                    )

                if "projects" in data.data:
                    projects = {
                        "name": "projects_name",
                        "tasks": "project_description",
                        "start_date": "project_start_date",
                        "end_date": "project_end_date",
                        "position": "project_role",
                    }
                    data.data["projects"] = rename_keys_in_list(
                        data.data["projects"], projects
                    )

                if "skills" in data.data:
                    skill = {
                        "name": "can_skill_name",
                    }
                    data.data["skills"] = rename_keys_in_list(
                        data.data["skills"], skill
                    )

                # Xử lý ảnh avatar nếu có
                if "avatar" in data and data["avatar"]:
                    try:
                        data.data["can_avatar"] = upload_base64_without_filename(
                            data["avatar"],
                            "Candidate",
                            data.data["personal_info"].get("can_full_name", "unknown"),
                        )
                    except Exception as avatar_error:
                        frappe.log_error(str(avatar_error), "CV Avatar Upload Error")
                        data.data["can_avatar"] = None
                    finally:
                        del data["avatar"]
                else:
                    data.data["can_avatar"] = None

            return data
        else:
            frappe.log_error("Error extract")
            return ""

    except frappe.DoesNotExistError:
        frappe.log_error("File does not exists")
        return ""

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "CV Upload API")
        return ""


@frappe.whitelist()
def add_ai_questions_to_quiz(quiz_id, question_names, is_knockout=False):
    """
    Add AI generated questions to a quiz
    """
    try:
        quiz = frappe.get_doc("LMS Quiz", quiz_id)

        added_count = 0
        knockout_count = 0

        for question_name in question_names:
            # Check if question already exists in quiz
            existing = frappe.db.exists(
                "LMS Quiz Question", {"parent": quiz_id, "question": question_name}
            )

            if not existing:
                quiz.append(
                    "questions",
                    {"question": question_name, "marks": 1, "is_knockout": is_knockout},
                )
                added_count += 1

                if is_knockout:
                    knockout_count += 1

        quiz.save()

        return {
            "success": True,
            "message": f"Added {added_count} questions to quiz",
            "added_questions": added_count,
            "knockout_questions": knockout_count,
        }

    except Exception as e:
        frappe.log_error(f"Error adding AI questions to quiz: {str(e)}")
        return {"success": False, "message": f"Error adding questions: {str(e)}"}


@frappe.whitelist()
def process_cv(file_url, job_opening_id=None):
    """
    Process CV file and extract information using AI
    """
    try:
        frappe.log_error(
            f"process_cv called with file_url: {file_url}, job_opening_id: {job_opening_id}",
            "CV Processing Debug",
        )

        # Extract file name from URL
        if not file_url:
            return {"success": False, "message": "No file URL provided"}

        # Get file name from URL - handle both full URLs and relative paths
        if file_url.startswith("/files/"):
            file_name = file_url.split("/")[-1]
        else:
            file_name = file_url.split("/")[-1]

        # Find the file document
        file_doc = frappe.db.get_value(
            "File",
            filters={"file_url": file_url},
            fieldname=["name", "file_name"],
            as_dict=True,
        )

        if not file_doc:
            # Try to find by file name
            file_doc = frappe.db.get_value(
                "File",
                filters={"file_name": file_name},
                fieldname=["name", "file_name"],
                as_dict=True,
            )

        if not file_doc:
            return {"success": False, "message": f"File not found: {file_name}"}

        # Use existing CV extraction function
        extracted_data_response = extract_cv_backend(file_doc.file_name)

        if not extracted_data_response or not extracted_data_response.get("data"):
            return {"success": False, "message": "Failed to extract data from CV"}

        # Process the extracted data
        extracted_data = extracted_data_response.get("data", {})

        # Flatten the structure for form compatibility
        form_data = {}

        # Personal info
        if "personal_info" in extracted_data:
            personal_info = extracted_data["personal_info"]
            form_data.update(
                {
                    "can_full_name": personal_info.get("can_full_name", ""),
                    "can_email": personal_info.get("can_email", ""),
                    "can_phone": personal_info.get("can_phone", ""),
                    "can_dob": personal_info.get("can_dob", ""),
                    "can_gender": personal_info.get("can_gender", ""),
                    "can_address": personal_info.get("can_address", ""),
                }
            )

        # Education - take first entry if it's a list
        if "education" in extracted_data:
            education = extracted_data["education"]
            if isinstance(education, list) and education:
                education = education[0]
            if isinstance(education, dict):
                form_data.update(
                    {
                        "educationlevel_id": education.get("level", ""),
                        "institution_id": education.get("institution", ""),
                        "major_id": education.get("major", ""),
                    }
                )

        # Work experience
        if "work_experience" in extracted_data:
            form_data["candidate_work_experience"] = extracted_data["work_experience"]

        # Projects
        if "projects" in extracted_data:
            form_data["candidate_project"] = extracted_data["projects"]

        # Skills
        if "skills" in extracted_data:
            form_data["candidate_skill"] = extracted_data["skills"]

        # Avatar
        if "can_avatar" in extracted_data:
            form_data["can_avatar"] = extracted_data["can_avatar"]

        # Determine extracted fields for display
        extracted_fields = []
        if form_data.get("can_full_name"):
            extracted_fields.append("Name")
        if form_data.get("can_email"):
            extracted_fields.append("Email")
        if form_data.get("can_phone"):
            extracted_fields.append("Phone")
        if form_data.get("candidate_work_experience"):
            extracted_fields.append("Work Experience")
        if form_data.get("candidate_skill"):
            extracted_fields.append("Skills")
        if form_data.get("educationlevel_id") or form_data.get("institution_id"):
            extracted_fields.append("Education")

        return {
            "success": True,
            "extracted_data": form_data,
            "extracted_fields": extracted_fields,
            "message": "CV processed successfully",
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Add AI Questions to Quiz Error")
        frappe.throw(f"Error adding questions to quiz: {str(e)}")


@frappe.whitelist()
def generate_content():
    try:
        data = frappe.request.data
        if not data:
            frappe.throw(frappe._("No data received"))

        payload = json.loads(data)
        pageTitle = payload.get("pageTitle", "")
        tone = payload.get("tone", "")
        comments = payload.get("comments", "")

        content = generate_content_func(
            pageTitle=pageTitle, tone=tone, comments=comments
        )
        return content
    except Exception as e:
        frappe.throw(str(e))
        frappe.log_error(str(e))


def generate_content_func(**kwargs):

    try:
        pageTitle = kwargs.get("pageTitle", "")
        tone = kwargs.get("tone", "")
        comments = kwargs.get("comments", "")

        body = {"pageTitle": pageTitle, "tone": tone, "comments": comments}

        response = request_data(endpoint="/api/v1/content_generate", body=body)
        if response.status_code == 200:
            content = response.json()
            return {"sitePageContent": content.get("emailTemplate", "")}
        else:
            frappe.throw(f"Lỗi tạo content {response.json()}")
            frappe.log_error(response.text)
    except Exception as e:
        frappe.throw(str(e))
        frappe.log_error(str(e))


@frappe.whitelist()
def generate_company_profile():
    try:
        data = frappe.request.data
        if not data:
            frappe.throw(frappe._("No data received"))

        payload = json.loads(data)
        urls = payload.get("urls")
        if not urls:
            frappe.throw("urls require")
        company = generate_company_profile_func(urls=urls)
        return company
    except Exception as e:
        frappe.throw(str(e))
        frappe.log_error(str(e))


def generate_company_profile_func(**kwargs):
    try:
        urls = kwargs.get("urls", "")
        if not urls:
            frappe.throw("urls require")
        body = {"urls": urls}

        response = request_data(endpoint="/api/v1/company_profile_generate", body=body)
        if response.status_code == 200:
            content = response.json()
            return {"company_profile": content.get("data", "")}
        else:
            frappe.throw(f"Lỗi tạo profile {response.json()}")
            frappe.log_error(response.text)
    except Exception as e:
        frappe.throw(str(e))
        frappe.log_error(str(e))


"""Lấy thông tin Company profile
"""


# def get_company_profile():
#     try:
#         com = frappe.db.get_value("Company Profile", as_dict=1)
#         return com
#     except Exception as e:
#         return ""
