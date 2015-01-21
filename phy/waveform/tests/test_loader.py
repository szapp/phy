
# -*- coding: utf-8 -*-

"""Tests of waveform loader."""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import os

import numpy as np
from numpy.testing import assert_array_equal
import numpy.random as npr
from pytest import raises

from ...datasets.mock import artificial_traces
from ..loader import WaveformLoader


#------------------------------------------------------------------------------
# Tests
#------------------------------------------------------------------------------

def test_loader():
    n_samples_trace, n_channels = 1000, 100
    n_samples = 40
    n_spikes = n_samples_trace // (2 * n_samples)

    traces = artificial_traces(n_samples_trace, n_channels)
    spike_times = np.cumsum(npr.randint(low=0, high=2 * n_samples,
                                        size=n_spikes))

    with raises(ValueError):
        WaveformLoader(traces)

    # Create a loader.
    loader = WaveformLoader(traces, n_samples=n_samples)
    assert id(loader.traces) == id(traces)
    loader.traces = traces

    # Extract a waveform.
    t = spike_times[0]
    waveform = loader.load_at(t)
    assert waveform.shape == (n_samples, n_channels)
    assert_array_equal(waveform, traces[t - 20:t + 20, :])

    # Invalid time.
    with raises(ValueError):
        loader.load_at(2000)

    # With filter.
    def my_filter(x):
        return x * x

    traces_filtered = my_filter(traces)

    loader = WaveformLoader(traces, n_samples=n_samples, filter=my_filter)

    t = spike_times[5]
    waveform_filtered = loader.load_at(t)

    assert np.allclose(waveform_filtered, traces_filtered[t - 20:t + 20, :])
