import frappe
from mbw_mira.integrations.api_provider import APIProvider

class CMSAPI:
    """
    Wrapper sử dụng APIProvider để gọi các dịch vụ CMS MBW.
    """

    def __init__(self):
        self.provider = APIProvider()

    # --- 1. Templates ---
    def get_templates(self):
        return self.provider.get("mbw_cms.api.page_api.get_templates")

    # --- 2. Page từ template ---
    def create_page_by_template(self, template_id, page_title, **kwargs):
        data = {"template_id": template_id, "page_title": page_title}
        data.update(kwargs)
        return self.provider.post("mbw_cms.api.page_api.create_page_by_template", data=data)

    # --- 3. Publish / Unpublish ---
    def publish_page(self, page_id):
        return self.provider.post("mbw_cms.api.page_api.publish_page", data={"page_id": page_id})

    def unpublish_page(self, page_id):
        return self.provider.post("mbw_cms.api.page_api.unpublish_page", data={"page_id": page_id})

    # --- 4. Update recruitment page ---
    def update_recruitment_page(self, page_id, **kwargs):
        data = {"page_id": page_id}
        data.update(kwargs)
        return self.provider.put("mbw_cms.api.page_api.update_recruitment_page_details", data=data)

    # --- 5. Create / Update page từ blocks ---
    def create_page(self, page_title, blocks=None):
        data = {"page_title": page_title}
        if blocks:
            data["blocks"] = blocks
        return self.provider.post("mbw_cms.api.page_api.create_page", data=data)

    def update_page(self, page_id, page_title=None, blocks=None):
        data = {"page_id": page_id}
        if page_title:
            data["page_title"] = page_title
        if blocks:
            data["blocks"] = blocks
        return self.provider.put("mbw_cms.api.page_api.update_page", data=data)

    # --- 6. Delete page ---
    def delete_page(self, page_id):
        return self.provider.delete("mbw_cms.api.page_api.delete_page", data={"page_id": page_id})

    # --- 7. Get page details ---
    def get_page_details(self, page_id):
        return self.provider.get("mbw_cms.api.page_api.get_page_details", params={"page_id": page_id})


def example_usage():
    cms = CMSAPI()

    # 1. Lấy template
    templates = cms.get_templates()
    print(templates)

    # # 2. Tạo page từ template
    # page = cms.create_page_by_template(
    #     template_id="TPL001",
    #     page_title="Trang tuyển dụng Dev",
    #     company_name="MBW Corp",
    #     job_title="Developer"
    # )
    # page_id = page["data"]["page_id"]

    # # 3. Publish page
    # cms.publish_page(page_id)

    # # 4. Update recruitment info
    # cms.update_recruitment_page(page_id, salary="15M-20M")

    # # 5. Lấy chi tiết page
    # details = cms.get_page_details(page_id)
    # frappe.logger().info(details)

    # # 6. Unpublish và xóa page
    # cms.unpublish_page(page_id)
    # cms.delete_page(page_id)


# ============================================
# Whitelisted API endpoints cho frontend
# ============================================

@frappe.whitelist(allow_guest=True)
def get_templates():
    """Lấy danh sách templates từ CMS"""
    try:
        cms = CMSAPI()
        return cms.get_templates()
    except Exception as e:
        frappe.log_error(f"Error getting templates: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def create_page_by_template(**kwargs):
    """Tạo page từ template"""
    try:
        # Debug: Log incoming kwargs
        frappe.logger().info(f"📥 Received kwargs: {kwargs}")
        frappe.logger().info(f"📥 kwargs type: {type(kwargs)}")
        frappe.logger().info(f"📥 kwargs keys: {list(kwargs.keys())}")
        
        # Remove Frappe-specific parameters
        kwargs.pop("cmd", None)  # ← FIX: Remove cmd parameter
        
        template_id = kwargs.pop("template_id", None)
        page_title = kwargs.pop("page_title", None)
        
        frappe.logger().info(f"📝 template_id: {template_id}")
        frappe.logger().info(f"📝 page_title: {page_title}")
        frappe.logger().info(f"📝 remaining kwargs: {kwargs}")
        
        if not template_id or not page_title:
            return {"status": "error", "message": "template_id and page_title are required"}
        
        cms = CMSAPI()
        # Pass remaining kwargs (optional fields)
        result = cms.create_page_by_template(template_id, page_title, **kwargs)
        frappe.logger().info(f"✅ CMS result: {result}")
        return result
    except Exception as e:
        frappe.logger().error(f"❌ Error creating page: {str(e)}")
        frappe.log_error(f"Error creating page by template: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def publish_page(page_id):
    """Publish page"""
    try:
        if not page_id:
            return {"status": "error", "message": "page_id is required"}
        
        cms = CMSAPI()
        return cms.publish_page(page_id)
    except Exception as e:
        frappe.log_error(f"Error publishing page: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def unpublish_page(page_id):
    """Unpublish page"""
    try:
        if not page_id:
            return {"status": "error", "message": "page_id is required"}
        
        cms = CMSAPI()
        return cms.unpublish_page(page_id)
    except Exception as e:
        frappe.log_error(f"Error unpublishing page: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def update_recruitment_page(page_id, **kwargs):
    """Update recruitment page details"""
    try:
        if not page_id:
            return {"status": "error", "message": "page_id is required"}
        
        cms = CMSAPI()
        return cms.update_recruitment_page(page_id, **kwargs)
    except Exception as e:
        frappe.log_error(f"Error updating recruitment page: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def create_page(page_title, blocks=None):
    """Tạo page từ blocks"""
    try:
        if not page_title:
            return {"status": "error", "message": "page_title is required"}
        
        cms = CMSAPI()
        return cms.create_page(page_title, blocks)
    except Exception as e:
        frappe.log_error(f"Error creating page: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def update_page(page_id, page_title=None, blocks=None):
    """Update page"""
    try:
        if not page_id:
            return {"status": "error", "message": "page_id is required"}
        
        cms = CMSAPI()
        return cms.update_page(page_id, page_title, blocks)
    except Exception as e:
        frappe.log_error(f"Error updating page: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def delete_page(page_id):
    """Delete page"""
    try:
        if not page_id:
            return {"status": "error", "message": "page_id is required"}
        
        cms = CMSAPI()
        return cms.delete_page(page_id)
    except Exception as e:
        frappe.log_error(f"Error deleting page: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def get_page_details(page_id):
    """Lấy chi tiết page"""
    try:
        if not page_id:
            return {"status": "error", "message": "page_id is required"}
        
        cms = CMSAPI()
        return cms.get_page_details(page_id)
    except Exception as e:
        frappe.log_error(f"Error getting page details: {str(e)}")
        return {"status": "error", "message": str(e)}