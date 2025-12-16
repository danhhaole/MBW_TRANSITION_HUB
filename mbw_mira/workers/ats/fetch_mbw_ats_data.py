import frappe
import logging
from mbw_mira.integrations.ats.frappe_site_provider import FrappeSiteProvider
from datetime import datetime
import json
from urllib.parse import unquote
from frappe.utils import get_datetime_str

logger = logging.getLogger(__name__)

def fetch_mbw_ats_data(campaign_name):
    """
    Worker: Fetch ACTIVE campaign data from MBW ATS and save to Mira Talent.
    """
    campaign = frappe.get_doc("Mira Campaign", campaign_name)
    source_name = campaign.source
    segment_id = campaign.target_segment

    with FrappeSiteProvider(source_name) as provider:
        if provider.sync_direction not in ("Pull", "Both"):
            return

        criteria = campaign.criteria or {}
        if isinstance(criteria, str):
            criteria = json.loads(criteria)

        total = 0
        try:
            filters = criteria.get("filters", {})
            fields = criteria.get("fields", ["name"])
            candidates = provider.get_list("ATS_Candidate", filters=filters, fields=fields)

            if candidates:
                total = save_candidates_to_talent_pool(provider, candidates, campaign, source_name, segment_id)

            frappe.publish_realtime(
                'fetch_data_integrations_ats',
                message={'campaign': campaign_name, "segment": segment_id}
            )

            return total
        except Exception as e:
            logger.error(f"[MBW ATS] Failed fetching data for campaign {campaign_name} — {str(e)}", exc_info=True)
            return total


def save_candidates_to_talent_pool(provider, candidates, campaign, source_name, segment_id):
    """
    Chuẩn hóa & lưu danh sách ứng viên vào Mira Talent
    """
    count = 0
    for record in candidates:
        try:
            record = provider.get_doc("ATS_Candidate", record.get('name'))
            doc_data = map_mbw_ats_to_talentprofiles(record, campaign.name, source_name, segment_id)

            # Kiểm tra ứng viên đã tồn tại theo email hoặc sync_id
            existing = None
            if doc_data.get("email"):
                existing = frappe.db.exists("Mira Talent", {"email": doc_data["email"]})
            if not existing and record.get("name"):
                existing = frappe.db.exists("Mira Talent", {"name": record.get("name")})

            if existing:
                doc = frappe.get_doc("Mira Talent", existing)
                doc.update(doc_data)
                doc.save(ignore_permissions=True)
            else:
                doc = frappe.get_doc(doc_data)
                doc.insert(ignore_permissions=True)

            frappe.db.commit()
            count += 1
        except Exception as e:
            logger.error(f"[Mira Talent] Failed to save {record.get('can_full_name')} — {str(e)}", exc_info=True)
            frappe.db.rollback()
            continue

    return count


def map_mbw_ats_to_talentprofiles(record, campaign_name, source_name, segment_id=None):
    """
    Chuẩn hóa dữ liệu từ MBW ATS → Mira Talent
    """

    # --- Mapping giới tính
    gender_map = {"Nam": "Male", "Nữ": "Female"}
    gender = gender_map.get(record.get("can_gender"), "Unknown")

    # --- Trạng thái CRM
    crm_status = "New" if not record.get("rejected") else "Dormant"

    # --- Kỹ năng (Candidate_Skill child table)
    skills = []
    if record.get("candidate_skill"):
        for skill in record["candidate_skill"]:
            name = skill.get("can_skill_name") or ""
            if name:
                skills.append(unquote(name))
    skills_text = ", ".join(skills)

    # --- Education (Candidate_Education)
    education_json = []
    if record.get("candidate_education"):
        for edu in record["candidate_education"]:
            education_json.append({
                "school": edu.get("school_name"),
                "degree": edu.get("degree"),
                "field_of_study": edu.get("major"),
                "start_date": edu.get("from_date"),
                "end_date": edu.get("to_date")
            })

    # --- Experience (Candidate_Work_Experience)
    experience_json = []
    if record.get("candidate_work_experience"):
        for exp in record["candidate_work_experience"]:
            experience_json.append({
                "company": exp.get("company_name"),
                "title": exp.get("job_title"),
                "start_date": exp.get("from_date"),
                "end_date": exp.get("to_date"),
                "description": exp.get("description")
            })

    # --- Certifications
    certs_json = []
    if record.get("candidate_certification"):
        for cert in record["candidate_certification"]:
            certs_json.append({
                "name": cert.get("certificate_name"),
                "issuer": cert.get("issuer"),
                "date": cert.get("issued_date")
            })

    # --- Build data for Mira Talent
    return {
        "doctype": "Mira Talent",
        "full_name": record.get("can_full_name"),
        "gender": gender,
        "date_of_birth": record.get("can_dob"),
        "email": record.get("can_email"),
        "phone": record.get("can_phone"),
        "linkedin_profile": record.get("can_other_links"),
        "current_city": record.get("can_address"),
        "skills": skills_text,
        "source": source_name or record.get("candidatesource_id"),
        "education": json.dumps(education_json),
        "experience": json.dumps(experience_json),
        "certifications": json.dumps(certs_json),
        "latest_company": record.get("can_last_workplace"),
        "highest_education": None,
        "current_status": "Active",
        "notes": record.get("can_profile"),
        "resume": record.get("can_cv"),
        "recruiter_owner_id": record.get("can_recruiter"),
        "crm_status": crm_status,
        "availability_date": datetime.now().date(),
        "last_interaction_date": datetime.now().date(),
        "priority_level": "Medium",
        "internal_rating": "B",
        "sync_id": record.get("name"),
        "domain_expertise": "",
        "cultural_fit": "",
        "desired_role": "",
        "soft_skills": "",
        "hard_skills": "",
        "languages": "[]",
    }

