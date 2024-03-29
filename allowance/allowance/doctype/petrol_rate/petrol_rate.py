# Copyright (c) 2024, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
import datetime
from frappe.model.document import Document

class PetrolRate(Document):
	@frappe.whitelist()
	def get_month_yaer(self):
		date=str(self.date)
		temp=date.split('-')
		month=int(temp[1])
		year=int(temp[0])
		month_obj = datetime.datetime.strptime(str(month), "%m")
		month_name = month_obj.strftime("%B")
		self.month=month_name
		self.year=year


