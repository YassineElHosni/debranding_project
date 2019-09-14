# -*- coding: utf-8 -*-
from odoo import models, fields, api
from . import polib
import json
import os
import os.path
import glob
import re

server_path = './'  # equal to server/
addons_path = server_path + 'odoo/addons'
web_path = addons_path + '/web'
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
    web_js_path = web_path + "/static/src/js"
    replace_occurrences_in_file(old_text, new_text, web_js_path + "/services/crash_manager.js", "title")
    replace_occurrences_in_file(old_text, new_text, web_js_path + "/core/dialog.js", "title")


def po_replace_msgsr(old_text, new_text, file):
    text_found_count = 0
    po = polib.pofile(file)
    for entry in po:
        if old_text in entry.msgstr:
            entry.msgstr = entry.msgstr.replace(old_text, new_text)
            text_found_count = text_found_count + 1
    if text_found_count > 0:
        po.save()


def edit_translations(old_text, new_text):  # needs testing
    paths = [f for f in glob.glob(addons_path + "/*/i18n/*.po") if "fr.po" in f or "en_AU.po" in f or "en_GB" in f]
    for f in paths:
        # replace_occurrences_in_file(old_text, new_text, f, "msgstr")
        po_replace_msgsr(old_text, new_text, f)


def edit_community_color(new_color):
    web_scss_path = web_path + '/static/src/scss/'
    replace_occurrences_in_file(0, new_color, web_scss_path + 'primary_variables.scss', '$o-community-color', 12)
    replace_occurrences_in_file(0, new_color, web_scss_path + 'fields_extra.scss', 'color', 28)
    replace_occurrences_in_file(0, new_color, web_scss_path + 'form_view_extra.scss', 'color', 72)


def get_community_color():  # get form scss file
    web_scss_path = web_path + '/static/src/scss/'
    with open(web_scss_path + 'primary_variables.scss', 'r') as f:
        for line_index, line in enumerate(f, start=1):
            if line_index == 12 and '$o-community-color' in line:
                return line.split('#')[len(line.split('#')) - 1].replace(';', '')


def edit_head_title(old_text, new_text):
    head_title_paths = [web_path + '/views/webclient_templates.xml', web_path + '/views/database_manager.html']
    for path in head_title_paths:
        if old_text.lower() == 'odoo':
            replace_occurrences_in_file('<title t-esc="title or \''+old_text+'\'"/>',  # NEED RETHINKING!
                                        '<title t-esc="title or \''+new_text+'\'"/>', path, '<title')
        else:
            replace_occurrences_in_file(old_text, new_text, path, '<title>')  # NEED RETHINKING!


def replace_database_manager_html():
    target_file_path = web_path + '/views/database_manager.html'
    debrand_file_path = addons_path + '/debranding_project/views/database_manager_debrand.html'
    if not os.path.isfile(target_file_path.replace('.html', '_old.html')):
        if os.path.isfile(target_file_path) and os.path.isfile(debrand_file_path):
            with open(debrand_file_path, 'r') as f:
                file_content = f.read()

            # rename target file to keep untouched
            os.rename(target_file_path, target_file_path.replace('.html', '_old.html'))

            # create new file
            with open(target_file_path, "w") as f:
                f.write(file_content)


def edit_favicon():
    favicon_path = web_path + '/static/src/img/favicon.ico'
    if not os.path.isfile(favicon_path.replace('.ico', '_old.ico')):
        os.rename(favicon_path, favicon_path.replace('.ico', '_old.ico'))

    favicon_path = web_path + '/static/src/img/logo.png'
    if not os.path.isfile(favicon_path.replace('.png', '_old.png')):
        os.rename(favicon_path, favicon_path.replace('.png', '_old.png'))

    favicon_path = web_path + '/static/src/img/logo2.png'
    if not os.path.isfile(favicon_path.replace('.png', '_old.png')):
        os.rename(favicon_path, favicon_path.replace('.png', '_old.png'))

    favicon_path = web_path + '/static/src/img/logo_inverse_white_206px.png'
    if not os.path.isfile(favicon_path.replace('.png', '_old.png')):
        os.rename(favicon_path, favicon_path.replace('.png', '_old.png'))


def debranding_parts(old_text, new_text, new_color, db_manager_was_replaced):  # put all your debranding parts here
    if not db_manager_was_replaced:  # HAS TO RUN ONCE AND BEFORE edit_head_title function.
        # only removes odoo from database manager/selector, meaning no replacing with new text, just turning odooless..
        replace_database_manager_html()  # TESTED
        # rename favicon file.. this change will only happen at next server reset.
        edit_favicon()  # TESTED

    if old_text != new_text:
        # error + warnings dialogs
        edit_dialogs(old_text, new_text)
        # translations(ar, fr, en)
        edit_translations(old_text, new_text)  # TESTED
        # title
        edit_head_title(old_text, new_text)  # NEEDS TESTING! # NEED RETHINKING!
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

        debranding_parts(old_data_store["company_name"], new_odoo, new_color, True)
    else:
        # use default string "Odoo" as target
        # print("odoo as target and ",new_odoo," as replacement")

        debranding_parts('Odoo', new_odoo, new_color, False)

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
def get_data_values():  # get form json file
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

    x_company_name = fields.Char(string='Brand Name',
                                 store=True,
                                 readonly=False,
                                 required=True)
    x_color = fields.Char(string="Brand Color",
                          store=True,
                          readonly=False,
                          required=True)

    # x_company_logo = fields.Binary(
    #                     string="Brand Logo",
    #                     required=True)

    @api.model
    def get_values(self):
        res = super(changer_backend_config, self).get_values()
        data_values = get_data_values()
        res.update(
            x_company_name=data_values["company_name"],
            x_color=data_values["color"],
        )
        return res

    @api.multi
    def set_values(self):
        debrand(self.x_company_name, self.x_color)
        super(changer_backend_config, self).set_values()
        self.env.ref('debranding_project.res_config_settings_view_form').write({'x_company_name': self.x_company_name,
                                                                                'x_color': self.x_color})

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