# Đồng bộ Postion -> Segment
def sync_ats_positions_to_segments():
    """
    Synchronize positions from ATS to Mira Segments
    """
    # Get active ATS data sources
    data_sources = frappe.get_all(
        "Mira Data Source",
        filters={
            "source_type": "ATS",
            "is_active": 1,
            "status": "Active",
            "sync_direction": ["in", ["Pull", "Both"]]
        },
        fields=["name", "source_title", "source_name"]
    )

    if not data_sources:
        frappe.log_error("No active ATS data sources found", "ATS Sync: No Data Sources")
        return

    for data_source in data_sources:
        try:
            data_source_doc = frappe.get_doc("Mira Data Source", data_source.name)
            sync_data_source_positions(data_source_doc)
        except Exception as e:
            frappe.log_error(
                f"Failed to sync positions for data source {data_source.name}: {str(e)}",
                "ATS Sync Error"
            )

def sync_data_source_positions(data_source):
    """
    Sync positions for a specific ATS data source
    Args:
        data_source: Mira Data Source document object
    """
    # Create sync log
    sync_log = frappe.get_doc({
        "doctype": "Mira ATS Sync Log",
        "connection": data_source.name,
        "sync_type": "Position to Segment",
        "status": "In Progress",
        "start_time": frappe.utils.now(),
        "details": f"Starting sync from {data_source.source_title} ({data_source.source_name})"
    })
    sync_log.insert(ignore_permissions=True)
    frappe.db.commit()

    total_records = 0
    try:
        with FrappeSiteProvider(data_source.name) as provider:
            if provider.sync_direction not in ("Pull", "Both"):
                sync_log.status = "Failed"
                sync_log.details = "Sync direction not set to Pull or Both"
                sync_log.save()
                return

            # Fetch positions from ATS
            positions = provider.get_list(
                "ATS_Position",
                filters={"cat_status": "Active"},
                fields=["name", "position_name", "position_description", "required_skills"]
            )

            total_records = len(positions)
            success_count = 0
            failed_count = 0
            error_log = []

            for position in positions:
                try:
                    # Check if segment already exists
                    position_id = position.get("name")
                    segment_name = f"ATS-{position_id}"
                    segment = frappe.db.get_value(
                        "Mira Segment",
                        {"sync_id": position_id, "type": "DYNAMIC"},
                        "name"
                    )

                    # Prepare segment data
                    # Parse HTML description to plain text
                    description_html = position.get("position_description") or ""
                    description_text = parse_html_to_text(description_html)
                    
                    # Extract skills and convert to criteria format
                    skills = extract_skills(position.get("required_skills")) if position.get("required_skills") else []
                    criteria = build_criteria_from_skills(skills)
                    
                    segment_data = {
                        "doctype": "Mira Segment",
                        "title": position.get("position_name"),
                        "description": description_text,
                        "type": "DYNAMIC",
                        "source": "SYNC_ATS",
                        "sync_id": position_id,  # Cần giữ để tránh duplicate và cho phép update
                        "criteria": json.dumps(criteria)
                    }

                    if segment:
                        # Update existing segment
                        segment_doc = frappe.get_doc("Mira Segment", segment)
                        segment_doc.update(segment_data)
                        segment_doc.save(ignore_permissions=True)
                        action = "updated"
                    else:
                        # Create new segment
                        segment_doc = frappe.get_doc(segment_data)
                        segment_doc.insert(ignore_permissions=True)
                        action = "created"

                    # Log success
                    success_count += 1
                    
                    # Commit after each successful segment to avoid conflicts
                    frappe.db.commit()

                except Exception as e:
                    failed_count += 1
                    error_log.append({
                        "position": position.get("name"),
                        "error": str(e)[:200]  # Limit error message length
                    })
                    
                    # Rollback failed transaction
                    frappe.db.rollback()

            # Update sync log
            sync_log.reload()  # Reload to avoid concurrent modification
            sync_log.status = "Completed" if failed_count == 0 else "Partially Completed"
            sync_log.total_records = total_records
            sync_log.success_count = success_count
            sync_log.failed_count = failed_count
            sync_log.error_log = json.dumps(error_log, indent=2)
            sync_log.end_time = frappe.utils.now()
            sync_log.details = f"Sync completed. Success: {success_count}, Failed: {failed_count}"
            sync_log.save(ignore_permissions=True)

    except Exception as e:
        try:
            sync_log.reload()  # Reload to avoid concurrent modification
            sync_log.status = "Failed"
            sync_log.total_records = total_records
            sync_log.error_log = str(e)[:500]  # Limit error log length
            sync_log.end_time = frappe.utils.now()
            sync_log.details = f"Sync failed: {str(e)[:200]}"
            sync_log.save(ignore_permissions=True)
        except Exception as save_error:
            # If save fails, just log it
            pass
        
        # Shorten error title to avoid exceeding 140 chars
        error_title = f"ATS Sync Error: {data_source.name[:30]}"
        error_message = f"Failed to sync positions for {data_source.name}\n\nError: {str(e)}"
        frappe.log_error(error_message, error_title)
    finally:
        frappe.db.commit()

