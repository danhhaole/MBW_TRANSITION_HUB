import frappe
import urllib.parse
import json
import requests
import datetime
from werkzeug.wrappers import Response
from frappe import _

@frappe.whitelist()
def get_linkedin_auth_url():    
    #client_id = frappe.conf.linkedin_client_id or "86t9ghzv49c4pg"
    data = frappe.request.data
    if not data:
        frappe.throw(frappe._("No data received"))
    
    payload = json.loads(data)
    client_id = payload.get("client_id")
    client_secret = payload.get("client_secret")
    if not client_id:
        frappe.throw(frappe._("Client ID Require"))
    if not client_secret:
        frappe.throw(frappe._("Client Secret Require"))
    scope = "profile w_member_social"
    host_url = frappe.request.host_url  # remove trailing slash nếu có
    redirect_uri = f"{host_url}api/method/mbw_mira.integration.social.linkedin_oauth_callback"
    
     # KHÔNG ENCODE redirect_uri ở đây!
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"  # <- giữ nguyên
        f"&scope={urllib.parse.quote(scope)}"
        f"&client_secret={client_secret}"
    )

    return auth_url

@frappe.whitelist(allow_guest=True)
def linkedin_oauth_callback(code=None):
    
    if not code:
        frappe.throw("Missing authorization code")

    client_id = frappe.request.args.get("client_id")
    client_secret = frappe.request.args.get("client_secret")
    redirect_uri = f"{frappe.request.host_url}api/method/mbw_mira.integration.social.linkedin_oauth_callback"

    # 1. Exchange code for token
    token_res = requests.post("https://www.linkedin.com/oauth/v2/accessToken", data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    })

    token_data = token_res.json()
    access_token = token_data.get("access_token")
    expires_in = token_data.get("expires_in")

    if not access_token:
        frappe.throw(f"Lỗi lấy token: {token_data}")

    # 2. Get user info
    user_info_res = requests.get("https://api.linkedin.com/v2/me", headers={
        "Authorization": f"Bearer {access_token}"
    })
    user_info = user_info_res.json()
    linkedin_id = user_info.get("id")
    linkedin_name = user_info.get("localizedFirstName", "") + " " + user_info.get("localizedLastName", "")

    # 3. Save to DB (each user has their own token)
    user = frappe.session.user

    doc = frappe.get_doc({
        "doctype":"Mira Social Media Token",
        "user":user,
        "provider":"LinkedIn",
        "access_token":access_token,
        "expires_at":frappe.utils.now_datetime() + datetime.timedelta(seconds=expires_in),
        "client_id": client_id,
        "client_secret": client_secret
    })
    doc.save(ignore_permissions=True)
    frappe.db.commit()

    html = """
    <html>
      <head><title>LinkedIn Connected</title></head>
      <body>
        <script>
          if (window.opener) {
            window.opener.postMessage({ platform: 'linkedin', status: 'connected' }, "*");
            window.close();
          } else {
            document.body.innerHTML = "Xác thực thành công. Bạn có thể đóng tab này.";
          }
        </script>
      </body>
    </html>
    """
    return Response(html, content_type='text/html')

