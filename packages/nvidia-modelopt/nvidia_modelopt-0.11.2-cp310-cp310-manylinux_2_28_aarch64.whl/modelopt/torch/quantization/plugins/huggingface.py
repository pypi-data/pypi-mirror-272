# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Support quantization for huggingface layers."""
import torch
import torch.nn as nn
import transformers

from modelopt.torch.opt.dynamic import DynamicModule

from ..nn import QuantModuleRegistry
from ..nn.modules.quant_linear import _QuantLinear

__all__ = []


# transformers.modeling_utils.Conv1D used in HF-GPT2 is not a real Conv1D
# It is actually a Linear layer where weight is transposed and torch.addmm is used
@QuantModuleRegistry.register({transformers.modeling_utils.Conv1D: "Conv1D"})
class _QuantConv1D(_QuantLinear):
    @classmethod
    @torch.no_grad()
    def convert(cls, module: nn.Module) -> "_QuantConv1D":
        module.weight = nn.Parameter(module.weight.T)
        module.out_features, module.in_features = module.weight.shape
        # We want the forward method of nn.Linear to be called instead of the forward method of Conv1D
        dyn_cls: DynamicModule = QuantModuleRegistry.get(nn.Linear)
        return dyn_cls.convert(module)


if hasattr(transformers.models, "falcon") and hasattr(
    transformers.models.falcon.modeling_falcon, "FalconLinear"
):
    QuantModuleRegistry.register(
        {transformers.models.falcon.modeling_falcon.FalconLinear: "FalconLinear"}
    )(_QuantLinear)


def register_falcon_linears_on_the_fly(model):
    """Register Falcon linear modules as a QUANT_MODULE.

    Certain falcon models (for example, falcon 40b) use remote code, which are loaded dynamically, to build their model.
    Therefore, we need to register the linear on the fly before quantization.
    """
    if type(model).__name__ in ["RWForCausalLM", "FalconForCausalLM"]:
        linear_type = type(model.transformer.h[0].self_attention.dense)
        # Create a QuantFalconLinear class on the fly
        if QuantModuleRegistry.get(linear_type) is None:
            QuantModuleRegistry.register({linear_type: linear_type.__name__})(_QuantLinear)
