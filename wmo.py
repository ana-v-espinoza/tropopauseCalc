import numpy as np
from metpy.calc import thickness_hydrostatic
from metpy.units import units
from metpy.constants import earth_gravity, dry_air_gas_constant

def wmo(pFull, TFull, lapseC=2.0*units("K/km"), height=False):
    """
    Implements NCAR's Fortran code in python:
        https://github.com/NCAR/ncl/blob/develop/ni/src/lib/nfpfort/stattrop_dp.f
    """

    nLev = pFull.size
    nLevm = nLev-1

    pMin = 85.0*units.mbar
    pMax = 450.0*units.mbar

    dZ = 2000.0*units.meters

    g = earth_gravity
    R = dry_air_gas_constant

    const = g/R

    found = False

    lapse = np.zeros(nLevm)*units.kelvin/units.km
    pHalf = np.zeros(nLevm)*units.mbar
    pTrop = 0*units.mbar
    for iLev in range(0, nLevm):
        lapse[iLev] = const*np.log(TFull[iLev]/TFull[iLev+1])/np.log(pFull[iLev]/pFull[iLev+1])
        pHalf[iLev] = (pFull[iLev]+pFull[iLev+1])*0.5

    for iLev in range(0,nLevm-1):
        if lapse[iLev] < lapseC and pFull[iLev] < pMax and not found:
            P1 = np.log(pHalf[iLev].magnitude)
            P2 = np.log(pHalf[iLev+1].magnitude)
            if (lapse[iLev] != lapse[iLev+1]):
                weight = (lapseC-lapse[iLev])/(lapse[iLev+1]-lapse[iLev])
                #tropopause pressure
                pTrop = np.exp(P1+weight*(P2-P1))*units.mbar
            else:
                pTrop = pHalf[iLev]

            p2km = pTrop*np.exp(-dZ*const/TFull[iLev])
            lapseAvg = 0
            lapseSum = 0
            kount = 0
            for L in range (iLev,nLevm):
                if pHalf[L] > p2km:
                    lapseSum = lapseSum + lapse[L]
                    kount = kount + 1
                    lapseAvg = lapseSum/kount
            found = lapseAvg < lapseC
            if not found:
                print ("Tropopause not found")
            else:
                iTrop = iLev
                pTrop = pMin if pTrop < pMin else pTrop
                break

    if height:
        z = thickness_hydrostatic(pFull[0:iTrop],TFull[0:iTrop])
        return z.to(units.km)

    return pTrop.to(units.mbar)
