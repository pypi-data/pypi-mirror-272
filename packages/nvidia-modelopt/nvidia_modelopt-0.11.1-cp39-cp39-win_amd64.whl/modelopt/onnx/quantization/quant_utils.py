# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Provides some basic utilities that can be used in quantize() methods."""

from typing import Sequence, Union

import numpy as np

INT4_MIN = -8
INT4_MAX = 7
UINT4_MIN = 0
UINT4_MAX = 15


def pack_float32_to_4bit_optimized(array: Union[np.ndarray, Sequence], signed: bool) -> np.ndarray:
    """Convert an array of float32 value to a 4bit data-type and pack every two concecutive elements in a byte.

    This is the optimized version of pack_float32_to_4bit() utility in ONNX helper file. The basic optimizations
    done here mainly rely on moving some common code out of the per-element function calls or loops, thereby making
    them per-input-array, instead of per-input-element. The remaining logic should largely remain as is.

    Args:
        array: array of float to convert and pack
        signed: Whether the 4 bit variant is signed or unsigned

    Returns:
        Packed array with size `ceil(farray.size/2)` (single dimension).
    """
    if not isinstance(array, np.ndarray):
        array = np.asarray(array, dtype=np.float32)

    array_flat = array.ravel()
    is_odd_volume = np.prod(array.shape) % 2 == 1
    if is_odd_volume:
        array_flat = np.append(array_flat, np.array([0]))

    inp_arr_len = array_flat.size
    dtype = np.int8 if signed else np.uint8
    clip_low = INT4_MIN if signed else UINT4_MIN
    clip_high = INT4_MAX if signed else UINT4_MAX
    array_flat = np.clip(array_flat, clip_low, clip_high)
    array_flat = np.rint(array_flat).astype(dtype)
    assert len(array_flat) % 2 == 0, "array length must be even at this point"
    assert len(array_flat) == inp_arr_len, "output-length must match the input-length"
    output_list = []
    for i in range(0, inp_arr_len, 2):
        output_list.append((array_flat[i + 1] << 4) | (array_flat[i] & 0x0F))
    arr = np.array(output_list)
    return arr.astype(np.uint8)
