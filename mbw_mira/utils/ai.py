import requests
import json
import frappe

# Lưu ý quan trọng:
# 1. TOKEN API (Bearer) KHÔNG NÊN được hardcode trong code production.
#    Nên lưu trữ trong DocType Setting hoặc Site Config.
# 2. Bạn cần đảm bảo thư viện 'requests' đã được cài đặt trong môi trường bench.

EMBEDDING_API_URL = "https://aiapi.fastwork.vn/embedding_qwen/v1/embeddings"
# Tạm thời hardcode, nhưng khuyến nghị lấy từ frappe.conf.get()
DEFAULT_API_TOKEN = "1d161ba4-ddab-491d-a2b6-ad0eac14fb33" 
MODEL_NAME = "Qwen/Qwen3-Embedding-0.6B"

def get_vector_embeddings(input_text_list, api_token=DEFAULT_API_TOKEN):
    """
    Gọi API để lấy vector embedding cho một danh sách các chuỗi văn bản.

    :param input_text_list: Danh sách các chuỗi văn bản cần tạo vector (ví dụ: ["hello", "world"]).
    :param api_token: Token API (Bearer) để xác thực.
    :return: Danh sách các vector (list of lists of floats) hoặc None nếu có lỗi.
    """
    if not input_text_list or not isinstance(input_text_list, list):
        frappe.log_error(title="Embedding Error", message="Input must be a non-empty list of strings.")
        return None

    # 1. Chuẩn bị Payload
    payload = {
        "model": MODEL_NAME,
        "input": input_text_list
    }

    # 2. Chuẩn bị Headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    try:
        # 3. Thực hiện POST Request
        response = requests.request(
            "POST", 
            EMBEDDING_API_URL, 
            headers=headers, 
            data=json.dumps(payload),
            timeout=30 # Đặt timeout để tránh treo
        )
        
        # 4. Kiểm tra trạng thái HTTP
        if response.status_code == 200:
            data = response.json()
            # Kiểm tra xem 'data' có tồn tại và chứa 'embedding' không
            if data.get('data'):
                # Trích xuất chỉ các mảng vector (embedding)
                embeddings = [item['embedding'] for item in data['data']]
                return embeddings
            else:
                frappe.log_error(
                    title="Embedding API Error", 
                    message=f"API returned 200 but missing embedding data. Response: {data}"
                )
                return None
        else:
            # Ghi log lỗi nếu API trả về trạng thái lỗi (4xx, 5xx)
            frappe.log_error(
                title="Embedding API Failed", 
                message=f"Status: {response.status_code}, Response: {response.text}"
            )
            return None

    except requests.exceptions.RequestException as e:
        # Xử lý các lỗi kết nối, timeout, DNS, v.v.
        frappe.log_error(
            title="Embedding Connection Error", 
            message=str(e)
        )
        return None


    