# -*- coding: utf-8 -*-
# from odoo import http


# class Cmt(http.Controller):
#     @http.route('/cmt/cmt/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cmt/cmt/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cmt.listing', {
#             'root': '/cmt/cmt',
#             'objects': http.request.env['cmt.cmt'].search([]),
#         })

#     @http.route('/cmt/cmt/objects/<model("cmt.cmt"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cmt.object', {
#             'object': obj
#         })
