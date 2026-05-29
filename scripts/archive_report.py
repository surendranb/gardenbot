import os
import json
from datetime import datetime

LOG_FILE = "logs/agent_reasoning.log"
HISTORY_FILE = "logs/warden_history.jsonl"
MAX_HISTORY = 4

def main():
    if not os.path.exists(LOG_FILE):
        return

    with open(LOG_FILE, "r") as f:
        content = f.read().strip()

    if not content:
        return

    # Extract timestamp from content if possible, else use file mod time
    # E.g., "Audit Date: 2026-05-29 09:54 AM (Asia/Calcutta)"
    audit_date_line = next((line for line in content.split('\n') if "Audit Date:" in line), None)
    timestamp = audit_date_line.replace("Audit Date: ", "").strip() if audit_date_line else datetime.now().isoformat()

    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            for line in f:
                if line.strip():
                    history.append(json.loads(line))

    # Check if we already have this exact report
    if history and history[-1].get("report") == content:
        return

    # Add new entry
    history.append({
        "timestamp": timestamp,
        "report": content
    })

    # Keep only last MAX_HISTORY
    history = history[-MAX_HISTORY:]

    # Write back to JSONL
    with open(HISTORY_FILE, "w") as f:
        for entry in history:
            f.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    main()
