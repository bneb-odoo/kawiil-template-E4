from odoo import api, models, fields


class Repair(models.Model):
    _inherit = 'repair.order'
    
    motorcycle_registry_entry = fields.Many2one(comodel_name="motorcycle.registry", compute='_find_registry_from_lot_or_vin', store=True)

    vin = fields.Char(related='motorcycle_registry_entry.vin', readonly=False)
    mileage = fields.Float(related='motorcycle_registry_entry.current_mileage')
    partner_id = fields.Many2one(related='motorcycle_registry_entry.owner_id', store=True)
    sale_order_id = fields.Many2one(related='motorcycle_registry_entry.sale_order_id')
    lot_id = fields.Many2one(related='motorcycle_registry_entry.stock_lot_id', readonly=False, store=True)
    
    product_id = fields.Many2one(related='lot_id.product_id', store=True)
    product_uom = fields.Many2one(precompute=False)

    @api.depends('lot_id', 'vin')
    def _find_registry_from_lot_or_vin(self):
        if self.lot_id and self.lot_id.product_id.product_tmpl_id.detailed_type == 'motorcycle':
            self.motorcycle_registry_entry = self.lot_id.motorcycle_registry_id
        elif self.vin:
            registry = self.env['motorcycle.registry'].search([('vin', '=', self.vin)], limit=1)
            self.motorcycle_registry_entry = registry[0].id if registry else False
        else:
            self.motorcycle_registry_entry = False
