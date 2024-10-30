# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, _, models, api
from odoo.exceptions import ValidationError
from datetime import date


class CarrierRoute(models.Model):
    _inherit = "carrier.route"

    crm_lead_ids = fields.One2many(
        "crm.lead",
        "carrier_route_id",
        string="Leads",
    )
    crm_lead_count = fields.Integer(
        compute="_compute_crm_lead_count",
        string="Opportunities",
        store=False,
    )
    route_type = fields.Selection(
        [
            ("air", "Air"),
            ("sea", "Sea"),
        ],
        string="Route Type",
        required=True,
        tracking=True,
        default="air",
    )

    def _compute_crm_lead_count(self):
        for record in self:
            record.crm_lead_count = len(record.crm_lead_ids)

    def action_open_crm_leads(self):
        # Get the predefined CRM lead pipeline action
        action = self.env.ref("crm.crm_lead_action_pipeline").read()[0]

        # Modify the view mode to include both 'kanban' and 'form'
        action["view_mode"] = "kanban,form"

        # Modify the domain to filter based on crm_lead_ids
        action["domain"] = [("id", "in", self.crm_lead_ids.ids)]

        # Add custom context, including default values for 'pol_id' and 'pod_id'
        action["context"] = {
            "default_pol_id": (
                self.pol_id.id if self.pol_id else False
            ),  # Replace with your field
            "default_pod_id": (
                self.pod_id.id if self.pod_id else False
            ),  # Replace with your field
            "default_type": "opportunity",
            **self.env.context,  # Retain any existing context values
        }

        # Specify the custom form view (eit_freight_sales.view_crm_lead_form_inherit)
        action["views"] = [
            (False, "kanban"),  # Keep kanban as the fallback view
            (self.env.ref("eit_freight_sales.view_crm_lead_form_inherit").id, "form"),
        ]

        return action
