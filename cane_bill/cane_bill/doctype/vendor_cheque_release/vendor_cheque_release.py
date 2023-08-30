# Copyright (c) 2023, quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_link_to_form

class VendorChequeRelease(Document):
    
	@frappe.whitelist()
	def get_list(self):
		# frappe.throw(str(frappe.get_all("Purchase Invoice", filters={"supplier": "FA-6309", "status": ["in", ["Unpaid", "Overdue", "Partly Paid"]]}, order_by="creation DESC", limit=1)[0].name))
		if (not self.bank):
			frappe.throw("Please Select Bank")
   
		if (not self.branch):
			frappe.throw("Please Select Branch")
   
		cheque_item_list =[]
		if self.vendor_payment_release:
			vendor_amt_info_child = frappe.get_all("Child Vendor Payment Release",
                                          					filters={"parent": self.vendor_payment_release ,"docstatus":1,'check':1},
															fields=["vendor_id","vendor_name","address","total_amount","acc_details","name","bank_name","debit_account"])
			for vc in vendor_amt_info_child:
				if vc.total_amount >0:
					cheque_item_list.append(
								{   "total_amount":vc.total_amount,
									"selected_bank":vc.acc_details,
									"bank_name": vc.bank_name,
									"vendor_name":vc.vendor_name,
									"vendor_id" :vc.vendor_id,
									"doc_name" :vc.name,
									"debit_account" : vc.debit_account    #{'total_amount': record['total_amount'], 'debit_account': record['debit_account']}
         })
			
			
			b = []
			same_bank_total = 0
			other_bank_total = 0
			list_same=[]
			list_other=[]
			same_account_amount_list=[]
			other_account_amount_list=[]
			for record in cheque_item_list:
				if record['bank_name'] == 'Bank not found':
					rrr=[record['doc_name']]
					kkk =[{'total_amount': record['total_amount'], 'debit_account': record['debit_account'] , 'vendor_id': record['vendor_id']}] #{'total_amount': record['total_amount'], 'debit_account': record['debit_account']}
					self.append("vendor_check_info", {  "total_amount": record["total_amount"],
														"name_on_cheque": record["vendor_name"],
														"bank": record["bank_name"],
														"type":record['selected_bank'],
														"doc_name" : str(rrr),
              											"account_with_amount":str(kkk),})
					# frappe.throw(str([record['doc_name']]))
     
				elif record['bank_name'] == self.bank:
					same_bank_total += record['total_amount']
					list_same.append(record['doc_name'])
					same_account_amount_list.append({'total_amount': record['total_amount'], 'debit_account': record['debit_account'],'vendor_id': record['vendor_id']})
				else:
					other_bank_total += record['total_amount']
					list_other.append(record['doc_name'])
					other_account_amount_list.append({'total_amount': record['total_amount'], 'debit_account': record['debit_account'],'vendor_id': record['vendor_id']})
     
			# frappe.throw(str(cheque_item_list))
			if same_bank_total > 0:
				b.append({ 'total_amount': same_bank_total, 'selected_bank': 'Self Bank Transfer' , 'doc_name':str(list_same) ,'account_amount': str(same_account_amount_list)})
			if other_bank_total > 0:
				b.append({'total_amount': other_bank_total, 'selected_bank': 'Other Bank Transfer','doc_name':str(list_other) ,'account_amount': str(other_account_amount_list)})
    
			
			for row in b:
				self.append("vendor_check_info", {
					"total_amount": row["total_amount"],
					"bank": self.bank,
					"name_on_cheque" : self.bank_account,
					"type" : row["selected_bank"],	
					"doc_name":str(row["doc_name"]),
					"account_with_amount": str(row["account_amount"])
					
				})
    
		else:
			frappe.throw("Please select Submited Vendor Payment Release")
   
			
		self.set_cheque_number()
		# self.journal_entry()
	@frappe.whitelist()
	def set_cheque_number(self):
		num=(len(self.get("vendor_check_info")))
		doc = frappe.db.get_all("Child Cheque Table",
                          				filters={"parent": self.branch , "bank" : self.bank_credit_account},
										fields=["fcm","tcn","current_cheque_number","deleted_cheque_list","name"] ,order_by ="idx")
		if doc:
			list_doc=[]
			for i in doc:
				current_value= i.current_cheque_number if i.current_cheque_number else i.fcm
				maximum_record = i.tcn
				if i.deleted_cheque_list:
					q= eval(i.deleted_cheque_list)
					list_doc = q[:num] if num >= len(q) else q[:num]
					remaining_items = [item for item in q if item not in list_doc]
					# frappe.db.set_value("Child Cheque Table",i.name,"deleted_cheque_list",str(remaining_items))
				if (len(list_doc))<num: 
					for r in range(num- (len(list_doc))):
						current_value=current_value+1
						if maximum_record >= current_value:
							list_doc.append(current_value)
						else:
							break

			for vk in (self.get("vendor_check_info")):
				vk.check_number= list_doc[0]
				list_doc.pop(0)
		else:
			frappe.throw(f'Please set Cheque Numbers for bank "{self.bank}" in Branch "{self.branch}"')
   
	@frappe.whitelist()
	def set_value_in_updated(self):
		pass

	@frappe.whitelist()
	def before_save(self):
		self.submit_effect_check_payment_release()
  
	@frappe.whitelist()
	def before_submit(self):
		self.journal_entry()
  
   
	@frappe.whitelist()
	def before_cancel(self):
		self.cancle_effect_check_payment_release()
		self.cancel_journal_entry()
  
	@frappe.whitelist()
	def on_trash(self):
		self.cancle_effect_check_payment_release() 

	@frappe.whitelist()
	def submit_effect_check_payment_release(self):
		for s in (self.get("vendor_check_info")):
			doc_name_list=eval(s.doc_name)
			for d in doc_name_list:
				frappe.set_value("Child Vendor Payment Release",d,"cheque_release_status",1)
    
    
	@frappe.whitelist()
	def cancle_effect_check_payment_release(self):
		for s in (self.get("vendor_check_info")):
			doc_name_list=eval(s.doc_name)
			for d in doc_name_list:
				frappe.set_value("Child Vendor Payment Release",d,"cheque_release_status",0)


	@frappe.whitelist()
	def journal_entry(self):

		branch_doc = frappe.get_all("Branch",
											filters={"name": self.branch},
											fields={"cane_rate", "name","company","debit_in_account_currency"},)
		if branch_doc:
			if not (branch_doc[0].company):
				frappe.throw( f" Please set Company for Branch '{str(self.branch) } '")
			company =  ((branch_doc[0].company))

		round_total_amt =0
		je = frappe.new_doc("Journal Entry")
		je.voucher_type = "Journal Entry"
		je.company = company
		je.posting_date = self.date
		for s in self.get("vendor_check_info"):
			for l in eval(s.account_with_amount):
				# frappe.msgprint(str("ytgru"))
				# frappe.msgprint(str(((l['total_amount']))))
				je.append(
					"accounts",
					{
						"account": l['debit_account'],
						"party_type": "Supplier",
						"party": l['vendor_id'],
						"reference_type":"Purchase Invoice",
						"reference_name":(frappe.get_all("Purchase Invoice", filters={"supplier": l['vendor_id'], "status": ["in", ["Unpaid", "Overdue", "Partly Paid"]]}, order_by="creation DESC", limit=1)[0].name) if l['debit_account'] == frappe.get_value("Branch",self.branch,"debit_in_account_currency") else None,
						"debit_in_account_currency": (float(l['total_amount'])),
						
					},)
				
				round_total_amt += (float(l['total_amount']))
			# frappe.msgprint(str((round_total_amt)))
		je.append(
			"accounts",
			{
				"account": self.bank_credit_account,
				"credit_in_account_currency":round_total_amt,
			},)


		je.insert()
		je.save()
		je.submit()
		journal_entry = frappe.db.get_all("Journal Entry", fields=["name"], order_by="creation DESC", limit=1)
		self.journal_entry_id =journal_entry[0].name

	@frappe.whitelist()
	def cancel_journal_entry(self):
		doc = frappe.get_doc("Journal Entry", (str(self.journal_entry_id)))
		if doc.docstatus == 1:
			doc.cancel()




















		# frappe.throw(str(len(self.get("vendor_check_info"))))	
		# for vk in range((len(self.get("vendor_check_info")))):
		# 	i.check_number= 
  
  
