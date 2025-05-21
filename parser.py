import re
import json

def redact_content(content):
    content = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}:\d+\b', '[REDACTED_IP]', content)
    content = re.sub(r'\(\[.*?\]-?\d+\.?\d*,\s*-?\d+\.?\d*,\s*-?\d+\.?\d*\)', '([REDACTED_COORDS])', content)
    return content

def parse_minecraft_log(file_path):
    log_entries = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(r"\[(.*?)\] \[(.*?)\]: (.*)", line)
            if not match:
                continue

            time, raw_type, content = match.groups()
            clean_type_match = re.match(r"([^\[/#]+)", raw_type)
            type_cleaned = clean_type_match.group(1).strip() if clean_type_match else raw_type.strip()
            content = redact_content(content)

            log_entries.append({
                "time": time.strip(),
                "type": type_cleaned,
                "content": content.strip()
            })

    #print(json.dumps(log_entries, indent=4))
    return log_entries
