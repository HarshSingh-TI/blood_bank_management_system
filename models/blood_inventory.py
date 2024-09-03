from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class BloodInventory(models.Model):
    _name = 'pathology.blood.inventory'
    _inherit = ['mail.thread']
    _description = 'Blood Inventory'

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
            if record.quantity < 0:
                raise ValidationError('The quantity cannot be negative.')

    @api.constrains('expiration_date')
    def _check_expiration_date(self):
        for record in self:
            if record.expiration_date and record.expiration_date < fields.Date.today():
                raise ValidationError(_('The expiration date cannot be in the past.'))

    def reduce_quantity(self, blood_type, quantity):
        """Reduce the quantity of blood of a specific type."""
        inventory_records = self.search([('blood_type', '=', blood_type), ('status', '=', 'available')], order='expiration_date asc')
        total_available = sum(record.quantity for record in inventory_records)

        if total_available < quantity:
            raise ValidationError(_('Not enough blood available for the given type.'))

        for record in inventory_records:
            if quantity <= 0:
                break
            if record.quantity >= quantity:
                record.quantity -= quantity
                quantity = 0
            else:
                quantity -= record.quantity
                record.quantity = 0

    def add_quantity(self, blood_type, quantity):
        """Add the quantity of blood of a specific type."""
        inventory_record = self.search([('blood_type', '=', blood_type), ('status', '=', 'available')], limit=1)
        if inventory_record:
            inventory_record.quantity += quantity
        else:
            raise ValidationError(_('No inventory record found for the specified blood type to add quantity.'))
