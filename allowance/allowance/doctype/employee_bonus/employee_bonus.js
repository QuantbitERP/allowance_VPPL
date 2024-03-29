// Copyright (c) 2024, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Bonus', {
	onload: function(frm) {
		frm.clear_table("component_details")
		frm.refresh_field('component_details')
		frm.call({
			method:'get_components',
			doc: frm.doc,
		});
	},
	bonus_apply_date: function(frm) {
		frm.clear_table("bonus_calculation")
		frm.refresh_field('bonus_calculation')
		frm.call({
			method:'get_month_year',
			doc: frm.doc,
		});
	},
	check_all: function(frm) {
		frm.call({
			method:'selectall',
			doc: frm.doc,
		});
	},
	get_bonus:function(frm) {
		frm.clear_table("bonus_calculation")
		frm.refresh_field('bonus_calculation')
		frm.call({
			method:'get_emp_bonus',
			doc: frm.doc,
		});
	},
});

