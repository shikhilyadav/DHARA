
import json
from pathlib import Path

INPUT_FILE = Path("nisar_search_results.json")

print("=" * 65)
print("DHARA | NISAR HDF5 PRODUCT INFORMATION")
print("=" * 65)

if not INPUT_FILE.exists():
    print("Search results file not found.")
    raise SystemExit

with INPUT_FILE.open("r", encoding="utf-8") as file:
    products = json.load(file)

if len(products) < 10:
    print("Product 10 is not available.")
    raise SystemExit

product = products[9]

print("\nPRODUCT:")
print(product.get("sceneName", "Not available"))

print("\nAVAILABLE METADATA FIELDS:")

for key in product.keys():
    print("-", key)

print("\nHDF5 FILE INFORMATION:")

associated_files = product.get("bytes", {})

if isinstance(associated_files, dict):

    for filename, details in associated_files.items():

        if filename.lower().endswith(".h5"):

            print("\nFilename:", filename)

            if isinstance(details, dict):
                size = details.get("bytes", 0)

                print("Size:", size, "bytes")
                print("Size in GiB:", round(size / (1024 ** 3), 3))

            else:
                print("File details:", details)

print("\nPRODUCT DOWNLOAD URL:")
print(product.get("url", "Not available"))

print("\nS3 URL INFORMATION:")

s3_urls = product.get("s3Urls", [])

if isinstance(s3_urls, list):
    for url in s3_urls:
        print(url)
else:
    print(s3_urls)

print("\nINSPECTION COMPLETE")
