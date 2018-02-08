from django.shortcuts import render, redirect
from django.db import models
from .models import RiskName, create_model
from django.db import connection
import pdb;
import json, ast

# Create your views here.
def landingPage(request):
    risk_list = [ i.title for i in RiskName.objects.all()]
    return render(request, 'index.html', {'risk_list': risk_list})

def ManageModel(request):
    params = ast.literal_eval(json.dumps(request.POST))
    cursor = connection.cursor()
    fields = []
    fields.append(('ID SERIAL PRIMARY KEY'))
    looper = int(params['risk[counter]'])
    for count in range(0, looper):
        if params['risk[type[{}]]'.format(count)] == 'integer':
            print("integerrr")
            fields.append((' %s BIGINT')% params['risk[label[{}]]'.format(count)])

        if params['risk[type[{}]]'.format(count)] == 'string':
            print('string in')
            fields.append((' %s varchar(255)')% params['risk[label[{}]]'.format(count)])

        if params['risk[type[{}]]'.format(count)] == 'date':
            print('date in')
            fields.append((' %s DATE')% params['risk[label[{}]]'.format(count)])
        
    table_name = params['risk[model_name]'].lower().replace(" ", "_")

    create_table_sql = "CREATE TABLE IF NOT EXISTS {} {}".format(table_name, tuple(fields)).replace("'", "")
    cursor.execute(create_table_sql)
    try:
        print("looorer if",looper)
        list_field = {'keys': [], 'values': []}
        for count in range(0, looper):
            list_field['keys'].append((str2(params['risk[label[{}]]'.format(count)]) ))
            list_field['values'].append((params['risk[value[{}]]'.format(count)]))
        if len(list_field['keys']) == 1:
            tab = "INSERT INTO {0} {1} VALUES {2}".format(table_name, tuple(list_field['keys']), tuple(list_field['values'])).replace(",","")
            print("insert query",tab)
            cursor.execute(tab)
        else:
            tab = "INSERT INTO {0} {1} VALUES {2}".format(table_name, tuple(list_field['keys']), tuple(list_field['values']))
            print("insert query",tab)
            cursor.execute(tab)
    except Exception as e:
        try:
            for count in range(0, looper):
                alter_tab = "ALTER TABLE {0} ADD COLUMN {1} varchar(40)".format(table_name,params['risk[label[{}]]'.format(count)])
                cursor.execute(alter_tab)
                tab = "UPDATE {0} SET {1}='{2}'".format(table_name, params['risk[label[{}]]'.format(count)],params['risk[value[{}]]'.format(count)])
                cursor.execute(tab)
        except:
            for count in range(0, looper):
                tab = "UPDATE {0} SET {1}='{2}'".format(table_name, params['risk[label[{}]]'.format(count)],params['risk[value[{}]]'.format(count)])
                cursor.execute(tab)

    cursor.execute("SELECT * FROM {}".format(table_name))
    # data = cursor.fetchone()
    data = cursor.fetchall()
    col = [i[0] for i in cursor.description]
    return render(request, 'detail.html', {'data': data[0], 'col':col})

class str2(str):
    def __repr__(self):
        return ''.join(('"', super().__repr__()[1:-1], '"'))

def all_risks(request):
    risk_list = [ i.title for i in RiskName.objects.all()]
    return render(request, 'view_risks.html', {'risk_list': risk_list})

def single_type(request):
    print("singel")
    risk_name = RiskName.objects.get(id=1)
    return render(request, 'view_risks.html',{'risk':risk_name.title})