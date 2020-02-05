{
    'name': "CMT",

    'summary': "Construction Material Testing",

    'description': """
        Provide Construction Material Testing Releted Information of Different Laboratories
    """,

    'author': "JS",

    'depends': ['web_dashboard', 'portal'],

    'version': '0.1',

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/report.xml',
        'report/result.xml',
        'views/template.xml',
        'views/observation.xml',
        'views/views.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],

    'application': True,
}
