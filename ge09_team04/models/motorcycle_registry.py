from odoo import models, fields, _


class MotorcycleRegistry(models.Model):
    _inherit = 'motorcycle.registry'
    repair_order_ids = fields.One2many(comodel_name="repair.order", inverse_name="motorcycle_registry_entry")

    def action_view_repair_order(self):
        return {
                'name': _('Repair Orders'),
                'type': 'ir.actions.act_window',
                'res_model': 'repair.order',
                'view_mode': 'kanban,tree,form',
                'domain': [('motorcycle_registry_entry', '=', self.id)],
                }
