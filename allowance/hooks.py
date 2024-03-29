from . import __version__ as app_version

app_name = "allowance"
app_title = "Allowance"
app_publisher = "Abhishek Chougule"
app_description = "Petrol Medical Retension Allowance"
app_email = "chouguleabhis@gmail.com"
app_license = "Dev-MrAbhi"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/allowance/css/allowance.css"
# app_include_js = "/assets/allowance/js/allowance.js"

# include js, css files in header of web template
# web_include_css = "/assets/allowance/css/allowance.css"
# web_include_js = "/assets/allowance/js/allowance.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "allowance/public/scss/website"

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

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "allowance.utils.jinja_methods",
#	"filters": "allowance.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "allowance.install.before_install"
# after_install = "allowance.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "allowance.uninstall.before_uninstall"
# after_uninstall = "allowance.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "allowance.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"allowance.tasks.all"
#	],
#	"daily": [
#		"allowance.tasks.daily"
#	],
#	"hourly": [
#		"allowance.tasks.hourly"
#	],
#	"weekly": [
#		"allowance.tasks.weekly"
#	],
#	"monthly": [
#		"allowance.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "allowance.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "allowance.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "allowance.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["allowance.utils.before_request"]
# after_request = ["allowance.utils.after_request"]

# Job Events
# ----------
# before_job = ["allowance.utils.before_job"]
# after_job = ["allowance.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"allowance.auth.validate"
# ]

fixtures = [
    {
        "doctype": "Employee Grade",
        "filters": [
            ["name", "in", ["SEMISKILLED", "UNSKILLED", "CLERICAL I","CLERICAL II","CLIRICAL IV","HIGHLY SKILLED"
            "MANAGERAL","SKILLED A","SKILLED B","SUPERVISORY A","SUPERVISORY B","SUPERVISORY C","CLERICAL III"]]
        ]
    },
    {
        "doctype": "Designation",
        "filters": [
            ["name", "in", ["FIELD MAN","SLIP BOY","AGRI.OVERSIER"]]
        ]
    },
     {
        "doctype": "Salary Component",
        "filters": [
            ["name", "in", ["Basic","Fixed Allowance","Dearness Allowance"]]
        ]
    },
      {
        "doctype": "Client Script",
        "filters": [
            ["name", "in", ["Salary Slip- Retention Days"]]
        ]
    }
]