# @frappe.whitelist()
# def set_cheque_number(self):
#     num = len(self.get("vendor_check_info"))
#     doc = frappe.get_all("Child Cheque Table",
#                          filters={"parent": self.branch, "bank": self.bank},
#                          fields=["fcm", "tcn", "current_cheque_number", "deleted_cheque_list", "name"],
#                          order_by="idx")

#     list_doc = []

#     for i in doc:
#         current_value = i.current_cheque_number or i.fcm
#         maximum_record = i.tcn

#         if i.deleted_cheque_list:
#             deleted_cheque_list = eval(i.deleted_cheque_list)
#             list_doc.extend(deleted_cheque_list[:num])
#             remaining_items = [item for item in deleted_cheque_list if item not in list_doc]
#             # Uncomment the following line to update the deleted_cheque_list field:
#             # frappe.db.set_value("Child Cheque Table", i.name, "deleted_cheque_list", str(remaining_items))

#         while len(list_doc) < num:
#             current_value += 1
#             if current_value <= maximum_record:
#                 list_doc.append(current_value)
#             else:
#                 break

#     for vk in self.get("vendor_check_info"):
#         vk.check_number = list_doc.pop(0)
# -------------------------------------------------------------------------------------------------------------------
	# @frappe.whitelist()
	# def get_list(self):
	# 	cheque_item_list = []

	# 	if self.vendor_payment_release:
	# 		vendor_amt_info_child = frappe.get_all("Child Vendor Payment Release",
	# 											filters={"parent": self.vendor_payment_release, "docstatus": 1, 'check': 1},
	# 											fields=["vendor_id", "vendor_name", "address", "total_amount", "acc_details", "name"])
			
	# 		for vc in vendor_amt_info_child:
	# 			if vc.total_amount > 0:
	# 				cheque_item_list.append({
	# 					"total_amount": vc.total_amount,
	# 					"selected_bank": vc.acc_details,
	# 					"vendor_name":vc.vendor_name
	# 					# "bank":vc.acc_details
	# 				})

	# 		list_2 = []
	# 		bank_totals = {}

	# 		for item in cheque_item_list:
	# 			bank = item['selected_bank']
	# 			total_amount = item['total_amount']

	# 			if bank == 'Bank not found':
	# 				self.append("vendor_check_info", {
	# 					"total_amount": item["total_amount"],
	# 					"bank": item["vendor_name"],
	# 					# "bank":item["bank"]
	# 				})
	# 			else:
	# 				if bank in bank_totals:
	# 					bank_totals[bank] += total_amount
	# 				else:
	# 					bank_totals[bank] = total_amount

	# 		for bank, total_amount in bank_totals.items():
	# 			list_2.append({'selected_bank': bank, 'total_amount': total_amount})

			# for row in list_2:
			# 	self.append("vendor_check_info", {
			# 		"total_amount": row["total_amount"],
			# 		"bank": row["selected_bank"],
					
			# 	})

	# 		self.set_cheque_number()
	# 	else:
	# 		frappe.throw("Please select Submitted Vendor Payment Release")

	# Make sure the child table 'vendor_amount_information' is properly defined in your DocType.

	# @frappe.whitelist()
	# def get_list(self):
	# 	cheque_item_list =[]
	# 	if self.vendor_payment_release:
	# 		vendor_amt_info_child = frappe.get_all("Child Vendor Payment Release",
    #                                       					filters={"parent": self.vendor_payment_release ,"docstatus":1,'check':1},
	# 														fields=["vendor_id","vendor_name","address","total_amount","acc_details","name"])
	# 		for vc in vendor_amt_info_child:
	# 			if vc.total_amount >0:
	# 				cheque_item_list.append(
	# 							{
	# 								# "vendor_id":vc.vendor_id,
	# 								# "vendor_name":vc.vendor_name,
	# 								# "address":vc.address,
	# 								"total_amount":vc.total_amount,
	# 								"selected_bank":vc.acc_details,
	# 								# "doc_name" :vc.name
	# 							}
	# 						)
			
	# 		list_2 = []
	# 		bank_totals = {}

	# 		for item in cheque_item_list:
	# 			bank = item['selected_bank']
	# 			total_amount = item['total_amount']
	# 			if bank == 'Bank not found':
	# 				self.append(
	# 						"vendor_amount_information",
	# 						{
								
	# 							"total_amount": item["total_amount"],
	# 							"selected_bank": item["selected_bank"],
	# 						}
	# 					)
	# 			else:
	# 				if bank in bank_totals:
	# 					bank_totals[bank] += total_amount
	# 				else:
	# 					bank_totals[bank] = total_amount
	# 		for bank, total_amount in bank_totals.items():
	# 			list_2.append({'selected_bank': bank, 'total_amount': total_amount})
    
	# 		for row in list_2:
	# 			self.append("vendor_amount_information", {
	# 				"total_amount": row["total_amount"],
	# 				"selected_bank": row["selected_bank"],
					
	# 			})

	# 	else:
	# 		frappe.throw("Please select Submited Vendor Payment Release")
   
			
	# 	self.set_cheque_number()