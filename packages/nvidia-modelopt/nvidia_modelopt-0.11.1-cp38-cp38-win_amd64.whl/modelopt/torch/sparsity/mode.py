# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Sparsity mode descriptor."""
from typing import Optional, Set, Type

from torch import nn

from modelopt.torch.opt.config import ModeloptBaseConfig
from modelopt.torch.opt.conversion import ApplyModeError
from modelopt.torch.opt.dynamic import DynamicSpace
from modelopt.torch.opt.mode import (
    ConvertEntrypoint,
    ConvertReturnType,
    MetadataDict,
    RestoreEntrypoint,
    UpdateEntrypoint,
    _ModeDescriptor,
    _ModeRegistryCls,
)
from modelopt.torch.opt.searcher import BaseSearcher
from modelopt.torch.utils import (
    compare_dict,
    unwrap_model,
)

from .config import ExportSparseConfig, SparseGPTConfig, SparseMagnitudeConfig
from .magnitude import MagnitudeSearcher
from .module import SpDMRegistry
from .sparsegpt import SparseGPTSearcher

SparsityModeRegistry = _ModeRegistryCls()


def convert_sparse_model(model: nn.Module, config: ModeloptBaseConfig) -> ConvertReturnType:
    """Function for converting a model to a sparsity meta-model."""
    # we use the search space utility here with a custom registry to convert the model
    dynamic_space = DynamicSpace(model)
    dynamic_space.convert_to_dynamic(config.model_dump(), SpDMRegistry)

    return dynamic_space.model, {"subnet_config": DynamicSpace(model).config()}


def restore_sparse_model(
    model: nn.Module, config: ModeloptBaseConfig, metadata: MetadataDict
) -> nn.Module:
    """Function for restoring a previously convert model to a sparsity meta-model."""
    assert "subnet_config" in metadata
    model, _ = convert_sparse_model(model, config)
    DynamicSpace(model).select(metadata["subnet_config"])

    return model


def update_sparse_metadata(
    model: nn.Module, config: ModeloptBaseConfig, metadata: MetadataDict
) -> None:
    """Update subnet config to current subnet config of model."""
    metadata["subnet_config"] = DynamicSpace(model).config()


def export_sparse(model: nn.Module, config: ExportSparseConfig) -> ConvertReturnType:
    """Export a sparse model to a regular model."""
    # sanity check to avoid DP/DDP here in the entrypoint
    model = unwrap_model(model, raise_error=True)

    # store config from model if we can find it for a future convert/restore process
    metadata = {"subnet_config": DynamicSpace(model).config()}

    # export model in-place
    model = DynamicSpace(model).export(SpDMRegistry)

    return model, metadata


def restore_export_sparse(
    model: nn.Module, config: ExportSparseConfig, metadata: MetadataDict
) -> nn.Module:
    """Restore & export a sparse model to a regular model."""
    # select activated/deactivated sparse modules
    DynamicSpace(model).select(metadata["subnet_config"])

    # run export
    model, metadata_new = export_sparse(model, config)

    # double check metadata
    unmatched_keys = compare_dict(metadata, metadata_new)
    if unmatched_keys:
        raise ApplyModeError(f"Unmatched metadata={unmatched_keys}!")

    return model


@SparsityModeRegistry.register_mode
class SparseMagnitudeModeDescriptor(_ModeDescriptor):
    """Class to define and describe magnitude-based sparsification."""

    @property
    def name(self) -> str:
        """Returns the name of the mode."""
        return "sparse_magnitude"

    @property
    def config_class(self) -> Type[ModeloptBaseConfig]:
        """Specifies the config class for the mode."""
        return SparseMagnitudeConfig

    @property
    def next_modes(self) -> Optional[Set[str]]:
        """Specifies the next modes for the mode."""
        return {"export_sparse", "kd_loss", "quantize"}

    @property
    def export_mode(self) -> Optional[str]:
        """The mode that corresponds to the export mode of this mode."""
        return "export_sparse"

    @property
    def search_algorithm(self) -> Type[BaseSearcher]:
        """Specifies the search algorithm for the mode."""
        return MagnitudeSearcher

    @property
    def convert(self) -> ConvertEntrypoint:
        """The mode's entrypoint for converting a model."""
        return convert_sparse_model

    @property
    def restore(self) -> RestoreEntrypoint:
        """The mode's entrypoint for restoring a model."""
        return restore_sparse_model

    @property
    def update_for_save(self) -> UpdateEntrypoint:
        """The mode's entrypoint for updating the models metadata."""
        return update_sparse_metadata

    @property
    def update_for_new_mode(self) -> UpdateEntrypoint:
        """The mode's entrypoint for updating the models metadata."""
        return update_sparse_metadata


@SparsityModeRegistry.register_mode
class SparseGPTModeDescriptor(SparseMagnitudeModeDescriptor):
    """Class to define and describe sparsification based on SparseGPT."""

    @property
    def name(self) -> str:
        """Returns the name of the mode."""
        return "sparsegpt"

    @property
    def config_class(self) -> Type[ModeloptBaseConfig]:
        """Specifies the config class for the mode."""
        return SparseGPTConfig

    @property
    def search_algorithm(self) -> Type[BaseSearcher]:
        """Specifies the search algorithm for the mode."""
        return SparseGPTSearcher


@SparsityModeRegistry.register_mode
class ExportSparseModeDescriptor(_ModeDescriptor):
    """Class to describe the ``"export_sparse"`` mode.

    The properties of this mode can be inspected via the source code.
    """

    @property
    def name(self) -> str:
        """Returns the value (str representation) of the mode."""
        return "export_sparse"

    @property
    def config_class(self) -> Type[ModeloptBaseConfig]:
        """Specifies the config class for the mode."""
        return ExportSparseConfig

    @property
    def is_export_mode(self) -> bool:
        """Specifies if this mode is an export mode."""
        return True

    @property
    def convert(self) -> ConvertEntrypoint:
        """The mode's entrypoint for converting a model."""
        return export_sparse

    @property
    def restore(self) -> RestoreEntrypoint:
        """The mode's entrypoint for restoring a model."""
        return restore_export_sparse
