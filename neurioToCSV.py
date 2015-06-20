#!/usr/bin/env python
"""
Copyright [2016] [Mark Petschek mark@petschek.com]
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.:
"""

#set up the imports
import sys
import neurio
import my_keys
import json
import dateutil.parser
import getopt
import datetime
import subprocess
import pprint
import requests

sys.path.append(".")
sys.path.append("..")



def gen_headers(token):
    """Utility method adding authentication token to requests."""
    headers = {
      "Authorization": " ".join(["Bearer", token])
    }
    return headers


def get_user_information(client,tp):
    """Gets the current user information, including sensor ID

    Args:
      None

    Returns:
      dictionary object containing information about the current user
    """
    url = "https://api.neur.io/v1/users/current"

    headers = gen_headers(tp.get_token())
    headers["Content-Type"] = "application/json"

    r = requests.get(url, headers=headers)
    return r.json()


def main(argv):

        
        
        entireDay=False
        stdOutput=True;
       
        getSensorId=False

        ltz = dateutil.tz.tzlocal()
        UTCtz = dateutil.tz.tzutc()



        try:
           opts, args = getopt.getopt(argv,"sht:o:",["hoursBack"])
        except getopt.GetoptError:
           print 'neurioToPvoutput -sh -t dHrs -o fileName'
           sys.exit(2)
        for opt, arg in opts:
           if opt in ("-s"):
              getSensorId=True
           if opt in ("-o"):
              ofile = arg
              stdOutput=False;
           if opt in ("-t"):
              dHrs = int(arg)
              entireDay=True;
           if opt in ("-h"):
              print 'neurioToCSv -sh -t dHrs '
              print '-s print sensor id'
              print '-h print help info'
              print '-t dHrs - dHrs = number of hours in the past go get the neurio data'
              sys.exit(0)

        # get the Neurio token
        tp = neurio.TokenProvider(key=my_keys.key,
                                       secret=my_keys.secret)
        nc = neurio.Client(token_provider=tp)

        #read the sensor Id 
        if getSensorId:
           user_info = get_user_information(nc,tp)
           locations = user_info.get("locations")
           sensors = locations[0].get("sensors")
           sensorId = sensors[0].get("sensorId")
           print "Sensor Id = " + sensorId.encode("utf-8")
           sys.exit(0)

        #do the file stuff
        if stdOutput:
            fO=sys.stdout
        else:
           try:
              fO = open(ofile,'w')
           except IOError:
              print "Could not open file for writing"
              sys.exit(-1)

        #Neurio doesnt allow more than a days worth of data in a single request
        #so limit the data to either now - 1day or input offset time + 1 day
        if entireDay:
          stime = datetime.datetime.now() - datetime.timedelta(hours=dHrs)
          etime = stime + datetime.timedelta(days=1)
        else:
          stime = datetime.datetime.now() - datetime.timedelta(days=1)
          etime = stime+datetime.timedelta(days=1)

        #nuerio uses UTC, so we need to convert localtime to UTC and 
        #format the strings that neurio expects
        stime = stime.replace(tzinfo=ltz)
        etime = etime.replace(tzinfo=ltz)
        stimeString = stime.astimezone(UTCtz).strftime("%Y-%m-%dT%H:%M:%S")
        etimeString = etime.astimezone(UTCtz).strftime("%Y-%m-%dT%H:%M:%S")

        #read the data from neurio
        stats = nc.get_samples_stats(my_keys.sensor_id,stimeString,"minutes",etimeString,5)


        #print "time,consuptionEnergy(Watt Sec),generationEnergy(Watt Sec)"
        fO.write( 'time,consuptionEnergy(Watt Sec),generationEnergy(Watt Sec)\n')
        for item in stats:
 
           #read the time
           time = dateutil.parser.parse(item.get("start")).astimezone(ltz)
           fO.write (str(time) + ',' + str(item.get('consumptionEnergy')) + ',' + str(item.get('generationEnergy')) + '\n')


if __name__ == '__main__':
   main(sys.argv[1:])

