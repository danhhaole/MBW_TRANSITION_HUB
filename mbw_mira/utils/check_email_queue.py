"""
Check Email Queue - Kiểm tra email đã gửi
"""

import frappe
from frappe.utils import nowdate

@frappe.whitelist()
def check_recent_email_queue():
    """Kiểm tra Email Queue gần đây"""
    try:
        # Kiểm tra Email Queue bằng get_all - chỉ lấy fields cơ bản
        emails = frappe.get_all("Email Queue",
            filters={
                "creation": [">=", nowdate()]
            },
            fields=["name", "status", "creation"],
            order_by="creation desc",
            limit=20
        )

        print(f"\n📧 EMAIL QUEUE CHECK - {nowdate()}")
        print("="*60)
        print(f"Found {len(emails)} emails in queue today")

        birthday_emails = []
        for email in emails:
            try:
                # Get full email details
                email_doc = frappe.get_doc("Email Queue", email.name)
                subject = getattr(email_doc, 'subject', '') or ''
                recipients = getattr(email_doc, 'recipients', '') or ''
                error = getattr(email_doc, 'error', '') or ''

                if "sinh nhật" in subject.lower() or "birthday" in subject.lower():
                    birthday_emails.append(email)
                    print(f"\n🎂 Birthday Email:")
                    print(f"   ID: {email.name}")
                    print(f"   Status: {email.status}")
                    print(f"   To: {recipients}")
                    print(f"   Subject: {subject}")
                    print(f"   Created: {email.creation}")
                    if error:
                        print(f"   Error: {error}")
                else:
                    print(f"\n📧 Email: {subject[:50]}... | Status: {email.status}")
            except Exception as e:
                print(f"\n❌ Error reading email {email.name}: {str(e)}")

        print(f"\n📊 Summary:")
        print(f"   Total emails today: {len(emails)}")
        print(f"   Birthday emails: {len(birthday_emails)}")
        print("="*60)

        return {
            "total_emails": len(emails),
            "birthday_emails": len(birthday_emails),
            "emails": emails,
            "birthday_email_details": birthday_emails
        }

    except Exception as e:
        print(f"❌ Error checking email queue: {str(e)}")
        return {"error": str(e)}

@frappe.whitelist()
def flush_email_queue():
    """Flush email queue để gửi email ngay"""
    try:
        print("\n📤 FLUSHING EMAIL QUEUE...")

        # Flush email queue
        from frappe.email.queue import flush
        flush(from_test=False)

        print("✅ Email queue flushed successfully!")

        # Kiểm tra lại sau khi flush
        result = check_recent_email_queue()
        return result

    except Exception as e:
        print(f"❌ Error flushing email queue: {str(e)}")
        return {"error": str(e)}

@frappe.whitelist()
def check_email_account():
    """Kiểm tra cấu hình email account"""
    try:
        print("\n📧 EMAIL ACCOUNT CHECK")
        print("="*50)

        # Lấy default email account
        email_accounts = frappe.get_all("Email Account",
            filters={"enable_outgoing": 1},
            fields=["name", "email_id", "smtp_server", "default_outgoing", "enable_outgoing"]
        )

        print(f"Found {len(email_accounts)} outgoing email accounts:")
        for acc in email_accounts:
            print(f"   - {acc.name}: {acc.email_id} (Default: {acc.default_outgoing})")
            print(f"     SMTP: {acc.smtp_server}")

        # Kiểm tra email settings
        email_settings = frappe.get_single("Email Settings")
        print(f"\nEmail Settings:")
        print(f"   Auto Email ID: {email_settings.auto_email_id}")
        print(f"   Send Print in Body: {email_settings.send_print_in_body_and_attachment}")

        return {
            "email_accounts": email_accounts,
            "email_settings": email_settings.as_dict()
        }

    except Exception as e:
        print(f"❌ Error checking email account: {str(e)}")
        return {"error": str(e)}
