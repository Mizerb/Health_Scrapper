import urllib2
import urllib
from bs4 import BeautifulSoup
import time
import json
import operator
from scipy.stats import linregress

def structures():
    facility={
        'facName': '16+HANDLES',
        'OpKey': '31472473'
    }
    inspection={
        'inspDate':'06/25/2015',
        'srvkey':'1001672706'
    }

    output={
        'facname': 'name',
        'Opkey' : '12121',
        'inspections' :
        [{
            'inspDate': '02/02/12',
            'srvkey' : '101001',
            'violations':[
            {'CODE': '12E',
            'VIOLATIONTEXT': 'SOMTHING SOMETHING'}
            ]
            
         }
        ]
    }
    print output
    return

def datatesting():

    data= {
        'inspDate':'06/25/2015',
        'srvkey':'1001672706'

    }
    #data = "facility=facility+name&town=&isSubmitted=1"
    print data
    data = urllib.urlencode(data)
    print data
    url = "http://app.albanycounty.com/doh/restaurantinspections/"
    Request =  urllib2.Request(url,data)
    response = urllib2.urlopen(Request)
    html = response.read()


    meh = open('testINSPC.html','w')
    meh.truncate()
    meh.write(html)
    meh.close()
    return

def htmlParse():
    html = open("testINSPC.html").read()
    soup = BeautifulSoup(html,'html.parser')
    mylines = soup.findAll("td",  align="left", valign="top", style="line-height:140%;")
    print mylines[0].string[1:3] + mylines[0].string[5:]
    #print mylines[0]
    return

def parseJson():
    jsonfile = open("OUT.json")
    text = jsonfile.read()
    jsonfile.close()



    find1 = " FLOORS, WALLS, CEILINGS, NOT SMOOTH, PROPERLY CONSTRUCTED, IN DISREPAIR, DIRTY SURFACES"
    find2 = "FOOD NOT PROTECTED DURING STORAGE, PREPARATION, DISPLAY, TRANSPORTATION AND SERVICE, FROM POTENTIAL SOURCES OF CONTAMINATION (E.G., FOOD UNCOVERED, MISLABELED, STORED ON FLOOR, MISSING OR INADEQUATE SNEEZE GUARDS, FOOD CONTAINERS DOUBLE STACKED)"

    check1 = []
    check2 = []

    facilities = json.loads(text)
    
    violas = {}
    violas[find1] = []

    for facility in facilities:
        viol1 = 0
        viol2 = 0
        for inspection in facility['inspections']:
            for violation in inspection['violations']:
                if violation['name'] not in violas:
                    violas[violation['name']] = []
        


    for facility in facilities:
        for key in violas:
            violas[key].append(0)

        for inspection in facility['inspections']:
            for violation in inspection['violations']:
                violas[violation['name']][-1] = 1 + violas[violation['name']][-1]

                # if violation['name'] == find:
                #     print facility
                #     return
                # if violation['name'] in count:
                #     count[violation['name']] = count[violation['name']] + 1
                # else :
                #     count[violation['name']] = 1



    
    meh = open('data.txt','w')
    meh.truncate()
    
    for key in violas:
        meh.write(key + "\n")
        print >>meh, linregress(violas[find1], violas[key])
        meh.write("\n\n")

    meh.close()


def cheat_fac( facility, find1 ):
    count = 0
    for inspection in facility['inspections']:
            for violation in inspection['violations']:
                if violation['name'] == find1:
                    count = count + 1
                    if( count > 2 ):
                        return 1

    return 0

def percent():
    jsonfile = open("OUT.json")
    text = jsonfile.read()
    jsonfile.close()


    facilities = json.loads(text)
    find1 = " FLOORS, WALLS, CEILINGS, NOT SMOOTH, PROPERLY CONSTRUCTED, IN DISREPAIR, DIRTY SURFACES"

    faclity_count = 0
    facility_w_violation = 0
    
    for facility in facilities:
        facility_w_violation = facility_w_violation + cheat_fac(facility, find1)
        faclity_count = faclity_count + 1

    print facility_w_violation
    print faclity_count

    print (1.0*facility_w_violation)/(1.0*faclity_count)
        

                
               

#structures()
#datatesting()
#htmlParse()
parseJson()

#percent()