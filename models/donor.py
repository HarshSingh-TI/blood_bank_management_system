from odoo import models, fields

class Donor(models.Model):
    _name = 'pathology.donor'
    _inherit = ['mail.thread']
    _description = 'Blood Donor'

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age', required=True, tracking=True)
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        string='Gender', 
        required=True
    )
    donor_image = fields.Binary(string='Donor Image')
    blood_type = fields.Selection(
        [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
         ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
        string='Blood Type', 
        required=True
    )
    contact_number = fields.Char(string='Contact Number', required=True, size=10)
    address = fields.Text(string='Address')
    last_donation_date = fields.Date(string='Last Donation Date')
    total_donations = fields.Integer(string='Total Donations', compute='_compute_total_donations', store=True)
    donor_media = fields.Many2many('ir.attachment', string='Donor Media')

    def _compute_total_donations(self):
        for donor in self:
            donor.total_donations = self.env['pathology.blood.donation'].search_count([('donor_id', '=', donor.id)])

    # CRUD Operations
    def create_donor(self, vals):
        return self.create(vals)

    def read_donor(self, donor_id):
        donor = self.browse(donor_id)
        return donor if donor.exists() else None

    def update_donor(self, donor_id, vals):
        donor = self.browse(donor_id)
        if donor.exists():
            donor.write(vals)
            return True
        return False

    def delete_donor(self, donor_id):
        donor = self.browse(donor_id)
        if donor.exists():
            donor.unlink()
            return True
        return False
