# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import datetime
import frappe
from frappe.model.document import Document
from dateutil import parser
import math
import calendar
from frappe import _

@frappe.whitelist()
def round_val(allo):
	rounded_get = allo // 1
	c=allo-rounded_get
	if c<0.50:
		res=math.floor(allo)
	else:
		res=math.ceil(allo)
	return res


class AllowanceCalculation(Document):
	@frappe.whitelist() 
	def get_Details(self):
		# frappe.throw("hiii")
		if(not self.branch):
			frappe.throw("Please Select the Branch")
		if(not self.company):
			frappe.throw("Please Select the Company")
		emp = frappe.db.get_all("Employee",fields=["name", "last_name", "middle_name", "first_name", "employee_name", "designation","grade"],filters={"company":self.company,"branch":self.branch,"status":"Active"})		
		# frappe.throw(str(emp))
		for i in emp:
			# frappe.throw(str(i))
			temp=str(self.date)
			lst=temp.split('-')
			year=int(lst[0])
			month=int(lst[1])
			date=int(lst[2])
			count=0
			present_days=0
			retension_days=half_days=0
			present_days=frappe.db.count('Attendance', {'docstatus':1,'company':self.company,'status': ['in', ['Present', 'Work From Home']],'attendance_date': ["between", [self.from_date, self.date]],"employee":i.name,"retation_status":'Not'})  
			half_days = frappe.db.count('Attendance', {'docstatus':1,'company':self.company,'status': 'Half Day','attendance_date': ["between", [self.from_date, self.date]],"employee":i.name,"retation_status":'Not'})  
			half_days=half_days*0.5
			# frappe.throw(str(half_days))
			present_days=present_days+half_days
			present_days_list=frappe.get_all('Attendance', {
				'status': ['in', ['Present', 'Work From Home','Half Day']],'docstatus':1,'company':self.company,
				'attendance_date': ['between', [self.from_date, self.date]],
				'employee': i.name,
				"retation_status":'Not'
			}, ["attendance_date"])
			# frappe.throw(str(present_days_list))

			retension_days = frappe.db.count('Attendance', {'status': 'Present','docstatus':1,'company':self.company,'attendance_date': ["between", [self.from_date, self.date]],"employee":i.name,"retation_status":'On Retation','custom_out_duty_status':'Not'}) 
			# frappe.throw(str(retension_days))
			retension_amt_basic = retension_amt_medi = retension_amt_hra  =retension_amt_da=retension_amt_fixed=retension_amt_personal_pay=0
			from_date = datetime.datetime.strptime(self.from_date, '%Y-%m-%d').date()
			basic_c = hra_c = personal_pay_c = fixed_allowance_c = dearness_allowance_c = medical_allowance_c = petrol_allowance = p_allowance_in_amount=petrol_amt= 0
			maintenance_amount=bhatta_amount=special_allowance=telephone_bhatta=0
			employee_payroll_li = frappe.db.sql("""
				SELECT basic_c, hra_c, personal_pay_c, fixed_allowance_c, dearness_allowance_c, medical_allowance_c,
					from_date, petrol_allowance, p_allowance_in_amount,maintenance_amount,bhatta_amount,special_allowance,telephone_bhatta
				FROM `tabEmployee Payroll` 
				WHERE parent = '{0}' ORDER BY from_date DESC
			""".format(i.name), as_dict=True)
			# frappe.throw(str(employee_payroll_li))
			if employee_payroll_li:
				for p in employee_payroll_li:
					if( p["from_date"]):
						if from_date >= p["from_date"]:
							basic_c = p["basic_c"]
							hra_c = p["hra_c"]
							personal_pay_c = p["personal_pay_c"]
							fixed_allowance_c = p["fixed_allowance_c"]   
							dearness_allowance_c = p["dearness_allowance_c"]
							medical_allowance_c = p["medical_allowance_c"]
							petrol_allowance = p["petrol_allowance"]
							p_allowance_in_amount = p["p_allowance_in_amount"]
							maintenance_amount=p["maintenance_amount"]
							bhatta_amount=p["bhatta_amount"]
							special_allowance=p["special_allowance"]
							telephone_bhatta=p["telephone_bhatta"]
							break
  
			if employee_payroll_li:
				#Below code for retention calculation
				retention_percentage=frappe.get_value("Employee Grade",{"name":i.grade},"retention_percentage")
				# frappe.throw(str(retention_percentage))
				if(retention_percentage):
					retension_amt_basic=(((float(basic_c)/date)*retension_days)*retention_percentage)/100
					retension_amt_medi=(((medical_allowance_c/date)*retension_days)*retention_percentage)/100
					retension_amt_hra=(((hra_c/date)*retension_days)*retention_percentage)/100
					if dearness_allowance_c is not None and date != 0:
						retension_amt_da = (((float(dearness_allowance_c) / date) * retension_days) * retention_percentage) / 100
					else:
						retension_amt_da = 0  # You can assign a default value or handle this case as needed
					retension_amt_fixed = (((fixed_allowance_c/date)*retension_days)*retention_percentage)/100
					retension_amt_personal_pay = (((personal_pay_c/date)*retension_days)*retention_percentage)/100
					
				#Below Program is for calculate petrol allowance
				on_season_present_days=0
				on_season_half_days=0
				off_season_present_days=0
				on_season_out_duty_present_days=0
				off_season_out_duty_present_days=0
				designation=False
				num_days=out_duty_count=half_day_out_duty=0
				num_days=calendar.monthrange(int(year), int(month))[1]
				season_list=frappe.get_all("Season For Payroll",{"enable":True,"docstatus":1,"branch":self.branch,"company":self.company},["season_start_date","season_end_date"])
				if(i.designation=="FIELD MAN" or i.designation=="SLIP BOY" or i.designation=="AGRI.OVERSIER"):
					petrol_rate=0
					temp=str(self.from_date)
					date_li=temp.split('-')
					month=date_li[1]
					year=date_li[0]
					month_obj = datetime.datetime.strptime(str(month), "%m")
					month_name = month_obj.strftime("%B")
					petrol_rate=frappe.get_value("Petrol Rate",{"branch":self.branch,"company":self.company,"month":month_name,"year":year,"date":['<=',self.from_date],"docstatus":1},"rate")
					if not petrol_rate or petrol_rate==None:
						petrol_rate=0
					designation=True
					if(season_list):
						for k in season_list:
							for m in present_days_list:
								if(m.attendance_date>=k.season_start_date and m.attendance_date<=k.season_end_date):
									if(m.status=="Half Day"):
										on_season_half_days+=1
									else:
										on_season_present_days+=1
						on_season_half_days=on_season_half_days*0.5
						on_season_present_days=on_season_present_days+on_season_half_days
						off_season_present_days=present_days-on_season_present_days
				if(designation):
					petrol_liter_amt=0
					if(i.designation=="FIELD MAN" or i.designation=="AGRI.OVERSIER"):
						petrol_liter_amt=petrol_allowance
					else:
						petrol_liter_amt=p_allowance_in_amount
					on_season_out_duty_half_day=0
					out_duty_li = frappe.db.sql("""
						SELECT attendance_date, name 
						FROM `tabAttendance` 
						WHERE docstatus = 1 
						AND employee = '{0}' 
						AND company = '{1}' 
						AND custom_out_duty_status = 'On Out Duty' 
						AND status IN ('Present', 'Half Day') 
						AND attendance_date BETWEEN '{2}' AND '{3}'
					""".format(i.name, self.company, self.from_date, self.date), as_dict=True)
					if(out_duty_li): 
						if(season_list):
							for k in season_list:
								for od in out_duty_li:
									if(od.attendance_date>=k.season_start_date and od.attendance_date<=k.season_end_date):
										if(od.status=="Half Day"):
											on_season_out_duty_half_day+=1
										else:
											on_season_out_duty_present_days+=1
					out_duty_count = frappe.db.count('Attendance', {'custom_out_duty_status':'On Out Duty','docstatus':1,'status': 'Present','attendance_date': ["between", [self.from_date, self.date]],"employee":i.name,"retation_status":'Not',"company":self.company})  #,"retation_status":'Not'
					half_day_out_duty = frappe.db.count('Attendance', {'custom_out_duty_status':'On Out Duty','docstatus':1,'status': 'Half Day','attendance_date': ["between", [self.from_date, self.date]],"employee":i.name,"retation_status":'Not',"company":self.company})  #,"retation_status":'Not'
					half_day_out_duty=half_day_out_duty*0.5
					out_duty_count=out_duty_count+half_day_out_duty
     
					on_season_out_duty_half_day=on_season_out_duty_half_day*0.5
					on_season_out_duty_present_days=on_season_out_duty_present_days+on_season_out_duty_half_day
					off_season_out_duty_present_days=out_duty_count-on_season_out_duty_present_days
     
					all_days_out_duty=True
					if(out_duty_count>=present_days):
						petrol_amt=0
						all_days_out_duty=False
	
					if(on_season_out_duty_present_days and all_days_out_duty):	
						on_season_present_days=on_season_present_days-on_season_out_duty_present_days
					if(off_season_out_duty_present_days and all_days_out_duty):	
						off_season_present_days=off_season_present_days-off_season_out_duty_present_days
					if(all_days_out_duty):
						if(i.designation=="FIELD MAN"):
							season_per,off_season_per=frappe.get_value("Designation",{'name':"FIELD MAN"},["season_rate","off_season_rate"])
							if(on_season_present_days):
								petrol_amt=petrol_amt+(((petrol_liter_amt*season_per*petrol_rate)/(100*num_days))*(on_season_present_days))
							if(off_season_present_days):
								petrol_amt=petrol_amt+(((petrol_liter_amt*off_season_per*petrol_rate)/(100*num_days))*(off_season_present_days))
						elif(i.designation=="AGRI.OVERSIER"):
							season_per,off_season_per=frappe.get_value("Designation",{'name':"AGRI.OVERSIER"},["season_rate","off_season_rate"])
							if(on_season_present_days):
								petrol_amt=petrol_amt+(((petrol_liter_amt*season_per*petrol_rate)/(100*num_days))*(on_season_present_days))
							if(off_season_present_days):
								petrol_amt=petrol_amt+(((petrol_liter_amt*off_season_per*petrol_rate)/(100*num_days))*(off_season_present_days))
						else:
							season_per,off_season_per=frappe.get_value("Designation",{'name':"SLIP BOY"},["season_rate","off_season_rate"])
							if(on_season_present_days):
								petrol_amt=((petrol_liter_amt*season_per)/(100*num_days))*(on_season_present_days)
							if(off_season_present_days):
								petrol_amt=((petrol_liter_amt*off_season_per)/(100*num_days))*(off_season_present_days)
																																																																				
				#below code is used to calculate HRA Deduction amount
				self_to_date = datetime.datetime.strptime(str(self.date), "%Y-%m-%d").date()
				self_from_date = datetime.datetime.strptime(str(self.from_date), "%Y-%m-%d").date()
				guest_house_li = frappe.get_all('Guest House Allotment List', {"parent": i.name}, ["from_date", "to_date"])
				total_guest_house_days = 0
				if(guest_house_li):
					for allotment in guest_house_li:
						if(allotment["from_date"]):
							from_date =allotment["from_date"]
							to_date=None
							if(allotment["to_date"]):
								to_date = allotment["to_date"]						
							if(to_date):
								if (to_date <= self_to_date and to_date >= self_from_date) or (from_date <= self_from_date and to_date >= self_from_date) or (from_date >= self_from_date and from_date <= self_to_date):
									start_date = max(from_date, self_from_date)
									end_date = min(to_date, self_to_date)
									days = (end_date - start_date).days + 1
									total_guest_house_days += days
							else:
								if(from_date<=self_to_date):
									if(from_date>=self_from_date and from_date<=self_to_date):
										days = (self_to_date - from_date).days + 1
										total_guest_house_days += days
									else:
										total_guest_house_days+=num_days
          
				#Below code content HRA Calculation
				medical_allow=hra=hra_deduction=0
				if(retension_days==0):
					if(present_days>=20):
						medical_allow=medical_allowance_c
						hra=hra_c
					elif(present_days<=19):
						medical_allow=((medical_allowance_c/date)*(present_days))
						hra=((hra_c/date)*(present_days)) 
				else:
					medical_allow=(((medical_allowance_c/date)*(present_days))+retension_amt_medi) if present_days!=0 else retension_amt_medi
					hra=(((hra_c/date)*(present_days))+retension_amt_hra) if present_days!=0 else retension_amt_hra
				if(total_guest_house_days and hra and num_days):
					hra_deduction=((hra/num_days)*total_guest_house_days)
				#below code is used to add overtime amount for particular employee
				overtime_amt=0
				overtime_amt=frappe.get_value("Employee Overtime Amount",{"employee_id":i.name,"start_date":self.from_date,"end_date":self.date,"docstatus":1},"total_overtime_amount")
				#below code is used to add Bonus amount for particular employee
				bonus_amt=0
				bonus_amt=frappe.get_value("EB Bonus Amount Calculation",{"employee_id":i.name,"from_date":self.from_date,"to_date":self.date,"docstatus":1},"total_bonus_amount")
				#below code to calculate Additional Amount
				if(maintenance_amount):
					maintenance_amount=(maintenance_amount/num_days)*present_days
				if(bhatta_amount):
					bhatta_amount=(bhatta_amount/num_days)*present_days
				if(special_allowance):
					if(present_days>=15):
						special_allowance=special_allowance
					else:
						special_allowance=(special_allowance/num_days)*present_days
				if(telephone_bhatta):
					if(present_days>=15):
						telephone_bhatta=telephone_bhatta
					else:
						telephone_bhatta=(telephone_bhatta/num_days)*present_days
      
				self.append("hra_and_medical_allowance_details",
				{
					"employee": i.name,
					"employee_name": i.employee_name,
					"grade": i.grade,
					"retention_days":retension_days,
					"basic":((float(basic_c)/date)*(present_days))+retension_amt_basic if present_days!=0 else retension_amt_basic,
					"medical_allowance":medical_allow,
					"hra": hra,
					"fixed_allowance": ((fixed_allowance_c/date)*(present_days))+retension_amt_fixed  if present_days!=0 else retension_amt_fixed,
					"personal_pay":((float(personal_pay_c)/date)*(present_days))+retension_amt_personal_pay if present_days!=0 else retension_amt_personal_pay,
					"dearness_allowance":((float(dearness_allowance_c)/date)*(present_days))+retension_amt_da if present_days!=0 else retension_amt_da,
					"petrol_allowance":petrol_amt,
					"overtime_value":overtime_amt,
					"bonus_amount":bonus_amt,
					"present_days":present_days,
					"hra_deduction":hra_deduction,
					"maintenance_amount":maintenance_amount,
					"bhatta_amount":bhatta_amount,
					"special_allowance":special_allowance,
					"telephone_bhatta":telephone_bhatta,
					"out_duty_days":out_duty_count,
					"start_date":self.from_date,
					"end_date":self.date
				},)
		# frappe.msgprint(str(present_days))

	@frappe.whitelist()
	def get_month_dates(self,input_date):
		selected_date = str(input_date)
		date_li = selected_date.split("-")
		year= int(date_li[0])
		month_num = int(date_li[1])
		num_days_in_month = calendar.monthrange(year,month_num)[1]
		start_date = datetime.datetime(year,month_num, 1).date()
		end_date = datetime.datetime(year, month_num, num_days_in_month).date()
		date_li = str(start_date).split("-")
		self.year = date_li[0]
		month_num = int(date_li[1])
		self.month = _(calendar.month_name[month_num]) 
		self.from_date=start_date
		self.date=end_date


	@frappe.whitelist()
	def on_submit(self):
		for i in self.get('hra_and_medical_allowance_details'):
			doc_name=frappe.get_value("Salary Structure Assignment",{"employee":i.employee},"name")	
			frappe.db.set_value("Salary Structure Assignment", doc_name, "base", round_val(i.basic))
			frappe.db.set_value("Salary Structure Assignment", doc_name, "medical_allowance", round_val(i.medical_allowance))
			frappe.db.set_value("Salary Structure Assignment", doc_name, "hra_ssa", round_val(i.hra))
			frappe.db.set_value("Salary Structure Assignment", doc_name, "fixed_allowance", round_val(i.fixed_allowance))
			frappe.db.set_value("Salary Structure Assignment", doc_name, "da", round_val(i.dearness_allowance))
			frappe.db.set_value("Salary Structure Assignment", doc_name, "personal_pay", round_val(i.personal_pay))
			frappe.db.set_value("Salary Structure Assignment", doc_name, "petrol_allowance", round_val(i.petrol_allowance))
			frappe.db.set_value("Salary Structure Assignment", doc_name, "total_over_allowance", round_val(i.overtime_value))
			frappe.db.set_value("Salary Structure Assignment", doc_name, "bonus_amount", round_val(i.bonus_amount))
			frappe.db.set_value("Salary Structure Assignment", doc_name, "hra_deduction_amount", round_val(i.hra_deduction))
			frappe.db.set_value("Salary Structure Assignment", doc_name, "maintenance_amt", round_val(i.maintenance_amount))
			frappe.db.set_value("Salary Structure Assignment", doc_name, "bhatta_amt", round_val(i.bhatta_amount))
			frappe.db.set_value("Salary Structure Assignment", doc_name, "special_allowance_amt", round_val(i.special_allowance))
			frappe.db.set_value("Salary Structure Assignment", doc_name, "telephone_bhatta_amt", round_val(i.telephone_bhatta))