def parse_html_to_text(html_content):
    """
    Parse HTML content to plain text
    
    Args:
        html_content: HTML string
        
    Returns:
        Plain text string
    """
    if not html_content:
        return ""
    
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean up
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up extra whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        text = '\n'.join(lines)
        
        return text
    except Exception as e:
        # If parsing fails, return original content
        return html_content

def extract_skills(html_content):
    """
    Extract skills from HTML content
    
    Args:
        html_content: HTML string containing skills
        
    Returns:
        List of skill strings
    """
    if not html_content:
        return []
    
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(separator=',', strip=True)
        
        # Split by common delimiters and clean up
        skills = []
        for part in text.split(','):
            part = part.strip()
            if part and len(part) < 50:  # Simple validation to avoid long strings
                skills.append(part)
        
        return skills
    except Exception as e:
        return []

def build_criteria_from_skills(skills):
    """
    Build criteria filter format from skills list
    
    Args:
        skills: List of skill strings
        
    Returns:
        List of filter criteria in format [["field", "operator", "value"]]
    """
    if not skills:
        return []
    
    # Return simple criteria format without "or"
    # If multiple skills, only use the first one
    # Format: [["skills", "==", "skill"]]
    first_skill = skills[0] if skills else ""
    return [["skills", "==", first_skill]]

def sync_ats_candidates_to_talents():
    """
    Synchronize candidates from all active ATS Data Sources to Mira Talents
    """
    # Get active ATS data sources
    data_sources = frappe.get_all(
        "Mira Data Source",
        filters={
            "source_type": "ATS",
            "is_active": 1,
            "status": "Active",
            "sync_direction": ["in", ["Pull", "Both"]]
        },
        fields=["name", "source_title", "source_name"]
    )

    if not data_sources:
        frappe.log_error("No active ATS data sources found for candidate sync", "ATS Candidate Sync: No Data Sources")
        return

    for data_source in data_sources:
        try:
            data_source_doc = frappe.get_doc("Mira Data Source", data_source.name)
            sync_data_source_candidates(data_source_doc)
        except Exception as e:
            frappe.log_error(
                f"Failed to sync candidates for data source {data_source.name}: {str(e)}",
                "ATS Candidate Sync Error"
            )

def sync_data_source_candidates(data_source):
    """
    Sync candidates for a specific ATS data source to Mira Talents
    
    Args:
        data_source: Mira Data Source document object
    """
    # Create sync log
    sync_log = frappe.get_doc({
        "doctype": "Mira ATS Sync Log",
        "connection": data_source.name,
        "sync_type": "Candidate to Talent",  # Tạo sync type mới
        "status": "In Progress",
        "start_time": frappe.utils.now(),
        "details": f"Starting candidate sync from {data_source.source_title} ({data_source.source_name})"
    })
    sync_log.insert(ignore_permissions=True)
    frappe.db.commit()

    try:
        with FrappeSiteProvider(data_source.name) as provider:
            if provider.sync_direction not in ("Pull", "Both"):
                sync_log.status = "Failed"
                sync_log.details = "Sync direction not set to Pull or Both"
                sync_log.save(ignore_permissions=True)
                return

            # Fetch candidates from ATS
            # Bạn có thể thêm filters nếu cần
            candidates = provider.get_list(
                "ATS_Candidate",
                filters={},  # Có thể thêm filters như {"rejected": 0}
                fields=["name"]  # Chỉ lấy name, chi tiết sẽ lấy trong loop
            )

            sync_log.total_records = len(candidates)
            sync_log.save(ignore_permissions=True)
            frappe.db.commit()
            
            success_count = 0
            failed_count = 0
            error_log = []

            for candidate in candidates:
                try:
                    # Lấy chi tiết candidate
                    candidate_doc = provider.get_doc("ATS_Candidate", candidate.get('name'))
                    
                    # Sử dụng hàm mapping có sẵn
                    talent_data = map_mbw_ats_to_talentprofiles(
                        candidate_doc, 
                        campaign_name=None,  # Không dùng campaign
                        source_name="MBW ATS",
                        segment_id=None
                    )
                    
                    # Kiểm tra talent đã tồn tại
                    existing = None
                    if talent_data.get("email"):
                        existing = frappe.db.exists("Mira Talent", {"email": talent_data["email"]})
                    
                    if not existing and candidate_doc.get("name"):
                        existing = frappe.db.exists("Mira Talent", {"sync_id": candidate_doc.get("name")})

                    if existing:
                        # Update existing talent
                        talent = frappe.get_doc("Mira Talent", existing)
                        talent.update(talent_data)
                        talent.save(ignore_permissions=True)
                        action = "updated"
                    else:
                        # Create new talent
                        talent = frappe.get_doc(talent_data)
                        talent.insert(ignore_permissions=True)
                        action = "created"

                    success_count += 1
                    
                    # Commit sau mỗi talent thành công
                    frappe.db.commit()

                except Exception as e:
                    failed_count += 1
                    error_log.append({
                        "candidate": candidate.get("name"),
                        "error": str(e)[:200]
                    })
                    
                    # Rollback failed transaction
                    frappe.db.rollback()

            # Update sync log
            sync_log.reload()
            sync_log.status = "Completed" if failed_count == 0 else "Partially Completed"
            sync_log.success_count = success_count
            sync_log.failed_count = failed_count
            sync_log.error_log = json.dumps(error_log, indent=2)
            sync_log.end_time = frappe.utils.now()
            sync_log.details = f"Candidate sync completed. Success: {success_count}, Failed: {failed_count}"
            sync_log.save(ignore_permissions=True)

    except Exception as e:
        try:
            sync_log.reload()
            sync_log.status = "Failed"
            sync_log.error_log = str(e)[:500]
            sync_log.end_time = frappe.utils.now()
            sync_log.details = f"Candidate sync failed: {str(e)[:200]}"
            sync_log.save(ignore_permissions=True)
        except Exception as save_error:
            pass
        
        # Log error với title ngắn
        error_title = f"ATS Candidate Sync: {data_source.name[:30]}"
        error_message = f"Failed to sync candidates for {data_source.name}\n\nError: {str(e)}"
        frappe.log_error(error_message, error_title)
    finally:
        frappe.db.commit()

