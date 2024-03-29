# Copyright (c) 2024, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SeasonForPayroll(Document):
	@frappe.whitelist()
	def check_dates(self):
		if(self.season_end_date and self.season_start_date):
			if(self.season_end_date < self.season_start_date):
				frappe.throw("From Date can not greater than To Date")
			
	def before_save(self):
		self.check_dates()
