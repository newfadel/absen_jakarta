import requests
import os

def download_and_update_file():
    url = "https://raw.githubusercontent.com/newfadel/absen_jakarta/refs/heads/main/absen.py"
    local_file = "absen.py"
    
    try:
        # Download file from URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Write content to absen.py, replacing if it exists
        with open(local_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Successfully updated {local_file} from {url}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {str(e)}")
    except IOError as e:
        print(f"Error writing to file: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    download_and_update_file()