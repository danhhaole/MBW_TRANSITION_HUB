import frappe
from frappe import _

@frappe.whitelist()
def get_automation_counts(doctypes=None):
    """
    Get record counts for multiple doctypes
    
    Args:
        doctypes: List of doctype names or comma-separated string
        
    Returns:
        dict: Dictionary with doctype names as keys and counts as values
        
    Example:
        get_automation_counts(['Mira Campaign', 'Mira Flow', 'Mira Sequence'])
        Returns: {
            'Mira Campaign': 10,
            'Mira Flow': 5,
            'Mira Sequence': 12
        }
    """
    try:
        # Parse doctypes parameter
        if isinstance(doctypes, str):
            doctypes = [dt.strip() for dt in doctypes.split(',')]
        
        if not doctypes:
            doctypes = ['Mira Campaign', 'Mira Flow', 'Mira Sequence']
        
        counts = {}
        
        for doctype in doctypes:
            try:
                # Check if user has permission to read this doctype
                if frappe.has_permission(doctype, "read"):
                    count = frappe.db.count(doctype)
                    counts[doctype] = count
                else:
                    counts[doctype] = 0
            except Exception as e:
                frappe.log_error(f"Error getting count for {doctype}: {str(e)}")
                counts[doctype] = 0
        
        return {
            'success': True,
            'data': counts
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_automation_counts: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'data': {}
        }


@frappe.whitelist()
def get_automation_stats(filters=None):
    """
    Get detailed statistics for automation doctypes with optional filters
    
    Args:
        filters: Optional filters dict for each doctype
        
    Returns:
        dict: Detailed statistics including counts by status
        
    Example:
        Returns: {
            'campaigns': {
                'total': 10,
                'active': 5,
                'draft': 3,
                'paused': 2
            },
            'flows': {
                'total': 5,
                'active': 3,
                'draft': 2
            },
            'sequences': {
                'total': 12,
                'active': 8,
                'draft': 4
            }
        }
    """
    try:
        stats = {}
        
        # Campaign stats
        try:
            stats['campaigns'] = {
                'total': frappe.db.count('Mira Campaign'),
                'active': frappe.db.count('Mira Campaign', {'status': 'Active'}),
                'draft': frappe.db.count('Mira Campaign', {'status': 'Draft'}),
                'paused': frappe.db.count('Mira Campaign', {'status': 'Paused'}),
                'completed': frappe.db.count('Mira Campaign', {'status': 'Completed'})
            }
        except Exception as e:
            frappe.log_error(f"Error getting campaign stats: {str(e)}")
            stats['campaigns'] = {'total': 0, 'active': 0, 'draft': 0, 'paused': 0, 'completed': 0}
        
        # Flow stats - chỉ lấy type = 'Automation'
        try:
            stats['flows'] = {
                'total': frappe.db.count('Mira Flow', {'type': 'Automation'}),
                'active': frappe.db.count('Mira Flow', {'type': 'Automation', 'status': 'Active'}),
                'draft': frappe.db.count('Mira Flow', {'type': 'Automation', 'status': 'Draft'}),
                'paused': frappe.db.count('Mira Flow', {'type': 'Automation', 'status': 'Paused'}),
                'archived': frappe.db.count('Mira Flow', {'type': 'Automation', 'status': 'Archived'})
            }
        except Exception as e:
            frappe.log_error(f"Error getting flow stats: {str(e)}")
            stats['flows'] = {'total': 0, 'active': 0, 'draft': 0, 'paused': 0, 'archived': 0}
        
        # Sequence stats
        try:
            stats['sequences'] = {
                'total': frappe.db.count('Mira Sequence'),
                'active': frappe.db.count('Mira Sequence', {'status': 'Active'}),
                'draft': frappe.db.count('Mira Sequence', {'status': 'Draft'}),
                'paused': frappe.db.count('Mira Sequence', {'status': 'Paused'}),
                'completed': frappe.db.count('Mira Sequence', {'status': 'Completed'})
            }
        except Exception as e:
            frappe.log_error(f"Error getting sequence stats: {str(e)}")
            stats['sequences'] = {'total': 0, 'active': 0, 'draft': 0, 'paused': 0, 'completed': 0}
        
        # Flow Template stats
        try:
            stats['flowTemplates'] = {
                'total': frappe.db.count('Mira Flow Template', {'is_delete': 0}),
                'system': frappe.db.count('Mira Flow Template', {'is_delete': 0, 'is_default': 1}),
                'my': frappe.db.count('Mira Flow Template', {'is_delete': 0, 'is_default': 0})
            }
        except Exception as e:
            frappe.log_error(f"Error getting flow template stats: {str(e)}")
            stats['flowTemplates'] = {'total': 0, 'system': 0, 'my': 0}
        
        return {
            'success': True,
            'data': stats
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_automation_stats: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'data': {}
        }
