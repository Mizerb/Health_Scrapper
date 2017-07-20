import urllib2
import urllib
from bs4 import BeautifulSoup
import time
import json

def Structures():
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

def GetFacilites():
    data= "facility=facility+name&town=&isSubmitted=1"
    #data = "facility=facility+name&town=&isSubmitted=1"
    print data
    #data = urllib.urlencode(data)
    #print data
    url = "http://app.albanycounty.com/doh/restaurantinspections/"
    Request =  urllib2.Request(url,data)
    response = urllib2.urlopen(Request)
    html = response.read()

    meh = open('SafteyCheck.html','w')
    meh.truncate()
    meh.write(html)
    meh.close()


    soup = BeautifulSoup(html,'html.parser')
    mylines = soup.findAll("form", class_="fac-name")
    print mylines[0].contents[1]
    print mylines[0].contents[3]
    
    ret = []

    for line in mylines:
        facility = {
            'facName': line.contents[1]['value'].encode("ascii"),
            'Opkey': line.contents[3]['value'].encode("ascii")
        }

        ret.append(facility)
    print len(mylines)
    print ret[0]

    return ret 



def GetInpections(facility):
    inspections = []
    try:
        data = urllib.urlencode(facility)
        url = "http://app.albanycounty.com/doh/restaurantinspections/"
        Request =  urllib2.Request(url,data)
        response = urllib2.urlopen(Request)
        html = response.read()

        soup = BeautifulSoup(html,'html.parser')
        mylines = soup.findAll("form",  id="detailform")
        #print mylines[0].contents[1]['value']
        
        inspections = []
        for line in mylines:
            inspection={
                'inspDate': line.contents[1]['value'].encode("ascii"),
                'srvkey': line.contents[3]['value'].encode("ascii")
            }
            inspections.append(inspection)
    except Exception, e:
        print e

    return inspections

def GetViolations(inspection):
    violations = []
    try:
        data = urllib.urlencode(inspection)
        url = "http://app.albanycounty.com/doh/restaurantinspections/"
        Request =  urllib2.Request(url,data)
        response = urllib2.urlopen(Request)
        html = response.read()

        soup = BeautifulSoup(html,'html.parser')
        mylines = soup.findAll("td",  align="left", valign="top", style="line-height:140%;")
        #print mylines[0].string[1:3] + mylines[0].string[5:]
        
        for line in mylines:
            violation={
                'number': (line.string[1:3]).encode("ascii"),
                'name': (line.string[6:]).encode("ascii")
            }
            violations.append(violation)

    except Exception, e:
        print e
    

    return violations
    


def main():
    Data = GetFacilites()
    return
    for facility in Data:
        time.sleep(1)
        inspections = GetInpections(facility)
        for inspection in inspections:
            time.sleep(1)
            violations = GetViolations(inspection)
            inspection['violations'] = violations
        facility['inspections'] = inspections

    meh = open('OUT.json','w')
    meh.truncate()
    print Data
    #meh.write(str(Data))
    text = json.dumps(Data)
    meh.write(text)
    meh.close()

    return


main()