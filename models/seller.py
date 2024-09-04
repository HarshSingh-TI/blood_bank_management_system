from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class BloodSale(models.Model):
    _name = 'pathology.blood.sale'
    _description = 'Blood Sale'

    blood_type = fields.Selection(
        [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
         ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
        string='Blood Type', required=True
    )
    quantity = fields.Float(string='Quantity (Pounds)', required=True)
    sale_date = fields.Date(string='Sale Date', required=True, default=fields.Date.today)
    sale_price = fields.Float(string='Sale Price', required=True)
    tax_amount = fields.Float(string='Tax Amount', compute='_compute_total', store=True)
    service_charge = fields.Float(string='Service Charge', default=200, required=True)
    grand_total = fields.Float(string='Grand Total', compute='_compute_total', store=True)
    media_image = fields.Binary(string="Media Image")  
    donor_name = fields.Char(string="Donor Name")  

    # Many2many field
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError(_('The quantity cannot be zero or negative.'))

    @api.depends('sale_price', 'service_charge', 'quantity')
    def _compute_total(self):
        """
        Computes the tax amount and grand total.
        """
        for record in self:
            record.tax_amount = record.sale_price * 0.125  # 12.5% tax
            record.grand_total = (record.sale_price + record.tax_amount + record.service_charge) * record.quantity

    @api.model
    def create(self, vals):
        blood_type = vals.get('blood_type')
        quantity = vals.get('quantity')
        inventory = self.env['pathology.blood.inventory']

        # Reduce the quantity from inventory
        inventory.reduce_quantity(blood_type, quantity)

        # Create the sale record
        return super(BloodSale, self).create(vals)

    def action_generate_invoice(self):
        """
        Action to generate an invoice for the blood sale.
        This is a placeholder for the actual invoice generation logic.
        """
        # Placeholder: Implement the invoice generation logic here
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'pathology.blood.sale',
            'view_mode': 'form',  # Changed to 'form' to test visibility
            'view_id': self.env.ref('pathology_blood_bank_management.view_blood_sale_invoice_form').id,
            'target': 'new',  # Changed to 'current' to open in the same window
            'res_id': self.id,
        }
