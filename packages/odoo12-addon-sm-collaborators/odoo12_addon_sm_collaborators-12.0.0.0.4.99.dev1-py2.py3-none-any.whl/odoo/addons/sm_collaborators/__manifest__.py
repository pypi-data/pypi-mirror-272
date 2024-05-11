# -*- coding: utf-8 -*-
{
    'name': "sm_collaborators",

    'summary': """""",

    'description': """""",

    'author': "Som Mobilitat",
    'website': "http://www.sommobilitat.coop",

    'category': 'Mobility',
    'version': '12.0.0.0.4',

    # any module necessary for this one to work correctly
    'depends': ['base', 'vertical_carsharing'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/views_collaborator.xml',
        'views/views_collaborator_actions.xml',
        'views/views_collaborator_fetch_wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
