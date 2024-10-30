# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class CommodityGroup(models.Model):
    _name = "commodity.group"
    _description = 'Commodity Group'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], 'Status')
    active = fields.Boolean(string='Active', default=True)
    commodities_ids = fields.Many2many(comodel_name='commodity.data', relation='commodity_group_commodity_rel',
                                       column1='commodity_group_id', column2='commodity_id', string="Commodities")

    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()
