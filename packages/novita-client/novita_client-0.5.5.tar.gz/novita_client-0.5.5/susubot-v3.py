#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from novita_client import NovitaClient, Txt2ImgV3LoRA, Samplers, ADETailerLoRA
from novita_client.utils import base64_to_image, input_image_to_pil
from PIL import Image


def make_image_grid(images, rows: int, cols: int, resize: int = None):
    """
    Prepares a single grid of images. Useful for visualization purposes.
    """
    assert len(images) == rows * cols

    if resize is not None:
        images = [img.resize((resize, resize)) for img in images]

    w, h = images[0].size
    grid = Image.new("RGB", size=(cols * w, rows * h))

    for i, img in enumerate(images):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid


client = NovitaClient(os.getenv('NOVITA_API_KEY'))

first_stage_response = client.txt2img_v3(
    prompt="Hana bunny, photorealistic, beautiful",
    negative_prompt="(hands:1.4), (cleft chin:1.4), (smile line:1.2), fingers, face lines, face shadow, extra limbs, defined cheekbones, face detail, (makeup:1.2), (dark eyebrows:1.2), prominent eyebrows, (wrinkles:1.2), (smile line:1.3), (defined cheekbones:1.2), extra limbs, open mouth, teeth, fat, tall, extremely big tits, bad nipples, (teeth:1.2), cross eyed, watermark, bangs, thin",
    model_name='epicrealism_pureEvolutionV5_97793.safetensors',
    image_num=1,
    steps=30,
    guidance_scale=4.0,
    height=960,
    width=640,
    seed=1234,
    sampler_name=Samplers.DPMPP_M_KARRAS,
    loras=[
        Txt2ImgV3LoRA(
            model_name='HanaBunnyv2_24326',
            strength=0.4
        ),
    ],
    download_images=False
)

second_stage = client.adetailer(
    model_name='epicrealism_pureEvolutionV5_97793.safetensors',
    input_images=first_stage_response.get_image_urls(),
    steps=20,
    sampler_name=Samplers.DPMPP_M_KARRAS,
    strength=0.5,
    guidance_scale=4.0,
    loras=[
        ADETailerLoRA(
            model_name='HanaBunnyv2_24326',
            strength=1.0
        )
    ],
    prompt="closeup photo of Hana bunny",
    negative_prompt="cleft chin, smile line, Lines on face, face shadows, bad chin, deformed, defined cheekbones, face detail, dark eyebrows, prominent eyebrows, wrinkles, extra limbs, open mouth, teeth, cross eyed, watermark, bangs",
    download_images=False
)

images = []
images.extend([input_image_to_pil(img) for img in first_stage_response.get_image_urls()])
images.extend([input_image_to_pil(img) for img in second_stage.get_image_urls()])
make_image_grid(images, 1, 2).save("output.jpg")
