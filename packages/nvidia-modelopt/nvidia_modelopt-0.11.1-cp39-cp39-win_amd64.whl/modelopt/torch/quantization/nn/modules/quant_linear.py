# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Quantized Linear."""

import types

import torch.nn as nn

from modelopt.torch.quantization import tensor_quant

from .quant_module import QuantLinearConvBase, QuantModuleRegistry, _LegacyQuantLinearConvBaseMixin

__all__ = ["Linear", "QuantLinear"]


@QuantModuleRegistry.register({nn.Linear: "nn.Linear"})
class _QuantLinear(QuantLinearConvBase):
    """Quantized base class for nn.Linear type classes."""

    default_quant_desc_weight = tensor_quant.QUANT_DESC_8BIT_LINEAR_WEIGHT_PER_ROW

    @staticmethod
    def quantized_linear_fn(package, func_name, self, input, weight, *args, **kwargs):
        """Quantized version of a generic linear functional."""
        output = getattr(package, func_name)(
            self.input_quantizer(input),
            self.weight_quantizer(weight),
            *args,
            **kwargs,
        )
        return self.output_quantizer(output)

    def _setup(self):
        super()._setup()
        if not hasattr(self.forward, "__func__") or (
            self.forward.__func__ is not self.__class__.forward
        ):
            if hasattr(self, "_hf_hook"):
                # The forward of this module has been monkey patched by HF accelerate
                # So it will not call _QuantLinear forward function
                # We need to remove the monkey patching, update the forward method and add the hook back

                from accelerate.hooks import add_hook_to_module

                assert hasattr(self, "_old_forward")

                hook = self._hf_hook
                delattr(self, "_hf_hook")
                delattr(self, "_old_forward")
                self.forward = types.MethodType(self.__class__.forward, self)
                add_hook_to_module(self, hook)
            else:
                raise RuntimeError(
                    "Received a module with monkey patched forward method. Quantization will not"
                    " work."
                )


class QuantLinear(_LegacyQuantLinearConvBaseMixin, nn.Linear):
    """Quantized version of nn.Linear."""

    default_quant_desc_weight = _QuantLinear.default_quant_desc_weight


Linear = QuantLinear
