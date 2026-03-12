import json
import re

def parse_flags(file_path):
    flags = []
    pattern = re.compile(r"\[(?P<type>.*?)\]\s+(?P<name>.*?)\s+\|\s+(?P<status>.*?)(?:\s+\|\s+Removed in version:\s+(?P<version>.*?)\s+\((?P<date>.*?)\))?$")

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            match = pattern.match(line)
            if match:
                flags.append({
                    "type": match.group("type"),
                    "name": match.group("name"),
                    "status": match.group("status"),
                    "version": match.group("version") if match.group("version") else "N/A",
                    "date": match.group("date") if match.group("date") else "N/A"
                })
    return flags

flag_data = parse_flags('flag_dump-2.txt')
with open('flags.json', 'w') as f:
    json.dump(flag_data, f, indent=4)

print(f"Successfully converted {len(flag_data)} flags!")