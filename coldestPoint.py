import numpy as np
from metpy.calc import thickness_hydrostatic
from metpy.units import units

def coldestPoint(pFull,TFull, lapseC=2.0*units("K/km"), height=False):
    """
    Finds the tropopause as the coldest point in a sounding
    """
    iTrop = np.argmin(TFull)
    if height:
        z = thickness_hydrostatic(pFull[0:iTrop],TFull[0:iTrop])
        return z.to(units.km)
    pTrop = pFull[iTrop]
    return pTrop.to(units.mbar)
