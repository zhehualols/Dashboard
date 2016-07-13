import os.path
import cherrypy
import mysql.connector

class Connection():
    
    def __init__(self, host, user, passwd,db):
        self.username = user
        self.password= passwd
        self.host = host
        self.database = db
        #Establish connection with mysql database server
        self.connection = mysql.connector.Connect(host = self.host ,
                                                user = self.username ,
                                                password = self.password ,
                                                database = self.database)
        self.cursor = self.connection.cursor()
        
    def execute_query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        print result
        self.connection.commit()
        return result
    
    def Get_data(self):
        query = "select * from edid_semantics"
        print "executing query"
        myconnection.execute_query(query)
class DashBoard(object):
    @cherrypy.expose
    def index(self):
        return open('/home/development/workspace/Dashboard/Public/html/index.html')
class EDID(object):
    @cherrypy.expose
    def index(self):
        return open('/home/development/workspace/Dashboard/Public/html/edid.html')
class IRcode(object):
    @cherrypy.expose
    def index(self):
        return open('/home/development/workspace/Dashboard/Public/html/ir.html')
class Analytics(object):
    @cherrypy.expose
    def index(self):
        return open('/home/development/workspace/Dashboard/Public/html/ana.html')
if __name__ == '__main__':
    myconnection = Connection('172.16.170.136','root','password123!','hdmi')
    print 'connected to database'
    conf = {
        '/':{
            'tools.staticdir.root':os.path.abspath(os.getcwd())
        },
        '/EDID':{},
        '/IRcode':{},
        '/Analytics':{},
        '/static':{
                'tools.staticdir.on': True,
                'tools.staticdir.dir':'./Public'
        }
    }
    webapp = DashBoard()
    webapp.EDID = EDID()
    webapp.IRcode = IRcode()
    webapp.Analytics = Analytics()
    myconnection.Get_data()
    cherrypy.quickstart(webapp,'/',conf)