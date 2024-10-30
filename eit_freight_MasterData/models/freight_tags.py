# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class FreightTags(models.Model):
    _name = "frieght.tags"
    _description = 'Freight Tags'

    name = fields.Text(string="Name")
    active = fields.Boolean(string='Status', default=True)
    color = fields.Integer(string="Color")

    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()