LINKEDIN_API = "https://api.linkedin.com/v2"
@frappe.whitelist()
def share_job_post_on_social_media(job_post_id, platform):
    try:
        job_post = frappe.get_doc("Mira Job Opening", job_post_id)
        job_title = job_post.jo_public_title
        job_description = job_post.jo_job_description
        job_url = f"{frappe.request.host_url}/job/{job_post_id}"
        token_doc = frappe.get_value(
            "Mira Social Media Token",
            {"user": frappe.session.user, "provider": "linkedin"},
            ["access_token"],
            as_dict=True,
        )
        
        if not token_doc:
            frappe.throw(frappe._("Bạn chưa kết nối."))
            
        access_token = token_doc.access_token
            
        # Chia sẻ lên Facebook
        if platform == "facebook":
            url = "https://graph.facebook.com/v13.0/me/feed"
            data = {
                "message": f"Job Opening: {job_title}\n{job_description}\nApply here: {job_url}",
                "access_token": access_token
            }
            response = requests.post(url, data=data)

        # Chia sẻ lên LinkedIn
        elif platform == "linkedin":
             # Bước 1: Lấy thông tin người dùng để có `person URN`
            
            profile = requests.get(
                f"{LINKEDIN_API}/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            print(profile.status_code)
            if not profile.ok:
                frappe.throw(frappe._("Không lấy được thông tin LinkedIn user."))
                
            linkedin_id = profile.json().get("id")
            person_urn = f"urn:li:person:{linkedin_id}"

            # Bước 2: Tạo nội dung bài đăng
            message = f"🚀 {job_title} - Ứng tuyển ngay tại: {job_url}"
            payload = {
                "author": person_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": message},
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            
             # Bước 3: Gửi POST lên LinkedIn
            response = requests.post(
                f"{LINKEDIN_API}/ugcPosts",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            if response.status_code != 201:
                frappe.log_error(response.text, "LinkedIn Share Error")
                frappe.throw(_("Không thể đăng bài lên LinkedIn: {0}").format(response.text))

            return {"message": "Đã chia sẻ thành công lên LinkedIn!"}

        # Kiểm tra nếu việc chia sẻ thành công
        if response.status_code == 200:
            return {"status": "success", "message": "Job post shared successfully!"}
        else:
            frappe.log_error(f"Share Error: {response.json}")
            frappe.throw(response.text)

    except Exception as e:
        frappe.log_error(f"TopCV Connect Error: {str(e)}")
        frappe.throw("Lỗi")
    
@frappe.whitelist()
def check_social_media_connection():
    try:
        # Kiểm tra xem người dùng đã kết nối với mạng xã hội chưa
        user_social_media = frappe.get_all("Mira Social Media Token",fields=["provider"], filters={"user": frappe.session.user})

        if user_social_media:
            # Nếu tìm thấy thông tin kết nối, trả về thông tin nền tảng đã kết nối
            social_media_data = user_social_media[0]
            return {
                "connected": True,
                "platform": social_media_data.provider,  # Facebook, LinkedIn, v.v.
                "client_id":social_media_data.client_id,
                "client_secret":social_media_data.client_secret
            }
        else:
            # Nếu không tìm thấy kết nối, trả về False
            return {
                "connected": False,
            }

    except Exception as e:
        frappe.log_error(f"Error in check_social_media_connection: {str(e)}")
        frappe.throw("Error in check_social_media_connection")
        return {"connected": False, "message": str(e)}


#Disconnect Platform
@frappe.whitelist()
def disconnect_platform():
    try:
        data = frappe.request.data
        if not data:
            frappe.throw(frappe._("No data received"))
        payload = json.loads(data)

        provider = payload.get("platform")
        if not provider:
            frappe.throw(frappe._("No data received"))
        user = frappe.session.user
        
        frappe.delete_doc(doctype="Mira Social Media Token", filters={"provider":provider, "user":user})
            
            
    except Exception as e:
        frappe.log_error(f"{str(e)}")
        frappe.throw(frappe._("Disconnect Fail"))

#Facebook
@frappe.whitelist()
def get_facebook_auth_url():
    data = frappe.request.data
    if not data:
        frappe.throw(frappe._("No data received"))
    
    payload = json.loads(data)
    client_id = payload.get("client_id")
    client_secret = payload.get("client_secret")
    if not client_id:
        frappe.throw(frappe._("Client ID Require"))
    if not client_secret:
        frappe.throw(frappe._("Client Secret Require"))
    redirect_uri = f"{frappe.request.host_url}/api/method/mbw_mira.integration.social.facebook_callback"
    scope = "public_profile,email,pages_manage_posts,pages_read_engagement,pages_show_list"

    query = urllib.parse.urlencode({
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scope,
        "state": frappe.session.user,
        "client_secret":client_secret
    })

    return f"https://www.facebook.com/v19.0/dialog/oauth?{query}"

@frappe.whitelist()
def facebook_callback():
    code = frappe.local.form_dict.get("code")
    state = frappe.local.form_dict.get("state")

    if not code:
        frappe.throw("Missing code")

    client_id = frappe.request.args.get("client_id")
    client_secret = frappe.request.args.get("client_secret")
    redirect_uri = "https://yourdomain.com/api/method/your_app.api.facebook_callback"

    # Gọi Facebook để lấy access_token
    token_res = requests.get("https://graph.facebook.com/v19.0/oauth/access_token", params={
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri
    })

    token_data = token_res.json()
    access_token = token_data.get("access_token")

    if not access_token:
        frappe.throw("Không lấy được Facebook access_token")

    # (Tuỳ chọn) Lấy thông tin user
    user_res = requests.get("https://graph.facebook.com/me", params={
        "access_token": access_token,
        "fields": "id,name,email"
    })
    user_data = user_res.json()

    # Lưu access_token vào SocialMediaToken hoặc DocType riêng
    user = frappe.session.user

    doc = frappe.get_doc({
        "doctype":"Mira Social Media Token",
        "user":user,
        "provider":"Facebook",
        "access_token":access_token,
        "expires_at":frappe.utils.now_datetime() + datetime.timedelta(seconds=300),
        "client_id": client_id,
        "client_secret": client_secret
    })
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    # ✅ Trả về HTML để đóng popup
    html = """
    <html>
      <body>
        <script>
          if (window.opener) {
            window.opener.postMessage({ platform: 'facebook', status: 'connected' }, "*");
            window.close();
          }
        </script>
      </body>
    </html>
    """
    return Response(html, content_type='text/html')