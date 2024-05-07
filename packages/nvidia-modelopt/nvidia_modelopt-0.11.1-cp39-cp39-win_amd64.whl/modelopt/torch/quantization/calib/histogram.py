# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Histogram based calibrators."""
import warnings
from collections import Counter

import numpy as np
import torch
import torch.distributed as dist
from scipy.stats import entropy

from .. import nn as qnn
from .. import utils as quant_utils
from ..tensor_quant import fake_tensor_quant, scaled_e4m3
from .calibrator import _Calibrator

__all__ = ["HistogramCalibrator", "calibrate_weights"]


class HistogramCalibrator(_Calibrator):
    """Unified histogram calibrator.

    Histogram will be only collected once. compute_amax() performs entropy, percentile, or mse
        calibration based on arguments

    Args:
        num_bits: An integer. Number of bits of quantization.
        axis: A tuple. see QuantDescriptor.
        unsigned: A boolean. using unsigned quantization.
        num_bins: An integer. Number of histograms bins. Default 2048.
        grow_method: A string. DEPRECATED. default None.
        skip_zeros: A boolean. If True, skips zeros when collecting data for histogram. Default False.
        torch_hist: A boolean. If True, collect histogram by torch.histc instead of np.histogram. If input tensor
            is on GPU, histc will also be running on GPU. Default True.
    """

    def __init__(
        self,
        num_bits=8,
        axis=None,
        unsigned=False,
        num_bins=2048,
        grow_method=None,
        skip_zeros=False,
        torch_hist=True,
    ):
        """Initialize."""
        super(HistogramCalibrator, self).__init__(num_bits, axis, unsigned)
        self._num_bins = num_bins
        self._skip_zeros = skip_zeros

        self._calib_bin_edges = None
        self._calib_hist = None

        self._torch_hist = torch_hist

        if axis is not None:
            raise NotImplementedError(
                "Calibrator histogram collection only supports per tensor scaling"
            )

    def collect(self, x):
        """Collect histogram."""
        if torch.min(x) < 0.0:
            x = x.abs()

        x = x.float()

        if not self._torch_hist:
            x_np = x.cpu().detach().numpy()

            if self._skip_zeros:
                x_np = x_np[np.where(x_np != 0)]

            if self._calib_bin_edges is None and self._calib_hist is None:
                # first time it uses num_bins to compute histogram.
                self._calib_hist, self._calib_bin_edges = np.histogram(x_np, bins=self._num_bins)
            else:
                temp_amax = np.max(x_np)
                if temp_amax > self._calib_bin_edges[-1]:  # type: ignore
                    # increase the number of bins
                    width = self._calib_bin_edges[1] - self._calib_bin_edges[0]  # type: ignore
                    # NOTE: np.arange may create an extra bin after the one containing temp_amax
                    new_bin_edges = np.arange(
                        self._calib_bin_edges[-1] + width, temp_amax + width, width  # type: ignore
                    )
                    self._calib_bin_edges = np.hstack((self._calib_bin_edges, new_bin_edges))
                hist, self._calib_bin_edges = np.histogram(x_np, bins=self._calib_bin_edges)
                hist[: len(self._calib_hist)] += self._calib_hist  # type: ignore
                self._calib_hist = hist
        else:
            # This branch of code is designed to match numpy version as close as possible
            with torch.no_grad():
                if self._skip_zeros:
                    x = x[torch.where(x != 0)]

                # Because we collect histogram on absolute value, setting min=0 simplifying the rare case where
                # minimum value is not exactly 0 and first batch collected has larger min value than later batches
                x_max = x.max()
                if self._calib_bin_edges is None and self._calib_hist is None:
                    self._calib_hist = torch.histc(x, bins=self._num_bins, min=0, max=x_max)
                    self._calib_bin_edges = torch.linspace(0, x_max, self._num_bins + 1)
                else:
                    if x_max > self._calib_bin_edges[-1]:  # type: ignore
                        width = self._calib_bin_edges[1] - self._calib_bin_edges[0]  # type: ignore
                        self._num_bins = int((x_max / width).ceil().item())
                        self._calib_bin_edges = torch.arange(
                            0, x_max + width, width, device=x.device
                        )

                    hist = torch.histc(x, bins=self._num_bins, min=0, max=self._calib_bin_edges[-1])  # type: ignore
                    hist[: self._calib_hist.numel()] += self._calib_hist  # type: ignore
                    self._calib_hist = hist

    def reset(self):
        """Reset the collected histogram."""
        self._calib_bin_edges = None
        self._calib_hist = None

    def compute_amax(
        self,
        method: str,
        *,
        stride: int = 1,
        start_bin: int = 128,
        percentile: float = 99.99,
    ):
        """Compute the amax from the collected histogram.

        Args:
            method: A string. One of ['entropy', 'mse', 'percentile']

        Keyword Arguments:
            stride: An integer. Default 1
            start_bin: An integer. Default 128
            percentils: A float number between [0, 100]. Default 99.99.

        Returns:
            amax: a tensor
        """
        if dist.is_available() and dist.is_initialized():
            warnings.warn(
                "This method does not perform any synchronization across DistributedDataParallel"
                " (DDP) https://pytorch.org/docs/stable/notes/ddp.html modules. The recommended"
                " method is to use the same calibration dataset across all distributed data"
                " parallel groups so that `amax` is the same for all DDP modules."
            )

        if isinstance(self._calib_hist, torch.Tensor):
            calib_hist = self._calib_hist.int().cpu().numpy()
            calib_bin_edges = self._calib_bin_edges.cpu().numpy()  # type: ignore
        else:
            calib_hist = self._calib_hist
            calib_bin_edges = self._calib_bin_edges

        if method == "entropy":
            calib_amax = _compute_amax_entropy(
                calib_hist, calib_bin_edges, self._num_bits, self._unsigned, stride, start_bin
            )
        elif method == "mse":
            calib_amax = _compute_amax_mse(
                calib_hist, calib_bin_edges, self._num_bits, self._unsigned, stride, start_bin
            )
        elif method == "percentile":
            calib_amax = _compute_amax_percentile(calib_hist, calib_bin_edges, percentile)
        else:
            raise TypeError("Unknown calibration method {}".format(method))

        return calib_amax

    def __str__(self):
        s = "HistogramCalibrator("
        if self._calib_bin_edges is None:
            bin_edge_str = "None"
        else:
            bin_edge_str = "[{:.3f}, ..., {:.3f}]({})".format(
                self._calib_bin_edges[0], self._calib_bin_edges[-1], len(self._calib_bin_edges)
            )
        s += "calib_bin_edges={})".format(bin_edge_str)
        return s

    def __repr__(self):
        s = "HistogramCalibrator("
        s += super(HistogramCalibrator, self).__repr__()
        s += " calib_bin_edges={_calib_bin_edges}"
        s += " calib_hist={_calib_hist})"
        return s.format(**self.__dict__)


