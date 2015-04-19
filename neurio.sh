#!/bin/bash
source ~/.bashrc
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR
./neurioToPvoutput.py -t 2 >> ./logs
