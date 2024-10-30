from odoo import models, fields, api, tools


class CrmLeadNonAirPackageType(models.Model):
    _name = 'crm.lead.non.air.package.type'
    _description = 'CRM Lead Non-AIR Package Type'

    lead_id = fields.Many2one('crm.lead', string="Lead", store=True)
    package_type_id = fields.Many2one(
        'package.type', string="Package Type", store=True,
        domain="[('tag_type_ids', 'in', [1])]")
    container_type_id = fields.Many2one(comodel_name='container.type', string='Container Type')
    qty = fields.Float(string="QTY", store=True)
    gw_kg = fields.Float(string="GW (KG)", store=True)
    length_cm = fields.Float(string="L (CM)", store=True)
    width_cm = fields.Float(string="W (CM)", store=True)
    height_cm = fields.Float(string="H (CM)", store=True)
    volume = fields.Float(string='Volume')
    weight = fields.Float(string='Weight')
    cbm = fields.Float(string="CBM")

    @api.onchange('length_cm', 'width_cm', 'height_cm')
    def _compute_cbm(self):
        for rec in self:
            cbm = (rec.length_cm * rec.width_cm * rec.height_cm) / 1000000
            rec.cbm = cbm * rec.qty
