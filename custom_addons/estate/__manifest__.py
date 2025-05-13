{
    'name': 'Estate',
    'depends': ['base','sale'],
    'application': True,
    'data' : [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/property_type_view.xml',
        'views/res_users_view.xml',
    ],
    'installable' : True,
    'auto_install' : True,
}


