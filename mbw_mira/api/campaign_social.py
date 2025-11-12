import frappe
from frappe import _
import json


@frappe.whitelist()
def save_campaign_social_posts(campaign_id, posts):
    """
    Save or update social media posts for a campaign
    
    Args:
        campaign_id: Mira Campaign ID
        posts: List of social post data
            [
                {
                    "platform": "Facebook",
                    "social_page_id": "page-123",
                    "social_page_name": "Company Page",
                    "template_content": "<p>Job opening...</p>",
                    "social_media_images": "https://...",
                    "status": "Pending"
                },
                {
                    "platform": "Zalo",
                    "template_content": '{"blocks":[...]}',
                    "status": "Pending"
                }
            ]
    
    Returns:
        {
            "success": True,
            "message": "Social posts saved successfully",
            "data": [list of created/updated post names]
        }
    """
    try:
        # Parse posts if string
        if isinstance(posts, str):
            posts = json.loads(posts)
        
        # Validate campaign exists
        if not frappe.db.exists("Mira Campaign", campaign_id):
            frappe.throw(_("Campaign {0} does not exist").format(campaign_id))
        
        # Get existing posts for this campaign
        existing_posts = frappe.get_all(
            "Mira Campaign Social",
            filters={"campaign_id": campaign_id},
            fields=["name", "platform"]
        )
        
        # Create a map of existing posts by platform
        existing_map = {post["platform"]: post["name"] for post in existing_posts}
        
        results = []
        
        for post_data in posts:
            platform = post_data.get("platform")
            
            if not platform:
                frappe.log_error(
                    message=f"Missing platform in post data: {post_data}",
                    title="Save Campaign Social Posts - Missing Platform"
                )
                continue
            
            # Check if post exists for this platform
            existing_name = existing_map.get(platform)
            
            if existing_name:
                # Update existing post
                doc = frappe.get_doc("Mira Campaign Social", existing_name)
                
                # Update fields
                for key, value in post_data.items():
                    if key != "doctype" and hasattr(doc, key):
                        setattr(doc, key, value)
                
                doc.save(ignore_permissions=True)
                results.append({
                    "name": doc.name,
                    "platform": platform,
                    "action": "updated"
                })
                
                frappe.logger().info(f"Updated social post {doc.name} for platform {platform}")
                
            else:
                # Create new post
                doc = frappe.get_doc({
                    "doctype": "Mira Campaign Social",
                    "campaign_id": campaign_id,
                    **post_data
                })
                
                doc.insert(ignore_permissions=True)
                results.append({
                    "name": doc.name,
                    "platform": platform,
                    "action": "created"
                })
                
                frappe.logger().info(f"Created social post {doc.name} for platform {platform}")
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": _("Social posts saved successfully"),
            "data": results
        }
        
    except Exception as e:
        frappe.log_error(
            message=frappe.get_traceback(),
            title="Save Campaign Social Posts Error"
        )
        return {
            "success": False,
            "message": str(e),
            "data": None
        }


@frappe.whitelist()
def get_campaign_social_posts(campaign_id):
    """
    Get all social media posts for a campaign
    
    Args:
        campaign_id: Mira Campaign ID
    
    Returns:
        {
            "success": True,
            "message": "Posts retrieved successfully",
            "data": [list of social posts]
        }
    """
    try:
        # Validate campaign exists
        if not frappe.db.exists("Mira Campaign", campaign_id):
            frappe.throw(_("Campaign {0} does not exist").format(campaign_id))
        
        # Get all posts for this campaign
        posts = frappe.get_all(
            "Mira Campaign Social",
            filters={"campaign_id": campaign_id},
            fields=["*"],
            order_by="creation asc"
        )
        
        return {
            "success": True,
            "message": _("Posts retrieved successfully"),
            "data": posts
        }
        
    except Exception as e:
        frappe.log_error(
            message=frappe.get_traceback(),
            title="Get Campaign Social Posts Error"
        )
        return {
            "success": False,
            "message": str(e),
            "data": None
        }


