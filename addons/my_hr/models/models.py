from odoo import api, fields, models, _
from pprint import pprint


class Penalties(models.Model):
    _name = "penalties"
    _description = "penalties"

    name = fields.Char()
    date = fields.Datetime()
    contrary = fields.Text()
    penalty = fields.Text()
    salary_affected = fields.Boolean()


class TaxMain(models.Model):
    _name = "tax.main"
    _description = "tax Model"

    start_date = fields.Datetime()
    end_date = fields.Datetime()
    segments_number = fields.Integer()
    personal_exemption = fields.Float()
    max_val = fields.Float()
    tax_lines = fields.One2many('tax.detail', 'tax_id', string='Tax Lines',  copy=True, auto_join=True)


class TaxDetail(models.Model):
    _name = "tax.detail"
    _description = "tax Model"

    tax_id = fields.Many2one('tax.main', string='Tax Reference', required=True, ondelete='cascade', index=True, copy=False)

    name = fields.Char()
    ultimate_flag = fields.Boolean()
    starting_from = fields.Integer()
    min_val = fields.Float()
    max_val = fields.Float()
    percentage = fields.Float(digits=(3,3))