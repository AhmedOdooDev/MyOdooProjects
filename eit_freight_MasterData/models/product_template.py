# # -*- coding: utf-8 -*-
#
from odoo import models, fields, api, _
# import datetime
# from odoo.exceptions import ValidationError
# from datetime import timedelta
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # detailed_type = fields.Selection(
    #     selection_add=[('charge_type', 'Charge Type')],
    #     ondelete={'charge_type': 'set default'})
    type = fields.Selection(
        selection_add=[('charge_type', 'Charge Type')],
        ondelete={'charge_type': 'set default'})
    is_sale_purchase = fields.Boolean()
    is_invoice_bill = fields.Boolean()

    @api.model_create_multi
    def create(self, values):
        for vals in values:
            if vals.get('type') == 'charge_type' and not self.env.user.id == 1 and not self.env.user.has_group(
                    'eit_freight_MasterData.group_freight_manager'):
                raise UserError('Only freight manager can create charge type')
        res = super(ProductTemplate, self).create(values)
        if res.type == 'charge_type' and res.is_sale_purchase:
            raise UserError(
                _('Please add the Charge Type from the MasterData App \n Master Data >> Service Setting Menu >> Charge Type'))

        if res.type == 'charge_type' and res.is_invoice_bill:
            raise UserError(
                _('Please add the Charge Type from the MasterData App \n Master Data >> Service Setting Menu >> Charge Type'))
        return res

    def write(self, vals):
        is_sale_purchase = self.env.context.get('default_is_sale_purchase', False)
        is_invoice_bill = self.env.context.get('default_is_invoice_bill', False)

        if vals.get('type') == 'charge_type' and is_sale_purchase:
            raise UserError(
                _('Please add the Charge Type from the MasterData App \n Master Data >> Service Setting Menu >> Charge Type'))

        if vals.get('type') == 'charge_type' and is_invoice_bill:
            raise UserError(
                _('Please add the Charge Type from the MasterData App \n Master Data >> Service Setting Menu >> Charge Type'))

        result = super(ProductTemplate, self).write(vals)
        if self.type == 'charge_type' and not self.env.user.id == 1 and not self.env.user.has_group(
                'eit_freight_MasterData.group_freight_manager'):
            raise UserError('Only freight manager can edit charge type')
        return result
