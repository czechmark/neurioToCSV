# neurioToCSV
Python script to output neur.io generation and consumption data to stdardoutput or a csv file

## Installation
1.  Install required packages (see section below)
  * Neurio Python
  * python package dateutil
2.  Download this package
  *   git clone https://github.com/czechmark/neurioToCSV
3.  Install your neurio and pvoutput api keys, systemids,.. example for linux
  1. cd neurioToCSV
  2. nano my_keys.py  (or any other editor) 
    * change key and secret to be the apikey info you got from neur.io 
    * leave sensor_id alone for now
    * save your changes and exit from the editor
4.  Determine your system_id 
  1. run ./neurioToCSV.py -s to  have the system read your system Id
  2. if you get an error like 'access token' this means your neurio apikey data is incorrect
  3. if you don't get an error copy the sensor id into my_keys (using method in 3 above)

## Running
1.  Running by hand examples
  * ./neurioToCSV.py -h  # gives you the help output
  * ./neurioToCSV.py -s  # printout systemId
  * ./neurioToCSV.py -t 2 # output csv to the screen with the last 2 hours of data
  * ./neurioToCSV.py -t 97 # output csv to the screen with 24 hours of data starting 97 hours ago
  * ./neurioToCSV.py -t 2 -o xxx.csv # make a csv file xxx.csv with the last 2 hours of data

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
