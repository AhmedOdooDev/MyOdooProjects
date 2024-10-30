from odoo import fields, _, models, api
from odoo.exceptions import UserError


class ContainerData(models.Model):
    _name = "container.data"
    _description = 'Container Data'
    _order = 'id desc'

    name = fields.Char(string="Container Number", required=True)
    container_type_id = fields.Many2one(comodel_name='container.type', string="Container Type")
    container_is = fields.Selection(selection=[('dry', 'Dry'), ('reefer', 'Reefer'), ('sequ', 'Special Equ')],
                                    string='Container Is')
    partner_id = fields.Many2one(comodel_name='res.partner', string="Container Owner")
    tare_weight = fields.Float(string="Tare Weight")
    max_load = fields.Float(string="Max Load")
    status = fields.Selection(selection=[('active', 'Active'), ('inactive', 'Inactive')], string='Status')
    active = fields.Boolean(string='Active', default=True)
    description = fields.Text(string="Description")

    _sql_constraints = [('name_uniq', "unique(name)", "This Container Has Been Added Before")]

    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()

    def create(self, vals_list):
        # Check if vals_list is a list
        if isinstance(vals_list, list):
            for vals in vals_list:
                if self.check_container_number(vals.get('name', '')):
                    for key, value in vals.items():
                        if isinstance(value, str):
                            vals[key] = value.strip()
            return super(ContainerData, self).create(vals_list)
        else:
            if self.check_container_number(vals_list.get('name', '')):
                for key, value in vals_list.items():
                    if isinstance(value, str):
                        vals_list[key] = value.strip()
            return super(ContainerData, self).create(vals_list)

    def write(self, vals_list):
        if self.check_container_number():
            for key, value in vals_list.items():
                if isinstance(value, str):
                    vals_list[key] = value.strip()
            return super(ContainerData, self).write(vals_list)

    @api.onchange('name')
    def _onchange_container_number(self):
        self.check_container_number()

    def check_container_number(self, name=None):
        container_name = self.name or name
        show_error = False
        if container_name:
            input_string = container_name
            if len(input_string) != 11:
                show_error = True
            elif input_string[3] != 'U':
                show_error = True
            elif not input_string[:3].isalpha() or not input_string[:3].isupper():
                show_error = True
            elif not input_string[4:].isdigit():
                show_error = True
        if show_error:
            raise UserError("The number should contain 4 Capital letters Must ended By (U) & 7 numbers")
        else:
            return True

