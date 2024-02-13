# -*- coding: utf-8 -*-

{
    'name': 'Alternative to Odoo.sh for Odoo Community',
    'summary': 'Manage Repositories.',
     "version": "17.0.5.0",
    'category': 'Extra Tools',
    'website': "https://odoonext.com/",
    'author': 'David Montero Crespo',
    'installable': True,
    'external_dependencies': {'python': ['GitPython']}, # Docker instances fails at subprocess.check_call(["python3", "-m", "pip", "install", 'GitPython'])
    'depends': [
        'base','mail'
    ],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/repository_repository_view.xml',
        'views/panel_tool.xml',
        'views/ir_module_module.xml',
        'views/upload_module.xml',
        'wizard/installer.xml'
    ],
    'application': True,
    'price': 40,
    "uninstall_hook": "uninstall_hook",
    'images': ['static/description/imagen.png'],
    'currency': 'EUR',
    'license': 'AGPL-3',

}
