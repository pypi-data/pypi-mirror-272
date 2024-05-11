# -*- coding: utf-8 -*-
{
    'name': "sm_teletacs",

    'summary': """
        Create extra expenses for carsharing usages""",

    'author': "Som Mobilitat",
    'website': "https://www.sommobilitat.coop",

    'category': 'vertical-carsharing',
    'version': '12.0.0.0.5',

    # any module necessary for this one to work correctly
    'depends': ['base', 'vertical_carsharing', 'sm_partago_usage'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views_teletac.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
