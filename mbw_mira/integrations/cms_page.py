import frappe
from mbw_mira.integrations.api_provider import APIProvider

class CMSAPI:
    """
    Wrapper sử dụng APIProvider để gọi các dịch vụ CMS MBW.
    """

    def __init__(self):
        self.provider = APIProvider()

    # --- 1. Templates ---
    def get_templates(self, project_folder=None, fields=None, start=0, limit_page_length=50, order_by=None, search_query=None):
        params = {
            "start": start,
            "limit_page_length": limit_page_length
        }
        
        if project_folder:
            params["project_folder"] = project_folder
        if fields:
            params["fields"] = fields
        if order_by:
            params["order_by"] = order_by
        if search_query:
            params["search_query"] = search_query
            
        return self.provider.get("mbw_cms.api.page_api.get_templates", params=params)

    # --- 2. Page từ template ---
    def create_page_by_template(self, template_id, page_title, **kwargs):
        # Filter out Frappe internal fields
        frappe_internal_fields = ['cmd', 'doctype', 'name', 'owner', 'modified_by']
        filtered_kwargs = {k: v for k, v in kwargs.items() if k not in frappe_internal_fields}
        
        data = {
            "template_id": template_id, 
            "page_title": page_title,
            "project_folder": "MBW_MIRA"  # Hardcoded to save pages in correct folder
        }
        data.update(filtered_kwargs)
        
        # Special handling for receive_data_configs
        if 'receive_data_configs' in data:
            receive_configs = data['receive_data_configs']
            print(f"📧 Raw receive_data_configs: {receive_configs}")
            print(f"📧 Type: {type(receive_configs)}")
            
            # Validate and clean receive_data_configs
            if receive_configs is None:
                print("⚠️ receive_data_configs is None, removing field")
                data.pop('receive_data_configs', None)
            elif isinstance(receive_configs, list):
                if len(receive_configs) == 0:
                    print("✅ receive_data_configs is empty list, keeping as empty array")
                    # Keep empty array as is
                else:
                    # Validate each config in the list
                    valid_configs = []
                    for i, config in enumerate(receive_configs):
                        if isinstance(config, dict) and config.get('type'):
                            valid_configs.append(config)
                            print(f"✅ Config {i} is valid: {config.get('type')}")
                        else:
                            print(f"⚠️ Config {i} is invalid, skipping: {config}")
                    
                    if valid_configs:
                        data['receive_data_configs'] = valid_configs
                        print(f"📧 Final valid configs: {len(valid_configs)} items")
                    else:
                        print("⚠️ No valid configs found, keeping as empty array")
                        data['receive_data_configs'] = []
            else:
                print(f"⚠️ receive_data_configs has unexpected type {type(receive_configs)}, removing field")
                data.pop('receive_data_configs', None)
        else:
            print("✅ receive_data_configs field not present in payload - this is OK")
        
        print("🚀 Final create page data:", data)
        return self.provider.post("mbw_cms.api.page_api.create_page_by_template", data=data)

    # --- 3. Publish / Unpublish ---
    def publish_page(self, page_id):
        return self.provider.post("mbw_cms.api.page_api.publish_page", data={"page_id": page_id})

    def unpublish_page(self, page_id):
        return self.provider.post("mbw_cms.api.page_api.unpublish_page", data={"page_id": page_id})

    # --- 4. Update recruitment page ---
    def update_recruitment_page(self, page_id, **kwargs):
        # Filter out Frappe internal fields
        frappe_internal_fields = ['cmd', 'doctype', 'name', 'owner', 'modified_by']
        filtered_kwargs = {k: v for k, v in kwargs.items() if k not in frappe_internal_fields}
        
        data = {"page_id": page_id}
        data.update(filtered_kwargs)
        
        print("🚀 Final data to send:", data)
        print("🚀 Filtered out fields:", [k for k in kwargs.keys() if k in frappe_internal_fields])
        
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

    # --- 8. Get pages (public/published) ---
    def get_page_public(self, published=1, fields=None, start=0, limit_page_length=20, order_by=None, search_query=None, project_folder="MBW_ATS"):
        params = {
            "published": published,
            "start": start,
            "limit_page_length": limit_page_length,
            "project_folder": project_folder  # Hardcoded to MBW_MIRA
        }
        
        if fields:
            params["fields"] = fields
        if order_by:
            params["order_by"] = order_by
        if search_query:
            params["search_query"] = search_query
            
        return self.provider.get("mbw_cms.api.page_api.get_pages", params=params)

    # --- 9. Get fields by template ---
    def get_fields_by_template(self, template_id):
        return self.provider.get("mbw_cms.api.page_api.get_fields_by_template", params={"template_id": template_id})

    # --- 9b. Get fields mapping (new API for field mapping) ---
    def get_fields_mapping(self):
        """Get fields available for mapping in receive data configs"""
        return self.provider.get("mbw_cms.api.page_api.get_fields_mapping")

    # --- 10. Create link account (receive data config) ---
    def create_link_account(self, form_config_id, receive_data_config):
        data = {
            "form_config_id": form_config_id,
            "receive_data_config": receive_data_config
        }
        return self.provider.post("mbw_cms.api.page_api.create_link_account", data=data)

    # --- 11. Update link account (receive data config) ---
    def update_link_account(self, receive_data_config):
        data = {"receive_data_config": receive_data_config}
        return self.provider.put("mbw_cms.api.page_api.update_link_account", data=data)

    # --- 12. Delete link account (receive data config) ---
    def delete_link_account(self, receive_data_config_id):
        return self.provider.delete("mbw_cms.api.page_api.delete_link_account", data={"receive_data_config_id": receive_data_config_id})

    # --- 13. Get link accounts by page ID ---
    def get_link_accounts_by_page(self, page_id):
        return self.provider.get("mbw_cms.api.page_api.get_link_accounts_by_page", params={"page_id": page_id})

    # --- 14. Get company profile list ---
    def get_company_profile_list(self):
        return self.provider.get("mbw_cms.api.company_profile_api.get_list")

    # --- 15. Get company profile detail ---
    def get_company_profile_detail(self, company_profile_name):
        return self.provider.get("mbw_cms.api.company_profile_api.get_detail", params={"company_profile_name": company_profile_name})


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
def get_templates(project_folder=None, fields=None, start=0, limit_page_length=50, order_by=None, search_query=None):
    """Lấy danh sách templates từ CMS
    
    Args:
        project_folder: Filter by project folder (optional)
        fields: Comma-separated list of fields to return (optional)
        start: Starting index for pagination (default: 0)
        limit_page_length: Number of records per page (default: 50)
        order_by: Field to order by (optional)
        search_query: Search query string (optional)
    """
    try:
        cms = CMSAPI()
        return cms.get_templates(
            project_folder=project_folder,
            fields=fields,
            start=int(start) if start else 0,
            limit_page_length=int(limit_page_length) if limit_page_length else 50,
            order_by=order_by,
            search_query=search_query
        )
    except Exception as e:
        error_msg = str(e)[:100]  # Truncate to prevent CharacterLengthExceededError
        frappe.log_error(title="CMS get_templates error", message=str(e))
        return {"status": "error", "message": error_msg}


