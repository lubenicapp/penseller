"""
Text-to-Image generation using fal.ai API

This module provides functionality to generate images from text prompts
using the fal.ai API.
"""

from decouple import config
import fal_client
import os

os.environ['FAL_KEY'] = config('FAL_KEY')

def generate_image(
    prompt: str,
    model: str = "fal-ai/flux/schnell",
    image_size: str = "landscape_4_3",
    num_inference_steps: int = 4,
    num_images: int = 1,
    enable_safety_checker: bool = True,
) -> dict:
    """
    Generate an image from a text prompt using fal.ai API.

    Args:
        prompt: Text description of the image to generate
        model: The model to use for generation (default: "fal-ai/flux/schnell")
        image_size: Size of the generated image (default: "landscape_4_3")
                   Options: "square_hd", "square", "portrait_4_3", "portrait_16_9",
                           "landscape_4_3", "landscape_16_9"
        num_inference_steps: Number of inference steps (default: 4)
        num_images: Number of images to generate (default: 1)
        enable_safety_checker: Enable safety checker (default: True)

    Returns:
        dict: Response containing generated image URLs and metadata

    Example:
        >>> result = generate_image("A beautiful sunset over mountains")
        >>> print(result['images'][0]['url'])
    """

    # Ensure API key is set
    if not config("FAL_KEY"):
        raise ValueError(
            "FAL_KEY environment variable not set. "
            "Get your API key from https://fal.ai/dashboard/keys"
        )

    # Call fal.ai API
    result = fal_client.subscribe(
        model,
        arguments={
            "prompt": prompt,
            "image_size": image_size,
            "num_inference_steps": num_inference_steps,
            "num_images": num_images,
            "enable_safety_checker": enable_safety_checker,
        },
    )

    return result


def generate_image_sync(
    prompt: str,
    model: str = "fal-ai/flux/schnell",
    **kwargs
) -> dict:
    """
    Synchronous wrapper for image generation.

    Args:
        prompt: Text description of the image to generate
        model: The model to use for generation
        **kwargs: Additional arguments passed to generate_image

    Returns:
        dict: Response containing generated image URLs and metadata
    """
    return generate_image(prompt, model, **kwargs)


if __name__ == "__main__":
    # Example usage
    import sys

    # Check if API key is set
    try:
        fal_key = config("FAL_KEY")
        if not fal_key:
            raise ValueError("FAL_KEY is empty")
    except Exception:
        print("Error: FAL_KEY not found in .env file")
        print("Add it to your .env file: FAL_KEY=your-api-key-here")
        print("Get your API key from: https://fal.ai/dashboard/keys")
        sys.exit(1)

    # Example prompt
    prompt = "A middle aged man holding a pencil"

    print(f"Generating image with prompt: '{prompt}'")
    print("Please wait...")

    try:
        result = generate_image(prompt)

        print("\n✅ Image generated successfully!")
        print(f"Number of images: {len(result.get('images', []))}")

        for idx, image in enumerate(result.get('images', []), 1):
            print(f"\nImage {idx}:")
            print(f"  URL: {image.get('url')}")
            print(f"  Width: {image.get('width')}px")
            print(f"  Height: {image.get('height')}px")
            print(f"  Content Type: {image.get('content_type')}")

        # Print seed if available
        if 'seed' in result:
            print(f"\nSeed: {result['seed']}")

    except Exception as e:
        print(f"\n❌ Error generating image: {e}")
        sys.exit(1)
