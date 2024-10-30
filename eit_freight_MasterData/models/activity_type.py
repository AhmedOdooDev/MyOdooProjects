# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, _, models, api


class ActivityType(models.Model):
    _name = "activity.type"
    _description = 'Activity Type Data'
    _order = 'id desc'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    active = fields.Boolean(string='Status', default=True)

    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()
