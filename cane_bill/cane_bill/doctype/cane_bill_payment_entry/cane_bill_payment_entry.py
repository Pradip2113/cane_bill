# Copyright (c) 2023, quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CaneBillPaymentEntry(Document):
    
    @frappe.whitelist()
    def get_list(self):
        doc = frappe.get_all("Child Calculation Cane Bill",
                                                filters={"docstatus": 1,"today": ["between", [self.from_date, self.to_date]],"branch" : self.branch },
                                                fields=["farmer_id","farmer_name","village","branch","total_weight","rate_kg","total_collection_amount","sales_invoice_deduction","lone_deduction",
                                                        "loan_interest_deduction", "total_deduction" ,"total_payable_amount",],)
        

        for FAR in doc:
            self.append(
                    "payable_list",
                    {
                        "farmer_id": FAR.farmer_id,
                        "farmer_name": FAR.farmer_name,
                        "village": FAR.village,
                        "branch" : FAR.branch,
                        "total_weight": FAR.total_weight,
                        "rate_kg": FAR.rate_kg,
                        "total_collection_amount": FAR.total_collection_amount,
                        "sales_invoice_deduction": FAR.sales_invoice_deduction,
                        "lone_deduction": FAR.lone_deduction,
                        "loan_interest_deduction": FAR.loan_interest_deduction,
                        "total_deduction": FAR.total_deduction,
                        "total_payable_amount": FAR.total_payable_amount,
                       
                    },
                )
            
        
        
        
    




