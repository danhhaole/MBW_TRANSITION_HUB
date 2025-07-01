
import frappe

def after_login():
    frappe.msgprint(f"Welcome!")

def after_logout():
    frappe.msgprint(f"Goodbye !")

def on_login_failed():
    frappe.log_error("Login failed for user: ")

def before_login(login_manager):
    # Custom pre-login logic (e.g., check if user is banned)
    pass

def before_logout(user):
    # Custom logic before logout
    pass

def on_session_creation(login_manager):
    # Called after login session is created
    pass

def custom_authenticate():
    # You can completely override how authentication works here
    # Your custom logic here
    pass
