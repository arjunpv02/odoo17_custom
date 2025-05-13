from odoo import models, api, fields
from odoo.exceptions import UserError

class EstateAccount(models.Model):
    _inherit = "estate_property"

    def action_set_sold(self):
        # Call the parent model's action_set_sold logic first
        res = super().action_set_sold()

        for record in self:
            # Ensure a buyer exists
            if not record.buyer_id:
                raise UserError("A buyer must be set before selling the property.")

            # Ensure the selling price is valid
            if float(record.selling_price) <= 0:
                raise UserError("Selling price must be greater than zero .")

            # Find a sale-type journal for creating the invoice
            journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
            if not journal:
                raise UserError("No Sale Journal found. Please configure at least one.")

            # Compute 6% of the selling price as a commission fee
            commission_price = record.selling_price * 0.06

            # Flat administrative fee
            admin_fee = 100.00

            # Prepare invoice line items: 
            # 1. Service fee - 6% of selling price
            # 2. Admin fee - fixed ₹100
            invoice_lines = [
                (0, 0, {
                    'name': f"Commission for {record.title}",  # line 1
                    'quantity': 1,
                    'price_unit': commission_price,
                }),
                (0, 0, {
                    'name': "Administrative fees",  # line 2
                    'quantity': 1,
                    'price_unit': admin_fee,
                }),
            ]

            # Create the invoice using account.move
            invoice_vals = {
                'partner_id': record.buyer_id.id,        # Link to buyer
                'move_type': 'out_invoice',              # Customer invoice
                'journal_id': journal.id,                # Journal to use
                'invoice_line_ids': invoice_lines        # Two lines as explained
            }

            # Create the invoice
            invoice = self.env['account.move'].create(invoice_vals)

            # Optional: Print for debug/logging
            print(f"Invoice {invoice.name} created for property {record.title}")

        # Return the result of super call
        return res
