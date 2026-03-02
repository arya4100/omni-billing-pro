{
    'name': 'OmniBilling Pro',
    'version': '1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'All-in-one premium business billing, invoicing, and transaction management suite.',
    'description': """
OmniBilling Pro
================
A classic, fully working and premium module for businesses to handle everything related to billing and transactions in one unified place.

Key Features:
- Create professional business invoices.
- Track fine-grained transactions and partial payments.
- Automatic balance calculation.
- Clean and premium User Interface.
- Dedicated unified dashboards.
    """,
    'author': 'Arya Solutions',
    'website': 'https://www.example.com',
    'depends': ['base', 'mail'],
    'data': [
        'data/sequence.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/billing_views.xml',
    ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
}
