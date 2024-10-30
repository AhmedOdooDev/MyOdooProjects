# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, _, models, api


class ServiceScope(models.Model):
    _name = "service.scope"
    _description = 'Service Scope Data'
    # _order = 'id desc'
    _order = 'name asc'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    description = fields.Text(string="Refrigerated")
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], 'Active')
    active = fields.Boolean(string='Status', default=True)
    sequence = fields.Integer(string="Sequence", default=-1)
    service_scope_type = fields.Selection(selection=[('freight', 'Freight'), ('clearance', 'Customs Clearance'),
                                                     ('transportation', 'Transportation'), ('insurance', 'Insurance'),
                                                     ('warehousing', 'Warehousing'), ('other', 'Other')],
                                          string='Service Type', default='other', required=True)
    
    show_on_website = fields.Boolean(string='Show on Website', default=False)
    
    @api.model_create_multi
    def create(self, vals_list):
        if not isinstance(vals_list, list):
            vals_list = [vals_list]

        sequence_max = self.env['service.scope'].search_count([])

        for index, vals in enumerate(vals_list):
            if isinstance(vals, dict):
                if 'sequence' not in vals or vals.get('sequence') == -1:
                    sequence_max += 1
                    vals['sequence'] = sequence_max

                # Set code based on name, considering spaces
                if 'name' in vals:
                    vals['code'] = self._generate_code(vals['name'])

                # Ensure service_scope_type is set
                if 'service_scope_type' not in vals:
                    vals['service_scope_type'] = 'other'

            else:
                # If vals is not a dict, handle the vals_list conversion to list of dicts
                vals_list = []
                for val in vals_list:
                    if isinstance(val, str):
                        sequence_max += 1
                        name = val
                        code = self._generate_code(name)
                        vals_list.append({
                            'name': name,
                            'code': code,
                            'sequence': sequence_max,
                            'service_scope_type': 'other'  # Default value as it's required
                        })
                    elif isinstance(val, dict):
                        if 'sequence' not in val or val.get('sequence') == -1:
                            sequence_max += 1
                            val['sequence'] = sequence_max

                        # Set code based on name
                        if 'name' in val:
                            val['code'] = self._generate_code(val['name'])

                        if 'service_scope_type' not in val:
                            val['service_scope_type'] = 'other'  # Default value as it's required

                        vals_list.append(val)
                    else:
                        # Handle other types if necessary
                        pass
                break  # Exit the loop as we've now converted the entire list

        return super(ServiceScope, self).create(vals_list)

    def write(self, vals):
        sequence_max = self.env['service.scope'].search_count([])

        for rec in self:
            if 'sequence' not in vals or vals.get('sequence') == -1:
                if sequence_max and rec.sequence == -1:
                    vals['sequence'] = sequence_max + 1

            # Update code if name is changed
            if 'name' in vals:
                vals['code'] = self._generate_code(vals['name'])

            super(ServiceScope, rec).write(vals)
        return True

    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()

    def _generate_code(self, name):
        if self.code in ('AIR', 'SEA', 'LND', 'WH', 'INS', 'CCL', 'ILT') or self.service_scope_type in (
                'freight', 'clearance', 'transportation', 'insurance', 'warehousing'):
            # Static codes
            return self.code
        # Split the name by spaces and take the first character of each word
        words = name.split()
        # Combine the first letters, and take up to the first 3 characters
        first_letters = [word[0].upper() for word in words]
        # Join the first letters and take up to the first 3 characters
        code = ''.join(first_letters[:3])
        # Ensure the code is exactly 3 characters long
        if len(code) < 3:
            code = words[0][0:3].upper()
            # code += words[0][1:2].upper()
        return code[:3]

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            # Generate code from name
            self.code = self._generate_code(self.name) if not self.code else self.code
