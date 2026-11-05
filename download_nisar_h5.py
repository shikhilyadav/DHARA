
import json
import getpass
from pathlib import Path

import requests
import asf_search as asf
from requests.auth import HTTPBasicAuth

# ---------------- CONFIGURATION ----------------

PRODUCT_INDEX = 9
CHUNK_SIZE = 1024 * 1024  # 1 MB

BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "nisar_search_results.json"
DOWNLOAD_DIR = BASE_DIR / "data" / "raw"

TOKEN_URL = (
    "https://urs.earthdata.nasa.gov/"
    "api/users/find_or_create_token"
)


def main():

    # 1. Read NISAR product information
    if not JSON_FILE.exists():
        print("Error: NISAR search results file not found.")
        return

    with open(JSON_FILE, "r", encoding="utf-8") as file:
        products = json.load(file)

    if PRODUCT_INDEX >= len(products):
        print("Error: Selected product not found.")
        return

    product = products[PRODUCT_INDEX]

    filename = product.get("fileName")
    download_url = product.get("url")

    if not filename or not download_url:
        print("Error: Product filename or URL missing.")
        return

    file_info = product.get("bytes", {})
    expected_size = file_info.get(filename, {}).get("bytes")

    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    output_file = DOWNLOAD_DIR / filename
    partial_file = DOWNLOAD_DIR / (filename + ".part")

    if output_file.exists():
        print("File already exists:", output_file)
        return

    print("\nDHARA - NISAR HDF5 Downloader")
    print("--------------------------------")
    print("Product:", filename)

    # 2. Get Earthdata credentials privately
    username = input("NASA Earthdata username: ")
    password = getpass.getpass("NASA Earthdata password: ")

    token = None
    session = None

    try:
        # 3. Obtain an Earthdata access token
        print("\nAuthenticating with NASA Earthdata...")

        response = requests.post(
            TOKEN_URL,
            auth=HTTPBasicAuth(username, password),
            timeout=30
        )

        response.raise_for_status()

        token_data = response.json()
        token = token_data.get("access_token")

        if not token:
            raise ValueError(
                "NASA response did not contain an access token."
            )

        password = None

        print("Earthdata credentials accepted.")

        # 4. Authenticate ASF session using the token
        print("Authenticating ASF download session...")

        session = asf.ASFSession()
        session.auth_with_token(token)

        print("ASF authentication successful!")
        print("\nStarting NISAR download...\n")

        # 5. Stream the HDF5 file in small chunks
        downloaded = 0

        with session.get(
            download_url,
            stream=True,
            timeout=(30, 180)
        ) as download_response:

            download_response.raise_for_status()

            with open(partial_file, "wb") as file:

                for chunk in download_response.iter_content(
                    chunk_size=CHUNK_SIZE
                ):

                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)

                        if downloaded % (100 * CHUNK_SIZE) < CHUNK_SIZE:
                            downloaded_mb = downloaded / (1024 ** 2)

                            if expected_size:
                                percentage = (
                                    downloaded / expected_size
                                ) * 100

                                print(
                                    f"Downloaded: {downloaded_mb:.1f} MB "
                                    f"({percentage:.1f}%)"
                                )
                            else:
                                print(
                                    f"Downloaded: {downloaded_mb:.1f} MB"
                                )

        # 6. Verify downloaded file size
        if expected_size and downloaded != expected_size:
            raise ValueError(
                f"File size mismatch. Expected {expected_size} bytes, "
                f"received {downloaded} bytes."
            )

        # 7. Rename partial file after successful verification
        partial_file.replace(output_file)

        print("\n--------------------------------")
        print("NISAR DOWNLOAD SUCCESSFUL!")
        print("--------------------------------")
        print("Saved location:", output_file)
        print(
            f"File size: {downloaded / (1024 ** 3):.3f} GiB"
        )

    except Exception as error:

        print("\nDOWNLOAD FAILED")
        print("Reason:", error)

        if partial_file.exists():
            print("Incomplete file retained:", partial_file)
            print("Do not use it for scientific analysis.")

    finally:
        password = None
        token = None

        if session is not None:
            session.close()


if __name__ == "__main__":
    main()
