import os.path
import cherrypy
import mysql.connector
import matplotlib.pyplot as plt
import json
from timeit import itertools

class hdmi_Connection():
    
    def __init__(self, host, user, passwd,db):
        print "Connecting to hdmi database"
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
        
    
    def Get_data(self):
        query = 'select * from edid_semantics'
        print 'query:' + query
        self.cursor.execute(query)
        desc = self.cursor.description
        return [dict(itertools.izip([col[0] for col in desc], row))
                for row in self.cursor.fetchall()]
        
class Staging_connection():
    
    def __init__(self , host , user , passwd , db):
        print "Connecting to Staging database"
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
        
    def get_array(self):
        pie_array = []
        self.cursor.execute('call testCount(10, 0, @total, @others, @othersPercentage)')
        # cursor.execute('select @total')
        # cursor.execute('select @others')
        # cursor.execute('select @othersPercentage')
        self.cursor.execute('select * from brand')
        for row in self.cursor:
            pie_array.append(row)
        return pie_array
        self.cursor.close()
        self.connection.close()
class DashBoard(object):
    @cherrypy.expose
    def index(self):
        return open('/home/development/workspace/Dashboard/Public/html/index.html')
class EDID(object):
    @cherrypy.expose
    def index(self):
        return open('/home/development/workspace/Dashboard/Public/html/edid.html')
    def json_loader(self, table_data):
        print 'Creating Json File'
        with open('/home/development/workspace/Dashboard/Public/files/data.json' , 'w') as outfile:
            json.dump(table_data, outfile)
class IRcode(object):
    @cherrypy.expose
    def index(self):
        return open('/home/development/workspace/Dashboard/Public/html/ir.html')
class Analytics(object):
    @cherrypy.expose
    def index(self):
        return open('/home/development/workspace/Dashboard/Public/html/ana.html')
    
    def PieChart(self , data_array):
        print "Ploting pie chart"
        name_array =[]
        num_array=[]
        percent_array=[]
        for i in range(len(data_array)):
            name_array.append(data_array[i][0])
            num_array.append(data_array[i][1])
            percent_array.append(data_array[i][2])
        name_array.append('others')   
        num_array.append(10015)
        labels = name_array
        sizes = num_array
        colors= ['red','blue','darkblue','cyan','silver','orange','pink','maroon','teal','yellow','white']
        explode = (0.1,0,0,0,0,0,0,0,0,0,0)
        fig = plt.figure()
        fig.suptitle('CpBrand',fontsize=20)
        ax = fig.gca()
        ax.pie(sizes,explode=explode,colors=colors, labels=labels , autopct= '%1.1f%%' ,shadow= True ,startangle=90,)
        ax.axis('equal')
        plt.legend(bbox_to_anchor=(0.8, 0.7), loc=2, borderaxespad=0.)
        plt.savefig("/home/development/workspace/Dashboard/Public/Images/testpie.png" , dpi=80)
        plt.close()
        
if __name__ == '__main__':
    hdmiconnection = hdmi_Connection('172.16.170.136','root','password123!','hdmi')
    Stagingconnection = Staging_connection('172.16.170.136','root','password123!','IrStaging')
    print 'connected to all database'
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
    # Ploting Pie chart
    pie = Stagingconnection.get_array()
    webapp.Analytics.PieChart(pie)
    # Loading Json table data
    edid_data = hdmiconnection.Get_data()
    webapp.EDID.json_loader(edid_data)
    cherrypy.config.update({'server.socket_port': 3030})
    cherrypy.server.socket_host = '172.16.170.181'
    cherrypy.quickstart(webapp,'/',conf)