# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, _, models, api
from odoo.exceptions import ValidationError
from datetime import date


class PartnerType(models.Model):
    _name = "partner.type"
    _description = 'Partner Type Data'
    _order = 'id asc, name asc'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    active = fields.Boolean(string='Status', default=True)
    color = fields.Integer(string="Color")

    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()
