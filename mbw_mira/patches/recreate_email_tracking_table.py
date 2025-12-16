"""
Recreate Mira Email Tracking table with proper Frappe structure
"""
import frappe

def execute():
    """Drop and recreate the Mira Email Tracking table with all required Frappe columns"""

    # Drop existing table if exists
    frappe.db.sql("DROP TABLE IF EXISTS `tabMira Email Tracking`")

    # Create new table with all Frappe required columns
    frappe.db.sql("""
        CREATE TABLE `tabMira Email Tracking` (
            `name` VARCHAR(140) NOT NULL PRIMARY KEY,
            `creation` DATETIME(6),
            `modified` DATETIME(6),
            `modified_by` VARCHAR(140),
            `owner` VARCHAR(140),
            `docstatus` INT(1) NOT NULL DEFAULT 0,
            `idx` INT(8) NOT NULL DEFAULT 0,
            `talent_id` VARCHAR(140),
            `campaign_id` VARCHAR(140),
            `email_subject` VARCHAR(255),
            `email_content` LONGTEXT,
            `email_sent` INT(1) NOT NULL DEFAULT 0,
            `email_sent_on` DATETIME(6),
            `email_clicked` INT(1) NOT NULL DEFAULT 0,
            `email_clicked_on` DATETIME(6),
            `is_active` INT(1) NOT NULL DEFAULT 1,
            `deactivated_on` DATETIME(6),
            `deactivation_reason` VARCHAR(255),
            KEY `modified` (`modified`),
            KEY `talent_id` (`talent_id`),
            KEY `campaign_id` (`campaign_id`),
            KEY `email_sent_on` (`email_sent_on`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)

    frappe.db.commit()
    print("✅ Recreated tabMira Email Tracking table with proper Frappe structure")