# Ideally, we want to decouple collector (collect histogram) and calibrator (compute amax) as opposed to
# the current calibrator design. The following compute amax functions are broken out from the calibrator
# as first step towards there.
def _compute_amax_entropy(calib_hist, calib_bin_edges, num_bits, unsigned, stride=1, start_bin=128):
    """Returns amax that minimizes KL-Divergence of the collected histogram."""
    # If calibrator hasn't collected any data, return none
    if calib_bin_edges is None and calib_hist is None:
        return None

    def _normalize_distr(distr):
        summ = np.sum(distr)
        if summ != 0:
            distr = distr / summ

    bins = calib_hist[:]
    bins[0] = bins[1]

    total_data = np.sum(bins)

    divergences = []
    arguments = []

    # we are quantizing to 128 values + sign if num_bits=8
    nbins = 1 << (num_bits - 1 + int(unsigned))

    starting = start_bin
    stop = len(bins)

    new_density_counts = np.zeros(nbins, dtype=np.float64)

    for i in range(starting, stop + 1, stride):
        new_density_counts.fill(0)
        space = np.linspace(0, i, num=nbins + 1)
        digitized_space = np.digitize(range(i), space) - 1

        digitized_space[bins[:i] == 0] = -1

        for idx, digitized in enumerate(digitized_space):
            if digitized != -1:
                new_density_counts[digitized] += bins[idx]

        counter = Counter(digitized_space)
        for key, val in counter.items():
            if key != -1:
                new_density_counts[key] = new_density_counts[key] / val

        new_density = np.zeros(i, dtype=np.float64)
        for idx, digitized in enumerate(digitized_space):
            if digitized != -1:
                new_density[idx] = new_density_counts[digitized]

        total_counts_new = np.sum(new_density) + np.sum(bins[i:])
        _normalize_distr(new_density)

        reference_density = np.array(bins[: len(digitized_space)])
        reference_density[-1] += np.sum(bins[i:])

        total_counts_old = np.sum(reference_density)
        if round(total_counts_new) != total_data or round(total_counts_old) != total_data:
            raise RuntimeError(
                "Count mismatch! total_counts_new={}, total_counts_old={}, total_data={}".format(
                    total_counts_new, total_counts_old, total_data
                )
            )

        _normalize_distr(reference_density)

        ent = entropy(reference_density, new_density)
        divergences.append(ent)
        arguments.append(i)

    divergences = np.array(divergences)
    last_argmin = len(divergences) - 1 - np.argmin(divergences[::-1])
    calib_amax = calib_bin_edges[last_argmin * stride + starting]
    calib_amax = torch.tensor(calib_amax.item())

    return calib_amax


