# -*- coding: utf-8 -*-

import logging

from odoo import fields, http, tools, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.osv import expression

_logger = logging.getLogger(__name__)

class WebsiteSaleGuadalstoreSearch(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values):
        """
            Modifica el domain de búsqueda, añade el EAN
        """

        domain = request.website.sale_product_domain()
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', '|', '|', ('name', 'ilike', srch), ('description', 'ilike', srch),
                    ('description_sale', 'ilike', srch), ('product_variant_ids.default_code', 'ilike', srch),
                    ('product_variant_ids.barcode', 'ilike', srch), ('product_brand_id.name', 'ilike', srch)
                ]

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

        # Código para filtrar por marca
        brand_list = request.httprequest.args.getlist('brand')
        brand_value = [int(v) for v in brand_list if v]
        if brand_value:
            domain += [('product_brand_id', '=', brand_value[0])]

        return domain

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        """ Added ref and barcode to original response """
        res = super(WebsiteSaleGuadalstoreSearch, self).shop(page, category, search, ppg, **post)
        brands = request.env['product.brand'].browse(
            map(lambda p: p['product'].product_brand_id.id, res.qcontext['bins'][0])
        )
        res.qcontext.update({
            'brands': brands,
            'brand_set': request.httprequest.args.get('brand', None)
        })
        return res
