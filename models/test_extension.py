from odoo import models,fields

class ExtendedPathologyTest(models.Model):
    _inherit = 'pathology.test'


    # Modifying exiting location field
    location = fields.Char(string='Location', required='False')

    #add new field to the extended model
    test_type = fields.Selection([
        ('blood', 'Blood Test'),
        ('urine', 'Urine Test'),
        ('Xray', ' X-RAY')
    ])

    doctor_name = fields.Char(string='Doctor name')