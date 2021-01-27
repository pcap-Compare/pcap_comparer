import os
import pcapkit
#import mysql.connector
import string
import sqlite3
import re
import getopt
import sys

def Credits():
    print('''
    =========================================================
    this is my humble attempt at a pcap file parser.
    it checks if you encountered an ip before basically


    SPECIAL THANKS TO: 
    Mystic#4242 on discord  
    Mudbill#6969 on discord
    for helping me with the regex
    and 
    ꧁👁 ꧂#9701 on discord
    Mrmellow#2662 on discord
    for helping me with some debugging
    =========================================================
    ''')

storageDBConnString = sqlite3.connect('pcapStorage.db')
storageDB = storageDBConnString.cursor()   

def Addcount(): #**copied from stackoverflow** function that just increments 1 to the count function
    if not os.path.exists('counterlog.txt'):
        f = open('counterlog.txt', 'x')
        queryCreate = """CREATE TABLE "Address"("ips"TEXT,"mac"TEXT,"countSeen"TEXT)"""
        storageDB.execute(queryCreate)
        storageDBConnString.commit()
        f.write("0")
        f.close()
    else:
        f = open("counterlog.txt", "r")
        a = f.readline()
        b = int(a[0])        
        b = b + 1
        f.close()
        with open('counterlog.txt', 'w') as f:
            f.write(str(b))
        return b

def DeleteAll(): #deletes all the content from the database
    ReturnQuery = """DELETE FROM Address;"""
    try:
        storageDB.execute(ReturnQuery)
        storageDBConnString.commit()
        print("successfully deleted DB contents")
    except Exception as e:
        print(e)
    
def AddNewAddress(ip,mac): #adds unseen mac and ip into the database
    storageDB.execute("""INSERT INTO Address(ips,mac,countSeen) VALUES(:ips, :mac, :countSeen);""", {"ips": ip, "mac": mac, "countSeen": "1"})
    storageDBConnString.commit()
    return storageDB.fetchall()

def PrintRecIP(): #prints out recurring ips
    ReturnQuery = """SELECT * FROM Address
     WHERE countSeen > 1"""
    temp = storageDB.execute(ReturnQuery)
    for i in temp.fetchall():
        print(i)
    
def PrintSpecIp(ip): #print specific ip
    ReturnQuery = """SELECT * FROM Address WHERE ips =" '{0}'";""".format(ip)
    temp = storageDB.execute(ReturnQuery)
    if not temp.fetchone():
        print("ip not in database")
    else:
        print("ip information: \n")
        for i in temp.fetchall():
            print("".join(str(i).strip()))
   


def PrintSpecMac(mac): #print specific mac
    ReturnQuery = """SELECT * FROM Address WHERE mac =" '{0}'";""".format(mac)
    temp = storageDB.execute(ReturnQuery)    
    for i in temp.fetchall():
        print(i)

def PrintAll():
    query1 = """SELECT * FROM Address"""
    temp = storageDB.execute(query1)
    for i in temp.fetchall():
        print(i)

def PrintAllMacs():
    query1 = """SELECT mac,countSeen FROM Address"""
    temp = storageDB.execute(query1)
    for i in temp.fetchall():
        print(i)





def AnalyzePCAP(pcapfile):
    count = Addcount()
    OutputFile = "parsedPCAP{0}".format(count)
    pcapkit.extract(fin=pcapfile, fout=OutputFile, format="tree",engine="PyShark") #im an actual idiot. why didn't i know that tree means text file??? 
    #^this line extracts the content of the pcap into a text file for parsing. 

    f = open("parsedPCAP{0}.txt".format(count), "r") 
    AddressReg = re.findall(r"ethernet\s*.*dst -> ((?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2}))\s*.*src -> ((?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2}))[\s\W\w]*?ipv4[\s\W\w]*?src -> ((?:[0-9]{1,3}.){3}[0-9]{1,3})\s*.*dst -> ((?:[0-9]{1,3}.){3}[0-9]{1,3})",f.read(), re.M)
     #^regex to get the addresses from the pcap file 
    f.close()
    os.remove('parsedPCAP{0}.txt'.format(count)) #update counterlog.txt to remove conflicting files

    UpdateSeenSRC = """"""
    UpdateSeenDST = """"""
    AddressDict = {}
    print("updating database....")
    for i in range(0,len(AddressReg)):
        addressUNSORTED = str(AddressReg[i])
        addressSORTED =addressUNSORTED.split(',')
        AddressDict["addressesSRC"] = ("mac:" + addressSORTED[1] + " | " + " ip:" + addressSORTED[2])
        AddressDict["addressesDST"] = ("mac:" + addressSORTED[0] + " | " + " ip:" + addressSORTED[3])         


        querySRC = """SELECT * FROM Address
         WHERE mac = "{0}" AND ips = "{1}";""".format(addressSORTED[1],addressSORTED[2]) #select for src ips
        queryDST = """SELECT * FROM Address
         WHERE mac = "{0}" AND ips = "{1}";""".format(addressSORTED[0],addressSORTED[3]) #select for dst ips
        
        
        UpdateSeenSRC = """
        UPDATE Address
         SET countSeen = countSeen + 1 WHERE mac = "{0}" AND ips = "{1}";
        """.format(addressSORTED[1],addressSORTED[2]) #update the counter for times seen per ip for src ips


        UpdateSeenDST = """
        UPDATE Address
         SET countSeen = countSeen + 1 WHERE mac = "{0}" AND ips = "{1}";
        """.format(addressSORTED[0],addressSORTED[3])#same as above just for dst ips
      
        CheckExist = storageDB.execute(querySRC) #checks to see if ip exists in database
        test = CheckExist.fetchone()
        if not test: #if it doesnt
            AddNewAddress(addressSORTED[2],addressSORTED[1]) #add it to the database
        else: #if it does
            storageDB.execute(UpdateSeenSRC) #update the counter of times seen


        #same as above
        CheckExist = storageDB.execute(queryDST)
        test = CheckExist.fetchone()
        if not test:
            AddNewAddress(addressSORTED[3].replace(")",""),addressSORTED[0].replace("(",""))
        else:    
            storageDB.execute(UpdateSeenDST)


        DeleteDuplicates ="""delete from Address
         where ROWID not in (select min(ROWID) from Address
         GROUP by ips, mac);"""
        storageDB.execute(DeleteDuplicates)
        storageDBConnString.commit()
    


    
    print("database updated")
