# # -*- coding: utf-8 -*-
#
from odoo import models, fields, api, _
# import datetime
# from odoo.exceptions import ValidationError
# from datetime import timedelta
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _order = 'id desc'

    invoice_type = fields.Selection(
        string='Invoice Type',
        selection=[('invoice', 'Invoice'),
                   ('statement', 'Statement '),
                   ])
    calculation_type = fields.Selection(
        string='Calculation Type',
        selection=[('invoice', 'Chargeable Weight'),
                   ('gross_weight', 'Gross Weight'),
                   ('fixed_charge', 'Fixed Charge'),
                   ('container', 'Container'),
                   ('teu', 'TEU'),
                   ('volume', 'Volume'),
                   ('days', 'Days'),
                   ])
    service_scope_ids = fields.Many2many(comodel_name='service.scope', string="Service Scope")
