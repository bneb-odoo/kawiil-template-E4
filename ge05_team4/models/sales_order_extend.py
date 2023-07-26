from odoo import api, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('user_id', 'company_id')
    def _compute_warehouse_id(self):
        for order in self:
            delivery_state = self.partner_id.state_id.name

            west_coast_locations = {'Washington', 'Oregon', 'California', 'Nevada', 'Idaho', 'Utah', 'Arizona','Montana', 'Wyoming', 'Colorado', 'New Mexico'}
            east_coast_locations = { 'Maine', 'New Hampshire', 'Vermont', 'Massachusetts', 'Rhode Island', 'Connecticut', 'New York', 'New Jersey', 'Delaware', 'Maryland', 'Virginia', 'West Virginia', 'North Carolina', 'South Carolina', 'Georgia', 'Florida'}
            
            if delivery_state in west_coast_locations:
                order.warehouse_id = self.env['stock.warehouse'].search([('name','=','Buffalo Dealership')])
                 # No external id, created
            elif delivery_state in east_coast_locations:
                order.warehouse_id = self.env['stock.warehouse'].search([('name','=','San Francisco Dealership')]) 
                # No external id, created
            else:
                order.warehouse_id = self.env.ref('stock.warehouse0')
