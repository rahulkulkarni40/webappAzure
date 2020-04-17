# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:30:54 2020

@author: Rahul
"""
import json
# import flask
from flask import Flask, render_template, request
import pandas as pd
from flask_cors import CORS
from azure.storage.table import TableService

app = Flask(__name__)

app.config["DEBUG"] = False
CORS(app)

@app.route("/")
def index():
    return render_template("mainpage.html")

@app.route("/reg")
def reg():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("loginpage.html")

@app.route("/test")
def test():
    return render_template("test.html")

@app.route('/azpost/', methods=['POST'])
def post_data():
    result = json.dumps(request.form)
    result2 = json.loads(result)
    data_send = connection(result2, "", "insert")
    if data_send == "added Successfully!!!!":
        # flash('added Successfully!!!!')
        print(data_send)
        render_template("test.html")
        return str(data_send)
    else:
        return str(data_send)


@app.route('/azget/', methods=['post'])
def get_data():
    keys = request.form["keyname"]
    keys_value = request.form["keyval"]
   # print(keys, keys_value)
    query = keys + " eq " + "'" + keys_value + "'"
    #print(query)
    data_send = connection("", query, "reterive")
    data1 = data_send.to_json(orient='records')
    return data1


@app.route('/getrowid/<string:pkey>', methods=['get'])
def get_rowid(pkey):
   # print(pkey)
    keys = "PartitionKey"
    keys_value = pkey
   # print(keys, keys_value)
    query = keys + " eq " + "'" + keys_value + "'"
   # print(query)
    data_send = connection("", query, "reterive")
   # print(data_send)
    if len(data_send) == 0:
        return "0"
    else :
        data_send["RowKey"] = pd.to_numeric(data_send["RowKey"])
        newlist1 = data_send.sort_values(by="RowKey")
        newlist = newlist1.tail(1)
        print(newlist)
        id = newlist.iloc[0]["RowKey"]
    #print(str(id))
        return str(id)

@app.route('/getid/<string:id>', methods=['get'])
def get_id(id):
    #print(id)
    keys = "ID"
    keys_value = id
   # print(keys, keys_value)
    query = keys + " eq " + "'" + keys_value + "'"
   # print(query)
    data_send = connection("", query, "reterive")
   # print(data_send)
    if len(data_send) == 0:
        return "0"
    else :
        data_send["ID"] = pd.to_numeric(data_send["ID"])
        newlist1 = data_send.sort_values(by ="ID" )
        newlist = newlist1.tail(1)
        id = newlist.iloc[0]["ID"]
    #print(str(id))
        return str(id)
################################################ Registration API ############################################################################################

@app.route('/regpost/', methods=['POST'])
def post_reg_data():
    result = json.dumps(request.form)
    result2 = json.loads(result)
    data_send = regconnection(result2, "", "insert")
    if data_send == "added Successfully!!!!":
        # flash('added Successfully!!!!')
        print(data_send)
        render_template("test.html")
        return str(data_send)
    else:
        return str(data_send)

@app.route('/getusername/<string:pkey>,<string:uname>', methods=['get'])
def get_uname(pkey,uname):
   # print(pkey)
    keys = "PartitionKey"
    keys_value = pkey
    print(keys, keys_value)
    query = keys + " eq " + "'" + keys_value + "'"
    print(query)
    data_send = regconnection("", query, "reterive")
   # print(data_send)
    if len(data_send) == 0:
        return "No Data"
    else :
        unames = data_send['RowKey'].tolist()
        print(unames)
        if uname in unames:
            print("entered")
            return "already exists"
        else:
            return "No Data"


@app.route('/getpartations', methods=['get'])
def get_partitions():
    data_send = regconnection("", "", "all")
    #print(data_send.keys())
    partis = data_send["PartitionKey"].drop_duplicates()
    #print(partis)
    return partis.to_json()

@app.route('/getusername/<string:pkey>,<string:uname>,<string:pwd>', methods=['get'])
def get_logincheck(pkey,uname,pwd):
   # print(pkey)
    keys = "PartitionKey"
    keys_value = pkey
    #print(keys, keys_value)
    query = keys + " eq " + "'" + keys_value + "'" + "and RowKey eq '" + uname +"' and pwd eq '" + pwd + "'"
    #print(query)
    data_send = regconnection("", query, "reterive")
    #print(data_send)
    if len(data_send) == 0:
        return "No Data"
    else:
        return "Data"




################################################# API Connection LIST ##################################################################################################
acc_name = 'cloudshell1842093256'
acc_key = '8NzcW1lBIDxhiIv9VX+7OaH87/TKSo2JIMukfBi3a7Qyjrhb/tNSiKArGEkWub4qbmYsiAK9R9D0A+GQ0OvPRQ=='

table_service = TableService(account_name=acc_name, account_key=acc_key)
def connection(tasks, query, types):
    table_service.create_table('customer')
    if types == "insert":
       # print(tasks)
        table_service.insert_entity('customer', tasks)
        return "added Successfully!!!!"
    elif types == "reterive":
        # print(query)
        tasks = table_service.query_entities('customer', filter=query)
        df = pd.DataFrame(df_con(tasks))
        # print(data1)
        return df

def regconnection(tasks,query,types):
    table_service.create_table('customerdetails')
    if types == "insert":
        # print(tasks)
        table_service.insert_entity('customerdetails', tasks)
        return "added Successfully!!!!"
    elif types == "reterive":
        # print(query)
        tasks = table_service.query_entities('customerdetails', filter=query)
        df = pd.DataFrame(df_con(tasks))
        # print(data1)
        return df
    elif types == "all":
        tasks = table_service.query_entities('customerdetails')
        df = pd.DataFrame(df_con(tasks))
        return df

def df_con(tasks):
    for task in tasks:
        yield task


if __name__ == '__main__':
    app.run()
