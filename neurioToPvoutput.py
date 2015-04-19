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

sys.path.append(".")
sys.path.append("..")

# a couple of global hacks


#PVoutput System ID
SYSTEMID=''

#PVoutput API Key
APIKEY=''

#method to upload the data to the pvoutput website
def log_pvoutput(batchS):
   #upload data to the pvoutput website

   #Args:
   #  bathS (string): the data to be uploaded.  The pvoutput method that 
   #                  will be called is the addbatchstatus method.  Documentation
   #                  can be found @ http://pvoutput.org/help.html#api-addbatchstatus
   #                  The data consists of multiple time
   #                  periods.  Each time period is in the form of
   #                  date,time,energyGeneration,powerGeneration,energyConsuption,powerConsumption;
   #                  date = yyyymmdd
   #                  time = hh:mm (in the local timezone )
   #                  energyGeneration (unused so use -1)
   #                  powerGeneration (the solar input)
   #                  energyConsumption (unused so use -1)
   #                  powerConsumption (household consumption)
   #                      ``0x0013A20040B65FAD``
   #Returns:
   #  Nothing

   # the globals we are going to use
   global SYSTEMID
   global APIKEY

   #build the http request to pvoutput including the ApiKey and the system Id
   cmd=('curl -d "data=%s" -H "X-Pvoutput-Apikey:%s" -H "X-Pvoutput-SystemId:%s" \
        http://pvoutput.org/service/r2/addbatchstatus.jsp' %(batchS,APIKEY,SYSTEMID)) 

   #send the request
   ret = subprocess.call(cmd, shell=True)

def main(argv):

        
        #make the keys available
        global APIKEY
        global SYSTEMID
        
        entireDay=False
        donation=False
       
        getSensorId=False

        ltz = dateutil.tz.tzlocal()
        UTCtz = dateutil.tz.tzutc()

        tp = neurio.TokenProvider(key=my_keys.key,
                                       secret=my_keys.secret)
        nc = neurio.Client(token_provider=tp)
        APIKEY=my_keys.APIKEY
        SYSTEMID=my_keys.SYSTEMID

        if my_keys.DONATION: 
           maxEntries=100
        else: 
           maxEntries=30


        try:
           opts, args = getopt.getopt(argv,"sht:",["hoursBack"])
        except getopt.GetoptError:
           print 'neurioToPvoutput -sh -t dHrs '
           sys.exit(2)
        for opt, arg in opts:
           if opt in ("-s"):
              getSensorId=True
           if opt in ("-t"):
              dHrs = int(arg)
              entireDay=True;
           if opt in ("-h"):
              print 'neurio_pvoutput -udh -t dHrs '
              print '-s print sensor id'
              print '-h print help info'
              print '-t dHrs - dHrs = number of hours in the past go get the neurio data'

        #read the sensor Id 
        if getSensorId:
           user_info = nc.get_user_information()
           locations = user_info.get("locations")
           sensors = locations[0].get("sensors")
           sensorId = sensors[0].get("sensorId")
           print "Sensor Id = " + sensorId.encode("utf-8")
           sys.exit(0)

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

        cnt = 0;
        batchString=''

        #build the string from the stats we read
        for item in stats:
 
           #read the time
           time = dateutil.parser.parse(item.get("start")).astimezone(ltz)

           #Read in the Energy and convert it to power in the 5 minute time
           #Energy is in WattSec, Pvoutput wants watts
           #So WattSec/3600Sec/Hr*12(5minute periods/hour) = Watts in the 5minute period
           cons = float(item.get("consumptionEnergy"))/3600*12
           gen = float(item.get("generationEnergy"))/3600*12

           #store the date,time,-1,,generatedPower,-1,consumedPower
           batchString=batchString+time.strftime("%Y%m%d,%H:%M")+',-1,'+str(int(gen+0.5))+',-1,'+str(int(cons+0.5))+';'
           cnt = cnt+1
           #We can't exceed the pvoutput limits so check if we have hit the limit for each batch upload
           if cnt == maxEntries:
              log_pvoutput(batchString)
              cnt=0
              batchString=''
           
        #finally check to see if there are any left over entries to uplad
        if cnt > 0:
              log_pvoutput(batchString)


if __name__ == '__main__':
   main(sys.argv[1:])

