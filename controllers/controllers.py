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
	fileodoo=open(file, "r")
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
 
files = [f for f in glob.glob(path +"**/i18n/*.po")]

for f in files:
    suppressionMot("Odoo","",f)
    suppressionMot("odoo","",f)
    suppressionMot("www.odoo.com","company-website",f)

files = [f for f in glob.glob(path +"/web/views/webclient_templates.xml") and f in glob.glob(path +"/web/views/databse_manager.html") ]
for f in files:
    suppressionMot("favicon.ico","",f)



