# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, _, models, api
from odoo.exceptions import ValidationError
from datetime import date


class CommodityData(models.Model):
    _name = "commodity.data"
    _description = 'Commodity Data'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string="Name")
    code = fields.Char(string="Hs Code", required=True)
    tax = fields.Integer(string="Import Tax")
    vat = fields.Integer(string="Vat")
    commodity_group_ids = fields.Many2many(comodel_name='commodity.group', relation='commodity_group_commodity_rel',
                                           column1='commodity_id', column2='commodity_group_id',
                                           string="Commodity Group")
    type = fields.Selection([('dry', 'Dry'), ('reefer', 'Reefer'), ('imo', 'IMO')], 'Commodity Type')
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], 'Status', readonly=True)
    active = fields.Boolean(string='Active', default=True)
    import_approval = fields.One2many('commodity.data.approval.import', 'approval_data_id_import'
                                      , string="Import Approvals")
    export_approval = fields.One2many('commodity.data.approval.export', 'approval_data_id_export'
                                      , string="Export Approvals")
    export_custom = fields.One2many('commodity.data.custom.export', 'custom_data_id_import'
                                    , string="Export Req")
    import_custom = fields.One2many('commodity.data.custom.import', 'custom_data_id_import'
                                    , string="Import Req")
    industry_id = fields.Many2one(
        comodel_name='res.partner.industry', string="Industry")
    req_id = fields.Many2many('commodity.req', string="Commodity Equip")
    tag_ids = fields.Many2many('frieght.tags', string="Tags")
    export_tax = fields.Integer(string="Export Tax")

    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()

    @api.constrains('code')
    def _check_even_numbers(self):
        for record in self:
            if record.code:
                counts = 0
                numbers = record.code
                # if len(numbers) not in {6, 8, 10}:
                #     raise ValidationError("HSCode Format Can Accept 6, 8, or 10 Digits")

    def write(self, values):
        if 'code' in values:
            self._check_even_numbers()
        return super(CommodityData, self).write(values)

    def create(self, values):
        record = super(CommodityData, self).create(values)
        return record
