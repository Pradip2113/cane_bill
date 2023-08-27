# Copyright (c) 2023, quantbit and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document

# class FarmerLoanType(Document):

# 	# ********Do not change naming seres of  Farmer Loan Type
# 	@frappe.whitelist()
# 	def before_save(self):
# 		# frappe.msgprint("Massage")
# 		doc = frappe.get_all("Deduction Type",
# 											filters={"name": self.loan_name},
# 											fields={"name"},)
# 		if not doc:
# 			doc = frappe.new_doc("Deduction Type")
# 			doc.deduction_name = self.loan_name
# 			doc.description = self.description
# 			doc.insert()
# 			doc.save()
# 		frappe.db.set_value("Deduction Type", str(doc[0].name) ,"description",self.description )
   
# 	@frappe.whitelist()
# 	def on_trash(self):
# 		doc = frappe.get_all("Deduction Type",
# 											filters={"name": self.loan_name},
# 											fields={"name"},)
# 		if doc:
# 			if (doc[0].name):
# 				frappe.delete_doc('Deduction Type', (doc[0].name))


import frappe
from frappe.model.document import Document

class FarmerLoanType(Document):

    @frappe.whitelist()
    def before_save(self):
        doc = frappe.get_all("Deduction Type",
                             filters={"name": self.loan_name},
                             fields=["name"])

        if not doc:
            doc = frappe.new_doc("Deduction Type")
            doc.deduction_name = self.loan_name
            doc.description = self.description
            doc.insert()
            doc.save()
        else:
            # Since we are using `get_all`, it returns a list of dicts. Let's use the first item if it exists.
            doc = doc[0]

        frappe.db.set_value("Deduction Type", doc.get("name"), "description", self.description)

    @frappe.whitelist()
    def on_trash(self):
        doc = frappe.get_all("Deduction Type",
                             filters={"name": self.loan_name},
                             fields=["name"])

        if doc and doc[0].get("name"):
            frappe.delete_doc('Deduction Type', doc[0].get("name"))



       