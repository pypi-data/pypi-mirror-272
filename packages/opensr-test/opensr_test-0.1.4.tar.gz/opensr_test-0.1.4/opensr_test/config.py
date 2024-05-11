from typing import Any, List, Optional, Union, Literal

import torch
from pydantic import BaseModel, field_validator, model_validator

DistanceMetrics = Literal[
    "kl", "l1", "l2", "pbias", "psnr", "sad",
    "mtf", "lpips", "clip"
]

class Config(BaseModel):
    # General parameters
    agg_method: str = "pixel"  # pixel, image, patch
    patch_size: Optional[int] = None
    border_mask: Optional[int] = 16    
    rgb_bands: Optional[List[int]] = [0, 1, 2]

    # Spatial parameters
    spatial_method: Literal["ecc", "pcc", "lightglue"] = "ecc"
    spatial_threshold_distance: int = 3
    spatial_max_num_keypoints: int = 100

    # Spectral parameters
    reflectance_distance: DistanceMetrics = "l1"
    spectral_distance: DistanceMetrics = "sad"

    # Create SRharm
    harm_apply_spectral: bool = True
    harm_apply_spatial: bool = True

    # Synthesis parameters
    synthesis_distance: DistanceMetrics = "l1"

    # Correctness parameters
    correctness_distance: DistanceMetrics = "l1"

    # General parameters - validator ----------------------------
    @field_validator("agg_method")
    @classmethod
    def check_agg_method(cls, value) -> str:
        valid_methods = ["pixel", "image", "patch"]
        if value not in valid_methods:
            raise ValueError(f"Invalid method. Must be one of {valid_methods}")
        return value

    @field_validator("rgb_bands")
    @classmethod
    def check_rgb_bands(cls, value) -> List[int]:
        if len(value) != 3:
            raise ValueError("rgb_bands must have 3 elements.")
        return value

    @field_validator("spatial_max_num_keypoints")
    @classmethod
    def check_spatial_max_num_keypoints(cls, value) -> int:
        if value < 0:
            raise ValueError("spatial_max_num_keypoints must be positive.")
        return value

    @field_validator("spatial_threshold_distance")
    @classmethod
    def check_spatial_threshold_distance(cls, value) -> int:
        if value < 0:
            raise ValueError("spatial_threshold_distance must be positive.")
        return value


    # Create SRharm - validator ------------------------------------------
    @field_validator("harm_apply_spectral")
    @classmethod
    def check_harm_apply_spectral(cls, value) -> bool:
        if not isinstance(value, bool):
            raise ValueError("harm_apply_spectral must be boolean.")
        return value

    @field_validator("harm_apply_spatial")
    @classmethod
    def check_harm_apply_spatial(cls, value) -> bool:
        if not isinstance(value, bool):
            raise ValueError("harm_apply_spatial must be boolean.")
        return value


class Consistency(BaseModel):
    reflectance: Any
    spectral: Any
    spatial: Any

class Synthesis(BaseModel):
    distance: Any

class Correctness(BaseModel):
    omission: Any
    improvement: Any
    hallucination: Any
    classification: Any

class Auxiliar(BaseModel):
    sr_harm: Any
    lr_to_hr: Any
    d_ref: Any
    d_im: Any
    d_om: Any

class Results(BaseModel):
    consistency: Consistency
    synthesis: Synthesis
    correctness: Correctness
    auxiliar: Auxiliar

