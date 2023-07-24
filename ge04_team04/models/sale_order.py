from odoo import api, fields, models

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    is_new_customer = fields.Boolean(compute='_compute_is_new_customer')
    
    @api.depends('partner_id')
    def _compute_is_new_customer(self):
        for order in self:
            if order.partner_id:
                sale_orders_from_customer = self.env['sale.order.line'].search([('product_type','=','motorcycle'),('order_partner_id','=',order.partner_id.id),('state','in',['sale', 'done'])])
                order.is_new_customer = False if sale_orders_from_customer else True
            else:
                order.is_new_customer = False
            
    def add_discount(self):
        for order in self:
            new_customer_pricelist = self.env.ref('ge04_team04.new_customer_pricelist')
            order.pricelist_id = new_customer_pricelist.id
            order.action_update_prices()
