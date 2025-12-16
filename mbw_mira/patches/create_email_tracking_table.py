"""
Create Mira Email Tracking table directly in database
"""
import frappe

def execute():
    """Create the Mira Email Tracking table if it doesn't exist"""
    frappe.db.sql("""
        CREATE TABLE IF NOT EXISTS `tabMira Email Tracking` (
            `name` VARCHAR(140) PRIMARY KEY,
            `talent_id` VARCHAR(140),
            `campaign_id` VARCHAR(140),
            `email_subject` VARCHAR(255),
            `email_content` LONGTEXT,
            `email_sent` INT DEFAULT 0,
            `email_sent_on` DATETIME,
            `email_clicked` INT DEFAULT 0,
            `email_clicked_on` DATETIME,
            `is_active` INT DEFAULT 1,
            `deactivated_on` DATETIME,
            `deactivation_reason` VARCHAR(255),
            `created_by` VARCHAR(140),
            `creation` DATETIME,
            `modified` DATETIME,
            `modified_by` VARCHAR(140),
            `owner` VARCHAR(140),
            INDEX idx_talent_id (`talent_id`),
            INDEX idx_campaign_id (`campaign_id`),
            INDEX idx_email_sent_on (`email_sent_on`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    frappe.db.commit()
    print("✅ Created tabMira Email Tracking table")
