from datetime import timedelta

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

SALE_ORDER_STATE = [
    ("draft", "Quotation"),
    ("sent", "Quotation Sent"),
    ("sale", "Booking"),
    ("cancel", "Cancelled"),
]


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)
        if self._context.get("default_opportunity_id"):
            crm_lead = self.env["crm.lead"].browse(
                self._context["default_opportunity_id"]
            )
            res.update(
                {
                    "pol": crm_lead.pol_id.id,
                    "pod": crm_lead.pod_id.id,
                    "commodity": crm_lead.commodity_id.id,
                    "commodity_equip": crm_lead.commodity_equip,
                    "incoterms": crm_lead.incoterms_id.id,
                    "shipment_scope_id": crm_lead.shipment_scope_id.id,
                    "container_type": crm_lead.container_type_ids.container_type_id.id,
                    "transport_type_id": crm_lead.transport_type_id.id,
                }
            )
        return res

    transport_type_id = fields.Many2one(
        "transport.type", string="Transport Type", tracking=True
    )
    shipment_scope_id = fields.Many2one(
        "shipment.scop", string="Shipment Scope", tracking=True
    )
    is_ocean_or_inland = fields.Boolean(
        string="Is Ocean or Inland", compute="_compute_is_ocean_or_inland"
    )
    is_fcl_or_ftl = fields.Boolean(
        string="Is FCL or FTL", compute="_compute_is_fcl_or_ftl"
    )
    is_lcl_or_ltl = fields.Boolean(
        string="Is LCL or LTL", compute="_compute_is_lcl_or_ltl"
    )
    container_type = fields.Many2one("container.type", string="Container Type")
    is_air = fields.Boolean(string="Is Air", compute="_compute_is_air")
    company_count = fields.Integer(
        default=lambda self: self.env["res.company"].search_count([])
    )
    rate_currency = fields.One2many(
        "total.rate.currency", "sale_cost", string="Rate Per Currency"
    )
    conndition_id = fields.Many2one("freight.conditions", string="Terms & Conditions")
    condition_text = fields.Text(string="Terms & Conditions")
    vessel_line_ids = fields.One2many(
        "sale.vessel.line", "sale_vessel_id", string="Vessels"
    )
    plane_line_ids = fields.One2many(
        "sale.plane.line", "sale_plane_id", string="Planes"
    )
    parties_line_ids = fields.One2many(
        "sale.parties.line", "sale_parties_id", string="Parties"
    )
    package_type = fields.Many2one(
        "package.type", string="Package Type", domain="[('tag_type_ids', 'in', [1])]"
    )
    package_types = fields.Many2one(
        "package.type", string="Package Types", domain="[('tag_type_ids', 'in', [2])]"
    )

    pol = fields.Many2one("port.cites", string="POL", tracking=True,
                          domain="['transport_type_id.code','not in', ['sea', 'are', 'land']")
    pod = fields.Many2one("port.cites", string="POD", tracking=True)
    pol_pod_domain = fields.Char(string="POL Domain", compute="_compute_pol_pod_domain")
    transit_time_duration = fields.Integer(string="Transit Time Duration")
    free_time_duration = fields.Integer(string="Free Time Duration")
    is_ocean = fields.Boolean(string="Is Ocean", compute="_compute_is_ocean")
    is_inland = fields.Boolean(string="IS Inland", compute="_compute_is_inland")
    pickup_address = fields.Char(string="Pickup Address")
    pickup_address2 = fields.Char(string="Delivery Address")

    incoterms = fields.Many2one(
        "account.incoterms",
        string="Incoterm",
        help="International Commercial Terms are a series of predefined commercial terms used in international transactions.",
    )
    pickup = fields.Boolean(related="incoterms.pickup")
    delivery = fields.Boolean(related="incoterms.delivery")

    charge_type = fields.Many2one("product.product", string="Charge Type")
    cost_price = fields.Float(string="Cost Price")
    currency_id = fields.Many2one("res.currency", string="Currency")
    exchange_rate = fields.Float(
        string="Exchange Rate", compute="_compute_exchange_rate", store=True
    )
    total_cost_usd = fields.Float(
        string="Total Cost in USD", compute="_compute_total_cost_usd", store=True
    )
    partner_id = fields.Many2one(
        domain="[('partner_type_id.code', '=', 'CST')),('is_company', '=', True)]"
    )
    shipment_domain = fields.Binary(
        string="shipment domain", compute="_compute_pol_domain"
    )
    shipping_line = fields.Many2one(
        "res.partner",
        string="Shipping Line",
        domain="[('partner_type_id.name', '=', 'Shipping Line'), ('is_company', '=', True)]",
    )
    air_line = fields.Many2one(
        "res.partner",
        string="Air Line",
        domain="[('partner_type_id.name', '=', 'Air Line'), ('is_company', '=', True)]",
    )
    trucker = fields.Many2one(
        "res.partner",
        string="Trucker",
        domain="[('partner_type_id.name', '=', 'Trucker'), ('is_company', '=', True)]",
    )

    commodity = fields.Many2one("commodity.data", string="Commodity")
    commodity_group_id = fields.Many2one(
        comodel_name="commodity.group", string="Commodity Group"
    )

    commodity_equip = fields.Selection(
        [
            ("dry", "Dry"),
            ("reefer", "Reefer"),
            ("imo", "IMO"),
        ],
        string="Commodity Equip",
    )
    state = fields.Selection(
        selection=SALE_ORDER_STATE,
        string="Status",
        readonly=True,
        copy=False,
        index=True,
        tracking=3,
        default="draft",
    )

    charges_ids = fields.One2many("sale.charges", "order_id")
    project_task_id = fields.Many2one(
        comodel_name="project.task", string="Project Task"
    )
    website_id = fields.Many2one(comodel_name="website", string="Website")
    service_scope = fields.Many2many(
        comodel_name="service.scope", string="Services", tracking=True
    )
    validity_date = fields.Date(
        string="Expiration",
        compute="_compute_validity_date",
        store=True,
        readonly=False,
        copy=False,
        precompute=True,
        tracking=3,
    )
    commodity_equipment = fields.Selection(
        [("Dry", "Dry"), ("IMO", "IMO"), ("Reefer", "Reefer")],
        string="Commodity Equip.",
        help="Select the type of commodity equipment",
    )
    un_number = fields.Char(string="UN Number", help="Enter the UN Number for IMO")
    msds = fields.Binary(string="MSDS", help="Upload the MSDS file for IMO")
    temperature = fields.Float(
        string="Temperature", help="Enter the temperature for Reefer"
    )
    bill_leading_type = fields.Many2one(
        "bill.leading.type",
        string="Bill of Lading Type",
        help="Select the Bill of Lading Type",
    )
    bill_of_lading_collection = fields.Selection(
        [("prepaid", "Prepaid"), ("collect", "Collect")],
        string="Bill of Lading Collection",
        default="prepaid",
        help="Select how the bill of lading is collected",
    )
    cargo_currency_id = fields.Many2one(
        comodel_name="res.currency", string="Cargo Currency"
    )
    cargo_value = fields.Monetary(
        string="Cargo Value",
        help="Enter the cargo value",
        currency_field="cargo_currency_id",
    )
    clearence_type = fields.Many2one(
        "clearence.type", string="Direction", help="Select the clearance direction"
    )
    booking_no = fields.Text(string="Vendor Booking No.", help="Enter the booking number")
    booking_instructions = fields.Text(
        string="B/L Instructions.", help="Enter special booking instructions"
    )
    show_acid_details = fields.Boolean(string="Show ACID Details", default=False)
    acid_no = fields.Char(string="ACID No", size=19)
    acid_importer_tax_id = fields.Char(string="Importer Tax ID")
    acid_issuance_date = fields.Date(string="ACID Issuance Date")
    foreign_exporter_id = fields.Char(string="Foreign Exporter ID")
    exporter_registry_type = fields.Selection(
        selection=[("reg", "Registration Number"), ("vat", "VAT Number")],
        string="Registration Type",
    )
    foreign_exporter_country_id = fields.Many2one(
        comodel_name="res.country", string="Foreign Exporter Country"
    )
    foreign_exporter_country_id_code = fields.Char(
        string="Country Code", related="foreign_exporter_country_id.code"
    )
    acid_expiry_date = fields.Date(string="ACID Expiry Date")
    date_order = fields.Datetime(
        string="Booking Date",
        required=True,
        copy=False,
        help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.",
        default=fields.Datetime.now,
    )

    pick_up = fields.Date(string='Pick-Up Date')
    type_of_package = fields.Many2one('package.type', string='Type Of Package.')
    no_of_package = fields.Integer(string='No Of Packing')
    cbm = fields.Text(string='CBM')
    gross_weight = fields.Float(string='Gross Weight')
    vessel_type_id = fields.Many2one('carrier.route')
    vessel_name = fields.Many2one('freight.vessels', string='Vessel Name')
    voyage_no = fields.Char(string='Voyage No.')
    plane_name = fields.Many2one('freight.airplane', string='Plane Name.')
    flight_no = fields.Char(string='Flight No.')
    arrival_eta = fields.Date(string='Arrival (ETA)')
    departure_etd = fields.Date(string='Departure (ETD)')
    origin = fields.Many2one('res.country', string='Origin')
    net_weight = fields.Integer(string='Net Weight.')
    tare_weight = fields.Integer(string='Tare Weight', domain="['shipment_scope_id.code', '!=', 'FCL']")
    vgm = fields.Integer(string='VGM', domain="['shipment_scope_id.code', '!=', 'FCL']")
    container_quantity = fields.Char(string='Container / Quantity', placeholder="3*40HQ + 2*20DC",
                                     domain="[('shipment_scope_id.code', 'not in', ['FCL', 'FTL']")


    @api.model
    def cancel_expired_orders(self):
        """Cancel sale orders that are expired and in draft or sent state."""
        today = fields.Date.today()
        expired_orders = self.search(
            [("state", "in", ["draft", "sent"]), ("validity_date", "<", today)]
        )
        for order in expired_orders:
            order.action_cancel()
        return True

    def _validate_order(self):
        if not self.pol:
            raise ValidationError("Please fill POL to confirm the order")

        if not self.pod:
            raise ValidationError("Please fill POD to confirm the order")

        if not self.transport_type_id:
            raise ValidationError("Please fill Transport Type to confirm the order")

        if not self.service_scope:
            raise ValidationError("Please fill Services to confirm the order")

        if self.is_expired:
            raise ValidationError("Order is expired, cannot confirm")

        if not self.order_line:
            raise ValidationError(
                "Please add at least one Order Line to confirm the order"
            )

    def action_confirm(self):
        self._validate_order()
        res = super(SaleOrder, self).action_confirm()
        if self.opportunity_id:
            self.opportunity_id.action_set_won()
        return res

    def action_view_opportunity(self):
        action = self.env.ref("crm.crm_lead_action_pipeline").read()[0]

        # Modify the view mode to include both 'kanban' and 'form'
        action["view_mode"] = "kanban,form"

        # Modify the domain to filter based on crm_lead_ids
        action["domain"] = [("id", "in", self.opportunity_id.ids)]

        # Add custom context, including default values for 'pol_id' and 'pod_id'
        action["context"] = {
            "default_pol_id": (
                self.pol.id if self.pol else False
            ),  # Replace with your field
            "default_pod_id": (
                self.pod.id if self.pod else False
            ),  # Replace with your field
            "default_type": "opportunity",
            **self.env.context,  # Retain any existing context values
        }

        # Specify the custom form view (eit_freight_sales.view_crm_lead_form_inherit)
        action["views"] = [
            (False, "kanban"),  # Keep kanban as the fallback view
            (self.env.ref("eit_freight_sales.view_crm_lead_form_inherit").id, "form"),
        ]

        return action

    def action_quotation_send(self):
        """Opens a wizard to compose an email, with relevant mail template loaded by default"""
        self.ensure_one()
        self._validate_order()
        self.order_line._validate_analytic_distribution()
        lang = self.env.context.get("lang")
        mail_template = self._find_mail_template()
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            "default_model": "sale.order",
            "default_res_ids": self.ids,
            "default_template_id": mail_template.id if mail_template else None,
            "default_composition_mode": "comment",
            "mark_so_as_sent": True,
            "default_email_layout_xmlid": "mail.mail_notification_layout_with_responsible_signature",
            "proforma": self.env.context.get("proforma", False),
            "force_email": True,
            "model_description": self.with_context(lang=lang).type_name,
        }
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
            "context": ctx,
        }

    @api.depends("partner_id", "order_line", "pol", "pod", "validity_date")
    def _compute_validity_date(self):
        today = fields.Date.context_today(self)
        for order in self:
            # days = order.company_id.quotation_validity_days
            days = 15
            if days > 0:
                order.validity_date = today + timedelta(days)
            else:
                order.validity_date = False

    def _compute_is_expired(self):
        today = fields.Date.today()
        for order in self:
            order.is_expired = (
                order.state in ("draft", "sent")
                and order.validity_date
                and order.validity_date < today
            )
            if order.is_expired and order.state != "sale":
                order.state = "cancel"

    @api.onchange("transport_type_id")
    def _compute_pol_pod_domain(self):
        for record in self:
            if record.transport_type_id.code == "SEA":
                record.pol_pod_domain = "[('type_id.code', '=', 'SEA')]"
            elif record.transport_type_id.code == "AIR":
                record.pol_pod_domain = "[('type_id.code', '=', 'AIR')]"
            elif record.transport_type_id.code == "LND":
                record.pol_pod_domain = "[('type_id.code', 'in', ['AIR','SEA','LND'])]"
            else:
                record.pol_pod_domain = (
                    "[('type_id.code', '=', 'AIR'), ('type_id.code', '=', 'SEA')]"
                )

    @api.onchange("acid_issuance_date")
    def _onchange_acid_issuance_date(self):
        if self.acid_issuance_date:
            self.acid_expiry_date = self.acid_issuance_date + relativedelta(months=6)

    @api.constrains("acid_no")
    def _check_acid_no(self):
        for record in self:
            if record.acid_no and (
                not record.acid_no.isdigit() or len(record.acid_no) > 19
            ):
                raise ValidationError(
                    "ACID No must contain only digits and be no longer than 19 digits."
                )

    @api.onchange("pod")
    def onchange_port_id_pod(self):
        for rec in self:
            rec.show_acid_details = False
            if (
                self.pod
                and self.pod.country_id
                and (
                    self.pod.country_id.code.lower() == "eg"
                    or self.pod.country_id.name.lower() == "egypt"
                )
            ):
                rec.show_acid_details = True

    @api.onchange("commodity_equipment")
    def _onchange_commodity_equipment(self):
        if self.commodity_equipment == "IMO":
            self.un_number = ""
            self.msds = False
        else:
            self.un_number = False
            self.msds = False

        if self.commodity_equipment == "Reefer":
            self.temperature = 0.0
        else:
            self.temperature = False

    @api.depends("pricelist_id", "company_id")
    def _compute_currency_id(self):
        for order in self:
            currency_usd_id = (
                self.env["res.currency"].search([("name", "=", "USD")], limit=1).id
            )
            # order.currency_id = order.pricelist_id.currency_id or order.company_id.currency_id
            order.currency_id = currency_usd_id or order.company_id.currency_id

    @api.onchange("conndition_id")
    def _onchange_conndition_ids(self):
        if self.conndition_id:
            self.condition_text = self.conndition_id.Terms

    @api.onchange("order_line")
    def compute_rate_currency(self):
        for rec in self:
            if rec.order_line:
                sale_list = [(5, 0, 0)]
                currency = rec.order_line.mapped("currency_id")
                for cur in currency:
                    amount = 0
                    for charg in rec.order_line:
                        if cur.id == charg.currency_id.id:
                            amount += charg.unit_rate * charg.product_uom_qty
                            print("am", amount)
                    val = {"currency_id": cur, "amount": amount}
                    sale_list.append((0, 0, val))
                rec.update({"rate_currency": sale_list})
            else:
                rec.rate_currency = False

    @api.depends("transport_type_id")
    def _compute_is_air(self):
        for record in self:
            record.is_air = (
                record.transport_type_id.name in ["Air"]
                if record.transport_type_id
                else False
            )

    @api.depends("transport_type_id")
    def _compute_is_ocean_or_inland(self):
        for record in self:
            record.is_ocean_or_inland = (
                record.transport_type_id.name in ["Sea", "Land"]
                if record.transport_type_id
                else False
            )

    @api.depends("shipment_scope_id", "is_ocean_or_inland")
    def _compute_is_fcl_or_ftl(self):
        for record in self:
            if record.shipment_scope_id and record.is_ocean_or_inland:
                record.is_fcl_or_ftl = record.shipment_scope_id.code in ["FCL", "FTL"]
            else:
                record.is_fcl_or_ftl = False

    @api.depends("shipment_scope_id", "is_ocean_or_inland")
    def _compute_is_lcl_or_ltl(self):
        for record in self:
            if record.shipment_scope_id and record.is_ocean_or_inland:
                record.is_lcl_or_ltl = record.shipment_scope_id.code in ["LCL", "LTL"]
            else:
                record.is_lcl_or_ltl = False

    @api.onchange("pol", "pod")
    def onchange_pod_id(self):
        if self.pol and self.pod:
            if self.pol.id == self.pod.id:
                raise UserError(
                    _(
                        "Please select another port."
                        "You can't choose the same port at two different locations."
                    )
                )

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        res.name = vals["name"].replace("S", "Q")
        return res

    def write(self, vals):
        if "website_id" in vals or self.website_id:
            vals["only_services"] = True
            currency_usd_id = self.env["res.currency"].search(
                [("name", "=", "USD")], limit=1
            )
            if currency_usd_id:
                vals["currency_id"] = currency_usd_id.id
        for record in self:
            old_validity_date = record.validity_date

        res = super(SaleOrder, self).write(vals)

        # Check if validity_date was changed
        for record in self:
            new_validity_date = record.validity_date
            if old_validity_date != new_validity_date:
                # Manually post a message in the chatter about the change
                record.message_post(
                    body=f"Expiration date changed from {old_validity_date} to {new_validity_date}."
                )

        if "parties_line_ids" in vals:
            for partner_line_vals in self.parties_line_ids:
                if partner_line_vals.partner_type_id.code == "CNEE":
                    self.acid_importer_tax_id = partner_line_vals.partner_id.vat
        return res

    @api.depends("transport_type_id")
    def _compute_is_ocean(self):
        for record in self:
            record.is_ocean = (
                record.transport_type_id.name == "Sea"
                if record.transport_type_id
                else False
            )

    @api.depends("transport_type_id")
    def _compute_is_inland(self):
        for record in self:
            record.is_inland = (
                record.transport_type_id.name == "In-land"
                if record.transport_type_id
                else False
            )

    @api.depends("currency_id")
    def _compute_exchange_rate(self):
        for record in self:
            record.exchange_rate = record.currency_id.rate

    @api.depends("charge_type.lst_price", "exchange_rate")
    def _compute_total_cost_usd(self):
        for record in self:
            record.total_cost_usd = record.charge_type.lst_price * record.exchange_rate

    @api.depends("transport_type_id")
    def _compute_pol_domain(self):
        for record in self:
            if record.transport_type_id.name == "Sea":
                record.shipment_domain = [("type", "=", "sea")]

            elif record.transport_type_id.name == "Land":
                record.shipment_domain = [("type", "=", "inland")]

            else:
                record.shipment_domain = [("id", "in", [])]

    def _prepare_order_line_update_values(
        self, order_line, quantity, linked_line_id=False, **kwargs
    ):
        values = super(SaleOrder, self)._prepare_order_line_update_values(
            order_line, quantity, linked_line_id, **kwargs
        )
        currency_usd_id = self.env["res.currency"].search(
            [("name", "=", "USD")], limit=1
        )
        values["price_unit"] = order_line.product_id.list_price
        values["currency_id"] = currency_usd_id.id
        return values

    @api.depends(
        "order_line.price_subtotal", "order_line.price_tax", "order_line.price_total"
    )
    def _compute_amounts(self):
        """Compute the total amounts of the SO."""
        for order in self:
            order_lines = order.order_line.filtered(lambda x: not x.display_type)

            if order.company_id.tax_calculation_rounding_method == "round_globally":
                tax_results = self.env["account.tax"]._compute_taxes(
                    [line._convert_to_tax_base_line_dict() for line in order_lines]
                )
                totals = tax_results["totals"]
                amount_untaxed = totals.get(order.currency_id, {}).get(
                    "amount_untaxed", 0.0
                )
                amount_tax = totals.get(order.currency_id, {}).get("amount_tax", 0.0)
            else:
                amount_untaxed = sum(order_lines.mapped("price_subtotal"))
                amount_tax = sum(order_lines.mapped("price_tax"))
            order.amount_untaxed = amount_untaxed
            order.amount_tax = amount_tax
            order.amount_total = order.amount_untaxed + order.amount_tax
