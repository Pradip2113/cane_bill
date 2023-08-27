
// Copyright (c) 2023, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Farmer Loan', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Farmer Loan', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});


// frappe.ui.form.on('Farmer Loan', {
// 	testing_button: function(frm) {
// 		frm.call({
// 			method: 'set_remaining_installment_amount_in_installment_table',//function name defined in python
// 			doc: frm.doc, //current document
// 		});

// 	}
// });

frappe.ui.form.on('Farmer Loan', {
	testing_button: function(frm) {
		frm.call({
			method: 'validation_of_installments',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});



// frappe.ui.form.on("Farmer Loan", {
//     refresh: function(frm) {
//         // if (frm.doc.isfarmer == 1) { // Replace with the name of the checkbox field
//             frm.set_query("harvester_code", function() { // Replace with the name of the link field
//                 return {
//                     filters: [
//                         ["Farmer List", "is_harvester", '=', self.application_id] // Replace with your actual filter criteria
//                     ]
//                 };
//             });
//         // }
//     }
// });

// frappe.ui.form.on("Farmer Loan", {
//     refresh: function(frm) {
//         // if (frm.doc.isfarmer == 1) { // Replace with the name of the checkbox field
//             frm.set_query("application", function() { // Replace with the name of the link field
//                 return {
//                     filters: [
//                         ["Farmer Loan Application", "applicant", '=', self.applicant_id] // Replace with your actual filter criteria
//                     ]
//                 };
//             });
//         // }
//     }
// });

frappe.ui.form.on("Farmer Loan", {
    refresh: function(frm) {
            frm.set_query("application", function() { // Replace with the name of the link field
                return {
                    filters: [
                        ["Farmer Loan Application", "applicant", '=', frm.doc.applicant_id ], // Replace with your actual filter criteria
                        ["Farmer Loan Application", "docstatus", '=', 1],
                        ["Farmer Loan Application", "status", '=', "Approved"]
                    ]

                    
                };
            });
        }
    });

    // frappe.ui.form.on("Farmer Loan", {
    //     refresh: function(frm) {
    //             frm.set_query("application", function() { // Replace with the name of the link field
    //                 return {
    //                     filters: [
    //                         ["Farmer Loan Application", "docstatus", '=', 1 ] // Replace with your actual filter criteria
    //                     ]
    
                        
    //                 };
    //             });
    //         }
    //     });



  frappe.ui.form.on('Farmer Loan', {
	application: function(frm) {
		frm.call({
			method:'after_insert_data',//function name defined in python
			doc: frm.doc, //current document
		});
		
	}
});


frappe.ui.form.on('Farmer Loan', {
	disbursement_amount: function(frm) {
		frm.call({
			method:'update_installment',//function name defined in python
			doc: frm.doc, //current document
		});
		
	}
});

// frappe.ui.form.on('Farmer Loan', {
// 	onload: function(frm) {
// 		frm.call({
// 			method:'update_installment',//function name defined in python
// 			doc: frm.doc, //current document
// 		});
		
// 	}
// });

frappe.ui.form.on('Farmer Loan', {
	application: function(frm) {
		frm.call({
			method:'before_da',//function name defined in python
			doc: frm.doc, //current document
		});
		
	}
});

frappe.ui.form.on('Farmer Loan', {
	disbursement_amount: function(frm) {
		frm.call({
			method:'validation_for_disbursement_amount',//function name defined in python
			doc: frm.doc, //current document
		});
		
	}
});