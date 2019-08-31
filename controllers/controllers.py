# -*- coding: utf-8 -*-
from odoo import http
import os
import os.path
import glob
import json

# class Debranding-project(http.Controller):
# @http.route([
# '/web/test',
# '/test',
# ], type='http', auth="none")

# too complexe, makes it hard to edit, plus as a wise man said:
#	"never waste time creating what already exists, understand it and make of it something better"
# def suppressionMot(m,n,file):
# 	fileodoo=open(file, "r")# will probably need encoding='utf-8' to manage few errors
# 	contenu=fileodoo.read()
# 	traitement=""
# 	i=0
# 	size=len(m)
# 	taille=len(contenu)

# 	while i<taille:
# 		if contenu[i]==m[0]:

# 			if contenu[i:i+size]==m:
# 				traitement=contenu[0:i]+n+contenu[i+size:taille]
# 				taille=taille-size
# 				contenu=traitement
# 				i=i+size
# 			else :
# 				i=i+1
				
# 		i=i+1
	
# 	fileodoo.close()
# 	fileodoo=open(file, "w")
# 	fileodoo.write(contenu)
# 	fileodoo.close()


#path ="../../"
# files = []
 
# files = [f for f in glob.glob(path +"**/i18n/*.po") if "fr.po" in f or "ar.po" in f or "en_" in f]

# for f in files:
#     suppressionMot("Odoo","",f)
#     suppressionMot("odoo","",f)
#     suppressionMot("www.odoo.com","company-website",f)

#this is wrong, we should not delete the favicon.icon text from these views, we only need to replace the /web/static/src/favicon.icon with the new company icon or just delete that file.
# files = [f for f in glob.glob(path +"/web/views/webclient_templates.xml") and f in glob.glob(path +"/web/views/databse_manager.html") ]
# for f in files:
#     suppressionMot("favicon.ico","",f)

# def replaceOccurrencesInFile(oldText, newText, atFile, theClue):
#     f = open(atFile, 'r', encoding='utf-8')
#     f_temp = open(atFile.split('.')[0]+"_temp.po", 'w')
#     for line in f:
#         if(theClue in line and oldText in line.lower()):
#         	f_temp.write(line.replace(oldText, newText))
#         else:
#         	f_temp.write(line)
#     f.close()
#     f_temp.close()
#     # the next two line work perfectly on my tests, but make sure to try them out carefully
#     os.remove(atFile)
#     os.rename(atFile.split('.')[0]+"_temp.po", atFile)
# 
# def editDialogs(oldText, newText):
# 	paths = [f for f in glob.glob("../../web/static/src/js/services/crash_manager.js") and f in glob.glob("../../web/static/src/js/core/dialog.js")]
# 	for f in paths:
# 		replaceOccurrencesInFile(oldText, newText, f, "title")
# 
# def editTranslations(oldText, newText):
# 	paths = [f for f in glob.glob("../../*/i18n/*.po") if "fr.po" in f or "en_AU.po" in f or "en_GB" in f]
# 	for f in paths:
# 		replaceOccurrencesInFile(oldText, newText, f, "msg")
# 
# def debrandingParts(oldText, newText): #put all your debranding parts here
# 
#         # error + warnings dialogs
#         editDialogs(oldText, newText)
#         # translations(ar, fr, en)
#         editTranslations(oldText, newText)
# 
# 
# def debrand(new_odoo, jsonfilename = '../../../../debrandingConfig.json'):
#     # check if json file exists
#     if os.path.isfile(jsonfilename):
#         # get company_name
#         with open(jsonfilename, 'r') as f:
#             datastore = json.load(f)
#         # use it(the company_name from json) as target
#         # print(datastore["company_name"]," as target and ",new_odoo," as replacement")
# 
#         debrandingParts(datastore["company_name"], new_odoo)
#     else:
#         # use default string "Odoo" as target
#         # print("odoo as target and ",new_odoo," as replacement")
# 
#         debrandingParts('Odoo', new_odoo)
# 
#     # write changes
#     datastore = {
#         "company_name": new_odoo
#     }
#     with open(filename, 'w') as f:
#         json.dump(datastore, f)
# 
# debrand('debranded_Odoo')


import json
import odoo
import os
import sys
import jinja2
from odoo import http, tools
from odoo.addons.web.controllers.main import Database, Binary
from django.shortcuts import render


if hasattr(sys, 'frozen'):
    # When running on compiled windows binary, we don't have access to package loader.
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'views'))
    loader = jinja2.FileSystemLoader(path)
else:
    loader = jinja2.PackageLoader('odoo.addons.web', "views")

env = jinja2.Environment(loader=loader, autoescape=True)
env.filters["json"] = json.dumps

# 1 week cache for asset bundles as advised by Google Page Speed
BUNDLE_MAXAGE = 60 * 60 * 24 * 7

DBNAME_PATTERN = '^[a-zA-Z0-9][a-zA-Z0-9_.-]+$'

#----------------------------------------------------------
# Odoo Web helpers
#----------------------------------------------------------

db_list = http.db_list

db_monodb = http.db_monodb
class debrand(Database):
    def _render_template(self, **d):
        d.setdefault('manage', True)
        d['insecure'] = odoo.tools.config.verify_admin_password('admin')
        d['list_db'] = odoo.tools.config['list_db']
        d['langs'] = odoo.service.db.exp_list_lang()
        d['countries'] = odoo.service.db.exp_list_countries()
        d['pattern'] = DBNAME_PATTERN
        # databases list
        d['databases'] = []
        try:
            d['databases'] = http.db_list()
            d['incompatible_databases'] = odoo.service.db.list_db_incompatible(d['databases'])
        except odoo.exceptions.AccessDenied:
            monodb = db_monodb()
            if monodb:
                d['databases'] = [monodb]
        try:
            d['company_name'] = 'MaxWare'
            d['company_url'] = 'https/:www.maxware.ma'
            d['favicon_url'] = ''
            d['logo_url'] = ''
            return env.get_template("database_manager_debrand.html").render(d)
        except:
            d['company_name'] = ''
            d['company_url'] = ''
            d['favicon_url'] = ''
            d['logo_url'] = ''
            return env.get_template("database_manager.html").render(d)
