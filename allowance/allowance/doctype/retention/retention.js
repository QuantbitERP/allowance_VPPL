// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt
frappe.ui.form.on('Retention', {
	from_date: function(frm) {
		frm.call({
			method:"check_dates",
			doc:frm.doc
		})
	},
	to_date: function(frm) {
		frm.call({
			method:"check_dates",
			doc:frm.doc
		})
	},
});
frappe.ui.form.on('Retention', {
	to_date: function(frm) {
		frm.call({
			method:"calculate_total_days",
			doc:frm.doc
		})
	},
});
