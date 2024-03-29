# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from dateutil import parser
from datetime import timedelta, datetime,date

class Retention(Document):
	@frappe.whitelist()
	def check_dates(self):
		if(self.to_date and self.from_date):
			if(self.to_date < self.from_date):
				frappe.throw("From Date can not greater than To Date")
    
	@frappe.whitelist()
	def before_save(self):
		self.check_dates()
		today_date=date.today()
		if(self.to_date):
			to_date=datetime.strptime(self.to_date,'%Y-%m-%d')
			today_date=datetime.strptime(str(today_date),'%Y-%m-%d')
			if(to_date>today_date):
				frappe.throw("You can not mark future attendance")
	
     
     
		# emp=frappe.db.get_list("Employee",fields=["name","on_retention"],filters={"name":self.employee})
		# for i in emp:
		# 	if str(self.to_date)=="None" or self.to_date=='' or str(self.to_date)=='' or self.to_date=="None":
		# 		frappe.db.set_value("Employee", i.name, "on_retention", 1)
		# 	else:
		# 		frappe.db.set_value("Employee", i.name, "on_retention", 0)

		# 	data = frappe.db.sql("""
		# 							select status,retation_status,name,attendance_date from `tabAttendance` where employee = %(empid)s
        #  							and attendance_date between %(from_date)s and %(to_date)s
		# 								""",{
		# 					'empid': self.employee	,	'from_date': self.from_date,'to_date': self.to_date
		# 				},  as_dict=1)	
		# if data:
		# 	for row in data:
		# 		frappe.db.set_value('Attendance',row.name , 'retation_status', 'On Retation')
		# else:
  
	def on_submit(self):
		today_date=date.today()
		if(self.to_date):
			to_date=datetime.strptime(self.to_date,'%Y-%m-%d')
			today_date=datetime.strptime(str(today_date),'%Y-%m-%d')
			if(to_date>today_date):
				frappe.throw("You can not mark future attendance")
		if(not self.to_date):
			frappe.throw("Please select the to date before submitting form")
		else:
			start_date = datetime.strptime(self.from_date, "%Y-%m-%d")  
			end_date = datetime.strptime(self.to_date, "%Y-%m-%d")   

			while start_date <= end_date:
				attendance_doc = {
					"doctype": "Attendance",
					"employee": self.employee,
					"status": "Present",
					"attendance_date": start_date.date(),
					"retation_status": "On Retation",
					"company":self.company,
					"docstatus":"1",
				}

				frappe.get_doc(attendance_doc).insert(ignore_permissions=True)
				start_date += timedelta(days=1)


	@frappe.whitelist()
	def calculate_total_days(self):
		if self.from_date:
			from_date = parser.parse(self.from_date)
			to_date = parser.parse(self.to_date)

			self.total_days = ((to_date - from_date).days)+1
   
   
	def on_cancel(self):
		if(self.to_date):
			data = frappe.db.sql("""
									select name from `tabAttendance` where employee = %(empid)s
									and attendance_date between %(from_date)s and %(to_date)s and docstatus=1
								""",{
								'empid': self.employee,'from_date': self.from_date,'to_date': self.to_date
							},  as_dict=1)	
			if data:
				for row in data:
					frappe.db.set_value('Attendance',row.name ,'docstatus',2)
					frappe.delete_doc('Attendance',row.name)

