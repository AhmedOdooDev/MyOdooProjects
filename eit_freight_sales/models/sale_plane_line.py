from odoo import models, fields, api
from datetime import timedelta


class SalePlanesLine(models.Model):
    _name = 'sale.plane.line'

    plane_id = fields.Many2one('freight.airplane', string="Plane")
    sale_plane_id = fields.Many2one('sale.order')
    voyage_number = fields.Char(string="Voyage Number")
    etd = fields.Date(string="ETD")
    eta = fields.Date(string="ETA")
    tt_day = fields.Integer(string="T.T Day")

    @api.onchange('etd', 'tt_day')
    def _compute_eta(self):
        for record in self:
            if record.etd and record.tt_day:
                record.eta = record.etd + timedelta(days=record.tt_day)
            else:
                record.eta = False

    @api.onchange('etd', 'eta')
    def _compute_tt_day(self):
        for record in self:
            if record.etd and record.eta:
                delta = record.eta - record.etd
                record.tt_day = delta.days
            else:
                record.tt_day = 0
