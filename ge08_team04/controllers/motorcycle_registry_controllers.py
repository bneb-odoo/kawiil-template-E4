from odoo.http import route, request
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.exceptions import MissingError, AccessError


class PortalMotorcycleRegistry(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        MotorcycleRegistry = request.env["motorcycle.registry"]
        if "motorcycle_registry_count" in counters:
            values['motorcycle_registry_count'] = MotorcycleRegistry.search_count([("owner_id", "=", partner.id)]) \
                if MotorcycleRegistry.check_access_rights('read', raise_exception=False) else 0
        return values

    def _prepare_motorcycle_registry_portal_rendering_values(self, search_domain, search_in, search, search_list):
        MotorcycleRegistry = request.env["motorcycle.registry"]
        domain = ['|',("owner_id", "=", request.env.user.partner_id.id),('public','=',True)]
        if search_domain:
            domain.append(search_domain[0])
        registries = MotorcycleRegistry.search(domain)
        total_registries = MotorcycleRegistry.search_count(domain)
        url = "/my/registries"
        values = self._prepare_portal_layout_values()
        pager_values = portal_pager(
            url=url,
            total=total_registries,
            url_args={'search_in': search_in, 'search': search}
        )
        values.update({
            "registries": registries,
            "page_name": "motorcycle_registry",
            "pager": pager_values,
            "default_url": url,
            "search_in": search_in,
            "searchbar_inputs": search_list,
            "search": search 
        })
        return values

    @route("/my/registries", type="http", auth="user", website=True)
    def portal_my_registries(self, search="", search_in="all",**kwargs):

        search_list = {
            'all' : {'label':'All', 'input':'all', 'domain':[]},
            "name" : {'label': "Owner's Name", 'input':"name", 'domain':[('owner_id.name', 'ilike', search)]},
            "state" : {'label': "Owner's State", 'input':"state", 'domain':[('owner_id.state_id.name', 'ilike', search)]},
            "country" : {'label': "Owner's Country", 'input':'country', 'domain':[('owner_id.country_id.name', 'ilike', search)]},
            'make' : {'label':'Make', 'input':'make', 'domain':[('make', 'ilike', search)]},
            'model' : {'label':'Model', 'input':'model', 'domain':[('model', 'ilike', search)]},
        }

        search_domain = search_list[search_in]['domain']

        values = self._prepare_motorcycle_registry_portal_rendering_values(search_domain, search_in, search, search_list)
        return request.render("ge08_team04.portal_motorcycle_registries", values)

    @route(['/my/registries/<int:registry_id>'], type='http', auth="public", website=True)
    def portal_registry(self, registry_id, access_token=None):
        try:
            registry_sudo = self._document_check_access('motorcycle.registry', registry_id, access_token=access_token)
        except (AccessError, MissingError): return request.redirect('/my')

        backend_url = f'/web#model={registry_sudo._name}&id={registry_sudo.id}&action={registry_sudo._get_portal_return_action().id}&view_type=form'
        values = {
            'registry': registry_sudo,
            'report_type': 'html',
            'backend_url': backend_url
        }
        values = self._get_page_view_values(registry_sudo, access_token, values, "my_registrations_history", False)
        return request.render('ge08_team04.motorcycle_registry_portal_template', values)
