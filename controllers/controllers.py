# -*- coding: utf-8 -*-
from odoo import http

# class Debranding-project(http.Controller):
#     @http.route('/debranding-project/debranding-project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/debranding-project/debranding-project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('debranding-project.listing', {
#             'root': '/debranding-project/debranding-project',
#             'objects': http.request.env['debranding-project.debranding-project'].search([]),
#         })

#     @http.route('/debranding-project/debranding-project/objects/<model("debranding-project.debranding-project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('debranding-project.object', {
#             'object': obj
#         })