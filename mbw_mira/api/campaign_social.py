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
