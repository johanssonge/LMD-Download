'''
Created on Feb 9, 2021

@author: Erik Johansson
'''
import datetime
import os
import pdb


if __name__ == '__main__':
    startdate = "2018 04 01"
    enddate = "2018 10 31"
    mainSaveDir = "/home/erikj/Projects/Data/Ostia"#"/scratch/erikj/Data/Ostia"
    mainWebAdress = "https://podaac-tools.jpl.nasa.gov/drive/files/allData/ghrsst/data/L4/GLOB/UKMO/OSTIA"
    user="smhi_erik"
    password="@AItE8W1EwHte82XFdK"

    datum = datetime.datetime.strptime(startdate, "%Y %m %d")
    stoppdatum = datetime.datetime.strptime(enddate, "%Y %m %d")
    c1 = 0
    c2 = 0
    run=True
    while run:
        saveDir = mainSaveDir + "/%i/%02i" %(datum.year, datum.month)
        if not os.path.isdir(saveDir):
            os.makedirs(saveDir)
        webAdress = mainWebAdress + "/%i/%03i" %(datum.year, datum.timetuple().tm_yday)
        filename = "%i%02i%02i-UKMO-L4HRfnd-GLOB-v01-fv02-OSTIA.nc.bz2" %(datum.year, datum.month, datum.day)
        totPath = webAdress + "/" + filename
        
        bz2file = "%s/%s" %(saveDir,filename)
        ncfile = bz2file.replace(".bz2", "")
        if not (os.path.isfile(ncfile) or os.path.isfile(bz2file)):
            print("Download data")
            cmd = "wget --user=%s --password=%s --directory-prefix=%s %s" %(user, password, saveDir, totPath)
            c1 = os.system(cmd)
        if not os.path.isfile(ncfile):
            print("Unpack data")
            bz2unzip = "bzip2 -d %s" %bz2file
            c2 = os.system(bz2unzip)
        if datum >= stoppdatum:
            run=False
        
          
        datum = datum + datetime.timedelta(days=1)
        if (c1 != 0) or (c2 != 0):
            print("something went wrong")
            pdb.set_trace()
        
    print("")
    print("Done")
    print("")
    pdb.set_trace()
    
        
        
    
    
    
    