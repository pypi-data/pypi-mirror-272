# WDM wavelet transform

This package hosts the python version of WDM wavelet used in coherentWaveBurst(cWB) search.

## Installation

```bash
pip install wdm-wavelet
```

## Example

Generate a timeseries waveform
```python
from pycbc.waveform import get_td_waveform
import matplotlib.pyplot as plt

hp, hc = get_td_waveform(approximant="IMRPhenomTPHM",
                         mass1=20,
                         mass2=20,
                         spin1z=0.9,
                         spin2z=0.4,
                         inclination=1.23,
                         coa_phase=2.45,
                         distance=100,
                         delta_t=1.0/2048,
                         f_lower=20)
```

Apply WDM wavelet transform
```python
from wdm_wavelet.wdm import WDM

wdm = WDM(32, 64, 6, 10)

tf_map = wdm.t2w(hp)

tf_map.plot_energy()
```

Inverse WDM wavelet transform
```python
ts = wdm.w2t(tf_map)

plt.plot(ts)
```

For more examples, please refer to the [example notebook](https://git.ligo.org/yumeng.xu/wdm-wavelet/-/blob/main/notebook/transform_GW.ipynb).
