{
    'name': 'Pathology Blood Bank Management',
    'version': '1.0',
    'category': 'Healthcare',
    'summary': 'Manage blood donations, donors, and blood inventory in a pathology lab',
    'description': """
        This module helps manage blood donations, donors, and blood inventory in a pathology lab. It provides functionalities for managing donation records, donor information, blood inventory, and more.
    """,
    'author': 'Harsh Singh',
    'depends': ['base', 'mail'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/donor_views.xml',
        'views/blood_inventory_views.xml',
        'views/test_views.xml',
        'views/menu_views.xml'
        # 'data/pathology.donor.csv',
        # 'data/pathology.donors.xml'
    ],
    'installable': True,
    'application': True,
}
