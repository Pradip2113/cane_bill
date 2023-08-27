# Copyright (c) 2023, quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class VendorChequeRelease(Document):
    
	@frappe.whitelist()
	def get_list(self):
		if (not self.bank):
			frappe.throw("Please Select Bank")
   
		if (not self.branch):
			frappe.throw("Please Select Branch")
   
		cheque_item_list =[]
		if self.vendor_payment_release:
			vendor_amt_info_child = frappe.get_all("Child Vendor Payment Release",
                                          					filters={"parent": self.vendor_payment_release ,"docstatus":1,'check':1},
															fields=["vendor_id","vendor_name","address","total_amount","acc_details","name"])
			for vc in vendor_amt_info_child:
				if vc.total_amount >0:
					cheque_item_list.append(
								{
									# "vendor_id":vc.vendor_id,
									# "vendor_name":vc.vendor_name,
									# "address":vc.address,
									"total_amount":vc.total_amount,
									"selected_bank":vc.acc_details,
									"vendor_name":vc.vendor_name,
									"doc_name" :vc.name
								}
							)
			
			b = []
			same_bank_total = 0
			other_bank_total = 0
			list_same=[]
			list_other=[]
			for record in cheque_item_list:
				if record['selected_bank'] == 'Bank not found':
					rrr=[record['doc_name']]
					self.append("vendor_check_info", {
						"total_amount": record["total_amount"],
						"name_on_cheque": record["vendor_name"],
						"bank": record["selected_bank"],
						"type":record['selected_bank'],
						
						"doc_name" : str(rrr),
					})
					# frappe.throw(str([record['doc_name']]))
				elif record['selected_bank'] == self.bank:
					same_bank_total += record['total_amount']
					list_same.append(record['doc_name'])
				else:
					other_bank_total += record['total_amount']
					list_other.append(record['doc_name'])
			if same_bank_total > 0:
				b.append({'total_amount': same_bank_total, 'selected_bank': 'Self Bank Transfer','doc_name':str(list_same)})
			if other_bank_total > 0:
				b.append({'total_amount': other_bank_total, 'selected_bank': 'Other Bank Transfer','doc_name':str(list_other)})
    
			
			for row in b:
				self.append("vendor_check_info", {
					"total_amount": row["total_amount"],
					"bank": self.bank,
					"name_on_cheque" : frappe.get_value("Bank Master",self.bank,"bank_name"),
					"type" : row["selected_bank"],	
					"doc_name":str(row["doc_name"]),
					
				})
    
		else:
			frappe.throw("Please select Submited Vendor Payment Release")
   
			
		self.set_cheque_number()
   
	@frappe.whitelist()
	def set_cheque_number(self):
		num=(len(self.get("vendor_check_info")))
		doc = frappe.db.get_all("Child Cheque Table",
                          				filters={"parent": self.branch , "bank" : self.bank},
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
	def before_cancel(self):
		self.cancle_effect_check_payment_release()
  
  
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