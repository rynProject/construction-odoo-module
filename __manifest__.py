{
    "name": "Construction",
    "summary": "Construction App",
    "author": "Riyan Andriyanto",
    "category": "",
    "license": "AGPL-3",
    "website": "https://www.github.com/rynproject",
    "version": "0.0.1",
    'depends': ['base'],
    "application": True,
    "data": [
        'security/ir.model.access.csv',
        'views/menu_item.xml',
        'views/project_view.xml',
        'views/task_view.xml',
        'views/budget_view.xml',
        'views/expenditure_view.xml',
        'views/progresnote_view.xml',
        'views/materials_view.xml',
        'views/purchase_view.xml',
        'views/worker_view.xml',
        'views/equipment_view.xml',
        'views/evaluation_view.xml',
        'views/changeinplanning_view.xml',
        'views/permit_view.xml',
        # 'views/map_only.xml',
    ],
    'sequence': 0,
        'assets': {
        'web.assets_backend': [
            'construction/static/src/js/*.js'
        ],
    },
}
