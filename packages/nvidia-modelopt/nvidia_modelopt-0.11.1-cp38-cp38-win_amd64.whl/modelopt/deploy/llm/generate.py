# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""A wrapper over the TensorRT-LLM high level API runner."""


import json
from pathlib import Path
from typing import Dict, Iterable, List, Union

from tensorrt_llm.bindings import KvCacheConfig as TRT_KvCacheConfig
from tensorrt_llm.hlapi.llm import LLM as TRT_LLM
from tensorrt_llm.hlapi.llm import ModelConfig as TRT_ModelConfig
from tensorrt_llm.hlapi.tokenizer import TokenizerBase, TransformersTokenizer


class LLM(TRT_LLM):
    """A wrapper over the ``tensorrt_llm.hlapi.llm.LLM`` for LLM profiling and validation."""

    def __init__(
        self,
        engine_dir: Union[str, Path],
        tokenizer: TokenizerBase,
        kv_cache_config: Dict[str, Union[int, float]] = {},
    ):
        """Initializes the LLM runner class.

        Args:
            engine_dir: the directory path of the TensorRT-LLM engine.
            tokenizer: the tokenizer. For example, a tokenizer from the Huggingface model.
            kv_cache_config: the kv cache config as a dict. Please refer to
                https://github.com/NVIDIA/TensorRT-LLM/blob/main/docs/source/performance/perf-best-practices.md
        """
        trt_llm_config = TRT_ModelConfig(model_dir=engine_dir)

        with open(Path(engine_dir) / "config.json", "r") as engine_config_file:
            engine_config = json.load(engine_config_file)
            build_config = engine_config["build_config"]
            max_tokens_in_paged_kv_cache = (
                build_config["max_input_len"]
                + build_config["max_output_len"] * build_config["max_beam_width"]
            ) * build_config["max_batch_size"]

        trt_kv_cache_config = TRT_KvCacheConfig()

        if (
            "kv_cache_free_gpu_mem_fraction" in kv_cache_config
            and "max_tokens_in_paged_kv_cache" not in kv_cache_config
        ):
            trt_kv_cache_config.free_gpu_memory_fraction = kv_cache_config[
                "free_gpu_memory_fraction"
            ]
        else:
            trt_kv_cache_config.max_tokens = kv_cache_config.get(
                "max_tokens_in_paged_kv_cache", max_tokens_in_paged_kv_cache
            )

        super().__init__(
            trt_llm_config,
            tokenizer=TransformersTokenizer(tokenizer),
            kv_cache_config=trt_kv_cache_config,
        )

    @property
    def max_input_len(self):
        """Get the max input length from the LLM instance."""
        return self.config.max_input_len

    @property
    def max_beam_width(self):
        """Get the max beam width from the LLM instance."""
        return self.config.max_beam_width

    def generate_text(
        self,
        prompts: Union[Iterable[str], Iterable[List[int]]],
        max_new_tokens: int,
        temperature: float = 1.0,
        keep_input_prompt: bool = True,
    ) -> Union[List[str], List[List[str]]]:
        """Generates the text based on the input prompts.

        Args:
            prompts: The input prompts. Could be a list of strings or token lists.
            max_new_tokens: The max output token length.
            temperature: The sampling temperature
            keep_input_prompt: Set to include input prommpts in the outputs.

        Returns:
            a list of output text strings if max_beam_width is 1 or a 2D list with shape [batch, beam].
        """
        beam_width = self.max_beam_width
        sampling_config = self.get_default_sampling_config()
        sampling_config.max_new_tokens = max_new_tokens
        sampling_config.beam_width = beam_width
        sampling_config.temperature = [temperature]

        prompt_ids = [
            self.tokenizer.encode(prompt) if isinstance(prompt, str) else prompt
            for prompt in prompts
        ]
        outputs = self.generate(prompt_ids, sampling_config=sampling_config)

        output_texts = []
        for prompt_id, output in zip(prompt_ids, outputs):
            if isinstance(output.token_ids[0], list):
                # beam search
                output_token_ids = output.token_ids
            else:
                output_token_ids = [output.token_ids]

            for output_token_id in output_token_ids:
                output_texts.append(
                    self.tokenizer.decode(
                        output_token_id if keep_input_prompt else output_token_id[len(prompt_id) :]
                    )
                )

        return (
            output_texts
            if beam_width == 1
            else [output_texts[i : i + beam_width] for i in range(0, len(output_texts), beam_width)]
        )
