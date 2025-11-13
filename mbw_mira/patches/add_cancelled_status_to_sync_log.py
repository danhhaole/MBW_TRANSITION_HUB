import frappe

def execute():
    """
    Add 'Cancelled' status to Mira ATS Sync Log status field
    """
    try:
        # Get the doctype
        doctype_name = "Mira ATS Sync Log"
        
        # Check if doctype exists
        if not frappe.db.exists("DocType", doctype_name):
            return
            
        # Get the doctype document
        doc = frappe.get_doc("DocType", doctype_name)
        
        # Find the status field
        status_field = None
        for field in doc.fields:
            if field.fieldname == "status":
                status_field = field
                break
        
        if status_field:
            # Check if 'Cancelled' is already in options
            current_options = status_field.options or ""
            if "Cancelled" not in current_options:
                # Add 'Cancelled' to the options
                new_options = current_options + "\nCancelled"
                status_field.options = new_options
                
                # Save the doctype
                doc.save()
                
                print(f"Added 'Cancelled' status to {doctype_name}")
            else:
                print(f"'Cancelled' status already exists in {doctype_name}")
        else:
            print(f"Status field not found in {doctype_name}")
            
    except Exception as e:
        print(f"Error updating {doctype_name}: {str(e)}")
        frappe.log_error(f"Failed to add Cancelled status: {str(e)}", "Patch Error")
