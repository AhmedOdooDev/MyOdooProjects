from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class Lead2OpportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    def action_apply(self):
        self.opportunity_source == "Lead"
        return super(Lead2OpportunityPartner, self).action_apply()
