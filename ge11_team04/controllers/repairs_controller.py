from odoo.http import route, request
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.exceptions import MissingError, AccessError


class PortalMotorcycleRegistry(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        RepairOrder = request.env["repair.order"]
        if "maintenance_requests_count" in counters:
            values['maintenance_requests_count'] = RepairOrder.search_count([("partner_id", "=", partner.id)]) \
                if RepairOrder.check_access_rights('read', raise_exception=False) else 0
        return values

    def _prepare_maintenance_requests_portal_rendering_values(self, search_domain, search_in, search, search_list):
        RepairOrder = request.env["repair.order"]
        domain = [("partner_id", "=", request.env.user.partner_id.id)]
        repairs = RepairOrder.search(domain)
        total_registries = RepairOrder.search_count(domain)
        url = "/my/maintenance_requests"
        values = self._prepare_portal_layout_values()
        pager_values = portal_pager(
            url=url,
            total=total_registries,
            url_args={'search_in': search_in, 'search': search}
        )
        values.update({
            "repairs": repairs,
            "page_name": "maintenance_requests",
            "pager": pager_values,
            "default_url": url,
            "search_in": search_in,
            "searchbar_inputs": search_list,
            "search": search 
        })
        return values

    @route("/my/maintenance_requests", type="http", auth="user", website=True)
    def portal_my_repairs(self, search="", search_in="all",**kwargs):
        search_list = {
            'all' : {'label':'All', 'input':'all', 'domain':[]},
            "name" : {'label': "Owner's Name", 'input':"name", 'domain':[('partner_id.name', 'ilike', search)]},
            "vin" : {'label': "Vehicle Identification Number (VIN)", 'input':"vin", 'domain':[('lot_id.name','=',search)]}
        }
        search_domain = search_list[search_in]['domain']
        values = self._prepare_maintenance_requests_portal_rendering_values(search_domain, search_in, search, search_list)
        return request.render("ge11_team04.portal_repair", values)

    @route(['/my/maintenance_requests/<int:repair_id>'], type='http', auth="public", website=True)
    def portal_repair(self, repair_id, access_token=None):
        try:
            repair_sudo = self._document_check_access('repair.order', repair_id, access_token=access_token)
        except (AccessError, MissingError): return request.redirect('/my')
        backend_url = f'/web#model={repair_sudo._name}&id={repair_sudo.id}&action={repair_sudo._get_portal_return_action().id}&view_type=form'
        values = {
            'repair': repair_sudo,
            'report_type': 'html',
            'backend_url': backend_url
        }
        values = self._get_page_view_values(repair_sudo, access_token, values, "my_repairs_history", False)
        return request.render('ge11_team04.repair_portal_template', values)
    
    @route("/my/maintenance_requests/new", type="http", auth="user", website=True)
    def portal_new_maintenance_request(self, **kwargs):
        url = "/my/maintenance_requests/new"
        values = self._prepare_portal_layout_values()
        products = request.env["product.product"].search([])
        pager_values = portal_pager(
            url=url,
            total=0,
        )
        values.update({
            "products": products,
            "page_name": "new_maintenance_request",
            "pager": pager_values,
            "default_url": url,
            'report_type': 'html',
        })
        return request.render('ge11_team04.new_repair', values)

    @route(['/my/maintenance_requests/new/submit'], type='http', auth="public", website=True)
    def portal_new_request_submit(self, **post):
        lot_id = request.env['stock.lot'].search([('name','=',post['vin'])], limit=1)
        if lot_id:
            request.env['repair.order'].create({
                'product_id' : post['product'],
                'lot_id' : lot_id[0].id,
                'description' : post['desc']
            })
        return request.render("portal.portal_my_home")