@frappe.whitelist()
def create_page_by_template(**kwargs):
    """Tạo page từ template"""
    try:
        # Debug: Log incoming kwargs
        frappe.logger().info(f"📥 Incoming kwargs: {kwargs}")
        
        template_id = kwargs.get('template_id')
        page_title = kwargs.get('page_title')
        receive_data_configs = kwargs.get('receive_data_configs', [])
        
        if not template_id:
            return {"status": "error", "message": "template_id is required"}
        
        if not page_title:
            return {"status": "error", "message": "page_title is required"}
        
        # Debug receive_data_configs
        frappe.logger().info(f"📧 Receive data configs: {receive_data_configs}")
        
        # Remove template_id and page_title from kwargs to avoid duplication
        kwargs.pop('template_id', None)
        kwargs.pop('page_title', None)
        
        frappe.logger().info(f"📤 Calling CMS API with template_id: {template_id}, page_title: {page_title}")
        frappe.logger().info(f"📤 Additional kwargs: {kwargs}")
        
        cms = CMSAPI()
        # Pass remaining kwargs (optional fields)
        result = cms.create_page_by_template(template_id, page_title, **kwargs)
        frappe.logger().info(f"✅ CMS result: {result}")
        return result
    except Exception as e:
        frappe.log_error(f"Error creating page: {str(e)}")
        frappe.logger().error(f"❌ Full error details: {e}")
        import traceback
        frappe.logger().error(f"❌ Traceback: {traceback.format_exc()}")
        return {"status": "error", "message": f"Error creating page: {str(e)}"}


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


