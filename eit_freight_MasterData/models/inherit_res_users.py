import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class InheritResUsers(models.Model):
    _inherit = "res.users"

    is_hide_archive_user = fields.Boolean(string="Hide All Action Archive User", compute="compute_is_hide_archive_user")
    is_hide_archive_manager = fields.Boolean(string="Hide All Action Archive Manger",
                                             compute="compute_is_hide_archive_manager")
    is_hide_archive_admin = fields.Boolean(string="Hide All Action Archive Admin",
                                           compute="compute_is_hide_archive_admin")

    def compute_is_hide_archive_user(self):
        for rec in self:
            if rec.has_group('eit_freight_MasterData.group_freight_user'):
                rec.is_hide_archive_user = True
            else:
                rec.is_hide_archive_user = False

    def compute_is_hide_archive_manager(self):
        for rec in self:
            if rec.has_group('eit_freight_MasterData.group_freight_manager') and rec.has_group(
                    'eit_freight_MasterData.group_freight_user'):
                rec.is_hide_archive_manager = True

            else:
                rec.is_hide_archive_manager = False

    def compute_is_hide_archive_admin(self):
        for rec in self:
            if rec.has_group('eit_freight_MasterData.group_freight_manager') and rec.has_group(
                    'eit_freight_MasterData.group_freight_admin') and rec.has_group(
                'eit_freight_MasterData.group_freight_user'):
                rec.is_hide_archive_admin = True
            else:
                rec.is_hide_archive_admin = False

    @api.model
    def get_is_hide_archive_and_applied_models(self):
        current_user = self.env.user
        is_hide_archive_user = current_user.is_hide_archive_user
        is_hide_archive_manager = current_user.is_hide_archive_manager
        is_hide_archive_admin = current_user.is_hide_archive_admin
        return {
            "is_hide_archive_user": is_hide_archive_user,
            "is_hide_archive_manager": is_hide_archive_manager,
            "is_hide_archive_admin": is_hide_archive_admin,
        }
