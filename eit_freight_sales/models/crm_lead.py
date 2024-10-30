from odoo import models, fields, api, tools
from odoo.tools.translate import _
from datetime import datetime
import json
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from datetime import date


class ResPartner(models.Model):
    _inherit = 'res.partner'

    team_id = fields.Many2one('crm.team', string='Sales Team')


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def _default_date_deadline(self):
        return (datetime.today() + timedelta(weeks=2)).date()

    date_deadline = fields.Date('Expected Closing',
                                help="Estimate of the date on which the opportunity will be won.",
                                default=_default_date_deadline)
    opportunity_source = fields.Char(string="Opportunity Source", compute="compute_opportunity_source")
    transport_type_id = fields.Many2one('transport.type', string="Transport Type", store=True, tracking=True)
    transport_type_id_code = fields.Char(string="Transport Type Code", related='transport_type_id.code', store=True)
    is_air = fields.Boolean(string="Is Air", compute='_compute_is_air_ocean_or_inland')
    is_ocean_or_inland = fields.Boolean(string="Is Ocean or Inland", compute='_compute_is_air_ocean_or_inland')
    shipment_scope_id = fields.Many2one('shipment.scop', string="Shipment Scope", store=True)
    is_fcl_or_ftl = fields.Boolean(string="Is FCL or FTL", compute='_compute_is_air_ocean_or_inland')
    is_lcl_or_ltl = fields.Boolean(string="Is LCL or LTL", compute='_compute_is_air_ocean_or_inland')
    product_id_domain = fields.Char(compute="_compute_product_id_domain", readonly=True, store=False)
    name = fields.Char(
        'Opportunity', index='trigram', required=False,
        compute='_compute_name', readonly=True, store=True)
    partner_id = fields.Many2one(domain="[('partner_type_id.code', '=', 'CST'),('is_company', '=', True)]")
    equipment_type_id = fields.Many2one(comodel_name='shipment.scop', string='Equipment Type')
    additional_information = fields.Text(string='Additional Information')
    by_unit = fields.Boolean(string='By Unit')
    commodity_id = fields.Many2one(comodel_name='commodity.data', string='Commodity')
    commodity_group_id = fields.Many2one(comodel_name='commodity.group', string="Commodity Group")
    cargo_readiness_date = fields.Date(string='Cargo Readiness Date')
    container_lines_ids = fields.One2many('container.lines', 'crm_id',
                                          string='Container/s Type, Quantity and Weight')

    air_package_type_ids = fields.One2many(
        'crm.lead.air.package.type', 'lead_id', string="Package Types", store=True, )
    non_air_package_type_ids = fields.One2many(
        'crm.lead.non.air.package.type', 'lead_id', string="Package Types", store=True, )

    container_type_ids = fields.One2many('crm.lead.container.type', 'lead_id', string="Container Types", store=True)

    pol_id = fields.Many2one(comodel_name='port.cites', string="POL", store=True, tracking=True)
    pol_id_country_id = fields.Many2one(comodel_name='res.country', string="POL Country", related='pol_id.country_id')
    pod_id = fields.Many2one(comodel_name='port.cites', string="POD", store=True, tracking=True)
    pod_id_country_id = fields.Many2one(comodel_name='res.country', string="POD Country", related='pod_id.country_id')
    pol_pod_domain = fields.Char(string="POL Domain", compute='_compute_pol_pod_domain')
    commodity_equip = fields.Selection([
        ('dry', 'Dry'),
        ('reefer', 'Reefer'),
        ('imo', 'IMO')
    ], string="Commodity Equip", store=True)

    temperature = fields.Float(string="Temperature", store=True)
    un_number = fields.Integer(string="UN Number", store=True)
    attachment = fields.Binary(string="Attachment", attachment=True, help="Upload your MSDS")
    incoterms_id = fields.Many2one('account.incoterms', string="Incoterms")
    pickup = fields.Boolean(string="Pickup Address", related="incoterms_id.pickup")
    delivery = fields.Boolean(string="Delivery Address", related="incoterms_id.delivery")
    transit_time_duration = fields.Integer(string="Transit Time", store=True)
    free_time_duration = fields.Integer(string="Free Time", store=True)
    target_rate = fields.Monetary(string="Target Rate", store=True, tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", tracking=True)
    preferred_line_id = fields.Many2one('res.partner', string="Preferred Line",
                                        domain="[('partner_type_id.name', '=', 'Shipping Line'), ('is_company', '=', True)]",
                                        store=True,
                                        )
    service_needed_ids = fields.Many2many('service.scope', string="Service Required", store=True, tracking=True)
    invoice_amount_for_insurance = fields.Monetary(string="Invoice Amount for Insurance", store=True)
    opp_id = fields.Char(
        string='OPP ID', index=True, readonly=True, store=True)
    pickup_address = fields.Char(string="Pickup Address")
    delivery_address = fields.Char(string="Delivery Address")
    is_from_website = fields.Boolean(string="Is From Web", default=False)
    order_ids = fields.One2many('sale.order', 'opportunity_id', string='Bookings')
    carrier_route_id = fields.Many2one('carrier.route', string='Carrier Route')

    def _get_carrier_route_id(self):
        for record in self:
            carrier_route_id = False
            if record.transport_type_id.code == 'SEA':
                carrier_route_id = self.env['carrier.route'].search([('pol_id', '=', record.pol_id.id),
                                                                     ('pod_id', '=', record.pod_id.id),
                                                                     ('route_type', '=', 'sea'),
                                                                     ('active', '=', True)], limit=1)
            elif record.transport_type_id.code == 'AIR':
                carrier_route_id = self.env['carrier.route'].search([('pol_id', '=', record.pol_id.id),
                                                                     ('pod_id', '=', record.pod_id.id),
                                                                     ('route_type', '=', 'air'),
                                                                     ('active', '=', True)], limit=1)
            if not carrier_route_id:
                if record.pol_id and record.pod_id and record.transport_type_id:
                    carrier_route_id = self.env['carrier.route'].create({
                        'pol_id': record.pol_id.id,
                        'pod_id': record.pod_id.id,
                        'route_type': 'air' if record.transport_type_id.code == 'AIR' else 'sea',
                        'active': True
                    })
            return carrier_route_id

    def action_open_carrier_route(self):
        return {
            'name': 'Carrier Route',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'carrier.route',
            'res_id': self.carrier_route_id.id,
        }

    @api.onchange('transport_type_id')
    def _compute_pol_pod_domain(self):
        for record in self:
            if record.transport_type_id.code == 'SEA':
                record.pol_pod_domain = "[('type_id.code', '=', 'SEA')]"
            elif record.transport_type_id.code == 'AIR':
                record.pol_pod_domain = "[('type_id.code', '=', 'AIR')]"
            else:
                record.pol_pod_domain = "[]"

    @api.depends('partner_id')
    def _compute_name(self):
        for lead in self:
            if not lead.name and lead.type == 'opportunity':
                lead.name = 'OPP'

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        """ Extract data from lead to create a partner.

        :param name : furtur name of the partner
        :param is_company : True if the partner is a company
        :param parent_id : id of the parent partner (False if no parent)

        :return: dictionary of values to give at res_partner.create()
        """
        email_parts = tools.email_split(self.email_from)
        res = {
            'name': partner_name,
            'user_id': self.env.context.get('default_user_id') or self.user_id.id,
            'comment': self.description,
            'team_id': self.team_id.id,
            'parent_id': parent_id,
            'phone': self.phone,
            'mobile': self.mobile,
            'email': email_parts[0] if email_parts else False,
            'title': self.title.id,
            'function': self.function,
            'street': self.street,
            'street2': self.street2,
            'zip': self.zip,
            'city': self.city,
            'country_id': self.country_id.id,
            'state_id': self.state_id.id,
            'website': self.website,
            'is_company': is_company,
            'type': 'contact',
            'partner_type_id': self.env['partner.type'].search([('code', '=', 'CST')])
        }
        if self.lang_id.active:
            res['lang'] = self.lang_id.code
        return res

    def compute_opportunity_source(self):
        for rec in self:
            if rec.is_from_website:
                rec.opportunity_source = "Website"
            elif rec.type == "opportunity":
                if not rec.opportunity_source:
                    rec.opportunity_source = "OPP"
            elif rec.type == "lead":
                if not rec.opportunity_source:
                    rec.opportunity_source = "Lead"

    # def redirect_lead_opportunity_view(self):
    #     self.ensure_one()
    #     action = super(CrmLead, self).redirect_lead_opportunity_view()
    #     print('actionnnn', action)
    #     action['context'].update({'default_opportunity_source': 'Lead'})
    #     print('actttt', action)
    #     return action

    @api.depends('transport_type_id')
    def _compute_product_id_domain(self):
        for rec in self:
            if rec.transport_type_id:
                if rec.transport_type_id.id == 2:
                    rec.product_id_domain = json.dumps(
                        [('type', '=', 'sea')]
                    )

                if self.transport_type_id.id == 3:
                    rec.product_id_domain = json.dumps(
                        [('type', '=', 'inland')]
                    )
                if self.transport_type_id.id == 1:
                    rec.product_id_domain = ""
            else:
                rec.product_id_domain = ""

    @api.depends('transport_type_id', 'shipment_scope_id')
    def _compute_is_air_ocean_or_inland(self):
        for record in self:
            record.is_air = record.transport_type_id.id == 1
            record.is_ocean_or_inland = record.transport_type_id.id in [2, 3]
            record.is_fcl_or_ftl = record.is_ocean_or_inland and record.shipment_scope_id.code in ['FCL', 'FTL']
            record.is_lcl_or_ltl = record.is_ocean_or_inland and record.shipment_scope_id.code in ['LCL', 'LTL']
            record.by_unit = record.is_air or record.is_lcl_or_ltl

    @api.onchange('pol_id', 'pod_id')
    def onchange_pod_id(self):
        if self.pol_id and self.pod_id:
            if self.pol_id.id == self.pod_id.id:
                raise UserError(
                    _("Please select another port."
                      "You can't choose the same port at two different locations."
                      "If you have internal transport at the same port, You can add it to the “Service” tab below after choosing the true destinations and saving."))

    @api.model
    def create(self, vals):
        if vals.get('type') == 'opportunity':
            vals['name'] = self._generate_opp_id()
        else:
            contact_name = ', ' + vals.get('contact_name') if vals.get('contact_name') else ''
            partner_name = vals.get('partner_name') if vals.get('partner_name') else ''
            contact_name = contact_name if vals.get('contact_name') else (
                ', ' + self.contact_name if self.contact_name else '')
            vals['name'] = partner_name + contact_name
        if not vals.get('carrier_route_id'):
            vals['carrier_route_id'] = self._get_carrier_route_id()
        return super(CrmLead, self).create(vals)

    def write(self, vals):
        if vals.get('type') == 'opportunity':
            vals['name'] = self._generate_opp_id()
        elif vals.get('type') == 'lead':
            contact_name = ', ' + vals.get('contact_name') if vals.get('contact_name') else ''
            partner_name = vals.get('partner_name') if vals.get(
                'partner_name') else self.partner_name if self.partner_name else ''
            contact_name = contact_name if vals.get('contact_name') else (
                ', ' + self.contact_name if self.contact_name else '')
            vals['name'] = partner_name + contact_name
        res = super(CrmLead, self).write(vals)
        if self.transport_type_id and not vals.get('carrier_route_id') and not self.carrier_route_id:
            self.carrier_route_id = self._get_carrier_route_id()
        return res

    @api.model
    def _generate_opp_id(self):
        current_year = datetime.now().year
        year_suffix = str(current_year)[-2:]
        seq = self.env['ir.sequence'].next_by_code('crm.lead.opp.id') or '0000'
        return f"OPP{year_suffix}/{seq}"
