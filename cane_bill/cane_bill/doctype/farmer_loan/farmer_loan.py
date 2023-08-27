# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FarmerLoan(Document):
	@frappe.whitelist()
	def after_insert_data(self):
		if self.application:
			application = frappe.get_doc("Farmer Loan Application", self.application)

			child_table_rows = application.get("installments_table")

			# Clear existing rows in the child table
			self.set("installment_table", [])

			# Replicate the child table from Farmer Loan Application to Farmer Loan
			for row in child_table_rows:
				new_row = self.append("installment_table", {})
				new_row.season = row.season
				new_row.installment = row.installment
				new_row.rate_of_interest = row.rate_of_interest
				new_row.interest = row.interest
				# Repeat this for other fields you want to replicate

			# self.save()
	
	@frappe.whitelist()
	def before_da(self):
		total_before_amount=0
		existing_installment = frappe.get_all('Farmer Loan', filters={'application': self.application , "docstatus": 1},fields=["disbursement_amount","name"])
		for ei in existing_installment:
			# frappe.msgprint(ei.disbursement_amount)
			total_before_amount=int(total_before_amount)+int(ei.disbursement_amount)
		self.disbursemented_amount=total_before_amount
		self.disbursement_amount=int(self.loan_amount) - (self.disbursemented_amount)
		self.update_installment()
  
	@frappe.whitelist()
	def update_installment(self):
		if self.disbursement_amount:
			d_a=int(self.disbursement_amount)/int(self.period_for_repayment)
			for d in self.get("installment_table"):
				d.installment=d_a
    
    
    
	@frappe.whitelist()
	def validation_for_disbursement_amount(self):
		if self.disbursement_amount:
			temp_1=0
			temp_2=0
			temp_1=int(self.disbursemented_amount)+int(self.disbursement_amount)
			if (int(temp_1)) > (int(self.loan_amount)):
				temp_2=int(self.loan_amount)-int(self.disbursemented_amount)
				frappe.msgprint(f"Amount Should not be greater than {temp_2} ")
				self.disbursement_amount=0
    
    
	@frappe.whitelist()
	def before_submit(self):
		# frappe.msgprint("ftrgyddfsdhjjjhb")
		doc = frappe.new_doc("Payment Entry")
		doc.payment_type = "Pay"
		doc.posting_date = self.posting_date
		doc.mode_of_payment = "Bank Draft"
		doc.party_type = "Supplier"
		doc.party = self.applicant_id
		doc.party_name = self.applicant_name
		doc.paid_from =  self.account_paid_from
		doc.paid_from_account_currency = "INR"
		doc.paid_to = self.account_paid_to
		doc.paid_to_account_currency = "INR"
		doc.paid_amount = self.disbursement_amount
		doc.reference_no = self.reference_no
		doc.reference_date = self.reference_date
		doc.received_amount = self.disbursement_amount
		doc.received_amount_after_tax = self.disbursement_amount
		doc.target_exchange_rate = 1
		doc.insert()
		doc.save()
		doc.submit()
		payment_entry = frappe.db.get_all("Payment Entry", fields=["name"], order_by="creation DESC", limit=1)
		self.payment_entry_id= (str(payment_entry[0].name))
		self.set_posting_date_to_first_installment()
		self.set_remaining_installment_amount_in_installment_table()
		self.validation_of_installments()
		for s in self.get("installment_table"):
			s.installment_status=0
			s.interest_status=0
  
  
	@frappe.whitelist()           
	def before_cancel(self):
		self.cancel_payment_entry()
	@frappe.whitelist()
	def on_update_after_submit(self):
		self.set_remaining_installment_amount_in_installment_table()
		self.validation_of_installments()
	@frappe.whitelist()
	def set_posting_date_to_first_installment(self):
		for s in self.get("installment_table"):
			s.from_date_interest_calculation=self.posting_date
			s.interest_calculate_on_amount=self.disbursement_amount
			break


	@frappe.whitelist()
	def set_remaining_installment_amount_in_installment_table(self):
		previous_interest_calculate_on_amount = None
		for index, s in enumerate(self.get("installment_table")):
			if index == 0:
				previous_interest_calculate_on_amount = (int(s.interest_calculate_on_amount)-int(s.installment))
				get_child_doc = frappe.get_doc("Child Farmer Loan",s.name)
				get_child_doc.save()
				
			else:
				s.interest_calculate_on_amount = previous_interest_calculate_on_amount
				previous_interest_calculate_on_amount = (int(s.interest_calculate_on_amount)-int(s.installment))
				get_child_doc = frappe.get_doc("Child Farmer Loan",s.name)
				get_child_doc.save()
	





    
	@frappe.whitelist()
	def validation_of_installments(self):
		# frappe.msgprint("fhgkjhfkhhkhkhkj")
		temp_amount=0
		if self.disbursement_amount:
			for s in (self.get("installment_table")):
				temp_amount=temp_amount+int(s.installment)
			if int(temp_amount) != int(self.disbursement_amount):
				frappe.throw(f"The Addition of all installments must be equal to {self.disbursement_amount}")
				
			
	@frappe.whitelist()           
	def cancel_payment_entry(self):
		doc = frappe.get_doc("Payment Entry",(str(self.payment_entry_id)))
		doc.cancel()		


		
		# for s in self.get("installment_table"):
		# 	self.
# ------------------------------------------------------------------------------------------------------------------------------------------			
		# # frappe.msgprint("ghhfjhfhfg")
		# # frappe.msgprint(self.disbursement_amount)
		# # frappe.msgprint(self.period_for_repayment)
		# d_a=int(self.disbursement_amount)/int(self.period_for_repayment)
		# # existing_cropsampling = frappe.get_all('Crop Harvesting', filters={'crop_sample_id': self.name})
		# doc= frappe.get_all('Child Farmer Loan', filters={'parent': self.name},fields=["installment","name"])
		# for d in self.get("installment_table"):
		# 	d.installment=d_a
		# # for d in doc:
		# 	# frappe.msgprint(str(d_a))
		# 	# frappe.msgprint(str(d.name))
		# 	# child_doc = frappe.get_doc('Child Farmer Loan', d.name)
		# 	# child_doc.installment = d_a
		# 	# child_doc.save()
			
		# 	# d.installment=0
		# 	# d.save()
		



# temp=0
# 		temto=0
# 		if self.disbursement_amount:
# 			temp=int(self.disbursemented_amount)+int(self.disbursemented_amount)
# 			if int(self.loan_amount)<int(temp):
# 				d_a=int(self.disbursement_amount)/int(self.period_for_repayment)
# 				for d in self.get("installment_table"):
# 					d.installment=d_a
# 			else:
# 				temto=int(self.loan_amount)-int(self.disbursemented_amount)
# 				frappe.msgprint(f"Amount Should not be greater than {temto} ")

