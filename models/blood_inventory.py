from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class BloodInventory(models.Model):
    _name = 'pathology.blood.inventory'
    _inherit = ['mail.thread']
    _description = 'Blood Inventory'

    # Existing fields
    blood_type = fields.Selection(
        [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
         ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
        string='Blood Type', required=True
    )
    quantity = fields.Float(string='Quantity (Pounds)', required=True, tracking=True)
    expiration_date = fields.Date(string='Expiration Date', required=True)
    location = fields.Selection([
        ('los_angeles_ca', 'Los Angeles, California'),
        ('san_francisco_ca', 'San Francisco, California'),
        ('san_diego_ca', 'San Diego, California'),
        ('houston_tx', 'Houston, Texas'),
        ('dallas_tx', 'Dallas, Texas'),
        ('austin_tx', 'Austin, Texas'),
        ('miami_fl', 'Miami, Florida'),
        ('orlando_fl', 'Orlando, Florida'),
        ('tampa_fl', 'Tampa, Florida'),
        ('new_york_ny', 'New York, New York'),
        ('buffalo_ny', 'Buffalo, New York'),
        ('rochester_ny', 'Rochester, New York'),
    ], string='Location')

    status = fields.Selection([('available', 'Available'), ('expired', 'Expired')], string='Status', compute='_compute_status', store=True)
    
    # Relational fields
    donor_id = fields.Many2one('pathology.donor', string='Donor', ondelete='set null')
    blood_bank_id = fields.Many2one('pathology.blood.bank', string='Blood Bank', ondelete='set null')
    
    @api.depends('expiration_date')
    def _compute_status(self):
        for record in self:
            if record.expiration_date and record.expiration_date < fields.Date.today():
                record.status = 'expired'
            else:
                record.status = 'available'

    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError('The quantity can not be null or negative .')


    @api.constrains('expiration_date')
    def _check_expiration_date(self):
        for record in self:
            if record.expiration_date and record.expiration_date < fields.Date.today():
                raise ValidationError(_('The expiration date cannot be in the past.'))
