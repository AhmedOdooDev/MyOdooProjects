from odoo import models, fields, api, tools


class Stage(models.Model):
    _inherit = "crm.stage"

    name = fields.Char(string="Pricing")
    is_pricing_stage = fields.Boolean(string="Is Pricing Stage")
    is_follow_up_stage = fields.Boolean(string="Is Follow Up Stage")
    #
    # @api.onchange('is_pricing_stage')
    # def _onchhange_is_pricing_stage(self):
    #     if self.is_pricing_stage:
    #         if self.name == "Proposition":
    #             self.name = "Follow Up"
    #     else:
    #         if self.name == "Proposition":
    #             self.name = "Proposition"
