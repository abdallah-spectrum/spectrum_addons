# -*- coding: utf-8 -*-
# from odoo import http


# class FixDynamicReportBalanceSheet(http.Controller):
#     @http.route('/fix_dynamic_report_balance_sheet/fix_dynamic_report_balance_sheet', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fix_dynamic_report_balance_sheet/fix_dynamic_report_balance_sheet/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('fix_dynamic_report_balance_sheet.listing', {
#             'root': '/fix_dynamic_report_balance_sheet/fix_dynamic_report_balance_sheet',
#             'objects': http.request.env['fix_dynamic_report_balance_sheet.fix_dynamic_report_balance_sheet'].search([]),
#         })

#     @http.route('/fix_dynamic_report_balance_sheet/fix_dynamic_report_balance_sheet/objects/<model("fix_dynamic_report_balance_sheet.fix_dynamic_report_balance_sheet"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fix_dynamic_report_balance_sheet.object', {
#             'object': obj
#         })
