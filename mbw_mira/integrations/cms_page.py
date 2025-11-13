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
    frappe.logger().info(templates)

    # 2. Tạo page từ template
    page = cms.create_page_by_template(
        template_id="TPL001",
        page_title="Trang tuyển dụng Dev",
        company_name="MBW Corp",
        job_title="Developer"
    )
    page_id = page["data"]["page_id"]

    # 3. Publish page
    cms.publish_page(page_id)

    # 4. Update recruitment info
    cms.update_recruitment_page(page_id, salary="15M-20M")

    # 5. Lấy chi tiết page
    details = cms.get_page_details(page_id)
    frappe.logger().info(details)

    # 6. Unpublish và xóa page
    cms.unpublish_page(page_id)
    cms.delete_page(page_id)