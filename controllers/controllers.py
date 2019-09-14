# -*- coding: utf-8 -*-

# import json
# import odoo
# import os
# import sys
# import jinja2
# from odoo import http, tools
# from odoo.addons.web.controllers.main import Database, Binary
# from odoo.addons.web.controllers import main
# # from django.shortcuts import render
#
#
# if hasattr(sys, 'frozen'):
#     # When running on compiled windows binary, we don't have access to package loader.
#     path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'views'))
#     loader = jinja2.FileSystemLoader(path)
# else:
#     loader = jinja2.PackageLoader('odoo.addons.debranding_project', "views")
#
# env = jinja2.Environment(loader=loader, autoescape=True)
# env.filters["json"] = json.dumps
#
# # 1 week cache for asset bundles as advised by Google Page Speed
# BUNDLE_MAXAGE = 60 * 60 * 24 * 7
#
# DBNAME_PATTERN = '^[a-zA-Z0-9][a-zA-Z0-9_.-]+$'
#
# #----------------------------------------------------------
# # Odoo Web helpers
# #----------------------------------------------------------
#
# db_list = http.db_list
#
# db_monodb = http.db_monodb
# class debrand(Database):
#     def _render_template(self, **d):
#         d.setdefault('manage', True)
#         d['insecure'] = odoo.tools.config.verify_admin_password('admin')
#         d['list_db'] = odoo.tools.config['list_db']
#         d['langs'] = odoo.service.db.exp_list_lang()
#         d['countries'] = odoo.service.db.exp_list_countries()
#         d['pattern'] = DBNAME_PATTERN
#         # databases list
#         d['databases'] = []
#         try:
#             d['databases'] = http.db_list()
#             d['incompatible_databases'] = odoo.service.db.list_db_incompatible(d['databases'])
#         except odoo.exceptions.AccessDenied:
#             monodb = db_monodb()
#             if monodb:
#                 d['databases'] = [monodb]
#         try:
#             d['company_name'] = 'MaxWare'
#             return env.get_template("database_manager_debrand.html").render(d)
#         except:
#             d['company_name'] = ''
#             return main.get_template("database_manager.html").render(d)
