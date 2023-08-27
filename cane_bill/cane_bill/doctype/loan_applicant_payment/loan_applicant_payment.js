// Copyright (c) 2023, quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Loan Applicant Payment', {
	// refresh: function(frm) {

	// }
});




frappe.ui.form.on('Loan Applicant Payment', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});

frappe.ui.form.on('Loan Applicant Payment', {
	
	show_list: function(frm) {
		frm.clear_table("applicant_list")
		frm.refresh_field('applicant_list')

		frm.call({
				method:'list',//function name defined in python
				doc: frm.doc, //current document    test_button
			});

	}
});   

frappe.ui.form.on('Loan Applicant Payment', {
	
	select_all: function(frm) {
		frm.call({
				method:'selectall',//function name defined in python
				doc: frm.doc, //current document    test_button
			});

	}
});   


frappe.ui.form.on('Loan Applicant Payment', {
	
	press: function(frm) {
		frm.call({
				method:'journal_entery_of_payment',//function name defined in python   total_values
				doc: frm.doc, //current document    test_button
			});

	}
});

frappe.ui.form.on('Child Loan Applicant Payment', {
	check(frm) {
		frm.call({
			method:'total_values',//function name defined in python   total_values
			doc: frm.doc, //current document    test_button
		});
	}
})

