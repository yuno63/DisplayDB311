import os, sys
import MySQLdb
import datetime
import copy
#from django.utils.datastructures import SortedDict

# DB properties
releaseDB_CERN = "old"  # "old" - (before 1 Dec 2016), "new" - (after 1 Dec 2016)

user = "wa105"
password = "Wa105-2016"
nameDB = "wa105_sc"
port = 0

if 'cern.ch' in os.getcwd():
    if releaseDB_CERN == "old":
        host = "wa105cpu0001.cern.ch"
    else:
        host = "dbod-wa105-sc.cern.ch"
        user = "admin"
        password = "Neutri2016"
        port = 5513
else:
    host="localhost"

propsDB = {"host":host, "user":user,"password":password, "nameDB":nameDB, "port":port}

def unix_to_date(date):
    "converct unix timestamp (int) to date strig ('Y-m-d H:M:S')"
    return datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')


def date_to_unix(unix):
    "converct date strig ('Y-m-d H:M:S') to unix timestamp (int)"
    return int(datetime.datetime.strptime(unix, '%Y-%m-%d %H:%M:%S').strftime("%s"))

def getDataFromCursor(cmd, cursor, ind=0, typ=''):
    cursor.execute(cmd)
    data =  cursor.fetchall()
    #print data
    if typ=='str':
        return [str(d[ind]) for d in data]
    elif typ=='float':
        return [float(d[ind]) for d in data]
    else:
        return [d[ind] for d in data]

class DataBase:
    def __init__(self, host, user, password, db, port):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port

    def get_db_names(self):
        "Returns names of all categories"

        db = MySQLdb.connect(self.host,
                             self.user,
                             self.password,
                             self.db,
                             self.port)

        cursor = db.cursor()
        dbNames = {}
        
        dbNames['nameTables'] = getDataFromCursor("show tables;",cursor,ind=0,typ='str')
        del dbNames['nameTables'][dbNames['nameTables'].index('PARAM_NAME')]
        
        cursor.execute("describe PARAM_NAME;")
        data =  cursor.fetchall()
        categorie_names = []
        for dt in data:
            if "categorie" in dt:
                categorie_names = eval('['+dt[1][5:-1]+']')
        categorie_names.insert(0,"All")
        dbNames["categorie_names"] = categorie_names
        
        cmd = "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'PARAM_NAME' ORDER BY ORDINAL_POSITION;"
        #print cmd
        fields = getDataFromCursor(cmd,cursor,ind=0,typ='str')
        #print 'fields:', fields
        for field in fields: 
            if field=='categorie': continue
            #print "\n  =======", field, "=========="
            pref = "select " + field + " from PARAM_NAME"
            dbField = {}
            for name in categorie_names:
                if name=="All":
                    cmd = pref+";"
                else:
                    cmd = pref+" where categorie='"+name+"';"
                #print "\n", cmd
                dbField[name] = getDataFromCursor(cmd,cursor,ind=0,typ='str')
                #print "\n\n=== field:", field
                #print "===dbField[", name, "]:", dbField[name][:5]
            dbNames[field] = dbField
        # correct empty names
        dbNames["db_name"] = copy.deepcopy(dbNames["name"])
        for name in categorie_names:
            for ind in xrange(len(dbNames["db_name"][name])): 
                if dbNames["db_name"][name][ind]=="":
                    dbNames["db_name"][name][ind] = \
                        dbNames["pvss_name"][name][ind]
            #print "\n===dbNames['name']:", dbNames['name'][name][:5]
            #print "===dbNames['db_name']:", dbNames['db_name'][name][:5]
            #print "===dbNames['paramid']:", dbNames['paramid'][name][:5]
        
        db.close()
        return dbNames

    def get_content(self, names, time1, time2, pvss_db, dbNames, len_array_max=50):
        #print "---- get_content ---"
        #print 'names:', names, '  time1:', time1, '  time2:', time2, 'pvss_db:', pvss_db
        #print 'type(time1):', type(time1)

        #len_array_max = 300
        #if len(names)>4:
            #len_array_max = 120
        #if len(names)>7:
            #len_array_max = 100

        db = MySQLdb.connect(self.host, self.user, self.password, self.db, self.port)
        if isinstance(time1,(str,unicode)):
            time1_unix = date_to_unix(time1)
            time2_unix = date_to_unix(time2)
        else:
            time1_unix = time1
            time2_unix = time2
        
        y, t, t_unix = {}, {}, {}

        #print 'dbNames["namesDB"].keys():', dbNames["namesDB"].keys()
        #print 'time1_unix:', time1_unix, '  time2_unix:', time2_unix
        if pvss_db in "db":
            names_db = []
            for name in names:
                indDB = dbNames["namesDB"]["All"].index(name)
                names_db.append(dbNames["namesPVSS"]["All"][indDB])
            #print 'names_db:', names_db
            names = names_db
        cursor = db.cursor()
        minY, maxY = [1.e7,], [-1.e7,]
        for name in names:
            if name in dbNames['nameTables']:
            #cmdCheck = "select table_name from information_schema.tables where table_schema='" + \
                #self.db + "' and table_name='" + name + "';"
                #print 'sensor ', name, ' exists'
                pass
            else:
                print '\n----------sensor ', name, ' does not exist!!!\n'
                y[name] = []
                t[name] = []
                t_unix[name] = []
                continue
            
            cmd1 = 'select * from ' + name + ' where date between '
            cmd2 = " '%i' and '%i';" % (time1_unix, time2_unix)
            cmd = cmd1+cmd2
            #print 'cmd: [', cmd, ']'

            dt_unix = getDataFromCursor(cmd, cursor, ind=0, typ='float')
            dt = [unix_to_date(d) for d in dt_unix]
            dy = getDataFromCursor(cmd, cursor, ind=1, typ='float')
            
            lenY = len(dy)
            #scale = float(lenY)/len_array_max
            [stepDown,lenLeft] = divmod(lenY,len_array_max)
            stepUp = stepDown+1
            #print 'len(dy):', lenY, 'stepDown:', stepDown, 'lenLeft:', lenLeft,
            if lenY>len_array_max:
                lenRight = len_array_max-lenLeft 
                firstRight = lenY-stepDown*(lenRight-1)-1
                dy = dy[:firstRight:stepUp] + dy[firstRight::stepDown]
                dt = dt[:firstRight:stepUp] + dt[firstRight::stepDown]
                dt_unix = dt_unix[:firstRight:stepUp] + dt_unix[firstRight::stepDown]
            
            y[name] = dy
            t[name] = dt
            t_unix[name] = dt_unix
            if lenY>0:
                minY.append(min(dy))
                maxY.append(max(dy))
            
        db.close()
        return [y, t, t_unix, min(minY), max(maxY)]

    def get_time_limit(self):
        db = MySQLdb.connect(self.host,
                             self.user,
                             self.password,
                             self.db,
                             self.port )

        cursor = db.cursor()
        cursor.execute("SELECT date FROM TE0001 ORDER BY date DESC LIMIT 1;")
        last = unix_to_date(int(cursor.fetchall()[0][0]))
        cursor.execute("SELECT date FROM TE0001 limit 1;")
        first = unix_to_date(int(cursor.fetchall()[0][0]))
        db.close()
        return [first, last]

DB311 = DataBase(host=propsDB["host"], 
                user=propsDB["user"],
                password=propsDB["password"],
                db=propsDB["nameDB"],
                port=propsDB["port"] )
    
