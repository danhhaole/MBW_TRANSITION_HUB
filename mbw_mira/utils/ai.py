import base64
import os
import requests
import json
import frappe
from frappe import _
import time
import filetype
from frappe.utils.file_manager import save_file
import urllib.parse

# ==============================
# CONFIG
# ==============================
EMBEDDING_API_URL = "https://aiapi.fastwork.vn/embedding_qwen/v1/embeddings"
VLM_API_URL = "https://aiapi.fastwork.vn/vlm/v1/chat/completions"
LLM_API_URL = "https://aiapi.fastwork.vn/vlm/v1/chat/completions"

API_KEY = "b8040c68-b18b-4e01-9d61-b03536c02fcb"
API_MODEL = f"5CD-AI/Vintern-3B-R-beta"
MODEL_NAME = f"Qwen/Qwen3-Embedding-0.6B"
MODEL_RAW_NAME = f"Qwen/Qwen3-8B"
DEFAULT_API_TOKEN = "1d161ba4-ddab-491d-a2b6-ad0eac14fb33"

AI_BASEURL_V2 = (
    frappe.conf.get("ai_baseurl_v2") or "https://aihub.fastwork.vn/hr_agent/"
)


# ==============================
# JSON PARSER
# ==============================
def extractJSON(text):
    """Cố gắng parse JSON từ các dạng trả về của LLM"""
    try:
        return json.loads(text)
    except:
        pass

    try:
        match = frappe.safe_decode(text).strip().split("```json")
        if len(match) > 1:
            block = match[1].split("```")[0]
            return json.loads(block)
    except:
        pass

    try:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            return json.loads(text[start : end + 1])
    except:
        pass

    return None


# ==============================
# FILE TO BASE64
# ==============================
def file_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        frappe.log_error(str(e), "File Base64 Error")
        return None


# ==============================
# EMBEDDING
# ==============================
def get_vector_embeddings(input_text_list, api_token=DEFAULT_API_TOKEN):
    if not input_text_list or not isinstance(input_text_list, list):
        frappe.log_error("Embedding Error", "Input must be list of strings")
        return None

    payload = {"model": MODEL_NAME, "input": input_text_list}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    try:
        res = requests.post(
            EMBEDDING_API_URL, headers=headers, data=json.dumps(payload), timeout=300
        )

        if res.status_code == 200:
            data = res.json()
            if data.get("data"):
                return [item["embedding"] for item in data["data"]]
            return None

        frappe.log_error("Embedding API Error", res.text)
        return None

    except Exception as e:
        frappe.log_error(str(e), "Embedding API Error")
        return None


# ==============================
# CALL VLM API (OCR ẢNH)
# ==============================
def call_vlm_api(base64_img, categories):
    prompt = f"""
Hãy phân tích hình ảnh này và thực hiện 2 nhiệm vụ:

1. OCR: Đọc toàn bộ chữ trong ảnh (giữ format dòng).
2. Phân loại: Xác định loại tài liệu thuộc nhóm sau: {categories}.

Trả về JSON:
{{
  "category": "",
  "confidence": "",
  "raw_text": ""
}}
"""

    body = {
        "model": API_MODEL,
        "messages": [
            {"role": "system", "content": "Bạn là assistant, luôn trả JSON hợp lệ."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": "data:image/jpeg;base64," + base64_img},
                    },
                ],
            },
        ],
        "temperature": 0,
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    res = requests.post(VLM_API_URL, headers=headers, data=json.dumps(body))

    if not res.ok:
        frappe.throw(f"VLM API error {res.status_code}: {res.text}")

    data = res.json()
    text = data["choices"][0]["message"]["content"]

    return extractJSON(text)


