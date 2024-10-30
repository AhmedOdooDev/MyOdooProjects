# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, _, models, api


class ClearanceType(models.Model):
    _name = "clearence.type"
    _description = 'Clearance Type Data'
    _order = 'id asc, name asc'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], 'Active')
    active = fields.Boolean(string='Status', default=True)

    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()
