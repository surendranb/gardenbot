import os
import sys
import json
from datetime import datetime

LOG_FILE = "logs/agent_reasoning.log"
HISTORY_FILE = "logs/warden_history.jsonl"
DASHBOARD_HISTORY = "src/docs/data/warden_history.jsonl"
MAX_HISTORY = 4

def main():
    if len(sys.argv) > 1:
        content = sys.argv[1].strip()
    else:
        if not os.path.exists(LOG_FILE):
            return
        with open(LOG_FILE, "r") as f:
            content = f.read().strip()

    if not content:
        return

    # Extract timestamp from content if possible
    audit_date_line = next((line for line in content.split('\n') if "Audit Date:" in line), None)
    timestamp = audit_date_line.replace("Audit Date: ", "").strip() if audit_date_line else datetime.now().isoformat()

    def update_history_file(filepath):
        history = []
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
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
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, "w") as f:
            for entry in history:
                f.write(json.dumps(entry) + "\n")

    update_history_file(HISTORY_FILE)
    update_history_file(DASHBOARD_HISTORY)
    
    # Also overwrite the current log file so temporal insights script can pick it up if it uses it directly
    os.makedirs(os.path.dirname(os.path.abspath(LOG_FILE)), exist_ok=True)
    with open(LOG_FILE, "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()
