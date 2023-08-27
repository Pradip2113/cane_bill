// Copyright (c) 2023, quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Deduction Form', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on('Deduction Form', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});