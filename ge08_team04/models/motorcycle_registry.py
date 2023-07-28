from odoo import api, fields, models


class MotorcycleRegistry(models.Model):
    _name = "motorcycle.registry"

    _inherit = ['motorcycle.registry', 'portal.mixin']

    make = fields.Char(compute='_compute_from_vin', store=True)
    model = fields.Char(compute='_compute_from_vin', store=True)

    public = fields.Boolean(default=False)

    def _compute_access_url(self):
        super()._compute_access_url()
        for registry in self:
            registry.access_url = f'/my/registries/{registry.id}'

    def _get_portal_return_action(self):
        self.ensure_one()
        return self.env.ref('motorcycle_registry.registry_list_action')
