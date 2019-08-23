# -*- coding: utf-8 -*-
from odoo import http
import os
import os.path
import glob
import json

class Debranding-project(http.Controller):
@http.route([
'/web/test',
'/test',
], type='http', auth="none")

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

def replaceOccurrencesInFile(oldText, newText, atFile, theClue):
    f = open(atFile, 'r', encoding='utf-8')
    f_temp = open(atFile.split('.')[0]+"_temp.po", 'w')
    for line in f:
        if(theClue in line and oldText in line.lower()):
        	f_temp.write(line.replace(oldText, newText))
        else:
        	f_temp.write(line)
    f.close()
    f_temp.close()
    # the next two line work perfectly on my tests, but make sure to try them out carefully
    os.remove(atFile)
    os.rename(atFile.split('.')[0]+"_temp.po", atFile)

def editDialogs(oldText, newText):
	paths = [f for f in glob.glob("../../web/static/src/js/services/crash_manager.js") and f in glob.glob("../../web/static/src/js/core/dialog.js")]
	for f in paths:
		replaceOccurrencesInFile(oldText, newText, f, "title")

def editTranslations(oldText, newText):
	paths = [f for f in glob.glob("../../*/i18n/*.po") if "fr.po" in f or "en_AU.po" in f or "en_GB" in f]
	for f in paths:
		replaceOccurrencesInFile(oldText, newText, f, "msg")

def debrandingParts(oldText, newText): #put all your debranding parts here

        # error + warnings dialogs
        editDialogs(oldText, newText)
        # translations(ar, fr, en)
        editTranslations(oldText, newText)


def debrand(newOdoo, jsonfilename = '../../../../debrandingConfig.json'):
    # check if json file exists
    if os.path.isfile(jsonfilename):
        # get company_name
        with open(jsonfilename, 'r') as f:
            datastore = json.load(f)
        # use it(the company_name from json) as target
        # print(datastore["company_name"]," as target and ",newOdoo," as replacement")

        debrandingParts(datastore["company_name"], newOdoo)
    else:
        # use default string "Odoo" as target
        # print("odoo as target and ",newOdoo," as replacement")

        debrandingParts('Odoo', newOdoo)

    # write changes
    datastore = {
        "company_name": newOdoo
    }
    with open(filename, 'w') as f:
        json.dump(datastore, f)

debrand('debranded_Odoo')