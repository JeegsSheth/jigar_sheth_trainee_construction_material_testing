{
    'name': "CMT",

    'summary': "Construction Material Testing",

    'description': """
        Provide Construction Material Testing Releted Information of Different Laboratories
    """,

    'author': "JS",

    'depends': ['web_dashboard'],

    'version': '0.1',

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'report/report.xml',
        'report/result.xml',
        'views/observation.xml',
        'views/views.xml',
    ],

    'application': True,
}
