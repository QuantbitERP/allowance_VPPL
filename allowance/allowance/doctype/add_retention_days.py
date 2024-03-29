import frappe
from frappe import _
from datetime import datetime,date

@frappe.whitelist()
def get_retention(start_date, end_date, employee_name):
    start_date = datetime.strptime(str(start_date), "%Y-%m-%d") 
    end_date = datetime.strptime(str(end_date), "%Y-%m-%d")   

    doc_list = frappe.get_all("HRA and Medical Allowance Details",
                              filters={
                                       "employee": employee_name,'docstatus':1,"start_date": start_date.date(),
                                       "end_date":end_date.date(),
                                      },
                              fields=["retention_days"],limit=1,order_by="creation desc"
    )
    if doc_list:
        return float(doc_list[0].get("retention_days"))
    else:
        return 0