import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

file_path = "Cybersecurity/directory-list-2.3-small.txt"
url = "https://dda5d8221c3c530b7628107d566ded0f.ctf.hacker101.com/api/v1"
dirb = []

def check_url(directory):
    directory = directory.lstrip('/').strip()
    target_url = f"{url.rstrip('/')}/{directory}/"
    try:
        response = requests.get(target_url, timeout=5)
        if response.status_code == 200 or response.status_code == 403:
            tqdm.write(f"Directory: {directory} [Status: {response.status_code}]")
            return directory
    except requests.RequestException:
        pass
    return None

print("Directory busting...")

try:
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with ThreadPoolExecutor(max_workers=40) as executor:
        results = list(tqdm(executor.map(check_url, lines), total=len(lines), unit="url"))

    dirb = [r for r in results if r is not None]

except FileNotFoundError:
    print("file not found. Please check the file path")
    exit()
except KeyboardInterrupt:
    print("\nProgram terminated by user")
    exit()
except Exception as e:
    print(f"An error occurred: {e}")
    exit()

if dirb:
    print("\nFollowing directories found:")
    for directory in dirb:
        print(directory)
else:
    print("\nNo directories found")