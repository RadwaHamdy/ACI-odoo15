# -*- coding: utf-8 -*-
{
    'name': "inventory_custom",
    'version': '1.0',
    'summary': """
        product and lot customization""",

    'description': """
       adding new field for product form , 
       lot generation formula ,
       new dates dependence ,
       custom labels pdfs and
       printing labels user group
    """,

    'author': "Radwa Hamdy",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'mail', 'sale', 'base_setup'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/brand_name.xml',
        'views/product_views.xml',
        'views/lot_view.xml',
        'reports/lot_label.xml',
        'reports/report_date_label.xml',
        'reports/stock_report_views_inherit.xml',
        # 'data/res_config_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
