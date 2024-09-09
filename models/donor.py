import logging
from odoo import models, fields

class Donor(models.Model):
    _name = 'pathology.donor'
    _inherit = ['mail.thread']
    _description = 'Blood Donor'

    # Setup logger
    _logger = logging.getLogger(__name__)

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
            total = self.env['pathology.blood.donation'].search_count([('donor_id', '=', donor.id)])
            donor.total_donations = total
            self._logger.info(f"Total donations computed for {donor.name}: {total}")

    # CRUD Operations
    def create_donor(self, vals):
        donor = self.create(vals)
        self._logger.info(f"Created new donor: {donor.name}")
        return donor

    def read_donor(self, donor_id):
        donor = self.browse(donor_id)
        if donor.exists():
            self._logger.info(f"Read donor: {donor.name}")
        else:
            self._logger.error(f"Donor with ID {donor_id} not found.")
        return donor if donor.exists() else None

    def update_donor(self, donor_id, vals):
        donor = self.browse(donor_id)
        if donor.exists():
            donor.write(vals)
            self._logger.info(f"Updated donor {donor.name} with values {vals}")
            return True
        else:
            self._logger.error(f"Failed to update. Donor with ID {donor_id} not found.")
        return False

    def delete_donor(self, donor_id):
        donor = self.browse(donor_id)
        if donor.exists():
            donor.unlink()
            self._logger.info(f"Deleted donor: {donor.name}")
            return True
        else:
            self._logger.error(f"Failed to delete. Donor with ID {donor_id} not found.")
        return False

    # Domain-based methods

    def search_donor_by_name(self, name):
        donors = self.search([('name', '=', name)])
        self._logger.info(f"Found donors with name '{name}': {donors}")
        return donors

    def search_donor_not_by_blood_type(self, blood_type):
        donors = self.search([('blood_type', '!=', blood_type)])
        self._logger.info(f"Found donors not having blood type '{blood_type}': {donors}")
        return donors

    def search_donors_older_than(self ):
        donors = self.search([('age', '>', 18)])
        self._logger.info(f"Found donors older than {18}: {donors}")
        return donors

    def search_donors_older_or_equal_than(self, age):
        donors = self.search([('age', '>=', age)])
        self._logger.info(f"Found donors older or equal to {age}: {donors}")
        return donors

    def search_donors_younger_than(self, age):
        donors = self.search([('age', '<', age)])
        self._logger.info(f"Found donors younger than {age}: {donors}")
        return donors

    def search_donors_younger_or_equal_than(self, age):
        donors = self.search([('age', '<=', age)])
        self._logger.info(f"Found donors younger or equal to {age}: {donors}")
        return donors

    def search_donors_without_donation_date(self):
        donors = self.search([('last_donation_date', '=?', False)])
        self._logger.info(f"Found donors without a donation date: {donors}")
        return donors

    def search_donor_by_partial_name(self, partial_name):
        donors = self.search([('name', 'like', partial_name)])
        self._logger.info(f"Found donors with partial name '{partial_name}': {donors}")
        return donors

    def search_donor_by_name_case_insensitive(self, partial_name):
        donors = self.search([('name', 'ilike', partial_name)])
        self._logger.info(f"Found donors with case-insensitive name '{partial_name}': {donors}")
        return donors

    def search_donors_by_blood_type_list(self, blood_types):
        donors = self.search([('blood_type', 'in', blood_types)])
        self._logger.info(f"Found donors with blood types in {blood_types}: {donors}")
        return donors

    def search_donors_not_in_blood_types(self, blood_types):
        donors = self.search([('blood_type', 'not in', blood_types)])
        self._logger.info(f"Found donors with blood types not in {blood_types}: {donors}")
        return donors

    def search_donor_child_of(self, parent_id):
        donors = self.search([('id', 'child_of', parent_id)])
        self._logger.info(f"Found donors child of parent with ID {parent_id}: {donors}")
        return donors

    def search_donor_parent_of(self, child_id):
        donors = self.search([('id', 'parent_of', child_id)])
        self._logger.info(f"Found donors parent of child with ID {child_id}: {donors}")
        return donors

    def search_donors_male_older_than(self, age):
        donors = self.search([('age', '>', age), ('gender', '=', 'male')])
        self._logger.info(f"Found male donors older than {age}: {donors}")
        return donors

    def search_donors_by_blood_type_or_city(self, blood_type, city):
        donors = self.search(['|', ('blood_type', '=', blood_type), ('address', 'ilike', city)])
        self._logger.info(f"Found donors with blood type '{blood_type}' or living in '{city}': {donors}")
        return donors

    def search_donors_not_from_city(self, city):
        donors = self.search([('!','address', 'ilike', city)])
        self._logger.info(f"Found donors not from city '{city}': {donors}")
        return donors
