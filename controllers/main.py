from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleEAN(WebsiteSale):

    def _get_shop_domain(self, search, category, attrib_values, search_in_description=True):
        domain = super()._get_shop_domain(self, search, category, attrib_values, search_in_description=True)
        if search:
            domain = ['|', ('barcode', 'ilike', search)] + domain
        return domain