{
    'name': 'Estate Account',
    'depends': ['estate','account'],
    'application': True,
    'data' : [
        'security/ir.model.access.csv',
    ],
    'installable' : True,
    'auto_install' : True,
    'category': 'Real Estate',
    'description': 'Link module between Estate and Accounting.',
}


