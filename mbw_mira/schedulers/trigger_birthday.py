"""
Birthday Scheduler - Tự động gửi email chúc mừng sinh nhật cho ứng viên từ talent pools
"""

import frappe
from frappe.utils import nowdate, now_datetime, getdate
import time
import json
from mbw_mira.utils.email import send_email
from mbw_mira.utils.birthday_utils import check_birthday

def get_birthday_email_template():
    """Tạo template email chúc mừng sinh nhật đẹp"""
    return {
        "subject": "🎂 Chúc mừng sinh nhật!",
        "content": """
<html>
<head>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .card { background: white; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); overflow: hidden; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 20px; text-align: center; }
        .header h1 { margin: 0; font-size: 32px; font-weight: 700; }
        .header p { margin: 10px 0 0 0; font-size: 16px; opacity: 0.9; }
        .content { padding: 40px; text-align: center; }
        .emoji { font-size: 60px; margin-bottom: 20px; }
        .greeting { font-size: 24px; color: #333; font-weight: 600; margin-bottom: 15px; }
        .message { font-size: 16px; color: #666; line-height: 1.6; margin: 20px 0; }
        .footer { background: #f5f5f5; padding: 20px; text-align: center; font-size: 12px; color: #999; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="header">
                <div class="emoji">🎂🎉🎊</div>
                <h1>Chúc mừng sinh nhật</h1>
                <p>Một ngày đặc biệt dành cho bạn</p>
            </div>
            <div class="content">
                <p class="greeting">Xin chào {talent_name},</p>
                <div class="message">
                    <p>Hôm nay là ngày đặc biệt của bạn! 🎈</p>
                    <p>Chúng tôi xin gửi lời chúc mừng sinh nhật chân thành nhất. Hy vọng ngày này sẽ mang đến cho bạn những khoảnh khắc tuyệt vời, những tràng cười vui vẻ và những điều kỳ diệu.</p>
                    <p>Cảm ơn bạn vì đã là một phần của chúng tôi. Chúng tôi trân trọng sự hợp tác và tin tưởng của bạn.</p>
                    <p>Chúc bạn một năm mới tràn đầy sức khỏe, hạnh phúc và thành công! 🌟</p>
                </div>
            </div>
            <div class="footer">
                <p>© 2025 MOBIWORK. All rights reserved.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""
    }

def run_trigger_birhday():
    """
    Wrapper function cho scheduler - đảm bảo có đủ context và permissions
    """
    try:
        # Chạy birthday check
        result = run_daily_birthday_check(migration_run=False)
        return result

    except Exception as e:
        frappe.logger("birthday_scheduler").error(f"Scheduler failed: {str(e)}")
        frappe.log_error(f"Birthday scheduler error: {str(e)}", "Birthday Scheduler")
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def run_daily_birthday_check(migration_run=False):
    """
    Chạy kiểm tra sinh nhật hàng ngày và gửi email tự động
    
    Logic:
    1. Tìm các chiến dịch có status = ACTIVE
    2. Kiểm tra chiến dịch có trigger ON_BIRTHDAY không
    3. Nếu đủ điều kiện, quét pool trong chiến dịch
    4. Gửi email cho ứng viên có sinh nhật hôm nay

    Args:
        migration_run (bool): True nếu đây là migration run
    """
    start_time = time.time()
    logger = frappe.logger("birthday_scheduler")

    total_checked = 0
    birthday_found = 0
    emails_sent = 0
    emails_failed = 0
    campaigns_processed = 0
    error_message = None
    log_name = None

    try:
        logger.info("🎂 Starting daily birthday check...")
        print("\n" + "="*80)
        print("🎂 DAILY BIRTHDAY CHECK - START")
        print("="*80)
        print(f"Date: {nowdate()}")
        print(f"Migration Run: {migration_run}")
        print(f"Current User: {frappe.session.user}")
        print("="*80)

        # Bước 1: Tìm các Flow ACTIVE có trigger ON_BIRTHDAY, sau đó lấy Campaign NURTURING
        active_campaigns = frappe.db.sql("""
            SELECT DISTINCT c.name, c.campaign_name, c.target_pool, c.type, 
                   f.name as flow_name, f.title as flow_title
            FROM `tabMira Flow` f
            INNER JOIN `tabMira Flow Trigger` ft ON ft.parent = f.name
            INNER JOIN `tabMira Campaign` c ON c.name = f.campaign_id
            WHERE f.status = 'Active'
            AND ft.trigger_type = 'ON_BIRTHDAY'
            AND c.status = 'ACTIVE'
            AND c.type = 'NURTURING'
        """, as_dict=True)
        
        campaigns_processed = len(active_campaigns)
        logger.info(f"📊 Found {campaigns_processed} NURTURING campaigns with ON_BIRTHDAY trigger")
        print(f"📊 Active NURTURING campaigns with ON_BIRTHDAY trigger: {campaigns_processed}")
        
        if not active_campaigns:
            print("⚠️ WARNING: No active NURTURING campaigns with ON_BIRTHDAY trigger found!")
            logger.warning("No active NURTURING campaigns with ON_BIRTHDAY trigger")
            
            # DEBUG: Kiểm tra tất cả Flows trong hệ thống
            print("\n" + "="*80)
            print("🔍 DEBUG - Checking ALL Flows in system")
            print("="*80)
            
            all_flows = frappe.db.sql("""
                SELECT f.name, f.title, f.status, f.campaign_id, f.type,
                       c.campaign_name, c.type as campaign_type, c.status as campaign_status
                FROM `tabMira Flow` f
                LEFT JOIN `tabMira Campaign` c ON c.name = f.campaign_id
            """, as_dict=True)
            
            print(f"📋 Total flows in system: {len(all_flows)}")
            
            flows_with_birthday_trigger = []
            for flow in all_flows:
                # Check if flow has ON_BIRTHDAY trigger
                triggers = frappe.db.sql("""
                    SELECT trigger_type, status
                    FROM `tabMira Flow Trigger`
                    WHERE parent = %s
                """, (flow.get('name'),), as_dict=True)
                
                has_birthday_trigger = any(t.get('trigger_type') == 'ON_BIRTHDAY' for t in triggers)
                
                if has_birthday_trigger:
                    flows_with_birthday_trigger.append(flow)
                    
                    # Get full campaign details
                    campaign_details = None
                    if flow.get('campaign_id'):
                        campaign_details = frappe.db.get_value('Mira Campaign', 
                            flow.get('campaign_id'), 
                            ['is_active', 'target_pool'], 
                            as_dict=True)
                    
                    print(f"\n🎂 Flow with ON_BIRTHDAY trigger:")
                    print(f"   Flow: {flow.get('title')} ({flow.get('name')})")
                    print(f"   Flow Status: {flow.get('status')}")
                    print(f"   Campaign: {flow.get('campaign_name')} ({flow.get('campaign_id')})")
                    print(f"   Campaign Type: {flow.get('campaign_type')}")
                    print(f"   Campaign Status: {flow.get('campaign_status')}")
                    if campaign_details:
                        print(f"   Campaign is_active: {campaign_details.get('is_active')}")
                        print(f"   Campaign target_pool: {campaign_details.get('target_pool')}")
                    print(f"   Triggers:")
                    for t in triggers:
                        print(f"      - {t.get('trigger_type')} (Status: {t.get('status')})")
                    
                    # Check why not selected
                    reasons = []
                    if flow.get('status') != 'Active':
                        reasons.append(f"Flow status is '{flow.get('status')}' (need 'Active')")
                    if flow.get('campaign_type') != 'NURTURING':
                        reasons.append(f"Campaign type is '{flow.get('campaign_type')}' (need 'NURTURING')")
                    if flow.get('campaign_status') != 'ACTIVE':
                        reasons.append(f"Campaign status is '{flow.get('campaign_status')}' (need 'ACTIVE')")
                    if campaign_details and not campaign_details.get('is_active'):
                        reasons.append(f"Campaign is_active is {campaign_details.get('is_active')} (need 1)")
                    
                    trigger_active = any(t.get('trigger_type') == 'ON_BIRTHDAY' and t.get('status') == 'ACTIVE' for t in triggers)
                    if not trigger_active:
                        reasons.append("No ON_BIRTHDAY trigger with status='ACTIVE'")
                    
                    if reasons:
                        print(f"   ❌ NOT SELECTED - Reasons:")
                        for reason in reasons:
                            print(f"      • {reason}")
                    else:
                        print(f"   ✅ SHOULD BE SELECTED - All conditions met!")
            
            if not flows_with_birthday_trigger:
                print("\n⚠️ No flows with ON_BIRTHDAY trigger found in system!")
            
            print("="*80 + "\n")
            
            # DEBUG: Kiểm tra TẤT CẢ pools và talents có sinh nhật hôm nay (bất kể có campaign hay không)
            print("\n" + "="*80)
            print("🔍 DEBUG - Checking ALL pools for birthday talents (no campaign filter)")
            print("="*80)
            
            all_pools = frappe.db.sql("""
                SELECT DISTINCT segment_id
                FROM `tabMira Talent Pool`
            """, as_dict=True)
            
            print(f"📋 Total pools in system: {len(all_pools)}")
            
            for pool in all_pools:
                pool_id = pool.get('segment_id')
                
                # Count talents in pool
                pool_talent_count = frappe.db.sql("""
                    SELECT COUNT(DISTINCT t.name) as count
                    FROM `tabMira Talent` t
                    INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
                    WHERE tp.segment_id = %s
                """, (pool_id,), as_dict=True)[0].get('count', 0)
                
                # Count with DOB
                pool_talent_with_dob = frappe.db.sql("""
                    SELECT COUNT(DISTINCT t.name) as count
                    FROM `tabMira Talent` t
                    INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
                    WHERE tp.segment_id = %s
                    AND t.date_of_birth IS NOT NULL
                """, (pool_id,), as_dict=True)[0].get('count', 0)
                
                # Count birthday today
                pool_talent_birthday_today = frappe.db.sql("""
                    SELECT COUNT(DISTINCT t.name) as count
                    FROM `tabMira Talent` t
                    INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
                    WHERE tp.segment_id = %s
                    AND t.date_of_birth IS NOT NULL
                    AND MONTH(t.date_of_birth) = MONTH(CURDATE())
                    AND DAY(t.date_of_birth) = DAY(CURDATE())
                """, (pool_id,), as_dict=True)[0].get('count', 0)
                
                if pool_talent_birthday_today > 0:
                    print(f"\n🎂 Pool: {pool_id}")
                    print(f"   📊 Total talents: {pool_talent_count}")
                    print(f"   📅 Talents with DOB: {pool_talent_with_dob}")
                    print(f"   🎉 Birthday today: {pool_talent_birthday_today}")
                    
                    # List birthday talents
                    birthday_talents = frappe.db.sql("""
                        SELECT t.name, t.full_name, t.email, t.date_of_birth, t.email_opt_out
                        FROM `tabMira Talent` t
                        INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
                        WHERE tp.segment_id = %s
                        AND t.date_of_birth IS NOT NULL
                        AND MONTH(t.date_of_birth) = MONTH(CURDATE())
                        AND DAY(t.date_of_birth) = DAY(CURDATE())
                    """, (pool_id,), as_dict=True)
                    
                    for bt in birthday_talents:
                        has_email = "✅" if bt.get('email') and bt.get('email') != '' else "❌ No email"
                        opt_out = "🚫 Opt-out" if bt.get('email_opt_out') else "✅ Active"
                        print(f"      - {bt.get('full_name')} | Email: {bt.get('email')} | {has_email} | {opt_out}")
                        print(f"        DOB: {bt.get('date_of_birth')} | ID: {bt.get('name')}")
            
            print("="*80)
            print("💡 TIP: To enable birthday emails, create a campaign with:")
            print("   - type = 'NURTURING'")
            print("   - status = 'ACTIVE'")
            print("   - is_active = 1")
            print("   - Add a Flow with trigger_type = 'ON_BIRTHDAY' and status = 'ACTIVE'")
            print("   - Set target_pool to a pool with birthday talents")
            print("="*80 + "\n")
            
            return {
                "success": True,
                "total_checked": 0,
                "birthday_found": 0,
                "emails_sent": 0,
                "emails_failed": 0,
                "campaigns_processed": 0,
                "execution_time": round(time.time() - start_time, 2),
                "message": "No active NURTURING campaigns with ON_BIRTHDAY trigger"
            }
        
        # Debug: Print campaigns and flows
        print(f"\n🔍 Active campaigns with flows:")
        for camp in active_campaigns:
            print(f"   - Campaign: {camp.get('campaign_name')} ({camp.get('name')})")
            print(f"     Flow: {camp.get('flow_title')} ({camp.get('flow_name')})")
            print(f"     Type: {camp.get('type')} | Pool: {camp.get('target_pool')}")

        # Bước 2: Lấy talents từ các pools của các chiến dịch này
        pool_ids = [c.get('target_pool') for c in active_campaigns if c.get('target_pool')]
        
        if not pool_ids:
            print("⚠️ WARNING: No target pools found in campaigns!")
            logger.warning("No target pools found in active campaigns")
            return {
                "success": True,
                "total_checked": 0,
                "birthday_found": 0,
                "emails_sent": 0,
                "emails_failed": 0,
                "campaigns_processed": campaigns_processed,
                "execution_time": round(time.time() - start_time, 2),
                "message": "No target pools in campaigns"
            }
        
        print(f"\n📋 Target pools from campaigns: {pool_ids}")
        logger.info(f"Target pools: {pool_ids}")
        
        # Debug: Kiểm tra từng pool có bao nhiêu talents
        for pool_id in pool_ids:
            pool_talent_count = frappe.db.sql("""
                SELECT COUNT(DISTINCT t.name) as count
                FROM `tabMira Talent` t
                INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
                WHERE tp.segment_id = %s
            """, (pool_id,), as_dict=True)[0].get('count', 0)
            
            pool_talent_with_dob = frappe.db.sql("""
                SELECT COUNT(DISTINCT t.name) as count
                FROM `tabMira Talent` t
                INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
                WHERE tp.segment_id = %s
                AND t.date_of_birth IS NOT NULL
            """, (pool_id,), as_dict=True)[0].get('count', 0)
            
            pool_talent_birthday_today = frappe.db.sql("""
                SELECT COUNT(DISTINCT t.name) as count
                FROM `tabMira Talent` t
                INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
                WHERE tp.segment_id = %s
                AND t.date_of_birth IS NOT NULL
                AND MONTH(t.date_of_birth) = MONTH(CURDATE())
                AND DAY(t.date_of_birth) = DAY(CURDATE())
            """, (pool_id,), as_dict=True)[0].get('count', 0)
            
            print(f"\n🔍 Pool: {pool_id}")
            print(f"   📊 Total talents: {pool_talent_count}")
            print(f"   📅 Talents with DOB: {pool_talent_with_dob}")
            print(f"   🎂 Birthday today: {pool_talent_birthday_today}")
            logger.info(f"Pool {pool_id}: {pool_talent_count} total, {pool_talent_with_dob} with DOB, {pool_talent_birthday_today} birthday today")
            
            # Nếu có sinh nhật hôm nay, list ra
            if pool_talent_birthday_today > 0:
                birthday_talents_in_pool = frappe.db.sql("""
                    SELECT t.name, t.full_name, t.email, t.date_of_birth, t.email_opt_out
                    FROM `tabMira Talent` t
                    INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
                    WHERE tp.segment_id = %s
                    AND t.date_of_birth IS NOT NULL
                    AND MONTH(t.date_of_birth) = MONTH(CURDATE())
                    AND DAY(t.date_of_birth) = DAY(CURDATE())
                """, (pool_id,), as_dict=True)
                
                print(f"   🎉 Birthday talents in pool {pool_id}:")
                for bt in birthday_talents_in_pool:
                    email_status = "✅ Valid" if bt.get('email') and not bt.get('email_opt_out') else "❌ Invalid/Opt-out"
                    print(f"      - {bt.get('full_name')} ({bt.get('email')}) - DOB: {bt.get('date_of_birth')} - {email_status}")
                    logger.info(f"Birthday talent: {bt.get('full_name')} ({bt.get('email')}) in pool {pool_id}")
        
        # Lấy talents từ pools
        pool_placeholders = ', '.join(['%s'] * len(pool_ids))
        talents = frappe.db.sql(f"""
            SELECT DISTINCT t.name, t.full_name, t.email, t.date_of_birth, t.email_opt_out,
                   tp.segment_id as pool_name
            FROM `tabMira Talent` t
            INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
            WHERE tp.segment_id IN ({pool_placeholders})
            AND t.date_of_birth IS NOT NULL
            AND t.email IS NOT NULL
            AND t.email != ''
            AND (t.email_opt_out = 0 OR t.email_opt_out IS NULL)
        """, tuple(pool_ids), as_dict=True)

        total_checked = len(talents)
        logger.info(f"📊 Found {total_checked} talents with DOB and email")
        print(f"\n📊 Total talents to check: {total_checked}")

        # Debug: Print first few talents for inspection
        if talents:
            print(f"\n🔍 DEBUG - First 5 talents from query:")
            for i, talent in enumerate(talents[:5]):
                print(f"   [{i+1}] {talent.get('full_name')} - DOB: {talent.get('date_of_birth')} - Email: {talent.get('email')} - Pool: {talent.get('pool_name')}")
        else:
            print("⚠️ WARNING: No talents found in pools!")
            logger.warning("No talents found in talent pools with valid DOB and email")
        
        # Debug: So sánh với tất cả talents có sinh nhật hôm nay (không filter email)
        all_birthday_today = frappe.db.sql(f"""
            SELECT DISTINCT t.name, t.full_name, t.email, t.date_of_birth, t.email_opt_out,
                   tp.segment_id as pool_name
            FROM `tabMira Talent` t
            INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
            WHERE tp.segment_id IN ({pool_placeholders})
            AND t.date_of_birth IS NOT NULL
            AND MONTH(t.date_of_birth) = MONTH(CURDATE())
            AND DAY(t.date_of_birth) = DAY(CURDATE())
        """, tuple(pool_ids), as_dict=True)
        
        if all_birthday_today:
            print(f"\n🎂 ALL talents with birthday today in pools (including no email): {len(all_birthday_today)}")
            for bt in all_birthday_today:
                has_email = "✅" if bt.get('email') and bt.get('email') != '' else "❌ No email"
                opt_out = "🚫 Opt-out" if bt.get('email_opt_out') else "✅ Active"
                in_query = "✅ In query" if bt.get('name') in [t.get('name') for t in talents] else "❌ FILTERED OUT"
                print(f"   - {bt.get('full_name')} | {has_email} | {opt_out} | {in_query}")
                print(f"     Email: {bt.get('email')} | DOB: {bt.get('date_of_birth')} | Pool: {bt.get('pool_name')}")
        else:
            print(f"\n⚠️ No talents with birthday today found in any pool!")
            logger.warning("No birthday talents found in pools today")

        # Get email template
        email_template = get_birthday_email_template()
        print(f"\n📧 Email template loaded - Subject: {email_template['subject']}")

        # Check each talent
        birthday_talents = []
        pools_processed = {}

        for talent in talents:
            try:
                # Debug: Print talent being checked
                talent_name = talent.get('full_name') or talent.get('name', 'Unknown')
                talent_dob = talent.get('date_of_birth')
                talent_email = talent.get('email')
                pool_name = talent.get('pool_name', 'Unknown Pool')
                
                print(f"\n🔍 Checking talent: {talent_name}")
                print(f"   📅 DOB: {talent_dob}")
                print(f"   📧 Email: {talent_email}")
                print(f"   📋 Pool: {pool_name}")
                print(f"   📆 Today: {nowdate()}")

                # Check if today is birthday
                is_birthday = check_birthday(talent)
                print(f"   🎂 Birthday check result: {is_birthday}")
                
                if not is_birthday:
                    # Debug why not birthday
                    from datetime import datetime
                    if talent_dob:
                        dob_date = getdate(talent_dob)
                        today_date = getdate(nowdate())
                        print(f"   ❌ Not birthday - DOB month/day: {dob_date.month}/{dob_date.day}, Today: {today_date.month}/{today_date.day}")
                    else:
                        print(f"   ❌ Not birthday - DOB is None")

                if is_birthday:
                    birthday_found += 1
                    birthday_talents.append(talent)

                    talent_name = talent.get('full_name') or talent.get('name', 'Bạn')
                    talent_email = talent.get('email')
                    pool_name = talent.get('pool_name', 'Unknown Pool')

                    logger.info(f"🎉 Birthday found: {talent_name} ({talent_email}) from pool: {pool_name}")
                    print(f"🎉 Birthday: {talent_name} ({talent_email}) from pool: {pool_name}")

                    # Track pools
                    if pool_name not in pools_processed:
                        pools_processed[pool_name] = {"sent": 0, "failed": 0}

                    try:
                        # Personalize email content
                        personalized_content = email_template["content"].replace("{talent_name}", talent_name)

                        print(f"   📧 Attempting to send email to: {talent_email}")
                        print(f"   📝 Subject: {email_template['subject']}")
                        print(f"   📄 Content length: {len(personalized_content)} characters")

                        # Send email
                        result = send_email(
                            recipients=[talent_email],
                            subject=email_template["subject"],
                            content=personalized_content,
                            as_html=True
                        )

                        print(f"   📤 Email send result: {result}")

                        emails_sent += 1
                        pools_processed[pool_name]["sent"] += 1
                        logger.info(f"✅ Email sent to {talent_email}")
                        print(f"   ✅ Email sent successfully")

                    except Exception as send_error:
                        emails_failed += 1
                        pools_processed[pool_name]["failed"] += 1
                        error_msg = str(send_error)
                        logger.error(f"❌ Failed to send email to {talent_email}: {error_msg}")
                        print(f"   ❌ Email failed: {error_msg}")

                        # Debug: Print full error details
                        import traceback
                        print(f"   🔍 Full error traceback:")
                        print(f"   {traceback.format_exc()}")

            except Exception as talent_error:
                logger.error(f"❌ Error processing talent {talent.get('name')}: {str(talent_error)}")

        execution_time = round(time.time() - start_time, 2)

        # Final summary
        print(f"\n📊 SUMMARY:")
        print(f"   Total checked: {total_checked}")
        print(f"   Birthdays found: {birthday_found}")
        print(f"   Emails sent: {emails_sent}")
        print(f"   Emails failed: {emails_failed}")
        print(f"   Execution time: {execution_time}s")

        # Pool summary
        if pools_processed:
            print(f"\n📋 POOLS PROCESSED:")
            for pool, stats in pools_processed.items():
                print(f"   {pool}: {stats['sent']} sent, {stats['failed']} failed")

        print("="*80 + "\n")

        logger.info(f"🎂 Birthday check completed")
        logger.info(f"📊 Results: {birthday_found} birthdays, {emails_sent} sent, {emails_failed} failed")
        logger.info(f"📋 Campaigns processed: {campaigns_processed}")
        logger.info(f"📋 Pools processed: {list(pools_processed.keys())}")

        return {
            "success": True,
            "total_checked": total_checked,
            "birthday_found": birthday_found,
            "emails_sent": emails_sent,
            "emails_failed": emails_failed,
            "campaigns_processed": campaigns_processed,
            "execution_time": execution_time,
            "pools_processed": pools_processed
        }

    except Exception as e:
        execution_time = round(time.time() - start_time, 2)
        error_message = str(e)

        logger.error(f"❌ Critical error in birthday check: {error_message}")
        print(f"❌ CRITICAL ERROR: {error_message}")

        frappe.log_error(f"Birthday scheduler error: {error_message}", "Birthday Scheduler")

        return {
            "success": False,
            "error": error_message,
            "total_checked": total_checked,
            "birthday_found": birthday_found,
            "emails_sent": emails_sent,
            "emails_failed": emails_failed,
            "campaigns_processed": campaigns_processed,
            "execution_time": execution_time
        }

@frappe.whitelist()
def run_migration_birthday_check():
    """Chạy birthday check cho migration scenario"""
    logger = frappe.logger("birthday_scheduler")
    logger.info("🚀 Running migration birthday check...")

    result = run_daily_birthday_check(migration_run=True)

    if result.get("success"):
        logger.info(f"✅ Migration birthday check completed: {result}")
        return {
            "status": "success",
            "message": f"Migration completed. Found {result['birthday_found']} birthdays, sent {result['emails_sent']} emails.",
            "details": result
        }
    else:
        logger.error(f"❌ Migration birthday check failed: {result}")
        return {
            "status": "error",
            "message": f"Migration failed: {result.get('error', 'Unknown error')}",
            "details": result
        }

@frappe.whitelist()
def get_birthday_dashboard_stats():
    """Lấy thống kê birthday cho dashboard từ talent pools"""
    try:
        # Get current stats from talent pools
        today_stats = get_current_birthday_stats()

        return {
            "today": {
                "total_talents_checked": today_stats.get("total_talents", 0),
                "birthday_talents_found": today_stats.get("birthday_talents", 0),
                "emails_sent_successfully": 0,  # Không track được từ pools
                "emails_failed": 0,  # Không track được từ pools
                "status": "Live Data"
            },
            "last_30_days": {
                "total_checked": today_stats.get("total_talents", 0),
                "total_birthdays": today_stats.get("birthday_talents", 0),
                "total_sent": 0,  # Không có historical data
                "total_failed": 0,  # Không có historical data
                "total_runs": 0,  # Không có historical data
                "success_rate": 0  # Không có historical data
            }
        }

    except Exception as e:
        frappe.log_error(f"Error getting birthday dashboard stats: {str(e)}")
        return {
            "today": {"status": "Error", "total_talents_checked": 0, "birthday_talents_found": 0, "emails_sent_successfully": 0, "emails_failed": 0},
            "last_30_days": {"total_checked": 0, "total_birthdays": 0, "total_sent": 0, "total_failed": 0, "total_runs": 0, "success_rate": 0}
        }

def get_current_birthday_stats():
    """Lấy thống kê hiện tại từ talent pools"""
    try:
        # Count total talents in pools with DOB
        total_talents = frappe.db.sql("""
            SELECT COUNT(DISTINCT t.name) as count
            FROM `tabMira Talent` t
            INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
            WHERE t.date_of_birth IS NOT NULL
            AND t.email IS NOT NULL
            AND t.email != ''
            AND (t.email_opt_out = 0 OR t.email_opt_out IS NULL)
        """, as_dict=True)[0].get("count", 0)

        # Count talents with birthday today
        birthday_talents = frappe.db.sql("""
            SELECT COUNT(DISTINCT t.name) as count
            FROM `tabMira Talent` t
            INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
            WHERE t.date_of_birth IS NOT NULL
            AND t.email IS NOT NULL
            AND t.email != ''
            AND (t.email_opt_out = 0 OR t.email_opt_out IS NULL)
            AND MONTH(t.date_of_birth) = MONTH(CURDATE())
            AND DAY(t.date_of_birth) = DAY(CURDATE())
        """, as_dict=True)[0].get("count", 0)

        return {
            "total_talents": total_talents,
            "birthday_talents": birthday_talents
        }

    except Exception as e:
        frappe.log_error(f"Error getting current birthday stats: {str(e)}")
        return {
            "total_talents": 0,
            "birthday_talents": 0
        }
