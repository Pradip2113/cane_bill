# Copyright (c) 2023, quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from collections import defaultdict

class DailyCanePurchase(Document):

	@frappe.whitelist()
	def get_cane_weight_data(self):
		doc = frappe.db.get_list("Cane Weight",
								filters={"docstatus": 1, "date": self.date, "purchase_receipt_status": 0 , "branch" : self.branch,"shft":self.shift},
								fields=["farmer_code", "farmer_name", "farmer_village", "actual_weight", "vehicle_number","season","branch","water_supplier_code","water_supplier_name","water_supplier_weight"])

		# Initialize a dictionary to store the aggregated data
		aggregated_data = defaultdict(lambda: {"farmer_name": "", "farmer_village": "", "total_weight": 0, "all_vehicle_number": [],"season": "","branch":""})

		# Iterate through the doc list and aggregate the data
		for entry in doc:
			if entry["farmer_code"]:
				farmer_code = entry["farmer_code"]
				farmer_name = entry["farmer_name"]
				farmer_village = entry["farmer_village"]
				actual_weight = entry["actual_weight"]
				vehicle_number = entry["vehicle_number"]
				season = entry["season"]
				branch = entry["branch"]

				# Update the aggregated data for the specific farmer_code
				aggregated_data[farmer_code]["farmer_name"] = farmer_name
				aggregated_data[farmer_code]["farmer_village"] = farmer_village
				aggregated_data[farmer_code]["total_weight"] += actual_weight
				aggregated_data[farmer_code]["all_vehicle_number"].append(vehicle_number)
				aggregated_data[farmer_code]["season"] = season
				aggregated_data[farmer_code]["branch"] = branch

		for p in doc:
			if p["water_supplier_weight"]:
				farmer_code = p["water_supplier_code"]
				farmer_name = p["water_supplier_name"]
				farmer_village = p["farmer_village"]
				actual_weight = float(p["water_supplier_weight"])
				vehicle_number = p["vehicle_number"]
				season = p["season"]
				branch = p["branch"]

				# Update the aggregated data for the specific farmer_code
				aggregated_data[farmer_code]["farmer_name"] = farmer_name
				aggregated_data[farmer_code]["farmer_village"] = farmer_village
				aggregated_data[farmer_code]["total_weight"] += actual_weight
				aggregated_data[farmer_code]["all_vehicle_number"].append(vehicle_number)
				aggregated_data[farmer_code]["season"] = season
				aggregated_data[farmer_code]["branch"] = branch

		# Convert the aggregated_data dictionary to a list
		aggregated_list = [
			{
				"farmer_code": code,
				"farmer_name": data["farmer_name"],
				"farmer_village": data["farmer_village"],
				"total_weight": data["total_weight"],
				"all_vehicle_number": ", ".join(filter(None, data["all_vehicle_number"])),
				"season": data["season"],
				"branch": data["branch"],
			}
			for code, data in aggregated_data.items()
		]
  
		# doc_for_water_supplier = frappe.db.get_list("Cane Weight",
		# 						filters={"docstatus": 1, "date": self.date, "purchase_receipt_status": 0 , "branch" : self.branch},
		# 						fields=["farmer_code", "farmer_name", "farmer_village", "actual_weight", "vehicle_number","season","branch","weight_partner_code","weight_partner_name","weight_partners_weight"])

		for row in aggregated_list:
			self.append("record_table", {
				"farmer_code": row["farmer_code"],
				"farmer_name": row["farmer_name"],
				"farmer_village": row["farmer_village"],
				"net_weight": round(row["total_weight"], 3),
				"all_vehicle_number": row["all_vehicle_number"],
				"season": row["season"],
				"branch": row["branch"],
			})
   
   
		self.selectall()
   
   
	@frappe.whitelist()
	def selectall(self):
		# pass
		children = self.get("record_table")
		if not children:
			return
		all_selected = all([child.check for child in children])
		value = 0 if all_selected else 1
		for child in children:
			child.check = value
   
	@frappe.whitelist()
	def before_save(self):
		self.change_status_from_cane_weight()
  
  
	@frappe.whitelist()
	def on_trash(self):
		self.change_status_from_cane_weight_cancel()

   
	@frappe.whitelist()
	def before_submit(self):
		self.bulk_purchase_receipt()
		# self.bulk_purchase_invoice()
		self.change_status_from_cane_weight()
  
	@frappe.whitelist()
	def before_cancel(self):
		# self.cancel_bulk_purchase_invoice()
		self.cancel_bulk_purchase_receipt()
		self.change_status_from_cane_weight_cancel()
	
   
   
	@frappe.whitelist()
	def bulk_purchase_receipt(self):
		branch_doc = frappe.get_all("Branch",
                                            filters={"name": self.branch},
                                            fields={ "name","company","cost_center","sugar_cane_item_code_"},)
		if branch_doc:
			if not (branch_doc[0].company):
				frappe.throw( f" Please set Company for Branch '{str(self.branch) } '")
			
			if not (branch_doc[0].cost_center):
				frappe.throw( f" Please set cost_center for Branch '{str(self.branch) } '")
    
			if not (branch_doc[0].sugar_cane_item_code_):
				frappe.throw( f" Please set sugar_cane_item_code_ for Branch '{str(self.branch) } '")
   
   
   
			i_c = ((branch_doc[0].sugar_cane_item_code_))
			c_c = ((branch_doc[0].cost_center))
			company =  ((branch_doc[0].company))
		for s in self.get("record_table"):
			if s.check:
	# ------------------------------------------------------------
				PR = frappe.new_doc("Purchase Receipt")
				PR.supplier = s.farmer_code
				PR.set_posting_time=1
				PR.posting_date = self.date
				PR.posting_time = self.time
				PR.season = s.season
				PR.branch = s.branch
				PR.supplier_delivery_note = (s.farmer_code+"/"+ self.date)
				PR.company = company
				PR.cost_center = str(c_c)
				PR.currency = "INR"
				PR.buying_price_list = "Standard Buying"
				PR.lr_no = "MHXXBKXXXX"
				PR.remarks = s.all_vehicle_number
				PR.append(
					"items",
					{
						"item_code": str(i_c),
						"qty": s.net_weight,
						"cost_center" :str(c_c),
						"warehouse" : str(frappe.get_value("Branch" ,self.branch,"purchase_receipt_warehouse")),
						
					},)
				# frappe.throw(str(frappe.get_value("Branch" ,self.branch,"purchase_receipt_warehouse")))
				PR.insert()
				PR.save()
				PR.submit()
				purchase_receipt = frappe.db.get_all("Purchase Receipt", fields=["name"], order_by="creation DESC", limit=1)
				s.purchase_receipt_id = str(purchase_receipt[0].name)
    
    
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

		for s in self.get("record_table"):
			if s.check:
				PI = frappe.new_doc("Purchase Invoice")
				PI.naming_series = n_s
				PI.supplier = s.farmer_code
				PI.set_posting_time=1
				PI.posting_date = self.date
				PI.posting_time = self.time
				PI.season = s.season
				PI.branch = s.branch
				PI.due_date =self.date
				PI.bill_no =(s.farmer_code+"/"+ self.date)
				PI.bill_date = self.date
				PI.cost_center = str(c_c)
				PI.set_posting_time = 1

    
				i_n_d = frappe.get_all("Purchase Receipt Item",
													filters={"parent": s.purchase_receipt_id,},
													fields=["qty", "name"],)
    
				item_name = str(i_n_d[0].name)
    
				PI.append(
					"items",
					{
						"item_code" :   "Sugar Cane"   ,#str(i_c),
						"qty" : s.net_weight,
						"cost_center" :str(c_c),
						"purchase_receipt":s.purchase_receipt_id,
						"pr_detail" : item_name,
						"received_qty": s.net_weight ,
						
						

					},)
				
				PI.credit_to = str(c_a)	
				PI.insert()
				PI.save()
				PI.submit()
				purchase_invoice = frappe.db.get_all("Purchase Invoice", fields=["name"], order_by="creation DESC", limit=1)
				s.purchase_invoice_id = str(purchase_invoice[0].name)
    
    
    
	@frappe.whitelist()
	def cancel_bulk_purchase_receipt(self):
		for s in self.get("record_table"):
			if s.purchase_receipt_id:
				doc = frappe.get_doc("Purchase Receipt", (str(s.purchase_receipt_id)))
				doc.cancel()
    
	@frappe.whitelist()
	def cancel_bulk_purchase_invoice(self):
		for s in self.get("record_table"):
			if s.purchase_invoice_id:
				doc = frappe.get_doc("Purchase Invoice", (str(s.purchase_invoice_id)))
				doc.cancel()

    

	@frappe.whitelist()
	def change_status_from_cane_weight(self):
		pop = self.get("record_table")
		for p in pop:
			if p.check:
				cane_weight_docs = frappe.get_all("Cane Weight",
													filters={"farmer_code": p.farmer_code,"date": self.date,"docstatus": 1,"purchase_receipt_status": 0,},
													fields=["farmer_code", "date", "name"],)
				for k in cane_weight_docs:
					frappe.db.set_value("Cane Weight", k.name, "purchase_receipt_status", 1)
					frappe.db.set_value("Cane Weight", k.name, "purchase_receipt", p.purchase_receipt_id)
					# frappe.db.set_value("Cane Weight", k.name, "purchase_invoice", p.purchase_invoice_id)
    
	@frappe.whitelist()
	def change_status_from_cane_weight_cancel(self):
		mop = self.get("record_table")
		for m in mop:
			if m.check:
				cane_weight_docs = frappe.get_all("Cane Weight",
													filters={"farmer_code": m.farmer_code,"date": self.date,"docstatus": 1,"purchase_receipt_status": 1,},
													fields=["farmer_code", "date", "name"],)
				for u in cane_weight_docs:
					frappe.db.set_value("Cane Weight", u.name, "purchase_receipt_status", 0)
					frappe.db.set_value("Cane Weight", u.name, "purchase_receipt", None)
					# frappe.db.set_value("Cane Weight", u.name, "purchase_invoice", None)
		
  
  
  
	@frappe.whitelist()
	def temp_method(self):
		PI = frappe.new_doc("Purchase Invoice")
		PI.naming_series = "PI-23-24-.#####."
		PI.supplier = "FA-144490"
		PI.set_posting_time=1
		PI.posting_date = self.date
		PI.posting_time = "14:43:35"
		PI.season = "2022-2023"
		PI.branch = "Bedkihal"
		PI.due_date =self.date
		PI.bill_no =("FA-144490-3/07-07-2023")
		PI.bill_date = self.date
		PI.append(
			"items",
			{
				"purchase_receipt": "GRN/B/23-24/00279",
				"qty" : "30",
				"item_code" :"Sugar Cane",
				# "expense_account" : "22600001 - Stock Received But Not Billed - VP"
				
				
			},)
			
		PI.insert()
		PI.save()


			




 