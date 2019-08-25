# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json
import os
import os.path
import glob


def replace_occurrences_in_file(old_text, new_text, at_file, theClue):
    f = open(at_file, 'r', encoding='utf-8')
    f_temp = open(at_file.split('.')[0] + "_temp.po", 'w')
    for line in f:
        if theClue in line and old_text in line.lower():
            f_temp.write(line.replace(old_text, new_text))
        else:
            f_temp.write(line)
    f.close()
    f_temp.close()
    # the next two line work perfectly on my tests, but make sure to try them out carefully
    os.remove(at_file)
    os.rename(at_file.split('.')[0] + "_temp.po", at_file)


def edit_dialogs(old_text, new_text):
    paths = [f for f in glob.glob("../../web/static/src/js/services/crash_manager.js") if
             f in glob.glob("../../web/static/src/js/core/dialog.js")]
    for f in paths:
        replace_occurrences_in_file(old_text, new_text, f, "title")


def edit_translations(old_text, new_text):
    paths = [f for f in glob.glob("../../*/i18n/*.po") if "fr.po" in f or "en_AU.po" in f or "en_GB" in f]
    for f in paths:
        replace_occurrences_in_file(old_text, new_text, f, "msg")


def debranding_parts(old_text, new_text):  # put all your debranding parts here

    # error + warnings dialogs
    edit_dialogs(old_text, new_text)
    # translations(ar, fr, en)
    edit_translations(old_text, new_text)


def debrand(new_odoo, json_file_name='../../../../debranding_config.json'):
    # check if json file exists
    if os.path.isfile(json_file_name):
        # get company_name
        with open(json_file_name, 'r') as f:
            data_store = json.load(f)
        # use it(the company_name from json) as target
        # print(data_store["company_name"]," as target and ",new_odoo," as replacement")

        debranding_parts(data_store["company_name"], new_odoo)
    else:
        # use default string "Odoo" as target
        # print("odoo as target and ",new_odoo," as replacement")

        debranding_parts('Odoo', new_odoo)

    # write changes
    data_store = {
        "company_name": new_odoo
    }
    with open(json_file_name, 'w') as f:
        json.dump(data_store, f)


debrand('debranded_Odoo')

# class debranding-project(models.Model):
#     _name = 'debranding-project.debranding-project'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
