# -*- coding: utf-8 -*

# Compatibility
from __future__ import absolute_import, division, print_function

# Imports
import warnings
import spectrum
import numpy as np
import scipy as sp
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import LineCollection
import matplotlib as mpl
from scipy.signal import welch, lombscargle
from matplotlib import pyplot as plt

# biosppy imports
import biosppy
from biosppy import utils

# Local imports/HRV toolbox imports
import pyhrv.tools as tools

# Surpress Lapack bug 0038 warning from scipy (may occur with older versions of the packages above)
warnings.filterwarnings(action="ignore", module="scipy")

    
class frequency_domain():
    def __init__(self):
        pass 
    
    def welch_psd(self,nni=None,
                  rpeaks=None,
                  fbands=None,
                  nfft=2**12,
                  detrend=True,
                  window='hamming',
                  show=True,
                  show_param=True,
                  legend=True,
                  mode='normal'):
    
        # Check input values
        nn = tools.check_input(nni, rpeaks)
    
        # Verify or set default frequency bands
        fbands = self._check_freq_bands(fbands)
    
        # Resampling (with 4Hz) and interpolate
        # Because RRi are unevenly spaced we must interpolate it for accurate PSD estimation.
        fs = 4
        t = np.cumsum(nn)
        t -= t[0]
        f_interpol = sp.interpolate.interp1d(t, nn, 'cubic')
        t_interpol = np.arange(t[0], t[-1], 1000./fs)
        nn_interpol = f_interpol(t_interpol)
    
        # Subtract mean value from each sample for surpression of DC-offsets
        if detrend:
            nn_interpol = nn_interpol - np.mean(nn_interpol)
    
        # Adapt 'nperseg' according to the total duration of the NNI series (5min threshold = 300000ms)
        if t.max() < 300000:
            nperseg = nfft
        else:
            nperseg = 300
    
        # Compute power spectral density estimation (where the magic happens)
        frequencies, powers = welch(
            x=nn_interpol,
            fs=fs,
            window=window,
            nperseg=nperseg,
            nfft=nfft,
            scaling='density'
        )
    
        # Metadata
        args = (nfft, window, fs, 'cubic')
        names = ('fft_nfft', 'fft_window', 'fft_resampling_frequency', 'fft_interpolation',)
        meta = utils.ReturnTuple(args, names)
    
        if mode not in ['normal', 'dev', 'devplot']:
            warnings.warn("Unknown mode '%s'. Will proceed with 'normal' mode." % mode, stacklevel=2)
            mode = 'normal'
    
        # Normal Mode:
        # Returns frequency parameters, PSD plot figure and no frequency & power series/arrays
        if mode == 'normal':
            # Compute frequency parameters
            params, freq_i = self._compute_parameters('fft', frequencies, powers, fbands)
    
            # Plot PSD
            figure = self._plot_psd('fft', frequencies, powers, freq_i, params, show, show_param, legend)
            figure = utils.ReturnTuple((figure, ), ('fft_plot', ))
    
            # Output
            return tools.join_tuples(params, figure, meta)
    
        # Dev Mode:
        # Returns frequency parameters and frequency & power series/array; does not create a plot figure nor plot the data
        elif mode == 'dev':
            # Compute frequency parameters
            params, _ = self._compute_parameters('fft', frequencies, powers, fbands)
    
            # Output
            return tools.join_tuples(params, meta), frequencies, (powers / 10 ** 6)
    
        # Devplot Mode:
        # Returns frequency parameters, PSD plot figure, and frequency & power series/arrays
        elif mode == 'devplot':
            # Compute frequency parameters
            params, freq_i = self._compute_parameters('fft', frequencies, powers, fbands)
    
            # Plot PSD
            figure = self._plot_psd('fft', frequencies, powers, freq_i, params, show, show_param, legend)
            figure = utils.ReturnTuple((figure, ), ('fft_plot', ))
    
            # Output
            return tools.join_tuples(params, figure, meta), frequencies, (powers / 10 ** 6)
    
    def lomb_psd(self,
            nni=None,
            rpeaks=None,
            fbands=None,
            nfft=2**8,
            ma_size=None,
            show=True,
            show_param=True,
            legend=True,
            mode='normal'
        ):
        # Check input
        nn = tools.check_input(nni, rpeaks)
    
        # Verify or set default frequency bands
        fbands = self._check_freq_bands(fbands)
        t = np.cumsum(nn)
        t -= t[0]
    
        # Compute PSD according to the Lomb-Scargle method
        # Specify frequency grid
        frequencies = np.linspace(0, 0.41, nfft)
        # Compute angular frequencies
        a_frequencies = np.asarray(2 * np.pi / frequencies)
        powers = np.asarray(lombscargle(t, nn, a_frequencies, normalize=True))
    
        # Fix power = inf at f=0
        powers[0] = 2
    
        # Apply moving average filter
        if ma_size is not None:
            powers = biosppy.signals.tools.smoother(powers, size=ma_size)['signal']
    
        # Define metadata
        meta = utils.ReturnTuple((nfft, ma_size, ), ('lomb_nfft', 'lomb_ma'))
    
        if mode not in ['normal', 'dev', 'devplot']:
            warnings.warn("Unknown mode '%s'. Will proceed with 'normal' mode." % mode, stacklevel=2)
            mode = 'normal'
    
        # Normal Mode:
        # Returns frequency parameters, PSD plot figure and no frequency & power series/arrays
        if mode == 'normal':
            # ms^2 to s^2
            powers = powers * 10 ** 6
    
            # Compute frequency parameters
            params, freq_i = self._compute_parameters('lomb', frequencies, powers, fbands)
    
            # Plot parameters
            figure = self._plot_psd('lomb', frequencies, powers, freq_i, params, show, show_param, legend)
            figure = utils.ReturnTuple((figure, ), ('lomb_plot', ))
    
            # Complete output
            return tools.join_tuples(params, figure, meta)
    
        # Dev Mode:
        # Returns frequency parameters and frequency & power series/array; does not create a plot figure nor plot the data
        elif mode == 'dev':
            # Compute frequency parameters
            params, _ = self._compute_parameters('lomb', frequencies, powers, fbands)
    
            # Complete output
            return tools.join_tuples(params, meta), frequencies, powers
    
        # Devplot Mode:
        # Returns frequency parameters, PSD plot figure, and frequency & power series/arrays
        elif mode == 'devplot':
            # ms^2 to s^2
            powers = powers * 10**6
    
            # Compute frequency parameters
            params, freq_i = self._compute_parameters('lomb', frequencies, powers, fbands)
    
            # Plot parameters
            figure = self._plot_psd('lomb', frequencies, powers, freq_i, params, show, show_param, legend)
            figure = utils.ReturnTuple((figure, ), ('lomb_plot', ))
    
            # Complete output
            return tools.join_tuples(params, figure, meta), frequencies, powers
    
    
    # TODO update docstring
    def ar_psd(self,nni=None,
               rpeaks=None,
               fbands=None,
               nfft=2**12,
               order=16,
               show=True,
               show_param=True,
               legend=True,
               mode='normal'):
        # Check input
        nn = tools.check_input(nni, rpeaks)
    
        # Verify or set default frequency bands
        fbands = self._check_freq_bands(fbands)
    
        # Resampling (with 4Hz) and interpolate
        # Because RRi are unevenly spaced we must interpolate it for accurate PSD estimation.
        fs = 4
        t = np.cumsum(nn)
        t -= t[0]
        f_interpol = sp.interpolate.interp1d(t, nn, 'cubic')
        t_interpol = np.arange(t[0], t[-1], 1000./fs)
        nn_interpol = f_interpol(t_interpol)
    
        # Compute autoregressive PSD
        ar = spectrum.pyule(data=nn_interpol, order=order, NFFT=nfft, sampling=fs, scale_by_freq=False)
        ar()
    
        # Get frequencies and powers
        frequencies = np.asarray(ar.frequencies())
        psd = np.asarray(ar.psd)
        powers = np.asarray(10 * np.log10(psd) * 10**3)     # * 10**3 to compensate with ms^2 to s^2 conversion
                                                            # in the upcoming steps
    
        # Define metadata
        meta = utils.ReturnTuple((nfft, order, fs, 'cubic'), ('ar_nfft', 'ar_order', 'ar_resampling_frequency',
                                                              'ar_interpolation'))
    
        if mode not in ['normal', 'dev', 'devplot']:
            warnings.warn("Unknown mode '%s'. Will proceed with 'normal' mode." % mode, stacklevel=2)
            mode = 'normal'
    
        # Normal Mode:
        # Returns frequency parameters, PSD plot figure and no frequency & power series/arrays
        if mode == 'normal':
            # Compute frequency parameters
            params, freq_i = self._compute_parameters('ar', frequencies, powers, fbands)
    
            # Plot PSD
            figure = self._plot_psd('ar', frequencies, powers, freq_i, params, show, show_param, legend)
            figure = utils.ReturnTuple((figure, ), ('ar_plot', ))
    
            # Complete output
            return tools.join_tuples(params, figure)
    
        # Dev Mode:
        # Returns frequency parameters and frequency & power series/array; does not create a plot figure nor plot the data
        elif mode == 'dev':
            # Compute frequency parameters
            params, _ = self._compute_parameters('ar', frequencies, powers, fbands)
    
            # Output
            return tools.join_tuples(params, meta), frequencies, (powers / 10 ** 6)
    
        # Devplot Mode:
        # Returns frequency parameters, PSD plot figure, and frequency & power series/arrays
        elif mode == 'devplot':
            # Compute frequency parameters
            params, freq_i = self._compute_parameters('ar', frequencies, powers, fbands)
    
            # Plot PSD
            figure = self._plot_psd('ar', frequencies, powers, freq_i, params, show, show_param, legend)
            figure = utils.ReturnTuple((figure, ), ('ar_plot', ))
    
            # Complete output
            return tools.join_tuples(params, figure, meta), frequencies, (powers / 10 ** 6)
    
    
    def _compute_parameters(self,method, frequencies, power, freq_bands):
        # Compute frequency resolution
        df = (frequencies[1] - frequencies[0])
    
        # Get indices of freq values within the specified freq bands
        ulf_i, vlf_i, lf_i, hf_i = self._get_frequency_indices(frequencies, freq_bands)
        ulf_f, vlf_f, lf_f, hf_f = self._get_frequency_arrays(frequencies, ulf_i, vlf_i, lf_i, hf_i)
    
        # Absolute powers
        if freq_bands['ulf'] is not None:
            ulf_power = np.sum(power[ulf_i]) * df
        vlf_power = np.sum(power[vlf_i]) * df
        lf_power = np.sum(power[lf_i]) * df
        hf_power = np.sum(power[hf_i]) * df
        abs_powers = (vlf_power, lf_power, hf_power, ) if freq_bands['ulf'] is None else (ulf_power, vlf_power, lf_power,
                                                                                          hf_power,)
        total_power = np.sum(abs_powers)
    
        # Peak frequencies
        if freq_bands['ulf'] is not None:
            ulf_peak = ulf_f[np.argmax(power[ulf_i])]
    
        # Compute Peak values and catch exception caused if the number of PSD samples is too low
        try:
            vlf_peak = vlf_f[np.argmax(power[vlf_i])]
            lf_peak = lf_f[np.argmax(power[lf_i])]
            hf_peak = hf_f[np.argmax(power[hf_i])]
            peaks = (vlf_peak, lf_peak, hf_peak,) if freq_bands['ulf'] is None else (ulf_peak, vlf_peak, lf_peak, hf_peak,)
        except ValueError as e:
            if 'argmax of an empty sequence' in str(e):
                raise ValueError("'nfft' is too low: not enough PSD samples to compute the frequency parameters. Try to "
                                 "increase 'nfft' to avoid this error.")
    
        # Relative, logarithmic powers & LF/HF ratio
        rels = tuple([float(x) / total_power * 100 for x in abs_powers])
        logs = tuple([float(np.log(x)) for x in abs_powers])
        ratio = float(lf_power) / hf_power
    
        # Normalized powers
        norms = tuple([100 * x / (lf_power + hf_power) for x in [lf_power, hf_power]])
    
        # Prepare parameters for plot
        args = (freq_bands, peaks, abs_powers, rels, logs, norms, ratio, total_power)
        names = (
            '%s_bands' % method, '%s_peak' % method, '%s_abs' % method,
            '%s_rel' % method, '%s_log' % method, '%s_norm' % method,
            '%s_ratio' % method, '%s_total' % method)
    
        # Output
        params = utils.ReturnTuple(args, names)
        freq_i = utils.ReturnTuple((ulf_i, vlf_i, lf_i, hf_i), ('ulf', 'vlf', 'lf', 'hf'))
        return params, freq_i
    
    
    def _check_freq_bands(self,freq_bands):
        if freq_bands is None:
            # Set default values
            ulf = None
            vlf = (0.000, 0.04)
            lf = (0.04, 0.15)
            hf = (0.15, 0.4)
            args = (ulf, vlf, lf, hf)
            names = ('ulf', 'vlf', 'lf', 'hf')
        else:
            # Check available data
            args_ = []
            names_ = []
    
            # ULF band
            ulf = freq_bands['ulf'] if 'ulf' in freq_bands.keys() else (0, 0)
            args_.append(ulf)
            names_.append('ulf')
    
            # VLF band
            vlf = freq_bands['vlf'] if 'vlf' in freq_bands.keys() else (0.003, 0.04)
            args_.append(vlf)
            names_.append('vlf')
    
            # LF band
            lf = freq_bands['lf'] if 'lf' in freq_bands.keys() else (0.04, 0.15)
            args_.append(lf)
            names_.append('lf')
    
            # HF band
            hf = freq_bands['hf'] if 'hf' in freq_bands.keys() else (0.15, 0.4)
            args_.append(hf)
            names_.append('hf')
    
            # Check if freq_band limits are valid
            # Rule: top frequency of a lower frequency band must not be higher than the lower frequency of a higher
            # frequency band
            invalid = False
            args_ = [list(x) for x in args_ if x is not None]
            for i, val in enumerate(args_[:-1]):
                if val != (0, 0):
                    if args_[i][1] > args_[i+1][0]:
                        subs = args_[i][1]
                        args_[i][1] = args_[i+1][0]
                        args_[i+1][0] = subs
                        invalid = True
                else:
                    args_[i] = None
    
            if invalid:
                raise ValueError("Invalid or overlapping frequency band limits.")
    
            args = args_
            names = names_
    
        return utils.ReturnTuple(args, names)
    
    
    def _get_frequency_indices(self,freq, freq_bands):
        indices = []
        for key in freq_bands.keys():
            if freq_bands[key] is None:
                indices.append(None)
            else:
                indices.append(np.where((freq_bands[key][0] <= freq) & (freq <= freq_bands[key][1])))
    
        if indices[0] is None or len(indices) == 3:
            return None, indices[1][0], indices[2][0], indices[3][0]
        else:
            return indices[0][0], indices[1][0], indices[2][0], indices[3][0]
    
    
    def _get_frequency_arrays(self,freq, ulf_i, vlf_i, lf_i, hf_i):
        ulf_f = np.asarray(freq[ulf_i]) if ulf_i is not None else None
        vlf_f = np.asarray(freq[vlf_i])
        lf_f = np.asarray(freq[lf_i])
        hf_f = np.asarray(freq[hf_i])
        return ulf_f, vlf_f, lf_f, hf_f
    
    
    def _plot_psd(self,method, freq, power, freq_indices, parameters, show, show_param, legend):
        # Variables
        power = power / 10 ** 6
        fbands = parameters['%s_bands' % method]
        colors = {'ulf': 'b', 'vlf': 'yellowgreen', 'lf': 'salmon', 'hf': 'lightskyblue'}
        df = freq[1] - freq[0]
    
        if show_param:
            # Add second subplot with all computed parameters
            fig_psd = plt.figure(figsize=(12, 5))
    
            ax = fig_psd.add_subplot(121)
            ax2 = fig_psd.add_subplot(122)
    
            # Prepare parameter listing
            data = []
            index = 0
    
            for band in ['ulf', 'vlf', 'lf', 'hf']:
                if fbands[band] is not None:
                    # Add frequency band specific data
                    data.append(mpl.patches.Patch(facecolor=colors[band], label='%s: %.3fHz - %.3fHz' %
                        (band.upper(), fbands[band][0], fbands[band][1])))
                    data.append(
                        mpl.patches.Patch(facecolor='white', label='Peak: %0.3f [$Hz$]' %
                            parameters['%s_peak' % method][index]))
                    data.append(
                        mpl.patches.Patch(facecolor='white', label='Abs:  %0.3f [$ms^2$]' %
                            parameters['%s_abs' % method][index]))
                    data.append(
                        mpl.patches.Patch(facecolor='white', label='Rel:  %0.3f [%%]' %
                            parameters['%s_rel' % method][index]))
                    data.append(
                        mpl.patches.Patch(facecolor='white', label='Log:  %0.3f [$-$]' %
                            parameters['%s_log' % method][index]))
    
                    if band == 'lf':
                        data.append(mpl.patches.Patch(facecolor='white', label='Norm: %0.3f [$-$]' %
                            parameters['%s_norm' % method][0]))
                        data.append(mpl.patches.Patch(facecolor='white', label=''))
                    elif band == 'hf':
                        data.append(mpl.patches.Patch(facecolor='white', label='Norm: %0.3f [$-$]' %
                            parameters['%s_norm' % method][1]))
                        data.append(mpl.patches.Patch(facecolor='white', label=''))
    
                    # Spacings, total power and LF/HF ratio to format
                    if band == 'ulf':
                        data.append(mpl.patches.Patch(facecolor='white', label=''))
                        data.append(mpl.patches.Patch(facecolor='white', label=''))
    
                    if band == 'hf':
                        spacing = 2 if fbands['ulf'] is not None else 8
                        for i in range(spacing):
                            data.append(mpl.patches.Patch(facecolor='white', label=''))
    
                    if band == 'vlf':
                        data.append(mpl.patches.Patch(facecolor='white', label=''))
                        data.append(mpl.patches.Patch(facecolor='white', label=''))
    
                    if (fbands['ulf'] is not None and  band == 'vlf') or (fbands['ulf'] is None and  band == 'lf'):
                        data.append(mpl.patches.Patch(fc='white', label='Total Power: %.3f [$ms^2$]' % parameters[
                            '%s_total' % method]))
                        data.append(mpl.patches.Patch(fc='white', label='LF/HF: %.3f [-]' %
                            parameters['%s_ratio' % method]))
                    index += 1
            ax2.legend(handles=data, ncol=2, frameon=False)
            ax2.axis('off')
        else:
            fig_psd = plt.figure()
            ax = fig_psd.add_subplot(111)
    
        # Highlight the individual frequency bands
        for band in fbands.keys():
            if fbands[band] is not None:
                ax.fill_between(freq[freq_indices[band]], power[freq_indices[band]],
                    facecolor=colors[band], label='%s: %.3fHz - %.3fHz' % (band.upper(), fbands[band][0], fbands[band][1]))
    
                # Add lines
                if band != 'hf':
                    ax.vlines(fbands[band][1], 0, max(power) * (1 + 0.05),
                        linestyle='--', alpha=0.5, linewidth=0.5)
    
        # Plot PSD function as line (not for Lomb as it tends to decrease the clarity of the plot)
        if method in ['fft', 'ar']:
            ax.plot(freq, power, color='grey', linewidth=0.5)
    
        # Add legend
        if legend and not show_param:
            ax.legend()
    
        ax.grid(alpha=0.3)
        ax.set_xlabel('Frequency [$Hz$]')
        ax.set_ylabel('PSD [$s^2/Hz$]')
        ax.axis([0, fbands['hf'][1], 0, max(power) * (1 + 0.05)])
    
        if show:
            plt.show()
    
        return fig_psd
    
    
    def frequency_domain(self,nni=None,
                         rpeaks=None,
                         signal=None,
                         sampling_rate=1000.,
                         fbands=None,
                         show=False,
                         show_param=True,
                         legend=True,
                         kwargs_welch=None,
                         kwargs_lomb=None,
                         kwargs_ar=None):
        # Check input
        if signal is not None:
            rpeaks = biosppy.ecg.ecg(signal=signal, sampling_rate=sampling_rate, show=False)[2]
        elif nni is None and rpeaks is None:
            raise TypeError('No input data provided. Please specify input data.')
    
        # Get NNI series
        nn = tools.check_input(nni, rpeaks)
    
        # Check for kwargs for the 'welch_psd' function and compute the PSD
        if kwargs_welch is not None:
            if type(kwargs_welch) is not dict:
                raise TypeError("Expected <type 'dict'>, got %s: 'kwargs_welch' must be a dictionary containing "
                                "parameters (keys) and values for the 'welch_psd' function." % type(kwargs_welch))
    
            # Supported kwargs
            available_kwargs = ['fbands', 'detrend', 'show', 'show_param', 'legend', 'window', 'nfft']
    
            # Unwrwap kwargs dictionary for Welch specific parameters
            detrend = kwargs_welch['detrend'] if 'detrend' in kwargs_welch.keys() else True
            window = kwargs_welch['window'] if 'window' in kwargs_welch.keys() else 'hamming'
            nfft = kwargs_welch['nfft'] if 'nfft' in kwargs_welch.keys() else 2**12
    
            unsupported_kwargs = []
            for args in kwargs_welch.keys():
                if args not in available_kwargs:
                    unsupported_kwargs.append(args)
    
            # Throw warning if additional unsupported kwargs have been provided
            if unsupported_kwargs:
                warnings.warn("Unknown kwargs for 'welch_psd': %s. These kwargs have no effect." %
                              unsupported_kwargs, stacklevel=2)
    
            # Compute Welch's PSD with custom parameter settings
            welch_results = self.welch_psd(nn, fbands=fbands, detrend=detrend, show=False, show_param=show_param,
                                      legend=legend, nfft=nfft, window=window)
        else:
            # Compute Welch's PSD with default values
            welch_results = self.welch_psd(nn, show=False, fbands=fbands, legend=legend, show_param=show_param)
    
        # Check for kwargs for the 'welch_psd' function and compute the PSD
        if kwargs_lomb is not None:
            if type(kwargs_lomb) is not dict:
                raise TypeError("Expected <type 'dict'>, got %s: 'kwargs_lomb' must be a dictionary containing "
                                "parameters (keys) and values for the 'kwargs_lomb' function." % type(kwargs_lomb))
    
            # Supported kwargs
            available_kwargs = ['fbands', 'ma_size', 'show', 'show_param', 'legend', 'nfft', '']
    
            # Unwrwap kwargs dictionary
            nfft = kwargs_lomb['nfft'] if 'nfft' in kwargs_lomb.keys() else 2**8
            ma_size = kwargs_lomb['ma_size'] if 'ma_size' in kwargs_lomb.keys() else None
    
            unsupported_kwargs = []
            for args in kwargs_lomb.keys():
                if args not in available_kwargs:
                    unsupported_kwargs.append(args)
    
            # Throw warning if additional unsupported kwargs have been provided
            if unsupported_kwargs:
                warnings.warn("Unknown kwargs for 'lomb_psd': %s. These kwargs have no effect."
                              % unsupported_kwargs, stacklevel=2)
    
            # Compute Welch's PSD with custom parameter settings
            lomb_results = self.lomb_psd(nn, fbands=fbands, ma_size=ma_size, show=False, show_param=show_param,
                                    legend=legend, nfft=nfft)
        else:
            # Compute Welch's PSD with default values
            lomb_results = self.lomb_psd(nn, show=False, fbands=fbands, legend=legend, show_param=show_param)
    
        # Check for kwargs for the 'ar_psd' function and compute the PSD
        if kwargs_ar is not None:
            if type(kwargs_ar) is not dict:
                raise TypeError("Expected <type 'dict'>, got %s: 'kwargs_ar' must be a dictionary containing "
                                "parameters (keys) and values for the 'ar_psd' function." % type(kwargs_ar))
    
            # Supported kwargs
            available_kwargs = ['fbands', 'show', 'order', 'show_param', 'legend', 'window', 'nfft']
    
            # Unwrwap kwargs dictionary for Welch specific parameters
            nfft = kwargs_ar['nfft'] if 'nfft' in kwargs_ar.keys() else 2**12
            order = kwargs_ar['order'] if 'order' in kwargs_ar.keys() else 16
    
            unsupported_kwargs = []
            for args in kwargs_ar.keys():
                if args not in available_kwargs:
                    unsupported_kwargs.append(args)
    
            # Throw warning if additional unsupported kwargs have been provided
            if unsupported_kwargs:
                warnings.warn("Unknown kwargs for 'welch_psd': %s. These kwargs have no effect." %
                              unsupported_kwargs, stacklevel=2)
    
            # Compute Autoregressive PSD with custom parameter settings
            ar_results = self.ar_psd(nn, fbands=fbands, order=order, show=False, show_param=show_param, legend=legend, nfft=nfft)
        else:
            # Compute Autoregressive PSD with default values
            ar_results = self.ar_psd(nn, show=False, fbands=fbands, legend=legend, show_param=show_param)
    
        # If plots should be shown (show all plots at once)
        if show:
            plt.show()
    
        # Output
        return tools.join_tuples(welch_results, lomb_results, ar_results)
    
    
