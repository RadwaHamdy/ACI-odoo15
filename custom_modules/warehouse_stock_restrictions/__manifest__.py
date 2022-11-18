# -*- coding: utf-8 -*-


{
    'name': "ACI Warehouse Access Rights",

    'summary': """
         Warehouse and Stock Location Restriction on Users.""",

    'description': """
        This Module Restricts the User from Accessing Warehouse 
        and Process Stock Moves other than allowed to Warehouses and Stock Locations.
    """,

    'author': "Radwa Hamdy",
    'website': "http://www.NoWebSite.com",
    'category': 'Warehouse',
    'version': '0.2',
    'images': ['static/description/WarehouseRestrictions.jpg'],
    'depends': ['base', 'stock'],

    'data': [

        'views/users_view.xml',
        'security/security.xml',
        # 'security/ir.model.access.csv',
    ],
    
    
}
