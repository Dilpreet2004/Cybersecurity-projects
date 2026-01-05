import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

valid_code = [200,204,301,302,400,401,403,405]
file_path = "Cybersecurity/common.txt"
url = "https://dda5d8221c3c530b7628107d566ded0f.ctf.hacker101.com/api/v1"
dirb = []

def check_url(directory):
    directory = directory.lstrip('/').strip()
    target_url = f"{url.rstrip('/')}/{directory}/"
    try:
        response = requests.get(target_url)
        if response.status_code in valid_code:
            tqdm.write(f"Directory: {target_url} [Status: {response.status_code}]")
            return directory
    except requests.RequestException:
        pass
    return None

print("Directory busting...")

try:
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with ThreadPoolExecutor(max_workers=45) as executor:
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
        print(f"/{directory}")
else:
    print("\nNo directories found")