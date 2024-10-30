# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, _, models, api
from odoo.exceptions import ValidationError
from datetime import date


class DocumentsTypes(models.Model):
    _name = "document.type"
    _description = 'Document types'

    name = fields.Text(string="Name")
    type = fields.Selection([('cdoc', 'Customer Docs'), ('odoc', 'Operation Docs')], 'Docs Type')
    active = fields.Boolean(string='Status', default=True)

    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()

