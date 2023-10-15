from odoo import api, fields, models, _
from pprint import pprint


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    employee_device_id = fields.Char(string='Employee Device ID',groups="hr.group_hr_user")