@frappe.whitelist()
def delete_campaign_social_post(post_name):
    """
    Delete a social media post
    
    Args:
        post_name: Mira Campaign Social name
    
    Returns:
        {
            "success": True,
            "message": "Post deleted successfully"
        }
    """
    try:
        # Validate post exists
        if not frappe.db.exists("Mira Campaign Social", post_name):
            frappe.throw(_("Post {0} does not exist").format(post_name))
        
        # Delete post
        frappe.delete_doc("Mira Campaign Social", post_name, ignore_permissions=True)
        frappe.db.commit()
        
        return {
            "success": True,
            "message": _("Post deleted successfully")
        }
        
    except Exception as e:
        frappe.log_error(
            message=frappe.get_traceback(),
            title="Delete Campaign Social Post Error"
        )
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_nurturing_campaign_triggers(campaign_id):
    """
    Get nurturing campaign triggers from Mira Campaign Social posts
    
    Args:
        campaign_id: Mira Campaign ID
    
    Returns:
        {
            "success": True,
            "message": "Triggers loaded successfully",
            "data": [list of triggers with calculated delays]
        }
    """
    try:
        # Validate campaign exists
        if not frappe.db.exists("Mira Campaign", campaign_id):
            frappe.throw(_("Campaign {0} does not exist").format(campaign_id))
        
        # Get all posts for this campaign, ordered by schedule time
        posts = frappe.get_all(
            "Mira Campaign Social",
            filters={"campaign_id": campaign_id},
            fields=[
                "name",
                "platform",
                "post_schedule_time",
                "subject",
                "template_content",
                "post_file",
                "social_media_images",
                "social_page_id",
                "social_page_name",
                "status"
            ],
            order_by="post_schedule_time ASC"
        )
        
        # Load attachments for each post
        for post in posts:
            post["attachments"] = frappe.get_all(
                "Mira Campaign Social Attachment",
                filters={"parent": post["name"]},
                fields=["file_name", "file_url", "file_size"],
                order_by="idx ASC"
            )
        
        if not posts:
            return {
                "success": True,
                "message": _("No triggers found"),
                "data": []
            }
        
        # Map platform back to channel
        platform_to_channel = {
            "Email": "email",
            "Zalo": "zalo",
            "Facebook": "messenger"
        }
        
        triggers = []
        prev_schedule_time = None
        
        for index, post in enumerate(posts):
            channel = platform_to_channel.get(post.platform, post.platform.lower())
            
            # Calculate delay from previous message
            if index == 0:
                # First message: use schedule_time
                schedule_time = post.post_schedule_time
                delay_minutes = 0
            else:
                # Subsequent messages: calculate delay
                schedule_time = None
                if prev_schedule_time and post.post_schedule_time:
                    time_diff = frappe.utils.get_datetime(post.post_schedule_time) - frappe.utils.get_datetime(prev_schedule_time)
                    delay_minutes = int(time_diff.total_seconds() / 60)
                else:
                    delay_minutes = 0
            
            # Prepare content based on channel
            content = {}
            if channel == "email":
                content = {
                    "email_subject": post.subject or "",
                    "email_content": post.template_content or "",
                    "attachments": post.get("attachments", [])
                }
            elif channel == "zalo":
                # Try to parse as JSON (blocks structure)
                try:
                    if post.template_content and post.template_content.startswith("{"):
                        content = json.loads(post.template_content)
                    else:
                        # Old simple format
                        content = {
                            "message": post.template_content or "",
                            "image": post.social_media_images
                        }
                except (json.JSONDecodeError, ValueError):
                    # Fallback to simple format
                    content = {
                        "message": post.template_content or "",
                        "image": post.social_media_images
                    }
            elif channel == "messenger":
                # Try to parse as JSON (blocks structure)
                try:
                    if post.template_content and post.template_content.startswith("{"):
                        content = json.loads(post.template_content)
                    else:
                        # Simple format
                        content = {
                            "message": post.template_content or ""
                        }
                except (json.JSONDecodeError, ValueError):
                    # Fallback to simple format
                    content = {
                        "message": post.template_content or ""
                    }
            
            # Create trigger object
            trigger = {
                "id": frappe.utils.now_datetime().timestamp() * 1000 + index,  # Generate unique ID
                "channel": channel,
                "schedule_time": schedule_time.isoformat() if schedule_time else None,
                "delay_minutes": delay_minutes,
                "sender_account": post.social_page_id,  # This is the account name/ID
                "content": content,
                "expanded": False,
                "post_name": post.name  # Keep reference to original post
            }
            
            triggers.append(trigger)
            prev_schedule_time = post.post_schedule_time
        
        return {
            "success": True,
            "message": _("Triggers loaded successfully"),
            "data": triggers
        }
        
    except Exception as e:
        frappe.log_error(
            message=frappe.get_traceback(),
            title="Get Nurturing Campaign Triggers Error"
        )
        return {
            "success": False,
            "message": str(e),
            "data": []
        }


