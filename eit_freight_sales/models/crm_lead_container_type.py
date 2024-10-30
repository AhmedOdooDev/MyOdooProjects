from odoo import models, fields, api, tools


class CrmLeadContainerType(models.Model):
    _name = 'crm.lead.container.type'
    _description = 'CRM Lead Container Type'

    lead_id = fields.Many2one('crm.lead', string="Lead", store=True)
    container_type_id = fields.Many2one('container.type', string="Container Type", store=True)
    qty = fields.Float(string="QTY", store=True)
    gw_kg = fields.Float(string="GW (KG)", store=True)
