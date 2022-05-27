from ..rainbows import *


def test_to_df():

    r = SimulatedRainbow(
        signal_to_noise=10,
        dt=1 * u.minute,
        R=50)

    r_df = r.to_df()

    # ensure the length of the df is the same as the original rainbow
    assert len(r_df) == r.nflux

    # ensure we have the right column names
    columnnames = r_df.columns
    for colname in ['Time (d)', 'Wavelength (microns)', 'Flux', 'Flux Uncertainty']:
        assert colname in columnnames

    # check the values in the df match the rainbow
    assert r_df['Time (d)'].values[0] == r.time.to_value()[0] / 24.  # default=days
    assert r_df['Wavelength (microns)'].values[0] == r.wavelength.to_value()[0]
    assert r_df['Flux'].values[0] == r.flux[0, 0]
    assert r_df['Flux Uncertainty'].values[0] == r.uncertainty[0, 0]

    # test the timeformat parameter
    for timeformat in ['h', 'hour', 'day', 'minute', 'second', 's']:
        r_df = r.to_df(timeformat=timeformat)
        assert f'Time ({timeformat})' in r_df.columns


def test_to_nparray():
    r = SimulatedRainbow(
        signal_to_noise=100,
        dt=1 * u.minute,
        R=50)

    rflux, rfluxu, rtime, rwavel = r.to_nparray()

    assert len(rtime) == r.ntime
    assert len(rwavel) == r.nwave
    assert len(rtime)*len(rwavel) == r.nflux
    assert len(rflux.flatten()) == r.nflux
    assert len(rfluxu.flatten()) == r.nflux
    assert np.shape(rflux) == r.shape
    assert np.shape(rfluxu) == r.shape

    assert np.all(rflux == r.flux)
    assert np.all(rfluxu == r.uncertainty)
    assert np.all(rwavel == r.wavelength.to_value())
    assert np.all(rwavel == r.wavelength.to_value())

    assert np.all(rtime == r.time.to_value()/24.)  # the default is days

    # test if the hours format works
    rflux, rfluxu, rtime, rwavel = r.to_nparray(timeformat='h')
    assert np.all(rtime == r.time.to_value())

    # test if the minutes format works
    rflux, rfluxu, rtime, rwavel = r.to_nparray(timeformat='m')
    assert np.all(rtime == r.time.to_value()*60)

    # test if the minutes format works
    rflux, rfluxu, rtime, rwavel = r.to_nparray(timeformat='s')
    assert np.all(rtime == r.time.to_value()*3600)



