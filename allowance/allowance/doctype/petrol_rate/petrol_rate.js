// Copyright (c) 2024, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('Petrol Rate', {
	date: function(frm) {
		frm.call({
			method: "get_month_yaer",
			doc:frm.doc,
		})
	}
});
