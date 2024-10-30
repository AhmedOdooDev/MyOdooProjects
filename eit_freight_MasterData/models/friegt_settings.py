# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, _, models, api
from odoo.exceptions import UserError


class TransportType(models.Model):
    _name = "transport.type"
    _description = 'Transport Type Data'
    _order = 'id asc'

    name = fields.Char(string="Name")
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], 'Status', readonly=True)
    code = fields.Char(string="Code")
    active = fields.Boolean(string='Active', default=True)

    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()


class PackageType(models.Model):
    _name = "package.type"
    _description = 'Package Type Data'
    _order = 'id desc'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    type = fields.Selection([('air', 'Air'), ('lcr', 'LCR')], 'Is')
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], 'Status', readonly=True)
    active = fields.Boolean(string='Active', default=True)
    tag_type_ids = fields.Many2many('package.tag.type', string="Package Is")

    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()


class ShipmentScop(models.Model):
    _name = "shipment.scop"
    _description = 'Ocean shipments scope Data'
    _order = 'id desc'

    name = fields.Char(string="Name", readonly=True)
    code = fields.Char(string="Code", readonly=True)
    type = fields.Selection([('sea', 'Sea'), ('inland', 'Inland')], 'Type', readonly=True)


class Vessels(models.Model):
    _name = "freight.vessels"
    _description = 'Vessels Data'
    _order = 'id desc'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    partner_id = fields.Many2one('res.partner', string="Vessel Owner")
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], 'Active', readonly=True)
    active = fields.Boolean(string='Status', default=True)

    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()


class BillLeadingType(models.Model):
    _name = "bill.leading.type"
    _description = 'BOL Type Data'
    _order = 'id desc'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    active = fields.Boolean(string='Active', default=True)

    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()


class PackageTagType(models.Model):
    _name = "package.tag.type"
    _description = 'Package Tag Type Data'

    name = fields.Char()


class PackageLine(models.Model):
    _name = "package.line"
    _description = "Package Line"

    commodity_data_id = fields.Many2one('commodity.data', string="Commodity")
    package_type_id = fields.Many2one('package.type', string="Package Type")
    quantity = fields.Integer(string="Quantity")
    gw = fields.Integer(string="GW")
    cbm = fields.Integer(string="CBM")
    shipping_container_id = fields.Many2one('container.data')
