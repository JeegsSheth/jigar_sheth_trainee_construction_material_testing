from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home


class Home(Home):
    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('cmt.group_manager'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_portal'):
            return '/builder'
        return super(BuilderPortal, self)._login_redirect(uid, redirect=redirect)


class BuilderPortal(http.Controller):
    @http.route(['/builder/<string:findlab>', '/builder'], auth='public', type="http", csrf=False)
    def Builder_Index(self, findlab=None, **post):
        if findlab:
            lab_fac = request.env['facility.detail'].sudo().search([('name', 'in', [post.get('usr_facility')])])
        else:
            lab_fac = request.env['facility.detail'].sudo().search([])
        return request.render('cmt.index_user', {'facilities': lab_fac, })

    @http.route(['/builder/inquiry/<int:lab_fac>', '/builder/inquiry/'], auth='public', type="http", csrf=False)
    def Builder_Inquiry(self, lab_fac=0, **post):
        # print("\n\n\n\n\n\n*****************", lab_fac, "**************************\n\n\n\n\n\n")
        lab_inq = request.env['facility.detail'].sudo().search([('id', '=', lab_fac)])
        return request.render('cmt.inquiry_builder', {'lab_inq': lab_inq, })

    @http.route(['/builder/inquirysubmit/<int:lab_fac>', '/builder/inquirysubmit'], auth='public', type="http", website=True, csrf=False)
    def Builder_Inquiry_Submit(self, lab_fac=0, **post):
        lab_inq = request.env['facility.detail'].sudo().search([('id', '=', lab_fac)])
        usr = request.env['res.users'].sudo().browse(request.session.uid)
        company = request.env['res.company'].sudo().search([('id', '=', lab_inq.company_id.id)])
        request.env['customer.detail'].sudo().create({
            'company_id': company.id,
            'user_id': request.session.uid,
            'name': usr.name,
            'contact': post.get('contact'),
            'email': usr.email,
            'address': post.get('address'),
            'facility_id': lab_inq.id,
            })
        return request.redirect('/builder')

    @http.route(['/order'], auth='public', type="http", csrf=False)
    def Builder_Order(self, **post):
        customer = request.env['customer.detail'].sudo().search([('user_id', '=', request.session.uid)])
        return request.render('cmt.order_list', {'cust': customer, })

    @http.route(['/testing'], auth='public', type="http", csrf=False)
    def Builder_Observation(self, **post):
        test = request.env['testing.detail'].sudo().search([('customer_id.user_id', '=', request.session.uid)])
        return request.render('cmt.testing_list', {'test': test, })
