import numpy as np
from metpy.calc import thickness_hydrostatic
from metpy.units import units

def birner(pFull, TFull, lapseC=2.0*units("K/km"), height=False):
    """
    Implements the calculation of the thermal tropopause as described by Birner in
    Appendix A of:
        T. Birner. Fine-scale structure of the extratropical tropopause region.
        Journal
    """

    # Calculate the heights of the pressure levels using the hypsometric equation
    z = np.zeros_like(pFull)*units.km
    for h in range(0,pFull.size):
        z[h] = thickness_hydrostatic(pFull[0:h+1],TFull[0:h+1])

    # Calculate the lapse rate through use of a centered difference
    # This needs the heights "z" at each pressure level, which can be calculated
    # using the hypsometric equation, or sent as a function argument
    lapse = (TFull[2:]-TFull[:-2])/(z[2:]-z[:-2])

    found = False
    for i in range(3,lapse.size):
        if lapse[i] >= lapseC:
            k = i
            for j in range(k,lapse.size-2):
                meanAbove = np.mean(lapse[j:j+2])
                meanBelow = np.mean(lapse[j-3:j-1])
                if meanAbove >= lapseC and meanBelow < lapseC:
                    if meanAbove > 0:
                        minTempIdx = np.argmin(lapse[j-3:j+2])
                        iTrop = k+minTempIdx
                        zTrop = z[iTrop]
                        TTrop = TFull[iTrop]
                    else:
                        print("linearly interpolated...")
                        minTempIdx = np.argmin(lapse[j-3:j+2])
                        iTrop = k+minTempIdx
                        # Linearly interpolate and find intersection point
                        ma = (TFull[j+2]-TFull[j])/(z[j+2]-z[j])
                        mb = (TFull[j-1]-TFull[j-3])/(z[j-1]-z[j-3])
                        zTrop = (TFull[j]-TFull[j-1]+mb*z[j-1]-ma*z[j])/(mb-ma)
                        TTrop = ma*(zTrop-z[j])+T[j]
                        # Find index of "layer" that has calculated tropopause
                        n = 0
                        while z[n] < zTrop:
                            iTrop = n
                    found = np.abs(zTrop-z[j]) <= 250*units.meters
                    found = found and pFull[iTrop] < 500*units.mbar
                    i2km = iTrop+1
                    while z[i2km] - z[iTrop] < 2000*units.meters:
                        found = found and (TFull[i2km]-TTrop)/(z[i2km]-zTrop) > lapseC
                        found = found and (TFull[i2km+1]-TTrop)/(z[i2km+1]-zTrop) > lapseC
                        i2km += 1
                    if found:
                        break
            if found:
                break
    if height:
        return zTrop.to(units.km)

    pTrop = pFull[iTrop]
    return pTrop.to(units.mbar)
