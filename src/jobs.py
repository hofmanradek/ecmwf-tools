"""
simple tool for preparing and submitting batch jobs at ECMWF server...
Radek Hofman
"""

import datetime
import os

DATE_FORMAT = "%Y%m%d"  # 20110901
JOB_PREFIX = "job_"

def prepare_job_files(start, end, step, out_dir, ecmwf_out_dir=None):
    """
    creates job files for submission
    """
    
    counter = 0
    d1 = start
    
    while d1 < end:
    
        d0 = start + step*counter
        d1 = start + step*(counter+1)
    
        d0_str = d0.strftime(DATE_FORMAT)
        d1_str = d1.strftime(DATE_FORMAT)        
    
        with open("../templates/flex_ecmwf_GLOBALETA.tmpl", "r+") as f:
            s = f.read()            
            s = s.replace("hovex_day1", d0_str).replace("hovex_day2", d1_str)
            
            job_name = JOB_PREFIX+"%4.4d_%s_%s" % (counter, d0_str, d1_str)

            if ecmwf_out_dir == None:
                #modify to fit your needs...
                s = s.replace("hovex_dir", job_name)
            else:
                #or some provided file name will be used
                s = s.replace("hovex_dir", ecmwf_out_dir)
                                    
            with open(os.path.join(out_dir, job_name), "w+") as f:
                f.write(s)

            counter += 1


def panda(s):
    """
    submits a job
    """
    command = "ecaccess-job-submit %s" % s
    print command
    os.system(command)


def submit_jobs(path):
    """
    lists all jobs in directory and submits them
    """
    
    #retrieve all jobs
    jobs = map(lambda x: os.path.join(path, x), filter(lambda x: x.startswith(JOB_PREFIX), os.listdir(path)))
    
    #submit all jobs...
    map(panda, jobs)


def main():
    """
    prepares a set of jobs for given time range and step and submits it...
    """
    
    #prepare job file to submit
    start = datetime.datetime(2011, 9, 01, 0, 0, 0)
    #end   = datetime.datetime(2011, 9, 02, 0, 0, 0)
    end   = datetime.datetime(2011, 12, 01, 0, 0, 0)
    step  = datetime.timedelta(days=1)
    out_dir = "../jobs"
    
    prepare_job_files(start, end, step, out_dir)
    
    submit_jobs(out_dir)
    

if __name__ == "__main__":
    print "Hello! Panda!"
    main()