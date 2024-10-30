# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, _, models, api


class ContainerType(models.Model):
    _name = "container.type"
    _description = 'Container Type Data'
    _order = 'id'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    container_type = fields.Selection([('dry', 'Dry'), ('reefer', 'Reefer'), ('sequ', 'Special Equ')], 'Type Is')
    size = fields.Float(string="Size")
    volume = fields.Float(string="Volume")
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], 'Status', readonly=True)
    active = fields.Boolean(string='Active', default=True)

    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()
