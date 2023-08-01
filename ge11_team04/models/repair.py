from odoo import models


class Repair(models.Model):
    _name = "repair.order"
    _inherit = ['repair.order', 'portal.mixin']

    def _compute_access_url(self):
        super()._compute_access_url()
        for registry in self:
            registry.access_url = f'/my/maintenance_requests/{registry.id}'

    def _get_portal_return_action(self):
        self.ensure_one()
        return self.env.ref('motorcycle_registry.registry_list_action')
