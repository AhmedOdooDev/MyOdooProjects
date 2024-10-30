# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class FreightCondition(models.Model):
    _name = "freight.conditions"
    _description = 'Freight Condition'
    _order = 'id desc'

    name = fields.Char(string="Name")
    Terms = fields.Html(string="Terms & Conditions")
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], 'Active')
    active = fields.Boolean(string='Status', default=True)

    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()
