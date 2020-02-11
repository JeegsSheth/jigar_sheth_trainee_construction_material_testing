from odoo import http
from odoo.http import request


class Registration(http.Controller):
    @http.route(['/reg/', '/web/signup'], auth='public', type="http", csrf=False)
    def custmoer_register(self, **kw):
        currency = http.request.env['res.currency'].sudo().search([])
        country = http.request.env['res.country'].sudo().search([('name', "=", "India")])
        state = http.request.env['res.country.state'].sudo().search([('country_id', "=", country.id)])
        return http.request.render('cmt.reg_user', {'currency': currency, 'state': state})

    @http.route('/reg/form/<string:user_type>', auth='public', type="http", csrf=False)
    def custmoer_register_form(self, user_type=None, **post):
        if user_type == "laboratory":
            groups_id_name = [(6, 0, [request.env.ref("cmt.group_manager").id])]

            currency_name = post.get('currency')
            currency = request.env['res.currency'].sudo().search([('name', '=', currency_name)], limit=1)
            state = http.request.env['res.country.state'].sudo().search([('name', "=", post.get('state'))], limit=1)
            partner = request.env['res.partner'].sudo().create({
                'name': post.get('username'),
                'email': post.get('email'),
                'mobile': post.get('labcontact'),
                'street': post.get('addressline1'),
                'street2': post.get('addressline2'),
                'city': post.get('city'),
                'state_id': state.id,
                'zip': post.get('pincode'),
                'country_id': state.country_id.id
            })
            company = request.env['res.company'].sudo().create({
                'name': post.get('company'),
                'partner_id': partner.id,
                'currency_id': currency.id,
            })
            request.env['res.users'].sudo().create({
                'partner_id': partner.id,
                'login': post.get('username'),
                'password': post.get('password'),
                'company_id': company.id,
                'company_ids': [(4, company.id)],
                'groups_id': groups_id_name,
            })
        else:
            groups_id_name = [(6, 0, [request.env.ref('base.group_portal', 'base.group_public').id])]

            partner = request.env['res.partner'].sudo().create({
                'name': post.get('username'),
                'email': post.get('email')
            })
            request.env['res.users'].sudo().create({
                'partner_id': partner.id,
                'login': post.get('username'),
                'password': post.get('password'),
                'groups_id': groups_id_name,
            })
        return http.local_redirect('/web/login')
