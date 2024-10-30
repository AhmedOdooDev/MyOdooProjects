from odoo import fields, models, api


class Flights(models.Model):
    _name = "freight.airplane"
    _description = 'Flights Data'
    _order = 'id desc'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    partner_id = fields.Many2one(comodel_name='res.partner', string="Plane Owner")
    status = fields.Selection(selection=[('active', 'Active'), ('inactive', 'Inactive')], string='Active')
    active = fields.Boolean(string='Status', default=True)


    @api.onchange('active')
    def _onchange_active(self):
        for rec in self:
            if not rec.active:
                rec.toggle_active()
