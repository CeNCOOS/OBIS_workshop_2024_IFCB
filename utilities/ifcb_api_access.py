import pyworms
import numpy as np
import pandas as pd
# IFCB API functions
import requests
import json
import pandas as pd
import numpy as np
# Ian's OBIS workshop R code translated to pytnon
# original R code is at:
# https://github.com/sccoos/OBIS_workshop_2023_IFCB/blob/main/README.md
def get_ifcb_metadata(bin):
    # code to get the metadata associeated with an IFCB
    # Note the Bin includes the info in ths case necessary to determine which IFCB
    # I'm not sure how generic this api is for IFCBS.
    # probably should include some error/logger instead of the print in the else statement
    #
    # input should be of the format:
    # DYYYYMMDDTHHmmss_IFCBNNN
    # where YYYY is 4 digit year
    # MM is two digit month (i.e. feb=02)
    # DD is two digit day
    # HH is two digit hour
    # mm is two digit minute
    # ss is two digit seconds
    # NNN is the serial number of the IFCB
    # D20210925T061303_IFCB158 would be an example
    # code either returns the metadata or the failure status
    #
    url="https://ifcb.caloos.org/api/metadata/"
    bin_url=url+bin
    response=requests.get(bin_url)
    if response.status_code==200:
        content=response.content
        content=json.loads(content)
        return(content)
    else:
        print("Metadata GET request failed with code: "+str(response.status_code))
        return(response.status_code)

# Ian's OBIS Workshop R code translated to python
def bin_has_autoclass(bin):
    # code to grab the autoclass information
    # input is the binID of the format
    # DYYYYMMDDTHHmmss_IFCBNNN
    # where YYYY is 4 digit year
    # MM is two digit month (i.e. feb=02)
    # DD is two digit day
    # HH is two digit hour
    # mm is two digit minute
    # ss is two digit seconds
    # NNN is the serial number of the IFCB
    # D20210925T061303_IFCB158 would be an example
    # code either returns if there are autoclass scores or the failure status
    url='https://ifcb.caloos.org/api/has_products/'
    bin_url=url+bin
    response=requests.get(bin_url)
    if response.status_code==200:
        content=response.content
        content=json.loads(content)       
        return(content['has_class_scores'])
    else:
        print('Autclass GET faile with code: '+str(response.status_code))
        return(response.status_code)

# Ian's read autoclass function translated to python
# Note labels is a list something like labels=["pid","Alexandrium_catenella"] 
def read_autoclass_csv(bin,labels):
    # code to grab the actual autoclass information
    # input is the binID and the labels
    # DYYYYMMDDTHHmmss_IFCBNNN    
    # NOTE URL needs to be changed below!
    url='https://ifcb.caloos.org/santa-cruz-municipal-wharf/'
    #url='https://ifcb.caloos.org/del-mar-mooring/' # place holder for the moment will use SC Wharf
    file_name=bin+"_class_scores.csv"
    bin_url=url+file_name
    lx=len(labels)
    # Need to replace blanks in name with "_"
    for i in np.arange(0,lx):
        # Not graceful code but a quick fix
        labels[i]=labels[i].replace(' ','_')
    try:
        autoclass=pd.read_csv(bin_url)
        if len(labels > 0):
            autoclass=autoclass[labels]
            return(autoclass)
        else:
            print("Target labels must be supplied (i.e column headers)")
            return(np.nan)
    except:
        # 
        print("Failed to read autoclass csv for bin "+bin)
        return(np.nan)

# Another of Ian's functions translated to python
def get_bin_details(bin):
    # code to get bin details
    # input is the binID
    # DYYYYMMDDTHHmmss_IFCBNNN    
    #
    url="https://ifcb.caloos.org/api/bin/"
    bin_url=url+bin
    response=requests.get(bin_url)
    if response.status_code==200:
        content=response.content
        content=json.loads(content)
        newdict={"bin_id":bin}
        newdict.update(content)
        return(newdict)
    else:
        print("Bin neighbors GET request failed with code: "+str(response.status_code))
        return(response.status_code)

# Date range IDs using Ian's function translated to python
def get_bins_in_range(start_date,end_date):
    # Dates should be of the form yyyy-mm-dd
    url="https://ifcb.caloos.org/santa-cruz-municipal-wharf/api/feed/temperature/start/"+start_date+"/end/"+end_date
    #url="https://ifcb.caloos.org/del-mar-mooring/api/feed/temperature/start/"+start_date+"/end/"+end_date
    response=requests.get(url)
    if response.status_code==200:
        content=response.content
        content=json.loads(content)
        content=pd.DataFrame.from_dict(content)
        content["pid"]=content["pid"].map(lambda x: x.lstrip("http://ifcb.caloos.org/del-mar-mooring/"))
        content=content["pid"]
        return(content)
    else:
        print('Failed to get all bins with range with code: '+str(response.status_code))
        return(response.status_code)

def get_worms_taxonomy(taxa):
    lx=np.arange(0,len(taxa))
    for i in lx:
        taxon=taxa[i]
        #print(taxon)
        wmentry=pyworms.aphiaRecordsByMatchNames(taxon,'marine_only')
        numentry=len(wmentry)
        #print(numentry)
        if numentry==1:
            df=pd.DataFrame(wmentry[0])
            bool=df['status']=='accepted'
            if bool[0]:
                newdf=df[["AphiaID","scientificname","lsid","rank","kingdom"]]
                #pdb.set_trace()
                [n,m]=newdf.shape
                newdf.insert(m,"intended_worms_taxon",taxon)
                if i==0:
                    wormsdf=newdf
                else:
                    wormsdf=pd.concat([wormsdf,newdf])
            else:
                print("Found record is currently not \"accepted\"")
        else:
            if numentry==0:
                print("No record found for taxon")
            else:
                # multiple entries found how do we deal with this?
                print("too many entries")
    return(wormsdf)

