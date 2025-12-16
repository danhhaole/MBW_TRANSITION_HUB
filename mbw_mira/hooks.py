app_name = "mbw_mira"
app_title = "Talent CRM"
app_publisher = "MBWCloud Co."
app_description = "MBW Talent CRM"
app_icon_url = "/assets/mbw_mira/images/mira-logo.png"
app_icon_title = "Talent CRM"
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
        "title": "Talent CRM",
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
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "mbw_mira.utils.jinja_methods",
# 	"filters": "mbw_mira.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "mbw_mira.install.before_install"
after_install = "mbw_mira.install.after_install"
after_migrate = "mbw_mira.install.seed_mbw_mira_features_if_ready"

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
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    "cron": {
        "0/1 * * * *": [
            "mbw_mira.schedulers.sync_candidates_queue.run",
            "mbw_mira.schedulers.task_campaign_social.run_campaign_social_facebook",
            "mbw_mira.schedulers.task_campaign_social.run_campaign_social_zalo",
            "mbw_mira.schedulers.task_campaign_social.run_campaign_social_topcv",
            "mbw_mira.schedulers.task_campaign_social.run_campaign_social_email",
            "mbw_mira.schedulers.task_action.send_email_action_campaign",
            "mbw_mira.schedulers.auto_segment_talent_profiles.run_enroll_talent_pool",
            "mbw_mira.schedulers.auto_segment_talent_profiles.run_disenroll_talent_pool",
        ],
        # "0/5 * * * *": [
        #     "mbw_mira.utils.email_tracking_scheduler.run_email_tracking_check",
        # ],
        "0/2 * * * *": [
            "mbw_mira.schedulers.task_mira_flow.schedule_message_tasks",
            "mbw_mira.schedulers.task_mira_flow.schedule_sms_tasks",
            "mbw_mira.schedulers.task_mira_flow.schedule_email_tasks",
            "mbw_mira.schedulers.task_mira_flow.schedule_zalo_tasks",
            "mbw_mira.schedulers.task_mira_flow.schedule_start_flow_tasks",
            "mbw_mira.schedulers.task_mira_flow.schedule_smart_delay_tasks",
            "mbw_mira.schedulers.task_mira_flow.schedule_add_tag_tasks",
            "mbw_mira.schedulers.task_mira_flow.schedule_remove_tag_tasks",
            "mbw_mira.schedulers.task_mira_flow.schedule_add_custom_field_tasks",
            "mbw_mira.schedulers.task_mira_flow.schedule_remove_custom_field_tasks",
            "mbw_mira.schedulers.task_mira_flow.schedule_lead_score_tasks",
            "mbw_mira.schedulers.task_mira_flow.schedule_external_request_tasks",
            "mbw_mira.schedulers.task_mira_flow.schedule_sent_notification_tasks",
            "mbw_mira.schedulers.task_mira_flow.schedule_unsubscribe_tasks",


        ],
    },
    "daily": [
        "mbw_mira.schedulers.task_talent_pool_cold.scan_talent_pool_interaction_cold",
        "mbw_mira.utils.birthday_scheduler.run_daily_birthday_check_scheduler"
    ],
    "hourly": [
        # "mbw_mira.schedulers.enroll_talent_campaign.run",
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
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "mbw_mira.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["mbw_mira.utils.before_request"]
# after_request = ["mbw_mira.utils.after_request"]

# Job Events
# ----------
# before_job = ["mbw_mira.utils.before_job"]
# after_job = ["mbw_mira.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"mbw_mira.auth.after_login",
#  "mbw_mira.auth.after_logout",
#  "mbw_mira.auth.on_login_failed",
#  "mbw_mira.auth.before_login",
#  "mbw_mira.auth.before_logout",
#  "mbw_mira.auth.on_session_creation"
# ]

# Automatically update python controller files with type annotations for this app
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
website_route_rules = [
    {"from_route": "/mbw_mira/<path:app_path>", "to_route": "mbw_mira"},
    {
        "from_route": "/track/open",
        "to_route": "mbw_mira.api.interaction.tracking_pixel",
    },
    {
        "from_route": "/track/click",
        "to_route": "mbw_mira.api.interaction.click_redirect",
    },
    {"from_route": "/track/event", "to_route": "mbw_mira.api.interaction.track"},
    {"from_route": "/unsubscribe", "to_route": "mbw_mira.api.email.unsubscribe"},
]

