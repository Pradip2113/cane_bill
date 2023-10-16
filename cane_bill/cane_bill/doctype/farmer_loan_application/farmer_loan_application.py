# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FarmerLoanApplication(Document):
	@frappe.whitelist()
	def before_save(self):
		self.loan_validation()
	@frappe.whitelist()
	def loan_validation(self):
		if self.loan_amount and self.maximum_amount:
			if self.loan_amount > self.maximum_amount:
				self.loan_amount=0
				frappe.throw(f"Loan Amount should not be greater than {self.maximum_amount} for Lone Type '{self.loan_type}'")
		

	@frappe.whitelist()
	def loan_i_p(self):
		if self.loan_type:
			if self.season:
				doc=frappe.get_doc("Farmer Loan Type",self.loan_type)
				self.rate_of_interest=doc.rate_of_interest
				self.repayment_period_in_years=doc.period_for_repayment
				self.append_on_installments_table()
			else:
				self.loan_type=""
				frappe.msgprint("Please select 'Posting Season'")
	
   
	@frappe.whitelist()
	def loan_amt_installment(self):
		if self.repayment_period_in_years and self.loan_amount:
			self.append_on_installments_table()

	@frappe.whitelist()
	def season_installment(self):
		if self.loan_amount and self.loan_type and  self.season:
			self.append_on_installments_table()
   
   
	@frappe.whitelist()
	def year_installment_installment(self):
		if self.loan_amount and self.loan_type and self.repayment_period_in_years:
			self.append_on_installments_table()
   
	@frappe.whitelist()
	def rate_of_interest_installment(self):
		if self.loan_amount and self.loan_type and self.repayment_period_in_years and self.rate_of_interest:
			self.append_on_installments_table()
		elif self.loan_amount and self.loan_type and self.repayment_period_in_years and self.rate_of_interest==0:
			self.append_on_installments_table()


	@frappe.whitelist()
	def append_on_installments_table (self):
		if self.loan_amount:
			loan_amt=self.loan_amount
			loan_installment_amt = int(loan_amt)/int(self.repayment_period_in_years)
		else:
			loan_installment_amt=0
   
		if self.rate_of_interest:
			loan_ir=self.rate_of_interest
			# loan_installment_amt = int(loan_amt)/int(self.repayment_period_in_years)
		else:
			loan_ir=0

		if self.season and self.repayment_period_in_years :
			current_year = int(self.season.split("-")[0])
			for i in range(int(self.repayment_period_in_years)):
				season_range = f"{current_year + i}-{current_year + i + 1}"
				self.append("installments_table", {
					"season": season_range,
					"installment": round((loan_installment_amt),2),
					"rate_of_interest":loan_ir,
					"interest":"Till The Billing Date",
     
				})
    
    #create new document on deduction form   before_submit   cndodf
	@frappe.whitelist()
	def  before_submit(self):
		self.on_update_after_submit()
  
  
	@frappe.whitelist()
	def target_Bank(self):
		doc = frappe.get_all("Bank Details", 
                    filters={ "Parent": self.applicant, "farmer": 1,"is_active":"Yes"}, 
                    fields=["bank_name", "branchifsc_code", "account_number", "bank_and_branch"])
		frappe.msgprint(doc)
		if doc:
			for d in doc:
				self.farmer_bank_name_=d.bank_and_branch
				# self.farmer_bank_branch=d.bank_name
				self.farmer_account_number=d.account_number
				self.framer_bank_ifsc_code=d.branchifsc_code
				

	@frappe.whitelist()
	def on_cancel(self):
		self.delete_document_after_cancle()
    
    
    # method used to create files in deduction form when tehy approved it  
	@frappe.whitelist()
	def on_update_after_submit(self):
			self.set_remaining_installment_amount_in_installment_table()
			if self.status == "Approved":
				for s in self.get("installments_table"):
					deduction_doc = frappe.get_all("Deduction Form",
                                            filters={"farmer_application_loan_id_child": s.name},
                                            fields={"name",},)
					if deduction_doc:
						pass
					else:
						doc = frappe.new_doc("Deduction Form")
						doc.season = s.season
						doc.date = self.posting_date   
						doc.branch = self.branch
						doc.farmer_code = self.applicant
						doc.deduction_name = self.loan_type
						doc.deduction_amount = s.installment
						doc.paid_amount = s.paid_installment
						doc.account = self.account_paid_to
						doc.farmer_application_loan_id = self.name
						doc.farmer_application_loan_id_child =s.name
						doc.rate_of_interest = s.rate_of_interest
						doc.interest_calculate_on_amount = s.interest_calculate_on_amount
						doc.from_date_interest_calculation = s.from_date_interest_calculation
						doc.account = self.account_paid_to
						doc.interest_account = self.account_interest_paid_to
						if(self.contract_id):
							doc.h_and_t_contract_id = self.contract_id
						doc.insert()
						doc.save()
						doc.submit()
				
    
		
	@frappe.whitelist()
	def delete_document_after_cancle(self):

		if self.status == "Approved":
				for s in self.get("installments_table"):
					deduction_doc = frappe.get_all("Deduction Form",
                                            filters={"farmer_application_loan_id_child": s.name},
                                            fields={"name",},)
					deduction_document = frappe.get_doc('Deduction Form', (deduction_doc[0].name))
					deduction_document.cancel()
					deduction_document.delete()


 
	@frappe.whitelist()
	def set_remaining_installment_amount_in_installment_table(self):
		previous_interest_calculate_on_amount = None
		for index, s in enumerate(self.get("installments_table")):
			if index == 0:
				s.interest_calculate_on_amount = self.loan_amount
				previous_interest_calculate_on_amount = round((float(s.interest_calculate_on_amount)-float(s.installment)),2)
				get_child_doc = frappe.get_doc("Child Farmer Loan Application",s.name)
				get_child_doc.save()
				
			else:
				s.interest_calculate_on_amount = previous_interest_calculate_on_amount
				previous_interest_calculate_on_amount = round((float(s.interest_calculate_on_amount)-float(s.installment)),2)
				get_child_doc = frappe.get_doc("Child Farmer Loan Application",s.name)
				get_child_doc.save()


	@frappe.whitelist()
	def get_register_ploat_for_applicant(self):
		total_area=0
		doc=  frappe.get_all("Cane Master",
                                            filters={"season": self.season , "grower_code" : self.applicant},
                                            fields={"area_acrs","name"},)
		if not doc:
			if not self.season:
					frappe.throw(f"Please select season")

		for d in doc :
			# total_area = round((total_area + d.area_acrs),2)
			pt = self.append("plot_table", {})
			pt.plot_no = d.name
			pt.total_area_in_acrs = d.area_acrs
			pt.check = 1
			
		if not self.plot_table:
			frappe.msgprint(f"There are no record of Cane registration of applicant {self.applicant} for season {self.season}")

		
		self.calculate_the_acrs()
  
	@frappe.whitelist()
	def calculate_the_acrs(self):
		sum_of_acrs=0
		sum_of_gunthas=0
		if self.plot_table:
			for s in self.get("plot_table"):
				if s.check:
					sum_of_acrs += (int(s.total_area_in_acrs))
					sum_of_gunthas += int(str(int((s.total_area_in_acrs) * 100) % 100).zfill(2))

			gunthas_into_acrs , remaining  = divmod(sum_of_gunthas, 40)
			
			total_acrs = (gunthas_into_acrs+sum_of_acrs)
			total_gunthas = remaining
			if total_gunthas<10:
				total_area_of_ploat = float(str(total_acrs) + '.0' + str(total_gunthas))
			else:
				total_area_of_ploat = float(str(total_acrs) + '.' + str(total_gunthas))
			self.total_area_in_acrs = total_area_of_ploat
		if self.loan_type:
			self.auto_fetch_amount()
    
	@frappe.whitelist()
	def auto_fetch_amount(self):
		if self.applicant:
			if self.total_area_in_acrs:
				doc=  frappe.get_all("Farmer Loan Type",
                                            filters={"name": self.loan_type },
                                            fields={"loan_amount_for_acrs",},)
				sum_of_gunthas = (int(str(int((self.total_area_in_acrs) * 100) % 100).zfill(2)))+((int(self.total_area_in_acrs))*40)
				amount_per_guntha = (doc[0].get("loan_amount_for_acrs"))/40
    
				self.loan_amount = round((sum_of_gunthas* amount_per_guntha),2)
				self.loan_amt_installment()
# ------------------------------------------------------------------------------------------------------------- 
		# if self.season:
		# 	for _ in range (int(self.repayment_period_in_years)):
		# 		self.append("installments_table",
		# 			{
		# 				"season": "pp",
		# 				"installment":0,
						
		# 			}
		# 		)



# if self.season:
		# 	current_year = int(self.season.split("-")[0])
		# 	installments = []
		# 	for i in range(int(self.repayment_period_in_years)):
		# 		season_range = f"{current_year + i}-{current_year + i + 1}"
		# 		installments.append({
		# 			"season": season_range,
		# 			"installment": 0,
		# 		})
		# 	self.installments_table = installments

