import json
import frappe
from frappe.utils import now_datetime,add_days,add_to_date
from mbw_mira.api.external_connections import share_job_posting
from mbw_mira.utils import _normalize_condition

def attraction_campaign(campaign_id):
    """
    Worker: Chạy campaign thu hút
    Chiến dịch thu hút chỉ gửi qua kênh socaial
    """
    campaign = frappe.get_doc("Mira Campaign", campaign_id)
    now = now_datetime()
    before_60s = add_to_date(now, seconds=-60)
    after_60s = add_to_date(now, seconds=60)
    #Lấy Mira campaign social
    campaign_socials = frappe.get_all("Mira Campaign Social",filters={"campaign_id":campaign_id,"status":"Pending"},fields=["*"])
    if campaign_socials:
        for cps in campaign_socials:
            if cps and cps.external_connection:
                #Kiểm tra nếu social thì gọi share
                if cps.platform in  ['Facebook','Zalo', 'TopCV']:
                    if cps.post_schedule_time:#Kiểm tra thời gian post nếu cầu hình delay
                        if cps.post_schedule_time >=before_60s and cps.post_schedule_time <= after_60s:
                            share_job_posting(cps.external_connection,campaign_id,campaign.ladipage_url, cps.social_media_images,cps.template_content)
                            
                    else:
                        share_job_posting(cps.external_connection,campaign_id,campaign.ladipage_url, cps.social_media_images,cps.template_content)
                    
            else:
                continue

def nurture_campaign(campaign_id):
    """
    Worker: Chạy campaign nuôi dưỡng
    Chiến dịch nuôi dưỡng sẽ chỉ tiếp cận qua các kênh:Email, ZaloOA
    """
    campaign = frappe.get_doc("Mira Campaign", campaign_id)
    
    #Lấy Mira campaign social
    #Tạo talent campaign
    _enroll_talent_for_campaign(campaign)
    # campaign_socials = frappe.get_all("Mira Campaign Social",filters={"campaign_id":campaign_id,"status":"Pending"},fields=["*"])
    # if campaign_socials:
    #     for cps in campaign_socials:
    #         if cps and cps.external_connection:
    #             if cps.platform in  ['Zalo']:
    #                 share_job_posting(cps.external_connection,campaign_id,cps.template_content, campaign.ladipage_url, cps.social_media_images)
    #             else:
    #                 #Gửi email
    #                 pass
    #         else:
    #             continue



def recruitment_campaign(campaign_id):
    """
    Worker: Chạy campaign tuyển dụng
    Chiến dịch này chạy trên cả
    """
    now = now_datetime()
    before_60s = add_to_date(now, seconds=-60)
    after_60s = add_to_date(now, seconds=60)
    campaign = frappe.get_doc("Mira Campaign", campaign_id)

    #Chiến dịch này có kích hoạt gửi email
    _enroll_talent_for_campaign(campaign)
    
    #Lấy Mira campaign social
    campaign_socials = frappe.get_all("Mira Campaign Social",filters={"campaign_id":campaign_id,"status":"Pending"},fields=["*"])
    if campaign_socials:
        for cps in campaign_socials:
            if cps and cps.external_connection:
                #Kiểm tra nếu social thì gọi share
                if cps.platform in  ['Facebook','Zalo', 'TopCV']:
                    if cps.post_schedule_time:#Kiểm tra thời gian post nếu cầu hình delay
                        if cps.post_schedule_time >=before_60s and cps.post_schedule_time <= after_60s:
                            share_job_posting(cps.external_connection,campaign_id,campaign.ladipage_url, cps.social_media_images,cps.template_content)
                    else:
                        share_job_posting(cps.external_connection,campaign_id,campaign.ladipage_url, cps.social_media_images,cps.template_content)
            else:
                continue
                


def _enroll_talent_for_campaign(campaign):
    """
    Worker: tìm ứng viên từ Mira Talent theo campaign và tạo Mira Talent Campaign.
    """
    talent_profiles = get_combined_talent(campaign)
    
    if not talent_profiles:
        return
    
    # tìm bước đầu tiên trong CampaignStep (nếu có)
    first_step = _get_first_campaign_step(campaign)
    

    count = 0
    try:
        print("count",len(talent_profiles))
        if first_step and talent_profiles:
            for profile in talent_profiles:                
                _create_talent_campaign(campaign, profile, first_step)
                
                count += 1
        #frappe.publish_realtime('enroll_talent_campaign', message={'campaign': campaign})
        return count
    except Exception as e:
        frappe.log_error(frappe.get_traceback())
        return count


