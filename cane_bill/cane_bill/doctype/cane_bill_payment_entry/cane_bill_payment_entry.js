// Copyright (c) 2023, quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cane Bill Payment Entry', {
	// refresh: function(frm) {

	// }
});



frappe.ui.form.on('Cane Bill Payment Entry', {
	
	show_list: function(frm) {

		frm.clear_table("payable_list")
		frm.refresh_field('payable_list')
		frm.call({
				method:'get_list',//function name defined in python
				doc: frm.doc, //current document
			});

	}
});

frappe.ui.form.on('Cane Bill Payment Entry', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});
