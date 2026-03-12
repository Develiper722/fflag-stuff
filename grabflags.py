import requests
import time
import base64

TOKEN = '' 
REPO = "MaximumADHD/Roblox-Client-Tracker"
FILE_PATH = "FVariables.txt"
TARGET_VERSION = "0.604.0.6040508"
OUTPUT_FILE = "flag_dump-2.txt"

HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

def get_commits_paginated(path, target_v):
    """Loops through API pages until the target version string is found."""
    page = 1
    all_collected = []
    found = False
    
    print(f"Searching for {target_v}...")
    
    while not found:
        print(f"  Checking page {page}...")
        url = f"https://api.github.com/repos/{REPO}/commits?path={path}&per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break
            
        data = response.json()
        if not data:
            print("Reached end of history without finding version.")
            break
            
        for i, commit in enumerate(data):
            all_collected.append(commit)
            if target_v in commit['commit']['message']:
                print(f"Found {target_v} at commit {len(all_collected)}!")
                return all_collected 
        
        page += 1
        time.sleep(0.5)
        
    return None

def get_file_content(sha, path):
    url = f"https://api.github.com/repos/{REPO}/contents/{path}?ref={sha}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return base64.b64decode(response.json()['content']).decode('utf-8', errors='ignore')

def parse_flags(content):
    return set(line.strip() for line in content.splitlines() if line.strip())

def main():
    relevant_commits = get_commits_paginated(FILE_PATH, TARGET_VERSION)
    
    if not relevant_commits:
        print("Could not locate that version in history.")
        return

    relevant_commits.reverse()
    
    flag_registry = {}
    previous_flags = set()

    print(f"Processing {len(relevant_commits)} versions. This may take a while...")

    for commit in relevant_commits:
        sha = commit['sha']
        first_line = commit['commit']['message'].split('\n')[0]
        timestamp = commit['commit']['committer']['date']
        
        try:
            content = get_file_content(sha, FILE_PATH)
            current_flags = parse_flags(content)

            for flag in current_flags:
                flag_registry[flag] = "Active"

            if previous_flags:
                removed = previous_flags - current_flags
                for flag in removed:
                    if flag_registry.get(flag) == "Active":
                        flag_registry[flag] = f"Removed | Removed in version: {first_line} ({timestamp})"

            previous_flags = current_flags
            print(f" Done: {first_line}")
        except Exception as e:
            print(f" Error at {sha[:7]}: {e}")
        
        time.sleep(0.2)

    print(f"\nSaving to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w") as f:
        for flag_name in sorted(flag_registry.keys()):
            status = flag_registry[flag_name]
            f.write(f"{flag_name} | {status}\n")

    print("Finished!")

if __name__ == "__main__":
    main()