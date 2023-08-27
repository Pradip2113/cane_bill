# Copyright (c) 2023, quantbit and contributors
# For license information, please see license.txt
#

# import frappe
# from frappe.model.document import Document

# class VendorPaymentEntry(Document):
# 	@frappe.whitelist()
# 	def set_payment_doctype(self):
# 		payment_type_mapping = {
# 			'Cane Billing Payment': 'Cane Billing',
# 			'H and T Advance Payment': 'Advance Request',
# 			'H and T Billing Payment': 'H and T Billing',
# 			'Loan Payment': 'Farmer Loan Application'
# 		}
# 		self.payment_type_doctype = payment_type_mapping.get(self.payment_type)
# 		if not self.payment_type_doctype:
# 			frappe.throw("Please select an appropriate 'Payment Type'")

# 	@frappe.whitelist()
# 	def get_list(self):

# 		doctype_mapping = {
# 			'Cane Billing Payment': ("Child Calculation Cane Bill", "farmer_id", "farmer_name", "total_payable_amount"),
# 			'H and T Advance Payment': ("Advance Request item", "transporter_code", "name1", "sanction_amount"),
# 			'H and T Billing Payment': ("Child H and T Calculation", "vender_id", "vender_name", "payable_amt"),
# 			'Loan Payment': ("Farmer Loan Application", "applicant", "applicant_name", "loan_amount")
# 		}

# 		doctype_info = doctype_mapping.get(self.payment_type)
		
# 		if not doctype_info:
# 			frappe.throw("Please select an appropriate 'Payment Type'")

# 		doctype_name, document_name, a, b, c = doctype_info
		
# 		doctype_filter = {"docstatus": 1, "parent": self.document_name}

# 		# if self.payment_type in ['Cane Billing Payment', 'H and T Advance Payment', 'Loan Payment']:
# 		# 	doctype_filter["branch"] = self.branch

# 		doc = frappe.get_all(doctype_name, filters=doctype_filter, fields=[a, b, c])

# 		for entry in doc:
# 			self.append(
# 				"vendor_amount_information",
# 				{
# 					"vendor_id": entry.get(a),
# 					"vendor_name": entry.get(b),
# 					"total_amount": entry.get(c),
# 				},
# 			)





# Cane Billing Payment
# H and T Advance Payment
# H and T Billing Payment
# Loan Payment
from frappe.utils import get_link_to_form
from frappe import _
import frappe
from frappe.model.document import Document



