from odoo import models, fields, api

class BloodDonation(models.Model):
    _name = 'pathology.blood.donation'
    _description = 'Blood Donation Record'
    
    donor_name = fields.Char(string='Donor Name', required=True)
    donor_id = fields.Many2one('pathology.donor', string='Donor', required=True)
    donation_date = fields.Date(string='Donation Date', required=True)
    blood_type = fields.Selection(related='donor_id.blood_type', string='Blood Type', store=True)
    quantity = fields.Float(string='Quantity (Liters)', required=True)
    status = fields.Selection([('completed', 'Completed'), ('pending', 'Pending')], string='Status', default='pending')
    
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
