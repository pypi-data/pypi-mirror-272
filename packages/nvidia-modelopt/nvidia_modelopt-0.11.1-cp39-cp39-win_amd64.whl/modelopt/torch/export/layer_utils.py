# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Utils for model_config export.

Some of the logics in this file are empirical and needs constant update if exceptions occur.
"""

from typing import List, Optional, Tuple

import torch
import torch.nn as nn

try:
    from transformers.activations import ACT2FN
except Exception:
    print("Cannot find transformers package. Hugginface modules cannot be exported.")
    pass

from ..quantization.nn import SequentialQuantizer, TensorQuantizer
from .distribute import get_rank, get_world_size
from .model_config import (
    KV_CACHE_FP8,
    KV_CACHE_INT8,
    LAYERNORM_DEFAULT,
    LAYERNORM_RMS,
    LINEAR_COLUMN,
    LINEAR_ROW,
    QUANTIZATION_FP8,
    QUANTIZATION_INT4_AWQ,
    QUANTIZATION_INT8_SQ,
    QUANTIZATION_NONE,
    QUANTIZATION_W4A8_AWQ,
    AttentionConfig,
    DecoderLayerConfig,
    EmbeddingConfig,
    ExpertConfig,
    LayernormConfig,
    LinearConfig,
    MLPConfig,
    MOEConfig,
    QKVConfig,
)
from .model_config_utils import pad_weights
from .scaling_factor_utils import resmooth_and_get_scale


def check_model_compatibility(module_list: List[nn.Module]) -> Tuple[bool, bool, bool]:
    """Returns whether the list of modules is compatible with the export logic.

    And if positional embedding and embedding layernorm exists.

    We assumes the model to be assembled with one or two embedding layers,
    a ModuleList of transformer decoders,
    and a final layernorm with optional embedding layernorm.
    Otherwise it will not be supported.
    """
    num_embeddings = 0
    num_module_list = 0
    num_layer_norm = 0
    for module in module_list:
        if is_embedding(module):
            num_embeddings += 1
        elif is_decoder_list(module):
            num_module_list += 1
        elif is_layernorm(module):
            num_layer_norm += 1

    return (
        1 <= num_embeddings
        and num_embeddings <= 2
        and num_module_list == 1
        and 1 <= num_layer_norm
        and num_layer_norm <= 2,
        num_embeddings > 1,
        num_layer_norm > 1,
    )


def get_transformer_layers(model: nn.Module) -> List[nn.Module]:
    """Returns the root module of the transformer model."""
    if "Megatron" in type(model).__name__:
        if hasattr(model, "model") and "GPTModel" in type(model.model).__name__:
            # NEMO mcore models can be handled with the following branch.
            model = model.model

        # NEMO non mcore models, we need to find the language_model module first.
        children = [model]
        language_model = None
        while children and not language_model:
            next_children = []
            for child in children:
                if type(child).__name__ == "TransformerLanguageModel":
                    language_model = child
                    break
                for m in child.children():
                    next_children.append(m)
            children = next_children
        if language_model:
            print("Warning: this is an old NEMO checkpoint format and will be deprecated soon.")
            layers = [m for m in language_model.embedding.children()] + [
                m for m in language_model.encoder.children()
            ]

            if hasattr(language_model, "output_layer"):
                layers.append(language_model.output_layer)

            return layers

    if "GPTModel" in type(model).__name__:
        # mcore models
        layers = []
        if hasattr(model, "embedding"):
            layers = layers + [m for m in model.embedding.children()]
        layers = layers + [m for m in model.decoder.children()]
        if hasattr(model, "output_layer"):
            layers.append(model.output_layer)
        return layers

    if hasattr(model, "transformer"):
        # This is a LMHead model
        # Add lm_head to be processed along with transformer layers
        modules = []
        for m in model.transformer.children():
            if "Transformer" in type(m).__name__ and is_decoder_list(m.layers):
                modules.append(m.layers)
                modules.append(m.final_layernorm)
            else:
                modules.append(m)
        if hasattr(model, "lm_head"):
            modules += [model.lm_head]
        return modules

    if hasattr(model, "model"):
        # LLAMA
        modules = [m for m in model.model.children()]
        if hasattr(model, "lm_head"):
            modules += [model.lm_head]

        return modules

    return [m for m in model.children()]


def is_linear(module: nn.Module) -> bool:
    """Returns whether the module is a linear layer."""
    return any([k in type(module).__name__ for k in ["Linear", "Conv1D", "NormHead"]])


def is_embedding(module: nn.Module) -> bool:
    """Returns whether the module is an embedding layer."""
    module_type_name = type(module).__name__
    return (
        "Embedding" in module_type_name
        and "Rotary" not in module_type_name
        and "PhiImage" not in module_type_name
    )


def build_embedding_config(
    module: nn.Module, dtype: torch.dtype, normalization_constant: float = 1
) -> EmbeddingConfig:
    """Builds the embedding config from the module."""
    assert is_embedding(module)

    world_size = get_world_size()
    rank = get_rank()

    # Special case for chatglm
    if hasattr(module, "word_embeddings"):
        module = module.word_embeddings

    weight = module.weight.detach().type(dtype)
    normalized_weight = weight * normalization_constant
    if "Parallel" in type(module).__name__:
        local_weight = normalized_weight
    else:
        padded_weight = pad_weights(normalized_weight, get_world_size())
        local_weight = torch.chunk(padded_weight, world_size, dim=0)[rank]
    return EmbeddingConfig(
        weight=local_weight,
    )


def is_layernorm(module: nn.Module) -> bool:
    """Returns whether the module is a layernorm layer."""
    module_name = type(module).__name__
    return any(norm in module_name for norm in ["LayerNorm", "RMSNorm"])


def build_layernorm_config(module: nn.Module, dtype: torch.dtype) -> LayernormConfig:
    """Builds the layernorm config from the module."""
    assert is_layernorm(module)

    layernorm_type = LAYERNORM_DEFAULT
    if "RMS" in type(module).__name__:
        layernorm_type = LAYERNORM_RMS

    weight = module.weight.detach()

    def _weights_plus_one(module):
        if any(name in type(module).__name__ for name in ["LayerNorm1P", "GemmaRMSNorm"]):
            return True

        if hasattr(module, "zero_centered_gamma") and module.zero_centered_gamma:
            return True

        return False

    if _weights_plus_one(module):
        # megatron layernorm's weight needs to be updated.
        weight = weight.float() + 1.0

    config = LayernormConfig(
        weight=weight.type(dtype),
        bias=(
            module.bias.detach().type(dtype)
            if hasattr(module, "bias") and module.bias is not None
            else None
        ),
        layernorm_type=layernorm_type,
    )

    # TODO: handle the nemo llama eps config.
    for eps_key in ["eps", "variance_epsilon"]:
        if hasattr(module, eps_key):
            config.eps = getattr(module, eps_key)
            break

    return config


def is_decoder_list(module: nn.Module) -> bool:
    """Returns whether the module is a decoder list."""
    return type(module) == nn.ModuleList


def is_attention(module: nn.Module) -> bool:
    """Returns whether the module is an attention layer."""
    return "Attention" in type(module).__name__


def is_mlp(module: nn.Module) -> bool:
    """Returns whether the module is an MLP layer."""
    return "MLP" in type(module).__name__


def is_moe(module: nn.Module) -> bool:
    """Returns whether the module is an MOE layer."""
    return type(module).__name__ in ["MixtralSparseMoeBlock", "ArcticMoE"]


def get_scaling_factor(quantizer: TensorQuantizer) -> torch.Tensor:
    """Returns scaling factor from the quantizer as torch.Tensor."""
    if not quantizer.is_enabled:
        return None

    amax = quantizer.export_amax()
    if amax is None:
        return None

    # tensorrt_llm uses float as the scaling_factors.
    scaling_factor = amax.float() / quantizer.maxbound

    assert torch.all(scaling_factor > 0), f"scaling factor {scaling_factor} not positive."

    return scaling_factor


def get_activation_scaling_factor(module: nn.Module) -> torch.Tensor:
    """Returns the activation scaling factor."""
    return (
        get_scaling_factor(module.input_quantizer) if hasattr(module, "input_quantizer") else None
    )


def get_weight_scaling_factor(module: nn.Module) -> torch.Tensor:
    """Returns the weight scaling factor."""
    # module.weight_quantizer could be a TensorQuantizer (for algorithms except W4A8) or
    # a SequentialQuantizer (for W4A8). In the latter case, we need to get the scaling factor from the
    # first quantizer of the SequentialQuantizer instance.
    if hasattr(module, "weight_quantizer") and isinstance(
        module.weight_quantizer, SequentialQuantizer
    ):
        return get_scaling_factor(module.weight_quantizer[0])
    return (
        get_scaling_factor(module.weight_quantizer) if hasattr(module, "weight_quantizer") else None
    )


def get_weight_block_size(module: nn.Module) -> int:
    """Returns the weight block size."""
    if not hasattr(module, "weight_quantizer"):
        return 0

    weight_quantizer = module.weight_quantizer

    if isinstance(weight_quantizer, SequentialQuantizer):
        weight_quantizer = weight_quantizer[0]

    if not weight_quantizer.is_enabled:
        return 0

    block_sizes = weight_quantizer.block_sizes

    if block_sizes:
        return block_sizes[-1]
    return 0


def get_weight_scaling_factor_2(module: nn.Module) -> torch.Tensor:
    """Returns the secondary weight scaling factor."""
    if (
        not hasattr(module, "weight_quantizer")
        or not isinstance(module.weight_quantizer, SequentialQuantizer)
        or not module.weight_quantizer[-1].is_enabled
    ):
        return None
    assert (
        len(module.weight_quantizer) == 2
    ), "modelopt only supports 2 sequential quantization layers for now"
    return get_scaling_factor(module.weight_quantizer[-1])


def get_prequant_scaling_factor(module: nn.Module, dtype: torch.dtype) -> torch.Tensor:
    """Returns the prequant scaling factor."""
    prequant_scaling_factor = (
        module.input_quantizer._pre_quant_scale.squeeze().type(dtype)
        if hasattr(module, "input_quantizer")
        and hasattr(module.input_quantizer, "_pre_quant_scale")
        else None
    )

    if prequant_scaling_factor is not None:
        assert torch.all(
            prequant_scaling_factor > 0
        ), f"prequant scaling factor {prequant_scaling_factor} not positive."
    return prequant_scaling_factor


def get_kv_cache_scaling_factor(qkv_modules: List[nn.Module]) -> torch.Tensor:
    """Returns the kv_cache scaling factor if output quantizer is set. Else returns None by default."""
    # For FP8, we recommend default kv cache scaling factor to be 1.
    if get_kv_cache_dtype(qkv_modules) == KV_CACHE_FP8:
        return torch.tensor([1.0], dtype=torch.float)

    scaling_factors = [
        get_scaling_factor(module.output_quantizer)
        for module in qkv_modules
        if hasattr(module, "output_quantizer")
    ]

    scaling_factors = [
        scaling_factor for scaling_factor in scaling_factors if scaling_factor is not None
    ]

    if not scaling_factors:
        return None

    return torch.stack(scaling_factors).max(dim=0).values


def get_kv_cache_dtype(qkv_modules: List[nn.Module]) -> str:
    """Returns the kv_cache dtype.

    If num_bits of output_quantizer is (4, 3) then returns FP8; if it is 8, returns int8,
    otherwise returns None.
    """
    num_bits_list = [
        qkv_module.output_quantizer.num_bits
        for qkv_module in qkv_modules
        if hasattr(qkv_module, "output_quantizer") and qkv_module.output_quantizer.is_enabled
    ]

    if (4, 3) in num_bits_list:
        return KV_CACHE_FP8
    elif 8 in num_bits_list:
        return KV_CACHE_INT8
    else:
        return QUANTIZATION_NONE


def build_qkv(
    qkv_modules: List[nn.Module],
    model_metadata_config,
    dtype: torch.dtype,
    ext_config: DecoderLayerConfig = None,
) -> QKVConfig:
    """Converts the qkv modules to the config."""
    config = QKVConfig()
    q_bias = None
    k_bias = None
    v_bias = None

    block_size = get_weight_block_size(qkv_modules[0])

    num_heads = ext_config.num_attention_heads
    training_tp = model_metadata_config["training_tensor_parallel"]
    if len(qkv_modules) == 1:
        # QKV layers combined as a single module, e.g. GPT2, GPTNext
        qkv_module = qkv_modules[0]
        assert ext_config is not None, "ext_config is None"
        num_kv_heads = ext_config.num_kv_heads

        if "ColumnParallelLinear" in type(qkv_module).__name__:
            # For NEMO model, num_kv_heads/num_attention_heads is the first dimension of QKV
            model_metadata_config["head_is_first_dim"] = True

        qkv_weight = qkv_module.weight.detach()
        if type(qkv_module).__name__ == "Conv1D":
            if not hasattr(qkv_module, "input_quantizer") and not hasattr(
                qkv_module, "output_quantizer"
            ):
                # For unquantized nn.Conv1D, the weights are transposed compared with the nn.Linear
                qkv_weight = qkv_weight.T

        # Handle the case that num_kv_heads/num_attention_heads is the first dimension of QKV.
        # This logic covers MQA and GQA as well.
        keep_channel_order = not model_metadata_config.get("head_is_first_dim", False)

        hidden_size = qkv_module.weight.shape[1]
        q_weight, k_weight, v_weight = _split_fused_qkv_weight_and_scaling(
            qkv_weight,
            hidden_size,
            num_heads,
            num_kv_heads,
            training_tp,
            False,
            keep_channel_order,
        )
        qkv_activation_scaling_factor = get_activation_scaling_factor(qkv_module)
        q_activation_scaling_factor = qkv_activation_scaling_factor
        k_activation_scaling_factor = qkv_activation_scaling_factor
        v_activation_scaling_factor = qkv_activation_scaling_factor

        qkv_weight_scaling_factor = get_weight_scaling_factor(qkv_module)

        if qkv_weight_scaling_factor is not None and qkv_weight_scaling_factor.numel() != 1:
            # INT8 sq case
            q_weight_scaling_factor, k_weight_scaling_factor, v_weight_scaling_factor = (
                _split_fused_qkv_weight_and_scaling(
                    qkv_weight_scaling_factor,
                    hidden_size,
                    num_heads,
                    num_kv_heads,
                    training_tp,
                    True,
                    keep_channel_order,
                )
            )
        else:
            q_weight_scaling_factor = qkv_weight_scaling_factor
            k_weight_scaling_factor = qkv_weight_scaling_factor
            v_weight_scaling_factor = qkv_weight_scaling_factor

        # bias
        if qkv_module.bias is not None:
            q_bias, k_bias, v_bias = _split_fused_qkv_weight_and_scaling(
                qkv_module.bias.detach(),
                hidden_size,
                num_heads,
                num_kv_heads,
                training_tp,
                True,
                keep_channel_order,
            )

        q_weight_scaling_factor_2 = k_weight_scaling_factor_2 = v_weight_scaling_factor_2 = (
            get_weight_scaling_factor_2(qkv_module)
        )

        q_prequant_scaling_factor = k_prequant_scaling_factor = v_prequant_scaling_factor = (
            get_prequant_scaling_factor(qkv_module, dtype)
        )

    elif len(qkv_modules) == 3:
        # Separate QKV layers
        q_weight = qkv_modules[0].weight.detach()
        q_activation_scaling_factor = get_activation_scaling_factor(qkv_modules[0])
        q_weight_scaling_factor = get_weight_scaling_factor(qkv_modules[0])
        k_weight = qkv_modules[1].weight.detach()
        k_activation_scaling_factor = get_activation_scaling_factor(qkv_modules[1])
        k_weight_scaling_factor = get_weight_scaling_factor(qkv_modules[1])
        v_weight = qkv_modules[2].weight.detach()
        v_activation_scaling_factor = get_activation_scaling_factor(qkv_modules[2])
        v_weight_scaling_factor = get_weight_scaling_factor(qkv_modules[2])

        q_weight_scaling_factor_2 = get_weight_scaling_factor_2(qkv_modules[0])
        k_weight_scaling_factor_2 = get_weight_scaling_factor_2(qkv_modules[1])
        v_weight_scaling_factor_2 = get_weight_scaling_factor_2(qkv_modules[2])

        q_prequant_scaling_factor = get_prequant_scaling_factor(qkv_modules[0], dtype)
        k_prequant_scaling_factor = get_prequant_scaling_factor(qkv_modules[1], dtype)
        v_prequant_scaling_factor = get_prequant_scaling_factor(qkv_modules[2], dtype)

        if hasattr(qkv_modules[0], "bias"):
            q_bias = qkv_modules[0].bias

        if hasattr(qkv_modules[1], "bias"):
            k_bias = qkv_modules[1].bias

        if hasattr(qkv_modules[2], "bias"):
            v_bias = qkv_modules[2].bias

    else:
        raise NotImplementedError(f"QKV modules format {qkv_modules} not supported")

    # Adopt the implementation from examples/llama/weight.py in the tekit repo for INT4 AWQ
    # Resmooth q, k, v for int4_awq, as they share the same pre_quant_scale during compulation
    # This logic is implemented at the export stage to reduce resource requirement for model building/deployment
    if all(
        pre_quant_scale is not None
        for pre_quant_scale in [
            q_prequant_scaling_factor,
            k_prequant_scaling_factor,
            v_prequant_scaling_factor,
        ]
    ):
        pre_quant_scale = (
            q_prequant_scaling_factor + k_prequant_scaling_factor + v_prequant_scaling_factor
        ) / 3.0
        # Resmooth q, k, v with average pre_quant_scale for AWQ
        q_weight, q_weight_scaling_factor, _ = resmooth_and_get_scale(
            merged_weights=q_weight,
            pre_quant_scales=[q_prequant_scaling_factor],
            ranks=1,
            group_size=block_size,
            avg_pre_quant_scale=pre_quant_scale,
        )
        k_weight, k_weight_scaling_factor, _ = resmooth_and_get_scale(
            merged_weights=k_weight,
            pre_quant_scales=[k_prequant_scaling_factor],
            ranks=1,
            group_size=block_size,
            avg_pre_quant_scale=pre_quant_scale,
        )
        v_weight, v_weight_scaling_factor, _ = resmooth_and_get_scale(
            merged_weights=v_weight,
            pre_quant_scales=[v_prequant_scaling_factor],
            ranks=1,
            group_size=block_size,
            avg_pre_quant_scale=pre_quant_scale,
        )
        q_prequant_scaling_factor = k_prequant_scaling_factor = v_prequant_scaling_factor = (
            pre_quant_scale
        )

    config.q = LinearConfig(linear_type=LINEAR_COLUMN)
    config.q.weight = q_weight.type(dtype).cpu()
    config.q.bias = q_bias.type(dtype) if q_bias is not None else None
    config.q.activation_scaling_factor = q_activation_scaling_factor
    config.q.weights_scaling_factor = q_weight_scaling_factor
    config.q.weights_scaling_factor_2 = q_weight_scaling_factor_2
    config.q.prequant_scaling_factor = q_prequant_scaling_factor
    config.q.awq_block_size = block_size

    config.k = LinearConfig(linear_type=LINEAR_COLUMN)
    config.k.weight = k_weight.type(dtype).cpu()
    config.k.bias = k_bias.type(dtype) if k_bias is not None else None
    config.k.activation_scaling_factor = k_activation_scaling_factor
    config.k.weights_scaling_factor = k_weight_scaling_factor
    config.k.weights_scaling_factor_2 = k_weight_scaling_factor_2
    config.k.prequant_scaling_factor = k_prequant_scaling_factor
    config.k.awq_block_size = block_size

    config.v = LinearConfig(linear_type=LINEAR_COLUMN)
    config.v.weight = v_weight.type(dtype).cpu()
    config.v.bias = v_bias.type(dtype) if v_bias is not None else None
    config.v.activation_scaling_factor = v_activation_scaling_factor
    config.v.weights_scaling_factor = v_weight_scaling_factor
    config.v.weights_scaling_factor_2 = v_weight_scaling_factor_2
    config.v.prequant_scaling_factor = v_prequant_scaling_factor
    config.v.awq_block_size = block_size

    if not ext_config.attention_head_size:
        ext_config.attention_head_size = config.q.weight.shape[0] * training_tp // num_heads

    return config


def build_linear_config(module: nn.Module, linear_type: str, dtype: torch.dtype) -> LinearConfig:
    """Builds the linear config for the module."""
    assert is_linear(module)

    torch_weight = module.weight.detach()

    if "NormHead" in type(module).__name__:
        torch_weight = torch.nn.functional.normalize(torch_weight)
    elif "Conv1D" in type(module).__name__ and not (
        hasattr(module, "input_quantizer") or hasattr(module, "output_quantizer")
    ):
        # Transpose Conv1D weights to linear unless it has been transposed by the quantization.
        torch_weight = torch_weight.T

    weight = torch_weight.type(dtype)

    config = LinearConfig(linear_type=linear_type)
    config.weight = weight.cpu()

    if hasattr(module, "bias") and module.bias is not None:
        config.bias = module.bias.detach().type(dtype)

    config.activation_scaling_factor = get_activation_scaling_factor(module)
    config.weights_scaling_factor = get_weight_scaling_factor(module)
    config.weights_scaling_factor_2 = get_weight_scaling_factor_2(module)
    config.prequant_scaling_factor = get_prequant_scaling_factor(module, dtype)
    config.awq_block_size = get_weight_block_size(module)
    return config


def build_attention_config(
    module: nn.Module,
    model_metadata_config,
    dtype: torch.dtype,
    ext_config: DecoderLayerConfig = None,
) -> AttentionConfig:
    """Builds the attention config from the module."""
    assert is_attention(module)

    config = AttentionConfig()
    if hasattr(module, "rotary_dim"):
        config.rotary_dim = module.rotary_dim
    if hasattr(module, "clip_qkv"):
        config.clip_qkv = module.clip_qkv

    qkv_modules = []
    q = None
    k = None
    v = None
    for name, layer in module.named_children():
        if is_linear(layer):
            if _is_qkv(name):
                qkv_modules.append(layer)
            elif "q" in name:
                q = layer
            elif "k" in name:
                k = layer
            elif "v" in name:
                v = layer
            else:
                # The dense layer
                config.dense = build_linear_config(layer, LINEAR_ROW, dtype)

    if not qkv_modules:
        assert q
        assert k
        assert v
        qkv_modules = [q, k, v]

    config.qkv = build_qkv(qkv_modules, model_metadata_config, dtype, ext_config)

    config.kv_cache_scaling_factor = get_kv_cache_scaling_factor(qkv_modules)
    if config.kv_cache_scaling_factor is not None:
        config.kv_cache_dtype = get_kv_cache_dtype(qkv_modules)

    return config


def _is_qkv(name) -> bool:
    return all([k in name for k in ["q", "k", "v"]]) or "W_pack" in name or "c_attn" in name


def _get_hidden_act(act_func) -> str:
    """Returns the name of the hidden activation functon based on ACT2FN."""
    if isinstance(act_func, str):
        return act_func

    # Falcon activation, "nn.GELU" is equivalent to "gelu" in ACT2FN
    if isinstance(act_func, nn.GELU):
        return "gelu"

    if hasattr(act_func, "func") and act_func.func == nn.functional.gelu:
        return "gelu"

    for name, func in ACT2FN.items():
        if isinstance(func, tuple):
            if isinstance(act_func, func[0]):
                return name
        elif isinstance(act_func, func):
            return name

    return act_func.__name__


def build_mlp_config(module: nn.Module, decoder_type, dtype: torch.dtype) -> MLPConfig:
    """Builds the MLP config for the module."""
    assert is_mlp(module)

    config = MLPConfig()

    # fc1 and gate will be merged to the same layer for chatglm
    if decoder_type == "chatglm":
        config.merged_fc1_gate = True

    def _split_gate_from_fc(decoder_type, module, fc_name, fc_layer):
        if (
            "ColumnParallelLinear" in type(fc_layer).__name__
            and hasattr(module.config, "gated_linear_unit")
            and module.config.gated_linear_unit
        ):
            return True

        if decoder_type == "chatglm":
            return True

        if decoder_type != "gptnext":
            return False

        if "dense_h_to_4h" in fc_name and "dense_h_to_4h_2" not in fc_name:
            return True

        return False

    # TODO: We may want to refactor these keywords/model mapping
    fc_keywords = set(
        [
            "c_fc",  # gpt2
            "fc_in",  # gptj
            "gate_proj",  # llama, baichuan
            "dense_h_to_4h",  # falcon, chatglm, bloom
            "linear_fc1",
            "w2",  # qwen
            "fc1",  # phi, gemma
            "gate_up_proj",  # phi
        ]
    )
    proj_keywords = set(
        [
            "c_proj",  # gpt2, qwen
            "fc_out",  # gptj
            "dense_4h_to_h",  # falcon, chatglm, bloom
            "4h_to_h",
            "down_proj",  # llama, baichuan, mpt, phi
            "linear_fc2",
            "proj",
            "fc2",  # phi, gemma
        ]
    )
    gate_keywords = set(
        [
            "up_proj",  # llama, baichuan
            "dense_h_to_4h_2",
            "w1",  # qwen
        ]
    )

    for name, layer in module.named_children():
        if is_linear(layer):
            # Arctic (llama-based MoE, decoder_type is "llama") has MLP keyword conflicts with Qwen
            # Arctic's residual MLP use w1 for fc, w2 for proj, w3 for gate
            if type(module).__name__ == "ArcticMLP":
                fc_keywords.discard("w2")
                gate_keywords.discard("w1")
                fc_keywords.add("w1")
                proj_keywords.add("w2")
                gate_keywords.add("w3")

            if decoder_type == "mpt":
                fc_keywords.add("up_proj")
                gate_keywords.discard("up_proj")

            if type(module).__name__ == "TLGv4MLP":  # for TLGv4ForCausalLM
                fc_keywords.add("up_proj")
                gate_keywords.discard("up_proj")

            split_gate = _split_gate_from_fc(decoder_type, module, name, layer)

            if any([keyword == name for keyword in fc_keywords]):
                if split_gate:
                    # We have to split the gate from the fc
                    weights = torch.chunk(layer.weight.detach().type(dtype), 2, dim=0)
                    if decoder_type == "chatglm":
                        # Chatglm's weight has gate first then fc in the HF model
                        weights = (weights[1], weights[0])

                    activation_scaling_factor = get_activation_scaling_factor(layer)
                    weight_scaling_factor = get_weight_scaling_factor(layer)
                    weight_scaling_factor_2 = get_weight_scaling_factor_2(layer)
                    prequant_scaling_factor = get_prequant_scaling_factor(layer, dtype)

                    weight_scaling_factors = [None, None]

                    if weight_scaling_factor is not None:
                        if weight_scaling_factor.numel() != 1:
                            # for Int8 SQ case, we split the weight scaling factor into two parts.
                            weight_scaling_factors = torch.chunk(weight_scaling_factor, 2, dim=0)
                            if decoder_type == "chatglm":
                                weight_scaling_factors = (
                                    weight_scaling_factors[1],
                                    weight_scaling_factors[0],
                                )
                        else:
                            # for FP8 case that weight_scaling_factor is a scalar, we repeat it for the gate.
                            weight_scaling_factors = (
                                [weight_scaling_factor] * 2
                                if weight_scaling_factor is not None
                                else [None, None]
                            )

                    config.fc = LinearConfig()
                    config.fc.linear_type = LINEAR_COLUMN
                    config.fc.weight = weights[0]
                    config.fc.weights_scaling_factor = weight_scaling_factors[0]
                    config.fc.weights_scaling_factor_2 = weight_scaling_factor_2
                    config.fc.activation_scaling_factor = activation_scaling_factor
                    config.fc.prequant_scaling_factor = prequant_scaling_factor
                    config.fc.awq_block_size = get_weight_block_size(layer)

                    config.gate = LinearConfig()
                    config.gate.linear_type = LINEAR_COLUMN
                    config.gate.weight = weights[1]
                    config.gate.weights_scaling_factor = weight_scaling_factors[1]
                    config.gate.weights_scaling_factor_2 = weight_scaling_factor_2
                    config.gate.activation_scaling_factor = activation_scaling_factor
                    config.gate.prequant_scaling_factor = prequant_scaling_factor
                    config.gate.awq_block_size = get_weight_block_size(layer)
                else:
                    config.fc = build_linear_config(layer, LINEAR_COLUMN, dtype)

            elif any([keyword == name for keyword in proj_keywords]):
                config.proj = build_linear_config(layer, LINEAR_ROW, dtype)
            elif any([keyword == name for keyword in gate_keywords]):
                config.gate = build_linear_config(layer, LINEAR_COLUMN, dtype)

    assert config.proj is not None and config.fc is not None, "proj or fc can not be found"

    hidden_act = None

    if hasattr(module, "activation"):
        hidden_act = module.activation
    elif hasattr(module, "activation_func"):
        # MCore activation_func can be swiglu (gated silu) or squared_relu.
        hidden_act = module.activation_func.__name__.replace("_", "-")
        if hidden_act in ["glu", "silu"]:
            hidden_act = "swiglu" if decoder_type == "gptnext" else "silu"
    else:
        for act in ["act", "act_fn", "activation_fn"]:
            if hasattr(module, act):
                hidden_act = _get_hidden_act(getattr(module, act)).split("_")[0]
                break

    if decoder_type == "bloom":
        hidden_act = "gelu"

    if decoder_type == "qwen":
        hidden_act = "silu"

    if type(module).__name__ == "TLGv4MLP":
        hidden_act = module.config.hidden_act  # The support from TRT LLM is still on-going.

    if hidden_act is None:
        raise NotImplementedError(f"{module} not supported.")

    config.hidden_act = hidden_act
    return config


def _build_stacked_linear(experts: nn.Module, module_name, linear_type, dtype):
    config = LinearConfig(linear_type=linear_type)

    first_module = getattr(experts[0], module_name)
    # weights
    config.weight = torch.stack(
        [getattr(e, module_name).weight.detach().type(dtype).to("cpu") for e in experts]
    )

    # bias
    if hasattr(first_module, "bias") and first_module.bias is not None:
        raise ValueError("Unexpected bias tensors inside MOE modules.")

    # scaling factors
    def get_stacked_scaling_factors(experts, get_function, module_name, karg={}):
        if get_function(getattr(experts[0], module_name), **karg) is not None:
            return torch.stack(
                [get_function(getattr(e, module_name), **karg).to("cpu") for e in experts]
            )
        return None

    config.activation_scaling_factor = get_stacked_scaling_factors(
        experts, get_activation_scaling_factor, module_name
    )
    # The moe plugin only supports a single activation scaling factor for all experts
    if config.activation_scaling_factor is not None:
        config.activation_scaling_factor = config.activation_scaling_factor.max().unsqueeze(0)
    config.weights_scaling_factor = get_stacked_scaling_factors(
        experts, get_weight_scaling_factor, module_name
    )
    config.weights_scaling_factor_2 = get_stacked_scaling_factors(
        experts, get_weight_scaling_factor_2, module_name
    )
    config.prequant_scaling_factor = get_stacked_scaling_factors(
        experts, get_prequant_scaling_factor, module_name, {"dtype": dtype}
    )
    config.awq_block_size = get_weight_block_size(getattr(experts[0], module_name))

    return config


def build_stacked_experts(experts: nn.Module, dtype: torch.dtype):
    """Builds the experts_weight_1 and experts_weight_2 configs for the experts."""
    experts_weight_1 = _build_stacked_linear(experts, "w1", LINEAR_COLUMN, dtype)
    experts_weight_2 = _build_stacked_linear(experts, "w2", LINEAR_ROW, dtype)
    experts_weight_3 = _build_stacked_linear(experts, "w3", LINEAR_COLUMN, dtype)

    # Concat w1 and w3 into w1
    experts_weight_1.weight = torch.concat(
        [experts_weight_3.weight, experts_weight_1.weight], dim=-2
    )

    def _resmooth_stack_weights(experts_weight_1, experts_weight_3):
        """Resmooth stacked weights for experts for int4_awq."""
        resmooth_weights = []
        resmooth_weights_scaling_factors = []
        resmooth_prequant_scaling_factors = []
        group_size = experts_weight_1.awq_block_size
        # resmooth each expert as w1 and w3 will share the average prequant_scaling_factor
        for idx in range(experts_weight_1.weight.shape[0]):
            merged_weight = experts_weight_1.weight[idx]  # weights should be concated already
            pre_quant_scales = [
                experts_weight_3.prequant_scaling_factor[idx],
                experts_weight_1.prequant_scaling_factor[idx],
            ]
            (
                resmooth_weight,
                resmooth_scaling_factor,
                resmooth_prequant_scaling_factor,
            ) = resmooth_and_get_scale(
                merged_weight,
                pre_quant_scales,
                len(pre_quant_scales),
                group_size,
            )
            resmooth_weights.append(resmooth_weight)
            resmooth_weights_scaling_factors.append(resmooth_scaling_factor)
            resmooth_prequant_scaling_factors.append(resmooth_prequant_scaling_factor)
        return (
            torch.stack(resmooth_weights),
            torch.stack(resmooth_weights_scaling_factors),
            torch.stack(resmooth_prequant_scaling_factors),
        )

    def _max_stack_scaling_factor(weights_scaling_factor_1, weights_scaling_factor_3):
        return torch.stack([weights_scaling_factor_3, weights_scaling_factor_1]).max(dim=0).values

    # scaling factors
    # TODO: check if this works with int8_sq
    if experts_weight_1.weights_scaling_factor is not None:
        # fp8 case, per-tensor quantization
        if experts_weight_1.weights_scaling_factor.dim() == 2:
            experts_weight_1.weights_scaling_factor = _max_stack_scaling_factor(
                experts_weight_3.weights_scaling_factor, experts_weight_1.weights_scaling_factor
            )
        # int4 awq case, group_wise quantization, and per tensor quantization for prequant_scaling_factor
        elif (
            experts_weight_1.weights_scaling_factor.dim() == 3
            and experts_weight_1.awq_block_size > 0
            and experts_weight_1.prequant_scaling_factor.dim() == 2
        ):
            (
                experts_weight_1.weight,
                experts_weight_1.weights_scaling_factor,
                experts_weight_1.prequant_scaling_factor,
            ) = _resmooth_stack_weights(experts_weight_1, experts_weight_3)
        else:
            raise NotImplementedError(
                "Unexpected shape of weights_scaling_factor. The quantization algorithm is not"
                " supported."
            )
    if experts_weight_1.weights_scaling_factor_2 is not None:
        if experts_weight_1.weights_scaling_factor_2.dim() == 2:
            experts_weight_1.weights_scaling_factor_2 = _max_stack_scaling_factor(
                experts_weight_3.weights_scaling_factor_2, experts_weight_1.weights_scaling_factor_2
            )
        else:
            raise NotImplementedError(
                "Unexpected shape of weights_scaling_factor_2. The quantization algorithm is not"
                " supported."
            )
    return experts_weight_1, experts_weight_2


def build_moe_config(module: nn.Module, decoder_type, dtype: torch.dtype) -> MOEConfig:
    """Builds the MOE config for the module."""
    assert is_moe(module)
    # We only support mixtral that use the llama decoder for now
    assert decoder_type in ["llama"]

    config = MOEConfig()

    # Router: TRT-LLM uses fp32 for router to keep precision
    config.router = build_linear_config(module.gate, LINEAR_ROW, torch.float32)

    # Experts
    experts = ExpertConfig()
    experts.fc, experts.proj = build_stacked_experts(module.experts, dtype)
    config.experts = experts

    # activation for mixtral
    config.hidden_act = "swiglu"

    return config


def build_decoder_config(
    module: nn.Module,
    model_metadata_config,
    decoder_type: str,
    dtype: torch.dtype,
) -> DecoderLayerConfig:
    """Builds the full decoder config from the module."""
    quantization = _get_quantization(module)
    config = DecoderLayerConfig(decoder_type=decoder_type, quantization=quantization)
    for k in ["n_head", "num_attention_heads", "n_heads"]:
        if k in model_metadata_config:
            config.num_attention_heads = model_metadata_config[k]

    for k in [
        "num_key_value_heads",
        "num_kv_heads",
        "num_kv",
        "n_head_kv",
        "multi_query_group_num",
        "num_query_groups",
    ]:
        if k in model_metadata_config:
            config.num_kv_heads = model_metadata_config[k]

    # Supporting different attention layer config in MCoreGPTModel. If per layer config
    # exists, override the global config.
    if hasattr(module, "self_attention"):
        if hasattr(module.self_attention, "config"):
            if hasattr(module.self_attention.config, "num_attention_heads"):
                config.num_attention_heads = module.self_attention.config.num_attention_heads
            if hasattr(module.self_attention.config, "kv_channels"):
                config.attention_head_size = module.self_attention.config.kv_channels
            if hasattr(module.self_attention.config, "num_query_groups"):
                config.num_kv_heads = module.self_attention.config.num_query_groups

    for k in ["n_positions", "max_position_embeddings"]:
        if k in model_metadata_config:
            config.max_position_embeddings = model_metadata_config[k]
    # 2048 is the default TRT LLM max_position_embeddings
    if config.max_position_embeddings == 0:
        config.max_position_embeddings = 2048

    for k in ["rotary_percentage", "rotary_percent", "rotary_pct"]:
        if k in model_metadata_config:
            config.rotary_pct = model_metadata_config[k]

    for k in ["alibi"]:
        if k in model_metadata_config:
            config.use_alibi = model_metadata_config[k]

    for k in ["alibi_bias_max"]:
        if k in model_metadata_config:
            config.alibi_bias_max = model_metadata_config[k]

    for k in ["new_decoder_architecture"]:
        if k in model_metadata_config:
            config.new_decoder_architecture = model_metadata_config[k]

    for k in ["apply_residual_connection_post_layernorm"]:
        if k in model_metadata_config:
            config.apply_residual_connection_post_layernorm = model_metadata_config[k]

    for k in ["use_cache"]:
        if k in model_metadata_config:
            config.use_cache = model_metadata_config[k]

    for k in ["_name_or_path"]:
        if k in model_metadata_config:
            model_path_name = model_metadata_config[k]
            model_version = ""
            model_scale = ""
            for n in ["chatglm3", "chatglm2", "chatglm"]:
                if n in model_path_name:
                    model_version = n
                    break
            for n in ["6b-32k", "6b-base", "6b"]:
                if n in model_path_name:
                    model_scale = n.replace("-", "_")
                    break
            config.model_name = model_version + "_" + model_scale
            if "chatglm" in config.model_name:
                assert config.model_name in (
                    [
                        "chatglm3_6b",
                        "chatglm3_6b_32k",
                        "chatglm3_6b_base",
                        "chatglm2_6b",
                        "chatglm2_6b_32k",
                    ]
                ), f"{config.model_name} is not supported now."

    # For chatglm
    for k in ["rope_ratio"]:
        if k in model_metadata_config:
            config.rope_ratio = model_metadata_config[k]

    # For Falcon variants do not provide new_decoder_architecture, but we can infer it from the model_type
    if "model_type" in model_metadata_config:
        if model_metadata_config["model_type"] == "RefinedWeb":
            # Case 1. Falcon-40B / Falcon-40B-instruct
            # https://huggingface.co/tiiuae/falcon-40b/blob/main/config.json
            config.new_decoder_architecture = True
        elif model_metadata_config["model_type"] == "RefinedWebModel":
            # Case 2. Falcon-7B / Falcon-7B-instruct
            # https://huggingface.co/tiiuae/falcon-7b/blob/main/config.json
            config.new_decoder_architecture = False
    for k in ["parallel_attn"]:
        if k in model_metadata_config:
            config.parallel_attention = model_metadata_config[k]

    # For Falcon variants, they might not specify the number of kv heads with MQA models, e.g., 7b
    if (
        not config.new_decoder_architecture
        and "multi_query" in model_metadata_config
        and model_metadata_config["multi_query"]
    ):
        config.num_kv_heads = 1

    # For Qwen
    for k in ["seq_length"]:
        if k in model_metadata_config:
            config.seq_length = model_metadata_config[k]

    # For Qwen rotary_emb_base
    # CodeLlama using different rotary_base in comparison to LLaMA v1/v2 models
    for k in ["rotary_emb_base", "rope_theta", "rotary_base"]:
        if k in model_metadata_config:
            config.rotary_base = model_metadata_config[k]

    # For Phi
    config.partial_rotary_factor = model_metadata_config.get("partial_rotary_factor", 0)

    # Mixture of Experts
    for k in ["num_local_experts"]:
        if k in model_metadata_config:
            config.moe_num_experts = model_metadata_config[k]
    for k in ["num_experts_per_tok"]:
        if k in model_metadata_config:
            config.moe_top_k = model_metadata_config[k]

    # Mixture of Experts
    for k in ["num_local_experts"]:
        if k in model_metadata_config:
            config.moe_num_experts = model_metadata_config[k]
    for k in ["num_experts_per_tok"]:
        if k in model_metadata_config:
            config.moe_top_k = model_metadata_config[k]

    for name, layer in module.named_children():
        # We assume input_layernorm should be before the post_layernorm in decoder block layout,
        # and residual_layernorm could be after post_layernorm
        if is_layernorm(layer):
            layernorm_config = build_layernorm_config(layer, dtype)
            if name in ["ln_mlp"]:
                config.mlp_layernorm = layernorm_config
            elif config.input_layernorm is None:
                config.input_layernorm = layernorm_config
            elif config.post_layernorm is None:
                config.post_layernorm = layernorm_config
            else:
                assert model_metadata_config[
                    "parallel_attn_mlp_res"
                ], "Unexpected layernorm in a layer"
                config.residual_layernorm = layernorm_config

        elif is_attention(layer):
            if decoder_type in ["bloom", "falcon"]:
                model_metadata_config["head_is_first_dim"] = True
            config.attention = build_attention_config(layer, model_metadata_config, dtype, config)

        elif is_moe(layer):
            config.mlp = build_moe_config(layer, decoder_type, dtype)

        # We assume MoE layer should be before the residual MLP layer in decoder block layout,
        # so MLP layer after a MoE layer is treated as a residual MLP layer
        elif is_mlp(layer):
            if config.mlp is None:
                config.mlp = build_mlp_config(layer, decoder_type, dtype)
            else:
                assert model_metadata_config["parallel_attn_mlp_res"], "Unexpected mlp in a layer"
                config.residual_mlp = build_mlp_config(layer, decoder_type, dtype)

    return config


def _split_fused_qkv_weight_and_scaling(
    weight: torch.Tensor,
    hidden_size: int,
    num_heads: int,
    num_kv_heads: Optional[int] = None,
    training_tp: int = 1,
    is_scaling_factor: bool = False,
    keep_channel_order: bool = False,
):
    """Reorder the qkv weight for spliting QKV weights.

    The shape of the fused QKV weights in HF is different from the shape that
    TRT-LLM requires. In particular, the weight of HF consists of interleaved
    q, k, v head weights, while that of TRT-LLM is contigous.
        HF     : [q1, k1, v1, ..., qh, kh, vh]
        TRT-LLM: [q1, ..., qh, k1, ..., kh, v1, vh]
    where qi, vi, ki are weight vectors corresponding to attention head i.
    It's similar to multi/grouped query attention cases.
    if keep_channel_order
        HF     : [q1, ..., qh, k1, ..., kh, v1, ..., vh]
        TRT-LLM: [q1, ..., qh, k1, ..., kh, v1, ..., vh]
    """
    # Query types and expected kv heads.
    #  - Conventional MHA: num_heads = num_kv_heads
    #  - Multi-Query Attention: num_kv_heads = 1
    #  - Grouped-Query Attention: num_heads % num_kv_heads = 0
    num_kv_heads = num_kv_heads if num_kv_heads else num_heads
    assert (
        num_heads % num_kv_heads == 0
    ), f"num_heads({num_heads}) must be divisible by num_kv_heads({num_kv_heads}))."

    # The number of attention heads per group: N q head + 1 k head + 1 v head.
    num_group_heads = num_heads // num_kv_heads + 2
    num_kv_heads_single_tp = max(num_kv_heads // training_tp, 1)
    size_per_head = weight.shape[0] // num_kv_heads_single_tp // num_group_heads

    if size_per_head != hidden_size // num_heads:
        print("Warning: qkv have different hidden size than the input.")

    if is_scaling_factor:
        # For AWQ, weight scaling facotrs will be a 2D array (out_feat, in_feat/group_size)
        # Int8_sq can be regarded as a specific instance where the group_size is equal to in_feat.
        output_ch = num_kv_heads_single_tp * num_group_heads * size_per_head
        weight_size = weight.numel()

        qkv_in = weight_size // output_ch
    else:
        qkv_in = hidden_size

    if keep_channel_order:
        kv_size = num_kv_heads * size_per_head
        q_w = weight[: -2 * kv_size, ...]
        k_w = weight[-2 * kv_size : -1 * kv_size, ...]
        v_w = weight[-1 * kv_size :, ...]

        if is_scaling_factor:
            q_w = q_w.reshape(-1)
            k_w = k_w.reshape(-1)
            v_w = v_w.reshape(-1)
    else:
        # Split Q/K/V weights
        weight = weight.reshape(num_kv_heads_single_tp, num_group_heads, size_per_head, qkv_in)
        q_w = weight[:, :-2, ...]  # (nKV, num_heads // nKV, size_per_head, qkv_in)
        k_w = weight[:, -2:-1, ...]  # (nKV, 1, size_per_head, qkv_in)
        v_w = weight[:, -1:, ...]  # (nKV, 1, size_per_head, qkv_in)

        q_w = q_w.reshape(-1, qkv_in)
        k_w = k_w.reshape(-1, qkv_in)
        v_w = v_w.reshape(-1, qkv_in)

        if not is_scaling_factor:
            q_w = q_w.reshape(-1, qkv_in)
            k_w = k_w.reshape(-1, qkv_in)
            v_w = v_w.reshape(-1, qkv_in)
        else:
            q_w = q_w.reshape(-1)
            k_w = k_w.reshape(-1)
            v_w = v_w.reshape(-1)

    return q_w, k_w, v_w


def _get_quantization(decoder_layer) -> str:
    """Gets the quantization string."""
    for _, decoder_sub_module in decoder_layer.named_children():
        if is_attention(decoder_sub_module):
            for _, layer in decoder_sub_module.named_children():
                if is_linear(layer):
                    if not hasattr(layer, "weight_quantizer"):
                        return QUANTIZATION_NONE
                    w_quantizer = layer.weight_quantizer
                    if isinstance(w_quantizer, SequentialQuantizer):
                        assert (
                            len(w_quantizer) == 2
                            and w_quantizer[0].num_bits == 4
                            and w_quantizer[1].num_bits == (4, 3)
                        ), "Unsupported quantizer"
                        assert (
                            w_quantizer[0].block_sizes
                            and len(w_quantizer[0].block_sizes) > 0
                            and w_quantizer[0].block_sizes[-1] > 0
                        ), "Invalid block_sizes"
                        return QUANTIZATION_W4A8_AWQ
                    if w_quantizer.num_bits == 4:
                        assert (
                            len(w_quantizer.block_sizes) > 0 and w_quantizer.block_sizes[-1] > 0
                        ), "Invalid block_sizes"
                        return QUANTIZATION_INT4_AWQ
                    elif w_quantizer.num_bits == 8:
                        return QUANTIZATION_INT8_SQ
                    elif w_quantizer.num_bits == (4, 3):
                        return QUANTIZATION_FP8
                    else:
                        raise NotImplementedError(
                            f"Unsupported quantizer with num_bits: {w_quantizer.num_bits}"
                        )

    return QUANTIZATION_NONE
