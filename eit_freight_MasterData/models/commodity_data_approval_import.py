# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CommodityDataApprovalsImport(models.Model):
    _name = "commodity.data.approval.import"
    _description = 'Import Approval Needs'

    name = fields.Text(string="Description")
    approval_data_id_import = fields.Many2one('commodity.data')
