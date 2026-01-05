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

        # Track which platforms are being saved
        platforms_in_request = {post_data.get("platform") for post_data in posts if post_data.get("platform")}

        results = []

        for post_data in posts:
            platform = post_data.get("platform")

            if not platform:
                frappe.log_error(
                    message=f"Missing platform in post data: {post_data}",
                    title="Save Campaign Social Posts - Missing Platform"
                )
                continue

            # DEBUG: Log post_data before processing
            frappe.logger().info(f"[save_campaign_social_posts] Processing post for platform: {platform}")
            frappe.logger().info(f"[save_campaign_social_posts] post_data keys: {list(post_data.keys())}")
            frappe.logger().info(f"[save_campaign_social_posts] subject: {post_data.get('subject')}")
            frappe.logger().info(f"[save_campaign_social_posts] subject type: {type(post_data.get('subject'))}")
            frappe.logger().info(f"[save_campaign_social_posts] attachments: {post_data.get('attachments')}")
            frappe.logger().info(f"[save_campaign_social_posts] attachments type: {type(post_data.get('attachments'))}")

            # Extract attachments data before creating/updating doc (attachments is a child table)
            attachments_data = post_data.pop("attachments", [])
            
            frappe.logger().info(f"[save_campaign_social_posts] After pop - attachments_data: {attachments_data}")
            frappe.logger().info(f"[save_campaign_social_posts] After pop - post_data keys: {list(post_data.keys())}")
            frappe.logger().info(f"[save_campaign_social_posts] After pop - subject: {post_data.get('subject')}")

            # Check if post exists for this platform
            existing_name = existing_map.get(platform)

            if existing_name:
                # Update existing post
                doc = frappe.get_doc("Mira Campaign Social", existing_name)

                # DEBUG: Log before updating
                frappe.logger().info(f"[save_campaign_social_posts] Updating existing post: {existing_name}")
                frappe.logger().info(f"[save_campaign_social_posts] Current doc.subject: {doc.subject}")
                frappe.logger().info(f"[save_campaign_social_posts] post_data.subject: {post_data.get('subject')}")

                # Update fields (skip attachments as it's handled separately)
                for key, value in post_data.items():
                    if key != "doctype" and key != "attachments" and hasattr(doc, key):
                        frappe.logger().info(f"[save_campaign_social_posts] Setting {key} = {value} (type: {type(value)})")
                        setattr(doc, key, value)
                
                # IMPORTANT: Explicitly set subject field to ensure it's saved
                if "subject" in post_data:
                    doc.subject = post_data["subject"]
                    frappe.logger().info(f"[save_campaign_social_posts] Explicitly set doc.subject = {post_data['subject']}")
                
                frappe.logger().info(f"[save_campaign_social_posts] After update - doc.subject: {doc.subject}")
                frappe.logger().info(f"[save_campaign_social_posts] doc.subject type: {type(doc.subject)}")
                frappe.logger().info(f"[save_campaign_social_posts] doc.subject length: {len(doc.subject) if doc.subject else 0}")

                # Handle attachments - clear existing and add new ones
                if attachments_data:
                    doc.attachments = []
                    for attachment in attachments_data:
                        doc.append("attachments", {
                            "file_name": attachment.get("file_name", ""),
                            "file_url": attachment.get("file_url", ""),
                            "file_size": attachment.get("file_size", 0)
                        })

                doc.save(ignore_permissions=True)
                results.append({
                    "name": doc.name,
                    "platform": platform,
                    "action": "updated"
                })

                frappe.logger().info(f"Updated social post {doc.name} for platform {platform}")

            else:
                # DEBUG: Log before creating
                frappe.logger().info(f"[save_campaign_social_posts] Creating new post for platform: {platform}")
                frappe.logger().info(f"[save_campaign_social_posts] post_data.subject: {post_data.get('subject')}")
                frappe.logger().info(f"[save_campaign_social_posts] post_data keys: {list(post_data.keys())}")
                
                # Create new post
                # IMPORTANT: Explicitly set subject field to ensure it's saved
                doc_data = {
                    "doctype": "Mira Campaign Social",
                    "campaign_id": campaign_id,
                    **post_data
                }
                
                # Ensure subject is explicitly set
                if "subject" in post_data:
                    doc_data["subject"] = post_data["subject"]
                    frappe.logger().info(f"[save_campaign_social_posts] Explicitly setting subject in doc_data: {post_data['subject']}")
                
                doc = frappe.get_doc(doc_data)
                
                frappe.logger().info(f"[save_campaign_social_posts] After create - doc.subject: {doc.subject}")
                frappe.logger().info(f"[save_campaign_social_posts] doc.subject type: {type(doc.subject)}")
                frappe.logger().info(f"[save_campaign_social_posts] doc.subject length: {len(doc.subject) if doc.subject else 0}")

                # Add attachments to child table
                if attachments_data:
                    for attachment in attachments_data:
                        doc.append("attachments", {
                            "file_name": attachment.get("file_name", ""),
                            "file_url": attachment.get("file_url", ""),
                            "file_size": attachment.get("file_size", 0)
                        })

                doc.insert(ignore_permissions=True)
                frappe.logger().info(f"[save_campaign_social_posts] After insert - doc.subject: {doc.subject}")
                results.append({
                    "name": doc.name,
                    "platform": platform,
                    "action": "created"
                })

                frappe.logger().info(f"Created social post {doc.name} for platform {platform}")

        # Delete posts for platforms that are no longer in the request
        posts_to_delete = []
        for existing_platform, existing_name in existing_map.items():
            if existing_platform not in platforms_in_request:
                posts_to_delete.append((existing_name, existing_platform))

        # Delete obsolete posts
        for post_name, platform in posts_to_delete:
            try:
                frappe.delete_doc("Mira Campaign Social", post_name, ignore_permissions=True)
                results.append({
                    "name": post_name,
                    "platform": platform,
                    "action": "deleted"
                })
                frappe.logger().info(f"Deleted obsolete social post {post_name} for platform {platform}")
            except Exception as e:
                frappe.log_error(
                    message=f"Failed to delete post {post_name}: {str(e)}",
                    title="Save Campaign Social Posts - Delete Error"
                )

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

        # Load attachments for each post (like get_nurturing_campaign_triggers does)
        for post in posts:
            post["attachments"] = frappe.get_all(
                "Mira Campaign Social Attachment",
                filters={"parent": post["name"]},
                fields=["file_name", "file_url", "file_size"],
                order_by="idx ASC"
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
                "block_content",
                "css_content",
                "mjml_content",
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
                # Prepare email content for editing
                email_content_data = {
                    "email_subject": post.subject or "",
                    "attachments": post.get("attachments", [])
                }

                # Prioritize block_content for editing, fallback to template_content
                if post.block_content:
                    # Use EmailBuilder blocks format for editing
                    email_content_data["email_content"] = post.block_content
                    email_content_data["block_content"] = post.block_content
                else:
                    # Fallback to template_content (HTML)
                    email_content_data["email_content"] = post.template_content or ""

                # Include other formats if available
                if post.template_content:
                    email_content_data["template_content"] = post.template_content
                if post.mjml_content:
                    email_content_data["mjml_content"] = post.mjml_content
                if post.css_content:
                    email_content_data["css_content"] = post.css_content

                content = email_content_data
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

                # Handle different content formats for email
                if content.get("template_content"):
                    # HTML format for rendering
                    post_data["template_content"] = content.get("template_content", "")
                else:
                    # Fallback to email_content (could be HTML or EmailBuilder JSON)
                    post_data["template_content"] = content.get("email_content", "")

                # MJML content for email services (if available)
                if content.get("mjml_content"):
                    post_data["mjml_content"] = content.get("mjml_content", "")
                if content.get("css_content"):
                    post_data["css_content"] = content.get("css_content", "")

                # EmailBuilder blocks content for editing (if available)
                if content.get("block_content"):
                    post_data["block_content"] = content.get("block_content", "")

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


@frappe.whitelist()
def check_email_queue_and_update_status(action_name, social_name, talent_email, subject):
    """
    Check Email Queue status và update Mira Campaign Social status
    Được gọi từ background job sau khi gửi email
    """
    logger = frappe.logger()
    try:
        logger.info(f"[EMAIL] ========== START check_email_queue_and_update_status ==========")
        logger.info(f"[EMAIL] Action: {action_name}")
        logger.info(f"[EMAIL] Social: {social_name}")
        logger.info(f"[EMAIL] Talent Email: {talent_email}")
        logger.info(f"[EMAIL] Subject: {subject[:50]}")
        
        # Load documents trước
        action = None
        if action_name:
            try:
                action = frappe.get_doc("Mira Action", action_name)
                logger.info(f"[EMAIL] Current Action status: {action.status}")
            except Exception as e:
                logger.warning(f"[EMAIL] Action {action_name} not found: {e}")
        
        social = frappe.get_doc("Mira Campaign Social", social_name)
        
        logger.info(f"[EMAIL] Current Social status: {social.status}")
        logger.info(f"[EMAIL] Current Social executed_at: {social.executed_at}")
        
        # Tìm Email Queue record gần nhất
        from frappe.utils import add_to_date
        time_filter = add_to_date(frappe.utils.now_datetime(), minutes=-10)
        logger.info(f"[EMAIL] Searching Email Queue: recipient={talent_email}, creation > {time_filter}")
        
        # Lấy tất cả Email Queue records gần đây (chỉ lấy fields cơ bản)
        email_queues = frappe.get_all(
            "Email Queue",
            filters={
                "creation": [">", time_filter]
            },
            fields=["name", "status", "modified", "error", "creation"],
            order_by="creation desc",
            limit=20
        )
        
        logger.info(f"[EMAIL] Found {len(email_queues)} Email Queue records (last 10 minutes)")
        
        # Filter trong Python code: check recipients và subject
        matching_queues = []
        for queue in email_queues:
            try:
                # Load full doc để lấy recipients và subject
                queue_doc = frappe.get_doc("Email Queue", queue.name)
                queue_recipients = getattr(queue_doc, 'recipients', '') or ''
                queue_subject = getattr(queue_doc, 'subject', '') or ''
                
                # Check recipient match
                recipient_match = talent_email.lower() in queue_recipients.lower() if queue_recipients else False
                # Check subject match (fuzzy)
                subject_match = False
                if subject and queue_subject:
                    subject_clean = subject[:50].lower().strip()
                    queue_subject_clean = queue_subject[:50].lower().strip()
                    subject_match = subject_clean in queue_subject_clean or queue_subject_clean in subject_clean
                
                if recipient_match and (subject_match or not subject):
                    matching_queues.append({
                        **queue,
                        'recipients': queue_recipients
                    })
                    logger.info(f"[EMAIL]   Match: {queue.name} | recipient={recipient_match} | subject={subject_match}")
            except Exception as e:
                logger.warning(f"[EMAIL]   Error loading queue {queue.name}: {e}")
                continue
        
        logger.info(f"[EMAIL] Found {len(matching_queues)} matching Email Queue records")
        if matching_queues:
            for idx, q in enumerate(matching_queues[:5]):
                logger.info(f"[EMAIL]   Queue {idx+1}: {q.name} | status={q.status} | subject={q.subject[:30] if q.subject else 'N/A'}")
        
        if not matching_queues:
            logger.warning(f"[EMAIL] ⚠️ No Email Queue found for {talent_email}")
            return {"success": False, "message": "No Email Queue found"}
        
        latest_queue = matching_queues[0]
        logger.info(f"[EMAIL] 📧 Using Email Queue {latest_queue.name} with status: {latest_queue.status}")
        
        if latest_queue.status == "Sent":
            # Email đã gửi thành công
            logger.info(f"[EMAIL] ✅ Email Queue status = Sent, updating to Success...")
            
            # Update action nếu có
            if action:
                action.status = "EXECUTED"
                action.execution_result = {
                    "status": "Success",
                    "message": f"[EMAIL] Sent to {talent_email} — Email Queue: {latest_queue.name}",
                    "email_queue_status": latest_queue.status,
                    "email_queue_name": latest_queue.name
                }
            
            # Update social
            social.status = "Success"
            # Dùng modified thay vì sent_at (vì sent_at không tồn tại trong Email Queue)
            social.executed_at = latest_queue.modified or frappe.utils.now_datetime()
            social.share_at = latest_queue.modified or frappe.utils.now_datetime()
            social.error_message = None  # Clear error message
            social.response_data = {
                "status": "Success",
                "message": f"[EMAIL] Sent to {talent_email} — Email Queue: {latest_queue.name}",
                "email_queue_status": latest_queue.status,
                "email_queue_name": latest_queue.name
            }
            
            logger.info(f"[EMAIL] Before save - social.status={social.status}, social.executed_at={social.executed_at}")
            logger.info(f"[EMAIL] ✅ Prepared data for save")
        elif latest_queue.status in ["Error", "Not Sent"]:
            # Email gửi thất bại
            if action:
                action.status = "FAILED"
                action.execution_result = {
                    "error": f"[EMAIL] Failed to send to {talent_email} — Email Queue: {latest_queue.name}",
                    "email_queue_status": latest_queue.status,
                    "email_queue_error": latest_queue.error
                }
            
            social.status = "Failed"
            social.response_data = {
                "error": f"[EMAIL] Failed to send to {talent_email} — Email Queue: {latest_queue.name}",
                "email_queue_status": latest_queue.status,
                "email_queue_error": latest_queue.error
            }
            social.error_message = latest_queue.error or f"Email Queue status: {latest_queue.status}"
            logger.warning(f"[EMAIL] ❌ Updated to Failed")
        else:
            # Status là "Queued" hoặc "Sending" - vẫn đang xử lý
            # Enqueue lại để check sau (tối đa 3 lần)
            # Check retry count từ execution_result hoặc response_data
            retry_count = 0
            if action and action.execution_result and isinstance(action.execution_result, dict):
                retry_count = action.execution_result.get("_retry_check_count", 0)
            elif social.response_data and isinstance(social.response_data, dict):
                retry_count = social.response_data.get("_retry_check_count", 0)
            
            if retry_count < 3:
                # Update retry count
                if action:
                    if not action.execution_result:
                        action.execution_result = {}
                    if not isinstance(action.execution_result, dict):
                        action.execution_result = {"status": "Processing"}
                    action.execution_result["_retry_check_count"] = retry_count + 1
                    action.execution_result["email_queue_status"] = latest_queue.status
                    action.save(ignore_permissions=True)
                
                if not social.response_data:
                    social.response_data = {}
                if not isinstance(social.response_data, dict):
                    social.response_data = {"status": "Processing"}
                social.response_data["_retry_check_count"] = retry_count + 1
                social.response_data["email_queue_status"] = latest_queue.status
                social.save(ignore_permissions=True)
                
                # Enqueue lại sau 5 giây
                frappe.enqueue(
                    "mbw_mira.api.campaign_social.check_email_queue_and_update_status",
                    action_name=action_name,
                    social_name=social_name,
                    talent_email=talent_email,
                    subject=subject,
                    queue="short",
                    job_name=f"check_email_queue_{action_name or 'test'}_{retry_count + 1}",
                    delay=5  # Đợi 5 giây trước khi check lại
                )
                logger.info(f"[EMAIL] ⏳ Status: {latest_queue.status}, will retry (attempt {retry_count + 1}/3)")
                return {"success": True, "message": f"Status: {latest_queue.status}, will retry"}
            else:
                # Đã retry 3 lần nhưng vẫn chưa có kết quả - set Processing
                social.status = "Processing"
                social.error_message = f"Email Queue status: {latest_queue.status} (checked 3 times)"
                logger.warning(f"[EMAIL] ⚠️ Max retries reached, status: {latest_queue.status}")
        
        # Save và commit
        logger.info(f"[EMAIL] ========== SAVING ==========")
        if action:
            logger.info(f"[EMAIL] Before save - Action status: {action.status}")
        logger.info(f"[EMAIL] Before save - Social status: {social.status}")
        logger.info(f"[EMAIL] Before save - Social executed_at: {social.executed_at}")
        
        try:
            if action:
                action.save(ignore_permissions=True)
                logger.info(f"[EMAIL] ✅ Action saved: {action.name} status={action.status}")
        except Exception as e:
            logger.error(f"[EMAIL] ❌ Error saving action: {e}")
            logger.error(f"[EMAIL] Traceback: {frappe.get_traceback()}")
        
        try:
            social.save(ignore_permissions=True)
            logger.info(f"[EMAIL] ✅ Social saved: {social.name} status={social.status}, executed_at={social.executed_at}")
        except Exception as e:
            logger.error(f"[EMAIL] ❌ Error saving social: {e}")
            logger.error(f"[EMAIL] Traceback: {frappe.get_traceback()}")
        
        try:
            frappe.db.commit()
            logger.info(f"[EMAIL] ✅ Database committed")
        except Exception as e:
            logger.error(f"[EMAIL] ❌ Error committing: {e}")
            logger.error(f"[EMAIL] Traceback: {frappe.get_traceback()}")
        
        # Verify sau khi save
        try:
            social_reload = frappe.get_doc("Mira Campaign Social", social_name)
            logger.info(f"[EMAIL] ========== VERIFICATION ==========")
            logger.info(f"[EMAIL] After save - Social status: {social_reload.status}")
            logger.info(f"[EMAIL] After save - Social executed_at: {social_reload.executed_at}")
            if action:
                logger.info(f"[EMAIL] After save - Action status: {action.status}")
            logger.info(f"[EMAIL] ========== END check_email_queue_and_update_status ==========")
        except Exception as e:
            logger.error(f"[EMAIL] ❌ Error verifying: {e}")
        
        return {"success": True, "message": f"Status updated to {social.status}"}
        
    except Exception as e:
        logger.error(f"[EMAIL] ❌ Exception in check_email_queue_and_update_status: {e}")
        logger.error(f"[EMAIL] Traceback: {frappe.get_traceback()}")
        frappe.log_error(frappe.get_traceback(), "Check Email Queue and Update Status Error")
        return {"success": False, "message": str(e)}
