# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, _, models, api
from odoo.exceptions import ValidationError
from datetime import date


class CommodityReq(models.Model):
    _name = "commodity.req"
    _description = 'Commodity Equip'

    name = fields.Char()
