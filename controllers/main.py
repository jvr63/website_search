# -*- coding: utf-8 -*-

import logging

from odoo import fields, http, tools, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.osv import expression

_logger = logging.getLogger(__name__)

class WebsiteSaleGuadalstore(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values):
        """
            Modifica el domain de búsqueda, añade el EAN
        """
        domain = request.website.sale_product_domain()
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', ('name', 'ilike', srch), ('description', 'ilike', srch),
                    ('description_sale', 'ilike', srch), ('product_variant_ids.default_code', 'ilike', srch)]

        if category:
            domain += [('public_categ_ids', 'child_of', int(category))]

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += [('attribute_line_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [('attribute_line_ids.value_ids', 'in', ids)]

        return domain

    @http.route()
    def get_combination_info_website(self, product_template_id, product_id, combination, add_qty, **kw)
        """
            Added ref and barcode to original response
        """
        _logger.info('-----------------------------------------------------------------------------------')
        kw.update({
            'barcode': request.env['product.product'].browse(int(product_id)).barcode
        })
        res = super(WebsiteSaleGuadalstore, self).get_combination_info_website(product_template_id, product_id, combination, add_qty, **kw)
        return res
