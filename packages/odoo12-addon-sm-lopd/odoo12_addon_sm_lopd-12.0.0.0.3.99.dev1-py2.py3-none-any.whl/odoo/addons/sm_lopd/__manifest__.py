# -*- coding: utf-8 -*-
{
    'name': "sm_lopd",

    'summary': """
  Manage GDPR contract send
  """,

    'author': "Som Mobilitat",
    'website': "https://www.sommobilitat.coop",

    'category': 'vertical-carsharing',
    'version': '12.0.0.0.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sm_partago_user'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv'
        'report/lopd_report.xml',
        'email_tmpl/lopd_email.xml',
        'email_tmpl/lopd_companies_template.xml',
        'views/views_cron.xml',
        'views/views_res_config_settings.xml',
        'views/views_members.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
