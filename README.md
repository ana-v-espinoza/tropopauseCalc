# tropopauseCalc
Working on Issue #1324 on Unidata's Metpy repo:
https://github.com/Unidata/MetPy/issues/1324

### Authors 

Lydia M. Bunting, Ana Victoria Espinoza, Zyanya Ramirez-Diaz, with special thanks
to Dr. Eric Bruning for valuable input 

### Summary

### Methodology
Two methods are implemented to calculate the tropopause from sounding data.
Similarly to other MetPy sounding functions, these methods take two `pint.Quanity`
objects, pressure and temperature, as function arguments. Both methods use the
WMO definition for tropopause height: 

```
The lowest level at which the lapse rate decreases to $2 \frac{K}{km}$ or
less, provided also the average lapse rate between this level and all higher
levels within 2 kilometers does not exceed $2 \frac{K}{km}.
```

The first method is based on the tropopause calculation code written in Fortran
for NCL (NCAR Command Language), which applies a forward difference to determine
the lapse rate for all heights. The criteria above is then implemented through
simple if-statements. 

The second method follows Birner (2006), who implemented the same WMO definition
of the thermal tropopause in an updated form to make use of high resolution
(1Hz) radiosonde data. The lapse rate is approximated using a 2 point centered
difference and the same lapse rate threshold is checked. Due to the availability
of higher resolution data, Birner applies several more criteria to the
determination of the tropopause. Details can be found in Appendix A of Birner
(2006). 

### Test Cases 

Sounding from various dates throughout the year were passed through the methods
to check their accuracy: 01/19/2020, 04/01/2020, 07/09/2020, and 09/23/2020. All
soundings were launched from Amarillo, TX at 12Z.

These test cases can be ran by using the environment.yml file to create the
appropriate conda environment: 

```
conda env create --file environment.yml
```

And running through python: 

```
python testTropCalc.py
```

### Results 

For our test cases, the NCAR implementation performed better (when compared to
a subjective approximation of tropopause height) for the summer and winter
sounding when the atmosphere does not present complex stability environments in
the upper-troposphere/lower-stratosphere. 

While the Birner implementation requires high resolution data, it appears that
it performs better in the spring and fall cases when the jet stream is further
south and moist deep convection could create changes to stability in the
upper-troposphere/lower-stratosphere. 

### Citations  

Citations found in the document `checkpoint1_ZR_LB_RE_ipynb` found in this repo

### Relevant Links
**NCAR Command Language (NCL) documentation for tropopause calculation:**  
`https://www.ncl.ucar.edu/Document/Functions/Built-in/trop_wmo.shtml`

**NLC tropopause calculation source code:**  
`https://github.com/NCAR/ncl/blob/develop/ni/src/lib/nfpfort/stattrop_dp.f`

**Other MetPy calculations done with soundings (to emulate the MetPy coding "style"):**  
`https://unidata.github.io/MetPy/latest/api/generated/metpy.calc.html#soundings`

**Example on how to make sounding calculations using MetPy**  
`https://unidata.github.io/MetPy/latest/tutorials/upperair_soundings.html`

**Requesting Wyoming upper air data using Siphon:**  
`https://unidata.github.io/siphon/latest/examples/upperair/Wyoming_Request.html`
