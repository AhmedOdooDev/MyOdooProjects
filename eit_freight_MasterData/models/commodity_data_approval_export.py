# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CommodityDataApprovalsExport(models.Model):
    _name = "commodity.data.approval.export"
    _description = 'Export Approval Needs'

    name = fields.Text(string="Description")
    approval_data_id_export = fields.Many2one('commodity.data')
