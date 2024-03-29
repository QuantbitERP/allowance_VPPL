// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt


frappe.ui.form.on('Allowance Calculation', {
	refresh: function(frm) {
		$('.layout-side-section').hide();
		$('.layout-main-section-wrapper').css('margin-left', '0');
	},
	get_details: function (frm) {
		frm.clear_table("hra_and_medical_allowance_details")
		frm.refresh_field("hra_and_medical_allowance_details")
		frm.call({
			method:'get_Details',
			doc: frm.doc,
		});
	},
	from_date: function (frm) {
		frm.clear_table("hra_and_medical_allowance_details")
		frm.refresh_field("hra_and_medical_allowance_details")
	},
	date: function (frm) {
		frm.clear_table("hra_and_medical_allowance_details")
		frm.refresh_field("hra_and_medical_allowance_details")
	}
});
frappe.ui.form.on('Allowance Calculation', {
	from_date: function (frm) {
		frm.call({
			method:"get_month_dates",
			doc:frm.doc,
			args:{
				"input_date":frm.doc.from_date
			}
		})
	}
});

frappe.ui.form.on('Allowance Calculation', {
	date: function (frm) {
		frm.call({
			method:"get_month_dates",
			doc:frm.doc,
			args:{
				"input_date":frm.doc.date
			}
		})
	}
});
