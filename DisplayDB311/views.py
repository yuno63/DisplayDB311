from django.http import HttpResponse

from django.shortcuts import render, redirect#, direct_to_template
from django.template import Template, Context
from django.utils.encoding import force_text
import forms
from db import unix_to_date, date_to_unix, DB311 #, DataBase
import os, sys, json, time, datetime
import numpy
import ROOT

def display(request):
    print "====== display ========"
    form = forms.DisplayForm(request.GET)
    
    context = {
        "nameTables" : form.nameTables,
        "names_PVSS_DB" : form.names_PVSS_DB,
        "dbNamesPVSS" : form.dbNamesPVSS,
        "dbNamesDB" : form.dbNamesDB,
        "dbNamesDBraw" : form.dbNamesDBraw,
        "dbNamesDescript" : form.dbNamesDescript,
        "dbNamesExp" : form.dbNamesExp,
        "dbNamesStatus" : form.dbNamesStatus,
        "dbNamesID" : form.dbNamesID,
        "dbValue" : form.dbValue,
        "categorie_names" : form.categorie_names,
        "category_name_active" : form.category_name_active,
        "sensor_filter" : form.sensor_filter,
        "pvss_status" : form.pvss_status,
        "now_str" : form.now_str,
        "now_unix" : form.now_unix,
        "start_str" : form.start_str,
        "start_unix" : form.start_unix,
        "time_monitor_shift" : form.time_monitor_shift,
        "time_monitor_access_str" : form.time_monitor_access_str,
        "time_table_shift" : form.time_table_shift,
        "time_table_access_str" : form.time_table_access_str,
        "time_interval" : form.time_interval,
        "repetition_db_access" : form.repetition_db_access,
        "tabNames" : form.tabNames,
        "tabTitles" : form.tabTitles,
        "tabDict" : form.tabDict,
        "tabName_active" : form.tabName_active,
    }
    return render(request, 'display.html', context)
    
