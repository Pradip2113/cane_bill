# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate
from frappe.model.document import Document
from frappe.utils import get_link_to_form

from datetime import datetime
    

class CaneBilling(Document):
    # ------------------------------------------------------------------------------------------------------------

    @frappe.whitelist()
    def vivek(self):

        # **********if you want to change or any kind of update in this method the make sure check other method because data is filter from this metod used to change billing_status from Cane Weight
        b_s = 0
        if self.advance_type != "First Advance":
            b_s = 1
        
        farmer_list_in_date = []
        doc = frappe.db.get_list("Cane Weight",
                                                filters={"docstatus": 1,"date": ["between", [self.from_date, self.to_date]],"billing_status": b_s,"season" : self.season ,"branch" : self.branch },
                                                fields=["farmer_name","farmer_village","date","farmer_code","docstatus","billing_status","cane_variety","state","is_kisan_card","water_supplier_code","water_supplier_name"],)
        for d in doc:
            # if str(self.from_date) <= str(d.date) <= str(self.to_date) and d.docstatus == 1 and d.billing_status == 0:  #*****please do not remove this commented line contact vivek.kumbhar@erpdata.in
            farmer_list_in_date.append({
                    "farmer_name": d.farmer_name,
                    "farmer_code": d.farmer_code,
                    "farmer_village": d.farmer_village,
                    "date": d.date,
                    "cane_variety": d.cane_variety ,
                    "state": d.state,
                    "is_kisan_card": d.is_kisan_card,})
            if d.water_supplier_code:
                farmer_list_in_date.append({
                        "farmer_name": d.water_supplier_name ,
                        "farmer_code": d.water_supplier_code,
                        "farmer_village":frappe.get_value("Farmer List", d.water_supplier_code, "village"),
                        # "date": d.date,
                        # "cane_variety": d.cane_variety ,
                        # "state": d.state,
                        "is_kisan_card": d.is_kisan_card,
                        })



        existing_farmer_codes = [ft.farmer_code for ft in self.farmer_table]  # Get existing farmer codes in the child table
        
        for farmer in farmer_list_in_date:
            if farmer["farmer_code"] not in existing_farmer_codes:
                if (( not self.village ) or (self.village == farmer["farmer_village"])) and (( not self.state) or (self.state == farmer["state"])) and (( not self.cane_variety) or (self.cane_variety == farmer["cane_variety"])):

                        farmer_table = self.append("farmer_table", {})
                        farmer_table.farmer_name = farmer["farmer_name"]
                        farmer_table.farmer_id = farmer["farmer_code"]
                        farmer_table.village = farmer["farmer_village"]
                        # farmer_table.date = farmer["date"] 
                        # farmer_table.cane_variety = farmer["cane_variety"]
                        farmer_table.is_kisan_card = farmer["is_kisan_card"]
                        # farmer_table.state = farmer["state"]
                        existing_farmer_codes.append(farmer["farmer_code"])  # Add the farmer code to the existing farmer codes list


    @frappe.whitelist()
    def selectall(self):
        # pass
        children = self.get("farmer_table")
        if not children:
            return
        all_selected = all([child.check for child in children])
        value = 0 if all_selected else 1
        for child in children:
            child.check = value
            
    #     deduction_forms = frappe.get_all("Deduction Form", fields={"name"},)

    # # Update each record with the new account value
    #     for deduction_form in deduction_forms:
    #         frappe.db.set_value("Deduction Form", deduction_form.name, "paid_amount", 0)

            


    @frappe.whitelist()
    def billing(self):
        b_s = 0
        if self.advance_type != "First Advance":
            b_s = 1
        cane_rate = 0
        cane_price = frappe.get_all("Branch",
                                            filters={"name": self.branch},
                                            fields={"cane_rate", "name","additional_rate_for_kisan_card_holder"},)
        if cane_price:
            cane_rate =  ((cane_price[0].cane_rate))
            AKCA = ((cane_price[0].additional_rate_for_kisan_card_holder))
            # frappe.msgprint(str(AKCA))
        if cane_rate == 0:
                frappe.throw( f" Please set Cane Rate/Ton for Branch '{get_link_to_form('Branch', self.branch) } '")
             
 
        
        for FAR in self.get("farmer_table"):
            total_weight = 0
            total_weight_kissan = 0
            binding_weight=0
            Total_collection_amount = 0
            total_deduction = 0
            sales_invoice_deduction = 0
            sales_invoices = []
            loan_installment_amount = 0
            loan_interest_amount = 0
            loan_installment = []
            loan_installment_intrest = []
            all_deduction = []
            total_payable = 0
            additional_rate = 0
            total_other_deductions=0
            other_deduction_dict =[]
            p=0
            q=0

            if FAR.check:
                # in doc all document are collcted from 'Cane Weight' where farmer is FAR.farmer_id
                doc = frappe.get_all("Cane Weight",
                                                    filters={ "docstatus": 1,"date": ["between", [self.from_date, self.to_date]], "billing_status": b_s,"farmer_code": FAR.farmer_id,},
                                                    fields={"actual_weight", "binding_weight","farmer_code", "is_kisan_card"},)
                # frappe.msgprint(str(doc))
                for d in doc:
                    if d.actual_weight:
                        if d.is_kisan_card=="Yes":
                            p=round(d.actual_weight,3)
                            total_weight_kissan=  total_weight_kissan +(p) # here all cane weight,s  will calculate    [total_weight += round((float(d.actual_weight) / 1000), 2)]
                            total_weight_kissan=round(total_weight_kissan,3)
                            # frappe.msgprint(str(total_weight_kissan))
                        else :
                            q =round(d.actual_weight,3)
                            total_weight = total_weight+(q)
                            total_weight=round(total_weight,3)
                            # frappe.msgprint(str(total_weight))
                        binding_weight += ((d.binding_weight))
                        
                moc = frappe.get_all("Cane Weight",
                                                    filters={ "docstatus": 1,"date": ["between", [self.from_date, self.to_date]], "billing_status": b_s,"water_supplier_code": FAR.farmer_id,},
                                                    fields={"water_supplier_weight", "binding_weight","farmer_code", "is_kisan_card"},)
                
                # frappe.msgprint(str(moc))
                for m in moc:
                    if m.water_supplier_weight:
                        if m.is_kisan_card=="Yes":
                            p=round(m.water_supplier_weight,3)
                            total_weight_kissan = total_weight_kissan+(p)
                            total_weight_kissan=round(total_weight_kissan,3)
                            # frappe.msgprint(str(total_weight_kissan))
                            
                        else :
                            q =round(m.water_supplier_weight,3)
                            total_weight =  total_weight+(q)
                            total_weight=round(total_weight,3)
                            # frappe.msgprint(str(total_weight))
                        
                            
                if FAR.is_kisan_card and self.kisan_card:
                    if FAR.is_kisan_card == "Yes" :
                        additional_rate = AKCA
                   

                Total_collection_amount = ((total_weight)*cane_rate) + ((total_weight_kissan) * (cane_rate + additional_rate))
                
                # frappe.msgprint(str(total_weight))
                total_weight =  (((total_weight) + (total_weight_kissan)))
                # frappe.msgprint(str(total_weight))   
                # frappe.msgprint((str(total_weight))+"-"(str(total_weight_kissan)))
                
                other_deductions = frappe.get_all("Deduction Form",
                                                            filters={"farmer_code": FAR.farmer_id,"docstatus":1, "season" : self.season , "deduction_status" : 0,'h_and_t_contract_id':"",},
                                                            fields=["farmer_code", "account", "name", "deduction_amount","paid_amount" , "farmer_application_loan_id","interest_calculate_on_amount", "rate_of_interest" , "from_date_interest_calculation","interest_account" ,"update_from_date_interest_calculation",],)
                if self.includes_other_deduction_deduction:
                    other_deduction_dict = [{"Farmer Code": o_d.farmer_code,"Deduction Amount": round((float(o_d.deduction_amount) - float(o_d.paid_amount)),2),"Account": o_d.account,"DFN": o_d.name,}for o_d in other_deductions if not o_d.farmer_application_loan_id ]
                    total_other_deductions = sum(float(g["Deduction Amount"]) for g in other_deduction_dict)
                    
                if self.includes_loan_installment:
                    loan_installment = [{"Farmer Loan ID": o_l.farmer_application_loan_id, "Farmer ID": o_l.farmer_code , "season": self.season, "Account": o_l.account, "Installment Amount": round((float(o_l.deduction_amount) - float(o_l.paid_amount)),2) }for o_l in other_deductions if o_l.farmer_application_loan_id and (round((float(o_l.deduction_amount) - float(o_l.paid_amount)),2)) != 0 ]
                    loan_installment_amount = sum(float(j["Installment Amount"]) for j in loan_installment)
                    
                if self.includes_loan_interest:
                    loan_installment_intrest = [{
                                                    "Farmer Loan ID": o_i.farmer_application_loan_id,
                                                    "Farmer ID": o_i.farmer_code,
                                                    "season": self.season,
                                                    "Account": o_i.interest_account,
                                                    "Installment Interest Amount": round(round(float(float(o_i.interest_calculate_on_amount)-float(o_i.paid_amount)) * (float(o_i.rate_of_interest) / 100) * ((datetime.strptime(self.to_date, "%Y-%m-%d") - datetime.strptime((str(o_i.from_date_interest_calculation)), "%Y-%m-%d")).days / 365), 2) +  round(float(float(o_i.interest_calculate_on_amount)-float(o_i.paid_amount)) * (float(o_i.rate_of_interest) / 100) * ((datetime.strptime(self.to_date, "%Y-%m-%d") - datetime.strptime((str(o_i.update_from_date_interest_calculation)), "%Y-%m-%d")).days / 365), 2),2)
                                                }
                                                
                                                if o_i.update_from_date_interest_calculation
                                                else 
                                                {
                                                    "Farmer Loan ID": o_i.farmer_application_loan_id,
                                                    "Farmer ID": o_i.farmer_code,
                                                    "season": self.season,
                                                    "Account": o_i.interest_account,
                                                    "Installment Interest Amount": round(float(o_i.interest_calculate_on_amount)* (float(o_i.rate_of_interest) / 100)* ((datetime.strptime(self.to_date, "%Y-%m-%d")- datetime.strptime((str(o_i.from_date_interest_calculation)),"%Y-%m-%d",)).days/ 365),2,),
                                                }
                                                
                                                for o_i in other_deductions if o_i.farmer_application_loan_id  and (round((float(o_i.deduction_amount) - float(o_i.paid_amount)),2)) != 0 and o_i.from_date_interest_calculation ]
                    loan_interest_amount = sum(float(m["Installment Interest Amount"]) for m in loan_installment_intrest)

                # in deduction_doc all document are collcted  from 'Sales Invoice' where farmer is FAR.farmer_id and status are ['Unpaid', 'Overdue', 'Partly Paid'] 'h_and_t_contract_id':None
                if self.includes_sales_invoice_deduction:
                    deduction_doc = frappe.get_all("Sales Invoice",
                                                                    filters={"sale_type": ["!=", "H and T Sales"],"customer": FAR.farmer_id,"status": ["in", ["Unpaid", "Overdue", "Partly Paid"]],},
                                                                    fields=["outstanding_amount", "customer", "name", "debit_to",],)
                    # frappe.throw(str(deduction_doc))
                    sales_invoices = [{"Sales invoice ID": d_d.name,"Outstanding Amount": d_d.outstanding_amount,"Account": d_d.debit_to,}for d_d in deduction_doc]  # in this list all sales invoice will recored with there accound and outstanding_amount info
                    sales_invoice_deduction = sum(float(d["Outstanding Amount"]) for d in sales_invoices)  # calculating sum of all sales invoice


                total_deduction = (sales_invoice_deduction+ loan_installment_amount+ loan_interest_amount+total_other_deductions)
                total_payable = float(Total_collection_amount) - float(total_deduction)

                if total_payable < 0: 
                    doc_acc = frappe.get_all("Account Priority Child",
                                                            filters={"parent": self.branch},
                                                            fields={"priority_account", "idx"},order_by="idx ASC",)  # frappe.msgprint(str(doc_acc))  #$$$$$
                    
                    all_deduction = ( loan_installment_intrest   + loan_installment + sales_invoices+other_deduction_dict)  # frappe.msgprint(str(all_deduction))
                    all_deduction = sorted(all_deduction,key=lambda x: next((item["idx"] for item in doc_acc if item["priority_account"] == x["Account"]),len(doc_acc) + 1,),)

                    while float(Total_collection_amount) < float(total_deduction):
                        last_poped_entry = all_deduction.pop(-1)
                        total_sum = float(sum([
                                                float(entry.get("Installment Interest Amount", 0))
                                                + float(entry.get("Installment Amount", 0))
                                                + float(entry.get("Outstanding Amount", 0))
                                                + float(entry.get("Deduction Amount", 0))
                                                for entry in all_deduction
                                            ]))

                        total_deduction = float(total_sum)
                        total_payable = float(Total_collection_amount) - float (total_deduction)

                    contains_key = next((key for key in ["Outstanding Amount","Installment Amount","Installment Interest Amount","Deduction Amount"] if key in last_poped_entry),None,)
                    if (str(contains_key)) == "Outstanding Amount":
                        new_outstanding_amount = round(float(total_payable), 2)
                        total_deduction = round((float(total_deduction) + float(total_payable)), 2)
                        total_payable = 0
                        last_poped_entry["Outstanding Amount"] = new_outstanding_amount
                        all_deduction.append(last_poped_entry)
                        
                        
                        
                    if (str(contains_key))== "Installment Amount":
                        # updating_temp_out_amount = last_poped_entry.get('Outstanding Amount')
                        paid_amount =round(float(total_payable),2)
                        total_deduction =round(( float(total_deduction)+ float(total_payable)),2)
                        total_payable=0
                        last_poped_entry['Installment Amount'] = paid_amount
                        all_deduction.append(last_poped_entry)
                        
                        
                        
                    if (str(contains_key)) == "Deduction Amount":
                        new_other_deduction_amount = round(float(total_payable), 2)
                        total_deduction = round((float(total_deduction) + float(total_payable)), 2)
                        total_payable = 0
                        last_poped_entry["Deduction Amount"] = new_other_deduction_amount
                        all_deduction.append(last_poped_entry)
                        
                    

                    loan_installment_amount = sum(float(record['Installment Amount']) for record in all_deduction if 'Installment Amount' in record)
                    loan_interest_amount = sum(float(record['Installment Interest Amount']) for record in all_deduction if 'Installment Interest Amount' in record)
                    sales_invoice_deduction = sum(float(record['Outstanding Amount']) for record in all_deduction if 'Outstanding Amount' in record)
                    total_other_deductions = sum(float(record['Deduction Amount']) for record in all_deduction if 'Deduction Amount' in record)

                    loan_installment = [record for record in all_deduction if 'Installment Amount' in record]
                    loan_installment_intrest = [record for record in all_deduction if 'Installment Interest Amount' in record]
                    sales_invoices = [record for record in all_deduction if 'Outstanding Amount' in record]
                    other_deduction_dict = [record for record in all_deduction if 'Deduction Amount' in record]

                self.append(
                    "calculation_table",
                    {
                        "farmer_name": FAR.farmer_name,
                        "farmer_id": FAR.farmer_id,
                        "village": FAR.village,
                        "branch" : self.branch,
                        "advance_type" : self.advance_type,
                        "total_weight": round(total_weight,3),
                        "binding_weight_kg": round(binding_weight,3),
                        "rate_kg": (cane_rate + additional_rate),
                        "total_collection_amount": Total_collection_amount,
                        "sales_invoice_deduction": sales_invoice_deduction,
                        "other_deductions" : total_other_deductions,
                        "lone_deduction": loan_installment_amount,
                        "loan_interest_deduction": loan_interest_amount,
                        "total_deduction": total_deduction,
                        "total_payable_amount": total_payable,
                        "sales_invoice_information": str(sales_invoices),
                        "farmer_loan_information": str(loan_installment),
                        "farmer_loan_interest_information": str(loan_installment_intrest),
                        "other_deduction_information" : str(other_deduction_dict)
                        
                    },
                )
                
        self.total_values()
        
        # self.je_of_sales_invoice_and_farmer_loan()
    @frappe.whitelist()
    def total_values(self):
        total_weight = 0
        total_collection_amount = 0
        total_deduction = 0
        total_payable_amount = 0
        total_binding_weight = 0
        
        totals=self.get("calculation_table")
        for d in totals:
            total_weight = total_weight+round(float(d.total_weight),3)
            total_collection_amount = total_collection_amount+round(float(d.total_collection_amount),2)
            total_deduction = total_deduction+round(float(d.total_deduction),2)
            total_payable_amount = total_payable_amount+round(float(d.total_payable_amount),2)
            total_binding_weight += round(float(d.binding_weight_kg),3)
            
        self.net_total_weight = total_weight
        self.net_total_collection_amount = total_collection_amount
        self.net_total_deduction = total_deduction
        self.net_total_payable_amount = total_payable_amount
        self.net_total_binding_weight = round((total_binding_weight)/1000,3)
        # frappe.msgprint(str(total_weight))
        # frappe.msgprint(str(total_collection_amount))
        # frappe.msgprint(str(total_deduction))
        # frappe.msgprint(str(total_payable_amount))
        # # pass

    @frappe.whitelist()
    def before_save(self):
        self.bill_status_change_of_cane_weight()

    @frappe.whitelist()
    def on_trash(self):
        self.bill_status_change_of_cane_weight_on_cancel()

    @frappe.whitelist()
    def before_submit(self):
        self.bill_status_change_of_cane_weight()
        self.bulk_purchase_invoice()
        self.je_of_sales_invoice_and_farmer_loan()
        self.interest_je()
        self.update_value_in_farmer_loan()
        # self.change_status_of_farmer_loan()
        self.set_date_in_farmer_loan_child_for_next_installment()
        self.update_value_in_deduction_form()
        self.delete_row_record()

    @frappe.whitelist()
    def before_cancel(self):
        self.bill_status_change_of_cane_weight_on_cancel()
        self.cancel_journal_entry()
        self.interest_je_on_cancle()
        self.bulk_purchase_invoice_cancel()
        self.update_value_in_farmer_loan_cancel()
        # self.change_status_of_farmer_loan_on_cancel()
        self.set_date_in_farmer_loan_child_for_next_installment_on_cancel()
        self.update_value_in_deduction_form_on_cancel()
        
        
    @frappe.whitelist()
    def interest_je(self):
        je_list=[]
        for viv in self.get("calculation_table"):      
            for each in eval(viv.farmer_loan_interest_information):
                # frappe.throw(str((each["Farmer Loan ID"])))
                je = frappe.new_doc("Journal Entry")
                je.voucher_type = "Journal Entry"
                je.company = frappe.get_value("Branch",self.branch,"company")
                je.posting_date = self.today
                je.append(
                    "accounts",
                    {
                        "account": each["Account"],
                        "party_type": "Customer",
                        "party": viv.farmer_id,
                        "debit_in_account_currency": round(each["Installment Interest Amount"],2),
                        
                    },)
                je.append(
                        "accounts",
                        {
                            "account": frappe.get_value("Farmer Loan Application",(each["Farmer Loan ID"]),"account_interest_credit"),
                            "credit_in_account_currency": round(each["Installment Interest Amount"],2),

                        },)
                je.insert()
                je.save()
                je.submit()
                journal_entry = frappe.db.get_all("Journal Entry", fields=["name"], order_by="creation DESC", limit=1)
                je_list.append(str(journal_entry[0].name))
        # frappe.throw(str(je_list))
        self.interest_journal_entry_id = (str(je_list))
        
    @frappe.whitelist()
    def interest_je_on_cancle(self):
        if self.interest_journal_entry_id:
            for xox in eval(self.interest_journal_entry_id):
                doc = frappe.get_doc("Journal Entry", xox)
                if doc.docstatus == 1:
                    doc.cancel()
                # ---------------------------------------------------
                    
                
                        

    @frappe.whitelist()
    def bill_status_change_of_cane_weight(self):
        pop = self.get("calculation_table")
        for p in pop:
            cane_weight_docs = frappe.get_all("Cane Weight",
                                                filters={"farmer_code": p.farmer_id,"date": ["between", [self.from_date, self.to_date]],"docstatus": 1,"billing_status": 0,},
                                                fields=["farmer_code", "date", "name"],)
            for k in cane_weight_docs:
                frappe.db.set_value("Cane Weight", k.name, "billing_status", 1)

    @frappe.whitelist()
    def bill_status_change_of_cane_weight_on_cancel(self):
        non = self.get("calculation_table")
        for q in non:
            cane_weight_docs_c = frappe.get_all("Cane Weight",
                                                filters={"farmer_code": q.farmer_id,"date": ["between", [self.from_date, self.to_date]],"docstatus": 1,"billing_status": 1,},
                                                fields=["farmer_code", "date", "name"],)
            for t in cane_weight_docs_c:
                frappe.db.set_value("Cane Weight", t.name, "billing_status", 0)
                
                
                
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
    @frappe.whitelist()
    def bulk_purchase_invoice(self):
        branch_doc = frappe.get_all("Branch",
                                            filters={"name": self.branch},
                                            fields={ "name","company","cost_center","sugar_cane_item_code_","naming_series_for_purchase_invoice","credit_to"},)
        if branch_doc:
            if not (branch_doc[0].company):
                frappe.throw( f" Please set Company for Branch '{str(self.branch) } '")
            
            if not (branch_doc[0].cost_center):
                frappe.throw( f" Please set cost_center for Branch '{str(self.branch) } '")

            if not (branch_doc[0].sugar_cane_item_code_):
                frappe.throw( f" Please set sugar_cane_item_code_ for Branch '{str(self.branch) } '")

            if not (branch_doc[0].naming_series_for_purchase_invoice):
                frappe.throw( f" Please set naming_series_for_purchase_invoice for Branch '{str(self.branch) } '")

            if not (branch_doc[0].credit_to):
                frappe.throw( f" Please set credit_to for Branch '{str(self.branch) } '")


            i_c = ((branch_doc[0].sugar_cane_item_code_))
            c_c = ((branch_doc[0].cost_center))
            company =  ((branch_doc[0].company))
            n_s = ((branch_doc[0].naming_series_for_purchase_invoice))
            c_a = ((branch_doc[0].credit_to))

        for s in self.get("calculation_table"):
            # if s.check:
                PI = frappe.new_doc("Purchase Invoice")
                PI.naming_series = n_s
                PI.supplier = s.farmer_id
                PI.set_posting_time=1
                PI.posting_date = self.today
                # PI.posting_time = self.time
                PI.season = self.season
                PI.branch = self.branch
                PI.due_date =self.today
                PI.bill_no = self.name
                PI.bill_date = self.today
                PI.cost_center = str(c_c)
                PI.set_posting_time = 1


                PRN = frappe.get_all("Purchase Receipt",
                                                    filters={"supplier":s.farmer_id, "posting_date": ["between", [self.from_date, self.to_date]],"docstatus": 1,"status": ["in", ["To Bill"]] },
                                                    fields=["name"],)
                for p in PRN:
                    PRNI = frappe.get_all("Purchase Receipt Item",
                                                    filters={"parent": p.name,},
                                                    fields=["qty", "name", "rate" , ""],)
                    # frappe.throw(str(PRNI))
                    for i in PRNI:
                        PI.append(
                            "items",
                            {   "purchase_receipt":p.name,
                                "item_code" :   "Sugar Cane"   ,#str(i_c),
                                "qty" : i.qty,
                                "cost_center" :str(c_c),
                                "rate":i.rate,
                                "pr_detail" : i.name,
                                "received_qty": i.qty ,
                                
                                

                            },)
                PI.credit_to = str(c_a)	
                PI.insert()
                PI.save()
                PI.submit()
                purchase_invoice = frappe.db.get_all("Purchase Invoice", fields=["name"], order_by="creation DESC", limit=1)
                s.purchase_invoice_id = str(purchase_invoice[0].name)
  
  
  
    @frappe.whitelist()
    def bulk_purchase_invoice_cancel(self):
        for s in self.get("calculation_table"):
            doc = frappe.get_doc("Purchase Invoice", (str(s.purchase_invoice_id)))
            if doc.docstatus == 1:
                doc.cancel()
    
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                


                

    @frappe.whitelist()
    def je_of_sales_invoice_and_farmer_loan(self):
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

        
                # frappe.throw(str(list_data_od))
                # frappe.throw(str(list_data_li)+" /" + str(list_data_se)+ " /" +str(list_data_od) + str(s.total_deduction) )
                # frappe.throw(str(s.total_deduction)) 'list_data_se + list_data_lo + list_data_li + list_data_od '
                # ------------------------------------------------------------
        je = frappe.new_doc("Journal Entry")
        je.voucher_type = "Journal Entry"
        je.company = company
        je.posting_date = self.today
        
        for s in self.get("calculation_table"):
            # frappe.throw(str(s.name))
            list_data_se = []
            list_data_lo = []
            list_data_li = []
            list_data_od = []
            if s.total_deduction:
                counter = counter + 1
                list_data_se = eval(s.sales_invoice_information)
                list_data_lo = eval(s.farmer_loan_information)
                list_data_li = eval(s.farmer_loan_interest_information)
                list_data_od = eval(s.other_deduction_information)
                
                
                je.append(
                    "accounts",
                    {
                        "account": acc_to_set_debit_side,
                        "party_type": "Supplier",
                        "party": s.farmer_id,
                        "reference_type":"Purchase Invoice",
                        "reference_name":s.purchase_invoice_id,
                        "debit_in_account_currency": round(s.total_deduction,2),
                        
                    },)
            
            if list_data_se:
                for data_se in list_data_se:
                    je.append(
                        "accounts",
                        {
                            "account": data_se["Account"],
                            "party_type": "Customer",
                            "party": s.farmer_id,
                            "credit_in_account_currency": data_se["Outstanding Amount"],
                            "reference_type": "Sales Invoice",
                            "reference_name": data_se["Sales invoice ID"],
                        },)
                    
            if list_data_lo:
                for data_lo in list_data_lo:
                    je.append(
                        "accounts",
                        {
                            "account": data_lo["Account"],
                            "party_type": "Customer",
                            "party": s.farmer_id,
                            "credit_in_account_currency": data_lo["Installment Amount"],
                        },)
                    
            if list_data_li:
                for data_li in list_data_li:
                    if int(data_li["Installment Interest Amount"]) != 0:
                        je.append(
                            "accounts",
                            {
                                "account": data_li["Account"],
                                "party_type": "Customer",
                                "party": s.farmer_id,
                                "credit_in_account_currency": data_li["Installment Interest Amount"],
                            },)
                        # frappe.msgprint(str(data_li["Installment Interest Amount"]))
                        
                        
            if list_data_od:
                for data_od in list_data_od:
                    if int(data_od["Deduction Amount"]) != 0:
                        je.append(
                            "accounts",
                            {
                                "account": data_od["Account"],
                                "party_type": "Supplier",
                                "party": s.farmer_id,
                                "credit_in_account_currency": data_od["Deduction Amount"],
                            },)
                    
                        
                    # frappe.msgprint(str(data_od["Deduction Amount"]))
                    
        if counter > 0:
            je.insert()
            je.save()
            je.submit()
            journal_entry = frappe.db.get_all("Journal Entry", fields=["name"], order_by="creation DESC", limit=1)
            self.journal_entry_id = str(journal_entry[0].name)
                # --------------------------------------------------------------------

    @frappe.whitelist()
    def cancel_journal_entry(self):
        doc = frappe.get_doc("Journal Entry", (str(self.journal_entry_id)))
        if doc.docstatus == 1:
            doc.cancel()

                # ------------------------------------------------------------------------
                
                
    @frappe.whitelist()           
    def update_value_in_farmer_loan(self):
        if self.includes_loan_installment:
            for s in self.get("calculation_table"):    
                list_data_lo =[]
                list_data_lo = eval(s.farmer_loan_information)
                for data_lo in list_data_lo:
                    child_doc_farmer_loan=frappe.get_all('Deduction Form', filters={'farmer_application_loan_id': data_lo['Farmer Loan ID'],'season':data_lo['season'],'h_and_t_contract_id':""}, fields=['name','paid_amount'])
                    for d in child_doc_farmer_loan:
                        frappe.db.set_value("Deduction Form",d.name,"paid_amount",round((float(d.paid_amount)+(float(data_lo['Installment Amount']))),2))
                        

    @frappe.whitelist()           
    def update_value_in_farmer_loan_cancel(self):
        if self.includes_loan_installment:
            for s in self.get("calculation_table"):
                
                list_data_lo =[]
                list_data_lo = eval(s.farmer_loan_information)
                for data_lo in list_data_lo:
                    child_doc_farmer_loan=frappe.get_all('Deduction Form', filters={'farmer_application_loan_id': data_lo['Farmer Loan ID'],'season':data_lo['season'],'h_and_t_contract_id':""}, fields=['name','paid_amount'])
                    for d in child_doc_farmer_loan:
                        frappe.db.set_value("Deduction Form",d.name,"paid_amount",round((float(d.paid_amount)-(float(data_lo['Installment Amount']))),2))

 

    @frappe.whitelist()           
    def set_date_in_farmer_loan_child_for_next_installment(self):
        for s in self.get("calculation_table"):
            list_data_lo =[]
            list_data_lo = eval(s.farmer_loan_information)
            current_season = self.season
            next_seasons = str(int(current_season.split('-')[1]) ) + '-' + str(int(current_season.split('-')[1]) + 1) 
            #Update date for Next season
            for data_lo in list_data_lo:
                child_doc_farmer_loan=frappe.get_all('Deduction Form', 
                                                                    filters={'farmer_application_loan_id': data_lo['Farmer Loan ID'],'season':next_seasons,'h_and_t_contract_id':""}, 
                                                                    fields=['name'])
                for d in child_doc_farmer_loan:
                    frappe.db.set_value("Deduction Form",d.name,"from_date_interest_calculation",self.to_date)
            #Update date for current season       
            for data_lo in list_data_lo:
                child_doc_farmer_loan=frappe.get_all('Deduction Form', 
                                                                    filters={'farmer_application_loan_id': data_lo['Farmer Loan ID'],'season':self.season,'h_and_t_contract_id':""}, 
                                                                    fields=['name',])
                for d in child_doc_farmer_loan:
                    frappe.db.set_value("Deduction Form",d.name,"update_from_date_interest_calculation",self.to_date)
                # --------------------------------------------------------------------------------
                
                
    @frappe.whitelist()           
    def set_date_in_farmer_loan_child_for_next_installment_on_cancel(self):
        for s in self.get("calculation_table"):
            list_data_lo =[]
            list_data_lo = eval(s.farmer_loan_information)
            current_season = self.season
            next_seasons = str(int(current_season.split('-')[1]) ) + '-' + str(int(current_season.split('-')[1]) + 1) 
            for data_lo in list_data_lo:
                child_doc_farmer_loan=frappe.get_all('Deduction Form', 
                                                    filters={'farmer_application_loan_id': data_lo['Farmer Loan ID'],'season':next_seasons,'h_and_t_contract_id':""}, 
                                                    fields=['name',])
                for d in child_doc_farmer_loan:
                    frappe.db.set_value("Deduction Form",d.name,"from_date_interest_calculation",None)
                    
                    
            for data_lo in list_data_lo:
                child_doc_farmer_loan=frappe.get_all('Deduction Form', 
                                                    filters={'farmer_application_loan_id': data_lo['Farmer Loan ID'],'season':self.season,'h_and_t_contract_id':""}, 
                                                    fields=['name',])
                for d in child_doc_farmer_loan:
                    frappe.db.set_value("Deduction Form",d.name,"update_from_date_interest_calculation",None)
                    
                    
    # (((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
    
    @frappe.whitelist()           
    def update_value_in_deduction_form(self):

        for s in self.get("calculation_table"):
            
            list_data_od =[]
            list_data_od = eval(s.other_deduction_information)
            for data_od in list_data_od:
                other_deduction_doc=frappe.get_all('Deduction Form', filters={'name': data_od['DFN'],'h_and_t_contract_id':""}, fields=['name',"paid_amount" , "deduction_amount"])
                for d in other_deduction_doc:
                        frappe.db.set_value("Deduction Form",d.name,"paid_amount",(float(d.paid_amount)+(float(data_od['Deduction Amount']))))
                        if (float(d.paid_amount)+(float(data_od['Deduction Amount']))) == d.deduction_amount:
                            frappe.db.set_value("Deduction Form",d.name,"deduction_status",1)
                            
    @frappe.whitelist()           
    def update_value_in_deduction_form_on_cancel(self):

        for s in self.get("calculation_table"):
            
            list_data_od =[]
            list_data_od = eval(s.other_deduction_information)
            for data_od in list_data_od:
                other_deduction_doc=frappe.get_all('Deduction Form', filters={'name': data_od['DFN'],'h_and_t_contract_id':""}, fields=['name',"paid_amount" , "deduction_amount"])
                for d in other_deduction_doc:
                        frappe.db.set_value("Deduction Form",d.name,"paid_amount",(float(d.paid_amount)-(float(data_od['Deduction Amount']))))
                        frappe.db.set_value("Deduction Form",d.name,"deduction_status",0)

                            
    
    
    # (((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))                
                    
                    

    @frappe.whitelist()
    def test_method_trigger_on_button_on_submit_event_call(self):
        branch_variable = frappe.get_value("Farmer List", "FA-100", "branch")
        frappe.msgprint(str(branch_variable))

    
    def delete_row_record(self):
        doc = frappe.get_all("Child Farmer Cane Bill",filters ={"parent": self.name , "check" : 0},)
        for d in doc:
            frappe.delete_doc("Child Farmer Cane Bill", d.name)
        # self.reload_doc()
        # self.update_value_in_farmer_loan_cancel()
        # self.set_date_in_farmer_loan_child_for_next_installment_on_cancel()
        
        # frappe.msgprint("hgjg")
        # doc_acc = frappe.get_doc("Account Priority", "Account Priority")
        # frappe.msgprint(str(doc_acc.company))
        
        
        
        
        
        
        
        
        
        
        
    # ********PLEAE DO NOT DELETE IT CONTACT vivek.kumbhar@erpdata.in*************    
        
       # @frappe.whitelist()
    # def change_status_of_farmer_loan(self):
    #     # ************Please set condition here to set filter here*********************
    #     if self.includes_loan_installment:
    #         for s in self.get("calculation_table"):
    #             list_data_lo = []
    #             list_data_lo = eval(s.farmer_loan_information)
    #             for data_lo in list_data_lo:
    #                 child_doc_farmer_loan = frappe.get_all(
    #                     "Child Farmer Loan",
    #                     filters={
    #                         "parent": data_lo["Farmer Loan ID"],
    #                         "season": data_lo["season"],
    #                     },
    #                     fields=["name", "installment"],
    #                 )
    #                 for d in child_doc_farmer_loan:
    #                     frappe.db.set_value(
    #                         "Child Farmer Loan", d.name, "installment_status", 1
    #                     )

    #     if self.includes_loan_interest:
    #         for s in self.get("calculation_table"):
    #             list_data_lo = []
    #             list_data_lo = eval(s.farmer_loan_information)
    #             for data_lo in list_data_lo:
    #                 child_doc_farmer_loan = frappe.get_all(
    #                     "Child Farmer Loan",
    #                     filters={
    #                         "parent": data_lo["Farmer Loan ID"],
    #                         "season": data_lo["season"],
    #                     },
    #                     fields=["name", "installment"],
    #                 )
    #                 for d in child_doc_farmer_loan:
    #                     frappe.db.set_value(
    #                         "Child Farmer Loan", d.name, "interest_status", 1
    #                     )

    # @frappe.whitelist()
    # def change_status_of_farmer_loan_on_cancel(self):
    #     # ************Please set condition here to set filter here*********************
    #     if self.includes_loan_installment:
    #         for s in self.get("calculation_table"):
    #             list_data_lo = []
    #             list_data_lo = eval(s.farmer_loan_information)
    #             for data_lo in list_data_lo:
    #                 child_doc_farmer_loan = frappe.get_all(
    #                     "Child Farmer Loan",
    #                     filters={
    #                         "parent": data_lo["Farmer Loan ID"],
    #                         "season": data_lo["season"],
    #                     },
    #                     fields=["name", "installment"],
    #                 )
    #                 for d in child_doc_farmer_loan:
    #                     frappe.db.set_value(
    #                         "Child Farmer Loan", d.name, "installment_status", 0
    #                     )

    #     if self.includes_loan_interest:
    #         for s in self.get("calculation_table"):
    #             list_data_lo = []
    #             list_data_lo = eval(s.farmer_loan_information)
    #             for data_lo in list_data_lo:
    #                 child_doc_farmer_loan = frappe.get_all(
    #                     "Child Farmer Loan",
    #                     filters={
    #                         "parent": data_lo["Farmer Loan ID"],
    #                         "season": data_lo["season"],
    #                     },
    #                     fields=["name", "installment"],
    #                 )
    #                 for d in child_doc_farmer_loan:
    #                     frappe.db.set_value(
    #                         "Child Farmer Loan", d.name, "interest_status", 0
    #                     )

                # -------------------------------------------------------------------------
       
       
                       # if self.includes_loan_installment:
                #     loan_doc = frappe.get_all("Farmer Loan",
                #                                 filters={"applicant_id": FAR.farmer_id,"docstatus": 1,},
                #                                 fields=["name","applicant_id","account_paid_to","account_interest_paid_to",],)
                #     for l_d in loan_doc:
                #         loan_doc_child = frappe.get_all("Child Farmer Loan",
                #                                                             filters={"parent": l_d.name,"docstatus": 1,},
                #                                                             fields=["name","season","installment","rate_of_interest","interest","from_date_interest_calculation","interest_calculate_on_amount",
                #                                                                     "installment_status","interest_status","paid_installment",],)
                #         for l_d_c in loan_doc_child:
                #             if str(self.season) == str(l_d_c.season):
                #                 if str(l_d_c.installment_status) == "1":
                #                     (l_d_c.installment) = 0
                #                     (l_d_c.paid_installment) =0
                #                 loan_installment_amount=loan_installment_amount+round((float(l_d_c.installment)-float(l_d_c.paid_installment)),2)   # loan_installment_amount = loan_installment_amount + int(l_d_c.installment)
                #                 if round((float(l_d_c.installment)-float(l_d_c.paid_installment)),2) > 0:
                #                     loan_installment.append({
                #                                                 "Farmer Loan ID": l_d.name,
                #                                                 "Farmer ID": l_d.applicant_id,
                #                                                 "season": l_d_c.season,
                #                                                 "Account": l_d.account_paid_to,
                #                                                 "Installment Amount":round((float(l_d_c.installment)-float(l_d_c.paid_installment)),2), })

                # if self.includes_loan_interest:
                #     loan_doc_int = frappe.get_all("Farmer Loan",
                #                                                 filters={"applicant_id": FAR.farmer_id,"docstatus": 1,},
                #                                                 fields=["name","applicant_id","account_paid_to","account_interest_paid_to",],)
                #     for l_d in loan_doc_int:
                #         loan_doc_child_int = frappe.get_all("Child Farmer Loan",
                #                                                             filters={"parent": l_d.name,"docstatus": 1, 'season': self.season },
                #                                                             fields=["name","season","installment","rate_of_interest","interest","from_date_interest_calculation","paid_installment",
                #                                                                     "interest_calculate_on_amount","installment_status","interest_status","update_from_date_interest_calculation",],)
                #         for l_d_c in loan_doc_child_int:
                #             p = 0
                #             if not l_d_c.update_from_date_interest_calculation:
                #                 p = round(float(l_d_c.interest_calculate_on_amount)* (float(l_d_c.rate_of_interest) / 100)* ((datetime.strptime(self.to_date, "%Y-%m-%d")- datetime.strptime((str(l_d_c.from_date_interest_calculation)),"%Y-%m-%d",)).days/ 365),2,)
                #                 if str(l_d_c.interest_status) == "1":
                #                     p = 0
                #                 loan_interest_amount = loan_interest_amount + p
                #                 # frappe.msgprint(str(p))
                #                 if p>0:
                #                     loan_installment_intrest.append({
                #                                                     "Farmer Loan ID": l_d.name,
                #                                                     "Farmer ID": l_d.applicant_id,
                #                                                     "season": l_d_c.season,
                #                                                     "Account": l_d.account_interest_paid_to,
                #                                                     "Installment Interest Amount": p,
                #                                             })
                                
                #             else:
                               
                #                 p= (round(float(float(l_d_c.interest_calculate_on_amount)-float(l_d_c.paid_installment)) * (float(l_d_c.rate_of_interest) / 100) * ((datetime.strptime(self.to_date, "%Y-%m-%d") - datetime.strptime((str(l_d_c.from_date_interest_calculation)), "%Y-%m-%d")).days / 365), 2)) + ( round(float(float(l_d_c.interest_calculate_on_amount)-float(l_d_c.paid_installment)) * (float(l_d_c.rate_of_interest) / 100) * ((datetime.strptime(self.to_date, "%Y-%m-%d") - datetime.strptime((str(l_d_c.update_from_date_interest_calculation)), "%Y-%m-%d")).days / 365), 2))
                #                 if str(l_d_c.interest_status)=="1":
                #                     p=0
                #                 loan_interest_amount=loan_interest_amount+p
                #                 if p>0:
                #                     loan_installment_intrest.append({
                #                                                     'Farmer Loan ID': l_d.name,
                #                                                     'Farmer ID': l_d.applicant_id, 
                #                                                     'season':l_d_c.season,
                #                                                     'Account':l_d.account_interest_paid_to, 
                #                                                     'Installment Interest Amount': p,})
