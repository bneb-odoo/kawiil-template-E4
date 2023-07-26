from odoo import api, fields, models

class StockLot(models.Model):

    _inherit = 'stock.lot'

    name = fields.Char('Lot/Serial Number', compute='_compute_name', store=True)

    @api.depends('product_id')
    def _compute_name(self):
        for stockLot in self:
            product_ref = stockLot.product_id.product_tmpl_id
            if product_ref.detailed_type == 'motorcycle' and stockLot.product_id.tracking != "none":
                make = product_ref.make.upper() if product_ref.make else 'XX'
                model = product_ref.model.upper() if product_ref.model else 'XX'
                year = str(product_ref.year)[-2:] if product_ref.year else '00'
                battery_capacity = str(product_ref.battery_capacity).upper() if product_ref.battery_capacity else 'XX'
                sequence = self.env['ir.sequence'].next_by_code('vin.serial.number')
                stockLot.name=f"{make}{model}{year}{battery_capacity}{sequence}"
            else:
                stockLot.name=self.env['ir.sequence'].next_by_code('stock.lot.serial')


