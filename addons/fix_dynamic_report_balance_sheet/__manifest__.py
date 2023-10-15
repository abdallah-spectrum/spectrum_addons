# -*- coding: utf-8 -*-
{
    'name': "fix dynamic report balance sheet",

    'summary': """
        short fix to balancesheet in sdynamic report module
        steps :
        1- inherit 'dynamic.balance.sheet.report' model
        2- override view_report method
        3-filter_move lines_parents method inside

        """,


    'description': """
       short fix to balancesheet in sdynamic report module
    """,

    'author': "Abdallah",
    'website': "https://www.sys-spectrum.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'short_fix',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','dynamic_accounts_report'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
