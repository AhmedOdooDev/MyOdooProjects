from odoo import models, fields, api


class SaleCharges(models.Model):
    _name = 'sale.charges'
    _description = "Sale Charges"

    product_id = fields.Many2one('product.template', string="Charge Type",
                                 domain="[('type', '=', 'charge_type')]")
    sale_price = fields.Float(string="Sale price")
    qty = fields.Float(string="QTY")
    package_type = fields.Many2one('package.type', string="Package Type")

    currency_id = fields.Many2one('res.currency', string="Currency")
    ex_rate = fields.Float(related='currency_id.rate', string="EX.Rate", store=True)
    tot_cost_fr = fields.Float(string="Total sale In System Currency", compute='_compute_tot_price')
    tot_cost = fields.Float(string="Total sale in ( auto fill from pricing currency)",
                            compute='_compute_tot_price')
    order_id = fields.Many2one('sale.order')

    @api.depends('sale_price', 'ex_rate', 'qty')
    def _compute_tot_price(self):
        for record in self:
            if record.sale_price and record.ex_rate and record.qty:
                record.tot_cost_fr = record.sale_price * record.ex_rate * record.qty
            else:
                record.tot_cost_fr = 0

            record.tot_cost = record.product_id.currency_id.rate * record.tot_cost_fr
