"""
Uses sounding data from University of Wyoming's sounding archive, retrieved
through Siphon, to both visually/subjectively determine tropopause height and
through the use of our code
"""

import numpy as np
from datetime import datetime
from metpy.units import units
from metpy.interpolate import interpolate_1d
from siphon.simplewebservice.wyoming import WyomingUpperAir
from matplotlib import pyplot as plt
from metpy.plots import SkewT
from tropCalc import tropCalc

def grabSounding(date, station):
    df = WyomingUpperAir.request_data(date,station)
    pFull = df["pressure"].values*units(df.units["pressure"])
    TFull = df["temperature"].values*units(df.units["temperature"])
    return pFull, TFull

calculateTrop = False
savePlots = True

year = 2020
month = 7
day = 9
hour = 12
date = datetime(year, month, day, hour)
# Amarillo, TX
station = "AMA"

lapseC = 2*units.kelvin/units.km
height = False

pFull, TFull = grabSounding(date, station)

pInterp = np.arange(pFull[0].m, pFull[1].m, (pFull[1].m-pFull[0].m)/10.0)*units.mbar
for i in range(1,pFull.size-1):
    if pFull[i+1]-pFull[i] != 0:
        tmp = np.arange(pFull[i].m, pFull[i+1].m, (pFull[i+1].m-pFull[i].m)/10.0)*units.mbar
        pInterp = np.concatenate((pInterp,tmp))

TInterp = interpolate_1d(pInterp, pFull, TFull)

if calculateTrop:
    print("WMO: ", tropCalc(pFull,TFull,lapseC=lapseC,height=height,method="wmo"))
    print("Birner: ", tropCalc(pFull,TFull,lapseC=lapseC,height=height,method="birner"))
    print("Coldest Point: ", tropCalc(pFull,TFull,lapseC=lapseC,height=height,method="cp"))

    print("WMO (interp): ", tropCalc(pInterp,TInterp,lapseC=lapseC,height=height,method="wmo"))
    print("Birner: (interp) ", tropCalc(pInterp,TInterp,lapseC=lapseC,height=height,method="birner"))
    print("Coldest Point: (interp) ", tropCalc(pInterp,TInterp,lapseC=lapseC,height=height,method="cp"))

if savePlots:
    titleStr = "AMA -- {}".format(date)
    skew = SkewT()
    skew.plot(pFull, TFull, 'r')
    skew.plot_dry_adiabats()
    skew.plot_moist_adiabats()
    skew.plot_mixing_lines()
    skew.ax.set_ylim(1000, 50)
    skew.ax.set_title(titleStr)
    plt.savefig("{}-{}-{}_{}.png".format(year,month,day,hour))

    titleStr = "(no skew) AMA -- {}".format(date)
    skew = SkewT(rotation=0)
    skew.plot(pFull, TFull, 'r')
    skew.plot_dry_adiabats()
    skew.plot_moist_adiabats()
    skew.plot_mixing_lines()
    skew.ax.set_ylim(1000, 50)
    skew.ax.set_xlim(-80, 60)
    skew.ax.set_title(titleStr)
    plt.savefig("noSkew_{}-{}-{}_{}.png".format(year,month,day,hour))
