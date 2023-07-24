from odoo.http import request, route, Controller

class SnippetControllers(Controller):

    @route(['/mileage_sum'], type='json', auth='public', website=True)
    def mileage_sum(self):
        return sum(request.env['motorcycle.registry'].search([]).mapped('current_mileage'))
         
