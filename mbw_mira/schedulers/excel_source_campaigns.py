import frappe
from datetime import date

def run():
    """
    Quét các chiến dịch ACTIVE có nguồn từ Excel/CSV và enqueue worker import.
    """
    today = date.today()
    campaigns = frappe.get_all(
        "Campaign",
        filters={
            "is_active": 1,
            "status": "ACTIVE",
            "start_date": ("<=", today),
            "end_date": (">=", today)
        },
        fields=["name", "campaign_name"]
    )

    logger = frappe.logger("campaign_enqueuer")
    count = 0

    for c in campaigns:
        # Tìm source config kèm file
        source_config = frappe.db.get_value(
            "Source Config",
            {"campaign": c.name},
            ["file_name"],
            as_dict=True
        )

        if not source_config:
            logger.warning(f"Campaign '{c.campaign_name}' has no Source Config.")
            continue

        file_name = source_config.file_name
        if not file_name or not file_name.endswith((".csv", ".xls", ".xlsx")):
            logger.warning(f"Campaign '{c.campaign_name}' file not supported: {file_name}")
            continue

        # Enqueue xử lý file
        frappe.enqueue(
            method="mbw_mira.workers.import_excel_for_talent.import_candidates_from_file",
            campaign_id=c.name,
            queue="default",
            timeout=600
        )

        logger.info(f"Enqueued import from Excel for campaign: {c.campaign_name}")
        count += 1

    logger.info(f"🎯 Total campaigns enqueued: {count}")
