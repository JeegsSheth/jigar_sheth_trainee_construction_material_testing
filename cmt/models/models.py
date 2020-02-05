from odoo import api, fields, models
from odoo.exceptions import ValidationError
import datetime


class CustomerDetail(models.Model):
    _name = 'customer.detail'
    _description = 'Customer Detail'

    company_id = field_name_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    user_id = fields.Many2one('res.users')
    name = fields.Char(string="Customer Name", related="user_id.partner_id.name", store=True)
    contact = fields.Char(string="Contact No.")
    email = fields.Char(string="E-Mail Address", related="user_id.partner_id.email", store=True)
    address = fields.Char(string="Testing Address")
    facility_id = fields.Many2one('facility.detail', string="Laboratory Facility")
    state = fields.Selection([("confirm", "Confirm"), ("pending", "Pending"), ("cancel", "Cancel")], string="State of Order", default="pending")

    @api.constrains('contact')
    def _check_ph_no(self):
        for cont in self:
            if cont.contact and len(str(cont.contact)) != 10:
                raise ValidationError("Your Contact No. +91%s is wrong................................" % cont.contact)


class FacilityDetail(models.Model):
    _name = 'facility.detail'
    _description = 'Facility Detail'

    company_id = field_name_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    name = fields.Selection([('soil_test', "Soil Test"), ('concrete_test', "Concrete Test"), ('steel_test', "Steel Test"), ('field_test', "Field Test"), ('cement_lime_mortar_test', "Cement, Lime & Mortar Test"), ('sand_aggregate_fillers_test', "Sand, Aggregate & Fillers Test"), ('rock_test', "Rock Test"), ('bitumen_asphalt_test', "Bitumen & Asphalt Test"), ('geotextile_test', "Geotextile Test"), ('water_test', "Water Testing"), ('brick_block_test', "Brick & Block Test")], string="Laboratory Facility", required=True)
    price = fields.Integer("Facility Price")


class TestingDetail(models.Model):
    _name = 'testing.detail'
    _description = 'Testing Detail'
    _rec_name = 'customer_id'

    company_id = field_name_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    customer_id = fields.Many2one('customer.detail', string="Customer Name", required=True)
    facility_id = fields.Many2one('facility.detail', string="Laboratory Facility", related="customer_id.facility_id", store=True)
    testingstart = fields.Date(string="Testing Start", required=True, default=datetime.date.today())
    testingend = fields.Date(string="Testing End", required=True, default=datetime.date.today())
    testingdays = fields.Integer("Testing Days", compute="_compute_value_day")
    testingdaysleft = fields.Integer("Testing Days Left", compute="_compute_value_day")
    state = fields.Selection([("todo", "To Do"), ("inprogress", "In Progress"), ("completed", "Completed")], string="State of Testing", default="todo", compute="_compute_value_day", store=True)

    @api.depends('testingstart', 'testingend')
    def _compute_value_day(self):
        for record in self:
            start = datetime.datetime.strptime(str(record.testingstart), "%Y-%m-%d").date()
            end = datetime.datetime.strptime(str(record.testingend), "%Y-%m-%d").date()
            curr = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d").date()
            record.testingdays = (end - start).days
            left = (end - curr).days
            if left > 0:
                record.testingdaysleft = left
            else:
                record.testingdaysleft = 0
            diffstart = (curr - start).days
            diffend = (end - curr).days
            if diffstart >= 0 and diffend < 0:
                record.state = "completed"
            elif diffstart >= 0 and diffend >= 0:
                record.state = "inprogress"
            elif diffstart < 0 and diffend >= 0:
                record.state = "todo"


class Observation(models.Model):
    _name = "testing.observation"
    _description = "Observation"
    _rec_name = 'test_id'

    company_id = field_name_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    test_id = fields.Many2one('testing.detail', string="Customer Name", required=True)
    facility_id = fields.Many2one('facility.detail', string="Laboratory Facility", related="test_id.facility_id")
    soil_result = fields.One2many(comodel_name='testing.result', inverse_name='observation_id', string="Soil Result")


class TestResult(models.Model):
    _name = "testing.result"
    _description = "Test Result"
    _rec_name = "sample_depth"

    company_id = field_name_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    observation_id = fields.Many2one("testing.observation", string="Observation", ondelete="cascade")
    sample_depth = fields.Float(string="Sample Depth")
    sample_type = fields.Selection([('uds', "UDS"), ('spt', "SPT"), ('rs', "RS")], string="Sample Type")
    gravel = fields.Integer(string="Gravel (%)")
    sand = fields.Integer(string="Sand (%)")
    silt_clay = fields.Integer(string="Silt & Clay (%)")
    classification = fields.Selection([('sm', "SM"), ('sp_sm', "SP-SM")], string="Classification")
    field_dry_density = fields.Float(string="Field Dry Density (gm/cc)")
    field_moisture_content = fields.Float(string="Field Moisture Content (%)")
    specific_gravity = fields.Float(string="Specific Gravity")
    cohesion = fields.Float(string="Cohesion (kg/cm²)")
    angle_of_internal_friction = fields.Float(string="Angle of Internal Friction")
