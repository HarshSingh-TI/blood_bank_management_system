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
    
    location_id = fields.Many2one('pathology.blood.location', string='Location', required=True)
