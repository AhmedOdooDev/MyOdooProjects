# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, _, models, api
from odoo.exceptions import ValidationError
from datetime import date


class CarrierRoute(models.Model):
    _name = "carrier.route"
    _description = 'Carrier Routes'
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', default='New', readonly=True, copy=False)
    pol_id = fields.Many2one('port.cites', string='POL', required=True, tracking=True)
    pol_country_id = fields.Many2one('res.country', string='POL Country', related='pol_id.country_id')
    pol_ocean_id = fields.Many2one(comodel_name='ocean.data', string='POL Ocean', related='pol_id.ocean_id')
    pol_country_group_id = fields.Many2one(comodel_name='res.country.group', string='POL Country Group',
                                           related='pol_id.country_group_id')
    pod_id = fields.Many2one('port.cites', string='POD', required=True, tracking=True)
    pod_country_id = fields.Many2one('res.country', string='POD Country', related='pod_id.country_id')
    pod_ocean_id = fields.Many2one(comodel_name='ocean.data', string='POD Ocean', related='pod_id.ocean_id')
    pod_country_group_id = fields.Many2one(comodel_name='res.country.group', string='POD Country Group',
                                           related='pod_id.country_group_id')
    pol_pod_domain = fields.Char(string="POL Domain", compute='_compute_pol_pod_domain')
    route_type = fields.Selection([
        ('none', ' '),
        ('air', 'Air'),
        ('sea', 'Sea')
    ], string='Route Type', required=True, tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    carrier_ids = fields.Many2many('res.partner', string='Carriers', tracking=True)
    carrier_ids_domain = fields.Char(string="Carriers Domain", compute='_compute_carrier_ids_domain')
    notes = fields.Text(string='Notes')
    equipment = fields.Selection([('dry', 'Dry'), ('reefer', 'Reefer'), ('imo', 'IMO'), ], string='Equipment')
    partner_id = fields.Many2one('res.partner', string="Partner")
    last_update = fields.Datetime(string='Last Updated On', compute='_compute_last_update', store=True)
    carrier_count = fields.Integer(string='Carrier Count', compute='_compute_carrier_count', store=True)
    terminal_ids = fields.One2many('terminal.port', compute='_compute_terminal_count', string="Terminals")
    warehouse_ids = fields.One2many('terminal.port', compute='_compute_warehouse_count', string="Warehouses")
    terminal_count = fields.Integer(string="Terminals", compute="_compute_terminal_count")
    warehouse_count = fields.Integer(string="Warehouses", compute="_compute_warehouse_count")
    ocean_count = fields.Integer(string="Oceans", compute="_compute_ocean_count")
    country_group_count = fields.Integer(string="Country Groups", compute="_compute_country_group_count")

    @api.depends('pol_id', 'pod_id')
    def _compute_terminal_count(self):
        for record in self:
            terminal_count = 0
            terminal_ids = []  # Collect terminal IDs as a list
            if record.pol_id and record.pod_id:
                pol_terminals = self.env['terminal.port'].search(
                    [('port_city_id', '=', record.pol_id.id), ('terminal', '=', True)])

                pod_terminals = self.env['terminal.port'].search(
                    [('port_city_id', '=', record.pod_id.id), ('terminal', '=', True)])

                # Combine both POL and POD terminal IDs
                terminal_ids = list(set(pol_terminals.ids + pod_terminals.ids))  # Ensure no duplicates and convert to list
                terminal_count = len(terminal_ids)

            record.terminal_count = terminal_count or False
            record.terminal_ids = terminal_ids or False  # Assign the list of terminal IDs
    # @api.depends('pol_id', 'pod_id')
    # def _compute_terminal_count(self):
    #     for record in self:
    #         terminal_count = 0
    #         terminal_ids = set()  # Collect terminal IDs
    #         if record.pol_id and record.pod_id:
    #             pol_terminals = self.env['terminal.port'].search(
    #                 [('port_city_id', '=', record.pol_id.id), ('terminal', '=', True)])

    #             pod_terminals = self.env['terminal.port'].search(
    #                 [('port_city_id', '=', record.pod_id.id), ('terminal', '=', True)])

    #             # Combine both POL and POD terminal IDs
    #             terminal_ids = pol_terminals.ids + pod_terminals.ids
    #             terminal_count = len(terminal_ids)
    #         record.terminal_count = terminal_count
    #         record.terminal_ids = terminal_ids  # Store terminal IDs for action_view_terminals

    # @api.depends('pol_id', 'pod_id')
    # def _compute_warehouse_count(self):
    #     for record in self:
    #         warehouse_count = 0
    #         warehouse_ids = []  # Collect warehouse IDs as a list
    #         if record.pol_id and record.pod_id:
    #             pol_warehouses = self.env['terminal.port'].search(
    #                 [('port_city_id', '=', record.pol_id.id), ('warehouse', '=', True)])
    #             pod_warehouses = self.env['terminal.port'].search(
    #                 [('port_city_id', '=', record.pod_id.id), ('warehouse', '=', True)])

    #             # Combine both POL and POD warehouse IDs
    #             warehouse_ids = list(set(pol_warehouses.ids + pod_warehouses.ids))  # Remove duplicates and convert to list
    #             warehouse_count = len(warehouse_ids)

    #         record.warehouse_count = warehouse_count
    #         record.warehouse_ids = warehouse_ids  # Store warehouse IDs as a list

    @api.depends('pol_id', 'pod_id')
    def _compute_warehouse_count(self):
        for record in self:
            warehouse_ids = self.env['terminal.port']  # Initialize an empty recordset
            if record.pol_id and record.pod_id:
                # Search for warehouses related to both POL and POD
                pol_warehouses = self.env['terminal.port'].search(
                    [('port_city_id', '=', record.pol_id.id), ('warehouse', '=', True)]
                )
                pod_warehouses = self.env['terminal.port'].search(
                    [('port_city_id', '=', record.pod_id.id), ('warehouse', '=', True)]
                )
                # Combine the two recordsets using the '|' operator
                warehouse_ids = pol_warehouses | pod_warehouses

            record.warehouse_count = len(warehouse_ids)  # Set the count of warehouse records
            record.warehouse_ids = warehouse_ids  # Assign the recordset to warehouse_ids
    # @api.depends('pol_id', 'pod_id')
    # def _compute_warehouse_count(self):
    #     for record in self:
    #         warehouse_count = 0
    #         warehouse_ids = set()  # Collect warehouse IDs
    #         if record.pol_id and record.pod_id:
    #             pol_warehouses = self.env['terminal.port'].search(
    #                 [('port_city_id', '=', record.pol_id.id), ('warehouse', '=', True)])
    #             pod_warehouses = self.env['terminal.port'].search(
    #                 [('port_city_id', '=', record.pod_id.id), ('warehouse', '=', True)])

    #             # Combine both POL and POD warehouse IDs
    #             warehouse_ids = pol_warehouses.ids + pod_warehouses.ids
    #             warehouse_count = len(warehouse_ids)
    #         record.warehouse_count = warehouse_count
    #         record.warehouse_ids = warehouse_ids  # Store warehouse IDs for action_view_warehouses

    @api.depends('pol_id', 'pod_id')
    def _compute_ocean_count(self):
        for record in self:
            ocean_count_ids = set()  # Use a set to collect distinct IDs
            if record.pol_ocean_id:
                ocean_count_ids.add(record.pol_ocean_id.id)  # Add the single ID, not a list
            if record.pod_ocean_id:
                ocean_count_ids.add(record.pod_ocean_id.id)  # Add the single ID, not a list
            record.ocean_count = len(ocean_count_ids)  # Count the distinct IDs

    @api.depends('pol_id', 'pod_id')
    def _compute_country_group_count(self):
        for record in self:
            country_group_ids = set()  # Use a set to collect distinct IDs
            if record.pol_country_group_id:
                country_group_ids.add(record.pol_country_group_id.id)  # Use .id to add a single ID
            if record.pod_country_group_id:
                country_group_ids.add(record.pod_country_group_id.id)  # Use .id to add a single ID
            record.country_group_count = len(country_group_ids)  # Count the distinct IDs

    def action_view_ocean(self):
        """ Opens all related Ocean records in a list view """
        self.ensure_one()  # Ensure only one record is processed
        ocean_ids = set()
        if self.pol_ocean_id:
            ocean_ids.add(self.pol_ocean_id.id)
        if self.pod_ocean_id:
            ocean_ids.add(self.pod_ocean_id.id)

        if ocean_ids:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Oceans',
                'view_mode': 'list,form',
                'res_model': 'ocean.data',
                'domain': [('id', 'in', list(ocean_ids))],
                'context': dict(self._context),
            }
        else:
            return {'type': 'ir.actions.act_window_close'}

    def action_view_country_group(self):
        """ Opens all related Country Group records in a list view """
        self.ensure_one()  # Ensure only one record is processed
        country_group_ids = set()
        if self.pol_country_group_id:
            country_group_ids.add(self.pol_country_group_id.id)
        if self.pod_country_group_id:
            country_group_ids.add(self.pod_country_group_id.id)

        if country_group_ids:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Country Groups',
                'view_mode': 'list,form',
                'res_model': 'res.country.group',
                'domain': [('id', 'in', list(country_group_ids))],
                'context': dict(self._context),
            }
        else:
            return {'type': 'ir.actions.act_window_close'}


    def action_view_terminals(self):
        """ Opens all terminals related to the POL and POD in a list view using precomputed terminal_ids """
        self.ensure_one()
        if self.terminal_ids:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Terminals',
                'view_mode': 'list,form',
                'res_model': 'terminal.port',
                'domain': [('id', 'in', self.terminal_ids.ids)],
                'context': dict(self._context),
            }
        else:
            return {'type': 'ir.actions.act_window_close'}

    def action_view_warehouses(self):
        """ Opens all warehouses related to the POL and POD in a list view using precomputed warehouse_ids """
        self.ensure_one()
        if self.warehouse_ids:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Warehouses',
                'view_mode': 'list,form',
                'res_model': 'terminal.port',
                'domain': [('id', 'in', self.warehouse_ids.ids)],
                'context': dict(self._context),
            }
        else:
            return {'type': 'ir.actions.act_window_close'}

    @api.onchange('route_type')
    def _compute_pol_pod_domain(self):
        for record in self:
            if record.route_type == 'sea':
                record.pol_pod_domain = "[('type_id.code', '=', 'SEA')]"
            elif record.route_type == 'air':
                record.pol_pod_domain = "[('type_id.code', '=', 'AIR')]"
            else:
                record.pol_pod_domain = "[('type_id.code', '=', 'AIR'), ('type_id.code', '=', 'SEA')]"

    @api.onchange('route_type')
    def _compute_carrier_ids_domain(self):
        for record in self:
            partner_type_all = self.env['partner.type'].search([('code', '=', 'SHL'), ('code', '=', 'ARL')]).ids
            record.carrier_ids_domain = "[('partner_type_id', 'in', " + str(partner_type_all) + "), ('is_company', '=', True)]"
            if record.route_type == 'sea':
                partner_type_sea = self.env['partner.type'].search([('code', '=', 'SHL')]).ids
                if partner_type_sea:
                    record.carrier_ids_domain = "[('partner_type_id', 'in', " + str(partner_type_sea) + "), ('is_company', '=', True)]"
            elif record.route_type == 'air':
                partner_type_air = self.env['partner.type'].search([('code', '=', 'ARL')]).ids
                if partner_type_air:
                    record.carrier_ids_domain = "[('partner_type_id', 'in', " + str(partner_type_air) + "), ('is_company', '=', True)]"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                sequence_number = self.env['ir.sequence'].next_by_code('carrier.route')
                vals['name'] = f"Route/{sequence_number}"
            if vals.get('pod_id') == vals.get('pol_id'):
                raise ValidationError('Please select another port. You cant choose the same port at two different locations.')

            return super(CarrierRoute, self).create(vals_list)

    @api.depends('carrier_ids')
    def _compute_carrier_count(self):
        for record in self:
            record.carrier_count = len(record.carrier_ids)

    @api.depends('create_date', 'write_date')
    def _compute_last_update(self):
        for record in self:
            record.last_update = record.write_date if record.write_date else record.create_date

    @api.constrains('pol_id', 'pod_id')
    def _check_pol_pod_unique(self):
        for record in self:
            duplicate_routes = self.env['carrier.route'].search([('pol_id', '=', record.pol_id.id), ('pod_id', '=', record.pod_id.id), ('id', '!=', record.id)])
            if duplicate_routes:
                raise ValidationError('A route with this POL and POD already exists.')

    @api.depends('pol_id', 'pod_id', 'route_type')
    def _compute_name(self):
        for record in self:
            pol_name = record.pol_id.name if record.pol_id else ''
            pod_name = record.pod_id.name if record.pod_id else ''
            route_type_display = dict(self._fields['route_type'].selection).get(record.route_type)
            record.name = f"Route from {pol_name} to {pod_name} by {route_type_display}"

    def write(self, values):
        res = super().write(values)
        if 'Route Route' in self.name and not values.get('name', False):
            self.name = self.name.replace('Route Route', 'Route')
        return res