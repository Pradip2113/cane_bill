// Copyright (c) 2023, quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vendor Payment Release', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Vendor Payment Release', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});

frappe.ui.form.on('Vendor Payment Release', {
	
	show_list: function(frm) {
		frm.clear_table("vendor_amount_information")
		frm.refresh_field('vendor_amount_information')
		frm.clear_table("self_bank_transfer")
		frm.refresh_field('self_bank_transfer')
		frm.clear_table("different_bank_transfer_vpe")
		frm.refresh_field('different_bank_transfer_vpe')
		frm.call({
			method: 'get_list',//function name defined in python
			doc: frm.doc, //current document
		});

	}

});
frappe.ui.form.on('Vendor Payment Release', {
	
	vendor_payment_entry: function(frm) {
		frm.clear_table("vendor_amount_information")
		frm.refresh_field('vendor_amount_information')
		frm.clear_table("self_bank_transfer")
		frm.refresh_field('self_bank_transfer')
		frm.clear_table("different_bank_transfer_vpe")
		frm.refresh_field('different_bank_transfer_vpe')
		
	}

});
frappe.ui.form.on('Vendor Payment Release', {
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


frappe.ui.form.on('Child Vendor Payment Release', {
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


frappe.ui.form.on('Child Vendor Payment Release', {
	acc_details: function(frm) {
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


frappe.ui.form.on('Child Vendor Payment Release', {
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

frappe.ui.form.on('Vendor Payment Release', {
	bank: function(frm) {
		
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

frappe.ui.form.on("Vendor Payment Release", {
	refresh: function(frm) {
		frm.set_query("vendor_payment_entry", "vpe_table", function(doc, cdt, cdn) { // Replace with the name of the link field
				return {
					filters: [
						["Vendor Payment Entry", "docstatus", '=', 1] // Replace with your actual filter criteria
					]
				};
			});
		}
	});


frappe.ui.form.on('Child Vendor Payment Entry Holder', {
	vendor_payment_entry: function(frm) {
		//frappe.msgprint('hi');
	  frm.set_query("vendor_payment_entry", "vpe_table", function(doc, cdt, cdn) {
				  let d = locals[cdt][cdn];
				  var b = [];
				  frm.doc.vpe_table.forEach(function(row) {
					 b.push(row.vendor_payment_entry);
				  });
				  return {
					  filters: [['name', 'not in', b],["docstatus", "=", 1] ]
					  
				  };
			  });
  
  
		  },
	  });


// frappe.ui.form.on('Child Vendor Payment Entry Holder', {
//     vendor_payment_entry: function(frm) {
       

//         // Set a query for the "vendor_payment_entry" field
//         frm.fields_dict['vpe_table'].grid.get_field('vendor_payment_entry').get_query = function(doc, cdt, cdn) {
//             return {
//                 filters: [
//                     ["name", "not in", existingValues], // Filter to exclude existing values
//                      // Additional filter criteria
//                 ]
//             };
//         };

// 		 // Initialize an empty list to store existing values
// 		 var existingValues = [];

// 		 // Loop through existing rows in vpe_table and add their values to existingValues
// 		 frm.doc.vpe_table.forEach(function(row) {
// 			 existingValues.push(row.vendor_payment_entry);
// 		 });
//     }
// });








	  frappe.ui.form.on('Child Vendor Payment Entry Holder', {
	
		vendor_payment_entry: function(frm) {
			frm.clear_table("vendor_amount_information")
			frm.refresh_field('vendor_amount_information')
			frm.clear_table("self_bank_transfer")
			frm.refresh_field('self_bank_transfer')
			frm.clear_table("different_bank_transfer_vpe")
			frm.refresh_field('different_bank_transfer_vpe')
			frm.call({
				method: 'get_list',//function name defined in python
				doc: frm.doc, //current document
			});
	
		},});


		frappe.ui.form.on('Child Vendor Payment Entry Holder', {
			vpe_table_remove: function(frm) {
				frm.clear_table("vendor_amount_information")
			frm.refresh_field('vendor_amount_information')
			frm.clear_table("self_bank_transfer")
			frm.refresh_field('self_bank_transfer')
			frm.clear_table("different_bank_transfer_vpe")
			frm.refresh_field('different_bank_transfer_vpe')
			frm.call({
				method: 'get_list',//function name defined in python
				doc: frm.doc, //current document
			});
		
			}
		});
		


