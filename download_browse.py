
import json
import os
from pathlib import Path
from urllib.parse import urlparse

import requests

INPUT_FILE = "nisar_search_results.json"
OUTPUT_DIR = Path("data") / "browse"

# --------------------------------------------------
# LOAD PRODUCTS
# --------------------------------------------------

if not os.path.exists(INPUT_FILE):
    print("Search results not found. Run search_nisar.py first.")
    raise SystemExit

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    products = json.load(file)

if len(products) < 10:
    print("Product 10 is not available in the search results.")
    raise SystemExit

# Select Product 10
product = products[9]

print("=" * 65)
print("DHARA | NISAR BROWSE IMAGE DOWNLOADER")
print("=" * 65)

print("Selected product:", product.get("sceneName"))

# --------------------------------------------------
# FIND BROWSE IMAGE URLS
# --------------------------------------------------

browse_urls = product.get("browse", [])

if isinstance(browse_urls, str):
    browse_urls = [browse_urls]

# Fallback: inspect additional URLs
if not browse_urls:
    additional_urls = product.get("additionalUrls", [])

    if isinstance(additional_urls, str):
        additional_urls = [additional_urls]

    browse_urls = [
        url for url in additional_urls
        if url.lower().endswith(".png")
    ]

if not browse_urls:
    print("\nNo browse image URL was found.")
    print("Available browse metadata:", product.get("browse"))
    print("Available additional URLs:", product.get("additionalUrls"))
    raise SystemExit

# Prefer geographic LATLON browse image
selected_url = next(
    (
        url for url in browse_urls
        if "LATLON" in url.upper()
    ),
    browse_urls[0]
)

filename = os.path.basename(urlparse(selected_url).path)

if not filename:
    print("Could not identify the browse image filename.")
    raise SystemExit

# --------------------------------------------------
# DOWNLOAD ONLY THE PNG
# --------------------------------------------------

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

output_path = OUTPUT_DIR / filename

if output_path.exists():
    print("\nBrowse image already exists:", output_path)
    print("No additional download needed.")
    raise SystemExit

print("\nBrowse image selected:", filename)
print("Downloading browse image...")

try:
    with requests.get(
        selected_url,
        stream=True,
        timeout=(15, 120)
    ) as response:

        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        print("Server Content-Type:", content_type)

        png_signature = b"\x89PNG\r\n\x1a\n"

        # Read the first chunk to validate the PNG signature
        chunks = response.iter_content(chunk_size=64 * 1024)
        first_chunk = next(chunks, b"")

        if not first_chunk.startswith(png_signature):
            print("\nThe downloaded file is not a valid PNG image.")
            print("Content-Type:", content_type)
            print("First bytes:", first_chunk[:20])

            if b"<html" in first_chunk.lower():
                print("The server may have returned an HTML login/error page.")

            raise SystemExit

        total_bytes = 0

        with open(output_path, "wb") as file:
            file.write(first_chunk)
            total_bytes += len(first_chunk)

            for chunk in chunks:
                if chunk:
                    file.write(chunk)
                    total_bytes += len(chunk)

    if total_bytes == 0:
        output_path.unlink(missing_ok=True)
        print("Downloaded file is empty.")
        raise SystemExit

    print("\nDOWNLOAD SUCCESSFUL")
    print("Saved to:", output_path)
    print(f"Image size: {total_bytes / (1024 * 1024):.2f} MB")

except requests.exceptions.HTTPError as error:
    output_path.unlink(missing_ok=True)
    print("\nHTTP error:", error)
    print(
        "The browse image may require authentication "
        "or the URL may be unavailable."
    )

except requests.exceptions.RequestException as error:
    output_path.unlink(missing_ok=True)
    print("\nNetwork error:", error)

except Exception as error:
    output_path.unlink(missing_ok=True)
    print("\nError:", type(error).__name__, error)
