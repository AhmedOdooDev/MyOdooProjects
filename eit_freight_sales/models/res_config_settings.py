from odoo import models, fields, api, tools


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_use_lead = fields.Boolean(default=True)

    # @api.model
    # def get_values(self):
    #     res = super(ResConfigSettings, self).get_values()
    #     res.update(
    #         group_use_lead=True,
    #         group_proforma_sales=True
    #     )
    #     return res
