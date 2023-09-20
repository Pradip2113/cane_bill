// Copyright (c) 2023, quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vendor Cheque Release', {
	// refresh: function(frm) {

	// }
});


// Copyright (c) 2023, quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vendor Cheque Release', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Vendor Cheque Release', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});

frappe.ui.form.on('Vendor Cheque Release', {
	
	show_list: function(frm) {

		frm.clear_table("vendor_check_info")
		frm.refresh_field('vendor_check_info')
		frm.call({
			method: 'get_list',//function name defined in python
			doc: frm.doc, //current document
		});

	}

});


frappe.ui.form.on('Vendor Cheque Release', {
	
	sub_button: function(frm) {

		frm.call({
			method: 'update_value_in_cheque_list_on_update',//function name defined in python
			doc: frm.doc, //current document
		});

	}

});

frappe.ui.form.on('Child Vendor Cheque Release', {
    refresh: function(frm) {
        // frappe.msgprint("Hello World"); // You can print a string directly
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Child Cheque Table',
                filters: {"parent": self.branch , "bank" : self.bank_credit_account},
                fieldname: 'cheque_number_list'
            },
            callback: function(response) {
                var options = eval(response.message.list_of_items);
                frm.set_df_property('address', 'options', options);
            }
        });
    }
});






// frappe.ui.form.on('Vendor Cheque Release', {
	
// 	sub_button: function(frm) {

// 		frm.call({
// 			method: 'update_value_in_cheque_list_on_save',//function name defined in python
// 			doc: frm.doc, //current document
// 		});

// 	}

// });


frappe.ui.form.on("Vendor Cheque Release", {
    refresh: function(frm) {
            frm.set_query("vendor_payment_release", function() { // Replace with the name of the link field
                return {
                    filters: [
                        ["Vendor Payment Release", "docstatus", '=', 1] // Replace with your actual filter criteria
                    ]
                };
            });
        }
    });



	// # Copyright (c) 2023, quantbit and contributors
	// # For license information, please see license.txt
	
	// import frappe
	// from frappe.model.document import Document
	
	// class VendorChequeRelease(Document):
	// 	@frappe.whitelist()
	// 	def get_list(self):
	// 		if self.vendor_payment_release:
	// 			vendor_amt_info_child = frappe.get_all("Different Bank Transfer VPV",
	// 															  filters={"parent": self.vendor_payment_release ,"docstatus":1},
	// 															fields=["vendor_id","vendor_name","address","total_amount","select_account","name"])
	// 			for vc in vendor_amt_info_child:
	// 				if vc.total_amount >0:
	// 					self.append(
	// 								"vendor_check_info",
	// 								{
	// 									"vendor_id":vc.vendor_id,
	// 									"vendor_name":vc.vendor_name,
	// 									"address":vc.address,
	// 									"total_amount":vc.total_amount,
	// 									# "account_details":vc.account_details,
	// 									"selected_bank":vc.select_account,
	// 									# "bank_name":vc.bank_name,
	// 									"doc_name" :vc.name
	// 								}
	// 							)
		
	// 		else:
	// 			frappe.throw("Please select Submited Vendor Payment Release")
	   
				
	// 		self.set_cheque_number()
	   
	// 	@frappe.whitelist()
	// 	def set_cheque_number(self):
	// 		uryruy=[{'idx': 1, 'vendor_id': 'FA-13', 'vendor_name': 'ANIL KALLINATH CHOUGULE', 'address': 'BEDKIHAL', 'total_amount': 442.0},{'idx': 2, 'vendor_id': 'FA-14', 'vendor_name': 'ANIL NARASU GADAVE', 'address': 'BEDKIHAL', 'total_amount': 3674.56}, {'idx': 3, 'vendor_id': 'FA-13', 'vendor_name': 'ANIL KALLINATH CHOUGULE', 'address': 'BEDKIHAL', 'total_amount': 3184.97},{'idx': 4, 'vendor_id': 'FA-13', 'vendor_name': 'ANIL KALLINATH CHOUGULE', 'address': 'BEDKIHAL', 'total_amount': 442.0},{'idx': 5, 'vendor_id': 'FA-14', 'vendor_name': 'ANIL NARASU GADAVE', 'address': 'BEDKIHAL', 'total_amount': 3674.56}, {'idx': 6, 'vendor_id': 'FA-13', 'vendor_name': 'ANIL KALLINATH CHOUGULE', 'address': 'BEDKIHAL', 'total_amount': 3184.97},{'idx': 7, 'vendor_id': 'FA-13', 'vendor_name': 'ANIL KALLINATH CHOUGULE', 'address': 'BEDKIHAL', 'total_amount': 442.0},{'idx': 8, 'vendor_id': 'FA-14', 'vendor_name': 'ANIL NARASU GADAVE', 'address': 'BEDKIHAL', 'total_amount': 3674.56}, {'idx': 9, 'vendor_id': 'FA-13', 'vendor_name': 'ANIL KALLINATH CHOUGULE', 'address': 'BEDKIHAL', 'total_amount': 3184.97},{'idx': 10, 'vendor_id': 'FA-13', 'vendor_name': 'ANIL KALLINATH CHOUGULE', 'address': 'BEDKIHAL', 'total_amount': 442.0},{'idx': 11, 'vendor_id': 'FA-14', 'vendor_name': 'ANIL NARASU GADAVE', 'address': 'BEDKIHAL', 'total_amount': 3674.56}, {'idx': 12, 'vendor_id': 'FA-13', 'vendor_name': 'ANIL KALLINATH CHOUGULE', 'address': 'BEDKIHAL', 'total_amount': 3184.97},{'idx': 13, 'vendor_id': 'FA-13', 'vendor_name': 'ANIL KALLINATH CHOUGULE', 'address': 'BEDKIHAL', 'total_amount': 442.0},{'idx': 14, 'vendor_id': 'FA-14', 'vendor_name': 'ANIL NARASU GADAVE', 'address': 'BEDKIHAL', 'total_amount': 3674.56}, {'idx': 15, 'vendor_id': 'FA-13', 'vendor_name': 'ANIL KALLINATH CHOUGULE', 'address': 'BEDKIHAL', 'total_amount': 3184.97},]
	// 		for d in uryruy:
	// 			num=d['idx']
	// 		list_doc=[]
	// 		doc = frappe.db.get_all("Child Cheque Table",
	// 										  filters={"parent": self.branch , "bank" : self.bank},
	// 										fields=["fcm","tcn","current_cheque_number","deleted_cheque_list","name"])
	
	// 		for i in doc:
	// 			current_value= i.current_cheque_number
	// 			maximum_record = i.tcn
	// 			if i.deleted_cheque_list:
	// 				q= eval(i.deleted_cheque_list)
	// 				list_doc = q[:num] if num >= len(q) else q[:num]
	// 				remaining_items = [item for item in q if item not in list_doc]
	// 				# frappe.db.set_value("Child Cheque Table",i.name,"deleted_cheque_list",str(remaining_items))
	// 			if (len(list_doc))<num: 
	// 				# frappe.throw(str(len(list_doc))+""+str(num)+str(remaining_items))
	// 				for r in range(num- (len(list_doc))):
	// 					current_value=current_value+1
	// 					if maximum_record <=current_value:
	// 						list_doc.append(current_value)
	// 					else:
	// 						break
		 
				
	// 			frappe.throw(str(list_doc))
					


		
		
					
