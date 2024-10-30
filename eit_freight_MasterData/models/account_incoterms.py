from odoo import api, fields, models


class AccountIncoterms(models.Model):
    _inherit = 'account.incoterms'
    _order = 'id desc'

    pickup = fields.Boolean(string="Pickup Address")
    delivery = fields.Boolean(string="Delivery Address")
