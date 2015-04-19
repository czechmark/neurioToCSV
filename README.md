# neurioToPvoutput
Python script to upload neur.io generation and consumption data to pvoutput.org

## Installation
1.  Install required packages (see section below)
  * Neurio Python
  * python package dateutil
2.  Download this package
  *   git clone https://github.com/czechmark/neurioToPvoutput
3.  Install your neurio and pvoutput api keys, systemids,.. example for linus
  1. cd neurioToPvoutput
  2. nano my_keys.py  (or any other editor) 
    * change key and secret to be the apikey info you got from neur.io 
    * leave sensor_id alone for now
    * change SYSTEMID and APIKEY to be the apikey info you got from pvoutput.org
    * change DONATION to True if you have donated to Pvoutput
    * save your changes and exit from the editor
4.  Determine your system_id 
  1. run ./neurioToPvoutput.py -s to  have the system read your system Id
  2. if you get an error like 'access token' this means your neurio apikey data is incorrect
  3. if you don't get an error copy the sensor id into my_keys (using method in 3 above)

## Running
1.  Running by hand examples
  * ./neurioToPvoutput.py -h  # gives you the help output
  * ./neurioToPvoutput.py -s  # printout systemId
  * ./neurioToPvoutput.py -t 2 # update pvoutput with the last 2 hours of data
2.  Running via crontab
  1. crontab -e
  2. add a line that looks like this but customized for the directory you installed in
```
        */5 * * * * /home/debian/neurioToPvoutput/neurio.sh
```
*this tells crontab to run every 5 minutes and execute the supplied script - neurio.sh.
    If you look inside neurio.sh, you will see that it tells the python script to upload the last two hours of data to pvoutput.  This should allow for system interruptions so that the chances of losing data is minimized.
## Setting up pvoutput
The only real suggestion I have is to set the update rate to 5 minutes
## Getting your old data into pvoutput
You are only allowed to upload data that is either younger than 14 days(no donation) or 90 days (donation mode).  If you want to load old data then run the script by hand in a series of commands like this.
```
   ./neurioToPvoutput.py -t 96
   ./neurioToPvoutput.pv -t 73
   ./neurioToPvoutput.pv -t 50
   ./neurioToPvoutput.pv -t 27
   ./neurioToPvoutput.pv -t 4
```
Each command will upload 24 hours of data starting 96 hrs in the past, 73 hrs in the past ... I didn't space them by 24 hours just so I didn't miss one update because time elapses between the calls.

## required packages
* python package dateutil
* Neurio Python

### Python dateutil Package Installation
The easiest way to install the module is via pip:

    $ sudo pip install python-dateutil
    
### Neurio Python Installation

The easiest way to install the module is via pip:

    $ sudo pip install neurio

Or, clone the source repository and install it by hand:

    $ git clone https://github.com/jordanh/neurio-python neurio-python
    $ cd neurio-python
    $ sudo python setup.py install
    
## ERRORs
When I first installed and tried to run the neurio-python library, I got an error complaining about "SSL InsecurePlatform".  In order to fix that I had to do the following (debian).  What you have to do may vary depending on how your linus and python are installed.  In any case, the InsecurePlatform is actually just a warning and I think the system will still work if you are getting that warning.
```
  sudo apt-get install build-essential libssl-dev libffi-dev python-dev
  sudo pip install requests[security]
  ```