class VendorPaymentEntry(Document):
	@frappe.whitelist()
	def set_payment_doctype(self):
		self.document_name=""
		payment_type_mapping = {
		'Cane Billing Payment': 'Cane Billing',
		'H and T Advance Payment': 'Advance Request',
		'H and T Billing Payment': 'H and T Billing',
		'Loan Payment': 'Farmer Loan Application'
		}
		self.payment_type_doctype = payment_type_mapping.get(self.payment_type)
		if not self.payment_type_doctype:
			frappe.throw("Please select an appropriate 'Payment Type'")
    

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
		if self.payment_type == "Cane Billing Payment":
			doctype_name = "Child Calculation Cane Bill"
			doctype_filter = {"docstatus": 1,"parent": self.document_name,} #"payment_status":0
			doctype_field = ["name","farmer_id", "farmer_name", "total_payable_amount"]
			x, a , b, c  = "farmer","farmer_id","farmer_name","total_payable_amount"

		elif self.payment_type == "H and T Billing Payment":
			doctype_name = "Child H and T Calculation"
			doctype_filter = {"docstatus": 1, "parent": self.document_name,} #"payment_status":0
			doctype_field = ["name","vender_id", "vender_name", "payable_amt","type","contract_id"]
			a, b, c  = "vender_id","vender_name","payable_amt" 

		elif self.payment_type == "H and T Advance Payment":
			doctype_name = "Advance Request item"
			doctype_filter = {"parent": self.document_name,} #"payment_status":False
			doctype_field = ["name","transporter_code", "name1", "sanction_amount"]
			x ,a ,b, c = "transporter","transporter_code","name1","sanction_amount" 

		elif self.payment_type == "Loan Payment":
			doctype_name = "Farmer Loan Application"
			doctype_filter = {"docstatus": 1,"branch": self.branch, "season": self.season,"payment_flag":False}
			doctype_field = ["name","applicant", "applicant_name", "loan_amount"]
			x,a ,b ,c = "farmer","applicant","applicant_name", "loan_amount"

		else:
			frappe.throw("Please select appropriate 'Payment Type'")

		doc = frappe.get_all(doctype_name, filters=doctype_filter, fields=doctype_field)

		
		for entry in doc:
      
			
			if self.payment_type == "H and T Billing Payment":
				bank_doc=frappe.get_all("Bank Details", filters = {"parent": entry.get(a),(str(entry.type.lower())):1},fields = ["bank_name"])
			else:
				bank_doc=frappe.get_all("Bank Details", filters = {"parent": entry.get(a),str(x):1} , fields = ["bank_name"])
				
    
			self.append(
				"vendor_amount_information",
				{
					"vendor_id": entry.get(a),
					"vendor_name": entry.get(b),
					"address" : frappe.get_value("Farmer List", entry.get(a), "village"),
					"total_amount": entry.get(c),
					"type": entry.type if  entry.type else None,
					"contract_id": entry.contract_id if entry.contract_id else None,
					"account_details":(bank_doc[0].bank_name) if bank_doc else 'Bank not found',
					"doc_name" : entry.name
				},
			)
			

	@frappe.whitelist()
	def sort_bank(self):
		for i in self.get("vendor_amount_information"):
			if i.check:
				if self.bank == None:
					frappe.throw("Please select Bank")
				# if i.account_details if i.account_details else i.account_details=='Bank not found':
				if self.bank == i.account_details :
					self.append(
						"self_bank_transfer",
						{
							"vendor_id": i.vendor_id,
							"vendor_name": i.vendor_name,
							"address" : i.address,
							"total_amount": i.total_amount,
							"type": i.type,
							"contract_id": i.contract_id,
							"account_details":i.account_details,
						},
					)
				else:
					self.append(
						"different_bank_transfer_vpe",
						{
							"vendor_id": i.vendor_id,
							"vendor_name": i.vendor_name,
							"address" : i.address,
							"total_amount": i.total_amount,
							"type": i.type,
							"contract_id": i.contract_id,
							"account_details":i.account_details if i.account_details else 'Bank not found',
						},
					)
				# else:
				# 	frappe.throw(f"Please Set the Bank of Vender: {get_link_to_form('Farmer List',i.vendor_id)}")
     
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

		self.change_status_on_sub()
  
  
	@frappe.whitelist()
	def before_cancel(self):
		self.change_status_on_can()
  
  
	@frappe.whitelist()
	def on_trash(self):
		self.change_status_on_can()


	
	@frappe.whitelist()
	def change_status_on_sub(self):
		payment_type_mapping = {
		'Cane Billing':'Child Calculation Cane Bill',
		'Advance Request':'Advance Request item',
		'H and T Billing':'Child H and T Calculation',
		'Farmer Loan Application': 'Farmer Loan Application',
		}
		doctye_name = payment_type_mapping.get(self.payment_type_doctype)

     
		for a in self.get("vendor_amount_information"):
			if a.check:
				frappe.db.set_value(doctye_name,a.doc_name,"payment_status",1)
    
    
	@frappe.whitelist()
	def change_status_on_can(self):
		payment_type_mapping = {
		'Cane Billing':'Child Calculation Cane Bill',
		'Advance Request':'Advance Request item',
		'H and T Billing':'Child H and T Calculation',
		'Farmer Loan Application': 'Farmer Loan Application',
		}
		doctye_name = payment_type_mapping.get(self.payment_type_doctype)
     
		for a in self.get("vendor_amount_information"):
			if a.check:
				frappe.db.set_value(doctye_name,a.doc_name,"payment_status",0)
		

			# table = self.append("vendor_amount_information", {})
			# table.vendor_id = entry.get(a)
			# table.vendor_name = entry.get(b)
			# table.total_amount = entry.get(c)

    # @frappe.whitelist()
    # def get_list(self):
    # 	if self.payment_type == 'Cane Billing Payment':
    # 		doctype_name="Child Calculation Cane Bill"
    # 		doctype_filter = {"docstatus": 1,"parent": self.document_name,"branch" : self.branch }
    # 		doctype_field = ["farmer_id","farmer_name","village","total_payable_amount",]
    # 		a,b,c,d ="farmer_id",  "farmer_name","village","total_payable_amount",

    # 	# if self.payment_type == 'H and T Advance Payment':
    # 	# 	doctype_name="Child Calculation Cane Bill"
    # 	# 	doctype_filter = {"docstatus": 1,"parent": self.document_name,"branch" : self.branch }
    # 	# 	doctype_field = ["farmer_id","farmer_name","village","total_payable_amount",]

    # 	if self.payment_type == 'H and T Billing Payment':
    # 		doctype_name="Child H and T Calculation"
    # 		doctype_filter = {"docstatus": 1,"parent": self.document_name,} #"branch" : self.branch
    # 		doctype_field = ["vender_id","vender_name","payable_amt",]

    # 	# if self.payment_type == 'Loan Payment':
    # 	# 	doctype_name="Child Calculation Cane Bill"
    # 	# 	doctype_filter = {"docstatus": 1,"parent": self.document_name,"branch" : self.branch }
    # 	# 	doctype_field = ["farmer_id","farmer_name","village","total_payable_amount",]

    # 	doc = frappe.get_all(doctype_name,filters=doctype_filter,fields=doctype_field,)
    # 	frappe.msgprint(str(doc))
    # 	# for FAR in doc:
    # 	# 	self.append(
    # 	# 			"vendor_amount_information",
    # 	# 			{
    # 	# 				"vendor_id": FAR.a,
    # 	# 				"vendor_name": FAR.b,
    # 	# 				"address": FAR.c,
    # 	# 				"total_amount": FAR.d,
    # 	# 			},
    # 	# 		)