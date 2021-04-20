# -*- coding: utf-8 -*-
# from odoo import http


# class Instagram(http.Controller):
#     @http.route('/instagram/instagram/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/instagram/instagram/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('instagram.listing', {
#             'root': '/instagram/instagram',
#             'objects': http.request.env['instagram.instagram'].search([]),
#         })

#     @http.route('/instagram/instagram/objects/<model("instagram.instagram"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('instagram.object', {
#             'object': obj
#         })
