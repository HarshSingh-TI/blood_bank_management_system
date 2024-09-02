from odoo import models, fields, api

class BloodInventory(models.Model):
    _name = 'pathology.blood.inventory'
    _inherit = ['mail.thread']
    _description = 'Blood Inventory'

    blood_type = fields.Selection(
        [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
         ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
        string='Blood Type', required=True
    )
    quantity = fields.Float(string='Quantity (Liters)', required=True, tracking=True)
    expiration_date = fields.Date(string='Expiration Date', required=True)
    location = fields.Char(string='Storage Location', required=True, tracking=True)
    status = fields.Selection([('available', 'Available'), ('expired', 'Expired')], string='Status', compute='_compute_status', store=True)

    @api.depends('expiration_date')
    def _compute_status(self):
        for record in self:
            if record.expiration_date and record.expiration_date < fields.Date.today():
                record.status = 'expired'
            else:
                record.status = 'available'
