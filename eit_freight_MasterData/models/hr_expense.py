# Part of Odoo. See LICENSE file for full copyright and licensing details.
import contextlib
import re

import psycopg2.errors

from odoo import api, fields, models, _


class HrExpense(models.Model):
    _inherit = ['hr.expense']

    invoice_nature = fields.Selection(selection=[('taxable', 'Taxable'), ('nontaxable', 'Nontaxable')],
                                      string="Invoice Nature", required=False)
