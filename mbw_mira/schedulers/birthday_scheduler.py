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

def run_daily_birthday_check_scheduler():
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

    Args:
        migration_run (bool): True nếu đây là migration run
    """
    start_time = time.time()
    logger = frappe.logger("birthday_scheduler")

    total_checked = 0
    birthday_found = 0
    emails_sent = 0
    emails_failed = 0
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
        print(f"Session Data: {frappe.session.data}")
        print(f"DB Connection: {frappe.db}")
        print("="*80)

        # Lấy talents từ talent pools có date_of_birth
        talents = frappe.db.sql("""
            SELECT DISTINCT t.name, t.full_name, t.email, t.date_of_birth, t.email_opt_out,
                   tp.segment_id as pool_name
            FROM `tabMira Talent` t
            INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
            WHERE t.date_of_birth IS NOT NULL
            AND t.email IS NOT NULL
            AND t.email != ''
            AND (t.email_opt_out = 0 OR t.email_opt_out IS NULL)
        """, as_dict=True)

        total_checked = len(talents)
        logger.info(f"📊 Found {total_checked} talents with DOB and email")
        print(f"📊 Total talents to check: {total_checked}")

        # Debug: Print first few talents for inspection
        if talents:
            print(f"\n🔍 DEBUG - First 3 talents:")
            for i, talent in enumerate(talents[:3]):
                print(f"   [{i+1}] {talent.get('full_name')} - DOB: {talent.get('date_of_birth')} - Email: {talent.get('email')} - Pool: {talent.get('pool_name')}")
        else:
            print("⚠️ WARNING: No talents found in pools!")
            logger.warning("No talents found in talent pools with valid DOB and email")

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
                print(f"\n🔍 Checking talent: {talent_name} - DOB: {talent_dob}")

                # Check if today is birthday
                is_birthday = check_birthday(talent)
                print(f"   Birthday check result: {is_birthday}")

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
        logger.info(f"📋 Pools processed: {list(pools_processed.keys())}")

        return {
            "success": True,
            "total_checked": total_checked,
            "birthday_found": birthday_found,
            "emails_sent": emails_sent,
            "emails_failed": emails_failed,
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
