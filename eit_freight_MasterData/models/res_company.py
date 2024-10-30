from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    show_bank_details = fields.Boolean(string="Show Bank Details", default=True)
    account_name = fields.Char(string="Account Name")
    bank_name = fields.Char(string="Bank Name")
    bank_address = fields.Char(string="Bank Address")
    swift_code = fields.Char(string="Swift Code")
    account_number = fields.Char(string="Account Number")
