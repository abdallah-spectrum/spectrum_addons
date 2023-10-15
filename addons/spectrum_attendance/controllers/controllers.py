# -*- coding: utf-8 -*-
# from odoo import http


# class SpectrumAttendance(http.Controller):
#     @http.route('/spectrum_attendance/spectrum_attendance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/spectrum_attendance/spectrum_attendance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('spectrum_attendance.listing', {
#             'root': '/spectrum_attendance/spectrum_attendance',
#             'objects': http.request.env['spectrum_attendance.spectrum_attendance'].search([]),
#         })

#     @http.route('/spectrum_attendance/spectrum_attendance/objects/<model("spectrum_attendance.spectrum_attendance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('spectrum_attendance.object', {
#             'object': obj
#         })
