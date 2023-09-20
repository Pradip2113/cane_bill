# Copyright (c) 2023, quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class VendorPaymentRelease(Document):
	@frappe.whitelist()
	def selectall(self):
		children = self.get("vendor_amount_information")
		if not children:
			return
		all_selected = all([child.check for child in children])
		value = 0 if all_selected else 1
		for child in children:
			child.check = value
		self.sort_bank()
   
	@frappe.whitelist()
	def get_list(self):
		# vendor_id_list={}
		# doc= frappe.get_all("Vendor Payment Entry", filters={"date": ["between", [self.from_date, self.to_date]],"branch":self.branch,"season":self.season},fields=["bank","date","name","payment_type"]) #"docstatus": 1
		# if not self.bank and doc:
		# 	self.bank=doc[0].bank if doc[0].bank else None
		for d in self.get("vpe_table"):
			vendor_amt_info_child = frappe.get_all("Child Vendor Payment Entry",
                                          										filters={"parent":d.vendor_payment_entry ,"pay_r_s":0,"docstatus":1,'check':1},
                                                    							fields=["vendor_id","vendor_name","address","total_amount","type","contract_id","account_details","bank_name","name","debit_account","doc_name"])
			# frappe.throw(str(vendor_amt_info_child))
			for vc in vendor_amt_info_child:
				self.append(
								"vendor_amount_information",
								{
									"vendor_id":vc.vendor_id,
									"vendor_name":vc.vendor_name,
									"address":vc.address,
									"total_amount":vc.total_amount,
									"type":str(frappe.get_value("Vendor Payment Entry",d.vendor_payment_entry,"payment_type")),
									"contract_id":vc.contract_id,
									"debit_account": vc.debit_account,
									"account_details":vc.account_details,
									"acc_details":vc.account_details,
									"bank_name":vc.bank_name,
									"payment_type":vc.parent,
									"doc_name" :vc.name,
									"payment_doc" : vc.doc_name,
								}
						)

	@frappe.whitelist()
	def sort_bank(self):
		if self.bank is None:
			frappe.throw("Please select Bank")

		for i in self.get("vendor_amount_information"):
			if i.check:
				transfer_data = {
					"vendor_id": i.vendor_id,
					"vendor_name": i.vendor_name,
					"address": i.address,
					"total_amount": i.total_amount,
					"type": i.type,
					"contract_id": i.contract_id,
					"account_details": i.account_details,
					"select_account": i.acc_details,
					"bank_name" :i.bank_name
				}
				transfer_type = "self_bank_transfer" if self.bank == i.bank_name else "different_bank_transfer_vpe"
				self.append(transfer_type, transfer_data)

		self.total_amount_sbt=self.total_amount_cal("self_bank_transfer")
		self.total_amount_dbt=self.total_amount_cal("different_bank_transfer_vpe")

	@frappe.whitelist()
	def total_amount_cal(self,table):
		total_amt=0
		for x in self.get(table):
			total_amt += x.total_amount
		return total_amt

	@frappe.whitelist()
	def before_save(self):
		self.change_status_on_VPE()
  
	@frappe.whitelist()
	def before_submit(self):
		self.delete_row_record()
  
	@frappe.whitelist()
	def before_cancel(self):
		self.change_status_on_VPE_on_cancel()
  
  
	@frappe.whitelist()
	def on_trash(self):
		self.change_status_on_VPE_on_cancel() 
    
    
	@frappe.whitelist()
	def change_status_on_VPE(self):
		for yz in  self.get("vendor_amount_information"):
			if yz.check:
				frappe.db.set_value("Child Vendor Payment Entry" , yz.doc_name , "pay_r_s", 1)
     
	@frappe.whitelist()
	def change_status_on_VPE_on_cancel(self):
		for yz in  self.get("vendor_amount_information"):
			if yz.check:
				frappe.db.set_value("Child Vendor Payment Entry" , yz.doc_name , "pay_r_s", 0)
		
	def delete_row_record(self):
		doc = frappe.get_all("Child Vendor Payment Entry",filters ={"parent": self.name , "check" : 0},)
		for d in doc:
			frappe.delete_doc("Child Vendor Payment Entry", d.name)
		# self.reload_doc()		
	# @frappe.whitelist() frappe.get_value("doctype_name" ,"docment_namr","field name")
	# def sort_bank(self):
	# 	for i in self.get("vendor_amount_information"):
	# 		if i.check:
	# 			if self.bank == None:
	# 				frappe.throw("Please select Bank")
	# 			if i.account_details:
	# 				if self.consolidated_payment_release:
	# 					bank_list=eval(i.account_details)
	# 					if self.bank in bank_list:
	# 						self.append(
	# 							"self_bank_transfer",
	# 							{
	# 								"vendor_id": i.vendor_id,
	# 								"vendor_name": i.vendor_name,
	# 								"address" : i.address,
	# 								"total_amount": i.total_amount,
	# 								"type": i.type,
	# 								"contract_id": i.contract_id,
	# 								"account_details":i.account_details,
	# 							},
	# 						)
	# 					else:
	# 						self.append(
	# 							"different_bank_transfer_vpe",
	# 							{
	# 								"vendor_id": i.vendor_id,
	# 								"vendor_name": i.vendor_name,
	# 								"address" : i.address,
	# 								"total_amount": i.total_amount,
	# 								"type": i.type,
	# 								"contract_id": i.contract_id,
	# 								"account_details":i.account_details,
	# 							},
	# 						)
  
  
	# 				else:
	# 					if self.bank == i.account_details :
	# 						self.append(
	# 							"self_bank_transfer",
	# 							{
	# 								"vendor_id": i.vendor_id,
	# 								"vendor_name": i.vendor_name,
	# 								"address" : i.address,
	# 								"total_amount": i.total_amount,
	# 								"type": i.type,
	# 								"contract_id": i.contract_id,
	# 								"account_details":i.account_details,
	# 							},
	# 						)
	# 					else:
	# 						self.append(
	# 							"different_bank_transfer_vpe",
	# 							{
	# 								"vendor_id": i.vendor_id,
	# 								"vendor_name": i.vendor_name,
	# 								"address" : i.address,
	# 								"total_amount": i.total_amount,
	# 								"type": i.type,
	# 								"contract_id": i.contract_id,
	# 								"account_details":i.account_details,
	# 							},
	# 						)

     	
		# 	if(self.consolidated_payment_release==1):
		# 		if(vc.vendor_id not in vendor_id_list):
		# 			vendor_id_list[vc.vendor_id]={
		# 				"vendor_id":vc.vendor_id,
		# 				"vendor_name":vc.vendor_name,
		# 				"address":vc.address,
		# 				"total_amount":vc.total_amount,
		# 				"type":[vc.type],
		# 				"contract_id":[vc.contract_id],
		# 				"account_details":[vc.account_details],
		# 				"bank_name":[vc.bank_name],
		# 				"doc_name":[vc.name],
		# 				"payment_type":[vc.payment_type]
		# 			}
		# 		else:
		# 			vendor_id_list[vc.vendor_id]["total_amount"]+=vc.total_amount
		# 			vendor_id_list[vc.vendor_id]["contract_id"].append(vc.contract_id)
		# 			vendor_id_list[vc.vendor_id]["bank_name"].append(vc.bank_name)
		# 			vendor_id_list[vc.vendor_id]["doc_name"].append(vc.name)
		# 			if  vc.account_details not in vendor_id_list[vc.vendor_id]["account_details"]:
		# 				vendor_id_list[vc.vendor_id]["account_details"].append(vc.account_details) 

		# 			vendor_id_list[vc.vendor_id]["payment_type"].append(vc.payment_type)
		# 	else:
		# 		self.append(
		# 					"vendor_amount_information",
		# 					{
		# 						"vendor_id":vc.vendor_id,
		# 						"vendor_name":vc.vendor_name,
		# 						"address":vc.address,
		# 						"total_amount":vc.total_amount,
		# 						"type":vc.type,
		# 						"contract_id":vc.contract_id,
		# 						"account_details":vc.account_details,
		# 						"acc_details":vc.account_details,
		# 						"bank_name":vc.bank_name,
		# 						"payment_type":d.payment_type,
		# 						"doc_name" :vc.name
		# 					}
		# 				) 
		# if(self.consolidated_payment_release):
		# 	for df in vendor_id_list:
		# 			self.append(
		# 					"vendor_amount_information",
		# 					{
		# 						"vendor_id":vendor_id_list[df]["vendor_id"],
		# 						"vendor_name":vendor_id_list[df]["vendor_name"],
		# 						"address":vendor_id_list[df]["address"],
		# 						"type":str(vendor_id_list[df]["type"]),
		# 						"contract_id":str(vendor_id_list[df]["contract_id"]),
		# 						"total_amount":str(vendor_id_list[df]["total_amount"]),
		# 						"bank_name":str(vendor_id_list[df]["bank_name"]),
		# 						"payment_type":str(vendor_id_list[df]["payment_type"]),
		# 						"account_details":str(vendor_id_list[df]["account_details"]),
		# 						"doc_name" : str(vendor_id_list[df]["doc_name"]),
		# 						"acc_details": str(self.bank if self.bank in (vendor_id_list[df]["account_details"]) else vendor_id_list[df]["account_details"][0])

		# 					}
		# 				) 

	

    