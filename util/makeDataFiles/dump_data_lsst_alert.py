# Created Nov 2, 2021
# read in lsst-alert format and plot them.
# [R.Hlozek, R.Kessler ...]
import os, sys, yaml, shutil, glob, math, datetime
import logging, subprocess, json
import matplotlib.pyplot as plt

import numpy as np
# from   makeDataFiles_params    import *
# import makeDataFiles_util  as util
import pandas as pd
from pathlib import Path
import lsst.alert.packet
from fastavro import writer, reader
from copy import copy

import gzip

def make_dataframe(packet):
    df = pd.DataFrame(packet['diaSource'], index=[0])
    df_prv = pd.DataFrame(packet['prvDiaSources'])
    return pd.concat([df,df_prv], ignore_index=True)

def plot_lightcurve(dflc, name, days_ago=True):
    filter_color = {'g':'green', 'r':'red', 'u':'pink'}
    
    t = dflc.midPointTai
    xlabel = 'Time (MJD)'    
    plt.figure()
    
    for fid, color in filter_color.items():
        # plot detections in this filter:
        w = (dflc.filterName == fid) & ~dflc.psFlux.isnull()
        if np.sum(w):
            plt.errorbar(t[w],dflc.loc[w,'apFlux'],dflc.loc[w,'apFluxErr'],fmt='.',color=color)
            
        else:
            plt.errorbar(t[w],dflc.loc[w,'apFlux'],dflc.loc[w,'apFluxErr'],fmt='.',color=color)
    
    plt.gca().invert_yaxis()
    plt.xlabel(xlabel)
    plt.ylabel('Magnitude')
    plt.savefig("lc_%s.png"%name[:-8])
    plt.clf()

def plot_alert_avro(name):
    print(f"Reading {name}")
    with gzip.open(name, 'rb') as f:
        freader = reader(f)
        for alert in freader:
            dflc = make_dataframe(alert)
            plot_lightcurve(dflc,name)
            

def dump_alert_avro(name):
    print(f"Reading {name}")
    with gzip.open(name, 'rb') as f:
        freader = reader(f)
        for alert in freader:
            dflc = make_dataframe(alert)
            dflc.to_csv("df_%s.csv"%name[:-8])

name = sys.argv[1]

dump_alert_avro(name)
