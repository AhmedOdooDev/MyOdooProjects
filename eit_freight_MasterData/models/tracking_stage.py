# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, _, models, api


class TrackingStage(models.Model):
    _name = "tracking.stage"
    _description = 'Tracking Stage Data'
    _order = 'code'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code", readonly=True)
    active = fields.Boolean(string='Status', default=True)
    docs_type = fields.Selection([('custom_doc', 'Customer Docs'), ('operation_doc', 'Operation Docs')])
    stage_clearance = fields.Boolean(string='Clearance')
    stage_freight = fields.Boolean(string='Freight')
    clearance_type_id = fields.Many2one(comodel_name='clearence.type', string='Clearance Type')
    description = fields.Text(string="Description")

    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()

    @api.model_create_multi
    def create(self, vals_list):
        # Fetch the clearance_type_id's code
        for vals in vals_list:
            clearance_type = self.env['clearence.type'].browse(vals.get('clearance_type_id'))
            sequence = self.env['ir.sequence'].next_by_code('tracking.stage.seq') or '/'
            if clearance_type and clearance_type.code:
                # Generate the sequence
                # Concatenate clearance type code with sequence
                vals['code'] = f"{clearance_type.code}-{sequence}"
            else:
                vals['code'] = f"NO_CODE/{sequence}"

        return super(TrackingStage, self).create(vals_list)

    def write(self, vals):
        # Check if clearance_type_id is in vals, which means it has been changed
        if 'clearance_type_id' in vals:
            clearance_type = self.env['clearence.type'].browse(vals.get('clearance_type_id'))
            sequence = self.env['ir.sequence'].next_by_code('tracking.stage.seq') or '/'
            if clearance_type and clearance_type.code:
                # Generate the sequence
                # Concatenate clearance type code with sequence
                vals['code'] = f"{clearance_type.code}-{sequence}"
            else:
                vals['code'] = f"NO_CODE/{sequence}"

        return super(TrackingStage, self).write(vals)
