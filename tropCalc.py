from birner import birner
from wmo import wmo
from coldestPoint import coldestPoint
from metpy.units import units

def tropCalc(pFull, TFull, lapseC=2.0*units("K/km"), height=False, method="wmo"):
    if method == "birner":
        return birner(pFull,TFull,lapseC=lapseC,height=height)
    elif method == "cp":
        return coldestPoint(pFull,TFull,lapseC=lapseC,height=height)
    else:
        return wmo(pFull,TFull,lapseC=lapseC,height=height)