@frappe.whitelist(allow_guest=True)
def get_page_public(published=1, fields=None, start=0, limit_page_length=20, order_by=None, search_query=None, project_folder=None):
    """Lấy danh sách pages đã publish
    
    Args:
        published: Filter by publish status (1=published, 0=draft, None=all)
        fields: Comma-separated list of fields to return (optional)
        start: Starting index for pagination (default: 0)
        limit_page_length: Number of records per page (default: 20)
        order_by: Field to order by (optional)
        search_query: Search query string (optional)
        project_folder: Filter by project folder (default: MBW_ATS)
    """
    try:
        cms = CMSAPI()
        return cms.get_page_public(
            published=int(published) if published is not None else None,
            fields=fields,
            start=int(start) if start else 0,
            limit_page_length=int(limit_page_length) if limit_page_length else 20,
            order_by=order_by,
            search_query=search_query,
            project_folder=project_folder or "MBW_MIRA"
        )
    except Exception as e:
        frappe.log_error(f"Error getting page public: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def get_fields_by_template(template_id):
    """Lấy danh sách các trường mapping có trong trang mẫu"""
    try:
        if not template_id:
            return {"status": "error", "message": "template_id is required"}
        
        cms = CMSAPI()
        return cms.get_fields_by_template(template_id)
    except Exception as e:
        frappe.log_error(f"Error getting fields by template: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def get_fields_mapping():
    """Lấy danh sách các trường có thể mapping cho receive data configs
    
    Returns danh sách fields với format:
    {
        "status": "success",
        "data": [
            {"label": "Full Name", "fieldname": "full_name", "fieldtype": "Data"},
            ...
        ]
    }
    """
    try:
        cms = CMSAPI()
        return cms.get_fields_mapping()
    except Exception as e:
        error_msg = str(e)[:100]  # Truncate to prevent CharacterLengthExceededError
        frappe.log_error(title="CMS get_fields_mapping error", message=str(e)[:500])
        
        # Return fallback fields if CMS API is not available yet
        fallback_fields = [
            {"label": "Full Name", "fieldname": "full_name", "fieldtype": "Data"},
            {"label": "Primary Email", "fieldname": "primary_email", "fieldtype": "Data"},
            {"label": "Phone Number", "fieldname": "phone_number", "fieldtype": "Data"},
            {"label": "LinkedIn URL", "fieldname": "linkedin_url", "fieldtype": "Data"},
            {"label": "CV Upload", "fieldname": "cv_upload", "fieldtype": "Attach"},
            {"label": "Date of Birth", "fieldname": "date_of_birth", "fieldtype": "Date"},
            {"label": "Form ID", "fieldname": "form_id", "fieldtype": "Data"},
            {"label": "Page ID", "fieldname": "page_id", "fieldtype": "Data"},
            {"label": "Acquisition Date", "fieldname": "acquisition_date", "fieldtype": "Date"},
            {"label": "UTM Source", "fieldname": "utm_source", "fieldtype": "Data"},
            {"label": "UTM Medium", "fieldname": "utm_medium", "fieldtype": "Data"},
            {"label": "UTM Campaign", "fieldname": "utm_campaign", "fieldtype": "Data"},
            {"label": "UTM Term", "fieldname": "utm_term", "fieldtype": "Data"},
            {"label": "UTM Content", "fieldname": "utm_content", "fieldtype": "Data"},
            {"label": "Form URL", "fieldname": "form_url", "fieldtype": "Data"},
            {"label": "Custom Field", "fieldname": "custom_field", "fieldtype": "Data"}
        ]
        
        return {
            "status": "success",
            "message": "Using fallback fields (CMS API not available)",
            "data": fallback_fields
        }


@frappe.whitelist()
def create_link_account(form_config_id, receive_data_config):
    """Tạo cấu hình nhận dữ liệu"""
    try:
        if not form_config_id or not receive_data_config:
            return {"status": "error", "message": "form_config_id and receive_data_config are required"}
        
        # Parse receive_data_config if it's a string
        if isinstance(receive_data_config, str):
            import json
            receive_data_config = json.loads(receive_data_config)
        
        cms = CMSAPI()
        return cms.create_link_account(form_config_id, receive_data_config)
    except Exception as e:
        frappe.log_error(f"Error creating link account: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def update_link_account(receive_data_config):
    """Cập nhật cấu hình nhận dữ liệu"""
    try:
        if not receive_data_config:
            return {"status": "error", "message": "receive_data_config is required"}
        
        # Parse receive_data_config if it's a string
        if isinstance(receive_data_config, str):
            import json
            receive_data_config = json.loads(receive_data_config)
        
        cms = CMSAPI()
        return cms.update_link_account(receive_data_config)
    except Exception as e:
        frappe.log_error(f"Error updating link account: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def delete_link_account(receive_data_config_id):
    """Xóa cấu hình nhận dữ liệu"""
    try:
        if not receive_data_config_id:
            return {"status": "error", "message": "receive_data_config_id is required"}
        
        cms = CMSAPI()
        return cms.delete_link_account(receive_data_config_id)
    except Exception as e:
        frappe.log_error(f"Error deleting link account: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def get_link_accounts_by_page(page_id):
    """Lấy danh sách cấu hình nhận dữ liệu theo page id"""
    try:
        if not page_id:
            return {"status": "error", "message": "page_id is required"}
        
        cms = CMSAPI()
        return cms.get_link_accounts_by_page(page_id)
    except Exception as e:
        frappe.log_error(f"Error getting link accounts by page: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def get_company_profile_list():
    """Lấy danh sách profile công ty"""
    try:
        cms = CMSAPI()
        return cms.get_company_profile_list()
    except Exception as e:
        frappe.log_error(f"Error getting company profile list: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def get_company_profile_detail(company_profile_name):
    """Lấy chi tiết một profile công ty"""
    try:
        if not company_profile_name:
            return {"status": "error", "message": "company_profile_name is required"}
        
        cms = CMSAPI()
        return cms.get_company_profile_detail(company_profile_name)
    except Exception as e:
        frappe.log_error(f"Error getting company profile detail: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def get_doctype_fields(doctype):
    """Lấy danh sách fields của doctype để mapping"""
    try:
        if not doctype:
            return {"status": "error", "message": "doctype is required"}
        
        # Kiểm tra quyền truy cập doctype
        if not frappe.has_permission(doctype, "read"):
            return {"status": "error", "message": f"No permission to read {doctype}"}
        
        meta = frappe.get_meta(doctype)
        
        # Lọc các fields phù hợp cho mapping
        relevant_fieldtypes = ['Data', 'Text', 'Small Text', 'Long Text', 'Int', 'Float', 'Date', 'Datetime', 'Check', 'Select', 'Link', 'Attach', 'Attach Image', 'Currency']
        exclude_fields = ['name', 'owner', 'creation', 'modified', 'modified_by', 'docstatus', 'idx', 'parent', 'parenttype', 'parentfield']
        
        fields = []
        for field in meta.get("fields"):
            if (field.fieldtype in relevant_fieldtypes and 
                field.fieldname not in exclude_fields and 
                not field.hidden and 
                not field.read_only):
                fields.append({
                    "fieldname": field.fieldname,
                    "label": field.label or field.fieldname,
                    "fieldtype": field.fieldtype
                })
        
        return {"status": "success", "data": fields}
    except Exception as e:
        frappe.log_error(f"Error getting doctype fields: {str(e)}")
        return {"status": "error", "message": str(e)}