if __name__ == "__main__":
        """
        Example Script - HRV Frequency Domain Analysis
        
        """
        # Load sample NNI series
        nni =   [859,
    867,
    883,
    805,
    852,
    953,
    1078,
    883,
    867,
    953,
    1031,
    930,
    828,
    820,
    844,
    906,
    883,
    812,
    883,
    1055,
    875,
    836,
    828,
    1022,
    875,
    844,
    969,
    1094,
    1117,
    875,
    852,
    859,
    1055,
    1039,
    875,
    922,
    1039,
    1000,
    875,
    883,
    961,
    1008,
    875,
    836,
    852,
    883,
    828,
    797,
    836,
    867,
    906,
    859,
    836,
    883,
    867,
    852,
    812,
    789,
    836,
    867,
    898,
    828,
    812,
    812,
    828,
    820,
    773,
    773,
    867,
    945,
    883,
    820,
    844,
    1062,
    1125,
    891,
    844,
    859,
    891,
    922,
    875,
    805,
    828,
    891,
    875,
    828,
    789,
    820,
    852,
    828,
    797,
    828,
    914,
    914,
    805,
    789,
    836,
    852,
    898,
    781,
    812,
    852,
    953,
    859,
    805,
    852,
    906,
    906,
    820,
    789,
    836,
    906,
    1008,
    828,
    781,
    742,
    734,
    758,
    1070,
    844,
    789,
    797,
    953,
    1008,
    828,
    836,
    883,
    922,
    930,
    828,
    828,
    867,
    883,
    828,
    773,
    781,
    805,
    852,
    789,
    797,
    953,
    1148,
    1102,
    875,
    852,
    938,
    1109,
    1133,
    930,
    828,
    867,
    977,
    914,
    930,
    977,
    1016,
    883,
    906,
    1148,
    914,
    836,
    891,
    1031,
    1008,
    875,
    914,
    812,
    883,
    1109,
    883,
    883,
    938,
    1172,
    969,
    859,
    1062,
    1016,
    867,
    984,
    1117,
    1109,
    922,
    844,
    883,
    953,
    930,
    852,
    961,
    1117,
    875,
    828,
    859,
    1055,
    945,
    930,
    977,
    992,
    867,
    922,
    977,
    859,
    828,
    844,
    922,
    953,
    844,
    898,
    1086,
    875,
    820,
    852,
    914,
    828,
    844,
    1125,
    906,
    867,
    914,
    969,
    930,
    859,
    906,
    1070,
    969,
    891,
    844,
    906,
    1086,
    898,
    836,
    867,
    945,
    836,
    836,
    1172,
    938,
    852,
    836,
    898,
    875,
    836,
    953,
    867,
    914,
    1062,
    906,
    812,
    883,
    914,
    805,
    781,
    797,
    836,
    844,
    844,
    875,
    828,
    820,
    820,
    820,
    789,
    742,
    750,
    773,
    781,
    773,
    734,
    750,
    750,
    742,
    750,
    742,
    773,
    828,
    844,
    812,
    781,
    820,
    852,
    859,
    812,
    766,
    734,
    719,
    727,
    781,
    836,
    781,
    758,
    859,
    1172,
    984,
    844,
    891,
    938,
    953,
    953,
    844,
    789,
    828,
    1000,
    1180,
    898,
    820,
    914,
    1047,
    961,
    859,
    891,
    1195,
    1086,
    914,
    836,
    844,
    922,
    930,
    828,
    844,
    852,
    914,
    984,
    836,
    812,
    930,
    945,
    867,
    789,
    797,
    812,
    812,
    797,
    930,
    836,
    820,
    1094,
    1078,
    852]
        #print(nni)
        # Compute all frequency domain parameters and all methods
        frequency_domain = frequency_domain()
        results = frequency_domain.frequency_domain(nni=nni)
        
        
        # Print results
        print("===========================")
        print("FREQUENCY DOMAIN PARAMETERS")
        print("===========================")
    
        print("Peak Frequencies:")
        print("VLF:        %f [Hz]" % results['fft_peak'][0])
        print("LF :        %f [Hz]" % results['fft_peak'][1])
        print("HLF:        %f [Hz]" % results['fft_peak'][2])
    
        print("Absolute Powers:")
        print("VLF:        %f [ms^2]" % results['fft_abs'][0])
        print("LF :        %f [ms^2]" % results['fft_abs'][1])
        print("HLF:        %f [ms^2]" % results['fft_abs'][2])
    
        print("Relative Powers:")
        print("VLF:        %f [%%]" % results['fft_rel'][0])
        print("LF :        %f [%%]" % results['fft_rel'][1])
        print("HLF:        %f [%%]" % results['fft_rel'][2])
    
        print("Logarithmic Powers:")
        print("VLF:        %f [-]" % results['fft_log'][0])
        print("LF :        %f [-]" % results['fft_log'][1])
        print("HLF:        %f [-]" % results['fft_log'][2])
        print("Total Power    :    %f [ms^2]" % results['fft_total'])
        print("LF/HF ratio    :     %f [-]" % results['fft_ratio'])
