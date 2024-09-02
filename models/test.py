from odoo import models, fields, api
from datetime import date

class PathologyTest(models.Model):
    _name = 'pathology.test'
    _description = 'Pathology Test'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Patient Name', required=True)
    dob = fields.Date(string='Date of Birth', required=True)
    location = fields.Char(string='Location', required=True)
    phone_number = fields.Char(string='Phone Number', required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender', required=True)

    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    
    is_minor = fields.Boolean(string='Is Minor', compute='_compute_is_minor', store=True)
    
    eligible_for_discount = fields.Boolean(string='Eligible for Discount', compute='_compute_eligible_for_discount', store=True)

    @api.depends('dob')
    def _compute_age(self):
        for record in self:
            if record.dob:
                today = date.today()
                dob = fields.Date.from_string(record.dob)
                record.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            else:
                record.age = 0

    @api.depends('age')
    def _compute_is_minor(self):
        for record in self:
            record.is_minor = record.age < 18

    @api.depends('is_minor')
    def _compute_eligible_for_discount(self):
        for record in self:
            record.eligible_for_discount = record.is_minor
