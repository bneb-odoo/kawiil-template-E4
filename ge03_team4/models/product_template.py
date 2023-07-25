# -*- coding: utf-8 -*-
from odoo import api, fields, models
class ProductTemplate(models.Model):
    _inherit = 'product.template'
 
    name = fields.Char(string="Name", store=True, compute='_compute_NAME', readonly=False)

    @api.depends('make','model','year')
    def _compute_NAME(self):
        name_computed = ''
        for product in self:
            if product.detailed_type == 'motorcycle':
                if product.make != False :
                    name_computed += product.make
                if product.model != False:
                    name_computed += product.model
                if product.year != False:
                    name_computed += str(product.year)
                if name_computed != '':
                    product.name = name_computed
                else:
                    product.name = False
            else:
                if product.name != False:
                    product.name = product.name   
                else:
                    product.name = False   
