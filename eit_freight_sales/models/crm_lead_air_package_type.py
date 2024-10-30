from odoo import models, fields, api, tools


class CrmLeadAirPackageType(models.Model):
    _name = 'crm.lead.air.package.type'
    _description = 'CRM Lead AIR Package Type'

    @api.model
    def _get_package_type_domain(self):
        # Search for records containing the specific value
        all_records = self.env['package.type'].sudo().search(
            [('tag_type_ids', 'in', [2])]
        )
        filtered_records = all_records.filtered(lambda r: r.tag_type_ids.ids == [2])
        return [('id', 'in', filtered_records.ids)]

    lead_id = fields.Many2one('crm.lead', string="Lead", store=True)
    package_type_id = fields.Many2one(
        'package.type', string="Package Type", store=True, domain=lambda self: self._get_package_type_domain())
    qty = fields.Float(string="QTY", store=True)
    gw_kg = fields.Float(string="GW (KG)", store=True)
    length_cm = fields.Float(string="L (CM)", store=True)
    width_cm = fields.Float(string="W (CM)", store=True)
    height_cm = fields.Float(string="H (CM)", store=True)
    cbm = fields.Float(string="CBM")
    vm = fields.Float(string="VM", compute='_compute_vm', store=True)
    chw = fields.Float(string="CHW", compute="compute_chw", store=True)
    volume = fields.Float(string='Volume')
    weight = fields.Float(string='Weight')

    @api.onchange('length_cm', 'width_cm', 'height_cm')
    def _compute_cbm(self):
        for rec in self:
            rec.cbm = (rec.length_cm * rec.width_cm * rec.height_cm) / 1000000
            # rec.cbm = cbm * rec.qty

    @api.depends('gw_kg', 'qty', 'width_cm', 'height_cm', 'length_cm', 'vm', 'cbm')
    def compute_chw(self):
        for rec in self:
            if rec.vm > 0 and ((rec.gw_kg * rec.qty) > rec.vm):
                rec.chw = rec.gw_kg * rec.qty
            else:
                total = rec.cbm / 0.006
                rec.chw = total * rec.qty

    @api.depends('gw_kg', 'qty', 'width_cm', 'height_cm', 'length_cm', 'vm', 'cbm')
    def _compute_vm(self):
        for rec in self:
            vm = (rec.length_cm * rec.width_cm * rec.height_cm) / 1000000
            rec.vm = vm / 0.006