def main():
    HelpString = """
    -h / --help: show this menu
    --file_path: set filepath for the pcap file to parse
    --return_Ip: returns specific information about given IP address
    --return_Mac: returns specific information about given Mac address
    --print_recurring: returns every IP that has been seen before
    --print_all: returns everything in the database
    --delete_all: deletes every address in the database
     ****USE ONLY IF YOU WANT TO RESET THE DATABASE CONTENTS****

    example usage:
    python3 pcapCompare.py --file_path /path/to/.pcap
    python3 pcapCompare.py --return_Ip [IP address]
    python3 pcapCompare.py --return_Mac [MAC address]
    python3 pcapCompare.py --print_recurring
    python3 pcapCompare.py --print_all
    python3 pcapCompare.py --delete_all

    """
    File_Path = None
    
    try:
        opts,args = getopt.getopt(sys.argv[1:], "h", ["help","file_path=","return_Ip=","return_Mac=","print_recurring","print_all", "delete_all","credits"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(0)
    for options, arguments in opts:
        if options in ("-h", "--help"):
            print(HelpString)
            sys.exit(0)
        elif options in ( "--file_path"): 
            File_Path = arguments

        elif options in ( "--return_Ip"):  
            print(PrintSpecIp(arguments))
        elif options in ("--return_Mac"):
            print(PrintSpecMac(arguments))
        elif options in("--print_recurring"):
            print(PrintRecIP())
        elif options in("--print_all"):
            print(PrintAll())
        elif options in("--delete_all"):
            DeleteAll()
        elif options in("--credits"):
            Credits()           
        else:
            print("invalid argument")
            sys.exit(0)
    if File_Path != None:
        AnalyzePCAP("{0}".format(File_Path)) 
    
    
    
    
main()
storageDB.close()
storageDBConnString.close()
#region
    #for line in f:
     #   rec = line.strip()
            #test = re.findall(r"ethernet\s*.*dst -> ((?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2}))\s*.*src -> ((?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2}))[\s\W\w]*?ipv4[\s\W\w]*?src -> ((?:[0-9]{1,3}.){3}[0-9]{1,3})\s*.*dst -> ((?:[0-9]{1,3}.){3}[0-9]{1,3})",line, flags=gm)
            #rec = line.replace(' ', '')
            #rec = line.replace(' | ', '')
            #rec = line.replace('|', '')
            #rec = line.replace('-','')
            #rec = line.replace('->', '')
            #rec = line.replace(' |-- ', '')
            #rec = line.replace(' | ','')
            #rec = line.strip()
      #  count = 1
            #print(test)
            

            #print(rec)"you have seen the address: ({0} | {1}) {2} times before".format(addressSORTED[3],addressSORTED[0], exec1)
            #print("")
       # if rec.startswith('|-- src -> '):
                #print(line)
        #    temp1 = line.split()[-1]
         #   Ip1 =re.findall(r"[s-s][r-r][c-c]..(?:[0-9]{1,3}\.){3}[0-9]{1,3}", rec)
          #  Mac1 = re.findall(r"(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})|(?:[0-9a-fA-F]{4}\\.[0-9a-fA-F]{4}\\.[0-9a-fA-F]{4})", rec)                
           # addressDict["address"] = (str(Mac1) + " : " + str(Ip1))           
            #print("----------")
            #srcArr.append(temp1)
        #if rec.startswith('||--dst->'):
                #print(line)
         #   Ip1 =re.findall(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", rec)
          #  print("destination: " + "".join(Ip1))
           # temp2 = line.split()[-1]
            #dstArr.append(temp2)
                #print("destinations: ")
                #print(dstArr)
                
            
        #count = count + 1
          
    #i didn't know that a tree format meant text file so i tried writing this with json but apparently tree is a .txt file so i changed to that
    #=========================USELESS CODE==============================
    #with open("parsedPCAP{0}.json".format(count), "r") as file1:
    #file1 = open('parsedPCAP{0}.json'.format(count), 'r')
    #data = json.load(file1)
     #   jsondata = json.load(file1)
        #print(jsondata)
    #for line in data['"ethernet":']:
    #    print(line)
    #file1.close()    
    #JsonFile = "parsedPCAP{0}.json".format(count)
    #print(json.loads(JsonFile))
    #========================/USELESS CODE==============================
   
    #def Addcount(): #**copied from stackoverflow** function that just increments 1 to the count function
    #   if not os.path.exists('counterlog.txt'):
    #      f = open('counterlog.txt', 'x')
        # else:
        #    f = open("counterlog.txt", "r")
        #   a = f.readline()
        #  f.close()
        # b = int(a[0])
            #b = b + 1
            #with open('counterlog.txt', 'w') as f:
             #   f.write(str(b))
            #return b
#endregion