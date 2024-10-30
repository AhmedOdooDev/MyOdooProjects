# File: your_module_name/models/shipping_info.py

from odoo import models, fields


class ShippingInfo(models.Model):
    _name = 'shipping.info'
    _description = 'Shipping Information'

    crm_lead_id = fields.Many2one(comodel_name='crm.lead', string='Opportunity')
    dimensions_l = fields.Float(string='Dimensions L')
    dimensions_w = fields.Float(string='Dimensions W')
    dimensions_h = fields.Float(string='Dimensions H')
    quantity = fields.Integer(string='Quantity')
    weight = fields.Float(string='Weight')
    chw = fields.Float(string='CHW')
    volume = fields.Float(string='Volume')
    container_type_id = fields.Many2one(comodel_name='container.type', string='Container Type')
    cbm = fields.Float(string='CBM')
