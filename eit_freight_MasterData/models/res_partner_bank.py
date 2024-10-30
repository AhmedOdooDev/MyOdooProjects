# -*- coding: utf-8 -*-
import base64
from collections import defaultdict

import werkzeug
import werkzeug.exceptions
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.image import image_data_uri


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    show_bank_details = fields.Boolean(string="Show Bank Details in Reports", default=False)