def schedule_sync():
    """
    Schedule this function to run periodically
    """
    sync_ats_positions_to_segments()
    sync_ats_candidates_to_talents()

def build_frappe_filters_from_conditions(filter_obj):
    """
    Convert frontend filter object to Frappe filters format
    
    Args:
        filter_obj: {
            'conditions': [...],
            'logic': 'AND'
        }
    
    Returns:
        list: Frappe filters as list of lists [[field, operator, value], ...]
    """
    if not filter_obj or not filter_obj.get('conditions'):
        return None
    
    # Use list format for Frappe get_all
    frappe_filters = []
    
    def process_conditions(conditions, parent_logic='AND'):
        """Recursively process conditions"""
        result = []
        
        for condition in conditions:
            if condition['type'] == 'condition':
                field = condition['field']
                operator = condition['operator']
                value = condition['value']
                
                # Map operators to Frappe format
                if operator == '==':
                    result.append([field, '=', value])
                elif operator == '!=':
                    result.append([field, '!=', value])
                elif operator == 'in':
                    # value is already an array from frontend
                    result.append([field, 'in', value])
                elif operator == 'not in':
                    result.append([field, 'not in', value])
                elif operator == 'like':
                    result.append([field, 'like', f'%{value}%'])
                elif operator == 'not like':
                    result.append([field, 'not like', f'%{value}%'])
                elif operator in ['>', '<', '>=', '<=']:
                    result.append([field, operator, value])
                    
            elif condition['type'] == 'group':
                # Process nested group
                nested = process_conditions(condition['conditions'], condition.get('logic', 'AND'))
                if nested:
                    # For OR logic within group, wrap in another list
                    if condition.get('logic') == 'OR':
                        result.append(nested)
                    else:
                        result.extend(nested)
        
        return result
    
    frappe_filters = process_conditions(filter_obj['conditions'])
    
    return frappe_filters if frappe_filters else None

