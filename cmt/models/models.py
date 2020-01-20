from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CustomerDetail(models.Model):
    _name = 'customer.detail'
    _description = 'Customer Detail'

    name = fields.Char(string="Customer Name", required=True)
    contact = fields.Char(string="Contact No.", required=True)
    email = fields.Char(string="E-Mail Address", required=True)
    facilityname = fields.Selection([('soiltest', "Soil Test"), ('concretetest', "Concrete Test"), ('cementtest', "Cement Test"), ('steeltest', "Steel Test"), ('fieldtest', "Field Test")], string="Laboratory Facility", required=True)

    @api.constrains('contact')
    def _check_ph_no(self):
        for cont in self:
            if cont.contact and len(str(cont.contact)) != 10:
                raise ValidationError("Your Contact No. +91%s is wrong................................" % cont.contact)


class TestingDetail(models.Model):
    _name = 'testing.detail'
    _description = 'Testing Detail'
    _rec_name = 'custid'

    custid = fields.Many2one('customer.detail', string="Laboratory Name", required=True)
    address = fields.Char(string="Testing Address", required=True)
    facilityname = fields.Selection([('soiltest', "Soil Test"), ('concretetest', "Concrete Test"), ('cementtest', "Cement Test"), ('steeltest', "Steel Test"), ('fieldtest', "Field Test")], string="Laboratory Facility", related="custid.facilityname")
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
