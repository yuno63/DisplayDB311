import os, sys
from django import forms
from django.conf import settings
import datetime, time
from db import unix_to_date, date_to_unix, DB311, releaseDB_CERN  #, DataBase, propsDB


def getValueDB(time_now=time.time(), db=0, dbNames={}):    
    names = dbNames['nameTables']
    [value, time, u_time, minY, maxY] = \
        db.get_content(names, time_now-1800., time_now, 'pvss', dbNames)
    dbValue = {}
    for name in names:
        if len(value[name])>0:
            dbValue[name] = str(value[name][-1])
            timeVal = time[name][-1]
        else:
            dbValue[name] = 'N/A'
            timeVal = 'N/A'
    print 'name:', name, '     time:',timeVal, '     val:', dbValue[name]
    return dbValue        
            

class DisplayForm(forms.Form):
    print "===== DisplayForm ======"
    # start-stop times
    dt_days = 1 # days
    shift = 0  # days
    if releaseDB_CERN == "old":
        shift = 90
    time_interval = 10  # min
    repetition_db_access = 10  # sec
    time_monitor_shift = shift # days
    time_monitor_shift_unix = time_monitor_shift*86400
    time_table_shift = shift # days
    time_table_shift_unix = time_table_shift*86400
    
    now_str=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now_unix = round(date_to_unix(now_str))
    
    time_monitor_access_unix = now_unix-time_monitor_shift_unix
    time_monitor_access_str = unix_to_date(time_monitor_access_unix)
    
    time_table_access_unix = now_unix-time_table_shift_unix
    time_table_access_str = unix_to_date(time_table_access_unix)

    now_unix -= time_monitor_shift*86400 
    now_str = unix_to_date(now_unix)

    print "now_str:", now_str
    print "now_unix:", now_unix
    start_unix = now_unix - dt_days*86400
    start_str = unix_to_date(start_unix)
    print "start_str:", start_str
    print "start_unix:", start_unix

    # DB processing
    #if 'cern.ch' in os.getcwd():
        #host="wa105cpu0001.cern.ch"
    #else:
        #host="localhost"
    #db = DataBase(host=host,
                  #user="wa105",
                  #password="Wa105-2016",
                  #db="wa105_sc")
    
    #db = DB311
    dbNames = DB311.get_db_names()
    #print '\ndbNames.keys():', dbNames.keys()
    nameTables = dbNames['nameTables']
    categorie_names = dbNames["categorie_names"]
    dbNamesDB = dbNames["db_name"]
    dbNamesDBraw = dbNames["name"]
    dbNamesPVSS = dbNames["pvss_name"]

    dbNamesExp = dbNames["exp"]
    dbNamesStatus = dbNames["statusitem"]
    dbNamesDescript = dbNames["description"]
    dbNamesID = dbNames["paramid"]
    
    category_name_active = categorie_names[0] # "All"
    pvss_status = True
    sensor_filter = ""
    if pvss_status:
        names_PVSS_DB = "namesPVSS"
    else:
        names_PVSS_DB = "namesDB"
    
    dbValue =  getValueDB(time_now=time_table_access_unix, \
        db=DB311, dbNames=dbNames)
    
    tabNames = ['disp','monit','tabl','3D','file']
    tabTitles = ['Graph','Live','Table','3D','File']
    tabName_active = 'disp'
    tabDict = {}
    for key, val in zip(tabNames,tabTitles):
        tabDict[key] = val

