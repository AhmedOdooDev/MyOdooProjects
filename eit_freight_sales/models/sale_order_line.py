from odoo import models, fields, api
from odoo.addons.test_import_export.models.models_export_impex import field


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    package_type = fields.Many2one("package.type", string="Package Type")
    container_type = fields.Many2one("container.type", string="Container Type")
    unit_rate = fields.Monetary(string="Unit Rate")
    currency_usd_id = fields.Many2one(
        comodel_name="res.currency",
        compute="_compute_currency_usd_id",
    )
    main_currency_id = fields.Many2one(
        comodel_name="res.currency",
        compute="_compute_main_currency_id",
        string="Main Currency",
        store=True,
    )
    main_curr = fields.Monetary(
        string="Main Currency",
        compute="_compute_tot_price",
        currency_field="main_currency_id",
    )
    technical_rate = fields.Float(string="Technical Rate", compute="compute_ex_rate")
    ex_rate = fields.Float(string="Ex. Rate", compute="compute_ex_rate")
    price_subtotal = fields.Monetary(
        string="Tax excl.",
        compute="_compute_amount",
        store=True,
        precompute=True,
        currency_field="currency_usd_id",
    )
    price_total = fields.Monetary(
        string="Total",
        compute="_compute_amount",
        store=True,
        precompute=True,
        currency_field="currency_usd_id",
    )
    price_subtotal_main_curr = fields.Monetary(
        string="Tax excl. (Main Curr)",
        compute="_compute_amount",
        store=True,
        precompute=True,
        currency_field="main_currency_id",
    )
    price_tax_main_curr = fields.Float(
        string="Total Tax",
        compute="_compute_amount",
        store=True,
        precompute=True,
        currency_field="main_currency_id",
    )
    price_total_main_curr = fields.Monetary(
        string="Tax incl. (Main Curr)",
        compute="_compute_amount",
        store=True,
        precompute=True,
        currency_field="main_currency_id",
    )

    @api.onchange("unit_rate", "product_id", "product_uom_qty")
    def onchange_get_unit_price(self):
        for record in self:
            record.price_unit = record.unit_rate

    @api.depends("order_id.pricelist_id", "company_id", "currency_id")
    def _compute_currency_usd_id(self):
        for record in self:
            record.currency_usd_id = (
                record.currency_id.id if record.currency_id else False
            )
            currency_id = self.env["res.currency"].search([("name", "=", "USD")])
            if currency_id:
                record.currency_usd_id = currency_id

    @api.depends("order_id.pricelist_id", "company_id")
    def _compute_main_currency_id(self):
        for line in self:
            line.main_currency_id = line.order_id.company_id.currency_id

    @api.depends("currency_id", "main_currency_id", "unit_rate")
    def compute_ex_rate(self):
        for rec in self:
            rec.ex_rate = 1
            rec.technical_rate = 1
            if rec.currency_id:
                rec.technical_rate = (
                    rec.currency_usd_id.rate_ids[0].rate
                    if rec.currency_usd_id.rate_ids
                    else 1.0
                )
                if rec.currency_id.id != rec.main_currency_id.id:
                    rec.ex_rate = (
                        rec.currency_id.rate_ids[0].inverse_company_rate
                        if rec.currency_id.rate_ids
                        else 1.0
                    )

    @api.depends("ex_rate", "unit_rate", "product_uom_qty")
    def _compute_tot_price(self):
        for rec in self:
            rec.main_curr = rec.ex_rate * rec.unit_rate * rec.product_uom_qty

    @api.depends("product_id", "product_uom", "product_uom_qty")
    def _compute_price_unit(self):
        for line in self:
            # check if there is already invoiced amount. if so, the price shouldn't change as it might have been
            # manually edited
            if line.qty_invoiced > 0 or (
                line.product_id.expense_policy == "cost" and line.is_expense
            ):
                continue
            if not line.product_uom or not line.product_id:
                line.price_unit = 0.0
            elif line.order_id.website_id:
                line.price_unit = line.product_id.uom_id._compute_price(
                    line.product_id.list_price, line.product_uom
                )
            else:
                line = line.with_company(line.company_id)
                price = line.unit_rate
                line.price_unit = (
                    line.product_id._get_tax_included_unit_price_from_price(
                        price,
                        product_taxes=line.product_id.taxes_id.filtered(
                            lambda tax: tax.company_id == line.env.company
                        ),
                        fiscal_position=line.order_id.fiscal_position_id,
                    )
                )

    def _get_displayed_unit_price(self):
        show_tax = self.order_id.website_id.show_line_subtotals_tax_selection
        tax_display = (
            "total_excluded" if show_tax == "tax_excluded" else "total_included"
        )

        return self.tax_id.compute_all(
            self.product_id.list_price,
            self.currency_id,
            1,
            self.product_id,
            self.order_partner_id,
        )[tax_display]

    @api.depends(
        "product_uom_qty", "discount", "price_unit", "tax_id", "unit_rate", "main_curr"
    )
    def _compute_amount(self):
        """
        Compute the amounts of the SO line in Odoo 18.
        """
        for line in self:
            if line.order_id.website_id:
                # Handle website-related pricing logic
                price_unit = line.product_id.list_price
                price_subtotal = 0
                is_fixed_charge = False
                total_fixed_charge = 0

                # Loop over the pricing charges
                for charge in line.product_id.product_tmpl_id.pricing_charge_ids:
                    if (
                        charge.product_id_2.product_variant_id.calculation_type
                        == "fixed_charge"
                    ):
                        price_unit -= charge.sale_price
                        total_fixed_charge += charge.sale_usd
                        is_fixed_charge = True

                # Compute price subtotal with fixed charges if applicable
                if is_fixed_charge:
                    line.price_subtotal = (
                        price_unit
                        * line.product_uom_qty
                        * (1 - (line.discount or 0.0) / 100.0)
                    )
                    line.price_subtotal += total_fixed_charge
                else:
                    line.price_subtotal = (
                        line.price_unit
                        * line.product_uom_qty
                        * (1 - (line.discount or 0.0) / 100.0)
                    )
            else:
                # Odoo 18 tax computation using _add_tax_details_in_base_line
                base_line = line._prepare_base_line_for_taxes_computation()
                self.env["account.tax"]._add_tax_details_in_base_line(
                    base_line, line.company_id
                )

                # Extract the untaxed and taxed amounts
                amount_untaxed = base_line["tax_details"]["total_excluded_currency"]
                amount_tax = (
                    base_line["tax_details"]["total_included_currency"] - amount_untaxed
                )
                print(
                    "amount_untaxed * line.technical_rate",
                    amount_untaxed * line.technical_rate,
                )
                print("amount_untaxed", amount_untaxed)
                # Update the line valuesunit_rate
                line.update(
                    {
                        "price_subtotal_main_curr": amount_untaxed * line.ex_rate,
                        "price_tax_main_curr": amount_tax,
                        "price_total_main_curr": (amount_untaxed * line.ex_rate)
                        + (amount_tax * line.ex_rate),
                        "price_subtotal": amount_untaxed,
                        "price_tax": amount_tax,
                        "price_total": (amount_untaxed + amount_tax),
                    }
                )

    # def _compute_amount(self):
    #     """
    #     Compute the amounts of the SO line.
    #     """
    #     for line in self:
    #         if line.order_id.website_id:
    #             price_unit = line.product_id.list_price
    #             price_subtotal = 0
    #             is_fixed_charge = False
    #             total_fixed_charge = 0
    #             for charge in line.product_id.product_tmpl_id.pricing_charge_ids:
    #                 if charge.product_id_2.product_variant_id.calculation_type == 'fixed_charge':
    #                     price_unit -= charge.sale_price
    #                     total_fixed_charge += charge.sale_usd
    #                     is_fixed_charge = True
    #             if is_fixed_charge:
    #                 line.price_subtotal = price_unit * line.product_uom_qty * (1 - (line.discount or 0.0) / 100.0)
    #                 line.price_subtotal += total_fixed_charge
    #             else:
    #                 line.price_subtotal = line.price_unit * line.product_uom_qty * (1 - (line.discount or 0.0) / 100.0)
    #         else:
    #             # main currency conversion
    #             tax_results = self.env['account.tax'].with_company(line.company_id)._compute_taxes([
    #                 line._convert_to_tax_base_line_dict_main_curr()
    #             ])
    #             totals = list(tax_results['totals'].values())[0]
    #             amount_untaxed = totals['amount_untaxed']
    #             amount_tax = totals['amount_tax']

    #             line.update({
    #                 'price_subtotal_main_curr': amount_untaxed,
    #                 'price_tax_main_curr': amount_tax,
    #                 'price_total_main_curr': amount_untaxed + amount_tax,
    #                 'price_subtotal': amount_untaxed * line.technical_rate,
    #                 'price_tax': amount_tax * line.technical_rate,
    #                 'price_total': (amount_untaxed + amount_tax) * line.technical_rate,
    #             })

    def _convert_to_tax_base_line_dict(self, **kwargs):
        """Convert the current record to a dictionary in order to use the generic taxes computation method
        defined on account.tax.

        :return: A python dictionary.
        """
        self.ensure_one()
        return self.env["account.tax"]._convert_to_tax_base_line_dict(
            self,
            partner=self.order_id.partner_id,
            currency=self.currency_id,
            product=self.product_id,
            taxes=self.tax_id,
            price_unit=self.price_subtotal / self.product_uom_qty or self.price_unit,
            quantity=self.product_uom_qty,
            discount=self.discount,
            price_subtotal=self.price_subtotal,
            **kwargs,
        )

    def _convert_to_tax_base_line_dict_main_curr(self, **kwargs):
        """Convert the current record to a dictionary in order to use the generic taxes computation method
        defined on account.tax.

        :return: A python dictionary.
        """
        self.ensure_one()
        return self.env["account.tax"]._convert_to_tax_base_line_dict(
            self,
            partner=self.order_id.partner_id,
            currency=self.main_currency_id,
            product=self.product_id,
            taxes=self.tax_id,
            price_unit=self.main_curr / self.product_uom_qty or self.unit_rate,
            quantity=self.product_uom_qty,
            discount=self.discount,
            price_subtotal=self.price_subtotal_main_curr,
            **kwargs,
        )
