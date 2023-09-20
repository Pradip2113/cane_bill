// Copyright (c) 2023, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cane Billing', {
	
	show_list: function(frm) {

		frm.clear_table("farmer_table")
		frm.refresh_field('farmer_table')
		frm.call({
				method:'vivek',//function name defined in python
				doc: frm.doc, //current document
			});

	}
});



frappe.ui.form.on('Cane Billing', {
	select_all: function(frm) {
		frm.call({
			method: 'selectall',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});

frappe.ui.form.on('Cane Billing', {
	
	do_billing: function(frm) {
		frm.clear_table("calculation_table")
		frm.refresh_field('calculation_table')
		frm.call({
			method: 'billing',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});

// frappe.ui.form.on('Cane Billing', {
//     onload: function(frm) {
//         frm.fields_dict['farmer_table'].grid.settings.limit =10;
//         frm.fields_dict['farmer_table'].grid.refresh();
//     }
// });

frappe.ui.form.on('Cane Billing', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});


frappe.ui.form.on('Cane Billing', {
	on_submit_event_call: function(frm) {
		frm.call({
			method: 'interest_je_on_cancle',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});

// frappe.ui.form.on('Cane Billing', {
	
// 	on_submit_event_call: function(frm) {
// 		frm.call({
// 				method:'test_method_trigger_on_button_on_submit_event_call',//function name defined in python
// 				doc: frm.doc, //current document    test_button
// 			});

// 	}
// });     


// frappe.ui.form.on('Cane Billing', {
	
// 	on_submit_event_call: function(frm) {
// 		frm.call({
// 				method:'total_values',//function name defined in python
// 				doc: frm.doc, //current document    test_button
// 			});

// 	}
// });   

