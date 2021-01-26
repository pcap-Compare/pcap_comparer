#!/bin/bash

if [ "$EUID" -ne 0 ];
    then
    echo "please run as root"
    exit
    else
        pip install pypcapkit
        apt-get install sqlite3
        mkdir pcapComparer 
        cd pcapComparer
        sqlite3 pcapStorage.db
        cd 
        exit
fi
