import pytz
from datetime import datetime,timedelta
from odoo import api, fields, models, _
from pprint import pprint
from odoo import tools

class ReportZkDevice(models.Model):
    _name = 'zk.report.daily.attendance'
    _order = 'punching_time'

    employee_device_id = fields.Char()
    punch_type = fields.Selection([('I', 'Check In'),
                                   ('O', 'Check Out'),
                                   ('E', 'Error'),
                                   ('3', 'Break In'),
                                   ('4', 'Overtime In'),
                                   ('5', 'Overtime Out')], string='Punching Type', help="Select the punch type")
    punching_time = fields.Datetime(string='Punching Time', help="Punching Time")

    @api.model
    def create(self, vals):
        att_obj = self.env['hr.attendance']
        atten_time = vals['punching_time']
        atten_time_obj = datetime.strptime(atten_time, '%Y-%m-%d %H:%M:%S')
        attendance_year =atten_time_obj.year
        now = datetime.now()
        year = now.year
        get_user_id = self.env['hr.employee'].search(
            [('employee_device_id', '=', vals['employee_device_id'])])
        result = super(ReportZkDevice, self).create(vals)
        required_date = self.env["spectrum.attendance"].search_read([("id", "!=", 0)], fields=["month"])
        required_month = required_date[-1]['month']
        if year == attendance_year and required_month ==required_month :
            att_var = att_obj.search([('employee_id', '=', get_user_id.id),
                                    ('check_out', '=', False)])
            if bool(get_user_id) != False:
                try:
                    if vals['punch_type'] == "I":  # check-in
                        if not att_var:
                            att_obj.create({'employee_id': get_user_id.id,
                                            'check_in': atten_time})
                    if vals['punch_type'] == "O":  # check-out
                            if len(att_var) == 1:
                                if atten_time_obj > att_var.check_in: 
                                    att_var.write({'check_out': atten_time})
                            else:
                                att_var1 = att_obj.search([('employee_id', '=', get_user_id.id)])
                                if att_var1:
                                    if atten_time_obj > att_var1.check_in: 
                                        att_var1[-1].write({'check_out': atten_time})
                except Exception as e:
                    # if 'singleton' not in e:
                    pprint(e)
                    pprint(vals)
        return result

