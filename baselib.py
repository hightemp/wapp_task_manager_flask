from jinja2 import Template, FunctionLoader, Environment, BaseLoader
from flask import render_template as render_template_default
from peewee import *
from playhouse.shortcuts import model_to_dict
import os
import zipfile

__DEBUG__ = False

def readfile(sFilePath):
    if (__DEBUG__):
        return open(sFilePath, 'rb').read()
    else:
        with zipfile.ZipFile(os.path.dirname(__file__)) as z:
            # print(z.namelist())
            with z.open(sFilePath) as f:
                print("[!] "+f.name)
                # print("[!] "+f.read().decode("utf-8"))
                return f.read()
        return "ERROR"

def load_template(name):
    return readfile("templates/"+name).decode("utf-8")

oTempFunctionLoader = FunctionLoader(load_template)

def render_template(name, **kwargs):
    if __DEBUG__:
        return render_template_default(name, **kwargs)
    else:
        data = load_template(name)
        tpl = Environment(loader=oTempFunctionLoader).from_string(data)
        return tpl.render(**kwargs)

def models_col_to_list(lModelsCol):
    lList = []
    for oA in lModelsCol:
        lList.append(model_to_dict(oA))

    return lList

# NOTE: Хелперы
def parse_get(args):
    data = {}

    for u, v in args.lists():
        if hasattr(v, "__len__"):
            for k in v:
                data[u] = k
                if k == '':
                    del data[u]
        else:
            data[u] = v
            if v == '':
                del data[u]

    return data

def parse_multi_form(form):
    data = {}
    for url_k, v in form.lists():
        if ('' in v):
            continue
        v = v[0]

        ks = []
        while url_k:
            if '[' in url_k:
                k, r = url_k.split('[', 1)
                ks.append(k)
                if r[0] == ']':
                    ks.append('')
                url_k = r.replace(']', '', 1)
            else:
                ks.append(url_k)
                break
        sub_data = data
        for i, k in enumerate(ks):
            if k.isdigit():
                k = int(k)
            if i+1 < len(ks):
                if not isinstance(sub_data, dict):
                    break
                if k in sub_data:
                    sub_data = sub_data[k]
                else:
                    sub_data[k] = {}
                    sub_data = sub_data[k]
            else:
                if isinstance(sub_data, dict):
                    sub_data[k] = v

    return data

def fnPrepareFormFields(aFields, cCls, sSelID):
    kls = globals()[cCls]
    oItem = {}
    if sSelID != "" and int(sSelID) > 0:
        try:
            oItem = kls.get_by_id(sSelID)
            oItem = model_to_dict(oItem, recurse=False, backrefs=False)
        except:
            pass

    for sK, oV in aFields.items():
        if 'sel_value' in aFields[sK]:
            aFields[sK]['value'] = aFields[sK]['sel_value']
        else:
            if sSelID==0:
                aFields[sK]['value'] = ''
            else:
                if sK in oItem and oItem[sK]:
                    aFields[sK]['value'] = oItem[oV['field_name']]
                else:
                    aFields[sK]['value'] = ''
    return aFields