# ==============================
# CALL LLM API
# ==============================
def call_llm_extract_transfer(raw_text):
    prompt = f"""
Dựa vào văn bản sau, trích thông tin chuyển khoản thành JSON:

NỘI DUNG OCR:
{raw_text}

Trả JSON:
{{
 "transaction_id": "",
 "sender_name": "",
 "receiver_name": "",
 "receiver_account": "",
 "amount": "",
 "content": ""
}}
"""

    body = {
        "model": API_MODEL,
        "messages": [
            {"role": "system", "content": "Trả JSON hợp lệ."},
            {"role": "user", "content": [{"type": "text", "text": prompt}]},
        ],
        "temperature": 0,
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    res = requests.post(LLM_API_URL, headers=headers, data=json.dumps(body))

    data = res.json()
    text = data["choices"][0]["message"]["content"]
    return extractJSON(text)


# ==============================
# Summary JSON to text
# ==============================
def call_llm_convert_json_to_text(json_cv):
    prompt = f"""Tóm tắt CV sau đây thành một bản mô tả chuẩn hóa, ngắn gọn (150–250 từ), tối ưu cho tạo vector embedding phục vụ semantic search và talent-pool matching.

Yêu cầu:
- Không dùng từ ngữ cảm tính (vd: nhiệt huyết, sáng tạo, nỗ lực...)
- Không viết theo văn phong giới thiệu. Không dùng câu văn dài.
- Chỉ tập trung vào dữ liệu: kỹ năng, kinh nghiệm, công nghệ, vị trí làm việc, lĩnh vực dự án và thành tựu định lượng.
- Chuẩn hóa output theo format sau:

{{
  "summary": "mô tả tổng quan 3–5 câu, nêu chức danh chính, số năm kinh nghiệm, lĩnh vực đã làm.",
  "skills": ["kỹ năng 1", "kỹ năng 2", ...],
  "technical_stack": ["tech 1", "tech 2", ...],
  "roles": ["vai trò chính đã đảm nhiệm"],
  "industries": ["lĩnh vực đã làm"],
  "key_experience": [
     "kinh nghiệm tiêu biểu 1",
     "kinh nghiệm tiêu biểu 2"
  ],
  "achievements": [
     "thành tựu định lượng nếu có"
  ],
  "location":["Nơi làm việc mong muốn nếu có"]
}}

CV:
{json_cv}
"""

    body = {
        "model": API_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that responds JSON.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.0,
        "max_tokens": 12048,
    }

    header = headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(LLM_API_URL, headers=headers, data=json.dumps(body))
        if response.status_code == 200:
            data = response.json()
            return json.loads(data["choices"][0]["message"]["content"])
        else:
            return response.text
    except Exception as e:
        frappe.log_error(f"Lỗi convert {str(e)}")
        return None

#Tóm tắt thông tin job
def call_llm_convert_json_to_text_JD(JD_JSON):
    prompt = f"""Tóm tắt Job Description sau thành một mô tả standard hóa, ngắn gọn (150–250 từ), tối ưu cho việc tạo vector embedding dùng trong semantic search và talent-pool matching.

Yêu cầu:
- Không dùng từ cảm tính, không mô tả môi trường, phúc lợi, giọng văn quảng cáo.
- Chỉ giữ thông tin nghề nghiệp: nhiệm vụ chính, kỹ năng, công nghệ, yêu cầu, lĩnh vực.
- Chuẩn hóa output theo cấu trúc cố định sau:

{{
  "role_summary": "mô tả 3–5 câu về mục tiêu vị trí, thâm niên, lĩnh vực, phạm vi công việc.",
  "responsibilities": [
    "nhiệm vụ quan trọng 1",
    "nhiệm vụ quan trọng 2",
    "..."
  ],
  "required_skills": ["kỹ năng bắt buộc 1", "kỹ năng 2", ...],
  "technical_stack": ["công nghệ / tool / framework (nếu có)"],
  "preferred_skills": ["ưu tiên (optional)"],
  "industry": ["lĩnh vực công ty/role"],
  "seniority": "cấp độ yêu cầu (Fresher/Junior/Mid/Senior/Lead)"
}}

Job Description:
{JD_JSON}
"""

    body = {
        "model": API_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that responds JSON.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.0,
        "max_tokens": 12048,
    }

    header = headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(LLM_API_URL, headers=headers, data=json.dumps(body), timeout=300)
        if response.status_code == 200:
            data = response.json()
            return json.loads(data["choices"][0]["message"]["content"])
        else:
            return response.text
    except Exception as e:
        frappe.log_error(f"Lỗi convert {str(e)}")
        return None


# ==============================
# UPLOAD BASE64 FILE
# ==============================
def upload_base64_without_filename(
    base64_data,
    attached_to_doctype=None,
    attached_to_name=None,
    attached_to_field=None,
    is_private=1,
):
    try:
        content = base64.b64decode(base64_data)
        kind = filetype.guess(content)

        ext = kind.extension if kind else "bin"
        mime = kind.mime if kind else "application/octet-stream"

        file_name = f"extract_{int(time.time())}.{ext}"

        saved = save_file(
            fname=file_name,
            content=content,
            dt=attached_to_doctype,
            dn=attached_to_name,
            is_private=is_private,
        )

        saved.file_type = ext.upper()
        saved.save(ignore_permissions=True)

        return saved.file_url

    except Exception:
        frappe.log_error(frappe.get_traceback(), "Upload Extracted CV Error")
        return None


# ==============================
# QUY TRÌNH HOÀN CHỈNH: OCR → TRÍCH THÔNG TIN
# ==============================
@frappe.whitelist()
def extract_image_document(
    file_name, categories="['bank_transfer','invoice','id_card','cv']"
):
    """
    Pipeline:
    1. Lấy file từ DocType File → base64
    2. OCR bằng VLM
    3. Nếu category = bank_transfer → Trích thông tin giao dịch
    """
    file_doc = frappe.get_doc("File", {"name": file_name, "is_private": 1})
    file_path = frappe.utils.get_files_path(file_doc.file_url)

    base64_img = file_to_base64(file_path)
    if not base64_img:
        frappe.throw("Cannot read file to base64")

    ocr_result = call_vlm_api(base64_img, categories)

    if not ocr_result:
        frappe.throw("OCR result invalid")

    result = {
        "ocr": ocr_result,
        "raw_text": ocr_result.get("raw_text"),
        "category": ocr_result.get("category"),
    }

    if ocr_result.get("category") == "bank_transfer":
        transfer_info = call_llm_extract_transfer(ocr_result["raw_text"])
        result["transfer_info"] = transfer_info

    return result


# ====================================
# Extract CV
# ====================================


def extract_cv_backend(file_name):
    # url_extract_ai = f"{AI_BASEURL}/v2/genai/hr-assistants/cv-extraction/pdf-upload"
    url_extract_ai = f"{AI_BASEURL_V2}/api/v1/cv_extract"

    if not file_name:
        frappe.throw("Missing 'file_name' in request parameters.")

    headers = {"x-api-key": "6Bwunlw3Fm1J23tGKZjb/WJXwBDI3gRY971+VUFOU+w="}

    try:
        file_url = frappe.db.get_value(
            "File", {"name": file_name, "is_private": 1}, "file_url"
        )

        file_path = os.path.join(frappe.get_site_path(), file_url.lstrip("/"))

        with open(file_path, "rb") as f:
            files = {"file": (file_name, f, "application/pdf")}
            response = requests.post(
                url_extract_ai, files=files, headers=headers, timeout=12000
            )
        if response.status_code == 200:
            profile = frappe.parse_json(response.json())

            return profile.data
        else:
            frappe.log_error("Error extract")
            return ""

    except frappe.DoesNotExistError:
        frappe.log_error("File does not exists")
        return ""

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "CV Upload API")
        return ""


def extract_cv_backend_file_url(file_url):
    # url_extract_ai = f"{AI_BASEURL}/v2/genai/hr-assistants/cv-extraction/pdf-upload"
    url_extract_ai = f"{AI_BASEURL_V2}/api/v1/cv_extract"

    if not file_url:
        frappe.throw("Missing 'file_url' in request parameters.")

    headers = {"x-api-key": "6Bwunlw3Fm1J23tGKZjb/WJXwBDI3gRY971+VUFOU+w="}

    try:
        file_name = frappe.db.get_value(
            "File", {"file_url": file_url, "is_private": 1}, "file_name"
        )

        file_path = os.path.join(frappe.get_site_path(), file_url.lstrip("/"))

        with open(file_path, "rb") as f:
            files = {"file": (file_name, f, "application/pdf")}
            response = requests.post(
                url_extract_ai, files=files, headers=headers, timeout=12000
            )
        if response.status_code == 200:
            profile = frappe.parse_json(response.json())

            return profile.data
        else:
            frappe.log_error("Error extract")
            return ""

    except frappe.DoesNotExistError:
        frappe.log_error("File does not exists")
        return ""

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "CV Upload API")
        return ""
