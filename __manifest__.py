# -*- coding: utf-8 -*-
{
    'name': "debranding_project",

    'summary': """
        backend debranding module""",

    'description': """
       maxware company backend debranding module
    """,

    'author': "Maxware Technology",
    'website': "http://www.maxware.ma",
    'category': 'Tools',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'qweb': ['static/src/xml/base.xml'],
    'demo': [
        'demo/demo.xml',
    ],
}
