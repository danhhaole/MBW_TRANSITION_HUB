import json
import frappe
import requests
from typing import Optional, Tuple
from datetime import datetime

from mbw_mira.api.external_connections import host as SOCIALHUB_HOST

def run():
    now = datetime.now()
    action  = frappe.get_all(
        "Action",
        filters={
            "status": "Scheduled",
            "scheduled_at": ("<=", now)
        },
        fields=["name","campaign_step"],
    )
    print("action>>>>>>>>>>>>>>>>>>>>>>:",action)
    
