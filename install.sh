#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "please run as root"
    exit
    else
        mkdir ~/$HOME/$USER/pcapComparer && cd ~/$HOME/$USER/pcapComparer
        sqlite3 pcapStorage.db
        cd 
    fi
fi
