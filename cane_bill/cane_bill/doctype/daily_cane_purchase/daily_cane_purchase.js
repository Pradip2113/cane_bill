// Copyright (c) 2023, quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Cane Purchase', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on('Daily Cane Purchase', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});



frappe.ui.form.on('Daily Cane Purchase', {
	
	show_list: function(frm) {
		frm.clear_table("record_table")
		frm.refresh_field('record_table')
		frm.call({
				method:'get_cane_weight_data',//function name defined in python
				doc: frm.doc, //current document
			});

	}
});


frappe.ui.form.on('Daily Cane Purchase', {
	
	check_all: function(frm) {
		frm.call({
				method:'selectall',//function name defined in python
				doc: frm.doc, //current document bulk_purchase_receipt
			});

	}
});

// frappe.ui.form.on('Daily Cane Purchase', {
	
// 	test: function(frm) {
// 		frm.call({
// 				method:'bulk_purchase_receipt',//function name defined in python
// 				doc: frm.doc, //current document bulk_purchase_receipt
// 			});

// 	}
// });


frappe.ui.form.on('Daily Cane Purchase', {
	
	test: function(frm) {
		frm.call({
				method:'temp_method',//function name defined in python
				doc: frm.doc, //current document bulk_purchase_receipt
			});

	}
});