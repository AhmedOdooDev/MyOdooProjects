from odoo import models, fields


class TotalRateCurrency(models.Model):
    _name = 'total.rate.currency'
    _description = "Total Rate currency"

    currency_id = fields.Many2one('res.currency', string="Currency")
    amount = fields.Float(string="Amount")
    sale_cost = fields.Many2one('sale.order')
