from odoo import models, fields

class Donor(models.Model):
    _name = 'pathology.donor'
    _inherit = ['mail.thread']
    _description = 'Blood Donor'

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age', required=True, tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', required=True)
    donor_image = fields.Binary(string='Donor Image')
    blood_type = fields.Selection(
        [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
         ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
        string='Blood Type', required=True
    )
    contact_number = fields.Char(string='Contact Number', required=True)
    address = fields.Text(string='Address', tracking=True)
    last_donation_date = fields.Date(string='Last Donation Date')
    total_donations = fields.Integer(string='Total Donations', compute='_compute_total_donations')

    def _compute_total_donations(self):
        for donor in self:
            donor.total_donations = self.env['pathology.blood.donation'].search_count([('donor_id', '=', donor.id)])
