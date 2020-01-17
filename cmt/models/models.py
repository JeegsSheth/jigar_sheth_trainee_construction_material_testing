from odoo import api, fields, models
from odoo.exceptions import ValidationError


class LaboratoryDetail(models.Model):
    _name = 'laboratory.detail'
    _description = 'Laboratory Detail'

    name = fields.Char(string="Laboratory Name", required=True)
    labaddress = fields.Char(string="Laboratory Address", required=True)
    labcontact = fields.Char(string="Contact No.", required=True)
    labemail = fields.Char(string="E-Mail Address", required=True)
    city = fields.Char(string="City", required=True)
    district = fields.Char(string="District", required=True)
    state = fields.Char(string="State", required=True)
    pincode = fields.Char(string="Pincode", required=True)
    facilityname = fields.Selection([('soiltest', "Soil Test"), ('concretetest', "Concrete Test"), ('cementtest', "Cement Test"), ('steeltest', "Steel Test"), ('fieldtest', "Field Test")], string="Laboratory Facility", required=True)
    price = fields.Integer(string="Price", required=True)

    @api.constrains('labcontact')
    def _check_ph_no(self):
        for cont in self:
            if cont.labcontact and len(str(cont.labcontact)) != 10:
                raise ValidationError("Your Contact No. is wrong :- %s" % cont.labcontact)


class BuilderDetail(models.Model):
    _name = 'builder.detail'
    _description = 'Buioder Detail'

    name = fields.Char(string="Builder Name", required=True)
    buildercompname = fields.Char(string="Company Name", required=True)
    buildercompaddress = fields.Char(string="Company Address", required=True)
    buildercontact = fields.Char(string="Contact No.", required=True)
    builderemail = fields.Char(string="E-Mail Address", required=True)
    city = fields.Char(string="City", required=True)
    district = fields.Char(string="District", required=True)
    state = fields.Char(string="State", required=True)
    pincode = fields.Char(string="Pincode", required=True)

    @api.constrains('buildercontact')
    def _check_ph_no(self):
        for cont in self:
            if cont.buildercontact and len(str(cont.buildercontact)) != 10:
                raise ValidationError("Your Contact No. is wrong :- %s" % cont.buildercontact)

    _sql_constraints = [
        ('buildercontact_uniq', 'unique(buildercontact)', 'Contact No. is Already in Detail!'),
        ('builderemail_uniq', 'unique(builderemail)', 'E-Mail is Already in Detail!')
    ]


class Testing(models.Model):
    _name = 'laboratory.testing.status'
    _description = 'Laboratory Testing'
    _rec_name = "builderid"

    labid = fields.Many2one('laboratory.detail', string="Laboratory Name", required=True)
    builderid = fields.Many2one('builder.detail', string="Builder Name", required=True)
    testingstart = fields.Date(string="Testing Start", required=True)
    testingend = fields.Date(string="Testing End", required=True)
    state = fields.Selection([("todo", "To Do"), ("inprogress", "In Progress"), ("completed", "Completed")], string="State of Testing", default="todo")

    def action_inprogress(self):
        self.write({'state': "inprogress"})
        return True

    def action_completed(self):
        self.write({'state': "completed"})
        return True

    def action_todo(self):
        self.write({'state': "todo"})
        return True
