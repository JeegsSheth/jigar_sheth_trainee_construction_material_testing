from odoo import fields, models


class LaboratoryRegistration(models.Model):
    _name = 'laboratory.registration'
    _description = 'Laboratory Registration'

    name = fields.Char(string="Laboratory Name", required=True)
    labaddress = fields.Char(string="Company Address", required=True)
    labcontact = fields.Char(string="Contact No.", required=True)
    labemail = fields.Char(string="E-Mail Address", required=True)
    city = fields.Char(string="City", required=True)
    district = fields.Char(string="District", required=True)
    state = fields.Char(string="State", required=True)
    pincode = fields.Char(string="Pincode", required=True)
    username = fields.Char(string="User Name", required=True)
    password = fields.Char(string="Password", required=True)


class BuilderRegistration(models.Model):
    _name = 'builder.registration'
    _description = 'Buioder Registration'

    name = fields.Char(string="Builder Name", required=True)
    buildercompname = fields.Char(string="Company Name", required=True)
    buildercompaddress = fields.Char(string="Company Address", required=True)
    buildercontact = fields.Char(string="Contact No.", required=True)
    builderemail = fields.Char(string="E-Mail Address", required=True)
    city = fields.Char(string="City", required=True)
    district = fields.Char(string="District", required=True)
    state = fields.Char(string="State", required=True)
    pincode = fields.Char(string="Pincode", required=True)
    username = fields.Char(string="User Name", required=True)
    password = fields.Char(string="Password", required=True)


class LaboratoryFacility(models.Model):
    _name = 'laboratory.facility'
    _description = 'Laboratory Facility'

    name = fields.Selection([('soiltest', "Soil Test"), ('concretetest', "Concrete Test"), ('cementtest', "Cement Test"), ('steeltest', "Steel Test"), ('fieldtest', "Field Test")], string="Laboratory Facility", required=True)
    labid = fields.Many2one('laboratory.registration', string="Laboratory Name", required=True)
    price = fields.Integer(string="Price", required=True)
