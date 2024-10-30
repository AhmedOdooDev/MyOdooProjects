from odoo import models, fields


class SalePartiesLine(models.Model):
    _name = 'sale.parties.line'

    partner_type_id = fields.Many2one('partner.type', string="Partner Type")
    partner_id = fields.Many2one('res.partner', string="Partner Name",
                                 domain="[('partner_type_id', '=', partner_type_id)]")
    phone = fields.Char(related='partner_id.phone', string="Phone")
    email = fields.Char(related='partner_id.email', string="Email")
    city = fields.Char(related="partner_id.city", string="City")
    country_id = fields.Many2one(related='partner_id.country_id', string="Country")
    sale_parties_id = fields.Many2one('sale.order')
