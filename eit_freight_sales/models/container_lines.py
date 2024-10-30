from odoo import fields, models, api


class ContainerLinesModel(models.Model):
    _name = 'container.lines'
    _description = 'Container lines'

    package_type = fields.Many2one('package.type', string='Package Types', domain="[('tag_type_ids', 'in', [2])]")
    type = fields.Many2one('freight.package')
    container_type_id = fields.Many2one(comodel_name='container.type', string='Container Type')
    qty = fields.Integer(string="QTY")
    refrigerated = fields.Boolean(related='type.refrigerated', store=True)
    temperature = fields.Integer()
    humidity = fields.Integer()
    ventilation = fields.Integer()
    cbm = fields.Float('CBM', compute='compute_cbm')
    length = fields.Integer(string="L (CM)")
    width = fields.Integer(string="W (CM)")
    height = fields.Integer(string="H (CM)")
    gw = fields.Integer(string="GW (KG)")
    cpm = fields.Float(string="CBM", compute='_compute_cpm', readonly=False, store=True)
    vm = fields.Float(string="VM", compute='_compute_vm', store=True)
    volume = fields.Float(string='Volume')
    chw = fields.Float(string="CHW", compute="compute_chw", store=True)
    crm_id = fields.Many2one('crm.lead')

    @api.depends('length', 'width', 'height', 'qty', 'gw')
    def compute_chw(self):
        for rec in self:
            if rec.gw * rec.qty > rec.vm:
                rec.chw = rec.gw * rec.qty
            else:
                rec.chw = rec.vm

    @api.depends('length', 'width', 'height')
    def _compute_cpm(self):
        for rec in self:
            rec.cpm = (rec.length / 100) * (rec.width / 100) * (rec.height / 100)

    @api.depends('cpm')
    def _compute_vm(self):
        for rec in self:
            rec.vm = rec.cpm / 0.006

    @api.depends('length', 'width', 'height', 'qty')
    def compute_cbm(self):
        for rec in self:
            total = (rec.length / 100) + (rec.length / 100) + (rec.length / 100)
            rec.cbm = total * rec.qty
