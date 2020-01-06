from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime as dt


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

    @api.constrains('labcontact')
    def _check_ph_no(self):
        for cont in self:
            if cont.labcontact and len(str(cont.labcontact)) != 10:
                raise ValidationError("Your Contact No. is wrong :- %s" % cont.labcontact)

    _sql_constraints = [
        ('labcontact_uniq', 'unique(labcontact)', 'Contact No. is Already register!'),
        ('labemail_uniq', 'unique(labemail)', 'E-Mail is Already register!')
    ]


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

    @api.constrains('buildercontact')
    def _check_ph_no(self):
        for cont in self:
            if cont.buildercontact and len(str(cont.buildercontact)) != 10:
                raise ValidationError("Your Contact No. is wrong :- %s" % cont.buildercontact)

    _sql_constraints = [
        ('buildercontact_uniq', 'unique(buildercontact)', 'Contact No. is Already register!'),
        ('builderemail_uniq', 'unique(builderemail)', 'E-Mail is Already register!')
    ]


class LaboratoryFacility(models.Model):
    _name = 'laboratory.facility'
    _description = 'Laboratory Facility'

    name = fields.Selection([('soiltest', "Soil Test"), ('concretetest', "Concrete Test"), ('cementtest', "Cement Test"), ('steeltest', "Steel Test"), ('fieldtest', "Field Test")], string="Laboratory Facility", required=True)
    labid = fields.Many2one('laboratory.registration', string="Laboratory Name", required=True)
    price = fields.Integer(string="Price", required=True)


class InquiryRequest(models.Model):
    _name = 'builder.inquiry'
    _description = 'Inquiry Request'
    _rec_name = "builderid"

    builderid = fields.Many2one('builder.registration', string="Builder Name", required=True)
    labfacid = fields.Many2one('laboratory.facility', string="Laboratory Facility", required=True)
    detail = fields.Text(string="Detail", required=True, help="Inquiry Detail")
    datetime = fields.Datetime(string="Inquiry Request Date And Time")

    @api.depends('detail')
    def _value_people(self):
        for record in self:
            dat = dt.utcnow()
            record.datetime = dat.strftime("%Y-%m-%d %H:%M:%S")


class InquiryResponce(models.Model):
    _name = 'laboratory.inquiry'
    _description = 'Inquiry Responce'
    _rec_name = "reqid"

    reqid = fields.Many2one("builder.inquiry", string="Builder Name", required=True)
    detail = fields.Text(string="Detail", required=True, help="Responce Detail of Inquiry")
    datetime = fields.Datetime(string="Inquiry Request Date And Time")

    @api.depends('detail')
    def _value_people(self):
        for record in self:
            dat = dt.utcnow()
            record.datetime = dat.strftime("%Y-%m-%d %H:%M:%S")


class Testing(models.Model):
    _name = 'laboratory.testing'
    _description = 'Laboratory Testing'
    _rec_name = "builderid"

    labid = fields.Many2one('laboratory.registration', string="Laboratory Name", required=True)
    builderid = fields.Many2one('builder.registration', string="Builder Name", required=True)
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
