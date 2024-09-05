from odoo import models, fields

class BloodDonationLocation(models.Model):
    _name = 'pathology.blood.location'
    _description = 'Blood Donation Location'

    name = fields.Char(string='Location Name', required=True)
    city = fields.Char(string='City', required=True)
    state = fields.Selection([
        ('andhra_pradesh', 'Andhra Pradesh'),
        ('arunachal_pradesh', 'Arunachal Pradesh'),
        ('assam', 'Assam'),
        ('bihar', 'Bihar'),
        ('chhattisgarh', 'Chhattisgarh'),
        ('goa', 'Goa'),
        ('gujarat', 'Gujarat'),
        ('haryana', 'Haryana'),
        ('himachal_pradesh', 'Himachal Pradesh'),
        ('jammu_kashmir', 'Jammu & Kashmir'),
        ('jharkhand', 'Jharkhand'),
        ('karnataka', 'Karnataka'),
        ('kerala', 'Kerala'),
        ('madhya_pradesh', 'Madhya Pradesh'),
        ('maharashtra', 'Maharashtra'),
        ('manipur', 'Manipur'),
        ('meghalaya', 'Meghalaya'),
        ('mizoram', 'Mizoram'),
        ('nagaland', 'Nagaland'),
        ('odisha', 'Odisha'),
        ('punjab', 'Punjab'),
        ('rajasthan', 'Rajasthan'),
        ('sikkim', 'Sikkim'),
        ('tamil_nadu', 'Tamil Nadu'),
        ('telangana', 'Telangana'),
        ('tripura', 'Tripura'),
        ('uttar_pradesh', 'Uttar Pradesh'),
        ('uttarakhand', 'Uttarakhand'),
        ('west_bengal', 'West Bengal'),
        ('andaman_nicobar', 'Andaman & Nicobar Islands'),
        ('chandigarh', 'Chandigarh'),
        ('dadra_nagar_haveli', 'Dadra & Nagar Haveli'),
        ('daman_diu', 'Daman & Diu'),
        ('delhi', 'Delhi'),
        ('lakshadweep', 'Lakshadweep'),
        ('puducherry', 'Puducherry'),
    ], string='State', required=True)
    country = fields.Char(string='Country', default='INDIA')
