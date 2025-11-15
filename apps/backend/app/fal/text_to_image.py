"""
Text-to-Image generation using fal.ai API

This module provides functionality to generate images from text prompts
using the fal.ai API.
"""

from decouple import config
import fal_client
import os

os.environ['FAL_KEY'] = config('FAL_KEY')

def generate_image(prompt: str) -> str:
    """
    Generate an image from a text prompt using fal.ai API.

    Args:
        prompt: Text description of the image to generate

    Returns:
        str: URL of the generated image
    """
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
            "image_size": "landscape_4_3",
            "num_inference_steps": 4,
            "num_images": 1,
            "enable_safety_checker": True,
        },
    )

    return result['images'][0]['url']
