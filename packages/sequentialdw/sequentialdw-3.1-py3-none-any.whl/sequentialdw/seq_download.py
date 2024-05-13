import os
import requests
import time

WARNING_COLOR = '\033[93m'  # Yellow color for warning
RESET_COLOR = '\033[0m'      # Reset color

def convert_bytes_to_mb(bytes_size):
    return bytes_size / (1024 * 1024)
def seqdownload(base_url, start_index, end_index, custom_iterator, file_extension, output_folder, mode):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    if not file_extension:
        # Print warning message if file extension is empty
        print(f"{WARNING_COLOR}WARNING: File extension is empty. Pausing at first trying / first download.{RESET_COLOR}")
        input("Press Enter to continue...")

    total_downloaded_files = 0
    total_downloaded_size = 0
    total_skipped_files = 0
    fileTotal = end_index - start_index + 1

    print(f"\nStart to downloading {fileTotal} .{file_extension} files in .\{output_folder}")

    for i in range(start_index, end_index + 1):
        if custom_iterator:
            url = f"{base_url}/{custom_iterator}_{i}.{file_extension}"
        else:
            url = f"{base_url}/{i}.{file_extension}"
        
        filename = os.path.join(output_folder, f"{custom_iterator}_{i}.{file_extension}" if custom_iterator else f"{i}.{file_extension}")

        # Check if the file already exists
        if os.path.exists(filename):
            if mode == 1:
                # Mode 1: Replace existing files
                os.remove(filename)
            elif mode == 2:
                # Mode 2: Skip existing files and continue to the next file
                total_skipped_files += 1
                print(f"File {filename} already exists. Skipping...")
                continue

        try:
            start_time = time()
            response = requests.get(url, stream=True, timeout=3)  # Timeout set to 3 seconds

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
                
                total_downloaded_files += 1
                total_downloaded_size += total_size

                print(f"\nDownloaded {filename}")
            else:
                print(f"Failed to download: {url}")

            end_time = time()
            elapsed_time = end_time - start_time

            if elapsed_time >= 3:
                print("Timeout reached. Skipping to the next file.")

        except requests.exceptions.Timeout:
            print("Timeout occurred. Skipping to the next file.")
        
        except Exception as e:
            print(f"Error occurred while downloading: {e}")

    total_downloaded_size_mb = convert_bytes_to_mb(total_downloaded_size)
    print(f"There {total_skipped_files} skipped file due duplicated")
    print(f"Total download {total_downloaded_files} files ({total_downloaded_size_mb:.2f} MB)")
