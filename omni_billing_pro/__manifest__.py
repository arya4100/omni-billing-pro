{
    'name': 'OmniBilling Pro',
    'version': '16.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'All-in-one business invoicing, billing & payment tracking for every business.',
    'description': """
OmniBilling Pro
================
A classic, fully-featured business billing and payment tracking module.
Manage invoices, confirm payments, and track transactions — all in one clean, premium interface.

Key Features:
- Create professional business invoices with auto-generated references (INV/YYYY/XXXXX)
- Add multiple line items with description, quantity and unit price
- Register full or partial payments (Cash, Bank, Credit Card, Online)
- Automatic balance and paid amount calculation
- Invoice lifecycle: Draft → Open → Paid → Cancelled
- Track all transactions with unique references (TRX/YYYY/XXXXX)
- Built-in Odoo chatter, notes and activity scheduling on every record
- Works for all internal Odoo users out of the box — zero configuration
- Multi-currency ready (uses company default currency)
- Lightweight: only requires base and mail — no full Accounting module needed
    """,
    'author': 'Arya Patel',
    'website': 'https://github.com/aryapatel4100',
    'support': 'aryapatel4100@gmail.com',
    'depends': ['base', 'mail'],
    'data': [
        'data/sequence.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/billing_views.xml',
    ],
    'demo': [],
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
    'price': 19.00,
    'currency': 'USD',
}
