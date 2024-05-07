# Adapted from https://github.com/microsoft/onnxruntime/blob/baeece44ba075009c6bfe95891a8c1b3d4571cb3/onnxruntime/python/tools/quantization/quant_utils.py
# and https://github.com/microsoft/onnxruntime/blob/baeece44ba075009c6bfe95891a8c1b3d4571cb3/onnxruntime/python/tools/quantization/calibrate.py
# and https://github.com/microsoft/onnxruntime/blob/2ac381c55397dffff327cc6efecf6f95a70f90a1/onnxruntime/python/tools/quantization/onnx_quantizer.py
#
# MIT License
#
# Copyright (c) Microsoft Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Not a contribution
# Changes made by NVIDIA CORPORATION & AFFILIATES or otherwise documented as
# NVIDIA-proprietary are not a contribution and subject to the following terms and conditions:
# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


"""This module contains all the patched functions from ORT."""

from pathlib import Path

import numpy as np
import onnx
import onnxruntime as ort
from onnx import ModelProto, onnx_pb
from onnxruntime.quantization import quant_utils
from onnxruntime.quantization.calibrate import CalibraterBase, HistogramCollector
from onnxruntime.quantization.onnx_quantizer import ONNXQuantizer
from onnxruntime_extensions import get_library_path as _get_library_path
from tqdm import tqdm


def _compute_scale_zp(rmin, rmax, qmin, qmax, symmetric=False):
    """Calculates the scale and zero point.

    Calculate the scale s and zero point z for the quantization relation
    r = s(q-z), where r are the original values and q are the corresponding
    quantized values.

    r and z are calculated such that every value within [rmin,rmax] has an
    approximate representation within [qmin,qmax]. In addition, qmin <= z <=
    qmax is enforced. If the symmetric flag is set to True, the interval
    [rmin,rmax] is symmetrized to [-absmax, +absmax], where
    absmax = max(abs(rmin), abs(rmax)).

    Args:
        rmin: minimum value of r
        rmax: maximum value of r
        qmin: minimum value representable by the target quantization data type
        qmax: maximum value representable by the target quantization data type

    Returns:
        A tuple zero and scale (z, s)
    """
    if qmin > 0 or qmax < 0:
        raise ValueError(
            f"qmin and qmax must meet requirement: qmin <= 0 <= qmax while qmin:{qmin},"
            f" qmmax:{qmax}"
        )

    # Adjust rmin and rmax such that 0 is included in the range. This is
    # required to make sure zero can be represented by the quantization data
    # type (i.e. to make sure qmin <= zero_point <= qmax)
    rmin = min(rmin, 0)
    rmax = max(rmax, 0)

    if symmetric:
        absmax = max(abs(rmin), abs(rmax))
        rmin = -absmax
        rmax = +absmax

    scale = (rmax - rmin) / float(qmax - qmin)
    if scale < 1e-9 or np.isinf(scale):
        scale = 1.0
        zero_point = 0
    else:
        zero_point = round(qmin - rmin / scale)

    return zero_point, scale


def _collect_value(histogram_collector, name_to_arr):
    """Collect histogram on real value."""
    for tensor, data_arr in tqdm(name_to_arr.items()):
        data_arr = np.asarray(data_arr)  # noqa: PLW2901
        data_arr = data_arr.flatten()  # noqa: PLW2901

        if data_arr.size > 0:
            min_value = np.min(data_arr)
            max_value = np.max(data_arr)
        else:
            min_value = 0
            max_value = 0

        # Change the inf and nan values to meaningful min/max
        min_value = (
            np.finfo(np.float32).tiny if np.isinf(min_value) or np.isnan(min_value) else min_value
        )
        max_value = (
            np.finfo(np.float32).max if np.isinf(max_value) or np.isnan(max_value) else max_value
        )

        threshold = max(abs(min_value), abs(max_value))

        if tensor in histogram_collector.histogram_dict:
            old_histogram = histogram_collector.histogram_dict[tensor]
            histogram_collector.histogram_dict[tensor] = histogram_collector.merge_histogram(
                old_histogram, data_arr, min_value, max_value, threshold
            )
        else:
            hist, hist_edges = np.histogram(
                data_arr, histogram_collector.num_bins, range=(-threshold, threshold)
            )
            histogram_collector.histogram_dict[tensor] = (
                hist,
                hist_edges,
                min_value,
                max_value,
                threshold,
            )


def _check_opset_version(onnx_quantizer):
    ai_onnx_domain = [
        opset
        for opset in onnx_quantizer.model.model.opset_import
        if not opset.domain or opset.domain in ["ai.onnx", "ai.onnx.contrib"]
    ]
    if len(ai_onnx_domain) != 1:
        raise ValueError("Failed to find proper ai.onnx domain")
    opset_version = ai_onnx_domain[0].version

    if opset_version == 10:
        return 10

    if opset_version < 10:
        onnx_quantizer.model.model.opset_import.remove(ai_onnx_domain[0])
        onnx_quantizer.model.model.opset_import.extend([onnx.helper.make_opsetid("", 11)])
        opset_version = 11

    if opset_version < 19 and onnx_quantizer.weight_qType == onnx_pb.TensorProto.FLOAT8E4M3FN:
        onnx_quantizer.model.model.opset_import.remove(ai_onnx_domain[0])
        onnx_quantizer.model.model.opset_import.extend([onnx.helper.make_opsetid("", 19)])
        onnx_quantizer.model.model.ir_version = 9
        opset_version = 19

    onnx_quantizer.fuse_dynamic_quant = True
    return opset_version


def _create_inference_session(calibrator):
    """Create an OnnxRuntime InferenceSession."""
    sess_options = ort.SessionOptions()
    sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_DISABLE_ALL
    sess_options.register_custom_ops_library(_get_library_path())
    calibrator.infer_session = ort.InferenceSession(
        calibrator.augmented_model_path,
        sess_options=sess_options,
        providers=calibrator.execution_providers,
    )


def _load_model_with_shape_infer(model_path: Path) -> ModelProto:
    # TODO: skip shape inference only for models with plugins
    return onnx.load(model_path.as_posix())


def patch_ort_modules():
    """Patches the ORT modules."""
    HistogramCollector.collect_value = _collect_value
    quant_utils.compute_scale_zp = _compute_scale_zp
    quant_utils.load_model_with_shape_infer = _load_model_with_shape_infer
    CalibraterBase.create_inference_session = _create_inference_session
    ONNXQuantizer.check_opset_version = _check_opset_version
