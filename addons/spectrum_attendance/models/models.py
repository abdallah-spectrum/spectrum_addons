# -*- coding: utf-8 -*-

from odoo import models, fields, api


class spectrum_attendance(models.Model):
    _name = 'spectrum.attendance'
    _description = 'spectrum.attendance'

    month =fields.Integer()
