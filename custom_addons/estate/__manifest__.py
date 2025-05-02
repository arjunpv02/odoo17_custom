{
    'name': 'Estate',
    'depends': ['base','sale'],
    'application': True,
    'data' : [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'installable' : True,
    'auto_install' : True,
}


