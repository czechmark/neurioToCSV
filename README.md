# neurioToPvoutput
Python script to upload neur.io generation and consumption data to pvoutput.org

## Installation
1.  Install required packages (see section below)
   a. Neurio Python
2.  Download this package
   a.  git clone httpr://github.com/czechmark/neurioToPvoutput neurioToPvoutput
3.  Install your neurio and pvoutput api keys, systemids,.. example for linus
   a.  cd neurioToPvoutput
   b.  nano my_keys.py  (or any other editor) 
       change key and secret to be the apikey info you got from neur.io 
       leave sensor_id alone for now
       change SYSTEMID and APIKEY to be the apikey info you got from pvoutput.org
       change DONATION to True if you have donated to Pvoutput
       save your changes and exit from the editor
4.  Determine your system_id 
   a.  run ./neurioToPvoutput.py -s to read have the system read your system Id
   b.  if you get an error like 'access token' this means your neurio apikey data is incorrect
   c.  if you don't get an error copy the sensor id into my_keys (using method in 3 above)

## Running
1.  Running by hand examples
    ./neurioToPvoutput.py -h  # gives you the help output
    ./neurioToPvoutput.py -s  # printout systemId
    ./neurioToPvoutput.py -t 2 # update pvoutput with the last 2 hours of data
2.  Running via crontab
    a. crontab -e
    b. add a line that looks like this but customized for the directory you installed in
        */5 * * * * /home/debian/neurioToPvoutput/neurio.sh
    this tells crontab to run every 5 minutes and execute the supplied script neurio.sh
    neurio.sh tells the python script to upload the last two hours of data to pvoutput

    

## required packages
Neurio Python
   ### Neurio Python Installation

The easiest way to install the module is via pip:

    $ sudo pip install neurio

Or, clone the source repository and install it by hand:

    $ git clone https://github.com/jordanh/neurio-python neurio-python
    $ cd neurio-python
    $ sudo python setup.py install
    
    
