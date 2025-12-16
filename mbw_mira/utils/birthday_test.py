"""
Birthday Test - Test và debug birthday reminder system
"""

import frappe
from frappe.utils import nowdate, getdate
from mbw_mira.utils.birthday_utils import check_birthday
from mbw_mira.utils.email import send_email

@frappe.whitelist()
def test_birthday_data():
    """Test để kiểm tra data có sẵn"""
    print("\n" + "="*60)
    print("🔍 BIRTHDAY DATA TEST")
    print("="*60)

    # 1. Kiểm tra có Mira Talent không
    talent_count = frappe.db.count("Mira Talent")
    print(f"📊 Total Mira Talents: {talent_count}")

    # 2. Kiểm tra có Mira Talent Pool không
    pool_count = frappe.db.count("Mira Talent Pool")
    print(f"📊 Total Talent Pools: {pool_count}")

    # 3. Kiểm tra talents có date_of_birth
    talents_with_dob = frappe.db.sql("""
        SELECT COUNT(*) as count
        FROM `tabMira Talent`
        WHERE date_of_birth IS NOT NULL
    """, as_dict=True)[0].count
    print(f"📊 Talents with DOB: {talents_with_dob}")

    # 4. Kiểm tra talents trong pools có date_of_birth
    talents_in_pools_with_dob = frappe.db.sql("""
        SELECT COUNT(DISTINCT t.name) as count
        FROM `tabMira Talent` t
        INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
        WHERE t.date_of_birth IS NOT NULL
    """, as_dict=True)[0].count
    print(f"📊 Talents in pools with DOB: {talents_in_pools_with_dob}")

    # 5. Lấy một vài talents để xem
    sample_talents = frappe.db.sql("""
        SELECT t.name, t.full_name, t.email, t.date_of_birth, tp.segment_id as pool_name
        FROM `tabMira Talent` t
        INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
        WHERE t.date_of_birth IS NOT NULL
        LIMIT 5
    """, as_dict=True)

    print(f"\n📋 Sample talents in pools:")
    for talent in sample_talents:
        print(f"   - {talent.full_name} | DOB: {talent.date_of_birth} | Email: {talent.email} | Pool: {talent.pool_name}")

    # 6. Kiểm tra có ai sinh nhật hôm nay không
    today = nowdate()
    print(f"\n📅 Today: {today}")

    birthday_today = frappe.db.sql("""
        SELECT t.name, t.full_name, t.email, t.date_of_birth, tp.segment_id as pool_name
        FROM `tabMira Talent` t
        INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
        WHERE t.date_of_birth IS NOT NULL
        AND MONTH(t.date_of_birth) = MONTH(CURDATE())
        AND DAY(t.date_of_birth) = DAY(CURDATE())
    """, as_dict=True)

    print(f"\n🎂 Talents with birthday today: {len(birthday_today)}")
    for talent in birthday_today:
        print(f"   🎉 {talent.full_name} | DOB: {talent.date_of_birth} | Email: {talent.email} | Pool: {talent.pool_name}")

    print("="*60)

    return {
        "total_talents": talent_count,
        "total_pools": pool_count,
        "talents_with_dob": talents_with_dob,
        "talents_in_pools_with_dob": talents_in_pools_with_dob,
        "birthday_today": len(birthday_today),
        "sample_talents": sample_talents,
        "birthday_talents": birthday_today
    }

@frappe.whitelist()
def test_email_sending(test_email=None):
    """Test gửi email"""
    if not test_email:
        test_email = frappe.session.user

    print(f"\n📧 Testing email sending to: {test_email}")

    try:
        from mbw_mira.utils.birthday_scheduler import get_birthday_email_template
        template = get_birthday_email_template()

        content = template["content"].replace("{talent_name}", "Test User")

        result = send_email(
            recipients=[test_email],
            subject=template["subject"],
            content=content,
            as_html=True
        )

        print(f"✅ Email sent successfully: {result}")
        return {"success": True, "result": result}

    except Exception as e:
        print(f"❌ Email failed: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def create_test_birthday_talent(pool_name=None):
    """Tạo test talent có sinh nhật hôm nay"""
    if not pool_name:
        pool_name = "Test Pool"

    try:
        # Tạo test talent với sinh nhật hôm nay
        today = nowdate()

        talent = frappe.get_doc({
            "doctype": "Mira Talent",
            "full_name": f"Test Birthday User {today}",
            "email": f"test.birthday.{today.replace('-', '')}@example.com",
            "date_of_birth": today,  # Sinh nhật hôm nay
            "email_opt_out": 0
        })
        talent.insert(ignore_permissions=True)

        # Tạo pool nếu chưa có
        if not frappe.db.exists("Mira Segment", pool_name):
            segment = frappe.get_doc({
                "doctype": "Mira Segment",
                "segment_name": pool_name,
                "description": "Test pool for birthday testing"
            })
            segment.insert(ignore_permissions=True)

        # Thêm vào pool
        pool_entry = frappe.get_doc({
            "doctype": "Mira Talent Pool",
            "segment_id": pool_name,
            "talent_id": talent.name,
            "enroll_type": "Manual",
            "match_score": 100
        })
        pool_entry.insert(ignore_permissions=True)

        frappe.db.commit()

        print(f"✅ Created test talent: {talent.name} with birthday today in pool: {pool_name}")
        return {
            "success": True,
            "talent_id": talent.name,
            "talent_name": talent.full_name,
            "talent_email": talent.email,
            "pool_name": pool_name
        }

    except Exception as e:
        print(f"❌ Failed to create test talent: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def run_birthday_test():
    """Chạy full test birthday system"""
    print("\n" + "="*80)
    print("🎂 FULL BIRTHDAY SYSTEM TEST")
    print("="*80)

    # 1. Test data
    print("\n1️⃣ Testing data...")
    data_result = test_birthday_data()

    # 2. Test email
    print("\n2️⃣ Testing email...")
    email_result = test_email_sending()

    # 3. Nếu không có birthday hôm nay, tạo test data
    if data_result["birthday_today"] == 0:
        print("\n3️⃣ No birthdays today, creating test data...")
        test_talent = create_test_birthday_talent("Test Birthday Pool")
        if test_talent["success"]:
            print("✅ Test talent created, re-running data test...")
            data_result = test_birthday_data()

    # 4. Chạy birthday check
    print("\n4️⃣ Running birthday check...")
    from mbw_mira.utils.birthday_scheduler import run_daily_birthday_check
    birthday_result = run_daily_birthday_check(migration_run=True)

    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    print(f"Data check: {data_result['birthday_today']} birthdays found")
    print(f"Email test: {'✅ Success' if email_result['success'] else '❌ Failed'}")
    print(f"Birthday check: {'✅ Success' if birthday_result['success'] else '❌ Failed'}")
    print("="*80)

    return {
        "data_result": data_result,
        "email_result": email_result,
        "birthday_result": birthday_result
    }
