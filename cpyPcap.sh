#!/bin/bash



function scpMain {
    #checks to see if a connection exists
    #$1 = port
    #$2 = hostname@ip
    wget -q --spider http://google.com
    if [ ! "$?" -eq 0 ]
    then
       echo "please connect to a network"
    else
        echo "transferring files..."
        scp -r "pcapFolder" $1:"/$HOME/"
        
        if [ ! $? -eq 0 ]
        then
            exit
        fi
    fi
}

COUNTER=0
if [ "$EUID" -ne 0 ]
then
    echo "please run as root"
    exit
else
    while [ $COUNTER -lt 3600 ]; do 
        sleep 1
        let COUNTER+=1
        if (( $COUNTER == 3600 )) 
        then 
            scpMain $1 
            let COUNTER=0
        fi
    done
fi