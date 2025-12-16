import frappe
import json
from mbw_mira.api.campaign import run_birthday_test_for_pool

def send_daily_birthday_emails_cron():
    """
    Daily Cron Job to trigger Birthday Campaigns.
    Instead of sending a generic email, this looks for ACTIVE Birthday Campaigns
    and executes their logic (sending the configured email to eligible candidates).
    """
    print("🎂 Starting Daily Birthday Campaign Job...")
    
    active_campaigns_count = 0
    
    # 1. Get all active campaigns
    try:
        active_campaigns = frappe.get_all("Mira Campaign", filters={"status": "ACTIVE"}, pluck="name")
    except Exception as e:
        print(f"❌ Error getting active campaigns: {e}")
        return
    
    if not active_campaigns:
        print("ℹ️ No active campaigns found. Skipping birthday check.")
        return

    # 2. Find flows belonging to active campaigns that have ON_BIRTHDAY trigger
    # We query the child table `Mira Flow Trigger` directly to find parents
    try:
        birthday_triggers = frappe.get_all(
            "Mira Flow Trigger",
            filters={"trigger_type": "ON_BIRTHDAY"},
            fields=["parent"]
        )
    except Exception as e:
        print(f"❌ Error getting birthday triggers: {e}")
        return
    
    processed_campaign_ids = set()

    for trigger in birthday_triggers:
        flow_name = trigger.parent
        try:
            flow = frappe.get_doc("Mira Flow", flow_name)
            
            # Check if flow is active
            if flow.status != 'Active':
                continue
                
            # Check if campaign is active
            if flow.campaign_id not in active_campaigns:
                continue
                
            # Avoid processing same campaign multiple times
            if flow.campaign_id in processed_campaign_ids:
                continue

            print(f"🚀 Processing Birthday Campaign: {flow.campaign_id} (Flow: {flow.name})")
            
            # Get Campaign to get the Pool
            campaign = frappe.get_doc("Mira Campaign", flow.campaign_id)
            target_pool = campaign.target_pool # This is the Link to Mira Talent Pool (actually segment_id usually)
            
            # Use target_segment directly if it's the pool ID, or map it if needed
            # In Mira, target_segment usually IS the pool name/ID for simple segmentation
            
            if not target_pool:
                 print(f"⚠️ Campaign {campaign.name} has no Target Pool. Skipping.")
                 continue

            # Get Email Content from Flow Actions
            email_action = None
            if flow.action_id:
                for action in flow.action_id:
                    if action.action_type == 'EMAIL':
                        email_action = action
                        break
            
            if not email_action:
                print(f"⚠️ Flow {flow.name} has no EMAIL action. Skipping.")
                continue

            # Parse content
            params = {}
            if email_action.action_parameters:
                if isinstance(email_action.action_parameters, str):
                    try:
                        params = json.loads(email_action.action_parameters)
                    except:
                        pass
                else:
                    params = email_action.action_parameters
            
            subject = params.get('email_subject') or params.get('subject') or "Happy Birthday!"
            content = params.get('content') or params.get('email_content') or ""

            # Execute sending logic
            print(f"📨 Sending emails for campaign '{campaign.campaign_name}' to pool '{target_pool}'...")
            result = run_birthday_test_for_pool(target_pool, subject, content)
            
            print(f"✅ Result: {result}")
            processed_campaign_ids.add(flow.campaign_id)
            active_campaigns_count += 1

        except Exception as e:
            print(f"❌ Error processing flow {flow_name}: {e}")

    if active_campaigns_count == 0:
        print("ℹ️ No active Birthday Campaigns found to execute.")
    else:
        print(f"🏁 Finished processing {active_campaigns_count} campaigns.")
