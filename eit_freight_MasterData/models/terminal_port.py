# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, _, models, api


class TerminalPort(models.Model):
    _name = "terminal.port"
    _description = 'Terminal Port Data'

    name = fields.Char(string="Name")
    port_city_id = fields.Many2one('port.cites', string="Port / City")
    country_id = fields.Many2one('res.country', string="Country")
    address = fields.Text(string="Address")
    warehouse = fields.Boolean(string="Warehouse")
    terminal = fields.Boolean(string="Terminal")
    active = fields.Boolean(string='Status', default=True)

    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()

    @api.onchange('port_city_id')
    def _onchange_port_city_id(self):
        if self.port_city_id:
            self.country_id = self.port_city_id.country_id


class PortCitiesType(models.Model):
    _name = "port.type"
    _description = 'Port Type Data'

    name = fields.Char()
