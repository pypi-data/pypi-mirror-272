import os
import requests
import time

WARNING_COLOR = '\033[93m'  # Yellow color for warning
RESET_COLOR = '\033[0m'      # Reset color

def convert_bytes_to_mb(bytes_size):
    return bytes_size / (1024 * 1024)

def seqdownload(base_url, start_index, end_index, custom_iterator, file_extension, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    if not file_extension:
        # Print warning message if file extension is empty
        print(f"{WARNING_COLOR}WARNING: File extension is empty. Pausing at first trying / first download.{RESET_COLOR}")
        input("Press Enter to continue...")

    total_downloaded_files = 0
    total_downloaded_size = 0

    for i in range(start_index, end_index + 1):
        if custom_iterator:
            url = f"{base_url}/{custom_iterator}_{i}.{file_extension}"
        else:
            url = f"{base_url}/{i}.{file_extension}"
        
        filename = os.path.join(output_folder, f"{custom_iterator}_{i}.{file_extension}" if custom_iterator else f"{i}.{file_extension}")

        # Download the image
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            total_size_mb = convert_bytes_to_mb(total_size)
            downloaded_size = 0
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        downloaded_size_mb = convert_bytes_to_mb(downloaded_size)
                        print(f"Downloading {filename} {downloaded_size_mb:.2f}/{total_size_mb:.2f} MB", end='\r')
            
            # Increment counters for downloaded files and total size
            total_downloaded_files += 1
            total_downloaded_size += total_size

            print(f"\nDownloaded {filename}")  # Add a newline before printing the filename
        else:
            print(f"Failed to download: {url}")

    # Print total downloaded files and total size
    total_downloaded_size_mb = convert_bytes_to_mb(total_downloaded_size)
    print(f"Total download {total_downloaded_files} files ({total_downloaded_size_mb:.2f} MB)")
