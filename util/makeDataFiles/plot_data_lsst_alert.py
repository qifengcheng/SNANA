# Created Nov 2, 2021
# read in lsst-alert format and plot them.
# [R.Hlozek, R.Kessler ...]
import os, sys, yaml, shutil, glob, math, datetime
import logging, subprocess, json

import numpy as np
from   makeDataFiles_params    import *
import makeDataFiles_util  as util

from pathlib import Path
import lsst.alert.packet
from fastavro import writer, reader
from copy import copy

import gzip

def plot_lightcurve(dflc, name, days_ago=True):
    filter_color = {'g':'green', 'r':'red', 'u':'pink'}
    if days_ago:
        now = Time.now().jd
        t = dflc.midPointTai - now
        xlabel = 'Days Ago'
    else:
        t = dflc.midPointTai
        xlabel = 'Time (JD)'    
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
    plt.savefig("lc_%s.png"%name)
    plt.clf()

def read_alert_avro(name):
    print(f"Reading {name}")
    with gzip.open(name, 'rb') as f:
        freader = reader(f)
        for alert in freader:
            dflc = make_dataframe(alert)
            plot_lightcurve(dflc)