# Copyright (c) 2024, Abhishek Chougule and contributors
# For license information, please see license.txt

from datetime import datetime
import frappe
from frappe.model.document import Document
import calendar
from frappe import _


class EmployeeBonus(Document):
	@frappe.whitelist()
	def get_components(self):
		comp_list=['Basic','Fixed Allowance','Dearness Allowance']
		for i in comp_list:
			check_com=frappe.get_value("Salary Component",{"name":i},"name")
			if(check_com):
				self.append('component_details',{
					"salary_component":i,
				})
			else:
				frappe.throw(f"'{i}' this component not present in Salary Component, please add it.")
		self.get_emp_list()
	
 
	def get_emp_list(self):
		filter={}
		filter["status"]="Active"
		if(self.company):
			filter["company"]=self.company
		if(self.branch):
			filter["branch"]=self.branch
		emp_li=frappe.get_all("Employee",filters=filter,fields=["name","employee_type","employee_name"])
		if(emp_li):
			for i in emp_li:
				self.append("employee_list",{
					"employee_id":i.name,
					"employee_name":i.employee_name,
					"employee_type":i.employee_type
				})
	
	@frappe.whitelist()
	def get_month_year(self):
		selected_date = self.bonus_apply_date
		date_li = selected_date.split("-")
		self.year = date_li[0]
		month_num = int(date_li[1])
		self.month = _(calendar.month_name[month_num]) 
			

	@frappe.whitelist()
	def selectall(self):
		children = self.get("employee_list")
		if not children:
			return
		all_selected = all([child.check for child in children])
		value = 0 if all_selected else 1
		for child in children:
			child.check = value	
   
	@frappe.whitelist()
	def get_emp_bonus(self):
		if(not self.working_employee_bonus_):
			frappe.throw("Please add the bonus percentage for Employee Type- Working")
		if(not self.retired_employee_bonus_):
			frappe.throw("Please add the bonus percentage for Employee Type- Retired")
		if(not self.from_date):
			frappe.throw("Please Select From Date In Previous Year Salary Slip Details Section")
		if(not self.to_date):
			frappe.throw("Please Select To Date In Previous Year Salary Slip Details Section")
  
		selected_date = self.bonus_apply_date
		date_li = selected_date.split("-")
		year= int(date_li[0])
		month_num = int(date_li[1])
		num_days_in_month = calendar.monthrange(year,month_num)[1]
		
		start_date = datetime(year,month_num, 1).date()
		end_date = datetime(year, month_num, num_days_in_month).date()
		

		comp_li=[]
		for k in self.get('component_details'):
			comp_li.append(str(k.salary_component))
		
		for i in self.get("employee_list"):
			if(i.check):
				prev_salary_amount=0
				bonus_amt=0
				bonus_per=0
				salary_slip_li=frappe.db.get_list("Salary Slip",fields=['name'],filters={'start_date':["between", [self.from_date, self.to_date]],"employee":i.employee_id,"docstatus":1})
				if(salary_slip_li):
					for j in salary_slip_li:
						doc=frappe.get_doc("Salary Slip",j.name)
						for k in doc.get('earnings'):
							if	k.salary_component in comp_li:
								prev_salary_amount=prev_salary_amount+k.amount
						if(prev_salary_amount>0):
								if(i.employee_type=="Working"):
									bonus_per=self.working_employee_bonus_
									bonus_amt=(prev_salary_amount*self.working_employee_bonus_)/100
								else:
									bonus_per=self.retired_employee_bonus_
									bonus_amt=(prev_salary_amount*self.retired_employee_bonus_)/100
								
					self.append('bonus_calculation',{
						"employee_id":i.employee_id,
						"employee_name":i.employee_name,
						"employee_type":i.employee_type,
						"bonus_percentage":bonus_per,
						"previous_total_amount":prev_salary_amount,
						"total_bonus_amount":bonus_amt,
						"from_date":start_date,
						"to_date":end_date
					})