def _compute_amax_mse(calib_hist, calib_bin_edges, num_bits, unsigned, stride=1, start_bin=128):
    """Returns amax that minimizes MSE of the collected histogram."""
    # If calibrator hasn't collected any data, return none
    if calib_bin_edges is None and calib_hist is None:
        return None

    counts = torch.from_numpy(calib_hist[:]).float()
    edges = torch.from_numpy(calib_bin_edges[:]).float()

    device = None
    if torch.cuda.is_available():
        device = counts.device
        counts = counts.cuda()
        edges = edges.cuda()

    centers = (edges[1:] + edges[:-1]) / 2

    mses = []
    arguments = []

    for i in range(start_bin, len(centers), stride):
        amax = centers[i]
        if isinstance(num_bits, int) and num_bits >= 0:
            quant_centers = fake_tensor_quant(centers, amax, num_bits, unsigned)
        elif num_bits == (4, 3):
            quant_centers = scaled_e4m3(centers, amax, num_bits[0], num_bits[1])
        else:
            raise TypeError("Invalid num_bits. num_bits must be a positive integer or tuple (4,3).")

        mse = ((quant_centers - centers) ** 2 * counts).mean()

        mses.append(mse.cpu())
        arguments.append(i)

    argmin = np.argmin(mses)
    calib_amax = centers[arguments[argmin]]

    if device is not None:
        calib_amax = calib_amax.to(device)

    return calib_amax


def _compute_amax_percentile(calib_hist, calib_bin_edges, percentile):
    """Returns amax that clips the percentile fraction of collected data."""
    if percentile < 0 or percentile > 100:
        raise ValueError("Invalid percentile. Must be in range 0 <= percentile <= 100.")

    # If calibrator hasn't collected any data, return none
    if calib_bin_edges is None and calib_hist is None:
        return None

    total = calib_hist.sum()
    cdf = np.cumsum(calib_hist / total)
    idx = np.searchsorted(cdf, percentile / 100)
    calib_amax = calib_bin_edges[idx]
    calib_amax = torch.tensor(calib_amax.item())

    return calib_amax


def calibrate_weights(model, method="percentile", perchannel=True, percentile=99.99, num_bins=2048):
    """Calibrate weights of all child quantized modules.

    Ideally, we would split calibration functionality to histogram collector and calibrator which
    takes histogram and compute amax. But since we haven't decoupled collector and calibrator, it
    is easier to create a separate function to calibrate weight.

    .. note::
        This function uses `method` specified by the argument to decide which method to use, NOT the one
        specified by the calibrator embedded in weight_quantizer.
        We haven't moved calibration to GPU, so everything is transfered to CPU

    Args:
        model: A torch.nn.Module.
        method: A string of calibration method. Supports "mse" and "percentile". Default "percentile"
        perchannel: A bool. Set channel/neuron axis if True. Default True.
        percentile: A float. Default 99.99
        num_bins: A integer. Number of bins of histogram. Default 2048.

    """
    for name, module in model.named_modules():
        if hasattr(module, "weight") and hasattr(module, "weight_quantizer"):
            num_bits = module.weight_quantizer.num_bits
            unsigned = module.weight_quantizer.unsigned
            channel_second_modules = (
                qnn.QuantConvTranspose1d,
                qnn.QuantConvTranspose2d,
                qnn.QuantConvTranspose3d,
            )
            if perchannel:
                axis = 1 if isinstance(module, channel_second_modules) else 0
            else:
                axis = None
            axis_size = module.weight.shape[axis] if axis is not None else 1

            # Histogram is always collected even if method is "max". Although "max" is supported here
            # but it is not the primary usage of this function
            if axis is None:
                input_weights = module.weight.abs().cpu().detach().numpy()
                calib_hist, calib_bin_edges = np.histogram(
                    input_weights, bins=2048, range=(0, input_weights.max())
                )
                calib_hist = [calib_hist]
                calib_bin_edges = [calib_bin_edges]
            else:
                calib_hist = []
                calib_bin_edges = []
                for i in range(axis_size):
                    input_weights = (
                        module.weight.index_select(
                            axis, torch.tensor(i, device=module.weight.device)
                        )
                        .abs()
                        .cpu()
                        .detach()
                        .numpy()
                    )
                    hist, bin_edges = np.histogram(
                        input_weights, bins=num_bins, range=(0, input_weights.max())
                    )
                    calib_hist.append(hist)
                    calib_bin_edges.append(bin_edges)

            calib_amax = []
            if method == "max":
                reduce_axis = list(range(module.weight.dim()))
                reduce_axis.remove(axis)  # type: ignore
                calib_amax.append(quant_utils.reduce_amax(module.weight, axis=reduce_axis))
            elif method == "mse":
                for i in range(axis_size):
                    calib_amax.append(
                        _compute_amax_mse(calib_hist[i], calib_bin_edges[i], num_bits, unsigned)
                    )
            elif method == "percentile":
                for i in range(axis_size):
                    calib_amax.append(
                        _compute_amax_percentile(calib_hist[i], calib_bin_edges[i], percentile)
                    )
            else:
                raise TypeError("Unsupported calibration method {}".format(method))

            if axis is None:
                calib_amax_t = calib_amax[0]
            else:
                calib_amax_shape = [1] * module.weight.dim()
                calib_amax_shape[axis] = module.weight.shape[axis]
                calib_amax_t = torch.stack(calib_amax).reshape(calib_amax_shape)
            if calib_amax_t.numel() == 1:
                calib_amax_t.squeeze_()
            module.weight_quantizer.amax = calib_amax_t.detach().cpu().numpy()
