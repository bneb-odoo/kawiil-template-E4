from odoo import api, models, fields, _
from odoo.exceptions import ValidationError



class MotorcycleRegistry(models.Model):
    _inherit = 'motorcycle.registry'

    stock_lot_ids = fields.One2many(comodel_name="stock.lot", inverse_name="motorcycle_registry_id", string="Lot IDs")
    stock_lot_id = fields.Many2one(comodel_name="stock.lot", compute='_compute_lot_id', string="Lot ID", store=True)
    sale_order_id = fields.Many2one(comodel_name='sale.order')
    
    vin = fields.Char(string="VIN", related="stock_lot_id.name", required=False)
    owner_id = fields.Many2one(comodel_name="res.partner", string="Owner", related="sale_order_id.partner_id")

    @api.constrains('stock_lot_ids')
    def _check_lot_ids(self):
        if len(self.stock_lot_ids) > 1: raise ValidationError(_('A registered motorcycle can only belong to one lot.'))

    @api.depends('stock_lot_ids')
    def _compute_lot_id(self):
        self.stock_lot_id = False
        for lot_id in self.filtered(lambda r: r.stock_lot_ids is not False and len(r.stock_lot_ids) > 0):
            lot_id.stock_lot_id = lot_id.stock_lot_ids[0]
