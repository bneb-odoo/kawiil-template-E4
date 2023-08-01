from odoo import models, api, Command

class MotorcycleRegistry(models.Model):
    _inherit = ['motorcycle.registry']

    @api.model_create_multi
    def create(self, vals_list):
        for value in vals_list:
            if value.get('sale_order_id', False):
                owner = self.env['sale.order'].browse([value['sale_order_id']]).partner_id
                if owner.email:
                    portal_user_group = self.env.ref('base.group_portal').id
                    group_user = self.env.ref('base.group_user')
                    if self.env['res.users'].search([('email', '=', owner.email)]):
                        continue
                    else:
                        self.env.context = dict(self.env.context, no_reset_password=True)
                        user = self.env['res.users'].create({'partner_id': owner.id, 
                                                    'login': owner.email,})
                        user.write({'groups_id': [(4, portal_user_group), (3, group_user.id)]})
                        user.action_reset_kawiil_password()
                else:
                    continue
        return super().create(vals_list)