def sync_data_source_candidates_background(data_source_name, sync_log_name, filters=None):
    """
    Background version of sync_data_source_candidates that works with existing sync log
    
    Args:
        data_source_name: Name of Mira Data Source document
        sync_log_name: Name of existing Mira ATS Sync Log document
        filters: Filter object from frontend {conditions: [...], logic: 'AND'}
    """
    try:
        # Get existing sync log
        sync_log = frappe.get_doc("Mira ATS Sync Log", sync_log_name)
        
        # Check if sync was cancelled
        if sync_log.status == "Cancelled":
            return
        
        # Update status to In Progress and set start time
        sync_log.status = "In Progress"
        sync_log.start_time = frappe.utils.now()
        sync_log.save(ignore_permissions=True)
        frappe.db.commit()
        
        # Get data source document
        data_source = frappe.get_doc("Mira Data Source", data_source_name)
        
        with FrappeSiteProvider(data_source.name) as provider:
            if provider.sync_direction not in ("Pull", "Both"):
                sync_log.status = "Failed"
                sync_log.details = "Sync direction not set to Pull or Both"
                sync_log.end_time = frappe.utils.now()
                sync_log.save(ignore_permissions=True)
                frappe.db.commit()
                return

            # Build Frappe filters from filter object
            frappe_filters = None
            if filters:
                try:
                    frappe.logger().info(f"Raw filters received: {json.dumps(filters)}")
                    frappe_filters = build_frappe_filters_from_conditions(filters)
                    if frappe_filters:
                        frappe.logger().info(f"Built Frappe filters: {json.dumps(frappe_filters)}")
                    else:
                        frappe.logger().warning("No filters built from conditions")
                except Exception as e:
                    frappe.logger().error(f"Error building filters: {str(e)}")
                    import traceback
                    frappe.logger().error(traceback.format_exc())
                    frappe_filters = None
            
            # Separate filters into direct fields and child table fields
            direct_filters = []
            child_table_filters = {}
            
            if frappe_filters:
                # Map of special filter fields that need post-processing
                special_filter_fields = {
                    'skills': 'candidate_skill',  # Child table field
                    'tags': 'candidate_tags',  # Child table field
                    'minimum_required_fields': 'required_fields_check'  # Special validation filter
                }
                
                for filter_item in frappe_filters:
                    field_name = filter_item[0] if isinstance(filter_item, list) else None
                    
                    # Check if this is a special filter field that needs post-processing
                    if field_name in special_filter_fields:
                        child_table_filters[field_name] = filter_item
                        frappe.logger().info(f"Special filter detected: {filter_item} - will apply post-fetch")
                    else:
                        direct_filters.append(filter_item)
            
            # Fetch candidates from ATS with direct filters only
            try:
                if direct_filters:
                    frappe.logger().info(f"Fetching candidates with direct filters: {direct_filters}")
                    candidates = provider.get_list(
                        "ATS_Candidate",
                        filters=direct_filters,
                        fields=["name"]
                    )
                    frappe.logger().info(f"Found {len(candidates)} candidates with direct filters")
                else:
                    # No direct filters - fetch all
                    frappe.logger().info("Fetching all candidates (no direct filters)")
                    candidates = provider.get_list(
                        "ATS_Candidate",
                        fields=["name"]
                    )
                    frappe.logger().info(f"Found {len(candidates)} total candidates")
            except Exception as e:
                frappe.logger().error(f"Error fetching candidates: {str(e)}")
                import traceback
                frappe.logger().error(traceback.format_exc())
                # Fallback: fetch all candidates without filters
                frappe.logger().info("Falling back to fetch all candidates")
                candidates = provider.get_list(
                    "ATS_Candidate",
                    fields=["name"]
                )
            
            # Apply child table filters post-fetch if any
            if child_table_filters and candidates:
                frappe.logger().info(f"Applying post-fetch child table filters to {len(candidates)} candidates")
                filtered_candidates = []
                
                for candidate in candidates:
                    try:
                        # Get full candidate doc to check child tables
                        candidate_doc = provider.get_doc("ATS_Candidate", candidate.get('name'))
                        
                        # Debug: Log candidate structure
                        frappe.logger().info(f"Checking candidate {candidate.get('name')}")
                        if 'candidate_skill' in candidate_doc:
                            frappe.logger().info(f"  candidate_skill: {candidate_doc.get('candidate_skill')}")
                        
                        # Check each special filter
                        matches = True
                        for field_name, filter_item in child_table_filters.items():
                            operator = filter_item[1]
                            value = filter_item[2]
                            
                            if field_name == 'minimum_required_fields':
                                # Special filter: Check if required fields are not empty
                                # Map display names to actual field names in ATS_Candidate
                                field_mapping = {
                                    'Full Name': 'can_full_name',
                                    'Email': 'can_email',
                                    'Phone': 'can_phone',
                                    'Phone Number': 'can_phone',
                                    'Source': 'candidatesource_id',
                                    'Gender': 'can_gender',
                                    'Date of Birth': 'can_dob',
                                    'DOB': 'can_dob',
                                    'Address': 'can_address',
                                    'Region': 'can_region',
                                    'Job Opening': 'job_opening_id',
                                    'Status': 'status',
                                    'Recruiter': 'can_recruiter',
                                    'CV': 'can_cv'
                                }
                                
                                required_fields = value if isinstance(value, list) else [value]
                                frappe.logger().info(f"  Checking required fields: {required_fields}")
                                
                                # Check if all required fields have values
                                for display_name in required_fields:
                                    actual_field = field_mapping.get(display_name, display_name.lower().replace(' ', '_'))
                                    field_value = candidate_doc.get(actual_field)
                                    
                                    # Check if field is empty
                                    is_empty = (
                                        field_value is None or 
                                        field_value == '' or 
                                        (isinstance(field_value, str) and field_value.strip() == '')
                                    )
                                    
                                    if is_empty:
                                        frappe.logger().info(f"  Required field '{display_name}' ({actual_field}) is empty")
                                        matches = False
                                        break
                                    else:
                                        frappe.logger().info(f"  Required field '{display_name}' ({actual_field}) = '{field_value}' ✓")
                                
                                if not matches:
                                    break
                            
                            elif field_name == 'skills':
                                # Check candidate_skill child table
                                skill_data = candidate_doc.get('candidate_skill', [])
                                frappe.logger().info(f"  Skill data type: {type(skill_data)}, length: {len(skill_data) if isinstance(skill_data, list) else 'N/A'}")
                                
                                if skill_data:
                                    # Extract skills from candidate_skill child table
                                    candidate_skills = []
                                    for skill in skill_data:
                                        frappe.logger().info(f"  Skill item: {skill}")
                                        # Field name is 'can_skill_name' based on Candidate_Skill DocType
                                        skill_name = skill.get('can_skill_name', '')
                                        if skill_name:
                                            # Normalize: lowercase and strip whitespace
                                            candidate_skills.append(skill_name.strip().lower())
                                    
                                    frappe.logger().info(f"  Extracted skills: {candidate_skills}")
                                    
                                    if operator == '=':
                                        # Check if any skill matches (case-insensitive)
                                        search_value = value.strip().lower()
                                        if search_value not in candidate_skills:
                                            frappe.logger().info(f"  No match for '{search_value}' in {candidate_skills}")
                                            matches = False
                                            break
                                    elif operator == 'in':
                                        # Check if any of the values match (case-insensitive)
                                        if isinstance(value, list):
                                            search_values = [v.strip().lower() for v in value]
                                        else:
                                            search_values = [value.strip().lower()]
                                        
                                        if not any(sv in candidate_skills for sv in search_values):
                                            frappe.logger().info(f"  No match for {search_values} in {candidate_skills}")
                                            matches = False
                                            break
                                else:
                                    # No skills data - doesn't match
                                    frappe.logger().info(f"  No skill data - skipping")
                                    matches = False
                                    break
                        
                        if matches:
                            frappe.logger().info(f"  ✓ Candidate {candidate.get('name')} matches filters")
                            filtered_candidates.append(candidate)
                        else:
                            frappe.logger().info(f"  ✗ Candidate {candidate.get('name')} does not match filters")
                            
                    except Exception as e:
                        frappe.logger().error(f"Error filtering candidate {candidate.get('name')}: {str(e)}")
                        continue
                
                frappe.logger().info(f"After post-fetch filtering: {len(filtered_candidates)} candidates match")
                candidates = filtered_candidates

            # Update total records
            sync_log.total_records = len(candidates)
            sync_log.save(ignore_permissions=True)
            frappe.db.commit()
            
            success_count = 0
            failed_count = 0
            skipped_count = 0
            error_log = []

            for i, candidate in enumerate(candidates):
                try:
                    # Check if sync was cancelled during processing
                    sync_log.reload()
                    if sync_log.status == "Cancelled":
                        sync_log.details = f"Sync cancelled after processing {success_count} records"
                        sync_log.save(ignore_permissions=True)
                        frappe.db.commit()
                        return
                    
                    # Lấy chi tiết candidate
                    candidate_doc = provider.get_doc("ATS_Candidate", candidate.get('name'))
                    
                    # Sử dụng hàm mapping có sẵn
                    talent_data = map_mbw_ats_to_talentprofiles(
                        candidate_doc, 
                        campaign_name=None,  # Không dùng campaign
                        source_name="MBW ATS",
                        segment_id=None
                    )
                    
                    # Kiểm tra duplicate email - SKIP nếu email đã tồn tại
                    if talent_data.get("email"):
                        existing_by_email = frappe.db.exists("Mira Talent", {"email": talent_data["email"]})
                        if existing_by_email:
                            # Skip duplicate email - không tạo/update
                            skipped_count += 1
                            error_log.append({
                                "candidate": candidate.get("name"),
                                "email": talent_data.get("email"),
                                "reason": "Duplicate email - skipped"
                            })
                            
                            # Publish realtime update for skipped record
                            try:
                                frappe.publish_realtime(
                                    event='candidate_sync_progress',
                                    message={
                                        'sync_log_name': sync_log_name,
                                        'sync_type': 'Candidate to Talent',
                                        'status': 'In Progress',
                                        'success_count': success_count,
                                        'failed_count': failed_count,
                                        'skipped_count': skipped_count,
                                        'total_records': len(candidates),
                                        'current_record': i + 1,
                                        'error': f"Duplicate email: {talent_data.get('email')}",
                                        'details': f"Processing {success_count + failed_count + skipped_count}/{len(candidates)}"
                                    }
                                )
                            except Exception as socket_error:
                                pass
                            
                            continue  # Skip to next candidate
                    
                    # Kiểm tra theo sync_id (nếu không có email hoặc email không trùng)
                    existing_by_sync_id = None
                    if candidate_doc.get("name"):
                        existing_by_sync_id = frappe.db.exists("Mira Talent", {"sync_id": candidate_doc.get("name")})
                    
                    if existing_by_sync_id:
                        # Update existing talent by sync_id
                        talent = frappe.get_doc("Mira Talent", existing_by_sync_id)
                        talent.update(talent_data)
                        talent.save(ignore_permissions=True)
                        action = "updated"
                    else:
                        # Create new talent
                        talent = frappe.get_doc(talent_data)
                        talent.insert(ignore_permissions=True)
                        action = "created"

                    success_count += 1
                    
                    # Commit sau mỗi talent thành công
                    frappe.db.commit()
                    
                    # Publish realtime update after each successful record
                    try:
                        frappe.publish_realtime(
                            event='candidate_sync_progress',
                            message={
                                'sync_log_name': sync_log_name,
                                'sync_type': 'Candidate to Talent',
                                'status': 'In Progress',
                                'success_count': success_count,
                                'failed_count': failed_count,
                                'skipped_count': skipped_count,
                                'total_records': len(candidates),
                                'current_record': i + 1,
                                'talent_name': talent.name,
                                'talent_full_name': talent.full_name,
                                'action': action,
                                'details': f"Processing {success_count + failed_count + skipped_count}/{len(candidates)}"
                            }
                        )
                    except Exception as socket_error:
                        # Don't fail the sync if socket emit fails
                        pass
                    
                    # Update sync log progress every 10 records
                    if (i + 1) % 10 == 0:
                        sync_log.reload()
                        sync_log.success_count = success_count
                        sync_log.failed_count = failed_count
                        sync_log.skipped_count = skipped_count
                        sync_log.details = f"Processing... {success_count + failed_count + skipped_count}/{len(candidates)} completed"
                        sync_log.save(ignore_permissions=True)
                        frappe.db.commit()

                except Exception as e:
                    failed_count += 1
                    error_log.append({
                        "candidate": candidate.get("name"),
                        "error": str(e)[:200]
                    })
                    
                    # Rollback failed transaction
                    frappe.db.rollback()
                    
                    # Publish realtime update for failed record
                    try:
                        frappe.publish_realtime(
                            event='candidate_sync_progress',
                            message={
                                'sync_log_name': sync_log_name,
                                'sync_type': 'Candidate to Talent',
                                'status': 'In Progress',
                                'success_count': success_count,
                                'failed_count': failed_count,
                                'skipped_count': skipped_count,
                                'total_records': len(candidates),
                                'current_record': i + 1,
                                'error': str(e)[:100],
                                'details': f"Processing {success_count + failed_count + skipped_count}/{len(candidates)}"
                            }
                        )
                    except Exception as socket_error:
                        pass

            # Final update sync log
            sync_log.reload()
            sync_log.status = "Completed" if (failed_count == 0 and skipped_count == 0) else "Partially Completed"
            sync_log.success_count = success_count
            sync_log.failed_count = failed_count
            sync_log.skipped_count = skipped_count
            sync_log.error_log = json.dumps(error_log, indent=2)
            sync_log.end_time = frappe.utils.now()
            sync_log.details = f"Candidate sync completed. Success: {success_count}, Failed: {failed_count}, Skipped (Duplicate): {skipped_count}"
            sync_log.save(ignore_permissions=True)
            
            # Emit socket event for real-time updates
            try:
                frappe.publish_realtime(
                    event='candidate_sync_complete',
                    message={
                        'sync_log_name': sync_log_name,
                        'sync_type': 'Candidate to Talent',
                        'status': sync_log.status,
                        'success_count': success_count,
                        'failed_count': failed_count,
                        'skipped_count': skipped_count,
                        'total_records': len(candidates),
                        'details': sync_log.details
                    }
                    # Broadcast to all users since background job doesn't have session context
                )
            except Exception as socket_error:
                # Don't fail the sync if socket emit fails
                frappe.log_error(f"Failed to emit socket event: {str(socket_error)}", "Socket Emit Error")

    except Exception as e:
        try:
            sync_log.reload()
            sync_log.status = "Failed"
            sync_log.error_log = str(e)[:500]
            sync_log.end_time = frappe.utils.now()
            sync_log.details = f"Candidate sync failed: {str(e)[:200]}"
            sync_log.save(ignore_permissions=True)
            
            # Emit socket event for failed sync
            try:
                frappe.publish_realtime(
                    event='candidate_sync_complete',
                    message={
                        'sync_log_name': sync_log_name,
                        'sync_type': 'Candidate to Talent',
                        'status': 'Failed',
                        'success_count': 0,
                        'failed_count': 0,
                        'total_records': 0,
                        'details': sync_log.details
                    }
                    # Broadcast to all users since background job doesn't have session context
                )
            except Exception as socket_error:
                # Don't fail the sync if socket emit fails
                frappe.log_error(f"Failed to emit socket event for failed sync: {str(socket_error)}", "Socket Emit Error")
        except Exception as save_error:
            pass
        
        # Log error với title ngắn
        error_title = f"ATS Candidate Sync BG: {data_source_name[:25]}"
        error_message = f"Background sync failed for {data_source_name}\n\nError: {str(e)}"
        frappe.log_error(error_message, error_title)
    finally:
        frappe.db.commit()

