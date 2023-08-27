// Copyright (c) 2023, quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vendor Payment Entry', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Vendor Payment Entry', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});

frappe.ui.form.on('Vendor Payment Entry', {
	payment_type: function(frm) {

		// frm.clear_field("document_name")
		// frm.refresh_field('document_name')

		frm.call({
			method: 'set_payment_doctype',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});


frappe.ui.form.on('Vendor Payment Entry', {
	show_list: function(frm) {
		frm.clear_table("vendor_amount_information")
		frm.refresh_field('vendor_amount_information')
		frm.call({
			method: 'get_list',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});

frappe.ui.form.on('Vendor Payment Entry', {
	select_all: function(frm) {
		frm.clear_table("self_bank_transfer")
			frm.refresh_field('self_bank_transfer')
			frm.clear_table("different_bank_transfer_vpe")
			frm.refresh_field('different_bank_transfer_vpe')
		frm.call({
			method: 'selectall',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});


frappe.ui.form.on("Vendor Payment Entry", {
    payment_type: function(frm) {
		if (frm.doc.payment_type_doctype == "Cane Billing") {
            frm.set_query("document_name", function() { // Replace with the name of the link field
                return {
					filters: [
								['Cane Billing', 'season', '=',frm.doc.season],
								['Cane Billing', 'branch', '=', frm.doc.branch],
								['Cane Billing', 'docstatus', '=', 1]
					]                 
                };
            });
        }
		else if(frm.doc.payment_type_doctype == "H and T Billing") {
            frm.set_query("document_name", function() { // Replace with the name of the link field
                return {
					filters: [
								['H and T Billing', 'season', '=',frm.doc.season],
								['H and T Billing', 'branch', '=', frm.doc.branch],
								['H and T Billing', 'docstatus', '=', 1]
					]                 
                };
            });
        }
		else{
            frm.set_query("document_name", function() { // Replace with the name of the link field
                return {
					             
                };
            });
        }
	}
    });


	frappe.ui.form.on('Child Vendor Payment Entry', {
		check: function(frm) {
			frm.clear_table("self_bank_transfer")
			frm.refresh_field('self_bank_transfer')
			frm.clear_table("different_bank_transfer_vpe")
			frm.refresh_field('different_bank_transfer_vpe')
			frm.call({
				method: 'sort_bank',//function name defined in python
				doc: frm.doc, //current document  table_remove
			});
	
		}
	});


	frappe.ui.form.on('Child Vendor Payment Entry', {
		vendor_amount_information_remove: function(frm) {
			frm.clear_table("self_bank_transfer")
			frm.refresh_field('self_bank_transfer')
			frm.clear_table("different_bank_transfer_vpe")
			frm.refresh_field('different_bank_transfer_vpe')
			frm.call({
				method: 'sort_bank',//function name defined in python
				doc: frm.doc, //current document  table_remove
			});
	
		}
	});
