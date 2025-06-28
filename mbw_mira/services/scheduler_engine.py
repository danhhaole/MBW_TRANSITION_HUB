# services/scheduler_engine/scheduler_engine.py

import frappe
from frappe.utils import now_datetime
from mbw_mira.services.base_engine import BaseScheduler
from mbw_mira.services.enqueue_worker import (
    enqueue_nurturing_collector_worker,
    enqueue_scheduler_worker,
)


class CampaignSchedulerEngine(BaseScheduler):
    def run(self):
        """Chỉ kiểm tra campaign đủ điều kiện (status = ACTIVE)

        Phân luồng xử lý theo type:

            NURTURING: enqueue worker chuyên thu thập ứng viên (NurturingCandidateCollectorWorker)

            ATTRACTION: enqueue worker chuyên xử lý candidate campaign (ActionSchedulerWorker)
        """

        now = now_datetime()

        # 1. Quét tất cả Campaign status = ACTIVE
        campaigns = frappe.get_all(
            "Campaign",
            filters={"status": "ACTIVE", "type": ["in", ["NURTURING", "ATTRACTION"]]},
            fields=["name", "type"],
        )

        for campaign in campaigns:
            if campaign["type"] == "NURTURING":
                enqueue_nurturing_collector_worker(campaign["name"])

            elif campaign["type"] == "ATTRACTION":
                # Với ATTRACTION, quét các ứng viên đến hạn
                candidate_campaigns = frappe.get_all(
                    "CandidateCampaign",
                    filters={
                        "status": "ACTIVE",
                        "campaign": campaign["name"],
                        "next_action_at": ["<=", now],
                    },
                    fields=["name"],
                )

                for cc in candidate_campaigns:
                    enqueue_scheduler_worker(cc["name"])
