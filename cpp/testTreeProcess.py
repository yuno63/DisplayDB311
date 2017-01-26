#!/usr/bin/env python

from ctypes import *
import datetime

def unix_to_date(date):
    "converct unix timestamp (int) to date strig ('Y-m-d H:M:S')"
    return datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')


def date_to_unix(unix):
    "converct date strig ('Y-m-d H:M:S') to unix timestamp (int)"
    return int(datetime.datetime.strptime(unix, '%Y-%m-%d %H:%M:%S').strftime("%s"))

print "=============== test treeProcess ==================="

lib = cdll.LoadLibrary("./libTreeProcess.so")
names = ["TE0001", "TE0002", "TE0003", "TE0004",]

fn = "SensNamesTmp.txt"
file = open(fn,"w")
for name in names:
    file.write(name+"\n")
file.close()

lib.treeProcess(fn)
#treeSens = ROOT.TTree('treeSens','tree for selected sensors')

class TTree_new(object):
    def __init__(self):
        self.obj = lib.TTree_new()
    def SetName(self,name):
        lib.TTree_SetName(name)
    
treeSens = TTree_new()
#treeSens.SetName("TE0001")
#print "treeSens:", treeSens

