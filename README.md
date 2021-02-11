# pcap_comparer
small tool to see which ip addresses and mac addresses you've seen before

*INSTALLATION PROCESS:*

`sudo chmod 777 installer.sh`

`sudo ./installer.sh`

`python3 pcapCompare.py -h` *will show you the available options*

***PLEASE PUT THE .PCAP FILES IN THE FOLDER WHERE THE PYTHON FILE IS. IM WORKING ON A FIX BUT THAT'S A WORKAROUND FOR NOW***

***if you have an problem message me on discord mrLochness350#7880 |
contributions are appreciated :)***

***(feb 11th, 2021) added bash scripts that allow user to have a headless scanning station and an automatic file upload system to their desired computer. REQUIRES STATIC IP AND PORT FORWARDING***

**usage for *onBootScanner.sh* and *cpyPcap.sh*:


  ***ON YOUR HEADLESS SCANNING DEVICE:***
  
  **1) sudo `chmod 777` both scripts**
  
  **2) open two terminals and run one terminal where you want your pcaps to be saved. run `onBootScanner.sh [network interface] [name of pcap-to-be] `. in the second terminal run `cpyPcap.sh hostname@ip `. you can change the default transfer time of 1h to your prefered time (convert to seconds)**


**changelog:**


*v0.1.2- added the option to copy all ip addresses to a text file*

