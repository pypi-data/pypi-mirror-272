# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Convert ONNX model without QDQ nodes + calib data into ONNX model with QDQ nodes.

Typically quantizing linear operations like Conv, MatMul etc. gives most of the performance boost.
But there are many other ops that are quantizable (aka low precision kernels available) and provides
optimal performance with lower accuracy drop. The default op types that this ONNX ptq tool quantizes
in different quantization modes are: INT8: ['Add', 'AveragePool', 'BatchNormalization', 'Clip',
'Conv', 'ConvTranspose', 'Gemm', 'GlobalAveragePool', 'MatMul', 'MaxPool', 'Mul'], INT4: ['MatMul'],
FP8: ['MatMul']. The tool inserts QDQ nodes following compiler friendly patterns and generates an
explicit ONNX model.
"""
import logging
import os
import re
import shutil
import tempfile
from typing import List, Tuple

import onnx
import onnx.onnx_cpp2py_export.checker as C  # noqa: N812
import onnx_graphsurgeon as gs
from onnx_graphsurgeon.ir.graph import Graph
from onnx_graphsurgeon.ir.node import Node
from onnxruntime.quantization import (
    CalibrationMethod,
    quantize_static,
)
from onnxruntime.quantization.operators.qdq_base_operator import QDQOperatorBase
from onnxruntime.quantization.quant_utils import (
    QuantType,
)
from onnxruntime.quantization.registry import QDQRegistry, QLinearOpsRegistry

from modelopt.onnx.op_types import get_quantizable_op_types
from modelopt.onnx.quantization.calib_utils import (
    CalibrationDataProvider,
    CalibrationDataType,
    RandomDataProvider,
)
from modelopt.onnx.quantization.graph_utils import (
    build_non_residual_input_map,
    classify_partition_nodes,
    filter_quantizable_kgen_heads,
    print_stat,
    remove_partial_input_qdq,
)
from modelopt.onnx.quantization.int4 import quantize_int4
from modelopt.onnx.quantization.operators import QDQConvTranspose, QDQNormalization
from modelopt.onnx.quantization.ort_patching import patch_ort_modules
from modelopt.onnx.quantization.partitioning import (
    find_fusible_partitions,
    find_non_quantizable_partitions_from_patterns,
    find_quantizable_nodes,
    get_skiped_output_layers,
)
from modelopt.onnx.utils import (
    duplicate_shared_linear_weights,
    name_onnx_nodes,
    save_onnx,
)

__all__ = ["quantize"]

QUANT_MODES = [
    "int8",  # INT8 quantization of both scales and activations.
    "int4_rtn",  # INT4 weight-only quantization. Inserts Q and DQ nodes around each eligible weight tensor.
    "int4_rtn_dq",  # INT4 weight-only quantization. Directly computes the INT4 weights, and only inserts DQ nodes.
    "int4_rtn_trt",  # Same as `int4_rtn`, but exports TRT custom Q/DQ nodes instead.
    "int4_rtn_trt_dq",  # Same as `int4_rtn_dq`, but exports TRT custom DQ nodes instead.
    "int4_awq_clip",  # INT4 AWQ Clip. Inserts DQ nodes for each eligible weight tensor.
    "int4_awq_clip_trt",  # Same as `int4_awq_clip`, but exports TRT custom DQ nodes instead.
    "fp8",
]

# Set logging level to info
logging.getLogger().setLevel(logging.INFO)


def _load_and_preprocess(
    onnx_path: str,
    use_external_data_format: bool,
    output_path: str,
):
    # Load the model and weights
    onnx_model = onnx.load(onnx_path, load_external_data=use_external_data_format)

    # Per-Channel support with QDQ format requires onnx opset version 13 or above
    ai_onnx_domain = [
        opset
        for opset in onnx_model.opset_import
        if not opset.domain or opset.domain in ["ai.onnx", "ai.onnx.contrib"]
    ]
    opset_version = ai_onnx_domain[0].version
    logging.info(f"Model {onnx_path} with opset_version {opset_version} is loaded.")

    intermediate_generated_files = []
    output_dir = os.path.dirname(output_path)
    model_name = os.path.splitext(os.path.basename(onnx_path))[0]

    required_opset_version = 13
    if opset_version < required_opset_version and opset_version != 1:
        opset_version = required_opset_version
        onnx_model = onnx.version_converter.convert_version(onnx_model, opset_version)
        onnx_path = os.path.join(output_dir, f"{model_name}_opset{opset_version}.onnx")
        save_onnx(onnx_model, onnx_path, use_external_data_format)
        logging.info(f"Model is cloned to {onnx_path} with opset_version {opset_version}.")
        intermediate_generated_files.append(onnx_path)

    # Sometimes input onnx model does not contain the node names
    # This tool depends on those names, so we assign names if needed
    graph = onnx_model.graph
    is_named = name_onnx_nodes(graph)
    is_duplicated = duplicate_shared_linear_weights(graph)

    if is_named or is_duplicated:
        onnx_path = os.path.join(output_dir, f"{model_name}_named.onnx")
        save_onnx(onnx_model, onnx_path, use_external_data_format)
        logging.info(f"Model is cloned to {onnx_path} after naming the nodes.")
        intermediate_generated_files.append(onnx_path)

    return onnx_model, onnx_path, opset_version, intermediate_generated_files


def _find_nodes_from_op_types_to_exclude(graph: Graph, op_types_to_exclude=None) -> List[str]:
    nodes_to_exclude = []
    if op_types_to_exclude:
        nodes_to_exclude = [node.name for node in graph.nodes if node.op in op_types_to_exclude]
    return nodes_to_exclude


def _expand_node_names_from_patterns(graph: Graph, name_patterns: List[str]) -> List[str]:
    matched_node_names = []
    for pattern in name_patterns:
        for node in graph.nodes:
            if re.match(pattern, node.name):
                matched_node_names.append(node.name)

    return matched_node_names


def _configure_ort(op_types: List[str], op_types_to_quantize: List[str]):
    # Register some new QDQ operators on top of ORT
    QDQRegistry["BatchNormalization"] = QDQNormalization
    QDQRegistry["ConvTranspose"] = QDQConvTranspose
    QDQRegistry["LRN"] = QDQNormalization  # Example: caffenet-12.onnx
    QDQRegistry["HardSwish"] = (
        QDQOperatorBase  # Example: mobilenet_v3_opset17, efficientvit_b3_opset17
    )

    # Patch ORT modules to fix bugs and support some edge cases
    patch_ort_modules()

    # Remove copy, reduction and activation ops from ORT QDQ registry
    for op_type in [
        "ArgMax",
        "Concat",
        "EmbedLayerNormalization",
        "Gather",
        "InstanceNormalization",
        "LeakyRelu",
        "Pad",
        "Relu",
        "Reshape",
        "Resize",
        "Sigmoid",
        "Softmax",
        "Split",
        "Squeeze",
        "Transpose",
        "Unsqueeze",
        "Where",
    ]:
        if op_type in QLinearOpsRegistry:
            del QLinearOpsRegistry[op_type]
        if op_type in QDQRegistry:
            del QDQRegistry[op_type]

    # Prepare TensorRT friendly quantization settings
    trt_guided_options = {
        "QuantizeBias": False,
        "ActivationSymmetric": True,
        "OpTypesToExcludeOutputQuantization": op_types,  # No output quantization
        "AddQDQPairToWeight": True,  # Instead of quantizing the weights, add QDQ node
        "QDQOpTypePerChannelSupportToAxis": {
            "Conv": 0,
            "ConvTranspose": 1,
        },  # per_channel should be True
        "DedicatedQDQPair": True,
        "ForceQuantizeNoInputCheck": (
            # By default, for some latent operators like MaxPool, Transpose, etc.,
            # ORT does not quantize if their input is not quantized already.
            True
        ),
    }

    quantizable_op_types = get_quantizable_op_types(op_types_to_quantize)
    return trt_guided_options, quantizable_op_types


def _find_nodes_to_quantize(
    graph: Graph,
    quantizable_op_types: List[str],
    verbose: bool,
) -> Tuple[List[Node], List[Tuple[Node, Node, str]]]:
    # Build a map of add nodes to their non-residual inputs, i.e. fusible with Conv group
    logging.info("Building non-residual Add input map ...")
    non_residual_inputs = build_non_residual_input_map(graph)

    logging.info(
        "Searching for hard-coded patterns like MHA, LayerNorm, etc. to avoid quantization."
    )
    non_quantizable_hard_coded_partitions = find_non_quantizable_partitions_from_patterns(graph)

    logging.info("Building KGEN/CASK targeted partitions ...")
    # partitioned_nodes keeps track of nodes that are already part of some partition.
    # Certain nodes of those partitions are quantizable. For example, heads.
    partitioned_nodes = set(sum(non_quantizable_hard_coded_partitions, []))
    cask_fusible_partitions, kgen_partitions = find_fusible_partitions(
        graph,
        partitioned_nodes,
        non_residual_inputs,
    )
    if verbose:
        logging.info(
            "CASK fusible partitions:"
            f" {[[node.name for node in partition] for partition in cask_fusible_partitions]}"
        )
        logging.info(
            "KGEN partitions:"
            f" {[[node.name for node in partition] for partition in kgen_partitions]}"
        )

    logging.info("Classifying the partition nodes ...")
    _, quantizable_partition_nodes, no_quantize_inputs = classify_partition_nodes(
        cask_fusible_partitions,
    )
    quantizable_kgen_heads, no_quantize_kgen_inputs = filter_quantizable_kgen_heads(
        cask_fusible_partitions,
        kgen_partitions,
        quantizable_op_types,
    )

    quantizable_nodes = quantizable_kgen_heads + quantizable_partition_nodes
    paritially_quantizable_nodes = [dst for _, dst, _ in no_quantize_inputs]

    # Quantize all inputs of partially quantizable nodes by ORT
    # but remove QDQ from non-quantizable inputs in the post-processing step
    quantizable_nodes.extend(paritially_quantizable_nodes)

    quantizable_nodes.extend(
        find_quantizable_nodes(graph, quantizable_nodes, partitioned_nodes, quantizable_op_types)
    )

    skip_list = get_skiped_output_layers(graph, paritially_quantizable_nodes)
    quantizable_nodes = [node for node in quantizable_nodes if node.name not in skip_list]

    return quantizable_nodes, no_quantize_inputs + no_quantize_kgen_inputs


def _find_nodes_to_exclude(
    graph: Graph, nodes_to_exclude: List[str], op_types_to_exclude: List[str]
):
    nodes_to_exclude = nodes_to_exclude or []
    nodes_to_exclude = _expand_node_names_from_patterns(graph, nodes_to_exclude)
    nodes_to_exclude.extend(_find_nodes_from_op_types_to_exclude(graph, op_types_to_exclude))

    # Remove duplicates from the exclusion list
    return [*set(nodes_to_exclude)]


def quantize(
    onnx_path: str,
    calibration_data: CalibrationDataType = None,
    calibration_method: str = "entropy",
    op_types_to_quantize: List[str] = None,
    op_types_to_exclude: List[str] = None,
    nodes_to_quantize: List[str] = None,
    nodes_to_exclude: List[str] = None,
    use_external_data_format: bool = False,
    keep_intermediate_files: bool = False,
    output_path: str = None,
    verbose: bool = False,
    quantize_mode: str = "int8",
) -> None:
    """Quantize the given onnx model.

    Args:
        onnx_path:
            Path to the input onnx model.
        calibration_data:
            Calibration data, either a numpy array or list/dict of numpy array.
        calibration_method:
            Calibration method. Options={entropy (default), minmax}.
        op_types_to_quantize:
            List of types of operators to quantize. When this list is not None, only the types in this list
            are quantized. Example: ['Conv'] indicates that only ops of type 'Conv' should be quantized.
            If this list is None (default), all supported operators are quantized.
            This flag does not support regular expression.
        op_types_to_exclude:
            List of types of operators to exclude from quantization.
            This flag does not support regular expression.
        nodes_to_quantize:
            List of node names to quantize. When this list is not None, only the nodes in this list
            are quantized. Example: ['Conv__224', 'Conv__252'].
            If this list is None (default), all supported nodes are quantized.
            This flag does not support regular expression.
        nodes_to_exclude:
            List of nodes names to exclude. The nodes in this list will be excluded from quantization
            when it is not None. This flag supports regular expression.
        use_external_data_format:
            If not None, this path will be used to store the weights of the quantized model.
        keep_intermediate_files:
            If False, only save the converted ONNX files for the user. Otherwise, keep all intermediate files
             generated during the ONNX models' conversion/calibration.
        output_path:
            Output filename to save the converted ONNX model.
            If None, save in the same directory as the original ONNX model with .quant suffix.
        verbose:
            Prints details of node partition, selection etc. throughout the quantization process.
        quantize_mode:
            Quantization mode. One of ['int8', 'int4_rtn', 'int4_rtn_dq', 'int4_rtn_trt', 'int4_rtn_trt_dq',
            'int4_awq_clip', 'int4_awq_clip_trt', 'fp8']. 'int8' by default. Any INT4-based mode is GEMM weight-only
            and FP8 mode is MatMul only quantization.

    Returns:
        None, write the quantized onnx model in the same directory with filename like "<model_name>.quant.onnx".
    """
    # quantize_static creates a shape-inferred copy at the input model's directory
    # Needs to check if we have write permission to this directory
    assert onnx_path.endswith(".onnx") or onnx_path.endswith(".pb")
    if not os.access(os.path.dirname(os.path.abspath(onnx_path)), os.W_OK):
        old_dir = os.path.dirname(os.path.abspath(onnx_path))
        tmp_dir = tempfile.mkdtemp()
        logging.info(f"Directory {old_dir} is not writable, store intermediate files in {tmp_dir}")
        onnx_path = os.path.join(tmp_dir, os.path.basename(onnx_path))

        # We assume that the model directory contains only model related weights and protobuf file
        # Anything extra in the model directory will be copied unnecessarily
        for file in os.listdir(old_dir):
            old_file_path = os.path.join(old_dir, file)
            new_file_path = os.path.join(tmp_dir, file)
            if os.path.isfile(old_file_path):
                shutil.copy(old_file_path, new_file_path)

    model_name = os.path.splitext(os.path.basename(onnx_path))[0]
    if not output_path:
        output_dir = os.path.dirname(onnx_path)
        output_path = os.path.join(output_dir, f"{model_name}.quant.onnx")
        logging.info(f"No output path specified, save quantized model to {output_path}")

    # We need to preprocess the model with naming, weight duplication etc.
    onnx_model, onnx_path, opset_version, intermediate_generated_files = _load_and_preprocess(
        onnx_path, use_external_data_format, output_path
    )

    # Use random scales if calibration data is not supplied
    if calibration_data is None:
        calibration_data_reader = RandomDataProvider(onnx_path)
    else:
        calibration_data_reader = CalibrationDataProvider(onnx_path, calibration_data)

    if quantize_mode == "int8" or quantize_mode == "fp8":
        # Take the onnx graph
        graph = gs.import_onnx(onnx_model)
        graph.toposort()

        # Change the default configuration of ORT quantization
        op_types_to_quantize = op_types_to_quantize or []
        op_types = set([node.op for node in graph.nodes])
        trt_guided_options, quantizable_op_types = _configure_ort(
            list(op_types), op_types_to_quantize
        )

        if quantize_mode == "fp8":
            # Quantizable op type is limited to Gemm (Matmul) and Conv for fp8
            quantizable_op_types = op_types_to_quantize or ["Gemm", "MatMul", "Conv"]

        logging.info(
            "Quantizable op types in the model:"
            f" {[t for t in quantizable_op_types if t in op_types]}"
        )

        no_quantize_inputs = []
        if not nodes_to_quantize:
            quantizable_nodes, no_quantize_inputs = _find_nodes_to_quantize(
                graph,
                quantizable_op_types,
                verbose,
            )
            nodes_to_quantize = [node.name for node in quantizable_nodes]

        if not op_types_to_quantize and not nodes_to_quantize:
            logging.info("No node or node type is selected for quantization!")
            return

        # Collect node names to exclude from quantization
        nodes_to_exclude = _find_nodes_to_exclude(graph, nodes_to_exclude, op_types_to_exclude)

        logging.info(f"Total number of nodes: {len(graph.nodes)}")
        logging.info(f"Manually skipped node count: {len(nodes_to_exclude)}")
        if verbose:
            logging.info(f"Manually skipped nodes: {nodes_to_exclude}")

        if not op_types_to_quantize and not nodes_to_quantize:
            logging.info("No node or node type is selected for quantization!")
            return

        if quantize_mode == "int8":
            # Use ort api to quantize the onnx model
            quantize_static(
                onnx_path,
                output_path,
                calibration_data_reader,
                op_types_to_quantize=op_types_to_quantize,
                nodes_to_quantize=nodes_to_quantize,
                nodes_to_exclude=nodes_to_exclude,
                per_channel=(opset_version >= 13),
                extra_options=trt_guided_options,
                use_external_data_format=use_external_data_format,
                calibrate_method=(
                    CalibrationMethod.Entropy
                    if calibration_method == "entropy"
                    else CalibrationMethod.MinMax
                ),
            )

            if use_external_data_format:
                intermediate_generated_files.append(output_path + ".data")

            # Post-processing of the onnx model after ort quantization
            onnx_model = onnx.load(output_path)
            graph = gs.import_onnx(onnx_model)

            remove_partial_input_qdq(graph, no_quantize_inputs)
            onnx_model = gs.export_onnx(graph)
        else:  # quantize_mode == "fp8"
            quantize_static(
                onnx_path,
                output_path,
                calibration_data_reader,
                op_types_to_quantize=op_types_to_quantize,
                nodes_to_quantize=nodes_to_quantize,
                nodes_to_exclude=nodes_to_exclude,
                # Enabling this causes a model with both FP8 and INT8 nodes which TRT is not happy with
                per_channel=False,
                use_external_data_format=use_external_data_format,
                # This is the only available calibrate method for fp8 now
                calibrate_method=CalibrationMethod.Distribution,
                extra_options=trt_guided_options,
                activation_type=QuantType.QFLOAT8E4M3FN,
                weight_type=QuantType.QFLOAT8E4M3FN,
            )
            # Load the quantized output model for printing stat etc.
            onnx_model = onnx.load(output_path)
    else:
        onnx_model = quantize_int4(
            quantize_mode,
            onnx_model,
            calibration_data_reader,
            use_external_data_format,
        )

    # Collect and print stats of the quantized model
    print_stat(gs.import_onnx(onnx_model), verbose)

    # Check if intermediate files should be deleted
    if not keep_intermediate_files:
        for file in intermediate_generated_files:
            os.remove(file)

    # Save the modified model after post-processing
    # Note. FP8 quantized model does not have any post-processing steps
    if quantize_mode != "fp8":
        save_onnx(onnx_model, output_path, use_external_data_format)
    logging.info(f"Quantized onnx model is saved as {output_path}")

    # Check if the quantized model is valid
    try:
        onnx.checker.check_model(output_path)
    except C.ValidationError as e:
        logging.warn("ONNX model checker failed, check your deployment status.")
        logging.warn(e)
