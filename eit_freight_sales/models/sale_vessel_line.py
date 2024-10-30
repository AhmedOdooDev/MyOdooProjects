from odoo import models, fields, api
from datetime import timedelta


class SaleVesselLine(models.Model):
    _name = 'sale.vessel.line'

    vessel_id = fields.Many2one('freight.vessels', string="Vessel")
    voyage_number = fields.Char(string="Voyage Number")
    etd = fields.Date(string="ETD")
    eta = fields.Date(string="ETA")
    tt_day = fields.Integer(string="T.T Day")
    sale_vessel_id = fields.Many2one('sale.order')

    @api.onchange('tt_day')
    def _compute_eta(self):
        for record in self:
            if record.etd and record.tt_day:
                etd_date = fields.Date.from_string(record.etd)
                eta_date = etd_date + timedelta(days=record.tt_day)
                record.eta = fields.Date.to_string(eta_date)

    @api.onchange('eta')
    def _compute_tt_day(self):
        for record in self:
            if record.etd and record.eta:
                etd_date = fields.Date.from_string(record.etd)
                eta_date = fields.Date.from_string(record.eta)
                delta = eta_date - etd_date
                record.tt_day = delta.days
