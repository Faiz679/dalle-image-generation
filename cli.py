#!/usr/bin/env python3

import os
import sys
import argparse
import openai
import json

# Set up defaults and get API key from environment variable
defaults = {
    "api_key": os.getenv('OPENAI_API_KEY'),
    "model": "dall-e-3",
    "size": "1024x1024",
    "quality": "standard",
    "number": "1",
}

def validate_and_parse_args(parser):
    args = parser.parse_args()

    for key, value in vars(args).items():
        if not value:
            args.__dict__[key] = parser.get_default(key)

    if not args.api_key:
        parser.error('The --api-key argument is required if OPENAI_API_KEY is not set.')
    if not args.prompt:
        parser.error('The --prompt argument is required.')
    if not args.number.isdigit():
        parser.error('The --number argument must be a number.')
    args.number = int(args.number)

    return args

def main():
    parser = argparse.ArgumentParser(description="Generate image using OpenAI DALL·E.")
    parser.add_argument('-k', '--api-key', type=str, default=defaults["api_key"],
                        help='OpenAI API key. Can also be set with OPENAI_API_KEY environment variable.')
    parser.add_argument('-p', '--prompt', type=str, required=True,
                        help='Prompt for image generation.')
    parser.add_argument('-m', '--model', type=str, default=defaults["model"],
                        help='Model to use for image generation. Default is "dall-e-3".')
    parser.add_argument('-s', '--size', type=str, default=defaults["size"],
                        help='Size of the image, format WxH (e.g. 1024x1024).')
    parser.add_argument('-q', '--quality', type=str, default=defaults["quality"],
                        help='Quality of the image. Allowed: "standard", "hd".')
    parser.add_argument('-n', '--number', type=str, default=defaults["number"],
                        help='Number of images to generate.')

    args = validate_and_parse_args(parser)

    # Set the OpenAI API key for the request
    openai.api_key = args.api_key

    try:
        response = openai.Image.create(
            model=args.model,
            prompt=args.prompt,
            size=args.size,
            quality=args.quality,
            n=args.number
        )
        # Output must be a proper JSON list of image URLs
        urls = [img["url"] for img in response["data"]]
        print(json.dumps(urls)) 
    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