@frappe.whitelist()
def save_nurturing_campaign_triggers(campaign_id, triggers):
    """
    Save nurturing campaign triggers (timeline messages) as Mira Campaign Social posts
    
    Args:
        campaign_id: Mira Campaign ID
        triggers: List of trigger data
            [
                {
                    "id": 1234567890,
                    "channel": "email",
                    "schedule_time": "2025-11-12T10:00",
                    "delay_minutes": 0,
                    "sender_account": "ACC-001",
                    "content": {
                        "email_subject": "Welcome!",
                        "email_content": "<p>Hello...</p>",
                        "attachments": [...]
                    }
                },
                {
                    "id": 1234567891,
                    "channel": "zalo",
                    "delay_minutes": 2880,
                    "sender_account": "ZALO-001",
                    "content": {
                        "message": "Follow up...",
                        "image": null
                    }
                },
                {
                    "id": 1234567892,
                    "channel": "messenger",
                    "delay_minutes": 10080,
                    "sender_account": "FB-PAGE-001",
                    "content": {
                        "message": "Check in..."
                    }
                }
            ]
    
    Returns:
        {
            "success": True,
            "message": "Triggers saved successfully",
            "data": {
                "created": 2,
                "updated": 1,
                "deleted": 0,
                "posts": [list of post names]
            }
        }
    """
    try:
        # Parse triggers if string
        if isinstance(triggers, str):
            triggers = json.loads(triggers)
        
        # Validate campaign exists
        if not frappe.db.exists("Mira Campaign", campaign_id):
            frappe.throw(_("Campaign {0} does not exist").format(campaign_id))
        
        # Get existing posts for this campaign
        existing_posts = frappe.get_all(
            "Mira Campaign Social",
            filters={"campaign_id": campaign_id},
            fields=["name", "platform", "post_schedule_time"]
        )
        
        # Track existing post names to identify which to keep/delete
        existing_names = {post["name"] for post in existing_posts}
        processed_names = set()
        
        results = {
            "created": 0,
            "updated": 0,
            "deleted": 0,
            "posts": []
        }
        
        # Calculate absolute schedule times for each trigger
        base_time = None
        
        for index, trigger in enumerate(triggers):
            channel = trigger.get("channel")
            content = trigger.get("content", {})
            sender_account = trigger.get("sender_account")
            
            if not channel:
                frappe.log_error(
                    message=f"Missing channel in trigger: {trigger}",
                    title="Save Nurturing Triggers - Missing Channel"
                )
                continue
            
            # Calculate schedule time
            if index == 0:
                # First message: use schedule_time if provided
                schedule_time = trigger.get("schedule_time")
                if schedule_time:
                    base_time = frappe.utils.get_datetime(schedule_time)
                else:
                    # Default to now if not specified
                    base_time = frappe.utils.now_datetime()
                post_schedule_time = base_time
            else:
                # Subsequent messages: add delay to base_time
                delay_minutes = trigger.get("delay_minutes", 0)
                if base_time:
                    post_schedule_time = frappe.utils.add_to_date(
                        base_time,
                        minutes=delay_minutes
                    )
                    base_time = post_schedule_time  # Update base for next message
                else:
                    post_schedule_time = None
            
            # Map channel to platform
            platform_map = {
                "email": "Email",
                "zalo": "Zalo",
                "messenger": "Facebook"
            }
            platform = platform_map.get(channel, channel.title())
            
            # Prepare post data based on channel
            post_data = {
                "platform": platform,
                "post_schedule_time": post_schedule_time,
                "status": "Pending"
            }
            
            # Add sender account info
            if sender_account:
                if channel == "email":
                    # Get email account details
                    email_acc = frappe.db.get_value(
                        "Email Account",
                        sender_account,
                        ["email_id", "email_account_name"],
                        as_dict=True
                    )
                    if email_acc:
                        post_data["social_page_name"] = f"{email_acc.email_id} ({email_acc.email_account_name})"
                        post_data["social_page_id"] = sender_account
                elif channel == "zalo":
                    # Get Zalo OA details from Mira External Connection
                    # sender_account is the external connection name
                    external_conn = frappe.get_doc("Mira External Connection", sender_account)
                    
                    if external_conn and external_conn.platform_type == "Zalo":
                        # Get primary account or first active OA account
                        zalo_account = None
                        for account in external_conn.connected_accounts:
                            if account.account_type == "OA" and account.is_active:
                                if account.is_primary or not zalo_account:
                                    zalo_account = account
                                    break
                        
                        if zalo_account:
                            post_data["social_page_name"] = f"{zalo_account.account_name} ({zalo_account.external_account_id})"
                            post_data["social_page_id"] = zalo_account.external_account_id
                            post_data["external_connection"] = sender_account
                elif channel == "messenger":
                    # Get Facebook Page details from Mira External Connection
                    # sender_account is the external connection name
                    external_conn = frappe.get_doc("Mira External Connection", sender_account)
                    
                    if external_conn and external_conn.platform_type == "Facebook":
                        # Get primary account or first active Page account
                        fb_account = None
                        for account in external_conn.connected_accounts:
                            if account.account_type == "Page" and account.is_active:
                                if account.is_primary or not fb_account:
                                    fb_account = account
                                    break
                        
                        if fb_account:
                            post_data["social_page_name"] = f"{fb_account.account_name} ({fb_account.external_account_id})"
                            post_data["social_page_id"] = fb_account.external_account_id
                            post_data["external_connection"] = sender_account
            
            # Add content based on channel
            if channel == "email":
                # Email: subject + content + attachments
                post_data["subject"] = content.get("email_subject", "")
                post_data["template_content"] = content.get("email_content", "")
                
                # Handle attachments - will be added to child table after doc creation
                # Store temporarily in post_data for later processing
                post_data["_attachments_data"] = content.get("attachments", [])
                
            elif channel == "zalo":
                # Zalo: blocks structure or simple message
                if "blocks" in content and isinstance(content["blocks"], list):
                    # New blocks structure - serialize to JSON
                    post_data["template_content"] = json.dumps(content)
                    
                    # Extract first image from blocks if exists
                    for block in content["blocks"]:
                        if block.get("type") == "image" and block.get("image"):
                            image_data = block["image"]
                            if isinstance(image_data, dict):
                                post_data["social_media_images"] = image_data.get("file_url", "")
                            else:
                                post_data["social_media_images"] = image_data
                            break
                else:
                    # Old simple message format
                    post_data["template_content"] = content.get("message", "")
                    if content.get("image"):
                        post_data["social_media_images"] = content.get("image")
                
            elif channel == "messenger":
                # Messenger: blocks structure or simple message
                if "blocks" in content and isinstance(content["blocks"], list):
                    # New blocks structure - serialize to JSON
                    post_data["template_content"] = json.dumps(content)
                    
                    # Extract first image from blocks if exists
                    for block in content["blocks"]:
                        if block.get("type") == "image" and block.get("image"):
                            image_data = block["image"]
                            if isinstance(image_data, dict):
                                post_data["social_media_images"] = image_data.get("file_url", "")
                            else:
                                post_data["social_media_images"] = image_data
                            break
                else:
                    # Simple message format
                    post_data["template_content"] = content.get("message", "")
            
            # Check if post exists for this trigger (match by platform and schedule time)
            existing_post = None
            for post in existing_posts:
                if (post["platform"] == platform and 
                    post["post_schedule_time"] == post_schedule_time):
                    existing_post = post
                    break
            
            # Extract attachments data before creating/updating doc
            attachments_data = post_data.pop("_attachments_data", [])
            
            if existing_post:
                # Update existing post
                doc = frappe.get_doc("Mira Campaign Social", existing_post["name"])
                
                # Update fields
                for key, value in post_data.items():
                    if hasattr(doc, key):
                        setattr(doc, key, value)
                
                # Clear existing attachments and add new ones
                doc.attachments = []
                for attachment in attachments_data:
                    doc.append("attachments", {
                        "file_name": attachment.get("file_name", ""),
                        "file_url": attachment.get("file_url", ""),
                        "file_size": attachment.get("file_size", 0)
                    })
                
                doc.save(ignore_permissions=True)
                processed_names.add(doc.name)
                results["updated"] += 1
                results["posts"].append({
                    "name": doc.name,
                    "platform": platform,
                    "action": "updated"
                })
                
                frappe.logger().info(f"Updated trigger post {doc.name} for {platform}")
                
            else:
                # Create new post
                doc = frappe.get_doc({
                    "doctype": "Mira Campaign Social",
                    "campaign_id": campaign_id,
                    **post_data
                })
                
                # Add attachments to child table
                for attachment in attachments_data:
                    doc.append("attachments", {
                        "file_name": attachment.get("file_name", ""),
                        "file_url": attachment.get("file_url", ""),
                        "file_size": attachment.get("file_size", 0)
                    })
                
                doc.insert(ignore_permissions=True)
                processed_names.add(doc.name)
                results["created"] += 1
                results["posts"].append({
                    "name": doc.name,
                    "platform": platform,
                    "action": "created"
                })
                
                frappe.logger().info(f"Created trigger post {doc.name} for {platform}")
        
        # Delete posts that are no longer in triggers
        posts_to_delete = existing_names - processed_names
        for post_name in posts_to_delete:
            frappe.delete_doc("Mira Campaign Social", post_name, ignore_permissions=True)
            results["deleted"] += 1
            frappe.logger().info(f"Deleted obsolete post {post_name}")
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": _("Triggers saved successfully"),
            "data": results
        }
        
    except Exception as e:
        frappe.log_error(
            message=frappe.get_traceback(),
            title="Save Nurturing Campaign Triggers Error"
        )
        return {
            "success": False,
            "message": str(e),
            "data": None
        }