def get_combined_talent(campaign):
    try:
        if isinstance(campaign.condition_filter, str):
            conditions = json.loads(campaign.condition_filter) if campaign.condition_filter else []
        
        # Start with base filters
        filters = {}
        talent_ids = None
        
        # Step 1: Get talent IDs from segment if provided
        if campaign.target_pool:
            # Get talents from Mira Talent Pool by segment_id
            pool_records = frappe.get_all('Mira Talent Pool', 
                filters={'segment_id': campaign.target_pool},
                pluck='talent_id'
            )
            talent_ids = set(pool_records)
        
        # Step 2: Add condition filters
        # Conditions format: [["field", "operator", "value"], ...]
        if conditions and len(conditions) > 0:
            for condition in conditions:
                # Handle both list format and dict format
                if isinstance(condition, list) and len(condition) >= 3:
                    field = condition[0]
                    operator = condition[1]
                    value = condition[2]
                elif isinstance(condition, dict):
                    field = condition.get('field')
                    operator = condition.get('operator', '=')
                    value = condition.get('value')
                else:
                    continue
                
                if not field:
                    continue
                
                # Map operators to Frappe format
                # Special handling for comma-separated fields (skills, tags, etc.)
                if field in ['skills', 'tags', 'soft_skills'] and operator in ['=', '==']:
                    # Use LIKE for comma-separated fields
                    filters[field] = ['like', f'%{value}%']
                elif operator in ['=', '==']:
                    filters[field] = value
                elif operator in ['!=', '<>']:
                    filters[field] = ['!=', value]
                elif operator == 'in':
                    filters[field] = ['in', value]
                elif operator == 'not in':
                    filters[field] = ['not in', value]
                elif operator in ['like', 'LIKE']:
                    filters[field] = ['like', f'%{value}%']
                elif operator == '>':
                    filters[field] = ['>', value]
                elif operator == '<':
                    filters[field] = ['<', value]
                elif operator == '>=':
                    filters[field] = ['>=', value]
                elif operator == '<=':
                    filters[field] = ['<=', value]
                else:
                    filters[field] = value
        
        # Step 3: Combine segment IDs with condition filters
        if talent_ids is not None:
            # Filter by talent IDs from segment
            filters['name'] = ['in', list(talent_ids)]
        
        # Step 4: Count
        talents = frappe.db.get_list('Mira Talent', filters=filters,fields=["*"])
        
        return talents
    except Exception as e:
        print(str(e))
        return []


def _get_first_campaign_step(campaign):
    """
    Lấy bước đầu tiên (step_order nhỏ nhất) của CampaignStep
    """
    step = frappe.get_all(
        "Mira Campaign Social",
        filters={"campaign_id": campaign.name, "status":"Pending"},
        fields=["*"],
        order_by="post_schedule_time asc",
        limit=1,
    )
    
    return step[0] if step else None
    


def _create_talent_campaign(campaign, profile, first_step):
    """
    Tạo mới Mira Talent Campaign, chỉ set current_step_order nếu có
    """
    try:        
        if first_step.post_schedule_time:
            next_action_at = add_days(first_step.post_schedule_time, 0)
        else:
            next_action_at = campaign.start_date
        if not _check_exists(campaign.name,profile.name) and profile.name:
            doc = frappe.get_doc(
                {
                    "doctype": "Mira Talent Campaign",
                    "campaign_id": campaign.name,
                    "talent_id": profile.name,
                    "campaign_social":first_step.name,
                    "status": "ACTIVE",
                    "enrolled_at": now_datetime(),
                    "current_step_order": 1,
                    "next_action_at": next_action_at,
                }
            )
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            return doc.name
        else:
            return None
    except Exception as e:
        frappe.log_error(f"talent_profiles {e}")
        return None

def _check_exists(campaign_id,talent_id):
    talent_campaign_exists = frappe.db.exists("Mira Talent Campaign",{"campaign_id":campaign_id,"talent_id":talent_id})
    if talent_campaign_exists:
        return True
    else:
        return False