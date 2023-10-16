// Copyright (c) 2023, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Farmer Loan Application', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Farmer Loan Application', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});

frappe.ui.form.on('Farmer Loan Application', {
	loan_amount: function(frm) {
		frm.call({
			method: 'loan_validation',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});

frappe.ui.form.on('Farmer Loan Application', {
	applicant: function(frm) {
		frm.call({
			method: 'target_Bank',//function name defined in python
			doc: frm.doc, //current document
		});
		frm.set_query("surety_code", "grantor", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
					['Farmer List', 'cane_registration_flag', '=', 1],
				]
			};
		});

	}
});


frappe.ui.form.on('Farmer Loan Application', {
	loan_type: function(frm) {
		frm.clear_table("installments_table")
		frm.refresh_field('installments_table')
		frm.call({
			method: 'loan_i_p',//function name defined in python
			doc: frm.doc, //current document
		});
		frm.set_query("surety_code", "grantor", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
					['Farmer List', 'cane_registration_flag', '=', 1],
				]
			};
		});

	}
});





frappe.ui.form.on('Farmer Loan Application', {
	loan_amount: function(frm) {
		frm.clear_table("installments_table")
		frm.refresh_field('installments_table')
		frm.call({
			method: 'loan_amt_installment',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});

frappe.ui.form.on('Farmer Loan Application', {
	season: function(frm) {
		frm.clear_table("installments_table")
		frm.refresh_field('installments_table')
		frm.call({
			method: 'season_installment',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});

frappe.ui.form.on('Farmer Loan Application', {
	repayment_period_in_years: function(frm) {
		frm.clear_table("installments_table")
		frm.refresh_field('installments_table')
		frm.call({
			method: 'year_installment_installment',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});

frappe.ui.form.on('Farmer Loan Application', {
	rate_of_interest: function(frm) {
		frm.clear_table("installments_table")
		frm.refresh_field('installments_table')
		frm.call({
			method: 'rate_of_interest_installment',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});


frappe.ui.form.on('Farmer Loan Application', {
	sample: function(frm) {

		frm.call({
			method: 'cndodf',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});


frappe.ui.form.on('Farmer Loan Application', {
	on_update: function(frm) {

		frm.call({
			method: 'update_approve',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});



frappe.ui.form.on('Farmer Loan Application', {
	applicant: function(frm) {
		frm.clear_table("plot_table")
		frm.refresh_field('plot_table')
		frm.call({
			method: 'get_register_ploat_for_applicant',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});

frappe.ui.form.on('Farmer Loan Application', {
    season: function(frm) {
		frm.clear_table("plot_table")
		frm.refresh_field('plot_table')
        if (frm.doc.applicant) { // Corrected the if condition by adding parentheses
            frm.call({
                method: 'get_register_ploat_for_applicant',
                doc: frm.doc,
            });
        }
    }
});

frappe.ui.form.on('Farmer Loan Application', {
    loan_type: function(frm) {
		frm.clear_table("installments_table")
		frm.refresh_field('installments_table')
        if (frm.doc.applicant) { // Corrected the if condition by adding parentheses
            frm.call({
                method: 'auto_fetch_amount',
                doc: frm.doc,
            });
        }
    }
});



frappe.ui.form.on('Child Farmer List Application For Plots', {
    check: function(frm) {
		if (frm.doc.loan_type) { // Corrected the if condition by adding parentheses
			frm.clear_table("installments_table")
			frm.refresh_field('installments_table')
        }
        if (frm.doc.applicant) { // Corrected the if condition by adding parentheses
            frm.call({
                method: 'calculate_the_acrs',
                doc: frm.doc,
            });
        }
    }
});
