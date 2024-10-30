from odoo import fields, models
from odoo.exceptions import UserError


class Country(models.Model):
    _inherit = 'res.country'
    _order = 'id desc'


class CountryGroup(models.Model):
    _inherit = 'res.country.group'
    _order = 'id desc'

    def create(self, vals_list):
        if not self.env.user.has_group('eit_freight_MasterData.group_freight_manager') and not self.env.user.id == 1:
            raise UserError('Only freight manager can add country group')
        res = super(CountryGroup, self).create(vals_list)
        return res

    def write(self, vals):
        if not self.env.user.has_group('eit_freight_MasterData.group_freight_manager') and not self.env.user.id == 1:
            raise UserError('Only freight manager can edit country group')
        res = super(CountryGroup, self).write(vals)
        return res
