#!/bin/bash



function monitorMode {
    ifconfig $1 down
    iwconfig $1 mode monitor
    ifconfig $1 up
    echo "entered monitor mode"
}
function printHelp {
    echo "usage:"
    echo "./onBootScanner.sh {network interface} {pcap file name}"
    echo ""
    echo "example:"
    echo "./onBootScanner.sh wlan0 example "
    exit 0
}
function main {
    if [ -z "$1" ]
    then
        echo "interface cannot be empty"
        printHelp
    else
        local Interface="$1"
        local File_Name="$2"
        local Counter=1
        local File_Ending=".pcap"
        local IncFile="$File_Name$Counter$File_Ending" #example1.pcap
        tshark -I $interface -w $File_Name -a duration:5 -F pcap -q #change the duration to 2 hours
        if ! pgrep -x "tshark" > '/dev/null' 2>&1
        then
            tshark -I $interface -w $IncFile -a duration:5 -F pcap -q
        fi
        let Counter+=1
    fi 
    
    
    
}

if [ "$EUID" -ne 0 ]
then
    echo "please run as root"
    exit
else
    if [ ! -d "pcapFolder" ]
    then 
        echo "making pcapFolder directory..."
        mkdir pcapFolder && cd pcapFolder
        chmod 777 pcapFolder
        while true; 
        do
            main $1 $2
        done
    else
        while true; do
            main $1 $2
        done
    fi  
fi
