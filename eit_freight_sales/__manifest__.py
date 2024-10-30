# -*- coding: utf-8 -*-
{
    'name': "Freight Sales",

    'summary': """
        Freight Forwarding Sales
        """,

    'description': """
        Freight Forwarding Sales.
    """,

    'author': "EIT-Hub (Expert Information Technology)",
    'website': 'www.eit-hub.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list

    'category': 'Services/Freight',
    'version': '18.0.0.0.2',
    'license': 'LGPL-3',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': [
        'base', 'crm', 'sale_management', 'delivery',
        'account', 'eit_freight_MasterData',
        'sale_crm', 'web', 'website'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/crm_lead_view.xml',
        'views/sale_order_view.xml',
        'views/request_quote.xml',
        'views/partner.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/eit_freight_sales/static/src/js/main.js',
            '/eit_freight_sales/static/src/img/quote-bg.png',
            '/eit_freight_sales/static/lib/select2.min.css',
            '/eit_freight_sales/static/lib/select2.min.js',
            '/eit_freight_sales/static/src/js/select2_init.js',
            '/eit_freight_sales/static/src/scss/style.scss',
        ],
        'web.assets_backend': [
            # '/eit_freight_sales/static/lib/select2.min.css',
            # '/eit_freight_sales/static/lib/select2.min.js',
        ],
        'website.assets_frontend': [
            '/eit_freight_sales/static/src/scss/style.scss',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
