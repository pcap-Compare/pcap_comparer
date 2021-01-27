#!/bin/bash

if [ "$EUID" -ne 0 ];
    then
    echo "please run as root"
    exit
    else
        pip install pypcapkit
        apt-get install sqlite3
        sqlite3 pcapStorage.db 'CREATE TABLE "Address"("ips"TEXT,"mac"TEXT,"countSeen"TEXT)'
        echo "created pcapStorage.db "
        exit
fi
