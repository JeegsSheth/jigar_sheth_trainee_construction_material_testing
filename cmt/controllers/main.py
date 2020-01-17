from odoo import http


class Lab(http.Controller):
    @http.route('/lab/', auth='public', website=True, csrf=False)
    def index(self, **kw):
        Status = http.request.env['laboratory.detail']
        return http.request.render('cmt.lab_det', {
            'status': Status.search([]),
        })

    @http.route('/lab/delete/<model("laboratory.detail"):st>', auth='public', website=True, csrf=False)
    def delete(self, st=None):
        if st:
            st.unlink()
        return http.request.redirect('/lab/')

    @http.route(['/lab/create/', '/lab/edit/<model("laboratory.detail"):st>'], auth='public', website=True, csrf=False)
    def create(self, st=None):
        if st:
            st = http.request.env["laboratory.detail"].browse([st.id])
        return http.request.render('cmt.lab_cre', {'labs': st})

    @http.route(['/lab/created/', '/lab/created/<int:labs>'], auth='public', website=True, csrf=False, method="post")
    def created(self, labs=None, **post):
        if post:
            if labs:
                http.request.env['laboratory.detail'].browse([labs]).write(post)
            else:
                http.request.env['laboratory.detail'].create(post)

        return http.request.redirect('/lab/')
