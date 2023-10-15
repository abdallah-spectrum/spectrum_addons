from odoo import api, fields, models, _
from pprint import pprint


class HrContract(models.Model):
    _inherit = 'hr.contract'

    college = fields.Char()
    degree = fields.Char()

    tax_id = fields.Many2one('tax.main')
