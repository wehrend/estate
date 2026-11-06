{
    'name': "Real Estate",
    'version': '19.0.1.0.0',
    'depends': ['base'],
    'author': "Wehrend",
    'category': 'Category',
    'description': """
    Description text
    """,
    'application': True,
    'installable': True,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
       # 'demo/demo_data.xml',
    ],
}
