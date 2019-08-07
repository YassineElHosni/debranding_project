# -*- coding: utf-8 -*-
from odoo import http
import os
import os.path
import glob

class Debranding-project(http.Controller):
@http.route([
'/web/test',
'/test',
], type='http', auth="none")
 
def suppressionMot(m,n,file):
	fileodoo=open(file, "r")# will probably need encoding='utf-8' to manage few errors
	contenu=fileodoo.read()
	traitement=""
	i=0
	size=len(m)
	taille=len(contenu)

	while i<taille:
		if contenu[i]==m[0]:

			if contenu[i:i+size]==m:
				traitement=contenu[0:i]+n+contenu[i+size:taille]
				taille=taille-size
				contenu=traitement
				i=i+size
			else :
				i=i+1
				
		i=i+1
	
	fileodoo.close()
	fileodoo=open(file, "w")
	fileodoo.write(contenu)
	fileodoo.close()


path ="../../"
files = []
 
files = [f for f in glob.glob(path +"**/i18n/*.po")] if "fr.po" in f or "ar.po" in f or "en_" in f]

for f in files:
    suppressionMot("Odoo","",f)
    suppressionMot("odoo","",f)
    suppressionMot("www.odoo.com","company-website",f)

files = [f for f in glob.glob(path +"/web/views/webclient_templates.xml") and f in glob.glob(path +"/web/views/databse_manager.html") ]
for f in files:
    suppressionMot("favicon.ico","",f)

def replaceOccurrencesInFile(oldText, newText, atFile):
    f = open(atFile, 'r')
    f_temp = open(atFile.split('.')[0]+"_temp.po", 'w')
    for line in f1:
        if("title" in line and "odoo" in line.lower()):
        	f_temp.write(line.replace(oldText, newText))
        else:
        	f_temp.write(line)
    f.close()
    f_temp.close()
    #the next two line work perfectly on my tests, but make sure to try them out carefully
    os.remove(atFile)
    os.rename(atFile.split('.')[0]+"_temp.po", atFile)

def editDialogs(oldText, newText):
	paths = [f for f in glob.glob("../../web/static/src/js/services/crash_manager.js") and f in glob.glob("../../web/static/src/js/core/dialog.js")]
	for f in path:
		replaceOccurrencesInFile(oldText, newText, f)

editDialogs('Odoo', 'debranded_Odoo')
