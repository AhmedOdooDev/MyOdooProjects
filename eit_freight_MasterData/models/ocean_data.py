from odoo import fields, models, api


class OceanData(models.Model):
    _name = 'ocean.data'
    _description = 'Ocean Data'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)