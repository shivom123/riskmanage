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
    print("paramsssss",params)
    cursor = connection.cursor()
    fields = []
    fields.append(('ID SERIAL PRIMARY KEY'))
    looper = int(params['risk[counter]'])
    print("looperrrrr",looper)
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
    print("tupleeee",tuple(fields))

    create_table_sql = "CREATE TABLE IF NOT EXISTS {} {}".format(table_name, tuple(fields)).replace("'", "")
    print("query",create_table_sql)
    cursor.execute(create_table_sql)
    try:
        print("looorer if",looper)
        list_field = {'keys': [], 'values': []}
        for count in range(0, looper):
            list_field['keys'].append((str2(params['risk[label[{}]]'.format(count)]) ))
            list_field['values'].append((params['risk[value[{}]]'.format(count)]))
        print(list_field)
        tab = "INSERT INTO {0} {1} VALUES {2}".format(table_name, tuple(list_field['keys']) , tuple(list_field['values']))
        print("insert query",tab)
        cursor.execute(tab)
    except Exception as e:
        print("excetpition",e)
        try:
            for count in range(0, looper):
                print("count",count)
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
    # print("xcvdfsd",data[-1])
    col = [i[0] for i in cursor.description]
    # print("col",col)
    return render(request, 'detail.html', {'data': data[0], 'col':col})

class str2(str):
    def __repr__(self):
        return ''.join(('"', super().__repr__()[1:-1], '"'))

