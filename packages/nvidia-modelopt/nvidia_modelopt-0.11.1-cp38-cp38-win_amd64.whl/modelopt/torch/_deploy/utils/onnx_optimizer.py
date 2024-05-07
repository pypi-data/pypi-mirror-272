# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Utility to optimze onnx graphs."""
import os
import tempfile

import onnx
import onnx_graphsurgeon as gs


class Optimizer:
    """Optimizer for onnx graphs."""

    def __init__(self, onnx_graph, verbose=False):
        """Initializes optimizer."""
        self.graph = gs.import_onnx(onnx_graph)
        self.verbose = verbose

    def info(self, prefix):
        """Prints the graph information."""
        if self.verbose:
            print(
                f"{prefix} .. {len(self.graph.nodes)} nodes,"
                f" {len(self.graph.tensors().keys())} tensors,"
                f" {len(self.graph.inputs)} inputs, {len(self.graph.outputs)} outputs"
            )

    def cleanup(self, return_onnx=False):
        """Cleans the onnx graph.

        Args:
            return_onnx (bool): If True, returns the onnx graph.

        Returns:
            onnx_graph: The cleaned onnx graph.
        """
        self.graph.cleanup().toposort()
        if return_onnx:
            return gs.export_onnx(self.graph)

    def select_outputs(self, keep, names=None):
        """Selects the output nodes."""
        self.graph.outputs = [self.graph.outputs[o] for o in keep]
        if names:
            for i, name in enumerate(names):
                self.graph.outputs[i].name = name

    def infer_shapes(self, return_onnx=False):
        """Infers shapes of the onnx graph."""
        onnx_graph = gs.export_onnx(self.graph)
        if onnx_graph.ByteSize() > 2147483648:
            temp_dir = tempfile.TemporaryDirectory().name
            os.makedirs(temp_dir, exist_ok=True)
            onnx_orig_path = os.path.join(temp_dir, "model.onnx")
            onnx_inferred_path = os.path.join(temp_dir, "inferred.onnx")
            onnx.save_model(
                onnx_graph,
                onnx_orig_path,
                save_as_external_data=True,
                all_tensors_to_one_file=True,
                convert_attribute=False,
            )
            onnx.shape_inference.infer_shapes_path(onnx_orig_path, onnx_inferred_path)
            onnx_graph = onnx.load(onnx_inferred_path)
        else:
            onnx_graph = onnx.shape_inference.infer_shapes(onnx_graph)

        if return_onnx:
            return onnx_graph

    # TODO: Move this fuctionality to the diffusion runner as it is specific to CLIP.
    def clip_add_hidden_states(self, return_onnx=False):
        """Adds hidden states to the CLIP model graph."""
        hidden_layers = -1
        onnx_graph = gs.export_onnx(self.graph)
        for i in range(len(onnx_graph.graph.node)):
            for j in range(len(onnx_graph.graph.node[i].output)):
                name = onnx_graph.graph.node[i].output[j]
                if "layers" in name:
                    hidden_layers = max(int(name.split(".")[1].split("/")[0]), hidden_layers)
        for i in range(len(onnx_graph.graph.node)):
            for j in range(len(onnx_graph.graph.node[i].output)):
                if onnx_graph.graph.node[i].output[
                    j
                ] == "/text_model/encoder/layers.{}/Add_1_output_0".format(hidden_layers - 1):
                    onnx_graph.graph.node[i].output[j] = "hidden_states"
            for j in range(len(onnx_graph.graph.node[i].input)):
                if onnx_graph.graph.node[i].input[
                    j
                ] == "/text_model/encoder/layers.{}/Add_1_output_0".format(hidden_layers - 1):
                    onnx_graph.graph.node[i].input[j] = "hidden_states"
        if return_onnx:
            return onnx_graph

    def fold_constants(self, return_onnx=False):
        """Folds constants in the onnx graph for multiple iterations till prefolded nodes == post folded nodes."""
        prefold_num_nodes = len(self.graph.nodes)
        post_fold_num_nodes = -1
        while prefold_num_nodes != post_fold_num_nodes:
            prefold_num_nodes = len(self.graph.nodes)
            self.graph.fold_constants()
            post_fold_num_nodes = len(self.graph.nodes)
        if return_onnx:
            return gs.export_onnx(self.graph)
