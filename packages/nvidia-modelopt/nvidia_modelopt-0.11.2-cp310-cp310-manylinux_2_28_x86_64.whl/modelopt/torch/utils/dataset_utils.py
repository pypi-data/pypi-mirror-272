# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Utility functions for getting samples and forward loop function for different datasets."""
from typing import TYPE_CHECKING, Callable, List, Optional, Union

import torch
from torch.utils.data import DataLoader

if TYPE_CHECKING:
    from transformers import PreTrainedTokenizer, PreTrainedTokenizerFast

# Use dict to store the config for each dataset.
# If we want to export more options to user like target languages, we need more standardized approach like dataclass.
SUPPORTED_DATASET_CONFIG = {
    "cnn_dailymail": {
        "config": {"path": "cnn_dailymail", "name": "3.0.0"},
        "target": "article",
    },
    "pile": {
        "config": {"path": "monology/pile-uncopyrighted"},
        "target": "text",
    },
    "pg19": {
        "config": {"path": "pg19"},
        "target": "text",
    },
    "wikipedia": {
        "config": {"path": "wikipedia", "name": "20220301.en"},
        "target": "text",
    },
    "c4": {
        "config": {"path": "c4", "name": "en"},
        "target": "text",
    },
}

__all__ = ["create_forward_loop", "get_dataset_dataloader"]


def _get_dataset_samples(dataset_name: str, num_samples: int) -> List[str]:
    """Load a portion of train dataset with the dataset name and a given size.

    Args:
        dataset_name: Name of the dataset to load.
        num_samples: Number of samples to load from the dataset.

    Returns:
        Smaples: The list of samples.
    """
    # Load the dataset
    if dataset_name in SUPPORTED_DATASET_CONFIG:
        try:
            from datasets import load_dataset
        except ModuleNotFoundError:
            print(
                "The 'datasets' module is not installed. Please install it using 'pip install"
                " datasets' to continue."
            )
        # Use streaming can reduce the downloading time for large datasets
        dataset = load_dataset(
            split="train", streaming=True, **SUPPORTED_DATASET_CONFIG[dataset_name]["config"]
        )
    else:
        raise NotImplementedError(
            f"dataset {dataset_name} is not supported. Check available datasets with"
            " get_supported_datasets."
        )

    # Access only the required samples
    samples = []
    target_key = SUPPORTED_DATASET_CONFIG[dataset_name]["target"]
    for i, sample in enumerate(dataset):
        if i >= num_samples:
            break
        samples.append(sample[target_key])

    return samples


def get_dataset_dataloader(
    dataset_name: str = "cnn_dailymail",
    tokenizer: Union["PreTrainedTokenizer", "PreTrainedTokenizerFast"] = None,
    batch_size: int = 1,
    num_samples: int = 512,
    max_sample_length: int = 512,
    device: Optional[str] = None,
) -> DataLoader:
    """Get a dataloader with the dataset name and toknizer of the target model.

    Args:
        dataset_name: Name of the dataset to load.
        tokenizer: Instancne of Hugginface tokenizer.
        batch_size: Batch size of the returned dataloader.
        num_samples: Number of samples from the dataset.
        max_sample_length: Maximum length of a sample.
        device: Target device for the returned dataloader.

    Returns:
        A instance of dataloader.
    """
    assert tokenizer is not None, "Please provide a tokenizer."

    dataset = _get_dataset_samples(dataset_name, num_samples=num_samples)

    batch_encoded = tokenizer.batch_encode_plus(
        dataset, return_tensors="pt", padding=True, truncation=True, max_length=max_sample_length
    )
    if device:
        batch_encoded = batch_encoded.to(device)
    batch_encoded = batch_encoded["input_ids"]

    calib_dataloader = DataLoader(batch_encoded, batch_size=batch_size, shuffle=False)

    return calib_dataloader


def get_supported_datasets():
    """Retrieves a list of datasets supported.

    Returns:
    - list[str]: A list of strings, where each string is the name of a supported dataset.

    Example usage:

    ```python
    print("Supported datasets:", get_supported_datasets())
    ```
    """
    return SUPPORTED_DATASET_CONFIG.keys()


def create_forward_loop(
    model: torch.nn.Module = None,
    dataset_name: str = "cnn_dailymail",
    tokenizer: Union["PreTrainedTokenizer", "PreTrainedTokenizerFast"] = None,
    batch_size: int = 1,
    num_samples: int = 512,
    max_sample_length: int = 512,
    device: Optional[str] = None,
) -> Callable:
    """Creates and returns a forward loop function configured for a specific model, dataset, and tokenizer.

    This function initializes a forward loop function tailored to process batches of data from the specified dataset
    using the given model and tokenizer. The forward loop function, when called, iterates over the dataset, applies the
    tokenizer to prepare the input data, feeds it into the model, and returns the model's predictions.

    Parameters:
    - model: The PyTorch model for inference.
    - dataset_name: The name of the dataset to be used.
    - tokenizer: The tokenizer used to preprocess text data into a format suitable
    for the model.
    - batch_size: Batch size of the returned dataloader.
    - num_samples: Number of samples from the dataset.
    - max_sample_length: Maximum length of a sample.
    - device: Target device for the returned dataloader.

    Example usage for quantization:

    .. code-block:: python

        import modelopt.torch.quantization as mtq

        # Initialize model and tokenizer
        # ...

        # Create forward loop for calibration
        forward_loop = create_forward_loop(model=model, dataset_name="cnn_dailymail", tokenizer=tokenizer)

        # Quantize the model with the calibration dataset
        mtq.quantize(model, quant_cfg, forward_loop=forward_loop)

    Returns:
    - function: A forward loop function that can be called with no arguments. When called, this function iterates over
    the dataset specified by `dataset_name`.
    """
    dataloader = get_dataset_dataloader(
        dataset_name=dataset_name,
        tokenizer=tokenizer,
        batch_size=batch_size,
        num_samples=num_samples,
        max_sample_length=max_sample_length,
        device=device,
    )

    def forward_loop(*args, **kwargs):
        """Adjusts weights and scaling factors based on selected algorithms."""
        if args or kwargs:
            print("Warning: The following arguments will not be used in the forward loop:")
            for i, arg in enumerate(args):
                print(f"- Positional argument {i}: {arg}")
            for key, value in kwargs.items():
                print(f"- Keyword argument '{key}': {value}")
        for idx, data in enumerate(dataloader):
            model(data)

    return forward_loop
