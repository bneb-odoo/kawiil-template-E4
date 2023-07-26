from odoo import api, models, fields, Command


class Picking(models.Model):
    _inherit = 'stock.picking'

    def _action_done(self):
        res = super()._action_done()
        if res:
            for line in self.move_ids.move_line_ids:
                lot = line.lot_id
                product_ref=lot.product_id.product_tmpl_id
                if product_ref.detailed_type == 'motorcycle' and self.location_dest_id.name == self.env.ref('stock.stock_location_customers').name:
                    if self.origin:
                        sale_order = self.env['sale.order'].search([('name','=',self.origin)], limit=1)
                        self.env['motorcycle.registry'].create({
                            'stock_lot_ids': [Command.link(lot.id)],
                            'sale_order_id': sale_order[0].id,})
                    else:
                        sale_order = False
        return res


