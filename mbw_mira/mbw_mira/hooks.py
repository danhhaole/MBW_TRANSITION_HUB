app_name = "mbw_mira"
app_title = "MBW Mira"
app_publisher = "MBWCloud Co."
app_description = "MBW Mira Talent Pool"
app_icon_url = "/assets/mbw_mira/images/mira-logo.png"
app_icon_title = "MBW Mira"
app_icon_route = "/mbw_mira"
app_email = "dev@mbw.vn"
app_license = "agpl-3.0"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
add_to_apps_screen = [
    {
        "name": "mbw_mira",
        "logo": "/assets/mbw_mira/images/mira-logo.png",
        "title": "MBW Mira",
        "route": "/mbw_mira",
        # "has_permission": "mbw_mira.api.permission.has_app_permission"
    }
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/mbw_mira/css/mbw_mira.css"
# app_include_js = "/assets/mbw_mira/js/mbw_mira.js"

# include js, css files in header of web template
# web_include_css = "/assets/mbw_mira/css/mbw_mira.css"
# web_include_js = "/assets/mbw_mira/js/mbw_mira.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "mbw_mira/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "mbw_mira/public/icons.svg"

# Home Pages
# ----------
# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#     "Role": "home_page"
# }

# Generators
# ----------
# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------
# add methods and filters to jinja environment
# jinja = {
#     "methods": "mbw_mira.utils.jinja_methods",
#     "filters": "mbw_mira.utils.jinja_filters"
# }

# Installation
# ------------
# before_install = "mbw_mira.install.before_install"
# after_install = "mbw_mira.install.after_install"

# Uninstallation
# ------------
# before_uninstall = "mbw_mira.uninstall.before_uninstall"
# after_uninstall = "mbw_mira.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "mbw_mira.utils.before_app_install"
# after_app_install = "mbw_mira.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "mbw_mira.utils.before_app_uninstall"
# after_app_uninstall = "mbw_mira.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mbw_mira.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#     "Event":
#     "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#     "Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#     "ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#     "*": {
#         "on_update": "method",
#         "on_cancel": "method",
#         "on_trash": "method"
#     }
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    "cron": {
        "* * * * *": [  # ✅ Chạy mỗi phút
            "mbw_mira.schedulers.auto_share_social_posts.run"
        ],
        "0/1 * * * *": [
            "mbw_mira.schedulers.fetch_ats_mbw_campaigns.run",
            "mbw_mira.schedulers.excel_source_campaigns.run",
            "mbw_mira.schedulers.auto_segment_talent_profiles.run",
            "mbw_mira.schedulers.auto_share_social_posts.run",
        ],
        "0/2 * * * *": [
            "mbw_mira.schedulers.enroll_talent_campaign.run",
            "mbw_mira.schedulers.create_actions.run",
            "mbw_mira.schedulers.send_email_action.run",
            "mbw_mira.schedulers.send_sms_action.run",
            "mbw_mira.schedulers.auto_share_social_posts.run",
        ],
    },
    "daily": [
        # "mbw_mira.schedulers.fetch_ats_mbw_campaigns.run",
        "mbw_mira.schedulers.fetch_jobboard_topcv_campaigns.run",
        "mbw_mira.schedulers.fetch_jobboard_vietnamworks_campaigns.run",
        "mbw_mira.schedulers.fetch_social_facebook_campaigns.run",
        "mbw_mira.schedulers.fetch_social_linkedin_campaigns.run",
        "mbw_mira.schedulers.auto_share_social_posts.run",
    ],
    "hourly": [
        # "mbw_mira.schedulers.enroll_talent_campaign.run",
        # "mbw_mira.schedulers.send_email_action.run",
        # "mbw_mira.schedulers.send_sms_action.run",
        "mbw_mira.schedulers.auto_share_social_posts.run",
        # "mbw_mira.schedulers.create_actions.run",
        # "mbw_mira.schedulers.auto_segment_talent_profiles.run",
        # "mbw_mira.schedulers.excel_source_campaigns.run"
    ],
    # "weekly": [],
    # "monthly": [],
}


# Testing
# -------
# before_tests = "mbw_mira.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
    # "frappe.desk.doctype.event.event.get_events": "mbw_mira.event.get_events"
    "frappe.client.get_list": "mbw_mira.api.override.get_list_with_links"
}
# 