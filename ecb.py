import requests
import base64
import json
from urllib.parse import unquote, quote

URL = "http://natas28.natas.labs.overthewire.org/index.php"
AUTH = ('natas28', '1JNwQM1Oi6J6j1k49Xyw7ZN6pXMQInVj')

def get_encrypted_query(payload):
    session = requests.Session()
    session.auth = AUTH
    response = session.post(URL, data={'query': payload})
    encrypted_b64 = response.url.split('query=')[1]
    raw_bytes = base64.b64decode(unquote(encrypted_b64))
    return raw_bytes

def analyze_blocks(max_input_len=10):
    results = {}

    for i in range(1, max_input_len + 1):
        payload = "A" * i
        ciphertext = get_encrypted_query(payload)
        blocks = [ciphertext[j:j+16].hex() for j in range(0, len(ciphertext), 16)]
        
        results[f"input_len_{i}"] = {
            "payload": payload,
            "raw_hex": ciphertext.hex(),
            "blocks": blocks,
            "block_count": len(blocks)
        }
        print(f"Processed length {i}: {len(blocks)} blocks found.")

    with open("natas28_analysis.json", "w") as f:
        json.dump(results, f, indent=4)
    
    print("\nAnalysis complete. Data saved to 'natas28_analysis.json'.")

if __name__ == "__main__":
    analyze_blocks(20)