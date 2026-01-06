import hashlib
import sys

# Constants
TARGET_HASH = "5f2940d65ca4140cc18d0878bc398955"
INPUT_VAL = "203.0.113.33"
WORDLIST_PATH = "/home/dennis/Documents/bug_bounty/lists/passwords/rockyou.txt"

def get_md5(data: str) -> str:
    """Helper function to return md5 hex digest of a string."""
    return hashlib.md5(data.encode('utf-8')).hexdigest()

def main():
    try:
        # Open the file with 'rb' (read binary) or specify encoding 
        # to handle potential non-UTF-8 characters in rockyou.txt
        with open(WORDLIST_PATH, 'r', encoding='latin-1') as file:
            for line in file:
                # Strip newline characters from the salt
                salt = line.strip()
                
                # Check md5(input + salt)
                if get_md5(INPUT_VAL + salt) == TARGET_HASH:
                    print(f"Found salt md5(input+salt): {salt}")
                    sys.exit(0)
                
                # Check md5(salt + input)
                if get_md5(salt + INPUT_VAL) == TARGET_HASH:
                    print(f"Found salt md5(salt+input): {salt}")
                    sys.exit(0)
                    
        print("FAILED")
        sys.exit(1)

    except FileNotFoundError:
        print(f"Error: Could not find file at {WORDLIST_PATH}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()