def sync_data_source_positions_background(data_source_name, sync_log_name):
    """
    Background version of sync_data_source_positions that works with existing sync log
    
    Args:
        data_source_name: Name of Mira Data Source document
        sync_log_name: Name of existing Mira ATS Sync Log document
    """
    try:
        # Get existing sync log
        sync_log = frappe.get_doc("Mira ATS Sync Log", sync_log_name)
        
        # Check if sync was cancelled
        if sync_log.status == "Cancelled":
            return
        
        # Update status to In Progress and set start time
        sync_log.status = "In Progress"
        sync_log.start_time = frappe.utils.now()
        sync_log.save(ignore_permissions=True)
        frappe.db.commit()
        
        # Get data source document
        data_source = frappe.get_doc("Mira Data Source", data_source_name)
        
        with FrappeSiteProvider(data_source.name) as provider:
            if provider.sync_direction not in ("Pull", "Both"):
                sync_log.status = "Failed"
                sync_log.details = "Sync direction not set to Pull or Both"
                sync_log.end_time = frappe.utils.now()
                sync_log.save(ignore_permissions=True)
                frappe.db.commit()
                return

            # Fetch positions from ATS
            positions = provider.get_list(
                "ATS_Position",
                filters={"cat_status": "Active"},
                fields=["name", "position_name", "position_description", "required_skills"]
            )

            # Update total records
            sync_log.total_records = len(positions)
            sync_log.save(ignore_permissions=True)
            frappe.db.commit()
            
            success_count = 0
            failed_count = 0
            skipped_count = 0
            error_log = []

            for i, position in enumerate(positions):
                try:
                    # Check if sync was cancelled during processing
                    sync_log.reload()
                    if sync_log.status == "Cancelled":
                        sync_log.details = f"Position sync cancelled after processing {success_count} records"
                        sync_log.save(ignore_permissions=True)
                        frappe.db.commit()
                        return
                    
                    # Check if segment already exists by sync_id
                    position_id = position.get("name")
                    position_title = position.get("position_name")
                    
                    existing_segment = frappe.db.get_value(
                        "Mira Segment",
                        {"sync_id": position_id, "type": "DYNAMIC"},
                        "name"
                    )
                    
                    # Check duplicate by title (similar to email check for talents)
                    if not existing_segment and position_title:
                        duplicate_by_title = frappe.db.exists(
                            "Mira Segment",
                            {"title": position_title, "type": "DYNAMIC"}
                        )
                        if duplicate_by_title:
                            # Skip duplicate title - không tạo/update
                            skipped_count += 1
                            error_log.append({
                                "position": position_id,
                                "title": position_title,
                                "reason": "Duplicate title - skipped"
                            })
                            
                            # Publish realtime update for skipped record
                            try:
                                frappe.publish_realtime(
                                    event='position_sync_progress',
                                    message={
                                        'sync_log_name': sync_log_name,
                                        'sync_type': 'Position to Segment',
                                        'status': 'In Progress',
                                        'success_count': success_count,
                                        'failed_count': failed_count,
                                        'skipped_count': skipped_count,
                                        'total_records': len(positions),
                                        'current_record': i + 1,
                                        'error': f"Duplicate title: {position_title}",
                                        'details': f"Processing {success_count + failed_count + skipped_count}/{len(positions)}"
                                    }
                                )
                            except Exception as socket_error:
                                pass
                            
                            continue  # Skip to next position

                    # Prepare segment data
                    # Parse HTML description to plain text
                    description_html = position.get("position_description") or ""
                    description_text = parse_html_to_text(description_html)
                    
                    # Extract skills and convert to criteria format
                    skills = extract_skills(position.get("required_skills")) if position.get("required_skills") else []
                    criteria = build_criteria_from_skills(skills)
                    
                    segment_data = {
                        "doctype": "Mira Segment",
                        "title": position_title,
                        "description": description_text,
                        "type": "DYNAMIC",
                        "source": "SYNC_ATS",
                        "sync_id": position_id,  # Keep to avoid duplicates and allow updates
                        "criteria": json.dumps(criteria)
                    }

                    if existing_segment:
                        # Update existing segment by sync_id
                        segment_doc = frappe.get_doc("Mira Segment", existing_segment)
                        segment_doc.update(segment_data)
                        segment_doc.save(ignore_permissions=True)
                        action = "updated"
                    else:
                        # Create new segment
                        segment_doc = frappe.get_doc(segment_data)
                        segment_doc.insert(ignore_permissions=True)
                        action = "created"

                    success_count += 1
                    
                    # Commit after each successful segment to avoid conflicts
                    frappe.db.commit()
                    
                    # Publish realtime update after each successful record
                    try:
                        frappe.publish_realtime(
                            event='position_sync_progress',
                            message={
                                'sync_log_name': sync_log_name,
                                'sync_type': 'Position to Segment',
                                'status': 'In Progress',
                                'success_count': success_count,
                                'failed_count': failed_count,
                                'skipped_count': skipped_count,
                                'total_records': len(positions),
                                'current_record': i + 1,
                                'segment_name': segment_doc.name,
                                'segment_title': segment_doc.title,
                                'action': action,
                                'details': f"Processing {success_count + failed_count + skipped_count}/{len(positions)}"
                            }
                        )
                    except Exception as socket_error:
                        # Don't fail the sync if socket emit fails
                        pass
                    
                    # Update progress every 5 records
                    if (i + 1) % 5 == 0:
                        sync_log.reload()
                        sync_log.success_count = success_count
                        sync_log.failed_count = failed_count
                        sync_log.skipped_count = skipped_count
                        sync_log.details = f"Processing... {success_count + failed_count + skipped_count}/{len(positions)} completed"
                        sync_log.save(ignore_permissions=True)
                        frappe.db.commit()

                except Exception as e:
                    failed_count += 1
                    error_log.append({
                        "position": position.get("name"),
                        "error": str(e)[:200]  # Limit error message length
                    })
                    
                    # Rollback failed transaction
                    frappe.db.rollback()
                    
                    # Publish realtime update for failed record
                    try:
                        frappe.publish_realtime(
                            event='position_sync_progress',
                            message={
                                'sync_log_name': sync_log_name,
                                'sync_type': 'Position to Segment',
                                'status': 'In Progress',
                                'success_count': success_count,
                                'failed_count': failed_count,
                                'skipped_count': skipped_count,
                                'total_records': len(positions),
                                'current_record': i + 1,
                                'error': str(e)[:100],
                                'details': f"Processing {success_count + failed_count + skipped_count}/{len(positions)}"
                            }
                        )
                    except Exception as socket_error:
                        pass

            # Final update sync log
            sync_log.reload()
            sync_log.status = "Completed" if (failed_count == 0 and skipped_count == 0) else "Partially Completed"
            sync_log.success_count = success_count
            sync_log.failed_count = failed_count
            sync_log.skipped_count = skipped_count
            sync_log.error_log = json.dumps(error_log, indent=2)
            sync_log.end_time = frappe.utils.now()
            sync_log.details = f"Position sync completed. Success: {success_count}, Failed: {failed_count}, Skipped (Duplicate): {skipped_count}"
            sync_log.save(ignore_permissions=True)
            
            # Emit socket event for real-time updates
            try:
                frappe.publish_realtime(
                    event='position_sync_complete',
                    message={
                        'sync_log_name': sync_log_name,
                        'sync_type': 'Position to Segment',
                        'status': sync_log.status,
                        'success_count': success_count,
                        'failed_count': failed_count,
                        'skipped_count': skipped_count,
                        'total_records': len(positions),
                        'details': sync_log.details
                    }
                    # Broadcast to all users since background job doesn't have session context
                )
            except Exception as socket_error:
                # Don't fail the sync if socket emit fails
                frappe.log_error(f"Failed to emit socket event: {str(socket_error)}", "Socket Emit Error")

    except Exception as e:
        try:
            sync_log.reload()
            sync_log.status = "Failed"
            sync_log.error_log = str(e)[:500]
            sync_log.end_time = frappe.utils.now()
            sync_log.details = f"Position sync failed: {str(e)[:200]}"
            sync_log.save(ignore_permissions=True)
            
            # Emit socket event for failed sync
            try:
                frappe.publish_realtime(
                    event='position_sync_complete',
                    message={
                        'sync_log_name': sync_log_name,
                        'sync_type': 'Position to Segment',
                        'status': 'Failed',
                        'success_count': 0,
                        'failed_count': 0,
                        'total_records': 0,
                        'details': sync_log.details
                    }
                    # Broadcast to all users since background job doesn't have session context
                )
            except Exception as socket_error:
                # Don't fail the sync if socket emit fails
                frappe.log_error(f"Failed to emit socket event for failed sync: {str(socket_error)}", "Socket Emit Error")
        except Exception as save_error:
            pass
        
        # Log error with short title
        error_title = f"ATS Position Sync BG: {data_source_name[:25]}"
        error_message = f"Background position sync failed for {data_source_name}\n\nError: {str(e)}"
        frappe.log_error(error_message, error_title)
    finally:
        frappe.db.commit()