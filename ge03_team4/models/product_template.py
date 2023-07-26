# -*- coding: utf-8 -*-
from odoo import api, fields, models
class ProductTemplate(models.Model):
    _inherit = 'product.template'
 
    name = fields.Char(string="Name", store=True, compute='_compute_NAME', readonly=False)

    @api.depends('make', 'model', 'year')
    def _compute_NAME(self):
        for product in self:
            if product.detailed_type == 'motorcycle':
                name_parts = [part for part in [product.make, product.model, str(product.year)] if part]
                product.name = ' '.join(name_parts) if name_parts else False
            else:
                product.name = product.name if product.name else False
