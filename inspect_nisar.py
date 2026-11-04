
import json
import os

INPUT_FILE = "nisar_search_results.json"


def format_size(size_bytes):
    """Convert bytes into readable MB and GB."""
    size_mb = size_bytes / (1024 * 1024)
    size_gb = size_bytes / (1024 * 1024 * 1024)

    if size_gb >= 1:
        return f"{size_gb:.2f} GB ({size_mb:.2f} MB)"

    return f"{size_mb:.2f} MB"


# --------------------------------------------------
# LOAD SEARCH RESULTS
# --------------------------------------------------

if not os.path.exists(INPUT_FILE):
    print("Search results file not found.")
    print("Run search_nisar.py first.")
    raise SystemExit

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    products = json.load(file)

print("=" * 70)
print("DHARA | NISAR PRODUCT METADATA INSPECTOR")
print("=" * 70)

if not products:
    print("No products available.")
    raise SystemExit


# --------------------------------------------------
# PRODUCT SIZE COLLECTION
# --------------------------------------------------

hdf5_products = []
png_products = []


# --------------------------------------------------
# INSPECT EACH PRODUCT
# --------------------------------------------------

for index, product in enumerate(products, start=1):

    print(f"\nPRODUCT {index}")
    print("-" * 70)

    name = product.get("sceneName", "Unknown")

    print("Product Name:", name)
    print("Acquisition Date:", product.get("startTime", "Unknown"))
    print("Processing Level:", product.get("processingLevel", "Unknown"))
    print("Flight Direction:", product.get("flightDirection", "Unknown"))
    print("File Name:", product.get("fileName", "Not available"))
    print("Download URL:", product.get("url", "Not available"))

    # ASF associated file metadata
    associated_files = product.get("bytes", {})

    if isinstance(associated_files, dict) and associated_files:

        print("\nASSOCIATED FILES")
        print("-" * 50)

        for filename, details in associated_files.items():

            if not isinstance(details, dict):
                continue

            size_bytes = details.get("bytes")
            file_format = details.get("format", "Unknown")

            if size_bytes is None:
                continue

            try:
                size_bytes = float(size_bytes)
            except (ValueError, TypeError):
                continue

            print("\nFile:", filename)
            print("Format:", file_format)
            print("Size:", format_size(size_bytes))

            file_info = {
                "product": name,
                "filename": filename,
                "size_bytes": size_bytes,
                "url": details.get("url")
            }

            extension = os.path.splitext(filename)[1].lower()

            if extension == ".h5":
                hdf5_products.append(file_info)

            elif extension == ".png":
                png_products.append(file_info)

    else:
        print("\nAssociated file sizes are unavailable.")

    print("\nAvailable metadata fields:")
    print(", ".join(sorted(product.keys())))


# --------------------------------------------------
# HDF5 PRODUCT SUMMARY
# --------------------------------------------------

print("\n" + "=" * 70)
print("HDF5 SATELLITE DATA SUMMARY")
print("=" * 70)

if hdf5_products:

    hdf5_products.sort(key=lambda item: item["size_bytes"])

    smallest_hdf5 = hdf5_products[0]

    print("HDF5 files found:", len(hdf5_products))

    print("\nSmallest HDF5 product:")
    print("Product:", smallest_hdf5["product"])
    print("File:", smallest_hdf5["filename"])
    print("Size:", format_size(smallest_hdf5["size_bytes"]))

    print("\nHDF5 files sorted by size:")

    for item in hdf5_products:
        print(
            f"{format_size(item['size_bytes']):>20} | "
            f"{item['filename']}"
        )

else:
    print("No HDF5 file sizes found.")


# --------------------------------------------------
# BROWSE IMAGE SUMMARY
# --------------------------------------------------

print("\n" + "=" * 70)
print("BROWSE PNG IMAGE SUMMARY")
print("=" * 70)

if png_products:

    png_products.sort(key=lambda item: item["size_bytes"])

    smallest_png = png_products[0]

    print("PNG files found:", len(png_products))

    print("\nSmallest PNG image:")
    print("Product:", smallest_png["product"])
    print("File:", smallest_png["filename"])
    print("Size:", format_size(smallest_png["size_bytes"]))

else:
    print("No PNG file sizes found.")


# --------------------------------------------------
# FINAL REPORT
# --------------------------------------------------

print("\n" + "=" * 70)
print("DHARA | INSPECTION COMPLETED")
print("=" * 70)

print("Products inspected:", len(products))
print("HDF5 files found:", len(hdf5_products))
print("PNG files found:", len(png_products))

print("\nNo satellite files were downloaded.")
print("Next step: Inspect the smallest browse PNG image.")
