import numpy as np
import pandas as pd
import pyworms # pyworms package is not in Anaconda distribution
import re
import requests

# We adopted some code contributed by Joe Futrelle (WHOI)

def get_metric_timeseries(dataset, metric, start='2000-01-01', end='2100-01-01'):
    url = f'{BASE_URL}/{dataset}/api/feed/{metric}/start/{start}/end/{end}'
    r = requests.get(url)
    assert r.ok
    return r.json()


def shorten(fq_pid):
    return re.sub('.*/', '', fq_pid)


def list_bins(dataset, start='2000-01-01', end='2100-01-01'):
    metric_timeseries = get_metric_timeseries(dataset, METRIC, start, end)
    metric_timeseries = sorted(metric_timeseries, key=lambda record: record['date'])
    return [shorten(record['pid']) for record in metric_timeseries]


def latest_bin(dataset):
    return list_bins(dataset)[-1]


def basic_info(pid):
    url = f'{BASE_URL}/api/bin/{pid}?include_coordinates=False'
    r = requests.get(url)
    assert r.ok
    record = r.json()
    return {
        'datetime': record['timestamp_iso'],
        'previous_bin': record['previous_bin_id'],
        'next_bin': record['next_bin_id'],
        'latitude': record['lat'],
        'longitude': record['lng'],
        'depth': record['depth'],
        'instrument': record['instrument'],
        'number_of_rois': record['num_images'],
        'ml_analyzed': float(re.sub(' .*', '', record['ml_analyzed'])),
        'concentration': record['concentration'],
        'sample_type': record['sample_type'],
        'cruise': record['cruise'],
        'cast': record['cast'],
        'niskin': record['niskin'],
    }

# presently this acquires the name/ID from the autoclass lookup table
# autoclass lookup table includes SeaBASS namespace for non-biota particles

# ultimately for some taxa expect to use WoRMS API to provide name/ID at higher rank
# in that case consider adding a function that uses identificationQualifier

def get_sci_attrs(r):
    if r['Taxon status'] == 'unaccepted':
        r['scientificNameID'] = "urn:lsid:marinespecies.org:taxname:" + str(r['AphiaID_accepted'])
        r['scientificName'] = r['ScientificName_accepted']
#    if r['Taxon status'] == 'NA': 
#        r['scientificNameID'] = r['LSID'] 
#        r['scientificName'] = r['ScientificName_accepted'] # did not manually populate this column when status NA
# the following else statement applies to all except status unaccepted
    else:
        r['scientificNameID'] = r['LSID'] 
        r['scientificName'] = r['ScientificName']
    return r

# Code for this function was developed from an initial prototype by Kathy Qi (EDI Fellow at WHOI)
# https://github.com/klqi/EDI-NES-LTER-2019/tree/master/auto_join

# We would like to split this function into multiple functions
# to accommodate decisions with regard to interpreting the autoclass scores
# and with regard to the particular taxa that the provider would like to provide to OBIS

# We would like to accommodate different thresholds for different taxa

# If subsetting only to particular taxa, we would need to alert the provider re: false positives:
# e.g., consider adding columns to the intermediate data table to report when
# an autoclass label other than the set of targeted labels had a higher autoclass score

# Presently hard coding for the column with autoclass labels
# autoclass list version is class_vNone_SIO_Delmar_mooring_20220225
 

def get_sci_id_name(url, dataset, pid, lookup_path, threshold):
    path = f'{url}/{dataset}/{pid}_class_scores.csv'
    df = pd.read_csv(path)
    classes = df.iloc[:, 1:]
    classes = classes.mask(classes < threshold) # presently constrained to single threshold
    winner = classes.idxmax(axis=1)
    winner.name = 'autoclass'
    winner_df = winner.to_frame()
    lookup = pd.read_csv(lookup_path)
    merged = pd.merge(winner_df, lookup, how="left", left_on="autoclass", right_on="class_vNone_SIO_Delmar_mooring_20220225")
    df_sci_id = merged.apply(get_sci_attrs, axis=1)
    df_sci_id = df_sci_id[["autoclass","scientificName","scientificNameID","Kingdom"]] # retain autoclass label
    occurance_id = df["pid"] 
    new_df = pd.concat([occurance_id, df_sci_id], axis=1)
    
    return new_df
# Code for this function was developed from an initial prototype by Kathy Qi (EDI Fellow at WHOI)
# https://github.com/klqi/EDI-NES-LTER-2019/tree/master/auto_join

# note this presently only retains one of the recommended features

def get_size(url, dataset, pid, lookup_path):
    path = f'{url}/{dataset}/{pid}_features.csv'
    df = pd.read_csv(path)
    size = df["Area"] 
    return size
    
def get_valid_sci_attrs(row):
    # print(row['roi']) # this provides a visual indicator of progress when running this function 
    if not pd.isnull(row['worms']):
        a = int(row['worms'])
        # print(a) # this provides a visual indicator of progress when running this function
        record = pyworms.aphiaRecordByAphiaID(a)
        row['valid_AphiaID'] = record['valid_AphiaID']
        row['valid_name'] = record['valid_name']
        row['valid_kingdom'] = record['kingdom']
    else:
        row['valid_AphiaID'] = np.nan
        row['valid_name'] = np.nan
        row['valid_kingdom'] = np.nan
    return row
