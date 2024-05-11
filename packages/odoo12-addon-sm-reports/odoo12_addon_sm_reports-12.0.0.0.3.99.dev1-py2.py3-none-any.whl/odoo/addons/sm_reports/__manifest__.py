# -*- coding: utf-8 -*-
{
    'name': "sm_reports",

    'summary': """
    reporting engine for carsgharing system
  """,

    'author': "Som Mobilitat",
    'website': "https://www.sommobilitat.coop",

    'category': 'Uncategorized',
    'version': '12.0.0.0.3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/default_template.xml',
        'views/views_members.xml'
    ],
    # only loaded in demonstration mode
    'demo': [],
}
