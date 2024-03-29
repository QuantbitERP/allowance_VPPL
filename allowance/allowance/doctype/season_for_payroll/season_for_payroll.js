// Copyright (c) 2024, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('Season For Payroll', {
	season_start_date: function(frm) {
		frm.call({
			method:"check_dates",
			doc:frm.doc
		})
	},
	season_end_date: function(frm) {
		frm.call({
			method:"check_dates",
			doc:frm.doc
		})
	},
});