def draw(request):
    print "======= draw ========="
    if request.method == 'POST':
        mode = request.POST['mode']
        mode = eval(mode)
        print 'mode:', mode, '  type:', type(mode)
        names = request.POST['names']
        pvss_db = request.POST['pvss_db']
        len_array_max = 300
        #print "--- 1 ----"
        if (mode=="draw") or (mode=="save"):
            time1 = request.POST['time1']
            time2 = request.POST['time2']
            if mode=="save":
                file_name = request.POST['file_name']
                print "  ---- mode:", mode, ",   file_name:", file_name
                len_array_max = int(1e6)
        if mode=="monitor":
            time_interval = request.POST['time_interval']
            time_monitor_shift = request.POST['time_monitor_shift']

            time_monitor_shift = eval(time_monitor_shift)
            time_monitor_shift = float(time_monitor_shift)
            #print 'time_monitor_shift:', time_monitor_shift, 'type:', type(time_monitor_shift)
            time_monitor_shift_unix = time_monitor_shift*86400
            time2 = time.time()-time_monitor_shift_unix
            time2 = round(time2)
            #print 'time2:', time2
            
            time_interval = str(time_interval)
            time_interval = float(time_interval) # min
            
            print 'time_interval:', time_interval, "   type:", type(time_interval)
            time1 = time2-time_interval*60
            time1 = round(time1)
        namesRequest = eval(names)
        pvss_db = eval(pvss_db)
        print 'time1:', time1
        print 'time2:', time2
        print 'pvss_db:', pvss_db

        dbNames = DB311.get_db_names()
        names = [name for name in namesRequest if name in dbNames['nameTables']]
        #print 'namesRequest:', namesRequest
        print 'names:', names
        if len(names)==0:       
            return HttpResponse(json.dumps({"nothing to see": "go home"}),
            content_type="application/json")
        outDB = DB311.get_content(names, time1, time2, pvss_db, dbNames, len_array_max)
        if mode=="save":
            treeSens = ROOT.TTree('treeSens','tree for selected sensors')
            dictVal_np, dictTime_np, dictN = {}, {}, {} 
            for name in names:
                valSens = outDB[0][name]
                timeSens = outDB[2][name]
                lenSens = len(valSens)
                print "name:", name, lenSens
                dictTime_np[name] = numpy.ndarray([lenSens],dtype=numpy.float32)
                dictVal_np[name] = numpy.ndarray([lenSens],dtype=numpy.float32)
                dictN[name] = numpy.ndarray([1],dtype=numpy.int32)
                dictN[name][0] = lenSens
                for i in xrange(lenSens):
                    dictVal_np[name][i] = valSens[i]
                    dictTime_np[name][i] = timeSens[i]
                print "dictVal_np[name]:", dictVal_np[name]
                treeSens.Branch("n_"+name, dictN[name], "n_"+name+"/I")
                treeSens.Branch(name+"_time", dictTime_np[name], name+"_time[n_"+name+"]/F")
                treeSens.Branch(name+"_val", dictVal_np[name], name+"_val[n_"+name+"]/F")
            treeSens.Fill()
            #treeSens.Print()
            #treeSens.Show(0)
            BASE_DIR = os.path.dirname(os.path.dirname(__file__))
            fnSaved = "file://" + BASE_DIR + "/tmp_root_files/" + file_name + ".root"
            print "fnSaved:", fnSaved
            fileSaved = ROOT.TFile(fnSaved,'recreate')
            treeSens.Write('',ROOT.TObject.kOverwrite)
            fileSaved.Close()

            content = {
                'tree': [],#treeSens,
                'fnSaved': fnSaved,
                }
            return HttpResponse(json.dumps(content), 
                content_type="application/json")
        else:
            if outDB[0]=={}:       
                return HttpResponse(json.dumps({"nothing to see": "go home"}),
                content_type="application/json")

            yy = [outDB[0][name] for name in names]
            #time_str = [outDB[1][name] for name in names]
            u_time = [outDB[2][name] for name in names]
            minY, maxY = outDB[3], outDB[4]
            print 'minY:', minY, '  maxY:', maxY
            print 'len(yy[0]):', len(yy[0]), 'len(u_time[0]):', len(u_time[0])#, 'len(time_str[0]):', len(time_str[0])
            time_shift = 0 #3*3600
            if isinstance(time1,(str,unicode)):
                minT = date_to_unix(time1) - time_shift
                maxT = date_to_unix(time2) - time_shift
                minTstr, maxTstr = time1, time2
            else:
                minT, maxT = time1 - time_shift, time2 - time_shift
                minTstr = unix_to_date(time1)
                maxTstr = unix_to_date(time2)
            print 'minT:', minT, '  maxT:', maxT

            #xlabels, xsForLabels = [], []
            ##print "--- 1 ----"
            #for i in xrange(len(time_str)):
                #for k in xrange(len(time_str[i])):
                    #u_time[i][k] -= time_shift #0.#minT
                    #try:
                        #xsForLabels.index(u_time[i][k])
                    #except:
                        #xsForLabels.append(u_time[i][k])
                        #xlabels.append(time_str[i][k])
            ##print "--- 2 ----"

            #xx, quantity, npoints = [], [], []
            #for i in xrange(len(names)):
                #xx.append(u_time[i]) 
                #quantity.append('')
                #npoints.append(len(u_time[i])),
            
            content = {
                'names': names,
                'xx': u_time,
                'yy': yy,
                #'time_str': time_str,
                'num_gr': len(names),
                'minY': minY,
                'maxY': maxY,
                'minX': minT, #0.,
                'maxX': maxT,#-minT,
                'minTstr': minTstr,
                'maxTstr': maxTstr,
                #'xlabels': xlabels,
                #'xsForLabels': xsForLabels,
                }
        print '\n\ncontent:'#, content
        for key in content.keys():
            print '\n', key, ':', content[key]

        return HttpResponse(json.dumps(content), 
            content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "go home"}),
            content_type="application/json")
    
def table(request):
    print "======= table ========="
    print request
    if request.method == 'POST':
        time_table_shift = request.POST['time_table_shift']
        time_table_shift = eval(time_table_shift)
        time_table_shift = float(time_table_shift)
        #print 'time_table_shift:', time_table_shift, 'type:', type(time_table_shift)
        time_table_shift_unix = time_table_shift*86400
        time_access = time.time()-time_table_shift_unix
        print 'time_access:', time_access
        time_table_access_str = unix_to_date(time_access)

        dbNames = DB311.get_db_names()
        dbValue =  forms.getValueDB(time_now=time_access, db=DB311, dbNames=dbNames)

        return HttpResponse(
            #json.dumps({"html": ren_template}), content_type="application/json"
            json.dumps({'dbValue': dbValue,'time_table_access_str': time_table_access_str,}), \
                content_type="application/json"
        )
    else:
        return HttpResponse(json.dumps({"nothing to see": "go home"}),
            content_type="application/json")
        