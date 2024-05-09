import numpy as np


def test_wdm():
    # Create a WDM object
    from wdm_wavelet.wdm import WDM

    fake_strain = np.random.randn(4096)

    wdm = WDM(32, 64, 6, 10)
    tf_map = wdm.t2w(fake_strain, sample_rate=4096.)

    assert len(tf_map.data) == tf_map.n_freq
    assert tf_map.df == 4096./32/2.
