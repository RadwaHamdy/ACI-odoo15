# -*- coding: utf-8 -*-
{
    'name': 'Product Enhancement',
    'version': '15.0',
    'category': 'Sales',
    'author': 'Ahmed Fathi <ahmed.fa.kh96@gmail.com>',
    'license': 'LGPL-3',
    'summary': """
    Product Enhancement 
    """,
    'depends': ['inventory_custom'],
    'data': [
        'security/ir.model.access.csv',
        # 'security/security.xml',
        'views/product_category.xml',
        'views/uom.xml',
        'views/product_type.xml',
        'views/product_version.xml',
        'views/product_subtype.xml',
        'views/product_product.xml',
        'views/menus.xml',
        # 'data/data.xml',
    ],
    'images': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
