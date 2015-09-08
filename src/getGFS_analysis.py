import os
import datetime
import time
import sys

"""
getting of GFS ANL - analyses
"""

STORAGE_DIR = "../data"
WGET = "wget"      # Path to local wget binary
FTPSERVER = "ftp://nomads.ncdc.noaa.gov/GFS/analysis_only"
FTPUSER   = "anonymous"
FTPPASSWD = "hofman.radek@gmail.com"
FORECAST_INCR_HRS = 3  # time step of forecasts on the server (GFS has 3 hour step)



def main(d0, d1, data_type):
    """
    """

    d = d0

    d0_str = d0.strftime("%Y%m%d")
    d1_str = d1.strftime("%Y%m%d")


    exts = {3: ".grb",
            4: ".grb2"}

    ress = {3: "1p0",
            4: "0p5"}

    #check if directory exists
    out_path = STORAGE_DIR+os.sep+d0_str+"_"+d1_str+"-"+ress[data_type]
    if not os.path.exists(out_path):
        os.makedirs(out_path)


    syn_hrs = ["0000", "0600", "1200", "1800"]

    fct_hrs = ["000", "003"]



    #start available string
    s  = "DATE     TIME         FILENAME     SPECIFICATIONS\n"
    s += "YYYYMMDD HHMISS\n"
    s += "________ ______      __________      __________\n"

    while d < d1:
        Ym = d.strftime("%Y%m")
        Ymd = d.strftime("%Y%m%d")

        for syn_hr in syn_hrs:
            for fct_hr in fct_hrs:
                #filename = "gfsanl_4_20110901_0000_006.grb2"
                filename = "gfsanl_"+str(data_type)+"_"+Ymd+"_"+syn_hr+"_"+fct_hr+exts[data_type]

                the_url = FTPSERVER+"/"+Ym+"/"+Ymd+"/"+filename

                hr = "%2.2d" % (int(syn_hr[:2])+int(fct_hr))
                s += Ymd+" "+hr+"0000"
                s += "      " + filename
                s += "      ON DISC"
                s += "\n"

                print "Fetching", the_url

                # Go ahead and fetch it now

                the_command = WGET + " " +                            \
                             "--http-user=" + FTPUSER + " " +         \
                             "--http-passwd=" + FTPPASSWD + " " +   \
                             "--output-document=" + out_path + "/" + \
                             filename + " " +   \
                             "--tries=5" + " " +                     \
                             "--retry-connrefused" + " " +           \
                             "--continue" + " " +                    \
                             "--timeout=300" + " " +                 \
                             "--wait=10" + " " +                     \
                             "--waitretry=10" + " " +                \
                             the_url

                print "Executing " + the_command
                os.system(the_command)
        
				#incerement to the next daty (another directory)
        d += datetime.timedelta(days=1)


    with open(out_path+os.sep+"AVAILABLE", "w+") as f:
        f.write(s)

if __name__ == "__main__":



    #d0_str = "20110901"
    #d1_str = "20110902" #"20111130"
    #data_type = 3  # 3 - 1.0 deg, 4 - 0.5 deg


    if len(sys.argv) > 3:
        d0_str = sys.argv[1]
        d1_str = sys.argv[2]
        data_type = int(sys.argv[3])
        d0 = datetime.datetime.strptime(d0_str, "%Y%m%d")
        d1 = datetime.datetime.strptime(d1_str, "%Y%m%d")

        main(d0, d1, data_type)
    else:
        print "Usage: getGFS_analysis.py <from YYYYMMDD> <to YYYYMMDD> <[3=1 deg,4=0.5deg]>"

