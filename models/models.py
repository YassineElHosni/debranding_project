# -*- coding: utf-8 -*-
from odoo import models, fields, api
import json
import os
import os.path
import glob
import re

server_path = './'  # equal to server/
addons_path = server_path + 'odoo/addons'
json_file_name = server_path + 'debranding_config.json'


# <editor-fold desc="changer backend code">
def replace_occurrences_in_file(old_text, new_text, at_file, theClue, target_line_num=-1):
    f = open(at_file, 'r')
    file_url_no_extension = at_file.split('.')[len(at_file.split('.')) - 2]
    file_extension = at_file.split('.')[len(at_file.split('.')) - 1]
    temp_file_full_url = "." + file_url_no_extension + "_temp." + file_extension
    f_temp = open(temp_file_full_url, 'w', encoding='utf-8')

    for line_num, line in enumerate(f, start=1):
        if target_line_num is not -1:
            if target_line_num == line_num and theClue in line:
                f_temp.write(re.sub('#.*', '#' + new_text + ';', line))
            else:
                f_temp.write(line)
        else:
            if theClue in line and old_text.lower() in line.lower():
                f_temp.write(line.replace(old_text, new_text))
            else:
                f_temp.write(line)

    f.close()
    f_temp.close()
    # the next two line work perfectly on my tests, but make sure to try them out carefully
    os.remove(at_file)
    os.rename(temp_file_full_url, at_file)


def edit_dialogs(old_text, new_text):
    web_js_path = addons_path + "/web/static/src/js"
    replace_occurrences_in_file(old_text, new_text, web_js_path + "/services/crash_manager.js", "title")
    replace_occurrences_in_file(old_text, new_text, web_js_path + "/core/dialog.js", "title")


def edit_translations(old_text, new_text):  # needs fixing
    paths = []  # [f for f in glob.glob(addons_path + "/*/i18n/*.po")
    # if "fr.po" in f or "en_AU.po" in f or "en_GB" in f]
    for f in paths:
        replace_occurrences_in_file(old_text, new_text, f, "msgstr")


def edit_community_color(new_color):
    web_scss_path = addons_path + '/web/static/src/scss/'
    replace_occurrences_in_file(0, new_color, web_scss_path + 'primary_variables.scss', '$o-community-color', 12)
    replace_occurrences_in_file(0, new_color, web_scss_path + 'fields_extra.scss', 'color', 28)
    replace_occurrences_in_file(0, new_color, web_scss_path + 'form_view_extra.scss', 'color', 72)


def get_community_color():  # get form scss file
    web_scss_path = addons_path + '/web/static/src/scss/'
    with open(web_scss_path + 'primary_variables.scss', 'r') as f:
        for line_index, line in enumerate(f, start=1):
            if line_index == 12 and '$o-community-color' in line:
                return line.split('#')[len(line.split('#')) - 1].replace(';', '')


def debranding_parts(old_text, new_text, new_color):  # put all your debranding parts here

    # error + warnings dialogs
    if old_text != new_text:
        edit_dialogs(old_text, new_text)
    # translations(ar, fr, en)
    # edit_translations(old_text, new_text)  # NEED FIXING!
    # community color changer
    if new_color != get_community_color():
        edit_community_color(new_color)  # TESTED


def debrand(new_odoo, new_color):
    # check if json file exists
    if os.path.isfile(json_file_name):
        # get company_name
        with open(json_file_name, 'r') as f:
            old_data_store = json.load(f)
        # use it(the company_name from json) as target
        # print(data_store["company_name"]," as target and ",new_odoo," as replacement")

        debranding_parts(old_data_store["company_name"], new_odoo, new_color)
    else:
        # use default string "Odoo" as target
        # print("odoo as target and ",new_odoo," as replacement")

        debranding_parts('Odoo', new_odoo, new_color)

    # write changes
    data_store = {
        "company_name": new_odoo,
        "color": new_color
    }
    with open(json_file_name, 'w') as f:
        json.dump(data_store, f)
    return data_store


# debrand('debranded_Odoo')
# </editor-fold>

# <editor-fold desc="changer config settings">
def get_x_company_name():  # get form json file
    data_store = {
        "company_name": 'Odoo',
        "color": '7C7BAD'
    }
    if os.path.isfile(json_file_name):
        with open(json_file_name, 'r') as f:
            data_store = json.load(f)

        return data_store
    else:
        return data_store


class changer_backend_config(models.TransientModel):
    _inherit = 'res.config.settings'

    x_company_name = fields.Char(string='Branding Name',
                                 store=True,
                                 readonly=False,
                                 required=True)
    x_color = fields.Char(string="Brand Color",
                          store=True,
                          readonly=False,
                          required=True)

    @api.model
    def get_values(self):
        res = super(changer_backend_config, self).get_values()
        data_values = get_x_company_name()
        res.update(
            x_company_name=data_values["company_name"],
            x_color=data_values["color"],
        )
        return res

    @api.multi
    def set_values(self):
        debrand(self.x_company_name, self.x_color)
        super(changer_backend_config, self).set_values()
        self.env.ref('res_config_settings_view_form').write({'x_company_name': self.x_company_name})
        self.env.ref('res_config_settings_view_form').write({'x_color': self.x_color})

    # @api.depends('x_company_name', 'x_color')
    # def set_x_company_name(self):
    #     return debrand(self.x_company_name, self.x_color)
    # data_store = {
    #     "company_name": self.x_company_name
    # }
    # if os.path.isfile(json_file_name):
    # get company_name
    # with open(json_file_name, 'r') as f:
    #     old_data_store = json.load(f)
    # use it(the company_name from json) as target
    # print(data_store["company_name"]," as target and ",new_od00," as replacement")

    # debrand(data_store["company_name"], new_od00)
    # else:
    # use default string "Odoo" as target
    # print("odoo as target and ",new_od00," as replacement")

    # debrand('Odoo', new_od00)

    # with open(json_file_name, 'w') as f:
    #     json.dump(data_store, f)
    # return data_store
# </editor-fold>
