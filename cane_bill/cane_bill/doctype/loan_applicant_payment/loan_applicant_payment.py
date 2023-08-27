# Copyright (c) 2023, quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LoanApplicantPayment(Document):
    
    @frappe.whitelist()
    def list(self):

        doc = frappe.db.get_list("Farmer Loan Application",
                                                filters={"docstatus": 1,"season" : self.season ,"branch" : self.branch ,"status":"Approved","payment_status":0},
                                                fields=["name","applicant","applicant_name","loan_type","loan_amount", "address","account_paid_from","account_paid_to","account_interest_paid_to"],) 
        # frappe.msgprint(str(doc))

        applicant_list = {}
        for d in doc:
            applicant = d['applicant']
            if applicant in applicant_list:
                applicant_list[applicant]["loan_amount"] += round(float(d['loan_amount']), 2)
                applicant_list[applicant]["name"].append(d['name'])
                applicant_list[applicant]["loan_type"].append(d['loan_type'])
                account_details_list = {"account_paid_from": d['account_paid_from'],"account_paid_to": d['account_paid_to'],"account_interest_paid_to": d['account_interest_paid_to'],"amount": d['loan_amount'],}
                applicant_list[applicant]["account_details"].append(account_details_list)
            else:
                applicant_list[applicant] = {
                    "name": [d['name']],
                    "applicant": d['applicant'],
                    "applicant_name": d['applicant_name'],
                    "address": d['address'],
                    "loan_type": [d['loan_type']], 
                    "branch": self.branch,
                    "loan_amount": round(float(d['loan_amount']), 2),
                    "account_details": [{"account_paid_from": d['account_paid_from'],"account_paid_to": d['account_paid_to'],"account_interest_paid_to": d['account_interest_paid_to'],"amount": d['loan_amount'],}],
                    
                }
        # frappe.msgprint(str(applicant_list))
        for applicant, data in applicant_list.items():
            applicant_list_row = self.append("applicant_list", {})
            applicant_list_row.loan_application_id =str(data["name"])
            applicant_list_row.applicant = data["applicant"]
            applicant_list_row.applicant_name = data["applicant_name"]
            applicant_list_row.address = data["address"]
            applicant_list_row.loan_type = str(data["loan_type"])
            applicant_list_row.loan_amount = data["loan_amount"] 
            applicant_list_row.account_details = str(data["account_details"])
    
            
    @frappe.whitelist()
    def selectall(self):
        # pass
        children = self.get("applicant_list")
        if not children:
            return
        all_selected = all([child.check for child in children])
        value = 0 if all_selected else 1
        for child in children:
            child.check = value
        
        self.total_values()
            
            
            
    @frappe.whitelist()
    def total_values(self):
        total_payable_amount = 0
        
        totals=self.get("applicant_list")
        for d in totals:
            if d.check:
                total_payable_amount = total_payable_amount+round(float(d.loan_amount),2)
        
        self.net_total_payable_amount = total_payable_amount
            

    @frappe.whitelist()
    def before_submit(self):
        self.change_status_FLA()
        self.set_date_on_deduction_form()
        self.journal_entery_of_payment()
        
    @frappe.whitelist()
    def before_cancel(self):
        self.change_status_FLA_on_cancel()
        self.set_date_on_deduction_form_on_cancel()
        self.cancel_journal_entry()
        
        
    @frappe.whitelist()
    def change_status_FLA(self):
        for FAR in self.get("applicant_list"):
            if FAR.check:
                for i in eval(FAR.loan_application_id):
                    frappe.db.set_value("Farmer Loan Application",(str(i)),"payment_status",1)
                
    @frappe.whitelist()
    def change_status_FLA_on_cancel(self):
        for FAR in self.get("applicant_list"):
            if FAR.check:
                for i in eval(FAR.loan_application_id):
                    frappe.db.set_value("Farmer Loan Application",(str(i)),"payment_status",0)
                
    @frappe.whitelist()
    def set_date_on_deduction_form(self):
        for FAR in self.get("applicant_list"):
            if FAR.check:
                for i in eval(FAR.loan_application_id):
                    doc = frappe.get_all("Deduction Form",
                                                        filters={ "docstatus": 1 ,"farmer_application_loan_id":(str(i)),"season":self.season, },  #"date": ["between", [self.from_date, self.to_date]]
                                                        fields={"name",},)
                    for d in doc:
                        frappe.db.set_value("Deduction Form",d.name,"from_date_interest_calculation",self.posting_date)
                    
                    
    @frappe.whitelist()
    def set_date_on_deduction_form_on_cancel(self):
        for FAR in self.get("applicant_list"):
            if FAR.check:
                for i in eval(FAR.loan_application_id):
                    doc = frappe.get_all("Deduction Form",
                                                        filters={ "docstatus": 1 ,"farmer_application_loan_id":(str(i)),"season":self.season, },  #"date": ["between", [self.from_date, self.to_date]]
                                                        fields={"name",},)
                    for d in doc:
                        frappe.db.set_value("Deduction Form",d.name,"from_date_interest_calculation",None)
    
    
    
    @frappe.whitelist()
    def journal_entery_of_payment(self):
        counter =0
        branch_doc = frappe.get_all("Branch",
                                            filters={"name": self.branch},
                                            fields={"cane_rate", "name","company","debit_in_account_currency"},)
        if branch_doc:
            if not (branch_doc[0].company):
                frappe.throw( f" Please set Company for Branch '{str(self.branch) } '")
                
            if not (branch_doc[0].debit_in_account_currency):
                frappe.throw( f" Please set Debit Account for Branch '{str(self.branch) } '")
            company =  ((branch_doc[0].company))
            acc_to_set_debit_side = ((branch_doc[0].debit_in_account_currency))
        
        
        je = frappe.new_doc("Journal Entry")
        je.voucher_type = "Journal Entry"
        je.company = company
        je.posting_date = self.posting_date
        
        for s in self.get("applicant_list"):
            if s.check:
                counter = counter + 1
                # if s.total_deduction:
                # frappe.msgprint(str(eval(s.loan_type)))
                # frappe.msgprint(str(eval(s.loan_application_id)))
                # frappe.msgprint(str(eval(s.account_details)))
                je.append(
                    "accounts",
                    {
                        "account": self.account_credit_to,
                        "credit_in_account_currency": round(s.loan_amount,2),
                        
                    },)
                
                for data_se in (eval(s.account_details)):
                    frappe.msgprint(str(data_se["account_paid_from"]))
                    je.append(
                        "accounts",
                        {
                            "account": (data_se["account_paid_to"]),
                            "party_type": "Customer",
                            "party": s.applicant,
                            "debit_in_account_currency": data_se["amount"],

                        },)            
        if counter > 0:
            je.insert()
            je.save()
            je.submit()
            journal_entry = frappe.db.get_all("Journal Entry", fields=["name"], order_by="creation DESC", limit=1)
            self.journal_entry_id = str(journal_entry[0].name)
        
    @frappe.whitelist()
    def cancel_journal_entry(self):
        doc = frappe.get_doc("Journal Entry", (str(self.journal_entry_id)))
        if doc.docstatus == 1:
            doc.cancel()
            
                # frappe.set_value()
                # doc = frappe.get_all("Farmer Loan Application",
                #                                             filters={ "docstatus": 1, "payment_status": 0,"name":(str(i)),},  #"date": ["between", [self.from_date, self.to_date]]
                #                                             fields={"actual_weight", "farmer_code", "is_kisan_card"},)
            # for d in (FAR.loan_application_id):
            #     frappe.msgprint(str(d))                
            # if FAR.check:
            #     doc = frappe.get_all("Farmer Loan Application",
            #     filters={ "docstatus": 1, "payment_status": 0,"farmer_code": FAR.farmer_id,},  #"date": ["between", [self.from_date, self.to_date]]
            #     fields={"actual_weight", "farmer_code", "is_kisan_card"},)

            

          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          