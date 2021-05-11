#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2021-02-09

Copyright (c) 2021 Erik Johansson

@author:     Erik Johansson
@contact:    <erik.johansson@smhi.se>
'''

'''
Program for Downloading Ostia data 
'''

import datetime
import os
import pdb


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-y","--year", type=int, default=2018,  
                        help="Year. Default=2018")
    parser.add_argument("-n","--nwc", action="store_false", default=True, 
                        help="Create links prepared fot NWC-SAF. Default=True (i.e. create links)")
    args = parser.parse_args()
    
    #: Date for first and last download
    startdate = "%d 04 01" %args.year
    enddate = "%d 10 31" %args.year

    #: If on icare save data on scratch
    #: else save on home
    if os.environ['HOSTNAME'].split('.')[1] == 'icare':
        baseDir = "/scratch/%s" %os.environ['USER']
    else:
        baseDir = os.environ['HOME']
    mainSaveDir = "%s/Data/Ostia" %baseDir
    
    #: Main web adress from where to get data    
    mainWebAdress = "https://podaac-tools.jpl.nasa.gov/drive/files/allData/ghrsst/data/L4/GLOB/UKMO/OSTIA"
    #: user name
    user="smhi_erik"
    #: password
    password="@AItE8W1EwHte82XFdK"
    
    #: Turn start and end date into datetime objects
    datum = datetime.datetime.strptime(startdate, "%Y %m %d")
    stoppdatum = datetime.datetime.strptime(enddate, "%Y %m %d")
    
    #: initiate c1 and c2 as ok incase they are not recived
    c1 = 0
    c2 = 0
    
    #: Start the while-loop
    run=True
    while run:
        print("---")
        print("New file")
        print("---")
        print("")
        #: Save dir with year and month
        saveDir = mainSaveDir + "/%i/%02i" %(datum.year, datum.month)
        #: Save dir for links. Same as saveDIr but without month
        #: Used by NWC
        linkSaveDir = mainSaveDir + "/%i" %(datum.year)
        #: Test if saveDir exist. Otherwise create
        if not os.path.isdir(saveDir):
            os.makedirs(saveDir)
        #: Web adress from where to get data. Data stored under year/doy
        webAdress = mainWebAdress + "/%i/%03i" %(datum.year, datum.timetuple().tm_yday)
        #: Filename latest name convention
        filename = "%i%02i%02i-UKMO-L4HRfnd-GLOB-v01-fv02-OSTIA.nc.bz2" %(datum.year, datum.month, datum.day)
        #: Filename old name convention
        #: Used by NWC
        linkFilename = "%i%02i%02i120000-UKMO-L4_GHRSST-SSTfnd-OSTIA-GLOB.nc" %(datum.year, datum.month, datum.day)
        #: webAdress + filenae = file for wget
        totPath = webAdress + "/" + filename
        
        #: Filename of downloaded file
        bz2file = "%s/%s" %(saveDir, filename)
        #: Filename of unziped file
        ncfile = bz2file.replace(".bz2", "")
        #: Filename of link for nwc
        linkfile = "%s/%s" %(linkSaveDir, linkFilename)
        
        #: If there is NO bz2-file nor nc-file. 
        #: Download bz2-file
        if not (os.path.isfile(ncfile) or os.path.isfile(bz2file)):
            print("Download data")
            print("")
            cmd = "wget --user=%s --password=%s --directory-prefix=%s %s" %(user, password, saveDir, totPath)
            c1 = os.system(cmd)
        #: Assume there is a bz2-file now.
        #: If there is NO nc-file
        #: Unzip bz2-file
        if not os.path.isfile(ncfile):
            print("Unpack data")
            print("")
            bz2unzip = "bzip2 -d %s" %bz2file
            c2 = os.system(bz2unzip)
        #: Assume there is a nc-file now.
        #: If prepare for NWC-SAF
        if args.nwc:
            #: If there already is a link but it is corruped
            #: Remove link
            if os.path.islink(linkfile):
                if not os.path.exists(linkfile):
                    os.remove(linkfile)
            #: If there is NO link
            #: Create link
            if not os.path.islink(linkfile):
                os.symlink(ncfile, linkfile)
        
        #: Control the end-date to stop while-loop
        #: > is just a precaution in case there is a date miss match
        if datum >= stoppdatum:
            run=False

        #: Add a day to the date to download next day
        datum = datum + datetime.timedelta(days=1)
        
        #: Check so the download and unzip worked
        if (c1 != 0) or (c2 != 0):
            if (c1 != 0) or (c2 != 0):
                print("")
                print("--- Something went wrong with downloading ---")
                print(cmd)
                print("c1 = %d" %c1)
            if (c1 != 0) or (c2 != 0):
                print("")
                print("--- Something went wrong with unzip ---")
                print(bz2unzip)
                print("c2 = %d" %c2)
            pdb.set_trace()
        
    print("")
    print("Done")
    print("")
    
        
        
    
    
    
    